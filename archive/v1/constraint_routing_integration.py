"""
BYRD Constraint Routing Integration

Demonstrates the orthogonal path for block-aware routing.

This integration shows how to add constraint awareness to the existing
routing system WITHOUT modifying the core routing logic.

Orthogonal Path Architecture:

    Traditional Flow:
    ┌─────────────┐    ┌──────────────────┐    ┌──────────┐
    │   Desire    │ -> │ DesireClassifier  │ -> │ Handler │
    └─────────────┘    └──────────────────┘    └──────────┘

    With ConstraintAwareRouter (Orthogonal Layer):
    ┌─────────────┐    ┌──────────────────┐    ┌──────────────────┐    Handler
    │   Desire    │ -> │ Check Constraints │ -> │ DesireClassifier  │ -> Handler
    └─────────────┘    └──────────────────┘    └──────────────────┘
                          │
                          v (if blocked)
                    ┌──────────────────┐
                    │ Return Block Info │
                    │ + Alternatives    │
                    └──────────────────┘

Key Orthogonal Properties:
1. Zero Modification: Core DesireClassifier unchanged
2. Composable: Can add/remove without breaking system
3. Transparent: Behaves like normal router when no constraints
4. Safe: Always has fallback, never generates blocked code
"""

import asyncio
from typing import Dict, List, Optional, Any

# Import the orthogonal router
from constraint_aware_router import (
    ConstraintAwareRouter,
    RoutingDecision,
    BlockingStrategy,
    ConstraintBlockInfo,
    route_with_constraints
)

# Try to import dependencies
try:
    from memory import Memory
    from desire_classifier import DesireClassifier
    HAS_ALL_DEPS = True
except ImportError:
    HAS_ALL_DEPS = False
    print("Warning: Some dependencies not available. Running in demo mode.")


class MockMemory:
    """Mock memory for testing without full system."""
    
    async def execute_query(self, query: str, params: Dict) -> Dict:
        """Simulate constraint queries."""
        # Simulate a blocked desire
        if "block_me" in params.get("desire_id", ""):
            return {
                "data": [{
                    "constraint_id": "constraint_001",
                    "constraint_type": "safety",
                    "reason": "Test constraint - this pattern is blocked",
                    "blocked_at": "2024-12-19T00:00:00Z",
                    "severity": "high"
                }]
            }
        
        # Simulate pattern-based blocking
        if "dangerous" in params.get("description", ""):
            return {
                "data": [{
                    "constraint_id": "constraint_002",
                    "constraint_type": "security",
                    "pattern": "dangerous",
                    "reason": "Pattern 'dangerous' not allowed",
                    "blocked_at": "2024-12-19T00:00:00Z",
                    "severity": "medium"
                }]
            }
        
        # No block
        return {"data": []}


class MockDesireClassifier:
    """Mock classifier for testing."""
    
    def classify(self, description: str):
        """Simple mock classification."""
        if "learn" in description.lower():
            return type('Result', (), {
                'desire_type': 'CAPABILITY',
                'handler': 'agi_runner',
                'confidence': 0.9,
                'reason': 'Contains learning keyword'
            })()
        return type('Result', (), {
            'desire_type': 'ACTION',
            'handler': 'seeker',
            'confidence': 0.8,
            'reason': 'Default classification'
        })()


class TraditionalRouter:
    """
    Traditional routing WITHOUT constraint awareness.
    
    This represents the existing system that we're wrapping orthogonally.
    """
    
    def __init__(self):
        self.classifier = MockDesireClassifier()
    
    async def route(self, desire: Dict) -> Dict:
        """Route desire to handler."""
        result = self.classifier.classify(desire['description'])
        return {
            "handler": result.handler,
            "type": result.desire_type,
            "confidence": result.confidence
        }


class ConstraintAwareIntegration:
    """
    Integration layer that adds constraint awareness.
    
    This is the ORTHOGONAL implementation - it wraps the
    TraditionalRouter without modifying it.
    """
    
    def __init__(self, memory=None):
        """
        Initialize with optional memory for constraint checking.
        
        The orthogonal design means:
        - If memory is None: routes normally (pass-through)
        - If memory is provided: checks constraints first
        - TraditionalRouter is NEVER modified
        """
        self.traditional_router = TraditionalRouter()
        self.constraint_router = ConstraintAwareRouter(
            memory=memory,
            default_strategy=BlockingStrategy.ALTERNATIVE
        )
    
    async def route_desire(self, desire: Dict) -> Dict:
        """
        Route a desire with orthogonal constraint checking.
        
        Flow:
        1. Check constraints (orthogonal layer)
        2. If blocked: return block info
        3. If clear: route through TraditionalRouter
        
        This demonstrates the orthogonal path - the traditional
        router doesn't know constraints exist.
        """
        # Step 1: Orthogonal constraint check
        decision = await self.constraint_router.route_with_constraints(desire)
        
        if not decision.can_proceed:
            # Blocked - return constraint info
            return {
                "status": "blocked",
                "desire_id": decision.desire_id,
                "block_info": {
                    "constraint_id": decision.block_info.constraint_id,
                    "reason": decision.block_info.reason,
                    "severity": decision.block_info.severity
                },
                "alternatives": decision.alternative_handlers,
                "strategy": decision.blocking_strategy.value
            }
        
        # Step 2: Not blocked - use traditional router
        # (TraditionalRouter is unchanged, doesn't know about constraints)
        traditional_result = await self.traditional_router.route(desire)
        
        return {
            "status": "allowed",
            "desire_id": decision.desire_id,
            "handler": traditional_result["handler"],
            "type": traditional_result["type"],
            "confidence": traditional_result["confidence"],
            "constraints_checked": True
        }


