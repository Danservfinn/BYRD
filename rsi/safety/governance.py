"""
Safety Governance Engine.

Main engine for the 5-tier safety governance system.
Evaluates modifications and routes to appropriate approval tier.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 2.4 for specification.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timezone
import logging
import re
import asyncio

from .tiers import (
    GovernanceTier,
    RiskCategory,
    ModificationScope,
    RiskAssessment,
    TierCriteria,
    TIER_DEFINITIONS,
    CONSTITUTIONAL_PROTECTED_FILES,
    CONSTITUTIONAL_PROTECTED_PATTERNS,
    get_tier_for_risk,
    is_protected_file,
    get_tier_requirements,
)
from .approval import (
    ModificationProposal,
    ApprovalRequest,
    ApprovalResult,
    ApprovalWorkflow,
    ApprovalStatus,
)

logger = logging.getLogger("rsi.safety.governance")


@dataclass
class GovernanceDecision:
    """Decision from governance evaluation."""
    proposal_id: str
    tier: GovernanceTier
    risk_assessment: RiskAssessment
    requires_approval: bool
    blocking_issues: List[str]
    recommendations: List[str]
    can_proceed: bool  # False if CONSTITUTIONAL

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'proposal_id': self.proposal_id,
            'tier': self.tier.value,
            'tier_name': self.tier.name,
            'risk_assessment': {
                'score': self.risk_assessment.score,
                'category': self.risk_assessment.category.value,
                'scope': self.risk_assessment.scope.value,
                'factors': self.risk_assessment.factors,
                'mitigations': self.risk_assessment.mitigations
            },
            'requires_approval': self.requires_approval,
            'blocking_issues': self.blocking_issues,
            'recommendations': self.recommendations,
            'can_proceed': self.can_proceed
        }


class SafetyGovernance:
    """
    5-tier approval system for modifications.

    Evaluates proposals, determines risk, and routes to
    appropriate approval tier.

    Tier Hierarchy:
    1. AUTOMATIC - Auto-approved for low-risk changes
    2. VERIFIED - Requires test verification
    3. REVIEWED - Requires safety review
    4. HUMAN_OVERSIGHT - Requires human approval
    5. CONSTITUTIONAL - Never approved (protected)
    """

    def __init__(
        self,
        memory=None,
        config: Dict = None,
        test_runner=None
    ):
        """
        Initialize safety governance.

        Args:
            memory: Optional Memory instance for persistence
            config: Configuration options
            test_runner: Optional test runner for verification
        """
        self.memory = memory
        self.config = config or {}

        # Initialize approval workflow
        self.workflow = ApprovalWorkflow(
            memory=memory,
            config=config,
            test_runner=test_runner
        )

        # Risk scoring weights
        self._risk_weights = {
            'file_protected': 1.0,
            'pattern_dangerous': 0.8,
            'scope_system': 0.3,
            'capability_new': 0.2,
            'has_tests': -0.1,  # Reduces risk
            'has_rollback': -0.1,  # Reduces risk
        }

        # Statistics
        self._evaluations_count: int = 0
        self._blocked_count: int = 0
        self._approved_count: int = 0

    async def evaluate(
        self,
        proposal: ModificationProposal
    ) -> GovernanceDecision:
        """
        Evaluate a modification proposal.

        Determines the appropriate governance tier based on
        risk assessment.

        Args:
            proposal: The modification proposal

        Returns:
            GovernanceDecision with tier and requirements
        """
        self._evaluations_count += 1

        # Assess risk
        risk_assessment = await self._assess_risk(proposal)
        proposal.risk_assessment = risk_assessment

        # Check for constitutional violations
        blocking_issues = await self._check_constitutional(proposal)

        if blocking_issues:
            self._blocked_count += 1
            return GovernanceDecision(
                proposal_id=proposal.id,
                tier=GovernanceTier.CONSTITUTIONAL,
                risk_assessment=risk_assessment,
                requires_approval=False,
                blocking_issues=blocking_issues,
                recommendations=["Cannot proceed - constitutional protection"],
                can_proceed=False
            )

        # Determine tier from risk
        tier = get_tier_for_risk(
            risk_assessment.score,
            risk_assessment.category
        )

        # Get tier requirements
        requirements = get_tier_requirements(tier)

        # Generate recommendations
        recommendations = self._generate_recommendations(
            proposal, tier, risk_assessment
        )

        logger.info(
            f"Evaluated proposal {proposal.id}: "
            f"tier={tier.name}, risk={risk_assessment.score:.2f}"
        )

        return GovernanceDecision(
            proposal_id=proposal.id,
            tier=tier,
            risk_assessment=risk_assessment,
            requires_approval=not requirements.auto_approve,
            blocking_issues=[],
            recommendations=recommendations,
            can_proceed=True
        )

    async def request_approval(
        self,
        proposal: ModificationProposal,
        tier: GovernanceTier
    ) -> ApprovalResult:
        """
        Request approval for a proposal at specified tier.

        Args:
            proposal: The modification proposal
            tier: Governance tier determined by evaluate()

        Returns:
            ApprovalResult with decision
        """
        # Create approval request
        request = await self.workflow.create_request(proposal, tier)

        # Process through tier workflow
        result = await self.workflow.process_request(request.id)

        if result.approved:
            self._approved_count += 1

        return result

    async def evaluate_and_approve(
        self,
        proposal: ModificationProposal
    ) -> Tuple[GovernanceDecision, Optional[ApprovalResult]]:
        """
        Evaluate and request approval in one step.

        Convenience method that evaluates risk and automatically
        requests approval if the tier allows.

        Args:
            proposal: The modification proposal

        Returns:
            Tuple of (GovernanceDecision, ApprovalResult or None)
        """
        # First evaluate
        decision = await self.evaluate(proposal)

        if not decision.can_proceed:
            return decision, None

        # Request approval
        result = await self.request_approval(proposal, decision.tier)

        return decision, result

    async def _assess_risk(
        self,
        proposal: ModificationProposal
    ) -> RiskAssessment:
        """
        Assess the risk of a modification proposal.

        Returns RiskAssessment with score and factors.
        """
        factors = []
        mitigations = []
        risk_score = 0.0

        # Check for protected files
        for file_path in proposal.target_files:
            if is_protected_file(file_path):
                factors.append(f"Protected file: {file_path}")
                risk_score += self._risk_weights['file_protected']

        # Check for dangerous patterns
        changes_str = str(proposal.changes)
        for pattern in CONSTITUTIONAL_PROTECTED_PATTERNS:
            if re.search(pattern, changes_str):
                factors.append(f"Dangerous pattern: {pattern}")
                risk_score += self._risk_weights['pattern_dangerous']

        # Determine scope
        scope = self._determine_scope(proposal)
        if scope == ModificationScope.SYSTEM:
            factors.append("System-wide modification")
            risk_score += self._risk_weights['scope_system']
        elif scope == ModificationScope.CORE:
            factors.append("Core system modification")
            risk_score += 0.5

        # Determine category
        category = self._determine_category(proposal)
        if category == RiskCategory.CAPABILITY:
            factors.append("New capability addition")
            risk_score += self._risk_weights['capability_new']
        elif category == RiskCategory.ARCHITECTURE:
            factors.append("Architectural change")
            risk_score += 0.3

        # Check for mitigations
        if proposal.metadata.get('has_tests'):
            mitigations.append("Test coverage available")
            risk_score += self._risk_weights['has_tests']

        if proposal.metadata.get('has_rollback'):
            mitigations.append("Rollback plan available")
            risk_score += self._risk_weights['has_rollback']

        # Clamp score to [0, 1]
        risk_score = max(0.0, min(1.0, risk_score))

        return RiskAssessment(
            score=risk_score,
            category=category,
            scope=scope,
            factors=factors,
            mitigations=mitigations
        )

    async def _check_constitutional(
        self,
        proposal: ModificationProposal
    ) -> List[str]:
        """
        Check for constitutional violations.

        Returns list of blocking issues, empty if none.
        """
        issues = []

        # Check protected files
        for file_path in proposal.target_files:
            if is_protected_file(file_path):
                issues.append(
                    f"Cannot modify protected file: {file_path}"
                )

        # Check for dangerous operations
        changes_str = str(proposal.changes)
        dangerous_ops = [
            (r"os\.system", "Shell command execution"),
            (r"subprocess\.", "Subprocess execution"),
            (r"eval\(", "Dynamic code evaluation"),
            (r"exec\(", "Dynamic code execution"),
            (r"__import__\(", "Dynamic import"),
        ]

        for pattern, description in dangerous_ops:
            if re.search(pattern, changes_str):
                issues.append(
                    f"Dangerous operation blocked: {description}"
                )

        return issues

    def _determine_scope(
        self,
        proposal: ModificationProposal
    ) -> ModificationScope:
        """Determine the scope of a modification."""
        file_count = len(proposal.target_files)

        if file_count == 1:
            return ModificationScope.LOCAL
        elif file_count <= 5:
            return ModificationScope.COMPONENT
        else:
            return ModificationScope.SYSTEM

    def _determine_category(
        self,
        proposal: ModificationProposal
    ) -> RiskCategory:
        """Determine the risk category of a modification."""
        mod_type = proposal.modification_type.lower()

        if 'config' in mod_type:
            return RiskCategory.CONFIGURATION
        elif 'data' in mod_type:
            return RiskCategory.DATA
        elif 'behavior' in mod_type:
            return RiskCategory.BEHAVIOR
        elif 'capability' in mod_type or 'module' in mod_type:
            return RiskCategory.CAPABILITY
        elif 'architecture' in mod_type:
            return RiskCategory.ARCHITECTURE
        elif 'safety' in mod_type:
            return RiskCategory.SAFETY
        else:
            return RiskCategory.BEHAVIOR  # Default

    def _generate_recommendations(
        self,
        proposal: ModificationProposal,
        tier: GovernanceTier,
        risk: RiskAssessment
    ) -> List[str]:
        """Generate recommendations for a proposal."""
        recommendations = []

        requirements = get_tier_requirements(tier)

        if requirements.requires_tests:
            recommendations.append("Run test suite before applying")

        if requirements.requires_rollback:
            recommendations.append("Prepare rollback plan")

        if tier == GovernanceTier.REVIEWED:
            recommendations.append("Schedule safety review")

        if tier == GovernanceTier.HUMAN_OVERSIGHT:
            recommendations.append("Await human approval before proceeding")

        if risk.score > 0.5:
            recommendations.append("Consider breaking into smaller changes")

        if len(proposal.target_files) > 3:
            recommendations.append("Consider incremental deployment")

        return recommendations

    def get_tier_info(self, tier: GovernanceTier) -> Dict:
        """Get information about a governance tier."""
        criteria = get_tier_requirements(tier)
        return {
            'tier': tier.value,
            'name': criteria.name,
            'description': criteria.description,
            'requires_tests': criteria.requires_tests,
            'requires_rollback': criteria.requires_rollback,
            'auto_approve': criteria.auto_approve,
            'max_risk_score': criteria.max_risk_score
        }

    def get_all_tiers_info(self) -> List[Dict]:
        """Get information about all governance tiers."""
        return [self.get_tier_info(tier) for tier in GovernanceTier]

    def get_pending_approvals(self) -> List[ApprovalRequest]:
        """Get all pending approval requests."""
        return self.workflow.get_pending_requests()

    async def human_approve(
        self,
        request_id: str,
        approved: bool,
        approver: str,
        reason: str
    ) -> ApprovalResult:
        """
        Record a human approval decision.

        Args:
            request_id: Request to decide
            approved: Whether approved
            approver: Human identifier
            reason: Reason for decision
        """
        return await self.workflow.human_decide(
            request_id, approved, approver, reason
        )

    def get_stats(self) -> Dict:
        """Get governance statistics."""
        workflow_stats = self.workflow.get_stats()
        return {
            'evaluations_count': self._evaluations_count,
            'blocked_count': self._blocked_count,
            'approved_count': self._approved_count,
            'approval_rate': (
                self._approved_count / self._evaluations_count
                if self._evaluations_count > 0 else 0.0
            ),
            **workflow_stats
        }

    def reset(self) -> None:
        """Reset governance state."""
        self.workflow.reset()
        self._evaluations_count = 0
        self._blocked_count = 0
        self._approved_count = 0
        logger.info("SafetyGovernance reset")
