"""
BYRD Compounding Orchestrator
Cross-activation of Memory Reasoner and Goal Evolver loops.

This module establishes the first compounding cycle between Loop 1 (Memory Reasoner)
and Loop 3 (Goal Evolver). The key insight:

    Memory Reasoner learns patterns from experience.
    Goal Evolver discovers which goals produce growth.
    
    When combined:
    - Goals that align with successful memory patterns get boosted fitness
    - Memory patterns that support high-fitness goals get strengthened
    - Both loops converge on patterns that maximize capability growth

THE COMPOUNDING CYCLE:
1. Goal Evolver generates candidate goals
2. Memory Reasoner evaluates goals against historical patterns
3. Goals aligned with successful patterns get fitness boost
4. Executed goals create new experiences
5. Successful experiences reinforce memory patterns
6. Repeat with improved patterns and goals

This is positive feedback: better memory → better goals → better experiences → better memory
"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from collections import defaultdict
import statistics

from event_bus import event_bus, Event, EventType
from memory import Memory
from llm_client import LLMClient

logger = logging.getLogger(__name__)


@dataclass
class PatternMatch:
    """A match between a goal and memory pattern."""
    pattern_id: str
    pattern_type: str  # 'capability_gain', 'efficient_action', 'successful_strategy'
    confidence: float
    supporting_nodes: List[str]
    historical_success_rate: float


@dataclass
class CompoundingMetrics:
    """Metrics for the compounding cycle."""
    cycle_count: int = 0
    goals_pattern_matched: int = 0
    fitness_boosts_applied: float = 0.0
    memory_nodes_reinforced: int = 0
    avg_pattern_confidence: float = 0.0
    capability_growth_rate: float = 0.0
    last_cycle_time: Optional[datetime] = None


class CompoundingOrchestrator:
    """
    Orchestrates cross-activation between Memory Reasoner and Goal Evolver.
    
    The orchestrator:
    1. Listens to events from both loops
    2. Identifies patterns connecting goals and memory
    3. Boosts fitness of goals that align with successful patterns
    4. Reinforces memory patterns that support high-fitness goals
    5. Tracks the compounding effect over time
    
    This creates a virtuous cycle where:
    - Better memory reasoning → smarter goal selection → more capability growth → richer memory
    """

    def __init__(
        self,
        memory: Memory,
        llm_client: LLMClient,
        config: Optional[Dict] = None
    ):
        self.memory = memory
        self.llm_client = llm_client
        self.config = config or {}

        # Configuration
        self.pattern_confidence_threshold = self.config.get(
            "pattern_confidence_threshold", 0.6
        )
        self.fitness_boost_multiplier = self.config.get(
            "fitness_boost_multiplier", 1.5
        )
        self.memory_reinforcement_strength = self.config.get(
            "memory_reinforcement_strength", 0.2
        )
        self.min_cycles_for_compounding = self.config.get(
            "min_cycles_for_compounding", 3
        )

        # State
        self._metrics = CompoundingMetrics()
        self._active_patterns: Dict[str, Dict] = {}  # pattern_id -> pattern data
        self._goal_pattern_matches: Dict[str, List[PatternMatch]] = defaultdict(list)
        self._is_running = False
        self._event_handlers = []

        # Cache for pattern discovery
        self._pattern_cache: Dict[str, List[Dict]] = {}
        self._cache_ttl = 300  # 5 minutes
        self._last_pattern_discovery: Optional[datetime] = None

    async def start(self) -> None:
        """Start the compounding orchestrator."""
        if self._is_running:
            logger.warning("Compounding Orchestrator already running")
            return

        logger.info("Starting Compounding Orchestrator")
        self._is_running = True

        # Register event handlers
        self._register_handlers()

        # Emit start event
        await event_bus.emit(Event(
            type=EventType.MEMORY_CRYSTALLIZED,
            data={"orchestrator": "compounding", "status": "started"},
            source="CompoundingOrchestrator"
        ))

    async def stop(self) -> None:
        """Stop the compounding orchestrator."""
        if not self._is_running:
            return

        logger.info("Stopping Compounding Orchestrator")
        self._is_running = False

        # Unregister handlers
        for handler_id in self._event_handlers:
            event_bus.remove_handler(handler_id)
        self._event_handlers.clear()

    def _register_handlers(self) -> None:
        """Register event bus handlers."""
        # Goal events - trigger pattern matching
        handler1 = event_bus.add_handler(
            EventType.GOAL_GENERATED,
            self._on_goal_generated
        )
        
        handler2 = event_bus.add_handler(
            EventType.GOAL_FITNESS_EVALUATED,
            self._on_goal_fitness_evaluated
        )

        # Memory events - reinforce successful patterns
        handler3 = event_bus.add_handler(
            EventType.MEMORY_REASONING_ANSWER,
            self._on_memory_reasoning_answer
        )

        handler4 = event_bus.add_handler(
            EventType.CAPABILITY_IMPROVED,
            self._on_capability_improved
        )

        # Goal completion - learn what works
        handler5 = event_bus.add_handler(
            EventType.GOAL_COMPLETED,
            self._on_goal_completed
        )

        self._event_handlers.extend([handler1, handler2, handler3, handler4, handler5])

    async def _on_goal_generated(self, event: Event) -> None:
        """
        When a goal is generated, match it against memory patterns.
        
        Goals that align with historically successful patterns get
        a fitness boost, making them more likely to be selected.
        """
        try:
            goal_data = event.data
            goal_id = goal_data.get("id")
            goal_description = goal_data.get("description", "")

            if not goal_id or not goal_description:
                return

            # Find matching patterns
            matches = await self._find_pattern_matches(goal_description, goal_id)

            if matches:
                self._goal_pattern_matches[goal_id] = matches
                self._metrics.goals_pattern_matched += 1
                
                # Calculate confidence boost
                avg_confidence = statistics.mean(m.confidence for m in matches)
                
                logger.info(
                    f"Goal {goal_id} matched {len(matches)} patterns "
                    f"(avg confidence: {avg_confidence:.2f})"
                )

                # Store for fitness evaluation
                await self._store_pattern_boost(goal_id, matches)

        except Exception as e:
            logger.error(f"Error processing goal generated event: {e}")

    async def _on_goal_fitness_evaluated(self, event: Event) -> None:
        """
        Apply pattern-based fitness boost if applicable.
        
        Goals that matched successful memory patterns get their fitness
        multiplied by the boost factor.
        """
        try:
            goal_id = event.data.get("id")
            base_fitness = event.data.get("fitness", 0.0)

            if not goal_id or goal_id not in self._goal_pattern_matches:
                return

            matches = self._goal_pattern_matches[goal_id]
            
            # Calculate boost based on pattern quality
            pattern_scores = [
                m.confidence * m.historical_success_rate 
                for m in matches
            ]
            avg_pattern_score = statistics.mean(pattern_scores)

            # Apply boost if patterns are strong enough
            if avg_pattern_score >= self.pattern_confidence_threshold:
                fitness_boost = self.fitness_boost_multiplier
                boosted_fitness = min(base_fitness * fitness_boost, 1.0)
                fitness_delta = boosted_fitness - base_fitness

                self._metrics.fitness_boosts_applied += fitness_delta

                logger.info(
                    f"Applied fitness boost to goal {goal_id}: "
                    f"{base_fitness:.3f} → {boosted_fitness:.3f} "
                    f"(delta: {fitness_delta:.3f})"
                )

                # Update the goal in memory with boosted fitness
                await self._update_goal_fitness(goal_id, boosted_fitness)

                # Emit boost event
                await event_bus.emit(Event(
                    type=EventType.CAPABILITY_IMPROVED,
                    data={
                        "goal_id": goal_id,
                        "boost_type": "pattern_match",
                        "base_fitness": base_fitness,
                        "boosted_fitness": boosted_fitness,
                        "pattern_count": len(matches)
                    },
                    source="CompoundingOrchestrator"
                ))

        except Exception as e:
            logger.error(f"Error processing fitness evaluated event: {e}")

    async def _on_memory_reasoning_answer(self, event: Event) -> None:
        """
        When memory reasoning produces high-confidence answers,
        reinforce the memory patterns involved.
        
        This strengthens the connections that lead to good answers.
        """
        try:
            result = event.data
            confidence = result.get("confidence", 0.0)
            source_nodes = result.get("source_nodes", [])

            # Only reinforce high-confidence answers
            if confidence >= self.pattern_confidence_threshold and source_nodes:
                await self._reinforce_memory_nodes(source_nodes, confidence)
                self._metrics.memory_nodes_reinforced += len(source_nodes)

                # Track which patterns produced good results
                for node_id in source_nodes:
                    await self._track_pattern_success(node_id, confidence)

        except Exception as e:
            logger.error(f"Error processing memory reasoning answer: {e}")

    async def _on_capability_improved(self, event: Event) -> None:
        """
        When capability improves, identify what led to it.
        
        This connects capability gains back to the goals and patterns
        that produced them.
        """
        try:
            capability_delta = event.data.get("capability_delta", 0.0)
            goal_id = event.data.get("goal_id")

            if capability_delta > 0:
                self._metrics.capability_growth_rate = (
                    self._metrics.capability_growth_rate * 0.9 + capability_delta * 0.1
                )

                # If this came from a goal, reinforce that goal's patterns
                if goal_id and goal_id in self._goal_pattern_matches:
                    matches = self._goal_pattern_matches[goal_id]
                    for match in matches:
                        await self._update_pattern_success_rate(
                            match.pattern_id,
                            capability_delta
                        )

                logger.info(
                    f"Capability improved by {capability_delta:.3f}. "
                    f"Current growth rate: {self._metrics.capability_growth_rate:.3f}"
                )

        except Exception as e:
            logger.error(f"Error processing capability improved event: {e}")

    async def _on_goal_completed(self, event: Event) -> None:
        """
        When a goal completes successfully, learn from it.
        
        Extract patterns that can guide future goal selection.
        """
        try:
            goal_id = event.data.get("id")
            success = event.data.get("success", True)
            capability_delta = event.data.get("capability_delta", 0.0)

            if success and capability_delta > 0:
                # This goal produced growth - analyze what made it successful
                await self._extract_success_patterns(goal_id, event.data)
                
                self._metrics.cycle_count += 1
                self._metrics.last_cycle_time = datetime.now()

        except Exception as e:
            logger.error(f"Error processing goal completed event: {e}")

    async def _find_pattern_matches(
        self,
        goal_description: str,
        goal_id: str
    ) -> List[PatternMatch]:
        """
        Find memory patterns that match the goal description.
        
        Returns list of PatternMatch objects with confidence scores.
        """
        try:
            # Check cache first
            cache_key = f"pattern:{hash(goal_description)}"
            if cache_key in self._pattern_cache:
                cached = self._pattern_cache[cache_key]
                if self._is_cache_valid(cached):
                    return self._convert_to_pattern_matches(cached["matches"])

            # Discover patterns from memory
            # Query for similar successful experiences
            query = f"""
            What patterns and strategies have been successful for goals similar to:
            "{goal_description}"
            
            Consider:
            - What types of capabilities were gained
            - What approaches were most efficient
            - What strategies led to completion
            """

            # Use memory to find relevant patterns
            result = await self.memory.semantic_search(
                query,
                filters={
                    "labels": ["experience", "belief", "strategy"],
                    "min_confidence": 0.6
                },
                limit=10
            )

            matches = []
            for node in result.get("nodes", []):
                node_id = node.get("id")
                node_type = node.get("labels", [""])[0]
                content = node.get("content", "")
                confidence = node.get("similarity", 0.0)

                # Get historical success rate for this pattern
                success_rate = await self._get_pattern_success_rate(node_id)

                if confidence >= self.pattern_confidence_threshold:
                    matches.append({
                        "pattern_id": node_id,
                        "pattern_type": node_type,
                        "confidence": confidence,
                        "supporting_nodes": [node_id],
                        "historical_success_rate": success_rate
                    })

            # Cache results
            self._pattern_cache[cache_key] = {
                "matches": matches,
                "timestamp": datetime.now()
            }

            return self._convert_to_pattern_matches(matches)

        except Exception as e:
            logger.error(f"Error finding pattern matches: {e}")
            return []

    def _convert_to_pattern_matches(self, matches: List[Dict]) -> List[PatternMatch]:
        """Convert dict matches to PatternMatch objects."""
        return [
            PatternMatch(
                pattern_id=m["pattern_id"],
                pattern_type=m["pattern_type"],
                confidence=m["confidence"],
                supporting_nodes=m["supporting_nodes"],
                historical_success_rate=m["historical_success_rate"]
            )
            for m in matches
        ]

    def _is_cache_valid(self, cached: Dict) -> bool:
        """Check if cache entry is still valid."""
        if "timestamp" not in cached:
            return False
        age = (datetime.now() - cached["timestamp"]).total_seconds()
        return age < self._cache_ttl

    async def _store_pattern_boost(
        self,
        goal_id: str,
        matches: List[PatternMatch]
    ) -> None:
        """Store pattern boost information for later use."""
        try:
            # Store as a transient property or in a separate tracking structure
            # For now, we keep it in memory since we also track in _goal_pattern_matches
            pass
        except Exception as e:
            logger.error(f"Error storing pattern boost: {e}")

    async def _update_goal_fitness(self, goal_id: str, new_fitness: float) -> None:
        """Update a goal's fitness in memory."""
        try:
            await self.memory.update_node(
                goal_id,
                properties={
                    "fitness": new_fitness,
                    "fitness_boosted_at": datetime.now().isoformat()
                }
            )
        except Exception as e:
            logger.error(f"Error updating goal fitness: {e}")

    async def _reinforce_memory_nodes(
        self,
        node_ids: List[str],
        confidence: float
    ) -> None:
        """Reinforce memory nodes that produced good results."""
        try:
            for node_id in node_ids:
                # Boost the node's importance/confidence
                boost_amount = confidence * self.memory_reinforcement_strength
                
                await self.memory.update_node(
                    node_id,
                    properties={
                        "reinforcement_count": self._safe_increment(node_id, "reinforcement_count"),
                        "last_reinforced_at": datetime.now().isoformat(),
                        "importance_boost": boost_amount
                    }
                )

                # Create connections between reinforced nodes
                if len(node_ids) > 1:
                    await self._create_pattern_connections(node_ids)

        except Exception as e:
            logger.error(f"Error reinforcing memory nodes: {e}")

    def _safe_increment(self, node_id: str, property_name: str) -> int:
        """Safely increment a node property."""
        try:
            node_data = self.memory._nodes.get(node_id, {})
            current = node_data.get(property_name, 0)
            return current + 1
        except Exception:
            return 1

    async def _create_pattern_connections(self, node_ids: List[str]) -> None:
        """Create connections between nodes that fired together."""
        try:
            for i in range(len(node_ids)):
                for j in range(i + 1, len(node_ids)):
                    await self.memory.create_connection(
                        node_ids[i],
                        node_ids[j],
                        connection_type="pattern_coactivation",
                        strength=0.5,
                        metadata={
                            "created_by": "CompoundingOrchestrator",
                            "created_at": datetime.now().isoformat()
                        }
                    )
        except Exception as e:
            logger.error(f"Error creating pattern connections: {e}")

    async def _track_pattern_success(self, node_id: str, confidence: float) -> None:
        """Track that a pattern produced a successful result."""
        try:
            if node_id not in self._active_patterns:
                self._active_patterns[node_id] = {
                    "success_count": 0,
                    "total_uses": 0,
                    "avg_confidence": 0.0
                }

            pattern = self._active_patterns[node_id]
            pattern["success_count"] += 1
            pattern["total_uses"] += 1
            pattern["avg_confidence"] = (
                pattern["avg_confidence"] * (pattern["success_count"] - 1) + confidence
            ) / pattern["success_count"]

        except Exception as e:
            logger.error(f"Error tracking pattern success: {e}")

    async def _update_pattern_success_rate(
        self,
        pattern_id: str,
        capability_delta: float
    ) -> None:
        """Update the success rate for a pattern based on capability gain."""
        try:
            if pattern_id not in self._active_patterns:
                return

            pattern = self._active_patterns[pattern_id]
            # Weight success by capability delta
            weighted_success = capability_delta
            
            pattern["weighted_success"] = pattern.get("weighted_success", 0.0) + weighted_success
            pattern["last_updated"] = datetime.now().isoformat()

        except Exception as e:
            logger.error(f"Error updating pattern success rate: {e}")

    async def _get_pattern_success_rate(self, pattern_id: str) -> float:
        """Get the historical success rate for a pattern."""
        try:
            if pattern_id not in self._active_patterns:
                # Try to get from memory
                node = await self.memory.get_node(pattern_id)
                if node:
                    return node.get("historical_success_rate", 0.5)
                return 0.5  # Default neutral

            pattern = self._active_patterns[pattern_id]
            if pattern["total_uses"] == 0:
                return 0.5
            
            return pattern["success_count"] / pattern["total_uses"]

        except Exception as e:
            logger.error(f"Error getting pattern success rate: {e}")
            return 0.5

    async def _extract_success_patterns(
        self,
        goal_id: str,
        completion_data: Dict
    ) -> None:
        """
        Extract patterns from a successful goal completion.
        
        Analyze what made this goal successful and create
        learnable patterns for future goals.
        """
        try:
            # Get the goal details
            goal = await self.memory.get_node(goal_id)
            if not goal:
                return

            # Create a success pattern belief
            pattern_content = f"""
            Success pattern from goal: {goal.get('description', 'Unknown')}
            
            Key factors:
            - Capability gained: {completion_data.get('capability_delta', 0):.3f}
            - Resources used: {completion_data.get('resources_used', 'unknown')}
            - Time to complete: {completion_data.get('completion_time', 'unknown')}
            - Strategy: {completion_data.get('strategy', 'unknown')}
            """

            # Create belief node
            pattern_id = await self.memory.create_belief(
                content=pattern_content,
                confidence=0.7,
                metadata={
                    "pattern_type": "successful_goal",
                    "source_goal": goal_id,
                    "extracted_at": datetime.now().isoformat(),
                    "capability_delta": completion_data.get("capability_delta", 0.0)
                }
            )

            # Connect pattern to goal
            await self.memory.create_connection(
                goal_id,
                pattern_id,
                connection_type="produced_pattern",
                strength=0.8
            )

            logger.info(f"Extracted success pattern {pattern_id} from goal {goal_id}")

        except Exception as e:
            logger.error(f"Error extracting success patterns: {e}")

    def get_metrics(self) -> Dict[str, Any]:
        """Get current compounding metrics."""
        return {
            "cycle_count": self._metrics.cycle_count,
            "goals_pattern_matched": self._metrics.goals_pattern_matched,
            "total_fitness_boost": self._metrics.fitness_boosts_applied,
            "memory_nodes_reinforced": self._metrics.memory_nodes_reinforced,
            "capability_growth_rate": self._metrics.capability_growth_rate,
            "active_patterns": len(self._active_patterns),
            "is_compounding": self._is_compounding(),
            "last_cycle_time": self._metrics.last_cycle_time.isoformat() if self._metrics.last_cycle_time else None
        }

    def _is_compounding(self) -> bool:
        """
        Check if the system is experiencing compounding growth.
        
        Compounding is detected when:
        - Multiple cycles have completed
        - Fitness boosts are being applied consistently
        - Capability growth rate is positive
        """
        if self._metrics.cycle_count < self.min_cycles_for_compounding:
            return False

        if self._metrics.fitness_boosts_applied < 1.0:
            return False

        if self._metrics.capability_growth_rate <= 0:
            return False

        return True

    def is_healthy(self) -> bool:
        """Check if the compounding cycle is healthy."""
        # Health requires active compounding
        if not self._is_compounding():
            return self._metrics.cycle_count < self.min_cycles_for_compounding

        # Healthy compounding requires positive growth and active patterns
        return (
            self._metrics.capability_growth_rate > 0.01 and
            len(self._active_patterns) >= 3
        )


async def create_compounding_orchestrator(
    memory: Memory,
    llm_client: LLMClient,
    config: Optional[Dict] = None
) -> CompoundingOrchestrator:
    """
    Factory function to create and configure a CompoundingOrchestrator.
    
    Args:
        memory: The Memory instance
        llm_client: The LLM client for pattern analysis
        config: Optional configuration dictionary
        
    Returns:
        Configured CompoundingOrchestrator instance
    """
    orchestrator = CompoundingOrchestrator(memory, llm_client, config)
    await orchestrator.start()
    return orchestrator
