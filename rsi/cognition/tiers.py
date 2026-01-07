"""
Cognitive Tier Definitions.

BYRD's cognitive hierarchy:
- TIER 0 (REFLEX): No LLM, pattern matching only
- TIER 1 (GLM_4_7): ZAI GLM 4.7 - FREE, UNLIMITED, DEFAULT
- TIER 2 (PREMIUM): Claude/GPT-4 - Paid, strategic escalation
- TIER 3 (CUSTOM): Fine-tuned models - Training investment

See PROMPT.md "Layer 2: Cognitive Tiering System (GLM-FIRST)" for spec.
"""

from typing import Dict, Optional, Any, List
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger("rsi.cognition.tiers")


class CognitiveTier(Enum):
    """
    Cognitive resource tiers.

    CRITICAL: GLM_4_7 is the FREE default. Always try it first.
    """
    REFLEX = 0      # No LLM - cache, pattern matching
    GLM_4_7 = 1     # ZAI GLM 4.7 - FREE, UNLIMITED
    PREMIUM = 2     # Claude/GPT-4 - Paid escalation
    EXTENDED = 3    # Extended thinking - High cost
    CUSTOM = 4      # Fine-tuned models - Training investment


@dataclass
class TierCost:
    """Cost structure for a tier."""
    cost_per_1k_input: float = 0.0
    cost_per_1k_output: float = 0.0
    base_cost: float = 0.0  # Per-request base cost

    def estimate(self, input_tokens: int, output_tokens: int) -> float:
        """Estimate total cost for a request."""
        return (
            self.base_cost +
            (input_tokens / 1000) * self.cost_per_1k_input +
            (output_tokens / 1000) * self.cost_per_1k_output
        )


@dataclass
class TierConfig:
    """Configuration for a cognitive tier."""
    tier: CognitiveTier
    name: str
    description: str
    provider: str
    model: str
    cost: TierCost
    max_context: int
    max_output: int
    capabilities: List[str] = field(default_factory=list)
    is_free: bool = False
    is_default: bool = False
    requires_approval: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'tier': self.tier.value,
            'name': self.name,
            'description': self.description,
            'provider': self.provider,
            'model': self.model,
            'cost': {
                'per_1k_input': self.cost.cost_per_1k_input,
                'per_1k_output': self.cost.cost_per_1k_output,
                'base': self.cost.base_cost
            },
            'max_context': self.max_context,
            'max_output': self.max_output,
            'capabilities': self.capabilities,
            'is_free': self.is_free,
            'is_default': self.is_default,
            'requires_approval': self.requires_approval
        }


# ============================================================================
# TIER CONFIGURATIONS
# ============================================================================

TIER_CONFIGS: Dict[CognitiveTier, TierConfig] = {
    CognitiveTier.REFLEX: TierConfig(
        tier=CognitiveTier.REFLEX,
        name="Reflex",
        description="Pattern matching, cache hits, no LLM required",
        provider="internal",
        model="cache",
        cost=TierCost(0.0, 0.0, 0.0),
        max_context=0,  # Not applicable
        max_output=0,
        capabilities=["pattern_matching", "cache_lookup", "simple_routing"],
        is_free=True,
        is_default=False,
        requires_approval=False
    ),

    CognitiveTier.GLM_4_7: TierConfig(
        tier=CognitiveTier.GLM_4_7,
        name="GLM 4.7",
        description="ZAI GLM 4.7 - BYRD's native substrate, UNLIMITED FREE",
        provider="zai",
        model="glm-4.7",
        cost=TierCost(0.0, 0.0, 0.0),  # FREE for 1 year
        max_context=128000,
        max_output=4096,
        capabilities=[
            "general_reasoning",
            "code_generation",
            "code_review",
            "analysis",
            "planning",
            "reflection",
            "multi_step_decomposition",
            "creative_problem_solving"
        ],
        is_free=True,
        is_default=True,  # THIS IS THE DEFAULT
        requires_approval=False
    ),

    CognitiveTier.PREMIUM: TierConfig(
        tier=CognitiveTier.PREMIUM,
        name="Premium API",
        description="Claude 3.5/Opus or GPT-4 - Strategic escalation only",
        provider="anthropic",  # or openai
        model="claude-3-5-sonnet-20241022",
        cost=TierCost(0.003, 0.015, 0.0),  # ~$0.003/1K in, ~$0.015/1K out
        max_context=200000,
        max_output=8192,
        capabilities=[
            "frontier_reasoning",
            "validation",
            "critical_decisions",
            "complex_synthesis",
            "cross_validation"
        ],
        is_free=False,
        is_default=False,
        requires_approval=False  # Automatic but logged
    ),

    CognitiveTier.EXTENDED: TierConfig(
        tier=CognitiveTier.EXTENDED,
        name="Extended Thinking",
        description="Multi-hour deep reasoning - Requires human approval",
        provider="anthropic",
        model="claude-3-opus",
        cost=TierCost(0.015, 0.075, 0.0),  # Higher cost
        max_context=200000,
        max_output=4096,
        capabilities=[
            "deep_reasoning",
            "paradigm_shifts",
            "novel_architecture",
            "major_decisions"
        ],
        is_free=False,
        is_default=False,
        requires_approval=True  # Human must approve
    ),

    CognitiveTier.CUSTOM: TierConfig(
        tier=CognitiveTier.CUSTOM,
        name="Custom Trained",
        description="BYRD-specialized fine-tuned models",
        provider="self",
        model="byrd-specialist",
        cost=TierCost(0.0001, 0.0002, 0.0),  # Inference is cheap
        max_context=32000,
        max_output=4096,
        capabilities=[
            "domain_specialist",
            "task_optimized",
            "capability_crystallized"
        ],
        is_free=True,  # After training investment
        is_default=False,
        requires_approval=False
    )
}


def get_tier_config(tier: CognitiveTier) -> TierConfig:
    """Get configuration for a tier."""
    return TIER_CONFIGS.get(tier, TIER_CONFIGS[CognitiveTier.GLM_4_7])


def get_default_tier() -> CognitiveTier:
    """Get the default tier (GLM 4.7)."""
    return CognitiveTier.GLM_4_7


def estimate_tier_cost(
    tier: CognitiveTier,
    input_tokens: int,
    output_tokens: int
) -> float:
    """Estimate cost for a tier request."""
    config = get_tier_config(tier)
    return config.cost.estimate(input_tokens, output_tokens)


def get_free_tiers() -> List[CognitiveTier]:
    """Get all free tiers."""
    return [t for t, c in TIER_CONFIGS.items() if c.is_free]


def get_approval_required_tiers() -> List[CognitiveTier]:
    """Get tiers requiring human approval."""
    return [t for t, c in TIER_CONFIGS.items() if c.requires_approval]


def tier_supports_capability(
    tier: CognitiveTier,
    capability: str
) -> bool:
    """Check if a tier supports a capability."""
    config = get_tier_config(tier)
    return capability in config.capabilities


def get_cheapest_tier_for_capability(capability: str) -> Optional[CognitiveTier]:
    """Get the cheapest tier that supports a capability."""
    matching = []
    for tier, config in TIER_CONFIGS.items():
        if capability in config.capabilities:
            matching.append((tier, config))

    if not matching:
        return None

    # Sort by free first, then by cost
    matching.sort(key=lambda x: (not x[1].is_free, x[1].cost.cost_per_1k_output))
    return matching[0][0]
