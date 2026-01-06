"""
Level-Invariant Representations.

Representations that work at any meta-level for recursive improvement.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 3.3 for specification.
"""

from typing import Dict, List, Optional, Any, TypeVar, Generic
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
from abc import ABC, abstractmethod
import uuid
import logging

logger = logging.getLogger("rsi.recursion.representation")

T = TypeVar('T')


class LevelType(Enum):
    """Types of meta-levels."""
    BASE = 0           # Base level (concrete operations)
    META = 1           # Meta level (improvement of operations)
    META_META = 2      # Meta-meta level (improvement of improvement)
    ABSTRACT = 3       # Abstract level (patterns across levels)


@dataclass
class Improvable:
    """
    Base class for improvable entities.

    Any entity that can be improved must implement this interface.
    The representation is level-invariant - the same structure
    works at any meta-level.
    """
    id: str
    level: int = 0
    content: Any = None
    score: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'level': self.level,
            'score': self.score,
            'metadata': self.metadata,
            'created_at': self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "Improvable":
        """Create from dictionary."""
        return cls(
            id=data['id'],
            level=data.get('level', 0),
            content=data.get('content'),
            score=data.get('score', 0.0),
            metadata=data.get('metadata', {}),
            created_at=data.get('created_at', datetime.now(timezone.utc).isoformat())
        )

    def at_level(self, new_level: int) -> "Improvable":
        """Create copy at different level."""
        return Improvable(
            id=f"{self.id}_L{new_level}",
            level=new_level,
            content=self.content,
            score=self.score,
            metadata={**self.metadata, 'source_level': self.level}
        )


@dataclass
class LeveledPattern:
    """
    A pattern that can be applied at any level.

    Level-invariant patterns capture improvement strategies
    that work regardless of whether we're improving:
    - Base objects (level 0)
    - Improvement strategies (level 1)
    - Meta-strategies (level 2)
    - And so on...
    """
    id: str
    name: str
    description: str

    # Level range this pattern applies to
    min_level: int = 0
    max_level: int = 100  # Effectively infinite

    # Pattern content - level-invariant representation
    pattern_template: Dict[str, Any] = field(default_factory=dict)

    # Instantiation rules for different levels
    level_adaptations: Dict[int, Dict[str, Any]] = field(default_factory=dict)

    # Statistics across levels
    applications_by_level: Dict[int, int] = field(default_factory=dict)
    successes_by_level: Dict[int, int] = field(default_factory=dict)

    metadata: Dict[str, Any] = field(default_factory=dict)

    def applies_at_level(self, level: int) -> bool:
        """Check if pattern applies at given level."""
        return self.min_level <= level <= self.max_level

    def instantiate_at_level(self, level: int) -> Dict[str, Any]:
        """Get level-specific instantiation of pattern."""
        base = self.pattern_template.copy()

        # Apply level adaptations if any
        if level in self.level_adaptations:
            base.update(self.level_adaptations[level])

        base['instantiation_level'] = level
        return base

    def record_application(self, level: int, success: bool) -> None:
        """Record pattern application at level."""
        self.applications_by_level[level] = self.applications_by_level.get(level, 0) + 1
        if success:
            self.successes_by_level[level] = self.successes_by_level.get(level, 0) + 1

    def success_rate_at_level(self, level: int) -> float:
        """Get success rate at level."""
        apps = self.applications_by_level.get(level, 0)
        if apps == 0:
            return 0.0
        succs = self.successes_by_level.get(level, 0)
        return succs / apps

    def overall_success_rate(self) -> float:
        """Get overall success rate across levels."""
        total_apps = sum(self.applications_by_level.values())
        if total_apps == 0:
            return 0.0
        total_succs = sum(self.successes_by_level.values())
        return total_succs / total_apps

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'min_level': self.min_level,
            'max_level': self.max_level,
            'pattern_template': self.pattern_template,
            'level_adaptations': self.level_adaptations,
            'applications_by_level': self.applications_by_level,
            'successes_by_level': self.successes_by_level,
            'overall_success_rate': self.overall_success_rate(),
            'metadata': self.metadata
        }


