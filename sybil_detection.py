"""
Sybil Attack Detection System for NexusOS
==========================================

Multi-dimensional clustering analysis to detect coordinated validator attacks.
Uses 7 detection vectors to identify when multiple validators are controlled
by a single entity across spectral regions.

Detection Vectors:
1. Temporal Clustering - Registration timestamp patterns
2. Behavioral Clustering - Voting pattern correlation
3. Economic Clustering - Funding source analysis
4. Network Topology Clustering - Connection patterns
5. Spectral Clustering - Cross-region coordination
6. Device Fingerprinting - Timing and computational signatures
7. Statistical Analysis - Community detection algorithms
"""

import time
import hashlib
import numpy as np
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict
from datetime import datetime
import networkx as nx
from scipy.stats import pearsonr
from sklearn.cluster import DBSCAN
from enum import Enum


class ClusterSeverity(Enum):
    """Severity levels for detected clusters"""
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class ValidatorProfile:
    """Complete profile of a validator for Sybil analysis"""
    validator_id: str
    address: str
    spectral_region: str
    stake_amount: float
    registration_time: float
    
    # Behavioral metrics
    votes_cast: List[Dict] = field(default_factory=list)  # {proposal_id, choice, timestamp}
    blocks_created: List[Dict] = field(default_factory=list)  # {block_id, timestamp, parents}
    
    # Economic metrics
    funding_tx_id: Optional[str] = None  # Transaction that funded this validator
    funding_source: Optional[str] = None  # Address that sent the stake
    funding_timestamp: Optional[float] = None
    
    # Network metrics
    connected_peers: Set[str] = field(default_factory=set)
    avg_latency_ms: float = 0.0
    ip_hash: Optional[str] = None  # Hashed IP for privacy
    isp_hash: Optional[str] = None  # Hashed ISP for pattern detection
    
    # Device fingerprint
    block_timing_signature: List[float] = field(default_factory=list)  # Milliseconds between blocks
    computational_signature: float = 0.0  # Average computation time


@dataclass
class ClusterDetectionResult:
    """Result of cluster detection analysis"""
    cluster_id: str
    validators: List[str]
    severity: ClusterSeverity
    confidence_score: float  # 0.0 to 1.0
    detection_vectors: Dict[str, float]  # Which vectors detected this cluster
    evidence: List[str]
    recommended_action: str
    timestamp: float = field(default_factory=time.time)


class TemporalClusterDetector:
    """Detects validators registered in suspicious time windows"""
    
    def __init__(self, window_seconds: float = 3600):
        """
        Args:
            window_seconds: Time window to consider suspicious (default 1 hour)
        """
        self.window_seconds = window_seconds
    
    def detect(self, profiles: List[ValidatorProfile]) -> Dict[str, List[str]]:
        """
        Detect temporal clusters of validator registrations.
        
        Returns:
            Dict mapping cluster_id to list of validator_ids
        """
        if len(profiles) < 2:
            return {}
        
        # Sort by registration time
        sorted_profiles = sorted(profiles, key=lambda p: p.registration_time)
        
        clusters = {}
        cluster_id = 0
        
        i = 0
        while i < len(sorted_profiles):
            current_cluster = [sorted_profiles[i].validator_id]
            base_time = sorted_profiles[i].registration_time
            
            # Find all validators within time window
            j = i + 1
            while j < len(sorted_profiles):
                time_diff = sorted_profiles[j].registration_time - base_time
                if time_diff <= self.window_seconds:
                    current_cluster.append(sorted_profiles[j].validator_id)
                    j += 1
                else:
                    break
            
            # Flag as suspicious if >= 3 validators in window
            if len(current_cluster) >= 3:
                clusters[f"temporal_{cluster_id}"] = current_cluster
                cluster_id += 1
            
            i = j if j > i + 1 else i + 1
        
        return clusters
    
    def calculate_score(self, cluster_size: int, window_seconds: float) -> float:
        """Calculate suspicion score for temporal cluster"""
        # More validators in shorter time = higher score
        density = cluster_size / (window_seconds / 60)  # validators per minute
        return min(1.0, density / 10.0)  # Normalize to 0-1


