"""
BYRD Memory Reasoner
Loop 1 of Option B: Graph-Based Reasoning

The Memory Reasoner answers queries by spreading activation through the
memory graph instead of defaulting to LLM. The key insight:

    BYRD's accumulated knowledge is already in the graph.
    Before asking the LLM, search what you already know.

Core Algorithm:
1. Embed the query
2. Find semantically similar nodes (seed nodes)
3. Spread activation through graph relationships
4. Compose answer from activated nodes
5. Only use LLM if memory-based answer is insufficient

THE CRITICAL METRIC: memory_ratio
- Target: 80% of queries answered from memory
- If LLM handles most queries, we're not learning

This loop compounds because:
- Every new experience/belief adds to the graph
- Better answers create better beliefs
- Graph structure captures relationships LLM can't see
"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field

from embedding import (
    EmbeddingProvider, cosine_similarity,
    get_embedding_provider, get_global_embedder
)
from event_bus import event_bus, Event, EventType
from memory import Memory

logger = logging.getLogger(__name__)


@dataclass
class ActivatedNode:
    """A node with spreading activation score."""
    node_id: str
    labels: List[str]
    content: str
    activation: float
    hops: int  # How many hops from seed
    path: List[str] = field(default_factory=list)  # Path from seed


@dataclass
class ReasoningResult:
    """Result of memory-based reasoning."""
    answer: str
    confidence: float
    source_nodes: List[str]
    activation_path: List[ActivatedNode]
    used_llm: bool
    reasoning_time_ms: float


class MemoryReasoner:
    """
    Answers queries using spreading activation through the memory graph.

    The reasoner embeds the query, finds similar nodes, spreads activation
    through relationships, and composes answers from highly activated nodes.
    """

    def __init__(
        self,
        memory: Memory,
        llm_client: Any,  # LLMClient for fallback
        config: Optional[Dict] = None
    ):
        """
        Initialize the Memory Reasoner.

        Args:
            memory: The BYRD memory system
            llm_client: LLM client for fallback when memory is insufficient
            config: Configuration from config.yaml option_b.memory_reasoner
        """
        self.memory = memory
        self.llm_client = llm_client
        self.config = config or {}

        # Spreading activation parameters
        sa_config = self.config.get("spreading_activation", {})
        self.decay = sa_config.get("decay", 0.6)
        self.threshold = sa_config.get("threshold", 0.1)
        self.max_hops = sa_config.get("max_hops", 3)
        self.max_nodes = sa_config.get("max_nodes", 50)

        # Similarity threshold for seed selection
        self.similarity_threshold = self.config.get("similarity_threshold", 0.6)

        # Target memory ratio
        self.target_memory_ratio = self.config.get("target_memory_ratio", 0.8)

        # Initialize embedding provider
        embedding_config = self.config.get("embedding", {})
        self._embedder: Optional[EmbeddingProvider] = None

        # Metrics
        self._total_queries = 0
        self._memory_answered = 0
        self._llm_answered = 0

    async def _get_embedder(self) -> EmbeddingProvider:
        """Get or create the embedding provider."""
        if self._embedder is None:
            self._embedder = get_global_embedder()
        return self._embedder

    async def reason(
        self,
        query: str,
        context: Optional[Dict] = None,
        force_memory: bool = False
    ) -> ReasoningResult:
        """
        Answer a query using memory-based reasoning.

        Args:
            query: The question or query to answer
            context: Optional context (e.g., recent experiences)
            force_memory: If True, never fall back to LLM

        Returns:
            ReasoningResult with answer, sources, and metrics
        """
        start_time = datetime.now()
        self._total_queries += 1

        try:
            # Step 1: Embed the query
            embedder = await self._get_embedder()
            query_result = await embedder.embed(query)
            query_embedding = query_result.embedding

            # Step 2: Find seed nodes (semantically similar)
            seed_nodes = await self._find_seed_nodes(query_embedding)

            if not seed_nodes:
                # No similar nodes found - must use LLM
                if force_memory:
                    return self._empty_result(query, start_time)
                return await self._llm_fallback(query, context, start_time)

            # Step 3: Spread activation through the graph
            activated = await self._spread_activation(seed_nodes)

            # Step 4: Try to compose answer from activated nodes
            answer, confidence = await self._compose_answer(query, activated)

            # Step 5: Decide if answer is sufficient
            if confidence >= 0.6 or force_memory:
                # Memory-based answer is good enough
                self._memory_answered += 1

                await event_bus.emit(Event(
                    type=EventType.MEMORY_QUERY_ANSWERED,
                    data={
                        "query": query[:100],
                        "confidence": confidence,
                        "source_count": len(activated),
                        "used_llm": False
                    }
                ))

                elapsed_ms = (datetime.now() - start_time).total_seconds() * 1000
                return ReasoningResult(
                    answer=answer,
                    confidence=confidence,
                    source_nodes=[n.node_id for n in activated[:10]],
                    activation_path=activated,
                    used_llm=False,
                    reasoning_time_ms=elapsed_ms
                )
            else:
                # Memory answer weak, fall back to LLM
                return await self._llm_fallback(
                    query, context, start_time,
                    memory_context=activated
                )

        except Exception as e:
            logger.error(f"Memory reasoning failed: {e}")
            if force_memory:
                return self._empty_result(query, start_time)
            return await self._llm_fallback(query, context, start_time)

    async def _find_seed_nodes(
        self,
        query_embedding: List[float]
    ) -> List[ActivatedNode]:
        """
        Find nodes semantically similar to the query.

        These become the seeds for spreading activation.
        """
        # Use memory's find_similar_nodes method
        similar = await self.memory.find_similar_nodes(
            embedding=query_embedding,
            min_similarity=self.similarity_threshold,
            limit=10,
            node_types=["Experience", "Belief", "Reflection", "Insight", "Crystal"]
        )

        seeds = []
        for node in similar:
            # Extract content from different node types
            content = (
                node.get("content") or
                node.get("essence") or  # Crystal
                str(node.get("raw_output", ""))[:500]  # Reflection
            )

            seeds.append(ActivatedNode(
                node_id=node["id"],
                labels=node.get("labels", []),
                content=content,
                activation=node["similarity"],  # Initial activation = similarity
                hops=0,
                path=[node["id"]]
            ))

        return seeds

    async def _spread_activation(
        self,
        seeds: List[ActivatedNode]
    ) -> List[ActivatedNode]:
        """
        Spread activation from seed nodes through graph relationships.

        Activation decays with each hop, stopping when below threshold.
        """
        # Track all activated nodes
        activated: Dict[str, ActivatedNode] = {
            n.node_id: n for n in seeds
        }

        # BFS frontier
        frontier = list(seeds)

        await event_bus.emit(Event(
            type=EventType.SPREADING_ACTIVATION,
            data={
                "seed_count": len(seeds),
                "max_hops": self.max_hops
            }
        ))

        for hop in range(1, self.max_hops + 1):
            if not frontier:
                break

            next_frontier = []

            for node in frontier:
                # Get neighbors
                neighbors = await self.memory.get_neighbors(node.node_id)

                for neighbor_data in neighbors:
                    neighbor = neighbor_data["node"]
                    neighbor_id = neighbor.get("id")

                    if not neighbor_id:
                        continue

                    # Compute activation for neighbor
                    new_activation = node.activation * self.decay

                    if new_activation < self.threshold:
                        continue

                    # Check if already activated (keep higher)
                    if neighbor_id in activated:
                        if new_activation <= activated[neighbor_id].activation:
                            continue

                    # Extract content
                    content = (
                        neighbor.get("content") or
                        neighbor.get("essence") or
                        neighbor.get("description") or
                        str(neighbor.get("raw_output", ""))[:500]
                    )

                    activated_node = ActivatedNode(
                        node_id=neighbor_id,
                        labels=neighbor_data.get("labels", []),
                        content=content,
                        activation=new_activation,
                        hops=hop,
                        path=node.path + [neighbor_id]
                    )

                    activated[neighbor_id] = activated_node
                    next_frontier.append(activated_node)

                    if len(activated) >= self.max_nodes:
                        break

                if len(activated) >= self.max_nodes:
                    break

            frontier = next_frontier

        # Sort by activation score
        result = sorted(
            activated.values(),
            key=lambda n: n.activation,
            reverse=True
        )

        return result[:self.max_nodes]

    async def _compose_answer(
        self,
        query: str,
        activated: List[ActivatedNode]
    ) -> Tuple[str, float]:
        """
        Compose an answer from activated nodes.

        Uses local LLM to synthesize the activated content into a coherent answer.
        Returns (answer, confidence).
        """
        if not activated:
            return "", 0.0

        # Build context from activated nodes
        context_parts = []
        for i, node in enumerate(activated[:15]):  # Top 15 nodes
            node_type = node.labels[0] if node.labels else "Unknown"
            context_parts.append(
                f"[{node_type}, activation={node.activation:.2f}] {node.content}"
            )

        context_text = "\n".join(context_parts)

        # Use LLM to synthesize
        prompt = f"""Based on the following relevant memories, answer the query.
