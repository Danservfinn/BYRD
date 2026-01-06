"""
Recursion Module.

Enables unbounded recursive improvement with level-invariant primitives.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 3.3 for specification.
"""

from .algebra import (
    # Types
    ImprovementType,
    ImprovementResult,
    # Base classes
    Improvement,
    IdentityImprovement,
    FunctionImprovement,
    # Composed improvements
    SequentialImprovement,
    ParallelImprovement,
    ConditionalImprovement,
    RecursiveImprovement,
    UntilImprovement,
    ChoiceImprovement,
    FallbackImprovement,
    # Algebra
    ImprovementAlgebra,
)

from .representation import (
    # Types
    LevelType,
    # Core representations
    Improvable,
    LeveledPattern,
    CompressedPatterns,
    # Primitives
    LevelInvariantPrimitive,
    ObservePrimitive,
    TransformPrimitive,
    EvaluatePrimitive,
    SelectPrimitive,
    ComposedPrimitive,
    # Compression
    MetaLevelCompressor,
)

from .depth_amplifier import (
    AmplificationConfig,
    AmplificationResult,
    RecursiveDepthAmplifier,
)

__all__ = [
    # Algebra - Types
    "ImprovementType",
    "ImprovementResult",
    # Algebra - Base
    "Improvement",
    "IdentityImprovement",
    "FunctionImprovement",
    # Algebra - Composed
    "SequentialImprovement",
    "ParallelImprovement",
    "ConditionalImprovement",
    "RecursiveImprovement",
    "UntilImprovement",
    "ChoiceImprovement",
    "FallbackImprovement",
    # Algebra - Operators
    "ImprovementAlgebra",
    # Representation - Types
    "LevelType",
    # Representation - Core
    "Improvable",
    "LeveledPattern",
    "CompressedPatterns",
    # Representation - Primitives
    "LevelInvariantPrimitive",
    "ObservePrimitive",
    "TransformPrimitive",
    "EvaluatePrimitive",
    "SelectPrimitive",
    "ComposedPrimitive",
    # Representation - Compression
    "MetaLevelCompressor",
    # Depth Amplifier
    "AmplificationConfig",
    "AmplificationResult",
    "RecursiveDepthAmplifier",
]