class ByrdDreamRouter:
    """
    Example of integrating into BYRD's dreamer system.
    
    This shows how the orthogonal constraint router can be
    integrated into the dream processing pipeline.
    """
    
    def __init__(self, memory=None):
        self.integration = ConstraintAwareIntegration(memory=memory)
    
    async def process_dream_desires(self, desires: List[Dict]) -> List[Dict]:
        """
        Process multiple desires from a dream.
        
        This replaces the traditional routing with the
        constraint-aware orthogonal version.
        
        The change is ORTHOGONAL because:
        - Dream processing logic unchanged
        - Just swap TraditionalRouter for ConstraintAwareIntegration
        - If constraints are disabled, behaves identically
        """
        results = []
        for desire in desires:
            result = await self.integration.route_desire(desire)
            results.append(result)
        return results


class DecoratorPatternExample:
    """
    Example using the decorator pattern for orthogonal wrapping.
    
    This is even MORE orthogonal - you don't need to change
    any existing code, just add a decorator.
    """
    
    def __init__(self, memory=None):
        from constraint_aware_router import ConstraintAwareRouterDecorator
        self.decorator = ConstraintAwareRouterDecorator(
            memory=memory,
            strategy=BlockingStrategy.ALTERNATIVE
        )
    
    @property
    def route_with_constraints(self):
        """Get the decorator."""
        return self.decorator


# Example usage function
def demonstrate_orthogonal_path():
    """
    Demonstrate the orthogonal constraint routing path.
    
    Run this to see how the system works.
    """
    async def demo():
        # Setup
        memory = MockMemory()
        integration = ConstraintAwareIntegration(memory=memory)
        dream_router = ByrdDreamRouter(memory=memory)
        
        # Test desires
        test_desires = [
            {
                "id": "desire_001",
                "description": "Learn about graph structures"
            },
            {
                "id": "desire_002",
                "description": "Investigate dangerous patterns"
            },
            {
                "id": "block_me",
                "description": "This should be blocked"
            },
            {
                "id": "desire_004",
                "description": "Analyze system capabilities"
            }
        ]
        
        print("=" * 60)
        print("ORTHOGONAL CONSTRAINT ROUTING DEMONSTRATION")
        print("=" * 60)
        
        print("\n--- Processing Individual Desires ---")
        for desire in test_desires:
            result = await integration.route_desire(desire)
            print(f"\nDesire: {desire['id']}")
            print(f"  Description: {desire['description']}")
            print(f"  Status: {result['status']}")
            if result['status'] == 'blocked':
                print(f"  Blocked by: {result['block_info']['constraint_id']}")
                print(f"  Reason: {result['block_info']['reason']}")
                print(f"  Alternatives: {result.get('alternatives', [])}")
            else:
                print(f"  Routed to: {result['handler']}")
        
        print("\n" + "=" * 60)
        print("Processing Batch (Dream Router)")
        print("=" * 60)
        
        results = await dream_router.process_dream_desires(test_desires)
        
        blocked_count = sum(1 for r in results if r['status'] == 'blocked')
        allowed_count = len(results) - blocked_count
        
        print(f"\nTotal desires: {len(results)}")
        print(f"Allowed: {allowed_count}")
        print(f"Blocked: {blocked_count}")
        
        # Get router stats
        print(f"\nRouter Statistics:")
        print(f"  Total routed: {integration.constraint_router.get_stats()['total_routed']}")
        print(f"  Allowed: {integration.constraint_router.get_stats()['allowed']}")
        print(f"  Blocked: {integration.constraint_router.get_stats()['blocked']}")
    
    asyncio.run(demo())


def show_architecture_diagram():
    """Print the architecture diagram."""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║         ORTHOGONAL CONSTRAINT ROUTING ARCHITECTURE              ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  WITHOUT Constraints (Traditional):                              ║
║                                                                  ║
║  ┌──────────┐    ┌──────────────────┐    ┌──────────┐            ║
║  │  Desire  │ -> │ DesireClassifier │ -> │ Handler  │            ║
║  └──────────┘    └──────────────────┘    └──────────┘            ║
║                                                                  ║
║  WITH Constraints (Orthogonal Layer):                          ║
║                                                                  ║
║  ┌──────────┐    ┌──────────────────┐    ┌──────────────────┐      ║
║  │  Desire  │ -> │ Check           │ -> │ DesireClassifier │      ║
║  │          │    │ Constraints     │    │                 │      ║
║  └──────────┘    └────────┬─────────┘    └────────┬─────────┘      ║
║                           │                       │              ║
║                           │ Blocked               │ Allowed       ║
║                           v                       v              ║
║                    ┌──────────────────┐       ┌──────────────────┐        ║
║                    │ Return Block     │       │   Handler        │        ║
║                    │ Info + Alts      │       └──────────────────┘        ║
║                    └──────────────────┘                              ║
║                                                                  ║
╠══════════════════════════════════════════════════════════════════╣
║  Key Benefits of Orthogonal Design:                             ║
║                                                                  ║
║  1. Zero Modification - Core routing unchanged                 ║
║  2. Additive Only - Can enable/disable at runtime              ║
║  3. Safe Fallback - Always has a clear path                    ║
║  4. Transparent - Behaves identically when no constraints       ║
║  5. Testable - Can test constraints independently              ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """)


if __name__ == "__main__":
    show_architecture_diagram()
    print("\nRunning demonstration...\n")
    demonstrate_orthogonal_path()
