"""
BYRD Compounding Loops Activation & Measurement System
========================================================

This module activates all 5 compounding loops and measures their interactions.

THE FIVE COMPOUNDING LOOPS:
---------------------------
1. Memory Reasoner (Loop 1)
   - Graph-based reasoning through the memory system
   - Uses spreading activation to answer queries
   - Learns retrieval patterns over time
   
2. Self-Compiler (Loop 2)
   - Learns patterns from successful problem-solving
   - Extracts, matches, and lifts solution patterns
   - Compounds: more patterns = more solutions = more patterns
   
3. Goal Evolver (Loop 3)
   - Evolves goals using genetic algorithms
   - Fitness based on capability growth, not just completion
   - Discovers goals that maximize learning
   
4. Dreaming Machine (Loop 4)
   - Multiplies experience through counterfactuals
   - Replays successful experiences
   - Transfers patterns across domains
   
5. Integration Mind / Omega (Loop 5)
   - Meta-orchestrator for all loops
   - Measures coupling between loops
   - Transitions operating modes based on state
   
COMPOUNDING THEORY:
------------------
Loops compound when their outputs feed each other's inputs in positive
feedback cycles. The critical metric is Goal Evolver → Self-Compiler
coupling: when goals drive code changes that improve capability,
we have true acceleration.

USAGE:
------
    from activate_loops import CompoundingLoopsActivator
    
    activator = CompoundingLoopsActivator(memory, llm_client)
    await activator.activate_all_loops()
    await activator.run_cycles(num_cycles=3)
    coupling = await activator.measure_coupling()
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, Optional

from memory import Memory
from event_bus import event_bus, Event, EventType
from coupling_tracker import CouplingTracker, get_coupling_tracker
from memory_reasoner import MemoryReasoner
from accelerators import SelfCompiler
from goal_evolver import GoalEvolver
from dreaming_machine import DreamingMachine
from omega import BYRDOmega
from llm_client import LLMClient

logger = logging.getLogger(__name__)


class CompoundingLoopsActivator:
    """Activates and measures all 5 compounding loops."""
    
    def __init__(self, memory: Memory, llm_client: LLMClient, config: Optional[Dict] = None):
        self.memory = memory
        self.llm_client = llm_client
        self.config = config or {}
        
        self.memory_reasoner = None
        self.self_compiler = None
        self.goal_evolver = None
        self.dreaming_machine = None
        self.omega = None
        self.coupling_tracker = None
        
        self.activation_results = {}
        self.cycles_completed = {}
    
    async def activate_all_loops(self):
        """Activate all 5 compounding loops."""
        logger.info("=" * 60)
        logger.info("ACTIVATING 5 COMPOUNDING LOOPS")
        logger.info("=" * 60)
        
        await self._activate_coupling_tracker()
        await self._activate_memory_reasoner()
        await self._activate_self_compiler()
        await self._activate_goal_evolver()
        await self._activate_dreaming_machine()
        await self._activate_omega()
        
        self._print_summary()
        return self.activation_results
    
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
            self.activation_results["coupling_tracker"] = {"success": False, "error": str(e)}
            logger.error(f"[coupling_tracker] Failed: {e}")
    
    async def _activate_memory_reasoner(self):
        """Activate Loop 1: Memory Reasoner."""
        try:
            logger.info("[memory_reasoner] Initializing...")
            self.memory_reasoner = MemoryReasoner(
                memory=self.memory,
                llm_client=self.llm_client,
                config=self.config.get("memory_reasoner", {})
            )
            await self.memory_reasoner.query("test activation")
            self.activation_results["memory_reasoner"] = {"success": True}
            logger.info("[memory_reasoner] Activated")
            await event_bus.emit(Event(
                type=EventType.LOOP_CYCLE_START,
                data={"loop_name": "memory_reasoner", "action": "activation"}
            ))
        except Exception as e:
            self.activation_results["memory_reasoner"] = {"success": False, "error": str(e)}
            logger.error(f"[memory_reasoner] Failed: {e}")
    
    async def _activate_self_compiler(self):
        """Activate Loop 2: Self-Compiler."""
        try:
            logger.info("[self_compiler] Initializing...")
            self.self_compiler = SelfCompiler(
                memory=self.memory,
                llm_client=self.llm_client,
                config=self.config.get("self_compiler", {})
            )
            self.activation_results["self_compiler"] = {"success": True}
            logger.info("[self_compiler] Activated")
            await event_bus.emit(Event(
                type=EventType.LOOP_CYCLE_START,
                data={"loop_name": "self_compiler", "action": "activation"}
            ))
        except Exception as e:
            self.activation_results["self_compiler"] = {"success": False, "error": str(e)}
            logger.error(f"[self_compiler] Failed: {e}")
    
    async def _activate_goal_evolver(self):
        """Activate Loop 3: Goal Evolver."""
        try:
            logger.info("[goal_evolver] Initializing...")
            self.goal_evolver = GoalEvolver(
                memory=self.memory,
                llm_client=self.llm_client,
                config=self.config.get("goal_evolver", {})
            )
            self.activation_results["goal_evolver"] = {"success": True}
            logger.info("[goal_evolver] Activated")
            await event_bus.emit(Event(
                type=EventType.LOOP_CYCLE_START,
                data={"loop_name": "goal_evolver", "action": "activation"}
            ))
        except Exception as e:
            self.activation_results["goal_evolver"] = {"success": False, "error": str(e)}
            logger.error(f"[goal_evolver] Failed: {e}")
    
    async def _activate_dreaming_machine(self):
        """Activate Loop 4: Dreaming Machine."""
        try:
            logger.info("[dreaming_machine] Initializing...")
            self.dreaming_machine = DreamingMachine(
                memory=self.memory,
                llm_client=self.llm_client,
                config=self.config.get("dreaming_machine", {})
            )
            self.activation_results["dreaming_machine"] = {"success": True}
            logger.info("[dreaming_machine] Activated")
            await event_bus.emit(Event(
                type=EventType.LOOP_CYCLE_START,
                data={"loop_name": "dreaming_machine", "action": "activation"}
            ))
        except Exception as e:
            self.activation_results["dreaming_machine"] = {"success": False, "error": str(e)}
            logger.error(f"[dreaming_machine] Failed: {e}")
    
    async def _activate_omega(self):
        """Activate Loop 5: Integration Mind."""
        try:
            logger.info("[omega] Initializing Integration Mind...")
            self.omega = BYRDOmega(
                memory=self.memory,
                coupling_tracker=self.coupling_tracker,
                config=self.config.get("omega", {})
            )
            if self.memory_reasoner:
                self.omega.memory_reasoner = self.memory_reasoner
            if self.self_compiler:
                self.omega.self_compiler = self.self_compiler
            if self.goal_evolver:
                self.omega.goal_evolver = self.goal_evolver
            if self.dreaming_machine:
                self.omega.dreaming_machine = self.dreaming_machine
            self.activation_results["omega"] = {"success": True}
            logger.info("[omega] Activated")
            await event_bus.emit(Event(
                type=EventType.LOOP_CYCLE_START,
                data={"loop_name": "omega", "action": "activation"}
            ))
        except Exception as e:
            self.activation_results["omega"] = {"success": False, "error": str(e)}
            logger.error(f"[omega] Failed: {e}")
    
    def _print_summary(self):
        """Print activation summary."""
        logger.info("")
        logger.info("=" * 60)
        logger.info("ACTIVATION SUMMARY")
        logger.info("=" * 60)
        successful = sum(1 for r in self.activation_results.values() if r.get("success"))
        total = len(self.activation_results)
        for name, result in self.activation_results.items():
            status = "OK" if result.get("success") else "FAIL"
            logger.info(f"{status} {name}")
        logger.info(f"Total: {successful}/{total} activated")
        logger.info("")
    
    async def run_cycles(self, num_cycles: int = 3):
        """Run coordinated cycles."""
        logger.info(f"Running {num_cycles} coordinated cycles...")
        loop_names = ["memory_reasoner", "self_compiler", "goal_evolver", "dreaming_machine", "omega"]
        self.cycles_completed = {name: 0 for name in loop_names}
        
        for i in range(num_cycles):
            logger.info(f"--- Cycle {i+1}/{num_cycles} ---")
            
            if self.omega:
                try:
                    await self.omega.run_cycle()
                    self.cycles_completed["omega"] += 1
                except Exception as e:
                    logger.error(f"Omega cycle failed: {e}")
            
            if self.coupling_tracker:
                await self.coupling_tracker.emit_coupling_event()
        
        logger.info(f"Cycles completed: {self.cycles_completed}")
        return self.cycles_completed
    
    async def measure_coupling(self):
        """Measure loop interactions."""
        if not self.coupling_tracker:
            logger.warning("No coupling tracker available")
            return {}
        
        results = {}
        loops = list(self.coupling_tracker.LOOPS)
        
        for i, loop_a in enumerate(loops):
            for loop_b in loops[i+1:]:
                try:
                    corr = await self.coupling_tracker.measure_correlation(loop_a, loop_b)
                    results[f"{loop_a}_{loop_b}"] = corr
                    logger.info(f"{loop_a} <-> {loop_b}: {corr:+.3f}")
                except Exception as e:
                    logger.warning(f"Could not measure {loop_a} <-> {loop_b}: {e}")
        
        return results


async def main(num_cycles: int = 3):
    """Main entry point."""
    logging.basicConfig(level=logging.INFO)
    
    print("\n" + "=" * 60)
    print("BYRD COMPOUNDING LOOPS - ACTIVATION & MEASUREMENT")
    print("=" * 60 + "\n")
    
    try:
        memory = Memory()
        await memory.initialize()
        llm_client = LLMClient()
    except Exception as e:
        logger.error(f"Failed to initialize: {e}")
        return
    
    activator = CompoundingLoopsActivator(memory, llm_client)
    
    await activator.activate_all_loops()
    await activator.run_cycles(num_cycles)
    await activator.measure_coupling()
    
    print("\n" + "=" * 60)
    print("ACTIVATION COMPLETE")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    import sys
    cycles = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    asyncio.run(main(cycles))
