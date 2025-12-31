"""
OpenCode Coder - HTTP Server Mode

Uses OpenCode's REST API via `opencode serve`.
Designed for headless operation in Docker/HuggingFace.

API Endpoints:
- POST /session - Create new session
- POST /session/:id/message - Send message and await response
"""

import asyncio
import json
import logging
import os
import httpx
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
    BYRD's coding capability via OpenCode HTTP API.

    Uses `opencode serve` to run a local HTTP server,
    then makes REST API calls for code generation.
    """

    SERVER_PORT = 4097  # Different from BYRD's 7860

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

        # Server process state
        self._server_process: Optional[asyncio.subprocess.Process] = None
        self._server_ready = False
        self._model = "zai/glm-4.7"
        self._base_url = f"http://localhost:{self.SERVER_PORT}"

        # Session state
        self._current_session_id: Optional[str] = None

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

    async def _start_server(self) -> bool:
        """Start the OpenCode HTTP server."""
        if self._server_ready:
            return True

        # Check if server is already running
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                resp = await client.get(f"{self._base_url}/global/health")
                if resp.status_code == 200:
                    self._server_ready = True
                    logger.info("OpenCode server already running")
                    return True
        except Exception:
            pass

        # Start server process
        try:
            self._server_process = await asyncio.create_subprocess_exec(
                "opencode", "serve",
                "--port", str(self.SERVER_PORT),
                "--hostname", "127.0.0.1",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            logger.info(f"OpenCode server starting on port {self.SERVER_PORT}...")

            # Wait for server to be ready
            for _ in range(30):  # 30 attempts, 1 second apart
                await asyncio.sleep(1)
                try:
                    async with httpx.AsyncClient(timeout=2.0) as client:
                        resp = await client.get(f"{self._base_url}/global/health")
                        if resp.status_code == 200:
                            self._server_ready = True
                            logger.info("OpenCode server is ready")
                            return True
                except Exception:
                    pass

            logger.error("OpenCode server failed to start within 30 seconds")
            return False

        except FileNotFoundError:
            logger.error("OpenCode CLI not found - install with: npm install -g opencode-ai")
            return False
        except Exception as e:
            logger.error(f"Failed to start OpenCode server: {e}")
            return False

    async def _create_session(self) -> Optional[str]:
        """Create a new OpenCode session."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    f"{self._base_url}/session",
                    json={"model": self._model}
                )
                if resp.status_code == 200:
                    data = resp.json()
                    session_id = data.get("id") or data.get("sessionId")
                    if session_id:
                        logger.info(f"Created OpenCode session: {session_id}")
                        return session_id
                logger.error(f"Failed to create session: {resp.status_code} - {resp.text}")
        except Exception as e:
            logger.error(f"Error creating session: {e}")
        return None

    async def _send_message(self, session_id: str, content: str) -> Dict:
        """Send a message to an OpenCode session."""
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                resp = await client.post(
                    f"{self._base_url}/session/{session_id}/message",
                    json={
                        "model": self._model,
                        "parts": [
                            {"type": "text", "text": content}
                        ]
                    }
                )
                if resp.status_code == 200:
                    return {"success": True, "data": resp.json()}
                return {"success": False, "error": f"HTTP {resp.status_code}: {resp.text[:200]}"}
        except httpx.TimeoutException:
            return {"success": False, "error": "Request timed out after 120 seconds"}
        except Exception as e:
            return {"success": False, "error": str(e)}

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
        """Execute a coding task via OpenCode HTTP API."""
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

        task = prompt
        if context:
            context_str = "\n".join(f"# {k}\n{v}" for k, v in context.items() if v)
            task = f"Context:\n{context_str}\n\nTask:\n{prompt}"

        logger.info(f"[Coder] Executing via HTTP: {task[:100]}...")

        if self.coordinator:
            self.coordinator.coder_started(task[:50])

        try:
            # Start server if needed
            if not await self._start_server():
                return CoderResult(
                    success=False, output="",
                    error="Failed to start OpenCode server",
                    session_id=desire_id,
                    duration_seconds=(datetime.now() - start_time).total_seconds(),
                )

            # Create session if needed
            if not self._current_session_id:
                self._current_session_id = await self._create_session()
                if not self._current_session_id:
                    return CoderResult(
                        success=False, output="",
                        error="Failed to create OpenCode session",
                        session_id=desire_id,
                        duration_seconds=(datetime.now() - start_time).total_seconds(),
                    )

            # Send message
            result = await self._send_message(self._current_session_id, task)
            duration = (datetime.now() - start_time).total_seconds()

            if not result["success"]:
                return CoderResult(
                    success=False, output="",
                    error=result["error"],
                    session_id=desire_id,
                    duration_seconds=duration,
                    duration_ms=int(duration * 1000),
                )

            # Extract content from response
            data = result["data"]
            content = ""

            # Try to extract text from response parts
            parts = data.get("parts", [])
            if parts:
                text_parts = []
                for part in parts:
                    if isinstance(part, dict):
                        if part.get("type") == "text":
                            text_parts.append(part.get("text", ""))
                        elif "content" in part:
                            text_parts.append(part["content"])
                content = "\n".join(text_parts)

            # Fallback to other response structures
            if not content:
                if isinstance(data, str):
                    content = data
                elif "content" in data:
                    content = data["content"]
                elif "text" in data:
                    content = data["text"]
                elif "info" in data:
                    info = data["info"]
                    if isinstance(info, dict) and "content" in info:
                        content = info["content"]

            logger.info(f"[Coder] HTTP success, {len(content)} chars in {duration:.1f}s")

            if self.memory:
                await self._record_provenance(prompt, desire_id, content)

            return CoderResult(
                success=True,
                output=content,
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
        """Stop the OpenCode server."""
        if self._server_process:
            self._server_process.terminate()
            try:
                await asyncio.wait_for(self._server_process.wait(), timeout=5.0)
            except asyncio.TimeoutError:
                self._server_process.kill()
            self._server_process = None
            self._server_ready = False
            self._current_session_id = None
            logger.info("OpenCode server stopped")

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
            "mode": "http",
            "reason": constitutional.get("reason"),
        }

    def get_stats(self) -> Dict[str, Any]:
        """Get coder statistics."""
        return {
            "execution_count": self._execution_count,
            "mode": "http",
            "model": self._model,
            "server_port": self.SERVER_PORT,
            "server_ready": self._server_ready,
            "current_session_id": self._current_session_id,
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
