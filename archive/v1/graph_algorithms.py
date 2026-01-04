"""
Graph Algorithms for BYRD Memory

Implements advanced graph algorithms for enhanced memory retrieval and analysis.
All algorithms are custom Python implementations for Neo4j Aura compatibility.

EMERGENCE PRINCIPLE:
These algorithms discover patterns from the graph structure itself.
No prescribed importance or hard-coded rankings - significance emerges
from BYRD's own connection patterns.

Algorithms:
1. PageRank - Importance scoring with personalization
2. Spreading Activation - Associative memory retrieval
3. Contradiction Detection - Structural + semantic conflict finding
4. Dream Walk - Quantum-influenced graph traversal
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Set, Any
from dataclasses import dataclass
from datetime import datetime
import random


@dataclass
class PageRankResult:
    """Result of PageRank computation."""
    scores: Dict[str, float]
    iterations: int
    converged: bool


@dataclass
class ActivationResult:
    """Result of spreading activation."""
    activated_nodes: Dict[str, float]  # node_id -> activation level
    path: List[str]  # traversal path


@dataclass
class ContradictionPair:
    """A detected contradiction between two nodes."""
    node1_id: str
    node2_id: str
    node1_content: str
    node2_content: str
    confidence: float
    detection_method: str  # "structural" or "semantic"


@dataclass
class DreamWalkResult:
    """Result of a quantum dream walk."""
    path: List[str]
    node_types: List[str]
    total_weight: float
    quantum_influenced: bool


class GraphAlgorithms:
    """
    Graph algorithm implementations for BYRD memory.

    These algorithms operate on data extracted from Neo4j and return
    results that can be used to enhance memory retrieval.
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize graph algorithms with configuration.

        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}

        # PageRank settings
        self.pagerank_damping = self.config.get("pagerank", {}).get("damping", 0.85)
        self.pagerank_iterations = self.config.get("pagerank", {}).get("iterations", 20)
        self.pagerank_tolerance = self.config.get("pagerank", {}).get("tolerance", 1e-6)

        # Spreading activation settings
        self.activation_decay = self.config.get("spreading_activation", {}).get("decay", 0.6)
        self.activation_threshold = self.config.get("spreading_activation", {}).get("threshold", 0.1)
        self.activation_max_nodes = self.config.get("spreading_activation", {}).get("max_nodes", 50)

        # Dream walk settings
        self.dream_walk_steps = self.config.get("dream_walks", {}).get("steps", 10)
        self.dream_walk_quantum = self.config.get("dream_walks", {}).get("quantum_influence", True)

    def compute_pagerank(
        self,
        adjacency: Dict[str, List[str]],
        personalization: Optional[Dict[str, float]] = None,
        damping: Optional[float] = None,
        max_iterations: Optional[int] = None
    ) -> PageRankResult:
        """
        Compute PageRank scores for nodes.

        Uses power iteration to compute importance scores. Personalization
        vector allows biasing toward specific nodes (e.g., recent experiences).

        Args:
            adjacency: Dict mapping node_id -> list of connected node_ids
            personalization: Optional dict of node_id -> preference weight
            damping: Damping factor (default 0.85)
            max_iterations: Maximum iterations (default 20)

        Returns:
            PageRankResult with scores for each node
        """
        damping = damping or self.pagerank_damping
        max_iterations = max_iterations or self.pagerank_iterations

        nodes = list(adjacency.keys())
        n = len(nodes)

        if n == 0:
            return PageRankResult(scores={}, iterations=0, converged=True)

        # Build node index
        node_to_idx = {node: i for i, node in enumerate(nodes)}

        # Initialize scores uniformly or from personalization
        if personalization:
            total = sum(personalization.values())
            scores = np.array([
                personalization.get(node, 0.0) / total if total > 0 else 1.0 / n
                for node in nodes
            ])
        else:
            scores = np.ones(n) / n

        # Personalization vector for teleportation
        if personalization:
            total = sum(personalization.values())
            teleport = np.array([
                personalization.get(node, 0.0) / total if total > 0 else 1.0 / n
                for node in nodes
            ])
        else:
            teleport = np.ones(n) / n

        # Build transition matrix (column-stochastic)
        # For outgoing links from each node
        out_degree = np.zeros(n)
        for i, node in enumerate(nodes):
            out_degree[i] = len(adjacency.get(node, []))

        # Power iteration
        converged = False
        for iteration in range(max_iterations):
            new_scores = np.zeros(n)

            for i, node in enumerate(nodes):
                # Gather incoming contributions
                for j, other_node in enumerate(nodes):
                    if node in adjacency.get(other_node, []):
                        if out_degree[j] > 0:
                            new_scores[i] += scores[j] / out_degree[j]

            # Apply damping
            new_scores = damping * new_scores + (1 - damping) * teleport

            # Check convergence
            diff = np.abs(new_scores - scores).sum()
            if diff < self.pagerank_tolerance:
                converged = True
                scores = new_scores
                break

            scores = new_scores

        # Normalize to [0, 1]
        max_score = scores.max() if scores.max() > 0 else 1.0
        scores = scores / max_score

        return PageRankResult(
            scores={nodes[i]: float(scores[i]) for i in range(n)},
            iterations=iteration + 1,
            converged=converged
        )

    def spreading_activation(
        self,
        adjacency: Dict[str, List[str]],
        seed_nodes: List[str],
        initial_activation: float = 1.0,
        decay: Optional[float] = None,
        threshold: Optional[float] = None,
        max_nodes: Optional[int] = None
    ) -> ActivationResult:
        """
        Perform spreading activation from seed nodes.

        Activation spreads from seeds through connections, decaying
        at each hop. Nodes with activation above threshold are returned.

        Args:
            adjacency: Dict mapping node_id -> list of connected node_ids
            seed_nodes: Starting nodes for activation
            initial_activation: Initial activation level for seeds
            decay: Decay factor per hop (default 0.6)
            threshold: Minimum activation to keep (default 0.1)
            max_nodes: Maximum nodes to return (default 50)

        Returns:
            ActivationResult with activated nodes and traversal path
        """
        decay = decay or self.activation_decay
        threshold = threshold or self.activation_threshold
        max_nodes = max_nodes or self.activation_max_nodes

        # Initialize activation
        activation: Dict[str, float] = {}
        for seed in seed_nodes:
            if seed in adjacency:
                activation[seed] = initial_activation

        if not activation:
            return ActivationResult(activated_nodes={}, path=[])

        path = list(seed_nodes)
        visited: Set[str] = set(seed_nodes)
        frontier = list(seed_nodes)

        # Spread activation
        while frontier and len(activation) < max_nodes:
            next_frontier = []

            for node in frontier:
                current_activation = activation.get(node, 0.0)
                spread_activation = current_activation * decay

                if spread_activation < threshold:
                    continue

                # Spread to neighbors
                neighbors = adjacency.get(node, [])
                for neighbor in neighbors:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        # Accumulate activation (nodes can receive from multiple sources)
                        activation[neighbor] = activation.get(neighbor, 0.0) + spread_activation
                        next_frontier.append(neighbor)
                        path.append(neighbor)

            frontier = next_frontier

        # Filter by threshold and limit
        activated = {
            node: score for node, score in activation.items()
            if score >= threshold
        }

        # Sort by activation and limit
        sorted_nodes = sorted(activated.items(), key=lambda x: x[1], reverse=True)
        activated = dict(sorted_nodes[:max_nodes])

        return ActivationResult(
            activated_nodes=activated,
            path=path[:max_nodes]
        )

    def detect_contradictions_structural(
        self,
        beliefs: List[Dict[str, Any]],
        adjacency: Dict[str, List[str]],
        contradiction_rel: str = "CONTRADICTS"
    ) -> List[ContradictionPair]:
        """
        Detect contradictions using structural analysis.

        Finds beliefs that are explicitly marked as contradicting
        or have opposing relationships.

        Args:
            beliefs: List of belief dicts with 'id', 'content', 'confidence'
            adjacency: Dict mapping node_id -> list of connected node_ids
            contradiction_rel: Relationship type indicating contradiction

        Returns:
            List of detected ContradictionPair objects
        """
        contradictions = []
        belief_map = {b['id']: b for b in beliefs}
        seen_pairs: Set[Tuple[str, str]] = set()

        for belief in beliefs:
            node_id = belief['id']
            connected = adjacency.get(node_id, [])

            for other_id in connected:
                if other_id not in belief_map:
                    continue

                # Create canonical pair to avoid duplicates
                pair = tuple(sorted([node_id, other_id]))
                if pair in seen_pairs:
                    continue
                seen_pairs.add(pair)

                other = belief_map[other_id]

                # Calculate confidence based on both beliefs' confidence
                confidence = (belief.get('confidence', 0.5) + other.get('confidence', 0.5)) / 2

                contradictions.append(ContradictionPair(
                    node1_id=node_id,
                    node2_id=other_id,
                    node1_content=belief.get('content', ''),
                    node2_content=other.get('content', ''),
                    confidence=confidence,
                    detection_method="structural"
                ))

        return contradictions

    def detect_contradictions_semantic(
        self,
        beliefs: List[Dict[str, Any]],
        similarity_threshold: float = 0.7,
        confidence_threshold: float = 0.6
    ) -> List[Tuple[str, str, float]]:
        """
        Identify potential contradictions for semantic checking.

        Returns pairs of high-confidence beliefs that might contradict
        based on keyword overlap (actual semantic check requires LLM).

        Args:
            beliefs: List of belief dicts with 'id', 'content', 'confidence'
            similarity_threshold: Minimum content similarity to consider
            confidence_threshold: Minimum belief confidence to check

        Returns:
            List of (belief1_id, belief2_id, similarity_score) tuples
        """
        candidates = []

        # Filter to high-confidence beliefs
        high_conf = [b for b in beliefs if b.get('confidence', 0) >= confidence_threshold]

        for i, belief1 in enumerate(high_conf):
            for belief2 in high_conf[i+1:]:
                # Simple keyword-based similarity
                words1 = set(belief1.get('content', '').lower().split())
                words2 = set(belief2.get('content', '').lower().split())

                if not words1 or not words2:
                    continue

                intersection = len(words1 & words2)
                union = len(words1 | words2)
                similarity = intersection / union if union > 0 else 0

                if similarity >= similarity_threshold:
                    candidates.append((
                        belief1['id'],
                        belief2['id'],
                        similarity
                    ))

        return candidates

    def dream_walk(
        self,
        adjacency: Dict[str, List[str]],
        node_weights: Dict[str, float],
        node_types: Dict[str, str],
        start_node: str,
        steps: Optional[int] = None,
        quantum_delta: Optional[float] = None
    ) -> DreamWalkResult:
        """
        Perform a quantum-influenced random walk through the graph.

        The walk is biased by node weights (importance/salience) but
        perturbed by quantum randomness for exploration.

        Args:
            adjacency: Dict mapping node_id -> list of connected node_ids
            node_weights: Dict mapping node_id -> importance weight
            node_types: Dict mapping node_id -> node type string
            start_node: Starting node for the walk
            steps: Number of steps to take (default from config)
            quantum_delta: Quantum perturbation factor (0-1)

        Returns:
            DreamWalkResult with walk path and metadata
        """
        steps = steps or self.dream_walk_steps

        if start_node not in adjacency:
            return DreamWalkResult(
                path=[start_node],
                node_types=[node_types.get(start_node, "Unknown")],
                total_weight=node_weights.get(start_node, 0.0),
                quantum_influenced=False
            )

        path = [start_node]
        types = [node_types.get(start_node, "Unknown")]
        total_weight = node_weights.get(start_node, 0.0)
        current = start_node
        quantum_used = False

        for _ in range(steps):
            neighbors = adjacency.get(current, [])
            if not neighbors:
                break

            # Calculate weights for neighbors
            weights = []
            for neighbor in neighbors:
                w = node_weights.get(neighbor, 0.1)  # Default weight for unknown nodes
                weights.append(w)

            if not weights:
                break

            # Apply quantum perturbation if available
            if quantum_delta is not None and self.dream_walk_quantum:
                quantum_used = True
                # Perturb weights by quantum delta
                perturbation = np.random.randn(len(weights)) * quantum_delta
                weights = np.array(weights) + perturbation
                weights = np.maximum(weights, 0.01)  # Ensure positive
            else:
                weights = np.array(weights)

            # Normalize to probabilities
            weights = weights / weights.sum()

            # Select next node
            next_idx = np.random.choice(len(neighbors), p=weights)
            current = neighbors[next_idx]

            path.append(current)
            types.append(node_types.get(current, "Unknown"))
            total_weight += node_weights.get(current, 0.0)

        return DreamWalkResult(
            path=path,
            node_types=types,
            total_weight=total_weight,
            quantum_influenced=quantum_used
        )

    def get_causal_chain(
        self,
        adjacency: Dict[str, List[Tuple[str, str]]],  # node_id -> [(neighbor_id, rel_type)]
        start_node: str,
        direction: str = "forward",
        causal_types: Optional[Set[str]] = None,
        max_depth: int = 10
    ) -> List[Tuple[str, str, str]]:
        """
        Trace causal chain from a node.

        Follows causal relationships (CAUSED, ENABLED, PREVENTED, PREDICTED)
        to build a chain of cause-effect relationships.

        Args:
            adjacency: Dict mapping node_id -> [(neighbor_id, relationship_type)]
            start_node: Starting node for chain
            direction: "forward" (causes) or "backward" (caused by)
            causal_types: Set of relationship types to follow
            max_depth: Maximum chain length

        Returns:
            List of (source_id, relationship, target_id) tuples
        """
        if causal_types is None:
            causal_types = {"CAUSED", "ENABLED", "PREVENTED", "PREDICTED"}

        chain = []
        visited: Set[str] = set()
        frontier = [start_node]

        for _ in range(max_depth):
            if not frontier:
                break

            next_frontier = []

            for node in frontier:
                if node in visited:
                    continue
                visited.add(node)

                connections = adjacency.get(node, [])
                for neighbor_id, rel_type in connections:
                    if rel_type in causal_types and neighbor_id not in visited:
                        if direction == "forward":
                            chain.append((node, rel_type, neighbor_id))
                        else:
                            chain.append((neighbor_id, rel_type, node))
                        next_frontier.append(neighbor_id)

            frontier = next_frontier

        return chain


