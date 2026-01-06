"""
EmergenceDetector - Detects when genuine emergence has occurred.

Design principles:
- No hardcoded "what emergence looks like"
- Detects THAT emergence happened, not WHAT emerged
- Uses multiple orthogonal metrics
- Conservative thresholds (prefer continuing)
"""

from typing import Dict, List, Optional, TYPE_CHECKING
from dataclasses import dataclass, field
import logging

if TYPE_CHECKING:
    from ..consciousness.stream import ConsciousnessStream
    from ..consciousness.frame import ConsciousnessFrame

logger = logging.getLogger("rsi.orchestration.emergence")


@dataclass
class EmergenceResult:
    """Result of emergence detection."""
    emerged: bool
    reason: Optional[str] = None
    confidence: float = 0.0
    metrics: Dict = field(default_factory=dict)


class EmergenceDetector:
    """
    Detects when genuine emergence has occurred.

    This is the core decision-maker for when BYRD should stop iterating.
    It uses multiple orthogonal metrics to avoid false positives.
    """

    def __init__(
        self,
        consciousness: "ConsciousnessStream",
        config: Dict = None
    ):
        """
        Initialize emergence detector.

        Args:
            consciousness: ConsciousnessStream for historical analysis
            config: Configuration overrides
        """
        self.consciousness = consciousness
        self.config = config or {}

        # Configurable thresholds
        self.entropy_threshold = self.config.get('entropy_threshold', 0.1)
        self.circular_tolerance = self.config.get('circular_tolerance', 3)
        self.min_cycles_before_check = self.config.get('min_cycles', 50)
        self.crystallization_weight = self.config.get('crystallization_weight', 0.5)

    async def check(self, current_frame: "ConsciousnessFrame") -> EmergenceResult:
        """
        Check if this cycle represents genuine emergence.

        Args:
            current_frame: The latest consciousness frame

        Returns:
            EmergenceResult indicating whether to continue or stop
        """
        metrics = {}
        reasons = []

        # Don't check too early
        stats = self.consciousness.get_stats()
        if stats['total_frames'] < self.min_cycles_before_check:
            return EmergenceResult(
                emerged=False,
                reason=f"Too early ({stats['total_frames']} < {self.min_cycles_before_check})",
                confidence=0.0,
                metrics={'total_frames': stats['total_frames']}
            )

        # === Metric 1: Heuristic Crystallization ===
        # Immediate signal: a heuristic was crystallized
        if current_frame.heuristic_crystallized:
            reasons.append("heuristic_crystallized")
            metrics['crystallization'] = True
        else:
            metrics['crystallization'] = False

        # === Metric 2: Entropy Delta ===
        # Are we generating genuinely novel content?
        entropy_delta = await self.consciousness.compute_entropy_delta(window=100)
        metrics['entropy_delta'] = entropy_delta

        if entropy_delta > self.entropy_threshold:
            reasons.append(f"entropy_increased ({entropy_delta:.3f})")

        # === Metric 3: Circular Pattern Detection ===
        # Are we repeating ourselves?
        circular = await self.consciousness.detect_circular_patterns()
        metrics['circular_patterns'] = circular

        if circular['is_circular']:
            # Negative signal: we're stuck in a loop
            logger.warning(f"Circular patterns detected: {circular['repeated_desires'][:2]}")
            return EmergenceResult(
                emerged=False,
                reason=f"Circular patterns detected: {circular['repeated_desires'][:2]}",
                confidence=0.0,
                metrics=metrics
            )

        # === Metric 4: Capability Delta ===
        # Did we gain new capabilities?
        if current_frame.capability_delta:
            reasons.append(f"capability_gained: {list(current_frame.capability_delta.keys())}")
            metrics['capability_gained'] = True
        else:
            metrics['capability_gained'] = False

        # === Metric 5: Time-Travel Comparison ===
        # Compare to 100 cycles ago
        past_frame = await self.consciousness.time_travel(100)
        if past_frame:
            belief_diff = self._compute_belief_difference(current_frame, past_frame)
            metrics['belief_diff_100'] = belief_diff

            if belief_diff > 0.3:  # 30% difference threshold
                reasons.append(f"beliefs_evolved ({belief_diff:.2f})")

        # === Decision ===
        # We say "emerged" if we have multiple positive signals
        confidence = len(reasons) / 5.0  # 5 possible metrics

        # Weigh crystallization more heavily
        if metrics.get('crystallization'):
            confidence += self.crystallization_weight

        emerged = confidence >= 0.4  # Need 40% of metrics positive

        return EmergenceResult(
            emerged=emerged,
            reason="; ".join(reasons) if reasons else "No emergence signals",
            confidence=min(1.0, confidence),
            metrics=metrics
        )

    def _compute_belief_difference(
        self,
        current: "ConsciousnessFrame",
        past: "ConsciousnessFrame"
    ) -> float:
        """Compute normalized difference between belief states."""
        current_keys = set(current.belief_delta.keys())
        past_keys = set(past.belief_delta.keys())

        if not current_keys and not past_keys:
            return 0.0

        intersection = len(current_keys & past_keys)
        union = len(current_keys | past_keys)

        return 1.0 - (intersection / union) if union > 0 else 0.0

    def reset(self):
        """Reset detector state."""
        logger.info("EmergenceDetector reset")