@dataclass
class CompressedPatterns:
    """
    Patterns compressed to a higher meta-level.

    When patterns at level N are observed, they can be
    compressed into meta-patterns at level N+1 that
    capture what's common across them.
    """
    id: str
    source_level: int
    target_level: int
    source_patterns: List[str]  # IDs of source patterns

    # Compressed representation
    compressed_template: Dict[str, Any] = field(default_factory=dict)

    # Compression statistics
    compression_ratio: float = 0.0
    preservation_score: float = 0.0  # How much info is preserved

    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'source_level': self.source_level,
            'target_level': self.target_level,
            'source_patterns': self.source_patterns,
            'compressed_template': self.compressed_template,
            'compression_ratio': self.compression_ratio,
            'preservation_score': self.preservation_score,
            'metadata': self.metadata,
            'created_at': self.created_at
        }


class LevelInvariantPrimitive(ABC):
    """
    A primitive operation that works at any meta-level.

    These primitives form the basis of level-invariant improvement.
    The same primitive can operate on:
    - Data at level 0
    - Improvement strategies at level 1
    - Meta-strategies at level 2
    - etc.
    """

    def __init__(self, name: str):
        """Initialize primitive."""
        self.name = name

    @abstractmethod
    def apply(
        self,
        target: Improvable,
        context: Dict = None
    ) -> Improvable:
        """Apply primitive at any level."""
        pass

    @abstractmethod
    def compose(
        self,
        other: "LevelInvariantPrimitive"
    ) -> "LevelInvariantPrimitive":
        """Compose with another primitive."""
        pass


class ObservePrimitive(LevelInvariantPrimitive):
    """
    Observe and extract features from target.

    Works at any level:
    - Level 0: Observe data properties
    - Level 1: Observe improvement patterns
    - Level 2: Observe meta-improvement patterns
    """

    def __init__(self):
        """Initialize observe primitive."""
        super().__init__("observe")

    def apply(self, target: Improvable, context: Dict = None) -> Improvable:
        """Observe target and annotate with observations."""
        observations = {
            'level': target.level,
            'score': target.score,
            'has_content': target.content is not None,
            'metadata_keys': list(target.metadata.keys())
        }

        return Improvable(
            id=f"observed_{target.id}",
            level=target.level,
            content=target.content,
            score=target.score,
            metadata={**target.metadata, 'observations': observations}
        )

    def compose(self, other: LevelInvariantPrimitive) -> LevelInvariantPrimitive:
        """Compose: observe then apply other."""
        return ComposedPrimitive(self, other)


class TransformPrimitive(LevelInvariantPrimitive):
    """
    Transform target structure.

    Works at any level to modify structure while preserving
    level-invariant properties.
    """

    def __init__(self, transform_fn: callable = None):
        """Initialize transform primitive."""
        super().__init__("transform")
        self.transform_fn = transform_fn

    def apply(self, target: Improvable, context: Dict = None) -> Improvable:
        """Transform target."""
        new_content = target.content

        if self.transform_fn and target.content:
            try:
                new_content = self.transform_fn(target.content, context or {})
            except Exception as e:
                logger.warning(f"Transform failed: {e}")

        return Improvable(
            id=f"transformed_{target.id}",
            level=target.level,
            content=new_content,
            score=target.score,
            metadata={**target.metadata, 'transformed': True}
        )

    def compose(self, other: LevelInvariantPrimitive) -> LevelInvariantPrimitive:
        """Compose: transform then apply other."""
        return ComposedPrimitive(self, other)


class EvaluatePrimitive(LevelInvariantPrimitive):
    """
    Evaluate and score target.

    Works at any level to assign quality scores.
    """

    def __init__(self, eval_fn: callable = None):
        """Initialize evaluate primitive."""
        super().__init__("evaluate")
        self.eval_fn = eval_fn

    def apply(self, target: Improvable, context: Dict = None) -> Improvable:
        """Evaluate target and update score."""
        new_score = target.score

        if self.eval_fn:
            try:
                new_score = self.eval_fn(target, context or {})
            except Exception as e:
                logger.warning(f"Evaluation failed: {e}")

        return Improvable(
            id=target.id,
            level=target.level,
            content=target.content,
            score=new_score,
            metadata={**target.metadata, 'evaluated': True}
        )

    def compose(self, other: LevelInvariantPrimitive) -> LevelInvariantPrimitive:
        """Compose: evaluate then apply other."""
        return ComposedPrimitive(self, other)


