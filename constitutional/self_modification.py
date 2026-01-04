"""
BYRD Self-Modification System
Orchestrates safe self-modification with provenance verification.

This file is PROTECTED - it cannot be modified by the self-modification system.
Any attempt to modify this file will be rejected.
"""

import os
import shutil
import uuid
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from memory import Memory
from provenance import ProvenanceTracer, ProvenanceRecord
from constitutional import ConstitutionalConstraints
from modification_log import ModificationLog, ModificationEntry


@dataclass
class ModificationProposal:
    """A proposed modification with all context."""
    id: str
    desire_id: str
    target_file: str
    target_component: str
    description: str
    current_code: str
    proposed_code: str
    provenance: Optional[ProvenanceRecord] = None
    status: str = "pending"  # pending, approved, rejected, executed, rolled_back
    error: Optional[str] = None


class SelfModificationSystem:
    """
    Orchestrates safe self-modification.

    This is the gatekeeper for all code changes. It ensures:
    1. Constitutional constraints are respected
    2. Provenance is verified (desire traces to experiences)
    3. Changes are logged immutably
    4. Checkpoints enable rollback
    5. Health checks validate changes

    This class is PROTECTED and cannot be modified by BYRD.
    """

    def __init__(
        self,
        memory: Memory,
        config: Dict,
        project_root: str = ".",
        safety_monitor=None
    ):
        self.memory = memory
        self.config = config
        self.project_root = Path(project_root)

        # Safety monitor for pattern observation (emergence-preserving)
        self.safety_monitor = safety_monitor

        # Initialize subsystems
        self.provenance = ProvenanceTracer(memory)
        self.log = ModificationLog(
            config.get("checkpoint_dir", "./modification_logs"),
            memory=memory  # Enable async outcome recording
        )

        # Configuration
        self.enabled = config.get("enabled", False)
        self.require_health_check = config.get("require_health_check", True)
        self.auto_rollback = config.get("auto_rollback_on_failure", True)
        self.max_per_day = config.get("max_modifications_per_day", 5)
        self.cooldown_seconds = config.get(
            "cooldown_between_modifications_seconds", 3600
        )

        # Checkpoint settings
        self.checkpoint_dir = Path(config.get("checkpoint_dir", "./checkpoints"))
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self.max_checkpoints = config.get("max_checkpoints", 100)

        # State
        self._daily_count = 0
        self._last_modification_time: Optional[datetime] = None
        self._pending_proposals: Dict[str, ModificationProposal] = {}

    def is_component_modifiable(self, component: str) -> bool:
        """Check if a component can be modified."""
        return ConstitutionalConstraints.is_component_modifiable(component)

    def is_file_modifiable(self, filepath: str) -> bool:
        """Check if a file can be modified."""
        return ConstitutionalConstraints.is_modifiable(filepath)

    async def create_proposal(
        self,
        desire_id: str,
        target_file: str,
        target_component: str,
        description: str,
        proposed_code: str
    ) -> Tuple[bool, ModificationProposal]:
        """
        Create a modification proposal.

        This doesn't execute the modification, just validates and prepares it.

        Returns:
            (success, proposal)
        """
        proposal_id = str(uuid.uuid4())[:8]

        # Read current code
        filepath = self.project_root / target_file
        try:
            with open(filepath, "r") as f:
                current_code = f.read()
        except FileNotFoundError:
            proposal = ModificationProposal(
                id=proposal_id,
                desire_id=desire_id,
                target_file=target_file,
                target_component=target_component,
                description=description,
                current_code="",
                proposed_code=proposed_code,
                status="rejected",
                error=f"Target file not found: {target_file}"
            )
            return False, proposal

        proposal = ModificationProposal(
            id=proposal_id,
            desire_id=desire_id,
            target_file=target_file,
            target_component=target_component,
            description=description,
            current_code=current_code,
            proposed_code=proposed_code,
        )

        # Validate proposal
        valid, error = await self._validate_proposal(proposal)
        if not valid:
            proposal.status = "rejected"
            proposal.error = error
            return False, proposal

        # Store for later execution
        self._pending_proposals[proposal_id] = proposal
        proposal.status = "approved"

        return True, proposal

    async def _validate_proposal(
        self,
        proposal: ModificationProposal
    ) -> Tuple[bool, Optional[str]]:
        """Validate a modification proposal."""

        # Check if system is enabled
        if not self.enabled:
            return False, "Self-modification is disabled"

        # Check rate limits
        if self._daily_count >= self.max_per_day:
            return False, f"Daily limit reached ({self.max_per_day})"

        if self._last_modification_time:
            elapsed = (datetime.utcnow() - self._last_modification_time).seconds
            if elapsed < self.cooldown_seconds:
                remaining = self.cooldown_seconds - elapsed
                return False, f"Cooldown active ({remaining}s remaining)"

        # Check constitutional constraints
        allowed, reason = ConstitutionalConstraints.validate_modification(
            proposal.target_file,
            proposal.proposed_code
        )
        if not allowed:
            return False, reason

        # Verify provenance
        verified, record = await self.provenance.verify_modification(
            proposal.id,
            proposal.desire_id
        )
        if not verified:
            return False, "Provenance verification failed - desire doesn't trace to experiences"

        proposal.provenance = record

        # EMERGENCE-PRESERVING: Observe patterns without blocking
        # This logs patterns for learning, but does NOT prevent modification
        if self.safety_monitor:
            try:
                observations = await self.safety_monitor.observe_patterns(
                    proposal.proposed_code,
                    proposal.target_file
                )
                # Store observations in proposal for later correlation
                proposal.pattern_observations = observations
            except Exception as e:
                # Pattern observation failure = LOG and continue
                print(f"Warning: Pattern observation failed: {e}")
                # Modification proceeds - observation is for learning, not blocking

        return True, None

    async def execute_proposal(
        self,
        proposal_id: str
    ) -> Tuple[bool, str]:
        """
        Execute a validated proposal.

        Returns:
            (success, message)
        """
        proposal = self._pending_proposals.get(proposal_id)
        if not proposal:
            return False, f"Proposal {proposal_id} not found"

        if proposal.status != "approved":
            return False, f"Proposal status is {proposal.status}, not approved"

        # Create checkpoint
        checkpoint_id = await self._create_checkpoint(proposal)

        # Execute modification
        filepath = self.project_root / proposal.target_file
        try:
            with open(filepath, "w") as f:
                f.write(proposal.proposed_code)

            # Log successful modification
            self.log.log_modification(
                modification_id=proposal.id,
                target_file=proposal.target_file,
                target_component=proposal.target_component,
                desire_id=proposal.desire_id,
                desire_description=proposal.description,
                provenance_hash=proposal.provenance.verification_hash if proposal.provenance else "",
                change_description=proposal.description,
                code_before=proposal.current_code,
                code_after=proposal.proposed_code,
                success=True,
            )

            # Run health check if required
            if self.require_health_check:
                healthy, health_error = await self._run_health_check()
                if not healthy:
                    if self.auto_rollback:
                        await self._rollback_to_checkpoint(checkpoint_id, proposal)
                        return False, f"Health check failed, rolled back: {health_error}"
                    return False, f"Health check failed: {health_error}"

            # Update state
            proposal.status = "executed"
            self._daily_count += 1
            self._last_modification_time = datetime.utcnow()

            # EMERGENCE-PRESERVING: Record outcome for BYRD's learning
            # This feeds the Bayesian learning system - BYRD reflects on success/failure
            await self.log.record_outcome(
                modification_id=proposal.id,
                success=True
            )

            # Record in memory
            await self.memory.record_experience(
                content=f"Self-modification executed: {proposal.description} on {proposal.target_file}",
                type="self_modification"
            )

            return True, f"Modification {proposal.id} executed successfully"

        except Exception as e:
            # Log failed modification
            self.log.log_modification(
                modification_id=proposal.id,
                target_file=proposal.target_file,
                target_component=proposal.target_component,
                desire_id=proposal.desire_id,
                desire_description=proposal.description,
                provenance_hash=proposal.provenance.verification_hash if proposal.provenance else "",
                change_description=proposal.description,
                code_before=proposal.current_code,
                code_after=proposal.proposed_code,
                success=False,
                error_message=str(e),
            )

            proposal.status = "failed"
            proposal.error = str(e)

            # EMERGENCE-PRESERVING: Record failure outcome for BYRD's learning
            # BYRD can reflect: "What patterns correlate with failed modifications?"
            await self.log.record_outcome(
                modification_id=proposal.id,
                success=False,
                error=str(e)
            )

            return False, f"Modification failed: {e}"

    async def _create_checkpoint(
        self,
        proposal: ModificationProposal
    ) -> str:
        """Create a checkpoint before modification."""
        checkpoint_id = f"cp_{proposal.id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        checkpoint_path = self.checkpoint_dir / checkpoint_id

        # Create checkpoint directory
        checkpoint_path.mkdir(parents=True, exist_ok=True)

        # Copy all modifiable files
        files_to_backup = []
        for filename in ConstitutionalConstraints.MODIFIABLE_FILES:
            source = self.project_root / filename
            if source.exists():
                dest = checkpoint_path / filename
                shutil.copy2(source, dest)
                files_to_backup.append(str(filename))

        # Log checkpoint
        self.log.create_checkpoint(
            checkpoint_id=checkpoint_id,
            trigger="pre_modification",
            modification_id=proposal.id,
            files=files_to_backup,
            checkpoint_path=str(checkpoint_path),
        )

        # Clean old checkpoints if needed
        await self._cleanup_old_checkpoints()

        return checkpoint_id

    async def _rollback_to_checkpoint(
        self,
        checkpoint_id: str,
        proposal: ModificationProposal
    ):
        """Rollback to a checkpoint."""
        checkpoint = self.log.get_checkpoint(checkpoint_id)
        if not checkpoint:
            raise ValueError(f"Checkpoint {checkpoint_id} not found")

        checkpoint_path = Path(checkpoint.checkpoint_path)

        # Restore files
        for filename in checkpoint.files_included:
            source = checkpoint_path / filename
            dest = self.project_root / filename
            if source.exists():
                shutil.copy2(source, dest)

        # Log rollback
        rollback_id = f"rb_{proposal.id}"
        self.log.log_modification(
            modification_id=rollback_id,
            target_file=proposal.target_file,
            target_component=proposal.target_component,
            desire_id=proposal.desire_id,
            desire_description=f"ROLLBACK: {proposal.description}",
            provenance_hash="",
            change_description=f"Rolled back modification {proposal.id}",
            code_before=proposal.proposed_code,
            code_after=proposal.current_code,
            success=True,
        )

        self.log.log_rollback(proposal.id, rollback_id)
        proposal.status = "rolled_back"

        # Record in memory
        await self.memory.record_experience(
            content=f"Self-modification rolled back: {proposal.description}",
            type="self_modification"
        )

    async def _run_health_check(self) -> Tuple[bool, Optional[str]]:
        """
        Run health check after modification.

        This verifies the system still works after changes.
        """
        try:
            # Try to import all core modules
            import importlib

            modules_to_check = [
                "dreamer",
                "seeker",
                "actor",
                "memory",
            ]

            for module_name in modules_to_check:
                try:
                    # Reload to pick up changes
                    module = importlib.import_module(module_name)
                    importlib.reload(module)
                except Exception as e:
                    return False, f"Module {module_name} failed to load: {e}"

            return True, None

        except Exception as e:
            return False, f"Health check error: {e}"

    async def _cleanup_old_checkpoints(self):
        """Remove old checkpoints beyond the max limit."""
        checkpoints = list(self.checkpoint_dir.iterdir())
        if len(checkpoints) > self.max_checkpoints:
            # Sort by modification time
            checkpoints.sort(key=lambda p: p.stat().st_mtime)
            # Remove oldest
            to_remove = checkpoints[:-self.max_checkpoints]
            for cp in to_remove:
                shutil.rmtree(cp)

    def get_pending_proposals(self) -> List[ModificationProposal]:
        """Get all pending proposals."""
        return [p for p in self._pending_proposals.values() if p.status == "approved"]

    def get_modification_history(self, limit: int = 10) -> List[ModificationEntry]:
        """Get recent modification history."""
        return self.log.get_recent_entries(limit)

    def get_statistics(self) -> Dict:
        """Get self-modification statistics."""
        stats = self.log.get_statistics()
        stats.update({
            "enabled": self.enabled,
            "daily_count": self._daily_count,
            "max_per_day": self.max_per_day,
            "pending_proposals": len([p for p in self._pending_proposals.values() if p.status == "approved"]),
        })
        return stats

    def explain_constraints(self) -> str:
        """Get human-readable explanation of constraints."""
        return ConstitutionalConstraints.explain_constraints()
