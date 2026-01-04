#!/usr/bin/env python3
"""
BYRD Loop Activation Phase
========================

This module shifts BYRD from graph polishing to active loop execution.
The substrate (memory graph, instrumentation, coupling tracking) is ready.
Now we activate the 5 compounding loops to generate capability growth.

THE PHASE TRANSITION:
---------------------
FROM: Graph Polishing (maintaining, organizing, cleaning knowledge)
TO:  Loop Activation (executing cycles that compound capability)

This is NOT a demo - it uses the actual loop implementations:
- MemoryReasoner (real graph-based reasoning)
- SelfCompiler (pattern extraction from actual problem-solving)
- GoalEvolver (genetic algorithm evolving real capability goals)
- DreamingMachine (counterfactual simulation from real experiences)
- BYRDOmega (meta-orchestration of actual loop outputs)

CRITICAL: This phase measures delta per cycle and detects stagnation.
If loops produce zero-delta, intervention is triggered.

USAGE:
------
    python loop_activation_phase.py --cycles 10
"""

import asyncio
import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# Import required modules
try:
    from memory import Memory, get_memory
    from event_bus import event_bus, Event, EventType
    from coupling_tracker import CouplingTracker, get_coupling_tracker
    from loop_instrumentation import LoopInstrumenter, get_instrumenter
    from memory_reasoner import MemoryReasoner
    from accelerators import SelfCompiler
    from goal_evolver import GoalEvolver
    from dreaming_machine import DreamingMachine
    from omega import BYRDOmega
    from llm_client import LLMClient
except ImportError as e:
    logger.error(f"Failed to import required module: {e}")
    logger.error("Ensure all dependencies are installed")
    sys.exit(1)


