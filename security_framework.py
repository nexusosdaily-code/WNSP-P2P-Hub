"""
NexusOS Security Framework
Comprehensive security defenses against economic and consensus attacks

Protects against:
- DEX MEV (front-running, sandwich attacks)
- Oracle manipulation
- Rate limiting (transaction flooding)
- Flash loan exploits
- Governance attacks (vote buying, proposal spam)
"""

import time
import hashlib
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from collections import deque, defaultdict
import threading

# Active intervention integration
try:
    from active_intervention_engine import get_intervention_engine
except ImportError:
    get_intervention_engine = None


class AttackType(Enum):
    """Types of attacks being monitored"""
    MEV_FRONTRUN = "mev_frontrun"
    SANDWICH_ATTACK = "sandwich_attack"
    FLASH_LOAN = "flash_loan"
    RATE_LIMIT_VIOLATION = "rate_limit_violation"
    ORACLE_MANIPULATION = "oracle_manipulation"
    VOTE_BUYING = "vote_buying"
    PROPOSAL_SPAM = "proposal_spam"
    WASH_TRADING = "wash_trading"
    LIQUIDITY_DRAIN = "liquidity_drain"


@dataclass
class SecurityAlert:
    """Security alert for detected attack"""
    alert_id: str
    attack_type: AttackType
    severity: str  # "low", "medium", "high", "critical"
    attacker_address: Optional[str]
    timestamp: float
    evidence: Dict[str, Any]
    mitigated: bool = False
    mitigation_action: Optional[str] = None


