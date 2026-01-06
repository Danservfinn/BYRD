"""
Recursive Depth Amplifier.

Enables unbounded recursive improvement - the same primitives
work at any meta-level.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 3.3 for specification.
"""

from typing import Dict, List, Optional, Any, Generic, TypeVar
from dataclasses import dataclass, field
from datetime import datetime, timezone
import uuid
import logging

from .algebra import (
    Improvement,
    ImprovementResult,
    ImprovementType,
    ImprovementAlgebra,
    FunctionImprovement,
    RecursiveImprovement,
)
from .representation import (
    Improvable,
    LeveledPattern,
    CompressedPatterns,
    MetaLevelCompressor,
    LevelInvariantPrimitive,
    ObservePrimitive,
    TransformPrimitive,
    EvaluatePrimitive,
    SelectPrimitive,
)

logger = logging.getLogger("rsi.recursion.depth_amplifier")

T = TypeVar('T')


@dataclass
class AmplificationConfig:
    """Configuration for depth amplification."""
    max_depth: int = 5
    min_improvement_threshold: float = 0.01
    compression_enabled: bool = True
    pattern_extraction_enabled: bool = True
    early_stopping: bool = True
    cost_limit: float = 1000.0

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'max_depth': self.max_depth,
            'min_improvement_threshold': self.min_improvement_threshold,
            'compression_enabled': self.compression_enabled,
            'pattern_extraction_enabled': self.pattern_extraction_enabled,
            'early_stopping': self.early_stopping,
            'cost_limit': self.cost_limit
        }


@dataclass
class AmplificationResult:
    """Result of recursive depth amplification."""
    id: str
    success: bool
    original: Improvable
    final: Improvable
    depth_reached: int
    total_improvement: float
    level_results: List[Dict] = field(default_factory=list)
    patterns_extracted: List[str] = field(default_factory=list)
    compressions_performed: int = 0
    total_cost: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'success': self.success,
            'original': self.original.to_dict(),
            'final': self.final.to_dict(),
            'depth_reached': self.depth_reached,
            'total_improvement': self.total_improvement,
            'level_results': self.level_results,
            'patterns_extracted': self.patterns_extracted,
            'compressions_performed': self.compressions_performed,
            'total_cost': self.total_cost,
            'metadata': self.metadata,
            'created_at': self.created_at
        }


