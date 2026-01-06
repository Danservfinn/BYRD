"""
Improvement Algebra.

Composable improvement operators for recursive self-improvement.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 3.3 for specification.
"""

from typing import Dict, List, Optional, Any, Callable, TypeVar, Generic, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
from abc import ABC, abstractmethod
import uuid
import logging
import asyncio

logger = logging.getLogger("rsi.recursion.algebra")

# Type variable for improvable targets
T = TypeVar('T')


class ImprovementType(Enum):
    """Types of improvement operations."""
    PARAMETER = "parameter"       # Tune parameters
    STRUCTURE = "structure"       # Modify structure
    COMPOSITION = "composition"   # Combine elements
    DISCOVERY = "discovery"       # Find new approaches
    META = "meta"                 # Improve improvement


@dataclass
class ImprovementResult(Generic[T]):
    """Result of an improvement operation."""
    id: str
    success: bool
    original: T
    improved: Optional[T]
    improvement_type: ImprovementType
    delta_score: float  # Improvement in score
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'success': self.success,
            'improvement_type': self.improvement_type.value,
            'delta_score': self.delta_score,
            'metadata': self.metadata,
            'created_at': self.created_at
        }


class Improvement(ABC, Generic[T]):
    """
    Base class for improvement operations.

    Improvements are composable operations that can be applied
    to any improvable target.
    """

    def __init__(self, name: str = None):
        """Initialize improvement."""
        self.id = f"imp_{uuid.uuid4().hex[:12]}"
        self.name = name or self.__class__.__name__

    @abstractmethod
    async def apply(self, target: T, context: Dict = None) -> ImprovementResult[T]:
        """
        Apply improvement to target.

        Args:
            target: Target to improve
            context: Additional context

        Returns:
            ImprovementResult with outcome
        """
        pass

    @abstractmethod
    def estimate_cost(self, target: T) -> float:
        """Estimate computational cost."""
        pass


class IdentityImprovement(Improvement[T]):
    """No-op improvement that returns target unchanged."""

    async def apply(self, target: T, context: Dict = None) -> ImprovementResult[T]:
        """Return target unchanged."""
        return ImprovementResult(
            id=f"result_{uuid.uuid4().hex[:12]}",
            success=True,
            original=target,
            improved=target,
            improvement_type=ImprovementType.PARAMETER,
            delta_score=0.0,
            metadata={'operation': 'identity'}
        )

    def estimate_cost(self, target: T) -> float:
        """Identity has zero cost."""
        return 0.0


class FunctionImprovement(Improvement[T]):
    """Improvement from a callable function."""

    def __init__(
        self,
        func: Callable[[T, Dict], T],
        name: str = None,
        improvement_type: ImprovementType = ImprovementType.PARAMETER,
        cost: float = 1.0
    ):
        """Initialize function improvement."""
        super().__init__(name or func.__name__)
        self.func = func
        self.improvement_type = improvement_type
        self._cost = cost

    async def apply(self, target: T, context: Dict = None) -> ImprovementResult[T]:
        """Apply function to target."""
        context = context or {}

        try:
            # Handle both sync and async functions
            if asyncio.iscoroutinefunction(self.func):
                improved = await self.func(target, context)
            else:
                improved = self.func(target, context)

            return ImprovementResult(
                id=f"result_{uuid.uuid4().hex[:12]}",
                success=True,
                original=target,
                improved=improved,
                improvement_type=self.improvement_type,
                delta_score=context.get('delta_score', 0.0),
                metadata={'function': self.name}
            )

        except Exception as e:
            logger.error(f"FunctionImprovement failed: {e}")
            return ImprovementResult(
                id=f"result_{uuid.uuid4().hex[:12]}",
                success=False,
                original=target,
                improved=None,
                improvement_type=self.improvement_type,
                delta_score=0.0,
                metadata={'error': str(e)}
            )

    def estimate_cost(self, target: T) -> float:
        """Return configured cost."""
        return self._cost