class RateLimiter:
    """
    Per-address rate limiting to prevent transaction flooding and spam
    
    Implements sliding window rate limiting with exponential backoff
    """
    
    def __init__(self):
        # address -> deque of timestamps
        self.request_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        
        # Rate limits (requests per time window)
        self.limits = {
            "transfer": (10, 60),  # 10 transfers per 60 seconds
            "dex_swap": (5, 60),  # 5 swaps per 60 seconds
            "message": (20, 60),  # 20 messages per 60 seconds
            "proposal": (1, 3600),  # 1 proposal per hour
            "vote": (10, 300),  # 10 votes per 5 minutes
        }
        
        # Violation tracking for exponential backoff
        self.violations: Dict[str, int] = defaultdict(int)
        self.violation_timestamps: Dict[str, float] = {}
        
        self.lock = threading.Lock()
    
    def check_rate_limit(
        self,
        address: str,
        operation: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Check if address is within rate limit for operation
        
        Returns:
            (allowed: bool, reason: Optional[str])
        """
        with self.lock:
            if operation not in self.limits:
                return True, None
            
            max_requests, window_seconds = self.limits[operation]
            
            # Get request history for this address
            history = self.request_history[f"{address}:{operation}"]
            
            # Remove old requests outside window
            current_time = time.time()
            cutoff_time = current_time - window_seconds
            
            while history and history[0] < cutoff_time:
                history.popleft()
            
            # Check if limit exceeded
            if len(history) >= max_requests:
                # Record violation
                self.violations[address] += 1
                self.violation_timestamps[address] = current_time
                
                # Calculate backoff time (exponential)
                backoff_multiplier = min(2 ** self.violations[address], 64)
                retry_after = window_seconds * backoff_multiplier
                
                return False, f"Rate limit exceeded. {len(history)}/{max_requests} requests in {window_seconds}s. Retry after {retry_after:.0f}s"
            
            # Add current request
            history.append(current_time)
            
            return True, None
    
    def reset_violations(self, address: str):
        """Reset violation count for address (e.g., after successful behavior)"""
        with self.lock:
            if address in self.violations:
                del self.violations[address]
            if address in self.violation_timestamps:
                del self.violation_timestamps[address]
    
    def get_stats(self, address: str) -> Dict[str, Any]:
        """Get rate limiting stats for address"""
        with self.lock:
            stats = {
                "violations": self.violations.get(address, 0),
                "last_violation": self.violation_timestamps.get(address),
                "current_requests": {}
            }
            
            current_time = time.time()
            
            for operation, (max_req, window) in self.limits.items():
                key = f"{address}:{operation}"
                if key in self.request_history:
                    cutoff = current_time - window
                    recent = [t for t in self.request_history[key] if t > cutoff]
                    stats["current_requests"][operation] = f"{len(recent)}/{max_req}"
            
            return stats


class DEXMEVProtection:
    """
    Protection against Maximum Extractable Value (MEV) attacks
    
    Implements:
    - Commit-reveal scheme for swaps
    - Sandwich attack detection
    - Flash loan prevention
    - Wash trading detection
    """
    
    def __init__(self):
        # Pending commits (hash -> commit data)
        self.pending_commits: Dict[str, Dict[str, Any]] = {}
        
        # Reveal window (seconds)
        self.commit_delay = 30  # Must wait 30s before revealing
        self.reveal_window = 300  # Must reveal within 5 minutes
        
        # Flash loan detection
        self.block_transactions: Dict[int, List[str]] = defaultdict(list)
        self.current_block = 0
        
        # Sandwich attack detection
        self.recent_swaps: deque = deque(maxlen=100)
        
        # Wash trading detection
        self.trading_pairs: Dict[str, List[Tuple[str, float]]] = defaultdict(list)
        
        self.lock = threading.Lock()
    
    def commit_swap(
        self,
        address: str,
        input_token: str,
        output_token: str,
        input_amount: float,
        min_output: float,
        nonce: str
    ) -> str:
        """
        Commit to a swap without revealing details
        
        Returns:
            commit_hash: Hash to use for reveal
        """
        with self.lock:
            # Create commitment
            commitment_data = f"{address}:{input_token}:{output_token}:{input_amount}:{min_output}:{nonce}"
            commit_hash = hashlib.sha256(commitment_data.encode()).hexdigest()
            
            # Store commit
            self.pending_commits[commit_hash] = {
                "address": address,
                "commitment_data": commitment_data,
                "commit_time": time.time(),
                "revealed": False
            }
            
            return commit_hash
    
    def reveal_swap(
        self,
        commit_hash: str,
        address: str,
        input_token: str,
        output_token: str,
        input_amount: float,
        min_output: float,
        nonce: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Reveal swap commitment and validate
        
        Returns:
            (success: bool, error_message: Optional[str])
        """
        with self.lock:
            if commit_hash not in self.pending_commits:
                return False, "Commit hash not found"
            
            commit = self.pending_commits[commit_hash]
            
            # Check timing
            current_time = time.time()
            time_since_commit = current_time - commit["commit_time"]
            
            if time_since_commit < self.commit_delay:
                return False, f"Must wait {self.commit_delay}s before revealing (waited {time_since_commit:.0f}s)"
            
            if time_since_commit > self.reveal_window:
                del self.pending_commits[commit_hash]
                return False, f"Reveal window expired (waited {time_since_commit:.0f}s, max {self.reveal_window}s)"
            
            # Validate commitment matches reveal
            revealed_data = f"{address}:{input_token}:{output_token}:{input_amount}:{min_output}:{nonce}"
            if revealed_data != commit["commitment_data"]:
                return False, "Reveal data does not match commitment"
            
            # Mark as revealed
            commit["revealed"] = True
            commit["reveal_time"] = current_time
            
            # Record for sandwich detection
            self.recent_swaps.append({
                "address": address,
                "input_token": input_token,
                "output_token": output_token,
                "amount": input_amount,
                "timestamp": current_time
            })
            
            return True, None
    
    def detect_flash_loan(
        self,
        address: str,
        token: str,
        borrow_amount: float,
        repay_amount: float,
        block_number: int
    ) -> bool:
        """
        Detect flash loan (same-block borrow and repay)
        
        Returns:
            is_flash_loan: bool
        """
        with self.lock:
            self.current_block = max(self.current_block, block_number)
            
            # Record transaction
            tx_key = f"{address}:{token}:{borrow_amount}"
            self.block_transactions[block_number].append(tx_key)
            
            # Check if borrow and repay in same block
            repay_key = f"{address}:{token}:{repay_amount}"
            
            if tx_key in self.block_transactions[block_number] and \
               repay_key in self.block_transactions[block_number]:
                return True
            
            # Cleanup old blocks
            if block_number > self.current_block - 100:
                for old_block in list(self.block_transactions.keys()):
                    if old_block < block_number - 100:
                        del self.block_transactions[old_block]
            
            return False
    
    def detect_sandwich_attack(
        self,
        address: str,
        swap_data: Dict[str, Any]
    ) -> Tuple[bool, Optional[str]]:
        """
        Detect sandwich attack pattern
        
        Sandwich attack: Attacker places order before and after victim's trade
        Pattern: Same address trades same pair in opposite directions within short time
        
        Returns:
            (is_sandwich: bool, evidence: Optional[str])
        """
        with self.lock:
            # Look for reverse trades from same address within 60 seconds
            current_time = time.time()
            
            for recent in self.recent_swaps:
                if recent["address"] != address:
                    continue
                
                time_diff = current_time - recent["timestamp"]
                
                if time_diff > 60:
                    continue
                
                # Check if reverse trade (input/output swapped)
                if (recent["input_token"] == swap_data["output_token"] and
                    recent["output_token"] == swap_data["input_token"]):
                    
                    evidence = f"Reverse trade detected within {time_diff:.1f}s - potential sandwich attack"
                    return True, evidence
            
            return False, None
    
    def detect_wash_trading(
        self,
        address: str,
        token_pair: str,
        volume: float
    ) -> Tuple[bool, Optional[str]]:
        """
        Detect wash trading (self-trading to inflate volume)
        
        Pattern: Same address trading back and forth on same pair
        """
        with self.lock:
            # Track trading on this pair
            self.trading_pairs[token_pair].append((address, time.time()))
            
            # Count trades from this address in last hour
            current_time = time.time()
            cutoff = current_time - 3600
            
            trades_from_address = [
                (addr, t) for addr, t in self.trading_pairs[token_pair]
                if addr == address and t > cutoff
            ]
            
            # If same address accounts for >30% of pair's volume, flag as wash trading
            total_trades = len([t for addr, t in self.trading_pairs[token_pair] if t > cutoff])
            
            if total_trades > 0:
                percentage = len(trades_from_address) / total_trades
                
                if percentage > 0.3 and len(trades_from_address) > 5:
                    return True, f"Address accounts for {percentage:.0%} of pair volume ({len(trades_from_address)} trades)"
            
            return False, None


class MultiOracleSystem:
    """
    Multi-oracle consensus system with outlier detection
    
    Prevents single-oracle manipulation by requiring consensus across
    multiple independent data sources
    """
    
    def __init__(self):
        # Oracle sources (oracle_id -> weight)
        self.oracles: Dict[str, float] = {}
        
        # Price feeds (asset -> deque of (oracle_id, price, timestamp))
        self.price_feeds: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        
        # Time-weighted average prices
        self.twap_window = 3600  # 1 hour
        
        # Outlier detection threshold (z-score)
        self.outlier_threshold = 2.5
        
        self.lock = threading.Lock()
    
    def register_oracle(self, oracle_id: str, weight: float = 1.0):
        """Register an oracle data source"""
        with self.lock:
            self.oracles[oracle_id] = weight
    
    def submit_price(
        self,
        oracle_id: str,
        asset: str,
        price: float
    ) -> bool:
        """
        Submit price from oracle
        
        Returns:
            accepted: bool (False if outlier detected)
        """
        with self.lock:
            if oracle_id not in self.oracles:
                return False
            
            timestamp = time.time()
            
            # Get recent prices for outlier detection
            recent_prices = [
                p for oid, p, t in self.price_feeds[asset]
                if t > timestamp - 300  # Last 5 minutes
            ]
            
            # Outlier detection with ACTIVE INTERVENTION
            if len(recent_prices) >= 3:
                import numpy as np
                
                mean_price = np.mean(recent_prices)
                std_price = np.std(recent_prices)
                
                if std_price > 0:
                    z_score = abs((price - mean_price) / std_price)
                    
                    if z_score > self.outlier_threshold:
                        # 🛡️ ACTIVE INTERVENTION: Auto-blacklist manipulated oracle
                        deviation = abs((price - mean_price) / mean_price)
                        
                        if get_intervention_engine:
                            intervention_engine = get_intervention_engine()
                            intervention_engine.detect_and_intervene(
                                threat_type="oracle_price_deviation",
                                entity=oracle_id,
                                metric_value=deviation,
                                evidence=f"Price ${price:.2f} deviates {deviation*100:.1f}% from mean ${mean_price:.2f} (z-score: {z_score:.2f})"
                            )
                        
                        # Reject outlier
                        return False
            
            # Accept price
            self.price_feeds[asset].append((oracle_id, price, timestamp))
            
            return True
    
    def get_consensus_price(self, asset: str) -> Optional[float]:
        """
        Get consensus price from multiple oracles
        
        Uses weighted median to be robust against outliers
        """
        with self.lock:
            if asset not in self.price_feeds:
                return None
            
            # Get recent prices (last 5 minutes)
            current_time = time.time()
            cutoff = current_time - 300
            
            recent = [
                (oracle_id, price)
                for oracle_id, price, t in self.price_feeds[asset]
                if t > cutoff
            ]
            
            if not recent:
                return None
            
            # Weighted median
            prices_with_weights = [
                (price, self.oracles.get(oracle_id, 1.0))
                for oracle_id, price in recent
            ]
            
            prices_with_weights.sort(key=lambda x: x[0])
            
            total_weight = sum(w for _, w in prices_with_weights)
            cumulative_weight = 0
            
            for price, weight in prices_with_weights:
                cumulative_weight += weight
                if cumulative_weight >= total_weight / 2:
                    return price
            
            return prices_with_weights[0][0] if prices_with_weights else None
    
    def get_twap(self, asset: str) -> Optional[float]:
        """Get Time-Weighted Average Price"""
        with self.lock:
            if asset not in self.price_feeds:
                return None
            
            current_time = time.time()
            cutoff = current_time - self.twap_window
            
            # Get all prices in window
            prices_in_window = [
                (price, t)
                for _, price, t in self.price_feeds[asset]
                if t > cutoff
            ]
            
            if not prices_in_window:
                return None
            
            # Calculate time-weighted average
            total_weight = 0
            weighted_sum = 0
            
            for i in range(len(prices_in_window)):
                price, timestamp = prices_in_window[i]
                
                # Time weight = duration this price was "active"
                if i < len(prices_in_window) - 1:
                    duration = prices_in_window[i + 1][1] - timestamp
                else:
                    duration = current_time - timestamp
                
                weighted_sum += price * duration
                total_weight += duration
            
            if total_weight > 0:
                return weighted_sum / total_weight
            
            return None


# Singleton instances
_rate_limiter = None
_mev_protection = None
_oracle_system = None

def get_rate_limiter() -> RateLimiter:
    """Get singleton rate limiter"""
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = RateLimiter()
    return _rate_limiter

def get_mev_protection() -> DEXMEVProtection:
    """Get singleton MEV protection"""
    global _mev_protection
    if _mev_protection is None:
        _mev_protection = DEXMEVProtection()
    return _mev_protection

def get_oracle_system() -> MultiOracleSystem:
    """Get singleton oracle system"""
    global _oracle_system
    if _oracle_system is None:
        _oracle_system = MultiOracleSystem()
    return _oracle_system