class RecursiveDepthAmplifier:
    """
    Enables unbounded recursive improvement.

    The same primitives work at any meta-level:
    - Level 0: Improve the target directly
    - Level 1: Improve the improvement strategy
    - Level 2: Improve how we improve improvement strategies
    - Level N: Improve^N

    Key insight: The improvement operation itself is improvable,
    enabling recursive self-improvement.
    """

    def __init__(self, config: AmplificationConfig = None):
        """
        Initialize recursive depth amplifier.

        Args:
            config: Amplification configuration
        """
        self.config = config or AmplificationConfig()

        # Core primitives
        self._observe = ObservePrimitive()
        self._transform = TransformPrimitive()
        self._evaluate = EvaluatePrimitive()
        self._select = SelectPrimitive()

        # Pattern extraction
        self._patterns: Dict[int, List[LeveledPattern]] = {}
        self._compressor = MetaLevelCompressor()

        # Statistics
        self._total_amplifications: int = 0
        self._max_depth_achieved: int = 0
        self._total_improvements: float = 0.0

    async def improve_at_level(
        self,
        target: Improvable,
        improvement: Improvement,
        level: int
    ) -> ImprovementResult[Improvable]:
        """
        Improve target at specified meta-level.

        Level 0 = base improvement
        Level 1 = improve the improvement
        Level N = improve^N

        Args:
            target: Target to improve
            improvement: Improvement to apply
            level: Meta-level

        Returns:
            ImprovementResult
        """
        if level == 0:
            # Base case: direct improvement
            return await improvement.apply(target, {'level': 0})

        # Meta case: wrap improvement for meta-level
        meta_improvement = self._create_meta_improvement(improvement, level)
        return await meta_improvement.apply(target, {'level': level})

    def _create_meta_improvement(
        self,
        base: Improvement,
        level: int
    ) -> Improvement:
        """Create meta-improvement at specified level."""
        # Build recursive improvement
        return ImprovementAlgebra.recurse(base, level)

    async def amplify(
        self,
        target: Improvable,
        improvement: Improvement,
        context: Dict = None
    ) -> AmplificationResult:
        """
        Amplify improvement through recursive depth.

        Applies improvement at increasing meta-levels until:
        - Improvement falls below threshold
        - Maximum depth is reached
        - Cost limit exceeded

        Args:
            target: Target to improve
            improvement: Base improvement
            context: Additional context

        Returns:
            AmplificationResult with final target and statistics
        """
        context = context or {}
        self._total_amplifications += 1

        current = target
        level_results = []
        total_improvement = 0.0
        total_cost = 0.0
        patterns_extracted = []

        for depth in range(self.config.max_depth):
            # Check cost limit
            est_cost = improvement.estimate_cost(current)
            if total_cost + est_cost > self.config.cost_limit:
                logger.info(f"Cost limit reached at depth {depth}")
                break

            # Apply improvement at this level
            level_context = {**context, 'depth': depth, 'level': depth}
            result = await self.improve_at_level(current, improvement, depth)

            level_results.append({
                'depth': depth,
                'success': result.success,
                'delta_score': result.delta_score,
                'cost': est_cost
            })

            total_cost += est_cost

            if not result.success:
                logger.info(f"Improvement failed at depth {depth}")
                break

            # Update current
            if result.improved is not None:
                if isinstance(result.improved, Improvable):
                    current = result.improved
                else:
                    # Wrap non-Improvable result
                    current = Improvable(
                        id=f"improved_{current.id}",
                        level=depth,
                        content=result.improved,
                        score=current.score + result.delta_score
                    )

            total_improvement += result.delta_score

            # Check for pattern extraction
            if self.config.pattern_extraction_enabled:
                pattern = self._extract_pattern(improvement, depth, result)
                if pattern:
                    patterns_extracted.append(pattern.id)

            # Early stopping if improvement is too small
            if (self.config.early_stopping and
                    result.delta_score < self.config.min_improvement_threshold):
                logger.info(f"Early stopping at depth {depth}: improvement too small")
                break

        # Update max depth achieved
        depth_reached = len(level_results)
        if depth_reached > self._max_depth_achieved:
            self._max_depth_achieved = depth_reached

        self._total_improvements += total_improvement

        # Perform compression if enabled
        compressions = 0
        if self.config.compression_enabled:
            compressions = await self._compress_patterns()

        return AmplificationResult(
            id=f"amp_{uuid.uuid4().hex[:12]}",
            success=total_improvement > 0,
            original=target,
            final=current,
            depth_reached=depth_reached,
            total_improvement=total_improvement,
            level_results=level_results,
            patterns_extracted=patterns_extracted,
            compressions_performed=compressions,
            total_cost=total_cost,
            metadata=context
        )

    async def amplify_until_convergence(
        self,
        target: Improvable,
        improvement: Improvement,
        convergence_threshold: float = 0.001,
        max_rounds: int = 10
    ) -> AmplificationResult:
        """
        Amplify until improvement converges.

        Keeps amplifying until the improvement per round
        falls below convergence threshold.

        Args:
            target: Target to improve
            improvement: Base improvement
            convergence_threshold: Stop when improvement < this
            max_rounds: Maximum amplification rounds

        Returns:
            Combined AmplificationResult
        """
        current = target
        all_level_results = []
        total_improvement = 0.0
        all_patterns = []
        total_compressions = 0
        total_cost = 0.0

        for round_num in range(max_rounds):
            result = await self.amplify(
                current,
                improvement,
                context={'round': round_num}
            )

            all_level_results.extend(result.level_results)
            total_improvement += result.total_improvement
            all_patterns.extend(result.patterns_extracted)
            total_compressions += result.compressions_performed
            total_cost += result.total_cost

            current = result.final

            # Check convergence
            if result.total_improvement < convergence_threshold:
                logger.info(
                    f"Converged after {round_num + 1} rounds "
                    f"(improvement: {result.total_improvement:.6f})"
                )
                break

        return AmplificationResult(
            id=f"amp_conv_{uuid.uuid4().hex[:12]}",
            success=total_improvement > 0,
            original=target,
            final=current,
            depth_reached=len(all_level_results),
            total_improvement=total_improvement,
            level_results=all_level_results,
            patterns_extracted=all_patterns,
            compressions_performed=total_compressions,
            total_cost=total_cost,
            metadata={'rounds': round_num + 1, 'converged': True}
        )

    def _extract_pattern(
        self,
        improvement: Improvement,
        depth: int,
        result: ImprovementResult
    ) -> Optional[LeveledPattern]:
        """Extract pattern from successful improvement."""
        if not result.success or result.delta_score <= 0:
            return None

        pattern = LeveledPattern(
            id=f"pattern_{uuid.uuid4().hex[:12]}",
            name=f"Pattern from {improvement.name} at depth {depth}",
            description=f"Extracted from improvement with delta {result.delta_score:.4f}",
            min_level=depth,
            max_level=depth + 2,  # Pattern likely works at nearby levels
            pattern_template={
                'improvement_name': improvement.name,
                'depth': depth,
                'delta_score': result.delta_score,
                'improvement_type': result.improvement_type.value
            }
        )

        # Store pattern
        if depth not in self._patterns:
            self._patterns[depth] = []
        self._patterns[depth].append(pattern)

        return pattern

    async def _compress_patterns(self) -> int:
        """Compress patterns to higher levels."""
        compressions = 0

        for level, patterns in list(self._patterns.items()):
            if len(patterns) >= 3:
                compressed = self._compressor.compress_to_level(
                    patterns,
                    target_level=level + 1
                )

                if compressed:
                    compressions += len(compressed)
                    logger.debug(
                        f"Compressed {len(patterns)} patterns at level {level} "
                        f"to {len(compressed)} patterns at level {level + 1}"
                    )

        return compressions

    async def compress_to_level(
        self,
        patterns: List[LeveledPattern],
        target_level: int
    ) -> List[CompressedPatterns]:
        """
        Compress patterns to higher meta-level.

        Extracts level-invariant representations from
        patterns at level N to create meta-patterns at level N+1.
        """
        return self._compressor.compress_to_level(patterns, target_level)

    def get_primitives(self) -> Dict[str, LevelInvariantPrimitive]:
        """Get available level-invariant primitives."""
        return {
            'observe': self._observe,
            'transform': self._transform,
            'evaluate': self._evaluate,
            'select': self._select
        }

    def get_patterns_at_level(self, level: int) -> List[LeveledPattern]:
        """Get patterns at specified level."""
        return self._patterns.get(level, [])

    def get_all_patterns(self) -> Dict[int, List[LeveledPattern]]:
        """Get all patterns by level."""
        return self._patterns.copy()

    def get_stats(self) -> Dict:
        """Get amplifier statistics."""
        return {
            'total_amplifications': self._total_amplifications,
            'max_depth_achieved': self._max_depth_achieved,
            'total_improvements': self._total_improvements,
            'patterns_by_level': {
                level: len(patterns)
                for level, patterns in self._patterns.items()
            },
            'total_patterns': sum(
                len(patterns) for patterns in self._patterns.values()
            ),
            'config': self.config.to_dict()
        }

    def reset(self) -> None:
        """Reset amplifier state."""
        self._patterns.clear()
        self._total_amplifications = 0
        self._max_depth_achieved = 0
        self._total_improvements = 0.0
        logger.info("RecursiveDepthAmplifier reset")
