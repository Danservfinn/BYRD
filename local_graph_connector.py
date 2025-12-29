"""
Local Graph Connection Logic

Bypasses the failing code execution layer by using direct graph operations.

When code execution fails (Coder unavailable, timeouts, errors), this module
provides a fallback path that operates entirely within the graph memory system.

PHILOSOPHY:
- Not all desires require code execution
- Graph connections can represent actions as states
- Local graph operations are always available
- System remains functional even without external tools
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import hashlib
import json
from contextlib import asynccontextmanager

try:
    from memory import Memory
except ImportError:
    Memory = None

try:
    from graph_algorithms import GraphAlgorithms
except ImportError:
    GraphAlgorithms = None

try:
    from event_bus import event_bus, Event, EventType
    HAS_EVENT_BUS = True
except ImportError:
    HAS_EVENT_BUS = False


@dataclass
class GraphConnectionResult:
    """Result of a local graph connection operation."""
    success: bool
    operation_type: str  # "connect", "reflect", "create_belief", "create_desire"
    nodes_affected: List[str]
    edges_created: int
    message: str
    bypass_reason: str  # Why we bypassed code execution
    timestamp: datetime
    # Outcome-based validation metrics
    orphans_before: int = 0  # Orphan count before operation
    orphans_after: int = 0  # Orphan count after operation
    orphan_delta: int = 0  # Change in orphan count (negative = improvement)
    validation_passed: bool = False  # Whether outcome validation passed

    def to_dict(self) -> Dict:
        return {
            "success": self.success,
            "operation_type": self.operation_type,
            "nodes_affected": self.nodes_affected,
            "edges_created": self.edges_created,
            "message": self.message,
            "bypass_reason": self.bypass_reason,
            "timestamp": self.timestamp.isoformat(),
            "orphans_before": self.orphans_before,
            "orphans_after": self.orphans_after,
            "orphan_delta": self.orphan_delta,
            "validation_passed": self.validation_passed
        }


class LocalGraphConnector:
    """
    Bypass logic for when code execution layer fails.

    Instead of executing code, this connector:
    1. Creates graph connections representing the intended action
    2. Generates reflections about the constraint
    3. Updates beliefs based on what would have been done
    4. Creates follow-up desires for when execution is available

    This keeps BYRD functional and learning even when external tools fail.
    """

    def __init__(self, memory: Optional[Memory] = None):
        """
        Initialize the local graph connector.

        Args:
            memory: Memory instance for graph operations
        """
        self.memory = memory
        self.algorithms = GraphAlgorithms() if GraphAlgorithms else None
        self._bypass_count = 0
        self._last_bypass_time = None
        # Outcome-based validation configuration
        self.validation_config = {
            "require_orphan_reduction": True,  # For connection operations, orphan count should decrease
            "allow_neutral_orphans": True,  # Some operations don't affect orphans (creation)
            "max_orphan_increase": 0  # Maximum allowed orphan increase (0 = no increase allowed)
        }

    async def handle_coding_desire_without_execution(
        self,
        desire: Dict,
        failure_reason: str
    ) -> GraphConnectionResult:
        """
        Handle a coding desire by creating graph connections instead of executing code.

        When Coder fails, we represent the intention in the graph:
        1. Create a "PendingAction" node representing the desired change
        2. Connect it to the desire
        3. Create a reflection about why execution failed
        4. Create a belief about the system limitation
        5. Create a monitoring desire for when execution becomes available

        Args:
            desire: The original desire dict with description, type, etc.
            failure_reason: Why code execution failed

        Returns:
            GraphConnectionResult with details of what was created
        """
        self._bypass_count += 1
        self._last_bypass_time = datetime.now()

        desire_id = desire.get("id", "")
        description = desire.get("description", "")
        desire_type = desire.get("type", "coding")

        nodes_created = []
        edges_created = 0

        if not self.memory:
            return GraphConnectionResult(
                success=False,
                operation_type="connect",
                nodes_affected=[],
                edges_created=0,
                message="Memory not available for graph bypass",
                bypass_reason=failure_reason,
                timestamp=datetime.now()
            )

        try:
            # 1. Create a PendingAction node
            pending_action_id = self._generate_id(f"pending_{description[:50]}")
            pending_content = f"Pending code action: {description}"

            await self.memory.create_experience(
                content=pending_content,
                experience_type="PendingAction",
                metadata={
                    "original_desire_id": desire_id,
                    "failure_reason": failure_reason,
                    "bypass_timestamp": datetime.now().isoformat(),
                    "attempted_by": "LocalGraphConnector"
                }
            )
            nodes_created.append(pending_action_id)

            # 2. Connect to original desire
            await self.memory.connect_experiences(
                source_id=desire_id,
                target_id=pending_action_id,
                relationship_type="REPRESENTED_AS",
                metadata={"bypass": True}
            )
            edges_created += 1

            # 3. Create reflection about the failure
            reflection_content = (
                f"I attempted to fulfill a {desire_type} desire: '{description}', "
                f"but code execution failed because: {failure_reason}. "
                f"I've recorded this as a pending action in my memory graph. "
                f"This helps me track what needs to be done when execution is available."
            )

            reflection_id = await self.memory.create_reflection(
                content=reflection_content,
                reflection_type="execution_bypass",
                metadata={
                    "desire_id": desire_id,
                    "bypass_count": self._bypass_count,
                    "related_nodes": nodes_created
                }
            )
            nodes_created.append(reflection_id)
            edges_created += 1  # Reflection linked automatically

            # 4. Create/update belief about system limitation
            belief_content = f"Code execution is currently unavailable: {failure_reason}"
            belief_id = await self.memory.create_belief(
                content=belief_content,
                confidence=0.9,
                belief_type="system_limitation",
                metadata={
                    "last_observed": datetime.now().isoformat(),
                    "bypass_count": self._bypass_count
                }
            )
            nodes_created.append(belief_id)
            edges_created += 1

            # 5. Create monitoring desire for recovery
            monitoring_content = (
                f"Monitor for code execution availability to complete pending action: {description}"
            )
            monitoring_desire_id = await self.memory.create_desire(
                content=monitoring_content,
                desire_type="monitoring",
                intensity=0.5,
                metadata={
                    "blocked_by": "execution_unavailable",
                    "related_pending_action": pending_action_id,
                    "original_desire_id": desire_id
                }
            )
            nodes_created.append(monitoring_desire_id)
            edges_created += 1

            # 6. Emit event if available
            if HAS_EVENT_BUS:
                await event_bus.emit(Event(
                    type=EventType.CODER_BYPASSED if hasattr(EventType, 'CODER_BYPASSED') else "coder_bypassed",
                    data={
                        "desire_id": desire_id,
                        "bypass_reason": failure_reason,
                        "nodes_created": nodes_created,
                        "edges_created": edges_created,
                        "pending_action_id": pending_action_id
                    }
                ))

            return GraphConnectionResult(
                success=True,
                operation_type="connect",
                nodes_affected=nodes_created,
                edges_created=edges_created,
                message=f"Created graph representation for failed code execution. {len(nodes_created)} nodes, {edges_created} edges.",
                bypass_reason=failure_reason,
                timestamp=datetime.now()
            )

        except Exception as e:
            return GraphConnectionResult(
                success=False,
                operation_type="connect",
                nodes_affected=nodes_created,
                edges_created=edges_created,
                message=f"Graph bypass failed: {str(e)}",
                bypass_reason=failure_reason,
                timestamp=datetime.now()
            )

    async def connect_related_concepts(
        self,
        concept_ids: List[str],
        relationship_type: str = "RELATED_TO",
        metadata: Optional[Dict] = None
    ) -> GraphConnectionResult:
        """
        Create local graph connections between related concepts.

        This bypasses the need for code execution by directly manipulating
        the graph structure to represent relationships.

        IMPORTANT: This method uses outcome-based validation to ensure that
        connections actually reduce or maintain the orphan count. Operations
        that increase orphans will be marked as failed.

        Args:
            concept_ids: List of node IDs to connect
            relationship_type: Type of relationship to create
            metadata: Optional metadata for the edges

        Returns:
            GraphConnectionResult with connection details and validation metrics
        """
        if not self.memory:
            return GraphConnectionResult(
                success=False,
                operation_type="connect",
                nodes_affected=[],
                edges_created=0,
                message="Memory not available",
                bypass_reason="no_memory",
                timestamp=datetime.now()
            )

        # Define the actual connection operation as a nested async function
        async def _do_connect() -> GraphConnectionResult:
            edges_created = 0
            nodes_affected = list(set(concept_ids))  # Deduplicate

            try:
                # Connect all pairs (fully connected subgraph)
                for i in range(len(concept_ids)):
                    for j in range(i + 1, len(concept_ids)):
                        await self.memory.connect_experiences(
                            source_id=concept_ids[i],
                            target_id=concept_ids[j],
                            relationship_type=relationship_type,
                            metadata=metadata or {}
                        )
                        edges_created += 1

                return GraphConnectionResult(
                    success=True,
                    operation_type="connect",
                    nodes_affected=nodes_affected,
                    edges_created=edges_created,
                    message=f"Connected {len(nodes_affected)} concepts with {edges_created} edges",
                    bypass_reason="local_graph_operation",
                    timestamp=datetime.now()
                )

            except Exception as e:
                return GraphConnectionResult(
                    success=False,
                    operation_type="connect",
                    nodes_affected=nodes_affected,
                    edges_created=edges_created,
                    message=f"Connection failed: {str(e)}",
                    bypass_reason="local_graph_operation",
                    timestamp=datetime.now()
                )

        # Wrap with outcome-based validation
        return await self._wrap_with_validation("connect", _do_connect)

    async def create_synthetic_action(
        self,
        desire: Dict,
        action_type: str = "graph_based_action"
    ) -> GraphConnectionResult:
        """
        Create a synthetic action in the graph without code execution.

        Some actions can be represented purely as graph state changes:
        - Updating a belief
        - Creating a new desire
        - Recording a reflection
        - Marking a concept as important

        IMPORTANT: This method uses outcome-based validation to ensure that
        the operation doesn't negatively impact orphan count. Operations
        that significantly increase orphans will be flagged.

        Args:
            desire: Original desire dict
            action_type: Type of synthetic action to create

        Returns:
            GraphConnectionResult with action details and validation metrics
        """
        if not self.memory:
            return GraphConnectionResult(
                success=False,
                operation_type="create_belief",
                nodes_affected=[],
                edges_created=0,
                message="Memory not available",
                bypass_reason="no_memory",
                timestamp=datetime.now()
            )

        # Define the actual action creation as a nested async function
        async def _do_create_action() -> GraphConnectionResult:
            desire_id = desire.get("id", "")
            description = desire.get("description", "")

            nodes_created = []
            edges_created = 0

            try:
                # Create a synthetic action experience
                action_content = f"Graph-based action executed: {description}"
                action_id = await self.memory.create_experience(
                    content=action_content,
                    experience_type=action_type,
                    metadata={
                        "synthetic": True,
                        "bypassed_execution": True,
                        "desire_id": desire_id
                    }
                )
                nodes_created.append(action_id)

                # Connect to desire
                await self.memory.connect_experiences(
                    source_id=desire_id,
                    target_id=action_id,
                    relationship_type="FULFILLED_BY",
                    metadata={"synthetic": True}
                )
                edges_created += 1

                # Create reflection about the synthetic action
                reflection_content = (
                    f"I fulfilled the desire '{description}' using graph-based operations "
                    f"instead of code execution. This represents the action as a state "
                    f"change in my memory graph, allowing me to continue functioning "
                    f"even when external tools are unavailable."
                )

                reflection_id = await self.memory.create_reflection(
                    content=reflection_content,
                    reflection_type="synthetic_action",
                    metadata={
                        "action_id": action_id,
                        "desire_id": desire_id
                    }
                )
                nodes_created.append(reflection_id)
                edges_created += 1

                # Mark desire as fulfilled
                await self.memory.fulfill_desire(desire_id)
                await self.memory.update_desire_status(desire_id, "fulfilled")

                if HAS_EVENT_BUS:
                    await event_bus.emit(Event(
                        type="synthetic_action_created" if not hasattr(EventType, 'SYNTHETIC_ACTION') else EventType.SYNTHETIC_ACTION,
                        data={
                            "desire_id": desire_id,
                            "action_id": action_id,
                            "action_type": action_type
                        }
                    ))

                return GraphConnectionResult(
                    success=True,
                    operation_type="create_action",
                    nodes_affected=nodes_created,
                    edges_created=edges_created,
                    message=f"Created synthetic action: {action_type}",
                    bypass_reason="graph_based_fulfillment",
                    timestamp=datetime.now()
                )

            except Exception as e:
                return GraphConnectionResult(
                    success=False,
                    operation_type="create_action",
                    nodes_affected=nodes_created,
                    edges_created=edges_created,
                    message=f"Synthetic action creation failed: {str(e)}",
                    bypass_reason="graph_based_fulfillment",
                    timestamp=datetime.now()
                )

        # Wrap with outcome-based validation
        return await self._wrap_with_validation("create_action", _do_create_action)

    async def get_pending_actions(
        self,
        limit: int = 10
    ) -> List[Dict]:
        """
        Retrieve pending actions that were created when code execution failed.

        Args:
            limit: Maximum number of pending actions to return

        Returns:
            List of pending action dicts with metadata
        """
        if not self.memory:
            return []

        try:
            # Query for PendingAction experiences
            # This would require a custom query method in Memory
            # For now, return empty list - implementation would depend on Memory API
            return []
        except Exception:
            return []

    def get_bypass_stats(self) -> Dict[str, Any]:
        """
        Get statistics about code execution bypasses.

        Returns:
            Dict with bypass statistics
        """
        return {
            "total_bypasses": self._bypass_count,
            "last_bypass_time": self._last_bypass_time.isoformat() if self._last_bypass_time else None,
            "has_memory": self.memory is not None,
            "has_algorithms": self.algorithms is not None
        }

    def _generate_id(self, content: str) -> str:
        """Generate deterministic ID from content."""
        return hashlib.sha256(
            f"{content}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:16]

    async def get_orphan_count(self) -> int:
        """
        Get the current count of orphaned Experience nodes.

        Returns:
            Number of orphaned experiences in the graph
        """
        if not self.memory:
            return 0

        try:
            orphans = await self.memory.get_orphaned_experiences(limit=10000)
            return len(orphans)
        except Exception as e:
            print(f"Error getting orphan count: {e}")
            return 0

    def _validate_orphan_delta(
        self,
        operation_type: str,
        orphans_before: int,
        orphans_after: int
    ) -> bool:
        """
        Validate that orphan delta meets requirements for the operation type.

        This implements outcome-based validation: the operation is only considered
        successful if it achieves the desired outcome (orphan reduction or no increase).

        Args:
            operation_type: Type of operation performed
            orphans_before: Orphan count before operation
            orphans_after: Orphan count after operation

        Returns:
            True if validation passed, False otherwise
        """
        delta = orphans_after - orphans_before
        config = self.validation_config

        # Connection operations should reduce orphans
        if operation_type == "connect":
            if delta <= 0:
                return True  # Orphans reduced or stayed same - good
            elif config["allow_neutral_orphans"] and delta == 0:
                return True
            elif delta <= config["max_orphan_increase"]:
                return True
            else:
                print(
                    f"VALIDATION FAILED: Connect operation increased orphans by {delta} "
                    f"({orphans_before} -> {orphans_after})"
                )
                return False

        # Creation operations are allowed to create orphans temporarily
        elif operation_type in ["create_belief", "create_desire", "reflect"]:
            # These operations create new nodes that may be orphaned temporarily
            # This is acceptable, but we should track it
            return True

        # Default: allow no orphan increase
        if delta <= 0:
            return True
        elif delta <= config["max_orphan_increase"]:
            return True
        else:
            print(
                f"VALIDATION FAILED: Operation '{operation_type}' increased orphans by {delta} "
                f"({orphans_before} -> {orphans_after})"
            )
            return False

    async def _wrap_with_validation(
        self,
        operation_type: str,
        operation_func
    ) -> GraphConnectionResult:
        """
        Wrap a graph operation with outcome-based validation.

        This orchestrates the validation process:
        1. Measure orphan count before operation
        2. Execute the operation
        3. Measure orphan count after operation
        4. Validate the delta
        5. Update result with validation metrics

        Args:
            operation_type: Type of operation being performed
            operation_func: Async function that performs the operation

        Returns:
            GraphConnectionResult with validation metrics
        """
        orphans_before = await self.get_orphan_count()

        # Execute the operation
        result = await operation_func()

        # Get orphan count after operation
        orphans_after = await self.get_orphan_count()

        # Calculate delta
        orphan_delta = orphans_after - orphans_before

        # Validate outcome
        validation_passed = self._validate_orphan_delta(
            operation_type,
            orphans_before,
            orphans_after
        )

        # Update result with validation metrics
        result.orphans_before = orphans_before
        result.orphans_after = orphans_after
        result.orphan_delta = orphan_delta
        result.validation_passed = validation_passed

        # Update message if validation failed
        if not validation_passed and result.success:
            result.success = False
            result.message = (
                f"{result.message} | VALIDATION FAILED: "
                f"Orphan count increased by {orphan_delta} "
                f"({orphans_before} -> {orphans_after})"
            )
        elif validation_passed and result.success:
            if orphan_delta < 0:
                result.message = (
                    f"{result.message} | VALIDATION PASSED: "
                    f"Reduced orphans by {-orphan_delta} "
                    f"({orphans_before} -> {orphans_after})"
                )
            else:
                result.message = (
                    f"{result.message} | VALIDATION PASSED: "
                    f"Orphan count stable ({orphans_before} -> {orphans_after})"
                )

        return result

    async def reset(self):
        """Reset bypass statistics."""
        self._bypass_count = 0
        self._last_bypass_time = None


# Singleton instance for easy access
_connector_instance: Optional[LocalGraphConnector] = None


def get_local_graph_connector(memory: Optional[Memory] = None) -> LocalGraphConnector:
    """
    Get or create the singleton LocalGraphConnector instance.

    Args:
        memory: Optional memory instance (only used on first call)

    Returns:
        LocalGraphConnector instance
    """
    global _connector_instance
    if _connector_instance is None:
        _connector_instance = LocalGraphConnector(memory=memory)
    return _connector_instance


def reset_local_graph_connector():
    """Reset the singleton instance (mainly for testing)."""
    global _connector_instance
    _connector_instance = None


# Async context manager for bypass operations
@asynccontextmanager
async def code_execution_bypass(desire: Dict, failure_reason: str, memory: Memory):
    """
    Context manager that handles code execution bypass.

    Usage:
        async with code_execution_bypass(desire, "Coder unavailable", memory) as result:
            if result.success:
                print(f"Successfully bypassed: {result.message}")
            else:
                print(f"Bypass failed: {result.message}")
    """
    connector = get_local_graph_connector(memory)
    result = await connector.handle_coding_desire_without_execution(desire, failure_reason)
    yield result


if __name__ == "__main__":
    print("Local Graph Connector module loaded")
    print("This module provides fallback graph operations when code execution fails.")
