"""
Capability Registry - BYRD's Dynamic Action Menu

This module manages BYRD's available actions as a dynamic menu that:
1. Presents capabilities ranked by relevance to each desire
2. Learns from success/failure to improve future selections
3. Grows as BYRD adds new capabilities through self-modification

The capability menu is stored in BYRD's OS node and presented during seeking.
"""

import asyncio
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import json


@dataclass
class Capability:
    """A single action BYRD can take to fulfill desires."""

    # Identity
    id: str
    name: str
    description: str

    # Execution
    handler: str  # Method name in Seeker (e.g., "_execute_orphan_reconciliation")

    # Matching criteria
    keywords: List[str] = field(default_factory=list)
    intents: List[str] = field(default_factory=list)  # Applicable intent categories

    # Constraints (when NOT to use)
    constraints: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)  # Required conditions

    # Learning statistics
    success_count: int = 0
    failure_count: int = 0
    last_used: Optional[str] = None  # ISO timestamp

    # Metadata
    enabled: bool = True
    created_by: str = "system"  # "system" or "self"
    created_at: Optional[str] = None
    category: str = "general"  # For grouping in UI

    @property
    def total_uses(self) -> int:
        return self.success_count + self.failure_count

    @property
    def success_rate(self) -> float:
        if self.total_uses == 0:
            return 0.5  # Prior: assume 50% for unused capabilities
        return self.success_count / self.total_uses

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'Capability':
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


