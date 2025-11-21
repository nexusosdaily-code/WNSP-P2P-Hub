"""
Civic Governance Layer - NexusOS Civilization OS
Spectral-region governance with voting, decision-making, civic participation

Uses Proof of Spectrum where validators represent different spectral regions
and consensus requires 5 of 6 regions to approve decisions.
"""

import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from datetime import datetime, timedelta
from enum import Enum

class SpectralRegion(Enum):
    """Spectral regions for distributed governance"""
    UV = "Ultraviolet"
    VIOLET = "Violet"
    BLUE = "Blue"
    GREEN = "Green"
    YELLOW = "Yellow"
    ORANGE = "Orange"
    RED = "Red"
    IR = "Infrared"

class ProposalType(Enum):
    """Types of governance proposals"""
    POLICY = "Policy Change"
    BUDGET = "Budget Allocation"
    INFRASTRUCTURE = "Infrastructure Project"
    BHLS_ADJUSTMENT = "BHLS Floor Adjustment"
    EMERGENCY = "Emergency Action"
    CONSTITUTIONAL = "Constitutional Amendment"

class VoteChoice(Enum):
    """Vote options"""
    APPROVE = "Approve"
    REJECT = "Reject"
    ABSTAIN = "Abstain"

class CampaignStatus(Enum):
    """Campaign lifecycle status"""
    ACTIVE = "Active - Accepting Votes"
    CLOSED = "Closed - Voting Complete"
    IMPLEMENTED = "Implemented"
    REJECTED = "Rejected by Community"

@dataclass
class Proposal:
    """Governance proposal"""
    proposal_id: str
    title: str
    description: str
    proposal_type: ProposalType
    proposer_id: str
    creation_date: datetime = field(default_factory=datetime.now)
    voting_deadline: Optional[datetime] = None
    required_approvals: int = 5  # Out of 6 spectral regions for normal proposals
    status: str = "OPEN"  # OPEN, APPROVED, REJECTED
    
    def __post_init__(self):
        if not self.voting_deadline:
            # Default: 7 days voting period
            self.voting_deadline = self.creation_date + timedelta(days=7)
    
    def is_active(self) -> bool:
        """Check if proposal is still accepting votes"""
        return self.status == "OPEN" and datetime.now() < self.voting_deadline


@dataclass
class Validator:
    """Validator representing a spectral region"""
    validator_id: str
    spectral_region: SpectralRegion
    stake_amount: float  # NXT staked
    reputation_score: float = 1.0  # 0-1, based on voting history
    votes_cast: int = 0
    is_active: bool = True


@dataclass
class Vote:
    """Individual vote on a proposal"""
    validator_id: str
    spectral_region: SpectralRegion
    proposal_id: str
    choice: VoteChoice
    timestamp: datetime = field(default_factory=datetime.now)
    weight: float = 1.0  # Can be modified by reputation


@dataclass
class Campaign:
    """Innovation campaign promoted by validators burning NXT"""
    campaign_id: str
    title: str
    description: str
    innovation_details: str  # Detailed explanation of the innovation
    proposer_id: str  # Validator who created campaign
    nxt_burned: float  # NXT burned to promote campaign
    creation_date: datetime = field(default_factory=datetime.now)
    voting_deadline: Optional[datetime] = None
    status: CampaignStatus = CampaignStatus.ACTIVE
    
    # Community voting results
    votes_approve: int = 0
    votes_reject: int = 0
    total_voters: int = 0
    
    # AI analysis results (populated after voting closes)
    ai_report_generated: bool = False
    
    def __post_init__(self):
        if not self.voting_deadline:
            # Default: 14 days voting period for campaigns
            self.voting_deadline = self.creation_date + timedelta(days=14)
    
    def is_active(self) -> bool:
        """Check if campaign is still accepting votes"""
        return self.status == CampaignStatus.ACTIVE and datetime.now() < self.voting_deadline
    
    def approval_percentage(self) -> float:
        """Calculate approval percentage"""
        if self.total_voters == 0:
            return 0.0
        return (self.votes_approve / self.total_voters) * 100
    
    def rejection_percentage(self) -> float:
        """Calculate rejection percentage"""
        if self.total_voters == 0:
            return 0.0
        return (self.votes_reject / self.total_voters) * 100


