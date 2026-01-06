"""
Proactive Resource Scaling.

Acquires resources ahead of projected capability growth.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 4.1 for specification.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
import logging

from .growth_rate import GrowthMetrics, GrowthCategory

logger = logging.getLogger("rsi.scaling.resource_scaling")


class ResourceType(Enum):
    """Types of scalable resources."""
    COMPUTE = "compute"
    MEMORY = "memory"
    STORAGE = "storage"
    BANDWIDTH = "bandwidth"
    API_QUOTA = "api_quota"


class ScalingStrategy(Enum):
    """Resource scaling strategies."""
    CONSERVATIVE = "conservative"   # Scale slowly, verify before scaling
    BALANCED = "balanced"           # Moderate scaling with monitoring
    AGGRESSIVE = "aggressive"       # Scale ahead of demand
    REACTIVE = "reactive"           # Scale only when needed


@dataclass
class ResourceAllocation:
    """Current resource allocation."""
    resource_type: ResourceType
    current_amount: float
    max_amount: float
    unit: str
    utilization: float  # 0-1

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'resource_type': self.resource_type.value,
            'current_amount': self.current_amount,
            'max_amount': self.max_amount,
            'unit': self.unit,
            'utilization': self.utilization
        }


@dataclass
class ScalingDecision:
    """Decision about resource scaling."""
    resource_type: ResourceType
    action: str  # "scale_up", "scale_down", "maintain"
    current_amount: float
    target_amount: float
    reason: str
    priority: float  # 0-1, higher = more urgent
    estimated_cost: float = 0.0

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'resource_type': self.resource_type.value,
            'action': self.action,
            'current_amount': self.current_amount,
            'target_amount': self.target_amount,
            'reason': self.reason,
            'priority': self.priority,
            'estimated_cost': self.estimated_cost
        }


@dataclass
class ScalingResult:
    """Result of resource scaling operation."""
    success: bool
    decisions: List[ScalingDecision]
    resources_scaled: List[ResourceType]
    total_cost: float
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'success': self.success,
            'decisions': [d.to_dict() for d in self.decisions],
            'resources_scaled': [r.value for r in self.resources_scaled],
            'total_cost': self.total_cost,
            'metadata': self.metadata
        }


class ResourceScaler:
    """
    Proactively scales resources for projected growth.

    Anticipates capability growth and acquires resources
    before they become bottlenecks.
    """

    def __init__(self, config: Dict = None):
        """Initialize resource scaler."""
        self.config = config or {}

        # Scaling strategy
        self._strategy = ScalingStrategy(
            self.config.get('strategy', 'balanced')
        )

        # Current allocations
        self._allocations: Dict[ResourceType, ResourceAllocation] = {}
        self._initialize_allocations()

        # Scaling parameters
        self._headroom_factor = self.config.get('headroom_factor', 0.2)
        self._scale_up_threshold = self.config.get('scale_up_threshold', 0.8)
        self._scale_down_threshold = self.config.get('scale_down_threshold', 0.3)

        # Cost tracking
        self._total_cost: float = 0.0
        self._scaling_operations: int = 0

    def _initialize_allocations(self) -> None:
        """Initialize default resource allocations."""
        defaults = {
            ResourceType.COMPUTE: (100.0, 1000.0, "vCPU-hours"),
            ResourceType.MEMORY: (16.0, 128.0, "GB"),
            ResourceType.STORAGE: (100.0, 1000.0, "GB"),
            ResourceType.BANDWIDTH: (100.0, 1000.0, "Mbps"),
            ResourceType.API_QUOTA: (1000.0, 100000.0, "requests/hour"),
        }

        for resource_type, (current, max_val, unit) in defaults.items():
            self._allocations[resource_type] = ResourceAllocation(
                resource_type=resource_type,
                current_amount=current,
                max_amount=max_val,
                unit=unit,
                utilization=0.0
            )

    async def scale_for_growth(
        self,
        growth_metrics: GrowthMetrics
    ) -> ScalingResult:
        """
        Scale resources based on projected growth.

        Args:
            growth_metrics: Current growth metrics

        Returns:
            ScalingResult with decisions and outcomes
        """
        decisions = []
        scaled_resources = []

        # Calculate required scaling for each resource
        for resource_type, allocation in self._allocations.items():
            decision = self._calculate_scaling_decision(
                allocation,
                growth_metrics
            )

            if decision.action != "maintain":
                decisions.append(decision)

                # Execute scaling
                success = await self._execute_scaling(decision)

                if success:
                    scaled_resources.append(resource_type)

        total_cost = sum(d.estimated_cost for d in decisions)
        self._total_cost += total_cost
        self._scaling_operations += len(scaled_resources)

        return ScalingResult(
            success=len(scaled_resources) == len([d for d in decisions if d.action == "scale_up"]),
            decisions=decisions,
            resources_scaled=scaled_resources,
            total_cost=total_cost,
            metadata={
                'growth_category': growth_metrics.category.value,
                'growth_rate': growth_metrics.current_rate
            }
        )

    def _calculate_scaling_decision(
        self,
        allocation: ResourceAllocation,
        growth_metrics: GrowthMetrics
    ) -> ScalingDecision:
        """Calculate scaling decision for a resource."""
        # Calculate projected utilization
        projected_util = allocation.utilization * (1 + growth_metrics.current_rate)

        # Determine action based on strategy and growth
        if growth_metrics.category == GrowthCategory.CRITICAL:
            # Critical growth - aggressive scaling regardless of strategy
            if allocation.utilization > 0.5:
                return self._create_scale_up_decision(
                    allocation,
                    "Critical growth detected, proactive scaling",
                    scale_factor=2.0,
                    priority=1.0
                )

        elif growth_metrics.category == GrowthCategory.EXPLOSIVE:
            # Explosive growth - scale up with high priority
            if allocation.utilization > 0.6:
                return self._create_scale_up_decision(
                    allocation,
                    "Explosive growth, scaling ahead of demand",
                    scale_factor=1.5,
                    priority=0.9
                )

        elif growth_metrics.category == GrowthCategory.RAPID:
            # Rapid growth - scale based on strategy
            if self._strategy in [ScalingStrategy.AGGRESSIVE, ScalingStrategy.BALANCED]:
                if allocation.utilization > 0.7:
                    return self._create_scale_up_decision(
                        allocation,
                        "Rapid growth, proactive scaling",
                        scale_factor=1.3,
                        priority=0.7
                    )

        # Standard utilization-based scaling
        if allocation.utilization > self._scale_up_threshold:
            return self._create_scale_up_decision(
                allocation,
                f"High utilization ({allocation.utilization:.0%})",
                scale_factor=1 + self._headroom_factor,
                priority=0.5
            )

        if allocation.utilization < self._scale_down_threshold:
            if self._strategy != ScalingStrategy.AGGRESSIVE:
                return self._create_scale_down_decision(
                    allocation,
                    f"Low utilization ({allocation.utilization:.0%})",
                    scale_factor=0.8,
                    priority=0.2
                )

        # Maintain current allocation
        return ScalingDecision(
            resource_type=allocation.resource_type,
            action="maintain",
            current_amount=allocation.current_amount,
            target_amount=allocation.current_amount,
            reason="Utilization within acceptable range",
            priority=0.0
        )

    def _create_scale_up_decision(
        self,
        allocation: ResourceAllocation,
        reason: str,
        scale_factor: float,
        priority: float
    ) -> ScalingDecision:
        """Create scale-up decision."""
        target = min(
            allocation.current_amount * scale_factor,
            allocation.max_amount
        )

        # Estimate cost (simplified model)
        increase = target - allocation.current_amount
        cost_per_unit = 0.1  # Placeholder cost
        estimated_cost = increase * cost_per_unit

        return ScalingDecision(
            resource_type=allocation.resource_type,
            action="scale_up",
            current_amount=allocation.current_amount,
            target_amount=target,
            reason=reason,
            priority=priority,
            estimated_cost=estimated_cost
        )

    def _create_scale_down_decision(
        self,
        allocation: ResourceAllocation,
        reason: str,
        scale_factor: float,
        priority: float
    ) -> ScalingDecision:
        """Create scale-down decision."""
        # Ensure we don't go below minimum
        min_amount = allocation.max_amount * 0.1
        target = max(
            allocation.current_amount * scale_factor,
            min_amount
        )

        return ScalingDecision(
            resource_type=allocation.resource_type,
            action="scale_down",
            current_amount=allocation.current_amount,
            target_amount=target,
            reason=reason,
            priority=priority,
            estimated_cost=0.0  # No cost for scaling down
        )

    async def _execute_scaling(self, decision: ScalingDecision) -> bool:
        """Execute a scaling decision."""
        try:
            # Update allocation
            allocation = self._allocations[decision.resource_type]
            allocation.current_amount = decision.target_amount

            logger.info(
                f"Scaled {decision.resource_type.value}: "
                f"{decision.current_amount} -> {decision.target_amount} "
                f"({decision.reason})"
            )

            return True

        except Exception as e:
            logger.error(f"Scaling failed for {decision.resource_type}: {e}")
            return False

    def update_utilization(
        self,
        resource_type: ResourceType,
        utilization: float
    ) -> None:
        """Update resource utilization."""
        if resource_type in self._allocations:
            self._allocations[resource_type].utilization = max(0.0, min(1.0, utilization))

    def get_allocation(self, resource_type: ResourceType) -> Optional[ResourceAllocation]:
        """Get current allocation for resource."""
        return self._allocations.get(resource_type)

    def get_all_allocations(self) -> Dict[ResourceType, ResourceAllocation]:
        """Get all allocations."""
        return self._allocations.copy()

    def get_stats(self) -> Dict:
        """Get scaler statistics."""
        return {
            'strategy': self._strategy.value,
            'total_cost': self._total_cost,
            'scaling_operations': self._scaling_operations,
            'allocations': {
                rt.value: alloc.to_dict()
                for rt, alloc in self._allocations.items()
            }
        }

    def reset(self) -> None:
        """Reset scaler state."""
        self._initialize_allocations()
        self._total_cost = 0.0
        self._scaling_operations = 0
        logger.info("ResourceScaler reset")
