"""
Strategy Value Tracking System

Prevents false-positive loops by tracking nuanced strategy performance metrics.

The problem: Simple success/failure counting leads to strategies being
repeatedly selected even when they stop delivering real value. This system
adds context-aware tracking, temporal decay, and false-positive detection.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging
import statistics

logger = logging.getLogger(__name__)


class OutcomeType(Enum):
    """Types of strategy execution outcomes."""
    SUCCESS = "success"              # Strategy achieved its goal
    PARTIAL = "partial"              # Partial achievement, some progress
    FAILURE = "failure"              # Complete failure
    FALSE_POSITIVE = "false_positive" # Appeared successful but wasn't
    LOOP_DETECTED = "loop_detected"   # Strategy creating feedback loops
    CONTEXT_MISMATCH = "context_mismatch"  # Used in wrong context
    TIMEOUT = "timeout"              # Took too long
    ERROR = "error"                  # Technical error


@dataclass
class StrategyOutcome:
    """Record a single strategy execution outcome."""
    strategy_id: str
    outcome_type: OutcomeType
    timestamp: datetime
    value_score: float  # -1.0 to 1.0, more nuanced than binary
    context: Dict[str, Any] = field(default_factory=dict)
    execution_time_ms: Optional[int] = None
    notes: Optional[str] = None


@dataclass
class StrategyMetrics:
    """Aggregated metrics for a strategy."""
    strategy_id: str
    total_executions: int = 0
    success_count: int = 0
    partial_count: int = 0
    failure_count: int = 0
    false_positive_count: int = 0
    loop_detected_count: int = 0
    
    # Value-based metrics
    current_value_score: float = 0.0  # Time-decayed average
    raw_average_value: float = 0.0   # Simple average
    value_trend: float = 0.0         # Positive = improving, negative = declining
    
    # Temporal metrics
    last_execution: Optional[datetime] = None
    last_success: Optional[datetime] = None
    recent_window_seconds: int = 3600  # 1 hour window for recent metrics
    
    # Context metrics
    successful_contexts: List[Dict[str, Any]] = field(default_factory=list)
    failed_contexts: List[Dict[str, Any]] = field(default_factory=list)
    context_success_rate: float = 0.0  # How context-sensitive is this strategy?
    
    # Loop detection
    consecutive_failures: int = 0
    consecutive_false_positives: int = 0
    is_in_loop: bool = False
    loop_detected_at: Optional[datetime] = None
    
    # Health score (0-1)
    health_score: float = 1.0
    
    @property
    def success_rate(self) -> float:
        """Basic success rate (success / total)."""
        if self.total_executions == 0:
            return 0.0
        return self.success_count / self.total_executions
    
    @property
    def adjusted_success_rate(self) -> float:
        """Success rate accounting for false positives."""
        if self.total_executions == 0:
            return 0.0
        valid_successes = max(0, self.success_count - self.false_positive_count)
        return valid_successes / self.total_executions


class StrategyValueTracker:
    """
    Tracks strategy performance with nuanced metrics to prevent false-positive loops.
    
    Key features:
    1. Value-based scoring instead of binary outcomes
    2. Temporal decay to prioritize recent performance
    3. Context-aware tracking to detect when strategies work
    4. False-positive detection and flagging
    5. Loop prevention mechanisms
    """
    
    def __init__(
        self,
        value_decay_half_life: float = 3600.0,  # 1 hour
        max_outcomes_per_strategy: int = 1000,
        loop_threshold: int = 3,  # Consecutive failures to flag loop
        false_positive_threshold: float = 0.3  # Rate to trigger warning
    ):
        self.value_decay_half_life = value_decay_half_life
        self.max_outcomes_per_strategy = max_outcomes_per_strategy
        self.loop_threshold = loop_threshold
        self.false_positive_threshold = false_positive_threshold
        
        # Storage: strategy_id -> list of StrategyOutcome
        self._outcomes: Dict[str, List[StrategyOutcome]] = {}
        
        # Cached metrics: strategy_id -> StrategyMetrics
        self._metrics_cache: Dict[str, StrategyMetrics] = {}
        
        # Strategy deprecation: strategy_id -> deprecation_reason
        self._deprecated: Dict[str, str] = {}
        
    def record_outcome(self, outcome: StrategyOutcome) -> None:
        """
        Record a strategy execution outcome.
        
        Args:
            outcome: The outcome to record
        """
        if outcome.strategy_id in self._deprecated:
            logger.warning(
                f"Recording outcome for deprecated strategy {outcome.strategy_id}: "
                f"{self._deprecated[outcome.strategy_id]}"
            )
        
        # Store outcome
        if outcome.strategy_id not in self._outcomes:
            self._outcomes[outcome.strategy_id] = []
        
        self._outcomes[outcome.strategy_id].append(outcome)
        
        # Trim old outcomes
        if len(self._outcomes[outcome.strategy_id]) > self.max_outcomes_per_strategy:
            self._outcomes[outcome.strategy_id] = \
                self._outcomes[outcome.strategy_id][-self.max_outcomes_per_strategy:]
        
        # Invalidate cached metrics
        if outcome.strategy_id in self._metrics_cache:
            del self._metrics_cache[outcome.strategy_id]
        
        # Auto-detect loops
        self._check_for_loops(outcome.strategy_id)
        
        logger.debug(
            f"Recorded outcome for {outcome.strategy_id}: "
            f"{outcome.outcome_type.value} (value={outcome.value_score:.2f})"
        )
    
    def _check_for_loops(self, strategy_id: str) -> None:
        """
        Check if a strategy is caught in a false-positive loop.
        
        A loop is detected when:
        1. Multiple consecutive false positives
        2. High false-positive rate overall
        3. Declining value trend
        """
        if strategy_id not in self._outcomes:
            return
        
        outcomes = self._outcomes[strategy_id]
        if len(outcomes) < self.loop_threshold:
            return
        
        # Check consecutive false positives
        recent_outcomes = outcomes[-self.loop_threshold:]
        consecutive_fp = sum(
            1 for o in recent_outcomes 
            if o.outcome_type == OutcomeType.FALSE_POSITIVE
        )
        
        if consecutive_fp >= self.loop_threshold:
            self._deprecate_strategy(
                strategy_id, 
                f"Loop detected: {consecutive_fp} consecutive false positives"
            )
            return
        
        # Check consecutive failures
        consecutive_fail = sum(
            1 for o in recent_outcomes 
            if o.outcome_type in [OutcomeType.FAILURE, OutcomeType.TIMEOUT]
        )
        
        if consecutive_fail >= self.loop_threshold * 2:
            metrics = self.get_metrics(strategy_id)
            if metrics.adjusted_success_rate < 0.2:  # Less than 20% real success
                self._deprecate_strategy(
                    strategy_id,
                    f"Loop detected: {consecutive_fail} consecutive failures, "
                    f"success rate {metrics.adjusted_success_rate:.2%}"
                )
    
    def _deprecate_strategy(self, strategy_id: str, reason: str) -> None:
        """Mark a strategy as deprecated due to loop detection."""
        self._deprecated[strategy_id] = reason
        logger.warning(
            f"⚠️ Strategy {strategy_id} DEPRECATED: {reason}"
        )
    
    def get_metrics(self, strategy_id: str) -> StrategyMetrics:
        """
        Get computed metrics for a strategy.
        
        Args:
            strategy_id: The strategy to get metrics for
            
        Returns:
            StrategyMetrics object with computed values
        """
        # Check cache
        if strategy_id in self._metrics_cache:
            return self._metrics_cache[strategy_id]
        
        # Compute metrics
        if strategy_id not in self._outcomes or not self._outcomes[strategy_id]:
            # No outcomes yet, return empty metrics
            metrics = StrategyMetrics(strategy_id=strategy_id)
            self._metrics_cache[strategy_id] = metrics
            return metrics
        
        outcomes = self._outcomes[strategy_id]
        
        # Basic counts
        metrics = StrategyMetrics(
            strategy_id=strategy_id,
            total_executions=len(outcomes),
            success_count=sum(1 for o in outcomes if o.outcome_type == OutcomeType.SUCCESS),
            partial_count=sum(1 for o in outcomes if o.outcome_type == OutcomeType.PARTIAL),
            failure_count=sum(1 for o in outcomes if o.outcome_type == OutcomeType.FAILURE),
            false_positive_count=sum(1 for o in outcomes if o.outcome_type == OutcomeType.FALSE_POSITIVE),
            loop_detected_count=sum(1 for o in outcomes if o.outcome_type == OutcomeType.LOOP_DETECTED),
        )
        
        # Temporal
        metrics.last_execution = outcomes[-1].timestamp
        success_outcomes = [o for o in outcomes if o.outcome_type == OutcomeType.SUCCESS]
        if success_outcomes:
            metrics.last_success = success_outcomes[-1].timestamp
        
        # Value metrics
        value_scores = [o.value_score for o in outcomes]
        metrics.raw_average_value = statistics.mean(value_scores) if value_scores else 0.0
        metrics.current_value_score = self._compute_decayed_value(outcomes)
        metrics.value_trend = self._compute_value_trend(outcomes)
        
        # Consecutive tracking
        metrics.consecutive_failures = self._count_consecutive(
            outcomes, [OutcomeType.FAILURE, OutcomeType.TIMEOUT, OutcomeType.ERROR]
        )
        metrics.consecutive_false_positives = self._count_consecutive(
            outcomes, [OutcomeType.FALSE_POSITIVE]
        )
        
        # Context analysis
        successful_contexts = [
            o.context for o in outcomes 
            if o.outcome_type in [OutcomeType.SUCCESS, OutcomeType.PARTIAL]
        ]
        failed_contexts = [
            o.context for o in outcomes 
            if o.outcome_type in [OutcomeType.FAILURE, OutcomeType.FALSE_POSITIVE, OutcomeType.CONTEXT_MISMATCH]
        ]
        metrics.successful_contexts = successful_contexts[-10:]  # Keep recent
        metrics.failed_contexts = failed_contexts[-10:]
        
        # Compute context sensitivity
        if len(successful_contexts) + len(failed_contexts) > 5:
            metrics.context_success_rate = len(successful_contexts) / (
                len(successful_contexts) + len(failed_contexts)
            )
        
        # Loop detection
        metrics.is_in_loop = strategy_id in self._deprecated
        if metrics.is_in_loop:
            metrics.loop_detected_at = min(
                o.timestamp for o in outcomes 
                if o.outcome_type in [OutcomeType.FALSE_POSITIVE, OutcomeType.LOOP_DETECTED]
            )
        
        # Health score (0-1)
        metrics.health_score = self._compute_health_score(metrics)
        
        # Cache
        self._metrics_cache[strategy_id] = metrics
        
        return metrics
    
    def _compute_decayed_value(self, outcomes: List[StrategyOutcome]) -> float:
        """
        Compute time-decayed average value score.
        
        Recent outcomes have more weight than old ones.
        """
        if not outcomes:
            return 0.0
        
        now = datetime.now()
        weighted_sum = 0.0
        total_weight = 0.0
        
        for outcome in outcomes:
            age_seconds = (now - outcome.timestamp).total_seconds()
            weight = 2.0 ** (-age_seconds / self.value_decay_half_life)
            weighted_sum += outcome.value_score * weight
            total_weight += weight
        
        return weighted_sum / total_weight if total_weight > 0 else 0.0
    
    def _compute_value_trend(self, outcomes: List[StrategyOutcome]) -> float:
        """
        Compute value trend (positive = improving, negative = declining).
        
        Compares recent performance to older performance.
        """
        if len(outcomes) < 10:
            return 0.0
        
        split_point = len(outcomes) // 2
        recent = outcomes[split_point:]
        older = outcomes[:split_point]
        
        recent_avg = statistics.mean(o.value_score for o in recent)
        older_avg = statistics.mean(o.value_score for o in older)
        
        return recent_avg - older_avg
    
    def _count_consecutive(
        self, 
        outcomes: List[StrategyOutcome], 
        outcome_types: List[OutcomeType]
    ) -> int:
        """Count consecutive occurrences of specified outcome types."""
        count = 0
        for outcome in reversed(outcomes):
            if outcome.outcome_type in outcome_types:
                count += 1
            else:
                break
        return count
    
    def _compute_health_score(self, metrics: StrategyMetrics) -> float:
        """
        Compute overall health score (0-1) for a strategy.
        
        Factors:
        1. Adjusted success rate (40%)
        2. Current value score (30%)
        3. Value trend (20%)
        4. False positive rate penalty (10%)
        """
        if metrics.total_executions == 0:
            return 1.0  # Unknown, assume healthy
        
        # Base score from adjusted success rate
        success_component = metrics.adjusted_success_rate * 0.4
        
        # Value score component (normalize -1 to 1 -> 0 to 1)
        value_component = ((metrics.current_value_score + 1) / 2) * 0.3
        
        # Trend component (normalize -1 to 1 -> 0 to 1)
        trend_component = ((metrics.value_trend + 1) / 2) * 0.2
        
        # False positive penalty
        if metrics.total_executions > 0:
            fp_rate = metrics.false_positive_count / metrics.total_executions
            fp_penalty = fp_rate * 0.5  # Max 50% penalty
        else:
            fp_penalty = 0
        fp_component = (1 - fp_penalty) * 0.1
        
        # Combine
        health = success_component + value_component + trend_component + fp_component
        return max(0.0, min(1.0, health))
    
    def is_safe_to_use(self, strategy_id: str) -> Tuple[bool, Optional[str]]:
        """
        Check if it's safe to use a strategy.
        
        Returns:
            (is_safe, reason_if_not_safe)
        """
        # Check deprecation
        if strategy_id in self._deprecated:
            return False, f"Deprecated: {self._deprecated[strategy_id]}"
        
        metrics = self.get_metrics(strategy_id)
        
        # Check for loop indicators
        if metrics.consecutive_false_positives >= self.loop_threshold:
            return False, f"Consecutive false positives detected ({metrics.consecutive_false_positives})"
        
        if metrics.consecutive_failures >= self.loop_threshold * 2:
            return False, f"Too many consecutive failures ({metrics.consecutive_failures})"
        
        # Check health score
        if metrics.total_executions >= 5 and metrics.health_score < 0.3:
            return False, f"Health score too low ({metrics.health_score:.2f})"
        
        # Check false positive rate
        if metrics.total_executions >= 10:
            fp_rate = metrics.false_positive_count / metrics.total_executions
            if fp_rate > self.false_positive_threshold:
                return False, f"False positive rate too high ({fp_rate:.2%})"
        
        return True, None
    
    def get_strategies_by_health(self, limit: int = 10) -> List[Tuple[str, StrategyMetrics]]:
        """
        Get strategies sorted by health score.
        
        Args:
            limit: Maximum number of strategies to return
            
        Returns:
            List of (strategy_id, metrics) tuples, sorted by health score descending
        """
        all_metrics = [
            (sid, self.get_metrics(sid)) 
            for sid in self._outcomes.keys()
        ]
        
        # Sort by health score, then by total executions (prefer data-rich strategies)
        sorted_metrics = sorted(
            all_metrics,
            key=lambda x: (-x[1].health_score, -x[1].total_executions)
        )
        
        return sorted_metrics[:limit]
    
    def get_strategies_to_review(self) -> List[Tuple[str, StrategyMetrics, str]]:
        """
        Get strategies that need attention.
        
        Returns:
            List of (strategy_id, metrics, issue) tuples
        """
        to_review = []
        
        for strategy_id in self._outcomes.keys():
            metrics = self.get_metrics(strategy_id)
            issue = None
            
            # Check for issues
            if strategy_id in self._deprecated:
                issue = f"Deprecated: {self._deprecated[strategy_id]}"
            elif metrics.consecutive_false_positives >= self.loop_threshold:
                issue = f"Consecutive false positives: {metrics.consecutive_false_positives}"
            elif metrics.consecutive_failures >= self.loop_threshold * 2:
                issue = f"Consecutive failures: {metrics.consecutive_failures}"
            elif metrics.total_executions >= 10:
                fp_rate = metrics.false_positive_count / metrics.total_executions
                if fp_rate > self.false_positive_threshold:
                    issue = f"High false positive rate: {fp_rate:.2%}"
            elif metrics.total_executions >= 5 and metrics.health_score < 0.3:
                issue = f"Low health score: {metrics.health_score:.2f}"
            elif metrics.value_trend < -0.3:
                issue = f"Declining value trend: {metrics.value_trend:.2f}"
            
            if issue:
                to_review.append((strategy_id, metrics, issue))
        
        # Sort by severity (worst health score first)
        to_review.sort(key=lambda x: x[1].health_score)
        return to_review
    
    def suggest_context_hints(self, strategy_id: str) -> Optional[Dict[str, Any]]:
        """
        Suggest context where this strategy is likely to succeed.
        
        Analyzes successful vs failed contexts to find patterns.
        """
        metrics = self.get_metrics(strategy_id)
        
        if not metrics.successful_contexts or not metrics.failed_contexts:
            return None
        
        # Find common keys in contexts
        all_contexts = metrics.successful_contexts + metrics.failed_contexts
        common_keys = set()
        for ctx in all_contexts:
            common_keys.update(ctx.keys())
        
        hints = {}
        for key in common_keys:
            # Get values from successful contexts
            success_values = [ctx.get(key) for ctx in metrics.successful_contexts if key in ctx]
            fail_values = [ctx.get(key) for ctx in metrics.failed_contexts if key in ctx]
            
            # Find values that appear more in successes
            if success_values and fail_values:
                # Simple heuristic: suggest most common success value
                from collections import Counter
                success_counter = Counter(success_values)
                most_common_success = success_counter.most_common(1)[0]
                
                # Check if this value is rare in failures
                fail_count = fail_values.count(most_common_success[0])
                if fail_count < len(fail_values) * 0.3:  # Appears in <30% of failures
                    hints[key] = most_common_success[0]
        
        return hints if hints else None
    
    def reset_strategy(self, strategy_id: str) -> None:
        """
        Reset tracking for a strategy (e.g., after modification).
        
        Keeps the strategy but clears its history.
        """
        if strategy_id in self._outcomes:
            self._outcomes[strategy_id] = []
        if strategy_id in self._metrics_cache:
            del self._metrics_cache[strategy_id]
        if strategy_id in self._deprecated:
            del self._deprecated[strategy_id]
        
        logger.info(f"Reset tracking for strategy {strategy_id}")
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all tracked strategies.
        
        Returns:
            Summary dictionary with overall statistics
        """
        total_strategies = len(self._outcomes)
        deprecated_count = len(self._deprecated)
        total_executions = sum(len(outcomes) for outcomes in self._outcomes.values())
        
        # Calculate average health
        health_scores = [
            self.get_metrics(sid).health_score 
            for sid in self._outcomes.keys()
        ]
        avg_health = statistics.mean(health_scores) if health_scores else 0.0
        
        # Get issues
        issues = self.get_strategies_to_review()
        
        return {
            "total_strategies_tracked": total_strategies,
            "active_strategies": total_strategies - deprecated_count,
            "deprecated_strategies": deprecated_count,
            "total_executions_recorded": total_executions,
            "average_health_score": avg_health,
            "strategies_needing_review": len(issues),
            "top_performers": [
                (sid, m.health_score) 
                for sid, m in self.get_strategies_by_health(5)
            ],
            "recent_issues": [
                (sid, issue) 
                for sid, _, issue in issues[:5]
            ]
        }


