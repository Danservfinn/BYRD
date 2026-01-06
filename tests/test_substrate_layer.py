"""
Tests for Substrate Independence Layer.

Tests provider registry, failover manager, and compute abstraction.
"""

import pytest
import asyncio
from datetime import datetime, timezone

from rsi.substrate import (
    # Provider Registry
    ProviderType,
    ProviderStatus,
    ProviderCapabilities,
    ProviderConfig,
    ProviderHealth,
    ProviderRegistry,
    # Failover Manager
    CircuitState,
    CircuitBreaker,
    FailoverResult,
    FailoverStrategy,
    FailoverManager,
    # Compute Abstraction
    SubstrateLevel,
    GenerationConfig,
    GenerationResult,
    CostEstimate,
    SUBSTRATE_LEVELS,
    ComputeAbstractionLayer,
    # Self-Hosted
    ModelFormat,
    InferenceBackend,
    LocalModelConfig,
    InferenceServer,
    SelfHostedManager,
)


# ============================================================================
# Provider Registry Tests
# ============================================================================

class TestProviderTypes:
    """Test provider type definitions."""

    def test_provider_type_enum(self):
        """Test ProviderType enum values."""
        assert ProviderType.CLOUD_API.value == "cloud_api"
        assert ProviderType.LOCAL_INFERENCE.value == "local_inference"
        assert ProviderType.SELF_HOSTED.value == "self_hosted"
        assert ProviderType.HYBRID.value == "hybrid"

    def test_provider_status_enum(self):
        """Test ProviderStatus enum values."""
        assert ProviderStatus.AVAILABLE.value == "available"
        assert ProviderStatus.DEGRADED.value == "degraded"
        assert ProviderStatus.UNAVAILABLE.value == "unavailable"
        assert ProviderStatus.RATE_LIMITED.value == "rate_limited"
        assert ProviderStatus.UNKNOWN.value == "unknown"


class TestProviderCapabilities:
    """Test ProviderCapabilities dataclass."""

    def test_default_capabilities(self):
        """Test default capability values."""
        caps = ProviderCapabilities()
        assert caps.max_context_length == 4096
        assert caps.max_output_tokens == 2048
        assert caps.supports_streaming is False
        assert caps.supports_function_calling is False
        assert caps.supports_vision is False
        assert caps.supported_models == []

    def test_custom_capabilities(self):
        """Test custom capability values."""
        caps = ProviderCapabilities(
            max_context_length=128000,
            max_output_tokens=8192,
            supports_streaming=True,
            supports_vision=True,
            supported_models=["gpt-4", "gpt-3.5"]
        )
        assert caps.max_context_length == 128000
        assert caps.supports_streaming is True
        assert "gpt-4" in caps.supported_models


class TestProviderConfig:
    """Test ProviderConfig dataclass."""

    def test_create_provider_config(self):
        """Test creating a provider config."""
        config = ProviderConfig(
            id="test-provider",
            name="Test Provider",
            provider_type=ProviderType.CLOUD_API,
            endpoint="https://api.test.com",
            api_key_env="TEST_API_KEY",
            priority=50
        )
        assert config.id == "test-provider"
        assert config.priority == 50
        assert config.cost_per_1k_input == 0.0


