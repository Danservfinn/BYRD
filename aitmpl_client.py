"""
BYRD aitmpl.com Client
Client for accessing claude-code-templates registry from GitHub.

Provides:
- Template discovery from davila7/claude-code-templates
- Caching to avoid GitHub API rate limits
- Search and retrieval methods
"""

import asyncio
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict, field
import httpx


@dataclass
class AitmplTemplate:
    """Represents a template from claude-code-templates."""
    name: str
    category: str  # agent, command, mcp, skill, hook, setting
    description: str
    content: str  # Raw template content
    source_url: str  # GitHub raw URL
    tags: List[str] = field(default_factory=list)
    author: str = ""
    last_updated: Optional[datetime] = None

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        d = asdict(self)
        if self.last_updated:
            d["last_updated"] = self.last_updated.isoformat()
        return d

    @classmethod
    def from_dict(cls, data: Dict) -> "AitmplTemplate":
        """Create from dictionary."""
        if data.get("last_updated") and isinstance(data["last_updated"], str):
            data["last_updated"] = datetime.fromisoformat(data["last_updated"])
        return cls(**data)


@dataclass
class AitmplRegistry:
    """Cached registry of available templates."""
    templates: Dict[str, AitmplTemplate]  # Keyed by "category/name"
    last_fetched: datetime
    commit_sha: str = ""

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "templates": {k: v.to_dict() for k, v in self.templates.items()},
            "last_fetched": self.last_fetched.isoformat(),
            "commit_sha": self.commit_sha
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "AitmplRegistry":
        """Create from dictionary."""
        templates = {
            k: AitmplTemplate.from_dict(v)
            for k, v in data.get("templates", {}).items()
        }
        return cls(
            templates=templates,
            last_fetched=datetime.fromisoformat(data["last_fetched"]),
            commit_sha=data.get("commit_sha", "")
        )


