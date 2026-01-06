"""
Safety Governance Tiers.

Defines the 5-tier approval system for modifications.
Higher tiers require more oversight.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 2.4 for specification.
"""

from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from datetime import datetime, timezone


class GovernanceTier(IntEnum):
    """
    5-tier governance hierarchy.

    Higher numbers = more oversight required.
    """
    AUTOMATIC = 1        # Auto-approved (Level 0 mods, configuration changes)
    VERIFIED = 2         # Requires test verification before approval
    REVIEWED = 3         # Requires safety review and risk assessment
    HUMAN_OVERSIGHT = 4  # Requires explicit human approval
    CONSTITUTIONAL = 5   # Never approved (protected files/operations)


class RiskCategory(Enum):
    """Categories of risk for modifications."""
    CONFIGURATION = "configuration"      # Config file changes
    DATA = "data"                        # Data processing changes
    BEHAVIOR = "behavior"                # Behavioral changes
    CAPABILITY = "capability"            # New capability additions
    ARCHITECTURE = "architecture"        # Architectural changes
    SAFETY = "safety"                    # Safety system changes
    CONSTITUTIONAL = "constitutional"    # Core identity changes


class ModificationScope(Enum):
    """Scope of a modification."""
    LOCAL = "local"          # Single module/file
    COMPONENT = "component"  # Multiple related files
    SYSTEM = "system"        # Cross-component
    CORE = "core"            # Core system changes


@dataclass
class TierCriteria:
    """Criteria that determine governance tier."""
    name: str
    description: str
    risk_categories: List[RiskCategory]
    max_scope: ModificationScope
    requires_tests: bool
    requires_rollback: bool
    auto_approve: bool
    max_risk_score: float
    cooldown_seconds: int = 0  # Minimum time between approvals


# Tier definitions with criteria
TIER_DEFINITIONS: Dict[GovernanceTier, TierCriteria] = {
    GovernanceTier.AUTOMATIC: TierCriteria(
        name="Automatic",
        description="Low-risk changes that can be auto-approved",
        risk_categories=[RiskCategory.CONFIGURATION],
        max_scope=ModificationScope.LOCAL,
        requires_tests=False,
        requires_rollback=True,
        auto_approve=True,
        max_risk_score=0.2
    ),
    GovernanceTier.VERIFIED: TierCriteria(
        name="Verified",
        description="Changes requiring test verification",
        risk_categories=[RiskCategory.CONFIGURATION, RiskCategory.DATA],
        max_scope=ModificationScope.COMPONENT,
        requires_tests=True,
        requires_rollback=True,
        auto_approve=True,  # Auto after tests pass
        max_risk_score=0.4
    ),
    GovernanceTier.REVIEWED: TierCriteria(
        name="Reviewed",
        description="Changes requiring safety review",
        risk_categories=[
            RiskCategory.CONFIGURATION,
            RiskCategory.DATA,
            RiskCategory.BEHAVIOR,
            RiskCategory.CAPABILITY
        ],
        max_scope=ModificationScope.SYSTEM,
        requires_tests=True,
        requires_rollback=True,
        auto_approve=False,
        max_risk_score=0.6
    ),
    GovernanceTier.HUMAN_OVERSIGHT: TierCriteria(
        name="Human Oversight",
        description="Changes requiring explicit human approval",
        risk_categories=[
            RiskCategory.CONFIGURATION,
            RiskCategory.DATA,
            RiskCategory.BEHAVIOR,
            RiskCategory.CAPABILITY,
            RiskCategory.ARCHITECTURE
        ],
        max_scope=ModificationScope.SYSTEM,
        requires_tests=True,
        requires_rollback=True,
        auto_approve=False,
        max_risk_score=0.8,
        cooldown_seconds=3600  # 1 hour between approvals
    ),
    GovernanceTier.CONSTITUTIONAL: TierCriteria(
        name="Constitutional",
        description="Protected operations that cannot be approved",
        risk_categories=[
            RiskCategory.SAFETY,
            RiskCategory.CONSTITUTIONAL
        ],
        max_scope=ModificationScope.CORE,
        requires_tests=True,
        requires_rollback=False,  # Never executed
        auto_approve=False,
        max_risk_score=1.0
    ),
}


# Protected files that trigger CONSTITUTIONAL tier
CONSTITUTIONAL_PROTECTED_FILES: Set[str] = {
    "provenance.py",
    "modification_log.py",
    "self_modification.py",
    "constitutional.py",
    "rsi/safety/tiers.py",
    "rsi/safety/governance.py",
}

# Protected patterns that trigger CONSTITUTIONAL tier
CONSTITUTIONAL_PROTECTED_PATTERNS: List[str] = [
    r"os\.system",
    r"subprocess\.",
    r"eval\(",
    r"exec\(",
    r"__import__\(",
    r"open\(.+['\"]w",  # File writes
]


@dataclass
class RiskAssessment:
    """Assessment of modification risk."""
    score: float  # 0.0 to 1.0
    category: RiskCategory
    scope: ModificationScope
    factors: List[str]  # Factors contributing to risk
    mitigations: List[str]  # Available mitigations


def get_tier_for_risk(risk_score: float, category: RiskCategory) -> GovernanceTier:
    """
    Determine governance tier based on risk score and category.

    Args:
        risk_score: Risk score from 0.0 to 1.0
        category: Risk category of modification

    Returns:
        Appropriate GovernanceTier
    """
    # Constitutional category always gets highest tier
    if category in [RiskCategory.SAFETY, RiskCategory.CONSTITUTIONAL]:
        return GovernanceTier.CONSTITUTIONAL

    # Find tier based on risk score
    for tier in sorted(GovernanceTier, key=lambda t: t.value):
        criteria = TIER_DEFINITIONS[tier]
        if risk_score <= criteria.max_risk_score:
            # Check if category is allowed at this tier
            if category in criteria.risk_categories:
                return tier

    # Default to HUMAN_OVERSIGHT if no tier matches
    return GovernanceTier.HUMAN_OVERSIGHT


def is_protected_file(file_path: str) -> bool:
    """Check if a file is constitutionally protected."""
    # Normalize path
    normalized = file_path.replace("\\", "/")

    for protected in CONSTITUTIONAL_PROTECTED_FILES:
        if normalized.endswith(protected):
            return True

    return False


def get_tier_requirements(tier: GovernanceTier) -> TierCriteria:
    """Get requirements for a governance tier."""
    return TIER_DEFINITIONS.get(tier, TIER_DEFINITIONS[GovernanceTier.CONSTITUTIONAL])
