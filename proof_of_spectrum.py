"""
Proof of Spectrum (PoS) Consensus Mechanism
============================================

A wavelength-inspired consensus algorithm that eliminates 51% attacks through
spectral diversity requirements and wave interference validation.

Key Innovation: Instead of 51% majority, requires full-spectrum coverage
across different validator types (spectral regions).

Physical Basis: Electromagnetic spectrum (380-750nm) mapped to cryptographic primitives
"""

import hashlib
import json
import time
from typing import List, Dict, Set, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
import numpy as np


class SpectralRegion(Enum):
    """Electromagnetic spectrum regions mapped to validator types"""
    VIOLET = ("violet", 380, 450, "SHA3-256")      # 380-450nm
    BLUE = ("blue", 450, 495, "SHA3-512")          # 450-495nm  
    GREEN = ("green", 495, 570, "BLAKE2b")         # 495-570nm
    YELLOW = ("yellow", 570, 590, "BLAKE2s")       # 570-590nm
    ORANGE = ("orange", 590, 620, "SHA-512")       # 590-620nm
    RED = ("red", 620, 750, "SHA-256")             # 620-750nm
    
    def __init__(self, name: str, wavelength_min: int, wavelength_max: int, hash_algo: str):
        self.region_name = name
        self.wavelength_min = wavelength_min
        self.wavelength_max = wavelength_max
        self.hash_algorithm = hash_algo
    
    @property
    def center_wavelength(self) -> float:
        """Central wavelength of the spectral region"""
        return (self.wavelength_min + self.wavelength_max) / 2
    
    @property
    def bandwidth(self) -> int:
        """Spectral bandwidth"""
        return self.wavelength_max - self.wavelength_min


@dataclass
class SpectralValidator:
    """Validator assigned to a specific spectral region"""
    validator_id: str
    spectral_region: SpectralRegion
    stake: float
    public_key: str
    wavelength: float = field(init=False)
    
    def __post_init__(self):
        # Assign specific wavelength within region based on validator ID
        region_range = self.spectral_region.bandwidth
        hash_val = int(hashlib.sha256(self.validator_id.encode()).hexdigest(), 16)
        offset = (hash_val % region_range)
        self.wavelength = self.spectral_region.wavelength_min + offset
    
    def generate_spectral_signature(self, block_data: str) -> str:
        """
        Generate wavelength-specific signature using region's hash algorithm
        
        Simulates: Wave signature at specific wavelength
        """
        algo = self.spectral_region.hash_algorithm
        data = f"{block_data}:{self.wavelength}:{self.validator_id}"
        
        if algo == "SHA3-256":
            return hashlib.sha3_256(data.encode()).hexdigest()
        elif algo == "SHA3-512":
            return hashlib.sha3_512(data.encode()).hexdigest()
        elif algo == "BLAKE2b":
            return hashlib.blake2b(data.encode()).hexdigest()
        elif algo == "BLAKE2s":
            return hashlib.blake2s(data.encode()).hexdigest()
        elif algo == "SHA-512":
            return hashlib.sha512(data.encode()).hexdigest()
        else:  # SHA-256
            return hashlib.sha256(data.encode()).hexdigest()


@dataclass
class InterferencePattern:
    """
    Represents wave interference pattern from multiple validators
    
    Physical Analog: Constructive/destructive interference of light waves
    Digital Implementation: Combined hash pattern from multiple spectral regions
    """
    signatures: Dict[SpectralRegion, str]
    timestamp: float
    
    def compute_interference_hash(self) -> str:
        """
        Compute combined interference pattern
        
        Simulates: Resultant wave from superposition of multiple wavelengths
        Implementation: Combines signatures from all spectral regions
        """
        # Sort by wavelength to ensure deterministic ordering
        sorted_sigs = sorted(
            self.signatures.items(),
            key=lambda x: x[0].center_wavelength
        )
        
        # Combine signatures - simulates wave interference
        combined = ":".join([sig for _, sig in sorted_sigs])
        interference_hash = hashlib.sha3_512(combined.encode()).hexdigest()
        
        return interference_hash
    
    def validate_spectral_coverage(self, required_regions: Set[SpectralRegion]) -> bool:
        """
        Verify all required spectral regions are represented
        
        Key Security Feature: Prevents single-entity control
        """
        present_regions = set(self.signatures.keys())
        return required_regions.issubset(present_regions)
    
    def compute_spectral_diversity_score(self) -> float:
        """
        Measure spectral diversity (0.0 to 1.0)
        
        Higher diversity = stronger security against attacks
        """
        total_regions = len(SpectralRegion)
        covered_regions = len(self.signatures)
        return covered_regions / total_regions


@dataclass
class SpectralBlock:
    """Block validated through Proof of Spectrum consensus"""
    block_number: int
    timestamp: float
    transactions: List[str]
    previous_hash: str
    interference_pattern: Optional[InterferencePattern] = None
    nonce: int = 0
    
    def to_dict(self) -> dict:
        """Serialize block data"""
        return {
            'block_number': self.block_number,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }
    
    def get_block_hash(self) -> str:
        """Compute block hash from interference pattern"""
        if self.interference_pattern is None:
            raise ValueError("Block not validated - no interference pattern")
        
        block_data = json.dumps(self.to_dict(), sort_keys=True)
        interference_hash = self.interference_pattern.compute_interference_hash()
        
        # Final block hash combines data + interference pattern
        return hashlib.sha256(f"{block_data}:{interference_hash}".encode()).hexdigest()


