"""
BYRD Omega
Loop 5 of Option B: Integration Mind / Meta-Orchestration

BYRD Omega is the integration layer that orchestrates all five loops:
1. Memory Reasoner - Graph-based reasoning
2. Self-Compiler - Pattern learning
3. Goal Evolver - Evolutionary optimization
4. Dreaming Machine - Experience multiplication
5. Integration Mind (this) - Meta-orchestration

THE KEY INSIGHT: Loops compound when coupled.
Omega measures coupling between loops and invests resources where
multiplication is happening.

Operating Modes:
- AWAKE: Normal operation, all loops running
- DREAMING: Deep reflection mode, dreaming machine prioritized
- EVOLVING: Goal evolution mode, evolver prioritized
- COMPILING: Self-modification mode, compiler prioritized

THE CRITICAL METRIC: Goal Evolver → Self-Compiler coupling.
When goals drive code changes that improve capability, we have true
acceleration.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

from memory import Memory
from event_bus import event_bus, Event, EventType
from coupling_tracker import CouplingTracker, get_coupling_tracker

logger = logging.getLogger(__name__)


class OperatingMode(Enum):
    """BYRD Omega operating modes."""
    AWAKE = "awake"
    DREAMING = "dreaming"
    EVOLVING = "evolving"
    COMPILING = "compiling"


@dataclass
class LoopStatus:
    """Status of a self-improvement loop."""
    name: str
    is_healthy: bool
    last_cycle: Optional[datetime]
    metrics: Dict[str, float]
    cycles_completed: int = 0


@dataclass
class OmegaState:
    """Current state of BYRD Omega."""
    mode: OperatingMode
    mode_start: datetime
    total_cycles: int
    capability_score: float
    growth_rate: float
    critical_coupling: float


class BYRDOmega:
    """
    Integration Mind: Orchestrates all Option B loops.

    Manages mode transitions, measures coupling, and allocates
    resources to maximize capability growth.
    """

    def __init__(
        self,
        memory: Memory,
        llm_client: Any,
        memory_reasoner: Any,
        self_compiler: Any,
        goal_evolver: Any,
        dreaming_machine: Any,
        config: Optional[Dict] = None
    ):
        """
        Initialize BYRD Omega.

        Args:
            memory: The BYRD memory system
            llm_client: LLM client
            memory_reasoner: Memory Reasoner instance
            self_compiler: Self-Compiler instance
            goal_evolver: Goal Evolver instance
            dreaming_machine: Dreaming Machine instance
            config: Configuration from config.yaml option_b.omega
        """
        self.memory = memory
        self.llm_client = llm_client

        # Component loops
        self.memory_reasoner = memory_reasoner
        self.self_compiler = self_compiler
        self.goal_evolver = goal_evolver
        self.dreaming_machine = dreaming_machine

        # Configuration
        self.config = config or {}
        mode_durations = self.config.get("mode_durations", {})
        self.mode_durations = {
            OperatingMode.AWAKE: mode_durations.get("AWAKE", 60),
            OperatingMode.DREAMING: mode_durations.get("DREAMING", 30),
            OperatingMode.EVOLVING: mode_durations.get("EVOLVING", 20),
            OperatingMode.COMPILING: mode_durations.get("COMPILING", 40),
        }

        coupling_config = self.config.get("coupling", {})
        self.target_critical_coupling = self.config.get("target_critical_coupling", 0.5)

        # State
        self._mode = OperatingMode.AWAKE
        self._mode_start = datetime.now()
        self._total_cycles = 0
        self._capability_score = 0.0
        self._growth_rate = 0.0

        # Coupling tracker
        self._coupling_tracker = get_coupling_tracker()

        # Meta-learning system (injected by BYRD if Option B enabled)
        self.meta_learning = None

        # AGI Runner and Rollback (injected by BYRD)
        self.agi_runner = None
        self.rollback = None

        # Learning components (injected later)
        self.hierarchical_memory = None
        self.code_learner = None
        self.intuition_network = None
        self.gnn_layer = None  # StructuralLearner

        # Metrics history
        self._capability_history: List[Tuple[datetime, float]] = []
        self._max_history = 1000

        # Track if goals have been seeded
        self._goals_seeded = False

    async def seed_initial_goals(self, goal_descriptions: List[str]) -> int:
        """
        Seed the Goal Evolver with initial goals from the kernel.

        This should be called once at startup to populate the goal population.
        Without goals, the Goal Evolver has nothing to evolve.

        Args:
            goal_descriptions: List of goal descriptions from kernel.initial_goals

        Returns:
            Number of goals created
        """
        if self._goals_seeded:
            return 0

        if not self.goal_evolver:
            return 0

        # Check if there are already goals in the population
        existing = await self.goal_evolver.get_current_population()
        if len(existing) >= 5:  # Already have a decent population
            self._goals_seeded = True
            return 0

        # Seed with initial goals
        if goal_descriptions:
            goal_ids = await self.goal_evolver.create_initial_population(goal_descriptions)
            self._goals_seeded = True

            await event_bus.emit(Event(
                type=EventType.GOAL_EVOLVED,
                data={
                    "event": "goals_seeded",
                    "count": len(goal_ids),
                    "source": "kernel_initial_goals"
                }
            ))

            return len(goal_ids)

        return 0

    @property
    def mode(self) -> OperatingMode:
        """Get current operating mode."""
        return self._mode

    async def transition_mode(self, new_mode: OperatingMode):
        """
        Transition to a new operating mode.

        Args:
            new_mode: The mode to transition to
        """
        old_mode = self._mode
        self._mode = new_mode
        self._mode_start = datetime.now()

        await event_bus.emit(Event(
            type=EventType.MODE_TRANSITION,
            data={
                "from_mode": old_mode.value,
                "to_mode": new_mode.value,
                "reason": "scheduled"
            }
        ))

        logger.info(f"Mode transition: {old_mode.value} -> {new_mode.value}")

    def should_transition(self) -> bool:
        """Check if it's time to transition modes."""
        elapsed = (datetime.now() - self._mode_start).total_seconds()
        duration = self.mode_durations.get(self._mode, 60)
        return elapsed >= duration

    def get_next_mode(self) -> OperatingMode:
        """
        Determine the next operating mode.

        Uses coupling measurements to decide where to focus.
        """
        # Get coupling measurements
        critical = self._coupling_tracker.get_critical_coupling()

        # If critical coupling is weak, prioritize building it
        if critical.correlation < self.target_critical_coupling:
            # Alternate between evolving (goals) and compiling (patterns)
            if self._mode == OperatingMode.EVOLVING:
                return OperatingMode.COMPILING
            elif self._mode == OperatingMode.COMPILING:
                return OperatingMode.DREAMING
            else:
                return OperatingMode.EVOLVING

        # Standard rotation
        mode_order = [
            OperatingMode.AWAKE,
            OperatingMode.DREAMING,
            OperatingMode.EVOLVING,
            OperatingMode.COMPILING,
        ]

        current_idx = mode_order.index(self._mode)
        next_idx = (current_idx + 1) % len(mode_order)
        return mode_order[next_idx]

    async def run_cycle(self) -> Dict[str, Any]:
        """
        Run a single Omega cycle.

        Coordinates all loops based on current mode.
        """
        self._total_cycles += 1

        await event_bus.emit(Event(
            type=EventType.LOOP_CYCLE_START,
            data={"loop_name": "omega", "mode": self._mode.value}
        ))

        results = {
            "mode": self._mode.value,
            "cycle": self._total_cycles,
            "loops": {}
        }

        try:
            # Run loops based on mode
            if self._mode == OperatingMode.AWAKE:
                results["loops"] = await self._run_awake_mode()
            elif self._mode == OperatingMode.DREAMING:
                results["loops"] = await self._run_dreaming_mode()
            elif self._mode == OperatingMode.EVOLVING:
                results["loops"] = await self._run_evolving_mode()
            elif self._mode == OperatingMode.COMPILING:
                results["loops"] = await self._run_compiling_mode()

            # Measure capability and growth
            await self._measure_capability()

            # Measure coupling
            await self._coupling_tracker.emit_coupling_event()

            # AGI SEED: Meta-learning plateau detection
            if self.meta_learning:
                try:
                    plateau = await self.meta_learning.detect_plateau()
                    if plateau.is_plateau:
                        results["plateau"] = {
                            "severity": plateau.severity.value,
                            "duration": plateau.duration_cycles,
                            "causes": plateau.likely_causes[:3] if plateau.likely_causes else []
                        }

                        # Respond to severe or critical plateaus
                        if plateau.severity.value in ["severe", "critical"]:
                            await self.meta_learning.respond_to_plateau(plateau)
                            logger.info(f"Meta-learning: Responding to {plateau.severity.value} plateau")
                except Exception as e:
                    logger.warning(f"Meta-learning plateau detection error: {e}")

            # TRAINING HOOKS: Run learning component updates
            training_results = await self._run_training_hooks()
            if training_results:
                results["training"] = training_results

            # Check for mode transition
            if self.should_transition():
                next_mode = self.get_next_mode()
                await self.transition_mode(next_mode)
                results["mode_transition"] = next_mode.value

        except Exception as e:
            logger.error(f"Omega cycle error: {e}")
            results["error"] = str(e)

        await event_bus.emit(Event(
            type=EventType.LOOP_CYCLE_END,
            data={
                "loop_name": "omega",
                "cycle": self._total_cycles,
                "results": results
            }
        ))

        return results

    async def _run_awake_mode(self) -> Dict[str, Any]:
        """Run all loops in normal mode."""
        results = {}

        # All loops run with equal priority
        if self.memory_reasoner:
            results["memory_reasoner"] = self.memory_reasoner.get_metrics()

        if self.self_compiler:
            results["self_compiler"] = self.self_compiler.get_metrics()

        if self.goal_evolver:
            results["goal_evolver"] = self.goal_evolver.get_metrics()

        if self.dreaming_machine:
            results["dreaming_machine"] = self.dreaming_machine.get_metrics()

        return results

    async def _run_dreaming_mode(self) -> Dict[str, Any]:
        """Run with dreaming machine prioritized."""
        results = {}

        # Dreaming machine is the focus
        if self.dreaming_machine:
            dm_results = await self.dreaming_machine.dream_cycle()
            results["dreaming_machine"] = dm_results

        # Other loops run at reduced priority
        if self.memory_reasoner:
            results["memory_reasoner"] = self.memory_reasoner.get_metrics()

        return results

    async def _run_evolving_mode(self) -> Dict[str, Any]:
        """Run with goal evolver prioritized."""
        results = {}

        # Goal evolver is the focus
        if self.goal_evolver:
            evolution = await self.goal_evolver.evolve_generation()
            results["goal_evolver"] = evolution

        # Memory reasoner supports evolution
        if self.memory_reasoner:
            results["memory_reasoner"] = self.memory_reasoner.get_metrics()

        return results

    async def _run_compiling_mode(self) -> Dict[str, Any]:
        """Run with self-compiler prioritized."""
        results = {}

        # Self-compiler is the focus
        if self.self_compiler:
            # Attempt pattern lifting
            lifted = await self.self_compiler.attempt_lifting()
            metrics = self.self_compiler.get_metrics()
            metrics["patterns_lifted_this_cycle"] = lifted
            results["self_compiler"] = metrics

        # Goal evolver feeds into compiler
        if self.goal_evolver:
            results["goal_evolver"] = self.goal_evolver.get_metrics()

        return results

    async def _measure_capability(self):
        """Measure current capability and compute growth rate."""
        # Aggregate capability from all loops
        metrics = []

        if self.memory_reasoner:
            mr_metrics = self.memory_reasoner.get_metrics()
            metrics.append(mr_metrics.get("memory_ratio", 0.0))

        if self.self_compiler:
            sc_metrics = self.self_compiler.get_metrics()
            metrics.append(sc_metrics.get("match_rate", 0.0))

        if self.goal_evolver:
            ge_metrics = self.goal_evolver.get_metrics()
            metrics.append(ge_metrics.get("completion_rate", 0.0))

        if self.dreaming_machine:
            dm_metrics = self.dreaming_machine.get_metrics()
            metrics.append(min(1.0, dm_metrics.get("multiplication_factor", 0.0)))

        # Average capability score
        if metrics:
            self._capability_score = sum(metrics) / len(metrics)
        else:
            self._capability_score = 0.0

        # Record in history
        now = datetime.now()
        self._capability_history.append((now, self._capability_score))

        # Trim history
        if len(self._capability_history) > self._max_history:
            self._capability_history = self._capability_history[-self._max_history:]

        # Compute growth rate (capability change per hour)
        if len(self._capability_history) >= 2:
            oldest = self._capability_history[0]
            newest = self._capability_history[-1]
            time_diff = (newest[0] - oldest[0]).total_seconds() / 3600  # Hours
            if time_diff > 0:
                self._growth_rate = (newest[1] - oldest[1]) / time_diff
            else:
                self._growth_rate = 0.0
        else:
            self._growth_rate = 0.0

        # Record in memory
        await self.memory.record_capability_score(
            capability_name="omega_aggregate",
            score=self._capability_score,
            measurement_source="omega"
        )

        # Emit event
        await event_bus.emit(Event(
            type=EventType.CAPABILITY_MEASURED,
            data={
                "capability_name": "omega_aggregate",
                "score": self._capability_score,
                "growth_rate": self._growth_rate
            }
        ))

    async def _run_training_hooks(self) -> Dict[str, Any]:
        """
        Run training updates for all learning components.

        Training hooks are called every Omega cycle to:
        1. Train GNN on graph structure (if gnn_layer available)
        2. Run hierarchical memory consolidation (every 10 cycles)
        3. Check for patterns to codify (every 20 cycles)
        4. Update intuition network from outcomes (every cycle)

        Returns:
            Dict with training results from each component
        """
        results = {}

        # 1. GNN Training (StructuralLearner) - every cycle
        if self.gnn_layer:
            try:
                # Extract graph structure
                nodes = await self.memory._run_query("""
                    MATCH (n)
                    WHERE n:Experience OR n:Belief OR n:Desire OR n:Pattern
                    RETURN elementId(n) as id, labels(n)[0] as type
                    LIMIT 500
                """)

                edges = await self.memory._run_query("""
                    MATCH (a)-[r]->(b)
                    RETURN elementId(a) as source, elementId(b) as target,
                           type(r) as rel_type
                    LIMIT 2000
                """)

                if nodes and edges:
                    # Run training epoch
                    training_result = await asyncio.to_thread(
                        self.gnn_layer.train_epoch,
                        list(nodes),
                        list(edges)
                    )
                    results["gnn"] = {
                        "loss": training_result.loss if hasattr(training_result, 'loss') else 0.0,
                        "accuracy": training_result.accuracy if hasattr(training_result, 'accuracy') else 0.0
                    }
            except Exception as e:
                logger.warning(f"GNN training error: {e}")

        # 2. Hierarchical Memory Consolidation - every 10 cycles
        if self.hierarchical_memory and self._total_cycles % 10 == 0:
            try:
                await self.hierarchical_memory.consolidation_cycle()
                results["hierarchical_memory"] = {
                    "consolidation_run": True
                }
            except Exception as e:
                logger.warning(f"Hierarchical memory consolidation error: {e}")

        # 3. Code Learner codification check - every 20 cycles
        if self.code_learner and self._total_cycles % 20 == 0:
            try:
                codification_results = await self.code_learner.codification_cycle()
                results["code_learner"] = {
                    "patterns_checked": len(codification_results),
                    "patterns_codified": sum(1 for r in codification_results if r.success)
                }
            except Exception as e:
                logger.warning(f"Code learner error: {e}")

        # 4. Intuition Network update - every cycle
        if self.intuition_network:
            try:
                # Get recent outcomes and update intuition
                recent_outcomes = await self.memory._run_query("""
                    MATCH (e:Experience {type: 'action_outcome'})
                    WHERE e.timestamp > datetime() - duration('PT1H')
                    RETURN e.action as action, e.success as success, e.context as context
                    ORDER BY e.timestamp DESC
                    LIMIT 20
                """)

                if recent_outcomes:
                    for outcome in recent_outcomes:
                        await self.intuition_network.record_outcome(
                            situation=str(outcome.get("context", "")),
                            action=outcome.get("action", ""),
                            success=outcome.get("success", False)
                        )
                    results["intuition"] = {
                        "outcomes_processed": len(recent_outcomes)
                    }
            except Exception as e:
                logger.warning(f"Intuition network error: {e}")

        return results

        if self._growth_rate != 0:
            await event_bus.emit(Event(
                type=EventType.GROWTH_RATE_COMPUTED,
                data={
                    "growth_rate": self._growth_rate,
                    "window_samples": len(self._capability_history)
                }
            ))

        # Phase 5: Capability regression detection and auto-rollback
        if self._growth_rate < -0.1:  # Significant regression threshold
            logger.warning(f"Capability regression detected: growth_rate={self._growth_rate:.4f}")

            if hasattr(self, 'rollback') and self.rollback:
                result = await self.rollback.auto_rollback_on_problem(
                    problem_type="capability_regression",
                    severity="high"
                )
                if result and result.success:
                    logger.info(f"Auto-rollback successful: {result.modifications_rolled_back} modifications reverted")
                    await event_bus.emit(Event(
                        type=EventType.ROLLBACK_TRIGGERED,
                        data={
                            "reason": "capability_regression",
                            "growth_rate": self._growth_rate,
                            "modifications_rolled_back": result.modifications_rolled_back
                        }
                    ))

    def get_state(self) -> OmegaState:
        """Get current Omega state."""
        critical = self._coupling_tracker.get_critical_coupling()
        return OmegaState(
            mode=self._mode,
            mode_start=self._mode_start,
            total_cycles=self._total_cycles,
            capability_score=self._capability_score,
            growth_rate=self._growth_rate,
            critical_coupling=critical.correlation
        )

    def get_metrics(self) -> Dict[str, Any]:
        """Get comprehensive Omega metrics."""
        critical = self._coupling_tracker.get_critical_coupling()

        # Get meta-learning stats if available
        meta_learning_data = {}
        if self.meta_learning:
            try:
                meta_learning_data = self.meta_learning.get_statistics()
            except Exception:
                pass

        return {
            "mode": self._mode.value,
            "total_cycles": self._total_cycles,
            "capability_score": self._capability_score,
            "growth_rate": self._growth_rate,
            "critical_coupling": critical.correlation,
            "critical_coupling_significant": critical.is_significant,
            "target_coupling": self.target_critical_coupling,
            "loops": {
                "memory_reasoner": self.memory_reasoner.get_metrics() if self.memory_reasoner else {},
                "self_compiler": self.self_compiler.get_metrics() if self.self_compiler else {},
                "goal_evolver": self.goal_evolver.get_metrics() if self.goal_evolver else {},
                "dreaming_machine": self.dreaming_machine.get_metrics() if self.dreaming_machine else {},
            },
            "coupling": self._coupling_tracker.get_summary(),
            "meta_learning": meta_learning_data
        }

    def get_loop_health(self) -> Dict[str, bool]:
        """Check health of all loops."""
        return {
            "memory_reasoner": self.memory_reasoner.is_healthy() if self.memory_reasoner else False,
            "self_compiler": self.self_compiler.is_healthy() if self.self_compiler else False,
            "goal_evolver": self.goal_evolver.is_healthy() if self.goal_evolver else False,
            "dreaming_machine": self.dreaming_machine.is_healthy() if self.dreaming_machine else False,
            "omega": self.is_healthy()
        }

    def is_healthy(self) -> bool:
        """Check if Omega is healthy overall."""
        if self._total_cycles < 10:
            return True  # Too early to judge

        # Need at least 3 of 4 loops healthy
        loop_health = self.get_loop_health()
        healthy_count = sum(1 for k, v in loop_health.items() if v and k != "omega")
        return healthy_count >= 3


# Factory function
def create_omega(
    memory: Memory,
    llm_client: Any,
    config: Dict
) -> BYRDOmega:
    """
    Create BYRD Omega with all loops.

    Args:
        memory: The BYRD memory system
        llm_client: LLM client
        config: Full config.yaml dict

    Returns:
        Configured BYRDOmega instance
    """
    from memory_reasoner import create_memory_reasoner
    from accelerators import SelfCompiler
    from goal_evolver import create_goal_evolver
    from dreaming_machine import create_dreaming_machine

    # Create all loops
    memory_reasoner = create_memory_reasoner(memory, llm_client, config)

    sc_config = config.get("option_b", {}).get("self_compiler", {})
    self_compiler = SelfCompiler(memory, llm_client, sc_config)

    goal_evolver = create_goal_evolver(memory, llm_client, config)
    dreaming_machine = create_dreaming_machine(memory, llm_client, config)

    # Create Omega
    omega_config = config.get("option_b", {}).get("omega", {})
    return BYRDOmega(
        memory=memory,
        llm_client=llm_client,
        memory_reasoner=memory_reasoner,
        self_compiler=self_compiler,
        goal_evolver=goal_evolver,
        dreaming_machine=dreaming_machine,
        config=omega_config
    )
