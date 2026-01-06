"""
Tests for Safety Governance System.

Tests 5-tier governance, risk assessment, and approval workflows.
"""

import pytest
from unittest.mock import MagicMock, AsyncMock
import asyncio

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rsi.safety import (
    GovernanceTier,
    RiskCategory,
    ModificationScope,
    RiskAssessment,
    ModificationProposal,
    ApprovalRequest,
    ApprovalResult,
    ApprovalStatus,
    ApprovalWorkflow,
    GovernanceDecision,
    SafetyGovernance,
    is_protected_file,
    get_tier_for_risk,
    get_tier_requirements,
)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def mock_memory():
    """Create mock memory for Neo4j operations."""
    memory = MagicMock()
    memory.query_neo4j = AsyncMock(return_value=[])
    return memory


@pytest.fixture
def governance(mock_memory):
    """Create governance instance with mock memory."""
    return SafetyGovernance(memory=mock_memory, config={})


@pytest.fixture
def workflow(mock_memory):
    """Create approval workflow with mock memory."""
    return ApprovalWorkflow(memory=mock_memory, config={})


@pytest.fixture
def low_risk_proposal():
    """Create a low-risk modification proposal."""
    return ModificationProposal(
        id="prop_001",
        description="Update configuration value",
        modification_type="config_update",
        target_files=["config.yaml"],
        changes={"key": "new_value"},
        rationale="Improve performance",
        metadata={"has_tests": True, "has_rollback": True}
    )


@pytest.fixture
def medium_risk_proposal():
    """Create a medium-risk modification proposal."""
    return ModificationProposal(
        id="prop_002",
        description="Add new feature module",
        modification_type="capability_add",
        target_files=["src/module.py", "src/utils.py"],
        changes={"add_function": "new_capability()"},
        rationale="Extend system capabilities"
    )


@pytest.fixture
def high_risk_proposal():
    """Create a high-risk modification proposal."""
    return ModificationProposal(
        id="prop_003",
        description="Modify core architecture",
        modification_type="architecture_change",
        target_files=[
            "src/core.py", "src/engine.py", "src/api.py",
            "src/db.py", "src/cache.py", "src/queue.py"
        ],  # 6 files triggers SYSTEM scope
        changes={"refactor": "major_change"},
        rationale="Performance optimization"
    )


@pytest.fixture
def constitutional_proposal():
    """Create a proposal that targets protected files."""
    return ModificationProposal(
        id="prop_004",
        description="Modify protected file",
        modification_type="code_change",
        target_files=["provenance.py"],
        changes={"modify": "protected"},
        rationale="Dangerous modification"
    )


# ============================================================================
# Tier Tests
# ============================================================================

class TestGovernanceTiers:
    """Tests for governance tier definitions."""

    def test_tier_ordering(self):
        """Test that tiers are ordered correctly."""
        assert GovernanceTier.AUTOMATIC < GovernanceTier.VERIFIED
        assert GovernanceTier.VERIFIED < GovernanceTier.REVIEWED
        assert GovernanceTier.REVIEWED < GovernanceTier.HUMAN_OVERSIGHT
        assert GovernanceTier.HUMAN_OVERSIGHT < GovernanceTier.CONSTITUTIONAL

    def test_tier_values(self):
        """Test tier numeric values."""
        assert GovernanceTier.AUTOMATIC.value == 1
        assert GovernanceTier.CONSTITUTIONAL.value == 5

    def test_is_protected_file(self):
        """Test protected file detection."""
        assert is_protected_file("provenance.py") == True
        assert is_protected_file("modification_log.py") == True
        assert is_protected_file("path/to/provenance.py") == True
        assert is_protected_file("some_other_file.py") == False

    def test_get_tier_for_risk_low(self):
        """Test tier selection for low risk."""
        tier = get_tier_for_risk(0.1, RiskCategory.CONFIGURATION)
        assert tier == GovernanceTier.AUTOMATIC

    def test_get_tier_for_risk_medium(self):
        """Test tier selection for medium risk."""
        tier = get_tier_for_risk(0.35, RiskCategory.DATA)
        assert tier == GovernanceTier.VERIFIED

    def test_get_tier_for_risk_high(self):
        """Test tier selection for high risk."""
        tier = get_tier_for_risk(0.55, RiskCategory.CAPABILITY)
        assert tier == GovernanceTier.REVIEWED

    def test_get_tier_for_risk_constitutional(self):
        """Test tier selection for constitutional category."""
        tier = get_tier_for_risk(0.1, RiskCategory.CONSTITUTIONAL)
        assert tier == GovernanceTier.CONSTITUTIONAL

    def test_get_tier_requirements(self):
        """Test getting tier requirements."""
        reqs = get_tier_requirements(GovernanceTier.VERIFIED)
        assert reqs.requires_tests == True
        assert reqs.requires_rollback == True
        assert reqs.auto_approve == True


