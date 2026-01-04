"""
Stub Coder - Disabled placeholder for removed OpenCode functionality.

The OpenCode integration has been removed as it was not functioning correctly.
This stub provides the same interface so existing code doesn't break,
but all operations are no-ops that return disabled status.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime


@dataclass
class CoderResult:
    """Result from a coder execution (always indicates disabled)."""
    success: bool = False
    output: str = "Coder is disabled"
    error: Optional[str] = None
    files_modified: List[str] = field(default_factory=list)
    files_created: List[str] = field(default_factory=list)
    duration_ms: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "output": self.output,
            "error": self.error,
            "files_modified": self.files_modified,
            "files_created": self.files_created,
            "duration_ms": self.duration_ms,
        }


class StubCoder:
    """
    Disabled coder stub that provides the same interface as OpenCodeCoder.

    All operations return immediately with disabled status.
    """

    def __init__(self, **kwargs):
        """Accept any kwargs for compatibility."""
        self.enabled = False
        self._model = "disabled"
        self._execution_count = 0
        self._modifications = []
        self.context_loader = None

    async def execute(self, prompt: str = "", context: Optional[Dict] = None, **kwargs) -> CoderResult:
        """Execute is disabled - returns immediately. Accepts any kwargs for compatibility."""
        return CoderResult(
            success=False,
            output="Coder is disabled - OpenCode integration has been removed",
            error="Coder disabled"
        )

    async def generate_code(self, prompt: str) -> str:
        """Generate code is disabled."""
        return "# Coder is disabled - OpenCode integration has been removed"

    def get_stats(self) -> Dict[str, Any]:
        """Return stats showing disabled status."""
        return {
            "enabled": False,
            "model": "disabled",
            "execution_count": 0,
            "modifications": [],
            "status": "OpenCode integration removed"
        }

    def reset(self) -> None:
        """Reset is a no-op."""
        self._execution_count = 0
        self._modifications = []


def create_stub_coder(**kwargs) -> StubCoder:
    """Factory function to create a stub coder."""
    return StubCoder(**kwargs)