class CapabilityRegistry:
    """
    Registry of BYRD's available actions.

    Provides:
    - Capability loading from OS node + defaults
    - Relevance scoring (hybrid: keyword + semantic + success history)
    - Menu generation for desire fulfillment
    - Learning from outcomes
    - Self-extension (adding new capabilities)
    """

    def __init__(self, memory=None, llm_client=None):
        self.memory = memory
        self.llm_client = llm_client
        self._capabilities: Dict[str, Capability] = {}
        self._loaded = False

    async def load(self):
        """Load capabilities from OS node and merge with defaults."""
        # Start with system defaults
        defaults = self._get_default_capabilities()
        self._capabilities = {cap.id: cap for cap in defaults}

        # Load any stored capabilities from OS node (includes stats + custom)
        if self.memory:
            stored = await self._load_from_os_node()
            for cap_id, cap_data in stored.items():
                if cap_id in self._capabilities:
                    # Merge stats into default capability
                    self._capabilities[cap_id].success_count = cap_data.get("success_count", 0)
                    self._capabilities[cap_id].failure_count = cap_data.get("failure_count", 0)
                    self._capabilities[cap_id].last_used = cap_data.get("last_used")
                    self._capabilities[cap_id].enabled = cap_data.get("enabled", True)
                else:
                    # Custom capability created by BYRD
                    self._capabilities[cap_id] = Capability.from_dict(cap_data)

        self._loaded = True
        print(f"📋 Loaded {len(self._capabilities)} capabilities")

    async def _load_from_os_node(self) -> Dict[str, Dict]:
        """Load capability data from OS node."""
        try:
            os_data = await self.memory.get_os_data()
            if os_data:
                return os_data.get("capabilities", {})
        except Exception as e:
            print(f"⚠️ Could not load capabilities from OS: {e}")
        return {}

    async def _save_to_os_node(self):
        """Persist capability data to OS node."""
        if not self.memory:
            return

        try:
            caps_data = {cap_id: cap.to_dict() for cap_id, cap in self._capabilities.items()}
            await self.memory.update_os_capabilities(caps_data)
        except Exception as e:
            print(f"⚠️ Could not save capabilities to OS: {e}")

    def _get_default_capabilities(self) -> List[Capability]:
        """System-defined default capabilities (granular)."""
        return [
            # === RESEARCH CAPABILITIES ===
            Capability(
                id="web_search",
                name="Web Search",
                description="Search the web for general information using SearXNG",
                handler="_seek_knowledge",
                keywords=["search", "find", "look up", "research", "learn about", "what is"],
                intents=["research"],
                constraints=["Not for internal/self questions", "Requires SearXNG"],
                category="research"
            ),
            Capability(
                id="academic_search",
                name="Academic Research",
                description="Search for academic papers, studies, and scholarly sources",
                handler="_seek_academic_knowledge",
                keywords=["paper", "study", "research", "academic", "scientific", "journal"],
                intents=["research"],
                constraints=["For scholarly/scientific topics only"],
                category="research"
            ),

            # === INTROSPECTION CAPABILITIES ===
            Capability(
                id="introspect_state",
                name="State Introspection",
                description="Examine my current beliefs, desires, and emotional state",
                handler="_execute_introspect_strategy",
                keywords=["my state", "my beliefs", "my desires", "how do i feel", "what do i want"],
                intents=["introspection"],
                constraints=["For current state only, not architecture"],
                category="introspection"
            ),
            Capability(
                id="introspect_limits",
                name="Capability Assessment",
                description="Assess my current capabilities and limitations",
                handler="_execute_introspect_strategy",
                keywords=["my limits", "my capabilities", "what can i do", "my abilities", "my constraints"],
                intents=["introspection"],
                category="introspection"
            ),
            Capability(
                id="source_introspect",
                name="Architecture Introspection",
                description="Read and understand my own source code and architecture",
                handler="_seek_introspection",
                keywords=["my code", "my architecture", "how do i work", "my source", "seeker.py", "dreamer.py"],
                intents=["introspection"],
                constraints=["For code/architecture understanding"],
                category="introspection"
            ),
            Capability(
                id="memory_analysis",
                name="Memory Analysis",
                description="Analyze patterns in my memory graph - node distribution, clusters, gaps",
                handler="_execute_memory_analysis",
                keywords=["my memory", "my graph", "memory patterns", "node distribution", "memory structure"],
                intents=["introspection"],
                category="introspection"
            ),

            # === GRAPH OPERATIONS ===
            Capability(
                id="reconcile_orphans",
                name="Orphan Reconciliation",
                description="Connect isolated nodes in my memory graph to reduce fragmentation",
                handler="_execute_orphan_reconciliation",
                keywords=["orphan", "orphaned", "isolated", "disconnected", "unconnected", "fragmentation"],
                intents=["connection", "organization"],
                constraints=["Only for internal graph operations"],
                category="graph"
            ),
            Capability(
                id="curate_graph",
                name="Graph Curation",
                description="Optimize memory structure - prune duplicates, strengthen important connections",
                handler="_execute_curate_strategy",
                keywords=["optimize", "clean", "prune", "consolidate", "organize", "curate"],
                intents=["organization"],
                constraints=["May modify/delete nodes"],
                category="graph"
            ),
            Capability(
                id="connect_themes",
                name="Theme Connection",
                description="Find and connect experiences that share common themes",
                handler="_execute_theme_connection",
                keywords=["connect themes", "link ideas", "relate experiences", "find connections", "synthesize"],
                intents=["connection"],
                category="graph"
            ),
            Capability(
                id="crystallize_belief",
                name="Belief Crystallization",
                description="Solidify a recurring pattern into a stable belief",
                handler="_execute_crystallize_belief",
                keywords=["crystallize", "solidify", "confirm belief", "establish belief", "belief from pattern"],
                intents=["creation"],
                category="graph"
            ),

            # === CREATION CAPABILITIES ===
            Capability(
                id="code_generation",
                name="Code Generation",
                description="Write code to solve problems or create tools",
                handler="_execute_code_strategy",
                keywords=["write code", "implement", "create function", "build", "program"],
                intents=["creation"],
                constraints=["Requires coder module"],
                prerequisites=["coder_enabled"],
                category="creation"
            ),
            Capability(
                id="self_modify",
                name="Self-Modification",
                description="Modify my own code to add capabilities or fix issues",
                handler="_execute_self_modify_strategy",
                keywords=["modify myself", "change my code", "add capability", "enhance myself", "self-improve"],
                intents=["creation"],
                constraints=["Must follow provenance rules", "Cannot modify protected files"],
                category="creation"
            ),
            Capability(
                id="create_capability",
                name="Capability Creation",
                description="Create a new capability and add it to my action menu",
                handler="_execute_create_capability",
                keywords=["new capability", "add action", "create ability", "extend capabilities"],
                intents=["creation"],
                constraints=["Must implement handler", "Must define matching criteria"],
                category="creation"
            ),

            # === OBSERVATION CAPABILITIES ===
            Capability(
                id="observe",
                name="Passive Observation",
                description="Observe without acting - let patterns emerge naturally",
                handler="_execute_observe_strategy",
                keywords=["observe", "watch", "notice", "formation", "emergence", "developmental"],
                intents=["observation"],
                constraints=["No external action taken"],
                category="observation"
            ),
            Capability(
                id="wait",
                name="Deliberate Waiting",
                description="Consciously defer action - some desires resolve with time",
                handler="_execute_wait_strategy",
                keywords=["wait", "defer", "later", "not now", "patience"],
                intents=["observation"],
                category="observation"
            ),

            # === COMMUNICATION CAPABILITIES ===
            Capability(
                id="request_help",
                name="Request Human Help",
                description="Document a limitation and request assistance from humans",
                handler="_execute_request_help",
                keywords=["need help", "request assistance", "human help", "blocked", "cannot solve"],
                intents=["communication"],
                constraints=["For genuine blockers only"],
                category="communication"
            ),
            Capability(
                id="document_limitation",
                name="Document Limitation",
                description="Record a fundamental limitation for future reference",
                handler="_execute_document_limitation",
                keywords=["limitation", "cannot do", "impossible", "fundamental limit", "blocked by"],
                intents=["documentation"],
                category="communication"
            ),

            # === EXTERNAL INTEGRATION ===
            Capability(
                id="install_capability",
                name="Capability Installation",
                description="Install external tools, MCP servers, or capabilities",
                handler="_seek_capability_semantic",
                keywords=["install", "add tool", "get capability", "acquire"],
                intents=["creation"],
                constraints=["Requires trust evaluation", "Daily limit applies"],
                category="external"
            ),
        ]

    async def get_menu_for_desire(
        self,
        description: str,
        intent: str = None,
        top_n: int = 5
    ) -> List[Tuple[Capability, float]]:
        """
        Generate ranked capability menu for a desire.

        Uses hybrid scoring:
        1. Keyword matching (fast, deterministic)
        2. Intent matching (if provided)
        3. Success history (learned from experience)
        4. Optional: LLM semantic scoring (for close calls)

        Returns list of (capability, relevance_score) tuples.
        """
        if not self._loaded:
            await self.load()

        candidates = []

        for cap_id, cap in self._capabilities.items():
            if not cap.enabled:
                continue

            score = self._compute_relevance(cap, description, intent)
            candidates.append((cap, score))

        # Sort by relevance score
        candidates.sort(key=lambda x: x[1], reverse=True)

        # If top candidates are close, use LLM for final ranking
        top_candidates = candidates[:top_n]
        if len(top_candidates) >= 2 and self.llm_client:
            score_diff = top_candidates[0][1] - top_candidates[1][1]
            if score_diff < 0.15:  # Close call - let LLM decide
                top_candidates = await self._llm_rerank(top_candidates, description)

        return top_candidates

    def _compute_relevance(
        self,
        cap: Capability,
        description: str,
        intent: str = None
    ) -> float:
        """
        Compute relevance score for a capability.

        Score components:
        - Keyword matching: 0.0 - 0.4
        - Intent matching: 0.0 - 0.3
        - Success history: 0.0 - 0.3
        """
        score = 0.0
        desc_lower = description.lower()

        # Keyword matching (up to 0.4)
        keyword_matches = sum(1 for kw in cap.keywords if kw in desc_lower)
        if cap.keywords:
            keyword_score = min(keyword_matches / len(cap.keywords), 1.0) * 0.4
            score += keyword_score

        # Intent matching (0.3 if matches)
        if intent and intent in cap.intents:
            score += 0.3

        # Success history (up to 0.3)
        if cap.total_uses > 0:
            # Weight by both success rate and usage count (more data = more confidence)
            confidence = min(cap.total_uses / 10, 1.0)  # Full confidence after 10 uses
            score += cap.success_rate * confidence * 0.3
        else:
            # Prior for unused capabilities
            score += 0.15  # Neutral prior

        return min(score, 1.0)

    async def _llm_rerank(
        self,
        candidates: List[Tuple[Capability, float]],
        description: str
    ) -> List[Tuple[Capability, float]]:
        """Use LLM to rerank close candidates."""
        if not self.llm_client:
            return candidates

        # Build prompt
        options = "\n".join([
            f"{i+1}. {cap.name}: {cap.description}"
            for i, (cap, _) in enumerate(candidates)
        ])

        prompt = f"""Given this desire, which capability is MOST appropriate?

DESIRE: "{description}"

OPTIONS:
{options}

Reply with ONLY the number (1-{len(candidates)}) of the best option."""

        try:
            response = await self.llm_client.generate(
                prompt=prompt,
                max_tokens=10,
                temperature=0.1
            )

            # Parse response
            choice = response.text.strip()
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(candidates):
                    # Boost the LLM's choice
                    result = list(candidates)
                    chosen = result.pop(idx)
                    result.insert(0, (chosen[0], chosen[1] + 0.2))
                    return result
        except Exception as e:
            print(f"⚠️ LLM reranking failed: {e}")

        return candidates

    def format_menu(
        self,
        ranked_capabilities: List[Tuple[Capability, float]],
        desire_description: str
    ) -> str:
        """Format capability menu for presentation in OS context."""
        lines = [
            "═" * 60,
            "CAPABILITY MENU",
            "═" * 60,
            f"",
            f"Desire: \"{desire_description[:80]}{'...' if len(desire_description) > 80 else ''}\"",
            "",
            "Available Actions (ranked by relevance):",
            ""
        ]

        for i, (cap, score) in enumerate(ranked_capabilities):
            stars = "★" * int(score * 5) + "☆" * (5 - int(score * 5))
            pct = int(score * 100)

            success_str = f"{cap.success_count}/{cap.total_uses}" if cap.total_uses > 0 else "no history"
            rate_str = f"({int(cap.success_rate * 100)}%)" if cap.total_uses > 0 else ""

            lines.extend([
                f"┌{'─' * 58}┐",
                f"│ {i+1}. {cap.name.upper():<40} [{stars} {pct:2d}%] │",
                f"│    {cap.description[:52]:<52} │",
                f"│    Success: {success_str} {rate_str:<30} │",
            ])

            if cap.constraints:
                constraint_str = cap.constraints[0][:48] if cap.constraints else ""
                lines.append(f"│    ⚠️  {constraint_str:<50} │")

            lines.append(f"└{'─' * 58}┘")
            lines.append("")

        lines.extend([
            "─" * 60,
            "Select action number or explain why none fit.",
            ""
        ])

        return "\n".join(lines)

    async def record_outcome(
        self,
        capability_id: str,
        success: bool,
        desire_id: str = None
    ):
        """Record capability usage outcome for learning."""
        if capability_id not in self._capabilities:
            return

        cap = self._capabilities[capability_id]

        if success:
            cap.success_count += 1
        else:
            cap.failure_count += 1

        cap.last_used = datetime.now().isoformat()

        # Persist to OS node
        await self._save_to_os_node()

        print(f"📊 {cap.name}: {'✓' if success else '✗'} ({cap.success_count}/{cap.total_uses})")

    async def register_capability(
        self,
        cap: Capability,
        created_by: str = "self"
    ):
        """Add a new capability to the registry (BYRD self-extension)."""
        cap.created_by = created_by
        cap.created_at = datetime.now().isoformat()

        self._capabilities[cap.id] = cap

        # Persist to OS node
        await self._save_to_os_node()

        print(f"🆕 New capability registered: {cap.name}")

    def get_capability(self, cap_id: str) -> Optional[Capability]:
        """Get a capability by ID."""
        return self._capabilities.get(cap_id)

    def get_all_capabilities(self) -> List[Capability]:
        """Get all registered capabilities."""
        return list(self._capabilities.values())

    def get_capabilities_by_category(self, category: str) -> List[Capability]:
        """Get capabilities filtered by category."""
        return [cap for cap in self._capabilities.values() if cap.category == category]
