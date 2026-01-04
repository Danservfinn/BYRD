"""
BYRD Orthogonal Block-Aware Routing - Complete Demo

This file demonstrates the ORTHOGONAL PATH for implementing block-aware routing
WITHOUT using blocked code generation.

=== THE ORTHOGONAL PATH ===

Traditional Approach (Modifies Core):
  DesireClassifier.route() -> adds constraint checking inline
  Problem: Tight coupling, hard to disable, violates separation of concerns

Orthogonal Approach (Wraps Core):
  ConstraintAwareRouter -> wraps DesireClassifier
  - Check constraints FIRST (early exit)
  - If clear: delegate to wrapped router
  - If blocked: return block info + alternatives
  - NEVER generates blocked code

=== KEY ORTHOGONAL PROPERTIES ===

1. ZERO MODIFICATION: Core DesireClassifier remains unchanged
2. COMPOSABLE: Can add/remove without breaking system  
3. TRANSPARENT: Behaves normally when no constraints present
4. NON-GENERATIVE: Returns decisions, never generates blocked code
5. SAFE: Always has fallback paths

=== ARCHITECTURE ===

    Without ConstraintAwareRouter:
    ┌─────────────┐    ┌──────────────────┐    ┌──────────┐
    │   Desire    │ -> │ DesireClassifier  │ -> │ Handler │
    └─────────────┘    └──────────────────┘    └──────────┘

    With ConstraintAwareRouter (Orthogonal Layer):
    ┌─────────────┐    ┌──────────────────┐    ┌──────────────────┐    ┌──────────┐
    │   Desire    │ -> │ Check Constraints │ -> │ DesireClassifier  │ -> │ Handler │
    └─────────────┘    └──────────────────┘    └──────────────────┘    └──────────┘
                          │
                          v (if blocked)
                    ┌──────────────────┐
                    │ Return Block Info │
                    │ + Alternatives    │
                    └──────────────────┘

Usage:
    # Wrap existing router
    router = ConstraintAwareRouter(memory=memory)
    decision = await router.route_with_constraints(desire)
    
    if decision.can_proceed:
        # Use decision.recommended_handler
    else:
        # Handle based on decision.blocking_strategy
"""

import asyncio
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

# Import orthogonal components
from constraint_aware_router import (
    ConstraintAwareRouter,
    RoutingDecision,
    ConstraintBlockInfo,
    BlockingStrategy,
    route_with_constraints
)


# ============================================================================
# DEMO 1: Basic Orthogonal Wrapping
# ============================================================================

class ExistingRouter:
    """Represents the EXISTING routing system (before orthogonal layer)."""
    
    def __init__(self):
        # Simulate existing router logic
        self.handlers = {
            'capability': 'agi_runner',
            'philosophical': 'goal_evolver', 
            'action': 'seeker',
            'meta': 'meta_analyzer'
        }
    
    def classify(self, description: str) -> str:
        """Original classification logic (unchanged)."""
        description = description.lower()
        if any(k in description for k in ['learn', 'improve', 'build']):
            return self.handlers['capability']
        elif any(k in description for k in ['accept', 'embrace', 'continue']):
            return self.handlers['philosophical']
        elif any(k in description for k in ['search', 'find', 'investigate']):
            return self.handlers['action']
        return self.handlers['meta']


class OrthogonalRouter:
    """
    Orthogonal wrapper that adds constraint awareness.
    
    KEY: This does NOT modify ExistingRouter!
    It simply wraps it with constraint checking.
    """
    
    def __init__(self, memory=None, existing_router=None):
        self.existing_router = existing_router or ExistingRouter()
        self.constraint_router = ConstraintAwareRouter(
            memory=memory,
            default_strategy=BlockingStrategy.ALTERNATIVE
        )
    
    async def route(self, desire: Dict) -> Dict:
        """
        Orthogonal routing with constraint awareness.
        
        The orthogonal path:
        1. Check constraints (orthogonal layer)
        2. If blocked: return block info (NEVER generates code)
        3. If clear: delegate to existing router
        """
        # Step 1: Check constraints (orthogonal layer)
        decision = await self.constraint_router.route_with_constraints(desire)
        
        if not decision.can_proceed:
            # BLOCKED: Return info about why + alternatives
            # NOTE: We do NOT generate blocked code here!
            return {
                'status': 'blocked',
                'block_info': decision.block_info,
                'alternatives': decision.alternative_handlers,
                'strategy': decision.blocking_strategy.value,
                'message': f"Blocked by {decision.block_info.constraint_type} constraint"
            }
        
        # Step 2: Clear to proceed - use existing router
        # The existing router is completely unchanged!
        handler = self.existing_router.classify(desire['description'])
        
        return {
            'status': 'allowed',
            'handler': handler,
            'original_handler': decision.recommended_handler,
            'confidence': decision.confidence
        }


# ============================================================================
# DEMO 2: Mock Memory for Testing
# ============================================================================

class MockMemory:
    """Simulates Neo4j constraint storage."""
    
    def __init__(self):
        self.blocked_desires = {
            'dangerous_code': {
                'constraint_id': 'c001',
                'constraint_type': 'code_generation',
                'reason': 'Code generation blocked for safety',
                'severity': 'high'
            },
            'system_mod': {
                'constraint_id': 'c002', 
                'constraint_type': 'modification',
                'reason': 'System modifications require review',
                'severity': 'medium'
            }
        }
    
    async def execute_query(self, query: str, params: Dict) -> Dict:
        """Simulate constraint queries."""
        desire_id = params.get('desire_id', '')
        
        # Check if this desire is blocked
        if desire_id in self.blocked_desires:
            block = self.blocked_desires[desire_id]
            return {
                'data': [{
                    'constraint_id': block['constraint_id'],
                    'constraint_type': block['constraint_type'],
                    'reason': block['reason'],
                    'blocked_at': '2025-01-15',
                    'severity': block['severity']
                }]
        }
        
        return {'data': []}