class SelectPrimitive(LevelInvariantPrimitive):
    """
    Select best among options.

    Works at any level to choose highest-scoring option.
    """

    def __init__(self):
        """Initialize select primitive."""
        super().__init__("select")

    def apply(self, target: Improvable, context: Dict = None) -> Improvable:
        """Select from options in content."""
        context = context or {}
        options = context.get('options', [target])

        if not options:
            return target

        # Select highest scoring
        best = max(options, key=lambda x: x.score if hasattr(x, 'score') else 0)

        return Improvable(
            id=f"selected_{target.id}",
            level=target.level,
            content=best.content if hasattr(best, 'content') else best,
            score=best.score if hasattr(best, 'score') else 0.0,
            metadata={**target.metadata, 'selected_from': len(options)}
        )

    def compose(self, other: LevelInvariantPrimitive) -> LevelInvariantPrimitive:
        """Compose: select then apply other."""
        return ComposedPrimitive(self, other)


class ComposedPrimitive(LevelInvariantPrimitive):
    """Composition of two primitives."""

    def __init__(self, first: LevelInvariantPrimitive, second: LevelInvariantPrimitive):
        """Initialize composed primitive."""
        super().__init__(f"{first.name};{second.name}")
        self.first = first
        self.second = second

    def apply(self, target: Improvable, context: Dict = None) -> Improvable:
        """Apply first, then second."""
        intermediate = self.first.apply(target, context)
        return self.second.apply(intermediate, context)

    def compose(self, other: LevelInvariantPrimitive) -> LevelInvariantPrimitive:
        """Compose with another."""
        return ComposedPrimitive(self, other)


class MetaLevelCompressor:
    """
    Compresses patterns from level N to level N+1.

    Finds common structure across patterns at a level
    and abstracts it into a higher-level pattern.
    """

    def __init__(self, config: Dict = None):
        """Initialize compressor."""
        self.config = config or {}
        self._min_patterns = self.config.get('min_patterns', 3)
        self._similarity_threshold = self.config.get('similarity_threshold', 0.7)

    def compress_to_level(
        self,
        patterns: List[LeveledPattern],
        target_level: int
    ) -> List[CompressedPatterns]:
        """
        Compress patterns to higher meta-level.

        Extracts level-invariant representations from
        patterns at level N to create meta-patterns at level N+1.
        """
        if len(patterns) < self._min_patterns:
            return []

        # Group patterns by similarity
        groups = self._group_similar(patterns)

        compressed = []
        for group in groups:
            if len(group) >= self._min_patterns:
                comp = self._compress_group(group, target_level)
                compressed.append(comp)

        logger.info(
            f"Compressed {len(patterns)} patterns to "
            f"{len(compressed)} meta-patterns at level {target_level}"
        )

        return compressed

    def _group_similar(
        self,
        patterns: List[LeveledPattern]
    ) -> List[List[LeveledPattern]]:
        """Group similar patterns together."""
        groups = []
        used = set()

        for p in patterns:
            if p.id in used:
                continue

            group = [p]
            used.add(p.id)

            for other in patterns:
                if other.id in used:
                    continue

                if self._similarity(p, other) >= self._similarity_threshold:
                    group.append(other)
                    used.add(other.id)

            groups.append(group)

        return groups

    def _similarity(self, p1: LeveledPattern, p2: LeveledPattern) -> float:
        """Compute similarity between patterns."""
        # Compare template keys
        keys1 = set(p1.pattern_template.keys())
        keys2 = set(p2.pattern_template.keys())

        if not keys1 and not keys2:
            return 1.0

        intersection = len(keys1 & keys2)
        union = len(keys1 | keys2)

        return intersection / union if union > 0 else 0.0

    def _compress_group(
        self,
        group: List[LeveledPattern],
        target_level: int
    ) -> CompressedPatterns:
        """Compress a group of patterns."""
        # Extract common template
        common_template = {}

        if group:
            # Start with first pattern's template
            common_template = group[0].pattern_template.copy()

            # Keep only keys present in all patterns
            for p in group[1:]:
                common_keys = set(common_template.keys()) & set(p.pattern_template.keys())
                common_template = {k: common_template[k] for k in common_keys}

        # Calculate compression metrics
        original_size = sum(len(p.pattern_template) for p in group)
        compressed_size = len(common_template)
        compression_ratio = compressed_size / original_size if original_size > 0 else 0

        return CompressedPatterns(
            id=f"compressed_{uuid.uuid4().hex[:12]}",
            source_level=group[0].min_level if group else 0,
            target_level=target_level,
            source_patterns=[p.id for p in group],
            compressed_template=common_template,
            compression_ratio=compression_ratio,
            preservation_score=1.0 - compression_ratio,
            metadata={
                'group_size': len(group),
                'original_size': original_size
            }
        )
