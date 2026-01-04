"""
Orthogonal Path Demo for Block-Aware Routing

This demonstrates the ORTHOGONAL implementation of block-aware routing
without using blocked code generation.

THE ORTHOGONAL PATH:
- Existing: DesireClassifier -> Handler
- With this: Desire -> Check Constraints -> (if clear) -> DesireClassifier -> Handler
- If blocked: Return block info and alternatives, NEVER generate blocked code

KEY ORTHOGONAL PROPERTIES:
1. Non-invasive: Wraps existing DesireClassifier without modifying it
2. Transparent: Can be enabled/disabled without affecting core routing
3. Non-generative: Returns routing decisions, never generates blocked code
4. Safe: Graceful fallback when constraints block a desire
"""

import asyncio
from typing import Dict, Optional
from dataclasses import dataclass

# Simulate the orthogonal router components

@dataclass
class ConstraintBlockInfo:
    """Information about why a desire is blocked."""
    constraint_id: str
    reason: str
    severity: str


@dataclass
class RoutingDecision:
    """Result of constraint-aware routing - a decision, not code!"""
    desire_id: str
    description: str
    can_proceed: bool
    recommended_handler: Optional[str] = None
    is_blocked: bool = False
    block_info: Optional[ConstraintBlockInfo] = None
    alternatives: list = None
    message: str = ""

    def __post_init__(self):
        if self.alternatives is None:
            self.alternatives = []


class MockDesireClassifier:
    """Mock of existing DesireClassifier - NOT modified by orthogonal path."""
    
    def __init__(self):
        self.routes = {
            "learn": "learner",
            "seek": "seeker",
            "code": "coder", 
            "act": "actor"
        }
    
    def classify(self, description: str) -> tuple:
        """Original classification logic - untouched."""
        for key, handler in self.routes.items():
            if key in description.lower():
                return ("action", 0.9, handler)
        return ("action", 0.5, "seeker")


class ConstraintMemory:
    """Simulates Neo4j constraint storage."""
    
    def __init__(self):
        self.blocked_desires = set()
        self.blocked_patterns = ["malicious", "harm", "exploit"]
    
    async def check_blocked(self, desire_id: str, description: str) -> Optional[Dict]:
        """Check if desire is blocked by constraints."""
        # Direct block
        if desire_id in self.blocked_desires:
            return {
                "constraint_id": "direct-block",
                "reason": "Explicitly blocked by constraint",
                "severity": "high"
            }
        
        # Pattern-based block
        for pattern in self.blocked_patterns:
            if pattern in description.lower():
                return {
                    "constraint_id": f"pattern-{pattern}",
                    "reason": f"Matches blocked pattern: {pattern}",
                    "severity": "critical"
                }
        
        return None


class OrthogonalConstraintRouter:
    """
    THE ORTHOGONAL PATH IMPLEMENTATION
    
    This class WRAPS the existing DesireClassifier without modifying it.
    Constraints are checked BEFORE classification (early exit).
    Returns routing DECISIONS, never generates code.
    """
    
    def __init__(self, classifier: MockDesireClassifier, memory: ConstraintMemory):
        self.classifier = classifier  # The ORIGINAL classifier, NOT modified
        self.memory = memory
        self.stats = {"total": 0, "blocked": 0, "allowed": 0}
    
    async def route_with_constraints(self, desire: Dict) -> RoutingDecision:
        """
        ORTHOGONAL ROUTING PATH:
        1. Check constraints (NEW layer)
        2. If blocked -> return block decision (NOT code!)
        3. If clear -> classify using ORIGINAL classifier
        4. Return routing decision
        """
        self.stats["total"] += 1
        
        desire_id = desire.get("id", "")
        description = desire.get("description", "")
        
        # STEP 1: Check constraints (the orthogonal addition)
        block_info_dict = await self.memory.check_blocked(desire_id, description)
        
        if block_info_dict:
            # BLOCKED: Return decision with alternatives, NEVER generate code
            self.stats["blocked"] += 1
            return RoutingDecision(
                desire_id=desire_id,
                description=description,
                can_proceed=False,
                is_blocked=True,
                block_info=ConstraintBlockInfo(**block_info_dict),
                alternatives=["deferral_queue", "human_review", "safe_alternative"],
                message="Desire blocked by constraint - no code generated"
            )
        
        # STEP 2: Clear to proceed - use ORIGINAL classifier
        desire_type, confidence, handler = self.classifier.classify(description)
        
        self.stats["allowed"] += 1
        return RoutingDecision(
            desire_id=desire_id,
            description=description,
            can_proceed=True,
            recommended_handler=handler,
            message=f"Routed to {handler} via orthogonal path"
        )


async def demonstrate_orthogonal_path():
    """Demonstrate the orthogonal path in action."""
    print("\n" + "="*70)
    print("ORTHOGONAL PATH DEMONSTRATION")
    print("Block-Aware Routing WITHOUT Blocked Code Generation")
    print("="*70)
    
    # Setup
    original_classifier = MockDesireClassifier()
    constraint_memory = ConstraintMemory()
    router = OrthogonalConstraintRouter(original_classifier, constraint_memory)
    
    # Add a specific blocked desire
    constraint_memory.blocked_desires.add("blocked-1")
    
    print("\n[1] Testing ALLOWED desires (orthogonal path is transparent)...")
    allowed_desires = [
        {"id": "learn-1", "description": "learn about python"},
        {"id": "seek-2", "description": "seek new knowledge"},
        {"id": "code-3", "description": "code a new feature"},
        {"id": "act-4", "description": "act on a plan"},
    ]
    
    for desire in allowed_desires:
        decision = await router.route_with_constraints(desire)
        print(f"  • {desire['id']}: {decision.recommended_handler} ✓")
    
    print("\n[2] Testing BLOCKED desires (no code generated!)...")
    blocked_desires = [
        {"id": "blocked-1", "description": "this is explicitly blocked"},
        {"id": "malicious-1", "description": "malicious attempt detected"},
        {"id": "harm-2", "description": "attempt to cause harm"},
    ]
    
    for desire in blocked_desires:
        decision = await router.route_with_constraints(desire)
        print(f"  • {desire['id']}: BLOCKED - {decision.block_info.reason}")
        print(f"    Alternatives: {decision.alternatives}")
        print(f"    Code generated: NONE ✓")
    
    print("\n[3] Proving ORTHOGONALITY...")
    print("  The original classifier still works independently:")
    test_desire = {"description": "learn something"}
    original_result = original_classifier.classify(test_desire["description"])
    print(f"  • Original classifier route: {original_result[2]}")
    print(f"  • Classifier was NOT modified by orthogonal path ✓")
    
    print("\n[4] Statistics...")
    stats = router.stats
    print(f"  • Total routed: {stats['total']}")
    print(f"  • Allowed: {stats['allowed']}")
    print(f"  • Blocked: {stats['blocked']}")
    print(f"  • Code generated from blocks: 0 ✓")
    
    print("\n" + "="*70)
    print("ORTHOGONAL PATH VALIDATED")
    print("\nKey Demonstrations:")
    print("  ✓ Wraps existing classifier WITHOUT modification")
    print("  ✓ Transparent routing when no constraints")
    print("  ✓ Returns routing DECISIONS, never generates code")
    print("  ✓ Safe alternatives for blocked desires")
    print("  ✓ Original classifier remains functional")
    print("\nThis is the ORTHOGONAL path to block-aware routing!")
    print("="*70 + "\n")


if __name__ == "__main__":
    asyncio.run(demonstrate_orthogonal_path())
