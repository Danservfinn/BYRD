"""
Value Tracking System for Strategy Execution

Prevents false-positive loops by tracking detailed outcome metrics beyond
simple success/failure. Detects repetitive patterns and measures actual value
produced by strategy executions.

Key Concepts:
- False Positive Loop: A strategy that reports "success" but produces no
  meaningful value or produces identical results repeatedly
- Value Score: Multi-dimensional metric measuring actual utility
- Outcome Fingerprint: Hash-based identification of similar outcomes
- Decay: Recent outcomes weighted more heavily
"""

import hashlib
import json
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Set, Tuple
from enum import Enum


class OutcomeQuality(Enum):
    """Quality classification of strategy outcomes."""
    HIGH_VALUE = "high_value"      # Meaningful, novel, useful result
    MODERATE_VALUE = "moderate_value"  # Partially useful, some novelty
    LOW_VALUE = "low_value"        # Minimal utility, mostly noise
    FALSE_POSITIVE = "false_positive"  # Appeared successful but produced no value
    LOOP_DETECTED = "loop_detected"  # Repeating same outcome
    ERROR = "error"                # Technical error


@dataclass
class StrategyOutcome:
    """Detailed record of a single strategy execution outcome."""
    strategy: str
    timestamp: datetime
    success: bool
    quality: OutcomeQuality
    result_fingerprint: str
    result_summary: str
    execution_time_ms: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "strategy": self.strategy,
            "timestamp": self.timestamp.isoformat(),
            "success": self.success,
            "quality": self.quality.value,
            "result_fingerprint": self.result_fingerprint,
            "result_summary": self.result_summary,
            "execution_time_ms": self.execution_time_ms,
            "metadata": self.metadata
        }


@dataclass
class StrategyMetrics:
    """Aggregated metrics for a strategy."""
    total_attempts: int = 0
    true_successes: int = 0  # High + moderate value
    false_positives: int = 0  # Appeared successful but low/no value
    loops_detected: int = 0
    errors: int = 0
    
    # Recent outcomes (last 50)
    recent_outcomes: deque = field(default_factory=lambda: deque(maxlen=50))
    
    # Outcome fingerprints for loop detection
    outcome_history: List[str] = field(default_factory=list)
    
    # Value score (0.0 to 1.0)
    value_score: float = 0.5
    
    # Confidence in value score (0.0 to 1.0)
    confidence: float = 0.0
    
    def get_success_rate(self) -> float:
        """Basic success rate (includes false positives)."""
        if self.total_attempts == 0:
            return 0.0
        return self.true_successes / self.total_attempts
    
    def get_effective_success_rate(self) -> float:
        """Success rate excluding false positives and loops."""
        if self.total_attempts == 0:
            return 0.0
        effective_successes = self.true_successes
        return effective_successes / self.total_attempts
    
    def get_false_positive_rate(self) -> float:
        """Rate of outcomes that appeared successful but weren't valuable."""
        if self.total_attempts == 0:
            return 0.0
        return self.false_positives / self.total_attempts
    
    def is_degraded(self, threshold: float = 0.3) -> bool:
        """Check if strategy effectiveness is degraded (high false positives)."""
        if self.total_attempts < 5:
            return False  # Not enough data
        return self.get_false_positive_rate() > threshold
    
    def is_looping(self, repetition_threshold: int = 3) -> bool:
        """Check if strategy is producing repetitive outcomes."""
        if len(self.outcome_history) < repetition_threshold:
            return False
        
        # Check last N outcomes for repetition
        recent = self.outcome_history[-repetition_threshold:]
        return len(set(recent)) == 1  # All same = loop


