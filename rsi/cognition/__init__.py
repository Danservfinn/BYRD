"""
Cognitive Tiering System for BYRD RSI.

GLM 4.7 is the native substrate (Tier 1) - unlimited, free, default.
Premium models (Tier 2) are strategic escalations.
Custom trained models (Tier 3) are capability crystallizations.

This module provides:
- CognitiveTier: Tier definitions (REFLEX, GLM_4_7, PREMIUM, CUSTOM)
- CognitiveRouter: Intelligent routing based on task + budget
- UnifiedCognition: High-level API (think, reason, create, evaluate)
- EscalationPolicy: When/why to escalate from Tier 1

See PROMPT.md "Layer 2: Cognitive Tiering" for specification.
"""

from .tiers import (
    CognitiveTier,
    TierConfig,
    TierCost,
    get_tier_config,
    estimate_tier_cost
)

from .router import (
    CognitiveRouter,
    RoutingDecision,
    RoutingContext,
    RouteResult,
    create_router
)

from .unified import (
    UnifiedCognition,
    CognitiveResult,
    CognitiveOperation,
    ThinkRequest,
    ReasonRequest,
    CreateRequest,
    EvaluateRequest,
    create_cognition
)

from .escalation import (
    EscalationPolicy,
    EscalationTrigger,
    EscalationDecision,
    should_escalate
)

from .integration import (
    TieredLLMClient,
    TieredLLMResponse,
    create_tiered_llm_client,
    wrap_llm_client
)

__all__ = [
    # Tiers
    "CognitiveTier",
    "TierConfig",
    "TierCost",
    "get_tier_config",
    "estimate_tier_cost",
    # Router
    "CognitiveRouter",
    "RoutingDecision",
    "RoutingContext",
    "RouteResult",
    "create_router",
    # Unified API
    "UnifiedCognition",
    "CognitiveResult",
    "CognitiveOperation",
    "ThinkRequest",
    "ReasonRequest",
    "CreateRequest",
    "EvaluateRequest",
    "create_cognition",
    # Escalation
    "EscalationPolicy",
    "EscalationTrigger",
    "EscalationDecision",
    "should_escalate",
    # Integration
    "TieredLLMClient",
    "TieredLLMResponse",
    "create_tiered_llm_client",
    "wrap_llm_client"
]
