"""
RSI Providers - Tier-aware LLM provider management.

Connects the cognitive tiering system to actual LLM clients.

This module provides:
- TierProvider: Tier-aware LLM client management
- ProviderFactory: Factory for creating providers per tier
- Integration with core/llm_client.py and rsi/cognition/

Design principle: GLM 4.7 is the native substrate (Tier 1).
All other tiers are escalations.

See PROMPT.md "Layer 2: Cognitive Tiering" for specification.
"""

from .tier_provider import (
    TierProvider,
    TierProviderConfig,
    create_tier_provider
)

__all__ = [
    "TierProvider",
    "TierProviderConfig",
    "create_tier_provider"
]