class BehavioralClusterDetector:
    """Detects validators with correlated voting patterns"""
    
    def __init__(self, correlation_threshold: float = 0.8):
        """
        Args:
            correlation_threshold: Minimum correlation to consider suspicious
        """
        self.correlation_threshold = correlation_threshold
    
    def detect(self, profiles: List[ValidatorProfile]) -> Dict[str, List[str]]:
        """
        Detect behavioral clusters through voting correlation.
        
        Returns:
            Dict mapping cluster_id to list of validator_ids
        """
        if len(profiles) < 2:
            return {}
        
        # Build voting matrix
        proposal_ids = set()
        for profile in profiles:
            for vote in profile.votes_cast:
                proposal_ids.add(vote['proposal_id'])
        
        if not proposal_ids:
            return {}
        
        proposal_list = sorted(list(proposal_ids))
        
        # Create vote vectors for each validator
        vote_vectors = {}
        for profile in profiles:
            vector = []
            vote_map = {v['proposal_id']: v['choice'] for v in profile.votes_cast}
            
            for prop_id in proposal_list:
                if prop_id in vote_map:
                    # Encode: APPROVE=1, REJECT=-1, ABSTAIN=0
                    choice = vote_map[prop_id]
                    value = 1 if choice == "APPROVE" else (-1 if choice == "REJECT" else 0)
                    vector.append(value)
                else:
                    vector.append(0)  # Didn't vote
            
            if any(v != 0 for v in vector):
                vote_vectors[profile.validator_id] = np.array(vector)
        
        # Calculate pairwise correlations
        clusters = {}
        cluster_id = 0
        processed = set()
        
        for val_id1, vec1 in vote_vectors.items():
            if val_id1 in processed:
                continue
            
            cluster = [val_id1]
            processed.add(val_id1)
            
            for val_id2, vec2 in vote_vectors.items():
                if val_id2 in processed or val_id1 == val_id2:
                    continue
                
                # Calculate Pearson correlation
                if len(vec1) >= 3:  # Need at least 3 votes for meaningful correlation
                    try:
                        corr, _ = pearsonr(vec1, vec2)
                        if corr >= self.correlation_threshold:
                            cluster.append(val_id2)
                            processed.add(val_id2)
                    except:
                        pass
            
            if len(cluster) >= 3:
                clusters[f"behavioral_{cluster_id}"] = cluster
                cluster_id += 1
        
        return clusters
    
    def calculate_score(self, correlation: float, cluster_size: int) -> float:
        """Calculate suspicion score for behavioral cluster"""
        # Perfect correlation + large cluster = very suspicious
        size_factor = min(1.0, cluster_size / 20.0)
        return (correlation * 0.7) + (size_factor * 0.3)


class EconomicClusterDetector:
    """Detects validators funded from the same source"""
    
    def __init__(self):
        self.funding_graph = nx.DiGraph()
    
    def detect(self, profiles: List[ValidatorProfile]) -> Dict[str, List[str]]:
        """
        Detect economic clusters through funding source analysis.
        
        Returns:
            Dict mapping cluster_id to list of validator_ids
        """
        if len(profiles) < 2:
            return {}
        
        # Group by funding source
        funding_groups = defaultdict(list)
        for profile in profiles:
            if profile.funding_source:
                funding_groups[profile.funding_source].append(profile.validator_id)
        
        # Flag groups with >= 3 validators
        clusters = {}
        cluster_id = 0
        for source, validators in funding_groups.items():
            if len(validators) >= 3:
                clusters[f"economic_{cluster_id}"] = validators
                cluster_id += 1
        
        return clusters
    
    def calculate_score(self, cluster_size: int, time_span: float) -> float:
        """Calculate suspicion score for economic cluster"""
        # Many validators funded quickly from same source = suspicious
        size_score = min(1.0, cluster_size / 50.0)
        time_score = 1.0 if time_span < 3600 else 0.5  # Within 1 hour vs longer
        return (size_score * 0.6) + (time_score * 0.4)


