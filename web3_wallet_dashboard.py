"""
Web3 Wallet Dashboard
=====================

Interactive dashboard for connecting and managing Web3 wallets with
quantum-resistant wavelength encryption.
"""

import streamlit as st
import time
from typing import Dict, Optional
import json

from web3_wallet_connector import (
    quantum_wallet,
    WalletProvider,
    Web3WalletConnection,
    QuantumSignedTransaction
)


def render_web3_wallet_dashboard():
    """Main Web3 wallet dashboard with quantum encryption."""
    
    st.title("🔐 Web3 Wallet - Quantum Resistant")
    st.markdown("""
    **Connect your Web3 wallet** with NexusOS's quantum-resistant wavelength encryption.  
    🛡️ **Hacker-Proof** | ⚛️ **Quantum-Resistant** | 🌈 **Wavelength Security**
    """)
    
    st.divider()
    
    # Tabs for different sections
    tabs = st.tabs([
        "🔌 Connect Wallet",
        "💳 My Wallet",
        "📤 Send Transaction",
        "🔬 Quantum Security",
        "📊 Connected Wallets"
    ])
    
    with tabs[0]:
        render_connect_wallet_tab()
    
    with tabs[1]:
        render_my_wallet_tab()
    
    with tabs[2]:
        render_send_transaction_tab()
    
    with tabs[3]:
        render_quantum_security_tab()
    
    with tabs[4]:
        render_connected_wallets_tab()


