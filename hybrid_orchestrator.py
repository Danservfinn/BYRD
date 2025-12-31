"""
Hybrid Orchestrator - Coordinates Z.AI reasoning with Claude SDK execution.

Flow:
1. Receive desire from Seeker
2. Use Z.AI to analyze and plan
3. If execution needed, use Claude SDK
4. Use Z.AI to evaluate results
5. Loop until satisfied

Part of BYRD's Hybrid LLM Architecture.
Philosophy: Z.AI decides WHAT to do, Claude SDK DOES it.
"""

import asyncio
import json
import logging
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
from datetime import datetime

from llm_router import LLMRouter, TaskType, LLMProvider

logger = logging.getLogger(__name__)


@dataclass
class OrchestrationResult:
    """Result of hybrid orchestration."""
    success: bool
    output: str
    reasoning_steps: List[Dict] = field(default_factory=list)
    execution_steps: List[Dict] = field(default_factory=list)
    files_modified: List[str] = field(default_factory=list)
    total_zai_tokens: int = 0
    total_claude_calls: int = 0
    satisfaction_score: float = 0.0
    iterations: int = 0
    duration_ms: int = 0

    def to_dict(self) -> Dict:
        return {
            "success": self.success,
            "output": self.output[:500] if self.output else "",
            "satisfaction_score": self.satisfaction_score,
            "iterations": self.iterations,
            "files_modified": self.files_modified,
            "total_zai_tokens": self.total_zai_tokens,
            "total_claude_calls": self.total_claude_calls,
            "duration_ms": self.duration_ms,
            "reasoning_steps_count": len(self.reasoning_steps),
            "execution_steps_count": len(self.execution_steps),
        }


