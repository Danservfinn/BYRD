"""
Architecture Design Patterns.

Learned patterns that guide architecture design.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 3.2 for specification.
"""

from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
import uuid
import logging

logger = logging.getLogger("rsi.plasticity.meta_architect.patterns")


class PatternType(Enum):
    """Types of architecture patterns."""
    STRUCTURAL = "structural"       # How nodes connect
    OPERATIONAL = "operational"     # What operations work well
    COMPOSITIONAL = "compositional" # How modules compose
    CONSTRAINT = "constraint"       # What to avoid
    OPTIMIZATION = "optimization"   # Performance patterns
    EMERGENCE = "emergence"         # Unexpected successes


class PatternStrength(Enum):
    """Confidence in pattern validity."""
    WEAK = "weak"           # Observed 1-2 times
    MODERATE = "moderate"   # Observed 3-5 times
    STRONG = "strong"       # Observed 6-10 times
    VERY_STRONG = "very_strong"  # Observed 10+ times


@dataclass
class PatternCondition:
    """Condition under which a pattern applies."""
    attribute: str
    operator: str  # eq, gt, lt, gte, lte, contains, in
    value: Any

    def matches(self, context: Dict) -> bool:
        """Check if condition matches context."""
        if self.attribute not in context:
            return False

        actual = context[self.attribute]

        if self.operator == "eq":
            return actual == self.value
        elif self.operator == "gt":
            return actual > self.value
        elif self.operator == "lt":
            return actual < self.value
        elif self.operator == "gte":
            return actual >= self.value
        elif self.operator == "lte":
            return actual <= self.value
        elif self.operator == "contains":
            return self.value in actual
        elif self.operator == "in":
            return actual in self.value

        return False

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'attribute': self.attribute,
            'operator': self.operator,
            'value': self.value
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "PatternCondition":
        """Create from dictionary."""
        return cls(
            attribute=data['attribute'],
            operator=data['operator'],
            value=data['value']
        )


@dataclass
class PatternAction:
    """Action recommended by a pattern."""
    action_type: str  # add_node, remove_node, add_connection, etc.
    parameters: Dict[str, Any] = field(default_factory=dict)
    priority: float = 1.0

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'action_type': self.action_type,
            'parameters': self.parameters,
            'priority': self.priority
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "PatternAction":
        """Create from dictionary."""
        return cls(
            action_type=data['action_type'],
            parameters=data.get('parameters', {}),
            priority=data.get('priority', 1.0)
        )


@dataclass
class DesignPattern:
    """
    A learned architecture design pattern.

    Patterns capture successful architectural decisions
    that can be applied to new architecture designs.
    """
    id: str
    name: str
    description: str
    pattern_type: PatternType

    # When this pattern applies
    conditions: List[PatternCondition]

    # What to do when pattern applies
    actions: List[PatternAction]

    # Pattern statistics
    observations: int = 0
    successes: int = 0
    failures: int = 0

    # Metadata
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    updated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    source_outcomes: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def success_rate(self) -> float:
        """Get pattern success rate."""
        if self.observations == 0:
            return 0.0
        return self.successes / self.observations

    @property
    def strength(self) -> PatternStrength:
        """Get pattern strength based on observations."""
        if self.observations >= 10:
            return PatternStrength.VERY_STRONG
        elif self.observations >= 6:
            return PatternStrength.STRONG
        elif self.observations >= 3:
            return PatternStrength.MODERATE
        else:
            return PatternStrength.WEAK

    @property
    def confidence(self) -> float:
        """Calculate pattern confidence (0-1)."""
        # Bayesian confidence with prior
        alpha = self.successes + 1  # Prior successes
        beta = self.failures + 1    # Prior failures

        # Expected value of Beta distribution
        return alpha / (alpha + beta)

    def applies_to(self, context: Dict) -> bool:
        """Check if pattern applies to context."""
        return all(cond.matches(context) for cond in self.conditions)

    def record_observation(self, success: bool, outcome_id: str = None) -> None:
        """Record observation of pattern application."""
        self.observations += 1
        if success:
            self.successes += 1
        else:
            self.failures += 1
        self.updated_at = datetime.now(timezone.utc).isoformat()
        if outcome_id:
            self.source_outcomes.append(outcome_id)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'pattern_type': self.pattern_type.value,
            'conditions': [c.to_dict() for c in self.conditions],
            'actions': [a.to_dict() for a in self.actions],
            'observations': self.observations,
            'successes': self.successes,
            'failures': self.failures,
            'success_rate': self.success_rate,
            'strength': self.strength.value,
            'confidence': self.confidence,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'source_outcomes': self.source_outcomes,
            'metadata': self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "DesignPattern":
        """Create from dictionary."""
        return cls(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            pattern_type=PatternType(data['pattern_type']),
            conditions=[PatternCondition.from_dict(c) for c in data.get('conditions', [])],
            actions=[PatternAction.from_dict(a) for a in data.get('actions', [])],
            observations=data.get('observations', 0),
            successes=data.get('successes', 0),
            failures=data.get('failures', 0),
            created_at=data.get('created_at', datetime.now(timezone.utc).isoformat()),
            updated_at=data.get('updated_at', datetime.now(timezone.utc).isoformat()),
            source_outcomes=data.get('source_outcomes', []),
            metadata=data.get('metadata', {})
        )