If the memories don't contain enough information, say "INSUFFICIENT".

Query: {query}

Relevant Memories:
{context_text}

Answer (be concise and cite which memories support your answer):"""

        try:
            response = await self.llm_client.query(prompt, max_tokens=500)

            # Check if LLM says insufficient
            if "INSUFFICIENT" in response.upper():
                return response, 0.3

            # Estimate confidence based on activation scores
            avg_activation = sum(n.activation for n in activated[:5]) / min(5, len(activated))
            confidence = min(0.9, avg_activation + 0.2)

            return response, confidence

        except Exception as e:
            logger.error(f"Answer composition failed: {e}")
            return "", 0.0

    async def _llm_fallback(
        self,
        query: str,
        context: Optional[Dict],
        start_time: datetime,
        memory_context: Optional[List[ActivatedNode]] = None
    ) -> ReasoningResult:
        """
        Fall back to LLM when memory is insufficient.

        Still uses memory context to enhance the answer if available.
        """
        self._llm_answered += 1

        # Build prompt with optional memory context
        if memory_context:
            context_parts = [
                f"[{n.labels[0] if n.labels else 'Memory'}] {n.content[:200]}"
                for n in memory_context[:5]
            ]
            context_text = "\n".join(context_parts)
            prompt = f"""Query: {query}