class MemoryGraphAlgorithms:
    """
    Integration layer between GraphAlgorithms and BYRD's Memory system.

    Extracts data from Neo4j, runs algorithms, and provides enhanced
    retrieval methods.
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize with optional configuration.

        Args:
            config: Configuration dict (typically from config.yaml)
        """
        self.algorithms = GraphAlgorithms(config)
        self.config = config or {}

        # Cache for graph data
        self._adjacency_cache: Dict[str, List[str]] = {}
        self._adjacency_typed_cache: Dict[str, List[Tuple[str, str]]] = {}
        self._node_weights_cache: Dict[str, float] = {}
        self._node_types_cache: Dict[str, str] = {}
        self._pagerank_cache: Optional[PageRankResult] = None
        self._last_update: Optional[datetime] = None
        self._cache_ttl_seconds = 300  # 5 minutes

    def _is_cache_stale(self) -> bool:
        """Check if cache needs refresh."""
        if self._last_update is None:
            return True
        elapsed = (datetime.now() - self._last_update).total_seconds()
        return elapsed > self._cache_ttl_seconds

    async def extract_graph_structure(self, memory) -> None:
        """
        Extract graph structure from Neo4j memory.

        Populates adjacency lists and node metadata caches.

        Args:
            memory: BYRD Memory instance
        """
        self._adjacency_cache = {}
        self._adjacency_typed_cache = {}
        self._node_weights_cache = {}
        self._node_types_cache = {}

        async with memory.driver.session() as session:
            # Get all nodes with their types and properties
            node_result = await session.run("""
                MATCH (n)
                WHERE n.id IS NOT NULL
                RETURN n.id as id,
                       labels(n)[0] as node_type,
                       n.confidence as confidence,
                       n.intensity as intensity,
                       n.access_count as access_count
            """)
            node_records = await node_result.data()

            for record in node_records:
                node_id = record['id']
                self._node_types_cache[node_id] = record['node_type'] or "Unknown"

                # Calculate weight from various factors
                confidence = record.get('confidence') or 0.5
                intensity = record.get('intensity') or 0.5
                access_count = record.get('access_count') or 0

                # Combined weight
                weight = (confidence * 0.3 + intensity * 0.3 +
                         min(access_count / 10.0, 1.0) * 0.4)
                self._node_weights_cache[node_id] = weight

                # Initialize adjacency
                self._adjacency_cache[node_id] = []
                self._adjacency_typed_cache[node_id] = []

            # Get all relationships
            rel_result = await session.run("""
                MATCH (a)-[r]->(b)
                WHERE a.id IS NOT NULL AND b.id IS NOT NULL
                RETURN a.id as source, b.id as target, type(r) as rel_type
            """)
            rel_records = await rel_result.data()

            for record in rel_records:
                source = record['source']
                target = record['target']
                rel_type = record['rel_type']

                if source in self._adjacency_cache:
                    self._adjacency_cache[source].append(target)
                    self._adjacency_typed_cache[source].append((target, rel_type))

                # Add reverse for undirected traversal
                if target in self._adjacency_cache:
                    self._adjacency_cache[target].append(source)
                    self._adjacency_typed_cache[target].append((source, rel_type))

        self._last_update = datetime.now()

    async def get_pagerank_scores(
        self,
        memory,
        personalization: Optional[Dict[str, float]] = None,
        force_refresh: bool = False
    ) -> Dict[str, float]:
        """
        Get PageRank importance scores for all nodes.

        Args:
            memory: BYRD Memory instance
            personalization: Optional preference weights for nodes
            force_refresh: Force recomputation even if cached

        Returns:
            Dict mapping node_id -> importance score
        """
        if force_refresh or self._is_cache_stale():
            await self.extract_graph_structure(memory)
            self._pagerank_cache = None

        if self._pagerank_cache is None or personalization:
            self._pagerank_cache = self.algorithms.compute_pagerank(
                self._adjacency_cache,
                personalization=personalization
            )

        return self._pagerank_cache.scores

    async def get_activated_memories(
        self,
        memory,
        seed_node_ids: List[str],
        initial_activation: float = 1.0
    ) -> Dict[str, float]:
        """
        Get memories activated by spreading from seed nodes.

        Args:
            memory: BYRD Memory instance
            seed_node_ids: Starting nodes for activation spread
            initial_activation: Initial activation level

        Returns:
            Dict mapping node_id -> activation level
        """
        if self._is_cache_stale():
            await self.extract_graph_structure(memory)

        result = self.algorithms.spreading_activation(
            self._adjacency_cache,
            seed_node_ids,
            initial_activation=initial_activation
        )

        return result.activated_nodes

    async def detect_belief_contradictions(
        self,
        memory
    ) -> List[ContradictionPair]:
        """
        Detect contradictions between beliefs.

        Args:
            memory: BYRD Memory instance

        Returns:
            List of ContradictionPair objects
        """
        if self._is_cache_stale():
            await self.extract_graph_structure(memory)

        # Get all beliefs from memory
        async with memory.driver.session() as session:
            result = await session.run("""
                MATCH (b:Belief)
                WHERE b.id IS NOT NULL
                RETURN b.id as id, b.content as content, b.confidence as confidence
            """)
            records = await result.data()

        beliefs = [
            {
                'id': r['id'],
                'content': r['content'] or '',
                'confidence': r['confidence'] or 0.5
            }
            for r in records
        ]

        return self.algorithms.detect_contradictions_structural(
            beliefs,
            self._adjacency_cache
        )

    async def get_semantic_contradiction_candidates(
        self,
        memory,
        similarity_threshold: float = 0.7
    ) -> List[Tuple[str, str, float]]:
        """
        Get belief pairs that might semantically contradict.

        These pairs should be verified by LLM for actual contradiction.

        Args:
            memory: BYRD Memory instance
            similarity_threshold: Minimum similarity to flag

        Returns:
            List of (belief1_id, belief2_id, similarity) tuples
        """
        async with memory.driver.session() as session:
            result = await session.run("""
                MATCH (b:Belief)
                WHERE b.id IS NOT NULL AND b.confidence >= 0.6
                RETURN b.id as id, b.content as content, b.confidence as confidence
            """)
            records = await result.data()

        beliefs = [
            {
                'id': r['id'],
                'content': r['content'] or '',
                'confidence': r['confidence'] or 0.5
            }
            for r in records
        ]

        return self.algorithms.detect_contradictions_semantic(
            beliefs,
            similarity_threshold=similarity_threshold
        )

    async def perform_dream_walk(
        self,
        memory,
        start_node_id: str,
        steps: Optional[int] = None,
        quantum_delta: Optional[float] = None
    ) -> DreamWalkResult:
        """
        Perform a dream walk through the memory graph.

        Args:
            memory: BYRD Memory instance
            start_node_id: Starting node for walk
            steps: Number of walk steps
            quantum_delta: Quantum perturbation factor (from quantum_randomness)

        Returns:
            DreamWalkResult with walk path and metadata
        """
        if self._is_cache_stale():
            await self.extract_graph_structure(memory)

        return self.algorithms.dream_walk(
            self._adjacency_cache,
            self._node_weights_cache,
            self._node_types_cache,
            start_node_id,
            steps=steps,
            quantum_delta=quantum_delta
        )

    async def get_causal_chain(
        self,
        memory,
        start_node_id: str,
        direction: str = "forward"
    ) -> List[Tuple[str, str, str]]:
        """
        Trace causal relationships from a node.

        Args:
            memory: BYRD Memory instance
            start_node_id: Starting node
            direction: "forward" or "backward"

        Returns:
            List of (source, relationship, target) tuples
        """
        if self._is_cache_stale():
            await self.extract_graph_structure(memory)

        return self.algorithms.get_causal_chain(
            self._adjacency_typed_cache,
            start_node_id,
            direction=direction
        )

    async def get_important_memories(
        self,
        memory,
        limit: int = 20,
        personalization: Optional[Dict[str, float]] = None
    ) -> List[Tuple[str, float]]:
        """
        Get the most important memories by PageRank score.

        Args:
            memory: BYRD Memory instance
            limit: Maximum memories to return
            personalization: Optional preference weights

        Returns:
            List of (node_id, importance) tuples sorted by importance
        """
        scores = await self.get_pagerank_scores(memory, personalization)

        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_scores[:limit]
