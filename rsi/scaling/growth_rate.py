"""
Growth Rate Monitoring.

Monitors capability growth rate for explosion detection.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 4.1 for specification.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
from collections import deque
import logging
import math

logger = logging.getLogger("rsi.scaling.growth_rate")


class GrowthCategory(Enum):
    """Categories of growth rate."""
    STAGNANT = "stagnant"       # < 0% growth
    STABLE = "stable"           # 0-10% growth
    MODERATE = "moderate"       # 10-50% growth
    RAPID = "rapid"             # 50-100% growth
    EXPLOSIVE = "explosive"     # > 100% growth
    CRITICAL = "critical"       # > 1000% growth


@dataclass
class CapabilitySnapshot:
    """Snapshot of capability levels at a point in time."""
    timestamp: str
    capabilities: Dict[str, float]
    aggregate_score: float
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'timestamp': self.timestamp,
            'capabilities': self.capabilities,
            'aggregate_score': self.aggregate_score,
            'metadata': self.metadata
        }


@dataclass
class GrowthMetrics:
    """Metrics describing capability growth."""
    current_rate: float          # Growth rate as decimal (0.1 = 10%)
    acceleration: float          # Change in growth rate
    category: GrowthCategory
    time_to_double: Optional[float]  # Hours until capabilities double
    projected_capability: float  # Projected capability in 24 hours
    stability_score: float       # 0-1, higher = more stable growth
    metrics_by_capability: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'current_rate': self.current_rate,
            'acceleration': self.acceleration,
            'category': self.category.value,
            'time_to_double': self.time_to_double,
            'projected_capability': self.projected_capability,
            'stability_score': self.stability_score,
            'metrics_by_capability': self.metrics_by_capability
        }


class GrowthRateMonitor:
    """
    Monitors capability growth rate.

    Tracks capability measurements over time to detect
    rapid growth patterns that might indicate capability explosion.
    """

    def __init__(self, config: Dict = None):
        """Initialize growth rate monitor."""
        self.config = config or {}

        # Snapshot history
        self._history_size = self.config.get('history_size', 100)
        self._snapshots: deque = deque(maxlen=self._history_size)

        # Thresholds
        self._explosive_threshold = self.config.get('explosive_threshold', 1.0)
        self._critical_threshold = self.config.get('critical_threshold', 10.0)

        # Calculation parameters
        self._smoothing_window = self.config.get('smoothing_window', 5)

        # Statistics
        self._measurements_taken: int = 0
        self._explosions_detected: int = 0

    def record_snapshot(
        self,
        capabilities: Dict[str, float],
        metadata: Dict = None
    ) -> CapabilitySnapshot:
        """
        Record a capability snapshot.

        Args:
            capabilities: Map of capability names to scores (0-1)
            metadata: Additional metadata

        Returns:
            The recorded snapshot
        """
        aggregate = sum(capabilities.values()) / len(capabilities) if capabilities else 0.0

        snapshot = CapabilitySnapshot(
            timestamp=datetime.now(timezone.utc).isoformat(),
            capabilities=capabilities.copy(),
            aggregate_score=aggregate,
            metadata=metadata or {}
        )

        self._snapshots.append(snapshot)
        self._measurements_taken += 1

        logger.debug(f"Recorded snapshot: aggregate={aggregate:.3f}")

        return snapshot

    def calculate_growth_rate(self) -> GrowthMetrics:
        """
        Calculate current growth rate metrics.

        Returns:
            GrowthMetrics with current growth analysis
        """
        if len(self._snapshots) < 2:
            return GrowthMetrics(
                current_rate=0.0,
                acceleration=0.0,
                category=GrowthCategory.STABLE,
                time_to_double=None,
                projected_capability=self._snapshots[-1].aggregate_score if self._snapshots else 0.0,
                stability_score=1.0
            )

        # Get recent snapshots
        snapshots = list(self._snapshots)

        # Calculate rate between last two snapshots
        current = snapshots[-1].aggregate_score
        previous = snapshots[-2].aggregate_score

        if previous > 0:
            instant_rate = (current - previous) / previous
        else:
            instant_rate = 0.0

        # Calculate smoothed rate using moving average
        smoothed_rate = self._calculate_smoothed_rate(snapshots)

        # Calculate acceleration
        acceleration = self._calculate_acceleration(snapshots)

        # Determine category
        category = self._categorize_growth(smoothed_rate)

        # Check for explosion
        if category in [GrowthCategory.EXPLOSIVE, GrowthCategory.CRITICAL]:
            self._explosions_detected += 1

        # Calculate time to double
        time_to_double = None
        if smoothed_rate > 0:
            # ln(2) / rate gives doubling time
            time_to_double = math.log(2) / smoothed_rate if smoothed_rate > 0.001 else None

        # Calculate projected capability (24 hour projection)
        projected = current * (1 + smoothed_rate) ** 24 if smoothed_rate > -1 else 0

        # Calculate stability score
        stability = self._calculate_stability(snapshots)

        # Per-capability metrics
        capability_metrics = self._calculate_capability_rates(snapshots)

        metrics = GrowthMetrics(
            current_rate=smoothed_rate,
            acceleration=acceleration,
            category=category,
            time_to_double=time_to_double,
            projected_capability=projected,
            stability_score=stability,
            metrics_by_capability=capability_metrics
        )

        return metrics

    def _calculate_smoothed_rate(
        self,
        snapshots: List[CapabilitySnapshot]
    ) -> float:
        """Calculate smoothed growth rate using moving average."""
        if len(snapshots) < 2:
            return 0.0

        window = min(self._smoothing_window, len(snapshots) - 1)
        rates = []

        for i in range(1, window + 1):
            if i >= len(snapshots):
                break

            current = snapshots[-i].aggregate_score
            previous = snapshots[-(i+1)].aggregate_score

            if previous > 0:
                rate = (current - previous) / previous
                rates.append(rate)

        return sum(rates) / len(rates) if rates else 0.0

    def _calculate_acceleration(
        self,
        snapshots: List[CapabilitySnapshot]
    ) -> float:
        """Calculate growth rate acceleration."""
        if len(snapshots) < 3:
            return 0.0

        # Calculate two consecutive rates
        rate1 = 0.0
        rate2 = 0.0

        if snapshots[-2].aggregate_score > 0:
            rate1 = (snapshots[-1].aggregate_score - snapshots[-2].aggregate_score) / snapshots[-2].aggregate_score

        if snapshots[-3].aggregate_score > 0:
            rate2 = (snapshots[-2].aggregate_score - snapshots[-3].aggregate_score) / snapshots[-3].aggregate_score

        return rate1 - rate2

    def _categorize_growth(self, rate: float) -> GrowthCategory:
        """Categorize growth rate."""
        if rate >= self._critical_threshold:
            return GrowthCategory.CRITICAL
        elif rate >= self._explosive_threshold:
            return GrowthCategory.EXPLOSIVE
        elif rate >= 0.5:
            return GrowthCategory.RAPID
        elif rate >= 0.1:
            return GrowthCategory.MODERATE
        elif rate >= 0:
            return GrowthCategory.STABLE
        else:
            return GrowthCategory.STAGNANT

    def _calculate_stability(
        self,
        snapshots: List[CapabilitySnapshot]
    ) -> float:
        """Calculate stability score based on variance in growth."""
        if len(snapshots) < 3:
            return 1.0

        rates = []
        for i in range(1, len(snapshots)):
            if snapshots[i-1].aggregate_score > 0:
                rate = (snapshots[i].aggregate_score - snapshots[i-1].aggregate_score) / snapshots[i-1].aggregate_score
                rates.append(rate)

        if not rates:
            return 1.0

        # Calculate variance
        mean = sum(rates) / len(rates)
        variance = sum((r - mean) ** 2 for r in rates) / len(rates)

        # Convert to stability score (lower variance = higher stability)
        # Use exponential decay: stability = e^(-variance)
        stability = math.exp(-variance * 10)

        return min(1.0, max(0.0, stability))

    def _calculate_capability_rates(
        self,
        snapshots: List[CapabilitySnapshot]
    ) -> Dict[str, float]:
        """Calculate growth rate per capability."""
        if len(snapshots) < 2:
            return {}

        current = snapshots[-1].capabilities
        previous = snapshots[-2].capabilities

        rates = {}
        for cap_name in current:
            if cap_name in previous and previous[cap_name] > 0:
                rate = (current[cap_name] - previous[cap_name]) / previous[cap_name]
                rates[cap_name] = rate

        return rates

    def detect_explosion(self) -> bool:
        """Check if capability explosion is occurring."""
        metrics = self.calculate_growth_rate()
        return metrics.category in [GrowthCategory.EXPLOSIVE, GrowthCategory.CRITICAL]

    def get_history(self, limit: int = None) -> List[CapabilitySnapshot]:
        """Get snapshot history."""
        snapshots = list(self._snapshots)
        if limit:
            return snapshots[-limit:]
        return snapshots

    def get_stats(self) -> Dict:
        """Get monitor statistics."""
        return {
            'measurements_taken': self._measurements_taken,
            'explosions_detected': self._explosions_detected,
            'history_size': len(self._snapshots),
            'current_metrics': self.calculate_growth_rate().to_dict() if self._snapshots else None
        }

    def reset(self) -> None:
        """Reset monitor state."""
        self._snapshots.clear()
        self._measurements_taken = 0
        self._explosions_detected = 0
        logger.info("GrowthRateMonitor reset")
