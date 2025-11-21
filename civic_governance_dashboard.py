"""
Civic Governance Dashboard - Innovation Campaign System
Validators burn NXT to promote ideas, community votes, AI analyzes results
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from civic_governance import (
    CivicGovernance, Campaign, CampaignStatus, VoteChoice,
    SpectralRegion, Validator
)
from nexus_ai import NexusAI
import numpy as np


def initialize_governance():
    """Initialize governance system with sample data if needed"""
    if 'governance' not in st.session_state:
        gov = CivicGovernance()
        
        # Register sample validators across spectral regions
        regions = [
            SpectralRegion.VIOLET, SpectralRegion.BLUE, SpectralRegion.GREEN,
            SpectralRegion.YELLOW, SpectralRegion.ORANGE, SpectralRegion.RED
        ]
        
        for i, region in enumerate(regions):
            validator_id = f"VAL-{region.name}-{i+1:03d}"
            gov.register_validator(validator_id, region, stake_amount=1500.0 + i*100)
        
        # Create sample campaigns for demo
        sample_campaigns = [
            Campaign(
                campaign_id="CAMP-001",
                title="🌊 WaveLang Standard Library",
                description="Develop comprehensive standard library for WaveLang with 100+ pre-built wavelength functions",
                innovation_details="""**Vision**: Expand WaveLang ecosystem with production-ready standard library.
                
**Features**:
- Math operations (trigonometry, logarithms, complex numbers)
- String manipulation via wavelength encoding
- File I/O with quantum error correction
- Network communication using E=hf protocols
- Data structures (arrays, hashmaps, trees) in wavelength space

**Impact**: Accelerates WaveLang adoption by 10x, eliminates need to write basic functions from scratch.

**Resource Requirements**: 15,000 NXT dev budget, 6-month timeline, 3 core developers.""",
                proposer_id="VAL-BLUE-002",
                nxt_burned=500.0
            ),
            Campaign(
                campaign_id="CAMP-002",
                title="🏥 BHLS Healthcare Expansion",
                description="Add dental and vision care to Basic Human Living Standard floor",
                innovation_details="""**Current State**: BHLS covers only emergency medical care.

**Proposal**: Expand to preventative healthcare:
- Annual dental checkups & cleanings
- Vision exams & prescription eyewear
- Mental health counseling (12 sessions/year)

**Economics**: +300 NXT/citizen/year (26% BHLS increase). Funded via:
- 40% from recycling pool surplus
- 40% from validator fee redirection  
- 20% from new healthcare recycling credits (medical equipment)

**Health Impact**: 70% reduction in preventable diseases, 15-year life expectancy increase.

**Implementation**: 18-month rollout, starting with pilot cities.""",
                proposer_id="VAL-GREEN-003",
                nxt_burned=750.0
            ),
            Campaign(
                campaign_id="CAMP-003",
                title="🛰️ Satellite Mesh Network Backbone",
                description="Launch 100 low-orbit satellites to provide global offline mesh coverage",
                innovation_details="""**Problem**: Offline mesh (Bluetooth/WiFi Direct) limited to ~200m range, fails in rural areas.

**Solution**: LEO satellite constellation providing:
- Global mesh network relay (even in deserts, oceans)
- 10 Mbps bandwidth per node
- Quantum-encrypted WNSP v2.0 protocol
- 99.9% uptime guarantee

**Architecture**:
- 100 satellites @ 550km altitude
- Inter-satellite laser links
- Ground stations in 50 countries
- Seamless handoff with terrestrial mesh

**Investment**: 2.5M NXT ($250M @ $100/NXT). ROI via:
- Messaging fees (0.5 NXT per 1000 messages)
- 5-year breakeven, then pure profit to validator pool

