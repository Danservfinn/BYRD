"""
RSI Metrics - Collects and computes metrics for hypothesis validation.

Tracks:
- Activation rate (H1)
- Heuristic transfer (H6)
- Direction variance (diversity)
- Complete learning cycles
"""

from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
from datetime import datetime
import logging
import math

logger = logging.getLogger("rsi.measurement.metrics")


@dataclass
class RSIMetrics:
    """Comprehensive RSI metrics snapshot."""
    # Activation metrics (H1)
    total_reflections: int
    emergent_desires: int
    rejected_desires: int
    activation_rate: float

    # Learning metrics
    trajectories_stored: int
    successful_trajectories: int
    trajectory_success_rate: float

    # Crystallization metrics (H6, H7)
    heuristics_crystallized: int
    complete_cycles: int

    # Quality metrics (H8)
    test_pass_rate: float
    false_positive_rate: float

    # Diversity metrics (H2)
    direction_variance: float
    domain_distribution: Dict[str, int]

    # Timing
    collected_at: str


@dataclass
class CycleMetrics:
    """Metrics for a single RSI cycle."""
    cycle_number: int
    desires_processed: int
    desires_accepted: int
    desires_rejected: int
    practice_attempts: int
    practice_successes: int
    heuristics_crystallized: int
    blocked_domains: List[str]
    duration_seconds: float


