"""
BYRD Emergent Category Discovery

Discovers categories from behavior, not prescription.

EMERGENCE PRINCIPLE:
Categories are not prescribed - they emerge from observed patterns.
This module watches BYRD's behavior and discovers natural categories
that form from clustering of similar actions, desires, and outcomes.

Key insight: Let BYRD's own vocabulary and behavior define its
categories, rather than imposing external taxonomies.

Version: 1.0
Created: December 2024
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple
from collections import Counter
import json


@dataclass
class EmergentCategory:
    """A category discovered from behavioral patterns."""
    name: str  # BYRD's own name for this category
    description: str
    exemplars: List[str]  # IDs of canonical examples
    member_count: int
    keywords: List[str]  # Common words in this category
    first_observed: datetime
    last_observed: datetime = field(default_factory=datetime.now)
    confidence: float = 0.5  # How stable is this category
    parent_category: Optional[str] = None  # For hierarchical categories


@dataclass
class CategoryAssignment:
    """Assignment of an item to a category."""
    item_id: str
    category_name: str
    confidence: float
    reasoning: str


class EmergentCategoryDiscovery:
    """
    Discovers categories from behavior, not prescription.

    EMERGENCE PRINCIPLE:
    We don't tell BYRD what categories exist. We watch its behavior
    and discover what natural clusters form.

    DISCOVERY PROCESS:
    1. Observe co-occurrence patterns in desires, actions, reflections
    2. Cluster similar items by semantic similarity
    3. Extract common keywords/themes as category labels
    4. Let categories split, merge, and evolve over time

    CRITICAL: Categories should be BYRD's own vocabulary,
    not imposed taxonomies.
    """

    def __init__(self, memory, llm_client, config: Dict = None):
        """
        Initialize category discovery.

        Args:
            memory: Memory system
            llm_client: LLM for semantic analysis
            config: Optional configuration
        """
        self.memory = memory
        self.llm_client = llm_client
        self.config = config or {}

        # Discovered categories
        self._categories: Dict[str, EmergentCategory] = {}

        # Category assignments
        self._assignments: Dict[str, str] = {}  # item_id -> category_name

        # Word co-occurrence tracking
        self._word_cooccurrence: Dict[Tuple[str, str], int] = {}

        # Statistics
        self._discovery_cycles = 0
        self._last_discovery: Optional[datetime] = None

    async def discover_from_recent(self):
        """
        Run category discovery on recent experiences.

        Analyzes recent desires, reflections, and actions to
        find emergent clusters.
        """
        self._discovery_cycles += 1
        self._last_discovery = datetime.now()

        # Get recent experiences
        experiences = await self.memory._run_query("""
            MATCH (e:Experience)
            WHERE e.timestamp > datetime() - duration('P7D')
            RETURN elementId(e) as id, e.content as content, e.type as type
            ORDER BY e.timestamp DESC
            LIMIT 100
        """)

        if not experiences:
            return

        # Get recent desires
        desires = await self.memory._run_query("""
            MATCH (d:Desire)
            WHERE d.created_at > datetime() - duration('P7D')
            RETURN elementId(d) as id, d.description as content
            ORDER BY d.created_at DESC
            LIMIT 50
        """)

        # Combine for analysis
        all_items = []
        for e in (experiences or []):
            all_items.append({
                "id": e["id"],
                "content": e.get("content", ""),
                "type": "experience"
            })

        for d in (desires or []):
            all_items.append({
                "id": d["id"],
                "content": d.get("content", ""),
                "type": "desire"
            })

        if len(all_items) < 5:
            return

        # Extract keywords and cluster
        await self._cluster_items(all_items)

    async def _cluster_items(self, items: List[Dict]):
        """Cluster items into emergent categories."""
        # Extract keywords from each item
        item_keywords: Dict[str, List[str]] = {}

        for item in items:
            content = item.get("content", "").lower()
            keywords = self._extract_keywords(content)
            item_keywords[item["id"]] = keywords

            # Track keyword co-occurrence
            for i, kw1 in enumerate(keywords):
                for kw2 in keywords[i+1:]:
                    pair = tuple(sorted([kw1, kw2]))
                    self._word_cooccurrence[pair] = self._word_cooccurrence.get(pair, 0) + 1

        # Find keyword clusters using co-occurrence
        clusters = self._find_keyword_clusters()

        # Assign items to clusters
        for item in items:
            keywords = item_keywords.get(item["id"], [])
            best_cluster = self._assign_to_cluster(keywords, clusters)

            if best_cluster:
                cluster_name, cluster_keywords = best_cluster
                self._assignments[item["id"]] = cluster_name

                # Update or create category
                if cluster_name not in self._categories:
                    self._categories[cluster_name] = EmergentCategory(
                        name=cluster_name,
                        description=f"Category discovered from: {', '.join(cluster_keywords[:5])}",
                        exemplars=[item["id"]],
                        member_count=1,
                        keywords=cluster_keywords,
                        first_observed=datetime.now()
                    )
                else:
                    cat = self._categories[cluster_name]
                    cat.member_count += 1
                    cat.last_observed = datetime.now()
                    if len(cat.exemplars) < 10:
                        cat.exemplars.append(item["id"])

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract significant keywords from text."""
        # Common stopwords to exclude
        stopwords = {
            'the', 'a', 'an', 'is', 'are', 'was', 'were', 'to', 'of', 'and',
            'or', 'in', 'on', 'at', 'for', 'with', 'by', 'from', 'as', 'be',
            'this', 'that', 'it', 'its', 'which', 'who', 'what', 'when', 'where',
            'how', 'why', 'can', 'could', 'would', 'should', 'will', 'have', 'has',
            'i', 'my', 'me', 'we', 'our', 'you', 'your', 'they', 'their'
        }

        words = text.split()
        keywords = []

        for word in words:
            # Clean and normalize
            word = ''.join(c for c in word if c.isalnum()).lower()
            if len(word) > 3 and word not in stopwords:
                keywords.append(word)

        return keywords[:20]  # Limit keywords per item

    def _find_keyword_clusters(self) -> List[Tuple[str, List[str]]]:
        """Find clusters of related keywords using co-occurrence."""
        # Find most co-occurring pairs
        sorted_pairs = sorted(
            self._word_cooccurrence.items(),
            key=lambda x: x[1],
            reverse=True
        )[:50]

        # Build clusters by connected components
        clusters: List[Set[str]] = []

        for (word1, word2), count in sorted_pairs:
            if count < 2:
                continue

            # Find existing clusters containing these words
            cluster1 = None
            cluster2 = None

            for i, cluster in enumerate(clusters):
                if word1 in cluster:
                    cluster1 = i
                if word2 in cluster:
                    cluster2 = i

            if cluster1 is None and cluster2 is None:
                # Create new cluster
                clusters.append({word1, word2})
            elif cluster1 is not None and cluster2 is None:
                # Add word2 to cluster1
                clusters[cluster1].add(word2)
            elif cluster1 is None and cluster2 is not None:
                # Add word1 to cluster2
                clusters[cluster2].add(word1)
            elif cluster1 != cluster2:
                # Merge clusters
                clusters[cluster1].update(clusters[cluster2])
                clusters.pop(cluster2)

        # Convert to named clusters
        named_clusters = []
        for cluster in clusters:
            if len(cluster) < 2:
                continue

            # Use most frequent word as cluster name
            sorted_words = sorted(cluster, key=lambda w: sum(
                self._word_cooccurrence.get(tuple(sorted([w, other])), 0)
                for other in cluster if other != w
            ), reverse=True)

            name = sorted_words[0]
            named_clusters.append((name, list(sorted_words)))

        return named_clusters

    def _assign_to_cluster(self, keywords: List[str], clusters: List[Tuple[str, List[str]]]) -> Optional[Tuple[str, List[str]]]:
        """Assign keywords to best matching cluster."""
        if not keywords or not clusters:
            return None

        keyword_set = set(keywords)
        best_match = None
        best_overlap = 0

        for name, cluster_keywords in clusters:
            cluster_set = set(cluster_keywords)
            overlap = len(keyword_set & cluster_set)

            if overlap > best_overlap:
                best_overlap = overlap
                best_match = (name, cluster_keywords)

        if best_overlap >= 2:  # Require at least 2 overlapping keywords
            return best_match

        return None

    async def suggest_name_for_category(self, category: EmergentCategory) -> str:
        """Use LLM to suggest a better name for a category."""
        prompt = f"""Based on these keywords and examples, suggest a short (1-3 word) name for this emergent category.

Keywords: {', '.join(category.keywords[:10])}

The name should:
1. Be descriptive of the category's essence
2. Be in BYRD's own vocabulary (not academic terms)
3. Be short and memorable

Suggested category name:"""

        try:
            response = await self.llm_client.generate(prompt=prompt, max_tokens=20, temperature=0.3)
            text = response.text if hasattr(response, 'text') else str(response)
            return text.strip().lower().replace(' ', '_')
        except:
            return category.name

    def get_category(self, name: str) -> Optional[EmergentCategory]:
        """Get a category by name."""
        return self._categories.get(name)

    def get_all_categories(self) -> List[EmergentCategory]:
        """Get all discovered categories."""
        return list(self._categories.values())

    def categorize(self, content: str) -> Optional[CategoryAssignment]:
        """
        Categorize new content based on discovered categories.

        Args:
            content: Text to categorize

        Returns:
            CategoryAssignment or None if no good match
        """
        if not self._categories:
            return None

        keywords = self._extract_keywords(content.lower())
        keyword_set = set(keywords)

        best_match = None
        best_score = 0

        for name, category in self._categories.items():
            cat_set = set(category.keywords)
            overlap = len(keyword_set & cat_set)
            score = overlap / max(len(keyword_set), 1)

            if score > best_score:
                best_score = score
                best_match = name

        if best_score >= 0.2 and best_match:
            return CategoryAssignment(
                item_id="",
                category_name=best_match,
                confidence=best_score,
                reasoning=f"Matched {int(best_score * 100)}% of category keywords"
            )

        return None

    async def prune_weak_categories(self, min_members: int = 3, min_confidence: float = 0.3):
        """Remove weak or unstable categories."""
        to_remove = []

        for name, category in self._categories.items():
            if category.member_count < min_members or category.confidence < min_confidence:
                to_remove.append(name)

        for name in to_remove:
            del self._categories[name]

            # Remove assignments to this category
            self._assignments = {
                k: v for k, v in self._assignments.items()
                if v != name
            }

        return len(to_remove)

    async def merge_similar_categories(self):
        """Merge categories with high keyword overlap."""
        categories = list(self._categories.keys())
        to_merge = []

        for i, cat1 in enumerate(categories):
            for cat2 in categories[i+1:]:
                set1 = set(self._categories[cat1].keywords)
                set2 = set(self._categories[cat2].keywords)

                overlap = len(set1 & set2) / min(len(set1), len(set2))

                if overlap > 0.7:  # High overlap
                    to_merge.append((cat1, cat2))

        for cat1, cat2 in to_merge:
            if cat1 in self._categories and cat2 in self._categories:
                # Merge cat2 into cat1
                c1 = self._categories[cat1]
                c2 = self._categories[cat2]

                c1.member_count += c2.member_count
                c1.keywords = list(set(c1.keywords + c2.keywords))[:20]
                c1.exemplars = (c1.exemplars + c2.exemplars)[:10]

                # Update assignments
                for k, v in self._assignments.items():
                    if v == cat2:
                        self._assignments[k] = cat1

                del self._categories[cat2]

        return len(to_merge)

    def get_statistics(self) -> Dict[str, Any]:
        """Get category discovery statistics."""
        return {
            "category_count": len(self._categories),
            "total_assignments": len(self._assignments),
            "discovery_cycles": self._discovery_cycles,
            "last_discovery": self._last_discovery.isoformat() if self._last_discovery else None,
            "categories": [
                {
                    "name": cat.name,
                    "members": cat.member_count,
                    "keywords": cat.keywords[:5]
                }
                for cat in self._categories.values()
            ]
        }

    async def persist(self):
        """Persist discovered categories to memory."""
        if not self.memory:
            return

        try:
            data = {
                "categories": {
                    name: {
                        "description": cat.description,
                        "exemplars": cat.exemplars,
                        "member_count": cat.member_count,
                        "keywords": cat.keywords,
                        "first_observed": cat.first_observed.isoformat(),
                        "last_observed": cat.last_observed.isoformat(),
                        "confidence": cat.confidence
                    }
                    for name, cat in self._categories.items()
                },
                "assignments": self._assignments,
                "discovery_cycles": self._discovery_cycles
            }

            await self.memory._run_query("""
                MERGE (n:EmergentCategories {id: 'default'})
                SET n.data = $data,
                    n.updated_at = datetime()
            """, {"data": json.dumps(data)})
        except Exception as e:
            print(f"EmergentCategories persist error: {e}")

    async def load(self):
        """Load discovered categories from memory."""
        if not self.memory:
            return

        try:
            result = await self.memory._run_query("""
                MATCH (n:EmergentCategories {id: 'default'})
                RETURN n.data as data
            """)

            if result and result[0].get("data"):
                data = json.loads(result[0]["data"])

                for name, cat_data in data.get("categories", {}).items():
                    self._categories[name] = EmergentCategory(
                        name=name,
                        description=cat_data.get("description", ""),
                        exemplars=cat_data.get("exemplars", []),
                        member_count=cat_data.get("member_count", 0),
                        keywords=cat_data.get("keywords", []),
                        first_observed=datetime.fromisoformat(cat_data.get("first_observed", datetime.now().isoformat())),
                        last_observed=datetime.fromisoformat(cat_data.get("last_observed", datetime.now().isoformat())),
                        confidence=cat_data.get("confidence", 0.5)
                    )

                self._assignments = data.get("assignments", {})
                self._discovery_cycles = data.get("discovery_cycles", 0)

        except Exception as e:
            print(f"EmergentCategories load error: {e}")
