"""
BYRD Bold Experiments Framework

Uses rollback safety to enable bolder, more aggressive self-improvement experiments.

ACCELERATION MINDSET:
- Safety nets enable risk-taking
- Rollback capability = freedom to experiment
- Failed experiments are learning opportunities, not failures

PRINCIPLES:
1. If you can rollback, you can be bold
2. Failed experiments accelerate learning through negative results
3. Parallel exploration beats sequential caution
4. Measure everything, including what doesn't work

This framework wraps risky modifications with automatic rollback,
tracks experiment outcomes, and supports parallel exploration of
multiple improvement paths simultaneously.
"""

import asyncio
import random
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple
from enum import Enum

from memory import Memory
from rollback import RollbackSystem, RollbackReason, RollbackResult


class ExperimentStatus(Enum):
    """Status of an experiment."""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"
    INCONCLUSIVE = "inconclusive"


class RiskLevel(Enum):
    """Risk level of an experiment - higher risk = bolder experiments."""
    SAFE = "safe"           # Proven patterns, high confidence
    MODERATE = "moderate"   # Some uncertainty, reasonable caution
    BOLD = "bold"           # Unproven, high risk, high reward
    AGGRESSIVE = "aggressive"  # Breaking conventions, may destabilize
    RADICAL = "radical"     # Fundamental changes, rollback expected

@dataclass
class ExperimentHypothesis:
    """A hypothesis to test through experimentation."""
    id: str
    description: str
    risk_level: RiskLevel
    expected_improvement: float  # Expected delta in capability
    confidence: float  # 0.0-1.0, how confident we are
    rollback_strategy: str  # What to do if it fails
    success_criteria: str
    failure_indicators: List[str]
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "description": self.description,
            "risk_level": self.risk_level.value,
            "expected_improvement": self.expected_improvement,
            "confidence": self.confidence,
            "rollback_strategy": self.rollback_strategy,
            "success_criteria": self.success_criteria,
            "failure_indicators": self.failure_indicators
        }


@dataclass
class ExperimentResult:
    """Result of running an experiment."""
    experiment_id: str
    status: ExperimentStatus
    actual_improvement: Optional[float]
    rollback_triggered: bool
    rollback_reason: Optional[str]
    lessons_learned: List[str]
    execution_time: float
    started_at: datetime
    completed_at: datetime
    logs: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        return {
            "experiment_id": self.experiment_id,
            "status": self.status.value,
            "actual_improvement": self.actual_improvement,
            "rollback_triggered": self.rollback_triggered,
            "rollback_reason": self.rollback_reason,
            "lessons_learned": self.lessons_learned,
            "execution_time": self.execution_time,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat(),
            "log_count": len(self.logs)
        }


