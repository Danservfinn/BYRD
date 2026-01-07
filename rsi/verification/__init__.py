"""
Verification Module.

Provides scale-invariant verification, human anchoring,
and multi-verifier lattice composition for safe capability scaling.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 4.2 for specification.
See docs/IMPLEMENTATION_PLAN.md Phase 1.1 for lattice specification.
"""

from .scale_invariant import (
    MetricDomain,
    NormalizationType,
    MetricDefinition,
    MetricValue,
    ScaleInvariantReport,
    ScaleInvariantMetrics,
)

from .cross_scale import (
    VerificationLevel,
    PropertyType,
    SafetyProperty,
    PropertyVerification,
    ScaleTransition,
    CrossScaleVerificationResult,
    CrossScaleVerifier,
)

from .human_anchoring import (
    AnchorType,
    ValidationPriority,
    ValidationStatus,
    ValidationRequest,
    AnchorPoint,
    AnchoringResult,
    HumanAnchoringSystem,
)

from .lattice import (
    VerifierType,
    VerificationOutcome,
    VerifierResult,
    LatticeResult,
    Improvement,
    BaseVerifier,
    ExecutionTestsVerifier,
    PropertyChecksVerifier,
    LLMCritiqueVerifier,
    AdversarialProbesVerifier,
    HumanSpotCheckVerifier,
    VerificationLattice,
)

from .entropic_drift import (
    DriftSeverity,
    DriftType,
    DriftSignal,
    DriftReport,
    SolutionDiversityTracker,
    BenchmarkTracker,
    StrategyEntropyTracker,
    EntropicDriftMonitor,
)

__all__ = [
    # Scale-Invariant Metrics
    "MetricDomain",
    "NormalizationType",
    "MetricDefinition",
    "MetricValue",
    "ScaleInvariantReport",
    "ScaleInvariantMetrics",
    # Cross-Scale Verification
    "VerificationLevel",
    "PropertyType",
    "SafetyProperty",
    "PropertyVerification",
    "ScaleTransition",
    "CrossScaleVerificationResult",
    "CrossScaleVerifier",
    # Human Anchoring
    "AnchorType",
    "ValidationPriority",
    "ValidationStatus",
    "ValidationRequest",
    "AnchorPoint",
    "AnchoringResult",
    "HumanAnchoringSystem",
    # Verification Lattice
    "VerifierType",
    "VerificationOutcome",
    "VerifierResult",
    "LatticeResult",
    "Improvement",
    "BaseVerifier",
    "ExecutionTestsVerifier",
    "PropertyChecksVerifier",
    "LLMCritiqueVerifier",
    "AdversarialProbesVerifier",
    "HumanSpotCheckVerifier",
    "VerificationLattice",
    # Entropic Drift Detection
    "DriftSeverity",
    "DriftType",
    "DriftSignal",
    "DriftReport",
    "SolutionDiversityTracker",
    "BenchmarkTracker",
    "StrategyEntropyTracker",
    "EntropicDriftMonitor",
]
