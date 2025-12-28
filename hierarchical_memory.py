"""
BYRD Hierarchical Memory

Memory consolidation with abstraction layers.

LAYERS:
- L0: Experience (raw observations)
- L1: Pattern (3+ similar experiences)
- L2: Principle (3+ related patterns)
- L3: Axiom (3+ connected principles)
- L4: Meta-Axiom (2+ observations about truths)

Key insight: Higher-level concepts can be retrieved without
re-querying raw experiences, reducing memory access cost.

Version: 1.0
Created: December 2024
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Set
from enum import IntEnum


class MemoryLevel(IntEnum):
    """Memory hierarchy levels."""
    EXPERIENCE = 0   # L0: Raw observations
    PATTERN = 1      # L1: Recurring observations
    PRINCIPLE = 2    # L2: Generalized patterns
    AXIOM = 3        # L3: Foundational truths
    META_AXIOM = 4   # L4: Truths about truths


@dataclass
class MemoryNode:
    """A node in the hierarchical memory system."""
    id: str
    level: MemoryLevel
    content: str
    confidence: float
    usage_count: int = 0
    abstraction_count: int = 1  # Number of lower-level items this abstracts
    created_at: datetime = field(default_factory=datetime.now)
    last_accessed: datetime = field(default_factory=datetime.now)
    source_ids: List[str] = field(default_factory=list)


@dataclass
class PromotionResult:
    """Result of a promotion operation."""
    success: bool
    new_node_id: Optional[str] = None
    new_level: Optional[MemoryLevel] = None
    reason: Optional[str] = None


class HierarchicalMemory:
    """
    Memory consolidation with abstraction layers.

    Automatically promotes recurring information to higher
    abstraction levels, reducing retrieval cost while
    preserving important knowledge.

    PROMOTION CRITERIA:
    - L0 → L1: 3+ similar experiences with shared semantics
    - L1 → L2: 3+ related patterns with common theme
    - L2 → L3: 3+ principles that form a coherent theory
    - L3 → L4: 2+ observations about how axioms relate
    """

    # Thresholds for promotion
    PROMOTION_THRESHOLDS = {
        MemoryLevel.EXPERIENCE: 3,  # Experiences -> Pattern
        MemoryLevel.PATTERN: 3,     # Patterns -> Principle
        MemoryLevel.PRINCIPLE: 3,   # Principles -> Axiom
        MemoryLevel.AXIOM: 2,       # Axioms -> Meta-Axiom
    }

    def __init__(self, memory, llm_client, config: Dict = None):
        """
        Initialize hierarchical memory.

        Args:
            memory: Base memory system (Neo4j)
            llm_client: LLM client for abstraction generation
            config: Optional configuration
        """
        self.memory = memory
        self.llm_client = llm_client
        self.config = config or {}

        # Statistics
        self._promotions_by_level: Dict[MemoryLevel, int] = {
            level: 0 for level in MemoryLevel
        }
        self._total_abstractions = 0

    async def maybe_promote(self, node_ids: List[str], source_level: MemoryLevel) -> PromotionResult:
        """
        Check if nodes are ready for promotion and promote if so.

        Args:
            node_ids: IDs of nodes to consider for promotion
            source_level: Current level of nodes

        Returns:
            PromotionResult with success status and new node ID
        """
        if source_level >= MemoryLevel.META_AXIOM:
            return PromotionResult(
                success=False,
                reason="Cannot promote beyond Meta-Axiom level"
            )

        threshold = self.PROMOTION_THRESHOLDS.get(source_level, 3)

        if len(node_ids) < threshold:
            return PromotionResult(
                success=False,
                reason=f"Need {threshold} nodes for promotion, have {len(node_ids)}"
            )

        # Check if nodes are similar enough for promotion
        similarity = await self._check_similarity(node_ids, source_level)

        if similarity < 0.7:
            return PromotionResult(
                success=False,
                reason=f"Nodes not similar enough (similarity: {similarity:.2f})"
            )

        # Generate abstraction
        abstraction = await self._generate_abstraction(node_ids, source_level)

        if not abstraction:
            return PromotionResult(
                success=False,
                reason="Failed to generate abstraction"
            )

        # Create promoted node
        target_level = MemoryLevel(source_level + 1)
        new_id = await self._create_promoted_node(abstraction, target_level, node_ids)

        if new_id:
            self._promotions_by_level[source_level] += 1
            self._total_abstractions += 1

            return PromotionResult(
                success=True,
                new_node_id=new_id,
                new_level=target_level
            )

        return PromotionResult(
            success=False,
            reason="Failed to create promoted node"
        )

    async def _check_similarity(self, node_ids: List[str], level: MemoryLevel) -> float:
        """Check semantic similarity between nodes."""
        # Get node contents
        label = self._level_to_label(level)
        result = await self.memory._run_query(f"""
            MATCH (n:{label})
            WHERE elementId(n) IN $ids
            RETURN n.content as content
        """, {"ids": node_ids})

        if not result or len(result) < 2:
            return 0.0

        # Use LLM to assess similarity
        contents = [r["content"][:200] for r in result]

        prompt = f"""Rate the semantic similarity of these {len(contents)} items on a scale of 0.0 to 1.0.

