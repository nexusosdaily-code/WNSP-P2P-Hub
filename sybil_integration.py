"""
Sybil Detection Integration Layer
==================================

Integrates Sybil detection with existing NexusOS systems:
- Validator Economics
- GhostDAG Consensus  
- Proof of Spectrum
- Civic Governance

Provides unified interface for real-time Sybil monitoring and automated response.
"""

import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from sybil_detection import (
    SybilDetectionEngine,
    SybilDetectionConfig,
    ValidatorProfile,
    ClusterDetectionResult
)
from sybil_penalty_system import SybilPenaltySystem, PenaltyAction


@dataclass
class IntegratedSybilMonitor:
    """
    Unified Sybil monitoring system that connects to all NexusOS components.
    """
    
    def __init__(
        self,
        detection_config: Optional[SybilDetectionConfig] = None,
        auto_penalize: bool = True
    ):
        """
        Args:
            detection_config: Configuration for detection engine
            auto_penalize: Whether to automatically apply penalties
        """
        self.detection_engine = SybilDetectionEngine(detection_config)
        self.penalty_system = SybilPenaltySystem()
        self.auto_penalize = auto_penalize
        
        # Monitoring stats
        self.total_scans = 0
        self.total_detections = 0
        self.last_scan_time: Optional[float] = None
        self.scan_interval_seconds = 300  # 5 minutes
    
    def build_validator_profiles(
        self,
        validator_economics,
        civic_governance,
        ghostdag_engine=None
    ) -> List[ValidatorProfile]:
        """
        Build complete validator profiles from existing system data.
        
        Args:
            validator_economics: ValidatorEconomicsSystem instance
            civic_governance: CivicGovernance instance
            ghostdag_engine: Optional GhostDAGEngine instance
        
        Returns:
            List of validator profiles for analysis
        """
        profiles = []
        
        # Get all validators from economics system
        econ_validators = getattr(validator_economics, 'validators', {})
        
        # Get governance validators
        gov_validators = getattr(civic_governance, 'validators', {})
        
        # Merge validator IDs
        all_validator_ids = set(econ_validators.keys()) | set(gov_validators.keys())
        
        for val_id in all_validator_ids:
            # Get data from both systems
            econ_data = econ_validators.get(val_id)
            gov_data = gov_validators.get(val_id)
            
            if not econ_data and not gov_data:
                continue
            
            # Build profile with safe attribute access
            profile = ValidatorProfile(
                validator_id=val_id,
                address=getattr(econ_data, 'address', val_id) if econ_data else val_id,
                spectral_region=gov_data.spectral_region.value if gov_data and hasattr(gov_data, 'spectral_region') else "UNKNOWN",
                stake_amount=getattr(econ_data, 'stake', 0.0) if econ_data else 0.0,
                registration_time=getattr(econ_data, 'activated_at', time.time()) if econ_data else time.time()
            )
            
            # Build voting history from governance system votes
            if civic_governance and hasattr(civic_governance, 'votes'):
                votes_cast = []
                # Iterate through all proposals to find this validator's votes
                for proposal_id, vote_list in civic_governance.votes.items():
                    for vote in vote_list:
                        if hasattr(vote, 'validator_id') and vote.validator_id == val_id:
                            votes_cast.append({
                                'proposal_id': proposal_id,
                                'choice': getattr(vote, 'choice', 'UNKNOWN').value if hasattr(getattr(vote, 'choice', None), 'value') else str(getattr(vote, 'choice', 'UNKNOWN')),
                                'timestamp': getattr(vote, 'timestamp', time.time())
                            })
                profile.votes_cast = votes_cast
            
            # Try to extract funding information from economics delegations
            if econ_data and hasattr(econ_data, 'delegations') and econ_data.delegations:
                try:
                    # Find earliest delegation
                    delegations_with_time = [d for d in econ_data.delegations if hasattr(d, 'delegated_at')]
                    if delegations_with_time:
                        first_delegation = min(delegations_with_time, key=lambda d: d.delegated_at)
                        profile.funding_source = getattr(first_delegation, 'delegator_address', None)
                        profile.funding_timestamp = getattr(first_delegation, 'delegated_at', None)
                except:
                    pass  # Safe fallback if delegation structure differs
            
            profiles.append(profile)
        
        return profiles
    
    def scan_for_sybil_attacks(
        self,
        validator_economics,
        civic_governance,
        ghostdag_engine=None,
        force_scan: bool = False
    ) -> List[ClusterDetectionResult]:
        """
        Perform comprehensive Sybil scan across all validators.
        
        Args:
            validator_economics: ValidatorEconomicsSystem instance
            civic_governance: CivicGovernance instance
            ghostdag_engine: Optional GhostDAGEngine instance
            force_scan: Force scan even if interval hasn't elapsed
        
        Returns:
            List of detected Sybil clusters
        """
        # Check scan interval
        if not force_scan and self.last_scan_time:
            time_since_scan = time.time() - self.last_scan_time
            if time_since_scan < self.scan_interval_seconds:
                return []
        
        # Build profiles
        profiles = self.build_validator_profiles(
            validator_economics,
            civic_governance,
            ghostdag_engine
        )
        
        if len(profiles) < 2:
            return []
        
        # Run detection
        detections = self.detection_engine.analyze_validators(profiles)
        
        # Update stats
        self.total_scans += 1
        self.total_detections += len(detections)
        self.last_scan_time = time.time()
        
        # Auto-penalize if enabled
        if self.auto_penalize and detections:
            self._apply_penalties(detections, validator_economics)
        
        return detections
    
    def _apply_penalties(
        self,
        detections: List[ClusterDetectionResult],
        validator_economics
    ) -> Dict[str, Any]:
        """Apply penalties for detected clusters"""
        all_results = {
            "total_applied": 0,
            "total_failed": 0,
            "total_slashed": 0.0,
            "validators_banned": 0,
            "validators_jailed": 0
        }
        
        # Get current stakes
        validator_stakes = {}
        if hasattr(validator_economics, 'validators'):
            for val_id, val_data in validator_economics.validators.items():
                validator_stakes[val_id] = val_data.stake
        
        for detection in detections:
            # Create penalties
            penalties = self.penalty_system.process_detection(
                detection,
                validator_stakes
            )
            
            # Apply penalties
            results = self.penalty_system.apply_penalties(
                penalties,
                validator_economics
            )
            
            # Aggregate results
            all_results["total_applied"] += results.get("applied", 0)
            all_results["total_failed"] += results.get("failed", 0)
            all_results["total_slashed"] += results.get("total_slashed", 0.0)
            all_results["validators_banned"] += results.get("validators_banned", 0)
            all_results["validators_jailed"] += results.get("validators_jailed", 0)
        
        return all_results
    
    def get_validator_risk_score(self, validator_id: str) -> Dict[str, Any]:
        """
        Calculate risk score for a specific validator.
        
        Returns:
            Risk assessment with score and factors
        """
        risk_factors = []
        risk_score = 0.0
        
        # Check if banned
        if self.penalty_system.is_validator_banned(validator_id):
            return {
                "validator_id": validator_id,
                "risk_score": 1.0,
                "risk_level": "CRITICAL",
                "factors": ["PERMANENTLY BANNED FOR SYBIL ATTACK"],
                "status": "banned"
            }
        
        # Check if jailed
        if self.penalty_system.is_validator_jailed(validator_id):
            risk_score += 0.4
            risk_factors.append("Currently jailed for suspicious activity")
        
        # Check if monitored
        if validator_id in self.penalty_system.monitored_validators:
            risk_score += 0.2
            risk_factors.append("Under enhanced monitoring")
        
        # Check penalty history
        active_penalties = self.penalty_system.active_penalties.get(validator_id, [])
        if active_penalties:
            risk_score += min(0.3, len(active_penalties) * 0.1)
            risk_factors.append(f"{len(active_penalties)} active penalty records")
        
        # Determine risk level
        if risk_score >= 0.7:
            risk_level = "HIGH"
        elif risk_score >= 0.4:
            risk_level = "MEDIUM"
        elif risk_score >= 0.2:
            risk_level = "LOW"
        else:
            risk_level = "MINIMAL"
        
        return {
            "validator_id": validator_id,
            "risk_score": min(1.0, risk_score),
            "risk_level": risk_level,
            "factors": risk_factors,
            "status": "active" if risk_score < 0.7 else "high_risk",
            "penalty_history": len(active_penalties)
        }
    
    def get_system_health_report(self) -> Dict[str, Any]:
        """Generate comprehensive system health report"""
        
        # Detection stats
        detection_stats = self.detection_engine.get_detection_stats()
        
        # Penalty stats
        penalty_stats = self.penalty_system.get_system_stats()
        
        # Calculate health score
        total_validators = detection_stats.get("total_flagged_validators", 0) + 100  # Estimate
        flagged_percentage = (detection_stats.get("total_flagged_validators", 0) / total_validators * 100)
        
        if flagged_percentage > 20:
            health_status = "CRITICAL - High Sybil Activity"
            health_score = 0.3
        elif flagged_percentage > 10:
            health_status = "WARNING - Elevated Sybil Activity"
            health_score = 0.6
        elif flagged_percentage > 5:
            health_status = "CAUTION - Some Sybil Activity"
            health_score = 0.8
        else:
            health_status = "HEALTHY - Minimal Sybil Activity"
            health_score = 0.95
        
        return {
            "health_status": health_status,
            "health_score": health_score,
            "total_scans_performed": self.total_scans,
            "last_scan": self.last_scan_time,
            "next_scan_in_seconds": self.scan_interval_seconds - (time.time() - self.last_scan_time) if self.last_scan_time else 0,
            "detection_summary": detection_stats,
            "penalty_summary": penalty_stats,
            "flagged_validators_percentage": flagged_percentage,
            "auto_penalize_enabled": self.auto_penalize
        }


# Global instance for easy access
_global_monitor: Optional[IntegratedSybilMonitor] = None


def get_sybil_monitor(
    detection_config: Optional[SybilDetectionConfig] = None,
    auto_penalize: bool = True
) -> IntegratedSybilMonitor:
    """Get or create global Sybil monitor instance"""
    global _global_monitor
    if _global_monitor is None:
        _global_monitor = IntegratedSybilMonitor(detection_config, auto_penalize)
    return _global_monitor
