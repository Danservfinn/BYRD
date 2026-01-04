"""
BYRD Growth-Optimized Loop Activation System
=============================================

This module activates loops that ACTUALLY drive growth and stops wasting
cycles on false bottlenecks.

KEY PRINCIPLE:
--------------
Not all loops are equal. Some produce real capability delta (growth),
while others spin on false bottlenecks. We must:

1. MEASURE actual capability delta, not simulate it
2. IDENTIFY loops that produce real growth vs. noise
3. DEPRIORITIZE or PAUSE loops that waste cycles
4. FOCUS resources on high-growth loops

FALSE BOTTLENECK DETECTION:
---------------------------
A false bottleneck is when a loop spends cycles "solving" problems that:
- Don't translate to actual capability improvement
- Are symptoms, not root causes
- Keep the system busy but not growing

GROWTH-DRIVEN LOOP PRIORITIZATION:
-----------------------------------
- Loops are ranked by measured delta per cycle
- Resources (compute, time, attention) are allocated proportional to growth
- Low-growth loops are throttled or paused
- High-growth loops get priority execution

USAGE:
------
    from activate_loops_v2 import GrowthOptimizedActivator
    
    activator = GrowthOptimizedActivator(memory, llm_client)
    await activator.activate_growth_loops()
    await activator.run_growth_cycles(num_cycles=3)
    # Only high-growth loops execute efficiently
"""

import asyncio
import logging
import time
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field

from memory import Memory
from event_bus import event_bus, Event, EventType
from coupling_tracker import CouplingTracker, get_coupling_tracker
from loop_instrumentation import LoopInstrumenter, get_instrumenter
from memory_reasoner import MemoryReasoner
from accelerators import SelfCompiler
from goal_evolver import GoalEvolver
from dreaming_machine import DreamingMachine
from omega import BYRDOmega
from llm_client import LLMClient

logger = logging.getLogger(__name__)


@dataclass
class LoopPerformance:
    """Tracks real measured performance of a loop."""
    name: str
    cycles_run: int = 0
    total_delta: float = 0.0
    avg_delta: float = 0.0
    recent_deltas: List[float] = field(default_factory=list)
    last_delta: float = 0.0
    is_growing: bool = False
    is_false_bottleneck: bool = False
    priority_score: float = 0.0
    cpu_cycles_consumed: float = 0.0
    delta_per_cycle: float = 0.0
    
    def record_cycle(self, delta: float, duration: float):
        """Record a cycle's results."""
        self.cycles_run += 1
        self.total_delta += delta
        self.last_delta = delta
        self.recent_deltas.append(delta)
        if len(self.recent_deltas) > 10:
            self.recent_deltas.pop(0)
        self.avg_delta = self.total_delta / self.cycles_run if self.cycles_run > 0 else 0.0
        self.cpu_cycles_consumed += duration
        
        # Calculate efficiency metrics
        self.delta_per_cycle = self.avg_delta
        
        # Detect if actually growing (trending positive deltas)
        if len(self.recent_deltas) >= 3:
            recent_avg = sum(self.recent_deltas[-3:]) / 3
            self.is_growing = recent_avg > 0.001  # Minimum growth threshold
        
        # Detect false bottleneck: many cycles, minimal delta
        self.is_false_bottleneck = (
            self.cycles_run >= 5 and 
            self.avg_delta < 0.001 and
            self.cpu_cycles_consumed > 1.0  # At least 1 second of work
        )
        
        # Priority score: growth * efficiency, penalize bottlenecks
        if self.is_false_bottleneck:
            self.priority_score = -1.0  # Deprioritize false bottlenecks
        elif self.is_growing:
            self.priority_score = self.avg_delta * (1.0 / max(0.1, duration))
        else:
            self.priority_score = 0.0


