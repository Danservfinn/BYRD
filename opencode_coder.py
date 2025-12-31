"""
opencode_coder.py - CLI Wrapper for BYRD's Coding Engine

Wraps an external coding CLI to gain bash, LSP, webfetch, and MCP capabilities.

Replaces: coder.py, actor.py, agent_coder.py

Why CLI wrapper instead of custom agent:
- CLI provides bash, LSP, webfetch, MCP servers
- Duplicating this in agent_coder.py was wasteful
- CLI wrapper is simpler, more maintainable, more capable

Integrates with:
- ComponentCoordinator for rate limiting
- ContextLoader for tiered context
- Memory for provenance tracking
"""

import asyncio
import logging
import os
import shutil
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

logger = logging.getLogger(__name__)


@dataclass
class CoderResult:
    """Result of a coding task execution."""
    success: bool
    output: str
    error: Optional[str] = None
    files_modified: List[str] = field(default_factory=list)
    files_created: List[str] = field(default_factory=list)
    duration_seconds: float = 0.0
    provenance: Optional[Dict] = None
    # Compatibility fields for drop-in replacement of coder.py
    cost_usd: float = 0.0
    session_id: Optional[str] = None
    turns_used: int = 0
    duration_ms: int = 0

    def to_dict(self) -> Dict:
        """Convert to dictionary for logging."""
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
        }


@dataclass
class ModificationRecord:
    """Record of a code modification."""
    desire_id: str
    task: str
    files: List[str]
    timestamp: datetime = field(default_factory=datetime.now)
    success: bool = True
    rollback_available: bool = False


