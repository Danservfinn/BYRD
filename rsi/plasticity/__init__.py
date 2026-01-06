"""
Cognitive Plasticity Module.

Provides infrastructure for self-modification through
module composition and configuration.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 2.2 for specification.
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

__all__ = [
    # Types
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
]