@dataclass
class CommunityVote:
    """Individual community member vote on a campaign"""
    voter_id: str  # Citizen/community member ID
    campaign_id: str
    choice: VoteChoice  # APPROVE or REJECT
    timestamp: datetime = field(default_factory=datetime.now)


class CivicGovernance:
    """
    Manages decentralized governance using Proof of Spectrum
    Requires spectral diversity for all decisions
    """
    
    def __init__(self):
        # Validators by spectral region
        self.validators: Dict[str, Validator] = {}
        self.validators_by_region: Dict[SpectralRegion, List[Validator]] = {
            region: [] for region in SpectralRegion
        }
        
        # Proposals and votes
        self.proposals: Dict[str, Proposal] = {}
        self.votes: Dict[str, List[Vote]] = {}  # proposal_id -> votes
        
        # Innovation campaigns (validators burn NXT to promote ideas)
        self.campaigns: Dict[str, Campaign] = {}
        self.community_votes: Dict[str, List[CommunityVote]] = {}  # campaign_id -> votes
        self.total_nxt_burned = 0.0  # Total NXT burned for campaigns
        
        # Governance parameters
        self.min_stake_required = 1000.0  # Minimum NXT to be validator
        self.spectral_diversity_requirement = 5  # Regions needed for approval
        self.min_campaign_burn = 100.0  # Minimum NXT to create campaign
        
        # Statistics
        self.total_proposals = 0
        self.approved_proposals = 0
        self.rejected_proposals = 0
        self.total_campaigns = 0
        self.successful_campaigns = 0
    
    def register_validator(self, validator_id: str, spectral_region: SpectralRegion, 
                          stake_amount: float) -> Validator:
        """Register a new validator for a spectral region"""
        if stake_amount < self.min_stake_required:
            raise ValueError(f"Stake {stake_amount} below minimum {self.min_stake_required} NXT")
        
        if validator_id in self.validators:
            raise ValueError(f"Validator {validator_id} already registered")
        
        validator = Validator(
            validator_id=validator_id,
            spectral_region=spectral_region,
            stake_amount=stake_amount
        )
        
        self.validators[validator_id] = validator
        self.validators_by_region[spectral_region].append(validator)
        
        return validator
    
    def submit_proposal(self, proposal: Proposal) -> str:
        """Submit a new governance proposal"""
        # Constitutional amendments require 6/6 regions (unanimous)
        if proposal.proposal_type == ProposalType.CONSTITUTIONAL:
            proposal.required_approvals = 6
        
        self.proposals[proposal.proposal_id] = proposal
        self.votes[proposal.proposal_id] = []
        self.total_proposals += 1
        
        return proposal.proposal_id
    
    def cast_vote(self, validator_id: str, proposal_id: str, choice: VoteChoice):
        """Validator casts a vote on a proposal"""
        if validator_id not in self.validators:
            raise ValueError(f"Validator {validator_id} not registered")
        
        if proposal_id not in self.proposals:
            raise ValueError(f"Proposal {proposal_id} not found")
        
        proposal = self.proposals[proposal_id]
        validator = self.validators[validator_id]
        
        if not proposal.is_active():
            raise ValueError(f"Proposal {proposal_id} is not accepting votes")
        
        # Check if validator already voted
        existing_votes = [v for v in self.votes[proposal_id] if v.validator_id == validator_id]
        if existing_votes:
            raise ValueError(f"Validator {validator_id} already voted on {proposal_id}")
        
        # Create vote with reputation weighting
        vote = Vote(
            validator_id=validator_id,
            spectral_region=validator.spectral_region,
            proposal_id=proposal_id,
            choice=choice,
            weight=validator.reputation_score
        )
        
        self.votes[proposal_id].append(vote)
        validator.votes_cast += 1
        
        # Check if voting is complete
        self._evaluate_proposal(proposal_id)
    
    def _evaluate_proposal(self, proposal_id: str):
        """Evaluate if proposal has reached decision threshold"""
        proposal = self.proposals[proposal_id]
        votes = self.votes[proposal_id]
        
        # Count approvals by spectral region
        region_approvals: Dict[SpectralRegion, int] = {region: 0 for region in SpectralRegion}
        region_rejections: Dict[SpectralRegion, int] = {region: 0 for region in SpectralRegion}
        
        for vote in votes:
            if vote.choice == VoteChoice.APPROVE:
                region_approvals[vote.spectral_region] += 1
            elif vote.choice == VoteChoice.REJECT:
                region_rejections[vote.spectral_region] += 1
        
        # Count regions with majority approval
        regions_approved = sum(1 for count in region_approvals.values() if count > 0)
        regions_rejected = sum(1 for count in region_rejections.values() if count > 0)
        
        # Check if proposal passes (only if still open)
        if proposal.status == "OPEN":
            if regions_approved >= proposal.required_approvals:
                proposal.status = "APPROVED"
                self.approved_proposals += 1
            # Check if proposal cannot pass (too many rejections)
            elif regions_rejected > (8 - proposal.required_approvals):
                proposal.status = "REJECTED"
                self.rejected_proposals += 1
    
    def get_proposal_status(self, proposal_id: str) -> dict:
        """Get detailed status of a proposal"""
        if proposal_id not in self.proposals:
            raise ValueError(f"Proposal {proposal_id} not found")
        
        proposal = self.proposals[proposal_id]
        votes = self.votes[proposal_id]
        
        # Count votes by region
        votes_by_region: Dict[SpectralRegion, Dict[str, int]] = {
            region: {"APPROVE": 0, "REJECT": 0, "ABSTAIN": 0} 
            for region in SpectralRegion
        }
        
        for vote in votes:
            votes_by_region[vote.spectral_region][vote.choice.name] += 1
        
        # Regions that approved
        approving_regions = [
            region for region, counts in votes_by_region.items() 
            if counts["APPROVE"] > 0
        ]
        
        return {
            "proposal_id": proposal.proposal_id,
            "title": proposal.title,
            "type": proposal.proposal_type.value,
            "status": proposal.status,
            "required_approvals": proposal.required_approvals,
            "regions_approved": len(approving_regions),
            "approving_regions": [r.value for r in approving_regions],
            "total_votes": len(votes),
            "votes_by_region": {
                region.value: counts for region, counts in votes_by_region.items()
            },
            "is_active": proposal.is_active(),
            "deadline": proposal.voting_deadline.isoformat()
        }
    
    def get_governance_stats(self) -> dict:
        """Get overall governance statistics"""
        active_proposals = sum(1 for p in self.proposals.values() if p.is_active())
        
        validators_by_region = {
            region.value: len(validators) 
            for region, validators in self.validators_by_region.items()
        }
        
        total_stake = sum(v.stake_amount for v in self.validators.values())
        avg_reputation = np.mean([v.reputation_score for v in self.validators.values()]) if self.validators else 0
        
        return {
            "total_validators": len(self.validators),
            "validators_by_region": validators_by_region,
            "total_stake": total_stake,
            "avg_validator_reputation": avg_reputation,
            "total_proposals": self.total_proposals,
            "active_proposals": active_proposals,
            "approved_proposals": self.approved_proposals,
            "rejected_proposals": self.rejected_proposals,
            "approval_rate": (self.approved_proposals / max(1, self.total_proposals)) * 100
        }
    
    # ===== INNOVATION CAMPAIGN METHODS =====
    
    def create_campaign(self, campaign: Campaign) -> str:
        """
        Create a new innovation campaign (validator burns NXT to promote idea)
        
        Args:
            campaign: Campaign object with all details
            
        Returns:
            campaign_id
        """
        # Verify minimum burn amount
        if campaign.nxt_burned < self.min_campaign_burn:
            raise ValueError(f"Campaign burn {campaign.nxt_burned} below minimum {self.min_campaign_burn} NXT")
        
        # Verify proposer is a registered validator
        if campaign.proposer_id not in self.validators:
            raise ValueError(f"Proposer {campaign.proposer_id} is not a registered validator")
        
        # Store campaign
        self.campaigns[campaign.campaign_id] = campaign
        self.community_votes[campaign.campaign_id] = []
        self.total_nxt_burned += campaign.nxt_burned
        self.total_campaigns += 1
        
        return campaign.campaign_id
    
    def submit_community_vote(self, voter_id: str, campaign_id: str, choice: VoteChoice):
        """
        Community member submits vote on a campaign
        
        Args:
            voter_id: Citizen/community member ID
            campaign_id: Campaign to vote on
            choice: APPROVE or REJECT
        """
        if campaign_id not in self.campaigns:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        campaign = self.campaigns[campaign_id]
        
        if not campaign.is_active():
            raise ValueError(f"Campaign {campaign_id} is not accepting votes")
        
        # Check if voter already voted
        existing_votes = [v for v in self.community_votes[campaign_id] if v.voter_id == voter_id]
        if existing_votes:
            raise ValueError(f"Voter {voter_id} already voted on {campaign_id}")
        
        # Only APPROVE/REJECT allowed for campaigns (no ABSTAIN)
        if choice == VoteChoice.ABSTAIN:
            raise ValueError("ABSTAIN not allowed for campaigns - choose APPROVE or REJECT")
        
        # Record vote
        vote = CommunityVote(
            voter_id=voter_id,
            campaign_id=campaign_id,
            choice=choice
        )
        
        self.community_votes[campaign_id].append(vote)
        
        # Update campaign tallies
        campaign.total_voters += 1
        if choice == VoteChoice.APPROVE:
            campaign.votes_approve += 1
        elif choice == VoteChoice.REJECT:
            campaign.votes_reject += 1
    
    def close_campaign(self, campaign_id: str) -> dict:
        """
        Close campaign voting and determine final result
        
        Args:
            campaign_id: Campaign to close
            
        Returns:
            Final campaign results dictionary
        """
        if campaign_id not in self.campaigns:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        campaign = self.campaigns[campaign_id]
        
        if campaign.status != CampaignStatus.ACTIVE:
            raise ValueError(f"Campaign {campaign_id} already closed")
        
        # Calculate approval percentage
        approval_pct = campaign.approval_percentage()
        
        # Determine outcome (60% approval threshold)
        if approval_pct >= 60.0:
            campaign.status = CampaignStatus.IMPLEMENTED
            self.successful_campaigns += 1
            result = "APPROVED - Implementation Recommended"
        else:
            campaign.status = CampaignStatus.REJECTED
            result = "REJECTED - Insufficient Community Support"
        
        return {
            "campaign_id": campaign_id,
            "title": campaign.title,
            "result": result,
            "approval_percentage": approval_pct,
            "total_votes": campaign.total_voters,
            "votes_approve": campaign.votes_approve,
            "votes_reject": campaign.votes_reject,
            "nxt_burned": campaign.nxt_burned,
            "status": campaign.status.value
        }
    
    def get_campaign_status(self, campaign_id: str) -> dict:
        """Get detailed status of a campaign"""
        if campaign_id not in self.campaigns:
            raise ValueError(f"Campaign {campaign_id} not found")
        
        campaign = self.campaigns[campaign_id]
        votes = self.community_votes[campaign_id]
        
        # Get proposer details
        proposer = self.validators.get(campaign.proposer_id)
        proposer_region = proposer.spectral_region.value if proposer else "Unknown"
        
        return {
            "campaign_id": campaign.campaign_id,
            "title": campaign.title,
            "description": campaign.description,
            "innovation_details": campaign.innovation_details,
            "proposer_id": campaign.proposer_id,
            "proposer_region": proposer_region,
            "nxt_burned": campaign.nxt_burned,
            "status": campaign.status.value,
            "is_active": campaign.is_active(),
            "creation_date": campaign.creation_date.isoformat(),
            "voting_deadline": campaign.voting_deadline.isoformat(),
            "total_voters": campaign.total_voters,
            "votes_approve": campaign.votes_approve,
            "votes_reject": campaign.votes_reject,
            "approval_percentage": campaign.approval_percentage(),
            "rejection_percentage": campaign.rejection_percentage(),
            "ai_report_generated": campaign.ai_report_generated,
            "total_votes_cast": len(votes)
        }
    
    def get_campaign_stats(self) -> dict:
        """Get overall campaign statistics"""
        active_campaigns = sum(1 for c in self.campaigns.values() if c.is_active())
        
        # Calculate average burn amount
        avg_burn = (self.total_nxt_burned / max(1, self.total_campaigns))
        
        # Total community participation
        total_community_votes = sum(len(votes) for votes in self.community_votes.values())
        
        return {
            "total_campaigns": self.total_campaigns,
            "active_campaigns": active_campaigns,
            "successful_campaigns": self.successful_campaigns,
            "total_nxt_burned": self.total_nxt_burned,
            "average_burn_per_campaign": avg_burn,
            "total_community_votes": total_community_votes,
            "success_rate": (self.successful_campaigns / max(1, self.total_campaigns)) * 100
        }


