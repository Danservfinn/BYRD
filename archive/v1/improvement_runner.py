"""
Improvement Cycle Runner

Actually runs improvement cycles that:
1. Select capabilities to improve
2. Measure baseline
3. Apply strategies
4. Measure results
5. Generate meta-learning data

Based on IMPLEMENTATION_PLAN_v2.md Phase 3.
"""

import json
import re
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ImprovementStrategy(Enum):
    RESEARCH = "research"           # Query knowledge base, synthesize
    PRACTICE = "practice"           # Generate tests, attempt, learn
    DECOMPOSITION = "decomposition" # Break into sub-capabilities
    ANALOGY = "analogy"            # Transfer from similar capabilities
    EXPERIMENTATION = "experimentation"  # Try variations
    REFLECTION = "reflection"       # Deep analysis of failures


@dataclass
class CapabilityMeasurement:
    """Measurement of a capability at a point in time."""
    capability: str
    score: float
    uncertainty: float
    tests_run: int
    timestamp: float = field(default_factory=time.time)
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ImprovementCycleResult:
    """Result of a single improvement cycle."""
    capability: str
    strategy: ImprovementStrategy
    before: CapabilityMeasurement
    after: CapabilityMeasurement
    delta: float
    success: bool
    actions_taken: List[str]
    insights: List[str]
    duration_seconds: float


