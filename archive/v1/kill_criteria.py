"""
BYRD Kill Criteria
Evaluation framework for Option B success/failure.

Kill criteria provide objective triggers for project evaluation:
- HARD TRIGGERS: Stop and re-evaluate fundamental approach
- SOFT TRIGGERS: Warning signs, consider simplifying

THE PHILOSOPHY: Honest measurement beats wishful thinking.
If BYRD isn't improving, we need to know and adapt.
"""

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

from event_bus import event_bus, Event, EventType

logger = logging.getLogger(__name__)


class TriggerSeverity(Enum):
    """Severity level of a triggered criterion."""
    SOFT = "soft"       # Warning, consider action
    HARD = "hard"       # Stop and re-evaluate


class TriggerType(Enum):
    """Types of kill criteria."""
    GROWTH_RATE_NEGATIVE = "growth_rate_negative"
    GROWTH_RATE_LOW = "growth_rate_low"
    LLM_RATIO_HIGH = "llm_ratio_high"
    COUPLING_LOW = "coupling_low"
    COUPLING_LOW_EXTENDED = "coupling_low_extended"
    LOOP_INACTIVE = "loop_inactive"


@dataclass
class KillTrigger:
    """A triggered kill criterion."""
    type: TriggerType
    severity: TriggerSeverity
    message: str
    value: float
    threshold: float
    triggered_at: datetime = field(default_factory=datetime.now)


@dataclass
class KillCriteriaConfig:
    """Configuration for kill criteria thresholds."""
    # Hard triggers
    growth_rate_negative_days: int = 7
    llm_ratio_above: float = 0.95
    coupling_below_for_days: int = 14

    # Soft triggers
    growth_rate_below: float = 0.01
    coupling_below: float = 0.3
    loop_inactive_hours: float = 24.0


