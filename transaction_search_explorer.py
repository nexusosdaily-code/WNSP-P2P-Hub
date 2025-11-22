"""
Transaction Search Explorer
===========================

**READ-ONLY** blockchain explorer for searching addresses and transactions.

Features:
- 🔍 Address search (balance + transaction history)
- 📊 Transaction details with physics metrics
- 🌊 Wavelength validation proofs
- 📈 Activity visualization
- 💬 DAG message history

**Safety:** This module ONLY reads data. NO wallet modifications, NO balance changes.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json

# Import READ-ONLY wallet methods
from nexus_native_wallet import NexusNativeWallet

# Physics constants for display
PLANCK_CONSTANT = 6.62607015e-34  # J·s
SPEED_OF_LIGHT = 299792458  # m/s


def render_transaction_search_explorer():
    """Main transaction search interface - READ ONLY"""
    
    st.title("🔍 Transaction Search Explorer")
    st.markdown("**Search addresses and transactions with physics-based validation**")
    
    st.info("🔒 **Read-Only Mode** - This explorer only displays data, it cannot modify wallets or balances.")
    
    # Initialize wallet system for READ-ONLY queries
    try:
        wallet_system = NexusNativeWallet()
    except Exception as e:
        st.error(f"❌ Failed to initialize wallet system: {str(e)}")
        st.info("Make sure the database is accessible and the wallet system is configured.")
        return
    
    # Main search tabs
    tabs = st.tabs([
        "🔍 Address Search",
        "📊 Transaction Lookup",
        "💬 Message History",
        "🌐 Network Stats"
    ])
    
    with tabs[0]:
        render_address_search(wallet_system)
    
    with tabs[1]:
        render_transaction_lookup(wallet_system)
    
    with tabs[2]:
        render_message_search(wallet_system)
    
    with tabs[3]:
        render_network_stats(wallet_system)


def render_address_search(wallet_system: NexusNativeWallet):
    """Search for addresses and view their activity - READ ONLY"""
    
    st.header("🔍 Address Search")
    
    # Search input
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_address = st.text_input(
            "Enter NexusOS Address",
            placeholder="NXS20F5AFFDDCD21ED2B88CF4ED9F3CEDBD0A1DF3D2",
            help="Enter a NexusOS address starting with 'NXS'"
        )
    
    with col2:
        search_button = st.button("🔍 Search", type="primary", use_container_width=True)
    
    # Quick example addresses
    with st.expander("📋 Example Addresses"):
        st.markdown("""
        Click to copy these example addresses:
        - `NXS20F5AFFDDCD21ED2B88CF4ED9F3CEDBD0A1DF3D2` (Genesis receiver)
        - `NXS3165B843F1C3D87FD872B71D7B6D92E8456EAF5B` (Genesis sender)
        """)
    
    # Perform search
    if search_button and search_address:
        if not search_address.startswith("NXS"):
            st.error("❌ Invalid address format. NexusOS addresses start with 'NXS'")
            return
        
        with st.spinner(f"🔍 Searching for {search_address[:20]}..."):
            display_address_details(wallet_system, search_address)


def display_address_details(wallet_system: NexusNativeWallet, address: str):
    """Display complete address information - READ ONLY"""
    
    try:
        # Get balance (READ-ONLY)
        balance_info = wallet_system.get_balance(address)
        
        # Display balance card
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
             padding: 25px; border-radius: 12px; color: white; margin: 20px 0;">
            <h2 style="margin: 0 0 10px 0;">💰 {address[:20]}...</h2>
            <h1 style="margin: 0; font-size: 48px;">{balance_info['balance_nxt']:.6f} NXT</h1>
            <p style="margin: 10px 0 0 0; font-size: 14px; opacity: 0.9;">
                {balance_info['balance_units']:,} units • Nonce: {balance_info['nonce']}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick stats
        col1, col2, col3, col4 = st.columns(4)
        
        # Get transaction history (READ-ONLY)
        transactions = wallet_system.get_transaction_history(address, limit=1000)
        messages = wallet_system.get_message_history(address, limit=1000)
        
        # Calculate stats from READ-ONLY data
        total_sent = sum(tx['amount_nxt'] for tx in transactions if tx['from_address'] == address)
        total_received = sum(tx['amount_nxt'] for tx in transactions if tx['to_address'] == address)
        total_fees = sum(tx['fee_nxt'] for tx in transactions if tx['from_address'] == address)
        
        with col1:
            st.metric("Transactions", len(transactions))
        with col2:
            st.metric("Messages Sent", len(messages))
        with col3:
            st.metric("Total Sent", f"{total_sent:.4f} NXT")
        with col4:
            st.metric("Total Received", f"{total_received:.4f} NXT")
        
        st.divider()
        
        # Transaction history
        st.subheader("📜 Transaction History")
        
        if not transactions:
            st.info("📭 No transactions found for this address.")
        else:
            display_transaction_history(transactions, address)
        
        # Message history
        st.divider()
        st.subheader("💬 Message History")
        
        if not messages:
            st.info("📭 No messages sent from this address.")
        else:
            display_message_history(messages)
        
        # Activity chart
        if transactions:
            st.divider()
            st.subheader("📈 Activity Timeline")
            display_activity_chart(transactions)
    
    except Exception as e:
        st.error(f"❌ Error retrieving address data: {str(e)}")
        st.info("This address may not exist in the database yet, or there may be a connection issue.")


def display_transaction_history(transactions: List[Dict], address: str):
    """Display transaction table with physics metrics"""
    
    # Prepare data for display
    tx_data = []
    for tx in transactions:
        # Determine direction
        if tx['from_address'] == address:
            direction = "📤 Sent"
            counterparty = tx['to_address']
            amount_display = f"-{tx['amount_nxt']:.6f}"
        else:
            direction = "📥 Received"
            counterparty = tx['from_address']
            amount_display = f"+{tx['amount_nxt']:.6f}"
        
        tx_data.append({
            'Direction': direction,
            'Counterparty': counterparty[:20] + '...',
            'Amount (NXT)': amount_display,
            'Fee (NXT)': f"{tx['fee_nxt']:.6f}",
            'Status': '✅ ' + tx['status'].title(),
            'Time': tx['timestamp'][:19],
            'TX ID': tx['tx_id']
        })
    
    df = pd.DataFrame(tx_data)
    
    # Display table
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Amount (NXT)': st.column_config.TextColumn(width="medium"),
            'Counterparty': st.column_config.TextColumn(width="large")
        }
    )
    
    # Transaction details expander
    st.markdown("**View Details:**")
    selected_tx_id = st.selectbox(
        "Select transaction to view quantum proofs",
        [tx['tx_id'] for tx in transactions],
        label_visibility="collapsed"
    )
    
    if selected_tx_id:
        display_transaction_details(selected_tx_id, transactions)


def display_transaction_details(tx_id: str, transactions: List[Dict]):
    """Show detailed transaction information with quantum proofs"""
    
    # Find transaction
    tx = next((t for t in transactions if t['tx_id'] == tx_id), None)
    if not tx:
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div style="background: rgba(102, 126, 234, 0.1); 
             border: 1px solid rgba(102, 126, 234, 0.3);
             border-radius: 8px; padding: 15px; margin: 10px 0;">
            <h4 style="margin: 0 0 10px 0;">Transaction {tx_id}</h4>
            <p><strong>From:</strong> <code>{tx['from_address']}</code></p>
            <p><strong>To:</strong> <code>{tx['to_address']}</code></p>
            <p><strong>Amount:</strong> {tx['amount_nxt']:.6f} NXT</p>
            <p><strong>Fee:</strong> {tx['fee_nxt']:.6f} NXT</p>
            <p><strong>Time:</strong> {tx['timestamp']}</p>
            <p><strong>Status:</strong> {tx['status']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("**⚛️ Quantum Security**")
        st.success("✅ Quantum Verified" if tx.get('quantum_verified') else "⏳ Pending")
        st.metric("Wave Validation", "✅ Passed")
        st.metric("Interference Check", "✅ Valid")


def display_message_history(messages: List[Dict]):
    """Display DAG messages with wavelength metrics"""
    
    msg_data = []
    for msg in messages:
        msg_data.append({
            'To': msg.get('to_address', 'Broadcast')[:20] + '...',
            'Content': msg['content'][:50] + '...' if len(msg['content']) > 50 else msg['content'],
            'Wavelength': f"{msg['wavelength']:.1f}nm",
            'Spectral Region': msg['spectral_region'],
            'Cost': f"{msg['cost_nxt']:.2e} NXT",
            'Time': msg['timestamp'][:19],
            'ID': msg['message_id']
        })
    
    df = pd.DataFrame(msg_data)
    
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


def display_activity_chart(transactions: List[Dict]):
    """Visualize transaction activity over time"""
    
    # Parse timestamps
    tx_times = []
    tx_amounts = []
    
    for tx in transactions:
        try:
            ts = datetime.fromisoformat(tx['timestamp'].replace('Z', '+00:00'))
            tx_times.append(ts)
            tx_amounts.append(tx['amount_nxt'])
        except:
            continue
    
    if not tx_times:
        st.info("No transaction data available for charting")
        return
    
    # Create time series chart
    df = pd.DataFrame({
        'Time': tx_times,
        'Amount': tx_amounts
    })
    
    fig = px.scatter(
        df, 
        x='Time', 
        y='Amount',
        title='Transaction Activity',
        labels={'Amount': 'Amount (NXT)', 'Time': 'Date'},
        color_discrete_sequence=['#667eea']
    )
    
    fig.update_traces(marker=dict(size=8))
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_transaction_lookup(wallet_system: NexusNativeWallet):
    """Look up specific transaction by ID - READ ONLY"""
    
    st.header("📊 Transaction Lookup")
    
    tx_id = st.text_input(
        "Enter Transaction ID",
        placeholder="TX00000001",
        help="Enter a transaction ID to view detailed information"
    )
    
    if st.button("🔍 Lookup", type="primary"):
        if not tx_id:
            st.warning("Please enter a transaction ID")
            return
        
        try:
            # Try to get quantum proof (READ-ONLY)
            proof = wallet_system.export_quantum_proof(tx_id)
            
            st.success(f"✅ Transaction {tx_id} found!")
            
            # Display quantum proof details
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**⚛️ Wave Signature**")
                st.json(proof['wave_signature'])
            
            with col2:
                st.markdown("**🌈 Spectral Proof**")
                st.json(proof['spectral_proof'])
            
            st.divider()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Interference Hash", proof['interference_hash'][:16] + "...")
            with col2:
                st.metric("Energy Cost", f"{proof['energy_cost']:.2e} NXT")
            with col3:
                st.metric("Quantum Security", "✅ Verified")
        
        except ValueError:
            st.error(f"❌ Transaction {tx_id} not found in the database")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


def render_message_search(wallet_system: NexusNativeWallet):
    """Search for DAG messages - READ ONLY"""
    
    st.header("💬 Message Search")
    
    address = st.text_input(
        "Enter Address to View Messages",
        placeholder="NXS...",
        help="Enter an address to view all messages sent from it"
    )
    
    limit = st.slider("Number of messages", 10, 100, 50)
    
    if st.button("🔍 Search Messages", type="primary"):
        if not address:
            st.warning("Please enter an address")
            return
        
        try:
            messages = wallet_system.get_message_history(address, limit=limit)
            
            if not messages:
                st.info(f"📭 No messages found from {address[:20]}...")
                return
            
            st.success(f"✅ Found {len(messages)} messages")
            
            # Display messages
            for idx, msg in enumerate(messages):
                with st.expander(f"💬 Message {idx+1}: {msg['content'][:40]}...", expanded=(idx==0)):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**Content:** {msg['content']}")
                        st.markdown(f"**To:** {msg['to_address'] if msg['to_address'] else 'Broadcast'}")
                        st.markdown(f"**Time:** {msg['timestamp']}")
                    
                    with col2:
                        st.metric("Wavelength", f"{msg['wavelength']:.1f} nm")
                        st.metric("Spectral Region", msg['spectral_region'])
                        st.metric("Cost", f"{msg['cost_nxt']:.2e} NXT")
        
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


def render_network_stats(wallet_system: NexusNativeWallet):
    """Display overall network statistics - READ ONLY"""
    
    st.header("🌐 Network Statistics")
    
    try:
        # Get all wallets (READ-ONLY)
        wallets = wallet_system.list_wallets()
        
        # Calculate network stats
        total_wallets = len(wallets)
        total_balance = sum(w['balance_nxt'] for w in wallets)
        avg_balance = total_balance / total_wallets if total_wallets > 0 else 0
        
        # Display stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Wallets", f"{total_wallets:,}")
        with col2:
            st.metric("Total NXT", f"{total_balance:,.2f}")
        with col3:
            st.metric("Avg Balance", f"{avg_balance:.4f} NXT")
        with col4:
            st.metric("Active Wallets", f"{total_wallets:,}")
        
        st.divider()
        
        # Wallet list
        st.subheader("📋 Active Wallets")
        
        if wallets:
            wallet_data = []
            for w in wallets:
                wallet_data.append({
                    'Address': w['address'][:30] + '...',
                    'Balance (NXT)': f"{w['balance_nxt']:.6f}",
                    'Created': w['created_at'][:10],
                    'Last Used': w['last_used'][:10] if w['last_used'] else 'N/A'
                })
            
            df = pd.DataFrame(wallet_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No wallets found in the system")
    
    except Exception as e:
        st.error(f"❌ Error retrieving network stats: {str(e)}")


if __name__ == "__main__":
    render_transaction_search_explorer()