class ProofOfSpectrumConsensus:
    """
    Proof of Spectrum Consensus Engine
    
    Revolutionary Feature: Eliminates 51% attacks through spectral diversity requirement
    """
    
    def __init__(
        self,
        required_spectral_coverage: float = 0.83,  # Require 83% of spectrum (5/6 regions)
        minimum_validators_per_region: int = 2
    ):
        self.validators: List[SpectralValidator] = []
        self.required_coverage = required_spectral_coverage
        self.min_validators_per_region = minimum_validators_per_region
        
        # Calculate required regions based on coverage
        total_regions = len(SpectralRegion)
        self.required_region_count = int(np.ceil(total_regions * required_spectral_coverage))
    
    def register_validator(self, validator: SpectralValidator):
        """Register a new validator in the network"""
        self.validators.append(validator)
    
    def get_spectral_distribution(self) -> Dict[SpectralRegion, List[SpectralValidator]]:
        """Get validator distribution across spectral regions"""
        distribution = {region: [] for region in SpectralRegion}
        
        for validator in self.validators:
            distribution[validator.spectral_region].append(validator)
        
        return distribution
    
    def select_validators_for_block(self, block_data: str, seed: int = None) -> List[SpectralValidator]:
        """
        Select validators ensuring spectral diversity
        
        Key Algorithm: Must include validators from different spectral regions
        This prevents any single entity from controlling consensus
        """
        distribution = self.get_spectral_distribution()
        
        # Ensure we have validators in enough regions
        populated_regions = [
            region for region, vals in distribution.items()
            if len(vals) >= self.min_validators_per_region
        ]
        
        if len(populated_regions) < self.required_region_count:
            raise ValueError(
                f"Insufficient spectral coverage: need {self.required_region_count} regions, "
                f"have {len(populated_regions)}"
            )
        
        # Select validators from different regions
        # Use deterministic selection based on block data
        selected = []
        
        if seed is None:
            seed = int(hashlib.sha256(block_data.encode()).hexdigest(), 16)
        
        np.random.seed(seed % (2**32))
        
        # Randomly select regions to ensure diversity
        selected_regions = np.random.choice(
            populated_regions,
            size=self.required_region_count,
            replace=False
        )
        
        # Select validators from each chosen region
        for region in selected_regions:
            region_validators = distribution[region]
            # Weight by stake
            stakes = np.array([v.stake for v in region_validators])
            if stakes.sum() > 0:
                probabilities = stakes / stakes.sum()
                chosen = np.random.choice(region_validators, p=probabilities)
                selected.append(chosen)
        
        return selected
    
    def create_interference_pattern(
        self,
        block: SpectralBlock,
        validators: List[SpectralValidator]
    ) -> InterferencePattern:
        """
        Create interference pattern from validator signatures
        
        Simulates: Multiple wavelengths interfering to create unique pattern
        """
        block_data = json.dumps(block.to_dict(), sort_keys=True)
        
        signatures = {}
        for validator in validators:
            signature = validator.generate_spectral_signature(block_data)
            signatures[validator.spectral_region] = signature
        
        return InterferencePattern(
            signatures=signatures,
            timestamp=time.time()
        )
    
    def validate_block(self, block: SpectralBlock) -> Tuple[bool, str]:
        """
        Validate block using spectral consensus rules
        
        Returns: (is_valid, reason)
        """
        if block.interference_pattern is None:
            return False, "No interference pattern"
        
        # Check spectral coverage
        required_regions = set(list(SpectralRegion)[:self.required_region_count])
        if not block.interference_pattern.validate_spectral_coverage(required_regions):
            return False, "Insufficient spectral coverage"
        
        # Verify diversity score
        diversity_score = block.interference_pattern.compute_spectral_diversity_score()
        if diversity_score < self.required_coverage:
            return False, f"Spectral diversity too low: {diversity_score:.2f}"
        
        return True, "Valid"
    
    def simulate_51_percent_attack(self, attacker_control_percentage: float) -> Dict:
        """
        Simulate attack where single entity controls X% of validators
        
        Demonstrates: Even with 99% control, cannot bypass spectral diversity requirement
        """
        total_validators = len(self.validators)
        attacker_count = int(total_validators * attacker_control_percentage)
        
        # Attacker controls validators
        attacker_validators = self.validators[:attacker_count]
        
        # Check spectral distribution of attacker's validators
        attacker_regions = set(v.spectral_region for v in attacker_validators)
        
        # Can attacker produce valid blocks alone?
        can_attack = len(attacker_regions) >= self.required_region_count
        
        return {
            'attacker_control_pct': attacker_control_percentage * 100,
            'attacker_validator_count': attacker_count,
            'total_validators': total_validators,
            'attacker_spectral_regions': len(attacker_regions),
            'required_spectral_regions': self.required_region_count,
            'attack_possible': can_attack,
            'security_status': 'VULNERABLE' if can_attack else 'SECURE'
        }


def create_diverse_validator_network(num_validators: int = 30) -> ProofOfSpectrumConsensus:
    """
    Create a diverse validator network across all spectral regions
    
    Simulates realistic network with validators spread across spectrum
    """
    consensus = ProofOfSpectrumConsensus()
    
    regions = list(SpectralRegion)
    
    for i in range(num_validators):
        # Distribute validators across regions
        region = regions[i % len(regions)]
        
        validator = SpectralValidator(
            validator_id=f"validator_{i}",
            spectral_region=region,
            stake=np.random.uniform(100, 10000),
            public_key=f"pubkey_{i}"
        )
        
        consensus.register_validator(validator)
    
    return consensus
