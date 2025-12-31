#!/usr/bin/env python3
"""
BYRD AGI Improvement Cycle Implementation

This module implements the 8-step improvement cycle:
ASSESS → IDENTIFY → GENERATE → PREDICT → VERIFY → EXECUTE → MEASURE → LEARN

The cycle breaks the analysis-action loop by ensuring each step produces
concrete outputs that drive the next step forward, with no opportunity for
infinite reflection without action.

INTEGRATED WITH LOOP INSTRUMENTATION:
- Tracks cycles over time to detect zero-delta loops
- Monitors stagnation patterns
- Triggers interventions when improvement stalls
- Prevents false-positive success loops
"""

import asyncio
import json
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from datetime import datetime

# Import loop instrumentation to break zero-delta loops
LoopInstrumenter = None
CycleMetrics = None
LoopState = None
HAS_INSTRUMENTATION = False
try:
    from loop_instrumentation import LoopInstrumenter, CycleMetrics, LoopState
    HAS_INSTRUMENTATION = True
    print("[INFO] Loop instrumentation enabled - zero-delta detection active")
except ImportError as e:
    print(f"[WARNING] loop_instrumentation not available - zero-delta detection disabled: {e}")


class CyclePhase(Enum):
    """The 8 phases of the AGI improvement cycle."""
    ASSESS = "assess"
    IDENTIFY = "identify"
    GENERATE = "generate"
    PREDICT = "predict"
    VERIFY = "verify"
    EXECUTE = "execute"
    MEASURE = "measure"
    LEARN = "learn"


