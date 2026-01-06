"""
Safe Modification Executor.

Executes approved modifications with checkpointing and rollback.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 2.1 for specification.
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
import logging
import asyncio
import uuid
import time

from .levels import PlasticityLevel
from .proposal import (
    PlasticityProposal,
    ModificationResult,
    ModificationType,
    RollbackPlan,
)

logger = logging.getLogger("rsi.plasticity.executor")


@dataclass
class Checkpoint:
    """Checkpoint for rollback."""
    id: str
    proposal_id: str
    created_at: str
    state_snapshot: Dict[str, Any]
    module_states: Dict[str, Any]


class ModificationExecutor:
    """
    Executes modifications with safety checkpointing.

    Handles:
    - Pre-execution checkpointing
    - Safe execution with timeout
    - Post-execution verification
    - Rollback on failure
    """

    def __init__(
        self,
        module_registry=None,
        memory=None,
        config: Dict = None
    ):
        """
        Initialize executor.

        Args:
            module_registry: ModuleRegistry instance
            memory: Memory instance for persistence
            config: Configuration options
        """
        self.module_registry = module_registry
        self.memory = memory
        self.config = config or {}

        # Checkpoints
        self._checkpoints: Dict[str, Checkpoint] = {}

        # Execution handlers by modification type
        self._handlers: Dict[ModificationType, Callable] = {}
        self._setup_default_handlers()

        # Statistics
        self._executions_count: int = 0
        self._successful_executions: int = 0
        self._rollbacks_triggered: int = 0

        # Configuration
        self._execution_timeout = config.get('execution_timeout', 30.0)
        self._max_rollback_time = config.get('max_rollback_time', 30.0)

    def _setup_default_handlers(self) -> None:
        """Set up default modification handlers."""
        self._handlers = {
            ModificationType.WEIGHT_ADJUST: self._handle_weight_adjust,
            ModificationType.CONFIG_UPDATE: self._handle_config_update,
            ModificationType.MODULE_ENABLE: self._handle_module_enable,
            ModificationType.MODULE_DISABLE: self._handle_module_disable,
            ModificationType.MODULE_COMPOSE: self._handle_module_compose,
            ModificationType.MODULE_CREATE: self._handle_module_create,
            ModificationType.ARCHITECTURE_CHANGE: self._handle_architecture_change,
        }

    async def execute(
        self,
        proposal: PlasticityProposal,
        dry_run: bool = False
    ) -> ModificationResult:
        """
        Execute a modification proposal.

        Args:
            proposal: The approved proposal to execute
            dry_run: If True, simulate without making changes

        Returns:
            ModificationResult with outcome
        """
        self._executions_count += 1
        start_time = time.time()

        logger.info(
            f"Executing proposal {proposal.id}: {proposal.modification_type.value}"
        )

        # Create checkpoint
        checkpoint = await self._create_checkpoint(proposal)

        try:
            if dry_run:
                # Simulate execution
                result = await self._simulate_execution(proposal)
            else:
                # Execute with timeout
                result = await asyncio.wait_for(
                    self._execute_modification(proposal),
                    timeout=self._execution_timeout
                )

            # Verify execution
            if result.success:
                verification = await self._verify_execution(proposal)
                result.verification_results = verification

                if not verification.get('passed', True):
                    logger.warning(
                        f"Verification failed for {proposal.id}, rolling back"
                    )
                    await self._rollback(checkpoint, proposal.rollback_plan)
                    result.success = False
                    result.rollback_triggered = True
                    result.error = "Post-execution verification failed"
                else:
                    self._successful_executions += 1

        except asyncio.TimeoutError:
            logger.error(f"Execution timeout for {proposal.id}")
            await self._rollback(checkpoint, proposal.rollback_plan)
            result = ModificationResult(
                success=False,
                proposal_id=proposal.id,
                rollback_triggered=True,
                error="Execution timeout"
            )

        except Exception as e:
            logger.error(f"Execution failed for {proposal.id}: {e}")
            await self._rollback(checkpoint, proposal.rollback_plan)
            result = ModificationResult(
                success=False,
                proposal_id=proposal.id,
                rollback_triggered=True,
                error=str(e)
            )

        execution_time = time.time() - start_time
        logger.info(
            f"Execution {'succeeded' if result.success else 'failed'} "
            f"for {proposal.id} in {execution_time:.2f}s"
        )

        return result

    async def _create_checkpoint(
        self,
        proposal: PlasticityProposal
    ) -> Checkpoint:
        """Create a checkpoint before execution."""
        checkpoint_id = f"chk_{uuid.uuid4().hex[:12]}"

        # Capture module states
        module_states = {}
        if self.module_registry:
            for module_id in proposal.target_modules:
                module = await self.module_registry.get_module(module_id)
                if module:
                    module_states[module_id] = module.to_dict()

        checkpoint = Checkpoint(
            id=checkpoint_id,
            proposal_id=proposal.id,
            created_at=datetime.now(timezone.utc).isoformat(),
            state_snapshot=proposal.parameters.copy(),
            module_states=module_states
        )

        self._checkpoints[checkpoint_id] = checkpoint

        # Update proposal's rollback plan with checkpoint
        if proposal.rollback_plan:
            proposal.rollback_plan.checkpoint_id = checkpoint_id

        logger.debug(f"Created checkpoint {checkpoint_id}")

        return checkpoint

    async def _execute_modification(
        self,
        proposal: PlasticityProposal
    ) -> ModificationResult:
        """Execute the modification using appropriate handler."""
        handler = self._handlers.get(proposal.modification_type)

        if not handler:
            return ModificationResult(
                success=False,
                proposal_id=proposal.id,
                error=f"No handler for {proposal.modification_type.value}"
            )

        return await handler(proposal)

    async def _simulate_execution(
        self,
        proposal: PlasticityProposal
    ) -> ModificationResult:
        """Simulate execution without making changes."""
        # Check if operation would succeed
        changes = []

        for module_id in proposal.target_modules:
            changes.append(f"Would modify module: {module_id}")

        return ModificationResult(
            success=True,
            proposal_id=proposal.id,
            changes_made=changes,
            verification_results={'simulated': True}
        )

    async def _verify_execution(
        self,
        proposal: PlasticityProposal
    ) -> Dict[str, Any]:
        """Verify that execution was successful."""
        verification = {
            'passed': True,
            'checks': []
        }

        # Verify target modules still exist
        if self.module_registry:
            for module_id in proposal.target_modules:
                module = await self.module_registry.get_module(module_id)
                if module:
                    verification['checks'].append({
                        'module': module_id,
                        'exists': True
                    })
                else:
                    verification['checks'].append({
                        'module': module_id,
                        'exists': False
                    })
                    verification['passed'] = False

        return verification

    async def _rollback(
        self,
        checkpoint: Checkpoint,
        rollback_plan: Optional[RollbackPlan]
    ) -> bool:
        """
        Execute rollback using checkpoint.

        Returns True if rollback succeeded.
        """
        self._rollbacks_triggered += 1

        start_time = time.time()

        logger.info(f"Rolling back from checkpoint {checkpoint.id}")

        try:
            # Restore module states
            if self.module_registry and checkpoint.module_states:
                for module_id, state in checkpoint.module_states.items():
                    await self.module_registry.update_module(
                        module_id,
                        state
                    )

            elapsed = time.time() - start_time

            if elapsed > self._max_rollback_time:
                logger.error(
                    f"Rollback took {elapsed:.2f}s, exceeding max of "
                    f"{self._max_rollback_time}s"
                )

            logger.info(f"Rollback completed in {elapsed:.2f}s")

            return True

        except Exception as e:
            logger.error(f"Rollback failed: {e}")
            return False

    # ========================================================================
    # Modification Handlers
    # ========================================================================

    async def _handle_weight_adjust(
        self,
        proposal: PlasticityProposal
    ) -> ModificationResult:
        """Handle weight adjustment modifications."""
        changes = []

        for module_id in proposal.target_modules:
            if self.module_registry:
                module = await self.module_registry.get_module(module_id)
                if module:
                    # Update module config with new weights
                    new_config = module.config.copy()
                    new_config.update(proposal.parameters)
                    await self.module_registry.update_module(
                        module_id,
                        {'config': new_config}
                    )
                    changes.append(f"Adjusted weights for {module_id}")

        return ModificationResult(
            success=True,
            proposal_id=proposal.id,
            changes_made=changes
        )

    async def _handle_config_update(
        self,
        proposal: PlasticityProposal
    ) -> ModificationResult:
        """Handle configuration update modifications."""
        changes = []

        for module_id in proposal.target_modules:
            if self.module_registry:
                await self.module_registry.update_module(
                    module_id,
                    {'config': proposal.parameters}
                )
                changes.append(f"Updated config for {module_id}")

        return ModificationResult(
            success=True,
            proposal_id=proposal.id,
            changes_made=changes
        )

    async def _handle_module_enable(
        self,
        proposal: PlasticityProposal
    ) -> ModificationResult:
        """Handle module enable modifications."""
        from .module_types import ModuleStatus

        changes = []

        for module_id in proposal.target_modules:
            if self.module_registry:
                await self.module_registry.update_module(
                    module_id,
                    {'status': ModuleStatus.ACTIVE}
                )
                changes.append(f"Enabled module {module_id}")

        return ModificationResult(
            success=True,
            proposal_id=proposal.id,
            changes_made=changes
        )

    async def _handle_module_disable(
        self,
        proposal: PlasticityProposal
    ) -> ModificationResult:
        """Handle module disable modifications."""
        from .module_types import ModuleStatus

        changes = []

        for module_id in proposal.target_modules:
            if self.module_registry:
                await self.module_registry.update_module(
                    module_id,
                    {'status': ModuleStatus.REGISTERED}
                )
                changes.append(f"Disabled module {module_id}")

        return ModificationResult(
            success=True,
            proposal_id=proposal.id,
            changes_made=changes
        )

    async def _handle_module_compose(
        self,
        proposal: PlasticityProposal
    ) -> ModificationResult:
        """Handle module composition modifications."""
        from .module_types import CompositionType
        from .module_composer import ModuleComposer

        changes = []

        if len(proposal.target_modules) < 2:
            return ModificationResult(
                success=False,
                proposal_id=proposal.id,
                error="Need at least 2 modules to compose"
            )

        if self.module_registry:
            # Fetch modules
            modules = []
            for module_id in proposal.target_modules:
                module = await self.module_registry.get_module(module_id)
                if module:
                    modules.append(module)

            if len(modules) < 2:
                return ModificationResult(
                    success=False,
                    proposal_id=proposal.id,
                    error="Not enough valid modules to compose"
                )

            # Determine composition type
            comp_type_str = proposal.parameters.get('composition_type', 'sequential')
            comp_type = CompositionType(comp_type_str)

            # Compose
            composer = ModuleComposer(registry=self.module_registry)
            composed = await composer.compose(
                modules=modules,
                composition_type=comp_type
            )

            # Register composed module
            await self.module_registry.register_module(composed)
            changes.append(f"Created composed module {composed.id}")

        return ModificationResult(
            success=True,
            proposal_id=proposal.id,
            changes_made=changes
        )

    async def _handle_module_create(
        self,
        proposal: PlasticityProposal
    ) -> ModificationResult:
        """Handle module creation modifications (Level 3+)."""
        # This would integrate with NAS in Phase 3
        return ModificationResult(
            success=False,
            proposal_id=proposal.id,
            error="Module creation requires NAS (Phase 3)"
        )

    async def _handle_architecture_change(
        self,
        proposal: PlasticityProposal
    ) -> ModificationResult:
        """Handle architecture change modifications (Level 4)."""
        # This would integrate with MetaArchitect in Phase 3
        return ModificationResult(
            success=False,
            proposal_id=proposal.id,
            error="Architecture changes require MetaArchitect (Phase 3)"
        )

    def register_handler(
        self,
        mod_type: ModificationType,
        handler: Callable
    ) -> None:
        """Register a custom modification handler."""
        self._handlers[mod_type] = handler

    def get_checkpoint(self, checkpoint_id: str) -> Optional[Checkpoint]:
        """Get a checkpoint by ID."""
        return self._checkpoints.get(checkpoint_id)

    def get_stats(self) -> Dict:
        """Get executor statistics."""
        return {
            'executions_count': self._executions_count,
            'successful_executions': self._successful_executions,
            'rollbacks_triggered': self._rollbacks_triggered,
            'success_rate': (
                self._successful_executions / self._executions_count
                if self._executions_count > 0 else 0.0
            ),
            'checkpoints_count': len(self._checkpoints)
        }

    def reset(self) -> None:
        """Reset executor state."""
        self._checkpoints.clear()
        self._executions_count = 0
        self._successful_executions = 0
        self._rollbacks_triggered = 0
        logger.info("ModificationExecutor reset")
