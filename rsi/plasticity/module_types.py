"""
Module Type Definitions for Cognitive Plasticity.

Defines the structure of cognitive modules that can be composed,
configured, and evolved by BYRD's plasticity engine.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 2.2 for specification.
See docs/COGNITIVE_PLASTICITY.md for architecture.
"""

from typing import Dict, List, Optional, Any, Callable, Set
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timezone
import uuid


class ModuleType(Enum):
    """Types of cognitive modules."""
    REASONING = "reasoning"       # Logical inference, deduction
    MEMORY = "memory"            # Storage, retrieval, indexing
    PLANNING = "planning"        # Goal decomposition, scheduling
    LEARNING = "learning"        # Pattern extraction, generalization
    PERCEPTION = "perception"    # Input processing, encoding
    GENERATION = "generation"    # Output synthesis, creation
    EVALUATION = "evaluation"    # Quality assessment, scoring
    META = "meta"               # Self-reflection, introspection


class ModuleStatus(Enum):
    """Module lifecycle status."""
    DRAFT = "draft"              # Being developed
    REGISTERED = "registered"    # Available but not active
    ACTIVE = "active"            # Currently in use
    DEPRECATED = "deprecated"    # Scheduled for removal
    ARCHIVED = "archived"        # Preserved but inactive


class CompositionType(Enum):
    """How modules can be composed together."""
    SEQUENTIAL = "sequential"    # Output of A feeds into B
    PARALLEL = "parallel"        # Both run, results merged
    CONDITIONAL = "conditional"  # Route based on condition
    ENSEMBLE = "ensemble"        # Vote/average results
    WRAPPER = "wrapper"          # A wraps B (pre/post processing)


@dataclass
class ModuleCapability:
    """A specific capability provided by a module."""
    name: str
    description: str
    input_schema: Dict[str, Any] = field(default_factory=dict)
    output_schema: Dict[str, Any] = field(default_factory=dict)
    performance_baseline: float = 0.0  # Expected baseline performance 0-1


@dataclass
class ModuleDependency:
    """Dependency on another module."""
    module_id: str
    required: bool = True
    version_constraint: Optional[str] = None  # e.g., ">=1.0.0"


@dataclass
class CognitiveModule:
    """
    A cognitive module that can be composed, configured, and evolved.

    Modules are the building blocks of BYRD's cognitive architecture.
    They can be composed together to create more complex behaviors.
    """
    id: str
    name: str
    module_type: ModuleType
    version: str = "1.0.0"
    status: ModuleStatus = ModuleStatus.DRAFT

    # Description and metadata
    description: str = ""
    author: str = "system"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    # Capabilities this module provides
    capabilities: List[ModuleCapability] = field(default_factory=list)

    # Dependencies on other modules
    dependencies: List[ModuleDependency] = field(default_factory=list)

    # Configuration
    config: Dict[str, Any] = field(default_factory=dict)
    default_config: Dict[str, Any] = field(default_factory=dict)

    # Composition rules
    composable_with: List[ModuleType] = field(default_factory=list)
    composition_position: str = "any"  # "first", "last", "any"

    # Performance tracking
    invocation_count: int = 0
    success_count: int = 0
    total_latency_ms: float = 0.0

    # Tags for discovery
    tags: List[str] = field(default_factory=list)

    # Provenance - where this module came from
    provenance: Optional[str] = None  # ID of desire/modification that created it

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            'id': self.id,
            'name': self.name,
            'module_type': self.module_type.value,
            'version': self.version,
            'status': self.status.value,
            'description': self.description,
            'author': self.author,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'capabilities': [
                {
                    'name': c.name,
                    'description': c.description,
                    'input_schema': c.input_schema,
                    'output_schema': c.output_schema,
                    'performance_baseline': c.performance_baseline
                }
                for c in self.capabilities
            ],
            'dependencies': [
                {
                    'module_id': d.module_id,
                    'required': d.required,
                    'version_constraint': d.version_constraint
                }
                for d in self.dependencies
            ],
            'config': self.config,
            'composable_with': [t.value for t in self.composable_with],
            'composition_position': self.composition_position,
            'invocation_count': self.invocation_count,
            'success_count': self.success_count,
            'total_latency_ms': self.total_latency_ms,
            'tags': self.tags,
            'provenance': self.provenance
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "CognitiveModule":
        """Create from dictionary."""
        return cls(
            id=data['id'],
            name=data['name'],
            module_type=ModuleType(data['module_type']),
            version=data.get('version', '1.0.0'),
            status=ModuleStatus(data.get('status', 'draft')),
            description=data.get('description', ''),
            author=data.get('author', 'system'),
            created_at=data.get('created_at', datetime.now(timezone.utc).isoformat()),
            updated_at=data.get('updated_at', datetime.now(timezone.utc).isoformat()),
            capabilities=[
                ModuleCapability(
                    name=c['name'],
                    description=c['description'],
                    input_schema=c.get('input_schema', {}),
                    output_schema=c.get('output_schema', {}),
                    performance_baseline=c.get('performance_baseline', 0.0)
                )
                for c in data.get('capabilities', [])
            ],
            dependencies=[
                ModuleDependency(
                    module_id=d['module_id'],
                    required=d.get('required', True),
                    version_constraint=d.get('version_constraint')
                )
                for d in data.get('dependencies', [])
            ],
            config=data.get('config', {}),
            composable_with=[ModuleType(t) for t in data.get('composable_with', [])],
            composition_position=data.get('composition_position', 'any'),
            invocation_count=data.get('invocation_count', 0),
            success_count=data.get('success_count', 0),
            total_latency_ms=data.get('total_latency_ms', 0.0),
            tags=data.get('tags', []),
            provenance=data.get('provenance')
        )

    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.invocation_count == 0:
            return 0.0
        return self.success_count / self.invocation_count

    @property
    def avg_latency_ms(self) -> float:
        """Calculate average latency."""
        if self.invocation_count == 0:
            return 0.0
        return self.total_latency_ms / self.invocation_count


