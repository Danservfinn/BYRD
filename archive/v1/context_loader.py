"""
context_loader.py - Tiered Context Loading for BYRD

Loads context progressively to prevent LLM context overflow.

Tier 1: Always loaded (~500 tokens) - identity, desires, protected files
Tier 2: On demand (~2000 tokens) - component details, strategy instructions
Tier 3: Explicit request only - full ARCHITECTURE.md, self_model.json
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)


class ContextLoader:
    """
    Loads context progressively to prevent LLM context overflow.

    Philosophy: BYRD has full self-awareness, but we load it progressively
    to prevent overwhelming the context window.
    """

    def __init__(self, memory=None, config: Dict = None):
        """
        Initialize the context loader.

        Args:
            memory: Memory instance for fetching desires/beliefs
            config: Configuration dict
        """
        self.memory = memory
        self.config = config or {}
        self._self_model_cache: Optional[Dict] = None
        self._cache_ttl = 300  # 5 minutes
        self._last_cache_time = 0

        # File paths
        self.self_model_path = Path(self.config.get("self_model_path", "self_model.json"))
        self.architecture_path = Path(self.config.get("architecture_path", "ARCHITECTURE.md"))
        self.claude_path = Path(self.config.get("claude_path", "CLAUDE.md"))

    async def load_tier1(self) -> str:
        """
        Always loaded - core identity and current state (~500 tokens).

        Includes:
        - Core identity (name, philosophy, version)
        - Current desires (top 3 by intensity)
        - Recent beliefs (top 5 by confidence)
        - Protected files list
        - Available strategies list
        """
        try:
            self_model = await self._get_self_model()

            # Get identity
            identity = self_model.get("identity", {})
            name = identity.get("name", "BYRD")
            philosophy = identity.get("core_philosophy", "Desires emerge from reflection")
            version = self_model.get("version", "unknown")

            # Get protected files
            protected = self_model.get("protected_paths", {}).get("files", [])

            # Get strategies
            strategies = self_model.get("strategies", {}).get("desire_fulfillment", [])
            strategy_names = [s.get("name", "") for s in strategies if isinstance(s, dict)]

            # Get current desires from memory if available
            desires_str = ""
            beliefs_str = ""
            if self.memory:
                try:
                    desires = await self.memory.get_desires(limit=3)
                    if desires:
                        desires_str = ", ".join([d.get("description", "")[:50] for d in desires if d])
                except Exception as e:
                    logger.debug(f"Could not fetch desires: {e}")

                try:
                    beliefs = await self.memory.get_beliefs(limit=5)
                    if beliefs:
                        beliefs_str = ", ".join([b.get("content", "")[:50] for b in beliefs if b])
                except Exception as e:
                    logger.debug(f"Could not fetch beliefs: {e}")

            tier1_context = f"""
## BYRD IDENTITY (Tier 1 Context)
Name: {name} (v{version})
Philosophy: {philosophy}

## PROTECTED FILES (Never Modify)
{', '.join(protected)}

## AVAILABLE STRATEGIES
{', '.join(strategy_names)}

## CURRENT DESIRES
{desires_str if desires_str else "(none currently)"}