class BoldExperimentFramework:
    """
    Framework for running bold, risky experiments with automatic rollback.
    
    The key insight: having a reliable rollback system changes the risk
    calculus entirely. We can afford to be aggressive because failures
    are cheap and reversible.
    
    This framework:
    1. Wraps any modification with automatic rollback
    2. Runs experiments in parallel when safe
    3. Tracks all outcomes, including negative results
    4. Builds a knowledge base of what doesn't work
    """

    def __init__(self, memory: Memory, rollback: RollbackSystem):
        self.memory = memory
        self.rollback = rollback
        
        # Experiment tracking
        self._hypotheses: List[ExperimentHypothesis] = []
        self._results: List[ExperimentResult] = []
        self._running_experiments: Dict[str, asyncio.Task] = {}
        
        # Settings
        self._max_concurrent_experiments = 3
        self._auto_rollback_threshold = -0.02  # Rollback if capability drops >2%
        self._bold_mode_enabled = True  # Allow aggressive experiments
        
        # Metrics
        self._total_experiments_run = 0
        self._successful_experiments = 0
        self._rolled_back_experiments = 0
        self._learning_from_failures = 0

    async def initialize(self):
        """Initialize the experiment framework."""
        await self.memory.record_experience(
            content="[BOLD_EXPERIMENTS] Framework initialized with rollback safety",
            type="system"
        )

    def enable_bold_mode(self, enabled: bool = True):
        """Enable or disable bold experimentation mode."""
        self._bold_mode_enabled = enabled
        print(f"🚀 Bold mode {'ENABLED' if enabled else 'DISABLED'} - time to be {'' if enabled else 'cautious'}aggressive!")

    async def propose_hypothesis(
        self,
        description: str,
        risk_level: RiskLevel,
        expected_improvement: float,
        confidence: float,
        success_criteria: str,
        failure_indicators: List[str]
    ) -> ExperimentHypothesis:
        """
        Propose a new hypothesis for experimentation.
        
        Higher risk levels are encouraged when bold_mode is enabled.
        The framework will create appropriate rollback strategies.
        """
        if not self._bold_mode_enabled and risk_level in [RiskLevel.AGGRESSIVE, RiskLevel.RADICAL]:
            print(f"⚠️ Bold mode disabled - cannot propose {risk_level.value} experiments")
            raise ValueError(f"{risk_level.value} experiments require bold mode")
        
        # Create rollback strategy based on risk
        rollback_strategy = self._create_rollback_strategy(risk_level)
        
        hypothesis = ExperimentHypothesis(
            id=f"hyp_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(self._hypotheses)}",
            description=description,
            risk_level=risk_level,
            expected_improvement=expected_improvement,
            confidence=confidence,
            rollback_strategy=rollback_strategy,
            success_criteria=success_criteria,
            failure_indicators=failure_indicators
        )
        
        self._hypotheses.append(hypothesis)
        
        await self.memory.record_experience(
            content=f"[HYPOTHESIS] {hypothesis.id}: {description} | risk={risk_level.value} expected={expected_improvement:+.2%}",
            type="hypothesis"
        )
        
        print(f"💡 Hypothesis proposed: {description}")
        print(f"   Risk: {risk_level.value} | Expected improvement: {expected_improvement:+.2%}")
        
        return hypothesis

    def _create_rollback_strategy(self, risk_level: RiskLevel) -> str:
        """Create appropriate rollback strategy for risk level."""
        strategies = {
            RiskLevel.SAFE: "Monitor only, rollback on explicit failure",
            RiskLevel.MODERATE: "Checkpoint before, rollback if any test fails",
            RiskLevel.BOLD: "Auto-rollback if improvement < 50% of expected",
            RiskLevel.AGGRESSIVE: "Auto-rollback if any regression, run parallel experiments",
            RiskLevel.RADICAL: "Expect rollback, document what breaks, try variations"
        }
        return strategies[risk_level]

    async def run_experiment(
        self,
        hypothesis: ExperimentHypothesis,
        modification_fn: Callable,
        evaluation_fn: Callable
    ) -> ExperimentResult:
        """
        Run an experiment with automatic rollback safety.
        
        Args:
            hypothesis: The hypothesis being tested
            modification_fn: Async function that applies the modification
            evaluation_fn: Async function that measures the outcome
        
        Returns:
            ExperimentResult with status, improvement, and lessons learned
        """
        print(f"\n{'='*60}")
        print(f"🧪 RUNNING EXPERIMENT: {hypothesis.id}")
        print(f"   {hypothesis.description}")
        print(f"   Risk level: {hypothesis.risk_level.value}")
        print(f"{'='*60}\n")
        
        started_at = datetime.now()
        logs: List[str] = []
        
        try:
            # Log experiment start
            await self.memory.record_experience(
                content=f"[EXPERIMENT_START] {hypothesis.id}: {hypothesis.description}",
                type="experiment"
            )
            
            # Apply modification
            logs.append("Applying modification...")
            modification_result = await modification_fn()
            logs.append(f"Modification applied: {modification_result}")
            
            # Evaluate outcome
            logs.append("Evaluating outcome...")
            evaluation_result = await evaluation_fn()
            actual_improvement = evaluation_result.get("improvement", 0.0)
            
            logs.append(f"Measured improvement: {actual_improvement:+.2%}")
            
            # Check if rollback should be triggered
            rollback_triggered = False
            rollback_reason = None
            
            if actual_improvement < self._auto_rollback_threshold:
                rollback_triggered = True
                rollback_reason = f"Improvement ({actual_improvement:+.2%}) below threshold ({self._auto_rollback_threshold:+.2%})"
                
                # Check for failure indicators
                for indicator in hypothesis.failure_indicators:
                    if indicator in str(evaluation_result):
                        rollback_reason = f"Failure indicator detected: {indicator}"
                        break
            
            # Perform rollback if needed
            if rollback_triggered:
                print(f"⚠️  Rollback triggered: {rollback_reason}")
                rollback_result = await self.rollback.rollback_last(
                    RollbackReason.CAPABILITY_REGRESSION
                )
                
                if rollback_result.success:
                    logs.append("✅ Rollback successful")
                    self._rolled_back_experiments += 1
                    status = ExperimentStatus.ROLLED_BACK
                else:
                    logs.append(f"❌ Rollback failed: {rollback_result.error}")
                    status = ExperimentStatus.FAILED
            else:
                # Success!
                self._successful_experiments += 1
                status = ExperimentStatus.SUCCESS
                logs.append("✅ Experiment successful - keeping changes")
            
            # Extract lessons learned
            lessons = self._extract_lessons(
                hypothesis,
                actual_improvement,
                rollback_triggered,
                evaluation_result
            )
            
            if rollback_triggered:
                self._learning_from_failures += 1
            
        except Exception as e:
            # Emergency rollback on any exception
            print(f"🚨 Exception during experiment: {e}")
            
            rollback_result = await self.rollback.rollback_last(
                RollbackReason.EMERGENCY_STOP
            )
            
            actual_improvement = None
            rollback_triggered = rollback_result.success
            rollback_reason = f"Exception: {str(e)}"
            lessons = [f"Exception encountered: {e}", "Emergency rollback triggered"]
            logs.append(f"❌ Exception: {e}")
            status = ExperimentStatus.FAILED
        
        completed_at = datetime.now()
        execution_time = (completed_at - started_at).total_seconds()
        
        result = ExperimentResult(
            experiment_id=hypothesis.id,
            status=status,
            actual_improvement=actual_improvement,
            rollback_triggered=rollback_triggered,
            rollback_reason=rollback_reason,
            lessons_learned=lessons,
            execution_time=execution_time,
            started_at=started_at,
            completed_at=completed_at,
            logs=logs
        )
        
        self._results.append(result)
        self._total_experiments_run += 1
        
        # Record result in memory
        await self._record_experiment_result(hypothesis, result)
        
        # Print summary
        self._print_experiment_summary(hypothesis, result)
        
        return result

    def _extract_lessons(
        self,
        hypothesis: ExperimentHypothesis,
        actual_improvement: float,
        rollback_triggered: bool,
        evaluation_result: Dict
    ) -> List[str]:
        """Extract lessons learned from the experiment."""
        lessons = []
        
        # Compare expectation vs reality
        if actual_improvement is not None:
            delta = actual_improvement - hypothesis.expected_improvement
            if abs(delta) > 0.05:
                lessons.append(f"Hypothesis was {'overconfident' if delta < 0 else 'underconfident'}: expected {hypothesis.expected_improvement:+.2%}, got {actual_improvement:+.2%}")
        
        if rollback_triggered:
            lessons.append(f"Risk level {hypothesis.risk_level.value} was appropriate - rollback prevented damage")
            lessons.append("Negative result is valuable data for future experiments")
        else:
            lessons.append(f"Successful experiment at {hypothesis.risk_level.value} risk level")
            if hypothesis.risk_level in [RiskLevel.BOLD, RiskLevel.AGGRESSIVE, RiskLevel.RADICAL]:
                lessons.append("Bold experiment succeeded - should explore similar directions")
        
        # Extract any insights from evaluation
        if "insights" in evaluation_result:
            lessons.extend(evaluation_result["insights"])
        
        return lessons

    async def _record_experiment_result(
        self,
        hypothesis: ExperimentHypothesis,
        result: ExperimentResult
    ):
        """Record experiment result in memory."""
        content = f"[EXPERIMENT_RESULT] {result.experiment_id} | status={result.status.value} improvement={result.actual_improvement or 'N/A':+} rollback={result.rollback_triggered}"
        
        if result.lessons_learned:
            content += f" | lessons={' | '.join(result.lessons_learned)}"
        
        await self.memory.record_experience(content, type="experiment_result")

    def _print_experiment_summary(
        self,
        hypothesis: ExperimentHypothesis,
        result: ExperimentResult
    ):
        """Print a summary of the experiment."""
        print(f"\n{'='*60}")
        print(f"📊 EXPERIMENT SUMMARY: {result.experiment_id}")
        print(f"   Status: {result.status.value}")
        if result.actual_improvement is not None:
            print(f"   Improvement: {result.actual_improvement:+.2%}")
        print(f"   Rollback triggered: {'Yes' if result.rollback_triggered else 'No'}")
        if result.rollback_reason:
            print(f"   Reason: {result.rollback_reason}")
        print(f"   Execution time: {result.execution_time:.2f}s")
        
        if result.lessons_learned:
            print(f"\n   📚 Lessons learned:")
            for lesson in result.lessons_learned:
                print(f"      • {lesson}")
        
        print(f"{'='*60}\n")

    async def run_parallel_experiments(
        self,
        experiments: List[Tuple[ExperimentHypothesis, Callable, Callable]]
    ) -> List[ExperimentResult]:
        """
        Run multiple experiments in parallel.
        
        This is where acceleration really happens - testing multiple
        hypotheses simultaneously rather than sequentially.
        """
        print(f"\n🚀 Running {len(experiments)} experiments in parallel...")
        
        # Limit concurrent experiments
        active_experiments = []
        results = []
        
        for i, (hypothesis, mod_fn, eval_fn) in enumerate(experiments):
            if len(active_experiments) >= self._max_concurrent_experiments:
                # Wait for one to complete
                done, pending = await asyncio.wait(
                    active_experiments,
                    return_when=asyncio.FIRST_COMPLETED
                )
                for task in done:
                    results.append(task.result())
                active_experiments = list(pending)
            
            # Start next experiment
            task = asyncio.create_task(
                self.run_experiment(hypothesis, mod_fn, eval_fn)
            )
            active_experiments.append(task)
        
        # Wait for remaining
        if active_experiments:
            results.extend(await asyncio.gather(*active_experiments))
        
        return results

    def get_experiment_statistics(self) -> Dict:
        """Get statistics about experiments run."""
        return {
            "total_experiments": self._total_experiments_run,
            "successful": self._successful_experiments,
            "rolled_back": self._rolled_back_experiments,
            "learning_from_failures": self._learning_from_failures,
            "success_rate": (
                self._successful_experiments / self._total_experiments_run
                if self._total_experiments_run > 0 else 0
            ),
            "rollback_rate": (
                self._rolled_back_experiments / self._total_experiments_run
                if self._total_experiments_run > 0 else 0
            )
        }

    async def generate_bold_hypotheses(
        self,
        context: Dict[str, Any]
    ) -> List[ExperimentHypothesis]:
        """
        Generate bold experiment hypotheses based on current context.
        
        This method analyzes the current state and suggests experiments
        that push boundaries, knowing rollback provides safety.
        """
        hypotheses = []
        
        # Example bold hypotheses based on context
        # In a real implementation, this would use LLM reasoning
        
        if "capability_gaps" in context:
            for gap in context["capability_gaps"]:
                hypotheses.append(await self.propose_hypothesis(
                    description=f"Radical refactor to address {gap['name']}",
                    risk_level=RiskLevel.RADICAL,
                    expected_improvement=0.15,
                    confidence=0.3,
                    success_criteria=f"{gap['name']} capability improves by >10%",
                    failure_indicators=["regression", "breakage", "error"]
                ))
        
        if "recent_failures" in context and context["recent_failures"] > 3:
            # Aggressive approach after failures
            hypotheses.append(await self.propose_hypothesis(
                description="Pivot to entirely different approach",
                risk_level=RiskLevel.AGGRESSIVE,
                expected_improvement=0.25,
                confidence=0.4,
                success_criteria="New approach shows >20% improvement",
                failure_indicators=["no_improvement", "worse_performance"]
            ))
        
        return hypotheses


