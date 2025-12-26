"""
BYRD Goal Evolver
Loop 3 of Option B: Evolutionary Goal Optimization

The Goal Evolver uses evolutionary algorithms to optimize which goals
BYRD pursues. Instead of random goal selection, goals compete and evolve:

1. Goals have FITNESS based on:
   - Completion rate (did the goal get achieved?)
   - Capability delta (how much did capability improve?)
   - Efficiency (resources spent vs gained)

2. Goals EVOLVE through:
   - Selection: High-fitness goals survive
   - Crossover: Combine successful goal aspects
   - Mutation: Random variations for exploration

THE KEY INSIGHT: Evolution finds goals that maximize capability growth.
Each generation produces better goals than the last.

This loop compounds because:
- Better goals → more capability → more possible goals
- Fitness function rewards capability growth directly
"""

import asyncio
import logging
import random
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

from memory import Memory
from event_bus import event_bus, Event, EventType

logger = logging.getLogger(__name__)


class GoalStatus(Enum):
    """Status of a goal in the population."""
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    ARCHIVED = "archived"


@dataclass
class EvolvedGoal:
    """A goal in the evolutionary population."""
    id: str
    description: str
    fitness: float
    generation: int
    parent_ids: List[str]
    success_criteria: Dict[str, Any]
    status: GoalStatus
    created_at: datetime
    capability_delta: float = 0.0
    attempts: int = 0
    completed_at: Optional[datetime] = None


@dataclass
class FitnessWeights:
    """Weights for the fitness function components."""
    completion: float = 0.4
    capability_delta: float = 0.4
    efficiency: float = 0.2


