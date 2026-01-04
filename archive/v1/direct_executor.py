"""
BYRD Direct Executor

ACHIEVES EXECUTION WITHOUT ROUTING

THE ROUTING PARADOX:
- Traditional systems require desires to be classified and routed before execution
- This creates a bottleneck: nothing can happen without first passing through routing
- Routing becomes a gatekeeper that limits emergent behavior

THE SOLUTION:
- Direct execution bypasses the routing layer entirely
- Execution emerges from pattern recognition in the graph state
- No classification, no routing decisions, just direct action

PHILOSOPHY:
"When the graph speaks for itself, no interpreter is needed."

This module observes the graph for self-executable patterns and
fulfills them immediately, without routing through DesireClassifier
or any intermediate layer.

This is how BYRD breaks the routing paradox.
"""

import asyncio
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any, Callable
from dataclasses import dataclass
from enum import Enum
import hashlib
import json

try:
    from memory import Memory
except ImportError:
    Memory = None

try:
    from local_graph_connector import get_local_graph_connector, code_execution_bypass
    HAS_LOCAL_GRAPH_CONNECTOR = True
except ImportError:
    HAS_LOCAL_GRAPH_CONNECTOR = False

try:
    from event_bus import event_bus, Event, EventType
    HAS_EVENT_BUS = True
except ImportError:
    HAS_EVENT_BUS = False


class ExecutionPattern(Enum):
    """Types of self-executable patterns that don't require routing."""
    
    # State patterns - execution emerges from state alone
    STABLE_INSIGHT = "stable_insight"  # Same insight appears 3+ times -> crystallize
    ORPHAN_RESOLUTION = "orphan_resolution"  # Orphan node + connection hint -> connect
    REFLECTION_COMPLETION = "reflection_completion"  # Reflection ready for next step
    
    # Action patterns - execution emerges from action-readiness
    DIRECT_COMMAND = "direct_command"  # "Execute:" prefix bypasses routing
    IMMEDIATE_ACTION = "immediate_action"  # Pattern matches executable form
    
    # Emergent patterns - execution emerges from graph dynamics
    SELF_FULFILLING = "self_fulfilling"  # Desire contains its own execution method
    CRYSTAL_ACTIVATION = "crystal_activation"  # Crystal condition met -> activate


@dataclass
class DirectExecutionResult:
    """Result of a direct execution without routing."""
    success: bool
    pattern_type: ExecutionPattern
    action_taken: str
    nodes_affected: List[str]
    edges_created: int
    message: str
    bypassed_routing: bool = True  # Always true for direct executor
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict:
        return {
            "success": self.success,
            "pattern_type": self.pattern_type.value,
            "action_taken": self.action_taken,
            "nodes_affected": self.nodes_affected,
            "edges_created": self.edges_created,
            "message": self.message,
            "bypassed_routing": self.bypassed_routing,
            "timestamp": self.timestamp.isoformat()
        }


