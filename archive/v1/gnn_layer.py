"""
Graph Neural Network Layer for BYRD Memory - v2.0

Implements a trainable GNN that learns structural patterns from the memory graph.
Unlike v1 which only did random projections, this version actually trains using:
1. Link prediction (self-supervised from graph structure)
2. Usage feedback (reinforcement from Memory Reasoner)

EMERGENCE PRINCIPLE:
The GNN learns patterns from the graph structure itself - no prescribed
categories or hard-coded importance. Relationship strength emerges from
BYRD's actual connections and their utility.

VERIFIED CAPABILITY PRINCIPLE:
All calculations produce observable side effects in the graph. Salience scores,
relationship strengths, and training metrics are persisted as nodes, edges,
and properties, creating an audit trail that capabilities are actually being used.
This transforms computational operations into verifiable, observable phenomena.

Key improvements over v1:
- Actual training loop with link prediction loss
- Directed edge handling (DERIVED_FROM is directional)
- Edge weights used in attention computation
- Semantic initialization option (sentence-transformers)
- Neo4j 5.x compatible queries
- Learning from BYRD's behavior (usage feedback)
- Observable side effects for capability verification
"""

import numpy as np
from typing import Dict, List, Optional, Tuple, Set, Any
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import json


@dataclass
class GraphNode:
    """Represents a node in the memory graph."""
    id: str
    node_type: str  # Experience, Belief, Desire, Capability, Reflection
    content: str = ""
    properties: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[np.ndarray] = None


@dataclass
class GraphEdge:
    """Represents an edge/relationship in the memory graph."""
    source_id: str
    target_id: str
    relationship: str  # DERIVED_FROM, MOTIVATED, FULFILLS, etc.
    weight: float = 1.0
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TrainingResult:
    """Result of a training epoch."""
    epoch: int
    loss: float
    positive_accuracy: float
    negative_accuracy: float
    edges_trained: int


