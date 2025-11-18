"""
Orbital Transition Engine
Revolutionary physics-based token flow mechanism using electron orbital transition theory.

Instead of "burning" tokens, NexusOS uses quantum electron orbital transitions (n1 → n2)
where energy flows into a TRANSITION_RESERVE pool, mimicking atomic spectroscopy.

Physics Foundation:
- Rydberg Formula: ΔE = 13.6 eV × Z² × (1/n₁² - 1/n₂²)
- Photon Energy: E = hf = hc/λ
- Spectral Lines: Each transition produces a specific wavelength

Economic Model:
- Emission (n2 → n1, n2 > n1): Energy released → TRANSITION_RESERVE
- Absorption (n1 → n2, n2 > n1): Energy absorbed ← TRANSITION_RESERVE
- Net Flow: Maintains 100-year sustainability via reserve caps
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from wavelength_validator import SpectralRegion

# Physical Constants
PLANCK_CONSTANT = 6.62607015e-34  # J·s
SPEED_OF_LIGHT = 299792458  # m/s
ELECTRON_VOLT = 1.602176634e-19  # J (1 eV in Joules)
RYDBERG_ENERGY = 13.6 * ELECTRON_VOLT  # Ground state energy of hydrogen (Joules)

# Bitcoin-style denomination (100M units per NXT)
UNITS_PER_NXT = 100_000_000

# Economic scaling factor - calibrated to match legacy burn rates
# Legacy: MESSAGE_BURN = 5,700 units = 0.000057 NXT
# Physics: Standard message (n=3→2) = 1.89 eV = 3.03e-19 J
# Scaling: 3.03e-19 J → 5,700 units
# Therefore: JOULES_PER_UNIT = 3.03e-19 / 5,700 = 5.32e-23
# For safety, use dynamic calibration in _calculate_transition_rates()
CALIBRATION_TARGET_UNITS = {
    'STANDARD_MESSAGE': 5_700,    # Target cost for n=3→2 transition
    'LINK_SHARE': 2_850,          # Target cost for n=4→2 transition  
    'VIDEO_SHARE': 11_400          # Target cost for n=5→2 transition
}


class QuantumLevel(Enum):
    """
    Principal quantum numbers (n) mapped to spectral regions.
    
    Energy increases as n decreases (n=1 is ground state, highest energy)
    Matches wavelength_validator.SpectralRegion for seamless integration.
    """
    N8_INFRARED = (8, "Infrared", SpectralRegion.IR, 750e-9, 1000e-9)
    N7_RED = (7, "Red", SpectralRegion.RED, 620e-9, 750e-9)
    N6_ORANGE = (6, "Orange", SpectralRegion.ORANGE, 590e-9, 620e-9)
    N5_YELLOW = (5, "Yellow", SpectralRegion.YELLOW, 570e-9, 590e-9)
    N4_GREEN = (4, "Green", SpectralRegion.GREEN, 495e-9, 570e-9)
    N3_BLUE = (3, "Blue", SpectralRegion.BLUE, 450e-9, 495e-9)
    N2_VIOLET = (2, "Violet", SpectralRegion.VIOLET, 380e-9, 450e-9)
    N1_ULTRAVIOLET = (1, "Ultraviolet", SpectralRegion.UV, 100e-9, 400e-9)
    
    def __init__(self, n: int, display_name: str, spectral: SpectralRegion, 
                 min_wavelength: float, max_wavelength: float):
        self.n = n  # Principal quantum number
        self.display_name = display_name
        self.spectral = spectral
        self.min_wavelength = min_wavelength
        self.max_wavelength = max_wavelength
        self.center_wavelength = (min_wavelength + max_wavelength) / 2
    
    @classmethod
    def from_quantum_number(cls, n: int) -> 'QuantumLevel':
        """Get quantum level from principal quantum number"""
        for level in cls:
            if level.n == n:
                return level
        raise ValueError(f"Invalid quantum number: {n}. Must be 1-8.")
    
    @classmethod
    def from_spectral_region(cls, region: SpectralRegion) -> 'QuantumLevel':
        """Get quantum level from spectral region"""
        for level in cls:
            if level.spectral == region:
                return level
        raise ValueError(f"No quantum level for spectral region: {region}")


class TransitionType(Enum):
    """Message types mapped to specific orbital transitions"""
    STANDARD_MESSAGE = ("Standard Message", 3, 2, "Basic text message")
    LINK_SHARE = ("Link Share", 4, 2, "Hyperlink with metadata")
    IMAGE_SHARE = ("Image Share", 5, 3, "Image/photo transmission")
    VIDEO_SHARE = ("Video Share", 5, 2, "Video content transmission")
    VALIDATOR_SETTLEMENT = ("Validator Settlement", 6, 3, "Block validation rewards")
    DEX_TRADE = ("DEX Trade", 6, 4, "Decentralized exchange transaction")
    STAKING_DEPOSIT = ("Staking Deposit", 7, 4, "Validator stake deposit")
    GOVERNANCE_VOTE = ("Governance Vote", 4, 3, "Protocol governance action")
    
    def __init__(self, display_name: str, n_upper: int, n_lower: int, description: str):
        self.display_name = display_name
        self.n_upper = n_upper  # Initial state (higher orbital)
        self.n_lower = n_lower  # Final state (lower orbital)
        self.description = description
        self.is_emission = n_upper > n_lower  # True for emission, False for absorption


@dataclass
class OrbitalTransition:
    """
    Represents a single electron orbital transition.
    
    Physics: When electron drops from n2 → n1, photon is emitted with energy ΔE
    Economics: ΔE (in NXT) flows into TRANSITION_RESERVE instead of being destroyed
    """
    transition_type: TransitionType
    n_initial: int  # Starting orbital
    n_final: int    # Ending orbital
    delta_e_joules: float  # Energy difference (Joules)
    delta_e_nxt: float     # Energy difference (NXT)
    wavelength_nm: float   # Emitted/absorbed photon wavelength
    spectral_region: SpectralRegion
    quantum_level_initial: QuantumLevel
    quantum_level_final: QuantumLevel
    timestamp: datetime = field(default_factory=datetime.now)
    
    @property
    def is_emission(self) -> bool:
        """Emission: n_initial > n_final (energy released)"""
        return self.n_initial > self.n_final
    
    @property
    def is_absorption(self) -> bool:
        """Absorption: n_initial < n_final (energy absorbed)"""
        return self.n_initial < self.n_final
    
    def to_dict(self) -> dict:
        """Serialize transition for ledger"""
        return {
            'transition_type': self.transition_type.display_name,
            'n_initial': self.n_initial,
            'n_final': self.n_final,
            'delta_e_joules': self.delta_e_joules,
            'delta_e_nxt': self.delta_e_nxt,
            'delta_e_units': int(self.delta_e_nxt * UNITS_PER_NXT),
            'wavelength_nm': self.wavelength_nm,
            'spectral_region': self.spectral_region.name,
            'is_emission': self.is_emission,
            'timestamp': self.timestamp.isoformat()
        }


@dataclass
class TransitionLedgerEntry:
    """Record of orbital transition in the quantum ledger"""
    entry_id: str
    user_address: str
    transition: OrbitalTransition
    nxt_units_transferred: int  # Actual units transferred to/from TRANSITION_RESERVE
    reserve_balance_before: int
    reserve_balance_after: int
    block_height: Optional[int] = None
    
    def to_dict(self) -> dict:
        """Serialize ledger entry"""
        return {
            'entry_id': self.entry_id,
            'user_address': self.user_address,
            'transition': self.transition.to_dict(),
            'nxt_units_transferred': self.nxt_units_transferred,
            'reserve_balance_before': self.reserve_balance_before,
            'reserve_balance_after': self.reserve_balance_after,
            'block_height': self.block_height
        }


class OrbitalTransitionEngine:
    """
    Core engine for physics-based token flow using orbital transitions.
    
    Replaces traditional "burn" mechanics with quantum electron transitions:
    - Messages trigger emission transitions (n2 → n1) → energy to TRANSITION_RESERVE
    - Validator rewards trigger absorption transitions (n1 → n2) → energy from TRANSITION_RESERVE
    - Net flow maintains 100-year sustainability
    """
    
    def __init__(self, effective_charge: float = 1.0):
        """
        Initialize orbital transition engine.
        
        Args:
            effective_charge: Z² in Rydberg formula (1.0 for hydrogen-like)
        """
        self.Z_squared = effective_charge
        self.transition_history: List[OrbitalTransition] = []
        self.ledger: List[TransitionLedgerEntry] = []
        
        # NOTE: NO internal reserve balance - native_token.py TRANSITION_RESERVE is single source of truth
        # This makes the engine stateless and prevents dual-ledger accounting bugs
        
        # Pre-calculate transition energies for all message types
        self.transition_rates = self._calculate_transition_rates()
    
    def _calculate_transition_rates(self) -> Dict[TransitionType, Dict[str, Any]]:
        """
        Pre-calculate energy costs for all transition types using Rydberg formula.
        
        Costs are CALIBRATED to match legacy burn rates for economic compatibility:
        - Standard Message (n=3→2): 5,700 units (0.000057 NXT)
        - Link Share (n=4→2): 2,850 units (0.0000285 NXT)  
        - Video Share (n=5→2): 11,400 units (0.000114 NXT)
        
        Wavelengths remain physically accurate (Hα = 656.4nm, Hβ = 486.2nm, etc.)
        
        Returns:
            Dictionary mapping TransitionType to energy values
        """
        rates = {}
        
        for trans_type in TransitionType:
            n_upper = trans_type.n_upper
            n_lower = trans_type.n_lower
            
            # Calculate PHYSICAL energy difference (Joules) - keeps spectroscopy accurate
            delta_e_joules = self.calculate_rydberg_energy(n_lower, n_upper)
            
            # Calculate photon wavelength: λ = hc/ΔE (REAL physics)
            if delta_e_joules > 0:
                wavelength_m = (PLANCK_CONSTANT * SPEED_OF_LIGHT) / delta_e_joules
                wavelength_nm = wavelength_m * 1e9
            else:
                wavelength_nm = 0
            
            # Determine spectral region from wavelength
            spectral_region = self._wavelength_to_spectral_region(wavelength_nm)
            
            # Use CALIBRATED units (economic pricing, not direct physics conversion)
            # This maintains the physics metadata while keeping costs affordable
            if trans_type == TransitionType.STANDARD_MESSAGE:
                delta_e_units = CALIBRATION_TARGET_UNITS['STANDARD_MESSAGE']
            elif trans_type == TransitionType.LINK_SHARE:
                delta_e_units = CALIBRATION_TARGET_UNITS['LINK_SHARE']
            elif trans_type == TransitionType.VIDEO_SHARE:
                delta_e_units = CALIBRATION_TARGET_UNITS['VIDEO_SHARE']
            else:
                # For other types, use relative scaling based on energy ratio
                # Standard message (n=3→2) is the baseline
                baseline_energy = self.calculate_rydberg_energy(2, 3)
                energy_ratio = delta_e_joules / baseline_energy
                delta_e_units = int(CALIBRATION_TARGET_UNITS['STANDARD_MESSAGE'] * energy_ratio)
            
            # Convert units to NXT for display
            delta_e_nxt = delta_e_units / UNITS_PER_NXT
            
            rates[trans_type] = {
                'delta_e_joules': delta_e_joules,
                'delta_e_nxt': delta_e_nxt,
                'delta_e_units': delta_e_units,
                'wavelength_nm': wavelength_nm,
                'spectral_region': spectral_region,
                'n_upper': n_upper,
                'n_lower': n_lower
            }
        
        return rates
    
    def calculate_rydberg_energy(self, n_lower: int, n_upper: int) -> float:
        """
        Calculate energy difference between orbital transitions using Rydberg formula.
        
        Formula: ΔE = 13.6 eV × Z² × (1/n₁² - 1/n₂²)
        
        Args:
            n_lower: Lower energy level (final state)
            n_upper: Upper energy level (initial state)
        
        Returns:
            Energy difference in Joules (positive for emission)
        """
        if n_lower <= 0 or n_upper <= 0:
            raise ValueError("Quantum numbers must be positive integers")
        
        # Rydberg formula
        delta_e_ev = RYDBERG_ENERGY / ELECTRON_VOLT * self.Z_squared * (
            1.0 / (n_lower ** 2) - 1.0 / (n_upper ** 2)
        )
        
        # Convert eV to Joules
        delta_e_joules = delta_e_ev * ELECTRON_VOLT
        
        return delta_e_joules
    
    def _wavelength_to_spectral_region(self, wavelength_nm: float) -> SpectralRegion:
        """Map photon wavelength to spectral region"""
        wavelength_m = wavelength_nm * 1e-9
        
        if wavelength_m < 400e-9:
            return SpectralRegion.UV
        elif wavelength_m < 450e-9:
            return SpectralRegion.VIOLET
        elif wavelength_m < 495e-9:
            return SpectralRegion.BLUE
        elif wavelength_m < 570e-9:
            return SpectralRegion.GREEN
        elif wavelength_m < 590e-9:
            return SpectralRegion.YELLOW
        elif wavelength_m < 620e-9:
            return SpectralRegion.ORANGE
        elif wavelength_m < 750e-9:
            return SpectralRegion.RED
        else:
            return SpectralRegion.IR
    
    def execute_transition(
        self,
        transition_type: TransitionType,
        user_address: str,
        reserve_balance_before: int,
        block_height: Optional[int] = None
    ) -> Tuple[OrbitalTransition, int]:
        """
        Calculate an orbital transition metadata (STATELESS - no internal state mutation).
        
        Caller (native_token.py) is responsible for:
        - Checking sender balance
        - Updating TRANSITION_RESERVE account
        - Maintaining reserve balance consistency
        
        Args:
            transition_type: Type of message/transaction
            user_address: User initiating the transition
            reserve_balance_before: Current TRANSITION_RESERVE balance (from caller)
            block_height: Optional blockchain height
        
        Returns:
            (OrbitalTransition object, NXT units to transfer)
        """
        # Get pre-calculated transition data
        trans_data = self.transition_rates[transition_type]
        
        # Create quantum levels
        n_upper = int(trans_data['n_upper'])
        n_lower = int(trans_data['n_lower'])
        level_initial = QuantumLevel.from_quantum_number(n_upper)
        level_final = QuantumLevel.from_quantum_number(n_lower)
        
        # Create transition object
        spectral_reg = trans_data['spectral_region']
        transition = OrbitalTransition(
            transition_type=transition_type,
            n_initial=n_upper,
            n_final=n_lower,
            delta_e_joules=trans_data['delta_e_joules'],
            delta_e_nxt=trans_data['delta_e_nxt'],
            wavelength_nm=trans_data['wavelength_nm'],
            spectral_region=spectral_reg,
            quantum_level_initial=level_initial,
            quantum_level_final=level_final
        )
        
        # Calculate units to transfer (ensure integer)
        nxt_units = int(trans_data['delta_e_units'])
        
        # Calculate reserve_after (but DON'T mutate any internal state)
        if transition.is_emission:
            # Emission: Energy flows INTO reserve
            reserve_after = reserve_balance_before + nxt_units
        else:
            # Absorption: Energy flows OUT of reserve
            if reserve_balance_before >= nxt_units:
                reserve_after = reserve_balance_before - nxt_units
            else:
                # Insufficient reserve - cap at available
                nxt_units = int(reserve_balance_before)
                reserve_after = 0
        
        # Create ledger entry (for analytics/audit trail)
        entry_id = f"TXN-{len(self.ledger)+1:08d}"
        ledger_entry = TransitionLedgerEntry(
            entry_id=entry_id,
            user_address=user_address,
            transition=transition,
            nxt_units_transferred=int(nxt_units),
            reserve_balance_before=reserve_balance_before,
            reserve_balance_after=reserve_after,
            block_height=block_height
        )
        
        # Record in history (for analytics only - NOT authoritative state)
        self.transition_history.append(transition)
        self.ledger.append(ledger_entry)
        
        return transition, nxt_units
    
    def get_transition_cost(self, transition_type: TransitionType) -> Dict[str, Any]:
        """
        Get the cost (in NXT) for a specific transition type.
        
        Args:
            transition_type: Type of transaction
        
        Returns:
            Dictionary with cost breakdown
        """
        trans_data = self.transition_rates[transition_type]
        spectral_region = trans_data['spectral_region']
        
        return {
            'transition_type': transition_type.display_name,
            'n_transition': f"{trans_data['n_upper']} → {trans_data['n_lower']}",
            'delta_e_nxt': trans_data['delta_e_nxt'],
            'delta_e_units': trans_data['delta_e_units'],
            'wavelength_nm': trans_data['wavelength_nm'],
            'spectral_region': spectral_region.name,
            'photon_color': spectral_region.value[0]
        }
    
    def get_reserve_balance_nxt(self, reserve_balance_units: int) -> float:
        """
        Convert reserve balance from units to NXT (stateless utility).
        
        Args:
            reserve_balance_units: Reserve balance in units (from native_token.py)
        
        Returns:
            Balance in NXT
        """
        return reserve_balance_units / UNITS_PER_NXT
    
    def get_ledger_summary(self, current_reserve_balance_units: int = 0) -> Dict[str, Any]:
        """
        Get summary statistics from transition ledger (analytics only).
        
        Args:
            current_reserve_balance_units: Authoritative reserve balance from native_token.py
        
        Returns:
            Summary statistics
        """
        if not self.ledger:
            return {
                'total_transitions': 0,
                'total_energy_collected_nxt': 0,
                'reserve_balance_nxt': self.get_reserve_balance_nxt(current_reserve_balance_units),
                'emission_count': 0,
                'absorption_count': 0
            }
        
        total_emissions = sum(
            1 for entry in self.ledger if entry.transition.is_emission
        )
        total_absorptions = sum(
            1 for entry in self.ledger if entry.transition.is_absorption
        )
        
        total_energy_units = sum(
            entry.nxt_units_transferred if entry.transition.is_emission 
            else -entry.nxt_units_transferred
            for entry in self.ledger
        )
        
        return {
            'total_transitions': len(self.ledger),
            'total_energy_collected_nxt': total_energy_units / UNITS_PER_NXT,
            'reserve_balance_nxt': self.get_reserve_balance_nxt(current_reserve_balance_units),
            'emission_count': total_emissions,
            'absorption_count': total_absorptions,
            'net_flow_nxt': total_energy_units / UNITS_PER_NXT
        }
    
    def visualize_energy_levels(self) -> Dict[int, Dict[str, Any]]:
        """
        Generate data for Bohr-style energy level diagram.
        
        Returns:
            Dictionary mapping quantum numbers to energy level data
        """
        levels = {}
        
        for n in range(1, 9):
            # Calculate energy of level n (relative to n=∞)
            energy_joules = -RYDBERG_ENERGY * self.Z_squared / (n ** 2)
            energy_ev = energy_joules / ELECTRON_VOLT
            
            level = QuantumLevel.from_quantum_number(n)
            
            levels[n] = {
                'quantum_number': n,
                'energy_joules': energy_joules,
                'energy_ev': energy_ev,
                'spectral_region': level.spectral.name,
                'wavelength_range_nm': (level.min_wavelength * 1e9, level.max_wavelength * 1e9),
                'color': level.name
            }
        
        return levels


# Create global instance
orbital_engine = OrbitalTransitionEngine(effective_charge=1.0)


# Export key components
__all__ = [
    'OrbitalTransitionEngine',
    'QuantumLevel',
    'TransitionType',
    'OrbitalTransition',
    'TransitionLedgerEntry',
    'orbital_engine'
]
