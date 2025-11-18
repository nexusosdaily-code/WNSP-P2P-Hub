"""
NexusOS Mobile Client SDK
===========================

Simple Python SDK demonstrating how mobile devices connect to the NexusOS web platform.
Mobile apps (iOS/Android) would use similar logic in Swift/Kotlin.

This SDK shows how mobiles access all existing web platform features:
- WNSP messaging
- NXT transfers
- Blockchain operations
- Validator participation
- DEX trading
"""

import requests
import json
from typing import Optional, Dict, List
from dataclasses import dataclass
import socketio

@dataclass
class MobileWallet:
    """Mobile wallet connected to NexusOS web platform"""
    device_id: str
    device_name: str
    auth_token: str
    account_id: str
    spectral_region: str
    base_url: str = "http://localhost:5001"
    
    def __post_init__(self):
        self.socket = socketio.Client()
        self._setup_socket_handlers()
    
    def _setup_socket_handlers(self):
        """Setup WebSocket event handlers"""
        
        @self.socket.on('connected')
        def on_connected(data):
            print(f"✅ Connected to NexusOS platform")
            # Authenticate via WebSocket
            self.socket.emit('authenticate', {'auth_token': self.auth_token})
        
        @self.socket.on('authenticated')
        def on_authenticated(data):
            if data.get('success'):
                print(f"✅ Authenticated as {data['account_id']}")
                print(f"🌈 Spectral Region: {data['spectral_region']}")
            else:
                print(f"❌ Authentication failed: {data.get('error')}")
        
        @self.socket.on('wnsp_message')
        def on_wnsp_message(data):
            print(f"\n📨 New WNSP Message:")
            print(f"   From: {data['sender_id']}")
            print(f"   Content: {data['content']}")
            print(f"   Region: {data['spectral_region']}")
            print(f"   Cost: {data['cost_nxt']} NXT")
        
        @self.socket.on('transaction')
        def on_transaction(data):
            print(f"\n💰 New Transaction:")
            print(f"   From: {data['from']}")
            print(f"   To: {data['to']}")
            print(f"   Amount: {data['amount_nxt']} NXT")
        
        @self.socket.on('block_update')
        def on_block_update(data):
            print(f"\n⛓️  New Block: #{data.get('height', 0)}")
    
    def connect_websocket(self):
        """Establish real-time WebSocket connection"""
        try:
            self.socket.connect(self.base_url)
            print(f"🔌 WebSocket connected to {self.base_url}")
        except Exception as e:
            print(f"❌ WebSocket connection failed: {e}")
    
    def disconnect_websocket(self):
        """Close WebSocket connection"""
        self.socket.disconnect()
    
    def _headers(self) -> Dict[str, str]:
        """Get authentication headers"""
        return {
            'Authorization': f'Bearer {self.auth_token}',
            'Content-Type': 'application/json'
        }
    
    # ========================================================================
    # ACCOUNT OPERATIONS
    # ========================================================================
    
    def get_balance(self) -> Dict:
        """
        Get NXT balance from web platform.
        
        Returns:
        {
            "account_id": "mobile_alice_123",
            "balance_nxt": 100.0,
            "balance_units": 10000
        }
        """
        response = requests.get(
            f"{self.base_url}/api/mobile/balance",
            headers=self._headers()
        )
        return response.json()
    
    def transfer_nxt(self, recipient_id: str, amount_nxt: float) -> Dict:
        """
        Send NXT to another account via web platform.
        
        Example:
            wallet.transfer_nxt("mobile_bob_456", 10.5)
        """
        response = requests.post(
            f"{self.base_url}/api/mobile/transfer",
            headers=self._headers(),
            json={
                "recipient_id": recipient_id,
                "amount_nxt": amount_nxt
            }
        )
        return response.json()
    
    def get_transactions(self) -> List[Dict]:
        """Get transaction history from web platform"""
        response = requests.get(
            f"{self.base_url}/api/mobile/transactions",
            headers=self._headers()
        )
        return response.json()
    
    # ========================================================================
    # WNSP MESSAGING
    # ========================================================================
    
    def send_wnsp_message(
        self,
        content: str,
        recipient_id: str = "broadcast",
        parent_message_ids: List[str] = None
    ) -> Dict:
        """
        Send WNSP message via web platform.
        All heavy computation happens on web platform!
        
        Example:
            wallet.send_wnsp_message(
                "Hello from mobile!",
                recipient_id="mobile_bob_456"
            )
        """
        response = requests.post(
            f"{self.base_url}/api/mobile/wnsp/send",
            headers=self._headers(),
            json={
                "content": content,
                "recipient_id": recipient_id,
                "spectral_region": self.spectral_region,
                "parent_message_ids": parent_message_ids or []
            }
        )
        return response.json()
    
    def get_inbox(self) -> Dict:
        """Get WNSP messages from web platform"""
        response = requests.get(
            f"{self.base_url}/api/mobile/wnsp/inbox",
            headers=self._headers()
        )
        return response.json()
    
    # ========================================================================
    # VALIDATOR OPERATIONS
    # ========================================================================
    
    def become_validator(self, stake_nxt: float = 100.0) -> Dict:
        """
        Stake NXT to become validator via web platform.
        
        Example:
            wallet.become_validator(100.0)
        """
        response = requests.post(
            f"{self.base_url}/api/mobile/validator/stake",
            headers=self._headers(),
            json={"stake_amount_nxt": stake_nxt}
        )
        return response.json()
    
    def get_validator_earnings(self) -> Dict:
        """Get validator earnings from web platform"""
        response = requests.get(
            f"{self.base_url}/api/mobile/validator/earnings",
            headers=self._headers()
        )
        return response.json()
    
    # ========================================================================
    # NETWORK STATUS
    # ========================================================================
    
    def get_network_status(self) -> Dict:
        """Get overall network status from web platform"""
        response = requests.get(f"{self.base_url}/api/mobile/network/status")
        return response.json()
    
    def get_peers(self) -> Dict:
        """Get list of connected mobile peers"""
        response = requests.get(
            f"{self.base_url}/api/mobile/peers",
            headers=self._headers()
        )
        return response.json()
    
    # ========================================================================
    # DEX OPERATIONS
    # ========================================================================
    
    def get_dex_pairs(self) -> Dict:
        """Get available DEX trading pairs from web platform"""
        response = requests.get(f"{self.base_url}/api/mobile/dex/pairs")
        return response.json()