class StructuralLearner:
    """
    Trainable Graph Neural Network for learning structural patterns.

    Uses multi-head attention with message passing to learn node embeddings
    that capture the structural importance and connectivity patterns in
    BYRD's memory graph.

    Training signals:
    1. Link prediction: Predict whether edges exist (self-supervised)
    2. Usage feedback: Learn which retrievals were helpful (from Memory Reasoner)
    """

    # Relationships that are inherently directional
    DIRECTED_RELATIONSHIPS = {
        'DERIVED_FROM',   # Belief derived FROM Experience
        'MOTIVATED',      # Desire motivated BY Belief
        'FULFILLS',       # Action fulfills Desire
        'LED_TO',         # Experience led to Belief
        'CAUSED',         # Action caused Outcome
        'PROMOTED_TO',    # Node promoted to higher abstraction
    }

    # Relationships that are bidirectional
    BIDIRECTIONAL_RELATIONSHIPS = {
        'RELATED_TO',
        'SIMILAR_TO',
        'CONNECTED',
        'COOCCURS_WITH',
    }

    def __init__(
        self,
        embedding_dim: int = 64,
        num_heads: int = 4,
        num_layers: int = 2,
        learning_rate: float = 0.01,
        margin: float = 0.3,
        use_semantic_init: bool = True
    ):
        """
        Initialize the structural learner.

        Args:
            embedding_dim: Dimension of node embeddings
            num_heads: Number of attention heads
            num_layers: Number of GNN layers (message passing rounds)
            learning_rate: Learning rate for weight updates
            margin: Margin for ranking loss
            use_semantic_init: Use sentence-transformers for initialization if available
        """
        self.embedding_dim = embedding_dim
        self.num_heads = num_heads
        self.num_layers = num_layers
        self.learning_rate = learning_rate
        self.margin = margin
        self.use_semantic_init = use_semantic_init

        # Head dimension
        self.head_dim = embedding_dim // num_heads

        # Type vocabularies (expand as new types are seen)
        self.node_types: Dict[str, int] = {}
        self.relationship_types: Dict[str, int] = {}

        # Learnable parameters
        self.node_type_embeddings: Optional[np.ndarray] = None
        self.relation_embeddings: Optional[np.ndarray] = None
        self.attention_weights: List[Dict[str, np.ndarray]] = []
        self.transform_weights: List[Dict[str, np.ndarray]] = []
        self.edge_scorer: Optional[np.ndarray] = None  # For link prediction

        # Semantic encoder (lazy loaded)
        self._semantic_encoder = None
        self._semantic_available = None

        # Node embeddings cache
        self.node_embeddings: Dict[str, np.ndarray] = {}

        # Training state
        self.is_initialized = False
        self.epoch = 0
        self.training_history: List[TrainingResult] = []

        # Edge weight adjustments from usage feedback
        self.edge_weight_adjustments: Dict[Tuple[str, str], float] = {}

    def _ensure_semantic_encoder(self):
        """Lazy load semantic encoder."""
        if self._semantic_available is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._semantic_encoder = SentenceTransformer('all-MiniLM-L6-v2')
                self._semantic_available = True
                print("   Semantic encoder loaded for GNN initialization")
            except ImportError:
                self._semantic_available = False
                print("   No semantic encoder - using hash-based initialization")

    def _initialize_weights(self, num_node_types: int, num_relation_types: int):
        """Initialize all learnable parameters."""
        np.random.seed(42)

        # Xavier initialization scale
        scale = np.sqrt(2.0 / (self.embedding_dim + self.embedding_dim))

        # Node type embeddings
        self.node_type_embeddings = np.random.randn(
            max(num_node_types, 10), self.embedding_dim
        ) * scale

        # Relationship type embeddings
        self.relation_embeddings = np.random.randn(
            max(num_relation_types, 10), self.embedding_dim
        ) * scale

        # Multi-head attention weights for each layer
        self.attention_weights = []
        self.transform_weights = []

        for _ in range(self.num_layers):
            attn = {
                'Q': np.random.randn(self.num_heads, self.embedding_dim, self.head_dim) * scale,
                'K': np.random.randn(self.num_heads, self.embedding_dim, self.head_dim) * scale,
                'V': np.random.randn(self.num_heads, self.embedding_dim, self.head_dim) * scale,
                'O': np.random.randn(self.num_heads * self.head_dim, self.embedding_dim) * scale,
            }
            self.attention_weights.append(attn)

            transform = {
                'W1': np.random.randn(self.embedding_dim, self.embedding_dim * 2) * scale,
                'b1': np.zeros(self.embedding_dim * 2),
                'W2': np.random.randn(self.embedding_dim * 2, self.embedding_dim) * scale,
                'b2': np.zeros(self.embedding_dim),
            }
            self.transform_weights.append(transform)

        # Edge scoring layer for link prediction
        self.edge_scorer = np.random.randn(self.embedding_dim * 3, 1) * scale

        self.is_initialized = True

    def _get_or_create_type_id(self, type_name: str, type_dict: Dict[str, int]) -> int:
        """Get or create a numeric ID for a type string."""
        if type_name not in type_dict:
            type_dict[type_name] = len(type_dict)
        return type_dict[type_name]

    def _initialize_node_embedding(self, node: GraphNode) -> np.ndarray:
        """
        Create initial embedding for a node.

        Uses semantic content if available, falls back to hash-based.
        """
        # Try semantic initialization first
        if self.use_semantic_init and node.content:
            self._ensure_semantic_encoder()
            if self._semantic_available:
                try:
                    semantic_emb = self._semantic_encoder.encode(node.content[:512])
                    # Project to our embedding dimension if needed
                    if len(semantic_emb) != self.embedding_dim:
                        # Simple projection via hashing
                        proj = np.zeros(self.embedding_dim)
                        for i, v in enumerate(semantic_emb):
                            proj[i % self.embedding_dim] += v
                        return proj / (len(semantic_emb) / self.embedding_dim)
                    return semantic_emb
                except Exception:
                    pass

        # Fallback: type embedding + deterministic hash
        type_id = self._get_or_create_type_id(node.node_type, self.node_types)

        if self.node_type_embeddings is not None and type_id < len(self.node_type_embeddings):
            base = self.node_type_embeddings[type_id].copy()
        else:
            base = np.random.randn(self.embedding_dim) * 0.1

        # Add content-based signal (deterministic)
        content_hash = hash(node.content + node.id) % (2**31)
        np.random.seed(content_hash)
        content_signal = np.random.randn(self.embedding_dim) * 0.05

        return base + content_signal

    def _softmax(self, x: np.ndarray, axis: int = -1) -> np.ndarray:
        """Numerically stable softmax."""
        x_max = np.max(x, axis=axis, keepdims=True)
        exp_x = np.exp(x - x_max)
        return exp_x / (np.sum(exp_x, axis=axis, keepdims=True) + 1e-10)

    def _relu(self, x: np.ndarray) -> np.ndarray:
        """ReLU activation."""
        return np.maximum(0, x)

    def _sigmoid(self, x: np.ndarray) -> np.ndarray:
        """Sigmoid activation."""
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

    def _layer_norm(self, x: np.ndarray, eps: float = 1e-6) -> np.ndarray:
        """Layer normalization."""
        mean = np.mean(x, axis=-1, keepdims=True)
        std = np.std(x, axis=-1, keepdims=True)
        return (x - mean) / (std + eps)

    def _build_adjacency(
        self,
        edges: List[GraphEdge],
        node_ids: Set[str]
    ) -> Dict[str, List[Tuple[str, str, float]]]:
        """
        Build adjacency structure respecting edge directionality.

        Returns: {node_id: [(neighbor_id, relationship, weight), ...]}
        """
        neighbors: Dict[str, List[Tuple[str, str, float]]] = {nid: [] for nid in node_ids}

        for edge in edges:
            if edge.source_id not in node_ids or edge.target_id not in node_ids:
                continue

            # Get adjusted weight
            edge_key = (edge.source_id, edge.target_id)
            adjusted_weight = edge.weight * self.edge_weight_adjustments.get(edge_key, 1.0)

            # Always add in forward direction (source -> target means target receives from source)
            neighbors[edge.target_id].append((edge.source_id, edge.relationship, adjusted_weight))

            # Add reverse direction only for bidirectional relationships
            if edge.relationship in self.BIDIRECTIONAL_RELATIONSHIPS:
                reverse_key = (edge.target_id, edge.source_id)
                reverse_weight = edge.weight * self.edge_weight_adjustments.get(reverse_key, 1.0)
                neighbors[edge.source_id].append((edge.target_id, edge.relationship, reverse_weight))
            elif edge.relationship not in self.DIRECTED_RELATIONSHIPS:
                # Unknown relationship - treat as bidirectional by default
                reverse_key = (edge.target_id, edge.source_id)
                reverse_weight = edge.weight * self.edge_weight_adjustments.get(reverse_key, 1.0)
                neighbors[edge.source_id].append((edge.target_id, edge.relationship, reverse_weight))

        return neighbors

    def _attention_layer(
        self,
        node_embeddings: Dict[str, np.ndarray],
        neighbors: Dict[str, List[Tuple[str, str, float]]],
        layer_idx: int
    ) -> Dict[str, np.ndarray]:
        """
        Apply one layer of graph attention with edge weights.
        """
        if not self.attention_weights:
            return node_embeddings

        attn = self.attention_weights[layer_idx]
        transform = self.transform_weights[layer_idx]

        new_embeddings = {}

        for node_id, node_emb in node_embeddings.items():
            node_neighbors = neighbors.get(node_id, [])

            if not node_neighbors:
                # No neighbors - just apply layer norm
                new_embeddings[node_id] = self._layer_norm(node_emb)
                continue

            # Gather neighbor embeddings with relationship and weight info
            neighbor_data = []
            for neighbor_id, rel_type, edge_weight in node_neighbors:
                n_emb = node_embeddings.get(neighbor_id)
                if n_emb is not None:
                    # Add relationship type signal
                    rel_id = self._get_or_create_type_id(rel_type, self.relationship_types)
                    if self.relation_embeddings is not None and rel_id < len(self.relation_embeddings):
                        rel_emb = self.relation_embeddings[rel_id]
                        n_emb = n_emb + rel_emb * 0.1
                    neighbor_data.append((n_emb, edge_weight))

            if not neighbor_data:
                new_embeddings[node_id] = self._layer_norm(node_emb)
                continue

            neighbor_embs = np.stack([nd[0] for nd in neighbor_data])
            edge_weights = np.array([nd[1] for nd in neighbor_data])

            # Multi-head attention
            all_head_outputs = []
            for h in range(self.num_heads):
                Q = np.dot(node_emb, attn['Q'][h])
                K = np.dot(neighbor_embs, attn['K'][h])
                V = np.dot(neighbor_embs, attn['V'][h])

                # Attention scores with edge weights
                scores = np.dot(K, Q) / np.sqrt(self.head_dim)
                scores = scores * edge_weights  # Apply edge weights
                weights = self._softmax(scores)

                head_out = np.dot(weights, V)
                all_head_outputs.append(head_out)

            # Concatenate heads and project
            multi_head = np.concatenate(all_head_outputs)
            attended = np.dot(multi_head, attn['O'])

            # Residual + layer norm
            x = self._layer_norm(node_emb + attended)

            # Feed-forward
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
        if not nodes:
            return {}

        # Initialize weights if needed
        if not self.is_initialized:
            for node in nodes:
                self._get_or_create_type_id(node.node_type, self.node_types)
            for edge in edges:
                self._get_or_create_type_id(edge.relationship, self.relationship_types)

            self._initialize_weights(
                len(self.node_types),
                len(self.relationship_types)
            )

        # Initialize node embeddings
        embeddings = {}
        for node in nodes:
            if node.embedding is not None:
                embeddings[node.id] = node.embedding.copy()
            else:
                embeddings[node.id] = self._initialize_node_embedding(node)

        # Build adjacency with directionality
        node_ids = set(embeddings.keys())
        neighbors = self._build_adjacency(edges, node_ids)

        # Apply GNN layers
        for layer_idx in range(self.num_layers):
            embeddings = self._attention_layer(embeddings, neighbors, layer_idx)

        # Cache embeddings
        self.node_embeddings = embeddings

        return embeddings

    def _score_edge(
        self,
        source_emb: np.ndarray,
        target_emb: np.ndarray,
        relationship: str
    ) -> float:
        """
        Score the likelihood of an edge existing.

        Uses: concat(source, target, rel_emb) -> linear -> sigmoid
        """
        rel_id = self._get_or_create_type_id(relationship, self.relationship_types)

        if self.relation_embeddings is not None and rel_id < len(self.relation_embeddings):
            rel_emb = self.relation_embeddings[rel_id]
        else:
            rel_emb = np.zeros(self.embedding_dim)

        # Concatenate source, target, relationship
        combined = np.concatenate([source_emb, target_emb, rel_emb])

        # Score
        if self.edge_scorer is not None:
            score = np.dot(combined, self.edge_scorer).item()
            return self._sigmoid(np.array([score]))[0]

        # Fallback: cosine similarity
        return self.compute_relationship_strength(source_emb, target_emb)

    def _sample_negative_edges(
        self,
        nodes: List[GraphNode],
        positive_edges: Set[Tuple[str, str]],
        num_samples: int
    ) -> List[Tuple[str, str, str]]:
        """Sample negative edges (non-existing connections)."""
        node_ids = [n.id for n in nodes]
        if len(node_ids) < 2:
            return []

        negatives = []
        attempts = 0
        max_attempts = num_samples * 10

        while len(negatives) < num_samples and attempts < max_attempts:
            src_idx = np.random.randint(0, len(node_ids))
            tgt_idx = np.random.randint(0, len(node_ids))

            if src_idx != tgt_idx:
                src, tgt = node_ids[src_idx], node_ids[tgt_idx]
                if (src, tgt) not in positive_edges and (tgt, src) not in positive_edges:
                    # Random relationship type
                    rel_types = list(self.relationship_types.keys()) or ['RELATED_TO']
                    rel = np.random.choice(rel_types)
                    negatives.append((src, tgt, rel))

            attempts += 1

        return negatives

    def train_epoch(
        self,
        nodes: List[GraphNode],
        edges: List[GraphEdge],
        negative_ratio: int = 5
    ) -> TrainingResult:
        """
        Train one epoch using link prediction.

        Loss: Margin ranking loss between positive and negative edges.

        Args:
            nodes: Graph nodes
            edges: Graph edges (positive samples)
            negative_ratio: Number of negative samples per positive

        Returns:
            Training result with metrics
        """
        if not edges:
            return TrainingResult(self.epoch, 0.0, 0.0, 0.0, 0)

        # Compute embeddings
        embeddings = self.compute_embeddings(nodes, edges)

        # Positive edges
        positive_edges = {(e.source_id, e.target_id) for e in edges}

        # Sample negative edges
        num_negatives = len(edges) * negative_ratio
        negative_samples = self._sample_negative_edges(nodes, positive_edges, num_negatives)

        # Score positive edges
        pos_scores = []
        pos_correct = 0
        for edge in edges:
            if edge.source_id in embeddings and edge.target_id in embeddings:
                score = self._score_edge(
                    embeddings[edge.source_id],
                    embeddings[edge.target_id],
                    edge.relationship
                )
                pos_scores.append(score)
                if score > 0.5:
                    pos_correct += 1

        # Score negative edges
        neg_scores = []
        neg_correct = 0
        for src, tgt, rel in negative_samples:
            if src in embeddings and tgt in embeddings:
                score = self._score_edge(embeddings[src], embeddings[tgt], rel)
                neg_scores.append(score)
                if score < 0.5:
                    neg_correct += 1

        # Compute margin ranking loss
        loss = 0.0
        loss_count = 0
        for pos in pos_scores:
            for neg in neg_scores[:5]:  # Compare each positive with a few negatives
                margin_loss = max(0, self.margin - pos + neg)
                loss += margin_loss
                loss_count += 1

        if loss_count > 0:
            loss /= loss_count

        # Gradient update (simplified - adjust embeddings based on loss)
        if loss > 0:
            self._update_weights(pos_scores, neg_scores, edges, negative_samples, embeddings)

        self.epoch += 1

        result = TrainingResult(
            epoch=self.epoch,
            loss=loss,
            positive_accuracy=pos_correct / len(pos_scores) if pos_scores else 0,
            negative_accuracy=neg_correct / len(neg_scores) if neg_scores else 0,
            edges_trained=len(edges)
        )

        self.training_history.append(result)
        return result

    def _update_weights(
        self,
        pos_scores: List[float],
        neg_scores: List[float],
        pos_edges: List[GraphEdge],
        neg_edges: List[Tuple[str, str, str]],
        embeddings: Dict[str, np.ndarray]
    ):
        """
        Update weights based on link prediction loss.

        Simple gradient descent on the edge scorer and relation embeddings.
        """
        if self.edge_scorer is None or self.relation_embeddings is None:
            return

        # Gradient for edge scorer
        grad_scorer = np.zeros_like(self.edge_scorer)

        # Push positive scores higher
        for i, edge in enumerate(pos_edges):
            if i >= len(pos_scores):
                break
            if edge.source_id in embeddings and edge.target_id in embeddings:
                rel_id = self._get_or_create_type_id(edge.relationship, self.relationship_types)
                if rel_id < len(self.relation_embeddings):
                    combined = np.concatenate([
                        embeddings[edge.source_id],
                        embeddings[edge.target_id],
                        self.relation_embeddings[rel_id]
                    ])
                    # Positive gradient (increase score)
                    grad_scorer += combined.reshape(-1, 1) * (1 - pos_scores[i]) * 0.1

        # Push negative scores lower
        for i, (src, tgt, rel) in enumerate(neg_edges[:len(neg_scores)]):
            if i >= len(neg_scores):
                break
            if src in embeddings and tgt in embeddings:
                rel_id = self._get_or_create_type_id(rel, self.relationship_types)
                if rel_id < len(self.relation_embeddings):
                    combined = np.concatenate([
                        embeddings[src],
                        embeddings[tgt],
                        self.relation_embeddings[rel_id]
                    ])
                    # Negative gradient (decrease score)
                    grad_scorer -= combined.reshape(-1, 1) * neg_scores[i] * 0.1

        # Apply gradient with clipping
        grad_norm = np.linalg.norm(grad_scorer)
        if grad_norm > 1.0:
            grad_scorer = grad_scorer / grad_norm

        self.edge_scorer += self.learning_rate * grad_scorer

    def reinforce_from_usage(
        self,
        source_id: str,
        retrieved_id: str,
        was_helpful: bool,
        reinforcement_strength: float = 0.1
    ):
        """
        Learn from Memory Reasoner's actual usage.

        When a retrieved memory is helpful, strengthen that connection.
        When unhelpful, weaken it.

        Args:
            source_id: The query node ID
            retrieved_id: The retrieved node ID
            was_helpful: Whether the retrieval was helpful
            reinforcement_strength: How much to adjust (0.0 to 1.0)
        """
        edge_key = (source_id, retrieved_id)
        current = self.edge_weight_adjustments.get(edge_key, 1.0)

        if was_helpful:
            # Strengthen connection (multiplicative)
            self.edge_weight_adjustments[edge_key] = current * (1 + reinforcement_strength)
        else:
            # Weaken connection
            self.edge_weight_adjustments[edge_key] = current * (1 - reinforcement_strength * 0.5)

        # Clamp to reasonable range
        self.edge_weight_adjustments[edge_key] = np.clip(
            self.edge_weight_adjustments[edge_key], 0.1, 5.0
        )

    def compute_relationship_strength(
        self,
        emb1: np.ndarray,
        emb2: np.ndarray
    ) -> float:
        """Compute relationship strength via cosine similarity."""
        norm1 = np.linalg.norm(emb1)
        norm2 = np.linalg.norm(emb2)

        if norm1 < 1e-10 or norm2 < 1e-10:
            return 0.0

        similarity = np.dot(emb1, emb2) / (norm1 * norm2)
        return (similarity + 1) / 2  # Map [-1, 1] to [0, 1]

    def compute_node_salience(self, node_id: str) -> float:
        """
        Compute salience (importance) score for a node.

        Based on embedding magnitude and centrality.
        """
        if node_id not in self.node_embeddings:
            return 0.0

        node_emb = self.node_embeddings[node_id]

        # Magnitude component
        magnitude = np.linalg.norm(node_emb)
        max_magnitude = max(
            (np.linalg.norm(e) for e in self.node_embeddings.values()),
            default=1.0
        )
        magnitude_score = magnitude / (max_magnitude + 1e-10)

        # Centrality component
        if len(self.node_embeddings) > 1:
            similarities = [
                self.compute_relationship_strength(node_emb, other_emb)
                for other_id, other_emb in self.node_embeddings.items()
                if other_id != node_id
            ]
            centrality_score = np.mean(similarities) if similarities else 0.0
        else:
            centrality_score = 0.5

        return 0.4 * magnitude_score + 0.6 * centrality_score

    def get_most_related(
        self,
        node_id: str,
        top_k: int = 10
    ) -> List[Tuple[str, float]]:
        """Get the most related nodes to a given node."""
        if node_id not in self.node_embeddings:
            return []

        node_emb = self.node_embeddings[node_id]

        scores = [
            (other_id, self.compute_relationship_strength(node_emb, other_emb))
            for other_id, other_emb in self.node_embeddings.items()
            if other_id != node_id
        ]

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

    def should_train(self) -> bool:
        """Check if we have enough data to train."""
        return len(self.node_embeddings) >= 10

    def save_state(self, filepath: str):
        """Save the GNN state to a file."""
        state = {
            'embedding_dim': self.embedding_dim,
            'num_heads': self.num_heads,
            'num_layers': self.num_layers,
            'learning_rate': self.learning_rate,
            'margin': self.margin,
            'node_types': self.node_types,
            'relationship_types': self.relationship_types,
            'epoch': self.epoch,
            'is_initialized': self.is_initialized,
            'edge_weight_adjustments': {
                f"{k[0]}|{k[1]}": v
                for k, v in self.edge_weight_adjustments.items()
            },
        }

        if self.node_type_embeddings is not None:
            state['node_type_embeddings'] = self.node_type_embeddings.tolist()
        if self.relation_embeddings is not None:
            state['relation_embeddings'] = self.relation_embeddings.tolist()
        if self.edge_scorer is not None:
            state['edge_scorer'] = self.edge_scorer.tolist()

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

        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
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
            self.learning_rate = state.get('learning_rate', 0.01)
            self.margin = state.get('margin', 0.3)
            self.node_types = state['node_types']
            self.relationship_types = state['relationship_types']
            self.epoch = state.get('epoch', 0)
            self.is_initialized = state.get('is_initialized', False)
            self.head_dim = self.embedding_dim // self.num_heads

            # Load edge weight adjustments
            self.edge_weight_adjustments = {}
            for key, val in state.get('edge_weight_adjustments', {}).items():
                parts = key.split('|')
                if len(parts) == 2:
                    self.edge_weight_adjustments[(parts[0], parts[1])] = val

            if state.get('node_type_embeddings'):
                self.node_type_embeddings = np.array(state['node_type_embeddings'])
            if state.get('relation_embeddings'):
                self.relation_embeddings = np.array(state['relation_embeddings'])
            if state.get('edge_scorer'):
                self.edge_scorer = np.array(state['edge_scorer'])

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
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(f"Could not load GNN state: {e}")
            return False


