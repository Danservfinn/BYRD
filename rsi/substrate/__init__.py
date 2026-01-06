"""
Substrate Independence Layer.

Provides unified compute abstraction with multi-provider
failover and eventual self-hosting capabilities.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 2.3 for specification.
See docs/COGNITIVE_PLASTICITY.md for architecture.
"""

from .provider_registry import (
    ProviderType,
    ProviderStatus,
    ProviderCapabilities,
    ProviderConfig,
    ProviderHealth,
    ProviderRegistry,
)

from .failover_manager import (
    CircuitState,
    CircuitBreaker,
    FailoverResult,
    FailoverStrategy,
    FailoverManager,
)

from .compute_abstraction import (
    SubstrateLevel,
    GenerationConfig,
    GenerationResult,
    CostEstimate,
    SubstrateLevelInfo,
    SUBSTRATE_LEVELS,
    ComputeAbstractionLayer,
)

from .self_hosted import (
    ModelFormat,
    InferenceBackend,
    LocalModelConfig,
    InferenceServer,
    SelfHostedManager,
)

__all__ = [
    # Provider Registry
    "ProviderType",
    "ProviderStatus",
    "ProviderCapabilities",
    "ProviderConfig",
    "ProviderHealth",
    "ProviderRegistry",
    # Failover Manager
    "CircuitState",
    "CircuitBreaker",
    "FailoverResult",
    "FailoverStrategy",
    "FailoverManager",
    # Compute Abstraction
    "SubstrateLevel",
    "GenerationConfig",
    "GenerationResult",
    "CostEstimate",
    "SubstrateLevelInfo",
    "SUBSTRATE_LEVELS",
    "ComputeAbstractionLayer",
    # Self-Hosted (Future)
    "ModelFormat",
    "InferenceBackend",
    "LocalModelConfig",
    "InferenceServer",
    "SelfHostedManager",
]
