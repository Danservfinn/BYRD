"""
Modification Proposal Handling.

Extends the safety module's ModificationProposal with plasticity-specific
features and proposal generation.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 2.1 for specification.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
import uuid
import logging

from .levels import PlasticityLevel, get_level_requirements, is_operation_allowed

logger = logging.getLogger("rsi.plasticity.proposal")


class ModificationType(Enum):
    """Types of cognitive modifications."""
    WEIGHT_ADJUST = "weight_adjust"
    CONFIG_UPDATE = "config_update"
    MODULE_ENABLE = "module_enable"
    MODULE_DISABLE = "module_disable"
    MODULE_COMPOSE = "module_compose"
    MODULE_CREATE = "module_create"
    ARCHITECTURE_CHANGE = "architecture_change"


@dataclass
class RollbackPlan:
    """Plan for rolling back a modification."""
    steps: List[str]
    estimated_time_seconds: float
    checkpoint_id: Optional[str] = None
    affected_modules: List[str] = field(default_factory=list)
    backup_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PlasticityProposal:
    """
    Proposal for a cognitive architecture modification.

    Extends ModificationProposal with plasticity-specific fields.
    """
    id: str
    goal: str  # What we're trying to achieve
    level: PlasticityLevel
    modification_type: ModificationType

    # Specification
    operation: str  # Specific operation to perform
    parameters: Dict[str, Any]  # Operation parameters
    target_modules: List[str]  # IDs of modules to modify

    # Context
    context: Dict[str, Any]  # Context that led to this proposal
    provenance_id: Optional[str] = None  # ID of originating desire

    # Risk and rollback
    estimated_risk: float = 0.0
    risk_factors: List[str] = field(default_factory=list)
    rollback_plan: Optional[RollbackPlan] = None

    # Metadata
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    estimated_benefit: float = 0.0
    rationale: str = ""

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'goal': self.goal,
            'level': self.level.value,
            'level_name': self.level.name,
            'modification_type': self.modification_type.value,
            'operation': self.operation,
            'parameters': self.parameters,
            'target_modules': self.target_modules,
            'context': self.context,
            'provenance_id': self.provenance_id,
            'estimated_risk': self.estimated_risk,
            'risk_factors': self.risk_factors,
            'rollback_plan': {
                'steps': self.rollback_plan.steps,
                'estimated_time_seconds': self.rollback_plan.estimated_time_seconds,
                'checkpoint_id': self.rollback_plan.checkpoint_id,
                'affected_modules': self.rollback_plan.affected_modules
            } if self.rollback_plan else None,
            'created_at': self.created_at,
            'estimated_benefit': self.estimated_benefit,
            'rationale': self.rationale
        }


@dataclass
class ModificationResult:
    """Result of executing a modification."""
    success: bool
    proposal_id: str
    executed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    changes_made: List[str] = field(default_factory=list)
    rollback_triggered: bool = False
    error: Optional[str] = None
    performance_delta: Optional[float] = None  # Change in capability score
    verification_results: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'success': self.success,
            'proposal_id': self.proposal_id,
            'executed_at': self.executed_at,
            'changes_made': self.changes_made,
            'rollback_triggered': self.rollback_triggered,
            'error': self.error,
            'performance_delta': self.performance_delta,
            'verification_results': self.verification_results
        }


class ProposalGenerator:
    """
    Generates modification proposals based on goals.

    Analyzes goals and context to propose appropriate modifications.
    """

    def __init__(self, config: Dict = None):
        """Initialize proposal generator."""
        self.config = config or {}
        self._proposals_generated: int = 0

    def generate_proposal(
        self,
        goal: str,
        current_level: PlasticityLevel,
        context: Dict[str, Any],
        available_modules: List[str]
    ) -> Optional[PlasticityProposal]:
        """
        Generate a modification proposal for a goal.

        Args:
            goal: Goal description
            current_level: Current plasticity level
            context: Context information
            available_modules: Available module IDs

        Returns:
            PlasticityProposal or None if no suitable proposal
        """
        # Determine modification type from goal
        mod_type, operation = self._analyze_goal(goal, current_level)

        if not mod_type:
            logger.warning(f"Could not determine modification type for goal: {goal}")
            return None

        # Check if operation is allowed at current level
        if not is_operation_allowed(current_level, operation):
            logger.warning(
                f"Operation {operation} not allowed at level {current_level.name}"
            )
            return None

        # Generate parameters based on goal and context
        parameters = self._generate_parameters(goal, mod_type, context)

        # Determine target modules
        target_modules = self._identify_targets(goal, available_modules, context)

        # Assess risk
        risk, risk_factors = self._assess_proposal_risk(
            mod_type, operation, target_modules, current_level
        )

        # Generate rollback plan
        rollback = self._generate_rollback_plan(mod_type, target_modules)

        # Estimate benefit
        benefit = self._estimate_benefit(goal, context)

        proposal = PlasticityProposal(
            id=f"prop_{uuid.uuid4().hex[:12]}",
            goal=goal,
            level=current_level,
            modification_type=mod_type,
            operation=operation,
            parameters=parameters,
            target_modules=target_modules,
            context=context,
            estimated_risk=risk,
            risk_factors=risk_factors,
            rollback_plan=rollback,
            estimated_benefit=benefit,
            rationale=f"Achieve goal: {goal}"
        )

        self._proposals_generated += 1

        logger.info(
            f"Generated proposal {proposal.id} for goal '{goal}' "
            f"at level {current_level.name}"
        )

        return proposal

    def _analyze_goal(
        self,
        goal: str,
        current_level: PlasticityLevel
    ) -> tuple[Optional[ModificationType], str]:
        """Analyze goal to determine modification type and operation."""
        goal_lower = goal.lower()

        # Level 0: Weight adjustments
        if any(kw in goal_lower for kw in ['tune', 'adjust', 'tweak', 'parameter']):
            return ModificationType.WEIGHT_ADJUST, "modify_weight"

        if any(kw in goal_lower for kw in ['config', 'setting', 'option']):
            return ModificationType.CONFIG_UPDATE, "update_config_value"

        # Level 1: Module configuration
        if any(kw in goal_lower for kw in ['enable', 'activate', 'turn on']):
            return ModificationType.MODULE_ENABLE, "enable_module"

        if any(kw in goal_lower for kw in ['disable', 'deactivate', 'turn off']):
            return ModificationType.MODULE_DISABLE, "disable_module"

        # Level 2: Module composition
        if any(kw in goal_lower for kw in ['combine', 'compose', 'merge', 'chain']):
            return ModificationType.MODULE_COMPOSE, "compose_sequential"

        if any(kw in goal_lower for kw in ['parallel', 'concurrent']):
            return ModificationType.MODULE_COMPOSE, "compose_parallel"

        if any(kw in goal_lower for kw in ['ensemble', 'vote', 'average']):
            return ModificationType.MODULE_COMPOSE, "compose_ensemble"

        # Level 3: Module creation
        if any(kw in goal_lower for kw in ['create', 'new module', 'discover']):
            return ModificationType.MODULE_CREATE, "create_module"

        # Level 4: Architecture changes
        if any(kw in goal_lower for kw in ['architecture', 'restructure', 'meta']):
            return ModificationType.ARCHITECTURE_CHANGE, "modify_plasticity_rules"

        # Default: configuration update
        return ModificationType.CONFIG_UPDATE, "update_config_value"

    def _generate_parameters(
        self,
        goal: str,
        mod_type: ModificationType,
        context: Dict
    ) -> Dict[str, Any]:
        """Generate operation parameters from goal and context."""
        params = {
            'goal': goal,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }

        if mod_type == ModificationType.WEIGHT_ADJUST:
            params['adjustment_range'] = 0.1
            params['direction'] = 'optimize'

        elif mod_type == ModificationType.MODULE_COMPOSE:
            params['composition_type'] = 'sequential'

        elif mod_type == ModificationType.MODULE_CREATE:
            params['search_budget'] = 100
            params['evaluation_metric'] = 'capability_score'

        return params

    def _identify_targets(
        self,
        goal: str,
        available_modules: List[str],
        context: Dict
    ) -> List[str]:
        """Identify target modules for modification."""
        # Start with modules mentioned in context
        targets = []

        if 'target_modules' in context:
            targets.extend(context['target_modules'])

        if 'current_module' in context:
            targets.append(context['current_module'])

        # If no specific targets, use first available
        if not targets and available_modules:
            targets.append(available_modules[0])

        return targets

    def _assess_proposal_risk(
        self,
        mod_type: ModificationType,
        operation: str,
        target_modules: List[str],
        level: PlasticityLevel
    ) -> tuple[float, List[str]]:
        """Assess risk of a proposal."""
        risk = 0.0
        factors = []

        # Base risk from modification type
        type_risks = {
            ModificationType.WEIGHT_ADJUST: 0.1,
            ModificationType.CONFIG_UPDATE: 0.15,
            ModificationType.MODULE_ENABLE: 0.2,
            ModificationType.MODULE_DISABLE: 0.3,
            ModificationType.MODULE_COMPOSE: 0.4,
            ModificationType.MODULE_CREATE: 0.6,
            ModificationType.ARCHITECTURE_CHANGE: 0.8
        }
        risk += type_risks.get(mod_type, 0.5)
        factors.append(f"Modification type: {mod_type.value}")

        # Risk from number of targets
        if len(target_modules) > 3:
            risk += 0.1
            factors.append(f"Multiple targets: {len(target_modules)}")

        # Risk multiplier from level
        level_reqs = get_level_requirements(level)
        risk *= level_reqs.risk_multiplier
        factors.append(f"Level multiplier: {level_reqs.risk_multiplier}x")

        # Clamp to [0, 1]
        risk = max(0.0, min(1.0, risk))

        return risk, factors

    def _generate_rollback_plan(
        self,
        mod_type: ModificationType,
        target_modules: List[str]
    ) -> RollbackPlan:
        """Generate a rollback plan for a modification."""
        steps = []

        if mod_type in [ModificationType.WEIGHT_ADJUST, ModificationType.CONFIG_UPDATE]:
            steps = [
                "Restore previous parameter values",
                "Verify module functionality"
            ]
            time_estimate = 5.0

        elif mod_type in [ModificationType.MODULE_ENABLE, ModificationType.MODULE_DISABLE]:
            steps = [
                "Toggle module back to previous state",
                "Verify module connections",
                "Run health check"
            ]
            time_estimate = 10.0

        elif mod_type == ModificationType.MODULE_COMPOSE:
            steps = [
                "Decompose the combined module",
                "Restore original module configurations",
                "Verify individual module functionality",
                "Run integration tests"
            ]
            time_estimate = 20.0

        elif mod_type == ModificationType.MODULE_CREATE:
            steps = [
                "Unregister new module",
                "Remove from composition graph",
                "Clean up resources",
                "Verify system stability"
            ]
            time_estimate = 30.0

        else:
            steps = ["Restore from checkpoint", "Verify system state"]
            time_estimate = 60.0

        return RollbackPlan(
            steps=steps,
            estimated_time_seconds=time_estimate,
            affected_modules=target_modules
        )

    def _estimate_benefit(self, goal: str, context: Dict) -> float:
        """Estimate potential benefit of achieving goal."""
        # Simple heuristic - could be enhanced with ML
        benefit = 0.5  # Default moderate benefit

        if 'expected_improvement' in context:
            benefit = context['expected_improvement']

        if 'priority' in context:
            benefit *= (context['priority'] + 1) / 2

        return max(0.0, min(1.0, benefit))

    def get_stats(self) -> Dict:
        """Get generator statistics."""
        return {
            'proposals_generated': self._proposals_generated
        }

    def reset(self) -> None:
        """Reset generator state."""
        self._proposals_generated = 0
