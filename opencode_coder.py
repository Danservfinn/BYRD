"""
OpenCode Coder - Direct Z.AI API Mode

Uses Z.AI API directly for code generation.
OpenCode CLI doesn't work in headless Docker containers.
"""

import asyncio
import json
import logging
import os
import httpx
from dataclasses import dataclass, field
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
    BYRD's coding capability via direct Z.AI API.

    Uses Z.AI's GLM model directly since OpenCode CLI
    doesn't work in headless Docker containers.
    """

    ZAI_API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

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

        self._model = "glm-4-plus"  # Z.AI model
        self._api_key = os.environ.get("ZAI_API_KEY")

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

        if not self._api_key:
            logger.warning("ZAI_API_KEY not set - coder will not work")

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool):
        self._enabled = value

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
        """Execute a coding task via direct Z.AI API."""
        start_time = datetime.now()
        self._execution_count += 1

        if not desire_id:
            desire_id = datetime.now().strftime("%Y%m%d%H%M%S%f")

        if not self._enabled:
            return CoderResult(success=False, output="", error="Coder is disabled", session_id=desire_id)

        if not self._api_key:
            return CoderResult(success=False, output="", error="ZAI_API_KEY not set", session_id=desire_id)

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

        logger.info(f"[Coder] Executing via Z.AI API: {task[:100]}...")

        if self.coordinator:
            self.coordinator.coder_started(task[:50])

        try:
            # Build system prompt for coding
            system_prompt = """You are an expert programmer. Generate clean, working code.
Follow these guidelines:
- Write complete, runnable code
- Include necessary imports
- Add brief comments for complex logic
- Handle edge cases appropriately
- Follow language best practices"""

            # Call Z.AI API directly
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    self.ZAI_API_URL,
                    headers={
                        "Authorization": f"Bearer {self._api_key}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": self._model,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": task},
                        ],
                        "temperature": 0.7,
                        "max_tokens": 4096,
                    },
                )

            duration = (datetime.now() - start_time).total_seconds()

            if response.status_code != 200:
                error_text = response.text[:500]
                logger.error(f"[Coder] Z.AI API error: {response.status_code} - {error_text}")
                return CoderResult(
                    success=False, output="",
                    error=f"API error {response.status_code}: {error_text}",
                    session_id=desire_id,
                    duration_seconds=duration,
                    duration_ms=int(duration * 1000),
                )

            data = response.json()

            # Extract content from response
            content = ""
            if "choices" in data and len(data["choices"]) > 0:
                choice = data["choices"][0]
                if "message" in choice:
                    content = choice["message"].get("content", "")

            logger.info(f"[Coder] Z.AI success, {len(content)} chars in {duration:.1f}s")

            if self.memory:
                await self._record_provenance(prompt, desire_id, content)

            return CoderResult(
                success=True,
                output=content,
                session_id=desire_id,
                duration_seconds=duration,
                duration_ms=int(duration * 1000),
            )

        except httpx.TimeoutException:
            duration = (datetime.now() - start_time).total_seconds()
            return CoderResult(
                success=False, output="",
                error="Request timed out after 120 seconds",
                session_id=desire_id,
                duration_seconds=duration,
                duration_ms=int(duration * 1000),
            )
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            logger.error(f"[Coder] Error: {e}")
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
        """No-op for API mode."""
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
            "can_execute": constitutional["allowed"] and bool(self._api_key),
            "constitutional_ok": constitutional["allowed"],
            "mode": "zai-api",
            "reason": constitutional.get("reason") or ("No API key" if not self._api_key else None),
        }

    def get_stats(self) -> Dict[str, Any]:
        """Get coder statistics."""
        return {
            "execution_count": self._execution_count,
            "mode": "zai-api",
            "model": self._model,
            "api_key_set": bool(self._api_key),
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
