"""
OpenCode Coder - ACP Mode Only

Uses OpenCode's Agent Client Protocol (JSON-RPC over stdin/stdout).
Designed for headless operation in Docker/HuggingFace.

ACP Protocol Flow:
1. session/initialize - establish capabilities
2. session/new - create a session (get sessionId)
3. session/prompt - send prompts with sessionId
4. Read session/update notifications for responses
"""

import asyncio
import json
import logging
import os
import uuid
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


class OpenCodeCoder:
    """
    BYRD's coding capability via OpenCode ACP.

    ACP = Agent Client Protocol (JSON-RPC over stdin/stdout)
    No fallbacks - if ACP fails, the operation fails.
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

        # ACP process state
        self._process: Optional[asyncio.subprocess.Process] = None
        self._request_id = 0
        self._lock = asyncio.Lock()
        self._model = "zai/glm-4.7"

        # ACP session state
        self._initialized = False
        self._acp_session_id: Optional[str] = None

        # Execution tracking
        self._execution_count = 0
        self._enabled = self.config.get("enabled", True)

        # Protected paths (never modify)
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

    async def _start_acp(self) -> bool:
        """Start the ACP subprocess."""
        if self._process and self._process.returncode is None:
            return True

        try:
            self._process = await asyncio.create_subprocess_exec(
                "opencode", "acp",
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            logger.info("OpenCode ACP process started")
            self._initialized = False
            self._acp_session_id = None
            return True
        except FileNotFoundError:
            logger.error("OpenCode CLI not found - install with: npm install -g opencode-ai")
            return False
        except Exception as e:
            logger.error(f"Failed to start ACP: {e}")
            return False

    async def _send_request(self, method: str, params: Dict = None) -> Dict:
        """Send a JSON-RPC request and wait for response."""
        self._request_id += 1
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "id": self._request_id
        }
        if params:
            request["params"] = params

        request_line = json.dumps(request) + "\n"
        self._process.stdin.write(request_line.encode())
        await self._process.stdin.drain()

        # Read response
        response_line = await asyncio.wait_for(
            self._process.stdout.readline(),
            timeout=60.0
        )

        if not response_line:
            raise Exception("Empty response from ACP")

        return json.loads(response_line.decode())

    async def _initialize_session(self) -> bool:
        """Initialize ACP session with capabilities."""
        if self._initialized:
            return True

        try:
            # Step 1: Initialize - tell agent what we support
            init_response = await self._send_request("session/initialize", {
                "clientInfo": {
                    "name": "byrd",
                    "version": "1.0.0"
                },
                "capabilities": {
                    "prompts": {
                        "text": True
                    }
                }
            })

            if "error" in init_response:
                logger.error(f"ACP initialize failed: {init_response['error']}")
                return False

            logger.info("ACP session initialized")

            # Step 2: Create new session
            session_response = await self._send_request("session/new", {
                "model": self._model
            })

            if "error" in session_response:
                logger.error(f"ACP session/new failed: {session_response['error']}")
                return False

            result = session_response.get("result", {})
            self._acp_session_id = result.get("sessionId")

            if not self._acp_session_id:
                # Generate our own session ID if not provided
                self._acp_session_id = f"sess_{uuid.uuid4().hex[:12]}"

            logger.info(f"ACP session created: {self._acp_session_id}")
            self._initialized = True
            return True

        except Exception as e:
            logger.error(f"ACP initialization failed: {e}")
            return False

    def _check_constitutional(self, task: str) -> Dict[str, Any]:
        """Check if task violates constitutional constraints."""
        task_lower = task.lower()

        for protected in self._protected_paths:
            if protected.lower() in task_lower:
                return {
                    "allowed": False,
                    "reason": f"Cannot modify protected file: {protected}",
                }

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
        """Execute a coding task via OpenCode ACP."""
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

        logger.info(f"[Coder] Executing via ACP: {task[:100]}...")

        if self.coordinator:
            self.coordinator.coder_started(task[:50])

        try:
            if not await self._start_acp():
                return CoderResult(
                    success=False, output="",
                    error="Failed to start OpenCode ACP process",
                    session_id=desire_id,
                    duration_seconds=(datetime.now() - start_time).total_seconds(),
                )

            async with self._lock:
                # Initialize session if needed
                if not await self._initialize_session():
                    return CoderResult(
                        success=False, output="",
                        error="Failed to initialize ACP session",
                        session_id=desire_id,
                        duration_seconds=(datetime.now() - start_time).total_seconds(),
                    )

                try:
                    # Send prompt using session/prompt method
                    prompt_response = await self._send_request("session/prompt", {
                        "sessionId": self._acp_session_id,
                        "prompt": [
                            {
                                "type": "text",
                                "text": task
                            }
                        ]
                    })

                    duration = (datetime.now() - start_time).total_seconds()

                    if "error" in prompt_response:
                        error_msg = prompt_response["error"].get("message", str(prompt_response["error"]))
                        return CoderResult(
                            success=False, output="",
                            error=error_msg,
                            session_id=desire_id,
                            duration_seconds=duration,
                            duration_ms=int(duration * 1000),
                        )

                    # Extract content from response
                    result = prompt_response.get("result", {})

                    # The response might be in different formats
                    content = ""
                    if isinstance(result, str):
                        content = result
                    elif isinstance(result, dict):
                        # Try various content locations
                        content = result.get("content", "")
                        if not content:
                            content = result.get("text", "")
                        if not content:
                            # Check for message array
                            messages = result.get("messages", [])
                            if messages:
                                content = "\n".join(
                                    m.get("content", "") or m.get("text", "")
                                    for m in messages if isinstance(m, dict)
                                )

                    logger.info(f"[Coder] ACP success, {len(content)} chars in {duration:.1f}s")

                    if self.memory:
                        await self._record_provenance(prompt, desire_id, content)

                    return CoderResult(
                        success=True,
                        output=content,
                        session_id=desire_id,
                        duration_seconds=duration,
                        duration_ms=int(duration * 1000),
                    )

                except asyncio.TimeoutError:
                    duration = (datetime.now() - start_time).total_seconds()
                    return CoderResult(
                        success=False, output="",
                        error="ACP request timed out after 60 seconds",
                        session_id=desire_id,
                        duration_seconds=duration,
                        duration_ms=int(duration * 1000),
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
        """Stop the ACP subprocess."""
        if self._process:
            self._process.terminate()
            try:
                await asyncio.wait_for(self._process.wait(), timeout=5.0)
            except asyncio.TimeoutError:
                self._process.kill()
            self._process = None
            self._initialized = False
            self._acp_session_id = None
            logger.info("OpenCode ACP process stopped")

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
            "mode": "acp",
            "reason": constitutional.get("reason"),
        }

    def get_stats(self) -> Dict[str, Any]:
        """Get coder statistics."""
        return {
            "execution_count": self._execution_count,
            "mode": "acp",
            "model": self._model,
            "process_running": self._process is not None and self._process.returncode is None,
            "acp_initialized": self._initialized,
            "acp_session_id": self._acp_session_id,
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
