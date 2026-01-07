"""
Escalation Policy for Cognitive Tiering.

Determines when to escalate from GLM 4.7 (Tier 1) to Premium (Tier 2).

CRITICAL DESIGN PRINCIPLE:
  GLM 4.7 is the FREE default. Only escalate when there's a clear reason.
  Every escalation is logged for pattern analysis -> future custom model training.

See PROMPT.md "Layer 2: Cognitive Tiering" for specification.
"""

from typing import Dict, Optional, Any, List
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
import logging

from .tiers import CognitiveTier

logger = logging.getLogger("rsi.cognition.escalation")


class EscalationTrigger(Enum):
    """Reasons for escalating to a higher tier."""

    # Quality failures
    GLM_QUALITY_FAILED = "glm_quality_failed"       # GLM output below threshold
    GLM_PARSE_FAILED = "glm_parse_failed"           # GLM output couldn't be parsed
    GLM_INCOMPLETE = "glm_incomplete"               # GLM output was incomplete

    # Task criticality
    CRITICAL_DECISION = "critical_decision"         # Irreversible or high-stakes
    SAFETY_VALIDATION = "safety_validation"         # Safety-critical verification
    CROSS_VALIDATION = "cross_validation"           # Multi-model verification

    # Capability requirements
    FRONTIER_REASONING = "frontier_reasoning"       # Beyond GLM capabilities
    EXTENDED_CONTEXT = "extended_context"           # Needs >128K context
    SPECIALIZED_TASK = "specialized_task"           # Task-specific requirements

    # Human request
    USER_REQUESTED = "user_requested"               # Human explicitly asked


@dataclass
class EscalationDecision:
    """Decision about whether to escalate."""
    should_escalate: bool
    trigger: Optional[EscalationTrigger] = None
    target_tier: CognitiveTier = CognitiveTier.GLM_4_7
    reason: str = ""
    confidence: float = 1.0
    estimated_cost: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'should_escalate': self.should_escalate,
            'trigger': self.trigger.value if self.trigger else None,
            'target_tier': self.target_tier.value,
            'reason': self.reason,
            'confidence': self.confidence,
            'estimated_cost': self.estimated_cost,
            'metadata': self.metadata
        }


@dataclass
class EscalationRecord:
    """Record of an escalation for pattern analysis."""
    timestamp: str
    trigger: EscalationTrigger
    from_tier: CognitiveTier
    to_tier: CognitiveTier
    task_type: str
    task_hash: str  # For identifying repeated patterns
    cost_incurred: float
    outcome: str  # "success", "failed", "partial"
    should_train_custom: bool = False  # Flag for training candidate

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'timestamp': self.timestamp,
            'trigger': self.trigger.value,
            'from_tier': self.from_tier.value,
            'to_tier': self.to_tier.value,
            'task_type': self.task_type,
            'task_hash': self.task_hash,
            'cost_incurred': self.cost_incurred,
            'outcome': self.outcome,
            'should_train_custom': self.should_train_custom
        }


