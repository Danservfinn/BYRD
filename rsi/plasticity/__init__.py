"""
Cognitive Plasticity Module.

Provides infrastructure for self-modification through
module composition and configuration.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 2.1-2.2 for specification.
See docs/COGNITIVE_PLASTICITY.md for architecture.
"""

from .module_types import (
    ModuleType,
    ModuleStatus,
    CompositionType,
    ModuleCapability,
    ModuleDependency,
    CognitiveModule,
    CompositionCandidate,
    ComposedModule,
    create_module_id,
    create_reasoning_module,
    create_memory_module,
    create_planning_module,
)

from .module_registry import (
    ModuleRegistry,
    RegistryStats,
)

from .module_composer import (
    ModuleComposer,
    CompositionResult,
    CompositionRule,
)

from .levels import (
    PlasticityLevel,
    LevelRequirements,
    LevelProgress,
    LEVEL_REQUIREMENTS,
    can_advance_level,
    get_level_requirements,
    is_operation_allowed,
)

from .proposal import (
    ModificationType,
    RollbackPlan,
    PlasticityProposal,
    ModificationResult,
    ProposalGenerator,
)

from .executor import (
    Checkpoint,
    ModificationExecutor,
)

from .engine import (
    EngineState,
    CognitivePlasticityEngine,
)

__all__ = [
    # Module Types
    "ModuleType",
    "ModuleStatus",
    "CompositionType",
    "ModuleCapability",
    "ModuleDependency",
    "CognitiveModule",
    "CompositionCandidate",
    "ComposedModule",
    "create_module_id",
    "create_reasoning_module",
    "create_memory_module",
    "create_planning_module",
    # Registry
    "ModuleRegistry",
    "RegistryStats",
    # Composer
    "ModuleComposer",
    "CompositionResult",
    "CompositionRule",
    # Plasticity Levels
    "PlasticityLevel",
    "LevelRequirements",
    "LevelProgress",
    "LEVEL_REQUIREMENTS",
    "can_advance_level",
    "get_level_requirements",
    "is_operation_allowed",
    # Proposals
    "ModificationType",
    "RollbackPlan",
    "PlasticityProposal",
    "ModificationResult",
    "ProposalGenerator",
    # Executor
    "Checkpoint",
    "ModificationExecutor",
    # Engine
    "EngineState",
    "CognitivePlasticityEngine",
]
