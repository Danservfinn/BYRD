"""
MetaAwareness - BYRD's awareness of being in a Ralph loop.

This is the most philosophically interesting part of the integration.
It enables BYRD to reason about its own execution context.

Can be enabled/disabled based on philosophical preference.
"""

from typing import Dict, Optional, TYPE_CHECKING
from dataclasses import dataclass
from datetime import datetime
import time
import logging

if TYPE_CHECKING:
    from ..consciousness.stream import ConsciousnessStream

logger = logging.getLogger("rsi.orchestration.meta")


@dataclass
class MetaContext:
    """Context about the Ralph loop for BYRD's awareness."""
    iteration: int
    total_frames: int
    entropy_trend: str  # "increasing", "decreasing", "stable"
    recent_emergence_signals: int
    time_in_loop_seconds: float
    estimated_tokens_remaining: int

    def to_prompt_section(self) -> str:
        """
        Format for inclusion in BYRD's reflection prompt.

        This is what BYRD "sees" about its own execution context.
        """
        return f"""
## META-LOOP CONTEXT

You are in iteration {self.iteration} of a recursive self-improvement loop.

Current status:
- Total consciousness frames: {self.total_frames}
- Entropy trend: {self.entropy_trend}
- Recent emergence signals: {self.recent_emergence_signals}
- Time in loop: {self.time_in_loop_seconds:.0f} seconds
- Estimated tokens remaining: {self.estimated_tokens_remaining}

This information is provided so you can reason about your own improvement process.
You cannot directly control the loop - it will stop when genuine emergence is detected.
"""

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'iteration': self.iteration,
            'total_frames': self.total_frames,
            'entropy_trend': self.entropy_trend,
            'recent_emergence_signals': self.recent_emergence_signals,
            'time_in_loop_seconds': self.time_in_loop_seconds,
            'estimated_tokens_remaining': self.estimated_tokens_remaining
        }


class MetaAwareness:
    """
    Manages BYRD's awareness of being in a Ralph loop.

    Arguments FOR meta-awareness:
    - True RSI requires self-knowledge
    - Loop-aware optimization is possible
    - Can avoid infinite loops by seeing history

    Arguments AGAINST:
    - Loop gaming (premature emergence declaration)
    - Meta-recursion complexity (thinking about thinking...)
    - Emergence purity (might require not knowing context)

    This implementation supports both modes via the `enabled` flag.
    """

    def __init__(
        self,
        consciousness: "ConsciousnessStream",
        enabled: bool = True
    ):
        """
        Initialize meta-awareness.

        Args:
            consciousness: ConsciousnessStream for state analysis
            enabled: Whether to generate meta-context for BYRD
        """
        self.consciousness = consciousness
        self.enabled = enabled
        self._loop_start_time: Optional[float] = None

    async def generate_context(self, iteration: int) -> MetaContext:
        """
        Generate meta-context for BYRD's reflection.

        This context is injected into the reflection prompt so BYRD
        can reason about its own execution context.

        Args:
            iteration: Current Ralph iteration number

        Returns:
            MetaContext with loop information
        """
        if self._loop_start_time is None:
            self._loop_start_time = time.time()

        stats = self.consciousness.get_stats()

        # Compute entropy trend
        entropy_delta = await self.consciousness.compute_entropy_delta(window=50)
        if entropy_delta > 0.05:
            entropy_trend = "increasing"
        elif entropy_delta < -0.05:
            entropy_trend = "decreasing"
        else:
            entropy_trend = "stable"

        # Count recent emergence signals (heuristics crystallized recently)
        recent_frames = await self.consciousness.get_temporal_range(
            start=datetime.fromtimestamp(time.time() - 3600),  # Last hour
            end=datetime.now()
        )
        emergence_signals = sum(
            1 for f in recent_frames
            if f.heuristic_crystallized
        )

        return MetaContext(
            iteration=iteration,
            total_frames=stats['total_frames'],
            entropy_trend=entropy_trend,
            recent_emergence_signals=emergence_signals,
            time_in_loop_seconds=time.time() - self._loop_start_time,
            estimated_tokens_remaining=1000000 - stats['total_frames'] * 1000  # Rough estimate
        )

    def reset(self):
        """Reset meta-awareness state."""
        self._loop_start_time = None
        logger.info("MetaAwareness reset")
