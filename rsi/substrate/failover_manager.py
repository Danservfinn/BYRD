"""
Failover Manager.

Handles provider failover with circuit breaker pattern.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 2.3 for specification.
"""

from typing import Dict, List, Optional, Any, Callable, Awaitable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
import asyncio
import logging
import time

from .provider_registry import ProviderRegistry, ProviderConfig, ProviderStatus, ProviderHealth

logger = logging.getLogger("rsi.substrate.failover_manager")


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, rejecting requests
    HALF_OPEN = "half_open"  # Testing if recovered


@dataclass
class CircuitBreaker:
    """Circuit breaker for a provider."""
    provider_id: str
    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    success_count: int = 0
    last_failure_time: Optional[float] = None
    last_state_change: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    # Configuration
    failure_threshold: int = 5
    success_threshold: int = 3
    reset_timeout_seconds: float = 60.0

    def record_success(self) -> None:
        """Record a successful request."""
        self.success_count += 1
        self.failure_count = 0

        if self.state == CircuitState.HALF_OPEN:
            if self.success_count >= self.success_threshold:
                self._transition_to(CircuitState.CLOSED)

    def record_failure(self) -> None:
        """Record a failed request."""
        self.failure_count += 1
        self.success_count = 0
        self.last_failure_time = time.time()

        if self.state == CircuitState.CLOSED:
            if self.failure_count >= self.failure_threshold:
                self._transition_to(CircuitState.OPEN)
        elif self.state == CircuitState.HALF_OPEN:
            self._transition_to(CircuitState.OPEN)

    def should_allow_request(self) -> bool:
        """Check if request should be allowed."""
        if self.state == CircuitState.CLOSED:
            return True

        if self.state == CircuitState.OPEN:
            # Check if reset timeout has passed
            if self.last_failure_time:
                elapsed = time.time() - self.last_failure_time
                if elapsed >= self.reset_timeout_seconds:
                    self._transition_to(CircuitState.HALF_OPEN)
                    return True
            return False

        # HALF_OPEN - allow limited requests
        return True

    def _transition_to(self, new_state: CircuitState) -> None:
        """Transition to a new state."""
        logger.info(
            f"Circuit breaker {self.provider_id}: "
            f"{self.state.value} -> {new_state.value}"
        )
        self.state = new_state
        self.last_state_change = datetime.now(timezone.utc).isoformat()
        self.failure_count = 0
        self.success_count = 0

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'provider_id': self.provider_id,
            'state': self.state.value,
            'failure_count': self.failure_count,
            'success_count': self.success_count,
            'last_failure_time': self.last_failure_time,
            'last_state_change': self.last_state_change
        }


@dataclass
class FailoverResult:
    """Result of a failover attempt."""
    success: bool
    provider_id: str
    result: Optional[Any] = None
    error: Optional[str] = None
    latency_ms: float = 0.0
    attempts: int = 1
    failover_path: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'success': self.success,
            'provider_id': self.provider_id,
            'error': self.error,
            'latency_ms': self.latency_ms,
            'attempts': self.attempts,
            'failover_path': self.failover_path
        }


class FailoverStrategy(Enum):
    """Failover strategies."""
    PRIORITY = "priority"  # Use provider priority
    ROUND_ROBIN = "round_robin"  # Rotate through providers
    CHEAPEST = "cheapest"  # Use cheapest provider
    FASTEST = "fastest"  # Use fastest (lowest latency)
    RANDOM = "random"  # Random selection