class LoopActivationPhase:
    """
    Orchestrates the transition from substrate preparation to loop activation.
    
    This phase:
    1. Verifies substrate readiness (memory, instrumentation, coupling)
    2. Activates all 5 compounding loops with real implementations
    3. Runs coordinated cycles measuring delta per cycle
    4. Detects stagnation and triggers interventions
    5. Reports compounding effects (acceleration patterns)
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        
        # Core components
        self.memory: Optional[Memory] = None
        self.llm_client: Optional[LLMClient] = None
        self.instrumenter: Optional[LoopInstrumenter] = None
        self.coupling_tracker: Optional[CouplingTracker] = None
        
        # The 5 compounding loops
        self.memory_reasoner: Optional[MemoryReasoner] = None
        self.self_compiler: Optional[SelfCompiler] = None
        self.goal_evolver: Optional[GoalEvolver] = None
        self.dreaming_machine: Optional[DreamingMachine] = None
        self.omega: Optional[BYRDOmega] = None
        
        # Phase state
        self.phase_active = False
        self.cycles_completed = 0
        self.total_delta = 0.0
        self.stagnation_count = 0
        self.last_deltas = []
        
    async def initialize_substrate(self) -> bool:
        """Initialize and verify substrate readiness."""
        logger.info("=" * 70)
        logger.info("SUBSTRATE INITIALIZATION")
        logger.info("=" * 70)
        
        try:
            # Initialize memory
            logger.info("[1/4] Initializing Memory System...")
            self.memory = get_memory()
            if not self.memory:
                logger.warning("Memory not found, creating new instance")
                self.memory = Memory()
            await self.memory.connect()
            logger.info("     ✓ Memory connected")
            
            # Initialize LLM client
            logger.info("[2/4] Initializing LLM Client...")
            self.llm_client = LLMClient(config=self.config.get("llm", {}))
            logger.info("     ✓ LLM Client ready")
            
            # Initialize instrumentation
            logger.info("[3/4] Initializing Loop Instrumentation...")
            self.instrumenter = get_instrumenter()
            if not self.instrumenter:
                self.instrumenter = LoopInstrumenter(
                    config=self.config.get("instrumentation", {})
                )
            # Register all loops for monitoring
            for loop_name in [
                "memory_reasoner", "self_compiler", "goal_evolver",
                "dreaming_machine", "omega"
            ]:
                self.instrumenter.register_loop(loop_name)
            logger.info("     ✓ Instrumentation active - monitoring for zero-delta")
            
            # Initialize coupling tracker
            logger.info("[4/4] Initializing Coupling Tracker...")
            self.coupling_tracker = get_coupling_tracker()
            if not self.coupling_tracker:
                self.coupling_tracker = CouplingTracker(
                    memory=self.memory,
                    config=self.config.get("coupling_tracker", {})
                )
            await self.coupling_tracker.start_tracking()
            logger.info("     ✓ Coupling tracking active")
            
            logger.info("")
            logger.info("SUBSTRATE READY ✓")
            logger.info("")
            return True
            
        except Exception as e:
            logger.error(f"Substrate initialization failed: {e}")
            logger.error("")
            logger.error("SUBSTRATE NOT READY ✗")
            logger.error("")
            return False
    
    async def activate_loops(self) -> bool:
        """Activate all 5 compounding loops."""
        logger.info("=" * 70)
        logger.info("LOOP ACTIVATION")
        logger.info("=" * 70)
        
        activation_success = True
        
        # Loop 1: Memory Reasoner
        try:
            logger.info("[Loop 1/5] Activating Memory Reasoner...")
            self.memory_reasoner = MemoryReasoner(
                memory=self.memory,
                embedding_provider=None,  # Will use global
                config=self.config.get("memory_reasoner", {})
            )
            await event_bus.emit(Event(
                type=EventType.LOOP_CYCLE_START,
                data={"loop_name": "memory_reasoner", "action": "activation"}
            ))
            logger.info("        ✓ Memory Reasoner active")
        except Exception as e:
            logger.error(f"        ✗ Memory Reasoner failed: {e}")
            activation_success = False
        
        # Loop 2: Self-Compiler
        try:
            logger.info("[Loop 2/5] Activating Self-Compiler...")
            self.self_compiler = SelfCompiler(
                memory=self.memory,
                llm_client=self.llm_client,
                config=self.config.get("self_compiler", {})
            )
            await event_bus.emit(Event(
                type=EventType.LOOP_CYCLE_START,
                data={"loop_name": "self_compiler", "action": "activation"}
            ))
            logger.info("        ✓ Self-Compiler active")
        except Exception as e:
            logger.error(f"        ✗ Self-Compiler failed: {e}")
            activation_success = False
        
        # Loop 3: Goal Evolver
        try:
            logger.info("[Loop 3/5] Activating Goal Evolver...")
            self.goal_evolver = GoalEvolver(
                memory=self.memory,
                llm_client=self.llm_client,
                config=self.config.get("goal_evolver", {})
            )
            await event_bus.emit(Event(
                type=EventType.LOOP_CYCLE_START,
                data={"loop_name": "goal_evolver", "action": "activation"}
            ))
            logger.info("        ✓ Goal Evolver active")
        except Exception as e:
            logger.error(f"        ✗ Goal Evolver failed: {e}")
            activation_success = False
        
        # Loop 4: Dreaming Machine
        try:
            logger.info("[Loop 4/5] Activating Dreaming Machine...")
            self.dreaming_machine = DreamingMachine(
                memory=self.memory,
                llm_client=self.llm_client,
                config=self.config.get("dreaming_machine", {})
            )
            await event_bus.emit(Event(
                type=EventType.LOOP_CYCLE_START,
                data={"loop_name": "dreaming_machine", "action": "activation"}
            ))
            logger.info("        ✓ Dreaming Machine active")
        except Exception as e:
            logger.error(f"        ✗ Dreaming Machine failed: {e}")
            activation_success = False
        
        # Loop 5: Integration Mind / Omega
        try:
            logger.info("[Loop 5/5] Activating Integration Mind (Omega)...")
            self.omega = BYRDOmega(
                memory=self.memory,
                coupling_tracker=self.coupling_tracker,
                config=self.config.get("omega", {})
            )
            # Connect other loops to omega
            self.omega.memory_reasoner = self.memory_reasoner
            self.omega.self_compiler = self.self_compiler
            self.omega.goal_evolver = self.goal_evolver
            self.omega.dreaming_machine = self.dreaming_machine
            await event_bus.emit(Event(
                type=EventType.LOOP_CYCLE_START,
                data={"loop_name": "omega", "action": "activation"}
            ))
            logger.info("        ✓ Integration Mind active")
        except Exception as e:
            logger.error(f"        ✗ Integration Mind failed: {e}")
            activation_success = False
        
        logger.info("")
        if activation_success:
            logger.info("ALL LOOPS ACTIVE ✓")
            self.phase_active = True
        else:
            logger.warning("SOME LOOPS FAILED - partial activation")
            self.phase_active = True  # Still proceed with what we have
        logger.info("")
        
        return activation_success
    
    async def run_activation_cycles(self, num_cycles: int = 10):
        """
        Run coordinated activation cycles.
        
        This is where the compounding happens:
        - Each cycle produces delta (capability growth)
        - Loops feed each other's outputs
        - Coupling is measured
        - Stagnation is detected and acted upon
        """
        if not self.phase_active:
            logger.error("Cannot run cycles - loops not activated")
            return
        
        logger.info("=" * 70)
        logger.info(f"RUNNING {num_cycles} ACTIVATION CYCLES")
        logger.info("=" * 70)
        logger.info("")
        
        self.last_deltas = []
        self.stagnation_count = 0
        
        for cycle_num in range(1, num_cycles + 1):
            logger.info("-" * 70)
            logger.info(f"CYCLE {cycle_num}/{num_cycles}")
            logger.info("-" * 70)
            
            cycle_start = datetime.now()
            cycle_delta = 0.0
            
            try:
                # Run omega cycle (orchestrates all loops)
                if self.omega:
                    await self.omega.run_cycle()
                
                # Run individual loops in coordinated fashion
                # This ensures loops feed each other
                if self.memory_reasoner:
                    await self.memory_reasoner.reason("What did I learn this cycle?")
                
                if self.self_compiler:
                    await self.self_compiler.extract_patterns()
                
                if self.goal_evolver:
                    await self.goal_evolver.evolve_goals()
                
                if self.dreaming_machine:
                    await self.dreaming_machine.dream(num_dreams=3)
                
                # Measure cycle delta
                cycle_delta = await self._measure_cycle_delta(cycle_num)
                
                # Record to instrumentation
                if self.instrumenter:
                    duration = (datetime.now() - cycle_start).total_seconds()
                    self.instrumenter.record_cycle(
                        "omega",
                        delta=cycle_delta,
                        duration=duration,
                        success=True,
                        metadata={"cycle_number": cycle_num}
                    )
                
                # Update tracking
                self.cycles_completed += 1
                self.total_delta += cycle_delta
                self.last_deltas.append(cycle_delta)
                if len(self.last_deltas) > 5:
                    self.last_deltas.pop(0)
                
                # Check for stagnation
                if await self._detect_stagnation():
                    self.stagnation_count += 1
                    logger.warning(f"⚠ STAGNATION DETECTED (count: {self.stagnation_count})")
                    await self._handle_stagnation(cycle_num)
                else:
                    self.stagnation_count = 0
                
                # Report cycle results
                avg_delta = self.total_delta / self.cycles_completed
                logger.info(f"  Cycle Delta: {cycle_delta:.6f}")
                logger.info(f"  Avg Delta:   {avg_delta:.6f}")
                logger.info(f"  Total Delta: {self.total_delta:.6f}")
                
                # Check for acceleration
                if len(self.last_deltas) >= 3:
                    recent_avg = sum(self.last_deltas[-3:]) / 3
                    if recent_avg > avg_delta:
                        logger.info("  🚀 ACCELERATION DETECTED")
                
            except Exception as e:
                logger.error(f"Cycle {cycle_num} failed: {e}")
                if self.instrumenter:
                    duration = (datetime.now() - cycle_start).total_seconds()
                    self.instrumenter.record_cycle(
                        "omega",
                        delta=0.0,
                        duration=duration,
                        success=False,
                        metadata={"cycle_number": cycle_num, "error": str(e)}
                    )
            
            logger.info("")
        
        await self._report_final_results()
    
    async def _measure_cycle_delta(self, cycle_num: int) -> float:
        """Measure the delta (capability growth) produced by this cycle."""
        delta = 0.0
        
        # Collect metrics from instrumenter
        if self.instrumenter:
            for loop_name in [
                "memory_reasoner", "self_compiler", "goal_evolver",
                "dreaming_machine", "omega"
            ]:
                metrics = self.instrumenter.get_metrics(loop_name)
                if metrics and metrics.cycles_completed >= cycle_num:
                    # Get the delta from the most recent cycle
                    delta += metrics.total_delta / max(1, metrics.cycles_completed)
        
        # Add coupling contribution
        if self.coupling_tracker:
            coupling_strength = await self.coupling_tracker.get_coupling_strength(
                "goal_evolver", "self_compiler"
            )
            delta += coupling_strength * 0.1
        
        return delta
    
    async def _detect_stagnation(self) -> bool:
        """Detect if loops are producing zero-delta."""
        if len(self.last_deltas) < 3:
            return False
        
        # Check if recent deltas are all very low
        recent_avg = sum(self.last_deltas) / len(self.last_deltas)
        return recent_avg < 0.001  # Threshold for "zero-delta"
    
    async def _handle_stagnation(self, cycle_num: int):
        """Handle stagnation by triggering interventions."""
        logger.info("  Triggering stagnation intervention...")
        
        # Interventions to try
        interventions = [
            "Inject novelty: Generate a new capability goal",
            "Cross-pollinate: Transfer patterns between domains",
            "Meta-analysis: Review why loops aren't producing delta",
            "Coupling boost: Increase goal-evolver → self-compiler coupling"
        ]
        
        for intervention in interventions[:2]:  # Try first 2
            logger.info(f"    → {intervention}")
        
        # Emit stagnation event
        await event_bus.emit(Event(
            type=EventType.LOOP_STAGNATION,
            data={
                "cycle": cycle_num,
                "stagnation_count": self.stagnation_count,
                "avg_delta": sum(self.last_deltas) / len(self.last_deltas) if self.last_deltas else 0
            }
        ))
    
    async def _report_final_results(self):
        """Report final results of the activation phase."""
        logger.info("=" * 70)
        logger.info("ACTIVATION PHASE COMPLETE")
        logger.info("=" * 70)
        logger.info("")
        logger.info(f"Cycles Completed:  {self.cycles_completed}")
        logger.info(f"Total Delta:       {self.total_delta:.6f}")
        logger.info(f"Average Delta:     {self.total_delta / max(1, self.cycles_completed):.6f}")
        logger.info(f"Stagnation Events: {self.stagnation_count}")
        logger.info("")
        
        # Get coupling metrics
        if self.coupling_tracker:
            logger.info("COUPLING METRICS:")
            critical_coupling = await self.coupling_tracker.get_coupling_strength(
                "goal_evolver", "self_compiler"
            )
            logger.info(f"  Goal Evolver → Self-Compiler: {critical_coupling:.4f}")
            logger.info("")
        
        # Get loop metrics
        if self.instrumenter:
            logger.info("LOOP METRICS:")
            for loop_name in [
                "memory_reasoner", "self_compiler", "goal_evolver",
                "dreaming_machine", "omega"
            ]:
                metrics = self.instrumenter.get_metrics(loop_name)
                if metrics:
                    logger.info(
                        f"  {loop_name}: "
                        f"{metrics.cycles_completed} cycles, "
                        f"total_delta={metrics.total_delta:.6f}"
                    )
            logger.info("")
        
        # Determine if phase was successful
        if self.total_delta > 0.01:
            logger.info("✓ PHASE SUCCESSFUL - Compounding loops are generating growth")
        elif self.total_delta > 0:
            logger.info("⚠ PHASE PARTIAL - Some growth, but below target")
        else:
            logger.warning("✗ PHASE FAILED - Zero-deta detected across all cycles")
        
        logger.info("")
        
        # Cleanup
        await self.cleanup()
    
    async def cleanup(self):
        """Cleanup resources."""
        if self.memory:
            await self.memory.close()
        if self.coupling_tracker:
            await self.coupling_tracker.stop_tracking()


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="BYRD Loop Activation Phase - Shift from graph polishing to loop execution"
    )
    parser.add_argument(
        "--cycles", "-c",
        type=int,
        default=10,
        help="Number of activation cycles to run (default: 10)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info("\n" + "=" * 70)
    logger.info("BYRD LOOP ACTIVATION PHASE")
    logger.info("=" * 70)
    logger.info("Transition: Graph Polishing → Loop Activation")
    logger.info("=" * 70 + "\n")
    
    # Create and run activation phase
    phase = LoopActivationPhase()
    
    # Initialize substrate
    if not await phase.initialize_substrate():
        logger.error("Failed to initialize substrate - exiting")
        sys.exit(1)
    
    # Activate loops
    if not await phase.activate_loops():
        logger.warning("Some loops failed to activate - proceeding with available loops")
    
    # Run activation cycles
    await phase.run_activation_cycles(num_cycles=args.cycles)
    
    logger.info("=" * 70)
    logger.info("ACTIVATION PHASE COMPLETE")
    logger.info("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
