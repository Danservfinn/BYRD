"""
Neural Architecture Search.

Discovers new module architectures through evolutionary search.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 3.1 for specification.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
import logging
import asyncio
import time
import heapq

from .space import (
    ArchitectureSpace,
    ArchitectureSpec,
    SpaceConstraints,
    SearchBudget
)
from .evaluator import (
    ArchitectureEvaluator,
    ArchitectureScore,
    TestSuite
)

logger = logging.getLogger("rsi.plasticity.nas.search")


class SearchStrategy(Enum):
    """NAS search strategies."""
    RANDOM = "random"
    EVOLUTIONARY = "evolutionary"
    REGULARIZED_EVOLUTION = "regularized_evolution"
    TOURNAMENT = "tournament"


@dataclass
class DiscoveredArchitecture:
    """A discovered architecture with its evaluation."""
    architecture: ArchitectureSpec
    score: ArchitectureScore
    generation: int
    discovery_time_ms: float
    parent_ids: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'architecture': self.architecture.to_dict(),
            'score': self.score.to_dict(),
            'generation': self.generation,
            'discovery_time_ms': self.discovery_time_ms,
            'parent_ids': self.parent_ids
        }


@dataclass
class SearchResult:
    """Complete result of architecture search."""
    best_architecture: Optional[DiscoveredArchitecture]
    all_discovered: List[DiscoveredArchitecture]
    total_evaluations: int
    total_time_seconds: float
    final_generation: int
    converged: bool
    target_reached: bool
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'best_architecture': (
                self.best_architecture.to_dict()
                if self.best_architecture else None
            ),
            'num_discovered': len(self.all_discovered),
            'total_evaluations': self.total_evaluations,
            'total_time_seconds': self.total_time_seconds,
            'final_generation': self.final_generation,
            'converged': self.converged,
            'target_reached': self.target_reached,
            'metadata': self.metadata
        }


class NeuralArchitectureSearch:
    """
    Discovers new module architectures through search.

    Uses evolutionary or gradient-based methods to explore
    the architecture space and find high-performing designs.
    """

    def __init__(
        self,
        space: ArchitectureSpace = None,
        evaluator: ArchitectureEvaluator = None,
        config: Dict = None
    ):
        """
        Initialize NAS.

        Args:
            space: Architecture search space
            evaluator: Architecture evaluator
            config: Configuration options
        """
        self.config = config or {}

        # Initialize or use provided space/evaluator
        self.space = space or ArchitectureSpace()
        self.evaluator = evaluator or ArchitectureEvaluator()

        # Search configuration
        self._strategy = SearchStrategy(
            self.config.get('strategy', 'evolutionary')
        )
        self._population_size = self.config.get('population_size', 20)
        self._mutation_rate = self.config.get('mutation_rate', 0.1)
        self._crossover_rate = self.config.get('crossover_rate', 0.3)
        self._elite_size = self.config.get('elite_size', 5)

        # Search state
        self._population: List[DiscoveredArchitecture] = []
        self._generation: int = 0
        self._best_ever: Optional[DiscoveredArchitecture] = None

        # Statistics
        self._total_searches: int = 0
        self._total_architectures_discovered: int = 0

    async def search(
        self,
        goal: str,
        search_space: ArchitectureSpace = None,
        budget: SearchBudget = None,
        test_suite: TestSuite = None
    ) -> SearchResult:
        """
        Search for architectures that achieve goal.

        Args:
            goal: Description of what architecture should achieve
            search_space: Optional custom search space
            budget: Search budget constraints
            test_suite: Test suite for evaluation

        Returns:
            SearchResult with discovered architectures
        """
        self._total_searches += 1
        start_time = time.time()

        space = search_space or self.space
        budget = budget or SearchBudget()

        # Create default test suite if none provided
        if not test_suite and not self.evaluator._test_suites:
            test_suite = self.evaluator.create_default_test_suite()

        logger.info(
            f"Starting NAS for goal: '{goal}' "
            f"(budget: {budget.max_evaluations} evals, "
            f"{budget.max_time_seconds}s)"
        )

        # Initialize population
        self._population = []
        self._generation = 0
        all_discovered = []
        evaluations = 0
        converged = False
        target_reached = False
        no_improvement_count = 0

        # Initial random population
        for i in range(self._population_size):
            arch = space.sample_random(f"Initial_{i}")
            score = await self.evaluator.evaluate(arch, test_suite)
            discovered = DiscoveredArchitecture(
                architecture=arch,
                score=score,
                generation=0,
                discovery_time_ms=(time.time() - start_time) * 1000
            )
            self._population.append(discovered)
            all_discovered.append(discovered)
            evaluations += 1
            self._total_architectures_discovered += 1

            # Check if target reached
            if budget.target_score and score.overall_score >= budget.target_score:
                target_reached = True
                break

        # Update best ever
        self._update_best()

        # Evolution loop
        while (
            evaluations < budget.max_evaluations and
            (time.time() - start_time) < budget.max_time_seconds and
            not target_reached and
            no_improvement_count < budget.early_stopping_patience
        ):
            self._generation += 1
            generation_start = time.time()

            # Select parents
            parents = self._select_parents()

            # Create offspring
            offspring = []

            for i in range(self._population_size - self._elite_size):
                # Crossover or mutation
                import random
                if len(parents) >= 2 and random.random() < self._crossover_rate:
                    p1 = random.choice(parents).architecture
                    p2 = random.choice(parents).architecture
                    child_arch = space.crossover(p1, p2)
                    parent_ids = [p1.id, p2.id]
                else:
                    parent = random.choice(parents).architecture
                    child_arch = space.mutate(parent, self._mutation_rate)
                    parent_ids = [parent.id]

                # Evaluate
                score = await self.evaluator.evaluate(child_arch, test_suite)
                discovered = DiscoveredArchitecture(
                    architecture=child_arch,
                    score=score,
                    generation=self._generation,
                    discovery_time_ms=(time.time() - start_time) * 1000,
                    parent_ids=parent_ids
                )
                offspring.append(discovered)
                all_discovered.append(discovered)
                evaluations += 1
                self._total_architectures_discovered += 1

                # Check target
                if budget.target_score and score.overall_score >= budget.target_score:
                    target_reached = True
                    break

            if target_reached:
                break

            # Select survivors (elitism + tournament)
            elite = sorted(
                self._population,
                key=lambda d: d.score.overall_score,
                reverse=True
            )[:self._elite_size]

            self._population = elite + offspring[:self._population_size - self._elite_size]

            # Check for improvement
            old_best = self._best_ever.score.overall_score if self._best_ever else 0
            self._update_best()
            new_best = self._best_ever.score.overall_score if self._best_ever else 0

            if new_best > old_best:
                no_improvement_count = 0
            else:
                no_improvement_count += 1

            gen_time = (time.time() - generation_start) * 1000
            logger.debug(
                f"Generation {self._generation}: "
                f"best={new_best:.3f}, evals={evaluations}, time={gen_time:.0f}ms"
            )

        # Check convergence
        if no_improvement_count >= budget.early_stopping_patience:
            converged = True

        total_time = time.time() - start_time

        logger.info(
            f"NAS complete: {evaluations} evaluations, "
            f"{self._generation} generations, "
            f"best={self._best_ever.score.overall_score:.3f}"
        )

        return SearchResult(
            best_architecture=self._best_ever,
            all_discovered=all_discovered,
            total_evaluations=evaluations,
            total_time_seconds=total_time,
            final_generation=self._generation,
            converged=converged,
            target_reached=target_reached,
            metadata={
                'goal': goal,
                'strategy': self._strategy.value,
                'population_size': self._population_size
            }
        )

    async def evaluate_architecture(
        self,
        architecture: ArchitectureSpec,
        test_suite: TestSuite = None
    ) -> ArchitectureScore:
        """
        Evaluate a discovered architecture on test suite.

        Args:
            architecture: Architecture to evaluate
            test_suite: Test suite to use

        Returns:
            ArchitectureScore with evaluation results
        """
        return await self.evaluator.evaluate(architecture, test_suite)

    def _select_parents(self) -> List[DiscoveredArchitecture]:
        """Select parents for next generation using tournament selection."""
        import random

        parents = []
        tournament_size = 3

        for _ in range(self._population_size):
            # Tournament selection
            tournament = random.sample(
                self._population,
                min(tournament_size, len(self._population))
            )
            winner = max(tournament, key=lambda d: d.score.overall_score)
            parents.append(winner)

        return parents

    def _update_best(self) -> None:
        """Update best ever architecture."""
        if not self._population:
            return

        current_best = max(
            self._population,
            key=lambda d: d.score.overall_score
        )

        if (
            self._best_ever is None or
            current_best.score.overall_score > self._best_ever.score.overall_score
        ):
            self._best_ever = current_best

    def get_best(self) -> Optional[DiscoveredArchitecture]:
        """Get best discovered architecture."""
        return self._best_ever

    def get_population(self) -> List[DiscoveredArchitecture]:
        """Get current population."""
        return self._population.copy()

    def get_stats(self) -> Dict:
        """Get NAS statistics."""
        return {
            'total_searches': self._total_searches,
            'total_architectures_discovered': self._total_architectures_discovered,
            'current_generation': self._generation,
            'current_population_size': len(self._population),
            'best_score': (
                self._best_ever.score.overall_score
                if self._best_ever else None
            ),
            'strategy': self._strategy.value,
            'space_stats': self.space.get_stats(),
            'evaluator_stats': self.evaluator.get_stats()
        }

    def reset(self) -> None:
        """Reset NAS state."""
        self._population.clear()
        self._generation = 0
        self._best_ever = None
        self.space.reset()
        self.evaluator.reset()
        logger.info("NeuralArchitectureSearch reset")
