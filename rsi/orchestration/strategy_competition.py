"""
Emergent Strategy Competition.

Implements a pool of competing strategies that evolve through
weighted selection based on performance. Supports:
- Strategy pool with performance tracking
- Weighted random selection
- Strategy discovery through exploration
- Automatic pruning of poor performers

See docs/IMPLEMENTATION_PLAN.md Phase 1.5 for specification.
"""

from typing import Dict, List, Optional, Any, Callable, Awaitable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
import logging
import random
import math

logger = logging.getLogger("rsi.orchestration.strategy_competition")


class StrategyStatus(Enum):
    """Status of a strategy in the pool."""
    ACTIVE = "active"         # Currently in use
    EXPERIMENTAL = "experimental"  # Being tested
    RETIRED = "retired"       # No longer used
    DISCOVERED = "discovered"  # Newly discovered


@dataclass
class Strategy:
    """A strategy in the competition pool."""
    id: str
    name: str
    description: str
    handler: Optional[Callable[..., Awaitable[Any]]] = None

    # Performance tracking
    uses: int = 0
    successes: int = 0
    failures: int = 0
    total_score: float = 0.0

    # Evolution
    created_at: str = ""
    last_used_at: str = ""
    parent_id: Optional[str] = None  # For derived strategies
    status: StrategyStatus = StrategyStatus.ACTIVE

    # Weighting
    base_weight: float = 1.0
    current_weight: float = 1.0

    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc).isoformat()

    @property
    def success_rate(self) -> float:
        """Get success rate."""
        if self.uses == 0:
            return 0.5  # Prior
        return self.successes / self.uses

    @property
    def average_score(self) -> float:
        """Get average score."""
        if self.uses == 0:
            return 0.0
        return self.total_score / self.uses

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'uses': self.uses,
            'successes': self.successes,
            'failures': self.failures,
            'success_rate': self.success_rate,
            'average_score': self.average_score,
            'total_score': self.total_score,
            'created_at': self.created_at,
            'last_used_at': self.last_used_at,
            'parent_id': self.parent_id,
            'status': self.status.value,
            'base_weight': self.base_weight,
            'current_weight': self.current_weight,
            'metadata': self.metadata
        }


@dataclass
class SelectionResult:
    """Result of strategy selection."""
    strategy: Strategy
    selection_method: str  # 'weighted', 'exploration', 'forced'
    pool_size: int
    entropy: float  # Selection entropy
    timestamp: str

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'strategy_id': self.strategy.id,
            'strategy_name': self.strategy.name,
            'selection_method': self.selection_method,
            'pool_size': self.pool_size,
            'entropy': self.entropy,
            'timestamp': self.timestamp
        }


@dataclass
class CompetitionResult:
    """Result of strategy execution in competition."""
    strategy_id: str
    success: bool
    score: float  # Performance score (0-1)
    duration_ms: float
    details: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'strategy_id': self.strategy_id,
            'success': self.success,
            'score': self.score,
            'duration_ms': self.duration_ms,
            'details': self.details,
            'metadata': self.metadata
        }


