"""
Neural Architecture Search Module.

Discovers new module architectures through evolutionary search.
Enables Level 3 plasticity (MODULE_DISCOVERY).

See docs/IMPLEMENTATION_PLAN_ASI.md Section 3.1 for specification.
"""

from .space import (
    NodeType,
    ConnectionType,
    OperationType,
    NodeSpec,
    ConnectionSpec,
    ArchitectureSpec,
    SpaceConstraints,
    SearchBudget,
    ArchitectureSpace,
)

from .evaluator import (
    TestCase,
    TestSuite,
    EvaluationMetric,
    ArchitectureScore,
    ArchitectureEvaluator,
)

from .search import (
    SearchStrategy,
    DiscoveredArchitecture,
    SearchResult,
    NeuralArchitectureSearch,
)

__all__ = [
    # Space
    "NodeType",
    "ConnectionType",
    "OperationType",
    "NodeSpec",
    "ConnectionSpec",
    "ArchitectureSpec",
    "SpaceConstraints",
    "SearchBudget",
    "ArchitectureSpace",
    # Evaluator
    "TestCase",
    "TestSuite",
    "EvaluationMetric",
    "ArchitectureScore",
    "ArchitectureEvaluator",
    # Search
    "SearchStrategy",
    "DiscoveredArchitecture",
    "SearchResult",
    "NeuralArchitectureSearch",
]