Items:
{chr(10).join(f'- {c}' for c in contents)}

Reply with ONLY a number between 0.0 and 1.0.
0.0 = completely unrelated
0.5 = somewhat related
1.0 = essentially the same concept

Similarity score:"""

        try:
            response = await self.llm_client.generate(prompt=prompt, max_tokens=10, temperature=0.1)
            text = response.text if hasattr(response, 'text') else str(response)
            score = float(text.strip())
            return max(0.0, min(1.0, score))
        except:
            return 0.5  # Assume moderate similarity on error

    async def _generate_abstraction(self, node_ids: List[str], source_level: MemoryLevel) -> Optional[str]:
        """Generate abstract content from source nodes."""
        label = self._level_to_label(source_level)
        target_label = self._level_to_label(MemoryLevel(source_level + 1))

        result = await self.memory._run_query(f"""
            MATCH (n:{label})
            WHERE elementId(n) IN $ids
            RETURN n.content as content
        """, {"ids": node_ids})

        if not result:
            return None

        contents = [r["content"] for r in result]

        level_descriptions = {
            MemoryLevel.PATTERN: "a recurring pattern",
            MemoryLevel.PRINCIPLE: "a general principle",
            MemoryLevel.AXIOM: "a foundational axiom",
            MemoryLevel.META_AXIOM: "a meta-axiom about truths"
        }

        target_level = MemoryLevel(source_level + 1)
        description = level_descriptions.get(target_level, "an abstraction")

        prompt = f"""Synthesize these {len(contents)} items into {description}.

Source items:
{chr(10).join(f'{i+1}. {c[:300]}' for i, c in enumerate(contents))}

Requirements:
1. The {target_label} should capture the common essence
2. Be concise but preserve important information
3. Make it actionable/useful for future retrieval
4. Do not include phrases like "based on the items" - state the {target_label} directly