# ============================================================================
# Risk Assessment Tests
# ============================================================================

class TestRiskAssessment:
    """Tests for risk assessment."""

    @pytest.mark.asyncio
    async def test_assess_low_risk(self, governance, low_risk_proposal):
        """Test assessment of low-risk proposal."""
        decision = await governance.evaluate(low_risk_proposal)

        assert decision.risk_assessment.score < 0.3
        assert decision.tier in [GovernanceTier.AUTOMATIC, GovernanceTier.VERIFIED]
        assert decision.can_proceed == True

    @pytest.mark.asyncio
    async def test_assess_medium_risk(self, governance, medium_risk_proposal):
        """Test assessment of medium-risk proposal."""
        decision = await governance.evaluate(medium_risk_proposal)

        assert decision.risk_assessment.category == RiskCategory.CAPABILITY
        assert decision.can_proceed == True

    @pytest.mark.asyncio
    async def test_assess_high_risk(self, governance, high_risk_proposal):
        """Test assessment of high-risk proposal."""
        decision = await governance.evaluate(high_risk_proposal)

        assert decision.risk_assessment.scope == ModificationScope.SYSTEM
        assert len(decision.risk_assessment.factors) > 0

    @pytest.mark.asyncio
    async def test_assess_constitutional_violation(self, governance, constitutional_proposal):
        """Test assessment blocks constitutional violations."""
        decision = await governance.evaluate(constitutional_proposal)

        assert decision.tier == GovernanceTier.CONSTITUTIONAL
        assert decision.can_proceed == False
        assert len(decision.blocking_issues) > 0

    @pytest.mark.asyncio
    async def test_dangerous_pattern_detection(self, governance):
        """Test detection of dangerous patterns."""
        proposal = ModificationProposal(
            id="prop_danger",
            description="Execute shell command",
            modification_type="code_change",
            target_files=["script.py"],
            changes={"code": "os.system('rm -rf /')"},
            rationale="Dangerous"
        )

        decision = await governance.evaluate(proposal)

        assert decision.tier == GovernanceTier.CONSTITUTIONAL
        assert decision.can_proceed == False


# ============================================================================
# Approval Workflow Tests
# ============================================================================

