"""
Native Payment Token System for NexusOS Layer 1 Blockchain

NexusToken (NXT): The native currency powering the entire ecosystem

**Bitcoin-Style Tokenomics:**
- Total Supply: 1,000,000 NXT (fixed, like Bitcoin's 21M BTC)
- Denomination: 100,000,000 units = 1 NXT (like 100M satoshis = 1 BTC)
- Total Units: 100 trillion units (1M NXT × 100M units)
- Smallest Unit: 1 unit = 0.00000001 NXT

**Economic Model:**
- Deflationary: Tokens burned for messaging activities (NOT fixed 4-year halving)
- Issuance: AI-controlled validator rewards (NOT predetermined mining schedule)
- Sustainability: Dynamic burn reduction + annual burn caps for 100+ year lifespan

**Use Cases:**
- Validator rewards and staking
- Messaging payments (WNSP protocol)
- DEX trading and liquidity
- Transaction fees
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
import time
import hashlib

# Orbital Transition Engine - Physics-based token flow
from orbital_transition_engine import (
    orbital_engine, 
    TransitionType as OrbitalTransitionType,
    OrbitalTransition
)


class TransactionType(Enum):
    """Types of token transactions"""
    TRANSFER = "transfer"
    BURN = "burn"
    MINT = "mint"
    REWARD = "reward"
    FEE = "fee"
    MESSAGE_PAYMENT = "message_payment"
    LINK_SHARE_PAYMENT = "link_share_payment"
    VIDEO_SHARE_PAYMENT = "video_share_payment"


@dataclass
class TokenTransaction:
    """
    Represents a token transaction on NexusOS blockchain.
    
    All amounts in integer units (100M units = 1 NXT, Bitcoin-style).
    """
    tx_id: str
    tx_type: TransactionType
    from_address: str
    to_address: str
    amount: int  # In units (100M units = 1 NXT)
    fee: int = 0  # In units
    timestamp: float = field(default_factory=time.time)
    data: dict = field(default_factory=dict)
    signature: str = ""
    
    def compute_hash(self) -> str:
        """Compute transaction hash"""
        tx_data = f"{self.tx_id}{self.tx_type.value}{self.from_address}{self.to_address}{self.amount}{self.fee}{self.timestamp}"
        return hashlib.sha256(tx_data.encode()).hexdigest()


@dataclass
class Account:
    """
    Token account for NexusOS blockchain.
    
    Balances stored in integer units (100M units = 1 NXT, like Bitcoin satoshis).
    """
    address: str
    balance: int = 0  # In units (100M units = 1 NXT)
    nonce: int = 0
    created_at: float = field(default_factory=time.time)
    
    def get_balance_nxt(self) -> float:
        """Get balance in NXT (human-readable)"""
        return self.balance / 100_000_000.0  # 100M units per NXT
    
    def has_sufficient_balance(self, amount: int) -> bool:
        """Check if account has sufficient balance"""
        return self.balance >= amount


class NativeTokenSystem:
    """
    Native Token System for NexusOS
    
    Token Economics:
    - Total Supply: 1,000,000 NXT (100,000,000 units)
    - Circulating Supply: Total - Burned
    - Deflationary: Tokens burned for messaging activities
    - Inflationary: Block rewards for validators (controlled rate)
    """
    
    # Token constants (Bitcoin model: 21M BTC × 100M satoshis)
    # NexusOS: 1M NXT × 100M units = 100 trillion total units
    UNITS_PER_NXT = 100_000_000  # 100 million units per NXT (like satoshis)
    TOTAL_SUPPLY = 100_000_000_000_000  # 100 trillion units = 1M NXT
    GENESIS_SUPPLY = 50_000_000_000_000  # 50 trillion units = 500K NXT
    VALIDATOR_RESERVE = 30_000_000_000_000  # 30 trillion units = 300K NXT
    ECOSYSTEM_RESERVE = 20_000_000_000_000  # 20 trillion units = 200K NXT
    
    # DEPRECATED: Old "burn" rates (kept for backwards compatibility)
    # Now replaced by physics-based orbital transitions (n1 → n2 energy gaps)
    MESSAGE_BURN_RATE = 5_700  # 5,700 units = 0.000057 NXT per message (LEGACY)
    LINK_SHARE_BURN_RATE = 2_850  # 2,850 units = 0.0000285 NXT per link (LEGACY)
    VIDEO_SHARE_BURN_RATE = 11_400  # 11,400 units = 0.000114 NXT per video (LEGACY)
    
    # NEW: Orbital transition-based pricing using Rydberg formula
    # ΔE = 13.6 eV × Z² × (1/n₁² - 1/n₂²)
    # Tokens flow into TRANSITION_RESERVE instead of being destroyed
    USE_ORBITAL_TRANSITIONS = True  # Enable physics-based transitions
    
    # Transaction fees
    BASE_TRANSFER_FEE = 1_000  # 1,000 units = 0.00001 NXT per transfer
    
    # Economic balancing parameters (Bitcoin-adapted for messaging burns)
    ENABLE_DYNAMIC_BURNS = True  # Auto-reduce burns as supply decreases (sqrt dampening)
    ENABLE_VALIDATOR_INFLATION = True  # AI-controlled validator rewards from VALIDATOR_RESERVE
    VALIDATOR_INFLATION_RATE = 0.02  # 2% annual (halves every 4 years, Bitcoin-style)
    MAX_ANNUAL_BURN_PCT = 5.0  # Cap burns at 5% of circulating supply per year
    
    def __init__(self):
        self.accounts: Dict[str, Account] = {}
        self.transactions: List[TokenTransaction] = []
        self.total_burned: int = 0
        self.total_minted: int = self.TOTAL_SUPPLY  # All tokens minted at genesis
        self.tx_counter: int = 0
        
        # Genesis account
        self._create_genesis_accounts()
    
    def _create_genesis_accounts(self):
        """Create initial accounts with genesis distribution"""
        # Main treasury account
        self.create_account("TREASURY", initial_balance=self.GENESIS_SUPPLY)
        
        # Validator rewards pool
        self.create_account("VALIDATOR_POOL", initial_balance=self.VALIDATOR_RESERVE)
        
        # Ecosystem development fund
        self.create_account("ECOSYSTEM_FUND", initial_balance=self.ECOSYSTEM_RESERVE)
        
        # Transition reserve pool (collects orbital transition energy)
        # Starts at zero, accumulates from message/transaction orbital transitions
        self.create_account("TRANSITION_RESERVE", initial_balance=0)
        
        # Burn address (tokens sent here are burned)
        self.create_account("BURN_ADDRESS", initial_balance=0)
    
    def create_account(self, address: str, initial_balance: int = 0) -> Account:
        """Create new account"""
        if address in self.accounts:
            return self.accounts[address]
        
        account = Account(address=address, balance=initial_balance)
        self.accounts[address] = account
        return account
    
    def get_account(self, address: str) -> Optional[Account]:
        """Get account by address"""
        return self.accounts.get(address)
    
    def get_or_create_account(self, address: str) -> Account:
        """Get existing account or create new one"""
        if address not in self.accounts:
            return self.create_account(address)
        return self.accounts[address]
    
    def transfer(self, from_address: str, to_address: str, amount: int, fee: Optional[int] = None) -> Optional[TokenTransaction]:
        """Transfer tokens between accounts"""
        if fee is None:
            fee = self.BASE_TRANSFER_FEE
        
        from_account = self.get_account(from_address)
        if not from_account:
            return None
        
        total_deduct = amount + fee
        if not from_account.has_sufficient_balance(total_deduct):
            return None
        
        # Deduct from sender
        from_account.balance -= total_deduct
        from_account.nonce += 1
        
        # Add to receiver
        to_account = self.get_or_create_account(to_address)
        to_account.balance += amount
        
        # Fee goes to validator pool (or can be distributed to validators)
        if fee > 0:
            validator_pool = self.get_account("VALIDATOR_POOL")
            if validator_pool:
                validator_pool.balance += fee
        
        # Create transaction record
        tx = TokenTransaction(
            tx_id=f"TX{self.tx_counter:08d}",
            tx_type=TransactionType.TRANSFER,
            from_address=from_address,
            to_address=to_address,
            amount=amount,
            fee=fee
        )
        self.tx_counter += 1
        self.transactions.append(tx)
        
        return tx
    
    def transfer_atomic(
        self, 
        from_address: str, 
        to_address: str, 
        amount: int, 
        fee: Optional[int] = None,
        reason: str = ""
    ) -> tuple[bool, Optional[TokenTransaction], str]:
        """
        Atomic transfer with rollback support - Production-safe transaction.
        
        This method ensures all-or-nothing semantics: if any step fails,
        all changes are rolled back to maintain consistency.
        
        Args:
            from_address: Sender account address
            to_address: Receiver account address
            amount: Amount in units to transfer
            fee: Optional transaction fee (defaults to BASE_TRANSFER_FEE)
            reason: Optional transaction reason for logging
        
        Returns:
            (success: bool, transaction: Optional[TokenTransaction], message: str)
        
        Example:
            success, tx, msg = token_system.transfer_atomic(
                "alice", "TRANSITION_RESERVE", 5700, reason="message burn"
            )
        """
        if fee is None:
            fee = self.BASE_TRANSFER_FEE
        
        # Step 1: Validate accounts exist
        from_account = self.get_account(from_address)
        if not from_account:
            return (False, None, f"Sender account '{from_address}' not found")
        
        # Step 2: Validate sufficient balance (BEFORE any mutations)
        total_deduct = amount + fee
        if not from_account.has_sufficient_balance(total_deduct):
            return (
                False,
                None,
                f"Insufficient balance: need {total_deduct} units, have {from_account.balance} units"
            )
        
        # Step 3: Snapshot balances for potential rollback
        from_balance_before = from_account.balance
        from_nonce_before = from_account.nonce
        
        to_account = self.get_or_create_account(to_address)
        to_balance_before = to_account.balance
        
        validator_pool = self.get_account("VALIDATOR_POOL")
        validator_balance_before = validator_pool.balance if validator_pool else 0
        
        try:
            # Step 4: Execute transfer (atomic block)
            from_account.balance -= total_deduct
            from_account.nonce += 1
            
            to_account.balance += amount
            
            if fee > 0 and validator_pool:
                validator_pool.balance += fee
            
            # Step 5: Create transaction record
            tx = TokenTransaction(
                tx_id=f"TX{self.tx_counter:08d}",
                tx_type=TransactionType.TRANSFER,
                from_address=from_address,
                to_address=to_address,
                amount=amount,
                fee=fee,
                data={"reason": reason} if reason else {}
            )
            self.tx_counter += 1
            self.transactions.append(tx)
            
            return (True, tx, f"Transfer successful: {amount} units → {to_address}")
            
        except Exception as e:
            # Step 6: ROLLBACK on any error
            from_account.balance = from_balance_before
            from_account.nonce = from_nonce_before
            to_account.balance = to_balance_before
            if validator_pool:
                validator_pool.balance = validator_balance_before
            
            return (
                False,
                None,
                f"Transfer failed and rolled back: {str(e)}"
            )
    
    def burn(self, from_address: str, amount: int, reason: str = "") -> Optional[TokenTransaction]:
        """Burn tokens (deflationary mechanism)"""
        from_account = self.get_account(from_address)
        if not from_account or not from_account.has_sufficient_balance(amount):
            return None
        
        # Deduct from account
        from_account.balance -= amount
        from_account.nonce += 1
        
        # Update total burned
        self.total_burned += amount
        
        # Optional: track in burn address
        burn_account = self.get_account("BURN_ADDRESS")
        if burn_account:
            burn_account.balance += amount
        
        # Create transaction record
        tx = TokenTransaction(
            tx_id=f"TX{self.tx_counter:08d}",
            tx_type=TransactionType.BURN,
            from_address=from_address,
            to_address="BURN_ADDRESS",
            amount=amount,
            data={"reason": reason}
        )
        self.tx_counter += 1
        self.transactions.append(tx)
        
        return tx
    
    def mint_reward(self, to_address: str, amount: int, reason: str = "") -> Optional[TokenTransaction]:
        """Mint new tokens as validator rewards (controlled inflation)"""
        # Check if we have reserve
        validator_pool = self.get_account("VALIDATOR_POOL")
        if not validator_pool or not validator_pool.has_sufficient_balance(amount):
            return None
        
        # Deduct from validator pool
        validator_pool.balance -= amount
        
        # Add to recipient
        to_account = self.get_or_create_account(to_address)
        to_account.balance += amount
        
        # Create transaction record
        tx = TokenTransaction(
            tx_id=f"TX{self.tx_counter:08d}",
            tx_type=TransactionType.REWARD,
            from_address="VALIDATOR_POOL",
            to_address=to_address,
            amount=amount,
            data={"reason": reason}
        )
        self.tx_counter += 1
        self.transactions.append(tx)
        
        return tx
    
    def pay_for_message(self, from_address: str) -> Optional[TokenTransaction]:
        """
        Pay for sending encrypted message using orbital transition physics.
        
        Physics: Electron drops from n=3 → n=2 (Hα line, 656.4nm red light)
        Energy flows into TRANSITION_RESERVE instead of being destroyed.
        """
        if self.USE_ORBITAL_TRANSITIONS:
            # Get pre-calculated cost (without executing transition yet)
            cost_info = orbital_engine.get_transition_cost(OrbitalTransitionType.STANDARD_MESSAGE)
            units_cost = cost_info['delta_e_units']
            
            # CHECK BALANCE FIRST (before any state mutations)
            from_account = self.get_account(from_address)
            if not from_account or not from_account.has_sufficient_balance(units_cost):
                return None
            
            # Balance is sufficient - NOW execute the orbital transition
            # Pass current reserve balance for stateless calculation
            reserve_account = self.get_account("TRANSITION_RESERVE")
            reserve_balance_before = reserve_account.balance if reserve_account else 0
            
            transition, units_cost = orbital_engine.execute_transition(
                OrbitalTransitionType.STANDARD_MESSAGE,
                user_address=from_address,
                reserve_balance_before=reserve_balance_before,
                block_height=None  # Could link to blockchain height
            )
            
            # Deduct from user account and increment nonce
            from_account.balance -= units_cost
            from_account.nonce += 1
            
            # Add to TRANSITION_RESERVE
            reserve_account = self.get_account("TRANSITION_RESERVE")
            if reserve_account:
                reserve_account.balance += units_cost
            
            # Create transaction record
            tx = TokenTransaction(
                tx_id=f"TX{self.tx_counter:08d}",
                tx_type=TransactionType.MESSAGE_PAYMENT,
                from_address=from_address,
                to_address="TRANSITION_RESERVE",
                amount=units_cost,
                data={
                    "reason": "Orbital transition: n=3→2 (Hα line)",
                    "transition_type": transition.transition_type.display_name,
                    "wavelength_nm": transition.wavelength_nm,
                    "spectral_region": transition.spectral_region.name,
                    "delta_e_nxt": transition.delta_e_nxt
                }
            )
            self.tx_counter += 1
            self.transactions.append(tx)
            
            return tx
        else:
            # LEGACY: Old burn mechanism
            base_burn_nxt = self.units_to_nxt(self.MESSAGE_BURN_RATE)
            adjusted_burn_nxt = self.calculate_dynamic_burn(base_burn_nxt)
            burn_amount = self.nxt_to_units(adjusted_burn_nxt)
            
            tx = self.burn(from_address, burn_amount, "Encrypted message payment")
            if tx:
                tx.tx_type = TransactionType.MESSAGE_PAYMENT
            return tx
    
    def pay_for_link_share(self, from_address: str) -> Optional[TokenTransaction]:
        """
        Pay for sharing link using orbital transition physics.
        
        Physics: Electron drops from n=4 → n=2 (Hβ line, 486.2nm blue light)
        Energy flows into TRANSITION_RESERVE instead of being destroyed.
        """
        if self.USE_ORBITAL_TRANSITIONS:
            # Get pre-calculated cost (without executing transition yet)
            cost_info = orbital_engine.get_transition_cost(OrbitalTransitionType.LINK_SHARE)
            units_cost = cost_info['delta_e_units']
            
            # CHECK BALANCE FIRST (before any state mutations)
            from_account = self.get_account(from_address)
            if not from_account or not from_account.has_sufficient_balance(units_cost):
                return None
            
            # Balance is sufficient - NOW execute the orbital transition
            # Pass current reserve balance for stateless calculation
            reserve_account = self.get_account("TRANSITION_RESERVE")
            reserve_balance_before = reserve_account.balance if reserve_account else 0
            
            transition, units_cost = orbital_engine.execute_transition(
                OrbitalTransitionType.LINK_SHARE,
                user_address=from_address,
                reserve_balance_before=reserve_balance_before,
                block_height=None
            )
            
            # Deduct from user account and increment nonce
            from_account.balance -= units_cost
            from_account.nonce += 1
            
            # Add to TRANSITION_RESERVE
            reserve_account = self.get_account("TRANSITION_RESERVE")
            if reserve_account:
                reserve_account.balance += units_cost
            
            # Create transaction record
            tx = TokenTransaction(
                tx_id=f"TX{self.tx_counter:08d}",
                tx_type=TransactionType.LINK_SHARE_PAYMENT,
                from_address=from_address,
                to_address="TRANSITION_RESERVE",
                amount=units_cost,
                data={
                    "reason": "Orbital transition: n=4→2 (Hβ line)",
                    "transition_type": transition.transition_type.display_name,
                    "wavelength_nm": transition.wavelength_nm,
                    "spectral_region": transition.spectral_region.name,
                    "delta_e_nxt": transition.delta_e_nxt
                }
            )
            self.tx_counter += 1
            self.transactions.append(tx)
            
            return tx
        else:
            # LEGACY: Old burn mechanism
            base_burn_nxt = self.units_to_nxt(self.LINK_SHARE_BURN_RATE)
            adjusted_burn_nxt = self.calculate_dynamic_burn(base_burn_nxt)
            burn_amount = self.nxt_to_units(adjusted_burn_nxt)
            
            tx = self.burn(from_address, burn_amount, "Link share payment")
            if tx:
                tx.tx_type = TransactionType.LINK_SHARE_PAYMENT
            return tx
    
    def pay_for_video_share(self, from_address: str) -> Optional[TokenTransaction]:
        """
        Pay for sharing video using orbital transition physics.
        
        Physics: Electron drops from n=5 → n=2 (434.1nm violet light)
        Energy flows into TRANSITION_RESERVE instead of being destroyed.
        """
        if self.USE_ORBITAL_TRANSITIONS:
            # Get pre-calculated cost (without executing transition yet)
            cost_info = orbital_engine.get_transition_cost(OrbitalTransitionType.VIDEO_SHARE)
            units_cost = cost_info['delta_e_units']
            
            # CHECK BALANCE FIRST (before any state mutations)
            from_account = self.get_account(from_address)
            if not from_account or not from_account.has_sufficient_balance(units_cost):
                return None
            
            # Balance is sufficient - NOW execute the orbital transition
            # Pass current reserve balance for stateless calculation
            reserve_account = self.get_account("TRANSITION_RESERVE")
            reserve_balance_before = reserve_account.balance if reserve_account else 0
            
            transition, units_cost = orbital_engine.execute_transition(
                OrbitalTransitionType.VIDEO_SHARE,
                user_address=from_address,
                reserve_balance_before=reserve_balance_before,
                block_height=None
            )
            
            # Deduct from user account and increment nonce
            from_account.balance -= units_cost
            from_account.nonce += 1
            
            # Add to TRANSITION_RESERVE
            reserve_account = self.get_account("TRANSITION_RESERVE")
            if reserve_account:
                reserve_account.balance += units_cost
            
            # Create transaction record
            tx = TokenTransaction(
                tx_id=f"TX{self.tx_counter:08d}",
                tx_type=TransactionType.VIDEO_SHARE_PAYMENT,
                from_address=from_address,
                to_address="TRANSITION_RESERVE",
                amount=units_cost,
                data={
                    "reason": "Orbital transition: n=5→2 (Balmer series)",
                    "transition_type": transition.transition_type.display_name,
                    "wavelength_nm": transition.wavelength_nm,
                    "spectral_region": transition.spectral_region.name,
                    "delta_e_nxt": transition.delta_e_nxt
                }
            )
            self.tx_counter += 1
            self.transactions.append(tx)
            
            return tx
        else:
            # LEGACY: Old burn mechanism
            base_burn_nxt = self.units_to_nxt(self.VIDEO_SHARE_BURN_RATE)
            adjusted_burn_nxt = self.calculate_dynamic_burn(base_burn_nxt)
            burn_amount = self.nxt_to_units(adjusted_burn_nxt)
            
            tx = self.burn(from_address, burn_amount, "Video share payment")
            if tx:
                tx.tx_type = TransactionType.VIDEO_SHARE_PAYMENT
            return tx
    
    def get_total_supply(self) -> int:
        """Get total possible supply"""
        return self.TOTAL_SUPPLY
    
    def get_burn_rate(self) -> float:
        """Calculate current burn rate (percentage)"""
        if self.total_minted == 0:
            return 0.0
        return (self.total_burned / self.total_minted) * 100
    
    def get_token_stats(self) -> dict:
        """Get comprehensive token statistics"""
        validator_pool = self.get_account("VALIDATOR_POOL")
        ecosystem_fund = self.get_account("ECOSYSTEM_FUND")
        
        return {
            "total_supply": self.TOTAL_SUPPLY,
            "total_minted": self.total_minted,
            "circulating_supply": self.get_circulating_supply(),
            "total_burned": self.total_burned,
            "burn_rate_percent": self.get_burn_rate(),
            "total_accounts": len(self.accounts),
            "total_transactions": len(self.transactions),
            "validator_reserve": validator_pool.balance if validator_pool else 0,
            "ecosystem_reserve": ecosystem_fund.balance if ecosystem_fund else 0,
        }
    
    def get_account_transactions(self, address: str, limit: int = 100) -> List[TokenTransaction]:
        """Get transactions for an account"""
        account_txs = [
            tx for tx in self.transactions
            if tx.from_address == address or tx.to_address == address
        ]
        return sorted(account_txs, key=lambda x: x.timestamp, reverse=True)[:limit]
    
    def units_to_nxt(self, units: int) -> float:
        """Convert units to NXT"""
        return units / self.UNITS_PER_NXT
    
    def nxt_to_units(self, nxt: float) -> int:
        """Convert NXT to units"""
        return int(nxt * self.UNITS_PER_NXT)
    
    def get_circulating_supply(self) -> int:
        """Get current circulating supply in units"""
        return self.total_minted - self.total_burned
    
    def get_supply_ratio(self) -> float:
        """Get ratio of circulating supply to total supply"""
        return self.get_circulating_supply() / self.TOTAL_SUPPLY
    
    def calculate_dynamic_burn(self, base_burn: float) -> float:
        """
        Calculate burn rate adjusted for remaining supply.
        
        Formula: adjusted_burn = base_burn * sqrt(supply_ratio)
        
        Examples:
        - 100% supply → 100% burn rate
        - 50% supply → 71% burn rate  
        - 25% supply → 50% burn rate
        - 10% supply → 32% burn rate
        """
        if not self.ENABLE_DYNAMIC_BURNS:
            return base_burn
        
        supply_ratio = self.get_supply_ratio()
        adjustment = supply_ratio ** 0.5  # Square root dampening
        return base_burn * adjustment
    
    def get_sustainability_metrics(self) -> Dict[str, float]:
        """
        Calculate economic sustainability metrics.
        
        Returns:
            Dict with circulating_nxt, total_burned_nxt, supply_pct, 
            burn_velocity, sustainability_score
        """
        circulating = self.get_circulating_supply()
        circulating_nxt = self.units_to_nxt(circulating)
        burned_nxt = self.units_to_nxt(self.total_burned)
        supply_pct = (circulating / self.TOTAL_SUPPLY) * 100
        
        # Simple sustainability score
        if supply_pct >= 90:
            score = 100
        elif supply_pct >= 75:
            score = 90
        elif supply_pct >= 50:
            score = 75
        elif supply_pct >= 25:
            score = 50
        else:
            score = max(0, supply_pct * 2)  # Linear degradation
        
        return {
            'circulating_nxt': circulating_nxt,
            'total_burned_nxt': burned_nxt,
            'supply_percentage': supply_pct,
            'sustainability_score': score,
            'total_supply_nxt': self.units_to_nxt(self.TOTAL_SUPPLY)
        }
    
    def format_balance(self, units: int) -> str:
        """
        Format balance for user display (Bitcoin-style).
        
        Shows appropriate precision based on amount:
        - < 0.001 NXT: Up to 8 decimals (like satoshis)
        - < 1 NXT: Up to 6 decimals
        - >= 1 NXT: 2-4 decimals
        
        Strips trailing zeros for clarity.
        """
        nxt = self.units_to_nxt(units)
        
        if nxt == 0:
            return "0 NXT"
        elif nxt < 0.001:
            # Micro-amounts: show up to 8 decimals (satoshi-level precision)
            formatted = f"{nxt:.8f}".rstrip('0').rstrip('.')
        elif nxt < 1:
            # Small amounts: show up to 6 decimals
            formatted = f"{nxt:.6f}".rstrip('0').rstrip('.')
        elif nxt < 1000:
            # Medium amounts: show 4 decimals
            formatted = f"{nxt:,.4f}".rstrip('0').rstrip('.')
        else:
            # Large amounts: show 2 decimals with thousands separators
            formatted = f"{nxt:,.2f}"
        
        return f"{formatted} NXT"


def format_nxt_amount(nxt: float) -> str:
    """
    Format NXT amount for display (Bitcoin-style precision).
    
    Helper function that can be imported and used across UI components.
    Shows appropriate decimal precision based on amount size.
    """
    if nxt == 0:
        return "0"
    elif nxt < 0.001:
        # Micro-amounts: up to 8 decimals (satoshi-level)
        return f"{nxt:.8f}".rstrip('0').rstrip('.')
    elif nxt < 1:
        # Small amounts: up to 6 decimals
        return f"{nxt:.6f}".rstrip('0').rstrip('.')
    elif nxt < 1000:
        # Medium amounts: 4 decimals
        return f"{nxt:,.4f}".rstrip('0').rstrip('.')
    else:
        # Large amounts: 2 decimals with commas
        return f"{nxt:,.2f}"


# Global token system instance
token_system = NativeTokenSystem()
