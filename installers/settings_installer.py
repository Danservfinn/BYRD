"""
BYRD Settings Installer
Merges settings templates into ~/.claude/settings.local.json.
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


class SettingsInstaller(BaseInstaller):
    """
    Merges settings templates into ~/.claude/settings.local.json.

    Settings are merged (not replaced) to preserve existing user settings.
    """

    def __init__(self, config: Dict):
        super().__init__(config)
        self.settings_path = Path(
            config.get("install_paths", {}).get("setting", "~/.claude/settings.local.json")
        ).expanduser()

    async def install(
        self,
        template: "AitmplTemplate",
        custom_config: Optional[Dict] = None
    ) -> Tuple[bool, str]:
        """
        Merge settings into settings.local.json.
        """
        try:
            # Parse template content as JSON
            new_settings = json.loads(template.content)

            # Load existing settings
            if self.settings_path.exists():
                existing = json.loads(self.settings_path.read_text())
            else:
                existing = {}

            # Deep merge settings
            merged = self._deep_merge(existing, new_settings)

            # Apply custom overrides
            if custom_config:
                merged = self._deep_merge(merged, custom_config)

            # Save settings
            self._ensure_directory(self.settings_path.parent)
            self.settings_path.write_text(json.dumps(merged, indent=2))

            return True, f"Merged settings from: {template.name}"

        except json.JSONDecodeError as e:
            return False, f"Invalid settings template JSON: {e}"
        except Exception as e:
            return False, f"Settings install error: {e}"

    def _deep_merge(self, base: Dict, override: Dict) -> Dict:
        """Deep merge two dictionaries."""
        result = base.copy()

        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value

        return result

    async def verify(self, template: "AitmplTemplate") -> bool:
        """Verify settings were merged (just check file exists)."""
        return self.settings_path.exists()

    def get_install_path(self, template: "AitmplTemplate") -> Path:
        """Settings file path."""
        return self.settings_path