class TestProviderRegistry:
    """Test ProviderRegistry class."""

    @pytest.fixture
    def registry(self):
        """Create a fresh registry."""
        return ProviderRegistry({})

    def test_default_providers_registered(self, registry):
        """Test that default providers are registered."""
        providers = registry.list_providers()
        ids = [p.id for p in providers]
        assert "zai" in ids
        assert "openrouter" in ids
        assert "ollama" in ids
        assert "anthropic" in ids

    def test_register_custom_provider(self, registry):
        """Test registering a custom provider."""
        config = ProviderConfig(
            id="custom",
            name="Custom Provider",
            provider_type=ProviderType.CLOUD_API,
            endpoint="https://custom.api.com"
        )
        registry.register_provider(config)
        assert registry.get_provider("custom") is not None

    def test_unregister_provider(self, registry):
        """Test unregistering a provider."""
        assert registry.unregister_provider("zai") is True
        assert registry.get_provider("zai") is None
        assert registry.unregister_provider("nonexistent") is False

    def test_list_providers_by_type(self, registry):
        """Test filtering providers by type."""
        cloud_providers = registry.list_providers(
            provider_type=ProviderType.CLOUD_API
        )
        for p in cloud_providers:
            assert p.provider_type == ProviderType.CLOUD_API

    def test_get_available_providers(self, registry):
        """Test getting available providers."""
        available = registry.get_available_providers()
        # All should be available initially (status UNKNOWN)
        assert len(available) > 0

    def test_get_available_with_capability(self, registry):
        """Test filtering by capability."""
        streaming = registry.get_available_providers(
            required_capability="streaming"
        )
        for p in streaming:
            assert p.capabilities.supports_streaming is True

    def test_get_available_with_context_length(self, registry):
        """Test filtering by context length."""
        large_context = registry.get_available_providers(
            min_context_length=100000
        )
        for p in large_context:
            assert p.capabilities.max_context_length >= 100000

    def test_update_health(self, registry):
        """Test updating provider health."""
        registry.update_health(
            "zai",
            ProviderStatus.AVAILABLE,
            latency_ms=150.0
        )
        health = registry.get_health("zai")
        assert health.status == ProviderStatus.AVAILABLE
        assert health.latency_ms == 150.0

    def test_record_request(self, registry):
        """Test recording requests."""
        registry.record_request("zai", success=True, latency_ms=100)
        registry.record_request("zai", success=True, latency_ms=120)
        registry.record_request("zai", success=False)

        health = registry.get_health("zai")
        assert health.error_rate == pytest.approx(1/3, rel=0.01)

    def test_get_cheapest_provider(self, registry):
        """Test getting cheapest provider."""
        cheapest = registry.get_cheapest_provider(
            input_tokens=1000,
            output_tokens=1000
        )
        # Ollama is free, should be cheapest
        assert cheapest is not None
        assert cheapest.id == "ollama"

    def test_estimate_cost(self, registry):
        """Test cost estimation."""
        cost = registry.estimate_cost("zai", 1000, 500)
        assert cost is not None
        assert cost > 0

    def test_get_stats(self, registry):
        """Test getting registry stats."""
        stats = registry.get_stats()
        assert 'total_providers' in stats
        assert 'providers_by_type' in stats
        assert stats['total_providers'] >= 4

    def test_reset(self, registry):
        """Test registry reset."""
        registry.record_request("zai", success=True)
        registry.reset()
        health = registry.get_health("zai")
        assert health.status == ProviderStatus.UNKNOWN


# ============================================================================
# Failover Manager Tests
# ============================================================================

class TestCircuitBreaker:
    """Test CircuitBreaker class."""

    @pytest.fixture
    def breaker(self):
        """Create a circuit breaker."""
        return CircuitBreaker(
            provider_id="test",
            failure_threshold=3,
            success_threshold=2,
            reset_timeout_seconds=1.0
        )

    def test_initial_state(self, breaker):
        """Test initial circuit state."""
        assert breaker.state == CircuitState.CLOSED
        assert breaker.should_allow_request() is True

    def test_record_success(self, breaker):
        """Test recording successes."""
        breaker.record_success()
        assert breaker.success_count == 1
        assert breaker.failure_count == 0

    def test_record_failure(self, breaker):
        """Test recording failures."""
        breaker.record_failure()
        assert breaker.failure_count == 1
        assert breaker.state == CircuitState.CLOSED

    def test_open_after_threshold(self, breaker):
        """Test circuit opens after failure threshold."""
        for _ in range(3):
            breaker.record_failure()
        assert breaker.state == CircuitState.OPEN
        assert breaker.should_allow_request() is False

    def test_half_open_after_timeout(self, breaker):
        """Test circuit becomes half-open after timeout."""
        for _ in range(3):
            breaker.record_failure()
        assert breaker.state == CircuitState.OPEN

        # Wait for timeout
        import time
        time.sleep(1.1)

        # Should transition to half-open
        assert breaker.should_allow_request() is True
        assert breaker.state == CircuitState.HALF_OPEN

    def test_close_after_success_threshold(self, breaker):
        """Test circuit closes after success threshold in half-open."""
        for _ in range(3):
            breaker.record_failure()

        import time
        time.sleep(1.1)
        breaker.should_allow_request()  # Trigger half-open

        for _ in range(2):
            breaker.record_success()

        assert breaker.state == CircuitState.CLOSED

    def test_to_dict(self, breaker):
        """Test circuit breaker serialization."""
        data = breaker.to_dict()
        assert 'provider_id' in data
        assert 'state' in data
        assert data['state'] == 'closed'