class KillCriteriaEvaluator:
    """
    Evaluates kill criteria for Option B.

    Monitors key metrics and triggers warnings/stops when
    thresholds are crossed.
    """

    def __init__(
        self,
        config: Optional[Dict] = None
    ):
        """
        Initialize the evaluator.

        Args:
            config: Configuration from config.yaml option_b.metrics.kill_criteria
        """
        self.config = config or {}

        # Parse configuration
        hard = self.config.get("hard", {})
        soft = self.config.get("soft", {})

        self.thresholds = KillCriteriaConfig(
            growth_rate_negative_days=hard.get("growth_rate_negative_days", 7),
            llm_ratio_above=hard.get("llm_ratio_above", 0.95),
            coupling_below_for_days=hard.get("coupling_below_for_days", 14),
            growth_rate_below=soft.get("growth_rate_below", 0.01),
            coupling_below=soft.get("coupling_below", 0.3),
            loop_inactive_hours=soft.get("loop_inactive_hours", 24.0),
        )

        # History tracking for extended criteria
        self._growth_rate_history: List[Tuple[datetime, float]] = []
        self._coupling_history: List[Tuple[datetime, float]] = []
        self._loop_activity: Dict[str, datetime] = {}

        # Active triggers
        self._active_triggers: List[KillTrigger] = []

    def record_growth_rate(self, rate: float):
        """Record a growth rate measurement."""
        self._growth_rate_history.append((datetime.now(), rate))
        # Keep last 30 days
        cutoff = datetime.now() - timedelta(days=30)
        self._growth_rate_history = [
            (t, r) for t, r in self._growth_rate_history if t > cutoff
        ]

    def record_coupling(self, coupling: float):
        """Record a coupling measurement."""
        self._coupling_history.append((datetime.now(), coupling))
        # Keep last 30 days
        cutoff = datetime.now() - timedelta(days=30)
        self._coupling_history = [
            (t, c) for t, c in self._coupling_history if t > cutoff
        ]

    def record_loop_activity(self, loop_name: str):
        """Record that a loop was active."""
        self._loop_activity[loop_name] = datetime.now()

    def evaluate(
        self,
        growth_rate: float,
        llm_ratio: float,
        critical_coupling: float,
        loop_health: Dict[str, bool]
    ) -> List[KillTrigger]:
        """
        Evaluate all kill criteria.

        Args:
            growth_rate: Current capability growth rate (per hour)
            llm_ratio: Ratio of queries answered by LLM (vs memory)
            critical_coupling: Goal Evolver → Self-Compiler coupling
            loop_health: Health status of each loop

        Returns:
            List of triggered criteria
        """
        self._active_triggers = []

        # Record metrics
        self.record_growth_rate(growth_rate)
        self.record_coupling(critical_coupling)

        # Evaluate each criterion
        self._check_growth_rate(growth_rate)
        self._check_llm_ratio(llm_ratio)
        self._check_coupling(critical_coupling)
        self._check_loop_activity(loop_health)

        # Emit event if any triggers
        if self._active_triggers:
            await_triggers = [
                t for t in self._active_triggers
                if t.severity == TriggerSeverity.HARD
            ]

            # Log triggers
            for trigger in self._active_triggers:
                level = logging.ERROR if trigger.severity == TriggerSeverity.HARD else logging.WARNING
                logger.log(level, f"Kill criterion triggered: {trigger.message}")

        return self._active_triggers

    def _check_growth_rate(self, current_rate: float):
        """Check growth rate criteria."""
        # Hard: Negative growth for N days
        if len(self._growth_rate_history) >= 2:
            days_ago = datetime.now() - timedelta(days=self.thresholds.growth_rate_negative_days)
            recent = [r for t, r in self._growth_rate_history if t > days_ago]

            if recent and all(r < 0 for r in recent) and len(recent) >= 3:
                self._active_triggers.append(KillTrigger(
                    type=TriggerType.GROWTH_RATE_NEGATIVE,
                    severity=TriggerSeverity.HARD,
                    message=f"Growth rate negative for {self.thresholds.growth_rate_negative_days}+ days",
                    value=current_rate,
                    threshold=0.0
                ))

        # Soft: Growth rate below threshold
        if current_rate < self.thresholds.growth_rate_below and current_rate >= 0:
            self._active_triggers.append(KillTrigger(
                type=TriggerType.GROWTH_RATE_LOW,
                severity=TriggerSeverity.SOFT,
                message=f"Growth rate {current_rate:.4f} below threshold {self.thresholds.growth_rate_below}",
                value=current_rate,
                threshold=self.thresholds.growth_rate_below
            ))

    def _check_llm_ratio(self, ratio: float):
        """Check LLM dependency ratio."""
        # Hard: LLM answering too many queries
        if ratio > self.thresholds.llm_ratio_above:
            self._active_triggers.append(KillTrigger(
                type=TriggerType.LLM_RATIO_HIGH,
                severity=TriggerSeverity.HARD,
                message=f"LLM ratio {ratio:.2%} above {self.thresholds.llm_ratio_above:.0%} - not learning from memory",
                value=ratio,
                threshold=self.thresholds.llm_ratio_above
            ))

    def _check_coupling(self, coupling: float):
        """Check coupling criteria."""
        # Hard: Coupling below minimum for extended period
        if len(self._coupling_history) >= 2:
            days_ago = datetime.now() - timedelta(days=self.thresholds.coupling_below_for_days)
            recent = [c for t, c in self._coupling_history if t > days_ago]

            if recent and all(c < 0.1 for c in recent) and len(recent) >= 5:
                self._active_triggers.append(KillTrigger(
                    type=TriggerType.COUPLING_LOW_EXTENDED,
                    severity=TriggerSeverity.HARD,
                    message=f"Critical coupling below 0.1 for {self.thresholds.coupling_below_for_days}+ days",
                    value=coupling,
                    threshold=0.1
                ))

        # Soft: Coupling below threshold
        if coupling < self.thresholds.coupling_below:
            self._active_triggers.append(KillTrigger(
                type=TriggerType.COUPLING_LOW,
                severity=TriggerSeverity.SOFT,
                message=f"Critical coupling {coupling:.2f} below threshold {self.thresholds.coupling_below}",
                value=coupling,
                threshold=self.thresholds.coupling_below
            ))

    def _check_loop_activity(self, loop_health: Dict[str, bool]):
        """Check loop activity criteria."""
        now = datetime.now()
        inactive_threshold = timedelta(hours=self.thresholds.loop_inactive_hours)

        for loop_name, healthy in loop_health.items():
            last_active = self._loop_activity.get(loop_name)

            if last_active:
                inactive_for = now - last_active
                if inactive_for > inactive_threshold:
                    self._active_triggers.append(KillTrigger(
                        type=TriggerType.LOOP_INACTIVE,
                        severity=TriggerSeverity.SOFT,
                        message=f"Loop '{loop_name}' inactive for {inactive_for.total_seconds()/3600:.1f} hours",
                        value=inactive_for.total_seconds() / 3600,
                        threshold=self.thresholds.loop_inactive_hours
                    ))

    def get_active_triggers(self) -> List[KillTrigger]:
        """Get currently active triggers."""
        return self._active_triggers

    def has_hard_triggers(self) -> bool:
        """Check if any hard triggers are active."""
        return any(t.severity == TriggerSeverity.HARD for t in self._active_triggers)

    def has_soft_triggers(self) -> bool:
        """Check if any soft triggers are active."""
        return any(t.severity == TriggerSeverity.SOFT for t in self._active_triggers)

    def get_summary(self) -> Dict[str, Any]:
        """Get summary of kill criteria status."""
        return {
            "hard_triggers": [
                {
                    "type": t.type.value,
                    "message": t.message,
                    "value": t.value,
                    "threshold": t.threshold
                }
                for t in self._active_triggers
                if t.severity == TriggerSeverity.HARD
            ],
            "soft_triggers": [
                {
                    "type": t.type.value,
                    "message": t.message,
                    "value": t.value,
                    "threshold": t.threshold
                }
                for t in self._active_triggers
                if t.severity == TriggerSeverity.SOFT
            ],
            "growth_rate_samples": len(self._growth_rate_history),
            "coupling_samples": len(self._coupling_history),
            "thresholds": {
                "growth_rate_negative_days": self.thresholds.growth_rate_negative_days,
                "llm_ratio_above": self.thresholds.llm_ratio_above,
                "coupling_below_for_days": self.thresholds.coupling_below_for_days,
                "growth_rate_below": self.thresholds.growth_rate_below,
                "coupling_below": self.thresholds.coupling_below,
                "loop_inactive_hours": self.thresholds.loop_inactive_hours
            }
        }

    async def emit_trigger_event(self, trigger: KillTrigger):
        """Emit an event for a triggered criterion."""
        await event_bus.emit(Event(
            type=EventType.KILL_CRITERION_TRIGGERED,
            data={
                "type": trigger.type.value,
                "severity": trigger.severity.value,
                "message": trigger.message,
                "value": trigger.value,
                "threshold": trigger.threshold
            }
        ))


# Factory function
def create_kill_criteria_evaluator(config: Dict) -> KillCriteriaEvaluator:
    """
    Create a Kill Criteria Evaluator from configuration.

    Args:
        config: Full config.yaml dict

    Returns:
        Configured KillCriteriaEvaluator instance
    """
    kc_config = config.get("option_b", {}).get("metrics", {}).get("kill_criteria", {})
    return KillCriteriaEvaluator(kc_config)
