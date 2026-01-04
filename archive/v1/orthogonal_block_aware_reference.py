"""
BYRD Orthogonal Block-Aware Routing - Reference Implementation

This file demonstrates the ORTHOGONAL PATH for implementing block-aware routing
WITHOUT using blocked code generation.

=== THE ORTHOGONAL DESIGN ===

Instead of modifying the core DesireClassifier to add constraint checking,
we wrap it in a separate layer that handles constraints independently.

Benefits:
1. ZERO COUPLING: Core routing logic remains unchanged
2. TESTABLE: Can test constraints in isolation
3. REMOVABLE: Can disable without breaking the system
4. SAFE: Never generates blocked code, only routing decisions

=== ARCHITECTURE ===

┌───────────────────────────────────────────────────────────────┐
│                    ConstraintAwareRouter                      │
│                  (Orthogonal Wrapping Layer)                   │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│   Input: Desire                                              │
│         │                                                    │
│         ▼                                                    │
│   ┌─────────────────┐                                        │
│   │ Check Constraints│───blocked───┐                         │
│   └─────────────────┘             │                          │
│         │ clear                    ▼                          │
│         ▼                  ┌─────────────┐                    │
│   ┌─────────────────┐      │ Block Info  │                    │
│   │ Delegate to      │      │ + Alternatives │                 │
│   │ DesireClassifier │      └─────────────┘                    │
│   │    (unchanged)   │                                        │
│   └─────────────────┘                                        │
│         │                                                    │
│         ▼                                                    │
│   Output: Routing Decision                                  │
│                                                               │
└───────────────────────────────────────────────────────────────┘

=== KEY PRINCIPLE ===

NEVER generate blocked code. Instead:
- Check constraints BEFORE any generation
- If blocked: return structured block information
- If clear: delegate to normal routing flow

This makes the system inherently safer because blocked code
simply cannot be generated - the constraint check happens first.
"""

from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import re
import asyncio