class NetworkTopologyDetector:
    """Detects validators with similar network characteristics"""
    
    def __init__(self, similarity_threshold: float = 0.7):
        """
        Args:
            similarity_threshold: Minimum similarity to cluster
        """
        self.similarity_threshold = similarity_threshold
    
    def detect(self, profiles: List[ValidatorProfile]) -> Dict[str, List[str]]:
        """
        Detect network topology clusters.
        
        Returns:
            Dict mapping cluster_id to list of validator_ids
        """
        if len(profiles) < 2:
            return {}
        
        # Group by ISP hash (same ISP)
        isp_groups = defaultdict(list)
        for profile in profiles:
            if profile.isp_hash:
                isp_groups[profile.isp_hash].append(profile.validator_id)
        
        # Group by IP subnet (first 3 octets when hashed)
        ip_groups = defaultdict(list)
        for profile in profiles:
            if profile.ip_hash:
                # Use first 8 chars of hash as subnet proxy
                subnet = profile.ip_hash[:8]
                ip_groups[subnet].append(profile.validator_id)
        
        clusters = {}
        cluster_id = 0
        
        # ISP-based clusters
        for isp, validators in isp_groups.items():
            if len(validators) >= 5:  # More validators in same ISP
                clusters[f"network_isp_{cluster_id}"] = validators
                cluster_id += 1
        
        # IP-based clusters
        for subnet, validators in ip_groups.items():
            if len(validators) >= 3:  # Validators in same subnet
                clusters[f"network_ip_{cluster_id}"] = validators
                cluster_id += 1
        
        return clusters
    
    def calculate_score(self, cluster_size: int, network_type: str) -> float:
        """Calculate suspicion score for network cluster"""
        if network_type == "ip":
            # Same IP subnet is very suspicious
            return min(1.0, 0.5 + (cluster_size / 10.0))
        else:  # ISP
            # Same ISP less suspicious but still notable
            return min(1.0, 0.3 + (cluster_size / 30.0))


