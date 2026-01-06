"""
Provider Registry.

Registry of available LLM providers with capability tracking.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 2.3 for specification.
"""

from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
import logging

logger = logging.getLogger("rsi.substrate.provider_registry")


class ProviderType(Enum):
    """Types of LLM providers."""
    CLOUD_API = "cloud_api"
    LOCAL_INFERENCE = "local_inference"
    SELF_HOSTED = "self_hosted"
    HYBRID = "hybrid"


class ProviderStatus(Enum):
    """Provider availability status."""
    AVAILABLE = "available"
    DEGRADED = "degraded"
    UNAVAILABLE = "unavailable"
    RATE_LIMITED = "rate_limited"
    UNKNOWN = "unknown"


@dataclass
class ProviderCapabilities:
    """Capabilities of an LLM provider."""
    max_context_length: int = 4096
    max_output_tokens: int = 2048
    supports_streaming: bool = False
    supports_function_calling: bool = False
    supports_vision: bool = False
    supports_embedding: bool = False
    supported_models: List[str] = field(default_factory=list)


@dataclass
class ProviderConfig:
    """Configuration for an LLM provider."""
    id: str
    name: str
    provider_type: ProviderType
    endpoint: str
    api_key_env: Optional[str] = None  # Environment variable for API key
    capabilities: ProviderCapabilities = field(default_factory=ProviderCapabilities)
    priority: int = 100  # Lower = higher priority
    cost_per_1k_input: float = 0.0
    cost_per_1k_output: float = 0.0
    rate_limit_rpm: Optional[int] = None
    rate_limit_tpm: Optional[int] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProviderHealth:
    """Health status of a provider."""
    provider_id: str
    status: ProviderStatus
    last_check: str
    latency_ms: Optional[float] = None
    error_rate: float = 0.0
    rate_limit_remaining: Optional[int] = None
    last_error: Optional[str] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'provider_id': self.provider_id,
            'status': self.status.value,
            'last_check': self.last_check,
            'latency_ms': self.latency_ms,
            'error_rate': self.error_rate,
            'rate_limit_remaining': self.rate_limit_remaining,
            'last_error': self.last_error
        }


