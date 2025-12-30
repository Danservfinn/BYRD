# ZEUS Plugin System
# Discovers and installs plugins from awesome-opencode registry

from .registry import AwesomeOpenCodeRegistry
from .evaluator import PluginEvaluator
from .installer import PluginInstaller

__all__ = [
    "AwesomeOpenCodeRegistry",
    "PluginEvaluator",
    "PluginInstaller",
]
