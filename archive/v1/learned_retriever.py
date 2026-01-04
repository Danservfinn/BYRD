"""
BYRD Learned Retriever

Learns relevance from feedback.

Key insight: Initial retrieval is based on surface similarity,
but over time the system learns what's actually relevant for
different types of queries through feedback.

Integrates with Memory Reasoner to provide learned relevance scoring.

Version: 1.0
Created: December 2024
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import json


@dataclass
class RetrievalResult:
    """Result of a retrieval operation."""
    node_id: str
    content: str
    base_score: float  # Score from basic retrieval
    learned_boost: float  # Learned relevance boost
    final_score: float  # Combined score
    node_type: str = "Experience"


@dataclass
class RetrievalFeedback:
    """Feedback on a retrieval result."""
    query: str
    node_id: str
    was_helpful: bool
    timestamp: datetime = field(default_factory=datetime.now)


class LearnedRetriever:
    """
    Learns relevance from feedback.

    Augments base retrieval with learned relevance adjustments.

    TRAINING SIGNAL:
    - Memory Reasoner provides feedback: "This memory was helpful"
    - Query-result pairs with helpfulness labels
    - Learns which types of content are useful for which queries

    LEARNING APPROACH:
    - Query type classification (what kind of question is this?)
    - Result type scoring (what kinds of results help this query type?)
    - Recency decay (recent feedback matters more)
    """

    def __init__(self, memory, config: Dict = None):
        """
        Initialize the learned retriever.

        Args:
            memory: Memory system for queries
            config: Optional configuration
        """
        self.memory = memory
        self.config = config or {}

        # Learned relevance adjustments
        # Maps (query_type, result_type) -> adjustment factor
        self._relevance_adjustments: Dict[Tuple[str, str], float] = {}

        # Feedback history
        self._feedback_buffer: List[RetrievalFeedback] = []
        self._max_feedback = 1000

        # Query type patterns
        self._query_patterns = {
            "how": "procedural",
            "why": "explanatory",
            "what": "definitional",
            "when": "temporal",
            "where": "locational",
            "who": "entity",
            "can": "capability",
            "should": "normative",
            "is": "factual",
            "does": "factual"
        }

        # Statistics
        self._total_retrievals = 0
        self._helpful_retrievals = 0

    def _classify_query(self, query: str) -> str:
        """Classify query into a type."""
        query_lower = query.lower().strip()

        for keyword, qtype in self._query_patterns.items():
            if query_lower.startswith(keyword):
                return qtype

        # Check for key phrases
        if "how to" in query_lower:
            return "procedural"
        elif "remember" in query_lower or "recall" in query_lower:
            return "recall"
        elif "example" in query_lower:
            return "example"
        elif "similar" in query_lower:
            return "similarity"

        return "general"

    def _classify_result(self, result: Dict) -> str:
        """Classify result node type."""
        node_type = result.get("type", result.get("node_type", "unknown"))

        # Map to broader categories
        type_mapping = {
            "Experience": "experience",
            "Reflection": "reflection",
            "Belief": "belief",
            "Desire": "desire",
            "Pattern": "pattern",
            "Principle": "principle",
            "research": "research",
            "observation": "observation",
            "action_outcome": "action",
            "system": "system"
        }

        return type_mapping.get(node_type, "other")

    def get_learned_boost(self, query_type: str, result_type: str) -> float:
        """Get learned relevance boost for query-result type pair."""
        key = (query_type, result_type)
        return self._relevance_adjustments.get(key, 1.0)

    async def retrieve(self, query: str, limit: int = 10) -> List[RetrievalResult]:
        """
        Retrieve relevant memories with learned boosting.

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            List of RetrievalResults with learned relevance applied
        """
        query_type = self._classify_query(query)

        # Base retrieval from memory
        keywords = query.lower().split()[:5]

        base_results = await self.memory._run_query("""
            MATCH (n)
            WHERE (n:Experience OR n:Reflection OR n:Belief OR n:Pattern)
            AND any(kw IN $keywords WHERE toLower(n.content) CONTAINS kw)
            WITH n, size([kw IN $keywords WHERE toLower(n.content) CONTAINS kw]) as matches
            RETURN elementId(n) as id,
                   n.content as content,
                   labels(n)[0] as node_type,
                   coalesce(n.type, 'unknown') as type,
                   toFloat(matches) / size($keywords) as base_score
            ORDER BY base_score DESC
            LIMIT $limit
        """, {"keywords": keywords, "limit": limit * 2})  # Get extra for reranking

        if not base_results:
            return []

        # Apply learned boosts
        results = []
        for r in base_results:
            result_type = self._classify_result(r)
            base_score = r.get("base_score", 0.5)
            learned_boost = self.get_learned_boost(query_type, result_type)
            final_score = base_score * learned_boost

            results.append(RetrievalResult(
                node_id=r["id"],
                content=r["content"],
                base_score=base_score,
                learned_boost=learned_boost,
                final_score=final_score,
                node_type=r.get("node_type", "unknown")
            ))

        # Sort by final score and limit
        results.sort(key=lambda r: r.final_score, reverse=True)
        self._total_retrievals += 1

        return results[:limit]

    async def record_feedback(self, query: str, node_id: str, was_helpful: bool):
        """
        Record feedback on a retrieval result.

        Args:
            query: Original query
            node_id: ID of the retrieved node
            was_helpful: Whether the result was helpful
        """
        feedback = RetrievalFeedback(
            query=query,
            node_id=node_id,
            was_helpful=was_helpful
        )

        self._feedback_buffer.append(feedback)

        if was_helpful:
            self._helpful_retrievals += 1

        # Trim buffer
        if len(self._feedback_buffer) > self._max_feedback:
            self._feedback_buffer = self._feedback_buffer[-self._max_feedback:]

        # Update learned adjustments
        await self._update_adjustments(feedback)

    async def _update_adjustments(self, feedback: RetrievalFeedback):
        """Update relevance adjustments based on feedback."""
        query_type = self._classify_query(feedback.query)

        # Get result type
        result = await self.memory._run_query("""
            MATCH (n) WHERE elementId(n) = $id
            RETURN labels(n)[0] as node_type, coalesce(n.type, 'unknown') as type
        """, {"id": feedback.node_id})

        if not result:
            return

        result_type = self._classify_result(result[0])
        key = (query_type, result_type)

        current = self._relevance_adjustments.get(key, 1.0)

        # Exponential moving average update
        alpha = 0.1  # Learning rate
        target = 1.2 if feedback.was_helpful else 0.8

        new_value = (1 - alpha) * current + alpha * target
        # Clamp to reasonable range
        new_value = max(0.5, min(2.0, new_value))

        self._relevance_adjustments[key] = new_value

    async def reinforce_from_usage(self, source_id: str, retrieved_id: str, was_helpful: bool):
        """
        API for Memory Reasoner to provide feedback.

        Called when a retrieved memory is used and we know if it helped.

        Args:
            source_id: ID of the query context (not used currently)
            retrieved_id: ID of the retrieved node
            was_helpful: Whether it was helpful
        """
        # We don't have the original query, so use a generic one
        await self.record_feedback("memory query", retrieved_id, was_helpful)

    def get_adjustments_summary(self) -> Dict[str, Dict[str, float]]:
        """Get summary of learned adjustments."""
        summary: Dict[str, Dict[str, float]] = {}

        for (query_type, result_type), adjustment in self._relevance_adjustments.items():
            if query_type not in summary:
                summary[query_type] = {}
            summary[query_type][result_type] = adjustment

        return summary

    def get_statistics(self) -> Dict[str, Any]:
        """Get retriever statistics."""
        return {
            "total_retrievals": self._total_retrievals,
            "helpful_retrievals": self._helpful_retrievals,
            "helpfulness_rate": self._helpful_retrievals / self._total_retrievals if self._total_retrievals > 0 else 0,
            "feedback_count": len(self._feedback_buffer),
            "adjustment_pairs": len(self._relevance_adjustments),
            "query_types_seen": len(set(qt for qt, _ in self._relevance_adjustments.keys())),
            "result_types_seen": len(set(rt for _, rt in self._relevance_adjustments.keys()))
        }

    async def persist(self):
        """Persist learned adjustments to memory."""
        if not self.memory:
            return

        try:
            data = {
                "adjustments": {f"{k[0]}:{k[1]}": v for k, v in self._relevance_adjustments.items()},
                "total_retrievals": self._total_retrievals,
                "helpful_retrievals": self._helpful_retrievals
            }

            await self.memory._run_query("""
                MERGE (n:LearnedRetriever {id: 'default'})
                SET n.data = $data,
                    n.updated_at = datetime()
            """, {"data": json.dumps(data)})
        except Exception as e:
            print(f"LearnedRetriever persist error: {e}")

    async def load(self):
        """Load learned adjustments from memory."""
        if not self.memory:
            return

        try:
            result = await self.memory._run_query("""
                MATCH (n:LearnedRetriever {id: 'default'})
                RETURN n.data as data
            """)

            if result and result[0].get("data"):
                data = json.loads(result[0]["data"])

                # Restore adjustments
                for key_str, value in data.get("adjustments", {}).items():
                    parts = key_str.split(":")
                    if len(parts) == 2:
                        self._relevance_adjustments[(parts[0], parts[1])] = value

                self._total_retrievals = data.get("total_retrievals", 0)
                self._helpful_retrievals = data.get("helpful_retrievals", 0)

        except Exception as e:
            print(f"LearnedRetriever load error: {e}")

    def suggest_improvements(self) -> List[str]:
        """Suggest improvements based on learned patterns."""
        suggestions = []

        # Find underperforming query-result combinations
        for (query_type, result_type), adjustment in self._relevance_adjustments.items():
            if adjustment < 0.7:
                suggestions.append(
                    f"'{result_type}' results are often unhelpful for '{query_type}' queries"
                )
            elif adjustment > 1.5:
                suggestions.append(
                    f"Prioritize '{result_type}' results for '{query_type}' queries"
                )

        return suggestions