class ProviderRegistry:
    """
    Registry of available LLM providers.

    Manages provider registration, health tracking, and selection.
    """

    def __init__(self, config: Dict = None):
        """
        Initialize provider registry.

        Args:
            config: Configuration options
        """
        self.config = config or {}

        # Registered providers
        self._providers: Dict[str, ProviderConfig] = {}

        # Provider health status
        self._health: Dict[str, ProviderHealth] = {}

        # Request/success tracking per provider
        self._request_counts: Dict[str, int] = {}
        self._success_counts: Dict[str, int] = {}

        # Tags for filtering
        self._provider_tags: Dict[str, Set[str]] = {}

        # Register default providers
        self._register_default_providers()

    def _register_default_providers(self) -> None:
        """Register default provider configurations."""
        # ZAI (GLM-4.7)
        self.register_provider(ProviderConfig(
            id="zai",
            name="Z.AI",
            provider_type=ProviderType.CLOUD_API,
            endpoint="https://open.bigmodel.cn/api/paas/v4/chat/completions",
            api_key_env="ZAI_API_KEY",
            capabilities=ProviderCapabilities(
                max_context_length=128000,
                max_output_tokens=4096,
                supports_streaming=True,
                supports_function_calling=True,
                supported_models=["glm-4.7", "glm-4"]
            ),
            priority=10,
            cost_per_1k_input=0.001,
            cost_per_1k_output=0.002,
            rate_limit_rpm=60
        ))

        # OpenRouter
        self.register_provider(ProviderConfig(
            id="openrouter",
            name="OpenRouter",
            provider_type=ProviderType.CLOUD_API,
            endpoint="https://openrouter.ai/api/v1/chat/completions",
            api_key_env="OPENROUTER_API_KEY",
            capabilities=ProviderCapabilities(
                max_context_length=200000,
                max_output_tokens=8192,
                supports_streaming=True,
                supports_function_calling=True,
                supports_vision=True,
                supported_models=[
                    "anthropic/claude-3-opus",
                    "anthropic/claude-3-sonnet",
                    "deepseek/deepseek-v3.2-speciale"
                ]
            ),
            priority=20,
            cost_per_1k_input=0.003,
            cost_per_1k_output=0.015
        ))

        # Ollama (local)
        self.register_provider(ProviderConfig(
            id="ollama",
            name="Ollama",
            provider_type=ProviderType.LOCAL_INFERENCE,
            endpoint="http://localhost:11434/api/generate",
            capabilities=ProviderCapabilities(
                max_context_length=32000,
                max_output_tokens=4096,
                supports_streaming=True,
                supported_models=["gemma2:27b", "llama3:70b", "mixtral"]
            ),
            priority=5,  # Prefer local when available
            cost_per_1k_input=0.0,  # Free (local)
            cost_per_1k_output=0.0
        ))

        # Anthropic
        self.register_provider(ProviderConfig(
            id="anthropic",
            name="Anthropic",
            provider_type=ProviderType.CLOUD_API,
            endpoint="https://api.anthropic.com/v1/messages",
            api_key_env="ANTHROPIC_API_KEY",
            capabilities=ProviderCapabilities(
                max_context_length=200000,
                max_output_tokens=8192,
                supports_streaming=True,
                supports_function_calling=True,
                supports_vision=True,
                supported_models=["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"]
            ),
            priority=30,
            cost_per_1k_input=0.015,
            cost_per_1k_output=0.075,
            rate_limit_rpm=50
        ))

    def register_provider(
        self,
        provider_config: ProviderConfig,
        tags: Set[str] = None
    ) -> None:
        """
        Register a provider.

        Args:
            provider_config: Provider configuration
            tags: Optional tags for filtering
        """
        self._providers[provider_config.id] = provider_config
        self._health[provider_config.id] = ProviderHealth(
            provider_id=provider_config.id,
            status=ProviderStatus.UNKNOWN,
            last_check=datetime.now(timezone.utc).isoformat()
        )
        self._request_counts[provider_config.id] = 0
        self._success_counts[provider_config.id] = 0
        self._provider_tags[provider_config.id] = tags or set()

        logger.info(f"Registered provider: {provider_config.id}")

    def unregister_provider(self, provider_id: str) -> bool:
        """
        Unregister a provider.

        Args:
            provider_id: Provider ID to remove

        Returns:
            True if removed, False if not found
        """
        if provider_id not in self._providers:
            return False

        del self._providers[provider_id]
        self._health.pop(provider_id, None)
        self._request_counts.pop(provider_id, None)
        self._success_counts.pop(provider_id, None)
        self._provider_tags.pop(provider_id, None)

        logger.info(f"Unregistered provider: {provider_id}")
        return True

    def get_provider(self, provider_id: str) -> Optional[ProviderConfig]:
        """Get provider configuration by ID."""
        return self._providers.get(provider_id)

    def list_providers(
        self,
        provider_type: ProviderType = None,
        status: ProviderStatus = None,
        tags: Set[str] = None
    ) -> List[ProviderConfig]:
        """
        List providers with optional filtering.

        Args:
            provider_type: Filter by provider type
            status: Filter by status
            tags: Filter by tags (must have all)

        Returns:
            List of matching provider configs
        """
        providers = list(self._providers.values())

        # Filter by type
        if provider_type:
            providers = [p for p in providers if p.provider_type == provider_type]

        # Filter by status
        if status:
            providers = [
                p for p in providers
                if self._health.get(p.id, ProviderHealth(
                    provider_id=p.id,
                    status=ProviderStatus.UNKNOWN,
                    last_check=""
                )).status == status
            ]

        # Filter by tags
        if tags:
            providers = [
                p for p in providers
                if tags.issubset(self._provider_tags.get(p.id, set()))
            ]

        return providers

    def get_available_providers(
        self,
        required_capability: str = None,
        min_context_length: int = None,
        model: str = None
    ) -> List[ProviderConfig]:
        """
        Get available providers matching requirements.

        Args:
            required_capability: Required capability
            min_context_length: Minimum context length
            model: Specific model support required

        Returns:
            List of matching available providers, sorted by priority
        """
        available = []

        for provider in self._providers.values():
            health = self._health.get(provider.id)

            # Skip unavailable
            if health and health.status == ProviderStatus.UNAVAILABLE:
                continue

            # Check context length
            if min_context_length:
                if provider.capabilities.max_context_length < min_context_length:
                    continue

            # Check capability
            if required_capability:
                cap = provider.capabilities
                cap_map = {
                    'streaming': cap.supports_streaming,
                    'function_calling': cap.supports_function_calling,
                    'vision': cap.supports_vision,
                    'embedding': cap.supports_embedding
                }
                if not cap_map.get(required_capability, False):
                    continue

            # Check model support
            if model:
                if model not in provider.capabilities.supported_models:
                    continue

            available.append(provider)

        # Sort by priority (lower = better)
        return sorted(available, key=lambda p: p.priority)

    def update_health(
        self,
        provider_id: str,
        status: ProviderStatus,
        latency_ms: float = None,
        error: str = None
    ) -> None:
        """
        Update provider health status.

        Args:
            provider_id: Provider ID
            status: New status
            latency_ms: Request latency
            error: Error message if any
        """
        if provider_id not in self._providers:
            logger.warning(f"Cannot update health for unknown provider: {provider_id}")
            return

        health = self._health.get(provider_id)
        if health:
            health.status = status
            health.last_check = datetime.now(timezone.utc).isoformat()
            health.latency_ms = latency_ms
            if error:
                health.last_error = error

        logger.debug(f"Updated health for {provider_id}: {status.value}")

    def record_request(
        self,
        provider_id: str,
        success: bool,
        latency_ms: float = None
    ) -> None:
        """
        Record a request for tracking.

        Args:
            provider_id: Provider ID
            success: Whether request succeeded
            latency_ms: Request latency
        """
        if provider_id not in self._providers:
            return

        self._request_counts[provider_id] = (
            self._request_counts.get(provider_id, 0) + 1
        )

        if success:
            self._success_counts[provider_id] = (
                self._success_counts.get(provider_id, 0) + 1
            )

        # Update error rate in health
        health = self._health.get(provider_id)
        if health:
            total = self._request_counts[provider_id]
            successes = self._success_counts[provider_id]
            health.error_rate = 1.0 - (successes / total) if total > 0 else 0.0

            if latency_ms:
                health.latency_ms = latency_ms

            # Update status based on error rate
            if health.error_rate > 0.5:
                health.status = ProviderStatus.DEGRADED
            elif health.error_rate > 0.9:
                health.status = ProviderStatus.UNAVAILABLE
            elif success:
                health.status = ProviderStatus.AVAILABLE

    def get_health(self, provider_id: str) -> Optional[ProviderHealth]:
        """Get health status for a provider."""
        return self._health.get(provider_id)

    def get_all_health(self) -> Dict[str, ProviderHealth]:
        """Get health status for all providers."""
        return self._health.copy()

    def get_cheapest_provider(
        self,
        input_tokens: int = 1000,
        output_tokens: int = 1000,
        required_capability: str = None
    ) -> Optional[ProviderConfig]:
        """
        Get the cheapest available provider.

        Args:
            input_tokens: Expected input tokens
            output_tokens: Expected output tokens
            required_capability: Required capability

        Returns:
            Cheapest available provider or None
        """
        available = self.get_available_providers(
            required_capability=required_capability
        )

        if not available:
            return None

        def total_cost(p: ProviderConfig) -> float:
            return (
                (input_tokens / 1000) * p.cost_per_1k_input +
                (output_tokens / 1000) * p.cost_per_1k_output
            )

        return min(available, key=total_cost)

    def get_fastest_provider(
        self,
        required_capability: str = None
    ) -> Optional[ProviderConfig]:
        """
        Get the fastest available provider based on latency.

        Args:
            required_capability: Required capability

        Returns:
            Fastest available provider or None
        """
        available = self.get_available_providers(
            required_capability=required_capability
        )

        if not available:
            return None

        def latency(p: ProviderConfig) -> float:
            health = self._health.get(p.id)
            if health and health.latency_ms:
                return health.latency_ms
            return float('inf')

        return min(available, key=latency)

    def estimate_cost(
        self,
        provider_id: str,
        input_tokens: int,
        output_tokens: int
    ) -> Optional[float]:
        """
        Estimate cost for a request.

        Args:
            provider_id: Provider ID
            input_tokens: Number of input tokens
            output_tokens: Expected output tokens

        Returns:
            Estimated cost in dollars or None
        """
        provider = self.get_provider(provider_id)
        if not provider:
            return None

        return (
            (input_tokens / 1000) * provider.cost_per_1k_input +
            (output_tokens / 1000) * provider.cost_per_1k_output
        )

    def get_stats(self) -> Dict:
        """Get registry statistics."""
        total_requests = sum(self._request_counts.values())
        total_successes = sum(self._success_counts.values())

        return {
            'total_providers': len(self._providers),
            'providers_by_type': {
                t.value: len([p for p in self._providers.values() if p.provider_type == t])
                for t in ProviderType
            },
            'providers_by_status': {
                s.value: len([
                    p for p in self._providers.values()
                    if self._health.get(p.id, ProviderHealth(
                        provider_id=p.id,
                        status=ProviderStatus.UNKNOWN,
                        last_check=""
                    )).status == s
                ])
                for s in ProviderStatus
            },
            'total_requests': total_requests,
            'total_successes': total_successes,
            'overall_success_rate': (
                total_successes / total_requests if total_requests > 0 else 0.0
            )
        }

    def reset(self) -> None:
        """Reset registry state (keeps providers, clears stats)."""
        for provider_id in self._providers:
            self._health[provider_id] = ProviderHealth(
                provider_id=provider_id,
                status=ProviderStatus.UNKNOWN,
                last_check=datetime.now(timezone.utc).isoformat()
            )
            self._request_counts[provider_id] = 0
            self._success_counts[provider_id] = 0

        logger.info("ProviderRegistry reset")