# ============================================================================
# MOBILE REGISTRATION HELPER
# ============================================================================

def register_mobile_device(
    device_id: str,
    device_name: str,
    base_url: str = "http://localhost:5001"
) -> MobileWallet:
    """
    Register new mobile device with NexusOS web platform.
    
    Example:
        wallet = register_mobile_device(
            device_id="alice_iphone_12345",
            device_name="Alice's iPhone"
        )
    
    Returns:
        MobileWallet instance ready to use
    """
    response = requests.post(
        f"{base_url}/api/mobile/register",
        json={
            "device_id": device_id,
            "device_name": device_name
        }
    )
    
    data = response.json()
    
    if data.get('success'):
        print(f"\n✅ Mobile device registered successfully!")
        print(f"📱 Device: {device_name}")
        print(f"💼 Account: {data['account_id']}")
        print(f"🌈 Spectral Region: {data['spectral_region']}")
        print(f"💰 Initial Balance: {data['initial_balance_nxt']} NXT")
        print(f"🔗 Web Dashboard: {data['web_dashboard_url']}")
        print(f"\n📱 QR Code Data (for mobile app):")
        print(f"   {data['qr_code_data']}\n")
        
        return MobileWallet(
            device_id=device_id,
            device_name=device_name,
            auth_token=data['auth_token'],
            account_id=data['account_id'],
            spectral_region=data['spectral_region'],
            base_url=base_url
        )
    else:
        raise Exception(f"Registration failed: {data.get('error')}")


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

def demo_mobile_wallet():
    """
    Demonstration of mobile wallet connecting to NexusOS web platform.
    Shows how ALL existing app features are accessible from mobile!
    """
    
    print("=" * 60)
    print("NexusOS Mobile Wallet Demo")
    print("Connecting to Web Platform")
    print("=" * 60)
    
    # 1. Register mobile device
    wallet = register_mobile_device(
        device_id="demo_mobile_001",
        device_name="Demo Mobile Device"
    )
    
    # 2. Connect WebSocket for real-time updates
    wallet.connect_websocket()
    
    # 3. Check balance
    print("\n--- Checking Balance ---")
    balance = wallet.get_balance()
    print(f"💰 Balance: {balance['balance_nxt']} NXT")
    
    # 4. Send WNSP message
    print("\n--- Sending WNSP Message ---")
    msg_result = wallet.send_wnsp_message(
        "Hello NexusOS! Sent from mobile via web platform!",
        recipient_id="broadcast"
    )
    if msg_result.get('success'):
        print(f"✅ Message sent! ID: {msg_result['message_id']}")
        print(f"💸 Cost: {msg_result['cost_nxt']} NXT")
    
    # 5. Transfer NXT
    print("\n--- Transferring NXT ---")
    # Create test recipient first
    requests.post(
        f"{wallet.base_url}/api/mobile/register",
        json={
            "device_id": "demo_mobile_002",
            "device_name": "Test Recipient"
        }
    )
    
    transfer_result = wallet.transfer_nxt("mobile_demo_mobile_002", 5.0)
    if transfer_result.get('success'):
        print(f"✅ Transferred {transfer_result['amount_nxt']} NXT")
        print(f"   To: {transfer_result['to']}")
    
    # 6. Become validator
    print("\n--- Becoming Validator ---")
    validator_result = wallet.become_validator(100.0)
    if validator_result.get('success'):
        print(f"✅ Now a validator!")
        print(f"🔒 Stake: {validator_result['stake_nxt']} NXT")
        print(f"🌈 Region: {validator_result['spectral_region']}")
    
    # 7. Check network status
    print("\n--- Network Status ---")
    network = wallet.get_network_status()
    print(f"📱 Connected Mobiles: {network['connected_mobiles']}")
    print(f"✅ Active Validators: {network['active_validators']}")
    print(f"💰 Total Staked: {network['total_nxt_staked']} NXT")
    
    # 8. Get peers
    print("\n--- Connected Peers ---")
    peers = wallet.get_peers()
    print(f"👥 Peers: {peers['count']}")
    for peer in peers['peers'][:5]:  # Show first 5
        status = "🟢" if peer['online'] else "🔴"
        validator = "✅" if peer['is_validator'] else ""
        print(f"   {status} {peer['device_name']} ({peer['spectral_region']}) {validator}")
    
    print("\n" + "=" * 60)
    print("Demo Complete!")
    print("Mobile connected to ALL web platform features! ✅")
    print("=" * 60)
    
    # Keep WebSocket alive for real-time updates
    input("\nPress Enter to disconnect...")
    wallet.disconnect_websocket()


if __name__ == '__main__':
    demo_mobile_wallet()
