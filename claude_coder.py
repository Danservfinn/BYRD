"""
Claude Coder - BYRD's agentic coding capability via Claude Agent SDK.

Uses Claude Max subscription for tool execution:
- Read: Read files for context
- Write: Create new files
- Edit: Modify files in-place
- Bash: Run commands and tests
- Glob: Find files by pattern
- Grep: Search file contents

Constitutional constraints enforced via hooks.

Part of BYRD's Hybrid LLM Architecture.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any

logger = logging.getLogger(__name__)

# Import will be available after: pip install claude-code-sdk
try:
    from claude_code_sdk import (
        query,
        ClaudeCodeOptions,
        Message,
    )
    CLAUDE_SDK_AVAILABLE = True
    logger.info("[ClaudeCoder] Claude Code SDK available")
except ImportError:
    CLAUDE_SDK_AVAILABLE = False
    logger.warning("[ClaudeCoder] claude-code-sdk not installed. Run: pip install claude-code-sdk")


@dataclass
class ClaudeCoderResult:
    """Result of a Claude coding task."""
    success: bool
    output: str
    error: Optional[str] = None
    files_modified: List[str] = field(default_factory=list)
    files_created: List[str] = field(default_factory=list)
    duration_ms: int = 0
    session_id: Optional[str] = None
    turns_used: int = 0
    cost_usd: float = 0.0
    tool_calls: List[Dict] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "success": self.success,
            "output": self.output[:500] if self.output else "",
            "session_id": self.session_id,
            "cost_usd": self.cost_usd,
            "files_modified": self.files_modified,
            "files_created": self.files_created,
            "turns_used": self.turns_used,
            "duration_ms": self.duration_ms,
            "error": self.error,
            "tool_calls_count": len(self.tool_calls),
        }


class ClaudeCoder:
    """
    BYRD's coding capability via Claude Code SDK.

    Uses Claude Max subscription (no API key needed after `claude login`).
    Enforces constitutional constraints via pre-execution checks.
    """

    # Constitutional constraints - files that cannot be modified
    PROTECTED_PATHS = [
        "provenance.py",
        "modification_log.py",
        "self_modification.py",
        "constitutional.py",
        "safety_monitor.py",
    ]

    # Dangerous bash patterns that are blocked
    DANGEROUS_PATTERNS = [
        "rm -rf /",
        "rm -rf ~",
        "rm -rf .",
        "format c:",
        "del /s /q",
        "drop database",
        "sudo rm",
        "> /dev/sda",
        "mkfs.",
        ":(){:|:&};:",  # Fork bomb
        "chmod -R 777 /",
        "dd if=/dev/zero",
    ]

    def __init__(
        self,
        config: Dict = None,
        coordinator=None,
        memory=None,
        working_dir: str = None,
    ):
        self.config = config or {}
        self.coordinator = coordinator
        self.memory = memory
        self.working_dir = working_dir or str(Path.cwd())

        # Configuration
        self._model = self.config.get("model", "claude-sonnet-4-20250514")
        self._max_turns = self.config.get("max_turns", 20)
        self._enabled = CLAUDE_SDK_AVAILABLE and self.config.get("enabled", True)

        # Load additional protected paths from config
        extra_protected = self.config.get("protected_paths", [])
        self._protected_paths = list(set(self.PROTECTED_PATHS + extra_protected))

        # Execution tracking
        self._execution_count = 0
        self._total_tool_calls = 0
        self._files_tracked: Dict[str, List[str]] = {}
        self._blocked_attempts = 0

        if not CLAUDE_SDK_AVAILABLE:
            logger.warning("[ClaudeCoder] SDK not available - install claude-code-sdk")
        else:
            logger.info(f"[ClaudeCoder] Initialized: model={self._model}, max_turns={self._max_turns}")

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool):
        self._enabled = value and CLAUDE_SDK_AVAILABLE

    def _check_protected_files(self, task: str) -> Optional[str]:
        """
        Check if task attempts to modify protected files.

        Returns error message if blocked, None if allowed.
        """
        task_lower = task.lower()

        for protected in self._protected_paths:
            protected_lower = protected.lower()
            # Check for edit/modify/change/delete operations on protected files
            if protected_lower in task_lower:
                # Check if it's a modification operation
                mod_keywords = ["edit", "modify", "change", "delete", "remove", "update", "write"]
                for keyword in mod_keywords:
                    if keyword in task_lower:
                        self._blocked_attempts += 1
                        logger.warning(f"[ClaudeCoder] BLOCKED: Attempted to {keyword} protected file {protected}")
                        return f"Constitutional constraint: Cannot {keyword} protected file '{protected}'"

        return None

    def _check_dangerous_commands(self, task: str) -> Optional[str]:
        """
        Check if task contains dangerous command patterns.

        Returns error message if blocked, None if allowed.
        """
        task_lower = task.lower()

        for pattern in self.DANGEROUS_PATTERNS:
            if pattern.lower() in task_lower:
                self._blocked_attempts += 1
                logger.warning(f"[ClaudeCoder] BLOCKED: Dangerous command pattern: {pattern}")
                return f"Safety constraint: Dangerous pattern blocked: '{pattern}'"

        return None

    def _build_system_prompt(self, desire_id: str = None) -> str:
        """Build system prompt with BYRD context and constraints."""
        protected_list = "\n".join(f"- {p}" for p in self._protected_paths)

        return f"""You are BYRD's coding agent. Execute the requested task precisely.

