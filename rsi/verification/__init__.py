"""
Verification Module.

Provides scale-invariant verification and human anchoring
for safe capability scaling.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 4.2 for specification.
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
]
