"""
Configuration loader with environment variable expansion.

Handles ${VAR:-default} syntax in YAML config files.
"""

import os
import re
import yaml
from pathlib import Path
from typing import Any, Dict, Union


def expand_env_vars(value: str) -> str:
    """
    Expand ${VAR:-default} patterns in a string.

    Examples:
        ${NEO4J_URI:-bolt://localhost:7687}
        ${API_KEY}  (no default, returns empty if not set)
    """
    if not isinstance(value, str):
        return value

    pattern = r'\$\{([^}:]+)(?::-([^}]*))?\}'

    def replace(match):
        var_name = match.group(1)
        default = match.group(2) if match.group(2) is not None else ''
        return os.environ.get(var_name, default)

    return re.sub(pattern, replace, value)


def expand_config(config: Any) -> Any:
    """
    Recursively expand environment variables in a config dict.

    Args:
        config: Config dict, list, or value

    Returns:
        Config with all ${VAR:-default} patterns expanded
    """
    if isinstance(config, dict):
        return {k: expand_config(v) for k, v in config.items()}
    elif isinstance(config, list):
        return [expand_config(v) for v in config]
    elif isinstance(config, str):
        return expand_env_vars(config)
    return config


def load_config(config_path: Union[str, Path] = None) -> Dict[str, Any]:
    """
    Load and expand configuration from YAML file.

    Args:
        config_path: Path to config file. Defaults to config.yaml in project root.

    Returns:
        Expanded configuration dictionary

    Raises:
        FileNotFoundError: If config file doesn't exist
    """
    if config_path is None:
        config_path = Path(__file__).parent.parent / "config.yaml"
    else:
        config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path) as f:
        config = yaml.safe_load(f)

    return expand_config(config)


def get_memory_config(config: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Get memory configuration section.

    Args:
        config: Full config dict. If None, loads from default path.

    Returns:
        Memory configuration section with proper key names
    """
    if config is None:
        config = load_config()

    return config.get("memory", {})


def get_rsi_config(config: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Get RSI configuration section.

    Args:
        config: Full config dict. If None, loads from default path.

    Returns:
        RSI configuration section
    """
    if config is None:
        config = load_config()

    return config.get("rsi", {})


def get_llm_config(config: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Get LLM configuration section.

    Args:
        config: Full config dict. If None, loads from default path.

    Returns:
        LLM configuration section
    """
    if config is None:
        config = load_config()

    return config.get("local_llm", {})
