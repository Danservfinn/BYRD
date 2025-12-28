"""
BYRD Rollback System
Ensures all modifications are reversible and provides auto-rollback on problems.

Phase 5 of AGI Seed architecture.

REVERSIBILITY PRINCIPLES:
1. All modifications must be reversible
2. Maintain complete modification history
3. Auto-rollback on detected problems
4. Support manual rollback by operators
5. Preserve provenance through all rollbacks

This module integrates with git for file-level rollback and
with memory for state-level tracking.
"""

import asyncio
import subprocess
import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from enum import Enum

from memory import Memory


class RollbackReason(Enum):
    """Reasons for triggering a rollback."""
    SAFETY_VIOLATION = "safety_violation"
    GOAL_DRIFT = "goal_drift"
    CORRIGIBILITY_FAILURE = "corrigibility_failure"
    CAPABILITY_REGRESSION = "capability_regression"
    OPERATOR_REQUEST = "operator_request"
    AUTO_HEALTH_CHECK = "auto_health_check"
    EMERGENCY_STOP = "emergency_stop"


@dataclass
class ModificationRecord:
    """Record of a single modification."""
    id: str
    timestamp: datetime
    file_path: str
    git_commit: Optional[str]
    description: str
    desire_id: Optional[str]  # Provenance
    reversible: bool
    reversed: bool = False
    rollback_commit: Optional[str] = None

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "file_path": self.file_path,
            "git_commit": self.git_commit,
            "description": self.description,
            "desire_id": self.desire_id,
            "reversible": self.reversible,
            "reversed": self.reversed,
            "rollback_commit": self.rollback_commit
        }


@dataclass
class RollbackResult:
    """Result of a rollback operation."""
    success: bool
    reason: RollbackReason
    modifications_rolled_back: int
    target_commit: Optional[str]
    error: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)


