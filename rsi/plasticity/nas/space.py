"""
Architecture Search Space.

Defines the space of possible architectures for NAS.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 3.1 for specification.
"""

from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
import uuid
import logging
import random

logger = logging.getLogger("rsi.plasticity.nas.space")


class NodeType(Enum):
    """Types of nodes in architecture."""
    INPUT = "input"
    OUTPUT = "output"
    PROCESSING = "processing"
    MEMORY = "memory"
    ATTENTION = "attention"
    AGGREGATION = "aggregation"
    TRANSFORMATION = "transformation"


class ConnectionType(Enum):
    """Types of connections between nodes."""
    SEQUENTIAL = "sequential"
    SKIP = "skip"
    ATTENTION = "attention"
    GATED = "gated"
    RESIDUAL = "residual"


class OperationType(Enum):
    """Operations that can be performed at nodes."""
    IDENTITY = "identity"
    LINEAR = "linear"
    NONLINEAR = "nonlinear"
    CONVOLUTION = "convolution"
    ATTENTION = "attention"
    POOLING = "pooling"
    NORMALIZATION = "normalization"
    DROPOUT = "dropout"
    EMBEDDING = "embedding"


@dataclass
class NodeSpec:
    """Specification for a node in the architecture."""
    id: str
    node_type: NodeType
    operation: OperationType
    input_dim: int
    output_dim: int
    parameters: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'node_type': self.node_type.value,
            'operation': self.operation.value,
            'input_dim': self.input_dim,
            'output_dim': self.output_dim,
            'parameters': self.parameters,
            'metadata': self.metadata
        }


@dataclass
class ConnectionSpec:
    """Specification for a connection between nodes."""
    id: str
    source_id: str
    target_id: str
    connection_type: ConnectionType
    weight: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'source_id': self.source_id,
            'target_id': self.target_id,
            'connection_type': self.connection_type.value,
            'weight': self.weight,
            'metadata': self.metadata
        }


@dataclass
class ArchitectureSpec:
    """Full specification of an architecture."""
    id: str
    name: str
    nodes: List[NodeSpec]
    connections: List[ConnectionSpec]
    input_nodes: List[str]
    output_nodes: List[str]
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'nodes': [n.to_dict() for n in self.nodes],
            'connections': [c.to_dict() for c in self.connections],
            'input_nodes': self.input_nodes,
            'output_nodes': self.output_nodes,
            'created_at': self.created_at,
            'metadata': self.metadata
        }

    @property
    def node_count(self) -> int:
        """Get number of nodes."""
        return len(self.nodes)

    @property
    def connection_count(self) -> int:
        """Get number of connections."""
        return len(self.connections)

    def get_node(self, node_id: str) -> Optional[NodeSpec]:
        """Get node by ID."""
        for node in self.nodes:
            if node.id == node_id:
                return node
        return None


@dataclass
class SpaceConstraints:
    """Constraints on the search space."""
    min_nodes: int = 2
    max_nodes: int = 50
    min_connections: int = 1
    max_connections: int = 200
    allowed_node_types: Set[NodeType] = field(
        default_factory=lambda: set(NodeType)
    )
    allowed_operations: Set[OperationType] = field(
        default_factory=lambda: set(OperationType)
    )
    allowed_connection_types: Set[ConnectionType] = field(
        default_factory=lambda: set(ConnectionType)
    )
    min_dimension: int = 1
    max_dimension: int = 4096
    require_input_output: bool = True


@dataclass
class SearchBudget:
    """Budget for architecture search."""
    max_evaluations: int = 100
    max_time_seconds: float = 3600.0
    max_memory_mb: float = 4096.0
    target_score: Optional[float] = None
    early_stopping_patience: int = 10