class ImprovementAlgebra:
    """
    Composable improvement operators.

    Provides algebraic operations for combining improvements
    into complex improvement strategies.
    """

    @staticmethod
    def sequential(
        a: Improvement[T],
        b: Improvement[T],
        name: str = None
    ) -> Improvement[T]:
        """
        Apply a, then b (a ; b).

        Sequential composition - the output of a becomes
        the input to b.
        """
        return SequentialImprovement(a, b, name)

    @staticmethod
    def parallel(
        a: Improvement[T],
        b: Improvement[T],
        merge: Callable[[T, T], T] = None,
        name: str = None
    ) -> Improvement[T]:
        """
        Apply both a and b, merge results (a || b).

        Parallel composition - both improvements run on the
        original target, results are merged.
        """
        return ParallelImprovement(a, b, merge, name)

    @staticmethod
    def conditional(
        improvement: Improvement[T],
        condition: Callable[[T, Dict], bool],
        name: str = None
    ) -> Improvement[T]:
        """
        Apply only if condition is met.

        Conditional improvement - only executes if predicate
        returns True.
        """
        return ConditionalImprovement(improvement, condition, name)

    @staticmethod
    def recurse(
        improvement: Improvement[T],
        depth: int,
        name: str = None
    ) -> Improvement[T]:
        """
        Apply at N meta-levels.

        Recursive improvement - applies improvement to itself
        depth times, enabling meta-improvement.
        """
        return RecursiveImprovement(improvement, depth, name)

    @staticmethod
    def until(
        improvement: Improvement[T],
        condition: Callable[[ImprovementResult[T]], bool],
        max_iterations: int = 10,
        name: str = None
    ) -> Improvement[T]:
        """
        Apply until condition is met.

        Iterative improvement - keeps applying until condition
        is satisfied or max iterations reached.
        """
        return UntilImprovement(improvement, condition, max_iterations, name)

    @staticmethod
    def choice(
        improvements: List[Improvement[T]],
        selector: Callable[[T, Dict], int] = None,
        name: str = None
    ) -> Improvement[T]:
        """
        Choose one improvement based on context.

        Selection improvement - picks best improvement for
        the given target and context.
        """
        return ChoiceImprovement(improvements, selector, name)

    @staticmethod
    def fallback(
        primary: Improvement[T],
        fallback: Improvement[T],
        name: str = None
    ) -> Improvement[T]:
        """
        Try primary, use fallback if it fails.

        Fallback improvement - provides resilience against
        improvement failures.
        """
        return FallbackImprovement(primary, fallback, name)

    @staticmethod
    def identity() -> Improvement[T]:
        """Return identity improvement (no-op)."""
        return IdentityImprovement()

    @staticmethod
    def from_function(
        func: Callable[[T, Dict], T],
        name: str = None,
        improvement_type: ImprovementType = ImprovementType.PARAMETER
    ) -> Improvement[T]:
        """Create improvement from function."""
        return FunctionImprovement(func, name, improvement_type)


class SequentialImprovement(Improvement[T]):
    """Sequential composition of improvements."""

    def __init__(self, a: Improvement[T], b: Improvement[T], name: str = None):
        """Initialize sequential improvement."""
        super().__init__(name or f"({a.name} ; {b.name})")
        self.a = a
        self.b = b

    async def apply(self, target: T, context: Dict = None) -> ImprovementResult[T]:
        """Apply a, then b."""
        context = context or {}

        # Apply first improvement
        result_a = await self.a.apply(target, context)

        if not result_a.success or result_a.improved is None:
            return ImprovementResult(
                id=f"result_{uuid.uuid4().hex[:12]}",
                success=False,
                original=target,
                improved=None,
                improvement_type=ImprovementType.COMPOSITION,
                delta_score=0.0,
                metadata={'failed_at': 'first', 'reason': result_a.metadata}
            )

        # Apply second improvement to result
        result_b = await self.b.apply(result_a.improved, context)

        return ImprovementResult(
            id=f"result_{uuid.uuid4().hex[:12]}",
            success=result_b.success,
            original=target,
            improved=result_b.improved,
            improvement_type=ImprovementType.COMPOSITION,
            delta_score=result_a.delta_score + result_b.delta_score,
            metadata={
                'first': result_a.to_dict(),
                'second': result_b.to_dict()
            }
        )

    def estimate_cost(self, target: T) -> float:
        """Sum of costs."""
        return self.a.estimate_cost(target) + self.b.estimate_cost(target)


