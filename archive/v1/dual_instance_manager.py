"""
BYRD Dual Instance Manager - Rate limiting for ZAI GLM-4.7 Max Coding Plan.

Manages two concurrent GLM-4.7 instances with independent rate limiting:
- Instance A (Primary): Dreamer, Seeker, Actor - core BYRD operations
- Instance B (Enrichment): Graphiti, Capability Evaluator, Code Verifier

Optimized for ZAI Max Coding Plan:
- 2400 prompts / 5 hours per instance
- 480 prompts/hour = 8/minute = 7.5s minimum interval
- With dual instances: 960 prompts/hour total capacity
"""

import asyncio
import time
from enum import Enum
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


class InstanceRole(Enum):
    PRIMARY = "primary"
    ENRICHMENT = "enrichment"


@dataclass
class InstanceMetrics:
    """Metrics for a single instance."""
    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    total_wait_time: float = 0.0
    tokens_used: int = 0
    last_call_time: float = 0.0
    session_start: float = field(default_factory=time.time)


class TokenBucket:
    """Token bucket for burst handling."""

    def __init__(self, capacity: int, refill_seconds: float):
        self.capacity = capacity
        self.refill_seconds = refill_seconds
        self.tokens = capacity
        self.last_refill = time.time()

    def try_acquire(self) -> bool:
        """Try to acquire a token. Returns True if successful."""
        self._refill()
        if self.tokens > 0:
            self.tokens -= 1
            return True
        return False

    def _refill(self):
        """Refill tokens based on elapsed time."""
        now = time.time()
        elapsed = now - self.last_refill
        refill_count = int(elapsed / self.refill_seconds)
        if refill_count > 0:
            self.tokens = min(self.capacity, self.tokens + refill_count)
            self.last_refill = now