class StrategyPool:
    """
    Pool of competing strategies with weighted selection.

    Implements Thompson Sampling-inspired selection:
    - Strategies with higher success rates get higher weights
    - Exploration bonus for underused strategies
    - Automatic pruning of poor performers
    """

    def __init__(self, config: Dict = None):
        """Initialize strategy pool."""
        self.config = config or {}

        # Strategies by ID
        self.strategies: Dict[str, Strategy] = {}

        # Configuration
        self.exploration_rate = self.config.get('exploration_rate', 0.1)
        self.min_uses_before_prune = self.config.get('min_uses_before_prune', 10)
        self.prune_threshold = self.config.get('prune_threshold', 0.2)
        self.weight_decay = self.config.get('weight_decay', 0.99)
        self.exploration_bonus = self.config.get('exploration_bonus', 0.1)

        # Statistics
        self._selections: int = 0
        self._explorations: int = 0

        logger.info("StrategyPool initialized")

    def register_strategy(self, strategy: Strategy) -> None:
        """Register a strategy in the pool."""
        self.strategies[strategy.id] = strategy
        logger.info(f"Registered strategy: {strategy.id} ({strategy.name})")

    def create_strategy(
        self,
        name: str,
        description: str,
        handler: Callable = None,
        parent_id: str = None,
        base_weight: float = 1.0
    ) -> Strategy:
        """Create and register a new strategy."""
        strategy_id = f"strategy_{len(self.strategies) + 1}_{name.lower().replace(' ', '_')}"

        strategy = Strategy(
            id=strategy_id,
            name=name,
            description=description,
            handler=handler,
            parent_id=parent_id,
            base_weight=base_weight,
            current_weight=base_weight,
            status=StrategyStatus.EXPERIMENTAL if parent_id else StrategyStatus.ACTIVE
        )

        self.register_strategy(strategy)
        return strategy

    def select(self, context: Dict = None) -> SelectionResult:
        """
        Select a strategy from the pool.

        Uses weighted random selection with exploration bonus.
        """
        self._selections += 1
        timestamp = datetime.now(timezone.utc).isoformat()

        active = [s for s in self.strategies.values()
                  if s.status in [StrategyStatus.ACTIVE, StrategyStatus.EXPERIMENTAL]]

        if not active:
            raise ValueError("No active strategies in pool")

        # Exploration: random selection
        if random.random() < self.exploration_rate:
            self._explorations += 1
            strategy = random.choice(active)
            return SelectionResult(
                strategy=strategy,
                selection_method='exploration',
                pool_size=len(active),
                entropy=self._compute_entropy(active),
                timestamp=timestamp
            )

        # Weighted selection
        weights = []
        for s in active:
            weight = s.current_weight

            # Exploration bonus for underused strategies
            if s.uses < self.min_uses_before_prune:
                weight += self.exploration_bonus * (self.min_uses_before_prune - s.uses)

            weights.append(max(0.01, weight))  # Minimum weight

        # Normalize
        total = sum(weights)
        weights = [w / total for w in weights]

        # Weighted random selection
        r = random.random()
        cumulative = 0.0
        selected = active[0]

        for strategy, weight in zip(active, weights):
            cumulative += weight
            if r <= cumulative:
                selected = strategy
                break

        return SelectionResult(
            strategy=selected,
            selection_method='weighted',
            pool_size=len(active),
            entropy=self._compute_entropy(active),
            timestamp=timestamp
        )

    def record_result(self, result: CompetitionResult) -> None:
        """Record the result of strategy execution."""
        if result.strategy_id not in self.strategies:
            logger.warning(f"Unknown strategy: {result.strategy_id}")
            return

        strategy = self.strategies[result.strategy_id]

        # Update statistics
        strategy.uses += 1
        strategy.total_score += result.score
        strategy.last_used_at = datetime.now(timezone.utc).isoformat()

        if result.success:
            strategy.successes += 1
        else:
            strategy.failures += 1

        # Update weight based on performance
        self._update_weight(strategy, result)

        # Check for pruning
        if strategy.uses >= self.min_uses_before_prune:
            if strategy.success_rate < self.prune_threshold:
                self._retire_strategy(strategy)

    def _update_weight(self, strategy: Strategy, result: CompetitionResult) -> None:
        """Update strategy weight based on result."""
        # Exponential moving average of performance
        alpha = 0.1  # Learning rate

        # Performance signal
        signal = result.score if result.success else -0.1

        # Update weight with decay
        strategy.current_weight *= self.weight_decay
        strategy.current_weight += alpha * signal

        # Clamp weight
        strategy.current_weight = max(0.1, min(10.0, strategy.current_weight))

    def _retire_strategy(self, strategy: Strategy) -> None:
        """Retire a poorly performing strategy."""
        strategy.status = StrategyStatus.RETIRED
        logger.info(
            f"Retired strategy {strategy.id} "
            f"(success rate: {strategy.success_rate:.1%})"
        )

    def _compute_entropy(self, strategies: List[Strategy]) -> float:
        """Compute entropy of strategy weights."""
        if len(strategies) < 2:
            return 0.0

        total = sum(s.current_weight for s in strategies)
        if total == 0:
            return 0.0

        entropy = 0.0
        for s in strategies:
            p = s.current_weight / total
            if p > 0:
                entropy -= p * math.log2(p)

        # Normalize by max entropy
        max_entropy = math.log2(len(strategies))
        return entropy / max_entropy if max_entropy > 0 else 0.0

    def discover_strategy(
        self,
        name: str,
        description: str,
        parent_id: str = None
    ) -> Strategy:
        """Discover a new strategy (typically through exploration)."""
        strategy = self.create_strategy(
            name=name,
            description=description,
            parent_id=parent_id,
            base_weight=0.5  # Start with lower weight
        )
        strategy.status = StrategyStatus.DISCOVERED
        logger.info(f"Discovered new strategy: {name}")
        return strategy

    def get_top_strategies(self, n: int = 5) -> List[Strategy]:
        """Get top N strategies by success rate."""
        active = [s for s in self.strategies.values()
                  if s.status == StrategyStatus.ACTIVE]
        return sorted(active, key=lambda s: s.success_rate, reverse=True)[:n]

    def get_strategy(self, strategy_id: str) -> Optional[Strategy]:
        """Get strategy by ID."""
        return self.strategies.get(strategy_id)

    def get_stats(self) -> Dict:
        """Get pool statistics."""
        active = [s for s in self.strategies.values()
                  if s.status == StrategyStatus.ACTIVE]

        return {
            'total_strategies': len(self.strategies),
            'active_strategies': len(active),
            'selections': self._selections,
            'explorations': self._explorations,
            'exploration_rate_actual': (
                self._explorations / self._selections
                if self._selections > 0 else 0.0
            ),
            'pool_entropy': self._compute_entropy(active),
            'top_strategies': [s.to_dict() for s in self.get_top_strategies(3)]
        }

    def reset(self) -> None:
        """Reset pool statistics (keeps strategies)."""
        self._selections = 0
        self._explorations = 0
        logger.info("StrategyPool reset")


