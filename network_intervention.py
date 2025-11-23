"""
NexusOS Network Layer Active Intervention
Real-time DDoS detection and automated IP banning

Protects against:
- Request flooding
- Connection exhaustion
- Distributed attacks
- Bot networks
"""

from typing import Dict, Optional, Tuple
from collections import deque, defaultdict
import time

from active_intervention_engine import get_intervention_engine


class NetworkInterventionGuard:
    """
    Network-layer active intervention for DDoS protection
    
    Monitors request patterns and automatically bans flooding IPs
    """
    
    def __init__(self):
        # Request tracking (IP -> request timestamps)
        self.request_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        
        # Connection tracking
        self.active_connections: Dict[str, int] = defaultdict(int)
        
        # Thresholds
        self.requests_per_second_critical = 100
        self.requests_per_second_high = 50
        self.max_connections_per_ip = 10
        
        # Window sizes
        self.flood_detection_window = 10  # seconds
    
    def check_request(self, ip_address: str, endpoint: str = "") -> Tuple[bool, Optional[str]]:
        """
        Check if request from IP should be allowed
        
        Returns:
            (allowed: bool, reason: Optional[str])
        """
        # Check if IP is already banned
        intervention_engine = get_intervention_engine()
        is_blocked, reason = intervention_engine.is_entity_blocked(ip_address)
        
        if is_blocked:
            return False, f"IP banned: {reason}"
        
        # Record request
        current_time = time.time()
        self.request_history[ip_address].append(current_time)
        
        # Calculate request rate
        cutoff = current_time - self.flood_detection_window
        recent_requests = [t for t in self.request_history[ip_address] if t > cutoff]
        
        requests_per_second = len(recent_requests) / self.flood_detection_window
        
        # 🛡️ ACTIVE INTERVENTION: DDoS detection
        if requests_per_second >= self.requests_per_second_critical:
            # CRITICAL flood - permanent ban
            intervention_engine.detect_and_intervene(
                threat_type="request_flood",
                entity=ip_address,
                metric_value=requests_per_second,
                evidence=f"{len(recent_requests)} requests in {self.flood_detection_window}s ({requests_per_second:.1f} req/s)"
            )
            return False, f"DDoS detected: {requests_per_second:.1f} req/s"
        
        elif requests_per_second >= self.requests_per_second_high:
            # HIGH flood - temporary ban
            intervention_engine.detect_and_intervene(
                threat_type="request_flood",
                entity=ip_address,
                metric_value=requests_per_second,
                evidence=f"{len(recent_requests)} requests in {self.flood_detection_window}s ({requests_per_second:.1f} req/s)"
            )
            return False, f"Rate limit exceeded: {requests_per_second:.1f} req/s"
        
        return True, None
    
    def track_connection(self, ip_address: str, connected: bool) -> Tuple[bool, Optional[str]]:
        """
        Track connection open/close and check limits
        
        Args:
            ip_address: IP address
            connected: True for new connection, False for close
        
        Returns:
            (allowed: bool, reason: Optional[str])
        """
        if connected:
            # Check current connection count
            current_connections = self.active_connections[ip_address]
            
            if current_connections >= self.max_connections_per_ip:
                intervention_engine = get_intervention_engine()
                intervention_engine.detect_and_intervene(
                    threat_type="connection_exhaustion",
                    entity=ip_address,
                    metric_value=current_connections,
                    evidence=f"{current_connections} concurrent connections (limit: {self.max_connections_per_ip})"
                )
                return False, f"Too many connections: {current_connections}"
            
            self.active_connections[ip_address] += 1
        else:
            # Close connection
            if self.active_connections[ip_address] > 0:
                self.active_connections[ip_address] -= 1
        
        return True, None
    
    def get_network_stats(self) -> Dict:
        """Get network security statistics"""
        total_ips = len(self.request_history)
        total_connections = sum(self.active_connections.values())
        
        # Calculate recent activity
        current_time = time.time()
        cutoff = current_time - 60  # Last minute
        
        active_ips = sum(
            1 for ip, timestamps in self.request_history.items()
            if timestamps and timestamps[-1] > cutoff
        )
        
        return {
            "total_ips_tracked": total_ips,
            "active_ips_last_minute": active_ips,
            "total_active_connections": total_connections,
            "max_connections_per_ip": self.max_connections_per_ip,
            "flood_threshold_critical": self.requests_per_second_critical,
            "flood_threshold_high": self.requests_per_second_high
        }


# Global singleton
_network_guard = None

def get_network_guard() -> NetworkInterventionGuard:
    """Get global network intervention guard"""
    global _network_guard
    if _network_guard is None:
        _network_guard = NetworkInterventionGuard()
    return _network_guard
