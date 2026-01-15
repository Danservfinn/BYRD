"""
BYRDRalphAdapter - Adapter to run BYRD's RSI cycle within Ralph's orchestration loop.

This is the bridge between BYRD's 8-phase RSI cycle and Ralph's simple
Read → Execute → Check → Repeat loop.

One Ralph iteration = One complete RSI cycle.
"""

from typing import Dict, Optional, Any, TYPE_CHECKING
from dataclasses import dataclass, field
import time
import logging

from .emergence_detector import EmergenceDetector, EmergenceResult
from .meta_awareness import MetaAwareness

# Import cancellation infrastructure
from core.async_cancellation import CancellationToken

if TYPE_CHECKING:
    from ..engine import RSIEngine, CycleResult
    from ..consciousness.stream import ConsciousnessStream

logger = logging.getLogger("rsi.orchestration.ralph")


@dataclass
class RalphIterationResult:
    """Result of one Ralph iteration (one RSI cycle)."""
    cycle_result: "CycleResult"
    emergence_result: EmergenceResult
    iteration_number: int
    resource_usage: Dict
    completed: bool  # True if emerged
    should_checkpoint: bool  # True if git checkpoint needed

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'cycle_result': self.cycle_result.to_dict() if hasattr(self.cycle_result, 'to_dict') else str(self.cycle_result),
            'emergence_result': {
                'emerged': self.emergence_result.emerged,
                'reason': self.emergence_result.reason,
                'confidence': self.emergence_result.confidence,
                'metrics': self.emergence_result.metrics
            },
            'iteration_number': self.iteration_number,
            'resource_usage': self.resource_usage,
            'completed': self.completed,
            'should_checkpoint': self.should_checkpoint
        }