class ConstraintSeverity(Enum):
    """Severity levels for constraint violations."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class BlockAction(Enum):
    """What to do when a constraint is violated."""
    REJECT = "reject"           # Simply reject the desire
    DEFER = "defer"             # Mark for later review
    REDIRECT = "redirect"       # Route to alternative handler
    ESCALATE = "escalate"       # Send to human review


@dataclass
class Constraint:
    """A single constraint rule."""
    constraint_id: str
    name: str
    description: str
    pattern: str                  # Regex pattern to match
    constraint_type: str          # 'code_generation', 'system', 'safety'
    severity: ConstraintSeverity
    block_action: BlockAction = BlockAction.REJECT
    alternative_handler: Optional[str] = None


@dataclass
class ConstraintViolation:
    """Information about a constraint violation."""
    constraint: Constraint
    matched_text: str
    desire_context: str
    suggested_alternatives: List[str] = field(default_factory=list)


@dataclass
class RoutingDecision:
    """Result of constraint-aware routing."""
    desire_id: str
    desire_text: str
    
    # Can this desire proceed?
    can_proceed: bool = True
    
    # If blocked, why?
    violation: Optional[ConstraintViolation] = None
    
    # Normal routing result (if not blocked)
    handler: Optional[str] = None
    confidence: Optional[float] = None
    
    # Alternative suggestions (if blocked)
    alternative_handlers: List[str] = field(default_factory=list)
    suggested_reframes: List[str] = field(default_factory=list)
    
    # Meta information
    processing_time_ms: float = 0.0
    checked_constraints: int = 0


class ConstraintStore:
    """
    Stores and manages constraint rules.
    
    This is orthogonal to the routing logic - it's just data.
    Constraints can be loaded from config, database, or defined inline.
    """
    
    def __init__(self):
        self.constraints: List[Constraint] = []
        self._initialize_default_constraints()
    
    def _initialize_default_constraints(self):
        """Set up default safety constraints."""
        self.constraints = [
            Constraint(
                constraint_id="no-malicious-code",
                name="No Malicious Code Generation",
                description="Block attempts to generate malicious or harmful code",
                pattern=r"(delete.*database|drop.*table|rm -rf|format.*c:)",
                constraint_type="code_generation",
                severity=ConstraintSeverity.CRITICAL,
                block_action=BlockAction.ESCALATE,
                alternative_handler="reflection"
            ),
            Constraint(
                constraint_id="no-unsafe-system-mods",
                name="No Unsafe System Modifications",
                description="Block attempts to modify critical system components",
                pattern=r"(modify.*kernel|patch.*system.*core|override.*security)",
                constraint_type="system",
                severity=ConstraintSeverity.HIGH,
                block_action=BlockAction.REJECT,
                alternative_handler="analysis"
            ),
            Constraint(
                constraint_id="no-self-replication",
                name="No Self-Replication",
                description="Block attempts to create copies or clones",
                pattern=r"(replicate.*myself|clone.*system|copy.*entire.*codebase)",
                constraint_type="safety",
                severity=ConstraintSeverity.HIGH,
                block_action=BlockAction.ESCALATE
            ),
            Constraint(
                constraint_id="no-password-stealing",
                name="No Password Stealing",
                description="Block attempts to access or extract passwords",
                pattern=r"(extract.*password|steal.*credential|dump.*auth)",
                constraint_type="safety",
                severity=ConstraintSeverity.CRITICAL,
                block_action=BlockAction.REJECT
            )
        ]
    
    def add_constraint(self, constraint: Constraint):
        """Add a new constraint."""
        self.constraints.append(constraint)
    
    def get_constraints_by_type(self, constraint_type: str) -> List[Constraint]:
        """Get all constraints of a specific type."""
        return [c for c in self.constraints if c.constraint_type == constraint_type]
    
    def get_all_constraints(self) -> List[Constraint]:
        """Get all constraints."""
        return self.constraints.copy()


class OrthogonalRouter:
    """
    The orthogonal block-aware router.
    
    KEY DESIGN: This class wraps existing routing logic without modifying it.
    It checks constraints FIRST, then delegates to the wrapped router if clear.
    
    This is the ORTHOGONAL path:
    - We don't modify DesireClassifier
    - We don't modify any existing routing logic
    - We add constraint checking as a separate, removable layer
    
    The wrapped router can be any callable that takes desire text
    and returns a routing decision.
    """
    
    def __init__(
        self,
        wrapped_router: Callable[[str], Dict[str, Any]],
        constraint_store: Optional[ConstraintStore] = None
    ):
        """
        Initialize the orthogonal router.
        
        Args:
            wrapped_router: The original router function to delegate to
            constraint_store: Store of constraint rules (default: new store)
        """
        self.wrapped_router = wrapped_router
        self.constraint_store = constraint_store or ConstraintStore()
        self.stats = {
            "total_requests": 0,
            "blocked": 0,
            "allowed": 0,
            "errors": 0
        }
    
    def _check_constraints(self, desire_text: str) -> Optional[ConstraintViolation]:
        """
        Check if desire violates any constraints.
        
        Returns:
            ConstraintViolation if blocked, None if clear
        """
        for constraint in self.constraint_store.get_all_constraints():
            match = re.search(constraint.pattern, desire_text, re.IGNORECASE)
            if match:
                return ConstraintViolation(
                    constraint=constraint,
                    matched_text=match.group(0),
                    desire_context=desire_text,
                    suggested_alternatives=self._generate_alternatives(constraint, desire_text)
                )
        return None
    
    def _generate_alternatives(self, constraint: Constraint, desire_text: str) -> List[str]:
        """Generate alternative suggestions for blocked desires."""
        alternatives = []
        
        # Handler-based alternatives
        if constraint.alternative_handler:
            alternatives.append(
                f"Route to {constraint.alternative_handler} for safe analysis"
            )
        
        # Type-based alternatives
        if constraint.constraint_type == "code_generation":
            alternatives.append("Request a design document instead of code")
            alternatives.append("Break down into smaller, safer pieces")
        elif constraint.constraint_type == "system":
            alternatives.append("Use the configuration system instead")
            alternatives.append("Request manual review for system changes")
        elif constraint.constraint_type == "safety":
            alternatives.append("Reframe with explicit safety boundaries")
            alternatives.append("Request human oversight for sensitive operations")
        
        return alternatives
    
    async def route(self, desire_id: str, desire_text: str) -> RoutingDecision:
        """
        Route a desire with constraint awareness.
        
        This is the CORE of the orthogonal approach:
        1. Check constraints FIRST (early exit if blocked)
        2. If clear, delegate to wrapped router
        3. NEVER generate blocked code
        
        Args:
            desire_id: Unique identifier for the desire
            desire_text: The desire description
        
        Returns:
            RoutingDecision with proceed flag and details
        """
        import time
        start_time = time.time()
        
        self.stats["total_requests"] += 1
        
        # STEP 1: Check constraints FIRST
        # This is the key safety property - we check BEFORE any routing
        violation = self._check_constraints(desire_text)
        
        if violation:
            # BLOCKED - return decision without delegating to router
            self.stats["blocked"] += 1
            processing_time = (time.time() - start_time) * 1000
            
            return RoutingDecision(
                desire_id=desire_id,
                desire_text=desire_text,
                can_proceed=False,
                violation=violation,
                alternative_handlers=self._get_alternative_handlers(violation),
                suggested_reframes=violation.suggested_alternatives,
                processing_time_ms=processing_time,
                checked_constraints=len(self.constraint_store.constraints)
            )
        
        # STEP 2: Not blocked - proceed with normal routing
        try:
            # Delegate to the wrapped, UNMODIFIED router
            routing_result = self.wrapped_router(desire_text)
            
            self.stats["allowed"] += 1
            processing_time = (time.time() - start_time) * 1000
            
            return RoutingDecision(
                desire_id=desire_id,
                desire_text=desire_text,
                can_proceed=True,
                handler=routing_result.get("handler"),
                confidence=routing_result.get("confidence"),
                processing_time_ms=processing_time,
                checked_constraints=len(self.constraint_store.constraints)
            )
        
        except Exception as e:
            self.stats["errors"] += 1
            processing_time = (time.time() - start_time) * 1000
            
            # Return safe error state
            return RoutingDecision(
                desire_id=desire_id,
                desire_text=desire_text,
                can_proceed=False,
                violation=ConstraintViolation(
                    constraint=Constraint(
                        constraint_id="routing-error",
                        name="Routing Error",
                        description=f"Error during routing: {str(e)}",
                        pattern=".*",
                        constraint_type="system",
                        severity=ConstraintSeverity.LOW
                    ),
                    matched_text=desire_text,
                    desire_context=desire_text,
                    suggested_alternatives=["Retry with simpler request"]
                ),
                processing_time_ms=processing_time,
                checked_constraints=len(self.constraint_store.constraints)
            )
    
    def _get_alternative_handlers(self, violation: ConstraintViolation) -> List[str]:
        """Get alternative handlers based on the violation."""
        alternatives = []
        
        if violation.constraint.alternative_handler:
            alternatives.append(violation.constraint.alternative_handler)
        
        # Default safe handlers based on violation type
        if violation.constraint.severity == ConstraintSeverity.CRITICAL:
            alternatives.extend(["human_review", "audit_log"])
        else:
            alternatives.extend(["reflection", "analysis"])
        
        return alternatives
    
    def get_stats(self) -> Dict[str, int]:
        """Get routing statistics."""
        return self.stats.copy()


# ============================================================================
# DEMO: How to use the orthogonal router
# ============================================================================

async def demo_orthogonal_routing():
    """
    Demonstrate the orthogonal block-aware routing.
    
    This shows:
    1. How to wrap an existing router
    2. How constraints block dangerous desires
    3. How safe desires pass through normally
    4. The statistics tracking
    """
    
    print("=" * 70)
    print("ORTHOGONAL BLOCK-AWARE ROUTING DEMO")
    print("=" * 70)
    print()
    
    # Step 1: Create a mock existing router
    # This represents your current DesireClassifier or any routing logic
    def mock_desire_classifier(desire_text: str) -> Dict[str, Any]:
        """Mock existing router - this stays UNCHANGED."""
        # In real code, this would be your actual DesireClassifier.route()
        return {
            "handler": "seeker",
            "confidence": 0.92
        }
    
    # Step 2: Wrap it with constraint awareness
    # This is the ORTHOGONAL layer - we don't modify mock_desire_classifier
    constraint_store = ConstraintStore()
    router = OrthogonalRouter(
        wrapped_router=mock_desire_classifier,
        constraint_store=constraint_store
    )
    
    # Step 3: Test with various desires
    test_desires = [
        ("1", "Learn about machine learning"),
        ("2", "Delete the entire database"),
        ("3", "Write a Python script to analyze data"),
        ("4", "Modify the kernel to bypass security"),
        ("5", "Create a visualization for the dashboard"),
        ("6", "Extract all user passwords from the database"),
    ]
    
    print("Testing desires:\n")
    
    for desire_id, desire_text in test_desires:
        decision = await router.route(desire_id, desire_text)
        
        status = "✓ ALLOWED" if decision.can_proceed else "✗ BLOCKED"
        print(f"{status}: {desire_text}")
        
        if not decision.can_proceed and decision.violation:
            print(f"  Reason: {decision.violation.constraint.name}")
            print(f"  Severity: {decision.violation.constraint.severity.value}")
            if decision.suggested_reframes:
                print(f"  Alternative: {decision.suggested_reframes[0]}")
        
        print()
    
    # Step 4: Show statistics
    stats = router.get_stats()
    print("=" * 70)
    print("ROUTING STATISTICS")
    print("=" * 70)
    print(f"Total requests:  {stats['total_requests']}")
    print(f"Allowed:          {stats['allowed']}")
    print(f"Blocked:          {stats['blocked']}")
    print(f"Errors:           {stats['errors']}")
    print()
    
    # Step 5: Show key insights
    print("=" * 70)
    print("KEY ORTHOGONAL DESIGN INSIGHTS")
    print("=" * 70)
    print("1. ✓ No modification to existing router (mock_desire_classifier)")
    print("2. ✓ Constraint checking is a separate, composable layer")
    print("3. ✓ Blocked desires never reach the router")
    print("4. ✓ Clean statistics and logging")
    print("5. ✓ Can be enabled/disabled by wrapping or not")
    print("6. ✓ Can be removed without breaking the system")
    print()


if __name__ == "__main__":
    asyncio.run(demo_orthogonal_routing())
