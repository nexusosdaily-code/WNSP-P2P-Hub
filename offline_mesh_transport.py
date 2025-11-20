"""
Offline Mesh Transport Layer for NexusOS
==========================================

Physical layer enabling direct phone-to-phone communication WITHOUT internet/WiFi/cellular data.
Integrates with existing WNSP v2.0 protocol and DAG messaging infrastructure.

Supported Protocols:
- Bluetooth Low Energy (BLE) Mesh: ~100m range, low power
- WiFi Direct (P2P): ~200m range, higher bandwidth
- NFC: <10cm range, secure pairing

Key Innovation: Makes existing WNSP DAG mesh work OFFLINE using quantum wavelength physics
as the logical layer and Bluetooth/WiFi Direct as the physical transport.
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import time
import hashlib
import json
from datetime import datetime

# Import existing WNSP infrastructure
from wnsp_protocol_v2 import WnspMessageV2, WnspEncoderV2, SpectralRegion
from wavelength_validator import ModulationType


class TransportProtocol(Enum):
    """Physical transport protocols for offline mesh."""
    BLUETOOTH_LE = "bluetooth_le"      # Primary: 100m range, low power
    WIFI_DIRECT = "wifi_direct"        # Secondary: 200m range, higher bandwidth
    NFC = "nfc"                        # Tertiary: <10cm, secure pairing only
    INTERNET = "internet"              # Fallback: when offline fails


class ConnectionStatus(Enum):
    """Connection state for offline peers."""
    DISCOVERING = "discovering"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    FAILED = "failed"


@dataclass
class OfflinePeer:
    """Represents a nearby NexusOS device discoverable offline."""
    device_id: str
    device_name: str
    public_key: str
    spectral_region: SpectralRegion
    transport_protocol: TransportProtocol
    signal_strength: float  # RSSI for Bluetooth, similar for WiFi Direct (-100 to 0 dBm)
    distance_meters: float  # Estimated distance based on signal strength
    last_seen: float
    status: ConnectionStatus
    hop_count: int = 1  # How many hops away (1 = direct neighbor)
    capabilities: Dict[str, bool] = field(default_factory=dict)
    
    def is_nearby(self) -> bool:
        """Check if peer is within direct communication range."""
        return (time.time() - self.last_seen) < 60 and self.hop_count == 1
    
    def to_dict(self) -> Dict:
        return {
            'device_id': self.device_id,
            'device_name': self.device_name,
            'spectral_region': self.spectral_region.name,
            'transport': self.transport_protocol.value,
            'signal_strength': self.signal_strength,
            'distance_m': self.distance_meters,
            'hop_count': self.hop_count,
            'status': self.status.value,
            'last_seen': self.last_seen
        }


@dataclass
class OfflineMeshStats:
    """Statistics for offline mesh network."""
    total_peers_discovered: int = 0
    direct_neighbors: int = 0  # Hop count = 1
    indirect_peers: int = 0    # Hop count > 1
    messages_sent_offline: int = 0
    messages_received_offline: int = 0
    messages_relayed: int = 0  # Messages forwarded through this node
    bytes_transferred: int = 0
    avg_latency_ms: float = 0.0
    mesh_diameter: int = 0     # Maximum hop count in network
    uptime_seconds: float = 0.0
    

class OfflineMeshTransport:
    """
    Physical transport layer for offline peer-to-peer mesh networking.
    
    Integrates with existing WNSP v2.0 protocol - instead of sending WNSP messages
    over HTTP/internet, this sends them via Bluetooth LE or WiFi Direct.
    
    Architecture:
    ┌──────────────────────────────────────────────────────────┐
    │  Application Layer (Existing)                            │
    │  - WNSP v2.0 Messages                                   │
    │  - DAG Topology                                         │
    │  - AI Routing (messaging_routing.py)                    │
    └──────────────────────────────────────────────────────────┘
                            ↓
    ┌──────────────────────────────────────────────────────────┐
    │  THIS MODULE: Offline Mesh Transport                     │
    │  - Bluetooth LE Discovery & Transmission                │
    │  - WiFi Direct P2P                                      │
    │  - Automatic Protocol Selection                         │
    └──────────────────────────────────────────────────────────┘
                            ↓
             Phone A ←→ Phone B ←→ Phone C
          (No internet, no infrastructure needed)
    """
    
    def __init__(self, device_id: str, device_name: str, spectral_region: SpectralRegion):
        """
        Initialize offline mesh transport.
        
        Args:
            device_id: Unique identifier for this device
            device_name: Human-readable name (e.g., "Alice's iPhone")
            spectral_region: WNSP spectral region for this device
        """
        self.device_id = device_id
        self.device_name = device_name
        self.spectral_region = spectral_region
        
        # Peer management
        self.nearby_peers: Dict[str, OfflinePeer] = {}  # device_id -> peer
        self.message_queue: List[WnspMessageV2] = []   # Messages waiting to be sent offline
        
        # Transport adapters (simulated - real implementation would use platform APIs)
        self.bluetooth_enabled = True
        self.wifi_direct_enabled = True
        self.nfc_enabled = True
        
        # Statistics
        self.stats = OfflineMeshStats()
        self.start_time = time.time()
        
        # WNSP encoder for creating messages
        self.wnsp_encoder = WnspEncoderV2()
        
        # Message history (prevent duplicate forwarding)
        self.seen_message_ids: set = set()
        
        print(f"✅ Offline mesh transport initialized for {device_name}")
        print(f"   Device ID: {device_id}")
        print(f"   Spectral Region: {spectral_region.name}")
        print(f"   Bluetooth LE: {'Enabled' if self.bluetooth_enabled else 'Disabled'}")
        print(f"   WiFi Direct: {'Enabled' if self.wifi_direct_enabled else 'Disabled'}")
    
    # ========================================================================
    # PEER DISCOVERY (Bluetooth LE & WiFi Direct)
    # ========================================================================
    
    def discover_nearby_peers(self) -> List[OfflinePeer]:
        """
        Scan for nearby NexusOS devices using all available protocols.
        
        Real implementation would use:
        - iOS: CoreBluetooth framework
        - Android: BluetoothLeScanner, WifiP2pManager APIs
        
        Returns:
            List of discovered peers
        """
        discovered = []
        
        # Simulate Bluetooth LE discovery
        if self.bluetooth_enabled:
            ble_peers = self._discover_bluetooth_le()
            discovered.extend(ble_peers)
        
        # Simulate WiFi Direct discovery
        if self.wifi_direct_enabled:
            wifi_peers = self._discover_wifi_direct()
            discovered.extend(wifi_peers)
        
        # Update peer list
        for peer in discovered:
            self.nearby_peers[peer.device_id] = peer
            self.stats.total_peers_discovered += 1
        
        # Calculate mesh topology stats
        self._update_topology_stats()
        
        return discovered
    
    def _discover_bluetooth_le(self) -> List[OfflinePeer]:
        """
        Discover nearby devices using Bluetooth Low Energy.
        
        Real implementation:
        - Scan for BLE advertisements with NexusOS service UUID
        - Read spectral region, device ID from advertisement data
        - Establish GATT connection for data transfer
        
        Simulated for development.
        """
        # In production, this would scan for actual BLE devices
        # For now, simulate discovery of nearby peers
        
        simulated_peers = []
        
        # Simulate discovering 2-5 nearby devices
        import random
        num_peers = random.randint(2, 5)
        
        spectral_regions = list(SpectralRegion)
        
        for i in range(num_peers):
            # Simulate signal strength based on distance
            signal_strength = random.uniform(-80, -40)  # dBm
            distance = self._estimate_distance_from_rssi(signal_strength)
            
            peer = OfflinePeer(
                device_id=f"ble_peer_{i}_{int(time.time())}",
                device_name=f"NexusPhone-{i+1}",
                public_key=f"pubkey_{i}",
                spectral_region=random.choice(spectral_regions),
                transport_protocol=TransportProtocol.BLUETOOTH_LE,
                signal_strength=signal_strength,
                distance_meters=distance,
                last_seen=time.time(),
                status=ConnectionStatus.DISCOVERING,
                hop_count=1,
                capabilities={'messaging': True, 'validator': random.choice([True, False])}
            )
            simulated_peers.append(peer)
        
        return simulated_peers
    
    def _discover_wifi_direct(self) -> List[OfflinePeer]:
        """
        Discover nearby devices using WiFi Direct (P2P).
        
        Real implementation:
        - Use WiFi Direct peer discovery
        - Negotiate group owner role
        - Establish socket connection for data transfer
        
        Simulated for development.
        """
        # Similar to Bluetooth but typically fewer devices, longer range
        simulated_peers = []
        
        import random
        num_peers = random.randint(1, 3)
        spectral_regions = list(SpectralRegion)
        
        for i in range(num_peers):
            signal_strength = random.uniform(-70, -30)  # WiFi Direct typically stronger
            distance = self._estimate_distance_from_rssi(signal_strength) * 2  # ~2x range of BLE
            
            peer = OfflinePeer(
                device_id=f"wifi_peer_{i}_{int(time.time())}",
                device_name=f"NexusPhone-WiFi-{i+1}",
                public_key=f"pubkey_wifi_{i}",
                spectral_region=random.choice(spectral_regions),
                transport_protocol=TransportProtocol.WIFI_DIRECT,
                signal_strength=signal_strength,
                distance_meters=distance,
                last_seen=time.time(),
                status=ConnectionStatus.DISCOVERING,
                hop_count=1,
                capabilities={'messaging': True, 'validator': True, 'high_bandwidth': True}
            )
            simulated_peers.append(peer)
        
        return simulated_peers
    
    def _estimate_distance_from_rssi(self, rssi: float, tx_power: float = -59) -> float:
        """
        Estimate distance in meters from RSSI (Received Signal Strength Indicator).
        
        Formula: distance = 10 ^ ((TxPower - RSSI) / (10 * n))
        Where n = path loss exponent (2.0 for free space, 2-4 for indoor)
        
        Args:
            rssi: Received signal strength in dBm
            tx_power: Transmit power at 1 meter (default -59 dBm for BLE)
        
        Returns:
            Estimated distance in meters
        """
        n = 2.5  # Path loss exponent (indoor environment)
        distance = 10 ** ((tx_power - rssi) / (10 * n))
        return round(distance, 2)
    
    # ========================================================================
    # MESSAGE TRANSMISSION (Offline)
    # ========================================================================
    
    def send_message_offline(
        self,
        message: WnspMessageV2,
        recipient_id: Optional[str] = None,
        broadcast: bool = False
    ) -> Tuple[bool, str]:
        """
        Send WNSP message to peer(s) using offline transport (NO INTERNET).
        
        This replaces HTTP/WebSocket transmission with Bluetooth/WiFi Direct.
        The WNSP message structure remains identical - only transport changes.
        
        Args:
            message: WNSP v2.0 message to send
            recipient_id: Target device ID (None for broadcast)
            broadcast: If True, send to all nearby peers
        
        Returns:
            (success, status_message)
        """
        # Check if we've already seen/forwarded this message (prevent loops)
        if message.message_id in self.seen_message_ids:
            return (True, "Message already forwarded")
        
        self.seen_message_ids.add(message.message_id)
        
        # Select transmission protocol and peers
        if broadcast:
            targets = list(self.nearby_peers.values())
            transmission_mode = "broadcast"
        elif recipient_id:
            if recipient_id in self.nearby_peers:
                targets = [self.nearby_peers[recipient_id]]
                transmission_mode = "unicast"
            else:
                # Recipient not directly reachable - use multi-hop routing
                return self._route_through_mesh(message, recipient_id)
        else:
            return (False, "No recipient specified and broadcast=False")
        
        # Send via best available protocol for each peer
        successful_sends = 0
        total_targets = len(targets)
        
        for peer in targets:
            success = self._transmit_to_peer(peer, message)
            if success:
                successful_sends += 1
        
        # Update statistics
        self.stats.messages_sent_offline += successful_sends
        self.stats.bytes_transferred += len(json.dumps(message.__dict__).encode('utf-8'))
        
        status = f"Sent offline ({transmission_mode}): {successful_sends}/{total_targets} peers"
        return (successful_sends > 0, status)
    
    def _transmit_to_peer(self, peer: OfflinePeer, message: WnspMessageV2) -> bool:
        """
        Physically transmit WNSP message to a single peer.
        
        Real implementation:
        - Bluetooth LE: Write to GATT characteristic
        - WiFi Direct: Send over socket connection
        - NFC: Write NDEF record
        
        Args:
            peer: Target peer
            message: WNSP message to send
        
        Returns:
            True if transmission succeeded
        """
        # Serialize WNSP message to bytes
        message_bytes = self._serialize_wnsp_message(message)
        
        try:
            if peer.transport_protocol == TransportProtocol.BLUETOOTH_LE:
                return self._transmit_bluetooth_le(peer, message_bytes)
            elif peer.transport_protocol == TransportProtocol.WIFI_DIRECT:
                return self._transmit_wifi_direct(peer, message_bytes)
            elif peer.transport_protocol == TransportProtocol.NFC:
                return self._transmit_nfc(peer, message_bytes)
            else:
                return False
        except Exception as e:
            print(f"❌ Transmission failed to {peer.device_name}: {e}")
            return False
    
    def _transmit_bluetooth_le(self, peer: OfflinePeer, data: bytes) -> bool:
        """
        Transmit data via Bluetooth LE GATT.
        
        Real implementation:
        - iOS: CBPeripheral writeValue:forCharacteristic
        - Android: BluetoothGatt.writeCharacteristic()
        
        Simulated for development.
        """
        # Simulate transmission delay and success rate
        import random
        time.sleep(0.01)  # ~10ms latency
        
        # Success rate based on signal strength
        success_probability = 0.95 if peer.signal_strength > -70 else 0.80
        success = random.random() < success_probability
        
        if success:
            print(f"  📡 Bluetooth LE → {peer.device_name} ({len(data)} bytes)")
        
        return success
    
    def _transmit_wifi_direct(self, peer: OfflinePeer, data: bytes) -> bool:
        """
        Transmit data via WiFi Direct socket.
        
        Real implementation:
        - Establish TCP/UDP socket over WiFi Direct connection
        - Send data packets
        
        Simulated for development.
        """
        import random
        time.sleep(0.005)  # ~5ms latency (faster than BLE)
        
        # WiFi Direct more reliable
        success = random.random() < 0.98
        
        if success:
            print(f"  📶 WiFi Direct → {peer.device_name} ({len(data)} bytes)")
        
        return success
    
    def _transmit_nfc(self, peer: OfflinePeer, data: bytes) -> bool:
        """
        Transmit data via NFC (for pairing/key exchange only).
        
        Real implementation:
        - iOS: CoreNFC write NDEF message
        - Android: NfcAdapter
        
        Limited to very short range (<10cm).
        """
        import random
        time.sleep(0.001)  # ~1ms latency (very fast, very short range)
        
        # NFC very reliable but requires physical proximity
        success = random.random() < 0.99
        
        if success:
            print(f"  📲 NFC → {peer.device_name} ({len(data)} bytes)")
        
        return success
    
    def _serialize_wnsp_message(self, message: WnspMessageV2) -> bytes:
        """
        Serialize WNSP message to bytes for transmission.
        
        Uses JSON encoding with message metadata.
        Real implementation might use more efficient binary encoding.
        """
        message_dict = {
            'message_id': message.message_id,
            'sender_id': message.sender_id,
            'recipient_id': message.recipient_id,
            'content': message.content,
            'spectral_region': message.spectral_region.name,
            'modulation_type': message.modulation_type.name,
            'frequency_thz': message.frequency_thz,
            'quantum_energy': message.quantum_energy,
            'cost_nxt': message.cost_nxt,
            'parent_message_ids': message.parent_message_ids,
            'interference_hash': message.interference_hash,
            'created_at': message.created_at,
            'frames': [f.__dict__ for f in message.frames] if hasattr(message, 'frames') else []
        }
        
        return json.dumps(message_dict).encode('utf-8')
    
    # ========================================================================
    # MULTI-HOP ROUTING (Messages through mesh)
    # ========================================================================
    
    def _route_through_mesh(self, message: WnspMessageV2, final_recipient: str) -> Tuple[bool, str]:
        """
        Route message through multiple hops to reach distant peer.
        
        Uses existing DAG topology - each peer knows their neighbors.
        Message propagates hop-by-hop until it reaches destination.
        
        Algorithm:
        1. Find best next hop toward recipient
        2. Send to that neighbor
        3. They repeat the process
        4. Eventually reaches recipient
        
        Similar to how existing messaging_routing.py works, but offline.
        """
        # Check if recipient is in extended peer list (multi-hop)
        best_next_hop = self._find_best_next_hop(final_recipient)
        
        if not best_next_hop:
            return (False, f"No route to {final_recipient}")
        
        # Forward to next hop
        success = self._transmit_to_peer(best_next_hop, message)
        
        if success:
            self.stats.messages_relayed += 1
            return (True, f"Routed through {best_next_hop.device_name}")
        else:
            return (False, f"Failed to relay through {best_next_hop.device_name}")
    
    def _find_best_next_hop(self, final_recipient: str) -> Optional[OfflinePeer]:
        """
        Find best neighbor to forward message toward final recipient.
        
        Uses greedy routing based on:
        1. Signal strength (prefer stronger connections)
        2. Hop count (prefer shorter paths)
        3. Spectral diversity (prefer different regions for redundancy)
        """
        candidates = [p for p in self.nearby_peers.values() if p.is_nearby()]
        
        if not candidates:
            return None
        
        # Score each candidate
        best_peer = None
        best_score = -1
        
        for peer in candidates:
            score = 0
            
            # Prefer stronger signal
            score += (peer.signal_strength + 100) / 100  # Normalize -100 to 0 dBm → 0 to 1
            
            # Prefer closer hops
            score += (10 - peer.hop_count) / 10
            
            # Spectral diversity bonus
            if peer.spectral_region != self.spectral_region:
                score += 0.5
            
            if score > best_score:
                best_score = score
                best_peer = peer
        
        return best_peer
    
    # ========================================================================
    # MESSAGE RECEPTION (Incoming from offline peers)
    # ========================================================================
    
    def receive_message_offline(self, message_bytes: bytes, from_peer_id: str) -> Optional[WnspMessageV2]:
        """
        Receive and deserialize WNSP message from offline peer.
        
        Real implementation:
        - Bluetooth LE: Triggered by GATT characteristic notification
        - WiFi Direct: Received via socket listener
        
        Args:
            message_bytes: Serialized WNSP message
            from_peer_id: Device ID of sender
        
        Returns:
            Deserialized WNSP message, or None if invalid
        """
        try:
            message_dict = json.loads(message_bytes.decode('utf-8'))
            
            # Reconstruct WNSP message
            # (Simplified - real implementation would fully reconstruct all fields)
            message = WnspMessageV2(
                message_id=message_dict['message_id'],
                sender_id=message_dict['sender_id'],
                recipient_id=message_dict['recipient_id'],
                content=message_dict['content'],
                spectral_region=SpectralRegion[message_dict['spectral_region']],
                modulation_type=ModulationType[message_dict['modulation_type']],
                frequency_thz=message_dict['frequency_thz'],
                quantum_energy=message_dict['quantum_energy'],
                cost_nxt=message_dict['cost_nxt'],
                parent_message_ids=message_dict.get('parent_message_ids', []),
                interference_hash=message_dict['interference_hash'],
                created_at=message_dict['created_at'],
                frames=[]  # Frames would be reconstructed here
            )
            
            self.stats.messages_received_offline += 1
            
            # If this message isn't for us, relay it
            if message.recipient_id != self.device_id and message.recipient_id != 'broadcast':
                self._route_through_mesh(message, message.recipient_id)
            
            return message
            
        except Exception as e:
            print(f"❌ Failed to deserialize message: {e}")
            return None
    
    # ========================================================================
    # TOPOLOGY & STATISTICS
    # ========================================================================
    
    def _update_topology_stats(self):
        """Update mesh topology statistics."""
        direct = sum(1 for p in self.nearby_peers.values() if p.hop_count == 1)
        indirect = sum(1 for p in self.nearby_peers.values() if p.hop_count > 1)
        max_hops = max([p.hop_count for p in self.nearby_peers.values()], default=0)
        
        self.stats.direct_neighbors = direct
        self.stats.indirect_peers = indirect
        self.stats.mesh_diameter = max_hops
        self.stats.uptime_seconds = time.time() - self.start_time
    
    def get_network_topology(self) -> Dict[str, Any]:
        """
        Get current mesh network topology.
        
        Returns:
            Dictionary describing network structure (for visualization)
        """
        nodes = [
            {
                'id': self.device_id,
                'name': self.device_name,
                'type': 'self',
                'spectral_region': self.spectral_region.name
            }
        ]
        
        edges = []
        
        for peer in self.nearby_peers.values():
            nodes.append({
                'id': peer.device_id,
                'name': peer.device_name,
                'type': 'peer',
                'spectral_region': peer.spectral_region.name,
                'distance_m': str(peer.distance_meters),
                'hop_count': str(peer.hop_count)
            })
            
            edges.append({
                'from': self.device_id,
                'to': peer.device_id,
                'transport': peer.transport_protocol.value,
                'signal_strength': str(peer.signal_strength)
            })
        
        return {
            'nodes': nodes,
            'edges': edges,
            'stats': {
                'total_nodes': len(nodes),
                'total_edges': len(edges),
                'mesh_diameter': self.stats.mesh_diameter
            }
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive mesh statistics."""
        self._update_topology_stats()
        
        return {
            'total_peers': len(self.nearby_peers),
            'direct_neighbors': self.stats.direct_neighbors,
            'indirect_peers': self.stats.indirect_peers,
            'messages_sent': self.stats.messages_sent_offline,
            'messages_received': self.stats.messages_received_offline,
            'messages_relayed': self.stats.messages_relayed,
            'bytes_transferred': self.stats.bytes_transferred,
            'mesh_diameter': self.stats.mesh_diameter,
            'uptime_seconds': self.stats.uptime_seconds,
            'bluetooth_enabled': self.bluetooth_enabled,
            'wifi_direct_enabled': self.wifi_direct_enabled
        }


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def create_offline_transport(
    device_id: str,
    device_name: str,
    spectral_region: SpectralRegion = SpectralRegion.VIOLET
) -> OfflineMeshTransport:
    """
    Factory function to create offline mesh transport instance.
    
    Args:
        device_id: Unique device identifier
        device_name: Human-readable name
        spectral_region: WNSP spectral region (default: Violet)
    
    Returns:
        Configured OfflineMeshTransport instance
    """
    return OfflineMeshTransport(device_id, device_name, spectral_region)
