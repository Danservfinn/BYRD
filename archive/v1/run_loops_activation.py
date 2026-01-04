#!/usr/bin/env python3
"""
BYRD Five Compounding Loops - Standalone Activation Demo
========================================================

This script activates and demonstrates all 5 compounding loops in a
self-contained manner, showing how they form the engine for growth.

THE FIVE COMPOUNDING LOOPS:
---------------------------
1. Memory Reasoner (Loop 1) - Graph-based knowledge retrieval
2. Self-Compiler (Loop 2) - Pattern extraction and code synthesis  
3. Goal Evolver (Loop 3) - Genetic goal evolution for capability growth
4. Dreaming Machine (Loop 4) - Counterfactual experience multiplication
5. Integration Mind / Omega (Loop 5) - Meta-orchestrator and coupling

COMPOUNDING EFFECT:
-------------------
Loops compound when their outputs feed each other's inputs in positive
feedback cycles. This demo shows the acceleration pattern.
"""

import asyncio
import time
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import json

# =============================================================================
# DATA STRUCTURES
# =============================================================================

class LoopState(Enum):
    """State of a compounding loop."""
    IDLE = "idle"
    ACTIVE = "active"
    STAGNANT = "stagnant"
    ACCELERATING = "accelerating"

@dataclass
class LoopMetrics:
    """Metrics for a single loop."""
    cycles_completed: int = 0
    total_delta: float = 0.0
    avg_delta: float = 0.0
    current_state: LoopState = LoopState.IDLE
    last_delta: float = 0.0
    outputs_produced: List[Any] = field(default_factory=list)
    inputs_consumed: List[Any] = field(default_factory=list)
    stagnation_count: int = 0