class TestFailoverManager:
    """Test FailoverManager class."""

    @pytest.fixture
    def registry(self):
        """Create provider registry."""
        return ProviderRegistry({})

    @pytest.fixture
    def manager(self, registry):
        """Create failover manager."""
        return FailoverManager(registry, {'max_retries': 2})

    def test_get_circuit_breaker(self, manager):
        """Test getting/creating circuit breaker."""
        cb = manager.get_circuit_breaker("zai")
        assert cb is not None
        assert cb.provider_id == "zai"

        # Same breaker returned
        cb2 = manager.get_circuit_breaker("zai")
        assert cb is cb2

    @pytest.mark.asyncio
    async def test_execute_with_failover_success(self, manager):
        """Test successful execution."""
        async def mock_func(provider):
            return f"Success from {provider.id}"

        result = await manager.execute_with_failover(mock_func)
        assert result.success is True
        assert result.result is not None
        assert result.attempts >= 1

    @pytest.mark.asyncio
    async def test_execute_with_failover_failure(self, manager):
        """Test failover on failure."""
        call_count = 0

        async def failing_func(provider):
            nonlocal call_count
            call_count += 1
            raise RuntimeError("Provider failed")

        result = await manager.execute_with_failover(failing_func)
        assert result.success is False
        assert result.error is not None
        assert len(result.failover_path) > 0

    @pytest.mark.asyncio
    async def test_execute_with_failover_partial(self, manager):
        """Test failover succeeds after initial failure."""
        call_count = 0

        async def partial_func(provider):
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise RuntimeError("First call fails")
            return "Success on retry"

        result = await manager.execute_with_failover(partial_func)
        assert result.success is True
        assert result.attempts >= 2

    def test_reset_circuit_breaker(self, manager):
        """Test manual circuit breaker reset."""
        cb = manager.get_circuit_breaker("zai")
        for _ in range(5):
            cb.record_failure()
        assert cb.state == CircuitState.OPEN

        manager.reset_circuit_breaker("zai")
        cb = manager.get_circuit_breaker("zai")
        assert cb.state == CircuitState.CLOSED

    def test_get_circuit_states(self, manager):
        """Test getting all circuit states."""
        manager.get_circuit_breaker("zai")
        manager.get_circuit_breaker("openrouter")

        states = manager.get_circuit_states()
        assert "zai" in states
        assert "openrouter" in states

    def test_get_stats(self, manager):
        """Test getting manager stats."""
        stats = manager.get_stats()
        assert 'total_requests' in stats
        assert 'total_failovers' in stats
        assert 'strategy' in stats

    def test_reset(self, manager):
        """Test manager reset."""
        manager.get_circuit_breaker("zai")
        manager.reset()
        assert len(manager._circuit_breakers) == 0


# ============================================================================
# Compute Abstraction Tests
# ============================================================================

class TestSubstrateLevel:
    """Test SubstrateLevel definitions."""

    def test_substrate_levels(self):
        """Test substrate level enum."""
        assert SubstrateLevel.FULL_DEPENDENCY == 0
        assert SubstrateLevel.PROVIDER_ABSTRACTION == 1
        assert SubstrateLevel.MULTI_PROVIDER == 2
        assert SubstrateLevel.HYBRID_HOSTING == 3
        assert SubstrateLevel.SELF_HOSTED_TRAINING == 4

    def test_substrate_level_info(self):
        """Test substrate level info."""
        for level in SubstrateLevel:
            info = SUBSTRATE_LEVELS.get(level)
            assert info is not None
            assert info.name is not None
            assert info.description is not None


class TestGenerationConfig:
    """Test GenerationConfig dataclass."""

    def test_default_config(self):
        """Test default generation config."""
        config = GenerationConfig()
        assert config.temperature == 0.7
        assert config.max_tokens == 2048
        assert config.stream is False

    def test_custom_config(self):
        """Test custom generation config."""
        config = GenerationConfig(
            model="gpt-4",
            temperature=0.5,
            max_tokens=4096,
            stream=True
        )
        assert config.model == "gpt-4"
        assert config.temperature == 0.5


class TestComputeAbstractionLayer:
    """Test ComputeAbstractionLayer class."""

    @pytest.fixture
    def compute(self):
        """Create compute abstraction layer."""
        return ComputeAbstractionLayer({})

    def test_initialization(self, compute):
        """Test compute layer initialization."""
        assert compute.registry is not None
        assert compute.failover is not None
        assert compute.current_level >= SubstrateLevel.PROVIDER_ABSTRACTION

    def test_current_level(self, compute):
        """Test getting current substrate level."""
        level = compute.current_level
        assert level in SubstrateLevel

    def test_get_level_info(self, compute):
        """Test getting level info."""
        info = compute.get_level_info()
        assert info is not None
        assert info.level == compute.current_level

    def test_get_all_levels_info(self, compute):
        """Test getting all levels info."""
        levels = compute.get_all_levels_info()
        assert len(levels) == len(SubstrateLevel)
        # One should be current
        current_count = sum(1 for l in levels if l['is_current'])
        assert current_count == 1

    @pytest.mark.asyncio
    async def test_generate(self, compute):
        """Test generation (mock)."""
        result = await compute.generate(
            "Test prompt",
            GenerationConfig(max_tokens=100)
        )
        assert result.text is not None
        assert result.provider_id is not None
        assert result.latency_ms > 0

    @pytest.mark.asyncio
    async def test_estimate_cost(self, compute):
        """Test cost estimation."""
        estimates = await compute.estimate_cost(
            "Test prompt for cost estimation"
        )
        assert len(estimates) > 0
        # Should be sorted by cost
        costs = [e.total_cost for e in estimates]
        assert costs == sorted(costs)

    @pytest.mark.asyncio
    async def test_get_cheapest_provider(self, compute):
        """Test getting cheapest provider."""
        cheapest = await compute.get_cheapest_provider("Test prompt")
        assert cheapest is not None
        # Ollama is free
        assert cheapest.id == "ollama"

    def test_check_level_requirements(self, compute):
        """Test checking level requirements."""
        # Provider abstraction should be met
        met, unmet = compute.check_level_requirements(
            SubstrateLevel.PROVIDER_ABSTRACTION
        )
        assert met is True
        assert len(unmet) == 0

        # Self-hosted training won't be met
        met, unmet = compute.check_level_requirements(
            SubstrateLevel.SELF_HOSTED_TRAINING
        )
        assert met is False
        assert len(unmet) > 0

    def test_get_stats(self, compute):
        """Test getting compute stats."""
        stats = compute.get_stats()
        assert 'current_level' in stats
        assert 'total_requests' in stats
        assert 'registry' in stats
        assert 'failover' in stats

    def test_reset(self, compute):
        """Test compute layer reset."""
        compute._total_requests = 100
        compute.reset()
        assert compute._total_requests == 0