class TestApprovalWorkflow:
    """Tests for approval workflow."""

    @pytest.mark.asyncio
    async def test_create_request(self, workflow, low_risk_proposal):
        """Test creating an approval request."""
        request = await workflow.create_request(
            low_risk_proposal,
            GovernanceTier.AUTOMATIC
        )

        assert request.id.startswith("apr_")
        assert request.status == ApprovalStatus.PENDING
        assert request.tier == GovernanceTier.AUTOMATIC

    @pytest.mark.asyncio
    async def test_automatic_approval(self, workflow, low_risk_proposal):
        """Test automatic tier auto-approves."""
        request = await workflow.create_request(
            low_risk_proposal,
            GovernanceTier.AUTOMATIC
        )

        result = await workflow.process_request(request.id)

        assert result.approved == True
        assert "auto-approved" in result.reason.lower()

    @pytest.mark.asyncio
    async def test_verified_with_tests(self, workflow, medium_risk_proposal):
        """Test verified tier with passing tests."""
        async def mock_test_runner(proposal):
            return {'passed': True, 'tests_run': 10}

        workflow.test_runner = mock_test_runner

        request = await workflow.create_request(
            medium_risk_proposal,
            GovernanceTier.VERIFIED
        )

        result = await workflow.process_request(request.id)

        assert result.approved == True
        assert "tests passed" in result.reason.lower()

    @pytest.mark.asyncio
    async def test_verified_with_failing_tests(self, workflow, medium_risk_proposal):
        """Test verified tier with failing tests."""
        async def mock_test_runner(proposal):
            return {'passed': False, 'tests_run': 10, 'failures': 2}

        workflow.test_runner = mock_test_runner

        request = await workflow.create_request(
            medium_risk_proposal,
            GovernanceTier.VERIFIED
        )

        result = await workflow.process_request(request.id)

        assert result.approved == False
        assert "failed" in result.reason.lower()

    @pytest.mark.asyncio
    async def test_constitutional_rejection(self, workflow, constitutional_proposal):
        """Test constitutional tier is always rejected."""
        request = await workflow.create_request(
            constitutional_proposal,
            GovernanceTier.CONSTITUTIONAL
        )

        result = await workflow.process_request(request.id)

        assert result.approved == False
        assert "constitutional" in result.reason.lower()

    @pytest.mark.asyncio
    async def test_human_oversight_pending(self, workflow, high_risk_proposal):
        """Test human oversight tier returns pending."""
        request = await workflow.create_request(
            high_risk_proposal,
            GovernanceTier.HUMAN_OVERSIGHT
        )

        result = await workflow.process_request(request.id)

        assert result.approved == False
        assert "awaiting human" in result.reason.lower()

    @pytest.mark.asyncio
    async def test_human_decision_approve(self, workflow, high_risk_proposal):
        """Test human can approve a request."""
        request = await workflow.create_request(
            high_risk_proposal,
            GovernanceTier.HUMAN_OVERSIGHT
        )

        # Process first (sets to awaiting human)
        await workflow.process_request(request.id)

        # Human decides
        result = await workflow.human_decide(
            request.id,
            approved=True,
            decided_by="human_reviewer",
            reason="Reviewed and approved"
        )

        assert result.approved == True

    @pytest.mark.asyncio
    async def test_human_decision_reject(self, workflow, high_risk_proposal):
        """Test human can reject a request."""
        request = await workflow.create_request(
            high_risk_proposal,
            GovernanceTier.HUMAN_OVERSIGHT
        )

        await workflow.process_request(request.id)

        result = await workflow.human_decide(
            request.id,
            approved=False,
            decided_by="human_reviewer",
            reason="Risk too high"
        )

        assert result.approved == False

    @pytest.mark.asyncio
    async def test_audit_logging(self, workflow, low_risk_proposal):
        """Test that actions are logged to audit."""
        await workflow.create_request(
            low_risk_proposal,
            GovernanceTier.AUTOMATIC
        )

        log = workflow.get_audit_log()
        assert len(log) >= 1
        assert log[0].event_type == "approval_requested"

    def test_get_stats(self, workflow):
        """Test workflow statistics."""
        stats = workflow.get_stats()

        assert 'requests_created' in stats
        assert 'requests_approved' in stats
        assert 'requests_rejected' in stats

    @pytest.mark.asyncio
    async def test_reset(self, workflow, low_risk_proposal):
        """Test workflow reset."""
        await workflow.create_request(
            low_risk_proposal,
            GovernanceTier.AUTOMATIC
        )

        assert workflow.get_stats()['requests_created'] == 1

        workflow.reset()

        assert workflow.get_stats()['requests_created'] == 0


# ============================================================================
# Full Governance Tests
# ============================================================================

class TestSafetyGovernance:
    """Integration tests for full governance flow."""

    @pytest.mark.asyncio
    async def test_evaluate_and_approve_low_risk(self, governance, low_risk_proposal):
        """Test full flow for low-risk proposal."""
        decision, result = await governance.evaluate_and_approve(low_risk_proposal)

        assert decision.can_proceed == True
        assert result.approved == True

    @pytest.mark.asyncio
    async def test_evaluate_and_approve_constitutional(self, governance, constitutional_proposal):
        """Test full flow for constitutional violation."""
        decision, result = await governance.evaluate_and_approve(constitutional_proposal)

        assert decision.can_proceed == False
        assert decision.tier == GovernanceTier.CONSTITUTIONAL
        assert result is None

    @pytest.mark.asyncio
    async def test_recommendations_generated(self, governance, medium_risk_proposal):
        """Test that recommendations are generated."""
        decision = await governance.evaluate(medium_risk_proposal)

        assert len(decision.recommendations) > 0

    def test_get_tier_info(self, governance):
        """Test getting tier information."""
        info = governance.get_tier_info(GovernanceTier.REVIEWED)

        assert info['name'] == "Reviewed"
        assert info['requires_tests'] == True

    def test_get_all_tiers_info(self, governance):
        """Test getting all tiers information."""
        all_info = governance.get_all_tiers_info()

        assert len(all_info) == 5

    @pytest.mark.asyncio
    async def test_get_pending_approvals(self, governance, high_risk_proposal):
        """Test getting pending approvals."""
        # Evaluate to get tier
        decision = await governance.evaluate(high_risk_proposal)

        # Request approval (will be pending for human oversight)
        await governance.request_approval(high_risk_proposal, GovernanceTier.HUMAN_OVERSIGHT)

        pending = governance.get_pending_approvals()
        assert len(pending) >= 1

    def test_get_stats(self, governance):
        """Test governance statistics."""
        stats = governance.get_stats()

        assert 'evaluations_count' in stats
        assert 'blocked_count' in stats
        assert 'approved_count' in stats

    @pytest.mark.asyncio
    async def test_reset(self, governance, low_risk_proposal):
        """Test governance reset."""
        await governance.evaluate(low_risk_proposal)

        assert governance.get_stats()['evaluations_count'] == 1

        governance.reset()

        assert governance.get_stats()['evaluations_count'] == 0


