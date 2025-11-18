# Mobile Connectivity Guide
## Connecting Mobile Devices to NexusOS Web Platform

This guide explains how mobile phones connect to the existing NexusOS web application to access all blockchain features.

---

## Architecture Overview

```
┌─────────────────────┐          ┌──────────────────────┐
│   Mobile Device     │          │   NexusOS Web App    │
│   (iOS/Android)     │ ◄──────► │   (Streamlit)        │
│                     │   REST   │                      │
│   - Wallet UI       │   +      │  - WNSP Messaging    │
│   - Send/Receive    │   WS     │  - Blockchain        │
│   - Messaging       │          │  - DEX               │
│   - Validator       │          │  - Validators        │
└─────────────────────┘          │  - Economics         │
                                 └──────────────────────┘
                                           ▲
                                           │
┌─────────────────────┐                   │
│  Mobile API Gateway │───────────────────┘
│  (Flask + SocketIO) │   
│  Port 5001          │   Exposes existing
└─────────────────────┘   web features via API
```

**Key Concept**: The web platform already has ALL features. Mobile devices simply connect to use them via API.

---

## Quick Start

### 1. Start the Mobile API Gateway

The gateway exposes web platform features to mobile devices:

```bash
python mobile_api_gateway.py
```

This starts a Flask server on port 5001 that:
- Provides REST/WebSocket endpoints
- Authenticates mobile devices
- Routes requests to existing web platform code
- Broadcasts updates to all connected mobiles

### 2. Test Mobile Connection

Use the Python SDK to simulate a mobile device:

```bash
python mobile_client_sdk.py
```

This will:
- Register a test mobile device
- Connect via WebSocket
- Check NXT balance
- Send WNSP message
- Transfer NXT
- Become a validator
- Show network status

### 3. View Connected Mobiles

Open the NexusOS web app and navigate to:
**📲 Mobile Connectivity** dashboard

This shows:
- All connected mobile devices
- Network status
- Spectral diversity distribution
- Validator activity
- Real-time connection statistics

---

## Mobile SDK Usage

### Registering a Mobile Device

```python
from mobile_client_sdk import register_mobile_device

# Register new mobile
wallet = register_mobile_device(
    device_id="alice_iphone_12345",
    device_name="Alice's iPhone",
    base_url="http://localhost:5001"
)

# Connect WebSocket for real-time updates
wallet.connect_websocket()
```

### Sending WNSP Messages

```python
# Mobile uses existing web platform's WNSP encoder
result = wallet.send_wnsp_message(
    content="Hello from mobile!",
    recipient_id="broadcast"
)

print(f"Message sent! Cost: {result['cost_nxt']} NXT")
```

### Transferring NXT

```python
# Mobile uses existing token system
result = wallet.transfer_nxt(
    recipient_id="mobile_bob_456",
    amount_nxt=10.5
)

print(f"Transferred {result['amount_nxt']} NXT")
```

### Becoming a Validator

```python
# Mobile stakes NXT via web platform
result = wallet.become_validator(stake_nxt=100.0)

print(f"Now validator in {result['spectral_region']} region!")
```

### Checking Balance

```python
balance = wallet.get_balance()
print(f"Balance: {balance['balance_nxt']} NXT")
```

---

## API Endpoints

### Authentication

#### Register Mobile Device
```http
POST /api/mobile/register
Content-Type: application/json

{
  "device_id": "unique_device_id",
  "device_name": "My iPhone"
}

Response:
{
  "success": true,
  "auth_token": "secure_token",
  "account_id": "mobile_unique_devi",
  "spectral_region": "Violet",
  "initial_balance_nxt": 100.0,
  "qr_code_data": "nexusos://connect?device_id=...&token=..."
}
```

### WNSP Messaging

#### Send Message
```http
POST /api/mobile/wnsp/send
Authorization: Bearer {auth_token}
Content-Type: application/json

{
  "content": "Hello NexusOS!",
  "recipient_id": "broadcast",
  "spectral_region": "Violet",
  "parent_message_ids": []
}

Response:
{
  "success": true,
  "message_id": "msg_000001_abc123",
  "cost_nxt": 0.0100,
  "interference_hash": "quantum_signature..."
}
```

#### Get Inbox
```http
GET /api/mobile/wnsp/inbox
Authorization: Bearer {auth_token}

Response:
{
  "messages": [...],
  "count": 10
}
```

### Blockchain Operations

#### Get Balance
```http
GET /api/mobile/balance
Authorization: Bearer {auth_token}

Response:
{
  "account_id": "mobile_alice_123",
  "balance_nxt": 100.0,
  "balance_units": 10000
}
```