@dataclass
class CycleState:
    """State tracking for a single improvement cycle."""
    cycle_id: str
    start_time: datetime
    current_phase: CyclePhase
    assessments: Dict[str, Any] = field(default_factory=dict)
    opportunities: List[Dict[str, Any]] = field(default_factory=list)
    solutions: List[Dict[str, Any]] = field(default_factory=list)
    predictions: Dict[str, float] = field(default_factory=dict)
    verification_results: Dict[str, bool] = field(default_factory=dict)
    execution_results: Dict[str, Any] = field(default_factory=dict)
    baseline_measurements: Dict[str, float] = field(default_factory=dict)
    measurements: Dict[str, float] = field(default_factory=dict)
    delta_measurements: Dict[str, float] = field(default_factory=dict)
    learnings: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary for logging/persistence."""
        return {
            "cycle_id": self.cycle_id,
            "start_time": self.start_time.isoformat(),
            "current_phase": self.current_phase.value,
            "assessments": self.assessments,
            "opportunities": self.opportunities,
            "solutions": self.solutions,
            "predictions": self.predictions,
            "verification_results": self.verification_results,
            "execution_results": self.execution_results,
            "baseline_measurements": self.baseline_measurements,
            "measurements": self.measurements,
            "delta_measurements": self.delta_measurements,
            "learnings": self.learnings,
            "errors": self.errors
        }


class AGIImprovementCycle:
    """
    The 8-step AGI improvement cycle that breaks analysis-action loops.
    
    Key design principle: Each phase MUST produce concrete output before
    proceeding. No phase can return to previous phases. Forward momentum
    is guaranteed by design.
    """
    
    def __init__(self, 
                 assess_fn: Callable,
                 identify_fn: Callable,
                 generate_fn: Callable,
                 predict_fn: Callable,
                 verify_fn: Callable,
                 execute_fn: Callable,
                 measure_fn: Callable,
                 learn_fn: Callable):
        """
        Initialize the improvement cycle with phase-specific functions.
        
        Args:
            assess_fn: Function to assess current state
            identify_fn: Function to identify improvement opportunities
            generate_fn: Function to generate solution approaches
            predict_fn: Function to predict outcomes
            verify_fn: Function to verify predictions
            execute_fn: Function to execute solutions
            measure_fn: Function to measure results
            learn_fn: Function to learn from results
        """
        self.assess_fn = assess_fn
        self.identify_fn = identify_fn
        self.generate_fn = generate_fn
        self.predict_fn = predict_fn
        self.verify_fn = verify_fn
        self.execute_fn = execute_fn
        self.measure_fn = measure_fn
        self.learn_fn = learn_fn
        
        self.cycle_history: List[CycleState] = []
        self.current_state: Optional[CycleState] = None
        
        # Initialize loop instrumentation to break zero-delta loops
        self.instrumenter: Optional['LoopInstrumenter'] = None
        self.loop_name: str = "agi_improvement_cycle"
        if HAS_INSTRUMENTATION:
            self.instrumenter = LoopInstrumenter()
            self.instrumenter.register_loop(self.loop_name)
            print(f"[INSTRUMENTATION] Registered loop '{self.loop_name}' for zero-delta detection")
    
    def _create_cycle_id(self) -> str:
        """Generate unique cycle identifier."""
        return f"cycle_{int(time.time() * 1000)}"
    
    async def run_cycle(self) -> CycleState:
        """
        Execute complete 8-step improvement cycle.
        
        Returns:
            CycleState: Complete state after all phases
            
        Raises:
            Exception: If any phase fails critically
        """
        cycle_id = self._create_cycle_id()
        state = CycleState(
            cycle_id=cycle_id,
            start_time=datetime.now(),
            current_phase=CyclePhase.ASSESS
        )
        self.current_state = state
        
        try:
            # Phase 1: ASSESS
            await self._phase_assess(state)
            
            # Phase 2: IDENTIFY
            await self._phase_identify(state)
            
            # Phase 3: GENERATE
            await self._phase_generate(state)
            
            # Phase 4: PREDICT
            await self._phase_predict(state)
            
            # Phase 5: VERIFY
            await self._phase_verify(state)
            
            # Phase 6: EXECUTE
            await self._phase_execute(state)
            
            # Phase 7: MEASURE
            await self._phase_measure(state)
            
            # Phase 8: LEARN
            await self._phase_learn(state)
            
            # Cycle complete
            state.current_phase = CyclePhase.LEARN  # Final phase
            self.cycle_history.append(state)
            
            # INTEGRATION WITH LOOP INSTRUMENTATION
            # Record cycle metrics to break zero-delta loops
            if self.instrumenter and HAS_INSTRUMENTATION:
                self._record_cycle_with_instrumentation(state)
                
                # Check for stagnation and trigger intervention if needed
                if self.instrumenter.is_stagnant(self.loop_name):
                    stagnation_analysis = self.instrumenter.analyze_stagnation(self.loop_name)
                    state.errors.append(
                        f"[INSTRUMENTATION] Stagnation detected: {stagnation_analysis}"
                    )
                    # Note: Intervention strategies should be handled by calling code
                    # We record the detection here
            
        except Exception as e:
            state.errors.append(f"Critical failure in {state.current_phase.value}: {str(e)}")
            raise
        
        return state
    
    def _record_cycle_with_instrumentation(self, state: CycleState) -> None:
        """
        Record completed cycle metrics with loop instrumenter.
        
        This breaks the zero-delta loop by tracking:
        - Overall delta from baseline
        - Success/failure based on positive delta
        - Duration of the cycle
        - Whether the improvement was meaningful
        """
        # Guard: Only proceed if instrumentation is available
        if not HAS_INSTRUMENTATION or not self.instrumenter or CycleMetrics is None:
            return
        
        # Calculate overall delta as average of all delta measurements
        if state.delta_measurements:
            overall_delta = sum(state.delta_measurements.values()) / len(state.delta_measurements)
        else:
            overall_delta = 0.0
        
        # Determine success based on positive delta
        has_positive_delta = any(d > 0 for d in state.delta_measurements.values())
        
        # Calculate duration
        cycle_duration = (datetime.now() - state.start_time).total_seconds()
        
        # Determine if improvement was meaningful (delta >= 0.5%)
        MIN_MEANINGFUL_DELTA = 0.005  # 0.5% improvement
        is_meaningful = overall_delta >= MIN_MEANINGFUL_DELTA
        
        # Record with instrumenter using individual parameters
        # (record_cycle expects delta, success, duration_seconds separately, not a CycleMetrics object)
        self.instrumenter.record_cycle(
            loop_name=self.loop_name,
            delta=overall_delta,
            success=has_positive_delta,
            duration_seconds=cycle_duration,
            error=state.errors[-1] if state.errors else None
        )
        
        # Log instrumentation data
        print(f"[INSTRUMENTATION] Cycle {len(self.cycle_history)} recorded: "
              f"delta={overall_delta:.4f}, success={has_positive_delta}, "
              f"meaningful={is_meaningful}")
        
        # Get current loop state from the loops dictionary
        if self.loop_name in self.instrumenter.loops:
            loop_profile = self.instrumenter.loops[self.loop_name]
            print(f"[INSTRUMENTATION] Loop state: {loop_profile.current_state.value}, "
                  f"success_rate={loop_profile.success_rate:.2%}, "
                  f"meaningful_rate={loop_profile.meaningful_rate:.2%}")
    
    async def _phase_assess(self, state: CycleState) -> None:
        """
        Phase 1: ASSESS - Evaluate current system state.
        
        Output: Complete assessment of capabilities, performance, and gaps.
        Must be concrete and complete before proceeding.
        
        CRITICAL: Establishes baseline measurements for delta calculation.
        All strategies must demonstrate positive delta to be considered successful.
        """
        state.current_phase = CyclePhase.ASSESS
        
        # Execute assessment function
        result = await self._execute_phase_function(
            self.assess_fn, 
            "assess",
            state.cycle_id
        )
        
        # Validate we got concrete output
        if not isinstance(result, dict):
            raise ValueError("ASSESS phase must return dictionary")
        
        state.assessments = result
        
        # Extract baseline measurements from assessment for delta calculation
        # Look for performance metrics in assessments
        if "performance" in result and isinstance(result["performance"], dict):
            state.baseline_measurements = {
                k: v for k, v in result["performance"].items()
                if isinstance(v, (int, float))
            }
        elif "metrics" in result and isinstance(result["metrics"], dict):
            state.baseline_measurements = {
                k: v for k, v in result["metrics"].items()
                if isinstance(v, (int, float))
            }
        else:
            # Extract any numeric values as baseline
            state.baseline_measurements = {
                k: v for k, v in result.items()
                if isinstance(v, (int, float))
            }
        
        if not state.baseline_measurements:
            raise ValueError("ASSESS phase must provide at least one numeric baseline measurement")
    
    async def _phase_identify(self, state: CycleState) -> None:
        """
        Phase 2: IDENTIFY - Find improvement opportunities.
        
        Output: Prioritized list of improvement opportunities.
        No revisiting assessment - must work with what was found.
        """
        state.current_phase = CyclePhase.IDENTIFY
        
        result = await self._execute_phase_function(
            self.identify_fn,
            "identify",
            state.assessments
        )
        
        if not isinstance(result, list):
            raise ValueError("IDENTIFY phase must return list")
        
        if len(result) == 0:
            raise ValueError("IDENTIFY phase must find at least one opportunity")
        
        state.opportunities = result
    
    async def _phase_generate(self, state: CycleState) -> None:
        """
        Phase 3: GENERATE - Create solution approaches.
        
        Output: Concrete solution proposals for top opportunities.
        No revisiting identification - must generate for what was found.
        """
        state.current_phase = CyclePhase.GENERATE
        
        result = await self._execute_phase_function(
            self.generate_fn,
            "generate",
            state.opportunities
        )
        
        if not isinstance(result, list):
            raise ValueError("GENERATE phase must return list")
        
        if len(result) == 0:
            raise ValueError("GENERATE phase must produce at least one solution")
        
        state.solutions = result
    
    async def _phase_predict(self, state: CycleState) -> None:
        """
        Phase 4: PREDICT - Forecast solution outcomes.
        
        Output: Quantitative predictions for each solution.
        Must be numeric predictions - no hedging.
        """
        state.current_phase = CyclePhase.PREDICT
        
        result = await self._execute_phase_function(
            self.predict_fn,
            "predict",
            state.solutions
        )
        
        if not isinstance(result, dict):
            raise ValueError("PREDICT phase must return dictionary")
        
        # Ensure all values are numeric
        for key, value in result.items():
            if not isinstance(value, (int, float)):
                raise ValueError(f"PREDICT value for {key} must be numeric")
        
        state.predictions = result
    
    async def _phase_verify(self, state: CycleState) -> None:
        """
        Phase 5: VERIFY - Validate predictions.
        
        Output: Boolean verification of prediction feasibility.
        Must approve at least one solution for execution.
        """
        state.current_phase = CyclePhase.VERIFY
        
        result = await self._execute_phase_function(
            self.verify_fn,
            "verify",
            {
                "solutions": state.solutions,
                "predictions": state.predictions
            }
        )
        
        if not isinstance(result, dict):
            raise ValueError("VERIFY phase must return dictionary")
        
        # Ensure at least one solution is verified
        if not any(result.values()):
            raise ValueError("VERIFY phase must approve at least one solution")
        
        state.verification_results = result
    
    async def _phase_execute(self, state: CycleState) -> None:
        """
        Phase 6: EXECUTE - Implement verified solutions.
        
        Output: Actual execution results - changes made, code deployed.
        This is the ACTION phase - no more analysis, just execution.
        """
        state.current_phase = CyclePhase.EXECUTE
        
        # Get verified solutions
        verified_solutions = [
            sol for sol, verified in zip(state.solutions, state.verification_results.values())
            if verified
        ]
        
        result = await self._execute_phase_function(
            self.execute_fn,
            "execute",
            verified_solutions
        )
        
        if not isinstance(result, dict):
            raise ValueError("EXECUTE phase must return dictionary")
        
        if len(result) == 0:
            raise ValueError("EXECUTE phase must produce some output")
        
        state.execution_results = result
    
    async def _phase_measure(self, state: CycleState) -> None:
        """
        Phase 7: MEASURE - Quantify actual outcomes.
        
        Output: Ground-truth measurements of execution impact.
        Objective comparison against predictions.
        
        CRITICAL: Calculates delta measurements (actual - baseline).
        Strategies with non-positive deltas are FAILURES regardless of predictions.
        This breaks the false-positive success loop.
        """
        state.current_phase = CyclePhase.MEASURE
        
        result = await self._execute_phase_function(
            self.measure_fn,
            "measure",
            state.execution_results
        )
        
        if not isinstance(result, dict):
            raise ValueError("MEASURE phase must return dictionary")
        
        # Ensure measurements are numeric
        for key, value in result.items():
            if not isinstance(value, (int, float)):
                raise ValueError(f"MEASURE value for {key} must be numeric")
        
        state.measurements = result
        
        # CRITICAL: Calculate delta measurements
        # Delta = Post-execution measurement - Baseline measurement
        state.delta_measurements = {}
        
        for metric_name, post_value in result.items():
            if metric_name in state.baseline_measurements:
                baseline_value = state.baseline_measurements[metric_name]
                delta = post_value - baseline_value
                state.delta_measurements[metric_name] = delta
            else:
                # No baseline for this metric - cannot calculate delta
                # This is a warning, not an error
                state.errors.append(
                    f"WARNING: No baseline measurement for metric '{metric_name}'. "
                    f"Cannot calculate delta."
                )
        
        if not state.delta_measurements:
            raise ValueError(
                "MEASURE phase failed: No delta measurements could be calculated. "
                "At least one measured metric must have a corresponding baseline."
            )
        
        # CRITICAL: Validate that at least one metric shows positive delta
        # This breaks the false-positive loop - you cannot claim success without improvement
        has_positive_delta = any(d > 0 for d in state.delta_measurements.values())
        
        if not has_positive_delta:
            # All deltas are zero or negative - FAILURE
            state.errors.append(
                "CRITICAL: MEASURE phase detected no positive deltas. "
                "All strategies failed to improve over baseline. "
                f"Deltas: {state.delta_measurements}"
            )
            # We don't raise an exception here - we let the LEARN phase handle it
            # But we mark it clearly as a failure
    
    async def _phase_learn(self, state: CycleState) -> None:
        """
        Phase 8: LEARN - Extract insights for next cycle.
        
        Output: Learnings that improve future cycles.
        Compare predictions vs measurements, update models.
        
        CRITICAL: Learns from delta measurements. Success is determined by
        positive delta, not by meeting predictions. Strategies that fail to
        improve over baseline must be abandoned regardless of how "predicted"
        they were.
        """
        state.current_phase = CyclePhase.LEARN
        
        result = await self._execute_phase_function(
            self.learn_fn,
            "learn",
            {
                "predictions": state.predictions,
                "baseline_measurements": state.baseline_measurements,
                "measurements": state.measurements,
                "delta_measurements": state.delta_measurements,
                "execution_results": state.execution_results,
                "success": any(d > 0 for d in state.delta_measurements.values())
            }
        )
        
        if not isinstance(result, dict):
            raise ValueError("LEARN phase must return dictionary")
        
        state.learnings = result
    
    async def _execute_phase_function(self, 
                                       fn: Callable,
                                       phase_name: str,
                                       input_data: Any) -> Any:
        """
        Execute a phase function with error handling and logging.
        
        Args:
            fn: The phase function to execute
            phase_name: Name of the phase for error messages
            input_data: Input data for the phase function
            
        Returns:
            Output from the phase function
            
        Raises:
            Exception: If phase function fails
        """
        try:
            if asyncio.iscoroutinefunction(fn):
                result = await fn(input_data)
            else:
                result = fn(input_data)
            return result
        except Exception as e:
            error_msg = f"{phase_name.upper()} phase failed: {str(e)}"
            if self.current_state:
                self.current_state.errors.append(error_msg)
            raise Exception(error_msg) from e


def create_default_cycle() -> AGIImprovementCycle:
    """
    Create an improvement cycle with default placeholder functions.
    
    In production, these would be replaced with actual BYRD components.
    This demonstrates the structure without requiring full implementation.
    """
    
    async def default_assess(state: Dict) -> Dict:
        """Default assessment: Return system metrics."""
        return {
            "timestamp": datetime.now().isoformat(),
            "capabilities": ["reasoning", "coding", "reflection"],
            "performance": {"accuracy": 0.85, "speed": 1.0},
            "gaps": ["multi-step planning", "long-term memory"]
        }
    
    async def default_identify(assessments: Dict) -> List[Dict]:
        """Default identification: Find opportunities from gaps."""
        return [
            {
                "opportunity": "improve_multi_step_planning",
                "priority": 0.9,
                "description": "Enhance ability to chain reasoning steps"
            },
            {
                "opportunity": "enhance_long_term_memory",
                "priority": 0.7,
                "description": "Improve memory consolidation and retrieval"
            }
        ]
    
    async def default_generate(opportunities: List[Dict]) -> List[Dict]:
        """Default generation: Create solutions for opportunities."""
        return [
            {
                "solution": "tree_of_thought_reasoning",
                "target": "improve_multi_step_planning",
                "approach": "Implement tree search for reasoning paths"
            },
            {
                "solution": "vector_memory_index",
                "target": "enhance_long_term_memory",
                "approach": "Add vector embeddings for semantic search"
            }
        ]
    
    async def default_predict(solutions: List[Dict]) -> Dict[str, float]:
        """Default prediction: Estimate impact scores."""
        return {
            "tree_of_thought_reasoning": 0.85,
            "vector_memory_index": 0.72
        }
    
    async def default_verify(data: Dict) -> Dict[str, bool]:
        """Default verification: Check feasibility."""
        return {
            "tree_of_thought_reasoning": True,
            "vector_memory_index": True
        }
    
    async def default_execute(solutions: List[Dict]) -> Dict[str, Any]:
        """Default execution: Simulate implementation."""
        results = {}
        for sol in solutions:
            solution_name = sol["solution"]
            results[solution_name] = {
                "status": "implemented",
                "timestamp": datetime.now().isoformat(),
                "changes": 3
            }
        return results
    
    async def default_measure(execution_results: Dict) -> Dict[str, float]:
        """
        Default measurement: Return simulated post-execution metrics.
        
        CRITICAL: Must return metrics with same names as baseline for delta calculation.
        For demonstration, we simulate improvement over baseline (accuracy: 0.85 -> 0.90).
        """
        # Simulate post-execution measurements
        # These must use the same keys as baseline_measurements for delta calc
        return {
            "accuracy": 0.90,  # Improved from baseline 0.85
            "speed": 1.15      # Improved from baseline 1.0
        }
    
    async def default_learn(data: Dict) -> Dict[str, Any]:
        """
        Default learning: Extract insights from delta measurements.
        
        CRITICAL: Success is determined by positive delta, not prediction accuracy.
        Strategies that fail to improve over baseline are rejected.
        """
        predictions = data.get("predictions", {})
        baseline = data.get("baseline_measurements", {})
        measurements = data.get("measurements", {})
        deltas = data.get("delta_measurements", {})
        success = data.get("success", False)
        
        if not success:
            # No positive deltas - cycle failed
            return {
                "cycle_success": False,
                "reason": "No positive delta measured",
                "deltas": deltas,
                "recommendation": "Abandon current strategies, reassess baseline"
            }
        
        # Success - identify which metrics improved most
        best_delta_metric = max(deltas.items(), key=lambda x: x[1])
        
        return {
            "cycle_success": True,
            "best_delta_metric": best_delta_metric[0],
            "best_delta_value": best_delta_metric[1],
            "baseline": baseline,
            "measurements": measurements,
            "deltas": deltas,
            "recommendation": "Continue scaling successful strategies"
        }
    
    return AGIImprovementCycle(
        assess_fn=default_assess,
        identify_fn=default_identify,
        generate_fn=default_generate,
        predict_fn=default_predict,
        verify_fn=default_verify,
        execute_fn=default_execute,
        measure_fn=default_measure,
        learn_fn=default_learn
    )


async def main():
    """
    Demonstrate the improvement cycle in action.
    
    This shows how the cycle enforces forward progress through
    all 8 phases without getting stuck in analysis.
    """
    print("\n" + "="*60)
    print("BYRD AGI Improvement Cycle - Breaking Analysis-Action Loops")
    print("="*60 + "\n")
    
    # Create cycle with default implementation
    cycle = create_default_cycle()
    
    # Run complete cycle
    print("Starting improvement cycle...")
    start_time = time.time()
    
    state = await cycle.run_cycle()
    
    duration = time.time() - start_time
    
    # Display results
    print(f"\n✓ Cycle completed in {duration:.2f} seconds")
    print(f"✓ Cycle ID: {state.cycle_id}")
    print(f"✓ Phases completed: 8/8")
    print(f"\n--- Results Summary ---")
    print(f"Assessments: {len(state.assessments)} metrics collected")
    print(f"Opportunities identified: {len(state.opportunities)}")
    print(f"Solutions generated: {len(state.solutions)}")
    print(f"Predictions made: {len(state.predictions)}")
    print(f"Solutions verified: {sum(state.verification_results.values())}")
    print(f"Solutions executed: {len(state.execution_results)}")
    print(f"Measurements taken: {len(state.measurements)}")
    print(f"Learnings extracted: {len(state.learnings)}")
    
    # CRITICAL: Display delta measurements to break false-positive loop
    print(f"\n--- DELTA MEASUREMENTS (Breaking False-Positive Loop) ---")
    print(f"Baseline measurements: {state.baseline_measurements}")
    print(f"Post-execution measurements: {state.measurements}")
    print(f"DELTA measurements: {state.delta_measurements}")
    has_positive_delta = any(d > 0 for d in state.delta_measurements.values())
    print(f"Positive delta detected: {has_positive_delta}")
    if has_positive_delta:
        print("✓ SUCCESS: At least one metric improved over baseline")
    else:
        print("✗ FAILURE: No metrics improved over baseline - false positive blocked")
    
    if state.errors:
        print(f"\n⚠ Errors/Warnings: {len(state.errors)}")
        for error in state.errors:
            print(f"  - {error}")
    
    print("\n" + "="*60)
    print("Cycle complete. Action taken. Analysis complete.")
    print("No infinite loops. Forward progress achieved.")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