@dataclass
class PatternMatch:
    """Result of pattern matching against context."""
    pattern: DesignPattern
    match_score: float  # 0.0 to 1.0
    matched_conditions: List[PatternCondition]
    unmatched_conditions: List[PatternCondition]

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'pattern_id': self.pattern.id,
            'pattern_name': self.pattern.name,
            'match_score': self.match_score,
            'matched_conditions': [c.to_dict() for c in self.matched_conditions],
            'unmatched_conditions': [c.to_dict() for c in self.unmatched_conditions]
        }


class PatternLibrary:
    """
    Library of learned design patterns.

    Manages pattern storage, retrieval, and matching.
    """

    def __init__(self, config: Dict = None):
        """Initialize pattern library."""
        self.config = config or {}

        # Pattern storage by ID
        self._patterns: Dict[str, DesignPattern] = {}

        # Index by type for faster lookup
        self._by_type: Dict[PatternType, List[str]] = {
            pt: [] for pt in PatternType
        }

        # Statistics
        self._total_matches: int = 0
        self._successful_matches: int = 0

    def add_pattern(self, pattern: DesignPattern) -> None:
        """Add pattern to library."""
        self._patterns[pattern.id] = pattern

        if pattern.id not in self._by_type[pattern.pattern_type]:
            self._by_type[pattern.pattern_type].append(pattern.id)

        logger.info(f"Added pattern to library: {pattern.id} ({pattern.name})")

    def get_pattern(self, pattern_id: str) -> Optional[DesignPattern]:
        """Get pattern by ID."""
        return self._patterns.get(pattern_id)

    def remove_pattern(self, pattern_id: str) -> bool:
        """Remove pattern from library."""
        if pattern_id not in self._patterns:
            return False

        pattern = self._patterns[pattern_id]
        del self._patterns[pattern_id]

        if pattern_id in self._by_type[pattern.pattern_type]:
            self._by_type[pattern.pattern_type].remove(pattern_id)

        logger.info(f"Removed pattern from library: {pattern_id}")
        return True

    def find_matching_patterns(
        self,
        context: Dict,
        pattern_type: PatternType = None,
        min_confidence: float = 0.5,
        limit: int = 10
    ) -> List[PatternMatch]:
        """
        Find patterns that match the given context.

        Args:
            context: Context to match against
            pattern_type: Optional type filter
            min_confidence: Minimum pattern confidence
            limit: Maximum results

        Returns:
            Sorted list of matching patterns
        """
        matches = []

        # Get patterns to check
        if pattern_type:
            pattern_ids = self._by_type.get(pattern_type, [])
        else:
            pattern_ids = list(self._patterns.keys())

        for pattern_id in pattern_ids:
            pattern = self._patterns[pattern_id]

            # Skip low-confidence patterns
            if pattern.confidence < min_confidence:
                continue

            # Check conditions
            matched = []
            unmatched = []

            for cond in pattern.conditions:
                if cond.matches(context):
                    matched.append(cond)
                else:
                    unmatched.append(cond)

            # Calculate match score
            if not pattern.conditions:
                match_score = 0.5  # Unconditional pattern
            else:
                match_score = len(matched) / len(pattern.conditions)

            # Include if any conditions match
            if match_score > 0:
                matches.append(PatternMatch(
                    pattern=pattern,
                    match_score=match_score,
                    matched_conditions=matched,
                    unmatched_conditions=unmatched
                ))

        # Sort by match score * confidence
        matches.sort(
            key=lambda m: m.match_score * m.pattern.confidence,
            reverse=True
        )

        self._total_matches += 1
        if matches:
            self._successful_matches += 1

        return matches[:limit]

    def get_patterns_by_type(
        self,
        pattern_type: PatternType
    ) -> List[DesignPattern]:
        """Get all patterns of a given type."""
        pattern_ids = self._by_type.get(pattern_type, [])
        return [self._patterns[pid] for pid in pattern_ids if pid in self._patterns]

    def get_all_patterns(self) -> List[DesignPattern]:
        """Get all patterns."""
        return list(self._patterns.values())

    def get_strong_patterns(
        self,
        min_strength: PatternStrength = PatternStrength.MODERATE
    ) -> List[DesignPattern]:
        """Get patterns with at least minimum strength."""
        strength_order = [
            PatternStrength.WEAK,
            PatternStrength.MODERATE,
            PatternStrength.STRONG,
            PatternStrength.VERY_STRONG
        ]

        min_index = strength_order.index(min_strength)

        return [
            p for p in self._patterns.values()
            if strength_order.index(p.strength) >= min_index
        ]

    def merge_similar_patterns(
        self,
        similarity_threshold: float = 0.8
    ) -> List[str]:
        """
        Merge patterns that are very similar.

        Returns list of merged pattern IDs.
        """
        merged = []
        patterns = list(self._patterns.values())

        for i, p1 in enumerate(patterns):
            for p2 in patterns[i+1:]:
                if p2.id in merged:
                    continue

                # Check if same type and similar conditions
                if p1.pattern_type != p2.pattern_type:
                    continue

                # Compare conditions
                if self._patterns_similar(p1, p2, similarity_threshold):
                    # Merge p2 into p1
                    p1.observations += p2.observations
                    p1.successes += p2.successes
                    p1.failures += p2.failures
                    p1.source_outcomes.extend(p2.source_outcomes)
                    p1.updated_at = datetime.now(timezone.utc).isoformat()

                    merged.append(p2.id)
                    logger.info(f"Merged pattern {p2.id} into {p1.id}")

        # Remove merged patterns
        for pattern_id in merged:
            self.remove_pattern(pattern_id)

        return merged

    def _patterns_similar(
        self,
        p1: DesignPattern,
        p2: DesignPattern,
        threshold: float
    ) -> bool:
        """Check if two patterns are similar."""
        if not p1.conditions or not p2.conditions:
            return False

        # Compare condition attributes
        p1_attrs = set(c.attribute for c in p1.conditions)
        p2_attrs = set(c.attribute for c in p2.conditions)

        intersection = len(p1_attrs & p2_attrs)
        union = len(p1_attrs | p2_attrs)

        if union == 0:
            return False

        return intersection / union >= threshold

    def get_stats(self) -> Dict:
        """Get library statistics."""
        return {
            'total_patterns': len(self._patterns),
            'patterns_by_type': {
                pt.value: len(ids) for pt, ids in self._by_type.items()
            },
            'total_matches': self._total_matches,
            'successful_matches': self._successful_matches,
            'match_rate': (
                self._successful_matches / self._total_matches
                if self._total_matches > 0 else 0.0
            ),
            'strong_patterns': len(self.get_strong_patterns()),
            'avg_confidence': (
                sum(p.confidence for p in self._patterns.values()) / len(self._patterns)
                if self._patterns else 0.0
            )
        }

    def reset(self) -> None:
        """Reset library state."""
        self._patterns.clear()
        self._by_type = {pt: [] for pt in PatternType}
        self._total_matches = 0
        self._successful_matches = 0
        logger.info("PatternLibrary reset")