#### Transfer NXT
```http
POST /api/mobile/transfer
Authorization: Bearer {auth_token}
Content-Type: application/json

{
  "recipient_id": "mobile_bob_456",
  "amount_nxt": 10.5
}

Response:
{
  "success": true,
  "from": "mobile_alice_123",
  "to": "mobile_bob_456",
  "amount_nxt": 10.5,
  "fee_nxt": 0.0105
}
```

### Validator Operations

#### Stake to Become Validator
```http
POST /api/mobile/validator/stake
Authorization: Bearer {auth_token}
Content-Type: application/json

{
  "stake_amount_nxt": 100.0
}

Response:
{
  "success": true,
  "validator_id": "mobile_alice_123",
  "stake_nxt": 100.0,
  "spectral_region": "Violet"
}
```

#### Get Validator Earnings
```http
GET /api/mobile/validator/earnings
Authorization: Bearer {auth_token}

Response:
{
  "validator_id": "mobile_alice_123",
  "is_active": true,
  "stake_nxt": 100.0,
  "spectral_region": "Violet",
  "total_earnings_nxt": 5.25
}
```

### Network Status

#### Get Network Status
```http
GET /api/mobile/network/status

Response:
{
  "connected_mobiles": 42,
  "active_validators": 15,
  "total_nxt_staked": 1500.0,
  "latest_block_height": 12345,
  "network_health": "healthy"
}
```

#### Get Connected Peers
```http
GET /api/mobile/peers
Authorization: Bearer {auth_token}

Response:
{
  "peers": [
    {
      "device_id": "bob_android",
      "device_name": "Bob's Android",
      "spectral_region": "Blue",
      "is_validator": true,
      "online": true
    }
  ],
  "count": 1
}
```

---

## WebSocket Events

### Connect and Authenticate

```javascript
// Connect to gateway
const socket = io('http://localhost:5001');

// Authenticate
socket.emit('authenticate', {
  auth_token: 'your_auth_token'
});

// Listen for authentication result
socket.on('authenticated', (data) => {
  if (data.success) {
    console.log('Authenticated!', data.account_id);
  }
});
```

### Real-time Events

```javascript
// New WNSP message received
socket.on('wnsp_message', (data) => {
  console.log('New message from', data.sender_id);
  console.log('Content:', data.content);
  console.log('Cost:', data.cost_nxt, 'NXT');
});

// New transaction
socket.on('transaction', (data) => {
  console.log('Transaction:', data.from, '→', data.to);
  console.log('Amount:', data.amount_nxt, 'NXT');
});

// New block
socket.on('block_update', (data) => {
  console.log('New block #', data.height);
});

// Heartbeat
socket.on('pong', (data) => {
  console.log('Pong received at', data.timestamp);
});
```

---

## Native Mobile App Integration

### iOS (Swift) Example

```swift
import Foundation

class NexusWallet {
    let deviceId: String
    let baseUrl: String
    var authToken: String?
    var accountId: String?
    
    init(deviceId: String, baseUrl: String = "https://your-app.repl.co:5001") {
        self.deviceId = deviceId
        self.baseUrl = baseUrl
    }
    
    func register(deviceName: String, completion: @escaping (Result<RegisterResponse, Error>) -> Void) {
        let url = URL(string: "\(baseUrl)/api/mobile/register")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body = [
            "device_id": deviceId,
            "device_name": deviceName
        ]
        request.httpBody = try? JSONEncoder().encode(body)
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            // Handle response
            if let data = data {
                let result = try? JSONDecoder().decode(RegisterResponse.self, from: data)
                if let result = result {
                    self.authToken = result.auth_token
                    self.accountId = result.account_id
                    completion(.success(result))
                }
            }
        }.resume()
    }
    
    func sendWnspMessage(content: String, completion: @escaping (Result<MessageResponse, Error>) -> Void) {
        guard let token = authToken else { return }
        
        let url = URL(string: "\(baseUrl)/api/mobile/wnsp/send")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body = [
            "content": content,
            "recipient_id": "broadcast"
        ]
        request.httpBody = try? JSONEncoder().encode(body)
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            // Handle response
        }.resume()
    }
    
    func getBalance(completion: @escaping (Result<BalanceResponse, Error>) -> Void) {
        guard let token = authToken else { return }
        
        let url = URL(string: "\(baseUrl)/api/mobile/balance")!
        var request = URLRequest(url: url)
        request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            // Handle response
        }.resume()
    }
}
```

### Android (Kotlin) Example

