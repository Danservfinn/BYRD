"""
Tier-aware LLM Provider.

Manages LLM clients per cognitive tier.
Routes requests to appropriate providers based on tier.

Design principle:
- Tier 0 (REFLEX): No LLM - cache/pattern matching
- Tier 1 (GLM_4_7): ZAI GLM 4.7 - FREE, UNLIMITED, DEFAULT
- Tier 2 (PREMIUM): Claude/GPT-4 via OpenRouter
- Tier 3 (EXTENDED): Extended thinking models
- Tier 4 (CUSTOM): Fine-tuned models (future)

See PROMPT.md "Layer 2: Cognitive Tiering" for specification.
"""

from typing import Dict, Optional, Any, List
from dataclasses import dataclass, field
from datetime import datetime, timezone
import logging
import os

from rsi.cognition.tiers import CognitiveTier, get_tier_config, TIER_CONFIGS
from rsi.substrate.provider_registry import (
    ProviderRegistry,
    ProviderStatus
)

logger = logging.getLogger("rsi.providers.tier_provider")


@dataclass
class TierProviderConfig:
    """Configuration for a tier provider."""
    # ZAI configuration (Tier 1 - DEFAULT)
    zai_api_key: Optional[str] = None
    zai_model: str = "glm-4.7"
    zai_use_coding_endpoint: bool = True

    # OpenRouter configuration (Tier 2 - PREMIUM)
    openrouter_api_key: Optional[str] = None
    openrouter_model: str = "anthropic/claude-3-5-sonnet-20241022"

    # Anthropic configuration (Tier 3 - EXTENDED)
    anthropic_api_key: Optional[str] = None
    anthropic_model: str = "claude-3-opus-20240229"

    # Cache configuration
    enable_cache: bool = True
    cache_ttl: float = 3600.0
    cache_max_entries: int = 1000

    # Rate limiting
    rate_limit_interval: float = 10.0

    # Request timeout
    timeout: float = 120.0

    # Retry settings
    max_retries: int = 3
    retry_delay: float = 5.0

    @classmethod
    def from_env(cls) -> "TierProviderConfig":
        """Create config from environment variables."""
        return cls(
            zai_api_key=os.environ.get("ZAI_API_KEY"),
            openrouter_api_key=os.environ.get("OPENROUTER_API_KEY"),
            anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY")
        )


@dataclass
class TierCallResult:
    """Result from a tier call."""
    success: bool
    tier: CognitiveTier
    text: str
    raw: Dict[str, Any] = field(default_factory=dict)
    model: str = ""
    provider: str = ""
    latency_ms: float = 0.0
    cached: bool = False
    error: Optional[str] = None


