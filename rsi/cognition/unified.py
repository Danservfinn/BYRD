"""
Unified Cognition API for BYRD RSI.

High-level cognitive operations that abstract away tier management.
All operations route through CognitiveRouter automatically.

Operations:
- think(): General cognitive processing
- reason(): Multi-step reasoning with chain-of-thought
- create(): Creative generation (code, text, ideas)
- evaluate(): Assessment and quality evaluation

Design principle: Simple interface, intelligent routing.
The caller shouldn't care about tiers - just ask for cognition.

See PROMPT.md "Layer 2: Cognitive Tiering" for specification.
"""

from typing import Dict, Optional, Any, List
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import logging
import json

from .tiers import CognitiveTier, get_tier_config
from .router import CognitiveRouter, RoutingContext, RouteResult
from .escalation import EscalationPolicy

logger = logging.getLogger("rsi.cognition.unified")


class CognitiveOperation(Enum):
    """Types of cognitive operations."""
    THINK = "think"
    REASON = "reason"
    CREATE = "create"
    EVALUATE = "evaluate"


@dataclass
class ThinkRequest:
    """Request for general cognitive processing."""
    prompt: str
    context: Optional[str] = None
    max_tokens: int = 2000
    temperature: float = 0.7
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReasonRequest:
    """Request for multi-step reasoning."""
    question: str
    context: Optional[str] = None
    steps: int = 3  # Number of reasoning steps
    max_tokens_per_step: int = 1000
    require_conclusion: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CreateRequest:
    """Request for creative generation."""
    task: str
    output_type: str = "text"  # text, code, json, plan
    context: Optional[str] = None
    constraints: Optional[List[str]] = None
    max_tokens: int = 4000
    temperature: float = 0.8  # Higher for creativity
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EvaluateRequest:
    """Request for assessment and evaluation."""
    content: str
    criteria: List[str]
    context: Optional[str] = None
    score_range: tuple = (0.0, 1.0)
    require_explanation: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CognitiveResult:
    """Result from a cognitive operation."""
    success: bool
    operation: CognitiveOperation
    content: str
    tier_used: CognitiveTier
    quality_score: Optional[float] = None
    cost: float = 0.0
    latency_ms: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'success': self.success,
            'operation': self.operation.value,
            'content_length': len(self.content),
            'tier_used': self.tier_used.value,
            'quality_score': self.quality_score,
            'cost': self.cost,
            'latency_ms': self.latency_ms,
            'metadata': self.metadata,
            'error': self.error
        }

    def parse_json(self) -> Optional[Dict]:
        """Parse content as JSON if applicable."""
        try:
            # Handle markdown code blocks
            text = self.content.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            return json.loads(text.strip())
        except (json.JSONDecodeError, IndexError):
            return None


