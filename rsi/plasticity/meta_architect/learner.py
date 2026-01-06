"""
Pattern Learning from Architecture Outcomes.

Extracts design patterns from architecture evaluation results.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 3.2 for specification.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timezone
import uuid
import logging

from .patterns import (
    DesignPattern,
    PatternType,
    PatternCondition,
    PatternAction,
    PatternLibrary
)

logger = logging.getLogger("rsi.plasticity.meta_architect.learner")


@dataclass
class ArchitectureOutcome:
    """Outcome of architecture evaluation."""
    id: str
    architecture_id: str
    goal: str
    success: bool
    score: float  # 0.0 to 1.0

    # Architecture characteristics
    node_count: int
    connection_count: int
    node_types: List[str]
    operation_types: List[str]
    connection_types: List[str]

    # Additional context
    context: Dict[str, Any] = field(default_factory=dict)
    evaluation_time_ms: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'architecture_id': self.architecture_id,
            'goal': self.goal,
            'success': self.success,
            'score': self.score,
            'node_count': self.node_count,
            'connection_count': self.connection_count,
            'node_types': self.node_types,
            'operation_types': self.operation_types,
            'connection_types': self.connection_types,
            'context': self.context,
            'evaluation_time_ms': self.evaluation_time_ms,
            'metadata': self.metadata,
            'created_at': self.created_at
        }


@dataclass
class PatternCandidate:
    """Candidate pattern extracted from outcomes."""
    pattern_type: PatternType
    conditions: List[PatternCondition]
    actions: List[PatternAction]
    support: int  # Number of outcomes supporting this pattern
    confidence: float  # Pattern confidence
    source_outcomes: List[str]

    def to_pattern(self, name: str = None, description: str = None) -> DesignPattern:
        """Convert to a full DesignPattern."""
        return DesignPattern(
            id=f"pattern_{uuid.uuid4().hex[:12]}",
            name=name or f"Learned Pattern ({self.pattern_type.value})",
            description=description or "Automatically learned pattern",
            pattern_type=self.pattern_type,
            conditions=self.conditions,
            actions=self.actions,
            observations=self.support,
            successes=int(self.support * self.confidence),
            failures=int(self.support * (1 - self.confidence)),
            source_outcomes=self.source_outcomes
        )


class PatternLearner:
    """
    Learns architecture patterns from outcomes.

    Analyzes successful and failed architectures to
    extract design patterns that can guide future designs.
    """

    def __init__(
        self,
        library: PatternLibrary = None,
        config: Dict = None
    ):
        """Initialize pattern learner."""
        self.config = config or {}
        self.library = library or PatternLibrary()

        # Learning configuration
        self._min_support = self.config.get('min_support', 3)
        self._min_confidence = self.config.get('min_confidence', 0.6)
        self._success_threshold = self.config.get('success_threshold', 0.7)

        # Outcome storage
        self._outcomes: List[ArchitectureOutcome] = []

        # Statistics
        self._patterns_learned: int = 0
        self._outcomes_processed: int = 0

    async def learn_from_outcome(
        self,
        architecture_id: str,
        goal: str,
        success: bool,
        score: float,
        architecture_data: Dict
    ) -> List[DesignPattern]:
        """
        Learn patterns from an architecture outcome.

        Args:
            architecture_id: ID of the evaluated architecture
            goal: Goal the architecture was designed for
            success: Whether evaluation was successful
            score: Evaluation score (0-1)
            architecture_data: Architecture details

        Returns:
            List of newly learned patterns
        """
        # Create outcome record
        outcome = ArchitectureOutcome(
            id=f"outcome_{uuid.uuid4().hex[:12]}",
            architecture_id=architecture_id,
            goal=goal,
            success=success,
            score=score,
            node_count=architecture_data.get('node_count', 0),
            connection_count=architecture_data.get('connection_count', 0),
            node_types=architecture_data.get('node_types', []),
            operation_types=architecture_data.get('operation_types', []),
            connection_types=architecture_data.get('connection_types', []),
            context=architecture_data.get('context', {}),
            evaluation_time_ms=architecture_data.get('evaluation_time_ms', 0.0),
            metadata=architecture_data.get('metadata', {})
        )

        self._outcomes.append(outcome)
        self._outcomes_processed += 1

        # Update existing patterns
        self._update_existing_patterns(outcome)

        # Try to extract new patterns
        new_patterns = []

        if len(self._outcomes) >= self._min_support:
            candidates = self._extract_pattern_candidates()

            for candidate in candidates:
                if self._should_create_pattern(candidate):
                    pattern = candidate.to_pattern()
                    self.library.add_pattern(pattern)
                    new_patterns.append(pattern)
                    self._patterns_learned += 1

                    logger.info(
                        f"Learned new pattern: {pattern.name} "
                        f"(support={candidate.support}, conf={candidate.confidence:.2f})"
                    )

        return new_patterns

    def _update_existing_patterns(self, outcome: ArchitectureOutcome) -> None:
        """Update existing patterns based on new outcome."""
        context = self._outcome_to_context(outcome)

        for pattern in self.library.get_all_patterns():
            if pattern.applies_to(context):
                pattern.record_observation(
                    success=outcome.success,
                    outcome_id=outcome.id
                )
                logger.debug(
                    f"Updated pattern {pattern.id}: "
                    f"success_rate={pattern.success_rate:.2f}"
                )

    def _outcome_to_context(self, outcome: ArchitectureOutcome) -> Dict:
        """Convert outcome to pattern matching context."""
        return {
            'goal': outcome.goal,
            'node_count': outcome.node_count,
            'connection_count': outcome.connection_count,
            'node_types': set(outcome.node_types),
            'operation_types': set(outcome.operation_types),
            'connection_types': set(outcome.connection_types),
            'connection_ratio': (
                outcome.connection_count / outcome.node_count
                if outcome.node_count > 0 else 0
            ),
            **outcome.context
        }

    def _extract_pattern_candidates(self) -> List[PatternCandidate]:
        """Extract pattern candidates from outcomes."""
        candidates = []

        # Extract structural patterns
        candidates.extend(self._extract_structural_patterns())

        # Extract operational patterns
        candidates.extend(self._extract_operational_patterns())

        # Extract constraint patterns (from failures)
        candidates.extend(self._extract_constraint_patterns())

        return candidates

    def _extract_structural_patterns(self) -> List[PatternCandidate]:
        """Extract patterns about structure (nodes, connections)."""
        candidates = []

        # Group successful outcomes by node count ranges
        success_outcomes = [o for o in self._outcomes if o.success]

        if len(success_outcomes) < self._min_support:
            return candidates

        # Pattern: Optimal node count range
        node_counts = [o.node_count for o in success_outcomes]
        avg_nodes = sum(node_counts) / len(node_counts)

        if len(success_outcomes) >= self._min_support:
            candidates.append(PatternCandidate(
                pattern_type=PatternType.STRUCTURAL,
                conditions=[
                    PatternCondition("goal_type", "eq", "any")
                ],
                actions=[
                    PatternAction(
                        "target_node_count",
                        {"min": int(avg_nodes * 0.7), "max": int(avg_nodes * 1.3)},
                        priority=0.8
                    )
                ],
                support=len(success_outcomes),
                confidence=len(success_outcomes) / len(self._outcomes),
                source_outcomes=[o.id for o in success_outcomes]
            ))

        # Pattern: Optimal connection ratio
        conn_ratios = [
            o.connection_count / o.node_count
            for o in success_outcomes if o.node_count > 0
        ]

        if conn_ratios:
            avg_ratio = sum(conn_ratios) / len(conn_ratios)

            candidates.append(PatternCandidate(
                pattern_type=PatternType.STRUCTURAL,
                conditions=[],
                actions=[
                    PatternAction(
                        "target_connection_ratio",
                        {"min": avg_ratio * 0.8, "max": avg_ratio * 1.2},
                        priority=0.7
                    )
                ],
                support=len(conn_ratios),
                confidence=len(success_outcomes) / len(self._outcomes),
                source_outcomes=[o.id for o in success_outcomes if o.node_count > 0]
            ))

        return candidates

    def _extract_operational_patterns(self) -> List[PatternCandidate]:
        """Extract patterns about operations."""
        candidates = []

        success_outcomes = [o for o in self._outcomes if o.success]
        failure_outcomes = [o for o in self._outcomes if not o.success]

        # Count operation type frequencies in successes vs failures
        success_ops = {}
        for o in success_outcomes:
            for op in o.operation_types:
                success_ops[op] = success_ops.get(op, 0) + 1

        failure_ops = {}
        for o in failure_outcomes:
            for op in o.operation_types:
                failure_ops[op] = failure_ops.get(op, 0) + 1

        # Find operations that correlate with success
        for op, count in success_ops.items():
            if count >= self._min_support:
                failure_count = failure_ops.get(op, 0)
                total = count + failure_count
                success_rate = count / total if total > 0 else 0

                if success_rate >= self._min_confidence:
                    candidates.append(PatternCandidate(
                        pattern_type=PatternType.OPERATIONAL,
                        conditions=[],
                        actions=[
                            PatternAction(
                                "include_operation",
                                {"operation_type": op},
                                priority=success_rate
                            )
                        ],
                        support=count,
                        confidence=success_rate,
                        source_outcomes=[
                            o.id for o in success_outcomes
                            if op in o.operation_types
                        ]
                    ))

        return candidates

    def _extract_constraint_patterns(self) -> List[PatternCandidate]:
        """Extract patterns about what to avoid (from failures)."""
        candidates = []

        failure_outcomes = [o for o in self._outcomes if not o.success]
        success_outcomes = [o for o in self._outcomes if o.success]

        if len(failure_outcomes) < self._min_support:
            return candidates

        # Find characteristics common in failures but not in successes
        failure_ops = {}
        for o in failure_outcomes:
            for op in o.operation_types:
                failure_ops[op] = failure_ops.get(op, 0) + 1

        success_ops = set()
        for o in success_outcomes:
            success_ops.update(o.operation_types)

        # Operations that frequently fail but rarely succeed
        for op, fail_count in failure_ops.items():
            if fail_count >= self._min_support:
                # Check success rate for this operation
                success_with_op = sum(
                    1 for o in success_outcomes if op in o.operation_types
                )
                total = fail_count + success_with_op
                failure_rate = fail_count / total if total > 0 else 0

                if failure_rate >= 0.7:  # High failure rate
                    candidates.append(PatternCandidate(
                        pattern_type=PatternType.CONSTRAINT,
                        conditions=[],
                        actions=[
                            PatternAction(
                                "avoid_operation",
                                {"operation_type": op, "reason": "high_failure_rate"},
                                priority=failure_rate
                            )
                        ],
                        support=fail_count,
                        confidence=failure_rate,
                        source_outcomes=[
                            o.id for o in failure_outcomes
                            if op in o.operation_types
                        ]
                    ))

        return candidates

    def _should_create_pattern(self, candidate: PatternCandidate) -> bool:
        """Determine if candidate should become a pattern."""
        # Check support threshold
        if candidate.support < self._min_support:
            return False

        # Check confidence threshold
        if candidate.confidence < self._min_confidence:
            return False

        # Check if similar pattern already exists
        existing = self.library.get_patterns_by_type(candidate.pattern_type)
        for pattern in existing:
            if self._candidate_matches_pattern(candidate, pattern):
                return False

        return True

    def _candidate_matches_pattern(
        self,
        candidate: PatternCandidate,
        pattern: DesignPattern
    ) -> bool:
        """Check if candidate matches existing pattern."""
        # Compare actions
        if not candidate.actions or not pattern.actions:
            return False

        # Simple comparison: same action type and similar parameters
        candidate_action_types = set(a.action_type for a in candidate.actions)
        pattern_action_types = set(a.action_type for a in pattern.actions)

        return candidate_action_types == pattern_action_types

    def consolidate_outcomes(self, max_outcomes: int = 1000) -> int:
        """
        Consolidate old outcomes to save memory.

        Keeps recent outcomes and removes old ones after
        their patterns have been learned.

        Returns number of outcomes removed.
        """
        if len(self._outcomes) <= max_outcomes:
            return 0

        # Keep most recent outcomes
        removed_count = len(self._outcomes) - max_outcomes
        self._outcomes = self._outcomes[-max_outcomes:]

        logger.info(f"Consolidated outcomes: removed {removed_count}")
        return removed_count

    def get_learning_insights(self) -> Dict:
        """Get insights about learned patterns."""
        if not self._outcomes:
            return {"message": "No outcomes recorded yet"}

        success_count = sum(1 for o in self._outcomes if o.success)
        success_rate = success_count / len(self._outcomes)

        # Find most common characteristics in successes
        success_outcomes = [o for o in self._outcomes if o.success]
        common_ops = {}
        for o in success_outcomes:
            for op in o.operation_types:
                common_ops[op] = common_ops.get(op, 0) + 1

        top_ops = sorted(
            common_ops.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        return {
            'total_outcomes': len(self._outcomes),
            'success_rate': success_rate,
            'patterns_learned': self._patterns_learned,
            'top_success_operations': [
                {'operation': op, 'count': count}
                for op, count in top_ops
            ],
            'library_stats': self.library.get_stats()
        }

    def get_stats(self) -> Dict:
        """Get learner statistics."""
        return {
            'outcomes_processed': self._outcomes_processed,
            'outcomes_stored': len(self._outcomes),
            'patterns_learned': self._patterns_learned,
            'min_support': self._min_support,
            'min_confidence': self._min_confidence,
            'library_patterns': len(self.library.get_all_patterns())
        }

    def reset(self) -> None:
        """Reset learner state."""
        self._outcomes.clear()
        self._patterns_learned = 0
        self._outcomes_processed = 0
        self.library.reset()
        logger.info("PatternLearner reset")