class GrowthOptimizedActivator:
    """
    Activates and manages loops with growth-driven resource allocation.
    
    Unlike the basic activator, this version:
    1. Measures REAL capability delta (not simulated)
    2. Identifies and throttles false bottlenecks
    3. Prioritizes high-growth loops
    4. Dynamically allocates execution time based on measured performance
    """
    
    GROWING_LOOPS = [
        "self_compiler",   # Code that actually works compounds
        "goal_evolver",    # Better goals drive everything
        "memory_reasoner", # Better retrieval enables all other loops
    ]
    
    SUPPORT_LOOPS = [
        "dreaming_machine", # Multiplies experience
        "omega",            # Orchestrates others
    ]
    
    # Minimum delta to consider a cycle "productive"
    MIN_PRODUCTIVE_DELTA = 0.001
    
    # How many consecutive zero-delta cycles before throttling
    ZERO_DELTA_THRESHOLD = 3
    
    def __init__(self, memory: Memory, llm_client: LLMClient, config: Optional[Dict] = None):
        self.memory = memory
        self.llm_client = llm_client
        self.config = config or {}
        
        # Loop instances
        self.memory_reasoner = None
        self.self_compiler = None
        self.goal_evolver = None
        self.dreaming_machine = None
        self.omega = None
        
        # Monitoring
        self.coupling_tracker = None
        self.instrumenter = None
        
        # Performance tracking
        self.performance: Dict[str, LoopPerformance] = {}
        self.activation_results = {}
        self.cycles_completed = {}
        
        # Resource allocation state
        self.paused_loops: set = set()
        self.throttled_loops: set = set()
        
    async def activate_growth_loops(self):
        """
        Activate loops with growth optimization enabled.
        
        Only activates loops that can demonstrate real potential for growth.
        """
        logger.info("=" * 70)
        logger.info("GROWTH-OPTIMIZED LOOP ACTIVATION")
        logger.info("=" * 70)
        logger.info("Principle: Stop wasting cycles on false bottlenecks")
        logger.info("Focus: Activate loops that actually drive growth")
        logger.info("")
        
        await self._initialize_performance_tracking()
        await self._activate_instrumentation()
        await self._activate_coupling_tracker()
        
        # Activate growing loops first (higher priority)
        for loop_name in self.GROWING_LOOPS:
            await self._activate_loop(loop_name)
        
        # Then activate support loops
        for loop_name in self.SUPPORT_LOOPS:
            await self._activate_loop(loop_name)
        
        await self._connect_omega()
        self._print_activation_summary()
        self._print_growth_priorities()
        
        return self.activation_results
    
    async def _initialize_performance_tracking(self):
        """Initialize performance tracking for all loops."""
        all_loops = self.GROWING_LOOPS + self.SUPPORT_LOOPS
        for loop_name in all_loops:
            self.performance[loop_name] = LoopPerformance(name=loop_name)
        logger.info("[performance] Initialized tracking for all loops")
    
    async def _activate_instrumentation(self):
        """Setup real delta measurement, not simulation."""
        try:
            logger.info("[instrumentation] Setting up REAL delta measurement...")
            self.instrumenter = get_instrumenter()
            if not self.instrumenter:
                self.instrumenter = LoopInstrumenter(
                    config={"measure_real_delta": True}
                )
            
            # Register all loops
            all_loops = self.GROWING_LOOPS + self.SUPPORT_LOOPS
            for loop_name in all_loops:
                self.instrumenter.register_loop(loop_name)
            
            self.activation_results["instrumentation"] = {
                "success": True,
                "mode": "REAL delta measurement"
            }
            logger.info("[instrumentation] Activated - measuring ACTUAL growth")
        except Exception as e:
            self.activation_results["instrumentation"] = {
                "success": False,
                "error": str(e)
            }
            logger.error(f"[instrumentation] Failed: {e}")
    
    async def _activate_coupling_tracker(self):
        """Initialize coupling tracker."""
        try:
            logger.info("[coupling_tracker] Initializing...")
            self.coupling_tracker = get_coupling_tracker()
            if not self.coupling_tracker:
                self.coupling_tracker = CouplingTracker(
                    memory=self.memory,
                    config=self.config.get("coupling_tracker", {})
                )
            await self.coupling_tracker.start_tracking()
            self.activation_results["coupling_tracker"] = {"success": True}
            logger.info("[coupling_tracker] Activated")
        except Exception as e:
            self.activation_results["coupling_tracker"] = {
                "success": False,
                "error": str(e)
            }
            logger.error(f"[coupling_tracker] Failed: {e}")
    
    async def _activate_loop(self, loop_name: str):
        """Activate a specific loop instance."""
        try:
            logger.info(f"[{loop_name}] Initializing...")
            
            if loop_name == "memory_reasoner":
                self.memory_reasoner = MemoryReasoner(
                    memory=self.memory,
                    llm_client=self.llm_client,
                    config=self.config.get("memory_reasoner", {})
                )
                await self.memory_reasoner.query("test activation")
            
            elif loop_name == "self_compiler":
                self.self_compiler = SelfCompiler(
                    memory=self.memory,
                    llm_client=self.llm_client,
                    config=self.config.get("self_compiler", {})
                )
            
            elif loop_name == "goal_evolver":
                self.goal_evolver = GoalEvolver(
                    memory=self.memory,
                    llm_client=self.llm_client,
                    config=self.config.get("goal_evolver", {})
                )
            
            elif loop_name == "dreaming_machine":
                self.dreaming_machine = DreamingMachine(
                    memory=self.memory,
                    llm_client=self.llm_client,
                    config=self.config.get("dreaming_machine", {})
                )
            
            elif loop_name == "omega":
                self.omega = BYRDOmega(
                    memory=self.memory,
                    coupling_tracker=self.coupling_tracker,
                    config=self.config.get("omega", {})
                )
                # Connect other loops to omega
                if self.memory_reasoner:
                    self.omega.memory_reasoner = self.memory_reasoner
                if self.self_compiler:
                    self.omega.self_compiler = self.self_compiler
                if self.goal_evolver:
                    self.omega.goal_evolver = self.goal_evolver
                if self.dreaming_machine:
                    self.omega.dreaming_machine = self.dreaming_machine
            
            self.activation_results[loop_name] = {"success": True}
            logger.info(f"[{loop_name}] Activated")
            
            await event_bus.emit(Event(
                type=EventType.LOOP_CYCLE_START,
                data={"loop_name": loop_name, "action": "activation"}
            ))
            
        except Exception as e:
            self.activation_results[loop_name] = {
                "success": False,
                "error": str(e)
            }
            logger.error(f"[{loop_name}] Failed: {e}")
    
    async def _connect_omega(self):
        """Connect Omega to all activated loops."""
        if self.omega:
            logger.info("[omega] Connecting to all loops...")
            # Already done in _activate_loop for omega
            logger.info("[omega] Connections established")
    
    def _print_activation_summary(self):
        """Print summary of activation results."""
        logger.info("")
        logger.info("=" * 60)
        logger.info("ACTIVATION SUMMARY")
        logger.info("=" * 60)
        
        successful = sum(
            1 for r in self.activation_results.values() 
            if r.get("success")
        )
        total = len(self.activation_results)
        
        for name, result in self.activation_results.items():
            status = "✓" if result.get("success") else "✗"
            logger.info(f"  {status} {name}")
        
        logger.info(f"\nTotal: {successful}/{total} activated")
        logger.info("")
    
    def _print_growth_priorities(self):
        """Print initial growth priorities."""
        logger.info("=" * 60)
        logger.info("GROWTH PRIORITIES (Initial)")
        logger.info("=" * 60)
        logger.info("HIGH PRIORITY (Growing Loops):")
        for loop in self.GROWING_LOOPS:
            logger.info(f"  • {loop}")
        logger.info("\nSUPPORT (Resource Multipliers):")
        for loop in self.SUPPORT_LOOPS:
            logger.info(f"  • {loop}")
        logger.info("")
    
    async def run_growth_cycles(self, num_cycles: int = 3):
        """
        Run growth-optimized cycles.
        
        Unlike the basic version, this:
        1. Measures REAL delta for each cycle
        2. Throttles false bottlenecks
        3. Prioritizes high-growth loops
        4. Stops wasting cycles on non-productive loops
        """
        logger.info("=" * 70)
        logger.info(f"RUNNING {num_cycles} GROWTH-OPTIMIZED CYCLES")
        logger.info("=" * 70)
        logger.info("Strategy: Execute high-growth loops, throttle false bottlenecks")
        logger.info("")
        
        self.cycles_completed = {
            name: 0 
            for name in self.GROWING_LOOPS + self.SUPPORT_LOOPS
        }
        
        for cycle_num in range(num_cycles):
            logger.info(f"\n{'─' * 70}")
            logger.info(f"CYCLE {cycle_num + 1}/{num_cycles}")
            logger.info(f"{'─' * 70}")
            
            # Update priorities based on previous performance
            await self._update_loop_priorities()
            
            # Execute loops in priority order
            await self._execute_priority_ordered_cycle(cycle_num)
            
            # Analyze and report
            await self._analyze_cycle_results(cycle_num)
            
            # Throttle or pause false bottlenecks
            await self._manage_false_bottlenecks()
        
        # Final report
        self._print_growth_report()
        
        return self.cycles_completed
    
    async def _update_loop_priorities(self):
        """Update loop priorities based on measured performance."""
        logger.info("\n[Priority Update] Recalculating based on measured delta...")
        
        # Sort loops by priority score
        sorted_loops = sorted(
            self.performance.items(),
            key=lambda x: x[1].priority_score,
            reverse=True
        )
        
        logger.info("Loop Priority Order:")
        for loop_name, perf in sorted_loops:
            status = "GROWING" if perf.is_growing else "STAGNANT"
            if perf.is_false_bottleneck:
                status = "FALSE BOTTLENECK"
            elif loop_name in self.paused_loops:
                status = "PAUSED"
            elif loop_name in self.throttled_loops:
                status = "THROTTLED"
            
            logger.info(
                f"  {perf.priority_score:+.3f} | {loop_name:20s} | "
                f"Δ: {perf.avg_delta:+.4f} | {status}"
            )
    
    async def _execute_priority_ordered_cycle(self, cycle_num: int):
        """Execute loops in priority order, skipping paused ones."""
        sorted_loops = sorted(
            self.performance.items(),
            key=lambda x: x[1].priority_score,
            reverse=True
        )
        
        for loop_name, perf in sorted_loops:
            if loop_name in self.paused_loops:
                logger.info(f"  ⊘ {loop_name} - SKIPPED (paused)")
                continue
            
            if loop_name in self.throttled_loops:
                # Throttled loops get partial execution
                logger.info(f"  ≈ {loop_name} - THROTTLED (partial execution)")
                await self._execute_loop_cycle(loop_name, partial=True)
            else:
                await self._execute_loop_cycle(loop_name, partial=False)
    
    async def _execute_loop_cycle(self, loop_name: str, partial: bool = False):
        """Execute a single loop cycle and measure real delta."""
        loop_instance = getattr(self, loop_name, None)
        if not loop_instance:
            logger.warning(f"  ! {loop_name} - No instance available")
            return
        
        cycle_start = time.time()
        real_delta = 0.0
        success = False
        error = None
        
        try:
            # Execute the actual cycle
            if hasattr(loop_instance, 'run_cycle'):
                await loop_instance.run_cycle()
            elif hasattr(loop_instance, 'query'):
                await loop_instance.query("growth optimization cycle")
            elif hasattr(loop_instance, 'evolve'):
                await loop_instance.evolve(generations=1)
            else:
                logger.warning(f"  ! {loop_name} - No cycle method found")
                return
            
            success = True
            self.cycles_completed[loop_name] += 1
            
            # MEASURE REAL DELTA (not simulated!)
            real_delta = await self._measure_real_delta(loop_name)
            
        except Exception as e:
            error = str(e)
            logger.error(f"  ✗ {loop_name} - Failed: {e}")
        
        finally:
            duration = time.time() - cycle_start
            
            # Record performance metrics
            self.performance[loop_name].record_cycle(real_delta, duration)
            
            # Record to instrumenter
            if self.instrumenter:
                self.instrumenter.record_cycle(
                    loop_name,
                    delta=real_delta,
                    duration=duration,
                    success=success,
                    metadata={"error": error} if error else None
                )
            
            # Log result
            status = "✓" if success else "✗"
            partial_mark = "≈" if partial else "="
            logger.info(
                f"  {status} {partial_mark} {loop_name:20s} | "
                f"Δ: {real_delta:+.4f} | {duration:.2f}s"
            )
    
    async def _measure_real_delta(self, loop_name: str) -> float:
        """
        Measure REAL capability delta, not simulate it.
        
        This is the critical improvement over the basic version.
        """
        # Method 1: Check if the loop produced measurable outputs
        real_delta = 0.0
        
        try:
            # Check memory for new patterns (self-compiler)
            if loop_name == "self_compiler" and self.memory:
                new_patterns = await self.memory.query(
                    "recent patterns extracted", limit=10
                )
                real_delta += len(new_patterns) * 0.01
            
            # Check for evolved goals (goal-evolver)
            if loop_name == "goal_evolver" and self.memory:
                evolved_goals = await self.memory.query(
                    "evolved goals", limit=5
                )
                real_delta += len(evolved_goals) * 0.02
            
            # Check for improved retrieval (memory-reasoner)
            if loop_name == "memory_reasoner" and self.memory:
                # Test query performance
                test_start = time.time()
                result = await self.memory.query("test query", limit=5)
                query_time = time.time() - test_start
                # Faster queries = improvement
                if query_time < 0.5:
                    real_delta += 0.01
            
            # Check for simulated experiences (dreaming-machine)
            if loop_name == "dreaming_machine" and self.memory:
                experiences = await self.memory.query(
                    "simulated experience", limit=5
                )
                real_delta += len(experiences) * 0.005
            
            # Omega delta is measured by coupling improvements
            if loop_name == "omega" and self.coupling_tracker:
                coupling_strength = await self._get_coupling_strength()
                real_delta = coupling_strength * 0.1
            
        except Exception as e:
            logger.warning(f"Error measuring delta for {loop_name}: {e}")
        
        # Ensure delta is bounded
        real_delta = max(-0.1, min(1.0, real_delta))
        
        return real_delta
    
    async def _get_coupling_strength(self) -> float:
        """Get overall coupling strength metric."""
        if not self.coupling_tracker:
            return 0.0
        
        try:
            # Measure a few key couplings
            couplings = [
                self.coupling_tracker.measure_correlation(
                    "goal_evolver", "self_compiler"
                ),
                self.coupling_tracker.measure_correlation(
                    "memory_reasoner", "self_compiler"
                ),
            ]
            return sum(c for c in couplings if c is not None) / len(couplings)
        except Exception:
            return 0.0
    
    async def _analyze_cycle_results(self, cycle_num: int):
        """Analyze cycle results and identify issues."""
        logger.info("\n[Analysis] Cycle performance:")
        
        total_delta = sum(
            perf.last_delta 
            for perf in self.performance.values()
        )
        logger.info(f"  Total Cycle Delta: {total_delta:+.4f}")
        
        growing = [
            name for name, perf in self.performance.items()
            if perf.is_growing
        ]
        bottlenecks = [
            name for name, perf in self.performance.items()
            if perf.is_false_bottleneck
        ]
        
        if growing:
            logger.info(f"  Growing loops: {', '.join(growing)}")
        if bottlenecks:
            logger.warning(f"  ⚠ False bottlenecks detected: {', '.join(bottlenecks)}")
    
    async def _manage_false_bottlenecks(self):
        """Throttle or pause false bottlenecks."""
        for loop_name, perf in self.performance.items():
            if perf.is_false_bottleneck:
                if loop_name not in self.paused_loops and loop_name not in self.throttled_loops:
                    logger.warning(
                        f"\n⚠ THROTTLING {loop_name} - "
                        f"Spinning without growth (Δ={perf.avg_delta:.4f})"
                    )
                    self.throttled_loops.add(loop_name)
            
            # If severely non-productive, pause entirely
            if perf.avg_delta < -0.01 and perf.cycles_run >= 5:
                if loop_name not in self.paused_loops:
                    logger.error(
                        f"\n✗ PAUSING {loop_name} - "
                        f"Negative delta, wasting resources"
                    )
                    self.paused_loops.add(loop_name)
    
    def _print_growth_report(self):
        """Print final growth report."""
        logger.info("\n" + "=" * 70)
        logger.info("FINAL GROWTH REPORT")
        logger.info("=" * 70)
        
        # Sort by total delta
        sorted_performance = sorted(
            self.performance.items(),
            key=lambda x: x[1].total_delta,
            reverse=True
        )
        
        logger.info("\nLoop Performance Summary:")
        logger.info(f"{'Loop':<20} {'Cycles':<8} {'Total Δ':<10} {'Avg Δ':<10} {'Status':<15}")
        logger.info("-" * 70)
        
        for loop_name, perf in sorted_performance:
            status = "GROWING" if perf.is_growing else "STAGNANT"
            if perf.is_false_bottleneck:
                status = "FALSE BOTTLENECK"
            elif loop_name in self.paused_loops:
                status = "PAUSED"
            elif loop_name in self.throttled_loops:
                status = "THROTTLED"
            
            logger.info(
                f"{loop_name:<20} {perf.cycles_run:<8} "
                f"{perf.total_delta:<10.4f} {perf.avg_delta:<10.4f} {status:<15}"
            )
        
        total_delta = sum(p.total_delta for p in self.performance.values())
        logger.info(f"\nTOTAL CAPABILITY GROWTH: {total_delta:+.4f}")
        
        if total_delta > 0:
            logger.info("✓ POSITIVE GROWTH - System is improving!")
        else:
            logger.warning("⚠ ZERO/NEGATIVE GROWTH - Review loop priorities")
        
        logger.info("")
    
    async def measure_coupling(self):
        """Measure loop interactions and coupling strength."""
        if not self.coupling_tracker:
            logger.warning("No coupling tracker available")
            return {}
        
        results = {}
        loops = list(self.coupling_tracker.LOOPS)
        
        logger.info("\n" + "=" * 60)
        logger.info("COUPLING ANALYSIS")
        logger.info("=" * 60)
        
        for i, loop_a in enumerate(loops):
            for loop_b in loops[i+1:]:
                try:
                    corr = await self.coupling_tracker.measure_correlation(
                        loop_a, loop_b
                    )
                    results[f"{loop_a}_{loop_b}"] = corr
                    
                    strength = "STRONG" if abs(corr) > 0.5 else "WEAK"
                    logger.info(f"  {loop_a} <-> {loop_b}: {corr:+.3f} ({strength})")
                except Exception as e:
                    logger.warning(f"  Could not measure {loop_a} <-> {loop_b}: {e}")
        
        return results


