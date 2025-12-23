"""
BYRD Base Installer
Abstract base class for all template installers.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Optional, Tuple
import sys

# Handle import for type checking
if sys.version_info >= (3, 8):
    from typing import TYPE_CHECKING
else:
    TYPE_CHECKING = False

if TYPE_CHECKING:
    from aitmpl_client import AitmplTemplate


class BaseInstaller(ABC):
    """
    Abstract base for template installers.

    Each installer knows how to:
    1. Validate a template
    2. Install it to the correct location
    3. Verify installation
    """

    def __init__(self, config: Dict):
        """
        Initialize the installer.

        Args:
            config: Configuration dict with install_paths and other settings
        """
        self.config = config
        self.install_paths = config.get("install_paths", {})

    @abstractmethod
    async def install(
        self,
        template: "AitmplTemplate",
        custom_config: Optional[Dict] = None
    ) -> Tuple[bool, str]:
        """
        Install a template.

        Args:
            template: Template to install
            custom_config: Optional configuration overrides

        Returns:
            (success, message_or_error)
        """
        pass

    @abstractmethod
    async def verify(self, template: "AitmplTemplate") -> bool:
        """Verify template was installed correctly."""
        pass

    @abstractmethod
    def get_install_path(self, template: "AitmplTemplate") -> Path:
        """Get the installation path for a template."""
        pass

    def _ensure_directory(self, path: Path) -> bool:
        """Ensure a directory exists, creating if necessary."""
        try:
            path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            print(f"Failed to create directory {path}: {e}")
            return False

    def _get_category_path(self, category: str) -> Path:
        """Get the installation path for a category."""
        path_str = self.install_paths.get(category, f"~/.claude/{category}s")
        return Path(path_str).expanduser()