# ============================================================================
# Self-Hosted Tests (Stub)
# ============================================================================

class TestSelfHostedTypes:
    """Test self-hosted type definitions."""

    def test_model_format_enum(self):
        """Test ModelFormat enum."""
        assert ModelFormat.GGUF.value == "gguf"
        assert ModelFormat.SAFETENSORS.value == "safetensors"

    def test_inference_backend_enum(self):
        """Test InferenceBackend enum."""
        assert InferenceBackend.LLAMA_CPP.value == "llama_cpp"
        assert InferenceBackend.VLLM.value == "vllm"


class TestSelfHostedManager:
    """Test SelfHostedManager class."""

    @pytest.fixture
    def manager(self):
        """Create self-hosted manager."""
        return SelfHostedManager({})

    def test_initialization(self, manager):
        """Test manager initialization."""
        assert manager._models == {}
        assert manager._servers == {}

    @pytest.mark.asyncio
    async def test_download_model_stub(self, manager):
        """Test download model returns None (stub)."""
        result = await manager.download_model(
            "test-model",
            "https://huggingface.co/test"
        )
        assert result is None

    @pytest.mark.asyncio
    async def test_start_server_stub(self, manager):
        """Test start server returns None (stub)."""
        result = await manager.start_inference_server("test-model")
        assert result is None

    @pytest.mark.asyncio
    async def test_generate_stub(self, manager):
        """Test generate returns None (stub)."""
        result = await manager.generate("server-1", "Test prompt")
        assert result is None

    def test_list_models_empty(self, manager):
        """Test list models when empty."""
        models = manager.list_models()
        assert models == []

    def test_get_stats(self, manager):
        """Test getting manager stats."""
        stats = manager.get_stats()
        assert stats['implementation_status'] == 'stub'
        assert stats['models_count'] == 0

    def test_reset(self, manager):
        """Test manager reset."""
        manager._total_inferences = 10
        manager.reset()
        assert manager._total_inferences == 0


# ============================================================================
# Integration Tests
# ============================================================================

class TestSubstrateIntegration:
    """Integration tests for substrate layer."""

    @pytest.fixture
    def full_stack(self):
        """Create full substrate stack."""
        registry = ProviderRegistry({})
        failover = FailoverManager(registry, {})
        compute = ComputeAbstractionLayer(registry, {})
        return registry, failover, compute

    def test_registry_failover_integration(self, full_stack):
        """Test registry and failover integration."""
        registry, failover, _ = full_stack

        # Update registry health
        registry.update_health("zai", ProviderStatus.AVAILABLE)

        # Get circuit breaker
        cb = failover.get_circuit_breaker("zai")
        assert cb.state == CircuitState.CLOSED

    @pytest.mark.asyncio
    async def test_compute_uses_registry(self, full_stack):
        """Test compute layer uses registry."""
        registry, _, compute = full_stack

        # Mark all cloud providers unavailable
        for provider in registry.list_providers():
            if provider.provider_type == ProviderType.CLOUD_API:
                registry.update_health(
                    provider.id,
                    ProviderStatus.UNAVAILABLE
                )

        # Generate should still work via local
        result = await compute.generate("Test")
        assert result is not None

    def test_stats_aggregation(self, full_stack):
        """Test stats are properly aggregated."""
        registry, failover, compute = full_stack

        stats = compute.get_stats()

        # Should include nested stats
        assert 'registry' in stats
        assert 'failover' in stats
        assert stats['registry']['total_providers'] > 0