class MemoryGNNIntegration:
    """
    Integration layer between StructuralLearner and BYRD's Memory system.

    Extracts graph structure from Neo4j, computes GNN embeddings,
    and provides enhanced retrieval methods with observable side effects.

    VERIFIED CAPABILITY PRINCIPLE:
    All calculations are persisted to the graph as observable side effects,
    creating an audit trail of computational activity and enabling verification.
    """

    def __init__(
        self,
        gnn: Optional[StructuralLearner] = None,
        state_path: str = "./data/gnn_state.json"
    ):
        """
        Initialize the memory-GNN integration.

        Args:
            gnn: Optional pre-configured GNN layer
            state_path: Path to save/load GNN state
        """
        self.gnn = gnn or StructuralLearner()
        self.state_path = state_path

        # Try to load existing state
        self.gnn.load_state(state_path)

        # Cache
        self._nodes_cache: List[GraphNode] = []
        self._edges_cache: List[GraphEdge] = []
        self._last_update: Optional[datetime] = None
        self._cache_ttl_seconds: int = 300  # 5 minutes, configurable

        # Write tracking for verification
        self._calculation_writes: Dict[str, int] = {}

    async def extract_graph_from_memory(self, memory) -> Tuple[List[GraphNode], List[GraphEdge]]:
        """
        Extract graph structure from Neo4j memory.

        Uses Neo4j 5.x compatible queries.
        """
        nodes = []
        edges = []

        try:
            # Extract all nodes (Neo4j 5.x syntax)
            node_result = await memory._run_query("""
                MATCH (n)
                WHERE n.content IS NOT NULL OR n.description IS NOT NULL
                RETURN n, labels(n)[0] as node_type, elementId(n) as neo_id
                LIMIT 1000
            """)

            for record in (node_result or []):
                node_data = dict(record['n'])
                node_type = record['node_type']
                neo_id = record['neo_id']

                node_id = node_data.get('id', neo_id)
                content = node_data.get('content', node_data.get('description', ''))

                nodes.append(GraphNode(
                    id=str(node_id),
                    node_type=node_type or 'Unknown',
                    content=str(content)[:1000],
                    properties={k: v for k, v in node_data.items()
                               if k not in ['content', 'description', 'embedding']}
                ))

            # Extract all relationships
            edge_result = await memory._run_query("""
                MATCH (a)-[r]->(b)
                WHERE a.id IS NOT NULL AND b.id IS NOT NULL
                RETURN a.id as source, b.id as target, type(r) as rel_type,
                       r.weight as weight
                LIMIT 5000
            """)

            for record in (edge_result or []):
                if record['source'] and record['target']:
                    edges.append(GraphEdge(
                        source_id=str(record['source']),
                        target_id=str(record['target']),
                        relationship=record['rel_type'],
                        weight=record.get('weight') or 1.0
                    ))

            self._nodes_cache = nodes
            self._edges_cache = edges
            self._last_update = datetime.now()

        except Exception as e:
            print(f"Error extracting graph: {e}")

        return nodes, edges

    def _is_cache_stale(self) -> bool:
        """Check if cache needs refresh."""
        if self._last_update is None:
            return True
        elapsed = (datetime.now() - self._last_update).total_seconds()
        return elapsed > self._cache_ttl_seconds

    async def update_embeddings(self, memory) -> Dict[str, np.ndarray]:
        """Update GNN embeddings from current memory state."""
        nodes, edges = await self.extract_graph_from_memory(memory)

        if not nodes:
            return {}

        embeddings = self.gnn.compute_embeddings(nodes, edges)

        # Periodic save
        if self.gnn.epoch % 10 == 0:
            self.gnn.save_state(self.state_path)

        return embeddings

    async def train_on_memory(
        self,
        memory,
        write_to_graph: bool = True
    ) -> Optional[TrainingResult]:
        """
        Train the GNN on current memory graph.

        Call this during DREAMING mode.

        Args:
            memory: Memory system with Neo4j driver
            write_to_graph: If True, persist training metrics as observable side effects

        Returns:
            TrainingResult with epoch metrics, or None if training cannot run
        """
        if self._is_cache_stale():
            await self.update_embeddings(memory)

        if not self._nodes_cache or not self._edges_cache:
            return None

        result = self.gnn.train_epoch(self._nodes_cache, self._edges_cache)

        # Save after training
        self.gnn.save_state(self.state_path)

        print(f"   GNN training epoch {result.epoch}: loss={result.loss:.4f}, "
              f"pos_acc={result.positive_accuracy:.2%}, neg_acc={result.negative_accuracy:.2%}")

        # Write to graph for verification (observable side effect)
        if write_to_graph:
            await self.write_training_metrics_to_graph(memory, result)

        return result

    async def get_enhanced_salience(
        self,
        memory,
        node_ids: List[str],
        write_to_graph: bool = True
    ) -> Dict[str, float]:
        """
        Get GNN-enhanced salience scores for nodes.

        Args:
            memory: Memory system with Neo4j driver
            node_ids: List of node IDs to compute salience for
            write_to_graph: If True, persist results as observable side effects

        Returns:
            Dict mapping node_id to salience score
        """
        if self._is_cache_stale():
            await self.update_embeddings(memory)

        salience_scores = {
            node_id: self.gnn.compute_node_salience(node_id)
            for node_id in node_ids
        }

        # Write to graph for verification (observable side effect)
        if write_to_graph:
            await self.write_salience_to_graph(memory, node_ids, salience_scores)

        return salience_scores

    async def get_related_memories(
        self,
        memory,
        source_id: str,
        top_k: int = 10,
        write_to_graph: bool = True
    ) -> List[Tuple[str, float]]:
        """
        Get memories most related to a source node using GNN embeddings.

        Args:
            memory: Memory system with Neo4j driver
            source_id: ID of source node
            top_k: Number of related nodes to return
            write_to_graph: If True, persist results as observable side effects

        Returns:
            List of (node_id, similarity_score) tuples
        """
        if self._is_cache_stale():
            await self.update_embeddings(memory)

        related = self.gnn.get_most_related(source_id, top_k)

        # Write to graph for verification (observable side effect)
        if write_to_graph and related:
            await self.write_related_nodes_to_graph(memory, source_id, related)

        return related

    async def record_retrieval_feedback(
        self,
        source_id: str,
        retrieved_ids: List[str],
        helpful_ids: Set[str]
    ):
        """
        Record feedback about which retrievals were helpful.

        This trains the GNN to improve future retrievals.
        """
        for ret_id in retrieved_ids:
            was_helpful = ret_id in helpful_ids
            self.gnn.reinforce_from_usage(source_id, ret_id, was_helpful)

        # Save updated weights
        self.gnn.save_state(self.state_path)

    async def write_salience_to_graph(
        self,
        memory,
        node_ids: List[str],
        salience_scores: Dict[str, float]
    ) -> int:
        """
        Write salience scores to graph as observable side effect.

        This creates a verifiable record of salience calculations,
        enabling audit trails and capability verification.
        """
        writes = 0
        timestamp = datetime.now().isoformat()

        try:
            async with memory.driver.session() as session:
                for node_id, salience in salience_scores.items():
                    if node_id not in node_ids:
                        continue

                    # Write salience as node property (observable side effect)
                    await session.run("""
                        MATCH (n {id: $node_id})
                        SET n.gnn_salience = $salience,
                            n.gnn_salience_updated = $timestamp
                    """, {
                        'node_id': node_id,
                        'salience': round(salience, 6),
                        'timestamp': timestamp
                    })
                    writes += 1

                # Track calculation for verification
                calculation_id = f"salience_{timestamp.replace(':', '-')}"
                self._calculation_writes[calculation_id] = writes

                print(f"   ✅ Wrote {writes} salience scores to graph")

        except Exception as e:
            print(f"   ❌ Error writing salience to graph: {e}")

        return writes

    async def write_related_nodes_to_graph(
        self,
        memory,
        source_id: str,
        related: List[Tuple[str, float]]
    ) -> int:
        """
        Write relationship strengths to graph as observable side effect.

        Creates edges with computed strengths, making GNN calculations
        visible and verifiable in the graph structure.
        """
        writes = 0
        timestamp = datetime.now().isoformat()

        try:
            async with memory.driver.session() as session:
                for related_id, strength in related:
                    # Create relationship edge with computed strength
                    await session.run("""
                        MATCH (source {id: $source_id})
                        MATCH (target {id: $target_id})
                        MERGE (source)-[r:GNN_RELATED]->(target)
                        SET r.strength = $strength,
                            r.computed_at = $timestamp,
                            r.embedding_similarity = round($strength, 6)
                    """, {
                        'source_id': source_id,
                        'target_id': related_id,
                        'strength': round(strength, 6),
                        'timestamp': timestamp
                    })
                    writes += 1

                # Track calculation for verification
                calculation_id = f"related_{source_id}_{timestamp.replace(':', '-')}"
                self._calculation_writes[calculation_id] = writes

                print(f"   ✅ Wrote {writes} relationship strengths to graph")

        except Exception as e:
            print(f"   ❌ Error writing relationships to graph: {e}")

        return writes

    async def write_training_metrics_to_graph(
        self,
        memory,
        result: TrainingResult
    ) -> bool:
        """
        Write training metrics to graph as observable side effect.

        Creates a permanent record of GNN training activity,
        enabling capability verification and audit trails.
        """
        timestamp = datetime.now().isoformat()

        try:
            async with memory.driver.session() as session:
                # Create training epoch node
                await session.run("""
                    MERGE (t:GNNTraining {epoch: $epoch})
                    SET t.loss = $loss,
                        t.positive_accuracy = $pos_acc,
                        t.negative_accuracy = $neg_acc,
                        t.edges_trained = $edges,
                        t.timestamp = $timestamp
                """, {
                    'epoch': result.epoch,
                    'loss': round(result.loss, 6),
                    'pos_acc': round(result.positive_accuracy, 6),
                    'neg_acc': round(result.negative_accuracy, 6),
                    'edges': result.edges_trained,
                    'timestamp': timestamp
                })

                # Track calculation for verification
                calculation_id = f"training_epoch_{result.epoch}"
                self._calculation_writes[calculation_id] = 1

                print(f"   ✅ Wrote training epoch {result.epoch} metrics to graph")
                return True

        except Exception as e:
            print(f"   ❌ Error writing training metrics to graph: {e}")
            return False

    def get_verification_stats(self) -> Dict[str, Any]:
        """
        Get statistics about calculation writes for verification.

        Returns information about observable side effects created,
        enabling verification that capabilities are actually being used.
        """
        total_writes = sum(self._calculation_writes.values())
        calculation_types = {
            'salience': sum(v for k, v in self._calculation_writes.items() if k.startswith('salience')),
            'related': sum(v for k, v in self._calculation_writes.items() if k.startswith('related')),
            'training': sum(v for k, v in self._calculation_writes.items() if k.startswith('training'))
        }

        return {
            'total_writes': total_writes,
            'calculation_count': len(self._calculation_writes),
            'by_type': calculation_types,
            'recent_calculations': list(self._calculation_writes.keys())[-10:]
        }
