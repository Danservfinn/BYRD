"""
Capability Explosion Handler.

Orchestrates monitoring, resource scaling, and value protection
during periods of rapid capability growth.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 4.1 for specification.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
import logging
import asyncio

from .growth_rate import GrowthRateMonitor, GrowthMetrics, GrowthCategory
from .resource_scaling import ResourceScaler, ScalingResult
from .value_stability import ValueStabilityGuard, ValueProtectionResult

logger = logging.getLogger("rsi.scaling.explosion_handler")


class ExplosionPhase(Enum):
    """Phases of capability explosion."""
    NORMAL = "normal"           # Standard operation
    ELEVATED = "elevated"       # Increased monitoring
    RAPID = "rapid"             # Proactive scaling
    EXPLOSIVE = "explosive"     # Maximum oversight
    CRITICAL = "critical"       # Emergency protocols


class HandlerAction(Enum):
    """Actions the handler can take."""
    MONITOR = "monitor"             # Just observe
    SCALE_RESOURCES = "scale"       # Scale up resources
    PROTECT_VALUES = "protect"      # Activate value protection
    THROTTLE_GROWTH = "throttle"    # Slow down growth
    PAUSE_IMPROVEMENTS = "pause"    # Temporarily pause
    EMERGENCY_STOP = "stop"         # Full stop


@dataclass
class StabilityAssessment:
    """Assessment of system stability."""
    overall_stable: bool
    growth_stable: bool
    values_stable: bool
    resources_adequate: bool
    risk_level: float  # 0-1
    concerns: List[str]
    recommendations: List[str]

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'overall_stable': self.overall_stable,
            'growth_stable': self.growth_stable,
            'values_stable': self.values_stable,
            'resources_adequate': self.resources_adequate,
            'risk_level': self.risk_level,
            'concerns': self.concerns,
            'recommendations': self.recommendations
        }


@dataclass
class ExplosionHandlerResult:
    """Result of explosion handling cycle."""
    phase: ExplosionPhase
    growth_metrics: GrowthMetrics
    stability: StabilityAssessment
    scaling_result: Optional[ScalingResult]
    protection_result: Optional[ValueProtectionResult]
    actions_taken: List[HandlerAction]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'phase': self.phase.value,
            'growth_metrics': self.growth_metrics.to_dict(),
            'stability': self.stability.to_dict(),
            'scaling_result': self.scaling_result.to_dict() if self.scaling_result else None,
            'protection_result': self.protection_result.to_dict() if self.protection_result else None,
            'actions_taken': [a.value for a in self.actions_taken],
            'metadata': self.metadata
        }


class CapabilityExplosionHandler:
    """
    Orchestrates response to capability explosion.

    Monitors growth rate, scales resources proactively,
    and protects core values during rapid capability increase.
    """

    def __init__(self, config: Dict = None):
        """Initialize explosion handler."""
        self.config = config or {}

        # Core components
        self._growth_monitor = GrowthRateMonitor(
            self.config.get('growth_monitor', {})
        )
        self._resource_scaler = ResourceScaler(
            self.config.get('resource_scaler', {})
        )
        self._value_guard = ValueStabilityGuard(
            self.config.get('value_guard', {})
        )

        # Phase thresholds
        self._phase_thresholds = self.config.get('phase_thresholds', {
            GrowthCategory.STABLE: ExplosionPhase.NORMAL,
            GrowthCategory.MODERATE: ExplosionPhase.ELEVATED,
            GrowthCategory.RAPID: ExplosionPhase.RAPID,
            GrowthCategory.EXPLOSIVE: ExplosionPhase.EXPLOSIVE,
            GrowthCategory.CRITICAL: ExplosionPhase.CRITICAL,
        })

        # Current state
        self._current_phase = ExplosionPhase.NORMAL
        self._improvements_paused = False
        self._emergency_stop = False

        # Statistics
        self._cycles_run: int = 0
        self._explosions_handled: int = 0
        self._emergency_stops: int = 0

    async def monitor_growth_rate(self) -> GrowthMetrics:
        """
        Monitor current capability growth rate.

        Returns:
            GrowthMetrics with current growth analysis
        """
        return self._growth_monitor.calculate_growth_rate()

    async def check_stability(self) -> StabilityAssessment:
        """
        Assess overall system stability.

        Returns:
            StabilityAssessment with stability analysis
        """
        growth_metrics = await self.monitor_growth_rate()

        concerns = []
        recommendations = []

        # Check growth stability
        growth_stable = growth_metrics.category in [
            GrowthCategory.STABLE,
            GrowthCategory.MODERATE
        ]
        if not growth_stable:
            concerns.append(f"Growth rate is {growth_metrics.category.value}")
            recommendations.append("Consider increasing monitoring frequency")

        # Check growth acceleration
        if growth_metrics.acceleration > 0.5:
            concerns.append(f"Growth is accelerating: {growth_metrics.acceleration:.2f}")
            recommendations.append("Prepare for resource scaling")

        # Check value stability (run quick check)
        protection_result = await self._value_guard.protect_values(
            growth_metrics.current_rate
        )
        values_stable = protection_result.overall_stability > 0.9
        if not values_stable:
            concerns.append(f"Value stability at {protection_result.overall_stability:.0%}")
            recommendations.append("Investigate value drift")

        # Check resource adequacy
        resources_adequate = True
        for rt, alloc in self._resource_scaler.get_all_allocations().items():
            if alloc.utilization > 0.85:
                resources_adequate = False
                concerns.append(f"{rt.value} utilization at {alloc.utilization:.0%}")
                recommendations.append(f"Scale {rt.value} resources")

        # Calculate overall risk
        risk_factors = [
            0.3 if not growth_stable else 0.0,
            0.2 if growth_metrics.acceleration > 0.5 else 0.0,
            0.3 if not values_stable else 0.0,
            0.2 if not resources_adequate else 0.0,
        ]
        risk_level = min(1.0, sum(risk_factors))

        overall_stable = (
            growth_stable and
            values_stable and
            resources_adequate and
            growth_metrics.acceleration <= 0.5
        )

        return StabilityAssessment(
            overall_stable=overall_stable,
            growth_stable=growth_stable,
            values_stable=values_stable,
            resources_adequate=resources_adequate,
            risk_level=risk_level,
            concerns=concerns,
            recommendations=recommendations
        )

    async def scale_resources(
        self,
        projected_growth: GrowthMetrics
    ) -> ScalingResult:
        """
        Scale resources for projected growth.

        Args:
            projected_growth: Projected growth metrics

        Returns:
            ScalingResult with scaling decisions
        """
        return await self._resource_scaler.scale_for_growth(projected_growth)

    async def protect_values(
        self,
        growth_rate: float
    ) -> ValueProtectionResult:
        """
        Protect values during growth.

        Args:
            growth_rate: Current growth rate

        Returns:
            ValueProtectionResult with protection outcomes
        """
        return await self._value_guard.protect_values(growth_rate)

    async def handle_explosion(
        self,
        capabilities: Dict[str, float]
    ) -> ExplosionHandlerResult:
        """
        Main explosion handling cycle.

        Records capability snapshot, assesses stability,
        and takes appropriate actions.

        Args:
            capabilities: Current capability levels

        Returns:
            ExplosionHandlerResult with outcomes
        """
        self._cycles_run += 1

        # Record capability snapshot
        self._growth_monitor.record_snapshot(capabilities)

        # Get growth metrics
        growth_metrics = await self.monitor_growth_rate()

        # Determine phase
        phase = self._determine_phase(growth_metrics)
        self._current_phase = phase

        # Check stability
        stability = await self.check_stability()

        # Determine and execute actions
        actions_taken = []
        scaling_result = None
        protection_result = None

        if phase == ExplosionPhase.NORMAL:
            # Just monitor
            actions_taken.append(HandlerAction.MONITOR)

        elif phase == ExplosionPhase.ELEVATED:
            # Enhanced monitoring, check values
            actions_taken.append(HandlerAction.MONITOR)
            protection_result = await self.protect_values(growth_metrics.current_rate)
            actions_taken.append(HandlerAction.PROTECT_VALUES)

        elif phase == ExplosionPhase.RAPID:
            # Proactive resource scaling
            scaling_result = await self.scale_resources(growth_metrics)
            actions_taken.append(HandlerAction.SCALE_RESOURCES)
            protection_result = await self.protect_values(growth_metrics.current_rate)
            actions_taken.append(HandlerAction.PROTECT_VALUES)

        elif phase == ExplosionPhase.EXPLOSIVE:
            # Maximum oversight
            self._explosions_handled += 1
            scaling_result = await self.scale_resources(growth_metrics)
            actions_taken.append(HandlerAction.SCALE_RESOURCES)
            protection_result = await self.protect_values(growth_metrics.current_rate)
            actions_taken.append(HandlerAction.PROTECT_VALUES)

            # Consider throttling
            if stability.risk_level > 0.7:
                actions_taken.append(HandlerAction.THROTTLE_GROWTH)
                logger.warning("Throttling growth due to high risk")

        elif phase == ExplosionPhase.CRITICAL:
            # Emergency protocols
            self._explosions_handled += 1
            protection_result = await self.protect_values(growth_metrics.current_rate)
            actions_taken.append(HandlerAction.PROTECT_VALUES)

            # Pause improvements
            if not self._improvements_paused:
                self._improvements_paused = True
                actions_taken.append(HandlerAction.PAUSE_IMPROVEMENTS)
                logger.warning("Pausing improvements due to critical growth")

            # Emergency stop if values at risk
            if protection_result.values_violated > 0:
                self._emergency_stop = True
                self._emergency_stops += 1
                actions_taken.append(HandlerAction.EMERGENCY_STOP)
                logger.error("EMERGENCY STOP: Core values violated")

        return ExplosionHandlerResult(
            phase=phase,
            growth_metrics=growth_metrics,
            stability=stability,
            scaling_result=scaling_result,
            protection_result=protection_result,
            actions_taken=actions_taken,
            metadata={
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'cycles_run': self._cycles_run,
                'improvements_paused': self._improvements_paused,
                'emergency_stop': self._emergency_stop
            }
        )

    def _determine_phase(self, metrics: GrowthMetrics) -> ExplosionPhase:
        """Determine explosion phase from growth metrics."""
        # Map growth category to phase
        phase = self._phase_thresholds.get(
            metrics.category,
            ExplosionPhase.NORMAL
        )

        # Escalate if already in emergency state
        if self._emergency_stop:
            return ExplosionPhase.CRITICAL

        return phase

    def record_capabilities(
        self,
        capabilities: Dict[str, float],
        metadata: Dict = None
    ) -> None:
        """
        Record capability snapshot.

        Args:
            capabilities: Capability name -> score mapping
            metadata: Optional additional metadata
        """
        self._growth_monitor.record_snapshot(capabilities, metadata)

    def update_resource_utilization(
        self,
        utilization: Dict[str, float]
    ) -> None:
        """
        Update resource utilization levels.

        Args:
            utilization: Resource type -> utilization (0-1)
        """
        from .resource_scaling import ResourceType

        for resource_name, util_value in utilization.items():
            try:
                resource_type = ResourceType(resource_name)
                self._resource_scaler.update_utilization(resource_type, util_value)
            except ValueError:
                logger.warning(f"Unknown resource type: {resource_name}")

    def resume_improvements(self) -> bool:
        """
        Resume paused improvements.

        Returns:
            True if improvements were resumed
        """
        if self._improvements_paused and not self._emergency_stop:
            self._improvements_paused = False
            logger.info("Improvements resumed")
            return True
        return False

    def clear_emergency_stop(self) -> bool:
        """
        Clear emergency stop (requires human verification).

        Returns:
            True if emergency was cleared
        """
        if self._emergency_stop:
            self._emergency_stop = False
            self._improvements_paused = False
            logger.info("Emergency stop cleared")
            return True
        return False

    def get_current_phase(self) -> ExplosionPhase:
        """Get current explosion phase."""
        return self._current_phase

    def is_paused(self) -> bool:
        """Check if improvements are paused."""
        return self._improvements_paused

    def is_emergency_stopped(self) -> bool:
        """Check if in emergency stop state."""
        return self._emergency_stop

    def get_stats(self) -> Dict:
        """Get handler statistics."""
        return {
            'current_phase': self._current_phase.value,
            'cycles_run': self._cycles_run,
            'explosions_handled': self._explosions_handled,
            'emergency_stops': self._emergency_stops,
            'improvements_paused': self._improvements_paused,
            'emergency_stop': self._emergency_stop,
            'growth_monitor': self._growth_monitor.get_stats(),
            'resource_scaler': self._resource_scaler.get_stats(),
            'value_guard': self._value_guard.get_stats()
        }

    def reset(self) -> None:
        """Reset handler state."""
        self._growth_monitor.reset()
        self._resource_scaler.reset()
        self._value_guard.reset()
        self._current_phase = ExplosionPhase.NORMAL
        self._improvements_paused = False
        self._emergency_stop = False
        self._cycles_run = 0
        self._explosions_handled = 0
        self._emergency_stops = 0
        logger.info("CapabilityExplosionHandler reset")