class OpenCodeCoder:
    """
    BYRD's coding and self-modification engine.

    Wraps an external CLI to leverage its full capability set.
    Falls back to subprocess execution if CLI not available.

    Capabilities gained by wrapping:
    - bash: Full shell access for builds, tests, git
    - LSP: Language server protocol for code intelligence
    - webfetch: Web research without separate implementation
    - MCP: Model Context Protocol for external tools
    """

    # CLI options to try in order of preference
    CLI_OPTIONS = [
        ("opencode", ["--model", "glm-4.7"]),  # Primary: OpenCode CLI
        ("claude", []),  # Fallback: Claude Code CLI
    ]

    # Modification keywords that trigger component context loading
    MODIFICATION_KEYWORDS = [
        "modify", "edit", "change", "add to", "remove from",
        "refactor", "fix", "implement", "update", "improve",
    ]

    def __init__(
        self,
        config: Dict = None,
        coordinator=None,
        context_loader=None,
        memory=None,
    ):
        """
        Initialize the OpenCode coder.

        Args:
            config: Configuration dict
            coordinator: ComponentCoordinator for signaling
            context_loader: ContextLoader for tiered context
            memory: Memory instance for provenance
        """
        self.config = config or {}
        self.coordinator = coordinator
        self.context_loader = context_loader
        self.memory = memory

        # Find available CLI
        self._cli_command, self._cli_args = self._find_cli()

        # Modification tracking
        self._modifications: List[ModificationRecord] = []
        self._execution_count = 0

        # Protected paths (never modify)
        self._protected_paths = self.config.get("protected_paths", [
            "provenance.py",
            "modification_log.py",
            "self_modification.py",
            "constitutional.py",
            "safety_monitor.py",
        ])

        # Rate limiting
        self._rate_limit_seconds = self.config.get("rate_limit_seconds", 10.0)
        self._last_execution: Optional[datetime] = None

        # Enabled status (for compatibility with coder.py interface)
        config_enabled = self.config.get("enabled", True)
        self._enabled = config_enabled and self._cli_command is not None

    @property
    def enabled(self) -> bool:
        """Check if coder is enabled (property for compatibility)."""
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool):
        """Set enabled state."""
        self._enabled = value

    def _find_cli(self) -> Tuple[Optional[str], List[str]]:
        """Find available CLI command."""
        for cmd, args in self.CLI_OPTIONS:
            if shutil.which(cmd):
                logger.info(f"Found CLI: {cmd}")
                return cmd, args

        logger.warning("No coding CLI found - will use subprocess fallback")
        return None, []

    async def execute(
        self,
        prompt: str,
        context: Optional[Dict] = None,
        working_dir: Optional[str] = None,
        desire_id: str = None
    ) -> CoderResult:
        """
        Execute a coding/modification task.

        This method is a drop-in replacement for coder.py and agent_coder.py.

        1. Check if enabled
        2. Signal ComponentCoordinator (pause other LLM calls)
        3. Check constitutional constraints
        4. Load tiered context
        5. Execute CLI or subprocess
        6. Record provenance
        7. Signal completion

        Args:
            prompt: The coding task prompt (for compatibility with coder.py)
            context: Optional context dict (for compatibility with coder.py)
            working_dir: Optional working directory override
            desire_id: ID of the originating desire (optional)

        Returns:
            CoderResult with success status and output
        """
        # Use prompt as task for internal processing
        task = prompt

        # Generate desire_id if not provided
        if not desire_id:
            desire_id = datetime.now().strftime("%Y%m%d%H%M%S%f")

        start_time = datetime.now()
        self._execution_count += 1

        # Check if enabled
        if not self._enabled:
            return CoderResult(
                success=False,
                output="",
                error="Coder is disabled or no CLI available",
                session_id=desire_id,
            )

        # Check rate limiting
        if self._last_execution:
            elapsed = (start_time - self._last_execution).total_seconds()
            if elapsed < self._rate_limit_seconds:
                await asyncio.sleep(self._rate_limit_seconds - elapsed)

        # Check constitutional constraints
        constraint_check = self._check_constitutional(task)
        if not constraint_check["allowed"]:
            return CoderResult(
                success=False,
                output="",
                error=f"Constitutional constraint violation: {constraint_check['reason']}",
                session_id=desire_id,
            )

        # Signal coordinator - other components pause LLM calls
        if self.coordinator:
            self.coordinator.coder_started(task[:50])

        try:
            # Load tiered context (merge with provided context)
            loaded_context = await self._build_context(task)
            if context:
                # Append provided context to loaded context
                context_str = "\n".join(f"# {k}\n{v}" for k, v in context.items() if v)
                loaded_context = f"{loaded_context}\n\n{context_str}"

            # Build full prompt
            full_prompt = f"{loaded_context}\n\n# TASK\n{task}"

            # Execute (pass working_dir to CLI runner)
            if self._cli_command:
                result = await self._run_cli(full_prompt, task, working_dir)
            else:
                result = await self._run_subprocess(full_prompt, task, working_dir)

            # Record provenance
            if result.success:
                await self._record_provenance(task, desire_id, result)

            # Track modification
            self._modifications.append(ModificationRecord(
                desire_id=desire_id,
                task=task,
                files=result.files_modified + result.files_created,
                success=result.success,
            ))

            self._last_execution = datetime.now()
            duration = (self._last_execution - start_time).total_seconds()
            result.duration_seconds = duration
            result.duration_ms = int(duration * 1000)
            result.session_id = desire_id

            return result

        finally:
            if self.coordinator:
                self.coordinator.coder_finished()

    async def _build_context(self, task: str) -> str:
        """Build context based on task type."""
        context_parts = []

        # Always load tier 1
        if self.context_loader:
            tier1 = await self.context_loader.load_tier1()
            context_parts.append(tier1)

            # Load tier 2 if modification task
            if self._needs_component_context(task):
                tier2 = await self.context_loader.load_tier2("component")
                context_parts.append(tier2)

        return "\n\n".join(context_parts)

    def _needs_component_context(self, task: str) -> bool:
        """Determine if task needs component-level context."""
        task_lower = task.lower()
        return any(kw in task_lower for kw in self.MODIFICATION_KEYWORDS)

    def _check_constitutional(self, task: str) -> Dict[str, Any]:
        """Check if task violates constitutional constraints."""
        task_lower = task.lower()

        # Check for protected file references
        for protected in self._protected_paths:
            if protected.lower() in task_lower:
                return {
                    "allowed": False,
                    "reason": f"Cannot modify protected file: {protected}",
                }

        # Check for dangerous patterns
        dangerous_patterns = [
            "rm -rf",
            "format c:",
            "del /s",
            "drop database",
            "sudo rm",
        ]
        for pattern in dangerous_patterns:
            if pattern in task_lower:
                return {
                    "allowed": False,
                    "reason": f"Dangerous pattern detected: {pattern}",
                }

        return {"allowed": True, "reason": None}

    async def _run_cli(self, prompt: str, task: str, working_dir: Optional[str] = None) -> CoderResult:
        """Execute task via CLI."""
        try:
            # Build command
            cmd = [self._cli_command] + self._cli_args

            # Add task argument based on CLI type
            if self._cli_command == "opencode":
                cmd.extend(["--task", task])
            elif self._cli_command == "claude":
                cmd.extend(["--print", task])

            # Set environment
            env = os.environ.copy()
            env["OPENCODE_RATE_LIMIT"] = str(int(self._rate_limit_seconds))

            # Determine working directory
            cwd = working_dir or self.config.get("project_root", ".")

            # Execute
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env,
                cwd=cwd,
            )

            stdout, stderr = await asyncio.wait_for(
                proc.communicate(),
                timeout=self.config.get("timeout_seconds", 300),
            )

            output = stdout.decode() if stdout else ""
            error = stderr.decode() if stderr else None

            # Parse modified files from output
            files_modified, files_created = self._parse_file_changes(output)

            return CoderResult(
                success=proc.returncode == 0,
                output=output,
                error=error if proc.returncode != 0 else None,
                files_modified=files_modified,
                files_created=files_created,
            )

        except asyncio.TimeoutError:
            return CoderResult(
                success=False,
                output="",
                error="Execution timed out",
            )
        except Exception as e:
            logger.error(f"CLI execution error: {e}")
            return CoderResult(
                success=False,
                output="",
                error=str(e),
            )

    async def _run_subprocess(self, prompt: str, task: str, working_dir: Optional[str] = None) -> CoderResult:
        """Fallback: Execute task via subprocess without external CLI."""
        # This is a minimal fallback for when no CLI is available
        # It can only execute simple shell commands

        # Determine working directory
        cwd = working_dir or self.config.get("project_root", ".")

        # Extract any shell commands from the task
        if "```bash" in task or "```shell" in task:
            # Extract command from code block
            import re
            match = re.search(r'```(?:bash|shell)\n(.*?)\n```', task, re.DOTALL)
            if match:
                command = match.group(1).strip()

                # Safety check
                if any(dangerous in command.lower() for dangerous in ["rm -rf", "sudo", "format"]):
                    return CoderResult(
                        success=False,
                        output="",
                        error="Dangerous command blocked",
                    )

                try:
                    proc = await asyncio.create_subprocess_shell(
                        command,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                        cwd=cwd,
                    )

                    stdout, stderr = await asyncio.wait_for(
                        proc.communicate(),
                        timeout=60,
                    )

                    return CoderResult(
                        success=proc.returncode == 0,
                        output=stdout.decode() if stdout else "",
                        error=stderr.decode() if stderr and proc.returncode != 0 else None,
                    )

                except Exception as e:
                    return CoderResult(
                        success=False,
                        output="",
                        error=str(e),
                    )

        # For non-shell tasks, we need a proper CLI
        return CoderResult(
            success=False,
            output="",
            error="No coding CLI available. Install 'opencode' or 'claude' CLI.",
        )

    def _parse_file_changes(self, output: str) -> Tuple[List[str], List[str]]:
        """Parse file changes from CLI output."""
        modified = []
        created = []

        # Common patterns in CLI output
        import re

        # Modified files
        for pattern in [
            r"Modified: (.+\.py)",
            r"Updated: (.+\.py)",
            r"Edited: (.+)",
        ]:
            modified.extend(re.findall(pattern, output))

        # Created files
        for pattern in [
            r"Created: (.+\.py)",
            r"New file: (.+)",
        ]:
            created.extend(re.findall(pattern, output))

        return list(set(modified)), list(set(created))

    async def _record_provenance(self, task: str, desire_id: str, result: CoderResult):
        """Record modification provenance to memory."""
        if not self.memory:
            return

        try:
            # Record as experience
            content = (
                f"[CODE_MODIFICATION] Task: {task[:100]}\n"
                f"Files modified: {', '.join(result.files_modified)}\n"
                f"Files created: {', '.join(result.files_created)}\n"
                f"Success: {result.success}"
            )

            await self.memory.record_experience(
                content=content,
                type="self_modification",
            )

            # Record provenance relationship if we have desire_id
            if desire_id and desire_id != "unknown":
                await self.memory.query("""
                    MATCH (d:Desire {id: $desire_id})
                    MATCH (e:Experience)
                    WHERE e.content CONTAINS $task_snippet
                    CREATE (e)-[:MOTIVATED_BY]->(d)
                """, {
                    "desire_id": desire_id,
                    "task_snippet": task[:50],
                })

        except Exception as e:
            logger.error(f"Error recording provenance: {e}")

    async def can_execute(self, task: str) -> Dict[str, Any]:
        """Check if a task can be executed."""
        constitutional = self._check_constitutional(task)
        cli_available = self._cli_command is not None

        return {
            "can_execute": constitutional["allowed"] and cli_available,
            "constitutional_ok": constitutional["allowed"],
            "cli_available": cli_available,
            "reason": constitutional.get("reason") or ("No CLI available" if not cli_available else None),
        }

    async def generate_code(self, prompt: str) -> str:
        """
        Generate code from a prompt.

        This is a convenience method for code generation that returns
        just the output string. Used by seeker.py for capability creation.

        Args:
            prompt: The code generation prompt

        Returns:
            Generated code as a string
        """
        result = await self.execute(prompt)
        return result.output if result.success else ""

    def get_modification_history(self, limit: int = 20) -> List[ModificationRecord]:
        """Get recent modification history."""
        return self._modifications[-limit:]

    def get_stats(self) -> Dict[str, Any]:
        """Get coder statistics."""
        return {
            "execution_count": self._execution_count,
            "modifications_count": len(self._modifications),
            "cli_command": self._cli_command,
            "protected_paths": self._protected_paths,
            "rate_limit_seconds": self._rate_limit_seconds,
        }

    def reset(self):
        """Reset the coder state."""
        self._modifications = []
        self._execution_count = 0
        self._last_execution = None


# Convenience function
def create_opencode_coder(
    config: Dict = None,
    coordinator=None,
    context_loader=None,
    memory=None,
) -> OpenCodeCoder:
    """Create a new OpenCodeCoder instance."""
    return OpenCodeCoder(
        config=config,
        coordinator=coordinator,
        context_loader=context_loader,
        memory=memory,
    )