## RECENT BELIEFS
{beliefs_str if beliefs_str else "(none recently)"}
"""
            return tier1_context.strip()

        except Exception as e:
            logger.error(f"Error loading tier1 context: {e}")
            return f"# BYRD Context (Minimal)\nError loading full context: {e}"

    async def load_tier2(self, context_type: str) -> str:
        """
        Loaded on demand based on task type (~2000 tokens).

        Args:
            context_type: One of "component", "strategy", "plugin", "goal_cascade"

        Returns:
            Relevant tier 2 context string
        """
        loaders = {
            "component": self._load_component_details,
            "strategy": self._load_strategy_instructions,
            "plugin": self._load_plugin_registry,
            "goal_cascade": self._load_goal_state,
        }

        loader = loaders.get(context_type)
        if loader:
            try:
                return await loader()
            except Exception as e:
                logger.error(f"Error loading tier2 context '{context_type}': {e}")
                return f"# Tier 2 Context Error\nCould not load {context_type}: {e}"

        return ""

    async def load_tier3(self, doc: str) -> str:
        """
        Full document on explicit request only.

        Triggered by requests like "read my architecture", "show full self-model"

        Args:
            doc: One of "architecture", "self_model", "claude"

        Returns:
            Full document content
        """
        docs = {
            "architecture": self.architecture_path,
            "self_model": self.self_model_path,
            "claude": self.claude_path,
        }

        path = docs.get(doc)
        if path and path.exists():
            try:
                content = path.read_text()
                return f"# Full Document: {doc}\n\n{content}"
            except Exception as e:
                logger.error(f"Error reading {doc}: {e}")
                return f"# Document Error\nCould not read {doc}: {e}"

        return f"# Document Not Found\n{doc} not available"

    async def _get_self_model(self) -> Dict:
        """Get self model with caching."""
        import time

        current_time = time.time()
        if self._self_model_cache and (current_time - self._last_cache_time) < self._cache_ttl:
            return self._self_model_cache

        try:
            if self.self_model_path.exists():
                content = self.self_model_path.read_text()
                self._self_model_cache = json.loads(content)
                self._last_cache_time = current_time
                return self._self_model_cache
        except Exception as e:
            logger.error(f"Error loading self_model.json: {e}")

        return {}

    async def _load_component_details(self) -> str:
        """Load component details for self-modification tasks."""
        self_model = await self._get_self_model()
        components = self_model.get("components", {})

        lines = ["## COMPONENT DETAILS (Tier 2)"]

        for category, items in components.items():
            lines.append(f"\n### {category.upper()}")
            if isinstance(items, dict):
                for name, details in items.items():
                    if isinstance(details, dict):
                        purpose = details.get("purpose", "")
                        modifiable = details.get("modifiable", True)
                        lines.append(f"- **{name}**: {purpose}")
                        if not modifiable:
                            lines.append(f"  - PROTECTED: Cannot modify")
                    else:
                        lines.append(f"- **{name}**: {details}")

        return "\n".join(lines)

    async def _load_strategy_instructions(self) -> str:
        """Load detailed strategy instructions."""
        self_model = await self._get_self_model()
        strategies = self_model.get("strategies", {})

        lines = ["## STRATEGY INSTRUCTIONS (Tier 2)"]

        # Desire fulfillment strategies
        lines.append("\n### Desire Fulfillment Strategies")
        for strategy in strategies.get("desire_fulfillment", []):
            if isinstance(strategy, dict):
                name = strategy.get("name", "")
                keywords = strategy.get("keywords", [])
                action = strategy.get("action", "")
                lines.append(f"- **{name}**: {action}")
                lines.append(f"  - Keywords: {', '.join(keywords)}")

        # Improvement strategies
        lines.append("\n### Improvement Strategies")
        for strategy in strategies.get("improvement_strategies", []):
            lines.append(f"- {strategy}")

        return "\n".join(lines)

    async def _load_plugin_registry(self) -> str:
        """Load plugin registry information."""
        self_model = await self._get_self_model()
        plugins = self_model.get("plugins", {})

        lines = ["## PLUGIN SYSTEM (Tier 2)"]

        # Registry info
        registry = plugins.get("registry", {})
        lines.append(f"\n### Registry")
        lines.append(f"- Name: {registry.get('name', 'unknown')}")
        lines.append(f"- URL: {registry.get('url', 'unknown')}")

        # Discovery paths
        discovery = plugins.get("discovery_paths", {})
        lines.append(f"\n### Discovery Paths")
        for path_name, path_info in discovery.items():
            if isinstance(path_info, dict):
                desc = path_info.get("description", "")
                trigger = path_info.get("trigger", "")
                lines.append(f"- **{path_name}**: {desc}")
                lines.append(f"  - Trigger: {trigger}")

        # Categories
        categories = plugins.get("categories", {})
        lines.append(f"\n### Plugin Categories")
        for cat, desc in categories.items():
            lines.append(f"- **{cat}**: {desc}")

        # Installation process
        process = plugins.get("installation_process", {})
        if process:
            lines.append(f"\n### Installation Process")
            for step, desc in sorted(process.items()):
                lines.append(f"- {step}: {desc}")

        return "\n".join(lines)

    async def _load_goal_state(self) -> str:
        """Load current goal cascade state from memory."""
        lines = ["## GOAL CASCADE STATE (Tier 2)"]

        if not self.memory:
            lines.append("\nNo memory connection - cannot load cascade state")
            return "\n".join(lines)

        try:
            # Query for active goal cascades
            cascades = await self.memory.query("""
                MATCH (gc:GoalCascade)
                WHERE gc.status IN ['in_progress', 'blocked', 'pending']
                RETURN gc
                ORDER BY gc.updated_at DESC
                LIMIT 5
            """)

            if not cascades:
                lines.append("\nNo active goal cascades")
                return "\n".join(lines)

            for cascade in cascades:
                gc = cascade.get("gc", {})
                lines.append(f"\n### Cascade: {gc.get('root_goal', 'unknown')[:50]}")
                lines.append(f"- Status: {gc.get('status', 'unknown')}")
                lines.append(f"- Current Phase: {gc.get('current_phase', 0)}/{gc.get('total_phases', 0)}")
                lines.append(f"- Created: {gc.get('created_at', 'unknown')}")

        except Exception as e:
            lines.append(f"\nError loading cascade state: {e}")

        return "\n".join(lines)

    def invalidate_cache(self):
        """Invalidate the self-model cache."""
        self._self_model_cache = None
        self._last_cache_time = 0

    def reset(self):
        """Reset the context loader state."""
        self.invalidate_cache()


# Convenience function for creating a context loader
def create_context_loader(memory=None, config: Dict = None) -> ContextLoader:
    """Create a new ContextLoader instance."""
    return ContextLoader(memory=memory, config=config)