class ArchitectureSpace:
    """
    Defines the space of possible architectures.

    Provides methods for sampling, mutating, and crossover
    of architectures within the defined constraints.
    """

    def __init__(
        self,
        constraints: SpaceConstraints = None,
        config: Dict = None
    ):
        """
        Initialize architecture space.

        Args:
            constraints: Space constraints
            config: Additional configuration
        """
        self.constraints = constraints or SpaceConstraints()
        self.config = config or {}

        # Track generated architectures
        self._architectures: Dict[str, ArchitectureSpec] = {}

        # Statistics
        self._samples_generated: int = 0
        self._mutations_performed: int = 0
        self._crossovers_performed: int = 0

    def sample_random(self, name: str = None) -> ArchitectureSpec:
        """
        Sample a random architecture from the space.

        Args:
            name: Optional name for the architecture

        Returns:
            Randomly sampled ArchitectureSpec
        """
        arch_id = f"arch_{uuid.uuid4().hex[:12]}"
        name = name or f"Random Architecture {self._samples_generated + 1}"

        # Determine number of nodes
        num_nodes = random.randint(
            self.constraints.min_nodes,
            min(self.constraints.max_nodes, 10)  # Start small
        )

        # Create nodes
        nodes = []
        node_ids = []

        # Input node
        input_node = NodeSpec(
            id=f"node_input",
            node_type=NodeType.INPUT,
            operation=OperationType.IDENTITY,
            input_dim=self._random_dim(),
            output_dim=self._random_dim()
        )
        nodes.append(input_node)
        node_ids.append(input_node.id)

        # Processing nodes
        for i in range(num_nodes - 2):
            node = NodeSpec(
                id=f"node_{i}",
                node_type=self._random_node_type(),
                operation=self._random_operation(),
                input_dim=self._random_dim(),
                output_dim=self._random_dim()
            )
            nodes.append(node)
            node_ids.append(node.id)

        # Output node
        output_node = NodeSpec(
            id=f"node_output",
            node_type=NodeType.OUTPUT,
            operation=OperationType.IDENTITY,
            input_dim=self._random_dim(),
            output_dim=self._random_dim()
        )
        nodes.append(output_node)
        node_ids.append(output_node.id)

        # Create connections
        connections = self._create_random_connections(node_ids)

        architecture = ArchitectureSpec(
            id=arch_id,
            name=name,
            nodes=nodes,
            connections=connections,
            input_nodes=["node_input"],
            output_nodes=["node_output"]
        )

        self._architectures[arch_id] = architecture
        self._samples_generated += 1

        logger.debug(f"Sampled random architecture: {arch_id}")

        return architecture

    def mutate(
        self,
        architecture: ArchitectureSpec,
        mutation_rate: float = 0.1
    ) -> ArchitectureSpec:
        """
        Mutate an architecture to create a new variant.

        Args:
            architecture: Architecture to mutate
            mutation_rate: Probability of each mutation

        Returns:
            Mutated ArchitectureSpec
        """
        arch_id = f"arch_{uuid.uuid4().hex[:12]}"

        # Copy nodes and connections
        new_nodes = []
        for node in architecture.nodes:
            new_node = NodeSpec(
                id=node.id,
                node_type=node.node_type,
                operation=node.operation,
                input_dim=node.input_dim,
                output_dim=node.output_dim,
                parameters=node.parameters.copy(),
                metadata=node.metadata.copy()
            )

            # Maybe mutate operation
            if random.random() < mutation_rate:
                new_node.operation = self._random_operation()

            # Maybe mutate dimensions
            if random.random() < mutation_rate:
                new_node.output_dim = self._random_dim()

            new_nodes.append(new_node)

        new_connections = []
        for conn in architecture.connections:
            new_conn = ConnectionSpec(
                id=conn.id,
                source_id=conn.source_id,
                target_id=conn.target_id,
                connection_type=conn.connection_type,
                weight=conn.weight,
                metadata=conn.metadata.copy()
            )

            # Maybe mutate connection type
            if random.random() < mutation_rate:
                new_conn.connection_type = self._random_connection_type()

            # Maybe mutate weight
            if random.random() < mutation_rate:
                new_conn.weight = random.uniform(0.1, 2.0)

            new_connections.append(new_conn)

        # Maybe add or remove node
        if random.random() < mutation_rate:
            if len(new_nodes) < self.constraints.max_nodes:
                # Add node
                new_node = NodeSpec(
                    id=f"node_mut_{uuid.uuid4().hex[:8]}",
                    node_type=self._random_node_type(),
                    operation=self._random_operation(),
                    input_dim=self._random_dim(),
                    output_dim=self._random_dim()
                )
                new_nodes.append(new_node)

        mutated = ArchitectureSpec(
            id=arch_id,
            name=f"Mutated {architecture.name}",
            nodes=new_nodes,
            connections=new_connections,
            input_nodes=architecture.input_nodes.copy(),
            output_nodes=architecture.output_nodes.copy(),
            metadata={'parent': architecture.id, 'mutation_rate': mutation_rate}
        )

        self._architectures[arch_id] = mutated
        self._mutations_performed += 1

        logger.debug(f"Mutated architecture: {architecture.id} -> {arch_id}")

        return mutated

    def crossover(
        self,
        parent1: ArchitectureSpec,
        parent2: ArchitectureSpec
    ) -> ArchitectureSpec:
        """
        Create offspring architecture from two parents.

        Args:
            parent1: First parent architecture
            parent2: Second parent architecture

        Returns:
            Offspring ArchitectureSpec
        """
        arch_id = f"arch_{uuid.uuid4().hex[:12]}"

        # Take nodes from both parents
        nodes_from_p1 = parent1.nodes[:len(parent1.nodes) // 2]
        nodes_from_p2 = parent2.nodes[len(parent2.nodes) // 2:]

        # Combine nodes (avoiding duplicates)
        new_nodes = []
        seen_ids = set()

        for node in nodes_from_p1 + nodes_from_p2:
            if node.id not in seen_ids:
                new_nodes.append(NodeSpec(
                    id=node.id,
                    node_type=node.node_type,
                    operation=node.operation,
                    input_dim=node.input_dim,
                    output_dim=node.output_dim
                ))
                seen_ids.add(node.id)

        # Ensure input/output nodes exist
        if "node_input" not in seen_ids:
            new_nodes.insert(0, NodeSpec(
                id="node_input",
                node_type=NodeType.INPUT,
                operation=OperationType.IDENTITY,
                input_dim=256,
                output_dim=256
            ))
        if "node_output" not in seen_ids:
            new_nodes.append(NodeSpec(
                id="node_output",
                node_type=NodeType.OUTPUT,
                operation=OperationType.IDENTITY,
                input_dim=256,
                output_dim=256
            ))

        # Create connections between combined nodes
        node_ids = [n.id for n in new_nodes]
        new_connections = self._create_random_connections(node_ids)

        offspring = ArchitectureSpec(
            id=arch_id,
            name=f"Offspring of {parent1.name} x {parent2.name}",
            nodes=new_nodes,
            connections=new_connections,
            input_nodes=["node_input"],
            output_nodes=["node_output"],
            metadata={'parent1': parent1.id, 'parent2': parent2.id}
        )

        self._architectures[arch_id] = offspring
        self._crossovers_performed += 1

        logger.debug(
            f"Crossover: {parent1.id} x {parent2.id} -> {arch_id}"
        )

        return offspring

    def _random_dim(self) -> int:
        """Get random dimension within constraints."""
        return random.choice([64, 128, 256, 512, 1024])

    def _random_node_type(self) -> NodeType:
        """Get random allowed node type."""
        allowed = list(self.constraints.allowed_node_types)
        # Exclude INPUT/OUTPUT for internal nodes
        allowed = [t for t in allowed if t not in [NodeType.INPUT, NodeType.OUTPUT]]
        return random.choice(allowed) if allowed else NodeType.PROCESSING

    def _random_operation(self) -> OperationType:
        """Get random allowed operation."""
        allowed = list(self.constraints.allowed_operations)
        return random.choice(allowed) if allowed else OperationType.LINEAR

    def _random_connection_type(self) -> ConnectionType:
        """Get random allowed connection type."""
        allowed = list(self.constraints.allowed_connection_types)
        return random.choice(allowed) if allowed else ConnectionType.SEQUENTIAL

    def _create_random_connections(
        self,
        node_ids: List[str]
    ) -> List[ConnectionSpec]:
        """Create random connections between nodes."""
        connections = []

        # Ensure sequential path from input to output
        for i in range(len(node_ids) - 1):
            conn = ConnectionSpec(
                id=f"conn_{i}",
                source_id=node_ids[i],
                target_id=node_ids[i + 1],
                connection_type=ConnectionType.SEQUENTIAL
            )
            connections.append(conn)

        # Maybe add skip connections
        num_skip = random.randint(0, len(node_ids) // 2)
        for i in range(num_skip):
            src_idx = random.randint(0, len(node_ids) - 2)
            tgt_idx = random.randint(src_idx + 1, len(node_ids) - 1)
            conn = ConnectionSpec(
                id=f"skip_{i}",
                source_id=node_ids[src_idx],
                target_id=node_ids[tgt_idx],
                connection_type=ConnectionType.SKIP
            )
            connections.append(conn)

        return connections

    def validate(self, architecture: ArchitectureSpec) -> Tuple[bool, List[str]]:
        """
        Validate architecture against constraints.

        Args:
            architecture: Architecture to validate

        Returns:
            Tuple of (valid, issues)
        """
        issues = []

        # Check node count
        if architecture.node_count < self.constraints.min_nodes:
            issues.append(f"Too few nodes: {architecture.node_count}")
        if architecture.node_count > self.constraints.max_nodes:
            issues.append(f"Too many nodes: {architecture.node_count}")

        # Check connection count
        if architecture.connection_count < self.constraints.min_connections:
            issues.append(f"Too few connections: {architecture.connection_count}")
        if architecture.connection_count > self.constraints.max_connections:
            issues.append(f"Too many connections: {architecture.connection_count}")

        # Check input/output nodes
        if self.constraints.require_input_output:
            if not architecture.input_nodes:
                issues.append("No input nodes defined")
            if not architecture.output_nodes:
                issues.append("No output nodes defined")

        return len(issues) == 0, issues

    def get_stats(self) -> Dict:
        """Get space statistics."""
        return {
            'architectures_in_space': len(self._architectures),
            'samples_generated': self._samples_generated,
            'mutations_performed': self._mutations_performed,
            'crossovers_performed': self._crossovers_performed,
            'constraints': {
                'min_nodes': self.constraints.min_nodes,
                'max_nodes': self.constraints.max_nodes,
                'min_connections': self.constraints.min_connections,
                'max_connections': self.constraints.max_connections
            }
        }

    def reset(self) -> None:
        """Reset space state."""
        self._architectures.clear()
        self._samples_generated = 0
        self._mutations_performed = 0
        self._crossovers_performed = 0
        logger.info("ArchitectureSpace reset")