class TierProvider:
    """
    Tier-aware LLM provider.

    Manages LLM clients per cognitive tier and routes requests
    to appropriate providers.

    Usage:
        provider = TierProvider.create_from_env()

        # Call default tier (GLM 4.7)
        result = await provider.call(
            tier=CognitiveTier.GLM_4_7,
            prompt="Analyze this code",
            max_tokens=2000
        )

        # Call premium tier
        result = await provider.call(
            tier=CognitiveTier.PREMIUM,
            prompt="Complex reasoning task",
            max_tokens=4000
        )
    """

    def __init__(
        self,
        config: TierProviderConfig = None,
        registry: Optional[ProviderRegistry] = None
    ):
        """
        Initialize tier provider.

        Args:
            config: Provider configuration
            registry: Optional provider registry for health tracking
        """
        self.config = config or TierProviderConfig.from_env()
        self._registry = registry or ProviderRegistry()

        # LLM clients per tier (lazy initialized)
        self._clients: Dict[CognitiveTier, Any] = {}

        # Statistics
        self._call_counts: Dict[CognitiveTier, int] = {t: 0 for t in CognitiveTier}
        self._success_counts: Dict[CognitiveTier, int] = {t: 0 for t in CognitiveTier}
        self._total_cost = 0.0

        # Initialize tier clients
        self._init_clients()

    def _init_clients(self) -> None:
        """Initialize LLM clients for each tier."""
        # Import here to avoid circular imports
        try:
            from core.llm_client import ZAIClient, OpenRouterClient, LLMError
            self._LLMError = LLMError
        except ImportError:
            logger.warning("Could not import LLM clients from core.llm_client")
            return

        # Tier 1: GLM 4.7 (ZAI) - ALWAYS available
        if self.config.zai_api_key:
            try:
                self._clients[CognitiveTier.GLM_4_7] = ZAIClient(
                    model=self.config.zai_model,
                    api_key=self.config.zai_api_key,
                    timeout=self.config.timeout,
                    use_coding_endpoint=self.config.zai_use_coding_endpoint,
                    enable_cache=self.config.enable_cache,
                    cache_ttl=self.config.cache_ttl,
                    cache_max_entries=self.config.cache_max_entries
                )
                logger.info(f"Initialized GLM 4.7 client (Tier 1)")
            except Exception as e:
                logger.error(f"Failed to initialize GLM 4.7 client: {e}")

        # Tier 2: Premium (OpenRouter)
        if self.config.openrouter_api_key:
            try:
                self._clients[CognitiveTier.PREMIUM] = OpenRouterClient(
                    model=self.config.openrouter_model,
                    api_key=self.config.openrouter_api_key,
                    timeout=self.config.timeout,
                    enable_cache=self.config.enable_cache,
                    cache_ttl=self.config.cache_ttl,
                    cache_max_entries=self.config.cache_max_entries
                )
                logger.info(f"Initialized Premium client (Tier 2)")
            except Exception as e:
                logger.error(f"Failed to initialize Premium client: {e}")

        # Tier 3: Extended (Anthropic direct) - uses OpenRouter for now
        # TODO: Add direct Anthropic client for extended thinking
        if CognitiveTier.PREMIUM in self._clients:
            self._clients[CognitiveTier.EXTENDED] = self._clients[CognitiveTier.PREMIUM]

        # Tier 4: Custom - not yet implemented
        # Will use fine-tuned models via training pipeline

    def get_client(self, tier: CognitiveTier) -> Optional[Any]:
        """Get LLM client for a tier."""
        return self._clients.get(tier)

    def is_tier_available(self, tier: CognitiveTier) -> bool:
        """Check if a tier is available."""
        if tier == CognitiveTier.REFLEX:
            return True  # Reflex is always available (no LLM)
        return tier in self._clients

    def get_available_tiers(self) -> List[CognitiveTier]:
        """Get list of available tiers."""
        available = [CognitiveTier.REFLEX]  # Reflex always available
        available.extend(self._clients.keys())
        return sorted(available, key=lambda t: t.value)

    async def call(
        self,
        tier: CognitiveTier,
        prompt: str,
        max_tokens: int = 2000,
        temperature: float = 0.7,
        system_message: Optional[str] = None,
        quantum_modulation: bool = False,
        quantum_context: str = "unknown",
        **kwargs
    ) -> TierCallResult:
        """
        Make an LLM call on the specified tier.

        Args:
            tier: Cognitive tier to use
            prompt: The prompt to send
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            system_message: Optional system message
            quantum_modulation: Enable quantum temperature modulation
            quantum_context: Context for quantum tracking
            **kwargs: Additional provider-specific arguments

        Returns:
            TierCallResult with response or error
        """
        import time
        start_time = time.time()

        # Handle reflex tier (no LLM)
        if tier == CognitiveTier.REFLEX:
            # Reflex tier uses cache or pattern matching, not LLM
            return TierCallResult(
                success=False,
                tier=tier,
                text="",
                error="REFLEX tier requires cache hit - no LLM call"
            )

        # Check tier availability
        if tier not in self._clients:
            # Fall back to GLM 4.7 if requested tier unavailable
            if CognitiveTier.GLM_4_7 in self._clients:
                logger.warning(
                    f"Tier {tier.name} unavailable, falling back to GLM 4.7"
                )
                tier = CognitiveTier.GLM_4_7
            else:
                return TierCallResult(
                    success=False,
                    tier=tier,
                    text="",
                    error=f"Tier {tier.name} not available and no fallback"
                )

        client = self._clients[tier]
        self._call_counts[tier] += 1

        try:
            response = await client.generate(
                prompt=prompt,
                temperature=temperature,
                max_tokens=max_tokens,
                system_message=system_message,
                quantum_modulation=quantum_modulation,
                quantum_context=quantum_context,
                **kwargs
            )

            latency_ms = (time.time() - start_time) * 1000

            # Update success count
            self._success_counts[tier] += 1

            # Update registry health
            provider_id = self._get_provider_id_for_tier(tier)
            if provider_id:
                self._registry.record_request(
                    provider_id=provider_id,
                    success=True,
                    latency_ms=latency_ms
                )

            # Check if cached
            cached = response.raw.get('cached', False) if response.raw else False

            return TierCallResult(
                success=True,
                tier=tier,
                text=response.text,
                raw=response.raw,
                model=response.model,
                provider=response.provider,
                latency_ms=latency_ms,
                cached=cached
            )

        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000

            # Update registry health
            provider_id = self._get_provider_id_for_tier(tier)
            if provider_id:
                self._registry.record_request(
                    provider_id=provider_id,
                    success=False,
                    latency_ms=latency_ms
                )
                self._registry.update_health(
                    provider_id=provider_id,
                    status=ProviderStatus.DEGRADED,
                    error=str(e)
                )

            logger.error(f"Tier {tier.name} call failed: {e}")

            return TierCallResult(
                success=False,
                tier=tier,
                text="",
                latency_ms=latency_ms,
                error=str(e)
            )

    def _get_provider_id_for_tier(self, tier: CognitiveTier) -> Optional[str]:
        """Map tier to provider ID for registry."""
        mapping = {
            CognitiveTier.GLM_4_7: "zai",
            CognitiveTier.PREMIUM: "openrouter",
            CognitiveTier.EXTENDED: "anthropic"
        }
        return mapping.get(tier)

    def get_llm_call_fn(self):
        """
        Get a callback function for CognitiveRouter.

        Returns:
            Async function (tier, prompt, kwargs) -> Dict
        """
        async def llm_call_fn(
            tier: CognitiveTier,
            prompt: str,
            kwargs: Dict[str, Any]
        ) -> Dict[str, Any]:
            result = await self.call(
                tier=tier,
                prompt=prompt,
                **kwargs
            )
            return {
                'text': result.text,
                'raw': result.raw,
                'model': result.model,
                'provider': result.provider,
                'cached': result.cached,
                'error': result.error
            }

        return llm_call_fn

    def get_stats(self) -> Dict[str, Any]:
        """Get provider statistics."""
        return {
            'available_tiers': [t.name for t in self.get_available_tiers()],
            'call_counts': {t.name: c for t, c in self._call_counts.items() if c > 0},
            'success_counts': {t.name: c for t, c in self._success_counts.items() if c > 0},
            'success_rates': {
                t.name: self._success_counts[t] / self._call_counts[t]
                for t in self._call_counts
                if self._call_counts[t] > 0
            },
            'total_cost': self._total_cost,
            'registry_stats': self._registry.get_stats()
        }


def create_tier_provider(
    config: TierProviderConfig = None
) -> TierProvider:
    """
    Factory function to create a tier provider.

    Args:
        config: Optional configuration (uses env vars if not provided)

    Returns:
        Configured TierProvider
    """
    return TierProvider(config or TierProviderConfig.from_env())