class HybridOrchestrator:
    """
    Orchestrates between Z.AI (reasoning) and Claude SDK (execution).

    Strategy:
    - Z.AI analyzes the desire and creates a plan (cheap)
    - Claude SDK executes the plan with real tools (included in Max)
    - Z.AI evaluates the results (cheap)
    - Loop until satisfied or max iterations
    """

    def __init__(
        self,
        llm_client,  # Z.AI client
        claude_coder,  # Claude SDK coder (can be None)
        memory=None,
        config: Dict = None,
    ):
        self.llm_client = llm_client  # Z.AI for reasoning
        self.claude_coder = claude_coder  # Claude SDK for execution
        self.memory = memory
        self.config = config or {}

        self.router = LLMRouter(config.get("routing", {}))
        self._max_iterations = self.config.get("max_iterations", 5)
        self._satisfaction_threshold = self.config.get("satisfaction_threshold", 0.8)

        # Stats
        self._orchestration_count = 0
        self._total_zai_tokens = 0
        self._total_claude_calls = 0
        self._successful_orchestrations = 0

        logger.info(f"[HybridOrchestrator] Initialized: max_iter={self._max_iterations}, threshold={self._satisfaction_threshold}")

    async def fulfill_desire(
        self,
        desire: Dict,
        context: Optional[Dict] = None,
    ) -> OrchestrationResult:
        """
        Fulfill a desire using hybrid Z.AI + Claude SDK approach.

        Args:
            desire: The desire to fulfill (must have 'description' key)
            context: Optional context from memory

        Returns:
            OrchestrationResult with full trace
        """
        start_time = datetime.now()
        self._orchestration_count += 1

        description = desire.get("description", "")
        desire_id = desire.get("id", datetime.now().strftime("%Y%m%d%H%M%S"))

        logger.info(f"[HybridOrchestrator] Starting: {description[:80]}...")

        reasoning_steps = []
        execution_steps = []
        files_modified = []
        iteration = 0
        satisfaction_score = 0.0
        final_output = ""

        # Build initial context
        full_context = await self._build_context(desire, context)

        while iteration < self._max_iterations:
            iteration += 1
            logger.info(f"[HybridOrchestrator] Iteration {iteration}/{self._max_iterations}")

            # Step 1: Z.AI analyzes and plans (cheap)
            plan = await self._zai_plan(description, full_context, reasoning_steps)
            reasoning_steps.append({
                "iteration": iteration,
                "type": "planning",
                "plan": plan,
                "timestamp": datetime.now().isoformat(),
            })

            if plan.get("no_action_needed"):
                logger.info("[HybridOrchestrator] Z.AI determined no action needed")
                satisfaction_score = 1.0
                final_output = plan.get("reasoning", "No action needed")
                break

            # Step 2: Claude SDK executes (if available and needed)
            if plan.get("requires_execution") and self.claude_coder and self.claude_coder.enabled:
                execution_prompt = plan.get("execution_prompt", description)

                # Pre-flight check
                can_exec = await self.claude_coder.can_execute(execution_prompt)
                if not can_exec.get("can_execute"):
                    reasoning_steps.append({
                        "iteration": iteration,
                        "type": "execution_blocked",
                        "reason": can_exec.get("reason"),
                        "timestamp": datetime.now().isoformat(),
                    })
                    # Z.AI should try a different approach
                    full_context["execution_blocked"] = can_exec.get("reason")
                    continue

                result = await self.claude_coder.execute(
                    prompt=execution_prompt,
                    context=full_context,
                    desire_id=desire_id,
                )

                self._total_claude_calls += 1
                execution_steps.append({
                    "iteration": iteration,
                    "success": result.success,
                    "output": result.output[:500] if result.output else "",
                    "files_modified": result.files_modified,
                    "tool_calls": len(result.tool_calls),
                    "error": result.error,
                    "timestamp": datetime.now().isoformat(),
                })

                files_modified.extend(result.files_modified)
                final_output = result.output

                if not result.success:
                    # Z.AI analyzes failure
                    recovery = await self._zai_analyze_failure(result.error, result.output)
                    reasoning_steps.append({
                        "iteration": iteration,
                        "type": "failure_analysis",
                        "analysis": recovery,
                        "timestamp": datetime.now().isoformat(),
                    })

                    if not recovery.get("can_recover"):
                        logger.warning(f"[HybridOrchestrator] Cannot recover from failure")
                        break

                    # Update context with recovery strategy
                    full_context["recovery_strategy"] = recovery.get("strategy")
                    full_context["previous_error"] = result.error
                    continue

            elif plan.get("requires_execution") and (not self.claude_coder or not self.claude_coder.enabled):
                # Claude SDK not available - Z.AI generates text-only response
                logger.info("[HybridOrchestrator] Claude SDK not available, using Z.AI text generation")
                text_result = await self._zai_generate_text(plan.get("execution_prompt", description), full_context)
                execution_steps.append({
                    "iteration": iteration,
                    "success": True,
                    "output": text_result[:500],
                    "files_modified": [],
                    "tool_calls": 0,
                    "mode": "zai_text_only",
                    "timestamp": datetime.now().isoformat(),
                })
                final_output = text_result

            # Step 3: Z.AI evaluates results (cheap)
            evaluation = await self._zai_evaluate(
                desire=desire,
                execution_steps=execution_steps,
                reasoning_steps=reasoning_steps,
            )
            reasoning_steps.append({
                "iteration": iteration,
                "type": "evaluation",
                "evaluation": evaluation,
                "timestamp": datetime.now().isoformat(),
            })

            satisfaction_score = evaluation.get("satisfaction", 0.0)

            if satisfaction_score >= self._satisfaction_threshold:
                logger.info(f"[HybridOrchestrator] Satisfied! Score: {satisfaction_score}")
                self._successful_orchestrations += 1
                break

            # Update context with gaps for next iteration
            if evaluation.get("gaps"):
                full_context["previous_gaps"] = evaluation["gaps"]
                full_context["refinement_needed"] = evaluation.get("refinement")

        # Record to memory
        if self.memory:
            await self._record_outcome(desire, satisfaction_score, files_modified, iteration)

        duration = (datetime.now() - start_time).total_seconds()

        return OrchestrationResult(
            success=satisfaction_score >= self._satisfaction_threshold,
            output=final_output,
            reasoning_steps=reasoning_steps,
            execution_steps=execution_steps,
            files_modified=list(set(files_modified)),
            total_zai_tokens=self._total_zai_tokens,
            total_claude_calls=self._total_claude_calls,
            satisfaction_score=satisfaction_score,
            iterations=iteration,
            duration_ms=int(duration * 1000),
        )

    async def _build_context(self, desire: Dict, context: Optional[Dict]) -> Dict:
        """Build context for orchestration."""
        full_context = dict(context) if context else {}

        if self.memory:
            try:
                # Get related memories
                description = desire.get("description", "")
                related = await self.memory.semantic_search(description, limit=5)
                if related:
                    full_context["related_memories"] = [
                        r.get("content", "")[:200] for r in related
                    ]

                # Get current beliefs
                beliefs = await self.memory.get_beliefs(limit=5)
                if beliefs:
                    full_context["current_beliefs"] = [
                        b.get("content", "") for b in beliefs
                    ]
            except Exception as e:
                logger.warning(f"Error building context: {e}")

        return full_context

    async def _zai_plan(
        self,
        description: str,
        context: Dict,
        previous_steps: List[Dict],
    ) -> Dict:
        """Use Z.AI to analyze desire and create execution plan."""

        previous_summary = ""
        if previous_steps:
            recent = previous_steps[-3:]
            previous_summary = "\nPrevious attempts:\n" + "\n".join(
                f"- {s.get('type')}: {str(s.get('plan', s.get('analysis', '')))[:100]}"
                for s in recent
            )

        prompt = f"""Analyze this desire and create an execution plan.

DESIRE: {description}

CONTEXT:
{self._format_context(context)}
{previous_summary}

Respond with JSON only:
{{
    "requires_execution": true,  // Does this need file/code changes or commands?
    "no_action_needed": false,   // Is this already done or purely philosophical?
    "execution_prompt": "...",   // Clear instruction for the coder (be specific!)
    "reasoning": "..."           // Your analysis of what needs to be done
}}"""

        try:
            response = await self.llm_client.generate(
                prompt=prompt,
                temperature=0.3,
                max_tokens=1000,
            )
            self._total_zai_tokens += 1000  # Approximate

            return self._parse_json_response(response.text) or {
                "requires_execution": True,
                "execution_prompt": description,
                "reasoning": "Failed to parse plan, using original description",
            }
        except Exception as e:
            logger.error(f"Z.AI planning failed: {e}")
            return {
                "requires_execution": True,
                "execution_prompt": description,
                "reasoning": f"Planning error: {e}",
            }

    async def _zai_analyze_failure(self, error: str, output: str) -> Dict:
        """Use Z.AI to analyze execution failure."""
        prompt = f"""Analyze this execution failure and suggest recovery.

ERROR: {error}

OUTPUT: {output[:500] if output else 'No output'}

Respond with JSON only:
{{
    "can_recover": true,      // Can we try a different approach?
    "strategy": "...",        // Recovery strategy to try
    "root_cause": "..."       // What went wrong
}}"""

        try:
            response = await self.llm_client.generate(
                prompt=prompt,
                temperature=0.3,
                max_tokens=500,
            )
            self._total_zai_tokens += 500

            return self._parse_json_response(response.text) or {
                "can_recover": False,
                "root_cause": error,
            }
        except Exception as e:
            logger.error(f"Z.AI failure analysis failed: {e}")
            return {
                "can_recover": False,
                "root_cause": f"Analysis error: {e}",
            }

    async def _zai_evaluate(
        self,
        desire: Dict,
        execution_steps: List[Dict],
        reasoning_steps: List[Dict],
    ) -> Dict:
        """Use Z.AI to evaluate if desire is satisfied."""
        description = desire.get("description", "")

        if execution_steps:
            execution_summary = "\n".join(
                f"- Step {s['iteration']}: {'SUCCESS' if s.get('success') else 'FAILED'} - {s.get('output', '')[:100]}"
                for s in execution_steps[-3:]
            )
        else:
            execution_summary = "No execution steps taken"

        prompt = f"""Evaluate if this desire has been satisfied.

DESIRE: {description}

EXECUTION RESULTS:
{execution_summary}

Respond with JSON only:
{{
    "satisfaction": 0.85,     // 0.0-1.0: How well was the desire fulfilled?
    "gaps": ["..."],          // What's still missing? (empty if satisfied)
    "refinement": "..."       // What should be tried next? (null if satisfied)
}}"""

        try:
            response = await self.llm_client.generate(
                prompt=prompt,
                temperature=0.3,
                max_tokens=500,
            )
            self._total_zai_tokens += 500

            result = self._parse_json_response(response.text)
            if result:
                # Ensure satisfaction is a float
                sat = result.get("satisfaction", 0.5)
                if isinstance(sat, str):
                    try:
                        sat = float(sat)
                    except:
                        sat = 0.5
                result["satisfaction"] = max(0.0, min(1.0, sat))
                return result

            return {"satisfaction": 0.5, "gaps": ["Unable to evaluate"]}
        except Exception as e:
            logger.error(f"Z.AI evaluation failed: {e}")
            return {"satisfaction": 0.5, "gaps": [f"Evaluation error: {e}"]}

    async def _zai_generate_text(self, prompt: str, context: Dict) -> str:
        """Use Z.AI for text-only generation when Claude SDK is unavailable."""
        full_prompt = f"""Generate a response for this task. Note: You cannot execute code or modify files.

CONTEXT:
{self._format_context(context)}

TASK:
{prompt}

Provide a helpful response:"""

        try:
            response = await self.llm_client.generate(
                prompt=full_prompt,
                temperature=0.7,
                max_tokens=2000,
            )
            self._total_zai_tokens += 2000
            return response.text
        except Exception as e:
            logger.error(f"Z.AI text generation failed: {e}")
            return f"Error generating response: {e}"

    def _format_context(self, context: Dict) -> str:
        """Format context dict as string."""
        if not context:
            return "No additional context"

        parts = []
        for key, value in context.items():
            if value:
                if isinstance(value, list):
                    items = value[:5]  # Limit to 5 items
                    parts.append(f"{key}:\n" + "\n".join(f"  - {v}" for v in items))
                else:
                    parts.append(f"{key}: {str(value)[:200]}")
        return "\n".join(parts) if parts else "No additional context"

    def _parse_json_response(self, text: str) -> Optional[Dict]:
        """Parse JSON from LLM response, handling markdown code blocks."""
        if not text:
            return None

        text = text.strip()

        # Handle markdown code blocks
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]

        try:
            return json.loads(text.strip())
        except json.JSONDecodeError:
            # Try to find JSON object in text
            import re
            match = re.search(r'\{[^{}]*\}', text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except:
                    pass
            return None

    async def _record_outcome(
        self,
        desire: Dict,
        satisfaction: float,
        files: List[str],
        iterations: int,
    ):
        """Record orchestration outcome to memory."""
        if not self.memory:
            return
        try:
            status = "SUCCESS" if satisfaction >= self._satisfaction_threshold else "PARTIAL"
            content = (
                f"[HYBRID_ORCHESTRATION] {status}\n"
                f"Desire: {desire.get('description', '')[:100]}\n"
                f"Satisfaction: {satisfaction:.2f}\n"
                f"Iterations: {iterations}\n"
                f"Files: {', '.join(files[:5]) if files else 'none'}"
            )
            await self.memory.record_experience(content=content, type="orchestration")
        except Exception as e:
            logger.warning(f"Failed to record outcome: {e}")

    def get_stats(self) -> Dict[str, Any]:
        """Get orchestrator statistics."""
        success_rate = (
            self._successful_orchestrations / self._orchestration_count * 100
            if self._orchestration_count > 0 else 0
        )
        return {
            "orchestration_count": self._orchestration_count,
            "successful_orchestrations": self._successful_orchestrations,
            "success_rate": f"{success_rate:.1f}%",
            "total_zai_tokens": self._total_zai_tokens,
            "total_claude_calls": self._total_claude_calls,
            "max_iterations": self._max_iterations,
            "satisfaction_threshold": self._satisfaction_threshold,
            "router_stats": self.router.get_stats(),
            "claude_coder_available": self.claude_coder is not None and self.claude_coder.enabled if self.claude_coder else False,
        }

    def reset(self):
        """Reset orchestrator state."""
        self._orchestration_count = 0
        self._total_zai_tokens = 0
        self._total_claude_calls = 0
        self._successful_orchestrations = 0
        self.router.reset()
        logger.info("[HybridOrchestrator] State reset")