# ============================================================================
# Edge Cases
# ============================================================================

class TestEdgeCases:
    """Tests for edge cases."""

    @pytest.mark.asyncio
    async def test_empty_proposal(self, governance):
        """Test handling of minimal proposal."""
        proposal = ModificationProposal(
            id="prop_empty",
            description="Empty",
            modification_type="unknown",
            target_files=[],
            changes={},
            rationale=""
        )

        decision = await governance.evaluate(proposal)

        # Should still work, just low risk
        assert decision.can_proceed == True

    @pytest.mark.asyncio
    async def test_multiple_protected_files(self, governance):
        """Test proposal targeting multiple protected files."""
        proposal = ModificationProposal(
            id="prop_multi",
            description="Modify multiple protected",
            modification_type="code_change",
            target_files=["provenance.py", "constitutional.py"],
            changes={"modify": "both"},
            rationale="Dangerous"
        )

        decision = await governance.evaluate(proposal)

        assert len(decision.blocking_issues) >= 2
        assert decision.can_proceed == False

    @pytest.mark.asyncio
    async def test_risk_mitigation_reduces_score(self, governance):
        """Test that mitigations reduce risk score."""
        # Proposal without mitigations
        proposal1 = ModificationProposal(
            id="prop_no_mit",
            description="No mitigations",
            modification_type="capability_add",
            target_files=["module.py"],
            changes={"add": "feature"},
            rationale="Test"
        )

        # Same proposal with mitigations
        proposal2 = ModificationProposal(
            id="prop_with_mit",
            description="With mitigations",
            modification_type="capability_add",
            target_files=["module.py"],
            changes={"add": "feature"},
            rationale="Test",
            metadata={"has_tests": True, "has_rollback": True}
        )

        decision1 = await governance.evaluate(proposal1)
        decision2 = await governance.evaluate(proposal2)

        assert decision2.risk_assessment.score <= decision1.risk_assessment.score

    @pytest.mark.asyncio
    async def test_request_not_found(self, workflow):
        """Test handling of non-existent request."""
        result = await workflow.process_request("nonexistent_id")

        assert result.approved == False
        assert "not found" in result.reason.lower()


# ============================================================================
# Dataclass Serialization Tests
# ============================================================================

class TestSerialization:
    """Tests for dataclass serialization."""

    def test_proposal_to_dict(self, low_risk_proposal):
        """Test ModificationProposal serialization."""
        d = low_risk_proposal.to_dict()

        assert d['id'] == "prop_001"
        assert d['modification_type'] == "config_update"

    @pytest.mark.asyncio
    async def test_decision_to_dict(self, governance, low_risk_proposal):
        """Test GovernanceDecision serialization."""
        decision = await governance.evaluate(low_risk_proposal)
        d = decision.to_dict()

        assert 'tier' in d
        assert 'tier_name' in d
        assert 'risk_assessment' in d

    @pytest.mark.asyncio
    async def test_request_to_dict(self, workflow, low_risk_proposal):
        """Test ApprovalRequest serialization."""
        request = await workflow.create_request(
            low_risk_proposal,
            GovernanceTier.AUTOMATIC
        )
        d = request.to_dict()

        assert d['tier'] == 1
        assert d['status'] == 'pending'