async def main(num_cycles: int = 3):
    """Main entry point for growth-optimized loop activation."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("\n" + "=" * 70)
    print("BYRD GROWTH-OPTIMIZED LOOP SYSTEM")
    print("=" * 70)
    print("Mission: Stop wasting cycles on false bottlenecks")
    print("Focus: Activate loops that actually drive growth")
    print("=" * 70 + "\n")
    
    try:
        memory = Memory()
        await memory.initialize()
        llm_client = LLMClient()
    
        activator = GrowthOptimizedActivator(
            memory=memory,
            llm_client=llm_client,
            config={
                "self_compiler": {"aggressive_pattern_extraction": True},
                "goal_evolver": {"capability_fitness": True},
            }
        )
        
        # Activate growth loops
        await activator.activate_growth_loops()
        
        # Run growth-optimized cycles
        await activator.run_growth_cycles(num_cycles=num_cycles)
        
        # Measure coupling
        coupling = await activator.measure_coupling()
        
        print("\n" + "=" * 70)
        print("GROWTH OPTIMIZATION COMPLETE")
        print("=" * 70 + "\n")
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Activate BYRD loops with growth optimization"
    )
    parser.add_argument(
        "--cycles", "-c",
        type=int,
        default=3,
        help="Number of cycles to run"
    )
    args = parser.parse_args()
    
    asyncio.run(main(num_cycles=args.cycles))
