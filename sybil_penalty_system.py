"""
Automated Penalty System for Detected Sybil Attacks
====================================================

Progressive slashing and isolation system that automatically penalizes
coordinated validator clusters based on detection confidence and severity.
"""

import time
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from sybil_detection import ClusterDetectionResult, ClusterSeverity


class PenaltyType(Enum):
    """Types of penalties that can be applied"""
    SLASH = "stake_slash"
    JAIL = "temporary_jail"
    BAN = "permanent_ban"
    VOTING_WEIGHT_REDUCTION = "voting_weight_reduction"
    ISOLATION = "network_isolation"
    MONITORING = "enhanced_monitoring"


@dataclass
class PenaltyAction:
    """Individual penalty action"""
    penalty_type: PenaltyType
    validator_id: str
    cluster_id: str
    severity: ClusterSeverity
    
    # Slash details
    slash_percentage: float = 0.0
    slashed_amount: float = 0.0
    
    # Jail details
    jail_duration_seconds: float = 0.0
    jail_until: Optional[float] = None
    
    # Voting weight reduction
    original_weight: float = 1.0
    reduced_weight: float = 1.0
    
    # Status
    applied: bool = False
    applied_at: Optional[float] = None
    reverted: bool = False
    
    # Evidence
    evidence: List[str] = field(default_factory=list)
    
    def apply(self) -> bool:
        """Mark penalty as applied"""
        if not self.applied:
            self.applied = True
            self.applied_at = time.time()
            if self.jail_duration_seconds > 0:
                self.jail_until = time.time() + self.jail_duration_seconds
            return True
        return False
    
    def is_expired(self) -> bool:
        """Check if jail period has expired"""
        if self.penalty_type == PenaltyType.JAIL:
            if self.jail_until and time.time() >= self.jail_until:
                return True
        return False


