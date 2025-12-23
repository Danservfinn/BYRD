"""
BYRD MCP Installer
Installs MCP server configurations to mcp_config.json.
"""

import json
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


class McpInstaller(BaseInstaller):
    """
    Installs MCP server templates to ~/.config/claude/mcp_config.json.

    MCP format:
    {
        "mcpServers": {
            "server_name": {
                "command": "npx",
                "args": ["-y", "package-name"]
            }
        }
    }
    """

    def __init__(self, config: Dict):
        super().__init__(config)
        self.mcp_config_path = Path(
            config.get("mcp_config_path", "~/.config/claude/mcp_config.json")
        ).expanduser()

    async def install(
        self,
        template: "AitmplTemplate",
        custom_config: Optional[Dict] = None
    ) -> Tuple[bool, str]:
        """
        Install MCP server to mcp_config.json.

        Merges the new server configuration with existing config.
        """
        try:
            # Parse template content as JSON
            server_config = json.loads(template.content)

            # Load existing config
            if self.mcp_config_path.exists():
                existing = json.loads(self.mcp_config_path.read_text())
            else:
                existing = {}

            # Ensure mcpServers key exists
            if "mcpServers" not in existing:
                existing["mcpServers"] = {}

            # Normalize server name (replace hyphens with underscores)
            server_name = template.name.replace("-", "_")

            # Apply custom config overrides
            if custom_config:
                server_config.update(custom_config)

            # Add the new server
            existing["mcpServers"][server_name] = server_config

            # Save config
            self._ensure_directory(self.mcp_config_path.parent)
            self.mcp_config_path.write_text(json.dumps(existing, indent=2))

            return True, f"Installed MCP server: {server_name}"

        except json.JSONDecodeError as e:
            return False, f"Invalid MCP template JSON: {e}"
        except Exception as e:
            return False, f"MCP install error: {e}"

    async def verify(self, template: "AitmplTemplate") -> bool:
        """Verify MCP server is in config."""
        if not self.mcp_config_path.exists():
            return False

        try:
            config = json.loads(self.mcp_config_path.read_text())
            server_name = template.name.replace("-", "_")
            return server_name in config.get("mcpServers", {})
        except Exception:
            return False

    def get_install_path(self, template: "AitmplTemplate") -> Path:
        """MCP config path."""
        return self.mcp_config_path
