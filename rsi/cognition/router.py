"""
Cognitive Router for BYRD RSI.

Routes cognitive requests to appropriate tiers based on:
- Task requirements
- Quality constraints
- Budget limits
- Escalation policy

Design principle: GLM 4.7 FIRST. Always.
Only escalate when there's a clear reason.

See PROMPT.md "Layer 2: Cognitive Tiering" for specification.
"""

from typing import Dict, Optional, Any, Callable, Awaitable, List
from dataclasses import dataclass, field
from datetime import datetime, timezone
import logging
import hashlib

from .tiers import (
    CognitiveTier,
    TierConfig,
    get_tier_config,
    estimate_tier_cost,
    TIER_CONFIGS
)
from .escalation import (
    EscalationPolicy,
    EscalationDecision,
    EscalationTrigger
)

logger = logging.getLogger("rsi.cognition.router")


@dataclass
class RoutingContext:
    """Context for making routing decisions."""
    task_type: str
    prompt: str
    max_tokens: int = 2000
    temperature: float = 0.7

    # Quality requirements
    min_quality_threshold: float = 0.7
    is_critical: bool = False
    is_safety_critical: bool = False
    requires_validation: bool = False

    # Budget constraints
    max_cost: Optional[float] = None  # None = no limit

    # State from previous attempts
    retry_count: int = 0
    previous_quality: Optional[float] = None

    # User preferences
    user_requested_tier: Optional[CognitiveTier] = None

    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'task_type': self.task_type,
            'prompt_hash': hashlib.sha256(self.prompt.encode()).hexdigest()[:16],
            'max_tokens': self.max_tokens,
            'temperature': self.temperature,
            'min_quality_threshold': self.min_quality_threshold,
            'is_critical': self.is_critical,
            'is_safety_critical': self.is_safety_critical,
            'requires_validation': self.requires_validation,
            'max_cost': self.max_cost,
            'retry_count': self.retry_count,
            'previous_quality': self.previous_quality,
            'user_requested_tier': self.user_requested_tier.value if self.user_requested_tier else None,
            'metadata': self.metadata
        }


@dataclass
class RoutingDecision:
    """Decision about which tier to use."""
    tier: CognitiveTier
    reason: str
    estimated_cost: float
    config: TierConfig
    escalation: Optional[EscalationDecision] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'tier': self.tier.value,
            'tier_name': self.config.name,
            'reason': self.reason,
            'estimated_cost': self.estimated_cost,
            'provider': self.config.provider,
            'model': self.config.model,
            'escalation': self.escalation.to_dict() if self.escalation else None
        }


@dataclass
class RouteResult:
    """Result of a routed cognitive request."""
    success: bool
    tier_used: CognitiveTier
    response_text: str
    quality_score: Optional[float] = None
    actual_cost: float = 0.0
    latency_ms: float = 0.0
    was_escalated: bool = False
    escalation_trigger: Optional[EscalationTrigger] = None
    raw_response: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'success': self.success,
            'tier_used': self.tier_used.value,
            'response_text_length': len(self.response_text),
            'quality_score': self.quality_score,
            'actual_cost': self.actual_cost,
            'latency_ms': self.latency_ms,
            'was_escalated': self.was_escalated,
            'escalation_trigger': self.escalation_trigger.value if self.escalation_trigger else None,
            'error': self.error
        }


# Type alias for LLM call function
LLMCallFn = Callable[[CognitiveTier, str, Dict[str, Any]], Awaitable[Dict[str, Any]]]


