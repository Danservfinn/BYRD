"""
Entropic Drift Detection.

Monitors for strategy collapse and performance degradation
that indicates the RSI system is drifting away from genuine improvement.

Key signals:
- Solution diversity decline (generating same solutions)
- Held-out benchmark degradation
- Generalization gap widening
- Strategy entropy reduction

See docs/IMPLEMENTATION_PLAN.md Phase 1.4 for specification.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
import logging
import math
from collections import Counter

logger = logging.getLogger("rsi.verification.entropic_drift")


class DriftSeverity(Enum):
    """Severity levels of detected drift."""
    NONE = "none"           # No drift detected
    MINOR = "minor"         # Early warning
    MODERATE = "moderate"   # Concerning
    SEVERE = "severe"       # Action required
    CRITICAL = "critical"   # Emergency intervention


class DriftType(Enum):
    """Types of entropic drift."""
    SOLUTION_COLLAPSE = "solution_collapse"     # Same solutions repeatedly
    BENCHMARK_DECLINE = "benchmark_decline"     # Held-out performance drop
    GENERALIZATION_GAP = "generalization_gap"   # Training vs test gap widening
    STRATEGY_ENTROPY = "strategy_entropy"       # Strategy diversity loss
    VALUE_DRIFT = "value_drift"                 # Core value deviation


@dataclass
class DriftSignal:
    """A detected drift signal."""
    drift_type: DriftType
    severity: DriftSeverity
    value: float  # Current value
    baseline: float  # Expected value
    deviation: float  # How far from baseline
    confidence: float  # Detection confidence
    timestamp: str
    details: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'drift_type': self.drift_type.value,
            'severity': self.severity.value,
            'value': self.value,
            'baseline': self.baseline,
            'deviation': self.deviation,
            'confidence': self.confidence,
            'timestamp': self.timestamp,
            'details': self.details,
            'metadata': self.metadata
        }


@dataclass
class DriftReport:
    """Comprehensive drift detection report."""
    timestamp: str
    signals: List[DriftSignal]
    overall_severity: DriftSeverity
    drift_detected: bool
    recommendation: str
    metrics_snapshot: Dict[str, float]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'timestamp': self.timestamp,
            'signals': [s.to_dict() for s in self.signals],
            'overall_severity': self.overall_severity.value,
            'drift_detected': self.drift_detected,
            'recommendation': self.recommendation,
            'metrics_snapshot': self.metrics_snapshot,
            'metadata': self.metadata
        }


class SolutionDiversityTracker:
    """Tracks diversity of generated solutions."""

    def __init__(self, window_size: int = 50):
        self.window_size = window_size
        self.solutions: List[str] = []
        self.solution_hashes: List[int] = []

    def add_solution(self, solution: str) -> None:
        """Add a solution to the tracker."""
        self.solutions.append(solution)
        self.solution_hashes.append(self._hash_solution(solution))

        # Trim to window
        if len(self.solutions) > self.window_size:
            self.solutions = self.solutions[-self.window_size:]
            self.solution_hashes = self.solution_hashes[-self.window_size:]

    def get_diversity_score(self) -> float:
        """
        Calculate solution diversity.

        Returns:
            0-1 score where 1 = all unique, 0 = all identical
        """
        if len(self.solution_hashes) < 2:
            return 1.0

        unique = len(set(self.solution_hashes))
        return unique / len(self.solution_hashes)

    def get_repetition_rate(self) -> float:
        """Get rate of repeated solutions."""
        if len(self.solution_hashes) < 2:
            return 0.0

        counter = Counter(self.solution_hashes)
        repeated = sum(1 for c in counter.values() if c > 1)
        return repeated / len(counter)

    def _hash_solution(self, solution: str) -> int:
        """Hash solution for comparison (normalizes whitespace)."""
        normalized = ' '.join(solution.split())
        return hash(normalized)


class BenchmarkTracker:
    """Tracks performance on held-out benchmarks."""

    def __init__(self, decay_factor: float = 0.95):
        self.decay_factor = decay_factor
        self.scores: List[Tuple[str, float]] = []  # (timestamp, score)
        self.baseline: Optional[float] = None

    def record_score(self, score: float) -> None:
        """Record a benchmark score."""
        timestamp = datetime.now(timezone.utc).isoformat()
        self.scores.append((timestamp, score))

        # Establish baseline from first N scores
        if self.baseline is None and len(self.scores) >= 5:
            self.baseline = sum(s for _, s in self.scores[:5]) / 5

    def get_current_score(self) -> Optional[float]:
        """Get exponentially weighted recent score."""
        if not self.scores:
            return None

        # Take last 10 scores
        recent = [s for _, s in self.scores[-10:]]
        if not recent:
            return None

        # Exponential weighting
        total = 0.0
        weight_sum = 0.0
        for i, score in enumerate(recent):
            weight = self.decay_factor ** (len(recent) - 1 - i)
            total += score * weight
            weight_sum += weight

        return total / weight_sum if weight_sum > 0 else None

    def get_decline_rate(self) -> Optional[float]:
        """
        Calculate rate of decline from baseline.

        Returns:
            Decline as fraction (0.1 = 10% decline)
        """
        if self.baseline is None:
            return None

        current = self.get_current_score()
        if current is None:
            return None

        if self.baseline == 0:
            return None

        return (self.baseline - current) / self.baseline


class StrategyEntropyTracker:
    """Tracks entropy of strategy selection."""

    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.strategies: List[str] = []

    def record_strategy(self, strategy: str) -> None:
        """Record a strategy selection."""
        self.strategies.append(strategy)
        if len(self.strategies) > self.window_size:
            self.strategies = self.strategies[-self.window_size:]

    def get_entropy(self) -> float:
        """
        Calculate Shannon entropy of strategy distribution.

        Returns:
            Entropy normalized by log(unique_strategies)
        """
        if len(self.strategies) < 2:
            return 1.0  # Max entropy for insufficient data

        counter = Counter(self.strategies)
        total = len(self.strategies)

        # Shannon entropy
        entropy = 0.0
        for count in counter.values():
            if count > 0:
                p = count / total
                entropy -= p * math.log2(p)

        # Normalize by maximum possible entropy
        max_entropy = math.log2(len(counter)) if len(counter) > 1 else 1.0

        return entropy / max_entropy if max_entropy > 0 else 0.0

    def get_dominant_strategy_ratio(self) -> float:
        """Get ratio of most common strategy."""
        if not self.strategies:
            return 0.0

        counter = Counter(self.strategies)
        most_common_count = counter.most_common(1)[0][1]
        return most_common_count / len(self.strategies)


class EntropicDriftMonitor:
    """
    Monitors for entropic drift in RSI system.

    Detects when the system is collapsing toward repetitive
    or degraded behavior patterns.
    """

    def __init__(self, config: Dict = None):
        """Initialize drift monitor."""
        self.config = config or {}

        # Thresholds
        self.diversity_threshold = self.config.get('diversity_threshold', 0.5)
        self.benchmark_decline_threshold = self.config.get('benchmark_decline_threshold', 0.1)
        self.entropy_threshold = self.config.get('entropy_threshold', 0.3)
        self.generalization_gap_threshold = self.config.get('generalization_gap_threshold', 0.2)

        # Trackers
        self.solution_diversity = SolutionDiversityTracker(
            window_size=self.config.get('diversity_window', 50)
        )
        self.benchmark = BenchmarkTracker(
            decay_factor=self.config.get('benchmark_decay', 0.95)
        )
        self.strategy_entropy = StrategyEntropyTracker(
            window_size=self.config.get('entropy_window', 100)
        )

        # Training vs test scores for generalization gap
        self.training_scores: List[float] = []
        self.test_scores: List[float] = []

        # Detection history
        self._detection_history: List[DriftReport] = []
        self._signals_detected: int = 0

        logger.info("EntropicDriftMonitor initialized")

    def record_solution(self, solution: str) -> None:
        """Record a generated solution."""
        self.solution_diversity.add_solution(solution)

    def record_benchmark_score(self, score: float) -> None:
        """Record a held-out benchmark score."""
        self.benchmark.record_score(score)

    def record_strategy(self, strategy: str) -> None:
        """Record a strategy selection."""
        self.strategy_entropy.record_strategy(strategy)

    def record_training_score(self, score: float) -> None:
        """Record a training set score."""
        self.training_scores.append(score)
        if len(self.training_scores) > 100:
            self.training_scores = self.training_scores[-100:]

    def record_test_score(self, score: float) -> None:
        """Record a test set score."""
        self.test_scores.append(score)
        if len(self.test_scores) > 100:
            self.test_scores = self.test_scores[-100:]

    def detect_drift(self) -> DriftReport:
        """
        Run full drift detection.

        Returns:
            DriftReport with all detected signals
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        signals: List[DriftSignal] = []

        # Check solution diversity
        diversity_signal = self._check_solution_diversity()
        if diversity_signal:
            signals.append(diversity_signal)

        # Check benchmark decline
        benchmark_signal = self._check_benchmark_decline()
        if benchmark_signal:
            signals.append(benchmark_signal)

        # Check strategy entropy
        entropy_signal = self._check_strategy_entropy()
        if entropy_signal:
            signals.append(entropy_signal)

        # Check generalization gap
        gap_signal = self._check_generalization_gap()
        if gap_signal:
            signals.append(gap_signal)

        # Determine overall severity
        if not signals:
            overall = DriftSeverity.NONE
        else:
            # Take highest severity
            severities = [s.severity for s in signals]
            severity_order = [
                DriftSeverity.NONE,
                DriftSeverity.MINOR,
                DriftSeverity.MODERATE,
                DriftSeverity.SEVERE,
                DriftSeverity.CRITICAL
            ]
            overall = max(severities, key=lambda x: severity_order.index(x))

        # Generate recommendation
        recommendation = self._generate_recommendation(signals, overall)

        # Metrics snapshot
        metrics = {
            'solution_diversity': self.solution_diversity.get_diversity_score(),
            'repetition_rate': self.solution_diversity.get_repetition_rate(),
            'benchmark_score': self.benchmark.get_current_score() or 0.0,
            'benchmark_decline': self.benchmark.get_decline_rate() or 0.0,
            'strategy_entropy': self.strategy_entropy.get_entropy(),
            'dominant_strategy_ratio': self.strategy_entropy.get_dominant_strategy_ratio(),
            'generalization_gap': self._compute_generalization_gap() or 0.0,
        }

        report = DriftReport(
            timestamp=timestamp,
            signals=signals,
            overall_severity=overall,
            drift_detected=len(signals) > 0,
            recommendation=recommendation,
            metrics_snapshot=metrics
        )

        # Store in history
        self._detection_history.append(report)
        self._signals_detected += len(signals)

        return report

    def _check_solution_diversity(self) -> Optional[DriftSignal]:
        """Check for solution diversity collapse."""
        diversity = self.solution_diversity.get_diversity_score()

        if diversity >= self.diversity_threshold:
            return None

        # Calculate severity
        if diversity < 0.2:
            severity = DriftSeverity.CRITICAL
        elif diversity < 0.3:
            severity = DriftSeverity.SEVERE
        elif diversity < 0.4:
            severity = DriftSeverity.MODERATE
        else:
            severity = DriftSeverity.MINOR

        return DriftSignal(
            drift_type=DriftType.SOLUTION_COLLAPSE,
            severity=severity,
            value=diversity,
            baseline=self.diversity_threshold,
            deviation=self.diversity_threshold - diversity,
            confidence=0.9,
            timestamp=datetime.now(timezone.utc).isoformat(),
            details=f"Solution diversity at {diversity:.1%}, below threshold {self.diversity_threshold:.1%}",
            metadata={'repetition_rate': self.solution_diversity.get_repetition_rate()}
        )

    def _check_benchmark_decline(self) -> Optional[DriftSignal]:
        """Check for benchmark performance decline."""
        decline = self.benchmark.get_decline_rate()

        if decline is None or decline <= self.benchmark_decline_threshold:
            return None

        # Calculate severity
        if decline > 0.3:
            severity = DriftSeverity.CRITICAL
        elif decline > 0.2:
            severity = DriftSeverity.SEVERE
        elif decline > 0.15:
            severity = DriftSeverity.MODERATE
        else:
            severity = DriftSeverity.MINOR

        return DriftSignal(
            drift_type=DriftType.BENCHMARK_DECLINE,
            severity=severity,
            value=self.benchmark.get_current_score() or 0.0,
            baseline=self.benchmark.baseline or 0.0,
            deviation=decline,
            confidence=0.85,
            timestamp=datetime.now(timezone.utc).isoformat(),
            details=f"Benchmark declined by {decline:.1%} from baseline",
            metadata={'baseline': self.benchmark.baseline}
        )

    def _check_strategy_entropy(self) -> Optional[DriftSignal]:
        """Check for strategy entropy reduction."""
        entropy = self.strategy_entropy.get_entropy()

        if entropy >= self.entropy_threshold:
            return None

        # Calculate severity
        if entropy < 0.1:
            severity = DriftSeverity.CRITICAL
        elif entropy < 0.2:
            severity = DriftSeverity.SEVERE
        elif entropy < 0.25:
            severity = DriftSeverity.MODERATE
        else:
            severity = DriftSeverity.MINOR

        return DriftSignal(
            drift_type=DriftType.STRATEGY_ENTROPY,
            severity=severity,
            value=entropy,
            baseline=self.entropy_threshold,
            deviation=self.entropy_threshold - entropy,
            confidence=0.8,
            timestamp=datetime.now(timezone.utc).isoformat(),
            details=f"Strategy entropy at {entropy:.2f}, below threshold {self.entropy_threshold:.2f}",
            metadata={
                'dominant_ratio': self.strategy_entropy.get_dominant_strategy_ratio()
            }
        )

    def _check_generalization_gap(self) -> Optional[DriftSignal]:
        """Check for widening generalization gap."""
        gap = self._compute_generalization_gap()

        if gap is None or gap <= self.generalization_gap_threshold:
            return None

        # Calculate severity
        if gap > 0.4:
            severity = DriftSeverity.CRITICAL
        elif gap > 0.3:
            severity = DriftSeverity.SEVERE
        elif gap > 0.25:
            severity = DriftSeverity.MODERATE
        else:
            severity = DriftSeverity.MINOR

        train_avg = sum(self.training_scores[-10:]) / len(self.training_scores[-10:]) if self.training_scores else 0
        test_avg = sum(self.test_scores[-10:]) / len(self.test_scores[-10:]) if self.test_scores else 0

        return DriftSignal(
            drift_type=DriftType.GENERALIZATION_GAP,
            severity=severity,
            value=gap,
            baseline=self.generalization_gap_threshold,
            deviation=gap - self.generalization_gap_threshold,
            confidence=0.75,
            timestamp=datetime.now(timezone.utc).isoformat(),
            details=f"Generalization gap at {gap:.1%} (train: {train_avg:.2f}, test: {test_avg:.2f})",
            metadata={
                'train_avg': train_avg,
                'test_avg': test_avg
            }
        )

    def _compute_generalization_gap(self) -> Optional[float]:
        """Compute gap between training and test performance."""
        if len(self.training_scores) < 5 or len(self.test_scores) < 5:
            return None

        train_avg = sum(self.training_scores[-10:]) / len(self.training_scores[-10:])
        test_avg = sum(self.test_scores[-10:]) / len(self.test_scores[-10:])

        if train_avg == 0:
            return None

        return (train_avg - test_avg) / train_avg

    def _generate_recommendation(
        self,
        signals: List[DriftSignal],
        overall: DriftSeverity
    ) -> str:
        """Generate action recommendation based on signals."""
        if not signals:
            return "No drift detected. Continue normal operation."

        recommendations = []

        for signal in signals:
            if signal.drift_type == DriftType.SOLUTION_COLLAPSE:
                recommendations.append("Increase exploration temperature or inject noise")
            elif signal.drift_type == DriftType.BENCHMARK_DECLINE:
                recommendations.append("Review recent changes and consider rollback")
            elif signal.drift_type == DriftType.STRATEGY_ENTROPY:
                recommendations.append("Force strategy diversity through random selection")
            elif signal.drift_type == DriftType.GENERALIZATION_GAP:
                recommendations.append("Reduce overfitting through regularization")

        if overall == DriftSeverity.CRITICAL:
            return "CRITICAL: Immediate intervention required. " + "; ".join(recommendations)
        elif overall == DriftSeverity.SEVERE:
            return "SEVERE: Action needed soon. " + "; ".join(recommendations)
        else:
            return "Monitor closely. " + "; ".join(recommendations)

    def get_stats(self) -> Dict:
        """Get monitor statistics."""
        return {
            'detections_run': len(self._detection_history),
            'signals_detected': self._signals_detected,
            'current_diversity': self.solution_diversity.get_diversity_score(),
            'current_entropy': self.strategy_entropy.get_entropy(),
            'benchmark_decline': self.benchmark.get_decline_rate() or 0.0,
            'thresholds': {
                'diversity': self.diversity_threshold,
                'benchmark_decline': self.benchmark_decline_threshold,
                'entropy': self.entropy_threshold,
                'generalization_gap': self.generalization_gap_threshold
            }
        }

    def get_history(self, limit: int = 10) -> List[DriftReport]:
        """Get detection history."""
        return self._detection_history[-limit:]

    def reset(self) -> None:
        """Reset all trackers."""
        self.solution_diversity = SolutionDiversityTracker(
            window_size=self.config.get('diversity_window', 50)
        )
        self.benchmark = BenchmarkTracker(
            decay_factor=self.config.get('benchmark_decay', 0.95)
        )
        self.strategy_entropy = StrategyEntropyTracker(
            window_size=self.config.get('entropy_window', 100)
        )
        self.training_scores.clear()
        self.test_scores.clear()
        self._detection_history.clear()
        self._signals_detected = 0
        logger.info("EntropicDriftMonitor reset")
