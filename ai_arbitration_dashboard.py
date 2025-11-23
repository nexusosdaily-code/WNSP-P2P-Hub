"""
AI Arbitration Dashboard
Centralized interface for AI-powered dispute resolution and moderation

Features:
- File new disputes and appeals
- Track arbitration cases
- View AI decisions and reasoning
- Submit evidence
- Monitor system statistics
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, List, Optional, Any
from datetime import datetime
import time

from ai_arbitration_controller import (
    get_arbitration_controller,
    DisputeType,
    DisputeStatus,
    ArbitrationDecision
)

from arbitration_penalty_appeals import get_penalty_bridge
from arbitration_governance import get_governance_arbitration


def render_arbitration_dashboard():
    """Main AI Arbitration Dashboard"""
    st.title("⚖️ AI Arbitration & Moderation Control")
    
    st.markdown("""
    **Autonomous AI-powered dispute resolution system**
    
    The AI Arbitration Controller provides neutral, evidence-based mediation for:
    - Penalty appeals (Sybil detection disputes)
    - Governance conflicts (contentious proposals)
    - Validator disagreements
    - Resource allocation disputes
    - Community conflicts
    """)
    
    # Get controllers
    arbitration = get_arbitration_controller()
    penalty_bridge = get_penalty_bridge()
    gov_arbitration = get_governance_arbitration()
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Overview",
        "📝 File Dispute",
        "🔍 Active Cases",
        "⚖️ Penalty Appeals",
        "🏛️ Governance Mediation",
        "📈 Statistics"
    ])
    
    with tab1:
        render_overview_tab(arbitration, penalty_bridge, gov_arbitration)
    
    with tab2:
        render_file_dispute_tab(arbitration, penalty_bridge, gov_arbitration)
    
    with tab3:
        render_active_cases_tab(arbitration)
    
    with tab4:
        render_penalty_appeals_tab(penalty_bridge)
    
    with tab5:
        render_governance_mediation_tab(gov_arbitration)
    
    with tab6:
        render_statistics_tab(arbitration, penalty_bridge, gov_arbitration)


def render_overview_tab(arbitration, penalty_bridge, gov_arbitration):
    """Render system overview"""
    st.markdown("### 🎯 Arbitration System Status")
    
    # Get statistics
    arb_stats = arbitration.get_statistics()
    appeal_stats = penalty_bridge.get_appeal_statistics()
    gov_stats = gov_arbitration.get_statistics()
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Cases",
            arb_stats["total_cases"],
            delta=f"{arb_stats['pending_cases']} pending"
        )
    
    with col2:
        resolution_rate = (
            arb_stats["resolved_cases"] / max(1, arb_stats["total_cases"]) * 100
        )
        st.metric(
            "Resolution Rate",
            f"{resolution_rate:.0f}%"
        )
    
    with col3:
        st.metric(
            "Penalty Appeals",
            appeal_stats["total_appeals"],
            delta=f"{appeal_stats['successful_appeals']} successful"
        )
    
    with col4:
        st.metric(
            "Governance Mediations",
            gov_stats["total_mediations"],
            delta=f"{gov_stats['average_controversy']:.0%} avg controversy"
        )
    
    # Recent activity
    st.markdown("### 📋 Recent Arbitration Activity")
    
    recent_decisions = arbitration.decision_history[-10:][::-1]  # Last 10, reversed
    
    if recent_decisions:
        decision_data = []
        for decision in recent_decisions:
            decision_data.append({
                "Case ID": decision["case_id"][:16] + "...",
                "Type": decision["dispute_type"].replace("_", " ").title(),
                "Decision": decision["decision"].replace("_", " ").title(),
                "Confidence": f"{decision['confidence']:.0%}",
                "Timestamp": datetime.fromtimestamp(decision["timestamp"]).strftime("%Y-%m-%d %H:%M")
            })
        
        df = pd.DataFrame(decision_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No arbitration decisions yet")
    
    # System health
    st.markdown("### 🏥 System Health")
    
    col1, col2 = st.columns(2)
    
    with col1:
        avg_confidence = arb_stats["average_confidence"]
        confidence_status = "🟢 Excellent" if avg_confidence > 0.8 else "🟡 Good" if avg_confidence > 0.6 else "🟠 Fair"
        
        st.markdown(f"""
        **AI Confidence**: {avg_confidence:.0%} {confidence_status}
        
        Average confidence in autonomous decisions. Higher is better.
        """)
    
    with col2:
        escalation_rate = arb_stats["escalated_cases"] / max(1, arb_stats["total_cases"])
        escalation_status = "🟢 Low" if escalation_rate < 0.1 else "🟡 Moderate" if escalation_rate < 0.3 else "🟠 High"
        
        st.markdown(f"""
        **Escalation Rate**: {escalation_rate:.0%} {escalation_status}
        
        Cases escalated to human governance. Lower is better.
        """)


def render_file_dispute_tab(arbitration, penalty_bridge, gov_arbitration):
    """Render dispute filing interface"""
    st.markdown("### 📝 File New Dispute or Appeal")
    
    dispute_type = st.selectbox(
        "Dispute Type",
        [
            "Penalty Appeal",
            "Governance Mediation",
            "Validator Conflict",
            "Resource Allocation",
            "Community Conflict"
        ]
    )
    
    if dispute_type == "Penalty Appeal":
        render_penalty_appeal_form(penalty_bridge)
    
    elif dispute_type == "Governance Mediation":
        render_governance_mediation_form(gov_arbitration)
    
    else:
        render_general_dispute_form(arbitration, dispute_type)


def render_penalty_appeal_form(penalty_bridge):
    """Render penalty appeal form"""
    st.markdown("#### Appeal a Sybil Detection Penalty")
    
    with st.form("penalty_appeal_form"):
        penalty_id = st.text_input(
            "Penalty ID",
            placeholder="PEN1A2B3C4D5E6F7G",
            help="Enter the ID of the penalty you wish to appeal"
        )
        
        validator_address = st.text_input(
            "Your Validator Address",
            placeholder="NXS1234567890abcdef...",
            help="Your validator address (plaintiff)"
        )
        
        appeal_reason = st.text_area(
            "Appeal Reason",
            placeholder="Explain why you believe this penalty was issued in error...",
            height=150,
            help="Detailed explanation of why the penalty should be reviewed"
        )
        
        st.markdown("**Additional Evidence (Optional)**")
        
        evidence_type = st.selectbox(
            "Evidence Type",
            ["None", "Blockchain Transaction", "Performance Record", "Witness Statement", "Other"]
        )
        
        evidence_content = st.text_area(
            "Evidence Details",
            placeholder="Provide details of your evidence...",
            height=100
        )
        
        submitted = st.form_submit_button("Submit Appeal", type="primary")
        
        if submitted:
            if not penalty_id or not validator_address or not appeal_reason:
                st.error("Please fill in all required fields")
            else:
                try:
                    # Prepare evidence
                    evidence_list = []
                    if evidence_type != "None" and evidence_content:
                        evidence_list.append({
                            "type": evidence_type.lower().replace(" ", "_"),
                            "content": {"details": evidence_content}
                        })
                    
                    # File appeal
                    appeal_id = penalty_bridge.file_penalty_appeal(
                        penalty_id=penalty_id,
                        validator_address=validator_address,
                        appeal_reason=appeal_reason,
                        evidence=evidence_list if evidence_list else None
                    )
                    
                    st.success(f"✅ Appeal filed successfully!")
                    st.info(f"**Appeal ID**: {appeal_id}")
                    st.markdown("""
                    Your appeal has been submitted to the AI Arbitration Controller.
                    
                    **Next Steps**:
                    1. AI will analyze the penalty record and your evidence
                    2. Decision typically issued within 24 hours
                    3. Check the "Penalty Appeals" tab to track status
                    """)
                    
                except Exception as e:
                    st.error(f"Error filing appeal: {str(e)}")


def render_governance_mediation_form(gov_arbitration):
    """Render governance mediation request form"""
    st.markdown("#### Request Mediation for Contentious Proposal")
    
    # Show contentious proposals
    contentious = gov_arbitration.get_contentious_proposals()
    
    if contentious:
        st.markdown(f"**🔥 {len(contentious)} Contentious Proposals Detected**")
        
        for prop in contentious[:5]:  # Show top 5
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"**{prop['title']}**")
            
            with col2:
                st.markdown(f"Controversy: {prop['controversy_score']:.0%}")
            
            with col3:
                st.markdown(f"Split: {prop['vote_split']['for']:.0%}/{prop['vote_split']['against']:.0%}")
    
    st.markdown("---")
    
    with st.form("governance_mediation_form"):
        proposal_id = st.text_input(
            "Proposal ID",
            placeholder="PROP1234567890",
            help="ID of the proposal requiring mediation"
        )
        
        requestor = st.text_input(
            "Your Address",
            placeholder="NXS1234567890abcdef...",
            help="Your address (mediation requestor)"
        )
        
        reason = st.text_area(
            "Mediation Request Reason",
            placeholder="Explain why this proposal requires AI mediation...",
            height=150
        )
        
        submitted = st.form_submit_button("Request Mediation", type="primary")
        
        if submitted:
            if not proposal_id or not requestor:
                st.error("Please fill in all required fields")
            else:
                try:
                    mediation_id = gov_arbitration.request_mediation(
                        proposal_id=proposal_id,
                        requestor=requestor,
                        reason=reason or "Mediation requested due to high controversy"
                    )
                    
                    st.success(f"✅ Mediation request filed successfully!")
                    st.info(f"**Mediation ID**: {mediation_id}")
                    st.markdown("""
                    AI will analyze the proposal and generate:
                    - Impact analysis on stakeholder groups
                    - Risk assessment
                    - Neutral recommendations
                    - Mediation strategy
                    """)
                    
                except Exception as e:
                    st.error(f"Error requesting mediation: {str(e)}")


def render_general_dispute_form(arbitration, dispute_type):
    """Render general dispute filing form"""
    st.markdown(f"#### File {dispute_type}")
    
    with st.form("general_dispute_form"):
        title = st.text_input(
            "Dispute Title",
            placeholder="Brief description of the dispute"
        )
        
        plaintiff = st.text_input(
            "Your Address (Plaintiff)",
            placeholder="NXS1234567890abcdef..."
        )
        
        defendant = st.text_input(
            "Other Party Address (Optional)",
            placeholder="NXS0987654321fedcba..."
        )
        
        description = st.text_area(
            "Detailed Description",
            placeholder="Provide a detailed description of the dispute...",
            height=200
        )
        
        submitted = st.form_submit_button("File Dispute", type="primary")
        
        if submitted:
            if not title or not plaintiff or not description:
                st.error("Please fill in all required fields")
            else:
                try:
                    # Map UI type to DisputeType enum
                    type_mapping = {
                        "Validator Conflict": DisputeType.VALIDATOR_CONFLICT,
                        "Resource Allocation": DisputeType.RESOURCE_ALLOCATION,
                        "Community Conflict": DisputeType.COMMUNITY_CONFLICT
                    }
                    
                    case_id = arbitration.file_dispute(
                        dispute_type=type_mapping[dispute_type],
                        plaintiff=plaintiff,
                        title=title,
                        description=description,
                        defendant=defendant if defendant else None
                    )
                    
                    st.success(f"✅ Dispute filed successfully!")
                    st.info(f"**Case ID**: {case_id}")
                    
                except Exception as e:
                    st.error(f"Error filing dispute: {str(e)}")


def render_active_cases_tab(arbitration):
    """Render active arbitration cases"""
    st.markdown("### 🔍 Active Arbitration Cases")
    
    pending_cases = arbitration.get_pending_cases()
    
    if not pending_cases:
        st.info("No active cases currently under review")
        return
    
    for case in pending_cases:
        with st.expander(f"**{case.title}** ({case.case_id[:16]}...)"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Type**: {case.dispute_type.value.replace('_', ' ').title()}")
                st.markdown(f"**Status**: {case.status.value.replace('_', ' ').title()}")
                st.markdown(f"**Filed**: {datetime.fromtimestamp(case.filed_timestamp).strftime('%Y-%m-%d %H:%M')}")
                
                st.markdown("**Description**:")
                st.markdown(case.description)
            
            with col2:
                st.markdown(f"**Plaintiff**: {case.plaintiff[:16]}...")
                if case.defendant:
                    st.markdown(f"**Defendant**: {case.defendant[:16]}...")
                
                st.markdown(f"**Evidence**: {len(case.evidence)} items")
                
                if st.button(f"Analyze Case", key=f"analyze_{case.case_id}"):
                    with st.spinner("AI analyzing case..."):
                        result = arbitration.resolve_case(case.case_id)
                        
                        st.success(f"**Decision**: {result['decision'].value.replace('_', ' ').title()}")
                        st.info(f"**Confidence**: {result['confidence']:.0%}")
                        st.markdown(f"**Reasoning**: {result['reasoning']}")


def render_penalty_appeals_tab(penalty_bridge):
    """Render penalty appeals tracking"""
    st.markdown("### ⚖️ Penalty Appeals")
    
    # Appeals statistics
    stats = penalty_bridge.get_appeal_statistics()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Appeals", stats["total_appeals"])
    
    with col2:
        st.metric("Success Rate", f"{stats['success_rate']:.0%}")
    
    with col3:
        st.metric("Penalties Modified", stats["penalties_modified"])
    
    # Decision breakdown
    if stats["decision_breakdown"]:
        st.markdown("#### Decision Distribution")
        
        fig = go.Figure(data=[go.Bar(
            x=list(stats["decision_breakdown"].keys()),
            y=list(stats["decision_breakdown"].values()),
            marker_color='rgb(102, 126, 234)'
        )])
        
        fig.update_layout(
            title="Appeal Decisions",
            xaxis_title="Decision Type",
            yaxis_title="Count",
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)


def render_governance_mediation_tab(gov_arbitration):
    """Render governance mediation tracking"""
    st.markdown("### 🏛️ Governance Mediation")
    
    # Statistics
    stats = gov_arbitration.get_statistics()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Mediations", stats["total_mediations"])
    
    with col2:
        st.metric("Avg Controversy", f"{stats['average_controversy']:.0%}")
    
    with col3:
        st.metric("Escalation Rate", f"{stats['escalation_rate']:.0%}")
    
    # Contentious proposals
    st.markdown("#### 🔥 Contentious Proposals")
    
    contentious = gov_arbitration.get_contentious_proposals()
    
    if contentious:
        for prop in contentious:
            with st.expander(f"**{prop['title']}** (Controversy: {prop['controversy_score']:.0%})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Proposal ID**: {prop['proposal_id']}")
                    st.markdown(f"**Vote Split**:")
                    st.markdown(f"- For: {prop['vote_split']['for']:.0%}")
                    st.markdown(f"- Against: {prop['vote_split']['against']:.0%}")
                    st.markdown(f"- Abstain: {prop['vote_split']['abstain']:.0%}")
                
                with col2:
                    if prop['requires_mediation']:
                        st.warning("⚠️ Mediation Recommended")
                    else:
                        st.info("ℹ️ Monitoring")
    else:
        st.success("✅ No contentious proposals currently")


def render_statistics_tab(arbitration, penalty_bridge, gov_arbitration):
    """Render comprehensive statistics"""
    st.markdown("### 📈 Arbitration System Analytics")
    
    arb_stats = arbitration.get_statistics()
    
    # Decision distribution pie chart
    st.markdown("#### Decision Distribution")
    
    decision_dist = arb_stats["decision_distribution"]
    if sum(decision_dist.values()) > 0:
        fig = go.Figure(data=[go.Pie(
            labels=[k.replace("_", " ").title() for k in decision_dist.keys()],
            values=list(decision_dist.values()),
            hole=0.4
        )])
        
        fig.update_layout(
            title="AI Arbitration Decisions",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No decisions issued yet")
    
    # Performance metrics
    st.markdown("#### Performance Metrics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Average Resolution Time",
            f"{arb_stats['average_resolution_time_seconds'] / 3600:.1f} hours"
        )
    
    with col2:
        st.metric(
            "Average AI Confidence",
            f"{arb_stats['average_confidence']:.0%}"
        )


if __name__ == "__main__":
    render_arbitration_dashboard()
