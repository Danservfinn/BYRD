"""
MetaArchitect Module.

Learns to design better architectures through pattern extraction.
Implements Level 4 plasticity (META_ARCHITECTURE).

See docs/IMPLEMENTATION_PLAN_ASI.md Section 3.2 for specification.
"""

from .patterns import (
    PatternType,
    PatternStrength,
    PatternCondition,
    PatternAction,
    DesignPattern,
    PatternMatch,
    PatternLibrary,
)

from .learner import (
    ArchitectureOutcome,
    PatternCandidate,
    PatternLearner,
)

from .proposer import (
    ArchitectureProposal,
    ProposalConstraints,
    ArchitectureProposer,
)

from .meta_architect import (
    Outcome,
    MetaArchitectState,
    MetaArchitect,
)

__all__ = [
    # Patterns
    "PatternType",
    "PatternStrength",
    "PatternCondition",
    "PatternAction",
    "DesignPattern",
    "PatternMatch",
    "PatternLibrary",
    # Learner
    "ArchitectureOutcome",
    "PatternCandidate",
    "PatternLearner",
    # Proposer
    "ArchitectureProposal",
    "ProposalConstraints",
    "ArchitectureProposer",
    # MetaArchitect
    "Outcome",
    "MetaArchitectState",
    "MetaArchitect",
]