class SybilPenaltySystem:
    """
    Automated penalty system for Sybil attack clusters.
    
    Penalty Tiers:
    - CRITICAL (confidence >= 0.8): 50% slash + permanent ban
    - HIGH (confidence >= 0.6): 30% slash + 48h jail
    - MEDIUM (confidence >= 0.4): 20% slash + 24h jail + monitoring
    - LOW (confidence >= 0.2): Warning + voting weight reduction + monitoring
    - NONE: Monitor only
    """
    
    def __init__(self):
        self.penalty_history: List[PenaltyAction] = []
        self.active_penalties: Dict[str, List[PenaltyAction]] = {}  # validator_id -> penalties
        self.banned_validators: set = set()
        self.jailed_validators: Dict[str, float] = {}  # validator_id -> jail_until
        self.monitored_validators: set = set()
    
    def process_detection(
        self, 
        detection: ClusterDetectionResult,
        validator_stakes: Dict[str, float]
    ) -> List[PenaltyAction]:
        """
        Process detection result and create penalty actions.
        
        Args:
            detection: Cluster detection result
            validator_stakes: Map of validator_id to current stake amount
        
        Returns:
            List of penalty actions to be applied
        """
        penalties = []
        
        for validator_id in detection.validators:
            if validator_id not in validator_stakes:
                continue
            
            stake = validator_stakes[validator_id]
            penalty = self._create_penalty_for_severity(
                validator_id=validator_id,
                cluster_id=detection.cluster_id,
                severity=detection.severity,
                confidence=detection.confidence_score,
                stake=stake,
                evidence=detection.evidence
            )
            
            penalties.append(penalty)
        
        return penalties
    
    def _create_penalty_for_severity(
        self,
        validator_id: str,
        cluster_id: str,
        severity: ClusterSeverity,
        confidence: float,
        stake: float,
        evidence: List[str]
    ) -> PenaltyAction:
        """Create appropriate penalty based on severity"""
        
        if severity == ClusterSeverity.CRITICAL:
            # 50% slash + permanent ban
            return PenaltyAction(
                penalty_type=PenaltyType.SLASH,
                validator_id=validator_id,
                cluster_id=cluster_id,
                severity=severity,
                slash_percentage=0.50,
                slashed_amount=stake * 0.50,
                jail_duration_seconds=float('inf'),  # Permanent
                evidence=evidence + ["CRITICAL SYBIL ATTACK - PERMANENT BAN"]
            )
        
        elif severity == ClusterSeverity.HIGH:
            # 30% slash + 48h jail
            return PenaltyAction(
                penalty_type=PenaltyType.SLASH,
                validator_id=validator_id,
                cluster_id=cluster_id,
                severity=severity,
                slash_percentage=0.30,
                slashed_amount=stake * 0.30,
                jail_duration_seconds=172800.0,  # 48 hours
                evidence=evidence + ["HIGH SEVERITY SYBIL - 48H JAIL"]
            )
        
        elif severity == ClusterSeverity.MEDIUM:
            # 20% slash + 24h jail + monitoring
            return PenaltyAction(
                penalty_type=PenaltyType.SLASH,
                validator_id=validator_id,
                cluster_id=cluster_id,
                severity=severity,
                slash_percentage=0.20,
                slashed_amount=stake * 0.20,
                jail_duration_seconds=86400.0,  # 24 hours
                evidence=evidence + ["MEDIUM SEVERITY SYBIL - 24H JAIL + MONITORING"]
            )
        
        elif severity == ClusterSeverity.LOW:
            # Voting weight reduction + monitoring
            return PenaltyAction(
                penalty_type=PenaltyType.VOTING_WEIGHT_REDUCTION,
                validator_id=validator_id,
                cluster_id=cluster_id,
                severity=severity,
                original_weight=1.0,
                reduced_weight=0.5,  # 50% voting power
                evidence=evidence + ["LOW SEVERITY SYBIL - VOTING WEIGHT REDUCED + MONITORING"]
            )
        
        else:  # NONE
            # Monitoring only
            return PenaltyAction(
                penalty_type=PenaltyType.MONITORING,
                validator_id=validator_id,
                cluster_id=cluster_id,
                severity=severity,
                evidence=evidence + ["SUSPICIOUS PATTERN - ENHANCED MONITORING"]
            )
    
    def apply_penalties(
        self,
        penalties: List[PenaltyAction],
        validator_economics
    ) -> Dict[str, Any]:
        """
        Apply penalties to validators through validator economics system.
        
        Args:
            penalties: List of penalty actions
            validator_economics: ValidatorEconomicsSystem instance (StakingEconomy class)
        
        Returns:
            Summary of applied penalties
        """
        results = {
            "applied": 0,
            "failed": 0,
            "total_slashed": 0.0,
            "validators_banned": 0,
            "validators_jailed": 0,
            "details": []
        }
        
        # Get validators dict
        validators = getattr(validator_economics, 'validators', {})
        
        for penalty in penalties:
            try:
                # Check if validator exists
                if penalty.validator_id not in validators:
                    results["failed"] += 1
                    results["details"].append({
                        "validator_id": penalty.validator_id,
                        "penalty_type": penalty.penalty_type.value,
                        "error": "Validator not found",
                        "applied": False
                    })
                    continue
                
                validator = validators[penalty.validator_id]
                
                if penalty.penalty_type == PenaltyType.SLASH:
                    # Import SlashingType for proper slashing
                    from validator_economics import SlashingType
                    
                    # Apply slashing through validator's slash method
                    # Note: slash() takes percentage as 0-100, not 0.0-1.0
                    slash_pct = penalty.slash_percentage * 100  # Convert to percentage
                    validator.slash(
                        SlashingType.NETWORK_ATTACK,
                        slash_pct,
                        f"Sybil Attack Detection - Cluster {penalty.cluster_id}"
                    )
                    
                    penalty.apply()
                    results["total_slashed"] += penalty.slashed_amount
                    
                    # Apply jail if needed
                    if penalty.jail_duration_seconds == float('inf'):
                        # Permanent ban
                        self.banned_validators.add(penalty.validator_id)
                        validator.is_jailed = True
                        validator.jail_until = float('inf')
                        results["validators_banned"] += 1
                    elif penalty.jail_duration_seconds > 0:
                        # Temporary jail
                        validator.jail(penalty.jail_duration_seconds)
                        if penalty.jail_until is not None:
                            self.jailed_validators[penalty.validator_id] = penalty.jail_until
                        results["validators_jailed"] += 1
                
                elif penalty.penalty_type == PenaltyType.VOTING_WEIGHT_REDUCTION:
                    # Reduce reputation score (acts as voting weight in validator economics)
                    validator.reputation_score *= penalty.reduced_weight
                    penalty.apply()
                    self.monitored_validators.add(penalty.validator_id)
                
                elif penalty.penalty_type == PenaltyType.MONITORING:
                    # Add to monitoring list
                    self.monitored_validators.add(penalty.validator_id)
                    penalty.apply()
                
                # Store penalty
                if penalty.validator_id not in self.active_penalties:
                    self.active_penalties[penalty.validator_id] = []
                self.active_penalties[penalty.validator_id].append(penalty)
                self.penalty_history.append(penalty)
                
                results["applied"] += 1
                results["details"].append({
                    "validator_id": penalty.validator_id,
                    "penalty_type": penalty.penalty_type.value,
                    "severity": penalty.severity.name,
                    "applied": True
                })
                
            except Exception as e:
                results["failed"] += 1
                results["details"].append({
                    "validator_id": penalty.validator_id,
                    "penalty_type": penalty.penalty_type.value,
                    "error": str(e),
                    "applied": False
                })
        
        return results
    
    def check_and_release_jailed(self) -> List[str]:
        """Check for expired jail periods and release validators"""
        released = []
        current_time = time.time()
        
        to_remove = []
        for validator_id, jail_until in self.jailed_validators.items():
            if current_time >= jail_until:
                to_remove.append(validator_id)
                released.append(validator_id)
        
        for validator_id in to_remove:
            del self.jailed_validators[validator_id]
        
        return released
    
    def is_validator_banned(self, validator_id: str) -> bool:
        """Check if validator is permanently banned"""
        return validator_id in self.banned_validators
    
    def is_validator_jailed(self, validator_id: str) -> bool:
        """Check if validator is currently jailed"""
        if validator_id in self.jailed_validators:
            if time.time() < self.jailed_validators[validator_id]:
                return True
            else:
                # Expired, remove from jail
                del self.jailed_validators[validator_id]
                return False
        return False
    
    def get_validator_status(self, validator_id: str) -> Dict:
        """Get complete penalty status for a validator"""
        return {
            "validator_id": validator_id,
            "banned": self.is_validator_banned(validator_id),
            "jailed": self.is_validator_jailed(validator_id),
            "jail_until": self.jailed_validators.get(validator_id),
            "monitored": validator_id in self.monitored_validators,
            "active_penalties": len(self.active_penalties.get(validator_id, [])),
            "total_slashed": sum(
                p.slashed_amount 
                for p in self.active_penalties.get(validator_id, [])
                if p.penalty_type == PenaltyType.SLASH
            )
        }
    
    def get_system_stats(self) -> Dict:
        """Get overall penalty system statistics"""
        return {
            "total_penalties_applied": len(self.penalty_history),
            "validators_banned": len(self.banned_validators),
            "validators_jailed": len(self.jailed_validators),
            "validators_monitored": len(self.monitored_validators),
            "total_stake_slashed": sum(
                p.slashed_amount 
                for p in self.penalty_history 
                if p.penalty_type == PenaltyType.SLASH
            ),
            "severity_breakdown": {
                severity.name: sum(
                    1 for p in self.penalty_history 
                    if p.severity == severity
                )
                for severity in ClusterSeverity
            },
            "recent_penalties": [
                {
                    "validator_id": p.validator_id,
                    "penalty_type": p.penalty_type.value,
                    "severity": p.severity.name,
                    "slash_pct": p.slash_percentage,
                    "applied_at": p.applied_at
                }
                for p in self.penalty_history[-20:]
            ]
        }
