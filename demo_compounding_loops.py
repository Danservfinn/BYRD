"""
BYRD Compounding Loops Demonstration
====================================

This script demonstrates how to activate and measure all 5 compounding loops.
It uses mock components to run standalone without requiring the full BYRD system.

The Five Compounding Loops:
1. Memory Reasoner - Graph-based reasoning through memory
2. Self-Compiler - Pattern learning from successes
3. Goal Evolver - Evolutionary goal optimization  
4. Dreaming Machine - Experience multiplication
5. Integration Mind (Omega) - Meta-orchestration

Run: python demo_compounding_loops.py
"""

import asyncio
import sys
import os
from datetime import datetime
from typing import Dict, Optional, Any
from unittest.mock import MagicMock, AsyncMock

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from event_bus import event_bus, Event, EventType


class MockMemory:
    """Mock memory for demonstration."""
    async def initialize(self):
        return True
    
    async def record_experience(self, content: str, type: str = "experience"):
        pass
    
    async def query(self, query: str):
        return []


class MockLLMClient:
    """Mock LLM client for demonstration."""
    async def generate(self, prompt: str, **kwargs):
        return "Mock response for demonstration"


class CompoundingLoopsDemo:
    """
    Demonstrates activation and measurement of all 5 compounding loops.
    
    This shows the proper sequence and dependencies:
    1. CouplingTracker (measures all interactions)
    2. Memory Reasoner (foundational)
    3. Self-Compiler (needs memory)
    4. Goal Evolver (needs memory)
    5. Dreaming Machine (needs memory and patterns)
    6. Omega (orchestrates all)
    """
    
    def __init__(self):
        self.memory = MockMemory()
        self.llm_client = MockLLMClient()
        self.loops = {}
        self.activation_times = {}
        self.cycle_counts = {}
        self.coupling_measurements = {}
    
    async def initialize(self):
        """Initialize mock memory."""
        await self.memory.initialize()
        print("\n" + "="*70)
        print("BYRD COMPOUNDING LOOPS - ACTIVATION & MEASUREMENT DEMO")
        print("="*70)
        print("\nInitializing mock memory... OK")
    
    async def activate_coupling_tracker(self):
        """Activate the coupling tracker (Loop 0)."""
        print("\n[0/6] Activating Coupling Tracker...")
        start = datetime.now()
        
        try:
            from coupling_tracker import CouplingTracker
            
            self.loops['coupling_tracker'] = CouplingTracker(
                memory=self.memory,
                config={}
            )
            await self.loops['coupling_tracker'].start_tracking()
            
            duration = (datetime.now() - start).total_seconds()
            self.activation_times['coupling_tracker'] = duration
            print(f"      ✓ Coupling Tracker activated ({duration:.3f}s)")
            print(f"      - Tracks: {len(self.loops['coupling_tracker'].LOOPS)} loops")
            
            return True
        except ImportError:
            print(f"      ! Coupling Tracker module not found (skipping)")
            self.loops['coupling_tracker'] = None
            return False
        except Exception as e:
            print(f"      ✗ Failed: {e}")
            return False
    
    async def activate_memory_reasoner(self):
        """Activate Loop 1: Memory Reasoner."""
        print("\n[1/6] Activating Memory Reasoner (Loop 1)...")
        start = datetime.now()
        
        try:
            from memory_reasoner import MemoryReasoner
            
            self.loops['memory_reasoner'] = MemoryReasoner(
                memory=self.memory,
                llm_client=self.llm_client,
                config={
                    "spreading_activation": {
                        "decay": 0.6,
                        "threshold": 0.1,
                        "max_hops": 3
                    }
                }
            )
            
            # Test with a query
            await self.loops['memory_reasoner'].query("test activation")
            
            duration = (datetime.now() - start).total_seconds()
            self.activation_times['memory_reasoner'] = duration
            print(f"      ✓ Memory Reasoner activated ({duration:.3f}s)")
            print(f"      - Uses spreading activation for graph reasoning")
            print(f"      - Can answer queries from memory patterns")
            
            # Emit activation event
            await event_bus.emit(Event(
                type=EventType.LOOP_CYCLE_START,
                data={"loop_name": "memory_reasoner", "action": "activation"}
            ))
            
            return True
        except ImportError:
            print(f"      ! Memory Reasoner module not found (skipping)")
            return False
        except Exception as e:
            print(f"      ✗ Failed: {e}")
            return False
    
    async def activate_self_compiler(self):
        """Activate Loop 2: Self-Compiler."""
        print("\n[2/6] Activating Self-Compiler (Loop 2)...")
        start = datetime.now()
        
        try:
            from accelerators import SelfCompiler
            
            self.loops['self_compiler'] = SelfCompiler(
                memory=self.memory,
                llm_client=self.llm_client,
                config={
                    "pattern_library": {
                        "min_similarity": 0.7,
                        "lifting_threshold": 3
                    }
                }
            )
            
            duration = (datetime.now() - start).total_seconds()
            self.activation_times['self_compiler'] = duration
            print(f"      ✓ Self-Compiler activated ({duration:.3f}s)")
            print(f"      - Learns patterns from successful solutions")
            print(f"      - Compounds: more patterns = more solutions")
            
            await event_bus.emit(Event(
                type=EventType.LOOP_CYCLE_START,
                data={"loop_name": "self_compiler", "action": "activation"}
            ))
            
            return True
        except ImportError:
            print(f"      ! Self-Compiler module not found (skipping)")
            return False
        except Exception as e:
            print(f"      ✗ Failed: {e}")
            return False
    
    async def activate_goal_evolver(self):
        """Activate Loop 3: Goal Evolver."""
        print("\n[3/6] Activating Goal Evolver (Loop 3)...")
        start = datetime.now()
        
        try:
            from goal_evolver import GoalEvolver
            
            self.loops['goal_evolver'] = GoalEvolver(
                memory=self.memory,
                llm_client=self.llm_client,
                config={
                    "population_size": 20,
                    "mutation_rate": 0.2,
                    "fitness_weights": {
                        "completion": 0.3,
                        "capability_delta": 0.5,
                        "efficiency": 0.2
                    }
                }
            )
            
            duration = (datetime.now() - start).total_seconds()
            self.activation_times['goal_evolver'] = duration
            print(f"      ✓ Goal Evolver activated ({duration:.3f}s)")
            print(f"      - Evolves goals using genetic algorithms")
            print(f"      - Fitness based on capability growth")
            
            await event_bus.emit(Event(
                type=EventType.LOOP_CYCLE_START,
                data={"loop_name": "goal_evolver", "action": "activation"}
            ))
            
            return True
        except ImportError:
            print(f"      ! Goal Evolver module not found (skipping)")
            return False
        except Exception as e:
            print(f"      ✗ Failed: {e}")
            return False
    
    async def activate_dreaming_machine(self):
        """Activate Loop 4: Dreaming Machine."""
        print("\n[4/6] Activating Dreaming Machine (Loop 4)...")
        start = datetime.now()
        
        try:
            from dreaming_machine import DreamingMachine
            
            self.loops['dreaming_machine'] = DreamingMachine(
                memory=self.memory,
                llm_client=self.llm_client,
                config={
                    "counterfactual": {
                        "enabled": True,
                        "variations_per_experience": 3
                    }
                }
            )
            
            duration = (datetime.now() - start).total_seconds()
            self.activation_times['dreaming_machine'] = duration
            print(f"      ✓ Dreaming Machine activated ({duration:.3f}s)")
            print(f"      - Multiplies experience through counterfactuals")
            print(f"      - Replays and transfers patterns across domains")
            
            await event_bus.emit(Event(
                type=EventType.LOOP_CYCLE_START,
                data={"loop_name": "dreaming_machine", "action": "activation"}
            ))
            
            return True
        except ImportError:
            print(f"      ! Dreaming Machine module not found (skipping)")
            return False
        except Exception as e:
            print(f"      ✗ Failed: {e}")
            return False
    
    async def activate_omega(self):
        """Activate Loop 5: Integration Mind (Omega)."""
        print("\n[5/6] Activating Omega - Integration Mind (Loop 5)...")
        start = datetime.now()
        
        try:
            from omega import BYRDOmega
            
            self.loops['omega'] = BYRDOmega(
                memory=self.memory,
                coupling_tracker=self.loops.get('coupling_tracker'),
                config={
                    "mode_durations": {"AWAKE": 60}
                }
            )
            
            # Inject other loops into Omega
            if 'memory_reasoner' in self.loops and self.loops['memory_reasoner']:
                self.loops['omega'].memory_reasoner = self.loops['memory_reasoner']
            if 'self_compiler' in self.loops and self.loops['self_compiler']:
                self.loops['omega'].self_compiler = self.loops['self_compiler']
            if 'goal_evolver' in self.loops and self.loops['goal_evolver']:
                self.loops['omega'].goal_evolver = self.loops['goal_evolver']
            if 'dreaming_machine' in self.loops and self.loops['dreaming_machine']:
                self.loops['omega'].dreaming_machine = self.loops['dreaming_machine']
            
            duration = (datetime.now() - start).total_seconds()
            self.activation_times['omega'] = duration
            print(f"      ✓ Omega activated ({duration:.3f}s)")
            print(f"      - Meta-orchestrator for all loops")
            print(f"      - Mode: {self.loops['omega']._mode.value}")
            print(f"      - Injected loops: {sum(1 for k in ['memory_reasoner', 'self_compiler', 'goal_evolver', 'dreaming_machine'] if self.loops.get(k))}/4")
            
            await event_bus.emit(Event(
                type=EventType.LOOP_CYCLE_START,
                data={"loop_name": "omega", "action": "activation"}
            ))
            
            return True
        except ImportError:
            print(f"      ! Omega module not found (skipping)")
            return False
        except Exception as e:
            print(f"      ✗ Failed: {e}")
            return False
    
    async def run_demo_cycles(self, num_cycles: int = 2):
        """Run demonstration cycles."""
        print("\n[6/6] Running demonstration cycles...")
        print(f"\n{'─'*70}")
        print(f"RUNNING {num_cycles} COORDINATED CYCLES")
        print(f"{'─'*70}")
        
        for cycle in range(1, num_cycles + 1):
            print(f"\n--- Cycle {cycle}/{num_cycles} ---")
            
            # Run Omega cycle
            if 'omega' in self.loops and self.loops['omega']:
                try:
                    print("  Running Omega cycle...")
                    result = await self.loops['omega'].run_cycle()
                    self.cycle_counts['omega'] = self.cycle_counts.get('omega', 0) + 1
                    print(f"    ✓ Omega cycle complete (mode: {result.get('mode', 'unknown')})")
                except Exception as e:
                    print(f"    ! Omega cycle: {e}")
            
            # Run Memory Reasoner
            if 'memory_reasoner' in self.loops and self.loops['memory_reasoner']:
                try:
                    await self.loops['memory_reasoner'].query(f"cycle {cycle} test query")
                    self.cycle_counts['memory_reasoner'] = self.cycle_counts.get('memory_reasoner', 0) + 1
                    print(f"    ✓ Memory Reasoner: query processed")
                except Exception as e:
                    print(f"    ! Memory Reasoner: {e}")
            
            # Emit coupling measurement
            if 'coupling_tracker' in self.loops and self.loops['coupling_tracker']:
                try:
                    await self.loops['coupling_tracker'].emit_coupling_event()
                    print(f"    ✓ Coupling measured")
                except Exception as e:
                    print(f"    ! Coupling tracker: {e}")
        
        print(f"\n{'─'*70}")
    
    async def measure_interactions(self):
        """Measure loop interactions."""
        print("\n\n" + "="*70)
        print("MEASURING LOOP INTERACTIONS")
        print("="*70)
        
        if 'coupling_tracker' not in self.loops or not self.loops['coupling_tracker']:
            print("\n! Coupling tracker not available - using simulated measurements")
            self._simulate_coupling_measurements()
            return
        
        tracker = self.loops['coupling_tracker']
        loops = list(tracker.LOOPS)
        
        print(f"\nMeasuring correlations between {len(loops)} loops...")
        print(f"\nLoop Pairs:")
        
        for i, loop_a in enumerate(loops):
            for loop_b in loops[i+1:]:
                try:
                    corr = await tracker.measure_correlation(loop_a, loop_b)
                    self.coupling_measurements[f"{loop_a}_{loop_b}"] = corr
                    
                    # Visual indicator
                    if abs(corr) >= 0.7:
                        symbol = "🔗 STRONG"
                    elif abs(corr) >= 0.4:
                        symbol = "🔗 MODERATE"
                    elif abs(corr) >= 0.2:
                        symbol = "🔗 WEAK"
                    else:
                        symbol = "○ NONE"
                    
                    print(f"  {symbol} {loop_a:20s} ↔ {loop_b:20s}: {corr:+.3f}")
                    
                except Exception as e:
                    print(f"  ! {loop_a} ↔ {loop_b}: {e}")
    
    def _simulate_coupling_measurements(self):
        """Simulate coupling measurements for demonstration."""
        print("\nSimulated coupling measurements:")
        
        # Simulated couplings demonstrating compounding
        simulations = [
            ("memory_reasoner", "self_compiler", 0.65, "Patterns from memory enable compilation"),
            ("memory_reasoner", "goal_evolver", 0.72, "Memory patterns guide goal fitness"),
            ("self_compiler", "goal_evolver", 0.81, "CRITICAL: Goals → Code → Capability"),
            ("goal_evolver", "dreaming_machine", 0.58, "High-fitness goals drive counterfactuals"),
            ("dreaming_machine", "memory_reasoner", 0.63, "Counterfactuals enrich memory"),
            ("omega", "memory_reasoner", 0.45, "Orchestration improves retrieval"),
            ("omega", "self_compiler", 0.52, "Orchestration improves pattern lifting"),
            ("omega", "goal_evolver", 0.48, "Orchestration improves evolution"),
            ("omega", "dreaming_machine", 0.41, "Orchestration improves dreaming"),
        ]
        
        for loop_a, loop_b, corr, reason in simulations:
            symbol = "🔗" if abs(corr) >= 0.5 else "○"
            self.coupling_measurements[f"{loop_a}_{loop_b}"] = corr
            print(f"  {symbol} {loop_a:20s} ↔ {loop_b:20s}: {corr:+.3f}")
            print(f"      {reason}")
    
    def print_summary(self):
        """Print activation and measurement summary."""
        print("\n\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        
        print("\nActivation Results:")
        for name, time in self.activation_times.items():
            status = "✓" if time > 0 else "✗"
            print(f"  {status} {name:25s} {time:6.3f}s")
        
        print(f"\nTotal loops activated: {len([t for t in self.activation_times.values() if t > 0])}")
        
        print("\nCycle Counts:")
        for name, count in self.cycle_counts.items():
            print(f"  • {name:25s}: {count} cycles")
        
        if self.coupling_measurements:
            significant = [c for c in self.coupling_measurements.values() if abs(c) >= 0.5]
            print(f"\nCoupling Analysis:")
            print(f"  • Total measurements: {len(self.coupling_measurements)}")
            print(f"  • Strong couplings (≥0.5): {len(significant)}")
            print(f"  • Overall compounding potential: {'HIGH' if len(significant) >= 4 else 'MODERATE' if len(significant) >= 2 else 'LOW'}")
        
        print("\n" + "="*70)
        print("DEMO COMPLETE")
        print("="*70 + "\n")


async def main():
    """Run the demonstration."""
    demo = CompoundingLoopsDemo()
    
    await demo.initialize()
    
    # Activate all loops
    await demo.activate_coupling_tracker()
    await demo.activate_memory_reasoner()
    await demo.activate_self_compiler()
    await demo.activate_goal_evolver()
    await demo.activate_dreaming_machine()
    await demo.activate_omega()
    
    # Run cycles
    await demo.run_demo_cycles(num_cycles=2)
    
    # Measure interactions
    await demo.measure_interactions()
    
    # Print summary
    demo.print_summary()


if __name__ == "__main__":
    asyncio.run(main())
