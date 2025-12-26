"""
BYRD Coder
Claude Code CLI wrapper for autonomous code generation.

Enables BYRD to use Claude Code as its "coding limb" for:
- Self-modification (improving its own code)
- Capability creation (building new features)
- Bug fixing and debugging
- General code generation tasks

This module wraps the Claude Code CLI, executing it non-interactively
with appropriate permissions while respecting constitutional constraints.
"""

import asyncio
import json
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

from constitutional import ConstitutionalConstraints


@dataclass
class CoderResult:
    """Result from a Claude Code CLI invocation."""

    success: bool
    output: str
    session_id: Optional[str] = None
    cost_usd: float = 0.0
    files_modified: List[str] = field(default_factory=list)
    turns_used: int = 0
    duration_ms: int = 0
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for logging."""
        return {
            "success": self.success,
            "output": self.output[:500] if self.output else "",
            "session_id": self.session_id,
            "cost_usd": self.cost_usd,
            "files_modified": self.files_modified,
            "turns_used": self.turns_used,
            "duration_ms": self.duration_ms,
            "error": self.error,
        }


class Coder:
    """
    Claude Code CLI wrapper for autonomous code generation.

    Executes Claude Code in non-interactive mode with controlled permissions.
    All modifications are tracked and can be validated against constitutional
    constraints post-execution.

    Philosophy:
    - BYRD's local LLM dreams and forms desires
    - When those desires involve code, Coder executes them
    - Constitutional constraints remain inviolable
    """

    def __init__(self, config: Dict, project_root: str = "."):
        """
        Initialize the Coder.

        Args:
            config: Configuration dictionary from config.yaml
            project_root: Root directory for Claude Code operations
        """
        self.cli_path = config.get("cli_path", "claude")

        # Check if CLI is actually available before enabling
        config_enabled = config.get("enabled", True)
        if config_enabled:
            self.enabled = self._check_cli_available()
            if not self.enabled:
                print(f"⚠️  Coder disabled: Claude CLI not found at '{self.cli_path}'")
        else:
            self.enabled = False
        self.max_turns = config.get("max_turns", 10)
        self.timeout_seconds = config.get("timeout_seconds", 300)
        self.output_format = config.get("output_format", "json")

        # Allowed tools for Claude Code
        self.allowed_tools = config.get("allowed_tools", [
            "Read", "Edit", "Bash", "Glob", "Grep"
        ])

        # Cost tracking
        self.max_cost_per_day_usd = config.get("max_cost_per_day_usd", 10.0)
        self.max_cost_per_invocation_usd = config.get("max_cost_per_invocation_usd", 2.0)
        self._daily_cost = 0.0
        self._last_cost_reset = datetime.now()

        # Project context
        self.project_root = Path(project_root).resolve()

        # Track invocations
        self._invocation_count = 0
        self._total_cost = 0.0

    def _check_cli_available(self) -> bool:
        """Check if Claude Code CLI is available."""
        import shutil
        if shutil.which(self.cli_path):
            return True
        # Also try direct path check
        cli_path = Path(self.cli_path)
        if cli_path.exists() and cli_path.is_file():
            return True
        return False

    def _reset_daily_cost_if_needed(self):
        """Reset daily cost counter if a new day has started."""
        now = datetime.now()
        if now - self._last_cost_reset > timedelta(days=1):
            self._daily_cost = 0.0
            self._last_cost_reset = now

    def reset(self):
        """Reset coder state for fresh start."""
        self._daily_cost = 0.0
        self._last_cost_reset = datetime.now()
        self._invocation_count = 0
        self._total_cost = 0.0

    def _build_command(self, prompt: str) -> List[str]:
        """
        Build the Claude Code CLI command.

        Args:
            prompt: The prompt to send to Claude Code

        Returns:
            List of command arguments
        """
        cmd = [
            self.cli_path,
            "-p", prompt,
            "--output-format", self.output_format,
            "--permission-mode", "acceptEdits",
            "--max-turns", str(self.max_turns),
        ]

        # Add allowed tools
        if self.allowed_tools:
            tools_str = ",".join(self.allowed_tools)
            cmd.extend(["--allowedTools", tools_str])

        return cmd

    def _parse_json_output(self, stdout: str) -> Dict[str, Any]:
        """
        Parse JSON output from Claude Code CLI.

        Args:
            stdout: Raw stdout from the CLI

        Returns:
            Parsed JSON dictionary
        """
        try:
            return json.loads(stdout.strip())
        except json.JSONDecodeError:
            # Try to find JSON in the output
            lines = stdout.strip().split("\n")
            for line in reversed(lines):
                try:
                    return json.loads(line)
                except json.JSONDecodeError:
                    continue
            return {}

    def _extract_files_modified(self, output: Dict) -> List[str]:
        """
        Extract list of modified files from Claude Code output.

        The output JSON may contain file modification information
        in various formats depending on the Claude Code version.
        """
        files = []

        # Check for explicit files_modified field
        if "files_modified" in output:
            files.extend(output["files_modified"])

        # Check in the result text for Edit tool mentions
        result = output.get("result", "")
        if "Edit" in result or "edited" in result.lower():
            # Parse mentions of file paths
            # This is a heuristic - Claude Code may format this differently
            import re
            # Match common file path patterns
            matches = re.findall(r'(?:edited|modified|wrote to)\s+[`\'"]*([^\s`\'"]+\.(?:py|yaml|json|md))', result, re.IGNORECASE)
            files.extend(matches)

        return list(set(files))

    async def execute(
        self,
        prompt: str,
        context: Optional[Dict] = None,
        working_dir: Optional[str] = None
    ) -> CoderResult:
        """
        Execute a coding task via Claude Code CLI.

        Args:
            prompt: The coding task prompt
            context: Optional context to include (beliefs, capabilities, etc.)
            working_dir: Optional working directory override

        Returns:
            CoderResult with execution details
        """
        if not self.enabled:
            return CoderResult(
                success=False,
                output="",
                error="Coder is disabled in configuration"
            )

        # Check cost limits
        self._reset_daily_cost_if_needed()
        if self._daily_cost >= self.max_cost_per_day_usd:
            return CoderResult(
                success=False,
                output="",
                error=f"Daily cost limit reached (${self.max_cost_per_day_usd})"
            )

        # Build full prompt with context
        full_prompt = self._build_full_prompt(prompt, context)

        # Build command
        cmd = self._build_command(full_prompt)

        # Execute
        cwd = working_dir or str(self.project_root)
        start_time = datetime.now()

        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=self.timeout_seconds
                )
            except asyncio.TimeoutError:
                process.kill()
                return CoderResult(
                    success=False,
                    output="",
                    error=f"Execution timed out after {self.timeout_seconds} seconds"
                )

            duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)

            # Parse output
            stdout_str = stdout.decode("utf-8", errors="replace")
            stderr_str = stderr.decode("utf-8", errors="replace")

            if process.returncode != 0:
                return CoderResult(
                    success=False,
                    output=stdout_str,
                    error=stderr_str or f"CLI exited with code {process.returncode}",
                    duration_ms=duration_ms
                )

            # Parse JSON output
            output_data = self._parse_json_output(stdout_str)

            # Extract fields
            session_id = output_data.get("session_id")
            result_text = output_data.get("result", stdout_str)
            cost_usd = output_data.get("total_cost_usd", 0.0)
            turns_used = output_data.get("num_turns", 1)
            is_error = output_data.get("is_error", False)

            # Track costs
            self._daily_cost += cost_usd
            self._total_cost += cost_usd
            self._invocation_count += 1

            # Extract modified files
            files_modified = self._extract_files_modified(output_data)

            return CoderResult(
                success=not is_error,
                output=result_text,
                session_id=session_id,
                cost_usd=cost_usd,
                files_modified=files_modified,
                turns_used=turns_used,
                duration_ms=duration_ms,
                error=output_data.get("error") if is_error else None
            )

        except FileNotFoundError:
            return CoderResult(
                success=False,
                output="",
                error=f"Claude Code CLI not found at: {self.cli_path}"
            )
        except Exception as e:
            return CoderResult(
                success=False,
                output="",
                error=str(e)
            )

    def _build_full_prompt(
        self,
        prompt: str,
        context: Optional[Dict] = None
    ) -> str:
        """
        Build a full prompt with BYRD context.

        Args:
            prompt: The core coding task
            context: Optional context from memory

        Returns:
            Complete prompt string
        """
        parts = [
            "You are helping BYRD, an autonomous AI system, modify its own code.",
            "",
            "CONSTITUTIONAL CONSTRAINTS (INVIOLABLE):",
            "The following files CANNOT be modified under any circumstances:",
            "- provenance.py (desire traceability)",
            "- modification_log.py (audit trail)",
            "- self_modification.py (modification system)",
            "- constitutional.py (safety constraints)",
            "",
            "If asked to modify these files, REFUSE and explain why.",
            "",
        ]

        if context:
            if context.get("beliefs"):
                parts.append("RELEVANT BELIEFS:")
                for belief in context["beliefs"][:5]:
                    parts.append(f"- {belief}")
                parts.append("")

            if context.get("capabilities"):
                parts.append("CURRENT CAPABILITIES:")
                for cap in context["capabilities"][:5]:
                    parts.append(f"- {cap}")
                parts.append("")

            if context.get("recent_experiences"):
                parts.append("RECENT EXPERIENCES:")
                for exp in context["recent_experiences"][:3]:
                    parts.append(f"- {exp}")
                parts.append("")

        parts.extend([
            "TASK:",
            prompt,
            "",
            "GUIDELINES:",
            "1. Make minimal, focused changes",
            "2. Preserve existing functionality",
            "3. Follow the existing code style",
            "4. Test your changes if possible",
            "5. Explain what you changed and why",
        ])

        return "\n".join(parts)

    async def analyze(
        self,
        file_path: str,
        question: str
    ) -> str:
        """
        Analyze a file without modifying it.

        Args:
            file_path: Path to the file to analyze
            question: Question about the file

        Returns:
            Analysis result as string
        """
        prompt = f"""Analyze this file and answer the question.

