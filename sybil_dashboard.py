"""
Sybil Detection Dashboard
=========================

Interactive Streamlit dashboard for monitoring and managing Sybil attack detection.
Provides real-time visualization of clusters, penalties, and system health.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
from sybil_integration import get_sybil_monitor
from sybil_detection import ClusterSeverity


def render_sybil_detection_dashboard(
    validator_economics=None,
    civic_governance=None,
    ghostdag_engine=None
):
    """
    Main Sybil detection dashboard.
    
    Args:
        validator_economics: ValidatorEconomicsSystem instance
        civic_governance: CivicGovernance instance
        ghostdag_engine: Optional GhostDAGEngine instance
    """
    st.title("🛡️ Sybil Attack Detection System")
    st.markdown("### Multi-Dimensional Cluster Analysis & Automated Defense")
    
    # Get monitor
    monitor = get_sybil_monitor(auto_penalize=True)
    
    # Header controls
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown("**Real-time monitoring of coordinated validator attacks**")
    
    with col2:
        scan_interval = st.number_input(
            "Scan Interval (sec)",
            min_value=60,
            max_value=3600,
            value=monitor.scan_interval_seconds,
            step=60
        )
        monitor.scan_interval_seconds = scan_interval
    
    with col3:
        if st.button("🔍 Force Scan Now", use_container_width=True):
            with st.spinner("Scanning validators..."):
                if validator_economics and civic_governance:
                    detections = monitor.scan_for_sybil_attacks(
                        validator_economics,
                        civic_governance,
                        ghostdag_engine,
                        force_scan=True
                    )
                    if detections:
                        st.success(f"Scan complete: {len(detections)} clusters detected!")
                    else:
                        st.info("Scan complete: No Sybil clusters detected")
    
    st.divider()
    
    # System Health Overview
    health_report = monitor.get_system_health_report()
    
    st.markdown("## 📊 System Health Overview")
    
    health_cols = st.columns(5)
    
    with health_cols[0]:
        health_score = health_report["health_score"]
        color = "🟢" if health_score > 0.8 else "🟡" if health_score > 0.6 else "🔴"
        st.metric(
            "Health Score",
            f"{color} {health_score:.1%}",
            health_report["health_status"]
        )
    
    with health_cols[1]:
        st.metric(
            "Total Scans",
            f"{health_report['total_scans_performed']:,}",
            f"Every {scan_interval}s"
        )
    
    with health_cols[2]:
        flagged = health_report.get("flagged_validators_percentage", 0)
        st.metric(
            "Flagged Validators",
            f"{flagged:.1f}%",
            "of network"
        )
    
    with health_cols[3]:
        banned = health_report["penalty_summary"].get("validators_banned", 0)
        st.metric(
            "Banned Validators",
            f"{banned:,}",
            "Permanent"
        )
    
    with health_cols[4]:
        jailed = health_report["penalty_summary"].get("validators_jailed", 0)
        st.metric(
            "Jailed Validators",
            f"{jailed:,}",
            "Temporary"
        )
    
    st.divider()
    
    # Tabs for different views
    tabs = st.tabs([
        "🔍 Active Clusters",
        "📈 Detection Vectors",
        "⚖️ Penalty System",
        "👤 Validator Risk",
        "📊 Analytics"
    ])
    
    # Tab 1: Active Clusters
    with tabs[0]:
        render_active_clusters_tab(health_report)
    
    # Tab 2: Detection Vectors
    with tabs[1]:
        render_detection_vectors_tab(health_report)
    
    # Tab 3: Penalty System
    with tabs[2]:
        render_penalty_system_tab(health_report)
    
    # Tab 4: Validator Risk
    with tabs[3]:
        render_validator_risk_tab(monitor)
    
    # Tab 5: Analytics
    with tabs[4]:
        render_analytics_tab(health_report)


def render_active_clusters_tab(health_report):
    """Render active Sybil clusters"""
    st.markdown("### 🎯 Detected Sybil Clusters")
    
    detection_summary = health_report.get("detection_summary", {})
    recent_detections = detection_summary.get("recent_detections", [])
    
    if not recent_detections:
        st.info("✅ No active Sybil clusters detected. Network is clean!")
        return
    
    # Display each cluster
    for i, detection in enumerate(recent_detections):
        severity = detection.get("severity", "NONE")
        confidence = detection.get("confidence", 0.0)
        cluster_size = detection.get("size", 0)
        
        # Color code by severity
        severity_colors = {
            "CRITICAL": "🔴",
            "HIGH": "🟠",
            "MEDIUM": "🟡",
            "LOW": "🟢",
            "NONE": "⚪"
        }
        
        color = severity_colors.get(severity, "⚪")
        
        with st.expander(
            f"{color} Cluster #{i+1}: {cluster_size} validators - {severity} ({confidence:.0%} confidence)",
            expanded=(severity in ["CRITICAL", "HIGH"])
        ):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Cluster ID:** `{detection.get('cluster_id', 'N/A')}`")
                st.markdown(f"**Size:** {cluster_size} coordinated validators")
                st.markdown(f"**Confidence:** {confidence:.1%}")
            
            with col2:
                st.markdown(f"**Severity:** {severity}")
                detected_at = datetime.fromtimestamp(detection.get("timestamp", time.time()))
                st.markdown(f"**Detected:** {detected_at.strftime('%Y-%m-%d %H:%M:%S')}")
            
            st.markdown("---")
            st.markdown("**Evidence:**")
            if detection_summary.get("total_detections", 0) > 0:
                st.info("Detected through multiple independent vectors - temporal registration patterns, behavioral correlation, and/or economic clustering.")
            else:
                st.info("No active clusters currently detected. Monitoring continues.")


def render_detection_vectors_tab(health_report):
    """Render detection vector performance"""
    st.markdown("### 🔬 Detection Vector Analysis")
    
    detection_summary = health_report.get("detection_summary", {})
    total_detections = detection_summary.get("total_detections", 0)
    
    if total_detections == 0:
        st.info("""
        ℹ️ **No detections yet** - The system is actively monitoring but hasn't detected any Sybil clusters.
        
        Detection vectors are operational and scanning every 5 minutes. Run a manual scan or wait for natural
        validator activity to see detection performance.
        """)
        
        # Show vector descriptions when no data available
        st.markdown("### 🛡️ Active Detection Vectors")
        
        vectors_info = [
            {"Vector": "Temporal Clustering", "Method": "Time-window analysis", "Threshold": "≥3 validators in 1 hour"},
            {"Vector": "Behavioral Correlation", "Method": "Pearson correlation", "Threshold": "≥0.8 correlation"},
            {"Vector": "Economic Tracing", "Method": "Funding source analysis", "Threshold": "≥3 from same source"},
            {"Vector": "Network Topology", "Method": "ISP/IP clustering", "Threshold": "≥5 same ISP or ≥3 same subnet"},
            {"Vector": "Spectral Coordination", "Method": "Cross-region behavioral analysis", "Threshold": "≥5 regions + high correlation"},
            {"Vector": "Device Fingerprinting", "Method": "DBSCAN timing analysis", "Threshold": "≥3 identical signatures"},
            {"Vector": "Statistical Analysis", "Method": "Community detection", "Threshold": "Graph-based clustering"}
        ]
        
        df = pd.DataFrame(vectors_info)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        return
    
    # Show recent detections breakdown by vector
    st.markdown(f"### 📊 Detection Summary ({total_detections} clusters detected)")
    
    recent_detections = detection_summary.get("recent_detections", [])
    
    # Analyze which vectors contributed to detections
    vector_contributions = {
        "Temporal": 0,
        "Behavioral": 0,
        "Economic": 0,
        "Network": 0,
        "Spectral": 0,
        "Device": 0,
        "Statistical": 0
    }
    
    for detection in recent_detections:
        # Note: Real detection vectors would be in detection data
        # For now, acknowledge this needs integration with actual detection results
        pass
    
    st.info("""
    **Note**: Detection vector performance metrics will be populated as clusters are detected and analyzed.
    Each detection records which vectors contributed to identifying the Sybil attack pattern.
    """)


def render_penalty_system_tab(health_report):
    """Render penalty system statistics"""
    st.markdown("### ⚖️ Automated Penalty System")
    
    penalty_summary = health_report.get("penalty_summary", {})
    
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_penalties = penalty_summary.get("total_penalties_applied", 0)
        st.metric("Total Penalties", f"{total_penalties:,}")
    
    with col2:
        total_slashed = penalty_summary.get("total_stake_slashed", 0.0)
        st.metric("Total Slashed", f"{total_slashed:,.0f} NXT")
    
    with col3:
        banned = penalty_summary.get("validators_banned", 0)
        st.metric("Permanently Banned", f"{banned:,}")
    
    with col4:
        jailed = penalty_summary.get("validators_jailed", 0)
        st.metric("Currently Jailed", f"{jailed:,}")
    
    st.markdown("---")
    
    # Severity breakdown
    st.markdown("### Penalty Severity Distribution")
    
    severity_breakdown = penalty_summary.get("severity_breakdown", {})
    
    if severity_breakdown:
        fig = go.Figure(data=[go.Pie(
            labels=list(severity_breakdown.keys()),
            values=list(severity_breakdown.values()),
            hole=0.4,
            marker_colors=['#dc2626', '#ea580c', '#eab308', '#22c55e', '#6b7280']
        )])
        
        fig.update_layout(
            title="Penalties by Severity Level",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent penalties
    st.markdown("### Recent Penalty Actions")
    
    recent_penalties = penalty_summary.get("recent_penalties", [])
    
    if recent_penalties:
        penalty_df = pd.DataFrame(recent_penalties)
        penalty_df['applied_at'] = penalty_df['applied_at'].apply(
            lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S') if x else 'N/A'
        )
        penalty_df['slash_pct'] = penalty_df['slash_pct'].apply(lambda x: f"{x:.0%}")
        
        st.dataframe(penalty_df, use_container_width=True, hide_index=True)
    else:
        st.info("No penalties applied yet")


def render_validator_risk_tab(monitor):
    """Render validator risk assessment"""
    st.markdown("### 👤 Validator Risk Assessment")
    
    # Input for validator lookup
    validator_id = st.text_input("Enter Validator ID to check risk score:")
    
    if validator_id:
        risk_assessment = monitor.get_validator_risk_score(validator_id)
        
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            risk_score = risk_assessment["risk_score"]
            color = "🔴" if risk_score > 0.7 else "🟡" if risk_score > 0.4 else "🟢"
            st.metric("Risk Score", f"{color} {risk_score:.1%}")
        
        with col2:
            st.metric("Risk Level", risk_assessment["risk_level"])
        
        with col3:
            st.metric("Status", risk_assessment["status"].upper())
        
        if risk_assessment.get("factors"):
            st.markdown("**Risk Factors:**")
            for factor in risk_assessment["factors"]:
                st.warning(f"⚠️ {factor}")
        else:
            st.success("✅ No risk factors detected")


def render_analytics_tab(health_report):
    """Render system analytics and trends"""
    st.markdown("### 📊 System Analytics")
    
    # Get real stats from health report
    total_scans = health_report.get("total_scans_performed", 0)
    detection_summary = health_report.get("detection_summary", {})
    penalty_summary = health_report.get("penalty_summary", {})
    
    total_detections = detection_summary.get("total_detections", 0)
    total_slashed = penalty_summary.get("total_stake_slashed", 0.0)
    
    # Summary stats
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Scans Performed", f"{total_scans:,}")
    
    with col2:
        st.metric("Total Clusters Detected", f"{total_detections:,}")
    
    with col3:
        st.metric("Total NXT Slashed", f"{total_slashed:,.0f}")
    
    st.divider()
    
    # Detection effectiveness info
    st.markdown("### 🔍 Detection System Effectiveness")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **Temporal Clustering**: Detects validators registering within suspicious time windows (default: 1 hour).
        Highly effective at catching bulk validator registration attacks.
        """)
        
        st.info("""
        **Behavioral Clustering**: Uses Pearson correlation to detect validators with identical voting patterns
        across proposals (threshold: 0.8 correlation).
        """)
        
        st.info("""
        **Economic Clustering**: Traces funding sources to detect validators funded from the same wallet.
        Prevents "wash trading" attacks where one entity splits funds across fake validators.
        """)
    
    with col2:
        st.success("""
        **Spectral Coordination Detection**: The critical defense against 100-phone attacks.
        Identifies validators that vote identically across ALL spectral regions despite appearing independent.
        """)
        
        st.success("""
        **Device Fingerprinting**: Uses DBSCAN clustering on block creation timing patterns to detect
        validators running on identical hardware/software configurations.
        """)
        
        st.success("""
        **Network Topology Analysis**: Detects validators operating from the same ISP or IP subnet,
        identifying datacenter-based Sybil attacks.
        """)


def main():
    """Standalone dashboard for testing"""
    st.set_page_config(
        page_title="Sybil Detection System",
        page_icon="🛡️",
        layout="wide"
    )
    
    render_sybil_detection_dashboard()


if __name__ == "__main__":
    main()