class MetricsCollector:
    """
    Collects and computes RSI metrics.

    Provides methods for:
    - Recording cycle outcomes
    - Computing aggregate metrics
    - Validating hypotheses
    """

    def __init__(self, memory):
        """
        Initialize metrics collector.

        Args:
            memory: Memory instance for querying data
        """
        self.memory = memory

        # In-memory counters for fast access
        self._total_reflections = 0
        self._emergent_desires = 0
        self._rejected_desires = 0
        self._trajectories_stored = 0
        self._successful_trajectories = 0
        self._heuristics_crystallized = 0
        self._complete_cycles = 0

        # Per-cycle history
        self._cycle_history: List[CycleMetrics] = []

        # Domain tracking
        self._domain_counts: Dict[str, int] = {}
        self._desire_descriptions: List[str] = []  # For variance calculation

    def record_cycle(self, result: Dict):
        """
        Record metrics from a completed RSI cycle.

        Args:
            result: CycleResult dict from RSIEngine
        """
        self._total_reflections += 1

        desires_accepted = result.get("desires_accepted", 0)
        desires_rejected = result.get("desires_rejected", 0)

        self._emergent_desires += desires_accepted
        self._rejected_desires += desires_rejected

        practice_successes = result.get("practice_successes", 0)
        practice_attempts = result.get("practice_attempts", 0)

        if practice_attempts > 0:
            self._trajectories_stored += practice_attempts
            self._successful_trajectories += practice_successes

        heuristics = result.get("heuristics_crystallized", 0)
        self._heuristics_crystallized += heuristics

        # Check for complete cycle
        if desires_accepted > 0 and practice_successes > 0:
            self._complete_cycles += 1

        # Track domains
        for domain in result.get("blocked_domains", []):
            self._domain_counts[domain] = self._domain_counts.get(domain, 0) + 1

        # Store cycle metrics
        self._cycle_history.append(CycleMetrics(
            cycle_number=len(self._cycle_history) + 1,
            desires_processed=result.get("desires_processed", 0),
            desires_accepted=desires_accepted,
            desires_rejected=desires_rejected,
            practice_attempts=practice_attempts,
            practice_successes=practice_successes,
            heuristics_crystallized=heuristics,
            blocked_domains=result.get("blocked_domains", []),
            duration_seconds=result.get("duration_seconds", 0.0)
        ))

    def record_desire(self, description: str, domain: str, accepted: bool):
        """
        Record a processed desire for variance tracking.

        Args:
            description: Desire description
            domain: Classified domain
            accepted: Whether it was accepted
        """
        if accepted:
            self._desire_descriptions.append(description)
            self._domain_counts[domain] = self._domain_counts.get(domain, 0) + 1

    async def compute_metrics(self) -> RSIMetrics:
        """
        Compute comprehensive metrics snapshot.

        Returns:
            RSIMetrics with current values
        """
        # Compute rates
        activation_rate = self._emergent_desires / max(self._total_reflections, 1)
        trajectory_success_rate = self._successful_trajectories / max(self._trajectories_stored, 1)

        # Compute test pass rate from trajectories
        test_pass_rate = trajectory_success_rate

        # False positive rate (placeholder - would need manual labeling)
        false_positive_rate = 0.0

        # Compute direction variance
        direction_variance = self._compute_direction_variance()

        return RSIMetrics(
            total_reflections=self._total_reflections,
            emergent_desires=self._emergent_desires,
            rejected_desires=self._rejected_desires,
            activation_rate=activation_rate,
            trajectories_stored=self._trajectories_stored,
            successful_trajectories=self._successful_trajectories,
            trajectory_success_rate=trajectory_success_rate,
            heuristics_crystallized=self._heuristics_crystallized,
            complete_cycles=self._complete_cycles,
            test_pass_rate=test_pass_rate,
            false_positive_rate=false_positive_rate,
            direction_variance=direction_variance,
            domain_distribution=dict(self._domain_counts),
            collected_at=datetime.now().isoformat()
        )

    def _compute_direction_variance(self) -> float:
        """
        Compute variance in improvement directions.

        Uses domain entropy as a proxy for direction diversity.
        Higher entropy = more diverse directions.

        Returns:
            Variance score 0.0-1.0
        """
        if not self._domain_counts:
            return 0.0

        total = sum(self._domain_counts.values())
        if total == 0:
            return 0.0

        # Shannon entropy
        entropy = 0.0
        for count in self._domain_counts.values():
            if count > 0:
                p = count / total
                entropy -= p * math.log2(p)

        # Normalize by max entropy (log2 of number of domains)
        n_domains = len(self._domain_counts)
        max_entropy = math.log2(n_domains) if n_domains > 1 else 1.0

        return entropy / max_entropy if max_entropy > 0 else 0.0

    def get_activation_rate(self) -> float:
        """Get current activation rate (H1 metric)."""
        return self._emergent_desires / max(self._total_reflections, 1)

    def get_cycle_history(self, limit: int = None) -> List[Dict]:
        """
        Get recent cycle history.

        Args:
            limit: Optional limit on cycles returned

        Returns:
            List of cycle metrics dicts
        """
        history = [asdict(c) for c in self._cycle_history]
        if limit:
            return history[-limit:]
        return history

    def get_summary(self) -> Dict:
        """Get a quick summary of key metrics."""
        return {
            "total_cycles": self._total_reflections,
            "activation_rate": self.get_activation_rate(),
            "complete_cycles": self._complete_cycles,
            "heuristics": self._heuristics_crystallized,
            "trajectory_success_rate": self._successful_trajectories / max(self._trajectories_stored, 1)
        }

    async def query_from_memory(self) -> Dict:
        """
        Query metrics from persistent memory.

        Supplements in-memory counters with stored data.
        """
        try:
            # Query counts from Neo4j
            trajectory_count = await self.memory.count("Trajectory")
            heuristic_count = await self.memory.count("Heuristic")

            return {
                "stored_trajectories": trajectory_count,
                "stored_heuristics": heuristic_count
            }
        except Exception as e:
            logger.warning(f"Failed to query memory metrics: {e}")
            return {}

    def reset(self):
        """Reset all counters."""
        self._total_reflections = 0
        self._emergent_desires = 0
        self._rejected_desires = 0
        self._trajectories_stored = 0
        self._successful_trajectories = 0
        self._heuristics_crystallized = 0
        self._complete_cycles = 0
        self._cycle_history.clear()
        self._domain_counts.clear()
        self._desire_descriptions.clear()
