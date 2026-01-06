"""
Safety Governance Module.

Provides 5-tier safety governance for system modifications.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 2.4 for specification.
"""

from .tiers import (
    GovernanceTier,
    RiskCategory,
    ModificationScope,
    TierCriteria,
    RiskAssessment,
    TIER_DEFINITIONS,
    CONSTITUTIONAL_PROTECTED_FILES,
    CONSTITUTIONAL_PROTECTED_PATTERNS,
    get_tier_for_risk,
    is_protected_file,
    get_tier_requirements,
)

from .approval import (
    ApprovalStatus,
    ModificationProposal,
    ApprovalRequest,
    ApprovalResult,
    AuditEntry,
    ApprovalWorkflow,
)

from .governance import (
    GovernanceDecision,
    SafetyGovernance,
)

__all__ = [
    # Tiers
    "GovernanceTier",
    "RiskCategory",
    "ModificationScope",
    "TierCriteria",
    "RiskAssessment",
    "TIER_DEFINITIONS",
    "CONSTITUTIONAL_PROTECTED_FILES",
    "CONSTITUTIONAL_PROTECTED_PATTERNS",
    "get_tier_for_risk",
    "is_protected_file",
    "get_tier_requirements",
    # Approval
    "ApprovalStatus",
    "ModificationProposal",
    "ApprovalRequest",
    "ApprovalResult",
    "AuditEntry",
    "ApprovalWorkflow",
    # Governance
    "GovernanceDecision",
    "SafetyGovernance",
]
