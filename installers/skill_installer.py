"""
BYRD Skill Installer
Installs skill templates to ~/.claude/skills/.
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


class SkillInstaller(BaseInstaller):
    """
    Installs skill templates to ~/.claude/skills/.

    Skills are reusable capabilities with progressive disclosure.
    """

    def __init__(self, config: Dict):
        super().__init__(config)
        self.skills_dir = self._get_category_path("skill")

    async def install(
        self,
        template: "AitmplTemplate",
        custom_config: Optional[Dict] = None
    ) -> Tuple[bool, str]:
        """
        Install skill to ~/.claude/skills/{name}.md.
        """
        try:
            # Ensure directory exists
            if not self._ensure_directory(self.skills_dir):
                return False, f"Failed to create skills directory: {self.skills_dir}"

            # Determine file path
            file_path = self.skills_dir / f"{template.name}.md"

            # Write content
            file_path.write_text(template.content)

            return True, f"Installed skill: {template.name} to {file_path}"

        except Exception as e:
            return False, f"Skill install error: {e}"

    async def verify(self, template: "AitmplTemplate") -> bool:
        """Verify skill file exists."""
        file_path = self.skills_dir / f"{template.name}.md"
        return file_path.exists()

    def get_install_path(self, template: "AitmplTemplate") -> Path:
        """Get skill file path."""
        return self.skills_dir / f"{template.name}.md"