class DualInstanceManager:
    """
    Manages two concurrent GLM-4.7 instances with independent rate limiting.

    Instance A (Primary): Dreamer, Seeker, Actor - core BYRD operations
    Instance B (Enrichment): Graphiti, Capability Evaluator, Code Verifier

    Optimized for ZAI Max Coding Plan:
    - 2400 prompts / 5 hours per instance
    - 480 prompts/hour = 8/minute = 7.5s minimum interval
    - With dual instances: 960 prompts/hour total capacity
    """

    def __init__(self, llm_client, config: Dict[str, Any]):
        self._client = llm_client
        self._config = config

        rate_config = config.get('rate_limit', {})
        self._interval = rate_config.get('interval_seconds', 8.0)
        burst_tokens = rate_config.get('burst_tokens', 3)
        burst_recovery = rate_config.get('burst_recovery_seconds', 24.0)

        # Per-instance locks and timing
        self._locks: Dict[InstanceRole, asyncio.Lock] = {
            InstanceRole.PRIMARY: asyncio.Lock(),
            InstanceRole.ENRICHMENT: asyncio.Lock()
        }

        self._last_call: Dict[InstanceRole, float] = {
            InstanceRole.PRIMARY: 0,
            InstanceRole.ENRICHMENT: 0
        }

        # Burst handling
        self._burst_buckets: Dict[InstanceRole, TokenBucket] = {
            InstanceRole.PRIMARY: TokenBucket(burst_tokens, burst_recovery),
            InstanceRole.ENRICHMENT: TokenBucket(burst_tokens, burst_recovery)
        }

        # Metrics
        self._metrics: Dict[InstanceRole, InstanceMetrics] = {
            InstanceRole.PRIMARY: InstanceMetrics(),
            InstanceRole.ENRICHMENT: InstanceMetrics()
        }

        # Component routing
        self._component_routing: Dict[str, InstanceRole] = {
            'dreamer': InstanceRole.PRIMARY,
            'seeker': InstanceRole.PRIMARY,
            'actor': InstanceRole.PRIMARY,
            'graphiti': InstanceRole.ENRICHMENT,
            'capability_evaluator': InstanceRole.ENRICHMENT,
            'code_verifier': InstanceRole.ENRICHMENT
        }

    def get_instance_for_component(self, component: str) -> InstanceRole:
        """Get the appropriate instance for a component."""
        return self._component_routing.get(component, InstanceRole.PRIMARY)

    async def call(
        self,
        role: InstanceRole,
        prompt: str,
        component: str = "unknown",
        **kwargs
    ) -> Any:
        """Make rate-limited call on specified instance."""
        async with self._locks[role]:
            wait_time = await self._wait_for_slot(role)

            try:
                result = await self._client.generate(prompt, **kwargs)
                self._record_success(role, wait_time)
                return result
            except Exception as e:
                self._record_failure(role, wait_time)
                raise

    async def _wait_for_slot(self, role: InstanceRole) -> float:
        """Wait for rate limit slot, returns wait time."""
        # Check burst bucket first
        if self._burst_buckets[role].try_acquire():
            return 0.0

        # Otherwise, wait for interval
        elapsed = time.time() - self._last_call[role]
        wait_time = max(0, self._interval - elapsed)

        if wait_time > 0:
            await asyncio.sleep(wait_time)

        self._last_call[role] = time.time()
        return wait_time

    def _record_success(self, role: InstanceRole, wait_time: float):
        """Record successful call metrics."""
        metrics = self._metrics[role]
        metrics.total_calls += 1
        metrics.successful_calls += 1
        metrics.total_wait_time += wait_time
        metrics.last_call_time = time.time()

    def _record_failure(self, role: InstanceRole, wait_time: float):
        """Record failed call metrics."""
        metrics = self._metrics[role]
        metrics.total_calls += 1
        metrics.failed_calls += 1
        metrics.total_wait_time += wait_time

    async def call_by_component(
        self,
        component: str,
        prompt: str,
        **kwargs
    ) -> Any:
        """Route call to appropriate instance based on component."""
        role = self.get_instance_for_component(component)
        return await self.call(role, prompt, component=component, **kwargs)

    async def call_parallel(
        self,
        primary_prompt: str,
        enrichment_prompt: str,
        **kwargs
    ) -> tuple:
        """Make parallel calls on both instances."""
        primary_task = self.call(InstanceRole.PRIMARY, primary_prompt, **kwargs)
        enrichment_task = self.call(InstanceRole.ENRICHMENT, enrichment_prompt, **kwargs)
        return await asyncio.gather(primary_task, enrichment_task)

    def get_metrics(self) -> Dict[str, Any]:
        """Get comprehensive metrics for both instances."""
        return {
            'primary': {
                'total_calls': self._metrics[InstanceRole.PRIMARY].total_calls,
                'successful': self._metrics[InstanceRole.PRIMARY].successful_calls,
                'failed': self._metrics[InstanceRole.PRIMARY].failed_calls,
                'avg_wait': (
                    self._metrics[InstanceRole.PRIMARY].total_wait_time /
                    max(1, self._metrics[InstanceRole.PRIMARY].total_calls)
                ),
                'utilization': self._calculate_utilization(InstanceRole.PRIMARY)
            },
            'enrichment': {
                'total_calls': self._metrics[InstanceRole.ENRICHMENT].total_calls,
                'successful': self._metrics[InstanceRole.ENRICHMENT].successful_calls,
                'failed': self._metrics[InstanceRole.ENRICHMENT].failed_calls,
                'avg_wait': (
                    self._metrics[InstanceRole.ENRICHMENT].total_wait_time /
                    max(1, self._metrics[InstanceRole.ENRICHMENT].total_calls)
                ),
                'utilization': self._calculate_utilization(InstanceRole.ENRICHMENT)
            },
            'total_calls': sum(m.total_calls for m in self._metrics.values()),
            'interval_seconds': self._interval
        }

    def _calculate_utilization(self, role: InstanceRole) -> float:
        """Calculate instance utilization (0-1) based on session duration."""
        metrics = self._metrics[role]
        if metrics.total_calls == 0:
            return 0.0

        # Use session_start for accurate duration calculation
        elapsed_hours = (time.time() - metrics.session_start) / 3600
        if elapsed_hours < 0.001:  # Less than ~4 seconds
            return 0.0

        # Max calls per hour at current interval
        max_calls_per_hour = 3600 / self._interval

        # Calls per hour during this session
        calls_per_hour = metrics.total_calls / elapsed_hours

        return min(1.0, calls_per_hour / max_calls_per_hour)

    def reset(self):
        """Reset for fresh start."""
        for role in InstanceRole:
            self._metrics[role] = InstanceMetrics()
            self._last_call[role] = 0
            self._burst_buckets[role].tokens = self._burst_buckets[role].capacity
