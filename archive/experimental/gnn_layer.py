"""
Graph Neural Network Layer for BYRD Memory

Implements a lightweight GNN to improve relationship strength between nodes
in the memory graph. Uses message passing to learn node embeddings that
capture structural patterns in the belief/memory network.

EMERGENCE PRINCIPLE:
The GNN learns patterns from the graph structure itself - no prescribed
categories or hard-coded importance. Relationship strength emerges from
the actual connections BYRD has made.

Architecture:
- Graph Attention mechanism for weighted message aggregation
- Node type embeddings for heterogeneous graph handling
- Relationship strength prediction from learned embeddings
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
import json
import hashlib
from datetime import datetime


@dataclass
class GraphNode:
    """Represents a node in the memory graph."""
    id: str
    node_type: str  # Experience, Belief, Desire, Capability, Reflection
    properties: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[np.ndarray] = None


@dataclass
class GraphEdge:
    """Represents an edge/relationship in the memory graph."""
    source_id: str
    target_id: str
    relationship: str  # DERIVED_FROM, MOTIVATED, FULFILLS, etc.
    properties: Dict[str, Any] = field(default_factory=dict)
    weight: float = 1.0


class GraphNeuralLayer:
    """
    Lightweight Graph Neural Network layer for memory relationship learning.

    Uses attention-based message passing to compute node embeddings that
    capture the structural importance and connectivity patterns.

    The learned embeddings can be used to:
    1. Score relationship strength between nodes
    2. Find semantically similar memories
    3. Identify important/central nodes (high salience)
    4. Predict potential connections
    """

    def __init__(
        self,
        embedding_dim: int = 64,
        num_heads: int = 4,
        num_layers: int = 2,
        dropout: float = 0.1,
        learning_rate: float = 0.01
    ):
        """
        Initialize the GNN layer.

        Args:
            embedding_dim: Dimension of node embeddings
            num_heads: Number of attention heads
            num_layers: Number of GNN layers (message passing rounds)
            dropout: Dropout rate for regularization
            learning_rate: Learning rate for weight updates
        """
        self.embedding_dim = embedding_dim
        self.num_heads = num_heads
        self.num_layers = num_layers
        self.dropout = dropout
        self.learning_rate = learning_rate

        # Node type vocabulary (will expand as new types are seen)
        self.node_types: Dict[str, int] = {}
        self.relationship_types: Dict[str, int] = {}

        # Learnable parameters (initialized lazily)
        self.node_type_embeddings: Optional[np.ndarray] = None
        self.relation_embeddings: Optional[np.ndarray] = None
        self.attention_weights: List[np.ndarray] = []
        self.transform_weights: List[np.ndarray] = []

        # Node embeddings cache
        self.node_embeddings: Dict[str, np.ndarray] = {}

        # Training state
        self.is_initialized = False
        self.epoch = 0

    def _initialize_weights(self, num_node_types: int, num_relation_types: int):
        """Initialize learnable parameters."""
        np.random.seed(42)  # For reproducibility

        # Node type embeddings
        self.node_type_embeddings = np.random.randn(
            num_node_types, self.embedding_dim
        ) * 0.1

        # Relationship type embeddings
        self.relation_embeddings = np.random.randn(
            num_relation_types, self.embedding_dim
        ) * 0.1

        # Multi-head attention weights for each layer
        head_dim = self.embedding_dim // self.num_heads
        self.attention_weights = []
        self.transform_weights = []

        for _ in range(self.num_layers):
            # Q, K, V projections for attention
            attn = {
                'Q': np.random.randn(self.num_heads, self.embedding_dim, head_dim) * 0.1,
                'K': np.random.randn(self.num_heads, self.embedding_dim, head_dim) * 0.1,
                'V': np.random.randn(self.num_heads, self.embedding_dim, head_dim) * 0.1,
                'O': np.random.randn(self.num_heads * head_dim, self.embedding_dim) * 0.1,
            }
            self.attention_weights.append(attn)

            # Feed-forward transformation
            transform = {
                'W1': np.random.randn(self.embedding_dim, self.embedding_dim * 2) * 0.1,
                'b1': np.zeros(self.embedding_dim * 2),
                'W2': np.random.randn(self.embedding_dim * 2, self.embedding_dim) * 0.1,
                'b2': np.zeros(self.embedding_dim),
            }
            self.transform_weights.append(transform)

        self.is_initialized = True

    def _get_or_create_type_id(
        self,
        type_name: str,
        type_dict: Dict[str, int]
    ) -> int:
        """Get or create a numeric ID for a type string."""
        if type_name not in type_dict:
            type_dict[type_name] = len(type_dict)
        return type_dict[type_name]

    def _initialize_node_embedding(self, node: GraphNode) -> np.ndarray:
        """
        Create initial embedding for a node based on its type and properties.

        EMERGENCE PRINCIPLE:
        Initial embeddings are based on structure (node type, property hash)
        not semantic content. The GNN will learn meaningful representations.
        """
        type_id = self._get_or_create_type_id(node.node_type, self.node_types)

        # Start with type embedding
        if self.node_type_embeddings is not None and type_id < len(self.node_type_embeddings):
            base = self.node_type_embeddings[type_id].copy()
        else:
            base = np.random.randn(self.embedding_dim) * 0.1

        # Add property-based signal (deterministic from properties)
        prop_str = json.dumps(node.properties, sort_keys=True, default=str)
        prop_hash = int(hashlib.md5(prop_str.encode()).hexdigest()[:8], 16)
        np.random.seed(prop_hash)
        prop_signal = np.random.randn(self.embedding_dim) * 0.05

        return base + prop_signal

    def _softmax(self, x: np.ndarray, axis: int = -1) -> np.ndarray:
        """Numerically stable softmax."""
        x_max = np.max(x, axis=axis, keepdims=True)
        exp_x = np.exp(x - x_max)
        return exp_x / (np.sum(exp_x, axis=axis, keepdims=True) + 1e-10)

    def _relu(self, x: np.ndarray) -> np.ndarray:
        """ReLU activation."""
        return np.maximum(0, x)

    def _layer_norm(self, x: np.ndarray, eps: float = 1e-6) -> np.ndarray:
        """Layer normalization."""
        mean = np.mean(x, axis=-1, keepdims=True)
        std = np.std(x, axis=-1, keepdims=True)
        return (x - mean) / (std + eps)

    def _attention_layer(
        self,
        node_embeddings: Dict[str, np.ndarray],
        edges: List[GraphEdge],
        layer_idx: int
    ) -> Dict[str, np.ndarray]:
        """
        Apply one layer of graph attention.

        For each node, aggregate messages from neighbors using attention
        weights learned from the embeddings.
        """
        if not self.attention_weights:
            return node_embeddings

        attn = self.attention_weights[layer_idx]
        transform = self.transform_weights[layer_idx]
        head_dim = self.embedding_dim // self.num_heads

        # Build adjacency structure
        neighbors: Dict[str, List[Tuple[str, str]]] = {nid: [] for nid in node_embeddings}
        for edge in edges:
            if edge.source_id in neighbors and edge.target_id in node_embeddings:
                neighbors[edge.target_id].append((edge.source_id, edge.relationship))
            if edge.target_id in neighbors and edge.source_id in node_embeddings:
                neighbors[edge.source_id].append((edge.target_id, edge.relationship))

        new_embeddings = {}

        for node_id, node_emb in node_embeddings.items():
            node_neighbors = neighbors.get(node_id, [])

            if not node_neighbors:
                # No neighbors - apply self-attention only
                new_embeddings[node_id] = self._layer_norm(node_emb)
                continue

            # Gather neighbor embeddings
            neighbor_embs = []
            for neighbor_id, rel_type in node_neighbors:
                n_emb = node_embeddings.get(neighbor_id)
                if n_emb is not None:
                    # Add relationship type signal
                    rel_id = self._get_or_create_type_id(rel_type, self.relationship_types)
                    if self.relation_embeddings is not None and rel_id < len(self.relation_embeddings):
                        rel_emb = self.relation_embeddings[rel_id]
                        n_emb = n_emb + rel_emb * 0.1
                    neighbor_embs.append(n_emb)

            if not neighbor_embs:
                new_embeddings[node_id] = self._layer_norm(node_emb)
                continue

            neighbor_stack = np.stack(neighbor_embs)  # [num_neighbors, embedding_dim]

            # Multi-head attention
            all_head_outputs = []
            for h in range(self.num_heads):
                # Project to Q, K, V
                Q = np.dot(node_emb, attn['Q'][h])  # [head_dim]
                K = np.dot(neighbor_stack, attn['K'][h])  # [num_neighbors, head_dim]
                V = np.dot(neighbor_stack, attn['V'][h])  # [num_neighbors, head_dim]

                # Attention scores
                scores = np.dot(K, Q) / np.sqrt(head_dim)  # [num_neighbors]
                weights = self._softmax(scores)

                # Weighted aggregation
                head_out = np.dot(weights, V)  # [head_dim]
                all_head_outputs.append(head_out)

            # Concatenate heads and project
            multi_head = np.concatenate(all_head_outputs)  # [num_heads * head_dim]
            attended = np.dot(multi_head, attn['O'])  # [embedding_dim]

            # Residual connection + layer norm
            x = self._layer_norm(node_emb + attended)

            # Feed-forward network
            ff = self._relu(np.dot(x, transform['W1']) + transform['b1'])
            ff = np.dot(ff, transform['W2']) + transform['b2']

            # Second residual + layer norm
            new_embeddings[node_id] = self._layer_norm(x + ff)

        return new_embeddings

    def compute_embeddings(
        self,
        nodes: List[GraphNode],
        edges: List[GraphEdge]
    ) -> Dict[str, np.ndarray]:
        """
        Compute node embeddings using message passing.

        Args:
            nodes: List of graph nodes
            edges: List of graph edges

        Returns:
            Dictionary mapping node IDs to their embeddings
        """
        # Initialize weights if needed
        if not self.is_initialized:
            # Collect all types first
            for node in nodes:
                self._get_or_create_type_id(node.node_type, self.node_types)
            for edge in edges:
                self._get_or_create_type_id(edge.relationship, self.relationship_types)

            self._initialize_weights(
                max(len(self.node_types), 1),
                max(len(self.relationship_types), 1)
            )

        # Initialize node embeddings
        embeddings = {}
        for node in nodes:
            if node.embedding is not None:
                embeddings[node.id] = node.embedding
            else:
                embeddings[node.id] = self._initialize_node_embedding(node)

        # Apply GNN layers (message passing)
        for layer_idx in range(self.num_layers):
            embeddings = self._attention_layer(embeddings, edges, layer_idx)

        # Cache embeddings
        self.node_embeddings = embeddings

        return embeddings

    def compute_relationship_strength(
        self,
        node1_id: str,
        node2_id: str,
        embeddings: Optional[Dict[str, np.ndarray]] = None
    ) -> float:
        """
        Compute relationship strength between two nodes.

        Uses cosine similarity of learned embeddings as the relationship
        strength measure. Higher values indicate stronger relationships.

        Args:
            node1_id: ID of first node
            node2_id: ID of second node
            embeddings: Optional pre-computed embeddings (uses cache if None)

        Returns:
            Relationship strength score in range [0, 1]
        """
        embs = embeddings or self.node_embeddings

        if node1_id not in embs or node2_id not in embs:
            return 0.0

        emb1 = embs[node1_id]
        emb2 = embs[node2_id]

        # Cosine similarity
        norm1 = np.linalg.norm(emb1)
        norm2 = np.linalg.norm(emb2)

        if norm1 < 1e-10 or norm2 < 1e-10:
            return 0.0

        similarity = np.dot(emb1, emb2) / (norm1 * norm2)

        # Map from [-1, 1] to [0, 1]
        return (similarity + 1) / 2

    def compute_node_salience(
        self,
        node_id: str,
        embeddings: Optional[Dict[str, np.ndarray]] = None
    ) -> float:
        """
        Compute salience (importance) score for a node.

        Salience is based on:
        1. Embedding magnitude (nodes with stronger signal)
        2. Average similarity to other nodes (central nodes)

        Args:
            node_id: ID of the node
            embeddings: Optional pre-computed embeddings

        Returns:
            Salience score in range [0, 1]
        """
        embs = embeddings or self.node_embeddings

        if node_id not in embs:
            return 0.0

        node_emb = embs[node_id]

        # Magnitude component (normalized)
        magnitude = np.linalg.norm(node_emb)
        max_magnitude = max(np.linalg.norm(e) for e in embs.values()) if embs else 1.0
        magnitude_score = magnitude / (max_magnitude + 1e-10)

        # Centrality component (average similarity to others)
        if len(embs) > 1:
            similarities = []
            for other_id, other_emb in embs.items():
                if other_id != node_id:
                    sim = self.compute_relationship_strength(node_id, other_id, embs)
                    similarities.append(sim)
            centrality_score = np.mean(similarities) if similarities else 0.0
        else:
            centrality_score = 0.5

        # Combined score
        return 0.4 * magnitude_score + 0.6 * centrality_score

    def get_most_related(
        self,
        node_id: str,
        top_k: int = 10,
        embeddings: Optional[Dict[str, np.ndarray]] = None
    ) -> List[Tuple[str, float]]:
        """
        Get the most related nodes to a given node.

        Args:
            node_id: ID of the source node
            top_k: Number of related nodes to return
            embeddings: Optional pre-computed embeddings

        Returns:
            List of (node_id, strength) tuples sorted by strength
        """
        embs = embeddings or self.node_embeddings

        if node_id not in embs:
            return []

        scores = []
        for other_id in embs:
            if other_id != node_id:
                strength = self.compute_relationship_strength(node_id, other_id, embs)
                scores.append((other_id, strength))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    def save_state(self, filepath: str):
        """Save the GNN state to a file."""
        state = {
            'embedding_dim': self.embedding_dim,
            'num_heads': self.num_heads,
            'num_layers': self.num_layers,
            'node_types': self.node_types,
            'relationship_types': self.relationship_types,
            'node_type_embeddings': self.node_type_embeddings.tolist() if self.node_type_embeddings is not None else None,
            'relation_embeddings': self.relation_embeddings.tolist() if self.relation_embeddings is not None else None,
            'epoch': self.epoch,
            'is_initialized': self.is_initialized,
        }

        # Save attention and transform weights
        if self.attention_weights:
            state['attention_weights'] = [
                {k: v.tolist() for k, v in layer.items()}
                for layer in self.attention_weights
            ]
        if self.transform_weights:
            state['transform_weights'] = [
                {k: v.tolist() for k, v in layer.items()}
                for layer in self.transform_weights
            ]

        with open(filepath, 'w') as f:
            json.dump(state, f)

    def load_state(self, filepath: str) -> bool:
        """Load the GNN state from a file."""
        try:
            with open(filepath, 'r') as f:
                state = json.load(f)

            self.embedding_dim = state['embedding_dim']
            self.num_heads = state['num_heads']
            self.num_layers = state['num_layers']
            self.node_types = state['node_types']
            self.relationship_types = state['relationship_types']
            self.epoch = state.get('epoch', 0)
            self.is_initialized = state.get('is_initialized', False)

            if state.get('node_type_embeddings'):
                self.node_type_embeddings = np.array(state['node_type_embeddings'])
            if state.get('relation_embeddings'):
                self.relation_embeddings = np.array(state['relation_embeddings'])

            if state.get('attention_weights'):
                self.attention_weights = [
                    {k: np.array(v) for k, v in layer.items()}
                    for layer in state['attention_weights']
                ]
            if state.get('transform_weights'):
                self.transform_weights = [
                    {k: np.array(v) for k, v in layer.items()}
                    for layer in state['transform_weights']
                ]

            return True
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            return False


class MemoryGNNIntegration:
    """
    Integration layer between GNN and BYRD's Memory system.

    Extracts graph structure from Neo4j, computes GNN embeddings,
    and provides enhanced retrieval methods.
    """

    def __init__(
        self,
        gnn: Optional[GraphNeuralLayer] = None,
        state_path: str = "./gnn_state.json"
    ):
        """
        Initialize the memory-GNN integration.

        Args:
            gnn: Optional pre-configured GNN layer
            state_path: Path to save/load GNN state
        """
        self.gnn = gnn or GraphNeuralLayer()
        self.state_path = state_path

        # Try to load existing state
        self.gnn.load_state(state_path)

        # Cache for graph extraction
        self._nodes_cache: List[GraphNode] = []
        self._edges_cache: List[GraphEdge] = []
        self._last_update: Optional[datetime] = None

    async def extract_graph_from_memory(self, memory) -> Tuple[List[GraphNode], List[GraphEdge]]:
        """
        Extract graph structure from Neo4j memory.

        Args:
            memory: BYRD Memory instance

        Returns:
            Tuple of (nodes, edges)
        """
        nodes = []
        edges = []

        async with memory.driver.session() as session:
            # Extract all nodes
            node_result = await session.run("""
                MATCH (n)
                RETURN n, labels(n)[0] as node_type, id(n) as neo_id
            """)
            node_records = await node_result.data()

            for record in node_records:
                node_data = record['n']
                node_type = record['node_type']

                # Use our ID if available, otherwise use Neo4j ID
                node_id = node_data.get('id', str(record['neo_id']))

                nodes.append(GraphNode(
                    id=node_id,
                    node_type=node_type,
                    properties={k: v for k, v in node_data.items() if k != 'embedding'}
                ))

            # Extract all relationships
            edge_result = await session.run("""
                MATCH (a)-[r]->(b)
                RETURN a.id as source, b.id as target, type(r) as rel_type, properties(r) as props
            """)
            edge_records = await edge_result.data()

            for record in edge_records:
                if record['source'] and record['target']:
                    edges.append(GraphEdge(
                        source_id=record['source'],
                        target_id=record['target'],
                        relationship=record['rel_type'],
                        properties=record['props'] or {}
                    ))

        self._nodes_cache = nodes
        self._edges_cache = edges
        self._last_update = datetime.now()

        return nodes, edges

    async def update_embeddings(self, memory) -> Dict[str, np.ndarray]:
        """
        Update GNN embeddings from current memory state.

        Args:
            memory: BYRD Memory instance

        Returns:
            Dictionary of node embeddings
        """
        nodes, edges = await self.extract_graph_from_memory(memory)

        if not nodes:
            return {}

        embeddings = self.gnn.compute_embeddings(nodes, edges)

        # Save state periodically
        self.gnn.save_state(self.state_path)

        return embeddings

    async def get_enhanced_salience(
        self,
        memory,
        node_ids: List[str]
    ) -> Dict[str, float]:
        """
        Get GNN-enhanced salience scores for nodes.

        Args:
            memory: BYRD Memory instance
            node_ids: List of node IDs to score

        Returns:
            Dictionary mapping node IDs to salience scores
        """
        # Update embeddings if cache is stale (older than 5 minutes)
        if (self._last_update is None or
            (datetime.now() - self._last_update).seconds > 300):
            await self.update_embeddings(memory)

        scores = {}
        for node_id in node_ids:
            scores[node_id] = self.gnn.compute_node_salience(node_id)

        return scores

    async def get_related_memories(
        self,
        memory,
        source_id: str,
        top_k: int = 10
    ) -> List[Tuple[str, float]]:
        """
        Get memories most related to a source node using GNN embeddings.

        Args:
            memory: BYRD Memory instance
            source_id: Source node ID
            top_k: Number of related nodes to return

        Returns:
            List of (node_id, relationship_strength) tuples
        """
        # Update embeddings if needed
        if (self._last_update is None or
            (datetime.now() - self._last_update).seconds > 300):
            await self.update_embeddings(memory)

        return self.gnn.get_most_related(source_id, top_k)

    async def compute_belief_memory_strength(
        self,
        memory,
        belief_id: str,
        experience_id: str
    ) -> float:
        """
        Compute relationship strength between a belief and an experience.

        Useful for determining how strongly a belief is supported by
        a particular experience.

        Args:
            memory: BYRD Memory instance
            belief_id: Belief node ID
            experience_id: Experience node ID

        Returns:
            Relationship strength in range [0, 1]
        """
        # Update embeddings if needed
        if (self._last_update is None or
            (datetime.now() - self._last_update).seconds > 300):
            await self.update_embeddings(memory)

        return self.gnn.compute_relationship_strength(belief_id, experience_id)
