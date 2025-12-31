"""
OpenCode Coder - Non-Interactive CLI Mode

Uses OpenCode's run command: `opencode run --model <model> --format json "prompt"`
Designed for headless operation in Docker/HuggingFace.

Key flags:
- run         : Non-interactive execution
- --model     : Specify model (e.g., zai/glm-4.7)
- --format    : Output format (json for structured output)
- [message..] : The prompt/task as positional argument
"""

import asyncio
import json
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime

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
    cost_usd: float = 0.0
    session_id: Optional[str] = None
    turns_used: int = 0
    duration_ms: int = 0

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
        }


class OpenCodeCoder:
    """
    BYRD's coding capability via OpenCode CLI.

    Uses non-interactive mode: opencode -p "prompt" -f json -q -m model
    No server required - direct CLI invocation per request.
    """

    def __init__(
        self,
        config: Dict = None,
        coordinator=None,
        context_loader=None,
        memory=None,
    ):
        self.config = config or {}
        self.coordinator = coordinator
        self.context_loader = context_loader
        self.memory = memory

        self._model = "zai/glm-4.7"

        # Execution tracking
        self._execution_count = 0
        self._enabled = self.config.get("enabled", True)

        # Protected paths
        self._protected_paths = self.config.get("protected_paths", [
            "provenance.py",
            "modification_log.py",
            "self_modification.py",
            "constitutional.py",
            "safety_monitor.py",
        ])

        # Ensure OpenCode auth is configured
        self._ensure_opencode_auth()

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool):
        self._enabled = value

    def _ensure_opencode_auth(self):
        """Ensure OpenCode has auth configured for Z.AI."""
        zai_key = os.environ.get("ZAI_API_KEY")
        if not zai_key:
            logger.warning("ZAI_API_KEY not set - OpenCode may not authenticate")
            return

        auth_dir = Path.home() / ".local" / "share" / "opencode"
        auth_file = auth_dir / "auth.json"

        try:
            auth_dir.mkdir(parents=True, exist_ok=True)
            auth_data = {"zai": {"type": "api", "key": zai_key}}
            auth_file.write_text(json.dumps(auth_data))
            logger.info(f"OpenCode auth configured at {auth_file}")
        except Exception as e:
            logger.error(f"Failed to configure OpenCode auth: {e}")

    def _check_constitutional(self, task: str) -> Dict[str, Any]:
        """Check if task violates constitutional constraints."""
        task_lower = task.lower()

        for protected in self._protected_paths:
            if protected.lower() in task_lower:
                return {"allowed": False, "reason": f"Cannot modify protected file: {protected}"}

        dangerous_patterns = ["rm -rf", "format c:", "del /s", "drop database", "sudo rm"]
        for pattern in dangerous_patterns:
            if pattern in task_lower:
                return {"allowed": False, "reason": f"Dangerous pattern detected: {pattern}"}

        return {"allowed": True, "reason": None}

    async def execute(
        self,
        prompt: str,
        context: Optional[Dict] = None,
        working_dir: Optional[str] = None,
        desire_id: str = None,
    ) -> CoderResult:
        """Execute a coding task via OpenCode CLI non-interactive mode."""
        start_time = datetime.now()
        self._execution_count += 1

        if not desire_id:
            desire_id = datetime.now().strftime("%Y%m%d%H%M%S%f")

        if not self._enabled:
            return CoderResult(success=False, output="", error="Coder is disabled", session_id=desire_id)

        constraint_check = self._check_constitutional(prompt)
        if not constraint_check["allowed"]:
            return CoderResult(
                success=False, output="",
                error=f"Constitutional constraint violation: {constraint_check['reason']}",
                session_id=desire_id,
            )

        # Build task with context
        task = prompt
        if context:
            context_str = "\n".join(f"# {k}\n{v}" for k, v in context.items() if v)
            task = f"Context:\n{context_str}\n\nTask:\n{prompt}"

        logger.info(f"[Coder] Executing via CLI: {task[:100]}...")

        if self.coordinator:
            self.coordinator.coder_started(task[:50])

        try:
            # Build CLI command
            # opencode run --model <model> --format json "prompt"
            cmd = [
                "opencode",
                "run",
                "--model", self._model,
                "--format", "json",
                task,
            ]

            # Set environment for headless operation
            env = os.environ.copy()
            env["TERM"] = "dumb"
            env["CI"] = "true"  # Common flag to disable interactive prompts
            env["NO_COLOR"] = "1"  # Disable color output

            logger.info(f"[Coder] Running: opencode run --model {self._model} --format json '...'")

            # Run with timeout
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=working_dir,
                env=env,
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=120.0  # 2 minute timeout
                )
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                duration = (datetime.now() - start_time).total_seconds()
                return CoderResult(
                    success=False, output="",
                    error="Request timed out after 120 seconds",
                    session_id=desire_id,
                    duration_seconds=duration,
                    duration_ms=int(duration * 1000),
                )

            duration = (datetime.now() - start_time).total_seconds()

            stdout_text = stdout.decode() if stdout else ""
            stderr_text = stderr.decode() if stderr else ""

            # Check for errors
            if process.returncode != 0:
                # Combine stdout and stderr for debugging
                error_parts = []
                if stderr_text:
                    error_parts.append(f"STDERR: {stderr_text[:400]}")
                if stdout_text:
                    error_parts.append(f"STDOUT: {stdout_text[:400]}")
                if not error_parts:
                    error_parts.append(f"Exit code {process.returncode}")
                error_msg = " | ".join(error_parts)

                logger.error(f"[Coder] CLI failed: {error_msg[:200]}")

                return CoderResult(
                    success=False, output="",
                    error=error_msg,
                    session_id=desire_id,
                    duration_seconds=duration,
                    duration_ms=int(duration * 1000),
                )

            # Parse JSON output
            content = ""
            try:
                # Output should be JSON with the response
                data = json.loads(stdout_text)

                # Extract content from response structure
                if isinstance(data, dict):
                    # Try various response structures
                    if "content" in data:
                        content = data["content"]
                    elif "text" in data:
                        content = data["text"]
                    elif "response" in data:
                        content = data["response"]
                    elif "parts" in data:
                        # Extract text from parts
                        parts = data["parts"]
                        text_parts = []
                        for part in parts:
                            if isinstance(part, dict) and part.get("type") == "text":
                                text_parts.append(part.get("text", ""))
                            elif isinstance(part, str):
                                text_parts.append(part)
                        content = "\n".join(text_parts)
                    else:
                        # Just use the whole thing
                        content = json.dumps(data)
                elif isinstance(data, str):
                    content = data

            except json.JSONDecodeError:
                # Not JSON - use raw stdout
                content = stdout_text

            # If content is empty, check if there's useful stderr info
            if not content.strip() and stderr_text:
                # Filter out INFO logs, keep actual content
                lines = stderr_text.split('\n')
                content_lines = [l for l in lines if not l.startswith('INFO ')]
                content = '\n'.join(content_lines)

            logger.info(f"[Coder] CLI success, {len(content)} chars in {duration:.1f}s")

            if self.memory:
                await self._record_provenance(prompt, desire_id, content)

            return CoderResult(
                success=True,
                output=content,
                session_id=desire_id,
                duration_seconds=duration,
                duration_ms=int(duration * 1000),
            )

        except FileNotFoundError:
            duration = (datetime.now() - start_time).total_seconds()
            return CoderResult(
                success=False, output="",
                error="OpenCode CLI not found - install with: npm install -g opencode-ai",
                session_id=desire_id,
                duration_seconds=duration,
            )
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            return CoderResult(
                success=False, output="",
                error=str(e),
                session_id=desire_id,
                duration_seconds=duration,
                duration_ms=int(duration * 1000),
            )
        finally:
            if self.coordinator:
                self.coordinator.coder_finished()

    async def _record_provenance(self, task: str, desire_id: str, output: str):
        """Record modification provenance to memory."""
        if not self.memory:
            return
        try:
            content = (
                f"[CODE_GENERATION] Task: {task[:100]}\n"
                f"Output length: {len(output)} chars\n"
                f"Desire ID: {desire_id}"
            )
            await self.memory.record_experience(content=content, type="code_generation")
        except Exception as e:
            logger.error(f"Error recording provenance: {e}")

    async def stop(self):
        """No-op for CLI mode - no persistent server to stop."""
        pass

    async def generate_code(self, prompt: str) -> str:
        """Generate code from a prompt."""
        result = await self.execute(prompt)
        return result.output if result.success else ""

    async def execute_turn(
        self,
        prompt: str,
        context: Optional[Dict] = None,
        turn_number: int = 1,
        session_id: str = None,
        working_dir: Optional[str] = None,
    ) -> CoderResult:
        """Execute a single turn within an interactive session."""
        result = await self.execute(
            prompt=prompt,
            context=context,
            working_dir=working_dir,
            desire_id=session_id,
        )
        result.turns_used = turn_number
        result.session_id = session_id
        return result

    async def can_execute(self, task: str) -> Dict[str, Any]:
        """Check if a task can be executed."""
        constitutional = self._check_constitutional(task)
        return {
            "can_execute": constitutional["allowed"],
            "constitutional_ok": constitutional["allowed"],
            "mode": "cli",
            "reason": constitutional.get("reason"),
        }

    def get_stats(self) -> Dict[str, Any]:
        """Get coder statistics."""
        return {
            "execution_count": self._execution_count,
            "mode": "cli",
            "model": self._model,
            "protected_paths": self._protected_paths,
        }

    def reset(self):
        """Reset coder state."""
        self._execution_count = 0


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
