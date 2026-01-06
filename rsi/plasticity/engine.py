"""
Cognitive Plasticity Engine.

Main engine for self-modification of cognitive architecture.
Implements 5-level plasticity progression.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 2.1 for specification.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timezone
import logging
import asyncio

from .levels import (
    PlasticityLevel,
    LevelProgress,
    LevelRequirements,
    LEVEL_REQUIREMENTS,
    can_advance_level,
    get_level_requirements,
    is_operation_allowed,
)
from .proposal import (
    PlasticityProposal,
    ModificationResult,
    ModificationType,
    ProposalGenerator,
)
from .executor import ModificationExecutor, Checkpoint

logger = logging.getLogger("rsi.plasticity.engine")


@dataclass
class EngineState:
    """State of the plasticity engine."""
    current_level: PlasticityLevel
    level_progress: Dict[PlasticityLevel, LevelProgress]
    total_modifications: int
    successful_modifications: int
    pending_proposals: List[str]  # Proposal IDs


class CognitivePlasticityEngine:
    """
    Enables self-modification of cognitive architecture.

    Implements 5-level plasticity progression:
    0. WEIGHT_ADJUSTMENT - Tune existing parameters
    1. MODULE_CONFIGURATION - Enable/disable modules
    2. MODULE_COMPOSITION - Combine modules
    3. MODULE_DISCOVERY - Create new modules (NAS)
    4. META_ARCHITECTURE - Modify the modifier

    Higher levels require demonstrated competence at lower levels.
    All modifications require safety governance approval.
    """

    def __init__(
        self,
        module_registry=None,
        safety_governance=None,
        memory=None,
        config: Dict = None
    ):
        """
        Initialize the plasticity engine.

        Args:
            module_registry: ModuleRegistry for module access
            safety_governance: SafetyGovernance for approval
            memory: Memory for persistence
            config: Configuration options
        """
        self.module_registry = module_registry
        self.safety_governance = safety_governance
        self.memory = memory
        self.config = config or {}

        # Current plasticity level
        self._current_level = PlasticityLevel.WEIGHT_ADJUSTMENT

        # Progress tracking per level
        self._level_progress: Dict[PlasticityLevel, LevelProgress] = {
            level: LevelProgress(level=level)
            for level in PlasticityLevel
        }
        self._level_progress[PlasticityLevel.WEIGHT_ADJUSTMENT].unlocked_at = (
            datetime.now(timezone.utc).isoformat()
        )

        # Proposal generator
        self._proposal_generator = ProposalGenerator(config)

        # Executor
        self._executor = ModificationExecutor(
            module_registry=module_registry,
            memory=memory,
            config=config
        )

        # Pending proposals awaiting approval
        self._pending_proposals: Dict[str, PlasticityProposal] = {}

        # Statistics
        self._total_modifications: int = 0
        self._successful_modifications: int = 0

    @property
    def current_level(self) -> PlasticityLevel:
        """Get current plasticity level."""
        return self._current_level

    @property
    def level_progress(self) -> Dict[PlasticityLevel, LevelProgress]:
        """Get progress at each level."""
        return self._level_progress.copy()

    async def propose_modification(
        self,
        goal: str,
        context: Dict = None
    ) -> Optional[PlasticityProposal]:
        """
        Propose a modification to achieve a goal.

        Args:
            goal: What we're trying to achieve
            context: Additional context

        Returns:
            PlasticityProposal or None if no suitable proposal
        """
        context = context or {}

        # Get available modules
        available_modules = []
        if self.module_registry:
            modules = await self.module_registry.list_modules()
            available_modules = [m.id for m in modules]

        # Generate proposal
        proposal = self._proposal_generator.generate_proposal(
            goal=goal,
            current_level=self._current_level,
            context=context,
            available_modules=available_modules
        )

        if not proposal:
            logger.warning(f"Could not generate proposal for goal: {goal}")
            return None

        # Add provenance if available
        if 'desire_id' in context:
            proposal.provenance_id = context['desire_id']

        # Store as pending
        self._pending_proposals[proposal.id] = proposal

        logger.info(
            f"Generated proposal {proposal.id} at level {self._current_level.name}"
        )

        return proposal

    async def evaluate_proposal(
        self,
        proposal: PlasticityProposal
    ) -> Tuple[bool, str]:
        """
        Evaluate a proposal through safety governance.

        Args:
            proposal: Proposal to evaluate

        Returns:
            Tuple of (approved, reason)
        """
        if not self.safety_governance:
            # No governance - auto-approve low-risk
            if proposal.estimated_risk < 0.3:
                return True, "Auto-approved (no governance, low risk)"
            return False, "Rejected (no governance, high risk)"

        # Convert to ModificationProposal for safety governance
        from ..safety import ModificationProposal as SafetyProposal

        safety_proposal = SafetyProposal(
            id=proposal.id,
            description=proposal.goal,
            modification_type=proposal.modification_type.value,
            target_files=[],  # Not file-based
            changes=proposal.parameters,
            rationale=proposal.rationale,
            metadata={
                'level': proposal.level.value,
                'operation': proposal.operation,
                'target_modules': proposal.target_modules,
                'has_rollback': proposal.rollback_plan is not None
            }
        )

        # Evaluate and request approval
        decision, result = await self.safety_governance.evaluate_and_approve(
            safety_proposal
        )

        if not decision.can_proceed:
            return False, f"Blocked: {decision.blocking_issues}"

        if result and result.approved:
            return True, result.reason

        return False, "Awaiting approval"

    async def execute_modification(
        self,
        proposal: PlasticityProposal,
        force: bool = False
    ) -> ModificationResult:
        """
        Execute an approved modification.

        Args:
            proposal: The proposal to execute
            force: If True, skip approval check

        Returns:
            ModificationResult with outcome
        """
        self._total_modifications += 1

        # Check operation is allowed at current level
        if not is_operation_allowed(self._current_level, proposal.operation):
            return ModificationResult(
                success=False,
                proposal_id=proposal.id,
                error=(
                    f"Operation {proposal.operation} not allowed at "
                    f"level {self._current_level.name}"
                )
            )

        # Check approval unless forced
        if not force:
            approved, reason = await self.evaluate_proposal(proposal)
            if not approved:
                return ModificationResult(
                    success=False,
                    proposal_id=proposal.id,
                    error=f"Not approved: {reason}"
                )

        # Execute
        result = await self._executor.execute(proposal)

        # Record progress
        progress = self._level_progress[self._current_level]
        progress.record_attempt(result.success)

        if result.success:
            self._successful_modifications += 1

        # Remove from pending
        self._pending_proposals.pop(proposal.id, None)

        return result

    async def propose_and_execute(
        self,
        goal: str,
        context: Dict = None
    ) -> Tuple[Optional[PlasticityProposal], Optional[ModificationResult]]:
        """
        Propose and execute a modification in one step.

        Convenience method for simple modifications.

        Args:
            goal: Goal description
            context: Additional context

        Returns:
            Tuple of (proposal, result)
        """
        proposal = await self.propose_modification(goal, context)

        if not proposal:
            return None, None

        result = await self.execute_modification(proposal)

        return proposal, result

    async def advance_level(self) -> Tuple[bool, str]:
        """
        Attempt to advance to the next plasticity level.

        Returns:
            Tuple of (success, reason)
        """
        progress = self._level_progress[self._current_level]
        can_advance, reason = can_advance_level(self._current_level, progress)

        if not can_advance:
            return False, reason

        # Advance to next level
        next_level = PlasticityLevel(self._current_level.value + 1)
        self._current_level = next_level

        # Mark as unlocked
        self._level_progress[next_level].unlocked_at = (
            datetime.now(timezone.utc).isoformat()
        )

        logger.info(f"Advanced to plasticity level: {next_level.name}")

        return True, f"Advanced to level {next_level.name}"

    async def check_level_progress(self) -> Dict[str, Any]:
        """
        Check progress toward next level.

        Returns:
            Progress status including requirements and current state
        """
        progress = self._level_progress[self._current_level]

        if self._current_level >= PlasticityLevel.META_ARCHITECTURE:
            return {
                'current_level': self._current_level.name,
                'at_max_level': True,
                'progress': progress.to_dict()
            }

        next_level = PlasticityLevel(self._current_level.value + 1)
        requirements = get_level_requirements(next_level)

        can_advance, _ = can_advance_level(self._current_level, progress)

        return {
            'current_level': self._current_level.name,
            'next_level': next_level.name,
            'at_max_level': False,
            'can_advance': can_advance,
            'progress': progress.to_dict(),
            'requirements': {
                'min_successful_mods': requirements.min_successful_mods,
                'current_successful_mods': progress.successful_modifications,
                'min_success_rate': requirements.min_success_rate,
                'current_success_rate': progress.success_rate
            }
        }

    def get_level_info(self, level: PlasticityLevel = None) -> Dict:
        """Get information about a plasticity level."""
        if level is None:
            level = self._current_level

        requirements = get_level_requirements(level)
        progress = self._level_progress[level]

        return {
            'level': level.value,
            'name': requirements.name,
            'description': requirements.description,
            'allowed_operations': requirements.allowed_operations,
            'risk_multiplier': requirements.risk_multiplier,
            'progress': progress.to_dict()
        }

    def get_all_levels_info(self) -> List[Dict]:
        """Get information about all plasticity levels."""
        return [self.get_level_info(level) for level in PlasticityLevel]

    def get_pending_proposals(self) -> List[PlasticityProposal]:
        """Get all pending proposals."""
        return list(self._pending_proposals.values())

    def get_state(self) -> EngineState:
        """Get current engine state."""
        return EngineState(
            current_level=self._current_level,
            level_progress=self._level_progress.copy(),
            total_modifications=self._total_modifications,
            successful_modifications=self._successful_modifications,
            pending_proposals=list(self._pending_proposals.keys())
        )

    def get_stats(self) -> Dict:
        """Get engine statistics."""
        executor_stats = self._executor.get_stats()
        generator_stats = self._proposal_generator.get_stats()

        return {
            'current_level': self._current_level.value,
            'current_level_name': self._current_level.name,
            'total_modifications': self._total_modifications,
            'successful_modifications': self._successful_modifications,
            'success_rate': (
                self._successful_modifications / self._total_modifications
                if self._total_modifications > 0 else 0.0
            ),
            'pending_proposals': len(self._pending_proposals),
            'levels_unlocked': sum(
                1 for p in self._level_progress.values()
                if p.unlocked_at is not None
            ),
            **executor_stats,
            **generator_stats
        }

    def reset(self) -> None:
        """Reset engine state."""
        self._current_level = PlasticityLevel.WEIGHT_ADJUSTMENT
        self._level_progress = {
            level: LevelProgress(level=level)
            for level in PlasticityLevel
        }
        self._level_progress[PlasticityLevel.WEIGHT_ADJUSTMENT].unlocked_at = (
            datetime.now(timezone.utc).isoformat()
        )
        self._pending_proposals.clear()
        self._total_modifications = 0
        self._successful_modifications = 0
        self._executor.reset()
        self._proposal_generator.reset()
        logger.info("CognitivePlasticityEngine reset")
