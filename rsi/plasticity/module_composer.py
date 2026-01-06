"""
Module Composer - Combine cognitive modules into novel configurations.

Enables composition of modules using different strategies:
- Sequential: Pipeline processing
- Parallel: Concurrent execution
- Conditional: Routing based on input
- Ensemble: Vote/average results

See docs/IMPLEMENTATION_PLAN_ASI.md Section 2.2 for specification.
"""

from typing import Dict, List, Optional, Any, Callable, Tuple
from dataclasses import dataclass, field
import logging
import asyncio
from datetime import datetime, timezone

from .module_types import (
    CognitiveModule,
    ComposedModule,
    CompositionType,
    ModuleType,
    ModuleStatus,
    ModuleCapability,
    create_module_id,
)

logger = logging.getLogger("rsi.plasticity.composer")


@dataclass
class CompositionResult:
    """Result of a composition execution."""
    success: bool
    output: Any
    module_outputs: Dict[str, Any]  # Output from each module
    total_latency_ms: float
    error: Optional[str] = None


@dataclass
class CompositionRule:
    """Rule for validating compositions."""
    name: str
    description: str
    validator: Callable[[List[CognitiveModule], CompositionType], Tuple[bool, str]]


class ModuleComposer:
    """
    Combines modules into novel configurations.

    Composition Types:
    - SEQUENTIAL: Output of A feeds into B
    - PARALLEL: Both run, results merged
    - CONDITIONAL: Route based on condition
    - ENSEMBLE: Vote/average results
    """

    def __init__(self, registry=None, config: Dict = None):
        """
        Initialize composer.

        Args:
            registry: ModuleRegistry for looking up modules
            config: Configuration options
        """
        self.registry = registry
        self.config = config or {}

        # Validation rules
        self._rules: List[CompositionRule] = []
        self._setup_default_rules()

        # Composition history
        self._compositions_created: int = 0
        self._compositions_executed: int = 0

    def _setup_default_rules(self) -> None:
        """Set up default composition validation rules."""
        self._rules = [
            CompositionRule(
                name="minimum_modules",
                description="Composition requires at least 2 modules",
                validator=lambda mods, _: (len(mods) >= 2, "At least 2 modules required")
            ),
            CompositionRule(
                name="status_check",
                description="All modules must be active or registered",
                validator=self._validate_module_status
            ),
            CompositionRule(
                name="composability_check",
                description="Modules must be composable with each other",
                validator=self._validate_composability
            ),
            CompositionRule(
                name="circular_dependency",
                description="No circular dependencies allowed",
                validator=self._validate_no_circular
            ),
        ]

    def _validate_module_status(
        self,
        modules: List[CognitiveModule],
        comp_type: CompositionType
    ) -> Tuple[bool, str]:
        """Validate that all modules have valid status."""
        for module in modules:
            if module.status not in [ModuleStatus.ACTIVE, ModuleStatus.REGISTERED]:
                return False, f"Module {module.name} has invalid status: {module.status.value}"
        return True, ""

    def _validate_composability(
        self,
        modules: List[CognitiveModule],
        comp_type: CompositionType
    ) -> Tuple[bool, str]:
        """Validate that modules can compose with each other."""
        for i, mod1 in enumerate(modules):
            for mod2 in modules[i + 1:]:
                if mod1.composable_with and mod2.module_type not in mod1.composable_with:
                    return False, f"{mod1.name} cannot compose with {mod2.name} (type restriction)"
        return True, ""

    def _validate_no_circular(
        self,
        modules: List[CognitiveModule],
        comp_type: CompositionType
    ) -> Tuple[bool, str]:
        """Validate no circular dependencies."""
        # Check if any module depends on itself through the chain
        module_ids = {m.id for m in modules}

        for module in modules:
            for dep in module.dependencies:
                if dep.module_id in module_ids:
                    # A module in the composition depends on another
                    # This is only circular if the other depends back
                    for other in modules:
                        if other.id == dep.module_id:
                            for other_dep in other.dependencies:
                                if other_dep.module_id == module.id:
                                    return False, f"Circular dependency: {module.name} <-> {other.name}"
        return True, ""

    async def compose(
        self,
        modules: List[CognitiveModule],
        composition_type: CompositionType,
        name: Optional[str] = None,
        config: Dict = None
    ) -> ComposedModule:
        """
        Create new module from combination.

        Args:
            modules: Modules to compose
            composition_type: How to combine them
            name: Optional name for composed module
            config: Composition-specific configuration

        Returns:
            New ComposedModule

        Raises:
            ValueError: If composition is invalid
        """
        # Validate
        for rule in self._rules:
            valid, error = rule.validator(modules, composition_type)
            if not valid:
                raise ValueError(f"Composition rule '{rule.name}' failed: {error}")

        # Generate name if not provided
        if not name:
            name = f"{'+'.join(m.name for m in modules)}"

        # Determine combined type
        combined_type = self._determine_combined_type(modules)

        # Merge capabilities
        merged_caps = self._merge_capabilities(modules, composition_type)

        # Create composed module
        composed = ComposedModule(
            id=create_module_id(),
            name=name,
            module_type=combined_type,
            version="1.0.0",
            status=ModuleStatus.REGISTERED,
            description=f"Composed from: {', '.join(m.name for m in modules)}",
            capabilities=merged_caps,
            source_modules=[m.id for m in modules],
            composition_type=composition_type,
            composition_config=config or {},
            composable_with=self._merge_composability(modules),
            tags=self._merge_tags(modules) + ["composed"],
        )

        self._compositions_created += 1

        logger.info(
            f"Created composed module: {composed.name} "
            f"({composition_type.value} of {len(modules)} modules)"
        )

        return composed

    def _determine_combined_type(
        self,
        modules: List[CognitiveModule]
    ) -> ModuleType:
        """Determine the type of the combined module."""
        types = {m.module_type for m in modules}

        # If all same type, keep it
        if len(types) == 1:
            return types.pop()

        # Otherwise, use META for hybrid
        return ModuleType.META

    def _merge_capabilities(
        self,
        modules: List[CognitiveModule],
        composition_type: CompositionType
    ) -> List[ModuleCapability]:
        """Merge capabilities from source modules."""
        capabilities = []
        seen_names = set()

        for module in modules:
            for cap in module.capabilities:
                if cap.name not in seen_names:
                    # Adjust baseline based on composition type
                    if composition_type == CompositionType.ENSEMBLE:
                        # Ensemble typically improves performance
                        adjusted_baseline = min(cap.performance_baseline * 1.1, 1.0)
                    elif composition_type == CompositionType.SEQUENTIAL:
                        # Sequential may reduce slightly (compound errors)
                        adjusted_baseline = cap.performance_baseline * 0.95
                    else:
                        adjusted_baseline = cap.performance_baseline

                    capabilities.append(ModuleCapability(
                        name=cap.name,
                        description=f"[Composed] {cap.description}",
                        input_schema=cap.input_schema,
                        output_schema=cap.output_schema,
                        performance_baseline=adjusted_baseline
                    ))
                    seen_names.add(cap.name)

        return capabilities

    def _merge_composability(
        self,
        modules: List[CognitiveModule]
    ) -> List[ModuleType]:
        """Merge composability rules from source modules."""
        # Union of all allowed types
        allowed = set()
        for module in modules:
            allowed.update(module.composable_with)
        return list(allowed)

    def _merge_tags(self, modules: List[CognitiveModule]) -> List[str]:
        """Merge tags from source modules."""
        tags = set()
        for module in modules:
            tags.update(module.tags)
        return list(tags)

    async def execute_composed(
        self,
        composed: ComposedModule,
        input_data: Any,
        executors: Dict[str, Callable]
    ) -> CompositionResult:
        """
        Execute a composed module.

        Args:
            composed: The composed module to execute
            input_data: Input to the composition
            executors: Map of module_id -> execution function

        Returns:
            CompositionResult with outputs
        """
        import time
        start = time.time()

        module_outputs = {}

        try:
            if composed.composition_type == CompositionType.SEQUENTIAL:
                output = await self._execute_sequential(
                    composed.source_modules, input_data, executors, module_outputs
                )
            elif composed.composition_type == CompositionType.PARALLEL:
                output = await self._execute_parallel(
                    composed.source_modules, input_data, executors, module_outputs
                )
            elif composed.composition_type == CompositionType.ENSEMBLE:
                output = await self._execute_ensemble(
                    composed.source_modules, input_data, executors, module_outputs
                )
            elif composed.composition_type == CompositionType.CONDITIONAL:
                output = await self._execute_conditional(
                    composed.source_modules, input_data, executors, module_outputs,
                    composed.composition_config
                )
            else:
                raise ValueError(f"Unknown composition type: {composed.composition_type}")

            self._compositions_executed += 1

            return CompositionResult(
                success=True,
                output=output,
                module_outputs=module_outputs,
                total_latency_ms=(time.time() - start) * 1000
            )

        except Exception as e:
            logger.error(f"Composition execution failed: {e}")
            return CompositionResult(
                success=False,
                output=None,
                module_outputs=module_outputs,
                total_latency_ms=(time.time() - start) * 1000,
                error=str(e)
            )

    async def _execute_sequential(
        self,
        module_ids: List[str],
        input_data: Any,
        executors: Dict[str, Callable],
        outputs: Dict
    ) -> Any:
        """Execute modules sequentially, piping outputs."""
        current_input = input_data

        for module_id in module_ids:
            if module_id not in executors:
                raise ValueError(f"No executor for module: {module_id}")

            executor = executors[module_id]
            if asyncio.iscoroutinefunction(executor):
                result = await executor(current_input)
            else:
                result = executor(current_input)

            outputs[module_id] = result
            current_input = result

        return current_input

    async def _execute_parallel(
        self,
        module_ids: List[str],
        input_data: Any,
        executors: Dict[str, Callable],
        outputs: Dict
    ) -> Dict[str, Any]:
        """Execute modules in parallel, return all results."""
        tasks = []

        for module_id in module_ids:
            if module_id not in executors:
                raise ValueError(f"No executor for module: {module_id}")

            executor = executors[module_id]

            async def run_executor(mid, exe):
                if asyncio.iscoroutinefunction(exe):
                    return mid, await exe(input_data)
                else:
                    return mid, exe(input_data)

            tasks.append(run_executor(module_id, executor))

        results = await asyncio.gather(*tasks)

        for module_id, result in results:
            outputs[module_id] = result

        return outputs.copy()

    async def _execute_ensemble(
        self,
        module_ids: List[str],
        input_data: Any,
        executors: Dict[str, Callable],
        outputs: Dict
    ) -> Any:
        """Execute modules and combine results (vote/average)."""
        parallel_results = await self._execute_parallel(
            module_ids, input_data, executors, outputs
        )

        results = list(parallel_results.values())

        # If numeric, average
        if all(isinstance(r, (int, float)) for r in results):
            return sum(results) / len(results)

        # If strings, vote (most common)
        if all(isinstance(r, str) for r in results):
            from collections import Counter
            counts = Counter(results)
            return counts.most_common(1)[0][0]

        # Otherwise return list
        return results

    async def _execute_conditional(
        self,
        module_ids: List[str],
        input_data: Any,
        executors: Dict[str, Callable],
        outputs: Dict,
        config: Dict
    ) -> Any:
        """Execute based on condition routing."""
        condition_fn = config.get('condition')
        if not condition_fn:
            # Default: use first module
            return await self._execute_sequential(
                [module_ids[0]], input_data, executors, outputs
            )

        # Evaluate condition to get module index
        if asyncio.iscoroutinefunction(condition_fn):
            index = await condition_fn(input_data)
        else:
            index = condition_fn(input_data)

        # Clamp to valid range
        index = max(0, min(index, len(module_ids) - 1))

        selected_id = module_ids[index]
        return await self._execute_sequential(
            [selected_id], input_data, executors, outputs
        )

    def add_rule(self, rule: CompositionRule) -> None:
        """Add a custom composition rule."""
        self._rules.append(rule)

    def get_stats(self) -> Dict:
        """Get composer statistics."""
        return {
            'compositions_created': self._compositions_created,
            'compositions_executed': self._compositions_executed,
            'rules_count': len(self._rules)
        }

    def reset(self) -> None:
        """Reset composer state."""
        self._compositions_created = 0
        self._compositions_executed = 0
        logger.info("ModuleComposer reset")
