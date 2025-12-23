"""
BYRD Agent Installer
Installs agent templates to ~/.claude/agents/.
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


class AgentInstaller(BaseInstaller):
    """
    Installs agent templates to ~/.claude/agents/.

    Agent format:
    ---
    name: agent-name
    description: Agent description
    tools: [Read, Write, Edit, Bash]
    model: sonnet
    ---
    # Agent instructions in markdown...
    """

    def __init__(self, config: Dict):
        super().__init__(config)
        self.agents_dir = self._get_category_path("agent")

    async def install(
        self,
        template: "AitmplTemplate",
        custom_config: Optional[Dict] = None
    ) -> Tuple[bool, str]:
        """
        Install agent to ~/.claude/agents/{name}.md.
        """
        try:
            # Ensure directory exists
            if not self._ensure_directory(self.agents_dir):
                return False, f"Failed to create agents directory: {self.agents_dir}"

            # Determine file path
            file_path = self.agents_dir / f"{template.name}.md"

            # Write content
            file_path.write_text(template.content)

            return True, f"Installed agent: {template.name} to {file_path}"

        except Exception as e:
            return False, f"Agent install error: {e}"

    async def verify(self, template: "AitmplTemplate") -> bool:
        """Verify agent file exists."""
        file_path = self.agents_dir / f"{template.name}.md"
        return file_path.exists()

    def get_install_path(self, template: "AitmplTemplate") -> Path:
        """Get agent file path."""
        return self.agents_dir / f"{template.name}.md"