class ValueTracker:
    """
    Tracks strategy outcomes with detailed value analysis to prevent
    false-positive loops.
    
    Core Principles:
    1. Track actual outcomes, not just success/failure
    2. Detect repetitive patterns (loops)
    3. Measure multi-dimensional value
    4. Weight recent outcomes more heavily (decay)
    5. Provide actionable metrics for strategy selection
    """
    
    def __init__(
        self,
        max_history_per_strategy: int = 100,
        decay_halflife_hours: float = 24.0,
        loop_detection_window: int = 5,
        loop_similarity_threshold: float = 0.9
    ):
        self._metrics: Dict[str, StrategyMetrics] = defaultdict(StrategyMetrics)
        self._max_history = max_history_per_strategy
        self._decay_halflife = timedelta(hours=decay_halflife_hours)
        self._loop_window = loop_detection_window
        self._loop_similarity_threshold = loop_similarity_threshold
        
        # Global outcome registry for cross-strategy analysis
        self._global_outcomes: deque = deque(maxlen=500)
        
        # Strategy-specific outcome fingerprints for detailed loop detection
        self._outcome_registry: Dict[str, Set[str]] = defaultdict(set)
    
    def record_outcome(
        self,
        strategy: str,
        success: bool,
        result: Any = None,
        result_summary: str = "",
        execution_time_ms: float = 0.0,
        quality: Optional[OutcomeQuality] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> StrategyOutcome:
        """
        Record a strategy execution outcome with detailed analysis.
        
        Args:
            strategy: Strategy name
            success: Basic success indicator
            result: Actual result (for fingerprinting)
            result_summary: Human-readable summary
            execution_time_ms: Execution duration
            quality: Optional pre-determined quality (auto-detected if None)
            metadata: Additional context
            
        Returns:
            StrategyOutcome object with analysis applied
        """
        # Generate outcome fingerprint
        fingerprint = self._generate_fingerprint(result, result_summary)
        
        # Auto-detect quality if not provided
        if quality is None:
            quality = self._detect_quality(strategy, success, fingerprint, result)
        
        # Check for loops
        if self._is_loop(strategy, fingerprint):
            quality = OutcomeQuality.LOOP_DETECTED
        
        # Create outcome record
        outcome = StrategyOutcome(
            strategy=strategy,
            timestamp=datetime.now(),
            success=success,
            quality=quality,
            result_fingerprint=fingerprint,
            result_summary=result_summary[:200] if result_summary else "",
            execution_time_ms=execution_time_ms,
            metadata=metadata or {}
        )
        
        # Update metrics
        metrics = self._metrics[strategy]
        metrics.total_attempts += 1
        
        if quality in (OutcomeQuality.HIGH_VALUE, OutcomeQuality.MODERATE_VALUE):
            metrics.true_successes += 1
        elif quality == OutcomeQuality.FALSE_POSITIVE:
            metrics.false_positives += 1
        elif quality == OutcomeQuality.LOOP_DETECTED:
            metrics.loops_detected += 1
        elif quality == OutcomeQuality.ERROR:
            metrics.errors += 1
        
        # Track outcome history for loop detection
        metrics.outcome_history.append(fingerprint)
        if len(metrics.outcome_history) > self._max_history:
            metrics.outcome_history = metrics.outcome_history[-self._max_history:]
        
        # Store recent outcome
        metrics.recent_outcomes.append(outcome)
        
        # Update global registry
        self._global_outcomes.append(outcome)
        self._outcome_registry[strategy].add(fingerprint)
        
        # Recalculate value score
        self._recalculate_value_score(strategy)
        
        return outcome
    
    def _generate_fingerprint(self, result: Any, summary: str) -> str:
        """
        Generate a hash-based fingerprint for outcome comparison.
        
        Uses both the result (if serializable) and summary to create
        a stable identifier for detecting similar outcomes.
        """
        # Normalize result for hashing
        try:
            result_str = json.dumps(result, sort_keys=True, default=str)
        except (TypeError, OverflowError):
            result_str = str(result)
        
        # Combine with summary
        combined = f"{result_str}|{summary.lower().strip()}"
        
        # Generate hash
        return hashlib.sha256(combined.encode()).hexdigest()[:16]
    
    def _detect_quality(
        self,
        strategy: str,
        success: bool,
        fingerprint: str,
        result: Any
    ) -> OutcomeQuality:
        """
        Auto-detect outcome quality based on result characteristics.
        
        Heuristics:
        - Empty results = false positive
        - Same as recent outcomes = loop
        - Error-like results = error
        - Substantive results = value
        """
        if not success:
            return OutcomeQuality.ERROR
        
        # Check if result is empty or minimal
        if self._is_empty_result(result):
            return OutcomeQuality.FALSE_POSITIVE
        
        # Check if this matches recent outcomes (potential loop)
        metrics = self._metrics.get(strategy)
        if metrics and len(metrics.outcome_history) >= 2:
            recent_fingerprints = metrics.outcome_history[-3:]
            if fingerprint in recent_fingerprints:
                return OutcomeQuality.LOOP_DETECTED
        
        # Check result substance
        if self._has_substance(result):
            return OutcomeQuality.HIGH_VALUE
        
        return OutcomeQuality.MODERATE_VALUE
    
    def _is_empty_result(self, result: Any) -> bool:
        """Check if result represents an empty/minimal outcome."""
        if result is None:
            return True
        if isinstance(result, (str, list, dict)) and len(result) == 0:
            return True
        if isinstance(result, str) and result.strip() in ("", "ok", "done", "success"):
            return True
        return False
    
    def _has_substance(self, result: Any) -> bool:
        """Check if result has meaningful content."""
        if isinstance(result, str):
            return len(result.strip()) > 50
        if isinstance(result, list):
            return len(result) > 0
        if isinstance(result, dict):
            return len(result) > 0 and any(
                v is not None and v != "" for v in result.values()
            )
        return bool(result)
    
    def _is_loop(self, strategy: str, fingerprint: str) -> bool:
        """
        Check if this outcome represents a loop.
        
        A loop is detected when:
        1. Same fingerprint appears multiple times recently
        2. Multiple consecutive outcomes have similar fingerprints
        """
        metrics = self._metrics.get(strategy)
        if not metrics or len(metrics.outcome_history) < 3:
            return False
        
        recent = metrics.outcome_history[-self._loop_window:]
        
        # Count occurrences of this fingerprint
        occurrences = sum(1 for fp in recent if fp == fingerprint)
        if occurrences >= 3:
            return True
        
        # Check for near-duplicates (fingerprint similarity not applicable with hash)
        # Instead, check if last 3 are identical
        if len(recent) >= 3 and len(set(recent[-3:])) == 1:
            return True
        
        return False
    
    def _recalculate_value_score(self, strategy: str) -> None:
        """
        Recalculate value score with time-based decay.
        
        Value score formula:
        score = (high * 1.0 + moderate * 0.5 + low * 0.1 + false_pos * 0.0 + loop * -0.5) / total
        
        Apply exponential decay based on outcome age.
        """
        metrics = self._metrics[strategy]
        
        if metrics.total_attempts == 0:
            metrics.value_score = 0.5
            metrics.confidence = 0.0
            return
        
        now = datetime.now()
        weighted_sum = 0.0
        weight_total = 0.0
        
        for outcome in metrics.recent_outcomes:
            # Calculate age-based decay factor
            age = now - outcome.timestamp
            decay_factor = 0.5 ** (age / self._decay_halflife)
            
            # Assign value based on quality
            quality_values = {
                OutcomeQuality.HIGH_VALUE: 1.0,
                OutcomeQuality.MODERATE_VALUE: 0.5,
                OutcomeQuality.LOW_VALUE: 0.1,
                OutcomeQuality.FALSE_POSITIVE: 0.0,
                OutcomeQuality.LOOP_DETECTED: -0.5,
                OutcomeQuality.ERROR: -0.2
            }
            
            value = quality_values.get(outcome.quality, 0.0)
            weighted_sum += value * decay_factor
            weight_total += decay_factor
        
        if weight_total > 0:
            metrics.value_score = max(0.0, min(1.0, weighted_sum / weight_total + 0.5))
            # Normalize: -0.5 to 1.0 -> 0.0 to 1.0
            metrics.value_score = (metrics.value_score + 0.5) / 1.5
        else:
            metrics.value_score = 0.5
        
        # Confidence increases with more data
        metrics.confidence = min(1.0, metrics.total_attempts / 20.0)
    
    def get_strategy_metrics(self, strategy: str) -> Optional[StrategyMetrics]:
        """Get metrics for a specific strategy."""
        return self._metrics.get(strategy)
    
    def get_all_metrics(self) -> Dict[str, Dict[str, Any]]:
        """Get metrics for all strategies in serializable format."""
        result = {}
        for strategy, metrics in self._metrics.items():
            result[strategy] = {
                "total_attempts": metrics.total_attempts,
                "true_successes": metrics.true_successes,
                "false_positives": metrics.false_positives,
                "loops_detected": metrics.loops_detected,
                "errors": metrics.errors,
                "success_rate": metrics.get_success_rate(),
                "effective_success_rate": metrics.get_effective_success_rate(),
                "false_positive_rate": metrics.get_false_positive_rate(),
                "value_score": metrics.value_score,
                "confidence": metrics.confidence,
                "is_degraded": metrics.is_degraded(),
                "is_looping": metrics.is_looping(),
                "recent_outcome_count": len(metrics.recent_outcomes)
            }
        return result
    
    def get_best_strategies(
        self,
        min_attempts: int = 5,
        min_confidence: float = 0.3
    ) -> List[Tuple[str, float]]:
        """
        Get strategies ranked by value score.
        
        Returns list of (strategy, value_score) tuples, sorted by score descending.
        """
        candidates = []
        for strategy, metrics in self._metrics.items():
            if (metrics.total_attempts >= min_attempts and
                metrics.confidence >= min_confidence):
                candidates.append((strategy, metrics.value_score))
        
        # Sort by value score descending
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates
    
    def should_avoid_strategy(
        self,
        strategy: str,
        degradation_threshold: float = 0.3
    ) -> Tuple[bool, str]:
        """
        Check if a strategy should be avoided due to poor performance.
        
        Returns:
            (should_avoid, reason)
        """
        metrics = self._metrics.get(strategy)
        if not metrics:
            return (False, "No data available")
        
        if metrics.is_looping():
            return (True, f"Loop detected: {metrics.loops_detected} repetitive outcomes")
        
        if metrics.is_degraded(degradation_threshold):
            return (True, f"High false positive rate: {metrics.get_false_positive_rate():.1%}")
        
        if metrics.confidence < 0.3:
            return (False, "Insufficient data for reliable assessment")
        
        if metrics.value_score < 0.3:
            return (True, f"Low value score: {metrics.value_score:.2f}")
        
        return (False, "Strategy appears healthy")
    
    def get_cross_strategy_analysis(self) -> Dict[str, Any]:
        """Analyze patterns across all strategies."""
        total_outcomes = sum(m.total_attempts for m in self._metrics.values())
        total_false_positives = sum(m.false_positives for m in self._metrics.values())
        total_loops = sum(m.loops_detected for m in self._metrics.values())
        
        return {
            "total_strategies": len(self._metrics),
            "total_outcomes": total_outcomes,
            "global_false_positive_rate": (
                total_false_positives / total_outcomes if total_outcomes > 0 else 0
            ),
            "global_loop_rate": (
                total_loops / total_outcomes if total_outcomes > 0 else 0
            ),
            "healthy_strategies": sum(
                1 for m in self._metrics.values()
                if not m.is_degraded() and not m.is_looping()
            ),
            "degraded_strategies": sum(
                1 for m in self._metrics.values() if m.is_degraded()
            ),
            "looping_strategies": sum(
                1 for m in self._metrics.values() if m.is_looping()
            )
        }
    
    def reset_strategy(self, strategy: str) -> None:
        """Reset metrics for a specific strategy."""
        if strategy in self._metrics:
            del self._metrics[strategy]
            if strategy in self._outcome_registry:
                del self._outcome_registry[strategy]
    
    def export_recent_outcomes(
        self,
        strategy: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Export recent outcomes for analysis."""
        if strategy:
            metrics = self._metrics.get(strategy)
            if metrics:
                outcomes = list(metrics.recent_outcomes)[-limit:]
            else:
                outcomes = []
        else:
            outcomes = list(self._global_outcomes)[-limit:]
        
        return [o.to_dict() for o in outcomes]
    
    def get_summary_report(self) -> str:
        """Generate a human-readable summary report."""
        lines = ["=" * 60, "VALUE TRACKER SUMMARY REPORT", "=" * 60, ""]
        
        # Cross-strategy analysis
        analysis = self.get_cross_strategy_analysis()
        lines.append("GLOBAL METRICS:")
        lines.append(f"  Total Strategies: {analysis['total_strategies']}")
        lines.append(f"  Total Outcomes: {analysis['total_outcomes']}")
        lines.append(f"  False Positive Rate: {analysis['global_false_positive_rate']:.1%}")
        lines.append(f"  Loop Rate: {analysis['global_loop_rate']:.1%}")
        lines.append(f"  Healthy Strategies: {analysis['healthy_strategies']}")
        lines.append(f"  Degraded Strategies: {analysis['degraded_strategies']}")
        lines.append(f"  Looping Strategies: {analysis['looping_strategies']}")
        lines.append("")
        
        # Per-strategy breakdown
        lines.append("PER-STRATEGY METRICS:")
        sorted_strategies = sorted(
            self._metrics.items(),
            key=lambda x: x[1].total_attempts,
            reverse=True
        )
        
        for strategy, metrics in sorted_strategies:
            lines.append(f"\n{strategy}:")
            lines.append(f"  Attempts: {metrics.total_attempts}")
            lines.append(f"  True Successes: {metrics.true_successes}")
            lines.append(f"  False Positives: {metrics.false_positives}")
            lines.append(f"  Loops: {metrics.loops_detected}")
            lines.append(f"  Success Rate: {metrics.get_success_rate():.1%}")
            lines.append(f"  Effective Rate: {metrics.get_effective_success_rate():.1%}")
            lines.append(f"  Value Score: {metrics.value_score:.2f} (confidence: {metrics.confidence:.2f})")
            
            should_avoid, reason = self.should_avoid_strategy(strategy)
            if should_avoid:
                lines.append(f"  ⚠️  AVOID: {reason}")
        
        lines.append("")
        lines.append("BEST STRATEGIES (by value score):")
        for strategy, score in self.get_best_strategies()[:5]:
            lines.append(f"  {strategy}: {score:.2f}")
        
        lines.append("")
        lines.append("=" * 60)
        
        return "\n".join(lines)


# Singleton instance for easy access
_value_tracker_instance: Optional[ValueTracker] = None


def get_value_tracker() -> ValueTracker:
    """Get or create the global ValueTracker instance."""
    global _value_tracker_instance
    if _value_tracker_instance is None:
        _value_tracker_instance = ValueTracker()
    return _value_tracker_instance


def reset_value_tracker() -> None:
    """Reset the global ValueTracker instance."""
    global _value_tracker_instance
    _value_tracker_instance = None