# Example usage
if __name__ == "__main__":
    from datetime import timedelta
    
    print("=" * 70)
    print("CIVIC GOVERNANCE - Proof of Spectrum")
    print("=" * 70)
    
    # Initialize governance
    gov = CivicGovernance()
    
    # Register validators across spectral regions
    print("\n1. REGISTERING VALIDATORS:")
    regions = [SpectralRegion.VIOLET, SpectralRegion.BLUE, SpectralRegion.GREEN,
               SpectralRegion.YELLOW, SpectralRegion.ORANGE, SpectralRegion.RED]
    
    for i, region in enumerate(regions):
        validator_id = f"VAL-{region.name}-{i:03d}"
        gov.register_validator(validator_id, region, stake_amount=1500.0)
        print(f"   Registered: {validator_id} ({region.value})")
    
    stats = gov.get_governance_stats()
    print(f"\n   Total validators: {stats['total_validators']}")
    print(f"   Total stake: {stats['total_stake']:,.0f} NXT")
    
    # Submit a proposal
    print("\n2. SUBMITTING PROPOSAL:")
    proposal = Proposal(
        proposal_id="PROP-001",
        title="Increase BHLS Food Allocation by 10%",
        description="Adjust monthly food allocation from 250 to 275 NXT per citizen",
        proposal_type=ProposalType.BHLS_ADJUSTMENT,
        proposer_id="CIT-001"
    )
    gov.submit_proposal(proposal)
    print(f"   Proposal submitted: {proposal.title}")
    print(f"   Required approvals: {proposal.required_approvals} spectral regions")
    
    # Cast votes
    print("\n3. VOTING PROCESS:")
    # 5 regions approve, 1 rejects
    for i, region in enumerate(regions[:5]):
        validator_id = f"VAL-{region.name}-{i:03d}"
        gov.cast_vote(validator_id, "PROP-001", VoteChoice.APPROVE)
        print(f"   {region.value:15s} → APPROVE")
    
    validator_id = f"VAL-{regions[5].name}-005"
    gov.cast_vote(validator_id, "PROP-001", VoteChoice.REJECT)
    print(f"   {regions[5].value:15s} → REJECT")
    
    # Check proposal status
    print("\n4. PROPOSAL RESULT:")
    status = gov.get_proposal_status("PROP-001")
    print(f"   Status: {status['status']}")
    print(f"   Regions approved: {status['regions_approved']}/{status['required_approvals']}")
    print(f"   Approving regions: {', '.join(status['approving_regions'])}")
    
    # Governance stats
    print("\n5. GOVERNANCE STATISTICS:")
    stats = gov.get_governance_stats()
    print(f"   Total proposals: {stats['total_proposals']}")
    print(f"   Approved: {stats['approved_proposals']}")
    print(f"   Approval rate: {stats['approval_rate']:.1f}%")
    
    print("\n" + "=" * 70)
    print("Civic governance operational - Spectral diversity ensures decentralization!")
    print("=" * 70)