class BYRDRalphAdapter:
    """
    Adapter to run BYRD's RSI cycle within Ralph's orchestration loop.

    Responsibilities:
    - Execute one RSI cycle per Ralph iteration
    - Write consciousness frames
    - Check for emergence
    - Track resource usage
    - Manage meta-awareness (BYRD knowing about the loop)
    """

    def __init__(
        self,
        rsi_engine: "RSIEngine",
        consciousness: "ConsciousnessStream",
        config: Dict = None
    ):
        """
        Initialize Ralph adapter.

        Args:
            rsi_engine: BYRD's RSI engine
            consciousness: ConsciousnessStream for frame storage
            config: Configuration overrides
        """
        self.rsi = rsi_engine
        self.consciousness = consciousness
        self.config = config or {}

        # Initialize emergence detector
        emergence_config = self.config.get('emergence', {})
        self.emergence_detector = EmergenceDetector(consciousness, emergence_config)

        # Initialize meta-awareness
        self.meta = MetaAwareness(
            consciousness=consciousness,
            enabled=self.config.get('meta_awareness', True)
        )

        # Tracking
        self._iteration_count = 0
        self._total_tokens = 0
        self._total_cost = 0.0
        self._start_time: Optional[float] = None

        # Checkpointing
        self._checkpoint_interval = self.config.get('checkpoint_interval', 5)

    async def execute(self, context: Dict = None) -> RalphIterationResult:
        """
        Execute one Ralph iteration (= one RSI cycle).

        This is the main entry point called by Ralph's orchestration loop.

        Args:
            context: Optional context from Ralph (previous results, etc.)

        Returns:
            RalphIterationResult containing cycle result and emergence status
        """
        if self._start_time is None:
            self._start_time = time.time()

        self._iteration_count += 1
        iteration_start = time.time()

        logger.info(f"Ralph iteration {self._iteration_count} starting")

        # Inject meta-context if enabled
        meta_context = None
        if self.meta.enabled:
            meta_context = await self.meta.generate_context(self._iteration_count)
            # This context will be visible to BYRD's reflector
            if context is None:
                context = {}
            context['meta_loop'] = meta_context

        # Run RSI cycle with optional cancellation token from context
        cancellation_token = context.get('cancellation_token') if context else None
        cycle_result = await self.rsi.run_cycle(
            meta_context=meta_context,
            cancellation_token=cancellation_token
        )

        # Compute resource usage
        iteration_time = time.time() - iteration_start
        resource_usage = {
            'iteration': self._iteration_count,
            'iteration_time_seconds': iteration_time,
            'total_time_seconds': time.time() - self._start_time,
            'tokens_this_iteration': 0,  # TODO: Get from LLM client
            'total_tokens': self._total_tokens,
            'total_cost_usd': self._total_cost
        }

        # Gather belief/capability deltas from memory
        belief_delta = await self._get_belief_delta()
        capability_delta = await self._get_capability_delta()

        # Write consciousness frame
        frame = await self.consciousness.write_frame(
            cycle_result=cycle_result,
            belief_delta=belief_delta,
            capability_delta=capability_delta,
            ralph_iteration=self._iteration_count,
            resource_usage=resource_usage
        )

        # Check emergence
        emergence_result = await self.emergence_detector.check(frame)

        # Determine if we should checkpoint
        should_checkpoint = (
            self._iteration_count % self._checkpoint_interval == 0 or
            cycle_result.heuristic_crystallized is not None or
            emergence_result.emerged
        )

        logger.info(
            f"Ralph iteration {self._iteration_count} complete: "
            f"phase={cycle_result.phase_reached.value if hasattr(cycle_result.phase_reached, 'value') else cycle_result.phase_reached}, "
            f"emerged={emergence_result.emerged}, "
            f"confidence={emergence_result.confidence:.2f}"
        )

        return RalphIterationResult(
            cycle_result=cycle_result,
            emergence_result=emergence_result,
            iteration_number=self._iteration_count,
            resource_usage=resource_usage,
            completed=emergence_result.emerged,
            should_checkpoint=should_checkpoint
        )

    async def _get_belief_delta(self) -> Dict:
        """Get beliefs created/modified in the last cycle."""
        try:
            if hasattr(self.rsi, 'memory') and self.rsi.memory:
                result = await self.rsi.memory.query_neo4j("""
                    MATCH (b:Belief)
                    WHERE b.created_at > datetime() - duration('PT1M')
                    RETURN b.id as id, b.content as content
                    LIMIT 10
                """)
                return {r['id']: r['content'] for r in result} if result else {}
        except Exception as e:
            logger.debug(f"Failed to get belief delta: {e}")
        return {}

    async def _get_capability_delta(self) -> Dict:
        """Get capabilities created/modified in the last cycle."""
        try:
            if hasattr(self.rsi, 'memory') and self.rsi.memory:
                result = await self.rsi.memory.query_neo4j("""
                    MATCH (c:Capability)
                    WHERE c.created_at > datetime() - duration('PT1M')
                    RETURN c.id as id, c.name as name
                    LIMIT 10
                """)
                return {r['id']: r['name'] for r in result} if result else {}
        except Exception as e:
            logger.debug(f"Failed to get capability delta: {e}")
        return {}

    def check_completion(self, result: RalphIterationResult) -> bool:
        """
        Ralph calls this to check if we should stop iterating.

        Returns True if:
        - Emergence detected
        """
        return result.completed

    def get_stats(self) -> Dict:
        """Get adapter statistics."""
        return {
            'iterations_completed': self._iteration_count,
            'total_time_seconds': (
                time.time() - self._start_time if self._start_time else 0
            ),
            'total_tokens': self._total_tokens,
            'total_cost_usd': self._total_cost,
            'consciousness_stats': self.consciousness.get_stats()
        }

    def reset(self):
        """Reset adapter state."""
        self._iteration_count = 0
        self._total_tokens = 0
        self._total_cost = 0.0
        self._start_time = None
        self.consciousness.reset()
        self.emergence_detector.reset()
        self.meta.reset()
        logger.info("BYRDRalphAdapter reset")