class SpectralClusterDetector:
    """Detects coordinated validators across spectral regions"""
    
    def __init__(self, required_regions: int = 5):
        """
        Args:
            required_regions: Minimum spectral regions to consider coordinated
        """
        self.required_regions = required_regions
    
    def detect(self, profiles: List[ValidatorProfile], 
               behavioral_clusters: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """
        Detect spectral clusters - coordinated validators across regions.
        Uses behavioral clusters to find validators that vote together
        AND span multiple spectral regions.
        
        Returns:
            Dict mapping cluster_id to list of validator_ids
        """
        clusters = {}
        cluster_id = 0
        
        # For each behavioral cluster, check spectral coverage
        for behavior_cluster_id, validator_ids in behavioral_clusters.items():
            # Get spectral regions represented
            regions = set()
            profile_map = {p.validator_id: p for p in profiles}
            
            for val_id in validator_ids:
                if val_id in profile_map:
                    regions.add(profile_map[val_id].spectral_region)
            
            # If cluster spans many regions, it's a Sybil attack
            if len(regions) >= self.required_regions:
                clusters[f"spectral_{cluster_id}"] = validator_ids
                cluster_id += 1
        
        return clusters
    
    def calculate_score(self, regions_covered: int, cluster_size: int) -> float:
        """Calculate suspicion score for spectral cluster"""
        # Covering all regions with coordinated behavior = critical
        region_score = regions_covered / 6.0  # Assuming 6 total regions
        size_score = min(1.0, cluster_size / 50.0)
        return (region_score * 0.8) + (size_score * 0.2)


class DeviceFingerprintDetector:
    """Detects validators with identical device signatures"""
    
    def __init__(self, timing_tolerance_ms: float = 5.0):
        """
        Args:
            timing_tolerance_ms: Tolerance for timing similarity
        """
        self.timing_tolerance_ms = timing_tolerance_ms
    
    def detect(self, profiles: List[ValidatorProfile]) -> Dict[str, List[str]]:
        """
        Detect device fingerprint clusters through timing analysis.
        
        Returns:
            Dict mapping cluster_id to list of validator_ids
        """
        if len(profiles) < 2:
            return {}
        
        # Group validators by similar timing signatures
        # Use DBSCAN clustering on timing patterns
        timing_profiles = []
        validator_indices = []
        
        for profile in profiles:
            if len(profile.block_timing_signature) >= 3:
                # Use mean and std of timing as features
                mean_timing = np.mean(profile.block_timing_signature)
                std_timing = np.std(profile.block_timing_signature)
                timing_profiles.append([mean_timing, std_timing])
                validator_indices.append(profile.validator_id)
        
        if len(timing_profiles) < 2:
            return {}
        
        # Apply DBSCAN clustering
        X = np.array(timing_profiles)
        clustering = DBSCAN(eps=self.timing_tolerance_ms, min_samples=3).fit(X)
        
        # Extract clusters
        clusters = {}
        for label in set(clustering.labels_):
            if label == -1:  # Noise points
                continue
            
            cluster_validators = [
                validator_indices[i] 
                for i, lbl in enumerate(clustering.labels_) 
                if lbl == label
            ]
            
            if len(cluster_validators) >= 3:
                clusters[f"device_{label}"] = cluster_validators
        
        return clusters
    
    def calculate_score(self, cluster_size: int, timing_variance: float) -> float:
        """Calculate suspicion score for device cluster"""
        # Identical timing + many validators = very suspicious
        size_score = min(1.0, cluster_size / 20.0)
        variance_score = 1.0 - min(1.0, timing_variance / 10.0)
        return (size_score * 0.5) + (variance_score * 0.5)


@dataclass
class SybilDetectionConfig:
    """Configuration for Sybil detection system"""
    temporal_window_seconds: float = 3600  # 1 hour
    behavioral_correlation_threshold: float = 0.8
    network_similarity_threshold: float = 0.7
    spectral_required_regions: int = 5
    device_timing_tolerance_ms: float = 5.0
    
    # Scoring weights
    temporal_weight: float = 0.15
    behavioral_weight: float = 0.25
    economic_weight: float = 0.20
    network_weight: float = 0.15
    spectral_weight: float = 0.20
    device_weight: float = 0.05


class SybilDetectionEngine:
    """
    Main Sybil detection engine coordinating all detection vectors.
    """
    
    def __init__(self, config: Optional[SybilDetectionConfig] = None):
        self.config = config or SybilDetectionConfig()
        
        # Initialize detectors
        self.temporal_detector = TemporalClusterDetector(
            self.config.temporal_window_seconds
        )
        self.behavioral_detector = BehavioralClusterDetector(
            self.config.behavioral_correlation_threshold
        )
        self.economic_detector = EconomicClusterDetector()
        self.network_detector = NetworkTopologyDetector(
            self.config.network_similarity_threshold
        )
        self.spectral_detector = SpectralClusterDetector(
            self.config.spectral_required_regions
        )
        self.device_detector = DeviceFingerprintDetector(
            self.config.device_timing_tolerance_ms
        )
        
        # Detection history
        self.detection_history: List[ClusterDetectionResult] = []
    
    def analyze_validators(
        self, 
        profiles: List[ValidatorProfile]
    ) -> List[ClusterDetectionResult]:
        """
        Run complete Sybil detection analysis on validator profiles.
        
        Returns:
            List of detected clusters with severity and evidence
        """
        if len(profiles) < 2:
            return []
        
        # Run all detectors
        temporal_clusters = self.temporal_detector.detect(profiles)
        behavioral_clusters = self.behavioral_detector.detect(profiles)
        economic_clusters = self.economic_detector.detect(profiles)
        network_clusters = self.network_detector.detect(profiles)
        spectral_clusters = self.spectral_detector.detect(profiles, behavioral_clusters)
        device_clusters = self.device_detector.detect(profiles)
        
        # Aggregate all detections
        all_clusters = {}
        
        # Merge clusters by validator overlap
        cluster_sources = {
            'temporal': (temporal_clusters, self.config.temporal_weight),
            'behavioral': (behavioral_clusters, self.config.behavioral_weight),
            'economic': (economic_clusters, self.config.economic_weight),
            'network': (network_clusters, self.config.network_weight),
            'spectral': (spectral_clusters, self.config.spectral_weight),
            'device': (device_clusters, self.config.device_weight)
        }
        
        # Build unified cluster index
        validator_to_clusters = defaultdict(set)
        for source_name, (clusters, _) in cluster_sources.items():
            for cluster_id, validators in clusters.items():
                for val_id in validators:
                    validator_to_clusters[val_id].add((source_name, cluster_id))
        
        # Group validators that appear together in multiple detection vectors
        processed = set()
        results = []
        
        for val_id, source_clusters in validator_to_clusters.items():
            if val_id in processed:
                continue
            
            # Find all validators that share detection vectors with this one
            cluster_validators = {val_id}
            processed.add(val_id)
            
            for other_val, other_sources in validator_to_clusters.items():
                if other_val in processed:
                    continue
                
                # Check overlap in detection sources
                overlap = source_clusters & other_sources
                if len(overlap) >= 2:  # Detected by at least 2 same vectors
                    cluster_validators.add(other_val)
                    processed.add(other_val)
            
            if len(cluster_validators) >= 3:
                # Calculate composite score and severity
                result = self._create_detection_result(
                    list(cluster_validators),
                    profiles,
                    cluster_sources
                )
                results.append(result)
                self.detection_history.append(result)
        
        return sorted(results, key=lambda r: r.confidence_score, reverse=True)
    
    def _create_detection_result(
        self,
        validator_ids: List[str],
        profiles: List[ValidatorProfile],
        cluster_sources: Dict
    ) -> ClusterDetectionResult:
        """Create detection result with evidence and scoring"""
        
        profile_map = {p.validator_id: p for p in profiles}
        
        # Calculate scores from each detection vector
        detection_vectors = {}
        evidence = []
        total_score = 0.0
        
        for source_name, (clusters, weight) in cluster_sources.items():
            # Check if this cluster was detected by this vector
            for cluster_id, cluster_vals in clusters.items():
                overlap = set(validator_ids) & set(cluster_vals)
                if len(overlap) >= 3:
                    detection_vectors[source_name] = weight
                    total_score += weight
                    evidence.append(f"Detected by {source_name} vector ({len(overlap)} validators)")
        
        # Additional evidence
        regions = set(profile_map[v].spectral_region for v in validator_ids if v in profile_map)
        if len(regions) >= 5:
            evidence.append(f"Spans {len(regions)} spectral regions - CRITICAL")
            total_score += 0.2
        
        # Determine severity
        if total_score >= 0.8:
            severity = ClusterSeverity.CRITICAL
            action = "IMMEDIATE SLASH 50% + PERMANENT BAN"
        elif total_score >= 0.6:
            severity = ClusterSeverity.HIGH
            action = "SLASH 30% + TEMPORARY JAIL 48h"
        elif total_score >= 0.4:
            severity = ClusterSeverity.MEDIUM
            action = "SLASH 20% + TEMPORARY JAIL 24h + MONITORING"
        elif total_score >= 0.2:
            severity = ClusterSeverity.LOW
            action = "WARNING + REDUCED VOTING WEIGHT + MONITORING"
        else:
            severity = ClusterSeverity.NONE
            action = "MONITOR ONLY"
        
        cluster_id = hashlib.sha256(
            "".join(sorted(validator_ids)).encode()
        ).hexdigest()[:12]
        
        return ClusterDetectionResult(
            cluster_id=cluster_id,
            validators=validator_ids,
            severity=severity,
            confidence_score=min(1.0, total_score),
            detection_vectors=detection_vectors,
            evidence=evidence,
            recommended_action=action
        )
    
    def get_detection_stats(self) -> Dict[str, Any]:
        """Get statistics on detection history"""
        if not self.detection_history:
            return {
                "total_detections": 0,
                "severity_breakdown": {},
                "average_cluster_size": 0,
                "total_flagged_validators": 0
            }
        
        severity_counts = defaultdict(int)
        total_validators = set()
        
        for result in self.detection_history:
            severity_counts[result.severity.name] += 1
            total_validators.update(result.validators)
        
        avg_size = np.mean([len(r.validators) for r in self.detection_history])
        
        return {
            "total_detections": len(self.detection_history),
            "severity_breakdown": dict(severity_counts),
            "average_cluster_size": avg_size,
            "total_flagged_validators": len(total_validators),
            "recent_detections": [
                {
                    "cluster_id": r.cluster_id,
                    "size": len(r.validators),
                    "severity": r.severity.name,
                    "confidence": r.confidence_score,
                    "timestamp": r.timestamp
                }
                for r in self.detection_history[-10:]
            ]
        }