class ParallelImprovement(Improvement[T]):
    """Parallel composition of improvements."""

    def __init__(
        self,
        a: Improvement[T],
        b: Improvement[T],
        merge: Callable[[T, T], T] = None,
        name: str = None
    ):
        """Initialize parallel improvement."""
        super().__init__(name or f"({a.name} || {b.name})")
        self.a = a
        self.b = b
        self.merge = merge or self._default_merge

    def _default_merge(self, x: T, y: T) -> T:
        """Default merge - return first."""
        return x

    async def apply(self, target: T, context: Dict = None) -> ImprovementResult[T]:
        """Apply both and merge."""
        context = context or {}

        # Run both in parallel
        result_a, result_b = await asyncio.gather(
            self.a.apply(target, context),
            self.b.apply(target, context)
        )

        # Merge results
        if result_a.success and result_b.success:
            merged = self.merge(result_a.improved, result_b.improved)
            success = True
        elif result_a.success:
            merged = result_a.improved
            success = True
        elif result_b.success:
            merged = result_b.improved
            success = True
        else:
            merged = None
            success = False

        return ImprovementResult(
            id=f"result_{uuid.uuid4().hex[:12]}",
            success=success,
            original=target,
            improved=merged,
            improvement_type=ImprovementType.COMPOSITION,
            delta_score=max(result_a.delta_score, result_b.delta_score),
            metadata={
                'first': result_a.to_dict(),
                'second': result_b.to_dict()
            }
        )

    def estimate_cost(self, target: T) -> float:
        """Max of costs (parallel execution)."""
        return max(self.a.estimate_cost(target), self.b.estimate_cost(target))


class ConditionalImprovement(Improvement[T]):
    """Conditional improvement."""

    def __init__(
        self,
        improvement: Improvement[T],
        condition: Callable[[T, Dict], bool],
        name: str = None
    ):
        """Initialize conditional improvement."""
        super().__init__(name or f"if ? {improvement.name}")
        self.improvement = improvement
        self.condition = condition

    async def apply(self, target: T, context: Dict = None) -> ImprovementResult[T]:
        """Apply if condition met."""
        context = context or {}

        if self.condition(target, context):
            return await self.improvement.apply(target, context)

        # Condition not met - return identity
        return ImprovementResult(
            id=f"result_{uuid.uuid4().hex[:12]}",
            success=True,
            original=target,
            improved=target,
            improvement_type=ImprovementType.PARAMETER,
            delta_score=0.0,
            metadata={'skipped': True, 'reason': 'condition_not_met'}
        )

    def estimate_cost(self, target: T) -> float:
        """Expected cost based on probability."""
        return self.improvement.estimate_cost(target) * 0.5


class RecursiveImprovement(Improvement[T]):
    """Recursive meta-improvement."""

    def __init__(
        self,
        improvement: Improvement[T],
        depth: int,
        name: str = None
    ):
        """Initialize recursive improvement."""
        super().__init__(name or f"recurse({improvement.name}, {depth})")
        self.improvement = improvement
        self.depth = depth

    async def apply(self, target: T, context: Dict = None) -> ImprovementResult[T]:
        """Apply at N meta-levels."""
        context = context or {}
        current = target
        total_delta = 0.0
        results = []

        for level in range(self.depth):
            # Add level to context
            level_context = {**context, 'recursion_level': level}

            result = await self.improvement.apply(current, level_context)
            results.append(result.to_dict())

            if not result.success:
                break

            current = result.improved
            total_delta += result.delta_score

        return ImprovementResult(
            id=f"result_{uuid.uuid4().hex[:12]}",
            success=results[-1]['success'] if results else False,
            original=target,
            improved=current,
            improvement_type=ImprovementType.META,
            delta_score=total_delta,
            metadata={
                'depth': self.depth,
                'levels_completed': len(results),
                'level_results': results
            }
        )

    def estimate_cost(self, target: T) -> float:
        """Cost grows with depth."""
        base_cost = self.improvement.estimate_cost(target)
        return base_cost * self.depth