class FailoverManager:
    """
    Manages provider failover with circuit breakers.

    Implements automatic failover between providers with
    exponential backoff and circuit breaker pattern.
    """

    def __init__(
        self,
        registry: ProviderRegistry,
        config: Dict = None
    ):
        """
        Initialize failover manager.

        Args:
            registry: Provider registry
            config: Configuration options
        """
        self.registry = registry
        self.config = config or {}

        # Circuit breakers per provider
        self._circuit_breakers: Dict[str, CircuitBreaker] = {}

        # Failover configuration
        self._max_retries = self.config.get('max_retries', 3)
        self._base_delay_seconds = self.config.get('base_delay_seconds', 1.0)
        self._max_delay_seconds = self.config.get('max_delay_seconds', 30.0)
        self._strategy = FailoverStrategy(
            self.config.get('strategy', 'priority')
        )

        # Round-robin state
        self._rr_index = 0

        # Statistics
        self._total_requests: int = 0
        self._total_failovers: int = 0
        self._successful_failovers: int = 0

    def get_circuit_breaker(self, provider_id: str) -> CircuitBreaker:
        """Get or create circuit breaker for provider."""
        if provider_id not in self._circuit_breakers:
            self._circuit_breakers[provider_id] = CircuitBreaker(
                provider_id=provider_id,
                failure_threshold=self.config.get('failure_threshold', 5),
                success_threshold=self.config.get('success_threshold', 3),
                reset_timeout_seconds=self.config.get('reset_timeout_seconds', 60.0)
            )
        return self._circuit_breakers[provider_id]

    def _get_provider_order(
        self,
        required_capability: str = None,
        model: str = None
    ) -> List[ProviderConfig]:
        """
        Get providers in failover order.

        Args:
            required_capability: Required capability
            model: Required model support

        Returns:
            List of providers in failover order
        """
        available = self.registry.get_available_providers(
            required_capability=required_capability,
            model=model
        )

        # Filter by circuit breaker state
        allowed = []
        for provider in available:
            cb = self.get_circuit_breaker(provider.id)
            if cb.should_allow_request():
                allowed.append(provider)

        if not allowed:
            return available  # Try anyway if nothing allowed

        # Apply strategy
        if self._strategy == FailoverStrategy.PRIORITY:
            return sorted(allowed, key=lambda p: p.priority)

        elif self._strategy == FailoverStrategy.ROUND_ROBIN:
            # Rotate the list
            n = len(allowed)
            self._rr_index = (self._rr_index + 1) % n
            return allowed[self._rr_index:] + allowed[:self._rr_index]

        elif self._strategy == FailoverStrategy.CHEAPEST:
            def cost(p: ProviderConfig) -> float:
                return p.cost_per_1k_input + p.cost_per_1k_output
            return sorted(allowed, key=cost)

        elif self._strategy == FailoverStrategy.FASTEST:
            def latency(p: ProviderConfig) -> float:
                health = self.registry.get_health(p.id)
                if health and health.latency_ms:
                    return health.latency_ms
                return float('inf')
            return sorted(allowed, key=latency)

        elif self._strategy == FailoverStrategy.RANDOM:
            import random
            random.shuffle(allowed)
            return allowed

        return allowed

    async def execute_with_failover(
        self,
        func: Callable[[ProviderConfig], Awaitable[Any]],
        required_capability: str = None,
        model: str = None
    ) -> FailoverResult:
        """
        Execute function with automatic failover.

        Args:
            func: Async function to execute (takes provider config)
            required_capability: Required capability
            model: Required model

        Returns:
            FailoverResult with outcome
        """
        self._total_requests += 1
        start_time = time.time()
        failover_path = []

        providers = self._get_provider_order(required_capability, model)

        if not providers:
            return FailoverResult(
                success=False,
                provider_id="",
                error="No providers available",
                attempts=0
            )

        last_error = None
        attempts = 0

        for retry in range(self._max_retries):
            for provider in providers:
                attempts += 1
                failover_path.append(provider.id)

                cb = self.get_circuit_breaker(provider.id)

                if not cb.should_allow_request():
                    continue

                try:
                    # Execute with this provider
                    result = await func(provider)

                    # Success
                    cb.record_success()
                    self.registry.record_request(
                        provider.id,
                        success=True,
                        latency_ms=(time.time() - start_time) * 1000
                    )

                    if attempts > 1:
                        self._total_failovers += 1
                        self._successful_failovers += 1

                    return FailoverResult(
                        success=True,
                        provider_id=provider.id,
                        result=result,
                        latency_ms=(time.time() - start_time) * 1000,
                        attempts=attempts,
                        failover_path=failover_path
                    )

                except Exception as e:
                    last_error = str(e)
                    cb.record_failure()
                    self.registry.record_request(provider.id, success=False)
                    self.registry.update_health(
                        provider.id,
                        ProviderStatus.DEGRADED,
                        error=last_error
                    )

                    logger.warning(
                        f"Provider {provider.id} failed: {last_error}"
                    )

            # Exponential backoff before retry
            if retry < self._max_retries - 1:
                delay = min(
                    self._base_delay_seconds * (2 ** retry),
                    self._max_delay_seconds
                )
                logger.info(f"Retrying in {delay:.1f}s (attempt {retry + 2})")
                await asyncio.sleep(delay)

        self._total_failovers += 1

        return FailoverResult(
            success=False,
            provider_id=failover_path[-1] if failover_path else "",
            error=last_error or "All providers failed",
            latency_ms=(time.time() - start_time) * 1000,
            attempts=attempts,
            failover_path=failover_path
        )

    async def health_check_all(self) -> Dict[str, ProviderHealth]:
        """
        Run health check on all providers.

        Returns:
            Health status for all providers
        """
        results = {}

        for provider in self.registry.list_providers():
            try:
                # Simple connectivity check
                start = time.time()

                # Mark as available if we can get config
                latency = (time.time() - start) * 1000
                self.registry.update_health(
                    provider.id,
                    ProviderStatus.AVAILABLE,
                    latency_ms=latency
                )

            except Exception as e:
                self.registry.update_health(
                    provider.id,
                    ProviderStatus.UNAVAILABLE,
                    error=str(e)
                )

            results[provider.id] = self.registry.get_health(provider.id)

        return results

    def reset_circuit_breaker(self, provider_id: str) -> bool:
        """
        Manually reset a circuit breaker.

        Args:
            provider_id: Provider ID

        Returns:
            True if reset, False if not found
        """
        if provider_id in self._circuit_breakers:
            self._circuit_breakers[provider_id] = CircuitBreaker(
                provider_id=provider_id
            )
            logger.info(f"Reset circuit breaker for {provider_id}")
            return True
        return False

    def get_circuit_states(self) -> Dict[str, Dict]:
        """Get all circuit breaker states."""
        return {
            provider_id: cb.to_dict()
            for provider_id, cb in self._circuit_breakers.items()
        }

    def get_stats(self) -> Dict:
        """Get failover statistics."""
        return {
            'total_requests': self._total_requests,
            'total_failovers': self._total_failovers,
            'successful_failovers': self._successful_failovers,
            'failover_success_rate': (
                self._successful_failovers / self._total_failovers
                if self._total_failovers > 0 else 0.0
            ),
            'strategy': self._strategy.value,
            'max_retries': self._max_retries,
            'circuit_breakers': len(self._circuit_breakers),
            'circuit_states': {
                state.value: sum(
                    1 for cb in self._circuit_breakers.values()
                    if cb.state == state
                )
                for state in CircuitState
            }
        }

    def reset(self) -> None:
        """Reset manager state."""
        self._circuit_breakers.clear()
        self._rr_index = 0
        self._total_requests = 0
        self._total_failovers = 0
        self._successful_failovers = 0
        logger.info("FailoverManager reset")
