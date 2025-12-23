"""
BYRD Installers Package
Specialized installers for different template types from aitmpl.com.
"""

from typing import Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .base import BaseInstaller
    from aitmpl_client import AitmplTemplate


def get_installer(category: str, config: Dict) -> Optional["BaseInstaller"]:
    """
    Factory function to get the appropriate installer for a category.

    Args:
        category: Template category (agent, command, mcp, skill, hook, setting)
        config: Configuration dict with install paths

    Returns:
        Appropriate installer instance, or None if category not supported
    """
    from .mcp_installer import McpInstaller
    from .agent_installer import AgentInstaller
    from .command_installer import CommandInstaller
    from .skill_installer import SkillInstaller
    from .hook_installer import HookInstaller
    from .settings_installer import SettingsInstaller

    installers = {
        "mcp": McpInstaller,
        "agent": AgentInstaller,
        "command": CommandInstaller,
        "skill": SkillInstaller,
        "hook": HookInstaller,
        "setting": SettingsInstaller,
    }

    installer_class = installers.get(category)
    if installer_class:
        return installer_class(config)

    return None


__all__ = [
    "get_installer",
    "BaseInstaller",
    "McpInstaller",
    "AgentInstaller",
    "CommandInstaller",
    "SkillInstaller",
    "HookInstaller",
    "SettingsInstaller",
]
