"""
BYRD Hook Installer
Installs hook templates to ~/.claude/hooks/.
"""

from pathlib import Path
from typing import Dict, Optional, Tuple
import sys

if sys.version_info >= (3, 8):
    from typing import TYPE_CHECKING
else:
    TYPE_CHECKING = False

if TYPE_CHECKING:
    from aitmpl_client import AitmplTemplate

from .base import BaseInstaller


class HookInstaller(BaseInstaller):
    """
    Installs hook templates to ~/.claude/hooks/.

    Hooks are automation triggers (pre-commit, post-completion, etc.).
    """

    def __init__(self, config: Dict):
        super().__init__(config)
        self.hooks_dir = self._get_category_path("hook")

    async def install(
        self,
        template: "AitmplTemplate",
        custom_config: Optional[Dict] = None
    ) -> Tuple[bool, str]:
        """
        Install hook to ~/.claude/hooks/{name}.md or appropriate format.
        """
        try:
            # Ensure directory exists
            if not self._ensure_directory(self.hooks_dir):
                return False, f"Failed to create hooks directory: {self.hooks_dir}"

            # Determine file extension based on content
            extension = ".md"
            if template.content.strip().startswith("{"):
                extension = ".json"
            elif template.content.strip().startswith("#!/"):
                extension = ".sh"

            # Determine file path
            file_path = self.hooks_dir / f"{template.name}{extension}"

            # Write content
            file_path.write_text(template.content)

            # Make shell scripts executable
            if extension == ".sh":
                file_path.chmod(0o755)

            return True, f"Installed hook: {template.name} to {file_path}"

        except Exception as e:
            return False, f"Hook install error: {e}"

    async def verify(self, template: "AitmplTemplate") -> bool:
        """Verify hook file exists."""
        # Check all possible extensions
        for ext in [".md", ".json", ".sh"]:
            file_path = self.hooks_dir / f"{template.name}{ext}"
            if file_path.exists():
                return True
        return False

    def get_install_path(self, template: "AitmplTemplate") -> Path:
        """Get hook file path (default to .md)."""
        return self.hooks_dir / f"{template.name}.md"