@dataclass
class CompositionCandidate:
    """A candidate composition of modules."""
    modules: List[CognitiveModule]
    composition_type: CompositionType
    estimated_capability_score: float
    rationale: str


@dataclass
class ComposedModule(CognitiveModule):
    """
    A module created by composing other modules.
    Inherits from CognitiveModule but tracks its composition.
    """
    source_modules: List[str] = field(default_factory=list)  # IDs of source modules
    composition_type: CompositionType = CompositionType.SEQUENTIAL
    composition_config: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary, including composition info."""
        base = super().to_dict()
        base['source_modules'] = self.source_modules
        base['composition_type'] = self.composition_type.value
        base['composition_config'] = self.composition_config
        base['is_composed'] = True
        return base


def create_module_id() -> str:
    """Generate a unique module ID."""
    return f"mod_{uuid.uuid4().hex[:12]}"


# Pre-defined core modules
def create_reasoning_module() -> CognitiveModule:
    """Create the core reasoning module."""
    return CognitiveModule(
        id="mod_reasoning_v1",
        name="Core Reasoning",
        module_type=ModuleType.REASONING,
        version="1.0.0",
        status=ModuleStatus.ACTIVE,
        description="Logical inference, deduction, and problem-solving",
        capabilities=[
            ModuleCapability(
                name="logical_inference",
                description="Draw conclusions from premises",
                input_schema={"premises": "List[str]"},
                output_schema={"conclusions": "List[str]", "confidence": "float"},
                performance_baseline=0.7
            ),
            ModuleCapability(
                name="problem_decomposition",
                description="Break complex problems into sub-problems",
                input_schema={"problem": "str"},
                output_schema={"subproblems": "List[str]"},
                performance_baseline=0.6
            )
        ],
        composable_with=[ModuleType.MEMORY, ModuleType.PLANNING, ModuleType.EVALUATION],
        tags=["core", "reasoning", "logic"]
    )


def create_memory_module() -> CognitiveModule:
    """Create the core memory module."""
    return CognitiveModule(
        id="mod_memory_v1",
        name="Core Memory",
        module_type=ModuleType.MEMORY,
        version="1.0.0",
        status=ModuleStatus.ACTIVE,
        description="Storage, retrieval, and indexing of information",
        capabilities=[
            ModuleCapability(
                name="store",
                description="Store information with metadata",
                input_schema={"content": "str", "metadata": "Dict"},
                output_schema={"id": "str"},
                performance_baseline=0.9
            ),
            ModuleCapability(
                name="retrieve",
                description="Retrieve relevant information",
                input_schema={"query": "str", "limit": "int"},
                output_schema={"results": "List[Dict]"},
                performance_baseline=0.7
            ),
            ModuleCapability(
                name="semantic_search",
                description="Find semantically similar content",
                input_schema={"query": "str"},
                output_schema={"results": "List[Dict]", "scores": "List[float]"},
                performance_baseline=0.65
            )
        ],
        composable_with=[ModuleType.REASONING, ModuleType.PLANNING, ModuleType.LEARNING],
        tags=["core", "memory", "storage", "retrieval"]
    )


def create_planning_module() -> CognitiveModule:
    """Create the core planning module."""
    return CognitiveModule(
        id="mod_planning_v1",
        name="Core Planning",
        module_type=ModuleType.PLANNING,
        version="1.0.0",
        status=ModuleStatus.ACTIVE,
        description="Goal decomposition, scheduling, and strategy",
        capabilities=[
            ModuleCapability(
                name="decompose_goal",
                description="Break goal into actionable sub-goals",
                input_schema={"goal": "str", "context": "Dict"},
                output_schema={"subgoals": "List[str]", "dependencies": "Dict"},
                performance_baseline=0.6
            ),
            ModuleCapability(
                name="create_plan",
                description="Create execution plan for goals",
                input_schema={"goals": "List[str]"},
                output_schema={"plan": "List[Dict]", "estimated_steps": "int"},
                performance_baseline=0.55
            ),
            ModuleCapability(
                name="prioritize",
                description="Order tasks by importance",
                input_schema={"tasks": "List[str]"},
                output_schema={"ordered_tasks": "List[str]", "priorities": "List[float]"},
                performance_baseline=0.7
            )
        ],
        composable_with=[ModuleType.REASONING, ModuleType.MEMORY, ModuleType.EVALUATION],
        tags=["core", "planning", "strategy", "goals"]
    )
