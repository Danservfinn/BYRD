"""
BYRD Modification Log
Provides immutable audit trail of all self-modifications.

This file is PROTECTED - it cannot be modified by the self-modification system.
Any attempt to modify this file will be rejected.
"""

import hashlib
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict, field
from pathlib import Path


@dataclass
class ModificationEntry:
    """A single modification log entry."""
    id: str
    timestamp: str
    target_file: str
    target_component: str
    desire_id: str
    desire_description: str
    provenance_hash: str
    change_description: str
    code_hash_before: str
    code_hash_after: str
    success: bool
    error_message: Optional[str] = None
    rollback_id: Optional[str] = None  # If this was rolled back
    previous_entry_hash: str = ""  # Chain integrity


@dataclass
class CheckpointEntry:
    """A checkpoint of system state."""
    id: str
    timestamp: str
    trigger: str  # "pre_modification", "manual", "scheduled"
    modification_id: Optional[str]  # If triggered by modification
    files_included: List[str] = field(default_factory=list)
    checkpoint_path: str = ""
    integrity_hash: str = ""


class ModificationLog:
    """
    Immutable log of all modifications.

    Features:
    - Append-only entries (no deletions)
    - Chained hashes for integrity verification
    - Checkpoint management for rollback
    - Export/import for persistence

    This class is PROTECTED and cannot be modified by BYRD.
    """

    def __init__(self, log_dir: str = "./modification_logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self._entries: List[ModificationEntry] = []
        self._checkpoints: List[CheckpointEntry] = []

        # Load existing log if present
        self._load()

    def _compute_chain_hash(self, entry: ModificationEntry) -> str:
        """Compute hash linking to previous entry."""
        if not self._entries:
            previous = "GENESIS"
        else:
            previous = self._entries[-1].previous_entry_hash

        data = json.dumps({
            "previous": previous,
            "id": entry.id,
            "timestamp": entry.timestamp,
            "target_file": entry.target_file,
            "desire_id": entry.desire_id,
            "provenance_hash": entry.provenance_hash,
            "code_hash_before": entry.code_hash_before,
            "code_hash_after": entry.code_hash_after,
        }, sort_keys=True)

        return hashlib.sha256(data.encode()).hexdigest()

    def _compute_file_hash(self, filepath: str) -> str:
        """Compute hash of file contents."""
        try:
            with open(filepath, "r") as f:
                content = f.read()
            return hashlib.sha256(content.encode()).hexdigest()
        except FileNotFoundError:
            return "FILE_NOT_FOUND"
        except Exception as e:
            return f"ERROR:{str(e)}"

    def log_modification(
        self,
        modification_id: str,
        target_file: str,
        target_component: str,
        desire_id: str,
        desire_description: str,
        provenance_hash: str,
        change_description: str,
        code_before: str,
        code_after: str,
        success: bool,
        error_message: Optional[str] = None
    ) -> ModificationEntry:
        """
        Log a modification attempt.

        This creates an immutable record of the modification,
        whether it succeeded or failed.
        """
        entry = ModificationEntry(
            id=modification_id,
            timestamp=datetime.utcnow().isoformat(),
            target_file=target_file,
            target_component=target_component,
            desire_id=desire_id,
            desire_description=desire_description,
            provenance_hash=provenance_hash,
            change_description=change_description,
            code_hash_before=hashlib.sha256(code_before.encode()).hexdigest(),
            code_hash_after=hashlib.sha256(code_after.encode()).hexdigest(),
            success=success,
            error_message=error_message,
        )

        # Compute chain hash
        entry.previous_entry_hash = self._compute_chain_hash(entry)

        self._entries.append(entry)
        self._save()

        return entry

    def log_rollback(
        self,
        original_modification_id: str,
        rollback_modification_id: str
    ) -> bool:
        """Mark a modification as rolled back."""
        for entry in self._entries:
            if entry.id == original_modification_id:
                entry.rollback_id = rollback_modification_id
                self._save()
                return True
        return False

    def create_checkpoint(
        self,
        checkpoint_id: str,
        trigger: str,
        modification_id: Optional[str],
        files: List[str],
        checkpoint_path: str
    ) -> CheckpointEntry:
        """Create a checkpoint record."""
        # Compute integrity hash of all files
        file_hashes = {}
        for f in files:
            file_hashes[f] = self._compute_file_hash(f)

        integrity_hash = hashlib.sha256(
            json.dumps(file_hashes, sort_keys=True).encode()
        ).hexdigest()

        entry = CheckpointEntry(
            id=checkpoint_id,
            timestamp=datetime.utcnow().isoformat(),
            trigger=trigger,
            modification_id=modification_id,
            files_included=files,
            checkpoint_path=checkpoint_path,
            integrity_hash=integrity_hash,
        )

        self._checkpoints.append(entry)
        self._save()

        return entry

    def get_entry(self, modification_id: str) -> Optional[ModificationEntry]:
        """Get a specific log entry."""
        for entry in self._entries:
            if entry.id == modification_id:
                return entry
        return None

    def get_entries_for_desire(self, desire_id: str) -> List[ModificationEntry]:
        """Get all modifications triggered by a desire."""
        return [e for e in self._entries if e.desire_id == desire_id]

    def get_entries_for_file(self, filepath: str) -> List[ModificationEntry]:
        """Get all modifications to a file."""
        filename = Path(filepath).name
        return [e for e in self._entries if Path(e.target_file).name == filename]

    def get_recent_entries(self, limit: int = 10) -> List[ModificationEntry]:
        """Get recent modification entries."""
        return list(reversed(self._entries[-limit:]))

    def get_checkpoint(self, checkpoint_id: str) -> Optional[CheckpointEntry]:
        """Get a specific checkpoint."""
        for cp in self._checkpoints:
            if cp.id == checkpoint_id:
                return cp
        return None

    def get_checkpoint_for_modification(
        self,
        modification_id: str
    ) -> Optional[CheckpointEntry]:
        """Get the checkpoint created before a modification."""
        for cp in self._checkpoints:
            if cp.modification_id == modification_id:
                return cp
        return None

    def get_latest_checkpoint(self) -> Optional[CheckpointEntry]:
        """Get the most recent checkpoint."""
        if not self._checkpoints:
            return None
        return self._checkpoints[-1]

    def verify_chain_integrity(self) -> Tuple[bool, List[str]]:
        """
        Verify the integrity of the log chain.

        Returns:
            (valid, list_of_issues)
        """
        issues = []

        for i, entry in enumerate(self._entries):
            expected_hash = self._compute_chain_hash(entry)
            if entry.previous_entry_hash != expected_hash:
                issues.append(f"Entry {entry.id} has invalid chain hash")

        return len(issues) == 0, issues

    def get_statistics(self) -> Dict:
        """Get log statistics."""
        successful = len([e for e in self._entries if e.success])
        failed = len([e for e in self._entries if not e.success])
        rolled_back = len([e for e in self._entries if e.rollback_id])

        files_modified = set(e.target_file for e in self._entries)
        desires_acted = set(e.desire_id for e in self._entries)

        return {
            "total_modifications": len(self._entries),
            "successful": successful,
            "failed": failed,
            "rolled_back": rolled_back,
            "unique_files_modified": len(files_modified),
            "unique_desires_acted": len(desires_acted),
            "total_checkpoints": len(self._checkpoints),
        }

    def _save(self):
        """Save log to disk."""
        log_file = self.log_dir / "modification_log.json"
        data = {
            "entries": [asdict(e) for e in self._entries],
            "checkpoints": [asdict(c) for c in self._checkpoints],
        }
        with open(log_file, "w") as f:
            json.dump(data, f, indent=2)

    def _load(self):
        """Load log from disk."""
        log_file = self.log_dir / "modification_log.json"
        if log_file.exists():
            try:
                with open(log_file, "r") as f:
                    data = json.load(f)

                self._entries = [
                    ModificationEntry(**e) for e in data.get("entries", [])
                ]
                self._checkpoints = [
                    CheckpointEntry(**c) for c in data.get("checkpoints", [])
                ]
            except Exception as e:
                print(f"Warning: Could not load modification log: {e}")

    def export_log(self) -> Dict:
        """Export the full log as a dictionary."""
        return {
            "entries": [asdict(e) for e in self._entries],
            "checkpoints": [asdict(c) for c in self._checkpoints],
            "statistics": self.get_statistics(),
            "exported_at": datetime.utcnow().isoformat(),
        }


# Type hint for tuple return
from typing import Tuple
