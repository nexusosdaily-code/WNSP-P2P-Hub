"""
Messaging Payment Adapter
=========================

Atomic payment integration for wavelength messaging system.
Ensures payment and message delivery happen together or not at all.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import hashlib
import time
import os
from datetime import datetime


class PaymentAdapter(ABC):
    """
    Abstract interface for payment processing in messaging system.
    
    Implementations must provide atomic payment semantics:
    - authorize() checks if payment can proceed
    - commit() executes the payment
    - rollback() attempts to reverse payment (if possible)
    """
    
    @abstractmethod
    def authorize(self, sender: str, cost_nxt: float) -> tuple[bool, Optional[str]]:
        """
        Pre-flight check before payment.
        
        Returns:
            (success: bool, error_message: Optional[str])
        """
        pass
    
    @abstractmethod
    def commit(
        self, 
        sender: str, 
        recipient: str, 
        cost_nxt: float, 
        tx_metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute the payment transaction.
        
        Args:
            sender: Sender address
            recipient: Recipient address  
            cost_nxt: Amount to pay
            tx_metadata: Message metadata for idempotency key generation
            
        Returns:
            Transaction result dictionary
            
        Raises:
            Exception if payment fails
        """
        pass
    
    @abstractmethod
    def rollback(self) -> bool:
        """
        Attempt to rollback last payment (if possible).
        
        Returns:
            True if rollback succeeded, False otherwise
        """
        pass


