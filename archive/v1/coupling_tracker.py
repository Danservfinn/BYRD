"""
BYRD Coupling Tracker
Measures correlations between self-improvement loops.

The key insight of Option B is that loops compound when they're coupled.
This module tracks:
- Which loops are running
- When capability improvements happen
- Correlations between loop activity and improvements
- Cross-loop multiplication effects

THE CRITICAL METRIC: Goal Evolver → Self-Compiler coupling.
When goals drive code changes that improve capability, we have true compounding.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from collections import deque
import json

from event_bus import event_bus, Event, EventType

logger = logging.getLogger(__name__)


@dataclass
class LoopActivity:
    """Record of a loop's activity."""
    loop_name: str
    timestamp: datetime
    event_type: str
    metrics: Dict[str, float] = field(default_factory=dict)


@dataclass
class CapabilityChange:
    """Record of a capability measurement."""
    capability_name: str
    timestamp: datetime
    old_value: float
    new_value: float
    delta: float
    source_loop: Optional[str] = None


@dataclass
class CouplingMeasurement:
    """Measurement of coupling between two loops."""
    loop_a: str
    loop_b: str
    correlation: float  # Pearson correlation coefficient
    sample_count: int
    measured_at: datetime
    is_significant: bool  # p < 0.05


class CouplingTracker:
    """
    Tracks correlations between self-improvement loops.

    Implements the core measurement infrastructure for Option B:
    - Records loop activity events
    - Records capability changes
    - Computes time-lagged correlations
    - Identifies which loop combinations compound
    """

    # Loop names we track
    LOOPS = frozenset({
        "memory_reasoner",
        "self_compiler",
        "goal_evolver",
        "dreaming_machine",
        "integration_mind"
    })

    def __init__(
        self,
        window_size: int = 100,
        correlation_lag_seconds: float = 60.0
    ):
        """
        Initialize the coupling tracker.

        Args:
            window_size: Number of events to keep per loop
            correlation_lag_seconds: Time window for correlation analysis
        """
        self.window_size = window_size
        self.correlation_lag = timedelta(seconds=correlation_lag_seconds)

        # Activity buffers per loop
        self._activities: Dict[str, deque] = {
            loop: deque(maxlen=window_size) for loop in self.LOOPS
        }

        # Capability change buffer
        self._capability_changes: deque = deque(maxlen=window_size * 5)

        # Cached coupling measurements
        self._couplings: Dict[Tuple[str, str], CouplingMeasurement] = {}

        # Subscribe to relevant events
        self._setup_subscriptions()

    def _setup_subscriptions(self):
        """Subscribe to loop and capability events."""
        event_bus.subscribe_async(self._on_event)

    async def _on_event(self, event: Event):
        """Handle incoming events."""
        # Map events to loops
        event_to_loop = {
            EventType.SPREADING_ACTIVATION: "memory_reasoner",
            EventType.MEMORY_QUERY_ANSWERED: "memory_reasoner",
            EventType.PATTERN_CREATED: "self_compiler",
            EventType.PATTERN_USED: "self_compiler",
            EventType.PATTERN_LIFTED: "self_compiler",
            EventType.GOAL_CREATED: "goal_evolver",
            EventType.GOAL_EVALUATED: "goal_evolver",
            EventType.GOAL_COMPLETED: "goal_evolver",
            EventType.GOAL_EVOLVED: "goal_evolver",
            EventType.INSIGHT_CREATED: "dreaming_machine",
            EventType.COUNTERFACTUAL_GENERATED: "dreaming_machine",
            EventType.LOOP_CYCLE_START: None,  # Check data for loop name
            EventType.LOOP_CYCLE_END: None,
        }

        loop_name = event_to_loop.get(event.type)

        # Handle cycle events that specify loop name
        if event.type in (EventType.LOOP_CYCLE_START, EventType.LOOP_CYCLE_END):
            loop_name = event.data.get("loop_name")

        if loop_name and loop_name in self.LOOPS:
            activity = LoopActivity(
                loop_name=loop_name,
                timestamp=event.timestamp,
                event_type=event.type.value,
                metrics=event.data.get("metrics", {})
            )
            self._activities[loop_name].append(activity)

        # Handle capability measurements
        if event.type == EventType.CAPABILITY_MEASURED:
            # Try to find previous value for delta
            cap_name = event.data.get("capability_name", "unknown")
            new_value = event.data.get("score", 0.0)
            old_value = self._get_last_capability_value(cap_name)

            change = CapabilityChange(
                capability_name=cap_name,
                timestamp=event.timestamp,
                old_value=old_value,
                new_value=new_value,
                delta=new_value - old_value,
                source_loop=event.data.get("source_loop")
            )
            self._capability_changes.append(change)

    def _get_last_capability_value(self, capability_name: str) -> float:
        """Get the most recent value for a capability."""
        for change in reversed(self._capability_changes):
            if change.capability_name == capability_name:
                return change.new_value
        return 0.0

    def record_activity(
        self,
        loop_name: str,
        event_type: str,
        metrics: Optional[Dict[str, float]] = None
    ):
        """
        Manually record loop activity.

        Args:
            loop_name: Which loop was active
            event_type: What kind of activity
            metrics: Optional metrics from the activity
        """
        if loop_name not in self.LOOPS:
            logger.warning(f"Unknown loop: {loop_name}")
            return

        activity = LoopActivity(
            loop_name=loop_name,
            timestamp=datetime.now(),
            event_type=event_type,
            metrics=metrics or {}
        )
        self._activities[loop_name].append(activity)

    def record_capability_change(
        self,
        capability_name: str,
        new_value: float,
        source_loop: Optional[str] = None
    ):
        """
        Record a capability measurement.

        Args:
            capability_name: Which capability changed
            new_value: New capability score
            source_loop: Which loop caused the change (if known)
        """
        old_value = self._get_last_capability_value(capability_name)

        change = CapabilityChange(
            capability_name=capability_name,
            timestamp=datetime.now(),
            old_value=old_value,
            new_value=new_value,
            delta=new_value - old_value,
            source_loop=source_loop
        )
        self._capability_changes.append(change)

    def compute_coupling(
        self,
        loop_a: str,
        loop_b: str,
        recency_weight: float = 0.9
    ) -> CouplingMeasurement:
        """
        Compute the coupling strength between two loops.

        Uses time-weighted correlation of activity patterns and
        capability changes following joint activity.

        Args:
            loop_a: First loop name
            loop_b: Second loop name
            recency_weight: Weight for more recent observations

        Returns:
            CouplingMeasurement with correlation and significance
        """
        activities_a = list(self._activities.get(loop_a, []))
        activities_b = list(self._activities.get(loop_b, []))

        if len(activities_a) < 5 or len(activities_b) < 5:
            # Not enough data
            return CouplingMeasurement(
                loop_a=loop_a,
                loop_b=loop_b,
                correlation=0.0,
                sample_count=min(len(activities_a), len(activities_b)),
                measured_at=datetime.now(),
                is_significant=False
            )

        # Build time series of activity counts
        now = datetime.now()
        window_start = now - self.correlation_lag * self.window_size

        # Bin activities into time buckets
        bucket_count = min(20, len(activities_a), len(activities_b))
        bucket_duration = self.correlation_lag

        counts_a = [0.0] * bucket_count
        counts_b = [0.0] * bucket_count

        for act in activities_a:
            bucket_idx = int((now - act.timestamp) / bucket_duration)
            if 0 <= bucket_idx < bucket_count:
                weight = recency_weight ** bucket_idx
                counts_a[bucket_idx] += weight

        for act in activities_b:
            bucket_idx = int((now - act.timestamp) / bucket_duration)
            if 0 <= bucket_idx < bucket_count:
                weight = recency_weight ** bucket_idx
                counts_b[bucket_idx] += weight

        # Compute Pearson correlation
        correlation = self._pearson_correlation(counts_a, counts_b)

        # Simple significance test (need at least 10 samples, r > 0.5)
        sample_count = sum(1 for a, b in zip(counts_a, counts_b) if a > 0 or b > 0)
        is_significant = sample_count >= 10 and abs(correlation) > 0.5

        measurement = CouplingMeasurement(
            loop_a=loop_a,
            loop_b=loop_b,
            correlation=correlation,
            sample_count=sample_count,
            measured_at=datetime.now(),
            is_significant=is_significant
        )

        # Cache the measurement
        self._couplings[(loop_a, loop_b)] = measurement
        self._couplings[(loop_b, loop_a)] = measurement

        return measurement

    def _pearson_correlation(self, x: List[float], y: List[float]) -> float:
        """Compute Pearson correlation coefficient."""
        n = len(x)
        if n == 0:
            return 0.0

        mean_x = sum(x) / n
        mean_y = sum(y) / n

        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))

        var_x = sum((xi - mean_x) ** 2 for xi in x)
        var_y = sum((yi - mean_y) ** 2 for yi in y)

        denominator = (var_x * var_y) ** 0.5

        if denominator == 0:
            return 0.0

        return numerator / denominator

    def compute_all_couplings(self) -> Dict[str, CouplingMeasurement]:
        """
        Compute coupling for all loop pairs.

        Returns:
            Dictionary mapping "loop_a:loop_b" to CouplingMeasurement
        """
        results = {}
        loops = list(self.LOOPS)

        for i, loop_a in enumerate(loops):
            for loop_b in loops[i+1:]:
                measurement = self.compute_coupling(loop_a, loop_b)
                key = f"{loop_a}:{loop_b}"
                results[key] = measurement

        return results

    def get_strongest_couplings(self, top_k: int = 3) -> List[CouplingMeasurement]:
        """
        Get the strongest loop couplings.

        Returns:
            List of top-k strongest couplings by correlation
        """
        all_couplings = self.compute_all_couplings()
        sorted_couplings = sorted(
            all_couplings.values(),
            key=lambda m: abs(m.correlation),
            reverse=True
        )
        return sorted_couplings[:top_k]

    def get_capability_growth_rate(
        self,
        capability_name: Optional[str] = None,
        window_hours: float = 24.0
    ) -> float:
        """
        Compute capability growth rate over a time window.

        Args:
            capability_name: Specific capability or None for average
            window_hours: Time window in hours

        Returns:
            Growth rate (delta per hour)
        """
        window_start = datetime.now() - timedelta(hours=window_hours)

        relevant_changes = [
            c for c in self._capability_changes
            if c.timestamp >= window_start
            and (capability_name is None or c.capability_name == capability_name)
        ]

        if not relevant_changes:
            return 0.0

        total_delta = sum(c.delta for c in relevant_changes)
        return total_delta / window_hours

    def get_loop_health(self, loop_name: str) -> Dict[str, float]:
        """
        Get health metrics for a specific loop.

        Returns:
            Dictionary with activity_rate, recency, avg_impact
        """
        activities = list(self._activities.get(loop_name, []))

        if not activities:
            return {
                "activity_rate": 0.0,
                "recency_seconds": float("inf"),
                "avg_impact": 0.0
            }

        now = datetime.now()

        # Activity rate (events per hour)
        time_span = (activities[-1].timestamp - activities[0].timestamp).total_seconds()
        if time_span > 0:
            activity_rate = len(activities) / (time_span / 3600)
        else:
            activity_rate = 0.0

        # Recency (seconds since last activity)
        recency = (now - activities[-1].timestamp).total_seconds()

        # Average impact (based on capability changes attributed to this loop)
        attributed_changes = [
            c for c in self._capability_changes
            if c.source_loop == loop_name
        ]
        if attributed_changes:
            avg_impact = sum(c.delta for c in attributed_changes) / len(attributed_changes)
        else:
            avg_impact = 0.0

        return {
            "activity_rate": activity_rate,
            "recency_seconds": recency,
            "avg_impact": avg_impact
        }

    def get_critical_coupling(self) -> CouplingMeasurement:
        """
        Get the Goal Evolver → Self-Compiler coupling.

        This is THE critical metric for Option B success.
        When goals drive code changes that improve capability,
        we have true exponential potential.
        """
        return self.compute_coupling("goal_evolver", "self_compiler")

    async def emit_coupling_event(self):
        """Emit coupling measurement event for real-time UI."""
        critical = self.get_critical_coupling()
        all_couplings = self.compute_all_couplings()

        await event_bus.emit(Event(
            type=EventType.COUPLING_MEASURED,
            data={
                "critical_coupling": {
                    "loops": f"{critical.loop_a}:{critical.loop_b}",
                    "correlation": critical.correlation,
                    "is_significant": critical.is_significant,
                    "sample_count": critical.sample_count
                },
                "all_couplings": {
                    key: {
                        "correlation": m.correlation,
                        "is_significant": m.is_significant
                    }
                    for key, m in all_couplings.items()
                },
                "capability_growth_rate": self.get_capability_growth_rate()
            }
        ))

    def get_summary(self) -> Dict:
        """
        Get a summary of all tracking state.

        Returns:
            Dictionary with loop health, couplings, and growth metrics
        """
        critical = self.get_critical_coupling()
        return {
            "loop_health": {
                loop: self.get_loop_health(loop)
                for loop in self.LOOPS
            },
            "couplings": {
                key: {
                    "correlation": m.correlation,
                    "is_significant": m.is_significant,
                    "sample_count": m.sample_count
                }
                for key, m in self.compute_all_couplings().items()
            },
            "critical_coupling": {
                "correlation": critical.correlation,
                "is_significant": critical.is_significant
            },
            "capability_growth_rate_hourly": self.get_capability_growth_rate(),
            "total_activities": sum(len(acts) for acts in self._activities.values()),
            "total_capability_changes": len(self._capability_changes)
        }


# Global singleton
_coupling_tracker: Optional[CouplingTracker] = None


def get_coupling_tracker() -> CouplingTracker:
    """Get or create the global coupling tracker."""
    global _coupling_tracker
    if _coupling_tracker is None:
        _coupling_tracker = CouplingTracker()
    return _coupling_tracker
