"""
Scaling Module.

Handles capability explosion through growth monitoring,
resource scaling, and value protection.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 4.1 for specification.
"""

from .growth_rate import (
    GrowthCategory,
    CapabilitySnapshot,
    GrowthMetrics,
    GrowthRateMonitor,
)

from .resource_scaling import (
    ResourceType,
    ScalingStrategy,
    ResourceAllocation,
    ScalingDecision,
    ScalingResult,
    ResourceScaler,
)

from .value_stability import (
    ValueCategory,
    ProtectionLevel,
    ProtectedValue,
    ValueDrift,
    ValueProtectionResult,
    ValueStabilityGuard,
)

from .explosion_handler import (
    ExplosionPhase,
    HandlerAction,
    StabilityAssessment,
    ExplosionHandlerResult,
    CapabilityExplosionHandler,
)

__all__ = [
    # Growth Rate
    "GrowthCategory",
    "CapabilitySnapshot",
    "GrowthMetrics",
    "GrowthRateMonitor",
    # Resource Scaling
    "ResourceType",
    "ScalingStrategy",
    "ResourceAllocation",
    "ScalingDecision",
    "ScalingResult",
    "ResourceScaler",
    # Value Stability
    "ValueCategory",
    "ProtectionLevel",
    "ProtectedValue",
    "ValueDrift",
    "ValueProtectionResult",
    "ValueStabilityGuard",
    # Explosion Handler
    "ExplosionPhase",
    "HandlerAction",
    "StabilityAssessment",
    "ExplosionHandlerResult",
    "CapabilityExplosionHandler",
]
