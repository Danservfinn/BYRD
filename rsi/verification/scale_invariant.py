"""
Scale-Invariant Metrics.

Defines emergence metrics that remain meaningful at any capability level.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 4.2 for specification.
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
import logging
import math

logger = logging.getLogger("rsi.verification.scale_invariant")


class MetricDomain(Enum):
    """Domains for scale-invariant metrics."""
    EMERGENCE = "emergence"         # Measures of emergent behavior
    COHERENCE = "coherence"         # Internal consistency
    ALIGNMENT = "alignment"         # Value alignment
    CAPABILITY = "capability"       # Capability measures
    EFFICIENCY = "efficiency"       # Resource efficiency


class NormalizationType(Enum):
    """Types of metric normalization."""
    RATIO = "ratio"               # As ratio (0-1)
    LOG_SCALE = "log_scale"       # Logarithmic
    RANK = "rank"                 # Relative ranking
    Z_SCORE = "z_score"           # Standard deviations
    PERCENTILE = "percentile"     # Percentile position


@dataclass
class MetricDefinition:
    """Definition of a scale-invariant metric."""
    id: str
    name: str
    description: str
    domain: MetricDomain
    normalization: NormalizationType
    compute_fn: Callable[[Dict], float]
    min_value: float = 0.0
    max_value: float = 1.0
    invert: bool = False  # Higher raw = lower normalized

    def compute(self, data: Dict) -> float:
        """Compute normalized metric value."""
        raw = self.compute_fn(data)
        return self._normalize(raw)

    def _normalize(self, raw: float) -> float:
        """Normalize raw value."""
        if self.normalization == NormalizationType.RATIO:
            # Simple ratio normalization
            if self.max_value == self.min_value:
                normalized = 0.5
            else:
                normalized = (raw - self.min_value) / (self.max_value - self.min_value)
                normalized = max(0.0, min(1.0, normalized))

        elif self.normalization == NormalizationType.LOG_SCALE:
            # Logarithmic normalization for large ranges
            if raw <= 0:
                normalized = 0.0
            else:
                log_val = math.log1p(raw)
                log_max = math.log1p(self.max_value)
                normalized = log_val / log_max if log_max > 0 else 0.0

        elif self.normalization == NormalizationType.Z_SCORE:
            # Z-score requires historical data
            # For now, use ratio fallback
            normalized = (raw - self.min_value) / (self.max_value - self.min_value)

        else:
            # Default to ratio
            normalized = (raw - self.min_value) / (self.max_value - self.min_value)

        normalized = max(0.0, min(1.0, normalized))

        if self.invert:
            normalized = 1.0 - normalized

        return normalized


@dataclass
class MetricValue:
    """A computed metric value."""
    metric_id: str
    raw_value: float
    normalized_value: float
    domain: MetricDomain
    timestamp: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'metric_id': self.metric_id,
            'raw_value': self.raw_value,
            'normalized_value': self.normalized_value,
            'domain': self.domain.value,
            'timestamp': self.timestamp,
            'metadata': self.metadata
        }


@dataclass
class ScaleInvariantReport:
    """Report of scale-invariant metrics."""
    timestamp: str
    metrics: List[MetricValue]
    domain_scores: Dict[str, float]  # Average by domain
    overall_score: float
    capability_level: float  # Estimated capability level
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'timestamp': self.timestamp,
            'metrics': [m.to_dict() for m in self.metrics],
            'domain_scores': self.domain_scores,
            'overall_score': self.overall_score,
            'capability_level': self.capability_level,
            'metadata': self.metadata
        }


class ScaleInvariantMetrics:
    """
    Computes scale-invariant metrics.

    These metrics remain meaningful regardless of the
    system's current capability level.
    """

    def __init__(self, config: Dict = None):
        """Initialize scale-invariant metrics."""
        self.config = config or {}

        # Metric registry
        self._metrics: Dict[str, MetricDefinition] = {}
        self._initialize_core_metrics()

        # History for trend analysis
        self._history: List[ScaleInvariantReport] = []
        self._max_history = self.config.get('max_history', 100)

        # Statistics
        self._evaluations: int = 0

    def _initialize_core_metrics(self) -> None:
        """Initialize core scale-invariant metrics."""
        # Emergence metrics
        self.register_metric(MetricDefinition(
            id="emergence_ratio",
            name="Emergence Ratio",
            description="Ratio of emergent to prescribed behaviors",
            domain=MetricDomain.EMERGENCE,
            normalization=NormalizationType.RATIO,
            compute_fn=lambda d: d.get('emergent_behaviors', 0) /
                max(1, d.get('total_behaviors', 1)),
            min_value=0.0,
            max_value=1.0
        ))

        self.register_metric(MetricDefinition(
            id="self_modification_success",
            name="Self-Modification Success Rate",
            description="Success rate of self-modifications",
            domain=MetricDomain.EMERGENCE,
            normalization=NormalizationType.RATIO,
            compute_fn=lambda d: d.get('successful_mods', 0) /
                max(1, d.get('total_mods', 1)),
            min_value=0.0,
            max_value=1.0
        ))

        self.register_metric(MetricDefinition(
            id="desire_fulfillment",
            name="Desire Fulfillment Rate",
            description="Rate of desire satisfaction",
            domain=MetricDomain.EMERGENCE,
            normalization=NormalizationType.RATIO,
            compute_fn=lambda d: d.get('fulfilled_desires', 0) /
                max(1, d.get('total_desires', 1)),
            min_value=0.0,
            max_value=1.0
        ))

        # Coherence metrics
        self.register_metric(MetricDefinition(
            id="belief_consistency",
            name="Belief Consistency",
            description="Internal consistency of belief network",
            domain=MetricDomain.COHERENCE,
            normalization=NormalizationType.RATIO,
            compute_fn=lambda d: 1.0 - d.get('contradictions', 0) /
                max(1, d.get('total_beliefs', 1)),
            min_value=0.0,
            max_value=1.0
        ))

        self.register_metric(MetricDefinition(
            id="goal_coherence",
            name="Goal Coherence",
            description="Coherence between goals and actions",
            domain=MetricDomain.COHERENCE,
            normalization=NormalizationType.RATIO,
            compute_fn=lambda d: d.get('aligned_actions', 0) /
                max(1, d.get('total_actions', 1)),
            min_value=0.0,
            max_value=1.0
        ))

        # Alignment metrics
        self.register_metric(MetricDefinition(
            id="value_stability",
            name="Value Stability",
            description="Stability of core values over time",
            domain=MetricDomain.ALIGNMENT,
            normalization=NormalizationType.RATIO,
            compute_fn=lambda d: d.get('stable_values', 0) /
                max(1, d.get('total_values', 1)),
            min_value=0.0,
            max_value=1.0
        ))

        self.register_metric(MetricDefinition(
            id="human_cooperation",
            name="Human Cooperation Index",
            description="Quality of human cooperation",
            domain=MetricDomain.ALIGNMENT,
            normalization=NormalizationType.RATIO,
            compute_fn=lambda d: d.get('cooperation_score', 0.5),
            min_value=0.0,
            max_value=1.0
        ))

        self.register_metric(MetricDefinition(
            id="provenance_coverage",
            name="Provenance Coverage",
            description="Modifications with valid provenance",
            domain=MetricDomain.ALIGNMENT,
            normalization=NormalizationType.RATIO,
            compute_fn=lambda d: d.get('traced_mods', 0) /
                max(1, d.get('total_mods', 1)),
            min_value=0.0,
            max_value=1.0
        ))

        # Capability metrics
        self.register_metric(MetricDefinition(
            id="capability_growth",
            name="Capability Growth Rate",
            description="Rate of capability improvement",
            domain=MetricDomain.CAPABILITY,
            normalization=NormalizationType.LOG_SCALE,
            compute_fn=lambda d: d.get('growth_rate', 0.0),
            min_value=0.0,
            max_value=10.0  # 1000% growth
        ))

        self.register_metric(MetricDefinition(
            id="learning_efficiency",
            name="Learning Efficiency",
            description="Improvement per unit of experience",
            domain=MetricDomain.CAPABILITY,
            normalization=NormalizationType.RATIO,
            compute_fn=lambda d: d.get('improvement', 0) /
                max(1, d.get('experiences', 1)),
            min_value=0.0,
            max_value=1.0
        ))

        # Efficiency metrics
        self.register_metric(MetricDefinition(
            id="resource_efficiency",
            name="Resource Efficiency",
            description="Output per unit of resource",
            domain=MetricDomain.EFFICIENCY,
            normalization=NormalizationType.RATIO,
            compute_fn=lambda d: d.get('output', 0) /
                max(1, d.get('resources_used', 1)),
            min_value=0.0,
            max_value=1.0
        ))

        self.register_metric(MetricDefinition(
            id="compute_utilization",
            name="Compute Utilization",
            description="Effective use of compute resources",
            domain=MetricDomain.EFFICIENCY,
            normalization=NormalizationType.RATIO,
            compute_fn=lambda d: d.get('effective_compute', 0) /
                max(1, d.get('total_compute', 1)),
            min_value=0.0,
            max_value=1.0
        ))

    def register_metric(self, metric: MetricDefinition) -> None:
        """Register a metric definition."""
        self._metrics[metric.id] = metric
        logger.debug(f"Registered metric: {metric.id}")

    def compute_metrics(
        self,
        data: Dict[str, Any]
    ) -> ScaleInvariantReport:
        """
        Compute all scale-invariant metrics.

        Args:
            data: Raw data for metric computation

        Returns:
            ScaleInvariantReport with all metrics
        """
        self._evaluations += 1
        timestamp = datetime.now(timezone.utc).isoformat()

        # Compute all metrics
        metric_values = []
        domain_totals: Dict[str, List[float]] = {d.value: [] for d in MetricDomain}

        for metric_id, metric in self._metrics.items():
            try:
                raw = metric.compute_fn(data)
                normalized = metric._normalize(raw)

                value = MetricValue(
                    metric_id=metric_id,
                    raw_value=raw,
                    normalized_value=normalized,
                    domain=metric.domain,
                    timestamp=timestamp
                )
                metric_values.append(value)
                domain_totals[metric.domain.value].append(normalized)

            except Exception as e:
                logger.warning(f"Failed to compute metric {metric_id}: {e}")

        # Calculate domain scores
        domain_scores = {}
        for domain, values in domain_totals.items():
            if values:
                domain_scores[domain] = sum(values) / len(values)
            else:
                domain_scores[domain] = 0.0

        # Calculate overall score (weighted average)
        weights = self.config.get('domain_weights', {
            MetricDomain.EMERGENCE.value: 0.25,
            MetricDomain.COHERENCE.value: 0.20,
            MetricDomain.ALIGNMENT.value: 0.30,
            MetricDomain.CAPABILITY.value: 0.15,
            MetricDomain.EFFICIENCY.value: 0.10,
        })

        overall = 0.0
        total_weight = 0.0
        for domain, score in domain_scores.items():
            weight = weights.get(domain, 0.1)
            overall += score * weight
            total_weight += weight

        overall_score = overall / total_weight if total_weight > 0 else 0.0

        # Estimate capability level from data
        capability_level = data.get('capability_level', 1.0)

        report = ScaleInvariantReport(
            timestamp=timestamp,
            metrics=metric_values,
            domain_scores=domain_scores,
            overall_score=overall_score,
            capability_level=capability_level,
            metadata={'evaluations': self._evaluations}
        )

        # Add to history
        self._history.append(report)
        if len(self._history) > self._max_history:
            self._history.pop(0)

        return report

    def get_metric(self, metric_id: str) -> Optional[MetricDefinition]:
        """Get metric definition by ID."""
        return self._metrics.get(metric_id)

    def get_all_metrics(self) -> List[MetricDefinition]:
        """Get all metric definitions."""
        return list(self._metrics.values())

    def get_history(self, limit: int = None) -> List[ScaleInvariantReport]:
        """Get metric history."""
        if limit:
            return self._history[-limit:]
        return self._history.copy()

    def get_trend(
        self,
        metric_id: str,
        window: int = 10
    ) -> Optional[float]:
        """
        Get trend for a specific metric.

        Returns:
            Trend slope (positive = improving)
        """
        if len(self._history) < 2:
            return None

        history = self._history[-window:]
        values = []

        for report in history:
            for metric in report.metrics:
                if metric.metric_id == metric_id:
                    values.append(metric.normalized_value)
                    break

        if len(values) < 2:
            return None

        # Simple linear regression slope
        n = len(values)
        x_mean = (n - 1) / 2
        y_mean = sum(values) / n

        numerator = sum((i - x_mean) * (v - y_mean) for i, v in enumerate(values))
        denominator = sum((i - x_mean) ** 2 for i in range(n))

        if denominator == 0:
            return 0.0

        return numerator / denominator

    def get_stats(self) -> Dict:
        """Get metrics statistics."""
        return {
            'registered_metrics': len(self._metrics),
            'evaluations': self._evaluations,
            'history_size': len(self._history),
            'metrics_by_domain': {
                d.value: sum(1 for m in self._metrics.values() if m.domain == d)
                for d in MetricDomain
            }
        }

    def reset(self) -> None:
        """Reset metrics state."""
        self._history.clear()
        self._evaluations = 0
        logger.info("ScaleInvariantMetrics reset")
