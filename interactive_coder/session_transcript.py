"""
session_transcript.py - JSONL Session Logging

Logs each coding session turn-by-turn in JSONL format for:
- Debugging and analysis
- Session resumption
- Learning from past sessions
"""

import json
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, IO

logger = logging.getLogger(__name__)


@dataclass
class TranscriptEntry:
    """A single entry in the session transcript."""
    type: str
    timestamp: datetime = field(default_factory=datetime.now)
    data: Dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> str:
        """Convert to JSON string."""
        entry = {
            "type": self.type,
            "timestamp": self.timestamp.isoformat(),
            **self.data,
        }
        return json.dumps(entry, default=str)


class SessionTranscript:
    """
    JSONL session logger for coding interactions.

    Each session creates a separate .jsonl file with entries for:
    - session_start: Session initialization
    - turn: Each coder execution
    - evaluation: Satisfaction evaluation results
    - refinement: Refinement generation
    - todo_extraction: TODOs extracted from output
    - error_recovery: Error recovery attempts
    - session_end: Final summary
    """

    def __init__(self, session_dir: Path = None):
        """
        Initialize the transcript logger.

        Args:
            session_dir: Directory to store session files
        """
        self.session_dir = session_dir or Path("coding_sessions")
        self.session_dir.mkdir(parents=True, exist_ok=True)

        self.session_id: Optional[str] = None
        self.desire_id: Optional[str] = None
        self._file_handle: Optional[IO] = None
        self._file_path: Optional[Path] = None
        self._entries: List[TranscriptEntry] = []
        self._turn_count = 0

    def start_session(self, desire_id: str, desire_description: str = "") -> str:
        """
        Start a new session.

        Args:
            desire_id: ID of the desire being fulfilled
            desire_description: Description of the desire

        Returns:
            Session ID
        """
        # Generate session ID
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_id = f"session_{timestamp}_{desire_id[:8]}"
        self.desire_id = desire_id
        self._turn_count = 0
        self._entries = []

        # Create session file
        self._file_path = self.session_dir / f"{self.session_id}.jsonl"
        self._file_handle = open(self._file_path, "w")

        # Log session start
        self._log_entry(TranscriptEntry(
            type="session_start",
            data={
                "session_id": self.session_id,
                "desire_id": desire_id,
                "desire_description": desire_description,
            }
        ))

        logger.info(f"Started session: {self.session_id}")
        return self.session_id

    def log_turn(
        self,
        turn_number: int,
        prompt: str,
        result: "CoderResult",
    ):
        """
        Log a coder turn.

        Args:
            turn_number: Turn number (1-indexed)
            prompt: The prompt sent to the coder
            result: The coder result
        """
        self._turn_count = turn_number

        self._log_entry(TranscriptEntry(
            type="turn",
            data={
                "turn_number": turn_number,
                "prompt": prompt[:2000],  # Truncate for storage
                "output": result.output[:5000] if result.output else "",
                "success": result.success,
                "error": result.error,
                "files_modified": result.files_modified,
                "files_created": result.files_created,
                "duration_ms": result.duration_ms,
            }
        ))

    def log_evaluation(
        self,
        turn_number: int,
        evaluation: "SatisfactionResult",
    ):
        """
        Log satisfaction evaluation.

        Args:
            turn_number: Turn number being evaluated
            evaluation: The evaluation result
        """
        self._log_entry(TranscriptEntry(
            type="evaluation",
            data={
                "turn_number": turn_number,
                "satisfaction": evaluation.score,
                "satisfied": evaluation.satisfied,
                "gaps": evaluation.gaps,
                "next_instruction": evaluation.next_instruction,
                "method_used": evaluation.method_used,
                "decision": "satisfied" if evaluation.satisfied else "refine",
            }
        ))

    def log_refinement(
        self,
        turn_number: int,
        instruction: str,
        context_added: Dict[str, Any] = None,
    ):
        """
        Log refinement generation.

        Args:
            turn_number: Turn number after which refinement was generated
            instruction: The refinement instruction
            context_added: Additional context provided
        """
        self._log_entry(TranscriptEntry(
            type="refinement",
            data={
                "turn_number": turn_number,
                "instruction": instruction,
                "context_added": context_added or {},
            }
        ))

    def log_todo_extraction(
        self,
        turn_number: int,
        todos: List[Dict],
    ):
        """
        Log TODO extraction.

        Args:
            turn_number: Turn from which TODOs were extracted
            todos: List of extracted TODOs
        """
        self._log_entry(TranscriptEntry(
            type="todo_extraction",
            data={
                "turn_number": turn_number,
                "todos": todos,
                "count": len(todos),
            }
        ))

    def log_error_recovery(
        self,
        turn_number: int,
        error_type: str,
        recovery_strategy: str,
        recovered: bool,
    ):
        """
        Log error recovery attempt.

        Args:
            turn_number: Turn in which error occurred
            error_type: Type of error
            recovery_strategy: Strategy used
            recovered: Whether recovery succeeded
        """
        self._log_entry(TranscriptEntry(
            type="error_recovery",
            data={
                "turn_number": turn_number,
                "error_type": error_type,
                "recovery_strategy": recovery_strategy,
                "recovered": recovered,
            }
        ))

    def log_state_transition(
        self,
        from_state: str,
        to_state: str,
        trigger: str,
    ):
        """
        Log state machine transition.

        Args:
            from_state: Previous state
            to_state: New state
            trigger: What caused the transition
        """
        self._log_entry(TranscriptEntry(
            type="state_transition",
            data={
                "from_state": from_state,
                "to_state": to_state,
                "trigger": trigger,
            }
        ))

    def end_session(
        self,
        success: bool,
        final_satisfaction: float,
        summary: Dict[str, Any] = None,
    ):
        """
        End the session and close the file.

        Args:
            success: Whether the session was successful
            final_satisfaction: Final satisfaction score
            summary: Optional summary data
        """
        self._log_entry(TranscriptEntry(
            type="session_end",
            data={
                "success": success,
                "total_turns": self._turn_count,
                "final_satisfaction": final_satisfaction,
                "summary": summary or {},
            }
        ))

        if self._file_handle:
            self._file_handle.close()
            self._file_handle = None

        logger.info(
            f"Ended session {self.session_id}: "
            f"success={success}, turns={self._turn_count}, "
            f"satisfaction={final_satisfaction:.2f}"
        )

    def get_session_context(self, last_n_turns: int = 5) -> str:
        """
        Get formatted context from recent turns for the next turn.

        Args:
            last_n_turns: Number of recent turns to include

        Returns:
            Formatted context string
        """
        turns = [e for e in self._entries if e.type == "turn"]
        recent = turns[-last_n_turns:] if len(turns) > last_n_turns else turns

        if not recent:
            return ""

        context_parts = []
        for entry in recent:
            turn_num = entry.data.get("turn_number", "?")
            output_preview = entry.data.get("output", "")[:500]
            files = entry.data.get("files_modified", []) + entry.data.get("files_created", [])

            context_parts.append(f"""
## Turn {turn_num}
Files: {', '.join(files) if files else 'None'}
Output Preview: {output_preview}...""")

        return "\n".join(context_parts)

    def get_gaps_so_far(self) -> List[str]:
        """Get all gaps identified across evaluations."""
        all_gaps = []
        for entry in self._entries:
            if entry.type == "evaluation":
                all_gaps.extend(entry.data.get("gaps", []))
        return list(set(all_gaps))  # Deduplicate

    def get_files_modified(self) -> List[str]:
        """Get all files modified across all turns."""
        all_files = set()
        for entry in self._entries:
            if entry.type == "turn":
                all_files.update(entry.data.get("files_modified", []))
                all_files.update(entry.data.get("files_created", []))
        return list(all_files)

    def _log_entry(self, entry: TranscriptEntry):
        """Write entry to file and memory."""
        self._entries.append(entry)
        if self._file_handle:
            self._file_handle.write(entry.to_json() + "\n")
            self._file_handle.flush()  # Ensure it's written

    def get_turn_count(self) -> int:
        """Get current turn count."""
        return self._turn_count

    def get_session_path(self) -> Optional[Path]:
        """Get path to session file."""
        return self._file_path

    @classmethod
    def load_session(cls, session_path: Path) -> List[Dict]:
        """
        Load a previous session from file.

        Args:
            session_path: Path to session file

        Returns:
            List of session entries
        """
        entries = []
        with open(session_path, "r") as f:
            for line in f:
                if line.strip():
                    entries.append(json.loads(line))
        return entries

    def reset(self):
        """Reset transcript state."""
        if self._file_handle:
            self._file_handle.close()
            self._file_handle = None

        self.session_id = None
        self.desire_id = None
        self._file_path = None
        self._entries = []
        self._turn_count = 0