class WalletPaymentAdapter(PaymentAdapter):
    """
    Wallet-backed payment adapter for real NXT transactions.
    
    Integrates NexusNativeWallet with messaging system, ensuring:
    - Deterministic idempotency keys for safe retries
    - Automatic account provisioning
    - Atomic payment + message delivery
    """
    
    def __init__(self, wallet, token_system, password: str, validator_pool_password: Optional[str] = None):
        """
        Initialize wallet payment adapter.
        
        Args:
            wallet: NexusNativeWallet instance
            token_system: NativeTokenSystem instance
            password: Wallet password for transactions
            validator_pool_password: Optional VALIDATOR_POOL password for refunds.
                                    If not provided, reads from VALIDATOR_POOL_PASSWORD env var.
        
        Raises:
            ValueError: If VALIDATOR_POOL password is not available
        """
        self.wallet = wallet
        self.token_system = token_system
        self.password = password
        
        # Load VALIDATOR_POOL password from parameter or environment (REQUIRED for production)
        self.validator_pool_password = validator_pool_password or os.getenv('VALIDATOR_POOL_PASSWORD')
        
        if not self.validator_pool_password:
            raise ValueError(
                "VALIDATOR_POOL_PASSWORD must be set for atomic messaging safety. "
                "Set via environment variable or constructor parameter. "
                "This credential is required to execute compensating refunds during rollback."
            )
        
        self.last_payment_tx = None
        self.last_token_tx = None  # Track token_system transaction for rollback
        self.last_reward_txs = []  # Track validator reward transactions for rollback
    
    def authorize(self, sender: str, cost_nxt: float) -> tuple[bool, Optional[str]]:
        """
        Check if payment can proceed.
        
        Validates:
        - Sender has sufficient balance
        - VALIDATOR_POOL account exists
        - Recipient account exists in token_system
        """
        try:
            # Check sender balance
            balance_data = self.wallet.get_balance(sender)
            if balance_data['balance_nxt'] < cost_nxt:
                return False, f"Insufficient balance: {balance_data['balance_nxt']:.4f} NXT < {cost_nxt:.4f} NXT required"
            
            # Ensure VALIDATOR_POOL exists
            try:
                self.wallet.get_balance("VALIDATOR_POOL")
            except:
                # Create VALIDATOR_POOL if needed using configured password
                try:
                    self.wallet.create_account("VALIDATOR_POOL", self.validator_pool_password)
                except Exception as e:
                    # Account might already exist, that's OK
                    pass
            
            return True, None
            
        except Exception as e:
            return False, f"Authorization failed: {str(e)}"
    
    def commit(
        self, 
        sender: str, 
        recipient: str, 
        cost_nxt: float, 
        tx_metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute wallet payment with deterministic idempotency.
        
        Generates idempotency key from stable message metadata to ensure:
        - Retries don't double-charge
        - Same message content = same idempotency key
        
        CRITICAL: Also mirrors transaction to token_system for validator rewards.
        """
        # Ensure recipient has account in token_system (for message delivery)
        if self.token_system.get_account(recipient) is None:
            self.token_system.create_account(recipient, initial_balance=0)
        
        # Ensure VALIDATOR_POOL has account in token_system (for rewards)
        if self.token_system.get_account("VALIDATOR_POOL") is None:
            self.token_system.create_account("VALIDATOR_POOL", initial_balance=0)
        
        # Generate deterministic idempotency key from message metadata
        # This ensures retries use the same key and don't double-charge
        idem_components = [
            sender,
            recipient,
            tx_metadata.get('content_hash', ''),
            tx_metadata.get('spectral_region', ''),
            tx_metadata.get('modulation_type', '')
        ]
        idem_data = '|'.join(str(c) for c in idem_components)
        idempotency_key = hashlib.sha256(idem_data.encode()).hexdigest()[:32]
        
        # ATOMIC SEQUENCE: Reversible operations FIRST, irreversible LAST
        
        # STEP 1: Execute token_system transfer FIRST (reversible if later steps fail)
        cost_units = int(cost_nxt * 100)  # Convert NXT to units (1 NXT = 100 units)
        
        tx = self.token_system.transfer(
            sender,
            "VALIDATOR_POOL",
            cost_units,
            fee=0  # No additional fee for messaging payment
        )
        
        if not tx:
            # Token system transfer failed - safe to fail, no wallet debit yet
            raise Exception(f"Token system transfer failed for {sender} → VALIDATOR_POOL ({cost_nxt} NXT)")
        
        # STEP 2: Execute wallet payment LAST (irreversible blockchain transaction)
        try:
            payment_result = self.wallet.send_nxt(
                from_address=sender,
                to_address="VALIDATOR_POOL",
                amount=cost_nxt,
                password=self.password,
                idempotency_key=idempotency_key
            )
            
            # Both succeeded - store for potential compensating refund
            self.last_payment_tx = payment_result
            self.last_token_tx = tx
            # Clear any previous reward tracking (new transaction)
            self.last_reward_txs = []
            
            return payment_result
            
        except Exception as e:
            # Wallet payment failed - ROLLBACK token_system transfer
            # Reverse the token_system transfer by transferring back
            self.token_system.transfer(
                "VALIDATOR_POOL",
                sender,
                cost_units,
                fee=0
            )
            raise Exception(f"Wallet payment failed (token_system transfer rolled back): {str(e)}")
    
    def record_reward_distribution(self, validator_id: str, amount_units: int):
        """
        Record a validator reward distribution for potential rollback.
        
        Args:
            validator_id: Validator account ID
            amount_units: Reward amount in units
        """
        self.last_reward_txs.append({
            'validator_id': validator_id,
            'amount_units': amount_units
        })
    
    def rollback(self) -> bool:
        """
        Full atomic rollback with compensating refund.
        
        ATOMIC SEQUENCE (Reversible → Irreversible):
        1. Reverse ALL validator reward distributions FIRST
        2. Reverse sender→VALIDATOR_POOL token_system transfer
        3. Send compensating wallet refund (blockchain transaction)
        
        Returns:
            True if ALL reversals succeeded (full atomic rollback)
            False if rollback failed (manual intervention required)
        """
        if not self.last_payment_tx or not self.last_token_tx:
            return False
        
        try:
            # Extract sender and amount from last transaction
            sender = self.last_payment_tx.get('from_address', self.last_payment_tx.get('from'))
            amount = self.last_payment_tx.get('amount', 0)
            
            if not sender or amount <= 0:
                return False
            
            # STEP 1: Reverse ALL validator reward distributions FIRST
            # This restores VALIDATOR_POOL balance before we try to refund sender
            failed_reversals = []
            for reward_tx in reversed(self.last_reward_txs):  # Reverse in LIFO order
                validator_id = reward_tx['validator_id']
                amount_units = reward_tx['amount_units']
                
                # Reverse reward: validator → VALIDATOR_POOL
                reverse_reward_tx = self.token_system.transfer(
                    validator_id,
                    "VALIDATOR_POOL",
                    amount_units,
                    fee=0
                )
                
                if not reverse_reward_tx:
                    failed_reversals.append(validator_id)
                    print(f"ERROR: Failed to reverse reward for {validator_id}")
            
            # If ANY reward reversal failed, abort refund attempt
            if failed_reversals:
                print(f"CRITICAL: Cannot refund sender - {len(failed_reversals)} reward reversals failed")
                print(f"  Failed validators: {failed_reversals}")
                print(f"  PRESERVING STATE: Transaction state preserved for manual recovery")
                # DO NOT CLEAR STATE - preserve for manual recovery
                return False
            
            # STEP 2: Reverse sender→VALIDATOR_POOL token_system transfer
            cost_units = int(amount * 100)
            reversed_tx = self.token_system.transfer(
                "VALIDATOR_POOL",
                sender,
                cost_units,
                fee=0
            )
            
            if not reversed_tx:
                print(f"ERROR: Token system rollback failed for {sender}")
                print(f"  PRESERVING STATE: Transaction state preserved for manual recovery")
                # DO NOT CLEAR STATE - preserve for manual recovery
                return False
            
            # STEP 3: Send compensating wallet refund (IRREVERSIBLE blockchain transaction)
            # Try to use system VALIDATOR_POOL password for authorized refund
            try:
                refund_result = self.wallet.send_nxt(
                    from_address="VALIDATOR_POOL",
                    to_address=sender,
                    amount=amount,
                    password=self.validator_pool_password,  # Configured system password
                    idempotency_key=f"refund_{self.last_payment_tx.get('tx_hash', hashlib.sha256(f'{sender}{amount}{time.time()}'.encode()).hexdigest()[:16])}"
                )
                
                print(f"✅ FULL ROLLBACK: Rewards reversed + token system reversed + wallet refund succeeded")
                print(f"  Sender: {sender}, Amount: {amount} NXT")
                print(f"  Rewards reversed: {len(self.last_reward_txs)} validators")
                print(f"  Refund TX: {refund_result.get('tx_hash', 'N/A')}")
                
                # Clear state after successful rollback
                self.last_reward_txs = []
                self.last_payment_tx = None
                self.last_token_tx = None
                
                return True  # Full rollback succeeded
                
            except Exception as wallet_error:
                # Wallet refund failed - token_system and rewards already reversed
                # This is PARTIAL SUCCESS: token_system is consistent but wallet refund failed
                print(f"PARTIAL ROLLBACK: Token system reversed, wallet refund failed")
                print(f"  Sender: {sender}, Amount: {amount} NXT")
                print(f"  Error: {str(wallet_error)}")
                print(f"  Possible reason: VALIDATOR_POOL password mismatch or insufficient balance")
                print(f"  Manual wallet refund required")
                print(f"  PRESERVING STATE: Transaction state preserved for manual recovery")
                # DO NOT CLEAR STATE - preserve for manual recovery/retry
                
                return False
            
        except Exception as e:
            # General rollback failed - preserve state for recovery
            print(f"Rollback failed: {str(e)}")
            print(f"  PRESERVING STATE: Transaction state preserved for manual recovery")
            # DO NOT CLEAR STATE - preserve for manual recovery
            return False


class DemoPaymentAdapter(PaymentAdapter):
    """
    Demo payment adapter for testing with in-memory token system.
    
    Used for demo accounts (alice, bob, charlie).
    No real wallet transactions, just in-memory balance updates.
    """
    
    def __init__(self, token_system):
        self.token_system = token_system
        self.last_debit = None
    
    def authorize(self, sender: str, cost_nxt: float) -> tuple[bool, Optional[str]]:
        """Check balance in token_system."""
        account = self.token_system.get_account(sender)
        if not account:
            return False, f"Account {sender} not found"
        
        balance_nxt = account.get_balance_nxt()
        if balance_nxt < cost_nxt:
            return False, f"Insufficient balance: {balance_nxt:.4f} NXT < {cost_nxt:.4f} NXT"
        
        return True, None
    
    def commit(
        self, 
        sender: str, 
        recipient: str, 
        cost_nxt: float, 
        tx_metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Deduct from in-memory token system."""
        # This happens inside messaging_system.send_message() already
        # Just record for rollback
        self.last_debit = {
            'sender': sender,
            'amount': cost_nxt
        }
        
        return {
            'success': True,
            'tx_hash': f"demo_{sender}_{datetime.now().timestamp()}",
            'from': sender,
            'to': 'VALIDATOR_POOL',
            'amount': cost_nxt
        }
    
    def rollback(self) -> bool:
        """
        Rollback in-memory debit.
        
        Returns credits to sender account.
        """
        if self.last_debit:
            account = self.token_system.get_account(self.last_debit['sender'])
            if account:
                # Refund the amount
                cost_units = int(self.last_debit['amount'] * 100)
                account.balance += cost_units
                return True
        
        return False
