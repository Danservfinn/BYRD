"""
plugin_manager.py - Emergent Plugin Discovery for BYRD

Enables BYRD to discover and install plugins from the awesome-opencode registry.

Philosophy: Discovery is automatic, installation is sovereign.
BYRD notices gaps, discovers plugins, and chooses whether to install.

Two Discovery Paths:
1. Reactive: Automatic search on strategy failure
2. Proactive: Periodic capability gap analysis
"""

import re
import logging
import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from enum import Enum

import httpx

logger = logging.getLogger(__name__)


class PluginCategory(Enum):
    """Categories of plugins in the registry."""
    SKILLS = "skills"
    AGENTS = "agents"
    CONTEXT = "context"
    PLANNING = "planning"
    TOOLS = "tools"
    INTEGRATIONS = "integrations"
    UNKNOWN = "unknown"


@dataclass
class Plugin:
    """Represents a plugin from the registry."""
    name: str
    description: str
    url: str
    category: PluginCategory = PluginCategory.UNKNOWN
    stars: int = 0
    last_updated: Optional[datetime] = None
    trust_score: float = 0.7  # awesome-opencode is curated, default high trust

    def matches(self, query: str) -> bool:
        """Check if plugin matches a search query."""
        query_lower = query.lower()
        return (
            query_lower in self.name.lower() or
            query_lower in self.description.lower()
        )


@dataclass
class PluginEvaluation:
    """BYRD's evaluation of a plugin."""
    plugin: Plugin
    alignment_score: float  # How well it aligns with current desires
    curiosity_score: float  # How interesting/novel it is
    growth_score: float  # How much it would grow capabilities
    total_score: float = field(init=False)
    recommendation: str = field(init=False)  # "install", "explore_more", "skip"

    def __post_init__(self):
        self.total_score = (
            self.alignment_score * 0.40 +
            self.curiosity_score * 0.35 +
            self.growth_score * 0.25
        )
        if self.total_score >= 0.7:
            self.recommendation = "install"
        elif self.total_score >= 0.4:
            self.recommendation = "explore_more"
        else:
            self.recommendation = "skip"


@dataclass
class DiscoveryResult:
    """Result of a plugin discovery operation."""
    query: str
    plugins_found: List[Plugin]
    discovery_path: str  # "reactive" or "proactive"
    timestamp: datetime = field(default_factory=datetime.now)