Relevant context from memory (may be incomplete):
{context_text}

Please answer the query, supplementing the memory context with your knowledge:"""
        else:
            prompt = f"Query: {query}\n\nPlease provide a helpful answer:"

        try:
            response = await self.llm_client.query(prompt, max_tokens=800)

            elapsed_ms = (datetime.now() - start_time).total_seconds() * 1000

            await event_bus.emit(Event(
                type=EventType.MEMORY_QUERY_ANSWERED,
                data={
                    "query": query[:100],
                    "confidence": 0.7,
                    "source_count": len(memory_context) if memory_context else 0,
                    "used_llm": True
                }
            ))

            return ReasoningResult(
                answer=response,
                confidence=0.7,  # Lower confidence for LLM-only answers
                source_nodes=[n.node_id for n in memory_context[:5]] if memory_context else [],
                activation_path=memory_context or [],
                used_llm=True,
                reasoning_time_ms=elapsed_ms
            )

        except Exception as e:
            logger.error(f"LLM fallback failed: {e}")
            return self._empty_result(query, start_time)

    def _empty_result(
        self,
        query: str,
        start_time: datetime
    ) -> ReasoningResult:
        """Return an empty result when reasoning fails completely."""
        elapsed_ms = (datetime.now() - start_time).total_seconds() * 1000
        return ReasoningResult(
            answer="Unable to answer the query.",
            confidence=0.0,
            source_nodes=[],
            activation_path=[],
            used_llm=False,
            reasoning_time_ms=elapsed_ms
        )

    def get_memory_ratio(self) -> float:
        """
        Get the ratio of queries answered from memory.

        This is THE critical metric for the Memory Reasoner.
        Target: 0.8 (80% from memory, 20% from LLM)
        """
        if self._total_queries == 0:
            return 0.0
        return self._memory_answered / self._total_queries

    def get_metrics(self) -> Dict[str, float]:
        """Get all Memory Reasoner metrics."""
        return {
            "total_queries": self._total_queries,
            "memory_answered": self._memory_answered,
            "llm_answered": self._llm_answered,
            "memory_ratio": self.get_memory_ratio(),
            "target_ratio": self.target_memory_ratio,
            "ratio_gap": self.target_memory_ratio - self.get_memory_ratio()
        }

    def is_healthy(self) -> bool:
        """
        Check if the Memory Reasoner is healthy.

        Health criteria:
        - Has processed at least 10 queries
        - Memory ratio is above 0.5 (half answered from memory)
        """
        if self._total_queries < 10:
            return True  # Too early to judge

        return self.get_memory_ratio() >= 0.5

    async def record_feedback(
        self,
        query: str,
        result: ReasoningResult,
        was_helpful: bool
    ):
        """
        Record feedback on a reasoning result.

        This helps the system learn which memory paths are useful.
        """
        if was_helpful and result.source_nodes:
            # Boost the embeddings/importance of source nodes
            # This could update PageRank or connection strengths
            for node_id in result.source_nodes[:5]:
                try:
                    # Could update node importance here
                    # For now, just log
                    logger.debug(f"Positive feedback for node {node_id}")
                except Exception:
                    pass

        # Record insight if we learned something
        if was_helpful and not result.used_llm:
            try:
                await self.memory.create_insight(
                    content=f"Successfully answered '{query[:50]}...' from memory",
                    source_type="reflection",
                    confidence=result.confidence,
                    supporting_evidence=result.source_nodes[:5]
                )
            except Exception as e:
                logger.debug(f"Could not record insight: {e}")


# Factory function
def create_memory_reasoner(
    memory: Memory,
    llm_client: Any,
    config: Dict
) -> MemoryReasoner:
    """
    Create a Memory Reasoner from configuration.

    Args:
        memory: The BYRD memory system
        llm_client: LLM client for fallback
        config: Full config.yaml dict

    Returns:
        Configured MemoryReasoner instance
    """
    mr_config = config.get("option_b", {}).get("memory_reasoner", {})
    return MemoryReasoner(memory, llm_client, mr_config)
