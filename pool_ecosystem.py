"""
NexusOS Pool Ecosystem
Hierarchical economic pool architecture as stated in the Nexus equation

Architecture:
  Reserve Pool → F_floor → Service Pools
  
Layer 1 (Base): Reserve Pool
  - VALIDATOR_POOL
  - TRANSITION_RESERVE  
  - ECOSYSTEM_FUND
  → Supports F_floor (basic human living standards)

Layer 2 (Foundation): F_floor
  - Guaranteed basic living standards for all beneficiaries
  - Minimum survival floor enforced by AI governance
  → Enables all economic activities and service pools

Layer 3 (Services): All Economic Pools
  - DEX Pool (decentralized exchange)
  - Investment Pools (capital allocation)
  - Staking Pools (network security)
  - Bonus Pool (performance rewards)
  - Lottery Pool (chance-based distribution)
  - Environmental Sustainability Pools (climate action)
  - Recycling Pools (circular economy)
  - Product/Service Pools (marketplace economics)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Any
from enum import Enum
from datetime import datetime
import time


class PoolType(Enum):
    """Types of economic pools in the ecosystem"""
    # Layer 1: Reserve pools (support F_floor)
    RESERVE_VALIDATOR = "reserve_validator"
    RESERVE_TRANSITION = "reserve_transition"
    RESERVE_ECOSYSTEM = "reserve_ecosystem"
    
    # Layer 2: F_floor pool (supported by reserves)
    F_FLOOR_POOL = "f_floor_pool"
    
    # Layer 3: Service pools (supported by F_floor)
    DEX_POOL = "dex_pool"
    INVESTMENT_POOL = "investment_pool"
    STAKING_POOL = "staking_pool"
    BONUS_POOL = "bonus_pool"
    LOTTERY_POOL = "lottery_pool"
    ENVIRONMENTAL_POOL = "environmental_pool"
    RECYCLING_POOL = "recycling_pool"
    PRODUCT_SERVICE_POOL = "product_service_pool"
    COMMUNITY_POOL = "community_pool"
    INNOVATION_POOL = "innovation_pool"


class PoolLayer(Enum):
    """Hierarchical layers in pool ecosystem"""
    RESERVE = "reserve"  # Layer 1: Supports F_floor
    FOUNDATION = "foundation"  # Layer 2: F_floor enables services
    SERVICE = "service"  # Layer 3: All economic activities


@dataclass
class PoolMetrics:
    """Performance metrics for a pool"""
    total_deposited: float = 0.0
    total_withdrawn: float = 0.0
    current_balance: float = 0.0
    participant_count: int = 0
    transactions_24h: int = 0
    volume_24h: float = 0.0
    apr_yield: float = 0.0  # Annual percentage rate
    last_updated: float = field(default_factory=time.time)
    
    def calculate_utilization(self) -> float:
        """Calculate pool utilization rate"""
        if self.current_balance == 0:
            return 0.0
        return (self.total_deposited - self.current_balance) / self.total_deposited * 100


@dataclass
class EconomicPool:
    """Represents an economic pool in the NexusOS ecosystem"""
    pool_id: str
    pool_type: PoolType
    pool_layer: PoolLayer
    name: str
    description: str
    metrics: PoolMetrics = field(default_factory=PoolMetrics)
    enabled: bool = True
    supported_by: Optional[str] = None  # Which pool/layer supports this pool
    supports: List[str] = field(default_factory=list)  # Which pools this pool supports
    parameters: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    
    def is_healthy(self) -> bool:
        """Check if pool is healthy and sustainable"""
        if not self.enabled:
            return False
        
        # Check if pool has sufficient balance
        if self.metrics.current_balance < 0:
            return False
        
        # Check utilization - pools shouldn't be over-utilized
        utilization = self.metrics.calculate_utilization()
        if utilization > 95:  # Over 95% utilization is risky
            return False
        
        return True


class PoolEcosystem:
    """
    Manages the hierarchical pool ecosystem
    
    Architecture enforces:
    1. Reserve pools support F_floor
    2. F_floor supports all service pools
    3. AI governs the entire hierarchy
    """
    
    def __init__(self):
        self.pools: Dict[str, EconomicPool] = {}
        self.hierarchy: Dict[PoolLayer, Set[str]] = {
            PoolLayer.RESERVE: set(),
            PoolLayer.FOUNDATION: set(),
            PoolLayer.SERVICE: set()
        }
        
        # Initialize the hierarchical pool system
        self._initialize_pools()
    
    def _initialize_pools(self):
        """Initialize the complete pool hierarchy"""
        
        # Layer 1: Reserve Pools (support F_floor)
        self.create_pool(
            pool_id="VALIDATOR_POOL",
            pool_type=PoolType.RESERVE_VALIDATOR,
            pool_layer=PoolLayer.RESERVE,
            name="Validator Reserve Pool",
            description="Supports validator rewards and network security, backing F_floor",
            supports=["F_FLOOR_POOL"]
        )
        
        self.create_pool(
            pool_id="TRANSITION_RESERVE",
            pool_type=PoolType.RESERVE_TRANSITION,
            pool_layer=PoolLayer.RESERVE,
            name="Transition Reserve Pool",
            description="Collects orbital transition energy, supporting F_floor sustainability",
            supports=["F_FLOOR_POOL"]
        )
        
        self.create_pool(
            pool_id="ECOSYSTEM_FUND",
            pool_type=PoolType.RESERVE_ECOSYSTEM,
            pool_layer=PoolLayer.RESERVE,
            name="Ecosystem Reserve Fund",
            description="Long-term ecosystem development, backing F_floor",
            supports=["F_FLOOR_POOL"]
        )
        
        # Layer 2: F_floor Pool (foundation layer)
        self.create_pool(
            pool_id="F_FLOOR_POOL",
            pool_type=PoolType.F_FLOOR_POOL,
            pool_layer=PoolLayer.FOUNDATION,
            name="F_floor Foundation Pool",
            description="Guaranteed basic human living standards - foundation for all economic activity",
            supported_by="RESERVE_POOLS",
            supports=[
                "DEX_POOL", "INVESTMENT_POOL", "STAKING_POOL", "BONUS_POOL",
                "LOTTERY_POOL", "ENVIRONMENTAL_POOL", "RECYCLING_POOL",
                "PRODUCT_SERVICE_POOL", "COMMUNITY_POOL", "INNOVATION_POOL"
            ]
        )
        
        # Layer 3: Service Pools (enabled by F_floor)
        self.create_pool(
            pool_id="DEX_POOL",
            pool_type=PoolType.DEX_POOL,
            pool_layer=PoolLayer.SERVICE,
            name="DEX Liquidity Pool",
            description="Decentralized exchange liquidity, enabled by F_floor",
            supported_by="F_FLOOR_POOL"
        )
        
        self.create_pool(
            pool_id="INVESTMENT_POOL",
            pool_type=PoolType.INVESTMENT_POOL,
            pool_layer=PoolLayer.SERVICE,
            name="Investment Pool",
            description="Capital allocation and growth opportunities, enabled by F_floor",
            supported_by="F_FLOOR_POOL"
        )
        
        self.create_pool(
            pool_id="STAKING_POOL",
            pool_type=PoolType.STAKING_POOL,
            pool_layer=PoolLayer.SERVICE,
            name="Staking Pool",
            description="Network security through staking, enabled by F_floor",
            supported_by="F_FLOOR_POOL"
        )
        
        self.create_pool(
            pool_id="BONUS_POOL",
            pool_type=PoolType.BONUS_POOL,
            pool_layer=PoolLayer.SERVICE,
            name="Bonus Reward Pool",
            description="Performance-based bonus distribution, enabled by F_floor",
            supported_by="F_FLOOR_POOL"
        )
        
        self.create_pool(
            pool_id="LOTTERY_POOL",
            pool_type=PoolType.LOTTERY_POOL,
            pool_layer=PoolLayer.SERVICE,
            name="Lottery Pool",
            description="Chance-based economic distribution, enabled by F_floor",
            supported_by="F_FLOOR_POOL"
        )
        
        self.create_pool(
            pool_id="ENVIRONMENTAL_POOL",
            pool_type=PoolType.ENVIRONMENTAL_POOL,
            pool_layer=PoolLayer.SERVICE,
            name="Environmental Sustainability Pool",
            description="Climate action and environmental initiatives, enabled by F_floor",
            supported_by="F_FLOOR_POOL"
        )
        
        self.create_pool(
            pool_id="RECYCLING_POOL",
            pool_type=PoolType.RECYCLING_POOL,
            pool_layer=PoolLayer.SERVICE,
            name="Circular Economy Recycling Pool",
            description="Recycling and circular economy programs, enabled by F_floor",
            supported_by="F_FLOOR_POOL"
        )
        
        self.create_pool(
            pool_id="PRODUCT_SERVICE_POOL",
            pool_type=PoolType.PRODUCT_SERVICE_POOL,
            pool_layer=PoolLayer.SERVICE,
            name="Product & Service Marketplace Pool",
            description="Commerce and marketplace economics, enabled by F_floor",
            supported_by="F_FLOOR_POOL"
        )
        
        self.create_pool(
            pool_id="COMMUNITY_POOL",
            pool_type=PoolType.COMMUNITY_POOL,
            pool_layer=PoolLayer.SERVICE,
            name="Community Development Pool",
            description="Community initiatives and social programs, enabled by F_floor",
            supported_by="F_FLOOR_POOL"
        )
        
        self.create_pool(
            pool_id="INNOVATION_POOL",
            pool_type=PoolType.INNOVATION_POOL,
            pool_layer=PoolLayer.SERVICE,
            name="Innovation & R&D Pool",
            description="Research, development, and innovation funding, enabled by F_floor",
            supported_by="F_FLOOR_POOL"
        )
    
    def create_pool(self, pool_id: str, pool_type: PoolType, pool_layer: PoolLayer,
                   name: str, description: str, supported_by: Optional[str] = None,
                   supports: Optional[List[str]] = None) -> EconomicPool:
        """Create a new economic pool"""
        if pool_id in self.pools:
            return self.pools[pool_id]
        
        pool = EconomicPool(
            pool_id=pool_id,
            pool_type=pool_type,
            pool_layer=pool_layer,
            name=name,
            description=description,
            supported_by=supported_by,
            supports=supports or []
        )
        
        self.pools[pool_id] = pool
        self.hierarchy[pool_layer].add(pool_id)
        
        return pool
    
    def get_pool(self, pool_id: str) -> Optional[EconomicPool]:
        """Get pool by ID"""
        return self.pools.get(pool_id)
    
    def get_pools_by_layer(self, layer: PoolLayer) -> List[EconomicPool]:
        """Get all pools in a specific layer"""
        pool_ids = self.hierarchy.get(layer, set())
        return [self.pools[pid] for pid in pool_ids if pid in self.pools]
    
    def verify_f_floor_support(self) -> Dict[str, Any]:
        """
        Verify that F_floor is properly supported by reserves
        and that F_floor properly supports all service pools
        
        Returns:
            Support verification report
        """
        # Get reserve pools
        reserve_pools = self.get_pools_by_layer(PoolLayer.RESERVE)
        reserve_total = sum(pool.metrics.current_balance for pool in reserve_pools)
        
        # Get F_floor pool
        f_floor_pool = self.get_pool("F_FLOOR_POOL")
        if not f_floor_pool:
            return {"error": "F_floor pool not found"}
        
        # Get service pools
        service_pools = self.get_pools_by_layer(PoolLayer.SERVICE)
        service_total = sum(pool.metrics.current_balance for pool in service_pools)
        
        # Verify support structure
        reserve_supports_f_floor = all(
            "F_FLOOR_POOL" in pool.supports for pool in reserve_pools
        )
        
        f_floor_supports_services = all(
            pool.supported_by == "F_FLOOR_POOL" for pool in service_pools
        )
        
        return {
            "reserve_total": reserve_total,
            "f_floor_balance": f_floor_pool.metrics.current_balance,
            "service_total": service_total,
            "reserve_supports_f_floor": reserve_supports_f_floor,
            "f_floor_supports_services": f_floor_supports_services,
            "hierarchy_valid": reserve_supports_f_floor and f_floor_supports_services,
            "service_pool_count": len(service_pools)
        }
    
    def get_ecosystem_health(self) -> Dict[str, Any]:
        """Get overall ecosystem health across all layers"""
        health_by_layer = {}
        
        for layer in PoolLayer:
            pools = self.get_pools_by_layer(layer)
            healthy_count = sum(1 for pool in pools if pool.is_healthy())
            
            health_by_layer[layer.value] = {
                "total_pools": len(pools),
                "healthy_pools": healthy_count,
                "health_percentage": (healthy_count / len(pools) * 100) if pools else 0
            }
        
        # Overall health
        all_pools = list(self.pools.values())
        overall_healthy = sum(1 for pool in all_pools if pool.is_healthy())
        
        return {
            "by_layer": health_by_layer,
            "overall": {
                "total_pools": len(all_pools),
                "healthy_pools": overall_healthy,
                "health_percentage": (overall_healthy / len(all_pools) * 100) if all_pools else 0
            }
        }


# Global pool ecosystem instance
_pool_ecosystem = None

def get_pool_ecosystem() -> PoolEcosystem:
    """Get singleton pool ecosystem instance"""
    global _pool_ecosystem
    if _pool_ecosystem is None:
        _pool_ecosystem = PoolEcosystem()
    return _pool_ecosystem
