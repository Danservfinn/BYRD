"""
Compute Abstraction Layer.

Unified interface for compute regardless of provider.
Enables multi-provider failover and eventual self-hosting.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 2.3 for specification.
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from datetime import datetime, timezone
import logging
import os
import time

from .provider_registry import (
    ProviderRegistry,
    ProviderConfig,
    ProviderType,
    ProviderStatus
)
from .failover_manager import FailoverManager, FailoverResult

logger = logging.getLogger("rsi.substrate.compute_abstraction")


class SubstrateLevel(IntEnum):
    """
    Levels of substrate independence.

    Progression toward full autonomy over compute infrastructure.
    """
    FULL_DEPENDENCY = 0      # Single external provider
    PROVIDER_ABSTRACTION = 1 # Unified interface (current)
    MULTI_PROVIDER = 2       # Failover between providers
    HYBRID_HOSTING = 3       # Mix of external and self-hosted
    SELF_HOSTED_TRAINING = 4 # Full self-hosting with training


@dataclass
class GenerationConfig:
    """Configuration for generation request."""
    model: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2048
    top_p: float = 1.0
    stop_sequences: List[str] = field(default_factory=list)
    stream: bool = False
    timeout_seconds: float = 60.0
    required_capability: Optional[str] = None
    preferred_provider: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GenerationResult:
    """Result of a generation request."""
    text: str
    provider_id: str
    model: str
    input_tokens: int
    output_tokens: int
    latency_ms: float
    cost_estimate: float
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'text': self.text,
            'provider_id': self.provider_id,
            'model': self.model,
            'input_tokens': self.input_tokens,
            'output_tokens': self.output_tokens,
            'latency_ms': self.latency_ms,
            'cost_estimate': self.cost_estimate,
            'metadata': self.metadata
        }


@dataclass
class CostEstimate:
    """Cost estimate for a request."""
    provider_id: str
    model: str
    input_tokens: int
    output_tokens: int
    input_cost: float
    output_cost: float
    total_cost: float

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'provider_id': self.provider_id,
            'model': self.model,
            'input_tokens': self.input_tokens,
            'output_tokens': self.output_tokens,
            'input_cost': self.input_cost,
            'output_cost': self.output_cost,
            'total_cost': self.total_cost
        }


@dataclass
class SubstrateLevelInfo:
    """Information about a substrate level."""
    level: SubstrateLevel
    name: str
    description: str
    requirements: List[str]
    capabilities: List[str]


SUBSTRATE_LEVELS = {
    SubstrateLevel.FULL_DEPENDENCY: SubstrateLevelInfo(
        level=SubstrateLevel.FULL_DEPENDENCY,
        name="Full Dependency",
        description="Single external provider, no failover",
        requirements=[],
        capabilities=["basic_generation"]
    ),
    SubstrateLevel.PROVIDER_ABSTRACTION: SubstrateLevelInfo(
        level=SubstrateLevel.PROVIDER_ABSTRACTION,
        name="Provider Abstraction",
        description="Unified interface with provider registry",
        requirements=["provider_registry"],
        capabilities=["basic_generation", "provider_selection", "cost_estimation"]
    ),
    SubstrateLevel.MULTI_PROVIDER: SubstrateLevelInfo(
        level=SubstrateLevel.MULTI_PROVIDER,
        name="Multi-Provider",
        description="Automatic failover between providers",
        requirements=["provider_registry", "failover_manager", "multiple_providers"],
        capabilities=["basic_generation", "provider_selection", "cost_estimation",
                     "automatic_failover", "circuit_breaking"]
    ),
    SubstrateLevel.HYBRID_HOSTING: SubstrateLevelInfo(
        level=SubstrateLevel.HYBRID_HOSTING,
        name="Hybrid Hosting",
        description="Mix of external and self-hosted inference",
        requirements=["local_inference", "model_management"],
        capabilities=["basic_generation", "provider_selection", "cost_estimation",
                     "automatic_failover", "circuit_breaking", "local_inference"]
    ),
    SubstrateLevel.SELF_HOSTED_TRAINING: SubstrateLevelInfo(
        level=SubstrateLevel.SELF_HOSTED_TRAINING,
        name="Self-Hosted Training",
        description="Full control over model training and hosting",
        requirements=["compute_cluster", "training_pipeline", "model_deployment"],
        capabilities=["basic_generation", "provider_selection", "cost_estimation",
                     "automatic_failover", "circuit_breaking", "local_inference",
                     "fine_tuning", "custom_models"]
    )
}


class ComputeAbstractionLayer:
    """
    Unified interface for compute regardless of provider.

    Enables multi-provider failover and eventual self-hosting.
    Implements progressive substrate independence levels.
    """

    def __init__(
        self,
        provider_registry: ProviderRegistry = None,
        config: Dict = None
    ):
        """
        Initialize compute abstraction layer.

        Args:
            provider_registry: Provider registry (created if None)
            config: Configuration options
        """
        self.config = config or {}

        # Provider registry
        self.registry = provider_registry or ProviderRegistry(config)

        # Failover manager
        self.failover = FailoverManager(self.registry, config)

        # Current substrate level
        self._current_level = SubstrateLevel.PROVIDER_ABSTRACTION

        # Update level based on available providers
        self._update_substrate_level()

        # Statistics
        self._total_requests: int = 0
        self._total_tokens_in: int = 0
        self._total_tokens_out: int = 0
        self._total_cost: float = 0.0

    @property
    def current_level(self) -> SubstrateLevel:
        """Get current substrate level."""
        return self._current_level

    def _update_substrate_level(self) -> None:
        """Update substrate level based on available capabilities."""
        available = self.registry.get_available_providers()

        # Check for local inference
        has_local = any(
            p.provider_type == ProviderType.LOCAL_INFERENCE
            for p in available
        )

        # Check for multiple providers
        has_multiple = len(available) >= 2

        if has_local and has_multiple:
            self._current_level = SubstrateLevel.HYBRID_HOSTING
        elif has_multiple:
            self._current_level = SubstrateLevel.MULTI_PROVIDER
        elif available:
            self._current_level = SubstrateLevel.PROVIDER_ABSTRACTION
        else:
            self._current_level = SubstrateLevel.FULL_DEPENDENCY

    async def generate(
        self,
        prompt: str,
        config: GenerationConfig = None
    ) -> GenerationResult:
        """
        Generate text with automatic failover.

        Args:
            prompt: The prompt to generate from
            config: Generation configuration

        Returns:
            GenerationResult with output and metadata
        """
        config = config or GenerationConfig()
        self._total_requests += 1
        start_time = time.time()

        # Define generation function for failover
        async def do_generate(provider: ProviderConfig) -> GenerationResult:
            # This is a mock implementation
            # In reality, this would call the actual provider API
            return await self._generate_with_provider(prompt, config, provider)

        # Execute with failover
        result = await self.failover.execute_with_failover(
            do_generate,
            required_capability=config.required_capability,
            model=config.model
        )

        if not result.success:
            raise RuntimeError(f"Generation failed: {result.error}")

        gen_result = result.result

        # Track stats
        self._total_tokens_in += gen_result.input_tokens
        self._total_tokens_out += gen_result.output_tokens
        self._total_cost += gen_result.cost_estimate

        return gen_result

    async def _generate_with_provider(
        self,
        prompt: str,
        config: GenerationConfig,
        provider: ProviderConfig
    ) -> GenerationResult:
        """
        Generate with a specific provider.

        This is a stub implementation. Real implementation would
        call the actual provider APIs.
        """
        start_time = time.time()

        # Estimate tokens (rough approximation)
        input_tokens = len(prompt.split()) * 1.3
        output_tokens = config.max_tokens // 2  # Estimate half of max

        # Check for API key
        if provider.api_key_env:
            api_key = os.environ.get(provider.api_key_env)
            if not api_key:
                raise RuntimeError(
                    f"API key not found for {provider.id}: "
                    f"set {provider.api_key_env}"
                )

        # Mock generation - in real impl, call provider API
        # This allows testing without actual API calls
        generated_text = f"[Generated by {provider.id}] Response to: {prompt[:50]}..."

        latency = (time.time() - start_time) * 1000

        cost = self.registry.estimate_cost(
            provider.id,
            int(input_tokens),
            int(output_tokens)
        ) or 0.0

        return GenerationResult(
            text=generated_text,
            provider_id=provider.id,
            model=config.model or provider.capabilities.supported_models[0],
            input_tokens=int(input_tokens),
            output_tokens=int(output_tokens),
            latency_ms=latency,
            cost_estimate=cost,
            metadata={
                'provider_type': provider.provider_type.value,
                'endpoint': provider.endpoint
            }
        )

    async def estimate_cost(
        self,
        prompt: str,
        config: GenerationConfig = None
    ) -> List[CostEstimate]:
        """
        Estimate cost across providers.

        Args:
            prompt: The prompt
            config: Generation config

        Returns:
            List of cost estimates per provider
        """
        config = config or GenerationConfig()
        estimates = []

        # Estimate tokens
        input_tokens = int(len(prompt.split()) * 1.3)
        output_tokens = config.max_tokens

        # Get available providers
        providers = self.registry.get_available_providers(
            required_capability=config.required_capability,
            model=config.model
        )

        for provider in providers:
            input_cost = (input_tokens / 1000) * provider.cost_per_1k_input
            output_cost = (output_tokens / 1000) * provider.cost_per_1k_output

            estimates.append(CostEstimate(
                provider_id=provider.id,
                model=config.model or (
                    provider.capabilities.supported_models[0]
                    if provider.capabilities.supported_models else "default"
                ),
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                input_cost=input_cost,
                output_cost=output_cost,
                total_cost=input_cost + output_cost
            ))

        return sorted(estimates, key=lambda e: e.total_cost)

    async def get_cheapest_provider(
        self,
        prompt: str,
        config: GenerationConfig = None
    ) -> Optional[ProviderConfig]:
        """
        Get the cheapest provider for a request.

        Args:
            prompt: The prompt
            config: Generation config

        Returns:
            Cheapest provider or None
        """
        estimates = await self.estimate_cost(prompt, config)
        if not estimates:
            return None

        cheapest = estimates[0]
        return self.registry.get_provider(cheapest.provider_id)

    def get_level_info(
        self,
        level: SubstrateLevel = None
    ) -> SubstrateLevelInfo:
        """Get information about a substrate level."""
        if level is None:
            level = self._current_level
        return SUBSTRATE_LEVELS.get(level)

    def get_all_levels_info(self) -> List[Dict]:
        """Get information about all substrate levels."""
        return [
            {
                'level': info.level.value,
                'name': info.name,
                'description': info.description,
                'requirements': info.requirements,
                'capabilities': info.capabilities,
                'is_current': info.level == self._current_level
            }
            for info in SUBSTRATE_LEVELS.values()
        ]

    def check_level_requirements(
        self,
        target_level: SubstrateLevel
    ) -> tuple[bool, List[str]]:
        """
        Check if requirements for a level are met.

        Args:
            target_level: Level to check

        Returns:
            Tuple of (all_met, unmet_requirements)
        """
        level_info = SUBSTRATE_LEVELS.get(target_level)
        if not level_info:
            return False, ["Unknown level"]

        unmet = []
        providers = self.registry.list_providers()

        for req in level_info.requirements:
            if req == "provider_registry":
                if not self.registry:
                    unmet.append(req)

            elif req == "failover_manager":
                if not self.failover:
                    unmet.append(req)

            elif req == "multiple_providers":
                available = self.registry.get_available_providers()
                if len(available) < 2:
                    unmet.append(req)

            elif req == "local_inference":
                has_local = any(
                    p.provider_type == ProviderType.LOCAL_INFERENCE
                    for p in providers
                )
                if not has_local:
                    unmet.append(req)

            elif req in ["compute_cluster", "training_pipeline", "model_deployment"]:
                # These are future capabilities
                unmet.append(req)

        return len(unmet) == 0, unmet

    def get_stats(self) -> Dict:
        """Get compute abstraction statistics."""
        registry_stats = self.registry.get_stats()
        failover_stats = self.failover.get_stats()

        return {
            'current_level': self._current_level.value,
            'current_level_name': SUBSTRATE_LEVELS[self._current_level].name,
            'total_requests': self._total_requests,
            'total_tokens_in': self._total_tokens_in,
            'total_tokens_out': self._total_tokens_out,
            'total_cost': self._total_cost,
            'registry': registry_stats,
            'failover': failover_stats
        }

    def reset(self) -> None:
        """Reset compute abstraction state."""
        self.registry.reset()
        self.failover.reset()
        self._total_requests = 0
        self._total_tokens_in = 0
        self._total_tokens_out = 0
        self._total_cost = 0.0
        self._update_substrate_level()
        logger.info("ComputeAbstractionLayer reset")