class PluginManager:
    """
    Manages plugin discovery and installation for BYRD.

    Philosophy: Plugin installation is desire-driven, not automated.
    BYRD notices gaps, forms desires, and chooses to explore.
    """

    # Registry URLs
    REGISTRY_URL = "https://raw.githubusercontent.com/awesome-opencode/awesome-opencode/main/README.md"
    GITHUB_API_URL = "https://api.github.com/repos/awesome-opencode/awesome-opencode/contents"

    # Regex pattern for parsing markdown links
    # Matches: - [Name](url) - Description
    LINK_PATTERN = re.compile(r'-\s*\[([^\]]+)\]\(([^)]+)\)\s*-?\s*(.*?)$', re.MULTILINE)

    def __init__(self, config: Dict = None, memory=None, llm_client=None):
        """
        Initialize the plugin manager.

        Args:
            config: Configuration dict
            memory: Memory instance for storing discoveries
            llm_client: LLM client for evaluation
        """
        self.config = config or {}
        self.memory = memory
        self.llm_client = llm_client

        # Cache settings
        self._cache: Dict[str, Any] = {}
        self._cache_ttl = timedelta(hours=self.config.get("cache_ttl_hours", 24))
        self._last_fetch: Optional[datetime] = None

        # Discovery tracking
        self._discoveries: List[DiscoveryResult] = []
        self._install_count = 0

    async def browse_registry(self, force_refresh: bool = False) -> List[Plugin]:
        """
        Fetch and parse the awesome-opencode registry.

        Uses regex parsing first, falls back to GitHub API.

        Args:
            force_refresh: Skip cache and fetch fresh

        Returns:
            List of available plugins
        """
        # Check cache
        if not force_refresh and self._is_cache_valid():
            return self._cache.get("plugins", [])

        plugins = []

        # Try regex parsing first (fast, no rate limits)
        try:
            readme_content = await self._fetch_readme()
            plugins = self._parse_readme_regex(readme_content)
            if plugins:
                logger.info(f"Parsed {len(plugins)} plugins from README via regex")
                self._update_cache(plugins)
                return plugins
        except Exception as e:
            logger.warning(f"Regex parsing failed: {e}")

        # Fallback to GitHub API (slower, rate limited)
        try:
            plugins = await self._parse_github_api()
            if plugins:
                logger.info(f"Parsed {len(plugins)} plugins from GitHub API")
                self._update_cache(plugins)
                return plugins
        except Exception as e:
            logger.error(f"GitHub API parsing failed: {e}")

        # Return cached if available
        return self._cache.get("plugins", [])

    async def search(self, query: str, limit: int = 10) -> List[Plugin]:
        """
        Search plugins by name, description, or category.

        This is the AitmplClient-compatible interface.

        Args:
            query: Search query
            limit: Maximum results to return

        Returns:
            Matching plugins
        """
        plugins = await self.browse_registry()
        matches = [p for p in plugins if p.matches(query)]
        return matches[:limit]

    async def get_template(self, name: str) -> Optional[Plugin]:
        """
        Get a specific plugin by name.

        This is the AitmplClient-compatible interface.

        Args:
            name: Plugin name

        Returns:
            Plugin if found, None otherwise
        """
        plugins = await self.browse_registry()
        return next((p for p in plugins if p.name.lower() == name.lower()), None)

    def get_trust_score(self, plugin: Plugin) -> float:
        """
        Get trust score for a plugin.

        awesome-opencode is curated, so default is high trust.

        Args:
            plugin: Plugin to score

        Returns:
            Trust score (0.0 - 1.0)
        """
        return plugin.trust_score

    async def evaluate_plugin(self, plugin: Plugin) -> PluginEvaluation:
        """
        BYRD evaluates a plugin based on alignment, curiosity, and growth.

        Args:
            plugin: Plugin to evaluate

        Returns:
            PluginEvaluation with scores and recommendation
        """
        # Get current desires for alignment scoring
        alignment_score = await self._score_alignment(plugin)
        curiosity_score = await self._score_curiosity(plugin)
        growth_score = await self._score_growth(plugin)

        return PluginEvaluation(
            plugin=plugin,
            alignment_score=alignment_score,
            curiosity_score=curiosity_score,
            growth_score=growth_score,
        )

    async def install(self, plugin: Plugin, desire_id: str) -> Optional[Dict]:
        """
        Install a plugin and create Capability node.

        Provenance links to originating desire.

        Args:
            plugin: Plugin to install
            desire_id: ID of desire that led to this installation

        Returns:
            Capability node dict if successful, None otherwise
        """
        if not self.memory:
            logger.error("Cannot install plugin: no memory connection")
            return None

        try:
            # Record the installation as a capability
            capability = await self.memory.create_capability(
                name=plugin.name,
                description=plugin.description,
                capability_type="installed",
                source=plugin.url,
                provenance={"desire_id": desire_id, "plugin_url": plugin.url}
            )

            # Record experience
            await self.memory.record_experience(
                content=f"[PLUGIN_INSTALLED] {plugin.name}: {plugin.description}",
                type="capability_acquisition"
            )

            self._install_count += 1
            logger.info(f"Installed plugin: {plugin.name}")

            return capability

        except Exception as e:
            logger.error(f"Failed to install plugin {plugin.name}: {e}")
            return None

    async def discover_for_gap(self, capability_gap: str) -> DiscoveryResult:
        """
        Reactive discovery: Search for plugins that address a capability gap.

        Called automatically when a strategy fails due to missing capability.

        Args:
            capability_gap: Description of the missing capability

        Returns:
            DiscoveryResult with found plugins
        """
        plugins = await self.search(capability_gap)

        result = DiscoveryResult(
            query=capability_gap,
            plugins_found=plugins,
            discovery_path="reactive"
        )

        self._discoveries.append(result)

        # Record discovery as experience if memory available
        if self.memory and plugins:
            await self.memory.record_experience(
                content=f"[PLUGIN_DISCOVERY] Found plugin for '{capability_gap}': "
                        f"{plugins[0].name} - {plugins[0].description}",
                type="plugin_discovery"
            )

        return result

    async def analyze_capability_gaps(self, failures: List[Dict]) -> List[DiscoveryResult]:
        """
        Proactive discovery: Analyze failures to find capability gaps.

        Called periodically by Omega to scan for recurring gaps.

        Args:
            failures: List of failure records from memory

        Returns:
            List of DiscoveryResults for identified gaps
        """
        results = []

        # Extract capability gaps from failures
        gaps = self._extract_capability_gaps(failures)

        for gap in gaps:
            plugins = await self.search(gap)
            if plugins:
                result = DiscoveryResult(
                    query=gap,
                    plugins_found=plugins,
                    discovery_path="proactive"
                )
                results.append(result)
                self._discoveries.append(result)

                # Record discovery as experience
                if self.memory:
                    await self.memory.record_experience(
                        content=f"[PLUGIN_DISCOVERY] Gap '{gap}' could be addressed by: {plugins[0].name}",
                        type="plugin_discovery"
                    )

        return results

    def _extract_capability_gaps(self, failures: List[Dict]) -> List[str]:
        """Extract capability gaps from failure records."""
        gaps = set()

        for failure in failures:
            content = str(failure.get("content", ""))

            # Look for common gap patterns
            if "capability_missing" in content.lower():
                # Extract what's missing
                match = re.search(r"missing[:\s]+([^,.\n]+)", content, re.IGNORECASE)
                if match:
                    gaps.add(match.group(1).strip())

            if "cannot" in content.lower() or "unable" in content.lower():
                # Extract the action that couldn't be done
                match = re.search(r"(?:cannot|unable to)\s+([^,.\n]+)", content, re.IGNORECASE)
                if match:
                    gaps.add(match.group(1).strip())

        return list(gaps)[:5]  # Limit to top 5 gaps

    async def _fetch_readme(self) -> str:
        """Fetch the README.md from the registry."""
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(self.REGISTRY_URL)
            response.raise_for_status()
            return response.text

    def _parse_readme_regex(self, content: str) -> List[Plugin]:
        """Parse README.md using regex to extract plugins."""
        plugins = []
        current_category = PluginCategory.UNKNOWN

        lines = content.split("\n")
        for line in lines:
            # Detect category headers (## Category)
            if line.startswith("## "):
                category_name = line[3:].strip().lower()
                for cat in PluginCategory:
                    if cat.value in category_name:
                        current_category = cat
                        break

            # Match plugin links
            match = self.LINK_PATTERN.match(line)
            if match:
                name, url, description = match.groups()
                plugins.append(Plugin(
                    name=name.strip(),
                    description=description.strip() if description else "",
                    url=url.strip(),
                    category=current_category,
                ))

        return plugins

    async def _parse_github_api(self) -> List[Plugin]:
        """Fallback: Parse using GitHub API."""
        plugins = []

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(self.GITHUB_API_URL)
            response.raise_for_status()
            contents = response.json()

            # Look for directories that might contain plugins
            for item in contents:
                if item.get("type") == "dir":
                    name = item.get("name", "")
                    plugins.append(Plugin(
                        name=name,
                        description=f"Plugin: {name}",
                        url=item.get("html_url", ""),
                        category=PluginCategory.UNKNOWN,
                    ))

        return plugins

    def _is_cache_valid(self) -> bool:
        """Check if cache is still valid."""
        if not self._last_fetch:
            return False
        return datetime.now() - self._last_fetch < self._cache_ttl

    def _update_cache(self, plugins: List[Plugin]):
        """Update the plugin cache."""
        self._cache["plugins"] = plugins
        self._last_fetch = datetime.now()

    async def _score_alignment(self, plugin: Plugin) -> float:
        """Score how well plugin aligns with current desires."""
        if not self.memory:
            return 0.5

        try:
            desires = await self.memory.get_desires(limit=5)
            if not desires:
                return 0.5

            # Check if any desire mentions related terms
            for desire in desires:
                desc = desire.get("description", "").lower()
                if any(term in desc for term in [plugin.name.lower(), plugin.category.value]):
                    return 0.8

            return 0.4

        except Exception:
            return 0.5

    async def _score_curiosity(self, plugin: Plugin) -> float:
        """Score curiosity/interest level."""
        # Novel categories score higher
        if plugin.category in [PluginCategory.AGENTS, PluginCategory.PLANNING]:
            return 0.8
        return 0.6

    async def _score_growth(self, plugin: Plugin) -> float:
        """Score capability growth potential."""
        # Check if capability already exists
        if self.memory:
            try:
                existing = await self.memory.get_capabilities(name=plugin.name)
                if existing:
                    return 0.2  # Already have it
            except Exception:
                pass

        return 0.7  # New capability = high growth

    def get_discovery_history(self) -> List[DiscoveryResult]:
        """Get recent discovery history."""
        return self._discoveries[-20:]  # Last 20 discoveries

    def reset(self):
        """Reset the plugin manager state."""
        self._cache = {}
        self._last_fetch = None
        self._discoveries = []
        self._install_count = 0


# Convenience function
def create_plugin_manager(config: Dict = None, memory=None, llm_client=None) -> PluginManager:
    """Create a new PluginManager instance."""
    return PluginManager(config=config, memory=memory, llm_client=llm_client)