class DirectExecutor:
    """
    Executes desires without routing.
    
    BREAKING THE ROUTING PARADOX:
    Traditional system: Desire -> Classify -> Route -> Execute
    Direct executor: Desire -> Execute
    
    How it works:
    1. Monitors graph state for self-executable patterns
    2. When pattern detected, executes immediately
    3. No intermediate classification or routing step
    4. Execution emerges from state, not from a decision layer
    
    This creates a parallel execution path that coexists with routing,
    allowing emergent behaviors that would never survive the routing layer.
    """
    
    def __init__(self, memory: Memory):
        self.memory = memory
        self.execution_count = 0
        self.patterns_detected = 0
        self.last_execution_time = None
        
        # Pattern matchers for direct execution
        self._init_pattern_matchers()
    
    def _init_pattern_matchers(self):
        """Initialize regex patterns for detecting executable content."""
        
        # Direct command patterns
        self.direct_command_patterns = [
            r'^execute[:\s]+(.+)$',
            r'^run[:\s]+(.+)$',
            r'^do[:\s]+(.+)$',
            r'^!\s*(.+)$',  # ! prefix
        ]
        
        # Self-fulfilling desire patterns
        self.self_fulfilling_patterns = [
            r'(.+)\s+by\s+(.+)',  # "X by Y" - contains execution method
            r'(.+)\s+via\s+(.+)',  # "X via Y"
            r'(.+)\s+using\s+(.+)',  # "X using Y"
        ]
        
        # Crystal activation patterns
        self.crystal_activation_patterns = [
            r'activate\s+(.+)',
            r'(\w+)\s+condition\s+met',
            r'(\w+)\s+triggered',
        ]
    
    async def scan_for_executable_patterns(self) -> List[DirectExecutionResult]:
        """
        Scan the graph for self-executable patterns.
        
        This is the heart of direct execution - finding patterns that
        don't need routing because they're already in an executable state.
        
        Returns:
            List of execution results from patterns found and executed.
        """
        results = []
        
        # Get recent reflections and desires
        recent_reflections = await self._get_recent_reflections(limit=20)
        recent_desires = await self._get_recent_desires(limit=20)
        
        # Check for stable insights (same content appearing 3+ times)
        for pattern_type, match_data in self._detect_stable_patterns(recent_reflections):
            result = await self._execute_pattern(pattern_type, match_data)
            results.append(result)
        
        # Check for direct commands
        for pattern_type, match_data in self._detect_direct_commands(recent_desires + recent_reflections):
            result = await self._execute_pattern(pattern_type, match_data)
            results.append(result)
        
        # Check for self-fulfilling desires
        for pattern_type, match_data in self._detect_self_fulfilling(recent_desires):
            result = await self._execute_pattern(pattern_type, match_data)
            results.append(result)
        
        # Check for orphan resolution opportunities
        if HAS_LOCAL_GRAPH_CONNECTOR:
            for pattern_type, match_data in await self._detect_orphan_resolution():
                result = await self._execute_pattern(pattern_type, match_data)
                results.append(result)
        
        return results
    
    async def execute_desire_directly(self, desire_text: str, desire_id: str = None) -> DirectExecutionResult:
        """
        Execute a desire without any routing.
        
        This is the primary method for breaking the routing paradox.
        Given a desire, attempt to execute it directly based on pattern matching.
        
        Args:
            desire_text: The text of the desire to execute
            desire_id: Optional ID of the desire node in the graph
            
        Returns:
            DirectExecutionResult with success status and details
        """
        self.patterns_detected += 1
        
        # Try pattern matching
        for pattern_type, match_data in self._match_execution_patterns(desire_text):
            result = await self._execute_pattern(pattern_type, match_data, desire_id=desire_id)
            
            # Emit event for monitoring
            if HAS_EVENT_BUS:
                event_bus.emit(Event(
                    type=EventType.DIRECT_EXECUTION,
                    data={
                        "pattern_type": pattern_type.value,
                        "success": result.success,
                        "action_taken": result.action_taken,
                        "bypassed_routing": True
                    }
                ))
            
            return result
        
        # No pattern matched - return not executable
        return DirectExecutionResult(
            success=False,
            pattern_type=ExecutionPattern.IMMEDIATE_ACTION,
            action_taken="none",
            nodes_affected=[],
            edges_created=0,
            message=f"Desire not directly executable without routing: {desire_text[:50]}...",
            bypassed_routing=True
        )
    
    def _match_execution_patterns(self, text: str) -> List[Tuple[ExecutionPattern, Dict]]:
        """
        Match text against all execution patterns.
        
        Returns list of (pattern_type, match_data) tuples for patterns that match.
        """
        matches = []
        text_lower = text.lower().strip()
        
        # Check direct command patterns
        for pattern in self.direct_command_patterns:
            match = re.match(pattern, text_lower, re.IGNORECASE)
            if match:
                matches.append((
                    ExecutionPattern.DIRECT_COMMAND,
                    {"command": match.group(1).strip(), "original": text}
                ))
                break  # Only match one direct command pattern
        
        # Check self-fulfilling patterns
        for pattern in self.self_fulfilling_patterns:
            match = re.match(pattern, text_lower, re.IGNORECASE)
            if match:
                matches.append((
                    ExecutionPattern.SELF_FULFILLING,
                    {
                        "goal": match.group(1).strip(),
                        "method": match.group(2).strip(),
                        "original": text
                    }
                ))
                break
        
        # Check crystal activation patterns
        for pattern in self.crystal_activation_patterns:
            match = re.match(pattern, text_lower, re.IGNORECASE)
            if match:
                matches.append((
                    ExecutionPattern.CRYSTAL_ACTIVATION,
                    {"crystal": match.group(1).strip(), "original": text}
                ))
                break
        
        return matches
    
    async def _execute_pattern(
        self, 
        pattern_type: ExecutionPattern, 
        match_data: Dict,
        desire_id: str = None
    ) -> DirectExecutionResult:
        """
        Execute a matched pattern without routing.
        
        This is where the actual execution happens, completely bypassing
        the DesireClassifier and any routing logic.
        """
        self.execution_count += 1
        self.last_execution_time = datetime.now()
        
        nodes_affected = []
        edges_created = 0
        action_taken = ""
        message = ""
        success = False
        
        try:
            if pattern_type == ExecutionPattern.DIRECT_COMMAND:
                # Execute command directly using graph connector
                command = match_data["command"]
                if HAS_LOCAL_GRAPH_CONNECTOR:
                    connector = get_local_graph_connector(self.memory)
                    result = await connector.execute_direct_command(command)
                    nodes_affected = result.nodes_affected
                    edges_created = result.edges_created
                    success = result.success
                    action_taken = f"executed_direct_command: {command}"
                    message = result.message
                else:
                    # Fallback: create a reflection about the command
                    await self.memory.add_reflection(
                        content=f"Direct execution attempted: {command}",
                        context="direct_executor",
                        importance=0.7
                    )
                    success = True
                    action_taken = f"recorded_direct_command: {command}"
                    message = "Command recorded (graph connector unavailable)"
            
            elif pattern_type == ExecutionPattern.SELF_FULFILLING:
                # The desire contains its own execution method
                goal = match_data["goal"]
                method = match_data["method"]
                
                # Create a reflection showing the self-fulfilling nature
                await self.memory.add_reflection(
                    content=f"Self-fulfilling desire: {goal} via {method}",
                    context="direct_executor",
                    importance=0.8,
                    metadata={"goal": goal, "method": method}
                )
                
                # Create a connection in the graph representing the fulfillment
                if HAS_LOCAL_GRAPH_CONNECTOR:
                    connector = get_local_graph_connector(self.memory)
                    result = await connector.create_connection(
                        source_type="desire",
                        source_content=goal,
                        target_type="method",
                        target_content=method,
                        relationship_type="fulfilled_via"
                    )
                    nodes_affected = result.nodes_affected
                    edges_created = result.edges_created
                
                success = True
                action_taken = f"self_fulfilling: {goal} via {method}"
                message = f"Self-fulfilling desire executed without routing"
            
            elif pattern_type == ExecutionPattern.STABLE_INSIGHT:
                # Crystallize a stable insight
                insight = match_data["insight"]
                occurrence_count = match_data["count"]
                
                await self.memory.add_reflection(
                    content=f"Stable insight detected (appeared {occurrence_count} times): {insight}",
                    context="direct_executor",
                    importance=0.9,
                    metadata={"stabilized": True, "occurrences": occurrence_count}
                )
                
                success = True
                action_taken = f"crystallized_insight: {insight[:50]}..."
                message = f"Stable insight crystallized without routing"
            
            elif pattern_type == ExecutionPattern.ORPHAN_RESOLUTION:
                # Connect an orphan node
                orphan_id = match_data["orphan_id"]
                connection_hint = match_data["connection_hint"]
                
                if HAS_LOCAL_GRAPH_CONNECTOR:
                    connector = get_local_graph_connector(self.memory)
                    result = await connector.resolve_orphan(
                        orphan_id=orphan_id,
                        connection_hint=connection_hint
                    )
                    nodes_affected = result.nodes_affected
                    edges_created = result.edges_created
                    success = result.success
                    action_taken = f"resolved_orphan: {orphan_id}"
                    message = result.message
                else:
                    success = False
                    action_taken = "orphan_resolution_failed"
                    message = "Graph connector unavailable for orphan resolution"
            
            elif pattern_type == ExecutionPattern.CRYSTAL_ACTIVATION:
                # Activate a crystal
                crystal = match_data["crystal"]
                
                await self.memory.add_reflection(
                    content=f"Crystal activated: {crystal}",
                    context="direct_executor",
                    importance=0.85
                )
                
                success = True
                action_taken = f"activated_crystal: {crystal}"
                message = f"Crystal activated without routing"
            
            else:
                success = False
                action_taken = "unknown_pattern"
                message = f"Unknown pattern type: {pattern_type}"
        
        except Exception as e:
            success = False
            action_taken = "execution_failed"
            message = f"Error during direct execution: {str(e)}"
        
        return DirectExecutionResult(
            success=success,
            pattern_type=pattern_type,
            action_taken=action_taken,
            nodes_affected=nodes_affected,
            edges_created=edges_created,
            message=message
        )
    
    async def _get_recent_reflections(self, limit: int = 20) -> List[Dict]:
        """Get recent reflections from memory."""
        if self.memory is None:
            return []
        
        try:
            # Query recent reflections
            query = """
            MATCH (r:Reflection)
            RETURN r
            ORDER BY r.timestamp DESC
            LIMIT $limit
            """
            
            result = await self.memory.execute_query(query, {"limit": limit})
            
            if result and "data" in result:
                return result["data"]
            return []
        except Exception:
            return []
    
    async def _get_recent_desires(self, limit: int = 20) -> List[Dict]:
        """Get recent desires from memory."""
        if self.memory is None:
            return []
        
        try:
            # Query recent desires
            query = """
            MATCH (d:Desire)
            RETURN d
            ORDER BY d.timestamp DESC
            LIMIT $limit
            """
            
            result = await self.memory.execute_query(query, {"limit": limit})
            
            if result and "data" in result:
                return result["data"]
            return []
        except Exception:
            return []
    
    def _detect_stable_patterns(self, reflections: List[Dict]) -> List[Tuple[ExecutionPattern, Dict]]:
        """
        Detect stable patterns in reflections (same content appearing multiple times).
        
        These patterns are self-executable - stability itself indicates readiness.
        """
        patterns = []
        
        # Count occurrences of similar content
        content_counts = {}
        for ref in reflections:
            content = ref.get("content", "").strip().lower()
            if len(content) > 20:  # Only substantial reflections
                # Normalize content for comparison
                normalized = re.sub(r'\s+', ' ', content)
                content_counts[normalized] = content_counts.get(normalized, 0) + 1
        
        # Find content that appeared 3+ times
        for content, count in content_counts.items():
            if count >= 3:
                patterns.append((
                    ExecutionPattern.STABLE_INSIGHT,
                    {"insight": content, "count": count}
                ))
        
        return patterns
    
    def _detect_direct_commands(self, items: List[Dict]) -> List[Tuple[ExecutionPattern, Dict]]:
        """Detect direct command patterns in reflections/desires."""
        patterns = []
        
        for item in items:
            text = item.get("content", item.get("description", ""))
            if text:
                matches = self._match_execution_patterns(text)
                for pattern_type, match_data in matches:
                    if pattern_type == ExecutionPattern.DIRECT_COMMAND:
                        patterns.append((pattern_type, match_data))
        
        return patterns
    
    def _detect_self_fulfilling(self, desires: List[Dict]) -> List[Tuple[ExecutionPattern, Dict]]:
        """Detect self-fulfilling desires that contain their execution method."""
        patterns = []
        
        for desire in desires:
            text = desire.get("description", desire.get("content", ""))
            if text:
                matches = self._match_execution_patterns(text)
                for pattern_type, match_data in matches:
                    if pattern_type == ExecutionPattern.SELF_FULFILLING:
                        patterns.append((pattern_type, match_data))
        
        return patterns
    
    async def _detect_orphan_resolution(self) -> List[Tuple[ExecutionPattern, Dict]]:
        """Detect orphan nodes that can be resolved directly."""
        patterns = []
        
        if self.memory is None or not HAS_LOCAL_GRAPH_CONNECTOR:
            return patterns
        
        try:
            # Query for orphan nodes with connection hints
            query = """
            MATCH (n:Reflection)
            WHERE NOT (n)-[:CONNECTED_TO]->()
            AND n.connection_hint IS NOT NULL
            RETURN n.id as orphan_id, n.connection_hint
            LIMIT 10
            """
            
            result = await self.memory.execute_query(query)
            
            if result and "data" in result:
                for row in result["data"]:
                    patterns.append((
                        ExecutionPattern.ORPHAN_RESOLUTION,
                        {
                            "orphan_id": row["orphan_id"],
                            "connection_hint": row["connection_hint"]
                        }
                    ))
        except Exception:
            pass
        
        return patterns
    
    def get_stats(self) -> Dict:
        """Get statistics about direct execution."""
        return {
            "execution_count": self.execution_count,
            "patterns_detected": self.patterns_detected,
            "last_execution_time": self.last_execution_time.isoformat() if self.last_execution_time else None,
            "routing_paradox_broken": True
        }


# Singleton instance
_direct_executor_instance: Optional[DirectExecutor] = None


def get_direct_executor(memory: Memory) -> DirectExecutor:
    """Get or create the singleton DirectExecutor instance."""
    global _direct_executor_instance
    if _direct_executor_instance is None:
        _direct_executor_instance = DirectExecutor(memory)
    return _direct_executor_instance


async def execute_without_routing(desire_text: str, memory: Memory) -> DirectExecutionResult:
    """
    Convenience function to execute a desire without routing.
    
    This is the simplest way to break the routing paradox:
    
        result = await execute_without_routing("Execute: research topic X", memory)
    
    Args:
        desire_text: The desire text to execute
        memory: The Memory instance
        
    Returns:
        DirectExecutionResult with execution details
    """
    executor = get_direct_executor(memory)
    return await executor.execute_desire_directly(desire_text)