class CognitiveRouter:
    """
    Routes cognitive requests to appropriate tiers.

    Design principle: Be conservative. GLM 4.7 handles 90%+ of tasks.
    Only escalate when there's evidence it's needed.
    """

    def __init__(
        self,
        llm_call_fn: Optional[LLMCallFn] = None,
        escalation_policy: Optional[EscalationPolicy] = None,
        config: Dict = None
    ):
        """
        Initialize cognitive router.

        Args:
            llm_call_fn: Async function to call LLM: (tier, prompt, kwargs) -> response
            escalation_policy: Policy for tier escalation decisions
            config: Router configuration options
        """
        self.config = config or {}
        self._llm_call_fn = llm_call_fn
        self._escalation_policy = escalation_policy or EscalationPolicy()

        # Tracking
        self._request_count = 0
        self._cost_total = 0.0
        self._tier_usage: Dict[CognitiveTier, int] = {t: 0 for t in CognitiveTier}
        self._recent_routes: List[Dict] = []

        # Quality evaluation callback (optional)
        self._quality_evaluator: Optional[Callable] = None

        # Budget tracking
        self._budget_limit = self.config.get('budget_limit')  # None = unlimited
        self._budget_period_start = datetime.now(timezone.utc)

    def set_llm_call_fn(self, fn: LLMCallFn):
        """Set the LLM call function."""
        self._llm_call_fn = fn

    def set_quality_evaluator(self, evaluator: Callable):
        """Set quality evaluation callback: (response_text, context) -> score."""
        self._quality_evaluator = evaluator

    def decide_tier(self, context: RoutingContext) -> RoutingDecision:
        """
        Decide which tier to use for a request.

        This is a synchronous decision - actual LLM calls are in route().

        Args:
            context: Routing context with task requirements

        Returns:
            RoutingDecision with tier, reason, and estimated cost
        """
        # Check if user explicitly requested a tier
        if context.user_requested_tier is not None:
            tier = context.user_requested_tier
            config = get_tier_config(tier)
            cost = estimate_tier_cost(tier, len(context.prompt) // 4, context.max_tokens)
            return RoutingDecision(
                tier=tier,
                reason=f"User requested {config.name}",
                estimated_cost=cost,
                config=config
            )

        # Build escalation context
        escalation_context = {
            'glm_quality_score': context.previous_quality,
            'is_critical': context.is_critical,
            'is_safety_critical': context.is_safety_critical,
            'requires_validation': context.requires_validation,
            'retry_count': context.retry_count,
            'context_tokens': len(context.prompt) // 4,  # Rough estimate
            'user_requested_premium': False
        }

        # Evaluate escalation
        escalation = self._escalation_policy.evaluate(
            context.task_type,
            escalation_context
        )

        if escalation.should_escalate:
            tier = escalation.target_tier
            config = get_tier_config(tier)
            cost = estimate_tier_cost(tier, len(context.prompt) // 4, context.max_tokens)

            # Check budget constraint
            if self._budget_limit is not None:
                remaining = self._budget_limit - self._cost_total
                if cost > remaining:
                    # Can't afford escalation - stay on GLM 4.7
                    tier = CognitiveTier.GLM_4_7
                    config = get_tier_config(tier)
                    cost = 0.0  # GLM is free
                    return RoutingDecision(
                        tier=tier,
                        reason=f"Budget constraint: ${remaining:.4f} remaining, need ${cost:.4f}",
                        estimated_cost=cost,
                        config=config,
                        escalation=escalation
                    )

            return RoutingDecision(
                tier=tier,
                reason=escalation.reason,
                estimated_cost=cost,
                config=config,
                escalation=escalation
            )

        # Default: Use GLM 4.7 (FREE)
        tier = CognitiveTier.GLM_4_7
        config = get_tier_config(tier)
        return RoutingDecision(
            tier=tier,
            reason="GLM 4.7 sufficient for task",
            estimated_cost=0.0,
            config=config,
            escalation=escalation
        )

    async def route(self, context: RoutingContext) -> RouteResult:
        """
        Route a cognitive request to the appropriate tier.

        This handles the full routing flow:
        1. Decide tier
        2. Make LLM call
        3. Evaluate quality (if evaluator set)
        4. Handle escalation if needed
        5. Track costs and usage

        Args:
            context: Routing context with task requirements

        Returns:
            RouteResult with response and metadata
        """
        if self._llm_call_fn is None:
            return RouteResult(
                success=False,
                tier_used=CognitiveTier.GLM_4_7,
                response_text="",
                error="No LLM call function configured"
            )

        import time
        start_time = time.time()

        # Make initial routing decision
        decision = self.decide_tier(context)

        logger.info(
            f"Routing {context.task_type} to {decision.config.name}: {decision.reason}"
        )

        try:
            # Make LLM call
            call_kwargs = {
                'max_tokens': context.max_tokens,
                'temperature': context.temperature,
                **context.metadata
            }

            response = await self._llm_call_fn(
                decision.tier,
                context.prompt,
                call_kwargs
            )

            response_text = response.get('text', '')
            raw_response = response

            # Evaluate quality if evaluator is set
            quality_score = None
            if self._quality_evaluator is not None:
                try:
                    quality_score = self._quality_evaluator(response_text, context)
                except Exception as e:
                    logger.warning(f"Quality evaluation failed: {e}")

            # Check if we need to escalate due to quality failure
            was_escalated = False
            escalation_trigger = None

            if (quality_score is not None and
                quality_score < context.min_quality_threshold and
                decision.tier == CognitiveTier.GLM_4_7 and
                context.retry_count < 2):

                # Quality below threshold - consider escalation
                new_context = RoutingContext(
                    task_type=context.task_type,
                    prompt=context.prompt,
                    max_tokens=context.max_tokens,
                    temperature=context.temperature,
                    min_quality_threshold=context.min_quality_threshold,
                    is_critical=context.is_critical,
                    is_safety_critical=context.is_safety_critical,
                    requires_validation=context.requires_validation,
                    max_cost=context.max_cost,
                    retry_count=context.retry_count + 1,
                    previous_quality=quality_score,
                    metadata=context.metadata
                )

                # Recursive call with updated context
                escalated_result = await self.route(new_context)

                if escalated_result.success and escalated_result.tier_used != CognitiveTier.GLM_4_7:
                    was_escalated = True
                    escalation_trigger = EscalationTrigger.GLM_QUALITY_FAILED

                    # Record escalation
                    self._escalation_policy.record_escalation(
                        trigger=escalation_trigger,
                        from_tier=CognitiveTier.GLM_4_7,
                        to_tier=escalated_result.tier_used,
                        task_type=context.task_type,
                        task_hash=hashlib.sha256(context.prompt.encode()).hexdigest()[:16],
                        cost=escalated_result.actual_cost,
                        outcome="success"
                    )

                    return escalated_result

            # Calculate actual cost
            actual_cost = estimate_tier_cost(
                decision.tier,
                len(context.prompt) // 4,
                len(response_text) // 4
            )

            # Track usage
            self._request_count += 1
            self._cost_total += actual_cost
            self._tier_usage[decision.tier] = self._tier_usage.get(decision.tier, 0) + 1

            latency_ms = (time.time() - start_time) * 1000

            result = RouteResult(
                success=True,
                tier_used=decision.tier,
                response_text=response_text,
                quality_score=quality_score,
                actual_cost=actual_cost,
                latency_ms=latency_ms,
                was_escalated=was_escalated,
                escalation_trigger=escalation_trigger,
                raw_response=raw_response
            )

            # Record in recent routes
            self._recent_routes.append({
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'task_type': context.task_type,
                'tier': decision.tier.value,
                'cost': actual_cost,
                'quality': quality_score,
                'latency_ms': latency_ms
            })

            # Keep only last 100 routes
            if len(self._recent_routes) > 100:
                self._recent_routes = self._recent_routes[-100:]

            return result

        except Exception as e:
            logger.error(f"Routing failed: {e}")
            return RouteResult(
                success=False,
                tier_used=decision.tier,
                response_text="",
                error=str(e)
            )

    def get_stats(self) -> Dict[str, Any]:
        """Get routing statistics."""
        return {
            'request_count': self._request_count,
            'cost_total': self._cost_total,
            'tier_usage': {t.value: c for t, c in self._tier_usage.items()},
            'glm_percentage': (
                self._tier_usage.get(CognitiveTier.GLM_4_7, 0) / max(self._request_count, 1) * 100
            ),
            'budget_limit': self._budget_limit,
            'budget_remaining': (
                self._budget_limit - self._cost_total if self._budget_limit else None
            ),
            'escalation_stats': self._escalation_policy.get_escalation_stats()
        }

    def get_recent_routes(self, limit: int = 20) -> List[Dict]:
        """Get recent routing decisions."""
        return self._recent_routes[-limit:]

    def reset_budget_period(self):
        """Reset budget tracking for new period."""
        self._cost_total = 0.0
        self._budget_period_start = datetime.now(timezone.utc)
        logger.info("Budget period reset")


def create_router(
    llm_call_fn: Optional[LLMCallFn] = None,
    config: Dict = None
) -> CognitiveRouter:
    """
    Factory function to create a cognitive router.

    Args:
        llm_call_fn: Async function to call LLM
        config: Router configuration

    Returns:
        Configured CognitiveRouter
    """
    return CognitiveRouter(
        llm_call_fn=llm_call_fn,
        config=config or {}
    )