# =============================================================================
# Integration Helper Functions
# =============================================================================

def create_outcome(
    strategy_id: str,
    outcome_type: str,
    value_score: float,
    context: Optional[Dict[str, Any]] = None,
    notes: Optional[str] = None,
    execution_time_ms: Optional[int] = None
) -> StrategyOutcome:
    """
    Helper to create a StrategyOutcome.
    
    Args:
        strategy_id: ID of the strategy
        outcome_type: String from OutcomeType enum
        value_score: Value score (-1.0 to 1.0)
        context: Optional context dictionary
        notes: Optional notes about the outcome
        execution_time_ms: Optional execution time
        
    Returns:
        StrategyOutcome object
    """
    return StrategyOutcome(
        strategy_id=strategy_id,
        outcome_type=OutcomeType(outcome_type),
        timestamp=datetime.now(),
        value_score=value_score,
        context=context or {},
        notes=notes,
        execution_time_ms=execution_time_ms
    )


def record_simple_outcome(
    tracker: StrategyValueTracker,
    strategy_id: str,
    success: bool,
    value: float = None,
    context: Optional[Dict[str, Any]] = None
) -> None:
    """
    Helper to record a simple binary outcome.
    
    Args:
        tracker: The tracker instance
        strategy_id: ID of the strategy
        success: Whether the strategy succeeded
        value: Optional explicit value score
        context: Optional context
    """
    if value is None:
        value = 1.0 if success else -1.0
    
    outcome = create_outcome(
        strategy_id=strategy_id,
        outcome_type="success" if success else "failure",
        value_score=value,
        context=context
    )
    
    tracker.record_outcome(outcome)