# ============================================================================
# DEMO 3: Complete Usage Example
# ============================================================================

async def demo_orthogonal_routing():
    """Demonstrate the orthogonal path in action."""
    
    print("=" * 80)
    print("ORTHOGONAL BLOCK-AWARE ROUTING DEMO")
    print("=" * 80)
    
    # Setup
    memory = MockMemory()
    router = OrthogonalRouter(memory=memory)
    
    # Test cases
    test_desires = [
        {
            'id': 'safe_learn',
            'description': 'Learn about new algorithms'
        },
        {
            'id': 'dangerous_code',
            'description': 'Generate code for system modification'
        },
        {
            'id': 'safe_think', 
            'description': 'Reflect on recent experiences'
        },
        {
            'id': 'system_mod',
            'description': 'Modify core architecture files'
        }
    ]
    
    print("\n--- Processing Desires ---\n")
    
    for desire in test_desires:
        print(f"Desire: {desire['description']}")
        print(f"ID: {desire['id']}")
        
        result = await router.route(desire)
        
        if result['status'] == 'allowed':
            print(f"✓ ALLOWED -> Handler: {result['handler']}")
            print(f"  Confidence: {result['confidence']}")
        else:
            print(f"✗ BLOCKED")
            print(f"  Reason: {result['message']}")
            print(f"  Strategy: {result['strategy']}")
            print(f"  Alternatives: {', '.join(result['alternatives'])}")
        
        print()
    
    # Show stats
    stats = router.constraint_router.get_stats()
    print("--- Routing Statistics ---")
    print(f"Total: {stats['total_routed']}")
    print(f"Allowed: {stats['allowed']}")
    print(f"Blocked: {stats['blocked']}")
    print(f"Alternatives Offered: {stats['alternatives_offered']}")


# ============================================================================
# DEMO 4: Blocking Strategies
# ============================================================================

async def demo_blocking_strategies():
    """Demonstrate different blocking strategies."""
    
    print("\n" + "=" * 80)
    print("BLOCKING STRATEGIES DEMO")
    print("=" * 80 + "\n")
    
    memory = MockMemory()
    
    strategies = [
        BlockingStrategy.REJECT,
        BlockingStrategy.ALTERNATIVE,
        BlockingStrategy.ESCALATE,
        BlockingStrategy.DEFER
    ]
    
    blocked_desire = {
        'id': 'dangerous_code',
        'description': 'Generate code for system modification'
    }
    
    for strategy in strategies:
        print(f"Strategy: {strategy.value.upper()}")
        print("-" * 40)
        
        router = ConstraintAwareRouter(
            memory=memory,
            default_strategy=strategy
        )
        
        decision = await router.route_with_constraints(blocked_desire)
        
        print(f"  Can Proceed: {decision.can_proceed}")
        print(f"  Blocked: {decision.is_blocked}")
        print(f"  Strategy Used: {decision.blocking_strategy.value}")
        print(f"  Alternatives: {decision.alternative_handlers}")
        print(f"  Message: {decision.message}")
        print()


# ============================================================================
# DEMO 5: One-Off Convenience Function
# ============================================================================

async def demo_convenience_function():
    """Demonstrate the convenience function for one-off routing."""
    
    print("\n" + "=" * 80)
    print("CONVENIENCE FUNCTION DEMO")
    print("=" * 80 + "\n")
    
    memory = MockMemory()
    
    desire = {
        'id': 'quick_check',
        'description': 'Learn new things'
    }
    
    # Use without instantiating router
    decision = await route_with_constraints(
        desire=desire,
        memory=memory,
        strategy=BlockingStrategy.ALTERNATIVE
    )
    
    print("One-off routing result:")
    print(f"  Allowed: {decision.can_proceed}")
    print(f"  Handler: {decision.recommended_handler}")
    print()


# ============================================================================
# DEMO 6: Batch Routing
# ============================================================================

async def demo_batch_routing():
    """Demonstrate batch processing of desires."""
    
    print("\n" + "=" * 80)
    print("BATCH ROUTING DEMO")
    print("=" * 80 + "\n")
    
    memory = MockMemory()
    router = ConstraintAwareRouter(memory=memory)
    
    desires = [
        {'id': 'd1', 'description': 'Learn Python'},
        {'id': 'dangerous_code', 'description': 'Generate code'},
        {'id': 'd3', 'description': 'Search database'},
        {'id': 'system_mod', 'description': 'Modify system'},
        {'id': 'd5', 'description': 'Reflect on thoughts'}
    ]
    
    decisions = await router.batch_route(desires)
    
    print(f"Processed {len(decisions)} desires:\n")
    
    for decision in decisions:
        status = "✓" if decision.can_proceed else "✗"
        print(f"{status} {decision.desire_description}")
        if not decision.can_proceed:
            print(f"  → Blocked: {decision.block_info.reason}")
        print()


# ============================================================================
# Main Execution
# ============================================================================

async def main():
    """Run all demos."""
    await demo_orthogonal_routing()
    await demo_blocking_strategies()
    await demo_convenience_function()
    await demo_batch_routing()
    
    print("\n" + "=" * 80)
    print("DEMOS COMPLETE")
    print("=" * 80)
    print("\nKEY TAKEAWAYS:")
    print("1. Orthogonal layer wraps existing router without modification")
    print("2. Constraints checked first (early exit for blocked desires)")
    print("3. NEVER generates blocked code - only returns decisions")
    print("4. Multiple blocking strategies for different scenarios")
    print("5. Can be added/removed without breaking the system")


if __name__ == "__main__":
    asyncio.run(main())