**Strategic Value**: Makes NexusOS truly censorship-proof, enables banking in 3B unbanked humans.""",
                proposer_id="VAL-VIOLET-001",
                nxt_burned=2000.0
            )
        ]
        
        for camp in sample_campaigns:
            gov.create_campaign(camp)
        
        # Add sample community votes
        # Campaign 1: 75% approval (successful)
        for i in range(1, 61):
            choice = VoteChoice.APPROVE if i <= 45 else VoteChoice.REJECT
            gov.submit_community_vote(f"CITIZEN-{i:04d}", "CAMP-001", choice)
        
        # Campaign 2: 55% approval (borderline)
        for i in range(1, 41):
            choice = VoteChoice.APPROVE if i <= 22 else VoteChoice.REJECT
            gov.submit_community_vote(f"CITIZEN-{i:04d}", "CAMP-002", choice)
        
        # Campaign 3: Still active, partial votes
        for i in range(1, 21):
            choice = VoteChoice.APPROVE if i <= 17 else VoteChoice.REJECT
            gov.submit_community_vote(f"CITIZEN-{i:04d}", "CAMP-003", choice)
        
        st.session_state.governance = gov
    
    return st.session_state.governance


def render_campaign_overview(gov: CivicGovernance):
    """Render campaign statistics overview"""
    st.header("🏛️ Civic Governance - Innovation Campaigns")
    st.markdown("**Validators burn NXT to promote ideas. Community votes. AI analyzes results.**")
    st.divider()
    
    # Get stats
    stats = gov.get_campaign_stats()
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Campaigns", stats['total_campaigns'])
    col2.metric("Active Campaigns", stats['active_campaigns'])
    col3.metric("Success Rate", f"{stats['success_rate']:.1f}%")
    col4.metric("Total NXT Burned", f"{stats['total_nxt_burned']:,.0f} NXT")
    
    col1, col2 = st.columns(2)
    col1.metric("Community Votes Cast", stats['total_community_votes'])
    col2.metric("Avg Burn/Campaign", f"{stats['average_burn_per_campaign']:,.0f} NXT")


def render_create_campaign_tab(gov: CivicGovernance):
    """Render campaign creation interface"""
    st.header("📝 Create Innovation Campaign")
    st.markdown("**Validators**: Burn NXT to promote your innovation idea to the community for votes")
    st.divider()
    
    # Get list of validators
    validator_ids = list(gov.validators.keys())
    
    if not validator_ids:
        st.warning("No validators registered. Register validators first.")
        return
    
    # Campaign creation form
    st.markdown("### Campaign Details")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        title = st.text_input("Campaign Title", 
                              placeholder="e.g., WaveLang Standard Library",
                              key="camp_title")
        
        description = st.text_area("Short Description (1-2 sentences)",
                                   placeholder="Brief overview of your innovation...",
                                   height=80,
                                   key="camp_desc")
        
        innovation_details = st.text_area(
            "Detailed Innovation Plan",
            placeholder="Explain your vision, implementation plan, resource requirements, expected impact...",
            height=200,
            key="camp_details"
        )
    
    with col2:
        proposer_id = st.selectbox("Your Validator ID", validator_ids, key="camp_proposer")
        
        proposer = gov.validators[proposer_id]
        st.info(f"**Region**: {proposer.spectral_region.value}\n**Stake**: {proposer.stake_amount:,.0f} NXT")
        
        nxt_burn = st.number_input(
            "NXT to Burn",
            min_value=gov.min_campaign_burn,
            max_value=10000.0,
            value=500.0,
            step=100.0,
            help="Higher burn = stronger commitment signal",
            key="camp_burn"
        )
        
        st.markdown(f"**Min required**: {gov.min_campaign_burn} NXT")
        
        voting_days = st.slider("Voting Period (days)", 7, 30, 14, key="camp_days")
    
    st.divider()
    
    # Submit button
    if st.button("🔥 Burn NXT & Launch Campaign", type="primary", key="create_camp_btn"):
        if not title or not description or not innovation_details:
            st.error("Please fill all fields")
            return
        
        try:
            # Create campaign
            campaign_id = f"CAMP-{len(gov.campaigns) + 1:03d}"
            campaign = Campaign(
                campaign_id=campaign_id,
                title=title,
                description=description,
                innovation_details=innovation_details,
                proposer_id=proposer_id,
                nxt_burned=nxt_burn,
                voting_deadline=datetime.now() + timedelta(days=voting_days)
            )
            
            gov.create_campaign(campaign)
            
            st.success(f"✅ Campaign {campaign_id} created successfully!")
            st.success(f"🔥 {nxt_burn} NXT burned to promote your innovation")
            st.info(f"Community voting open for {voting_days} days")
            st.balloons()
            
        except Exception as e:
            st.error(f"Error creating campaign: {str(e)}")


def render_active_campaigns_tab(gov: CivicGovernance):
    """Render active campaigns for community voting"""
    st.header("🗳️ Active Campaigns - Cast Your Vote")
    st.markdown("**Community**: Review innovation proposals and vote APPROVE or REJECT")
    st.divider()
    
    # Filter active campaigns
    active_campaigns = [c for c in gov.campaigns.values() if c.is_active()]
    
    if not active_campaigns:
        st.info("No active campaigns currently. Check back later or create one!")
        return
    
    # Voter ID input
    voter_id = st.text_input("Your Citizen ID", 
                              placeholder="e.g., CITIZEN-0001",
                              key="voter_id")
    
    st.divider()
    
    # Display each campaign
    for campaign in active_campaigns:
        status = gov.get_campaign_status(campaign.campaign_id)
        
        with st.expander(f"**{campaign.title}** ({status['approval_percentage']:.1f}% approval)", expanded=True):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Description**: {campaign.description}")
                st.markdown("**Innovation Details**:")
                st.markdown(campaign.innovation_details)
            
            with col2:
                st.metric("NXT Burned", f"{campaign.nxt_burned:,.0f}")
                st.metric("Total Votes", status['total_voters'])
                st.metric("Approval", f"{status['approval_percentage']:.1f}%")
                
                # Voting progress bar
                st.progress(status['approval_percentage'] / 100)
                
                # Deadline
                deadline = datetime.fromisoformat(status['voting_deadline'])
                time_left = deadline - datetime.now()
                st.caption(f"⏰ {time_left.days} days left")
            
            # Vote buttons
            st.divider()
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                if st.button(f"✅ APPROVE", key=f"approve_{campaign.campaign_id}"):
                    if not voter_id:
                        st.error("Enter your Citizen ID first")
                    else:
                        try:
                            gov.submit_community_vote(voter_id, campaign.campaign_id, VoteChoice.APPROVE)
                            st.success("Vote recorded: APPROVE ✅")
                            st.rerun()
                        except Exception as e:
                            st.error(str(e))
            
            with col2:
                if st.button(f"❌ REJECT", key=f"reject_{campaign.campaign_id}"):
                    if not voter_id:
                        st.error("Enter your Citizen ID first")
                    else:
                        try:
                            gov.submit_community_vote(voter_id, campaign.campaign_id, VoteChoice.REJECT)
                            st.success("Vote recorded: REJECT ❌")
                            st.rerun()
                        except Exception as e:
                            st.error(str(e))


def render_completed_campaigns_tab(gov: CivicGovernance):
    """Render completed campaigns with AI analysis"""
    st.header("📊 Completed Campaigns - AI Analysis")
    st.markdown("**Validators**: View community vote results and comprehensive AI analysis reports")
    st.divider()
    
    # Filter completed campaigns
    completed_campaigns = [c for c in gov.campaigns.values() if not c.is_active()]
    
    if not completed_campaigns:
        st.info("No completed campaigns yet. Active campaigns will appear here after voting closes.")
        return
    
    # Display each completed campaign
    for campaign in completed_campaigns:
        status = gov.get_campaign_status(campaign.campaign_id)
        
        # Determine result color
        if campaign.status == CampaignStatus.IMPLEMENTED:
            status_color = "🟢"
            status_text = "APPROVED"
        else:
            status_color = "🔴"
            status_text = "REJECTED"
        
        with st.expander(f"{status_color} **{campaign.title}** - {status_text} ({status['approval_percentage']:.1f}% approval)"):
            # Campaign summary
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Votes", status['total_voters'])
            col2.metric("Approval", f"{status['votes_approve']} ({status['approval_percentage']:.1f}%)")
            col3.metric("Rejection", f"{status['votes_reject']} ({status['rejection_percentage']:.1f}%)")
            col4.metric("NXT Burned", f"{campaign.nxt_burned:,.0f}")
            
            # Vote distribution chart
            fig = go.Figure(data=[go.Pie(
                labels=['Approve', 'Reject'],
                values=[status['votes_approve'], status['votes_reject']],
                marker_colors=['#00ff88', '#ff4444'],
                hole=0.4
            )])
            fig.update_layout(
                title="Vote Distribution",
                height=300,
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # AI Analysis Report Button
            st.divider()
            if not campaign.ai_report_generated:
                if st.button(f"🤖 Generate Comprehensive AI Analysis", key=f"ai_report_{campaign.campaign_id}"):
                    # Prepare data for AI report
                    campaign_data = {
                        'campaign': campaign,
                        'status': status,
                        'governance': gov,
                        'community_votes': gov.community_votes[campaign.campaign_id]
                    }
                    
                    # Generate AI report
                    with st.expander("📊 Nexus AI Campaign Analysis Report", expanded=True):
                        NexusAI.generate_campaign_analysis_report(campaign_data)
                        campaign.ai_report_generated = True
                    
                    st.rerun()
            else:
                # Show already generated report
                st.success("✅ AI Analysis Report Generated")
                
                # Prepare data for AI report
                campaign_data = {
                    'campaign': campaign,
                    'status': status,
                    'governance': gov,
                    'community_votes': gov.community_votes[campaign.campaign_id]
                }
                
                # Display report again
                with st.expander("📊 Nexus AI Campaign Analysis Report", expanded=True):
                    NexusAI.generate_campaign_analysis_report(campaign_data)


def render_governance_analytics_tab(gov: CivicGovernance):
    """Render overall governance analytics"""
    st.header("📈 Governance Analytics")
    st.divider()
    
    stats = gov.get_campaign_stats()
    
    # Overall metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Success Rate", f"{stats['success_rate']:.1f}%")
    col2.metric("Avg Burn/Campaign", f"{stats['average_burn_per_campaign']:,.0f} NXT")
    col3.metric("Avg Votes/Campaign", f"{stats['total_community_votes'] / max(1, stats['total_campaigns']):.0f}")
    
    # Campaign outcomes pie chart
    if stats['total_campaigns'] > 0:
        approved = stats['successful_campaigns']
        rejected = stats['total_campaigns'] - approved - stats['active_campaigns']
        active = stats['active_campaigns']
        
        fig = go.Figure(data=[go.Pie(
            labels=['Approved', 'Rejected', 'Active'],
            values=[approved, rejected, active],
            marker_colors=['#00ff88', '#ff4444', '#ffaa00']
        )])
        fig.update_layout(
            title="Campaign Outcomes",
            height=400,
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # NXT burn over time
    st.divider()
    st.markdown("### Campaign Economics")
    
    campaigns_list = sorted(gov.campaigns.values(), key=lambda c: c.creation_date)
    
    if campaigns_list:
        campaign_ids = [c.campaign_id for c in campaigns_list]
        burns = [c.nxt_burned for c in campaigns_list]
        
        fig = go.Figure(data=[
            go.Bar(x=campaign_ids, y=burns, marker_color='#ff6b35')
        ])
        fig.update_layout(
            title="NXT Burned Per Campaign",
            xaxis_title="Campaign ID",
            yaxis_title="NXT Burned",
            height=300,
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.metric("Total NXT Burned (All Campaigns)", f"{stats['total_nxt_burned']:,.0f} NXT")
        st.caption("💡 Higher burn amounts signal stronger validator commitment to innovation")


def main():
    """Main civic governance dashboard"""
    gov = initialize_governance()
    
    # Render overview
    render_campaign_overview(gov)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Create Campaign",
        "🗳️ Active Campaigns",
        "📊 Completed Campaigns",
        "📈 Analytics"
    ])
    
    with tab1:
        render_create_campaign_tab(gov)
    
    with tab2:
        render_active_campaigns_tab(gov)
    
    with tab3:
        render_completed_campaigns_tab(gov)
    
    with tab4:
        render_governance_analytics_tab(gov)


if __name__ == "__main__":
    main()