class AitmplClient:
    """
    Client for accessing claude-code-templates registry.

    Uses GitHub API to fetch templates since there's no public REST API.
    Implements caching to avoid repeated fetches.
    """

    REPO_OWNER = "davila7"
    REPO_NAME = "claude-code-templates"

    # Paths in the repo where templates are stored
    TEMPLATE_PATHS = {
        "agent": ".claude/agents",
        "command": ".claude/commands",
        "mcp": "cli-tool/templates/common/.mcp.json",
        "skill": ".claude/skills",
        "hook": ".claude/hooks",
        "setting": ".claude/settings.local.json",
    }

    # Category keywords for desire matching
    CATEGORY_KEYWORDS = {
        "agent": ["agent", "assistant", "specialist", "expert", "developer"],
        "mcp": ["mcp", "integration", "database", "api", "server", "tool"],
        "command": ["command", "slash", "cli", "action"],
        "skill": ["skill", "capability", "ability"],
        "hook": ["hook", "automation", "trigger", "pre-", "post-"],
        "setting": ["setting", "config", "preference", "option"],
    }

    def __init__(self, config: Dict):
        """
        Initialize the client.

        Args:
            config: Dict with:
                - github_token: Optional GitHub PAT for higher rate limits
                - cache_dir: Where to store registry cache
                - cache_ttl_hours: Cache validity (default: 24)
        """
        self.github_token = config.get("github_token")
        self.cache_dir = Path(
            config.get("cache_dir", "~/.cache/byrd/aitmpl")
        ).expanduser()
        self.cache_ttl = timedelta(hours=config.get("cache_ttl_hours", 24))

        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / "registry.json"

        self._registry: Optional[AitmplRegistry] = None

    def _get_headers(self) -> Dict[str, str]:
        """Get HTTP headers for GitHub API requests."""
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "BYRD-Agent"
        }
        if self.github_token:
            headers["Authorization"] = f"token {self.github_token}"
        return headers

    async def fetch_registry(self, force: bool = False) -> AitmplRegistry:
        """
        Fetch the full template registry from GitHub.

        Uses cache if valid, otherwise fetches from API.

        Args:
            force: Bypass cache and fetch fresh

        Returns:
            AitmplRegistry with all available templates
        """
        # Check cache first
        if not force and self._registry and self.is_cache_valid():
            return self._registry

        # Try to load from disk cache
        if not force and self.cache_file.exists():
            try:
                cached = self._load_cache()
                if cached and self._is_registry_valid(cached):
                    self._registry = cached
                    return cached
            except Exception as e:
                print(f"🔍 Cache load error: {e}")

        # Fetch fresh from GitHub
        templates = {}

        async with httpx.AsyncClient(timeout=60.0) as client:
            # Fetch agents
            agent_templates = await self._fetch_directory_templates(
                client, "agent", self.TEMPLATE_PATHS["agent"]
            )
            templates.update(agent_templates)

            # Fetch commands
            command_templates = await self._fetch_directory_templates(
                client, "command", self.TEMPLATE_PATHS["command"]
            )
            templates.update(command_templates)

            # Fetch MCPs (single JSON file)
            mcp_templates = await self._fetch_mcp_templates(client)
            templates.update(mcp_templates)

            # Fetch skills
            skill_templates = await self._fetch_directory_templates(
                client, "skill", self.TEMPLATE_PATHS["skill"]
            )
            templates.update(skill_templates)

            # Fetch hooks
            hook_templates = await self._fetch_directory_templates(
                client, "hook", self.TEMPLATE_PATHS["hook"]
            )
            templates.update(hook_templates)

        # Create registry
        registry = AitmplRegistry(
            templates=templates,
            last_fetched=datetime.utcnow(),
            commit_sha=""
        )

        # Save to cache
        self._save_cache(registry)
        self._registry = registry

        print(f"🔍 Fetched {len(templates)} templates from aitmpl.com")
        return registry

    async def _fetch_directory_templates(
        self,
        client: httpx.AsyncClient,
        category: str,
        path: str
    ) -> Dict[str, AitmplTemplate]:
        """Fetch templates from a directory in the repo."""
        templates = {}

        try:
            # Get directory listing
            url = f"https://api.github.com/repos/{self.REPO_OWNER}/{self.REPO_NAME}/contents/{path}"
            response = await client.get(url, headers=self._get_headers())

            if response.status_code != 200:
                return templates

            files = response.json()

            for file_info in files:
                if not isinstance(file_info, dict):
                    continue

                name = file_info.get("name", "")
                if not name.endswith(".md"):
                    continue

                # Fetch file content
                download_url = file_info.get("download_url")
                if not download_url:
                    continue

                content_response = await client.get(download_url)
                if content_response.status_code != 200:
                    continue

                content = content_response.text

                # Parse template
                template = self._parse_markdown_template(
                    name=name.replace(".md", ""),
                    category=category,
                    content=content,
                    source_url=download_url
                )

                if template:
                    key = f"{category}/{template.name}"
                    templates[key] = template

        except Exception as e:
            print(f"🔍 Error fetching {category} templates: {e}")

        return templates

    async def _fetch_mcp_templates(
        self,
        client: httpx.AsyncClient
    ) -> Dict[str, AitmplTemplate]:
        """Fetch MCP templates from .mcp.json file."""
        templates = {}

        try:
            # Try multiple possible locations
            paths = [
                "cli-tool/templates/common/.mcp.json",
                ".mcp.json",
            ]

            for path in paths:
                url = f"https://raw.githubusercontent.com/{self.REPO_OWNER}/{self.REPO_NAME}/main/{path}"
                response = await client.get(url)

                if response.status_code == 200:
                    data = response.json()
                    mcp_servers = data.get("mcpServers", {})

                    for server_id, server_config in mcp_servers.items():
                        template = AitmplTemplate(
                            name=server_id,
                            category="mcp",
                            description=server_config.get("description", server_config.get("name", server_id)),
                            content=json.dumps(server_config, indent=2),
                            source_url=url,
                            tags=["mcp", "integration"],
                        )
                        templates[f"mcp/{server_id}"] = template

                    break

        except Exception as e:
            print(f"🔍 Error fetching MCP templates: {e}")

        return templates

    def _parse_markdown_template(
        self,
        name: str,
        category: str,
        content: str,
        source_url: str
    ) -> Optional[AitmplTemplate]:
        """Parse a markdown template with YAML frontmatter."""
        description = ""
        tags = []

        # Try to parse YAML frontmatter
        frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)

            # Extract description
            desc_match = re.search(r'description:\s*["\']?([^"\'\n]+)["\']?', frontmatter)
            if desc_match:
                description = desc_match.group(1).strip()

            # Extract name if present
            name_match = re.search(r'name:\s*["\']?([^"\'\n]+)["\']?', frontmatter)
            if name_match:
                name = name_match.group(1).strip()

            # Extract tags/tools as tags
            tools_match = re.search(r'tools:\s*\[(.*?)\]', frontmatter)
            if tools_match:
                tags = [t.strip().strip('"\'') for t in tools_match.group(1).split(',')]

        # If no description from frontmatter, use first paragraph
        if not description:
            body = content.split('---')[-1].strip() if '---' in content else content
            first_para = body.split('\n\n')[0].strip()
            description = first_para[:200] if first_para else name

        return AitmplTemplate(
            name=name,
            category=category,
            description=description,
            content=content,
            source_url=source_url,
            tags=tags,
        )

    async def search(
        self,
        query: str,
        categories: Optional[List[str]] = None,
        limit: int = 10
    ) -> List[AitmplTemplate]:
        """
        Search templates by query and optional category filter.

        Uses fuzzy matching on name, description, and tags.

        Args:
            query: Search query
            categories: Optional category filter
            limit: Max results

        Returns:
            List of matching templates, sorted by relevance
        """
        registry = await self.fetch_registry()

        query_lower = query.lower()
        query_words = set(query_lower.split())

        results = []

        for key, template in registry.templates.items():
            # Category filter
            if categories and template.category not in categories:
                continue

            # Calculate relevance score
            score = 0

            # Name match
            if query_lower in template.name.lower():
                score += 10

            # Description match
            if query_lower in template.description.lower():
                score += 5

            # Word matches
            template_text = f"{template.name} {template.description} {' '.join(template.tags)}".lower()
            for word in query_words:
                if word in template_text:
                    score += 2

            # Tag matches
            for tag in template.tags:
                if query_lower in tag.lower():
                    score += 3

            if score > 0:
                results.append((score, template))

        # Sort by score descending
        results.sort(key=lambda x: x[0], reverse=True)

        return [t for _, t in results[:limit]]

    async def get_template(
        self,
        category: str,
        name: str
    ) -> Optional[AitmplTemplate]:
        """
        Get a specific template by category and name.

        Args:
            category: Template category
            name: Template name

        Returns:
            Template if found, None otherwise
        """
        registry = await self.fetch_registry()
        key = f"{category}/{name}"
        return registry.templates.get(key)

    def infer_categories(self, desire_description: str) -> List[str]:
        """
        Infer which categories to search based on desire description.

        Args:
            desire_description: The desire description

        Returns:
            List of category names to search
        """
        description_lower = desire_description.lower()
        matched_categories = []

        for category, keywords in self.CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in description_lower:
                    if category not in matched_categories:
                        matched_categories.append(category)
                    break

        # Default to all categories if no match
        if not matched_categories:
            matched_categories = list(self.CATEGORY_KEYWORDS.keys())

        return matched_categories

    def is_cache_valid(self) -> bool:
        """Check if in-memory registry cache is still valid."""
        if not self._registry:
            return False
        return datetime.utcnow() - self._registry.last_fetched < self.cache_ttl

    def _is_registry_valid(self, registry: AitmplRegistry) -> bool:
        """Check if a registry is still valid."""
        return datetime.utcnow() - registry.last_fetched < self.cache_ttl

    def _load_cache(self) -> Optional[AitmplRegistry]:
        """Load registry from disk cache."""
        if not self.cache_file.exists():
            return None

        data = json.loads(self.cache_file.read_text())
        return AitmplRegistry.from_dict(data)

    def _save_cache(self, registry: AitmplRegistry):
        """Save registry to disk cache."""
        self.cache_file.write_text(json.dumps(registry.to_dict(), indent=2))

    async def refresh_cache(self) -> AitmplRegistry:
        """Force refresh the cache."""
        return await self.fetch_registry(force=True)

    def get_statistics(self) -> Dict:
        """Get client statistics."""
        if not self._registry:
            return {
                "cached": False,
                "template_count": 0,
                "categories": {},
            }

        categories = {}
        for template in self._registry.templates.values():
            cat = template.category
            categories[cat] = categories.get(cat, 0) + 1

        return {
            "cached": True,
            "cache_valid": self.is_cache_valid(),
            "last_fetched": self._registry.last_fetched.isoformat(),
            "template_count": len(self._registry.templates),
            "categories": categories,
        }