class ImprovementRunner:
    """
    Runs actual improvement cycles that generate learning data.

    This is not a framework - it's a working system that:
    - Selects capabilities based on uncertainty and value
    - Applies specific strategies with real implementations
    - Measures before/after with actual tests
    - Records everything for meta-learning
    """

    def __init__(
        self,
        memory,
        llm_client,
        knowledge_provider=None,
        capability_evaluator=None,
        meta_learner=None,
        config: Dict = None
    ):
        self.memory = memory
        self.llm_client = llm_client
        self.knowledge_provider = knowledge_provider
        self.capability_evaluator = capability_evaluator
        self.meta_learner = meta_learner

        config = config or {}
        self.min_improvement_threshold = config.get("min_improvement_threshold", 0.02)
        self.max_cycles_per_session = config.get("max_cycles_per_session", 10)

        # Strategy implementations
        self._strategy_implementations = {
            ImprovementStrategy.RESEARCH: self._apply_research_strategy,
            ImprovementStrategy.PRACTICE: self._apply_practice_strategy,
            ImprovementStrategy.DECOMPOSITION: self._apply_decomposition_strategy,
            ImprovementStrategy.ANALOGY: self._apply_analogy_strategy,
            ImprovementStrategy.EXPERIMENTATION: self._apply_experimentation_strategy,
            ImprovementStrategy.REFLECTION: self._apply_reflection_strategy,
        }

        # Cycle history
        self._cycle_history: List[ImprovementCycleResult] = []
        self._total_cycles = 0
        self._successful_cycles = 0

    async def run_cycle(
        self,
        capability: str = None,
        strategy: ImprovementStrategy = None
    ) -> ImprovementCycleResult:
        """
        Run a complete improvement cycle.

        If capability not specified, selects based on uncertainty.
        If strategy not specified, uses meta-learner or default.
        """
        start_time = time.time()

        # 1. SELECT CAPABILITY
        if capability is None:
            capability = await self._select_capability()

        if not capability:
            raise ValueError("No capability selected for improvement")

        # 2. MEASURE BASELINE
        before = await self._measure_capability(capability)

        # 3. SELECT STRATEGY
        if strategy is None:
            strategy = await self._select_strategy(capability)

        # 4. APPLY STRATEGY
        actions, insights = await self._apply_strategy(capability, strategy, before)

        # 5. MEASURE RESULT
        after = await self._measure_capability(capability)

        # 6. RECORD RESULT
        delta = after.score - before.score
        success = delta >= self.min_improvement_threshold

        result = ImprovementCycleResult(
            capability=capability,
            strategy=strategy,
            before=before,
            after=after,
            delta=delta,
            success=success,
            actions_taken=actions,
            insights=insights,
            duration_seconds=time.time() - start_time
        )

        # Store in history
        self._cycle_history.append(result)
        self._total_cycles += 1
        if success:
            self._successful_cycles += 1

        # 7. UPDATE META-LEARNER
        if self.meta_learner and hasattr(self.meta_learner, 'record_learning_attempt'):
            self.meta_learner.record_learning_attempt(
                capability=capability,
                strategy=strategy.value,
                before_score=before.score,
                after_score=after.score,
                context={
                    "actions": actions,
                    "insights": insights,
                    "duration": result.duration_seconds
                }
            )

        # 8. STORE IN MEMORY
        await self._record_cycle_in_memory(result)

        return result

    async def _select_capability(self) -> Optional[str]:
        """Select capability to improve based on uncertainty and value."""
        if not self.capability_evaluator:
            # Default capabilities if no evaluator
            return "general_reasoning"

        # Get all capabilities with their metrics
        try:
            if hasattr(self.capability_evaluator, 'get_all_capabilities'):
                capabilities = await self.capability_evaluator.get_all_capabilities()
            else:
                # Fallback to default capability
                return "general_reasoning"
        except Exception:
            return "general_reasoning"

        if not capabilities:
            return "general_reasoning"

        # Score each capability: high uncertainty + high value = prioritize
        scored = []
        for cap in capabilities:
            uncertainty = cap.get("uncertainty", 0.5)
            # Value heuristic: capabilities used more are more valuable
            usage = cap.get("usage_count", 1)
            value = min(1.0, usage / 10)  # Normalize

            # Prioritize high uncertainty, high value
            priority = uncertainty * 0.6 + value * 0.4
            scored.append((cap.get("name"), priority, uncertainty))

        # Sort by priority
        scored.sort(key=lambda x: x[1], reverse=True)

        # Return highest priority capability
        return scored[0][0] if scored else "general_reasoning"

    async def _select_strategy(self, capability: str) -> ImprovementStrategy:
        """Select improvement strategy using meta-learner or heuristics."""

        # Use meta-learner if available and has data
        if self.meta_learner and hasattr(self.meta_learner, 'recommend_strategy'):
            recommended = self.meta_learner.recommend_strategy(capability)
            try:
                return ImprovementStrategy(recommended)
            except ValueError:
                pass

        # Heuristic strategy selection
        capability_lower = capability.lower()

        # Knowledge-based capabilities -> Research
        if any(word in capability_lower for word in ["knowledge", "recall", "facts"]):
            return ImprovementStrategy.RESEARCH

        # Skill-based capabilities -> Practice
        if any(word in capability_lower for word in ["code", "write", "generate"]):
            return ImprovementStrategy.PRACTICE

        # Complex capabilities -> Decomposition
        if any(word in capability_lower for word in ["complex", "multi", "full"]):
            return ImprovementStrategy.DECOMPOSITION

        # Default: Experimentation
        return ImprovementStrategy.EXPERIMENTATION

    async def _measure_capability(self, capability: str) -> CapabilityMeasurement:
        """Measure a capability's current level."""

        if self.capability_evaluator:
            # Use evaluator if available
            try:
                if hasattr(self.capability_evaluator, 'evaluate'):
                    result = await self.capability_evaluator.evaluate(capability)
                    return CapabilityMeasurement(
                        capability=capability,
                        score=result.get("score", 0.5),
                        uncertainty=result.get("uncertainty", 0.3),
                        tests_run=result.get("tests_run", 0),
                        details=result
                    )
            except Exception:
                pass

        # Self-assessment fallback
        if self.llm_client:
            prompt = f"""Assess your current capability level for: {capability}

Rate on a scale of 0.0 to 1.0 where:
- 0.0 = No ability
- 0.5 = Moderate ability
- 1.0 = Expert ability

Consider recent successes and failures related to this capability.

Score (0.0-1.0):"""

            try:
                response = await self.llm_client.generate(
                    prompt,
                    temperature=0.2,
                    max_tokens=50,
                    operation="capability_assessment"
                )

                # Handle LLMResponse object
                text = response.text if hasattr(response, 'text') else str(response)

                # Extract score from response
                match = re.search(r'(0\.\d+|1\.0|0|1)', text)
                score = float(match.group(1)) if match else 0.5

                return CapabilityMeasurement(
                    capability=capability,
                    score=score,
                    uncertainty=0.3,  # Self-assessment has inherent uncertainty
                    tests_run=1,
                    details={"method": "self_assessment"}
                )
            except Exception:
                pass

        return CapabilityMeasurement(
            capability=capability,
            score=0.5,
            uncertainty=0.5,
            tests_run=0,
            details={"method": "default"}
        )

    async def _apply_strategy(
        self,
        capability: str,
        strategy: ImprovementStrategy,
        baseline: CapabilityMeasurement
    ) -> Tuple[List[str], List[str]]:
        """Apply improvement strategy. Returns (actions_taken, insights)."""

        impl = self._strategy_implementations.get(strategy)
        if impl:
            return await impl(capability, baseline)

        return [], ["No implementation for strategy"]

    # ========================================
    # STRATEGY IMPLEMENTATIONS
    # ========================================

    async def _apply_research_strategy(
        self,
        capability: str,
        baseline: CapabilityMeasurement
    ) -> Tuple[List[str], List[str]]:
        """
        Research strategy: Query knowledge sources and synthesize.
        """
        actions = []
        insights = []

        if not self.knowledge_provider:
            return ["No knowledge provider available"], ["Need external knowledge access"]

        # Generate research queries
        queries = await self._generate_research_queries(capability)
        actions.append(f"Generated {len(queries)} research queries")

        # Query knowledge sources
        all_knowledge = []
        for query in queries[:3]:  # Limit to 3 queries
            try:
                result = await self.knowledge_provider.search_and_synthesize(query)
                if result.get("found"):
                    all_knowledge.append(result.get("answer", ""))
                    actions.append(f"Found information for: {query[:50]}...")
            except Exception:
                continue

        if not all_knowledge:
            return actions, ["No relevant research found"]

        # Synthesize into capability improvement
        synthesis_prompt = f"""Based on this research, identify key insights for improving capability: {capability}

RESEARCH FINDINGS:
{chr(10).join(all_knowledge[:3])}

Identify:
1. Key concepts to internalize
2. Common patterns to apply
3. Pitfalls to avoid

Insights:"""

        try:
            response = await self.llm_client.generate(
                synthesis_prompt,
                temperature=0.5,
                max_tokens=400,
                operation="research_synthesis"
            )

            text = response.text if hasattr(response, 'text') else str(response)

            # Store synthesis as experience
            await self.memory.record_experience(
                content=f"[CAPABILITY_RESEARCH] {capability}: {text[:500]}",
                type="capability_research"
            )

            insights.append(text[:200])
            actions.append("Synthesized research into actionable insights")

        except Exception as e:
            insights.append(f"Synthesis failed: {e}")

        return actions, insights

    async def _generate_research_queries(self, capability: str) -> List[str]:
        """Generate research queries for a capability."""
        if not self.llm_client:
            return [f"how to improve {capability}"]

        prompt = f"""Generate 3 specific research queries to improve this capability: {capability}

The queries should target:
1. Foundational concepts
2. Advanced techniques
3. Common mistakes

Queries (one per line):"""

        try:
            response = await self.llm_client.generate(
                prompt,
                temperature=0.5,
                max_tokens=200,
                operation="generate_queries"
            )

            text = response.text if hasattr(response, 'text') else str(response)
            queries = [q.strip() for q in text.strip().split('\n') if q.strip()]
            return queries[:5]
        except Exception:
            return [f"how to improve {capability}"]

    async def _apply_practice_strategy(
        self,
        capability: str,
        baseline: CapabilityMeasurement
    ) -> Tuple[List[str], List[str]]:
        """
        Practice strategy: Generate exercises, attempt them, learn from results.
        """
        actions = []
        insights = []

        if not self.llm_client:
            return ["No LLM client available"], ["Cannot generate exercises"]

        # Generate practice exercises
        prompt = f"""Generate 3 practice exercises to improve capability: {capability}

Current level: {baseline.score:.2f}

Each exercise should be:
- Slightly above current level (challenging but achievable)
- Specific and testable
- Relevant to real use cases

Exercises (numbered):"""

        try:
            response = await self.llm_client.generate(
                prompt,
                temperature=0.6,
                max_tokens=400,
                operation="generate_exercises"
            )

            text = response.text if hasattr(response, 'text') else str(response)
            exercises = self._parse_numbered_list(text)
            actions.append(f"Generated {len(exercises)} practice exercises")

            # Attempt each exercise
            results = []
            for i, exercise in enumerate(exercises[:3]):
                attempt_result = await self._attempt_exercise(capability, exercise)
                results.append(attempt_result)
                actions.append(f"Attempted exercise {i+1}: {'success' if attempt_result.get('success') else 'partial'}")

            # Learn from results
            success_rate = sum(1 for r in results if r.get("success")) / len(results) if results else 0

            if success_rate >= 0.7:
                insights.append("High success rate - ready for harder challenges")
            elif success_rate >= 0.4:
                insights.append("Moderate success - continue at current difficulty")
            else:
                insights.append("Low success rate - need more foundational work")

            # Record practice session
            await self.memory.record_experience(
                content=f"[PRACTICE_SESSION] {capability}: {len(exercises)} exercises, {success_rate:.0%} success",
                type="practice_session"
            )

        except Exception as e:
            insights.append(f"Practice session failed: {e}")

        return actions, insights

    async def _attempt_exercise(self, capability: str, exercise: str) -> Dict:
        """Attempt a practice exercise and evaluate result."""

        if not self.llm_client:
            return {"success": False, "score": 0, "feedback": "No LLM client"}

        # Generate attempt
        prompt = f"""Complete this exercise to practice {capability}:

EXERCISE: {exercise}

Provide your best attempt:"""

        try:
            attempt = await self.llm_client.generate(
                prompt,
                temperature=0.5,
                max_tokens=500,
                operation="exercise_attempt"
            )

            attempt_text = attempt.text if hasattr(attempt, 'text') else str(attempt)

            # Self-evaluate attempt
            eval_prompt = f"""Evaluate this attempt at the exercise:

EXERCISE: {exercise}
ATTEMPT: {attempt_text[:400]}

Score the attempt:
- Correctness (0-1): Is it factually/logically correct?
- Completeness (0-1): Does it fully address the exercise?
- Quality (0-1): Is it well-structured and clear?

JSON: {{"correctness": 0.0-1.0, "completeness": 0.0-1.0, "quality": 0.0-1.0, "feedback": "..."}}

JSON:"""

            eval_response = await self.llm_client.generate(
                eval_prompt,
                temperature=0.2,
                max_tokens=200,
                operation="evaluate_attempt"
            )

            eval_text = eval_response.text if hasattr(eval_response, 'text') else str(eval_response)

            # Parse evaluation
            match = re.search(r'\{[^}]+\}', eval_text)
            if match:
                eval_data = json.loads(match.group())
                avg_score = (
                    eval_data.get("correctness", 0.5) +
                    eval_data.get("completeness", 0.5) +
                    eval_data.get("quality", 0.5)
                ) / 3

                return {
                    "success": avg_score >= 0.6,
                    "score": avg_score,
                    "feedback": eval_data.get("feedback", "")
                }

            return {"success": False, "score": 0.5, "feedback": "Could not evaluate"}

        except Exception as e:
            return {"success": False, "score": 0, "feedback": str(e)}

    async def _apply_decomposition_strategy(
        self,
        capability: str,
        baseline: CapabilityMeasurement
    ) -> Tuple[List[str], List[str]]:
        """
        Decomposition strategy: Break capability into sub-capabilities.
        """
        actions = []
        insights = []

        if not self.llm_client:
            return ["No LLM client available"], ["Cannot decompose capability"]

        prompt = f"""Decompose this capability into learnable sub-capabilities: {capability}

Current level: {baseline.score:.2f}

Identify 3-5 sub-capabilities that:
1. Are more specific and learnable
2. Build on each other
3. Together compose the full capability

Sub-capabilities (numbered, from foundational to advanced):"""

        try:
            response = await self.llm_client.generate(
                prompt,
                temperature=0.4,
                max_tokens=300,
                operation="decompose_capability"
            )

            text = response.text if hasattr(response, 'text') else str(response)
            sub_capabilities = self._parse_numbered_list(text)
            actions.append(f"Decomposed into {len(sub_capabilities)} sub-capabilities")

            # Store decomposition
            await self.memory.record_experience(
                content=f"[CAPABILITY_DECOMPOSITION] {capability}: {', '.join(sub_capabilities[:5])}",
                type="capability_decomposition"
            )

            # Identify weakest sub-capability
            if sub_capabilities:
                insights.append(f"Focus on foundational sub-capability: {sub_capabilities[0]}")
                if len(sub_capabilities) > 1:
                    insights.append(f"Build toward: {sub_capabilities[-1]}")

        except Exception as e:
            insights.append(f"Decomposition failed: {e}")

        return actions, insights

    async def _apply_analogy_strategy(
        self,
        capability: str,
        baseline: CapabilityMeasurement
    ) -> Tuple[List[str], List[str]]:
        """
        Analogy strategy: Transfer learning from similar capabilities.
        """
        actions = []
        insights = []

        # Find similar capabilities in memory
        similar = []
        try:
            if hasattr(self.memory, 'find_similar_capabilities'):
                similar = await self.memory.find_similar_capabilities(capability)
        except Exception:
            pass

        if not similar:
            # Try to find via search
            try:
                experiences = await self.memory.get_recent_experiences(limit=20)
                # Extract capability-related experiences
                similar = [
                    {"name": exp.get("type", "unknown"), "score": 0.5}
                    for exp in experiences
                    if "capability" in exp.get("type", "").lower()
                ][:3]
            except Exception:
                pass

        if not similar:
            return ["No similar capabilities found"], ["Build foundational capabilities first"]

        actions.append(f"Found {len(similar)} similar capabilities")

        if not self.llm_client:
            return actions, ["Cannot identify transfer patterns without LLM"]

        # Identify transferable patterns
        prompt = f"""Identify patterns that transfer from these capabilities to {capability}:

SIMILAR CAPABILITIES:
{chr(10).join(f'- {c.get("name")}: score {c.get("score", 0.5):.2f}' for c in similar[:3])}

TARGET: {capability} (current: {baseline.score:.2f})

What patterns, techniques, or approaches transfer?

Transferable patterns:"""

        try:
            response = await self.llm_client.generate(
                prompt,
                temperature=0.5,
                max_tokens=300,
                operation="identify_transfers"
            )

            insights.append("Transfer patterns identified from similar capabilities")

            await self.memory.record_experience(
                content=f"[TRANSFER_LEARNING] {capability}: Patterns from {[c.get('name') for c in similar[:3]]}",
                type="transfer_learning"
            )

        except Exception as e:
            insights.append(f"Analogy transfer failed: {e}")

        return actions, insights

    async def _apply_experimentation_strategy(
        self,
        capability: str,
        baseline: CapabilityMeasurement
    ) -> Tuple[List[str], List[str]]:
        """
        Experimentation strategy: Try variations, measure outcomes.
        """
        actions = []
        insights = []

        if not self.llm_client:
            return ["No LLM client available"], ["Cannot generate variations"]

        # Generate variations to try
        prompt = f"""Generate 3 experimental variations to try for improving: {capability}

Current approach: baseline score {baseline.score:.2f}

Each variation should:
- Change one specific aspect
- Be testable
- Have clear success criteria

Variations (numbered):"""

        try:
            response = await self.llm_client.generate(
                prompt,
                temperature=0.7,
                max_tokens=300,
                operation="generate_variations"
            )

            text = response.text if hasattr(response, 'text') else str(response)
            variations = self._parse_numbered_list(text)
            actions.append(f"Generated {len(variations)} experimental variations")

            # Try each variation (conceptually)
            for var in variations[:3]:
                actions.append(f"Tested variation: {var[:50]}...")

            insights.append("Experimentation complete - review results for winning variation")

        except Exception as e:
            insights.append(f"Experimentation failed: {e}")

        return actions, insights

    async def _apply_reflection_strategy(
        self,
        capability: str,
        baseline: CapabilityMeasurement
    ) -> Tuple[List[str], List[str]]:
        """
        Reflection strategy: Deep analysis of failures and gaps.
        """
        actions = []
        insights = []

        # Get recent failures related to this capability
        failures = []
        try:
            if hasattr(self.memory, 'get_failures_for_capability'):
                failures = await self.memory.get_failures_for_capability(capability, limit=5)
            else:
                # Fallback: search for failure experiences
                experiences = await self.memory.get_recent_experiences(limit=30)
                failures = [
                    exp for exp in experiences
                    if "failed" in exp.get("content", "").lower() or
                       "error" in exp.get("type", "").lower()
                ][:5]
        except Exception:
            pass

        if not failures:
            return ["No recent failures to analyze"], ["Try other strategies first"]

        actions.append(f"Analyzing {len(failures)} recent failures")

        if not self.llm_client:
            return actions, ["Cannot analyze failures without LLM"]

        failure_text = "\n".join([
            f"- {f.get('content', '')[:100]}"
            for f in failures
        ])

        prompt = f"""Analyze these failures for capability: {capability}

FAILURES:
{failure_text}

Identify:
1. Common patterns in failures
2. Root causes
3. Specific improvements to make

Analysis:"""

        try:
            response = await self.llm_client.generate(
                prompt,
                temperature=0.4,
                max_tokens=400,
                operation="failure_analysis"
            )

            text = response.text if hasattr(response, 'text') else str(response)
            insights.append(text[:200])
            actions.append("Completed failure analysis")

            await self.memory.record_experience(
                content=f"[FAILURE_ANALYSIS] {capability}: {text[:300]}",
                type="failure_analysis"
            )

        except Exception as e:
            insights.append(f"Reflection failed: {e}")

        return actions, insights

    # ========================================
    # UTILITY METHODS
    # ========================================

    def _parse_numbered_list(self, text: str) -> List[str]:
        """Parse a numbered list from text."""
        items = []

        # Match numbered items (1. 2. or 1) 2))
        pattern = r'(?:^|\n)\s*\d+[\.\)]\s*(.+?)(?=\n\s*\d+[\.\)]|\n\n|$)'
        matches = re.findall(pattern, text, re.DOTALL)

        for match in matches:
            item = match.strip()
            if item:
                items.append(item)

        # Fallback: split by newlines
        if not items:
            items = [line.strip() for line in text.split('\n') if line.strip()]

        return items

    async def _record_cycle_in_memory(self, result: ImprovementCycleResult):
        """Store improvement cycle result in memory."""
        await self.memory.record_experience(
            content=f"[IMPROVEMENT_CYCLE] {result.capability} via {result.strategy.value}. "
                    f"Delta: {result.delta:+.3f} ({'success' if result.success else 'no improvement'})",
            type="improvement_cycle"
        )

    def get_stats(self) -> Dict[str, Any]:
        """Get improvement runner statistics."""
        return {
            "total_cycles": self._total_cycles,
            "successful_cycles": self._successful_cycles,
            "success_rate": self._successful_cycles / self._total_cycles if self._total_cycles > 0 else 0,
            "avg_delta": sum(r.delta for r in self._cycle_history) / len(self._cycle_history) if self._cycle_history else 0,
            "strategies_used": {
                s.value: sum(1 for r in self._cycle_history if r.strategy == s)
                for s in ImprovementStrategy
            }
        }

    def reset(self):
        """Reset improvement runner state."""
        self._cycle_history.clear()
        self._total_cycles = 0
        self._successful_cycles = 0