class UntilImprovement(Improvement[T]):
    """Iterative improvement until condition."""

    def __init__(
        self,
        improvement: Improvement[T],
        condition: Callable[[ImprovementResult[T]], bool],
        max_iterations: int = 10,
        name: str = None
    ):
        """Initialize until improvement."""
        super().__init__(name or f"until({improvement.name})")
        self.improvement = improvement
        self.condition = condition
        self.max_iterations = max_iterations

    async def apply(self, target: T, context: Dict = None) -> ImprovementResult[T]:
        """Apply until condition met."""
        context = context or {}
        current = target
        total_delta = 0.0
        iterations = 0

        for i in range(self.max_iterations):
            iterations += 1
            iter_context = {**context, 'iteration': i}

            result = await self.improvement.apply(current, iter_context)

            if not result.success:
                break

            current = result.improved
            total_delta += result.delta_score

            # Check termination condition
            if self.condition(result):
                break

        return ImprovementResult(
            id=f"result_{uuid.uuid4().hex[:12]}",
            success=True,
            original=target,
            improved=current,
            improvement_type=ImprovementType.COMPOSITION,
            delta_score=total_delta,
            metadata={
                'iterations': iterations,
                'max_iterations': self.max_iterations
            }
        )

    def estimate_cost(self, target: T) -> float:
        """Expected iterations cost."""
        base_cost = self.improvement.estimate_cost(target)
        return base_cost * (self.max_iterations / 2)


class ChoiceImprovement(Improvement[T]):
    """Choice between improvements."""

    def __init__(
        self,
        improvements: List[Improvement[T]],
        selector: Callable[[T, Dict], int] = None,
        name: str = None
    ):
        """Initialize choice improvement."""
        names = [imp.name for imp in improvements]
        super().__init__(name or f"choice({', '.join(names)})")
        self.improvements = improvements
        self.selector = selector or (lambda t, c: 0)

    async def apply(self, target: T, context: Dict = None) -> ImprovementResult[T]:
        """Apply selected improvement."""
        context = context or {}

        # Select improvement
        index = self.selector(target, context)
        index = max(0, min(index, len(self.improvements) - 1))

        selected = self.improvements[index]

        result = await selected.apply(target, context)

        return ImprovementResult(
            id=f"result_{uuid.uuid4().hex[:12]}",
            success=result.success,
            original=target,
            improved=result.improved,
            improvement_type=result.improvement_type,
            delta_score=result.delta_score,
            metadata={
                'selected_index': index,
                'selected_name': selected.name,
                'inner_result': result.to_dict()
            }
        )

    def estimate_cost(self, target: T) -> float:
        """Average cost across choices."""
        costs = [imp.estimate_cost(target) for imp in self.improvements]
        return sum(costs) / len(costs) if costs else 0.0


class FallbackImprovement(Improvement[T]):
    """Fallback on failure."""

    def __init__(
        self,
        primary: Improvement[T],
        fallback: Improvement[T],
        name: str = None
    ):
        """Initialize fallback improvement."""
        super().__init__(name or f"try({primary.name}) else({fallback.name})")
        self.primary = primary
        self.fallback = fallback

    async def apply(self, target: T, context: Dict = None) -> ImprovementResult[T]:
        """Try primary, fallback if fails."""
        context = context or {}

        result = await self.primary.apply(target, context)

        if result.success:
            return result

        # Primary failed, try fallback
        logger.info(f"Primary improvement failed, trying fallback")
        fallback_result = await self.fallback.apply(target, context)

        return ImprovementResult(
            id=f"result_{uuid.uuid4().hex[:12]}",
            success=fallback_result.success,
            original=target,
            improved=fallback_result.improved,
            improvement_type=fallback_result.improvement_type,
            delta_score=fallback_result.delta_score,
            metadata={
                'used_fallback': True,
                'primary_result': result.to_dict(),
                'fallback_result': fallback_result.to_dict()
            }
        )

    def estimate_cost(self, target: T) -> float:
        """Expected cost with fallback probability."""
        primary_cost = self.primary.estimate_cost(target)
        fallback_cost = self.fallback.estimate_cost(target)
        # Assume 80% primary success
        return primary_cost + 0.2 * fallback_cost