class GoalEvolver:
    """
    Loop 3 of Option B: Evolutionary Goal Optimization.

    Evolves a population of goals using genetic algorithms to find
    goals that maximize capability growth.
    """

    def __init__(
        self,
        memory: Memory,
        llm_client: Any,
        config: Optional[Dict] = None
    ):
        """
        Initialize the Goal Evolver.

        Args:
            memory: The BYRD memory system
            llm_client: LLM client for goal generation/mutation
            config: Configuration from config.yaml option_b.goal_evolver
        """
        self.memory = memory
        self.llm_client = llm_client
        self.config = config or {}

        # Population settings
        self.population_size = self.config.get("population_size", 20)
        self.elite_count = self.config.get("elite_count", 3)
        self.mutation_rate = self.config.get("mutation_rate", 0.2)
        self.crossover_rate = self.config.get("crossover_rate", 0.6)

        # Fitness weights
        weights_config = self.config.get("fitness_weights", {})
        self.fitness_weights = FitnessWeights(
            completion=weights_config.get("completion", 0.4),
            capability_delta=weights_config.get("capability_delta", 0.4),
            efficiency=weights_config.get("efficiency", 0.2)
        )

        # Tournament selection
        self.tournament_size = self.config.get("tournament_size", 3)

        # Archive threshold
        self.archive_threshold = self.config.get("archive_fitness_threshold", 0.2)

        # Tracking
        self._current_generation = 0
        self._total_goals_created = 0
        self._total_goals_completed = 0
        self._total_capability_delta = 0.0

    async def get_current_population(self) -> List[EvolvedGoal]:
        """Get the current goal population from memory."""
        goals = await self.memory.get_active_goals(limit=self.population_size * 2)

        return [
            EvolvedGoal(
                id=g["id"],
                description=g.get("description", ""),
                fitness=g.get("fitness", 0.5),
                generation=g.get("generation", 0),
                parent_ids=g.get("parent_goals", []),
                success_criteria=self._parse_criteria(g.get("success_criteria", "{}")),
                status=GoalStatus(g.get("status", "active")),
                created_at=self._parse_datetime(g.get("created_at")),
                capability_delta=g.get("capability_delta", 0.0),
                attempts=g.get("attempts", 0)
            )
            for g in goals
        ]

    def _parse_criteria(self, criteria: Any) -> Dict:
        """Parse success criteria from storage format."""
        if isinstance(criteria, dict):
            return criteria
        if isinstance(criteria, str):
            import json
            try:
                return json.loads(criteria)
            except:
                return {}
        return {}

    def _parse_datetime(self, dt: Any) -> datetime:
        """Parse datetime from storage format."""
        if isinstance(dt, datetime):
            return dt
        if isinstance(dt, str):
            try:
                return datetime.fromisoformat(dt.replace("Z", "+00:00"))
            except:
                return datetime.now()
        return datetime.now()

    async def create_initial_population(
        self,
        seed_descriptions: List[str]
    ) -> List[str]:
        """
        Create the initial population of goals.

        Args:
            seed_descriptions: Initial goal descriptions

        Returns:
            List of created goal IDs
        """
        goal_ids = []

        for desc in seed_descriptions[:self.population_size]:
            goal_id = await self.memory.create_goal(
                description=desc,
                fitness=0.5,  # Initial neutral fitness
                generation=0,
                parent_goals=[],
                success_criteria={"type": "subjective"}
            )
            goal_ids.append(goal_id)
            self._total_goals_created += 1

        await event_bus.emit(Event(
            type=EventType.GOAL_EVOLVED,
            data={
                "generation": 0,
                "population_size": len(goal_ids),
                "event": "initial_population"
            }
        ))

        return goal_ids

    async def evaluate_goal(
        self,
        goal_id: str,
        completed: bool,
        capability_delta: float,
        resources_spent: float = 1.0
    ):
        """
        Evaluate a goal's fitness based on its outcome.

        Args:
            goal_id: The goal to evaluate
            completed: Whether the goal was completed
            capability_delta: Change in capability from pursuing this goal
            resources_spent: Resources spent (for efficiency calculation)
        """
        # Calculate fitness components
        completion_score = 1.0 if completed else 0.0
        delta_score = min(1.0, max(0.0, capability_delta))  # Normalize to [0, 1]
        efficiency_score = delta_score / max(0.1, resources_spent)  # Avoid div by zero
        efficiency_score = min(1.0, efficiency_score)

        # Weighted fitness
        fitness = (
            self.fitness_weights.completion * completion_score +
            self.fitness_weights.capability_delta * delta_score +
            self.fitness_weights.efficiency * efficiency_score
        )

        # Update in memory
        await self.memory.update_goal_fitness(
            goal_id=goal_id,
            fitness=fitness,
            capability_delta=capability_delta
        )

        if completed:
            await self.memory.complete_goal(goal_id)
            self._total_goals_completed += 1

        self._total_capability_delta += capability_delta

        # Archive if fitness too low
        if fitness < self.archive_threshold and not completed:
            await self.memory.archive_goal(goal_id)

    def _tournament_select(
        self,
        population: List[EvolvedGoal]
    ) -> EvolvedGoal:
        """
        Select a goal using tournament selection.

        Randomly sample tournament_size goals, return the fittest.
        """
        if len(population) <= self.tournament_size:
            tournament = population
        else:
            tournament = random.sample(population, self.tournament_size)

        return max(tournament, key=lambda g: g.fitness)

    async def _crossover(
        self,
        parent1: EvolvedGoal,
        parent2: EvolvedGoal
    ) -> str:
        """
        Create a new goal by combining two parent goals.

        Uses LLM to intelligently combine goal aspects.
        """
        prompt = f"""Create a new goal by combining the best aspects of these two goals:

Goal 1 (fitness={parent1.fitness:.2f}): {parent1.description}

Goal 2 (fitness={parent2.fitness:.2f}): {parent2.description}

Create a combined goal that captures the essence of both.
The new goal should be specific, achievable, and focused on capability improvement.

New goal description (1-2 sentences):"""

        try:
            new_description = await self.llm_client.query(prompt, max_tokens=200)
            new_description = new_description.strip()

            goal_id = await self.memory.create_goal(
                description=new_description,
                fitness=0.5,  # Start neutral
                generation=self._current_generation + 1,
                parent_goals=[parent1.id, parent2.id],
                success_criteria={"type": "inherited"}
            )

            self._total_goals_created += 1
            return goal_id

        except Exception as e:
            logger.error(f"Crossover failed: {e}")
            return ""

    async def _mutate(
        self,
        goal: EvolvedGoal
    ) -> str:
        """
        Create a mutated version of a goal.

        Uses LLM to create a variation.
        """
        prompt = f"""Create a variation of this goal:

Original: {goal.description}

Create a slightly different version that:
- Maintains the core intent
- Adds a new angle or approach
- Could lead to capability improvement

Mutated goal (1-2 sentences):"""

        try:
            mutated = await self.llm_client.query(prompt, max_tokens=200)
            mutated = mutated.strip()

            goal_id = await self.memory.create_goal(
                description=mutated,
                fitness=0.5,
                generation=self._current_generation + 1,
                parent_goals=[goal.id],
                success_criteria={"type": "mutated"}
            )

            self._total_goals_created += 1
            return goal_id

        except Exception as e:
            logger.error(f"Mutation failed: {e}")
            return ""

    async def evolve_generation(self) -> Dict[str, Any]:
        """
        Evolve the population to the next generation.

        Returns:
            Statistics about the evolution
        """
        population = await self.get_current_population()

        if len(population) < 2:
            return {"error": "Population too small", "size": len(population)}

        # Sort by fitness
        population.sort(key=lambda g: g.fitness, reverse=True)

        # Keep elites
        elites = population[:self.elite_count]
        new_goal_ids = [e.id for e in elites]

        # Generate new goals through crossover and mutation
        while len(new_goal_ids) < self.population_size:
            if random.random() < self.crossover_rate and len(population) >= 2:
                # Crossover
                parent1 = self._tournament_select(population)
                parent2 = self._tournament_select(population)
                if parent1.id != parent2.id:
                    new_id = await self._crossover(parent1, parent2)
                    if new_id:
                        new_goal_ids.append(new_id)

            if len(new_goal_ids) < self.population_size and random.random() < self.mutation_rate:
                # Mutation
                parent = self._tournament_select(population)
                new_id = await self._mutate(parent)
                if new_id:
                    new_goal_ids.append(new_id)

            # Safety: add random new goal if stuck
            if len(new_goal_ids) < self.population_size:
                await asyncio.sleep(0.1)  # Prevent tight loop

        # Archive low-fitness non-elite goals from previous generation
        for goal in population[self.elite_count:]:
            if goal.fitness < self.archive_threshold:
                await self.memory.archive_goal(goal.id)

        self._current_generation += 1

        # Emit evolution event
        await event_bus.emit(Event(
            type=EventType.GOAL_EVOLVED,
            data={
                "generation": self._current_generation,
                "population_size": len(new_goal_ids),
                "elite_count": self.elite_count,
                "avg_fitness": sum(g.fitness for g in population) / len(population)
            }
        ))

        return {
            "generation": self._current_generation,
            "new_goals": len(new_goal_ids) - self.elite_count,
            "elites_preserved": self.elite_count,
            "avg_fitness": sum(g.fitness for g in population) / len(population),
            "max_fitness": max(g.fitness for g in population),
            "archived": len([g for g in population if g.fitness < self.archive_threshold])
        }

    async def get_best_goals(self, n: int = 5) -> List[EvolvedGoal]:
        """Get the top N goals by fitness."""
        population = await self.get_current_population()
        population.sort(key=lambda g: g.fitness, reverse=True)
        return population[:n]

    async def suggest_next_goal(self) -> Optional[EvolvedGoal]:
        """
        Suggest the next goal to pursue.

        Uses a combination of fitness and exploration:
        - Usually picks high-fitness goals
        - Sometimes picks random goals for exploration
        """
        population = await self.get_current_population()

        if not population:
            return None

        # 80% exploit (high fitness), 20% explore (random)
        if random.random() < 0.8:
            # Exploit: tournament selection
            return self._tournament_select(population)
        else:
            # Explore: random selection
            return random.choice(population)

    def get_metrics(self) -> Dict[str, Any]:
        """Get Goal Evolver metrics."""
        return {
            "current_generation": self._current_generation,
            "total_goals_created": self._total_goals_created,
            "total_goals_completed": self._total_goals_completed,
            "total_capability_delta": self._total_capability_delta,
            "completion_rate": (
                self._total_goals_completed / self._total_goals_created
                if self._total_goals_created > 0 else 0.0
            ),
            "avg_capability_per_goal": (
                self._total_capability_delta / self._total_goals_completed
                if self._total_goals_completed > 0 else 0.0
            )
        }

    def is_healthy(self) -> bool:
        """Check if the Goal Evolver is healthy."""
        if self._current_generation < 3:
            return True  # Too early to judge

        # Should complete at least 10% of goals
        if self._total_goals_created > 10:
            completion_rate = self._total_goals_completed / self._total_goals_created
            return completion_rate >= 0.1

        return True


# Factory function
def create_goal_evolver(
    memory: Memory,
    llm_client: Any,
    config: Dict
) -> GoalEvolver:
    """
    Create a Goal Evolver from configuration.

    Args:
        memory: The BYRD memory system
        llm_client: LLM client
        config: Full config.yaml dict

    Returns:
        Configured GoalEvolver instance
    """
    ge_config = config.get("option_b", {}).get("goal_evolver", {})
    return GoalEvolver(memory, llm_client, ge_config)