class UnifiedCognition:
    """
    Unified cognitive interface for BYRD.

    Provides high-level cognitive operations that automatically
    route to the appropriate tier based on task requirements.

    Usage:
        cognition = UnifiedCognition(llm_client)

        # Simple thinking
        result = await cognition.think(ThinkRequest(prompt="Analyze this code"))

        # Multi-step reasoning
        result = await cognition.reason(ReasonRequest(question="Why did the test fail?"))

        # Creative generation
        result = await cognition.create(CreateRequest(task="Write a function to..."))

        # Evaluation
        result = await cognition.evaluate(EvaluateRequest(content="...", criteria=["accuracy"]))
    """

    def __init__(
        self,
        llm_client=None,
        router: Optional[CognitiveRouter] = None,
        config: Dict = None
    ):
        """
        Initialize unified cognition.

        Args:
            llm_client: LLM client for making calls (from core/llm_client.py)
            router: Optional pre-configured router
            config: Configuration options
        """
        self.config = config or {}
        self._llm_client = llm_client
        self._router = router

        # Create router if not provided
        if self._router is None:
            self._router = CognitiveRouter(
                llm_call_fn=self._make_llm_call,
                escalation_policy=EscalationPolicy(self.config.get('escalation', {})),
                config=self.config.get('router', {})
            )
        else:
            self._router.set_llm_call_fn(self._make_llm_call)

        # Operation tracking
        self._operation_count = {op: 0 for op in CognitiveOperation}
        self._total_cost = 0.0

    def set_llm_client(self, client):
        """Set the LLM client."""
        self._llm_client = client

    async def _make_llm_call(
        self,
        tier: CognitiveTier,
        prompt: str,
        kwargs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Make an LLM call for the specified tier.

        This is the callback used by CognitiveRouter.
        """
        if self._llm_client is None:
            raise RuntimeError("No LLM client configured")

        tier_config = get_tier_config(tier)

        # For now, we use the same client for all tiers
        # In future, different tiers may use different providers
        response = await self._llm_client.generate(
            prompt=prompt,
            temperature=kwargs.get('temperature', 0.7),
            max_tokens=kwargs.get('max_tokens', 2000),
            quantum_modulation=kwargs.get('quantum_modulation', False),
            quantum_context=kwargs.get('quantum_context', tier_config.name)
        )

        return {
            'text': response.text,
            'raw': response.raw,
            'model': response.model,
            'provider': response.provider,
            'quantum_influence': response.quantum_influence
        }

    async def think(self, request: ThinkRequest) -> CognitiveResult:
        """
        General cognitive processing.

        Args:
            request: ThinkRequest with prompt and options

        Returns:
            CognitiveResult with response
        """
        # Build prompt
        prompt = request.prompt
        if request.context:
            prompt = f"Context:\n{request.context}\n\nTask:\n{request.prompt}"

        # Create routing context
        context = RoutingContext(
            task_type="think",
            prompt=prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            metadata=request.metadata
        )

        # Route and execute
        result = await self._router.route(context)

        # Track
        self._operation_count[CognitiveOperation.THINK] += 1
        self._total_cost += result.actual_cost

        return CognitiveResult(
            success=result.success,
            operation=CognitiveOperation.THINK,
            content=result.response_text,
            tier_used=result.tier_used,
            quality_score=result.quality_score,
            cost=result.actual_cost,
            latency_ms=result.latency_ms,
            metadata={'routing': result.to_dict()},
            error=result.error
        )

    async def reason(self, request: ReasonRequest) -> CognitiveResult:
        """
        Multi-step reasoning with chain-of-thought.

        Args:
            request: ReasonRequest with question and options

        Returns:
            CognitiveResult with reasoning chain and conclusion
        """
        # Build chain-of-thought prompt
        prompt_parts = []

        if request.context:
            prompt_parts.append(f"Context:\n{request.context}")

        prompt_parts.append(f"""Question: {request.question}

Think through this step by step:""")

        for i in range(request.steps):
            prompt_parts.append(f"\nStep {i + 1}:")

        if request.require_conclusion:
            prompt_parts.append("\n\nConclusion:")

        prompt = "\n".join(prompt_parts)

        # Reasoning tasks may need higher quality threshold
        context = RoutingContext(
            task_type="reason",
            prompt=prompt,
            max_tokens=request.max_tokens_per_step * request.steps + 500,
            temperature=0.5,  # Lower for reasoning
            min_quality_threshold=0.75,  # Higher for reasoning
            requires_validation=True,  # Reasoning should be validated
            metadata=request.metadata
        )

        # Route and execute
        result = await self._router.route(context)

        # Track
        self._operation_count[CognitiveOperation.REASON] += 1
        self._total_cost += result.actual_cost

        return CognitiveResult(
            success=result.success,
            operation=CognitiveOperation.REASON,
            content=result.response_text,
            tier_used=result.tier_used,
            quality_score=result.quality_score,
            cost=result.actual_cost,
            latency_ms=result.latency_ms,
            metadata={
                'routing': result.to_dict(),
                'steps_requested': request.steps
            },
            error=result.error
        )

    async def create(self, request: CreateRequest) -> CognitiveResult:
        """
        Creative generation (code, text, ideas).

        Args:
            request: CreateRequest with task and options

        Returns:
            CognitiveResult with generated content
        """
        # Build creation prompt
        prompt_parts = []

        if request.context:
            prompt_parts.append(f"Context:\n{request.context}")

        prompt_parts.append(f"Task: {request.task}")

        if request.output_type == "json":
            prompt_parts.append("\nProvide your response as valid JSON.")
        elif request.output_type == "code":
            prompt_parts.append("\nProvide your response as code with appropriate comments.")

        if request.constraints:
            prompt_parts.append("\nConstraints:")
            for constraint in request.constraints:
                prompt_parts.append(f"- {constraint}")

        prompt = "\n".join(prompt_parts)

        # Creation may need more tokens and higher temperature
        context = RoutingContext(
            task_type="create",
            prompt=prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            metadata=request.metadata
        )

        # Route and execute
        result = await self._router.route(context)

        # Track
        self._operation_count[CognitiveOperation.CREATE] += 1
        self._total_cost += result.actual_cost

        return CognitiveResult(
            success=result.success,
            operation=CognitiveOperation.CREATE,
            content=result.response_text,
            tier_used=result.tier_used,
            quality_score=result.quality_score,
            cost=result.actual_cost,
            latency_ms=result.latency_ms,
            metadata={
                'routing': result.to_dict(),
                'output_type': request.output_type
            },
            error=result.error
        )

    async def evaluate(self, request: EvaluateRequest) -> CognitiveResult:
        """
        Assessment and quality evaluation.

        Args:
            request: EvaluateRequest with content and criteria

        Returns:
            CognitiveResult with evaluation scores
        """
        # Build evaluation prompt
        min_score, max_score = request.score_range
        criteria_str = "\n".join(f"- {c}" for c in request.criteria)

        prompt_parts = []

        if request.context:
            prompt_parts.append(f"Context:\n{request.context}")

        prompt_parts.append(f"""Evaluate the following content:

---
{request.content}
---

Evaluation criteria:
{criteria_str}

Score each criterion on a scale of {min_score} to {max_score}.

Provide your response as JSON:
{{
    "scores": {{
        "<criterion>": <score>,
        ...
    }},
    "overall_score": <average_score>,
    "explanation": "<brief explanation>"
}}""")

        prompt = "\n".join(prompt_parts)

        # Evaluation may be critical
        context = RoutingContext(
            task_type="evaluate",
            prompt=prompt,
            max_tokens=1500,
            temperature=0.3,  # Low for consistent evaluation
            is_critical=True,
            requires_validation=True,
            metadata=request.metadata
        )

        # Route and execute
        result = await self._router.route(context)

        # Track
        self._operation_count[CognitiveOperation.EVALUATE] += 1
        self._total_cost += result.actual_cost

        # Parse evaluation result
        eval_data = None
        if result.success:
            try:
                # Try to parse JSON from response
                text = result.response_text.strip()
                if "```json" in text:
                    text = text.split("```json")[1].split("```")[0]
                elif "```" in text:
                    text = text.split("```")[1].split("```")[0]
                eval_data = json.loads(text.strip())
            except (json.JSONDecodeError, IndexError):
                pass

        return CognitiveResult(
            success=result.success,
            operation=CognitiveOperation.EVALUATE,
            content=result.response_text,
            tier_used=result.tier_used,
            quality_score=eval_data.get('overall_score') if eval_data else None,
            cost=result.actual_cost,
            latency_ms=result.latency_ms,
            metadata={
                'routing': result.to_dict(),
                'evaluation': eval_data
            },
            error=result.error
        )

    def get_stats(self) -> Dict[str, Any]:
        """Get unified cognition statistics."""
        return {
            'operation_counts': {op.value: c for op, c in self._operation_count.items()},
            'total_operations': sum(self._operation_count.values()),
            'total_cost': self._total_cost,
            'router_stats': self._router.get_stats()
        }

    def get_router(self) -> CognitiveRouter:
        """Get the underlying router for direct access."""
        return self._router


def create_cognition(
    llm_client=None,
    config: Dict = None
) -> UnifiedCognition:
    """
    Factory function to create unified cognition instance.

    Args:
        llm_client: LLM client for making calls
        config: Configuration options

    Returns:
        Configured UnifiedCognition
    """
    return UnifiedCognition(
        llm_client=llm_client,
        config=config or {}
    )