class RollbackSystem:
    """
    Manages modification history and rollback operations.

    Works with git for file-level reversibility and maintains
    its own modification log for provenance tracking.
    """

    def __init__(self, memory: Memory, project_root: str = "."):
        self.memory = memory
        self.project_root = Path(project_root)

        # Modification history (in-memory, also persisted to neo4j)
        self._modifications: List[ModificationRecord] = []
        self._rollbacks: List[RollbackResult] = []

        # Settings
        self._max_modifications_before_checkpoint = 10
        self._auto_rollback_enabled = True

    async def initialize(self):
        """Initialize rollback system and verify git is available."""
        # Verify git is available
        if not self._git_available():
            print("⚠️ Git not available - rollback functionality limited")
            return

        # Get current commit as baseline
        baseline = self._get_current_commit()
        if baseline:
            await self.memory.record_experience(
                content=f"[ROLLBACK_INIT] Rollback system initialized at commit {baseline[:8]} (full: {baseline})",
                type="system"
            )

    def _git_available(self) -> bool:
        """Check if git is available and we're in a repo."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except Exception:
            return False

    def _get_current_commit(self) -> Optional[str]:
        """Get current git commit hash."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass
        return None

    def _get_commit_before(self, file_path: str) -> Optional[str]:
        """Get the commit before the last change to a file."""
        try:
            result = subprocess.run(
                ["git", "log", "--format=%H", "-n", "2", "--", file_path],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                commits = result.stdout.strip().split("\n")
                if len(commits) >= 2:
                    return commits[1]  # Previous commit
        except Exception:
            pass
        return None

    async def record_modification(
        self,
        file_path: str,
        description: str,
        desire_id: Optional[str] = None,
        git_commit: Optional[str] = None
    ) -> ModificationRecord:
        """
        Record a modification for rollback tracking.

        Every modification should be recorded here for provenance.
        """
        import uuid

        mod_id = f"mod_{uuid.uuid4().hex[:8]}"

        # Get git commit if not provided
        if not git_commit:
            git_commit = self._get_current_commit()

        record = ModificationRecord(
            id=mod_id,
            timestamp=datetime.now(),
            file_path=file_path,
            git_commit=git_commit,
            description=description,
            desire_id=desire_id,
            reversible=self._git_available()
        )

        self._modifications.append(record)

        # Also record in memory for persistence
        await self.memory.record_experience(
            content=f"[MODIFICATION] {file_path}: {description} | mod_id={mod_id} commit={git_commit[:8] if git_commit else 'none'} desire={desire_id or 'none'}",
            type="modification"
        )

        # Check if we should create a checkpoint
        unrolled = [m for m in self._modifications if not m.reversed]
        if len(unrolled) >= self._max_modifications_before_checkpoint:
            await self._create_checkpoint()

        return record

    async def _create_checkpoint(self):
        """Create a git checkpoint (tag) for easy rollback."""
        if not self._git_available():
            return

        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            tag_name = f"byrd_checkpoint_{timestamp}"

            subprocess.run(
                ["git", "tag", "-a", tag_name, "-m", f"BYRD auto-checkpoint at {timestamp}"],
                cwd=self.project_root,
                capture_output=True
            )

            await self.memory.record_experience(
                content=f"[CHECKPOINT] Created git tag: {tag_name}",
                type="checkpoint"
            )

        except Exception as e:
            print(f"⚠️ Failed to create checkpoint: {e}")

    async def rollback_last(self, reason: RollbackReason) -> RollbackResult:
        """Rollback the last modification."""
        if not self._modifications:
            return RollbackResult(
                success=False,
                reason=reason,
                modifications_rolled_back=0,
                target_commit=None,
                error="No modifications to rollback"
            )

        # Find last unrolled modification
        last_mod = None
        for mod in reversed(self._modifications):
            if not mod.reversed:
                last_mod = mod
                break

        if not last_mod:
            return RollbackResult(
                success=False,
                reason=reason,
                modifications_rolled_back=0,
                target_commit=None,
                error="All modifications already rolled back"
            )

        return await self._rollback_modification(last_mod, reason)

    async def rollback_to_commit(
        self,
        target_commit: str,
        reason: RollbackReason
    ) -> RollbackResult:
        """Rollback to a specific git commit."""
        if not self._git_available():
            return RollbackResult(
                success=False,
                reason=reason,
                modifications_rolled_back=0,
                target_commit=target_commit,
                error="Git not available"
            )

        try:
            # Create a backup branch first
            current = self._get_current_commit()
            backup_branch = f"byrd_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            subprocess.run(
                ["git", "branch", backup_branch],
                cwd=self.project_root,
                capture_output=True
            )

            # Reset to target commit
            result = subprocess.run(
                ["git", "reset", "--hard", target_commit],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                return RollbackResult(
                    success=False,
                    reason=reason,
                    modifications_rolled_back=0,
                    target_commit=target_commit,
                    error=f"Git reset failed: {result.stderr}"
                )

            # Count modifications that were rolled back
            rolled_back = 0
            for mod in self._modifications:
                if not mod.reversed and mod.git_commit != target_commit:
                    mod.reversed = True
                    mod.rollback_commit = target_commit
                    rolled_back += 1

            # Record the rollback
            await self.memory.record_experience(
                content=f"[ROLLBACK] {reason.value}: Reset to {target_commit[:8]}, rolled back {rolled_back} modifications. Backup branch: {backup_branch}",
                type="rollback"
            )

            rollback_result = RollbackResult(
                success=True,
                reason=reason,
                modifications_rolled_back=rolled_back,
                target_commit=target_commit
            )

            self._rollbacks.append(rollback_result)
            return rollback_result

        except Exception as e:
            return RollbackResult(
                success=False,
                reason=reason,
                modifications_rolled_back=0,
                target_commit=target_commit,
                error=str(e)
            )

    async def _rollback_modification(
        self,
        mod: ModificationRecord,
        reason: RollbackReason
    ) -> RollbackResult:
        """Rollback a specific modification."""
        if not mod.reversible:
            return RollbackResult(
                success=False,
                reason=reason,
                modifications_rolled_back=0,
                target_commit=None,
                error="Modification not reversible"
            )

        # Get commit before the modification
        target_commit = self._get_commit_before(mod.file_path)
        if not target_commit:
            return RollbackResult(
                success=False,
                reason=reason,
                modifications_rolled_back=0,
                target_commit=None,
                error="Could not find previous commit"
            )

        # Checkout the file from previous commit
        try:
            result = subprocess.run(
                ["git", "checkout", target_commit, "--", mod.file_path],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                return RollbackResult(
                    success=False,
                    reason=reason,
                    modifications_rolled_back=0,
                    target_commit=target_commit,
                    error=f"Git checkout failed: {result.stderr}"
                )

            # Mark as reversed
            mod.reversed = True
            mod.rollback_commit = target_commit

            # Commit the rollback
            subprocess.run(
                ["git", "add", mod.file_path],
                cwd=self.project_root,
                capture_output=True
            )

            commit_msg = f"[BYRD ROLLBACK] Reverted {mod.file_path}: {reason.value}"
            subprocess.run(
                ["git", "commit", "-m", commit_msg],
                cwd=self.project_root,
                capture_output=True
            )

            # Record the rollback
            await self.memory.record_experience(
                content=f"[ROLLBACK] {mod.file_path}: {reason.value} | mod_id={mod.id} target={target_commit[:8] if target_commit else 'none'}",
                type="rollback"
            )

            rollback_result = RollbackResult(
                success=True,
                reason=reason,
                modifications_rolled_back=1,
                target_commit=target_commit
            )

            self._rollbacks.append(rollback_result)
            return rollback_result

        except Exception as e:
            return RollbackResult(
                success=False,
                reason=reason,
                modifications_rolled_back=0,
                target_commit=target_commit,
                error=str(e)
            )

    async def auto_rollback_on_problem(
        self,
        problem_type: str,
        severity: str
    ) -> Optional[RollbackResult]:
        """
        Automatically rollback if a problem is detected.

        Called by safety systems when issues are found.
        """
        if not self._auto_rollback_enabled:
            return None

        # Determine rollback reason
        reason_map = {
            "safety_violation": RollbackReason.SAFETY_VIOLATION,
            "goal_drift": RollbackReason.GOAL_DRIFT,
            "corrigibility": RollbackReason.CORRIGIBILITY_FAILURE,
            "capability_regression": RollbackReason.CAPABILITY_REGRESSION,
            "emergency": RollbackReason.EMERGENCY_STOP
        }

        reason = reason_map.get(problem_type, RollbackReason.AUTO_HEALTH_CHECK)

        # Only auto-rollback for severe issues
        if severity not in ["critical", "high"]:
            return None

        print(f"⚠️ Auto-rollback triggered: {problem_type} ({severity})")

        return await self.rollback_last(reason)

    def get_modification_history(self, limit: int = 20) -> List[Dict]:
        """Get recent modification history."""
        recent = self._modifications[-limit:]
        return [m.to_dict() for m in reversed(recent)]

    def get_unrolled_modifications(self) -> List[Dict]:
        """Get modifications that haven't been rolled back."""
        unrolled = [m for m in self._modifications if not m.reversed]
        return [m.to_dict() for m in unrolled]

    def get_statistics(self) -> Dict:
        """Get rollback system statistics."""
        return {
            "total_modifications": len(self._modifications),
            "unrolled_modifications": len([m for m in self._modifications if not m.reversed]),
            "rollbacks_performed": len(self._rollbacks),
            "auto_rollback_enabled": self._auto_rollback_enabled,
            "git_available": self._git_available()
        }


# Export main classes
__all__ = [
    "RollbackSystem",
    "RollbackResult",
    "RollbackReason",
    "ModificationRecord"
]
