"""
BYRD Constraint-Aware Router

Provides orthogonal block-aware routing without using blocked code generation.

This is an ORTHOGONAL path - it wraps the existing DesireClassifier without
modifying it, adding constraint awareness as a separate layer.

Key Design Principles:
1. Orthogonal: Doesn't modify existing routing logic, just wraps it
2. Transparent: Can be enabled/disabled without affecting core routing
3. Non-generative: Doesn't generate code, only routes existing desires
4. Safe: Falls back gracefully when constraints block a desire

The orthogonal path:
- Existing: DesireClassifier -> Handler
- With this: Desire -> Check Constraints -> (if clear) -> DesireClassifier -> Handler
- If blocked: Return block info and alternatives, never generate blocked code
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum

try:
    from memory import Memory
    HAS_MEMORY = True
except ImportError:
    HAS_MEMORY = False

try:
    from desire_classifier import DesireClassifier, DesireType, ClassificationResult
    HAS_DESIRE_CLASSIFIER = True
except ImportError:
    HAS_DESIRE_CLASSIFIER = False


class BlockingStrategy(Enum):
    """How to handle blocked desires."""
    REJECT = "reject"  # Simply reject with block info
    DEFER = "defer"    # Mark for later review
    ALTERNATIVE = "alternative"  # Try alternative routes
    ESCALATE = "escalate"  # Send to human review


@dataclass
class ConstraintBlockInfo:
    """Information about why a desire is blocked."""
    constraint_id: str
    constraint_type: str
    reason: str
    blocked_at: str
    severity: str = "medium"  # low, medium, high, critical


@dataclass
class RoutingDecision:
    """Result of constraint-aware routing."""
    desire_id: Optional[str]
    desire_description: str
    
    # Is this blocked?
    is_blocked: bool = False
    block_info: Optional[ConstraintBlockInfo] = None
    
    # If not blocked, where to route?
    classification: Optional[ClassificationResult] = None
    recommended_handler: Optional[str] = None
    
    # If blocked, what to do?
    blocking_strategy: Optional[BlockingStrategy] = None
    alternative_handlers: List[str] = field(default_factory=list)
    
    # Overall outcome
    can_proceed: bool = True
    message: str = ""
    
    # Trace info
    routing_path: List[str] = field(default_factory=list)


class ConstraintAwareRouter:
    """
    Orthogonal constraint-aware routing layer.
    
    This class WRAPS the existing DesireClassifier without modifying it.
    It adds constraint checking as a separate, orthogonal concern.
    
    Usage:
        router = ConstraintAwareRouter(memory, desire_classifier)
        decision = await router.route_with_constraints(desire)
        
        if decision.can_proceed:
            # Route to recommended_handler
        else:
            # Handle blocked case based on blocking_strategy
    
    The orthogonal path means:
    - Existing routing logic is untouched
    - Constraints are checked BEFORE classification (early exit)
    - No code generation, only routing decisions
    - Can be removed without breaking the system
    """
    
    def __init__(
        self,
        memory: Optional['Memory'] = None,
        desire_classifier: Optional[DesireClassifier] = None,
        default_strategy: BlockingStrategy = BlockingStrategy.ALTERNATIVE
    ):
        """
        Initialize the constraint-aware router.
        
        Args:
            memory: Memory instance for checking constraints
            desire_classifier: Existing DesireClassifier to wrap
            default_strategy: Default strategy for handling blocked desires
        """
        self.memory = memory
        self.desire_classifier = desire_classifier or (DesireClassifier() if HAS_DESIRE_CLASSIFIER else None)
        self.default_strategy = default_strategy
        
        # Routing statistics
        self._stats = {
            "total_routed": 0,
            "blocked": 0,
            "allowed": 0,
            "alternatives_offered": 0
        }
    
    async def route_with_constraints(
        self,
        desire: Dict[str, Any],
        strategy_override: Optional[BlockingStrategy] = None
    ) -> RoutingDecision:
        """
        Route a desire with constraint awareness.
        
        This is the orthogonal path - it wraps the existing routing
        with constraint checking, never generating blocked code.
        
        Args:
            desire: Desire dictionary with at least 'id' and 'description'
            strategy_override: Override default blocking strategy
        
        Returns:
            RoutingDecision with routing information and constraint status
        """
        desire_id = desire.get('id', 'unknown')
        description = desire.get('description', '')
        
        self._stats["total_routed"] += 1
        
        decision = RoutingDecision(
            desire_id=desire_id,
            desire_description=description,
            routing_path=["constraint_aware_router"]
        )
        
        # STEP 1: Check for constraints blocking this desire
        # This is the orthogonal layer - happens BEFORE classification
        if self.memory and HAS_MEMORY:
            block_info = await self._check_constraints(desire_id, description)
            
            if block_info:
                decision.is_blocked = True
                decision.block_info = block_info
                decision.can_proceed = False
                
                # Determine handling strategy
                strategy = strategy_override or self._determine_strategy(block_info)
                decision.blocking_strategy = strategy
                
                # Generate alternatives (orthogonal - don't execute, just suggest)
                alternatives = await self._generate_alternatives(desire, block_info, strategy)
                decision.alternative_handlers = alternatives
                
                decision.message = f"Desire blocked by constraint: {block_info.reason}"
                self._stats["blocked"] += 1
                
                return decision
        
        # STEP 2: No blocks - proceed with normal routing
        decision.routing_path.append("classification")
        
        if self.desire_classifier:
            classification = self.desire_classifier.classify(description)
            decision.classification = classification
            decision.recommended_handler = classification.handler
        else:
            # Fallback: route to seeker if no classifier
            decision.recommended_handler = "seeker"
        
        decision.can_proceed = True
        decision.message = f"Route to {decision.recommended_handler}"
        self._stats["allowed"] += 1
        
        return decision
    
    async def _check_constraints(
        self,
        desire_id: str,
        description: str
    ) -> Optional[ConstraintBlockInfo]:
        """
        Check if any constraints block this desire.
        
        This queries the Neo4j graph for BLOCKED relationships.
        """
        if not self.memory:
            return None
        
        try:
            # Check for direct blocks on this desire
            blocked = await self.memory.execute_query("""
                MATCH (c:Constraint)-[r:BLOCKED]->(d:Desire {id: $desire_id})
                RETURN c.id as constraint_id,
                       c.type as constraint_type,
                       r.reason as reason,
                       r.created_at as blocked_at,
                       c.severity as severity
                LIMIT 1
            """, {"desire_id": desire_id})
            
            if blocked and blocked.get("data"):
                record = blocked["data"][0]
                return ConstraintBlockInfo(
                    constraint_id=record["constraint_id"],
                    constraint_type=record["constraint_type"],
                    reason=record["reason"],
                    blocked_at=record["blocked_at"],
                    severity=record.get("severity", "medium")
                )
            
            # Check for pattern-based blocks (constraints with pattern matching)
            # This allows blocking categories of desires without explicit BLOCKED links
            pattern_blocks = await self.memory.execute_query("""
                MATCH (c:Constraint)
                WHERE c.pattern IS NOT NULL
                AND c.pattern <> ''
                AND $description CONTAINS c.pattern
                RETURN c.id as constraint_id,
                       c.type as constraint_type,
                       c.pattern as pattern,
                       'Pattern match' as reason,
                       datetime() as blocked_at,
                       c.severity as severity
                LIMIT 1
            """, {"description": description})
            
            if pattern_blocks and pattern_blocks.get("data"):
                record = pattern_blocks["data"][0]
                return ConstraintBlockInfo(
                    constraint_id=record["constraint_id"],
                    constraint_type=record["constraint_type"],
                    reason=f"Pattern '{record['pattern']}' not allowed",
                    blocked_at=record["blocked_at"],
                    severity=record.get("severity", "medium")
                )
            
        except Exception as e:
            print(f"Error checking constraints: {e}")
            # On error, proceed without blocking (fail-safe)
            return None
        
        return None
    
    def _determine_strategy(
        self,
        block_info: ConstraintBlockInfo
    ) -> BlockingStrategy:
        """
        Determine how to handle a blocked desire based on constraint properties.
        
        This is orthogonal - it decides HOW to handle, never generates blocked code.
        """
        # Critical constraints always escalate
        if block_info.severity == "critical":
            return BlockingStrategy.ESCALATE
        
        # High severity constraints reject immediately
        if block_info.severity == "high":
            return BlockingStrategy.REJECT
        
        # Medium and low use default strategy (usually alternative)
        return self.default_strategy
    
    async def _generate_alternatives(
        self,
        desire: Dict,
        block_info: ConstraintBlockInfo,
        strategy: BlockingStrategy
    ) -> List[str]:
        """
        Generate alternative handlers for a blocked desire.
        
        ORTHOGONAL PATH:
        - This does NOT generate code
        - This only suggests alternative routing targets
        - The actual execution is handled by the caller
        
        Alternatives are based on:
        1. The constraint type (what's blocked)
        2. The original desire classification
        3. The handling strategy
        """
        alternatives = []
        description = desire.get('description', '')
        
        # Try to classify the desire to understand original intent
        original_handler = None
        if self.desire_classifier:
            classification = self.desire_classifier.classify(description)
            original_handler = classification.handler
        
        # Strategy-based alternatives
        if strategy == BlockingStrategy.ALTERNATIVE:
            # Suggest orthogonal routes that bypass the block
            if block_info.constraint_type == "code_generation":
                # If code generation is blocked, route to reflection
                alternatives.extend(["dreamer", "memory_reasoner"])
            
            if block_info.constraint_type == "modification":
                # If modification is blocked, route to analysis
                alternatives.extend(["seeker", "research"])
            
            # Always add meta handler for meta-analysis of blocks
            alternatives.append("meta_analyzer")
            
        elif strategy == BlockingStrategy.DEFER:
            # Suggest reviewing later
            alternatives.append("deferral_queue")
        
        elif strategy == BlockingStrategy.ESCALATE:
            # Suggest human review
            alternatives.append("human_review")
        
        elif strategy == BlockingStrategy.REJECT:
            # No alternatives, just reject
            alternatives = []
        
        # Track stats
        if alternatives:
            self._stats["alternatives_offered"] += 1
        
        return alternatives
    
    async def batch_route(
        self,
        desires: List[Dict],
        strategy_override: Optional[BlockingStrategy] = None
    ) -> List[RoutingDecision]:
        """
        Route multiple desires with constraint awareness.
        
        Useful for processing batches of desires from the dreamer.
        """
        decisions = []
        for desire in desires:
            decision = await self.route_with_constraints(desire, strategy_override)
            decisions.append(decision)
        return decisions
    
    def get_stats(self) -> Dict[str, int]:
        """Get routing statistics."""
        return self._stats.copy()
    
    def reset_stats(self) -> None:
        """Reset routing statistics."""
        self._stats = {
            "total_routed": 0,
            "blocked": 0,
            "allowed": 0,
            "alternatives_offered": 0
        }


# Convenience function for one-off routing
async def route_with_constraints(
    desire: Dict,
    memory: Optional['Memory'] = None,
    strategy: Optional[BlockingStrategy] = None
) -> RoutingDecision:
    """
    Quick constraint-aware routing without instantiating a router.
    
    This is the orthogonal entry point - can be used anywhere
    without modifying existing routing code.
    """
    router = ConstraintAwareRouter(memory=memory)
    return await router.route_with_constraints(desire, strategy)


class ConstraintAwareRouterDecorator:
    """
    Decorator pattern for adding constraint awareness to existing routers.
    
    This demonstrates the orthogonal path - you can wrap any existing
    routing function without modifying it.
    
    Usage:
        @constraint_aware_decorator
        async def route_desire(desire):
            return existing_router.classify(desire['description'])
    """
    
    def __init__(
        self,
        memory: Optional['Memory'] = None,
        strategy: BlockingStrategy = BlockingStrategy.ALTERNATIVE
    ):
        self.router = ConstraintAwareRouter(memory=memory, default_strategy=strategy)
    
    def __call__(self, func):
        """Decorator that wraps a routing function."""
        async def wrapper(desire: Dict, *args, **kwargs) -> Any:
            # Check constraints first (orthogonal layer)
            decision = await self.router.route_with_constraints(desire)
            
            if not decision.can_proceed:
                # Blocked - return decision, don't call original function
                return decision
            
            # Not blocked - call original routing function
            return await func(desire, *args, **kwargs)
        
        return wrapper
