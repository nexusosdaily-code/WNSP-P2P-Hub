"""
NexusOS - Civilization Operating System
Unified Dashboard Launcher
=========================================

Central hub providing access to all NexusOS modules:
- Civilization Dashboard (7 tabs with Mobile Wallet)
- Web3 Wallet Dashboard
- WNSP Protocol v2.0
- Wavelength Economics
- Nexus Consensus
- Mobile Connectivity
- Long-term Supply Forecasting
"""

import streamlit as st

# Import all dashboard modules
from civilization_dashboard import main as civilization_main
from web3_wallet_dashboard import render_web3_wallet_dashboard
from wnsp_dashboard_v2 import render_wnsp_v2_dashboard
from wavelength_economics_dashboard import render_wavelength_economics_dashboard
from nexus_consensus_dashboard import render_nexus_consensus_dashboard
from mobile_connectivity_dashboard import show_mobile_connectivity_dashboard
from longterm_supply_dashboard import render_longterm_supply_dashboard


def main():
    """Unified NexusOS Dashboard Launcher"""
    
    # Page config
    st.set_page_config(
        page_title="NexusOS - Civilization Operating System",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    
    # Sidebar - Module Selector
    with st.sidebar:
        st.title("🌍 NexusOS")
        st.markdown("**Civilization Operating System**")
        st.divider()
        
        # Module selector - clean and simple
        module = st.selectbox(
            "**Select Dashboard**",
            [
                "🌍 Civilization Dashboard",
                "💎 Web3 Wallet",
                "📡 WNSP Protocol v2.0",
                "💰 Wavelength Economics",
                "⚙️ Nexus Consensus",
                "📱 Mobile Connectivity",
                "📊 Long-term Supply"
            ],
            key="module_selector"
        )
        
        st.divider()
        
        # Simple module info
        module_info = {
            "🌍 Civilization Dashboard": {
                "icon": "🌍",
                "desc": "Complete civilization architecture with 7 integrated systems",
                "features": ["Wave Computation", "BHLS Floor", "Circular Economy", "Civilization Simulator", "Governance", "Supply Chain", "**Mobile Wallet** 💰"]
            },
            "💎 Web3 Wallet": {
                "icon": "💎",
                "desc": "Native quantum-resistant wallet for NXT tokens",
                "features": ["Create Wallets", "Send NXT", "WNSP Messaging", "Transaction History"]
            },
            "📡 WNSP Protocol v2.0": {
                "icon": "📡",
                "desc": "Wavelength-Native Signaling Protocol with quantum cryptography",
                "features": ["64 Characters", "DAG Messaging", "E=hf Pricing", "Network Visualization"]
            },
            "💰 Wavelength Economics": {
                "icon": "💰",
                "desc": "Physics-based economic validation system",
                "features": ["Wave Validation", "E=hf Economics", "Spectral Consensus"]
            },
            "⚙️ Nexus Consensus": {
                "icon": "⚙️",
                "desc": "Unified consensus engine with GhostDAG + PoS",
                "features": ["Parallel Processing", "Spectral Diversity", "AI Optimization"]
            },
            "📱 Mobile Connectivity": {
                "icon": "📱",
                "desc": "Real-time mobile device network monitoring",
                "features": ["Connected Devices", "Validator Network", "Network Health"]
            },
            "📊 Long-term Supply": {
                "icon": "📊",
                "desc": "50-100 year supply forecasting and analytics",
                "features": ["Predictive Models", "Trend Analysis", "Strategic Insights"]
            }
        }
        
        if module in module_info:
            info = module_info[module]
            with st.expander(f"{info['icon']} About this module"):
                st.write(info['desc'])
                st.markdown("**Features:**")
                for feature in info['features']:
                    st.markdown(f"• {feature}")
        
        st.divider()
        st.caption("🌊 NexusOS v3.0")
        st.caption("Production Ready ✅")
    
    # Main content area - Route to selected module
    if module == "🌍 Civilization Dashboard":
        # Full civilization dashboard with 7 tabs
        civilization_main()
    
    elif module == "💎 Web3 Wallet":
        # Native wallet interface
        render_web3_wallet_dashboard()
    
    elif module == "📡 WNSP Protocol v2.0":
        # WNSP protocol dashboard
        render_wnsp_v2_dashboard()
    
    elif module == "💰 Wavelength Economics":
        # Economics dashboard
        render_wavelength_economics_dashboard()
    
    elif module == "⚙️ Nexus Consensus":
        # Consensus dashboard
        render_nexus_consensus_dashboard()
    
    elif module == "📱 Mobile Connectivity":
        # Mobile connectivity monitor
        show_mobile_connectivity_dashboard()
    
    elif module == "📊 Long-term Supply":
        # Long-term supply forecasting
        render_longterm_supply_dashboard()


if __name__ == "__main__":
    main()
