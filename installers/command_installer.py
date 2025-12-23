"""
BYRD Command Installer
Installs command templates to ~/.claude/commands/.
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


class CommandInstaller(BaseInstaller):
    """
    Installs command templates to ~/.claude/commands/.

    Command format is similar to agents - markdown with YAML frontmatter.
    """

    def __init__(self, config: Dict):
        super().__init__(config)
        self.commands_dir = self._get_category_path("command")

    async def install(
        self,
        template: "AitmplTemplate",
        custom_config: Optional[Dict] = None
    ) -> Tuple[bool, str]:
        """
        Install command to ~/.claude/commands/{name}.md.
        """
        try:
            # Ensure directory exists
            if not self._ensure_directory(self.commands_dir):
                return False, f"Failed to create commands directory: {self.commands_dir}"

            # Determine file path
            file_path = self.commands_dir / f"{template.name}.md"

            # Write content
            file_path.write_text(template.content)

            return True, f"Installed command: {template.name} to {file_path}"

        except Exception as e:
            return False, f"Command install error: {e}"

    async def verify(self, template: "AitmplTemplate") -> bool:
        """Verify command file exists."""
        file_path = self.commands_dir / f"{template.name}.md"
        return file_path.exists()

    def get_install_path(self, template: "AitmplTemplate") -> Path:
        """Get command file path."""
        return self.commands_dir / f"{template.name}.md"
