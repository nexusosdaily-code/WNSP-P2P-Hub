"""
Hybrid AI Routing Controller for NexusOS
=========================================

Intelligently routes WNSP messages through BOTH online and offline paths:
- Online: Traditional internet/HTTP (messaging_routing.py)
- Offline: Peer-to-peer mesh via Bluetooth/WiFi Direct (offline_mesh_transport.py)

AI Decision Criteria:
1. Network availability (is internet accessible?)
2. Message priority (critical messages prefer redundant paths)
3. Peer proximity (nearby peers = offline preferred)
4. Cost optimization (E=hf quantum pricing)
5. Security requirements (censorship resistance)

ZERO BREAKING CHANGES - extends existing systems without modification.
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import time

# Import existing AI routing system (UNCHANGED)
from messaging_routing import (
    AIMessageRouter, get_ai_message_router,
    Message, MessageRoute, MessagePriority, MessageStatus
)

# Import offline mesh transport (NEW)
from offline_mesh_transport import (
    OfflineMeshTransport, OfflinePeer,
    TransportProtocol, ConnectionStatus
)

# Import WNSP protocol (SHARED by both paths)
from wnsp_protocol_v2 import WnspMessageV2, SpectralRegion


class RoutingMode(Enum):
    """Routing path selection modes"""
    ONLINE_ONLY = "online"          # Internet/HTTP only
    OFFLINE_ONLY = "offline"        # Mesh network only
    HYBRID_AUTO = "hybrid_auto"     # AI chooses best path
    HYBRID_REDUNDANT = "redundant"  # Send through BOTH paths


@dataclass
class HybridRoute:
    """
    Enhanced route supporting both online and offline paths.
    Extends MessageRoute without breaking existing code.
    """
    route_id: str
    message_id: str
    
    # Online path (existing)
    online_route: Optional[MessageRoute] = None
    online_available: bool = False
    
    # Offline path (new)
    offline_peers: List[OfflinePeer] = field(default_factory=list)
    offline_hops: int = 0
    offline_available: bool = False
    
    # AI decision
    selected_mode: RoutingMode = RoutingMode.HYBRID_AUTO
    primary_path: str = "online"  # or "offline"
    backup_path: Optional[str] = None
    
    # Cost comparison
    online_cost_nxt: float = 0.0
    offline_cost_nxt: float = 0.0
    
    # Performance metrics
    online_latency_ms: float = 0.0
    offline_latency_ms: float = 0.0
    
    created_at: float = field(default_factory=time.time)


class HybridAIRouter:
    """
    Hybrid AI Routing Controller
    
    Extends existing AIMessageRouter to support offline mesh networking.
    
    Architecture:
    ┌─────────────────────────────────────────────────────────┐
    │  HybridAIRouter (This Module)                           │
    │  ┌────────────────────┐  ┌──────────────────────────┐  │
    │  │  Online Path       │  │  Offline Path            │  │
    │  │  (Existing)        │  │  (New Mesh)              │  │
    │  │                    │  │                          │  │
    │  │  Internet/HTTP     │  │  Bluetooth LE            │  │
    │  │  Validators        │  │  WiFi Direct             │  │
    │  │  DAG Routing       │  │  Multi-hop Relay         │  │
    │  └────────────────────┘  └──────────────────────────┘  │
    │                    ↓              ↓                     │
    │              AI Chooses Best Path                       │
    └─────────────────────────────────────────────────────────┘
    
    ZERO BREAKING CHANGES to existing code:
    - messaging_routing.py: UNCHANGED
    - offline_mesh_transport.py: UNCHANGED
    - This module EXTENDS, doesn't modify
    """
    
    def __init__(
        self,
        offline_transport: Optional[OfflineMeshTransport] = None,
        default_mode: RoutingMode = RoutingMode.HYBRID_AUTO
    ):
        """
        Initialize hybrid AI router.
        
        Args:
            offline_transport: Optional offline mesh transport instance
            default_mode: Default routing mode
        """
        # Existing online AI router (UNCHANGED)
        self.online_router = get_ai_message_router()
        
        # Offline mesh transport (NEW)
        self.offline_transport = offline_transport
        
        # Routing configuration
        self.default_mode = default_mode
        self.force_offline_mode = False  # Emergency mode (no internet)
        
        # Hybrid routing statistics
        self.routes_via_online: int = 0
        self.routes_via_offline: int = 0
        self.routes_via_both: int = 0
        self.total_hybrid_routes: int = 0
        
        # Network health monitoring
        self.internet_available: bool = True
        self.mesh_active: bool = False
        
        print("✅ Hybrid AI Router initialized")
        print(f"   Online routing: {self.online_router is not None}")
        print(f"   Offline mesh: {self.offline_transport is not None}")
        print(f"   Default mode: {default_mode.value}")
    
    # ========================================================================
    # NETWORK AVAILABILITY DETECTION
    # ========================================================================
    
    def check_internet_available(self) -> bool:
        """
        Check if internet connectivity is available.
        
        Real implementation would:
        - Ping known servers
        - Check DNS resolution
        - Test HTTP connectivity
        
        Returns:
            True if internet is accessible
        """
        # Simulated for development
        # In production, this would actually test connectivity
        return self.internet_available
    
    def check_mesh_available(self) -> bool:
        """
        Check if offline mesh network is available.
        
        Returns:
            True if nearby peers are reachable
        """
        if not self.offline_transport:
            return False
        
        # Check if we have any nearby peers
        nearby_peers = [
            p for p in self.offline_transport.nearby_peers.values()
            if p.is_nearby()
        ]
        
        return len(nearby_peers) > 0
    
    # ========================================================================
    # INTELLIGENT PATH SELECTION (AI DECISION MAKING)
    # ========================================================================
    
    def select_optimal_path(
        self,
        message: Message,
        recipient_location: Optional[str] = None
    ) -> Tuple[RoutingMode, str]:
        """
        AI selects optimal routing path based on comprehensive analysis.
        
        Decision Criteria:
        1. Network availability (can't use offline if no internet AND no mesh)
        2. Message priority (CRITICAL → redundant paths)
        3. Peer proximity (nearby recipient → offline preferred)
        4. Cost optimization (E=hf quantum pricing)
        5. Security requirements (censorship resistance → offline)
        6. Latency requirements (offline often faster for nearby peers)
        
        Args:
            message: Message to route
            recipient_location: Optional hint about recipient location
        
        Returns:
            (routing_mode, reasoning)
        """
        internet_ok = self.check_internet_available()
        mesh_ok = self.check_mesh_available()
        
        # Emergency mode: No internet, only mesh
        if not internet_ok and mesh_ok:
            return (
                RoutingMode.OFFLINE_ONLY,
                "Internet unavailable, using mesh network"
            )
        
        # No connectivity at all
        if not internet_ok and not mesh_ok:
            return (
                RoutingMode.ONLINE_ONLY,  # Will fail, but try anyway
                "No connectivity available"
            )
        
        # Only internet available
        if internet_ok and not mesh_ok:
            return (
                RoutingMode.ONLINE_ONLY,
                "Mesh network unavailable, using internet"
            )
        
        # BOTH paths available - AI decides optimal route
        if internet_ok and mesh_ok:
            # Critical messages use BOTH paths for redundancy
            if message.priority == MessagePriority.CRITICAL:
                return (
                    RoutingMode.HYBRID_REDUNDANT,
                    "Critical message - sending via both paths for redundancy"
                )
            
            # Check if recipient is nearby (prefer offline for local)
            if recipient_location and self._is_recipient_nearby(message.recipient):
                return (
                    RoutingMode.OFFLINE_ONLY,
                    "Recipient nearby - offline mesh faster and cheaper"
                )
            
            # Check offline cost vs online cost
            offline_cost = self._estimate_offline_cost(message)
            online_cost = self.online_router.calculate_message_cost(
                message.wavelength, message.priority
            )
            
            # Prefer offline if significantly cheaper
            if offline_cost < online_cost * 0.5:
                return (
                    RoutingMode.OFFLINE_ONLY,
                    f"Offline cheaper ({offline_cost:.6f} vs {online_cost:.6f} NXT)"
                )
            
            # Default: Use online for reliability (existing infrastructure)
            return (
                RoutingMode.ONLINE_ONLY,
                "Online path selected for reliability"
            )
        
        # Fallback
        return (RoutingMode.ONLINE_ONLY, "Default online routing")
    
    def _is_recipient_nearby(self, recipient_id: str) -> bool:
        """Check if recipient is a nearby peer in mesh network."""
        if not self.offline_transport:
            return False
        
        # Check if recipient is in our direct neighbor list
        for peer in self.offline_transport.nearby_peers.values():
            if peer.device_id == recipient_id and peer.is_nearby():
                return True
        
        return False
    
    def _estimate_offline_cost(self, message: Message) -> float:
        """
        Estimate cost of sending message via offline mesh.
        
        Uses same E=hf quantum pricing, but may be cheaper due to:
        - Direct peer-to-peer (no validator fees)
        - Shared infrastructure costs
        """
        # Same base quantum pricing
        online_cost = self.online_router.calculate_message_cost(
            message.wavelength, message.priority
        )
        
        # Offline typically 30% cheaper (no validator overhead)
        offline_cost = online_cost * 0.7
        
        # Additional hop cost if multi-hop routing needed
        if self.offline_transport:
            # Simple heuristic: cost increases with hops
            min_hops = self._estimate_hops_to_recipient(message.recipient)
            hop_cost = min_hops * 0.00001  # Small cost per hop
            offline_cost += hop_cost
        
        return offline_cost
    
    def _estimate_hops_to_recipient(self, recipient_id: str) -> int:
        """Estimate number of hops to reach recipient via mesh."""
        if not self.offline_transport:
            return 999  # Unreachable
        
        # Check direct neighbors (1 hop)
        for peer in self.offline_transport.nearby_peers.values():
            if peer.device_id == recipient_id:
                return peer.hop_count
        
        # Not found in current peer list
        return 999
    
    # ========================================================================
    # UNIFIED ROUTING INTERFACE (Works with both paths)
    # ========================================================================
    
    def route_message_hybrid(
        self,
        message: Message,
        mode_override: Optional[RoutingMode] = None
    ) -> Tuple[bool, str, HybridRoute]:
        """
        Route message using hybrid AI intelligence.
        
        This is the MAIN routing function that:
        1. Analyzes network conditions
        2. Selects optimal path(s)
        3. Routes via online, offline, or both
        4. Returns unified result
        
        Args:
            message: Message to route
            mode_override: Optional override for routing mode
        
        Returns:
            (success, status_message, hybrid_route)
        """
        # Determine routing mode
        if mode_override:
            selected_mode = mode_override
            reasoning = "Mode override by caller"
        else:
            selected_mode, reasoning = self.select_optimal_path(message)
        
        # Create hybrid route object
        hybrid_route = HybridRoute(
            route_id=f"hybrid_route_{message.message_id}",
            message_id=message.message_id,
            selected_mode=selected_mode
        )
        
        # Route based on selected mode
        if selected_mode == RoutingMode.ONLINE_ONLY:
            return self._route_online_only(message, hybrid_route, reasoning)
        
        elif selected_mode == RoutingMode.OFFLINE_ONLY:
            return self._route_offline_only(message, hybrid_route, reasoning)
        
        elif selected_mode == RoutingMode.HYBRID_REDUNDANT:
            return self._route_redundant(message, hybrid_route, reasoning)
        
        else:
            # Default to online
            return self._route_online_only(message, hybrid_route, "Default routing")
    
    def _route_online_only(
        self,
        message: Message,
        hybrid_route: HybridRoute,
        reasoning: str
    ) -> Tuple[bool, str, HybridRoute]:
        """Route message via online internet/HTTP path ONLY."""
        # Use existing AI router (UNCHANGED)
        success, status = self.online_router.route_message_ai(message)
        
        if success:
            # Get the route created by online router
            route_id = f"route_{message.message_id}"
            online_route = self.online_router.active_routes.get(route_id)
            
            hybrid_route.online_route = online_route
            hybrid_route.online_available = True
            hybrid_route.primary_path = "online"
            hybrid_route.online_cost_nxt = message.burn_amount
            
            self.routes_via_online += 1
        
        self.total_hybrid_routes += 1
        
        return (success, f"Online: {status} | {reasoning}", hybrid_route)
    
    def _route_offline_only(
        self,
        message: Message,
        hybrid_route: HybridRoute,
        reasoning: str
    ) -> Tuple[bool, str, HybridRoute]:
        """Route message via offline mesh network ONLY."""
        if not self.offline_transport:
            return (False, "Offline transport not initialized", hybrid_route)
        
        # Convert Message to WnspMessageV2 for offline transport
        wnsp_message = self._convert_to_wnsp(message)
        
        # Send via offline mesh
        success, status = self.offline_transport.send_message_offline(
            message=wnsp_message,
            recipient_id=message.recipient,
            broadcast=False
        )
        
        if success:
            hybrid_route.offline_available = True
            hybrid_route.primary_path = "offline"
            hybrid_route.offline_cost_nxt = message.burn_amount
            hybrid_route.offline_hops = self._estimate_hops_to_recipient(message.recipient)
            
            # Track nearby peers used
            nearby_peers = [
                p for p in self.offline_transport.nearby_peers.values()
                if p.is_nearby()
            ]
            hybrid_route.offline_peers = nearby_peers
            
            self.routes_via_offline += 1
        
        self.total_hybrid_routes += 1
        
        return (success, f"Offline: {status} | {reasoning}", hybrid_route)
    
    def _route_redundant(
        self,
        message: Message,
        hybrid_route: HybridRoute,
        reasoning: str
    ) -> Tuple[bool, str, HybridRoute]:
        """
        Route message via BOTH online and offline paths for redundancy.
        Critical for high-priority messages.
        """
        # Send via online
        online_success, online_status = self.online_router.route_message_ai(message)
        
        # Send via offline
        offline_success = False
        offline_status = "Offline not attempted"
        
        if self.offline_transport:
            wnsp_message = self._convert_to_wnsp(message)
            offline_success, offline_status = self.offline_transport.send_message_offline(
                message=wnsp_message,
                recipient_id=message.recipient,
                broadcast=False
            )
        
        # Update hybrid route
        if online_success:
            route_id = f"route_{message.message_id}"
            online_route = self.online_router.active_routes.get(route_id)
            hybrid_route.online_route = online_route
            hybrid_route.online_available = True
            hybrid_route.online_cost_nxt = message.burn_amount
        
        if offline_success:
            hybrid_route.offline_available = True
            hybrid_route.offline_cost_nxt = message.burn_amount
        
        hybrid_route.primary_path = "both"
        self.routes_via_both += 1
        self.total_hybrid_routes += 1
        
        # Success if at least one path worked
        overall_success = online_success or offline_success
        status = f"Redundant: Online={online_success}, Offline={offline_success} | {reasoning}"
        
        return (overall_success, status, hybrid_route)
    
    def _convert_to_wnsp(self, message: Message) -> WnspMessageV2:
        """
        Convert Message to WnspMessageV2 for offline transport.
        Both online and offline use the same WNSP protocol structure.
        """
        from wnsp_protocol_v2 import WnspEncoderV2
        from wavelength_validator import ModulationType
        
        encoder = WnspEncoderV2()
        
        # Determine spectral region from wavelength
        spectral_region = self._wavelength_to_spectral_region(message.wavelength)
        
        # Create WNSP message
        wnsp_message = WnspMessageV2(
            message_id=message.message_id,
            sender_id=message.sender,
            recipient_id=message.recipient,
            content=message.content_hash,  # Use content hash
            frames=[],  # Simplified
            spectral_region=spectral_region,
            modulation_type=ModulationType.FSK,
            parent_message_ids=[],
            interference_hash="",
            cost_nxt=message.burn_amount,
            quantum_energy=message.energy_contributed,
            frequency_thz=299792458 / (message.wavelength * 1e-9) / 1e12  # Convert to THz
        )
        
        return wnsp_message
    
    def _wavelength_to_spectral_region(self, wavelength_nm: float) -> SpectralRegion:
        """Map wavelength to spectral region."""
        if wavelength_nm < 450:
            return SpectralRegion.VIOLET
        elif wavelength_nm < 495:
            return SpectralRegion.BLUE
        elif wavelength_nm < 570:
            return SpectralRegion.GREEN
        elif wavelength_nm < 590:
            return SpectralRegion.YELLOW
        elif wavelength_nm < 620:
            return SpectralRegion.ORANGE
        elif wavelength_nm < 750:
            return SpectralRegion.RED
        else:
            return SpectralRegion.IR
    
    # ========================================================================
    # STATISTICS & MONITORING
    # ========================================================================
    
    def get_hybrid_stats(self) -> Dict[str, Any]:
        """Get comprehensive hybrid routing statistics."""
        return {
            "total_routes": self.total_hybrid_routes,
            "routes_via_online": self.routes_via_online,
            "routes_via_offline": self.routes_via_offline,
            "routes_via_both": self.routes_via_both,
            "internet_available": self.internet_available,
            "mesh_active": self.check_mesh_available(),
            "default_mode": self.default_mode.value,
            "offline_peers_count": len(self.offline_transport.nearby_peers) if self.offline_transport else 0,
            
            # From online router
            "online_stats": self.online_router.get_routing_stats() if self.online_router else {},
            
            # From offline transport
            "offline_stats": self.offline_transport.get_stats() if self.offline_transport else {}
        }


# ============================================================================
# GLOBAL SINGLETON
# ============================================================================

_hybrid_router = None

def get_hybrid_router(
    offline_transport: Optional[OfflineMeshTransport] = None
) -> HybridAIRouter:
    """Get singleton hybrid AI router instance."""
    global _hybrid_router
    if _hybrid_router is None:
        _hybrid_router = HybridAIRouter(
            offline_transport=offline_transport,
            default_mode=RoutingMode.HYBRID_AUTO
        )
    return _hybrid_router