{target_label}:"""

        try:
            response = await self.llm_client.generate(prompt=prompt, max_tokens=200, temperature=0.3)
            text = response.text if hasattr(response, 'text') else str(response)
            return text.strip()
        except Exception as e:
            print(f"Abstraction generation error: {e}")
            return None

    async def _create_promoted_node(self, content: str, level: MemoryLevel, source_ids: List[str]) -> Optional[str]:
        """Create a new node at the target level."""
        label = self._level_to_label(level)

        result = await self.memory._run_query(f"""
            CREATE (n:{label} {{
                content: $content,
                level: $level,
                confidence: 0.8,
                usage_count: 0,
                abstraction_count: $count,
                created_at: datetime(),
                source_ids: $sources
            }})
            RETURN elementId(n) as id
        """, {
            "content": content,
            "level": level.value,
            "count": len(source_ids),
            "sources": source_ids
        })

        if result:
            new_id = result[0]["id"]

            # Create PROMOTED_TO relationships
            for source_id in source_ids:
                await self.memory._run_query("""
                    MATCH (s), (t)
                    WHERE elementId(s) = $source AND elementId(t) = $target
                    CREATE (s)-[:PROMOTED_TO {timestamp: datetime()}]->(t)
                """, {"source": source_id, "target": new_id})

            return new_id

        return None

    def _level_to_label(self, level: MemoryLevel) -> str:
        """Convert memory level to Neo4j node label."""
        labels = {
            MemoryLevel.EXPERIENCE: "Experience",
            MemoryLevel.PATTERN: "Pattern",
            MemoryLevel.PRINCIPLE: "Principle",
            MemoryLevel.AXIOM: "Axiom",
            MemoryLevel.META_AXIOM: "MetaAxiom"
        }
        return labels.get(level, "Experience")

    async def retrieve_at_level(self, query: str, level: MemoryLevel, limit: int = 5) -> List[Dict]:
        """
        Retrieve memories at a specific abstraction level.

        Higher levels return more abstract/general knowledge.

        Args:
            query: Search query
            level: Target abstraction level
            limit: Maximum results

        Returns:
            List of matching memory nodes
        """
        label = self._level_to_label(level)

        # Simple keyword search (can be enhanced with embeddings)
        keywords = query.lower().split()[:5]  # Limit keywords

        result = await self.memory._run_query(f"""
            MATCH (n:{label})
            WHERE any(kw IN $keywords WHERE toLower(n.content) CONTAINS kw)
            RETURN elementId(n) as id,
                   n.content as content,
                   n.confidence as confidence,
                   n.abstraction_count as abstraction_count
            ORDER BY n.confidence DESC, n.abstraction_count DESC
            LIMIT $limit
        """, {"keywords": keywords, "limit": limit})

        # Update access time
        if result:
            for r in result:
                await self.memory._run_query("""
                    MATCH (n) WHERE elementId(n) = $id
                    SET n.last_accessed = datetime(),
                        n.usage_count = coalesce(n.usage_count, 0) + 1
                """, {"id": r["id"]})

        return list(result) if result else []

    async def smart_retrieve(self, query: str, prefer_abstract: bool = True) -> List[Dict]:
        """
        Retrieve memories using adaptive level selection.

        Starts at highest abstraction level and drills down if needed.

        Args:
            query: Search query
            prefer_abstract: If True, prefer higher-level abstractions

        Returns:
            List of relevant memories with level information
        """
        results = []

        # Start from highest level if preferring abstract
        levels = list(MemoryLevel) if prefer_abstract else list(reversed(MemoryLevel))

        for level in levels:
            level_results = await self.retrieve_at_level(query, level, limit=3)
            if level_results:
                for r in level_results:
                    r['level'] = level.name
                    r['level_value'] = level.value
                results.extend(level_results)

            if len(results) >= 5:
                break

        return results[:10]

    async def consolidation_cycle(self):
        """
        Run a consolidation cycle across all levels.

        Finds groups of similar nodes and promotes them.
        """
        print("🧠 HierarchicalMemory: Running consolidation...")

        for level in [MemoryLevel.EXPERIENCE, MemoryLevel.PATTERN, MemoryLevel.PRINCIPLE, MemoryLevel.AXIOM]:
            await self._consolidate_level(level)

        print(f"   Promotions: {dict((l.name, c) for l, c in self._promotions_by_level.items() if c > 0)}")

    async def _consolidate_level(self, level: MemoryLevel):
        """Consolidate nodes at a specific level."""
        label = self._level_to_label(level)
        threshold = self.PROMOTION_THRESHOLDS.get(level, 3)

        # Find candidate groups (nodes that share keywords/themes)
        candidates = await self.memory._run_query(f"""
            MATCH (n:{label})
            WHERE NOT exists((n)-[:PROMOTED_TO]->())
            WITH n, toLower(n.content) as content
            ORDER BY n.created_at DESC
            LIMIT 50
            RETURN elementId(n) as id, n.content as content
        """)

        if not candidates or len(candidates) < threshold:
            return

        # Simple grouping by shared words (can be enhanced with embeddings)
        groups: Dict[str, List[str]] = {}

        for c in candidates:
            content = c["content"].lower()
            # Extract key words (>5 chars, not common)
            words = set(w for w in content.split() if len(w) > 5)

            for word in list(words)[:3]:  # Use top 3 words as keys
                if word not in groups:
                    groups[word] = []
                groups[word].append(c["id"])

        # Try to promote groups that meet threshold
        for key, node_ids in groups.items():
            if len(node_ids) >= threshold:
                # Deduplicate
                unique_ids = list(set(node_ids))[:threshold + 2]

                result = await self.maybe_promote(unique_ids, level)
                if result.success:
                    print(f"   Promoted {len(unique_ids)} {label}s to {result.new_level.name}")

    def get_statistics(self) -> Dict[str, Any]:
        """Get hierarchical memory statistics."""
        return {
            "promotions_by_level": {l.name: c for l, c in self._promotions_by_level.items()},
            "total_abstractions": self._total_abstractions,
            "thresholds": {l.name: t for l, t in self.PROMOTION_THRESHOLDS.items()}
        }

    async def get_level_counts(self) -> Dict[str, int]:
        """Get count of nodes at each level."""
        counts = {}

        for level in MemoryLevel:
            label = self._level_to_label(level)
            result = await self.memory._run_query(f"""
                MATCH (n:{label})
                RETURN count(n) as count
            """)
            counts[level.name] = result[0]["count"] if result else 0

        return counts