# Example usage demonstration
async def demo_bold_experiments():
    """
    Demonstrate the bold experiments framework.
    
    This shows how rollback safety enables aggressive experimentation.
    """
    from memory import Memory
    from rollback import RollbackSystem
    
    # Initialize components
    memory = Memory()
    rollback = RollbackSystem(memory)
    framework = BoldExperimentFramework(memory, rollback)
    
    await memory.initialize()
    await rollback.initialize()
    await framework.initialize()
    
    # Enable bold mode
    framework.enable_bold_mode(True)
    
    # Propose a bold hypothesis
    hypothesis = await framework.propose_hypothesis(
        description="Replace existing reasoning engine with experimental graph-based approach",
        risk_level=RiskLevel.RADICAL,
        expected_improvement=0.30,  # Expect 30% improvement
        confidence=0.25,  # But only 25% confident - still worth trying!
        success_criteria="Reasoning tasks complete 30% faster with similar accuracy",
        failure_indicators=["accuracy_drop", "timeout", "inconsistency"]
    )
    
    # Define the experiment functions
    async def apply_modification():
        # In real usage, this would apply actual code changes
        return "Applied graph-based reasoning engine"
    
    async def evaluate_outcome():
        # Simulate an outcome (in real usage, measure actual performance)
        # This one fails, triggering rollback
        return {
            "improvement": -0.15,  # 15% regression
            "accuracy_drop": True
        }
    
    # Run the experiment
    result = await framework.run_experiment(
        hypothesis,
        apply_modification,
        evaluate_outcome
    )
    
    # Print statistics
    stats = framework.get_experiment_statistics()
    print(f"\n📈 Experiment Statistics:")
    print(f"   Total: {stats['total_experiments']}")
    print(f"   Successful: {stats['successful']}")
    print(f"   Rolled back: {stats['rolled_back']}")
    print(f"   Learning from failures: {stats['learning_from_failures']}")
    print(f"   Success rate: {stats['success_rate']:.1%}")
    print(f"   Rollback rate: {stats['rollback_rate']:.1%}")


if __name__ == "__main__":
    asyncio.run(demo_bold_experiments())