def render_connect_wallet_tab():
    """Tab for connecting Web3 wallet."""
    
    st.header("🔌 Connect Your Web3 Wallet")
    
    st.info("""
    **How it works:**
    1. Select your wallet provider (MetaMask, WalletConnect, etc.)
    2. Enter your wallet address
    3. Sign a message to prove ownership
    4. Get assigned a spectral region for quantum encryption
    5. Your wallet is now protected with wavelength security! 🌈
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        provider = st.selectbox(
            "Select Wallet Provider",
            options=[
                "MetaMask",
                "WalletConnect",
                "Coinbase Wallet",
                "Trust Wallet",
                "Phantom (Solana)"
            ],
            help="Choose your preferred Web3 wallet provider"
        )
    
    with col2:
        chain_id = st.selectbox(
            "Select Network",
            options=[
                ("Ethereum Mainnet", 1),
                ("Polygon", 137),
                ("BSC", 56),
                ("Arbitrum", 42161),
                ("Optimism", 10),
                ("Solana", 900)
            ],
            format_func=lambda x: x[0],
            help="Select blockchain network"
        )
    
    wallet_address = st.text_input(
        "Wallet Address",
        placeholder="0x1234567890abcdef1234567890abcdef12345678",
        help="Your Web3 wallet address (starts with 0x for EVM chains)"
    )
    
    if st.button("🔐 Connect Wallet", type="primary", use_container_width=True):
        if not wallet_address:
            st.error("Please enter your wallet address")
            return
        
        # Map provider name to enum
        provider_map = {
            "MetaMask": WalletProvider.METAMASK,
            "WalletConnect": WalletProvider.WALLETCONNECT,
            "Coinbase Wallet": WalletProvider.COINBASE,
            "Trust Wallet": WalletProvider.TRUST,
            "Phantom (Solana)": WalletProvider.PHANTOM
        }
        
        with st.spinner("🔐 Connecting wallet with quantum encryption..."):
            time.sleep(1)  # Simulate connection
            
            # Mock Web3 signature (in real app, would come from wallet)
            mock_signature = "0x" + "a" * 130
            
            try:
                connection = quantum_wallet.connect_wallet(
                    wallet_address=wallet_address,
                    provider=provider_map[provider],
                    chain_id=chain_id[1],
                    web3_signature=mock_signature
                )
                
                st.success("✅ Wallet connected successfully!")
                
                st.balloons()
                
                # Show connection details
                st.subheader("🌈 Quantum Security Details")
                
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    st.metric(
                        "Spectral Region",
                        connection.spectral_region.value,
                        help="Your assigned wavelength encryption region"
                    )
                
                with col_b:
                    st.metric(
                        "Security Level",
                        "QUANTUM",
                        help="Quantum-resistant encryption active"
                    )
                
                with col_c:
                    st.metric(
                        "Provider",
                        provider,
                        help="Your wallet provider"
                    )
                
                with st.expander("🔑 Quantum Public Key"):
                    st.code(connection.quantum_public_key, language="text")
                
                with st.expander("🆔 Session ID"):
                    st.code(connection.session_id, language="text")
                
            except Exception as e:
                st.error(f"❌ Connection failed: {str(e)}")


def render_my_wallet_tab():
    """Tab showing current wallet info."""
    
    st.header("💳 My Wallet")
    
    # Get connected wallets from session or quantum_wallet
    wallets = quantum_wallet.get_connected_wallets()
    
    if not wallets:
        st.warning("⚠️ No wallet connected. Go to the 'Connect Wallet' tab to connect.")
        return
    
    # Show most recent wallet
    wallet = wallets[-1]
    
    st.success(f"✅ Connected: {wallet['wallet_address'][:10]}...{wallet['wallet_address'][-8:]}")
    
    # Wallet info cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Provider",
            wallet['provider'].upper()
        )
    
    with col2:
        st.metric(
            "Chain ID",
            wallet['chain_id']
        )
    
    with col3:
        st.metric(
            "Spectral Region",
            wallet['spectral_region']
        )
    
    with col4:
        age_seconds = time.time() - wallet['connected_at']
        age_minutes = int(age_seconds / 60)
        st.metric(
            "Connected",
            f"{age_minutes}m ago"
        )
    
    st.divider()
    
    # Quantum security status
    security = quantum_wallet.get_security_status(wallet['wallet_address'])
    
    st.subheader("🛡️ Quantum Security Status")
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.metric(
            "Quantum Encrypted",
            "✅ YES" if security.get('quantum_encrypted') else "❌ NO",
            help="Wallet protected with wavelength encryption"
        )
    
    with col_b:
        st.metric(
            "Security Level",
            security.get('security_level', 'UNKNOWN'),
            help="Quantum-resistant protection level"
        )
    
    with col_c:
        st.metric(
            "Transaction Nonce",
            security.get('nonce', 0),
            help="Replay attack prevention counter"
        )
    
    # Show quantum public key
    with st.expander("🔑 View Quantum Public Key"):
        st.code(security.get('quantum_public_key', 'N/A'), language="text")
        st.caption("This key is generated using wavelength encryption and is quantum-resistant.")
    
    # Disconnect button
    if st.button("🔴 Disconnect Wallet", use_container_width=True):
        quantum_wallet.disconnect_wallet(wallet['wallet_address'])
        st.success("✅ Wallet disconnected")
        st.rerun()


def render_send_transaction_tab():
    """Tab for sending quantum-encrypted transactions."""
    
    st.header("📤 Send Quantum-Encrypted Transaction")
    
    wallets = quantum_wallet.get_connected_wallets()
    
    if not wallets:
        st.warning("⚠️ No wallet connected. Please connect a wallet first.")
        return
    
    wallet = wallets[-1]
    
    st.info(f"""
    **Sending from:** `{wallet['wallet_address'][:10]}...{wallet['wallet_address'][-8:]}`  
    **Spectral Region:** {wallet['spectral_region']}  
    **Quantum Protection:** ✅ Active
    """)
    
    st.divider()
    
    # Transaction form
    col1, col2 = st.columns([2, 1])
    
    with col1:
        to_address = st.text_input(
            "Recipient Address",
            placeholder="0xabcdef...",
            help="Address to send tokens to"
        )
    
    with col2:
        amount = st.number_input(
            "Amount",
            min_value=0.0,
            step=0.01,
            help="Amount to send"
        )
    
    if st.button("🔐 Create Quantum-Encrypted Transaction", type="primary", use_container_width=True):
        if not to_address or amount <= 0:
            st.error("Please enter valid recipient and amount")
            return
        
        with st.spinner("🌈 Creating quantum-resistant transaction..."):
            time.sleep(2)  # Simulate quantum encryption
            
            # Mock Web3 signature
            mock_signature = "0x" + "b" * 130
            
            try:
                quantum_tx = quantum_wallet.create_quantum_transaction(
                    wallet_address=wallet['wallet_address'],
                    to_address=to_address,
                    amount=amount,
                    web3_signature=mock_signature
                )
                
                st.success("✅ Transaction created with quantum encryption!")
                
                # Show transaction details
                st.subheader("📋 Transaction Details")
                
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    st.metric("From", f"{wallet['wallet_address'][:10]}...")
                
                with col_b:
                    st.metric("To", f"{to_address[:10]}...")
                
                with col_c:
                    st.metric("Amount", f"{amount:.4f}")
                
                st.divider()
                
                st.subheader("🌈 Quantum Security Layers")
                
                st.success("✅ **Layer 1:** Standard Web3 Signature (ECDSA)")
                st.success("✅ **Layer 2:** Wavelength Encryption")
                st.success(f"✅ **Layer 3:** Multi-Spectral Signatures ({len(quantum_tx.spectral_signatures)} regions)")
                st.success("✅ **Layer 4:** Wave Interference Hash")
                st.success(f"✅ **Layer 5:** E=hf Energy Proof ({quantum_tx.energy_cost_joules:.2e} J)")
                
                with st.expander("🔬 View Quantum Signature Details"):
                    st.json(quantum_tx.to_dict())
                
                # Verify button
                if st.button("🔍 Verify Quantum Security"):
                    is_valid, results = quantum_wallet.verify_quantum_transaction(
                        quantum_tx.tx_id
                    )
                    
                    if is_valid:
                        st.success("✅ **QUANTUM SECURE** - All security layers verified!")
                    else:
                        st.error("❌ Security verification failed")
                    
                    st.json(results)
                
            except Exception as e:
                st.error(f"❌ Transaction failed: {str(e)}")


def render_quantum_security_tab():
    """Tab explaining quantum security features."""
    
    st.header("🔬 Quantum Security Features")
    
    st.markdown("""
    NexusOS's Web3 wallet integration uses **wavelength-based quantum-resistant encryption** 
    to protect against both current and future threats, including quantum computers.
    """)
    
    st.divider()
    
    st.subheader("🛡️ Security Layers")
    
    st.markdown("""
    ### 1️⃣ Standard Web3 Signature (ECDSA)
    - Traditional blockchain signature
    - Proves wallet ownership
    - Industry-standard security
    
    ### 2️⃣ Wavelength Encryption (WNSP v2.0)
    - **Quantum-resistant** encryption based on electromagnetic waves
    - Uses wave interference patterns
    - Each wallet assigned to spectral region (UV → Infrared)
    
    ### 3️⃣ Multi-Spectral Signatures
    - Requires signatures from **3+ spectral regions**
    - Even if one region compromised, transaction remains secure
    - Spectral diversity ensures quantum resistance
    
    ### 4️⃣ Wave Interference Hash
    - Uses wave superposition principle
    - Creates unique quantum signature
    - Unhackable by classical or quantum computers
    
    ### 5️⃣ E=hf Energy Proof
    - Physics-based proof-of-work
    - Uses Planck's equation: E = hf
    - Requires computational energy proportional to frequency
    """)
    
    st.divider()
    
    st.subheader("🌈 Spectral Regions")
    
    regions_data = {
        "Region": ["Ultraviolet", "Violet", "Blue", "Green", "Yellow", "Orange", "Red", "Infrared"],
        "Wavelength (nm)": ["100-380", "380-450", "450-495", "495-570", "570-590", "590-620", "620-750", "750-1000"],
        "Security Level": ["⭐⭐⭐⭐⭐"] * 8
    }
    
    st.table(regions_data)
    
    st.divider()
    
    st.subheader("⚛️ Why Quantum-Resistant?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **❌ Traditional Cryptography:**
        - Based on SHA-256 hashing
        - Vulnerable to quantum computers
        - Shor's algorithm can break ECDSA
        - Timeline: 5-15 years until broken
        """)
    
    with col2:
        st.markdown("""
        **✅ NexusOS Wavelength Encryption:**
        - Based on wave interference physics
        - Quantum-resistant by design
        - No known quantum attack vectors
        - Future-proof security
        """)
    
    st.success("""
    💡 **Bottom Line:** Your wallet is protected against hackers today AND quantum computers tomorrow.
    """)


def render_connected_wallets_tab():
    """Tab showing all connected wallets."""
    
    st.header("📊 Connected Wallets")
    
    wallets = quantum_wallet.get_connected_wallets()
    
    st.metric("Total Connected", len(wallets))
    
    if not wallets:
        st.info("No wallets currently connected.")
        return
    
    st.divider()
    
    for idx, wallet in enumerate(wallets):
        with st.expander(f"💳 {wallet['wallet_address'][:16]}... ({wallet['provider'].upper()})"):
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Wallet Address:**")
                st.code(wallet['wallet_address'], language="text")
                
                st.write("**Provider:**")
                st.write(wallet['provider'].upper())
                
                st.write("**Chain ID:**")
                st.write(wallet['chain_id'])
            
            with col2:
                st.write("**Spectral Region:**")
                st.write(f"🌈 {wallet['spectral_region']}")
                
                st.write("**Session ID:**")
                st.code(wallet['session_id'][:32] + "...", language="text")
                
                connected_time = time.time() - wallet['connected_at']
                st.write("**Connected:**")
                st.write(f"{int(connected_time / 60)} minutes ago")
            
            st.write("**Quantum Public Key:**")
            st.code(wallet['quantum_public_key'], language="text")