```kotlin
class NexusWallet(
    private val deviceId: String,
    private val baseUrl: String = "https://your-app.repl.co:5001"
) {
    private var authToken: String? = null
    private var accountId: String? = null
    private val client = OkHttpClient()
    
    suspend fun register(deviceName: String): RegisterResponse {
        val json = JSONObject().apply {
            put("device_id", deviceId)
            put("device_name", deviceName)
        }
        
        val request = Request.Builder()
            .url("$baseUrl/api/mobile/register")
            .post(json.toString().toRequestBody("application/json".toMediaType()))
            .build()
        
        val response = client.newCall(request).execute()
        val result = response.body?.string()?.let {
            Gson().fromJson(it, RegisterResponse::class.java)
        }
        
        authToken = result?.auth_token
        accountId = result?.account_id
        
        return result!!
    }
    
    suspend fun sendWnspMessage(content: String): MessageResponse {
        val json = JSONObject().apply {
            put("content", content)
            put("recipient_id", "broadcast")
        }
        
        val request = Request.Builder()
            .url("$baseUrl/api/mobile/wnsp/send")
            .addHeader("Authorization", "Bearer $authToken")
            .post(json.toString().toRequestBody("application/json".toMediaType()))
            .build()
        
        val response = client.newCall(request).execute()
        return Gson().fromJson(response.body?.string(), MessageResponse::class.java)
    }
    
    suspend fun getBalance(): BalanceResponse {
        val request = Request.Builder()
            .url("$baseUrl/api/mobile/balance")
            .addHeader("Authorization", "Bearer $authToken")
            .get()
            .build()
        
        val response = client.newCall(request).execute()
        return Gson().fromJson(response.body?.string(), BalanceResponse::class.java)
    }
}
```

---

## Benefits of This Architecture

### ✅ No Code Duplication
- Mobile apps are lightweight (just UI + API calls)
- All blockchain logic stays on web platform
- Fix bugs once, all mobiles benefit

### ✅ Rapid Development
- Existing web features instantly available to mobile
- No need to rewrite WNSP, blockchain, DEX, etc.
- Focus mobile development on UI/UX only

### ✅ Easy Updates
- Update web platform → all mobiles get new features
- No app store approval needed for backend changes
- Real-time feature deployment

### ✅ Resource Efficient
- Mobiles don't need to store full blockchain
- Heavy computation happens on web platform
- Lower battery and data usage

### ✅ Consistent Experience
- Same features across web and mobile
- Unified business logic
- Single source of truth

---

## Production Deployment

### 1. Deploy Web Platform
```bash
# Already running on Replit
https://your-app.repl.co
```

### 2. Deploy Mobile API Gateway
```bash
# Run on separate port or subdomain
https://api.your-app.repl.co:5001

# Or use Replit's deployment features
```

### 3. Configure Mobile Apps
```swift
// Point to production gateway
let wallet = NexusWallet(
    deviceId: UIDevice.current.identifierForVendor!.uuidString,
    baseUrl: "https://api.your-app.repl.co:5001"
)
```

### 4. Security Considerations

- ✅ Use HTTPS in production
- ✅ Implement rate limiting
- ✅ Add CORS restrictions
- ✅ Enable request logging
- ✅ Monitor for abuse
- ✅ Implement session expiry
- ✅ Use secure WebSocket (WSS)

---

## Troubleshooting

### Mobile API Gateway Not Starting

```bash
# Check if port 5001 is available
lsof -i :5001

# Install required packages
pip install flask flask-cors flask-socketio python-socketio

# Start with debug logging
python mobile_api_gateway.py
```

### Mobile Can't Connect

1. Check gateway is running on port 5001
2. Verify base_url in mobile code
3. Check auth_token is valid
4. Look at gateway logs for errors

### WebSocket Connection Drops

1. Implement heartbeat (ping/pong)
2. Auto-reconnect on disconnect
3. Resume session with saved auth_token

---

## Next Steps

1. **Build Native Mobile Apps**:
   - iOS app (SwiftUI)
   - Android app (Jetpack Compose)

2. **Enhanced Features**:
   - Push notifications for transactions
   - Biometric authentication
   - QR code scanning
   - Offline transaction queue

3. **Optimization**:
   - Response caching
   - Batch API requests
   - Lazy loading
   - Background sync

4. **Monitoring**:
   - Mobile analytics
   - API usage metrics
   - Error tracking
   - Performance monitoring

---

## Support

For questions or issues:
- Check logs: Mobile API Gateway console output
- View dashboard: **📲 Mobile Connectivity** in web app
- Test with SDK: `python mobile_client_sdk.py`

---

*Last Updated: November 18, 2025*  
*Version: 1.0*