class CouplingTracker:
    """Tracks coupling strength between loops."""
    
    def __init__(self):
        self.coupling_matrix: Dict[str, Dict[str, float]] = {}
        self.interaction_history: List[Dict] = []
    
    def record_interaction(self, source_loop: str, target_loop: str, strength: float):
        """Record an interaction between loops."""
        if source_loop not in self.coupling_matrix:
            self.coupling_matrix[source_loop] = {}
        self.coupling_matrix[source_loop][target_loop] = strength
        self.interaction_history.append({
            "source": source_loop,
            "target": target_loop,
            "strength": strength,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_coupling_strength(self, source_loop: str, target_loop: str) -> float:
        """Get coupling strength between two loops."""
        return self.coupling_matrix.get(source_loop, {}).get(target_loop, 0.0)
    
    def get_total_coupling(self) -> float:
        """Get total coupling across all loops."""
        total = 0.0
        for source, targets in self.coupling_matrix.items():
            total += sum(targets.values())
        return total

# =============================================================================
# LOOP 1: MEMORY REASONER
# =============================================================================

class MemoryReasoner:
    """
    Loop 1: Memory Reasoner
    
    Answers queries by spreading activation through memory graph.
    Compounds: More knowledge → better answers → better knowledge
    """
    
    def __init__(self):
        self.name = "memory_reasoner"
        self.knowledge_graph: Dict[str, List[str]] = {
            "learning": ["patterns", "experience", "improvement"],
            "patterns": ["code", "behavior", "solutions"],
            "experience": ["success", "failure", "data"],
            "improvement": ["capability", "efficiency", "growth"]
        }
        self.metrics = LoopMetrics()
    
    def activate(self):
        """Activate the loop."""
        self.metrics.current_state = LoopState.ACTIVE
        print(f"[{self.name.upper()}] ACTIVATED - Knowledge graph ready")
    
    def run_cycle(self, inputs: List[str]) -> Dict[str, Any]:
        """Run one reasoning cycle."""
        start = time.time()
        
        # Simulate spreading activation
        activated_nodes = []
        for query in inputs:
            if query in self.knowledge_graph:
                activated_nodes.extend(self.knowledge_graph[query])
                # Add related nodes
                for node in self.knowledge_graph[query]:
                    if node in self.knowledge_graph:
                        activated_nodes.extend(self.knowledge_graph[node][:1])
        
        # Calculate delta (growth from retrieving knowledge)
        delta = len(set(activated_nodes)) * 0.01
        
        self.metrics.cycles_completed += 1
        self.metrics.total_delta += delta
        self.metrics.avg_delta = self.metrics.total_delta / self.metrics.cycles_completed
        self.metrics.last_delta = delta
        self.metrics.inputs_consumed.extend(inputs)
        self.metrics.outputs_produced.append({"nodes": list(set(activated_nodes))})
        
        # Detect stagnation
        if delta < self.metrics.avg_delta * 0.5:
            self.metrics.stagnation_count += 1
            if self.metrics.stagnation_count > 3:
                self.metrics.current_state = LoopState.STAGNANT
        else:
            self.metrics.stagnation_count = 0
            if delta > self.metrics.avg_delta:
                self.metrics.current_state = LoopState.ACCELERATING
        
        duration = time.time() - start
        
        return {
            "loop": self.name,
            "delta": delta,
            "activated_nodes": list(set(activated_nodes)),
            "duration": duration
        }

# =============================================================================
# LOOP 2: SELF-COMPILER
# =============================================================================

class SelfCompiler:
    """
    Loop 2: Self-Compiler
    
    Extracts patterns from successful solutions and compiles them.
    Compounds: More patterns → more solutions → more patterns
    """
    
    def __init__(self):
        self.name = "self_compiler"
        self.pattern_library: Dict[str, Any] = {}
        self.metrics = LoopMetrics()
    
    def activate(self):
        """Activate the loop."""
        self.metrics.current_state = LoopState.ACTIVE
        print(f"[{self.name.upper()}] ACTIVATED - Pattern library ready")
    
    def run_cycle(self, inputs: List[str]) -> Dict[str, Any]:
        """Run one compilation cycle."""
        start = time.time()
        
        # Extract new patterns from inputs
        new_patterns = []
        for experience in inputs:
            # Simulate pattern extraction
            if len(experience) > 3:
                pattern_name = f"pattern_{hash(experience) % 1000}"
                new_patterns.append({
                    "name": pattern_name,
                    "source": experience,
                    "confidence": random.uniform(0.5, 1.0)
                })
        
        # Add to library
        for pattern in new_patterns:
            self.pattern_library[pattern["name"]] = pattern
        
        # Calculate delta (growth from new patterns)
        delta = len(new_patterns) * 0.02
        
        self.metrics.cycles_completed += 1
        self.metrics.total_delta += delta
        self.metrics.avg_delta = self.metrics.total_delta / self.metrics.cycles_completed
        self.metrics.last_delta = delta
        self.metrics.inputs_consumed.extend(inputs)
        self.metrics.outputs_produced.append({"patterns": new_patterns})
        
        # Detect stagnation
        if delta < self.metrics.avg_delta * 0.5:
            self.metrics.stagnation_count += 1
            if self.metrics.stagnation_count > 3:
                self.metrics.current_state = LoopState.STAGNANT
        else:
            self.metrics.stagnation_count = 0
            if delta > self.metrics.avg_delta:
                self.metrics.current_state = LoopState.ACCELERATING
        
        duration = time.time() - start
        
        return {
            "loop": self.name,
            "delta": delta,
            "new_patterns": len(new_patterns),
            "total_patterns": len(self.pattern_library),
            "duration": duration
        }

# =============================================================================
# LOOP 3: GOAL EVOLVER
# =============================================================================

class GoalEvolver:
    """
    Loop 3: Goal Evolver
    
    Evolves goals using genetic algorithms based on capability growth.
    Compounds: Better goals → more capability growth → better goals
    """
    
    def __init__(self):
        self.name = "goal_evolver"
        self.population: List[Dict[str, Any]] = [
            {"id": 0, "description": "Learn faster", "fitness": 0.5},
            {"id": 1, "description": "Improve accuracy", "fitness": 0.6},
            {"id": 2, "description": "Reduce errors", "fitness": 0.4},
            {"id": 3, "description": "Generate novel solutions", "fitness": 0.7}
        ]
        self.metrics = LoopMetrics()
    
    def activate(self):
        """Activate the loop."""
        self.metrics.current_state = LoopState.ACTIVE
        print(f"[{self.name.upper()}] ACTIVATED - Population ready")
    
    def run_cycle(self, inputs: List[str]) -> Dict[str, Any]:
        """Run one evolution cycle."""
        start = time.time()
        
        # Update fitness based on inputs (capability signals)
        for goal in self.population:
            # Fitness improves when goals align with capability growth
            improvement_signal = len(inputs) * 0.1
            goal["fitness"] = min(0.99, goal["fitness"] + improvement_signal * random.random())
        
        # Selection: keep top performers
        self.population.sort(key=lambda g: g["fitness"], reverse=True)
        survivors = self.population[:len(self.population)//2 + 1]
        
        # Crossover: create new goals from parents
        new_goals = []
        for i in range(0, len(survivors) - 1, 2):
            parent1, parent2 = survivors[i], survivors[i+1]
            child_fitness = (parent1["fitness"] + parent2["fitness"]) / 2
            child = {
                "id": len(self.population) + len(new_goals),
                "description": f"Evolved from {parent1['id']} & {parent2['id']}",
                "fitness": child_fitness
            }
            new_goals.append(child)
        
        # Mutation: randomly modify some goals
        for goal in new_goals:
            if random.random() < 0.2:  # 20% mutation rate
                goal["fitness"] *= random.uniform(0.9, 1.1)
                goal["fitness"] = min(0.99, max(0.1, goal["fitness"]))
        
        # Update population
        self.population = survivors + new_goals
        
        # Calculate delta (growth from evolved goals)
        avg_fitness = sum(g["fitness"] for g in self.population) / len(self.population)
        delta = (avg_fitness - 0.5) * 0.1
        
        self.metrics.cycles_completed += 1
        self.metrics.total_delta += delta
        self.metrics.avg_delta = self.metrics.total_delta / self.metrics.cycles_completed
        self.metrics.last_delta = delta
        self.metrics.inputs_consumed.extend(inputs)
        self.metrics.outputs_produced.append({"goals": self.population.copy()})
        
        # Detect stagnation
        if delta < self.metrics.avg_delta * 0.5:
            self.metrics.stagnation_count += 1
            if self.metrics.stagnation_count > 3:
                self.metrics.current_state = LoopState.STAGNANT
        else:
            self.metrics.stagnation_count = 0
            if delta > self.metrics.avg_delta:
                self.metrics.current_state = LoopState.ACCELERATING
        
        duration = time.time() - start
        
        return {
            "loop": self.name,
            "delta": delta,
            "avg_fitness": avg_fitness,
            "population_size": len(self.population),
            "duration": duration
        }

# =============================================================================
# LOOP 4: DREAMING MACHINE
# =============================================================================

class DreamingMachine:
    """
    Loop 4: Dreaming Machine
    
    Multiplies experience through counterfactual simulation.
    Compounds: More experiences → more simulations → more learning
    """
    
    def __init__(self):
        self.name = "dreaming_machine"
        self.experience_bank: List[Dict[str, Any]] = []
        self.metrics = LoopMetrics()
    
    def activate(self):
        """Activate the loop."""
        self.metrics.current_state = LoopState.ACTIVE
        print(f"[{self.name.upper()}] ACTIVATED - Dream engine ready")
    
    def run_cycle(self, inputs: List[str]) -> Dict[str, Any]:
        """Run one dreaming cycle."""
        start = time.time()
        
        # Add real experiences to bank
        for experience in inputs:
            self.experience_bank.append({
                "content": experience,
                "type": "real",
                "timestamp": datetime.now().isoformat()
            })
        
        # Generate counterfactuals (dreams)
        counterfactuals = []
        num_dreams = min(len(self.experience_bank), 5)
        
        for _ in range(num_dreams):
            if self.experience_bank:
                base_exp = random.choice(self.experience_bank)
                # Create variation
                dream = {
                    "content": f"What if {base_exp['content']} differently?",
                    "type": "counterfactual",
                    "source": base_exp["content"],
                    "timestamp": datetime.now().isoformat()
                }
                counterfactuals.append(dream)
                self.experience_bank.append(dream)
        
        # Calculate delta (growth from multiplied experiences)
        delta = len(counterfactuals) * 0.015
        
        self.metrics.cycles_completed += 1
        self.metrics.total_delta += delta
        self.metrics.avg_delta = self.metrics.total_delta / self.metrics.cycles_completed
        self.metrics.last_delta = delta
        self.metrics.inputs_consumed.extend(inputs)
        self.metrics.outputs_produced.append({"dreams": counterfactuals})
        
        # Detect stagnation
        if delta < self.metrics.avg_delta * 0.5:
            self.metrics.stagnation_count += 1
            if self.metrics.stagnation_count > 3:
                self.metrics.current_state = LoopState.STAGNANT
        else:
            self.metrics.stagnation_count = 0
            if delta > self.metrics.avg_delta:
                self.metrics.current_state = LoopState.ACCELERATING
        
        duration = time.time() - start
        
        return {
            "loop": self.name,
            "delta": delta,
            "dreams_generated": len(counterfactuals),
            "total_experiences": len(self.experience_bank),
            "duration": duration
        }

# =============================================================================
# LOOP 5: OMEGA (INTEGRATION MIND)
# =============================================================================

class BYRDOmega:
    """
    Loop 5: Omega / Integration Mind
    
    Meta-orchestrator that coordinates all loops and measures coupling.
    Critical metric: Goal Evolver → Self-Compiler coupling strength
    """
    
    def __init__(self):
        self.name = "omega"
        self.operating_mode = "coordinate"
        self.metrics = LoopMetrics()
        self.coupling_tracker = CouplingTracker()
        
    def activate(self):
        """Activate the loop."""
        self.metrics.current_state = LoopState.ACTIVE
        print(f"[{self.name.upper()}] ACTIVATED - Integration mind ready")
    
    def run_cycle(self, loop_outputs: Dict[str, Dict]) -> Dict[str, Any]:
        """Run one orchestration cycle."""
        start = time.time()
        
        total_delta = 0.0
        
        # Calculate coupling between loops
        for loop_name, output in loop_outputs.items():
            if "delta" in output:
                total_delta += output["delta"]
        
        # Feed outputs as inputs to other loops (coupling)
        coupling_strength = 0.0
        
        # Critical coupling: Goal Evolver → Self-Compiler
        if "goal_evolver" in loop_outputs and "self_compiler" in loop_outputs:
            # When goals drive code changes, we have true acceleration
            ge_delta = loop_outputs["goal_evolver"].get("delta", 0)
            sc_delta = loop_outputs["self_compiler"].get("delta", 0)
            
            # Coupling strength = product of deltas (both need to be strong)
            coupling = ge_delta * sc_delta * 10  # Scale for visibility
            self.coupling_tracker.record_interaction("goal_evolver", "self_compiler", coupling)
            coupling_strength += coupling
        
        # Other couplings
        if "memory_reasoner" in loop_outputs and "dreaming_machine" in loop_outputs:
            coupling = loop_outputs["memory_reasoner"].get("delta", 0) * 0.5
            self.coupling_tracker.record_interaction("memory_reasoner", "dreaming_machine", coupling)
            coupling_strength += coupling
        
        if "dreaming_machine" in loop_outputs and "self_compiler" in loop_outputs:
            coupling = loop_outputs["dreaming_machine"].get("delta", 0) * 0.3
            self.coupling_tracker.record_interaction("dreaming_machine", "self_compiler", coupling)
            coupling_strength += coupling
        
        # Calculate delta from orchestration
        delta = total_delta * 0.1 + coupling_strength * 0.05
        
        self.metrics.cycles_completed += 1
        self.metrics.total_delta += delta
        self.metrics.avg_delta = self.metrics.total_delta / self.metrics.cycles_completed
        self.metrics.last_delta = delta
        self.metrics.inputs_consumed.extend([str(o) for o in loop_outputs.values()])
        self.metrics.outputs_produced.append({"coordination": True})
        
        # Adjust operating mode based on coupling strength
        if coupling_strength > 0.1:
            self.operating_mode = "accelerate"
        elif coupling_strength > 0.05:
            self.operating_mode = "coordinate"
        else:
            self.operating_mode = "stabilize"
        
        # Detect stagnation
        if delta < self.metrics.avg_delta * 0.5:
            self.metrics.stagnation_count += 1
            if self.metrics.stagnation_count > 3:
                self.metrics.current_state = LoopState.STAGNANT
        else:
            self.metrics.stagnation_count = 0
            if delta > self.metrics.avg_delta:
                self.metrics.current_state = LoopState.ACCELERATING
        
        duration = time.time() - start
        
        return {
            "loop": self.name,
            "delta": delta,
            "coupling_strength": coupling_strength,
            "operating_mode": self.operating_mode,
            "duration": duration
        }

# =============================================================================
# COMPOUNDING LOOPS ACTIVATOR
# =============================================================================

class CompoundingLoopsActivator:
    """
    Main activator for all 5 compounding loops.
    Demonstrates the compounding effect through coordinated cycles.
    """
    
    def __init__(self):
        self.loops = {
            "memory_reasoner": MemoryReasoner(),
            "self_compiler": SelfCompiler(),
            "goal_evolver": GoalEvolver(),
            "dreaming_machine": DreamingMachine(),
            "omega": BYRDOmega()
        }
        self.omega = self.loops["omega"]
        self.activation_results = {}
        self.cycle_history = []
    
    def activate_all_loops(self):
        """Activate all 5 compounding loops."""
        print("\n" + "=" * 70)
        print("BYRD FIVE COMPOUNDING LOOPS - ACTIVATION")
        print("=" * 70)
        print()
        
        for name, loop in self.loops.items():
            loop.activate()
            self.activation_results[name] = True
        
        print()
        print("All loops activated. Ready for compounding cycles.")
        print()
    
    def run_cycles(self, num_cycles: int = 5):
        """Run coordinated cycles across all loops."""
        print("\n" + "=" * 70)
        print(f"RUNNING {num_cycles} COMPOUNDING CYCLES")
        print("=" * 70)
        print()
        
        for cycle_num in range(1, num_cycles + 1):
            print(f"\n--- CYCLE {cycle_num} ---")
            
            # Generate initial inputs for the cycle
            base_inputs = [f"experience_{cycle_num}_{i}" for i in range(3)]
            
            # Run each loop
            loop_outputs = {}
            
            # Loop 1: Memory Reasoner
            output = self.loops["memory_reasoner"].run_cycle(base_inputs)
            loop_outputs["memory_reasoner"] = output
            print(f"  [Loop 1] Memory Reasoner: Δ={output['delta']:.4f}, nodes={len(output['activated_nodes'])}")
            
            # Loop 2: Self-Compiler (uses outputs from memory and goals)
            sc_inputs = base_inputs + [f"goal_{cycle_num}"]
            output = self.loops["self_compiler"].run_cycle(sc_inputs)
            loop_outputs["self_compiler"] = output
            print(f"  [Loop 2] Self-Compiler: Δ={output['delta']:.4f}, patterns={output['new_patterns']}")
            
            # Loop 3: Goal Evolver
            output = self.loops["goal_evolver"].run_cycle(base_inputs)
            loop_outputs["goal_evolver"] = output
            print(f"  [Loop 3] Goal Evolver: Δ={output['delta']:.4f}, fitness={output['avg_fitness']:.3f}")
            
            # Loop 4: Dreaming Machine (uses all experiences)
            dm_inputs = base_inputs + [f"reflection_{cycle_num}"]
            output = self.loops["dreaming_machine"].run_cycle(dm_inputs)
            loop_outputs["dreaming_machine"] = output
            print(f"  [Loop 4] Dreaming Machine: Δ={output['delta']:.4f}, dreams={output['dreams_generated']}")
            
            # Loop 5: Omega (orchestrates and measures coupling)
            output = self.omega.run_cycle(loop_outputs)
            loop_outputs["omega"] = output
            print(f"  [Loop 5] Omega: Δ={output['delta']:.4f}, coupling={output['coupling_strength']:.4f}")
            print(f"             Operating Mode: {output['operating_mode'].upper()}")
            
            self.cycle_history.append({
                "cycle": cycle_num,
                "outputs": loop_outputs,
                "total_delta": sum(o.get('delta', 0) for o in loop_outputs.values())
            })
            
            # Show acceleration indicator
            cycle_delta = self.cycle_history[-1]["total_delta"]
            if cycle_num > 1:
                prev_delta = self.cycle_history[-2]["total_delta"]
                growth = ((cycle_delta - prev_delta) / prev_delta * 100) if prev_delta > 0 else 0
                if growth > 0:
                    print(f"  >>> COMPOUNDING GROWTH: +{growth:.1f}%")
                elif growth < 0:
                    print(f"  <<< DECELERATION: {growth:.1f}%")
        
        print()
    
    def measure_coupling(self):
        """Measure and display coupling between loops."""
        print("\n" + "=" * 70)
        print("LOOP COUPLING ANALYSIS")
        print("=" * 70)
        print()
        
        coupling_matrix = self.omega.coupling_tracker
        
        # Display coupling matrix
        print("Coupling Strength Matrix:")
        print("-" * 50)
        for source, targets in coupling_matrix.coupling_matrix.items():
            for target, strength in targets.items():
                print(f"  {source:20s} → {target:20s} : {strength:.4f}")
        
        total_coupling = coupling_matrix.get_total_coupling()
        print(f"\nTotal System Coupling: {total_coupling:.4f}")
        
        # Critical coupling metric
        critical_coupling = coupling_matrix.get_coupling_strength("goal_evolver", "self_compiler")
        print(f"\nCRITICAL COUPLING (Goal Evolver → Self-Compiler): {critical_coupling:.4f}")
        
        if critical_coupling > 0.1:
            print(">>> STRONG COMPOUNDING: Goals are driving capability growth!")
        elif critical_coupling > 0.05:
            print(">> MODERATE COMPOUNDING: Loops are interacting productively.")
        else:
            print("> WEAK COMPOUNDING: Loops need stronger integration.")
        
        print()
    
    def print_summary(self):
        """Print summary of loop performance."""
        print("\n" + "=" * 70)
        print("PERFORMANCE SUMMARY")
        print("=" * 70)
        print()
        
        for name, loop in self.loops.items():
            m = loop.metrics
            state_emoji = {
                LoopState.IDLE: "⏸️",
                LoopState.ACTIVE: "✅",
                LoopState.STAGNANT: "⚠️",
                LoopState.ACCELERATING: "🚀"
            }[m.current_state]
            
            print(f"{state_emoji} {name.upper()}")
            print(f"   Cycles: {m.cycles_completed}")
            print(f"   Total Δ: {m.total_delta:.4f}")
            print(f"   Avg Δ:   {m.avg_delta:.4f}")
            print(f"   State:   {m.current_state.value}")
            print()
        
        # Overall system health
        total_system_delta = sum(l.metrics.total_delta for l in self.loops.values())
        print(f"TOTAL SYSTEM GROWTH: {total_system_delta:.4f}")
        print()

# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main():
    """Main entry point for loop activation."""
    num_cycles = 5
    
    print("\n")
    print("█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + "  " * 20 + "BYRD GROWTH ENGINE" + "  " * 28 + "█")
    print("█" + " " * 68 + "█")
    print("█" + "  Five Compounding Loops - The Engine for Growth" + " " * 14 + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)
    print()
    
    # Create activator
    activator = CompoundingLoopsActivator()
    
    # Activate all loops
    activator.activate_all_loops()
    
    # Run compounding cycles
    activator.run_cycles(num_cycles)
    
    # Measure coupling
    activator.measure_coupling()
    
    # Print summary
    activator.print_summary()
    
    print("\n" + "█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + "  " * 20 + "ACTIVATION COMPLETE" + "  " * 29 + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)
    print()\n
if __name__ == "__main__":
    main()
