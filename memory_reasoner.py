#!/usr/bin/env python3
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

INTEGRATED WITH LOOP INSTRUMENTATION:
- Tracks memory ratio improvement over time to detect zero-delta loops
- Monitors stagnation patterns in memory retrieval
- Triggers interventions when improvement stalls
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

# Import loop instrumentation to break zero-delta loops
try:
    from loop_instrumentation import LoopInstrumenter, CycleMetrics, get_instrumenter
    HAS_INSTRUMENTATION = True
except ImportError:
    HAS_INSTRUMENTATION = False
    print("[WARNING] loop_instrumentation not available - zero-delta detection disabled")

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

        # Initialize loop instrumentation to break zero-delta loops
        self.instrumenter: Optional['LoopInstrumenter'] = None
        self.loop_name: str = "memory_reasoner"
        if HAS_INSTRUMENTATION:
            try:
                self.instrumenter = get_instrumenter()
                if self.instrumenter:
                    self.instrumenter.register_loop(self.loop_name)
                    print(f"[INSTRUMENTATION] Registered loop '{self.loop_name}' for zero-delta detection")
            except Exception:
                pass

        # Learning component (injected by Omega)
        self.learned_retriever = None  # LearnedRetriever for relevance boosting

        # Cycle counter for instrumentation
        self._cycle_counter = 0

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

        # Emit query event for compounding orchestrator
        await event_bus.emit(Event(
            type=EventType.MEMORY_REASONING_QUERY,
            data={
                "query": query[:200],
                "context": context
            }
        ))

        try:
            # Step 1: Embed the query
            embedder = await self._get_embedder()
            query_result = await embedder.embed(query)
            query_embedding = query_result.embedding

            # Step 2: Find seed nodes (semantically similar, with learned boosting)
            seed_nodes = await self._find_seed_nodes(query_embedding, query_text=query)

            if not seed_nodes:
                # No similar nodes found - must use LLM
                if force_memory:
                    result = self._empty_result(query, start_time)
                    self._record_reasoning_cycle(result, start_time, memory_based=False, confidence=0.0)
                    return result
                result = await self._llm_fallback(query, context, start_time)
                self._record_reasoning_cycle(result, start_time, memory_based=False, confidence=0.7)
                return result

            # Step 3: Spread activation through the graph
            activated = await self._spread_activation(seed_nodes)

            # Step 4: Try to compose answer from activated nodes
            answer, confidence = await self._compose_answer(query, activated)

            # Step 5: Decide if answer is sufficient
            if confidence >= 0.6 or force_memory:
                # Memory-based answer is good enough
                self._memory_answered += 1

                await event_bus.emit(Event(
                    type=EventType.MEMORY_REASONING_ANSWER,
                    data={
                        "query": query[:100],
                        "confidence": confidence,
                        "source_nodes": [n.node_id for n in activated[:10]],
                        "used_llm": False,
                        "activation_count": len(activated)
                    }
                ))

                elapsed_ms = (datetime.now() - start_time).total_seconds() * 1000

                # Record feedback to learned retriever (helpful = high confidence)
                if self.learned_retriever and activated:
                    for node in activated[:5]:  # Top 5 were most helpful
                        await self.learned_retriever.record_feedback(
                            query, node.node_id, was_helpful=(confidence >= 0.6)
                        )

                # INTEGRATION WITH LOOP INSTRUMENTATION
                # Record cycle metrics to break zero-delta loops
                if self.instrumenter and HAS_INSTRUMENTATION:
                    result = ReasoningResult(
                        answer=answer,
                        confidence=confidence,
                        source_nodes=[n.node_id for n in activated[:10]],
                        activation_path=activated,
                        used_llm=False,
                        reasoning_time_ms=elapsed_ms
                    )
                    self._record_reasoning_cycle(result, start_time, memory_based=True, confidence=confidence)

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
                result = await self._llm_fallback(
                    query, context, start_time,
                    memory_context=activated
                )
                self._record_reasoning_cycle(result, start_time, memory_based=False, confidence=0.7)
                return result

        except Exception as e:
            logger.error(f"Memory reasoning failed: {e}")
            if force_memory:
                result = self._empty_result(query, start_time)
            else:
                result = await self._llm_fallback(query, context, start_time)
            self._record_reasoning_cycle(result, start_time, memory_based=False, confidence=0.0)
            return result

    async def _find_seed_nodes(
        self,
        query_embedding: List[float],
        query_text: str = ""
    ) -> List[ActivatedNode]:
        """
        Find nodes semantically similar to the query.

        These become the seeds for spreading activation.
        """
        try:
            # Search for similar nodes
            results = await self.memory.search_similar(
                embedding=query_embedding,
                limit=20
            )

            if not results:
                return []

            # Convert to ActivatedNode with similarity as base activation
            seeds = []
            for node in results:
                # Extract content from different node types
                content = (
                    node.get("content") or
                    node.get("essence") or  # Crystal
                    str(node.get("raw_output", ""))[:500]  # Reflection
                )

                # Base activation is similarity
                base_activation = node["similarity"]

                # Apply learned boost if available
                learned_boost = 1.0
                if self.learned_retriever and query_text:
                    learned_boost = self.learned_retriever.get_learned_boost(
                        self.learned_retriever._classify_query(query_text),
                        self.learned_retriever._classify_result({"type": node.get("labels", ["unknown"])[0] if node.get("labels") else "unknown"})
                    )

                seeds.append(ActivatedNode(
                    node_id=node["id"],
                    labels=node.get("labels", []),
                    content=content,
                    activation=base_activation * learned_boost,
                    hops=0,
                    path=[node["id"]]
                ))

            # Re-sort by boosted activation and limit
            seeds.sort(key=lambda s: s.activation, reverse=True)
            return seeds[:10]

        except Exception as e:
            logger.error(f"Seed node search failed: {e}")
            return []

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
        """Return empty result when reasoning fails."""
        elapsed_ms = (datetime.now() - start_time).total_seconds() * 1000
        return ReasoningResult(
            answer=f"Unable to answer query '{query[:50]}...'",
            confidence=0.0,
            source_nodes=[],
            activation_path=[],
            used_llm=False,
            reasoning_time_ms=elapsed_ms
        )

    def get_memory_ratio(self) -> float:
        """Return the ratio of queries answered from memory."""
        if self._total_queries == 0:
            return 0.0
        return self._memory_answered / self._total_queries

    def is_performing_well(self) -> bool:
        """
        Check if the memory reasoner is performing well.

        Criteria:
        - At least 10 queries processed
        - Memory ratio is above 0.5 (half answered from memory)
        """
        if self._total_queries < 10:
            return True  # Too early to judge

        return self.get_memory_ratio() >= 0.5

    def get_metrics(self) -> Dict[str, Any]:
        """Get Memory Reasoner metrics for Omega monitoring."""
        memory_ratio = self.get_memory_ratio()
        return {
            "total_queries": self._total_queries,
            "memory_answered": self._memory_answered,
            "llm_answered": self._llm_answered,
            "memory_ratio": round(memory_ratio, 3),
            "target_memory_ratio": self.target_memory_ratio,
            "is_performing_well": self.is_performing_well(),
            "similarity_threshold": self.similarity_threshold,
            "spreading_activation": {
                "decay": self.decay,
                "threshold": self.threshold,
                "max_hops": self.max_hops,
                "max_nodes": self.max_nodes
            }
        }

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

    def _record_reasoning_cycle(
        self,
        result: Optional[ReasoningResult],
        start_time: datetime,
        memory_based: bool,
        confidence: float
    ) -> None:
        """
        Record reasoning cycle metrics with loop instrumenter.
        
        This breaks the zero-delta loop by tracking:
        - Memory ratio improvement (delta)
        - Success based on memory-based answering
        - Duration of the reasoning cycle
        - Whether the improvement was meaningful
        """
        if not self.instrumenter:
            return
        
        self._cycle_counter += 1
        
        # Calculate delta as change in memory ratio
        if self._total_queries > 0:
            current_memory_ratio = self._memory_answered / self._total_queries
        else:
            current_memory_ratio = 0.0
        
        # Track baseline memory ratio from previous cycles
        if not hasattr(self, '_baseline_memory_ratio'):
            self._baseline_memory_ratio = 0.0
        
        # Delta is improvement in memory ratio
        delta = current_memory_ratio - self._baseline_memory_ratio
        self._baseline_memory_ratio = current_memory_ratio
        
        # Success if we answered from memory (memory_based=True) or improved ratio
        success = memory_based or delta > 0
        
        # Duration
        duration_seconds = (datetime.now() - start_time).total_seconds()
        
        # Meaningful if delta >= 0.5% (MIN_MEANINGFUL_DELTA)
        MIN_MEANINGFUL_DELTA = 0.005
        is_meaningful = delta >= MIN_MEANINGFUL_DELTA
        
        # Create cycle metrics
        from loop_instrumentation import CycleMetrics
        metrics = CycleMetrics(
            cycle_number=self._cycle_counter,
            timestamp=datetime.now(),
            delta=delta,
            success=success,
            meaningful=is_meaningful,
            duration_seconds=duration_seconds,
            error=None
        )
        
        # Record with instrumenter
        self.instrumenter.record_cycle(self.loop_name, metrics)
        
        # Check for stagnation and log warning
        if self.instrumenter.is_stagnant(self.loop_name):
            analysis = self.instrumenter.analyze_stagnation(self.loop_name)
            logger.warning(f"[INSTRUMENTATION] Memory Reasoner stagnation detected: {analysis}")


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