class EscalationPolicy:
    """
    Policy engine for deciding when to escalate cognitive tiers.

    Design principle: Be conservative with escalation.
    GLM 4.7 is free and should handle 90%+ of tasks.
    """

    def __init__(self, config: Dict = None):
        """
        Initialize escalation policy.

        Args:
            config: Policy configuration options
        """
        self.config = config or {}

        # Quality thresholds
        self._quality_threshold = self.config.get('quality_threshold', 0.7)
        self._max_retries_before_escalate = self.config.get('max_retries', 2)

        # Escalation tracking
        self._escalation_history: List[EscalationRecord] = []
        self._escalation_count = 0
        self._total_escalation_cost = 0.0

        # Pattern tracking for training candidates
        self._task_pattern_counts: Dict[str, int] = {}

    def evaluate(
        self,
        task_type: str,
        context: Dict[str, Any]
    ) -> EscalationDecision:
        """
        Evaluate whether a task should escalate from GLM 4.7.

        Args:
            task_type: Type of cognitive task
            context: Context including quality score, criticality, etc.

        Returns:
            EscalationDecision
        """
        # Extract context
        glm_quality = context.get('glm_quality_score')
        is_critical = context.get('is_critical', False)
        is_safety = context.get('is_safety_critical', False)
        requires_validation = context.get('requires_validation', False)
        retry_count = context.get('retry_count', 0)
        context_tokens = context.get('context_tokens', 0)
        user_requested = context.get('user_requested_premium', False)

        # Rule 1: User explicitly requested premium
        if user_requested:
            return EscalationDecision(
                should_escalate=True,
                trigger=EscalationTrigger.USER_REQUESTED,
                target_tier=CognitiveTier.PREMIUM,
                reason="User explicitly requested premium model",
                confidence=1.0
            )

        # Rule 2: Safety-critical validation
        if is_safety:
            return EscalationDecision(
                should_escalate=True,
                trigger=EscalationTrigger.SAFETY_VALIDATION,
                target_tier=CognitiveTier.PREMIUM,
                reason="Safety-critical task requires premium validation",
                confidence=0.95
            )

        # Rule 3: GLM quality failed threshold after retries
        if glm_quality is not None:
            if glm_quality < self._quality_threshold:
                if retry_count >= self._max_retries_before_escalate:
                    return EscalationDecision(
                        should_escalate=True,
                        trigger=EscalationTrigger.GLM_QUALITY_FAILED,
                        target_tier=CognitiveTier.PREMIUM,
                        reason=f"GLM quality {glm_quality:.2f} below threshold after {retry_count} retries",
                        confidence=0.85
                    )

        # Rule 4: Critical/irreversible decisions require cross-validation
        if is_critical and requires_validation:
            return EscalationDecision(
                should_escalate=True,
                trigger=EscalationTrigger.CROSS_VALIDATION,
                target_tier=CognitiveTier.PREMIUM,
                reason="Critical decision requires cross-validation",
                confidence=0.9
            )

        # Rule 5: Extended context beyond GLM capacity
        if context_tokens > 120000:  # Leave buffer below 128K
            return EscalationDecision(
                should_escalate=True,
                trigger=EscalationTrigger.EXTENDED_CONTEXT,
                target_tier=CognitiveTier.PREMIUM,
                reason=f"Context size {context_tokens} exceeds GLM capacity",
                confidence=1.0
            )

        # Default: No escalation needed
        return EscalationDecision(
            should_escalate=False,
            target_tier=CognitiveTier.GLM_4_7,
            reason="GLM 4.7 sufficient for task",
            confidence=0.9
        )

    def record_escalation(
        self,
        trigger: EscalationTrigger,
        from_tier: CognitiveTier,
        to_tier: CognitiveTier,
        task_type: str,
        task_hash: str,
        cost: float,
        outcome: str
    ) -> None:
        """
        Record an escalation for pattern analysis.

        Args:
            trigger: What triggered the escalation
            from_tier: Source tier
            to_tier: Target tier
            task_type: Type of task
            task_hash: Hash for identifying patterns
            cost: Cost incurred
            outcome: "success", "failed", or "partial"
        """
        record = EscalationRecord(
            timestamp=datetime.now(timezone.utc).isoformat(),
            trigger=trigger,
            from_tier=from_tier,
            to_tier=to_tier,
            task_type=task_type,
            task_hash=task_hash,
            cost_incurred=cost,
            outcome=outcome,
            should_train_custom=False
        )

        self._escalation_history.append(record)
        self._escalation_count += 1
        self._total_escalation_cost += cost

        # Track patterns
        self._task_pattern_counts[task_hash] = (
            self._task_pattern_counts.get(task_hash, 0) + 1
        )

        # Flag for custom training if pattern is frequent
        if self._task_pattern_counts[task_hash] >= 5:
            record.should_train_custom = True
            logger.info(
                f"Task pattern {task_hash} escalated 5+ times - "
                "candidate for custom model training"
            )

        logger.info(
            f"Escalation recorded: {trigger.value} from {from_tier.value} "
            f"to {to_tier.value} (cost: ${cost:.4f})"
        )

    def get_training_candidates(self) -> List[str]:
        """Get task patterns that should be trained into custom models."""
        return [
            task_hash for task_hash, count in self._task_pattern_counts.items()
            if count >= 5
        ]

    def get_escalation_stats(self) -> Dict[str, Any]:
        """Get escalation statistics."""
        trigger_counts = {}
        for record in self._escalation_history:
            trigger_val = record.trigger.value
            trigger_counts[trigger_val] = trigger_counts.get(trigger_val, 0) + 1

        return {
            'total_escalations': self._escalation_count,
            'total_cost': self._total_escalation_cost,
            'by_trigger': trigger_counts,
            'training_candidates': len(self.get_training_candidates()),
            'unique_patterns': len(self._task_pattern_counts)
        }

    def get_recent_escalations(self, limit: int = 20) -> List[Dict]:
        """Get recent escalation records."""
        return [r.to_dict() for r in self._escalation_history[-limit:]]


def should_escalate(
    task_type: str,
    glm_quality: Optional[float] = None,
    is_critical: bool = False,
    is_safety: bool = False,
    context_tokens: int = 0
) -> EscalationDecision:
    """
    Quick check for escalation (stateless convenience function).

    Args:
        task_type: Type of cognitive task
        glm_quality: Quality score from GLM attempt (0-1)
        is_critical: Is this a critical/irreversible decision?
        is_safety: Is this safety-critical?
        context_tokens: Number of context tokens

    Returns:
        EscalationDecision
    """
    policy = EscalationPolicy()
    return policy.evaluate(task_type, {
        'glm_quality_score': glm_quality,
        'is_critical': is_critical,
        'is_safety_critical': is_safety,
        'context_tokens': context_tokens
    })