class StrategyCompetitionManager:
    """
    Manages strategy competition within RSI cycles.

    Integrates with Ralph Loop to:
    - Select strategies for each iteration
    - Track performance across iterations
    - Evolve the strategy pool over time
    - Detect strategy collapse (via entropy monitoring)
    """

    def __init__(
        self,
        config: Dict = None,
        drift_monitor=None
    ):
        """Initialize competition manager."""
        self.config = config or {}

        self.pool = StrategyPool(config.get('pool', {}))
        self.drift_monitor = drift_monitor

        # History
        self._selection_history: List[SelectionResult] = []
        self._result_history: List[CompetitionResult] = []

        # Entropy tracking for collapse detection
        self._entropy_history: List[float] = []
        self._entropy_window = self.config.get('entropy_window', 20)
        self._entropy_threshold = self.config.get('entropy_threshold', 0.3)

        logger.info("StrategyCompetitionManager initialized")

    def initialize_default_strategies(self) -> None:
        """Initialize pool with default RSI strategies."""
        strategies = [
            ("TDD Practice", "Test-driven development for code improvement"),
            ("Consistency Check", "Multi-run consistency verification for logic"),
            ("Exploratory", "Open-ended exploration of capability space"),
            ("Targeted Improvement", "Focused improvement on specific metric"),
            ("Meta-Learning", "Learning from previous improvement patterns"),
            ("Decomposition", "Break complex improvements into simpler steps"),
        ]

        for name, desc in strategies:
            self.pool.create_strategy(name, desc)

    async def select_for_iteration(
        self,
        iteration: int,
        context: Dict = None
    ) -> SelectionResult:
        """
        Select strategy for an RSI iteration.

        Args:
            iteration: Current iteration number
            context: Optional context (previous results, etc.)

        Returns:
            SelectionResult with chosen strategy
        """
        result = self.pool.select(context)

        # Track selection
        self._selection_history.append(result)

        # Track entropy for collapse detection
        self._entropy_history.append(result.entropy)
        if len(self._entropy_history) > self._entropy_window:
            self._entropy_history = self._entropy_history[-self._entropy_window:]

        # Report to drift monitor if available
        if self.drift_monitor:
            self.drift_monitor.record_strategy(result.strategy.name)

        logger.debug(
            f"Iteration {iteration}: Selected '{result.strategy.name}' "
            f"via {result.selection_method}"
        )

        return result

    def record_iteration_result(
        self,
        strategy_id: str,
        success: bool,
        score: float = 0.0,
        duration_ms: float = 0.0,
        details: str = ""
    ) -> CompetitionResult:
        """
        Record result of strategy execution.

        Args:
            strategy_id: ID of strategy used
            success: Whether execution succeeded
            score: Performance score (0-1)
            duration_ms: Execution time
            details: Result details

        Returns:
            CompetitionResult
        """
        result = CompetitionResult(
            strategy_id=strategy_id,
            success=success,
            score=score,
            duration_ms=duration_ms,
            details=details
        )

        self.pool.record_result(result)
        self._result_history.append(result)

        # Check for collapse
        if self._detect_collapse():
            logger.warning("Strategy collapse detected - entropy critically low")
            self._inject_diversity()

        return result

    def _detect_collapse(self) -> bool:
        """Detect if strategy selection is collapsing."""
        if len(self._entropy_history) < self._entropy_window:
            return False

        avg_entropy = sum(self._entropy_history[-10:]) / 10
        return avg_entropy < self._entropy_threshold

    def _inject_diversity(self) -> None:
        """Inject diversity when collapse detected."""
        # Temporarily increase exploration rate
        self.pool.exploration_rate = min(0.5, self.pool.exploration_rate * 2)

        # Boost weights of underused strategies
        for strategy in self.pool.strategies.values():
            if strategy.uses < self.pool.min_uses_before_prune:
                strategy.current_weight *= 1.5

        logger.info("Injected diversity into strategy pool")

    def evolve_strategies(self) -> List[Strategy]:
        """
        Evolve the strategy pool based on performance.

        Called periodically to:
        - Create variations of successful strategies
        - Retire poor performers
        - Discover new strategies

        Returns:
            List of newly created/discovered strategies
        """
        new_strategies = []

        top = self.pool.get_top_strategies(3)
        for strategy in top:
            if strategy.success_rate > 0.7 and random.random() < 0.3:
                # Create variation
                variant = self.pool.discover_strategy(
                    name=f"{strategy.name} v{random.randint(2, 9)}",
                    description=f"Variant of {strategy.name}",
                    parent_id=strategy.id
                )
                new_strategies.append(variant)

        return new_strategies

    def get_stats(self) -> Dict:
        """Get competition statistics."""
        return {
            'pool_stats': self.pool.get_stats(),
            'selections_total': len(self._selection_history),
            'results_total': len(self._result_history),
            'average_entropy': (
                sum(self._entropy_history) / len(self._entropy_history)
                if self._entropy_history else 0.0
            ),
            'collapse_risk': self._entropy_history[-1] < self._entropy_threshold
                            if self._entropy_history else False,
            'recent_selections': [
                s.to_dict() for s in self._selection_history[-5:]
            ]
        }

    def reset(self) -> None:
        """Reset competition state."""
        self.pool.reset()
        self._selection_history.clear()
        self._result_history.clear()
        self._entropy_history.clear()
        logger.info("StrategyCompetitionManager reset")