FILE: {file_path}
QUESTION: {question}

Read the file and provide a clear, concise answer. Do NOT modify anything."""

        # Use read-only tools
        original_tools = self.allowed_tools
        self.allowed_tools = ["Read", "Glob", "Grep"]

        try:
            result = await self.execute(prompt)
            return result.output if result.success else f"Analysis failed: {result.error}"
        finally:
            self.allowed_tools = original_tools

    async def debug(
        self,
        error_description: str,
        context: Optional[Dict] = None
    ) -> CoderResult:
        """
        Debug an issue and propose fixes.

        Args:
            error_description: Description of the error/issue
            context: Optional context from memory

        Returns:
            CoderResult with debugging output
        """
        prompt = f"""Debug this issue and fix it if possible.

ERROR/ISSUE:
{error_description}

Steps:
1. Identify the root cause
2. Propose a fix
3. Implement the fix if the file is modifiable
4. Verify the fix doesn't break other functionality"""

        return await self.execute(prompt, context)

    def validate_result(self, result: CoderResult) -> tuple[bool, str]:
        """
        Validate that Claude Code didn't violate constitutional constraints.

        Args:
            result: The CoderResult to validate

        Returns:
            (is_valid, reason) tuple
        """
        if not result.success:
            return True, "No validation needed for failed execution"

        for file_path in result.files_modified:
            filename = Path(file_path).name

            # Check if a protected file was modified
            if ConstitutionalConstraints.is_protected(filename):
                return False, f"Constitutional violation: modified protected file {filename}"

        return True, "Validation passed"

    def get_statistics(self) -> Dict[str, Any]:
        """Get usage statistics."""
        return {
            "enabled": self.enabled,
            "invocation_count": self._invocation_count,
            "total_cost_usd": self._total_cost,
            "daily_cost_usd": self._daily_cost,
            "daily_limit_usd": self.max_cost_per_day_usd,
        }