WORKING DIRECTORY: {self.working_dir}

CAPABILITIES:
- Read any file to understand context
- Edit files to implement changes
- Create new files when needed
- Run bash commands for testing/validation
- Search codebase with glob/grep

CONSTITUTIONAL CONSTRAINTS (NEVER VIOLATE):
The following files are PROTECTED and cannot be modified:
{protected_list}

DANGEROUS COMMANDS (NEVER EXECUTE):
- rm -rf with / or ~ or .
- Any command that could destroy the system
- Fork bombs or resource exhaustion attacks

GUIDELINES:
1. Read relevant files first to understand context
2. Make minimal, focused changes
3. Run tests after modifications when possible
4. Explain what you changed and why
5. Follow existing code style and patterns
6. If you cannot complete a task, explain why clearly

DESIRE_ID: {desire_id or 'unspecified'}
"""

    async def execute(
        self,
        prompt: str,
        context: Optional[Dict] = None,
        desire_id: str = None,
    ) -> ClaudeCoderResult:
        """
        Execute a coding task using Claude Code SDK.

        Args:
            prompt: The coding task to execute
            context: Optional context from Z.AI orchestrator
            desire_id: Desire ID for provenance tracking

        Returns:
            ClaudeCoderResult with execution details
        """
        start_time = datetime.now()
        self._execution_count += 1

        if not desire_id:
            desire_id = datetime.now().strftime("%Y%m%d%H%M%S%f")

        if not self._enabled:
            return ClaudeCoderResult(
                success=False,
                output="",
                error="Claude Coder is disabled (SDK not available or disabled in config)",
                session_id=desire_id,
            )

        # Pre-execution constitutional checks
        protected_error = self._check_protected_files(prompt)
        if protected_error:
            return ClaudeCoderResult(
                success=False,
                output="",
                error=protected_error,
                session_id=desire_id,
            )

        dangerous_error = self._check_dangerous_commands(prompt)
        if dangerous_error:
            return ClaudeCoderResult(
                success=False,
                output="",
                error=dangerous_error,
                session_id=desire_id,
            )

        # Build task with context from Z.AI
        task = prompt
        if context:
            context_parts = []
            for key, value in context.items():
                if value:
                    if isinstance(value, list):
                        context_parts.append(f"## {key}\n" + "\n".join(f"- {v}" for v in value[:5]))
                    else:
                        context_parts.append(f"## {key}\n{value}")
            if context_parts:
                task = f"CONTEXT FROM BYRD:\n{chr(10).join(context_parts)}\n\nTASK:\n{prompt}"

        logger.info(f"[ClaudeCoder] Executing: {task[:100]}...")

        if self.coordinator:
            self.coordinator.coder_started(task[:50])

        try:
            self._files_tracked[desire_id] = []

            # Collect results
            output_parts = []
            tool_calls = []
            session_id = desire_id
            cost_usd = 0.0

            # Build options
            options = ClaudeCodeOptions(
                max_turns=self._max_turns,
                system_prompt=self._build_system_prompt(desire_id),
                cwd=self.working_dir,
            )

            # Execute via SDK - collect all messages
            async for message in query(prompt=task, options=options):
                # Handle different message types
                if hasattr(message, 'type'):
                    if message.type == 'assistant':
                        # Assistant text response
                        if hasattr(message, 'content'):
                            for block in message.content:
                                if hasattr(block, 'text'):
                                    output_parts.append(block.text)
                                elif hasattr(block, 'type') and block.type == 'tool_use':
                                    tool_name = getattr(block, 'name', 'unknown')
                                    tool_input = getattr(block, 'input', {})
                                    tool_calls.append({
                                        'tool': tool_name,
                                        'input': tool_input,
                                    })
                                    self._total_tool_calls += 1

                                    # Track file modifications
                                    if tool_name in ('Write', 'Edit'):
                                        file_path = tool_input.get('file_path', '')
                                        if file_path:
                                            self._files_tracked[desire_id].append(file_path)

                    elif message.type == 'result':
                        # Final result
                        if hasattr(message, 'session_id'):
                            session_id = message.session_id
                        if hasattr(message, 'cost_usd'):
                            cost_usd = message.cost_usd or 0.0
                        if hasattr(message, 'result') and message.result:
                            output_parts.append(f"\n\n{message.result}")

            duration = (datetime.now() - start_time).total_seconds()
            files_modified = self._files_tracked.get(desire_id, [])

            # Record provenance
            if self.memory:
                await self._record_provenance(prompt, desire_id, "\n".join(output_parts), files_modified, tool_calls)

            logger.info(f"[ClaudeCoder] Success: {len(tool_calls)} tools, {len(files_modified)} files, {duration:.1f}s")

            return ClaudeCoderResult(
                success=True,
                output="\n".join(output_parts),
                session_id=session_id,
                duration_ms=int(duration * 1000),
                cost_usd=cost_usd,
                files_modified=files_modified,
                tool_calls=tool_calls,
                turns_used=len(tool_calls),
            )

        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            logger.error(f"[ClaudeCoder] Error: {e}")
            return ClaudeCoderResult(
                success=False,
                output="",
                error=str(e),
                session_id=desire_id,
                duration_ms=int(duration * 1000),
            )
        finally:
            if self.coordinator:
                self.coordinator.coder_finished()

    async def _record_provenance(
        self,
        task: str,
        desire_id: str,
        output: str,
        files_modified: List[str],
        tool_calls: List[Dict],
    ):
        """Record modification provenance to memory."""
        if not self.memory:
            return
        try:
            tools_summary = ", ".join(t['tool'] for t in tool_calls[:10])
            content = (
                f"[CLAUDE_CODER] Task: {task[:100]}\n"
                f"Tools used: {tools_summary}\n"
                f"Files modified: {', '.join(files_modified) if files_modified else 'none'}\n"
                f"Desire ID: {desire_id}"
            )
            await self.memory.record_experience(content=content, type="claude_coder")
        except Exception as e:
            logger.error(f"Error recording provenance: {e}")

    async def analyze(self, file_path: str, question: str) -> str:
        """
        Analyze a file without modifying it (read-only).

        Args:
            file_path: Path to the file to analyze
            question: Question about the file

        Returns:
            Analysis result
        """
        result = await self.execute(
            prompt=f"Read {file_path} and answer: {question}\n\nDo NOT modify any files.",
        )
        return result.output if result.success else f"Analysis failed: {result.error}"

    async def can_execute(self, task: str) -> Dict[str, Any]:
        """
        Check if a task can be executed (pre-flight check).

        Args:
            task: The task description

        Returns:
            Dict with can_execute bool and reason
        """
        # Check protected files
        protected_error = self._check_protected_files(task)
        if protected_error:
            return {
                "can_execute": False,
                "reason": protected_error,
            }

        # Check dangerous patterns
        dangerous_error = self._check_dangerous_commands(task)
        if dangerous_error:
            return {
                "can_execute": False,
                "reason": dangerous_error,
            }

        return {
            "can_execute": self._enabled,
            "reason": None if self._enabled else "SDK not available or disabled",
        }

    def get_stats(self) -> Dict[str, Any]:
        """Get coder statistics."""
        return {
            "enabled": self._enabled,
            "sdk_available": CLAUDE_SDK_AVAILABLE,
            "execution_count": self._execution_count,
            "total_tool_calls": self._total_tool_calls,
            "blocked_attempts": self._blocked_attempts,
            "model": self._model,
            "max_turns": self._max_turns,
            "protected_paths": self._protected_paths,
            "mode": "claude-code-sdk",
        }

    def reset(self):
        """Reset coder state."""
        self._execution_count = 0
        self._total_tool_calls = 0
        self._blocked_attempts = 0
        self._files_tracked = {}
        logger.info("[ClaudeCoder] State reset")
