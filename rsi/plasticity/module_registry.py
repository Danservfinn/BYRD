"""
Module Registry - Track and manage cognitive modules.

Provides centralized registration, discovery, and management of
cognitive modules that can be composed by the plasticity engine.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 2.2 for specification.
"""

from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass
import logging
import json
from datetime import datetime, timezone

from .module_types import (
    CognitiveModule,
    ModuleType,
    ModuleStatus,
    ModuleCapability,
    ModuleDependency,
    CompositionCandidate,
    CompositionType,
    create_module_id,
    create_reasoning_module,
    create_memory_module,
    create_planning_module,
)

logger = logging.getLogger("rsi.plasticity.registry")


@dataclass
class RegistryStats:
    """Statistics about the registry."""
    total_modules: int
    active_modules: int
    modules_by_type: Dict[str, int]
    total_capabilities: int
    total_invocations: int


class ModuleRegistry:
    """
    Registry of available cognitive modules.

    Tracks capabilities, dependencies, and composition rules.
    Provides discovery and search functionality.
    """

    def __init__(self, memory=None, config: Dict = None):
        """
        Initialize module registry.

        Args:
            memory: Optional Memory instance for Neo4j persistence
            config: Configuration options
        """
        self.memory = memory
        self.config = config or {}

        # In-memory cache
        self._modules: Dict[str, CognitiveModule] = {}
        self._by_type: Dict[ModuleType, Set[str]] = {t: set() for t in ModuleType}
        self._by_capability: Dict[str, Set[str]] = {}
        self._by_tag: Dict[str, Set[str]] = {}

        # Core modules loaded flag
        self._core_loaded = False

    async def initialize(self) -> None:
        """Initialize registry with core modules."""
        if self._core_loaded:
            return

        # Register core modules
        core_modules = [
            create_reasoning_module(),
            create_memory_module(),
            create_planning_module(),
        ]

        for module in core_modules:
            await self.register_module(module)

        self._core_loaded = True
        logger.info(f"Registry initialized with {len(core_modules)} core modules")

    async def register_module(self, module: CognitiveModule) -> str:
        """
        Register a new module.

        Args:
            module: The module to register

        Returns:
            Module ID
        """
        # Generate ID if not provided
        if not module.id:
            module.id = create_module_id()

        # Update timestamp
        module.updated_at = datetime.now(timezone.utc).isoformat()

        # Set to registered status if draft
        if module.status == ModuleStatus.DRAFT:
            module.status = ModuleStatus.REGISTERED

        # Store in memory cache
        self._modules[module.id] = module

        # Update indices
        self._by_type[module.module_type].add(module.id)

        for capability in module.capabilities:
            if capability.name not in self._by_capability:
                self._by_capability[capability.name] = set()
            self._by_capability[capability.name].add(module.id)

        for tag in module.tags:
            if tag not in self._by_tag:
                self._by_tag[tag] = set()
            self._by_tag[tag].add(module.id)

        # Persist to Neo4j if available
        await self._persist_module(module)

        logger.info(f"Registered module: {module.name} ({module.id})")

        return module.id

    async def get_module(self, module_id: str) -> Optional[CognitiveModule]:
        """
        Get module by ID.

        Args:
            module_id: Module ID

        Returns:
            Module or None if not found
        """
        return self._modules.get(module_id)

    async def list_modules(
        self,
        filter_type: Optional[ModuleType] = None,
        filter_status: Optional[ModuleStatus] = None,
        filter_tags: Optional[List[str]] = None,
        limit: int = 100
    ) -> List[CognitiveModule]:
        """
        List all modules with optional filters.

        Args:
            filter_type: Filter by module type
            filter_status: Filter by status
            filter_tags: Filter by tags (any match)
            limit: Maximum modules to return

        Returns:
            List of matching modules
        """
        results = []

        # Start with type filter or all
        if filter_type:
            candidate_ids = self._by_type.get(filter_type, set())
        else:
            candidate_ids = set(self._modules.keys())

        # Apply tag filter
        if filter_tags:
            tag_matches = set()
            for tag in filter_tags:
                if tag in self._by_tag:
                    tag_matches.update(self._by_tag[tag])
            candidate_ids = candidate_ids.intersection(tag_matches)

        # Fetch and filter by status
        for module_id in list(candidate_ids)[:limit * 2]:  # Over-fetch for status filter
            module = self._modules.get(module_id)
            if module:
                if filter_status and module.status != filter_status:
                    continue
                results.append(module)
                if len(results) >= limit:
                    break

        return results

    async def search_modules(
        self,
        query: str,
        limit: int = 10
    ) -> List[CognitiveModule]:
        """
        Search modules by name, description, or tags.

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            Matching modules ordered by relevance
        """
        query_lower = query.lower()
        scored = []

        for module in self._modules.values():
            score = 0

            # Name match (highest weight)
            if query_lower in module.name.lower():
                score += 10
            if module.name.lower() == query_lower:
                score += 5

            # Description match
            if query_lower in module.description.lower():
                score += 3

            # Tag match
            for tag in module.tags:
                if query_lower in tag.lower():
                    score += 2

            # Capability match
            for cap in module.capabilities:
                if query_lower in cap.name.lower():
                    score += 2

            if score > 0:
                scored.append((score, module))

        # Sort by score descending
        scored.sort(key=lambda x: x[0], reverse=True)

        return [m for _, m in scored[:limit]]

    async def find_by_capability(
        self,
        capability_name: str
    ) -> List[CognitiveModule]:
        """
        Find modules providing a specific capability.

        Args:
            capability_name: Capability to search for

        Returns:
            Modules providing the capability
        """
        module_ids = self._by_capability.get(capability_name, set())
        return [self._modules[mid] for mid in module_ids if mid in self._modules]

    async def get_composition_candidates(
        self,
        goal: str,
        max_modules: int = 3
    ) -> List[CompositionCandidate]:
        """
        Get modules that could be composed to achieve goal.

        Args:
            goal: Goal description
            max_modules: Maximum modules per composition

        Returns:
            Composition candidates sorted by estimated score
        """
        candidates = []
        goal_lower = goal.lower()

        # Find relevant modules
        relevant = await self.search_modules(goal, limit=max_modules * 2)

        if len(relevant) < 2:
            return candidates

        # Generate composition combinations
        for i, mod1 in enumerate(relevant):
            for mod2 in relevant[i + 1:]:
                # Check if modules can compose
                if self._can_compose(mod1, mod2):
                    # Determine best composition type
                    comp_type = self._suggest_composition_type(mod1, mod2, goal)

                    # Estimate capability score
                    score = self._estimate_composition_score(mod1, mod2, comp_type)

                    candidates.append(CompositionCandidate(
                        modules=[mod1, mod2],
                        composition_type=comp_type,
                        estimated_capability_score=score,
                        rationale=f"Combine {mod1.name} + {mod2.name} for {goal}"
                    ))

        # Sort by score
        candidates.sort(key=lambda c: c.estimated_capability_score, reverse=True)

        return candidates[:5]

    def _can_compose(self, mod1: CognitiveModule, mod2: CognitiveModule) -> bool:
        """Check if two modules can be composed."""
        # Check composability lists
        type1_allows = (
            not mod1.composable_with or
            mod2.module_type in mod1.composable_with
        )
        type2_allows = (
            not mod2.composable_with or
            mod1.module_type in mod2.composable_with
        )

        # Check position constraints
        position_ok = True
        if mod1.composition_position == "last" and mod2.composition_position == "last":
            position_ok = False
        if mod1.composition_position == "first" and mod2.composition_position == "first":
            position_ok = False

        return type1_allows and type2_allows and position_ok

    def _suggest_composition_type(
        self,
        mod1: CognitiveModule,
        mod2: CognitiveModule,
        goal: str
    ) -> CompositionType:
        """Suggest the best composition type for two modules."""
        goal_lower = goal.lower()

        # Sequential if one feeds into another
        if mod1.module_type == ModuleType.PERCEPTION and mod2.module_type == ModuleType.REASONING:
            return CompositionType.SEQUENTIAL
        if mod1.module_type == ModuleType.REASONING and mod2.module_type == ModuleType.GENERATION:
            return CompositionType.SEQUENTIAL

        # Ensemble if both are same type
        if mod1.module_type == mod2.module_type:
            return CompositionType.ENSEMBLE

        # Parallel for different types
        if "and" in goal_lower or "both" in goal_lower:
            return CompositionType.PARALLEL

        # Default to sequential
        return CompositionType.SEQUENTIAL

    def _estimate_composition_score(
        self,
        mod1: CognitiveModule,
        mod2: CognitiveModule,
        comp_type: CompositionType
    ) -> float:
        """Estimate the capability score of a composition."""
        # Base score from individual performance
        score1 = mod1.success_rate if mod1.invocation_count > 0 else 0.5
        score2 = mod2.success_rate if mod2.invocation_count > 0 else 0.5

        # Combine based on composition type
        if comp_type == CompositionType.SEQUENTIAL:
            return score1 * score2  # Both must succeed
        elif comp_type == CompositionType.PARALLEL:
            return max(score1, score2)  # Best one counts
        elif comp_type == CompositionType.ENSEMBLE:
            return (score1 + score2) / 2 + 0.1  # Averaging with bonus
        else:
            return (score1 + score2) / 2

    async def update_module(
        self,
        module_id: str,
        updates: Dict[str, Any]
    ) -> Optional[CognitiveModule]:
        """
        Update module properties.

        Args:
            module_id: Module ID
            updates: Properties to update

        Returns:
            Updated module or None
        """
        module = self._modules.get(module_id)
        if not module:
            return None

        # Apply updates
        for key, value in updates.items():
            if hasattr(module, key):
                setattr(module, key, value)

        module.updated_at = datetime.now(timezone.utc).isoformat()

        # Re-index if type or tags changed
        if 'module_type' in updates or 'tags' in updates or 'capabilities' in updates:
            await self._reindex_module(module)

        # Persist
        await self._persist_module(module)

        return module

    async def record_invocation(
        self,
        module_id: str,
        success: bool,
        latency_ms: float
    ) -> None:
        """
        Record a module invocation for tracking.

        Args:
            module_id: Module ID
            success: Whether invocation succeeded
            latency_ms: Latency in milliseconds
        """
        module = self._modules.get(module_id)
        if module:
            module.invocation_count += 1
            if success:
                module.success_count += 1
            module.total_latency_ms += latency_ms

    async def deprecate_module(self, module_id: str) -> bool:
        """
        Mark a module as deprecated.

        Args:
            module_id: Module ID

        Returns:
            True if deprecated, False if not found
        """
        module = self._modules.get(module_id)
        if not module:
            return False

        module.status = ModuleStatus.DEPRECATED
        module.updated_at = datetime.now(timezone.utc).isoformat()

        await self._persist_module(module)
        logger.info(f"Deprecated module: {module.name} ({module_id})")

        return True

    async def _persist_module(self, module: CognitiveModule) -> None:
        """Persist module to Neo4j."""
        if not self.memory:
            return

        try:
            await self.memory.query_neo4j("""
                MERGE (m:CognitiveModule {id: $id})
                SET m.name = $name,
                    m.module_type = $module_type,
                    m.version = $version,
                    m.status = $status,
                    m.description = $description,
                    m.config = $config,
                    m.capabilities = $capabilities,
                    m.tags = $tags,
                    m.invocation_count = $invocation_count,
                    m.success_count = $success_count,
                    m.updated_at = $updated_at
            """, {
                'id': module.id,
                'name': module.name,
                'module_type': module.module_type.value,
                'version': module.version,
                'status': module.status.value,
                'description': module.description,
                'config': json.dumps(module.config),
                'capabilities': json.dumps([c.name for c in module.capabilities]),
                'tags': json.dumps(module.tags),
                'invocation_count': module.invocation_count,
                'success_count': module.success_count,
                'updated_at': module.updated_at
            })
        except Exception as e:
            logger.warning(f"Failed to persist module: {e}")

    async def _reindex_module(self, module: CognitiveModule) -> None:
        """Re-index module after changes."""
        module_id = module.id

        # Clear from all indices
        for type_set in self._by_type.values():
            type_set.discard(module_id)
        for cap_set in self._by_capability.values():
            cap_set.discard(module_id)
        for tag_set in self._by_tag.values():
            tag_set.discard(module_id)

        # Re-add to indices
        self._by_type[module.module_type].add(module_id)

        for capability in module.capabilities:
            if capability.name not in self._by_capability:
                self._by_capability[capability.name] = set()
            self._by_capability[capability.name].add(module_id)

        for tag in module.tags:
            if tag not in self._by_tag:
                self._by_tag[tag] = set()
            self._by_tag[tag].add(module_id)

    async def load_from_memory(self) -> int:
        """
        Load modules from Neo4j.

        Returns:
            Number of modules loaded
        """
        if not self.memory:
            return 0

        try:
            result = await self.memory.query_neo4j("""
                MATCH (m:CognitiveModule)
                RETURN m
            """)

            count = 0
            for row in result:
                node = row['m']
                module = CognitiveModule(
                    id=node['id'],
                    name=node['name'],
                    module_type=ModuleType(node['module_type']),
                    version=node.get('version', '1.0.0'),
                    status=ModuleStatus(node.get('status', 'registered')),
                    description=node.get('description', ''),
                    config=json.loads(node.get('config', '{}')),
                    tags=json.loads(node.get('tags', '[]')),
                    invocation_count=node.get('invocation_count', 0),
                    success_count=node.get('success_count', 0)
                )

                # Add to cache (don't persist again)
                self._modules[module.id] = module
                self._by_type[module.module_type].add(module.id)
                count += 1

            logger.info(f"Loaded {count} modules from memory")
            return count

        except Exception as e:
            logger.warning(f"Failed to load modules: {e}")
            return 0

    def get_stats(self) -> RegistryStats:
        """Get registry statistics."""
        modules_by_type = {}
        for module_type, ids in self._by_type.items():
            if ids:
                modules_by_type[module_type.value] = len(ids)

        total_caps = sum(
            len(m.capabilities) for m in self._modules.values()
        )

        total_invocations = sum(
            m.invocation_count for m in self._modules.values()
        )

        active_count = sum(
            1 for m in self._modules.values()
            if m.status == ModuleStatus.ACTIVE
        )

        return RegistryStats(
            total_modules=len(self._modules),
            active_modules=active_count,
            modules_by_type=modules_by_type,
            total_capabilities=total_caps,
            total_invocations=total_invocations
        )

    def reset(self) -> None:
        """Reset registry state."""
        self._modules.clear()
        self._by_type = {t: set() for t in ModuleType}
        self._by_capability.clear()
        self._by_tag.clear()
        self._core_loaded = False
        logger.info("ModuleRegistry reset")
