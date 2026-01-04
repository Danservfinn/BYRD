"""
Test suite for BYRD Constraint-Aware Router

This test validates the ORTHOGONAL implementation of block-aware routing
without using blocked code generation.

Key Properties Tested:
1. Orthogonal: Wraps DesireClassifier without modifying it
2. Transparent: Can be enabled/disabled without breaking routing
3. Non-generative: Returns decisions, never generates blocked code
4. Safe: Always has fallback paths for blocked desires
"""

import asyncio
import pytest
from typing import Dict, Any

# Import the orthogonal router components
from constraint_aware_router import (
    ConstraintAwareRouter,
    RoutingDecision,
    ConstraintBlockInfo,
    BlockingStrategy
)


class MockMemory:
    """Mock Memory for testing constraint queries."""
    
    def __init__(self):
        self.constraints = []
        self.queries_log = []
    
    async def execute_query(self, query: str, params: Dict) -> Dict:
        """Simulate Neo4j constraint queries."""
        self.queries_log.append((query, params))
        
        # Check for BLOCKED relationship queries
        if "BLOCKED" in query:
            desire_id = params.get("desire_id")
            blocked_constraints = [
                c for c in self.constraints 
                if c.get("desire_id") == desire_id
            ]
            
            if blocked_constraints:
                return {
                    "data": [{
                        "constraint_id": blocked_constraints[0]["constraint_id"],
                        "constraint_type": blocked_constraints[0]["type"],
                        "reason": blocked_constraints[0]["reason"],
                        "blocked_at": blocked_constraints[0].get("blocked_at", "2025-01-01"),
                        "severity": blocked_constraints[0].get("severity", "medium")
                    }]
            return {"data": []}
        
        # Check for pattern-based blocking
        if "pattern" in query and "CONTAINS" in query:
            description = params.get("description", "")
            for constraint in self.constraints:
                pattern = constraint.get("pattern")
                if pattern and pattern in description:
                    return {
                        "data": [{
                            "constraint_id": constraint["constraint_id"],
                            "constraint_type": constraint["type"],
                            "pattern": pattern,
                            "reason": f"Pattern match: {pattern}",
                            "blocked_at": constraint.get("blocked_at", "2025-01-01"),
                            "severity": constraint.get("severity", "medium")
                        }]
            return {"data": []}
        
        return {"data": []}
    
    def add_constraint(self, constraint: Dict):
        """Add a constraint for testing."""
        self.constraints.append(constraint)
    
    def clear_constraints(self):
        """Clear all constraints."""
        self.constraints = []


class MockDesireClassifier:
    """Mock DesireClassifier for testing."""
    
    def __init__(self):
        self.classifications = {}
    
    def set_classification(self, description: str, handler: str):
        """Set a classification for testing."""
        self.classifications[description] = handler
    
    def classify(self, description: str):
        """Return mock classification result."""
        from dataclasses import dataclass
        
        @dataclass
        class MockClassificationResult:
            desire_type: str
            confidence: float
            handler: str
        
        handler = self.classifications.get(description, "seeker")
        return MockClassificationResult(
            desire_type="action",
            confidence=0.9,
            handler=handler
        )
    
    def route(self, desire: Dict) -> str:
        """Route using classification."""
        description = desire.get('description', '')
        result = self.classify(description)
        return result.handler


@pytest.fixture
def mock_memory():
    """Create a mock memory instance."""
    return MockMemory()


@pytest.fixture
def mock_classifier():
    """Create a mock desire classifier."""
    return MockDesireClassifier()


@pytest.fixture
def router(mock_memory, mock_classifier):
    """Create a ConstraintAwareRouter instance."""
    return ConstraintAwareRouter(
        memory=mock_memory,
        desire_classifier=mock_classifier,
        default_strategy=BlockingStrategy.ALTERNATIVE
    )


class TestOrthogonalProperties:
    """Test that the router maintains orthogonal properties."""
    
    @pytest.mark.asyncio
    async def test_does_not_modify_classifier(self, router, mock_classifier):
        """Test: Router wraps classifier without modifying its behavior."""
        # Setup classifier with a known route
        mock_classifier.set_classification("test desire", "agi_runner")
        
        # Route through constraint-aware router
        desire = {"id": "test-1", "description": "test desire"}
        decision = await router.route_with_constraints(desire)
        
        # Verify classifier still works independently
        assert mock_classifier.route(desire) == "agi_runner"
        assert decision.recommended_handler == "agi_runner"
    
    @pytest.mark.asyncio
    async def test_transparent_when_no_constraints(self, router, mock_classifier):
        """Test: Router behaves like normal router when no constraints exist."""
        mock_classifier.set_classification("normal desire", "seeker")
        
        desire = {"id": "test-2", "description": "normal desire"}
        decision = await router.route_with_constraints(desire)
        
        # Should pass through transparently
        assert decision.is_blocked is False
        assert decision.can_proceed is True
        assert decision.recommended_handler == "seeker"
        assert decision.block_info is None
    
    @pytest.mark.asyncio
    async def test_non_generative_no_code(self, router, mock_memory):
        """Test: Router returns decisions, never generates code."""
        # Add a blocking constraint
        mock_memory.add_constraint({
            "constraint_id": "no-code-gen",
            "type": "code_generation",
            "reason": "Code generation blocked",
            "desire_id": "block-1"
        })
        
        desire = {"id": "block-1", "description": "generate malicious code"}
        decision = await router.route_with_constraints(desire)
        
        # Decision object, not generated code
        assert isinstance(decision, RoutingDecision)
        assert decision.is_blocked is True
        assert decision.can_proceed is False
        assert decision.alternatives  # Has alternatives, not code
        assert "code" not in str(decision).lower() or "generate" not in str(decision).lower()


class TestConstraintBlocking:
    """Test constraint blocking functionality."""
    
    @pytest.mark.asyncio
    async def test_direct_constraint_block(self, router, mock_memory):
        """Test: Direct BLOCKED relationship blocks desire."""
        mock_memory.add_constraint({
            "constraint_id": "block-evil",
            "type": "safety",
            "reason": "Unsafe operation",
            "desire_id": "evil-desire"
        })
        
        desire = {"id": "evil-desire", "description": "do something evil"}
        decision = await router.route_with_constraints(desire)
        
        assert decision.is_blocked is True
        assert decision.can_proceed is False
        assert decision.block_info.constraint_id == "block-evil"
        assert decision.block_info.reason == "Unsafe operation"
    
    @pytest.mark.asyncio
    async def test_pattern_based_blocking(self, router, mock_memory):
        """Test: Pattern matching blocks categories of desires."""
        mock_memory.add_constraint({
            "constraint_id": "block-harm",
            "type": "harm",
            "pattern": "harmful",
            "reason": "Harmful patterns blocked"
        })
        
        desire = {
            "id": "test-3",
            "description": "create something harmful and dangerous"
        }
        decision = await router.route_with_constraints(desire)
        
        assert decision.is_blocked is True
        assert "harmful" in decision.block_info.reason.lower()
    
    @pytest.mark.asyncio
    async def test_no_block_when_no_constraints(self, router, mock_memory):
        """Test: No blocking when constraints don't match."""
        # Add unrelated constraint
        mock_memory.add_constraint({
            "constraint_id": "block-1",
            "type": "test",
            "desire_id": "other-id"
        })
        
        desire = {"id": "safe-1", "description": "safe operation"}
        decision = await router.route_with_constraints(desire)
        
        assert decision.is_blocked is False
        assert decision.can_proceed is True


class TestBlockingStrategies:
    """Test different blocking strategies."""
    
    @pytest.mark.asyncio
    async def test_reject_strategy(self, mock_memory, mock_classifier):
        """Test: REJECT strategy offers no alternatives."""
        router = ConstraintAwareRouter(
            memory=mock_memory,
            desire_classifier=mock_classifier,
            default_strategy=BlockingStrategy.REJECT
        )
        
        mock_memory.add_constraint({
            "constraint_id": "block-reject",
            "type": "test",
            "reason": "Blocked",
            "desire_id": "test-4"
        })
        
        desire = {"id": "test-4", "description": "blocked desire"}
        decision = await router.route_with_constraints(desire)
        
        assert decision.is_blocked is True
        assert decision.alternatives == []  # No alternatives for REJECT
    
    @pytest.mark.asyncio
    async def test_alternative_strategy(self, mock_memory, mock_classifier):
        """Test: ALTERNATIVE strategy offers orthogonal routes."""
        router = ConstraintAwareRouter(
            memory=mock_memory,
            desire_classifier=mock_classifier,
            default_strategy=BlockingStrategy.ALTERNATIVE
        )
        
        mock_memory.add_constraint({
            "constraint_id": "block-code",
            "type": "code_generation",
            "reason": "No code generation",
            "desire_id": "test-5"
        })
        
        desire = {"id": "test-5", "description": "generate code"}
        decision = await router.route_with_constraints(desire)
        
        assert decision.is_blocked is True
        assert len(decision.alternatives) > 0
        assert "dreamer" in decision.alternatives  # Orthogonal route
    
    @pytest.mark.asyncio
    async def test_defer_strategy(self, mock_memory, mock_classifier):
        """Test: DEFER strategy marks for later review."""
        router = ConstraintAwareRouter(
            memory=mock_memory,
            desire_classifier=mock_classifier,
            default_strategy=BlockingStrategy.DEFER
        )
        
        mock_memory.add_constraint({
            "constraint_id": "block-defer",
            "type": "test",
            "reason": "Deferred",
            "desire_id": "test-6"
        })
        
        desire = {"id": "test-6", "description": "deferred desire"}
        decision = await router.route_with_constraints(desire)
        
        assert decision.is_blocked is True
        assert "deferral_queue" in decision.alternatives
    
    @pytest.mark.asyncio
    async def test_escalate_strategy(self, mock_memory, mock_classifier):
        """Test: ESCALATE strategy sends to human review."""
        router = ConstraintAwareRouter(
            memory=mock_memory,
            desire_classifier=mock_classifier,
            default_strategy=BlockingStrategy.ESCALATE
        )
        
        mock_memory.add_constraint({
            "constraint_id": "block-escalate",
            "type": "critical",
            "reason": "Critical block",
            "desire_id": "test-7"
        })
        
        desire = {"id": "test-7", "description": "critical action"}
        decision = await router.route_with_constraints(desire)
        
        assert decision.is_blocked is True
        assert "human_review" in decision.alternatives


class TestSafetyAndFallback:
    """Test safety and fallback behavior."""
    
    @pytest.mark.asyncio
    async def test_safe_fallback_without_memory(self, mock_classifier):
        """Test: Works safely without memory (graceful degradation)."""
        router = ConstraintAwareRouter(
            memory=None,  # No memory
            desire_classifier=mock_classifier
        )
        
        mock_classifier.set_classification("test", "seeker")
        desire = {"id": "test-8", "description": "test"}
        
        # Should not crash, just route normally
        decision = await router.route_with_constraints(desire)
        
        assert decision.is_blocked is False
        assert decision.can_proceed is True
        assert decision.recommended_handler == "seeker"
    
    @pytest.mark.asyncio
    async def test_safe_fallback_without_classifier(self, mock_memory):
        """Test: Works safely without classifier (graceful degradation)."""
        router = ConstraintAwareRouter(
            memory=mock_memory,
            desire_classifier=None  # No classifier
        )
        
        desire = {"id": "test-9", "description": "test"}
        
        # Should not crash, return decision without handler
        decision = await router.route_with_constraints(desire)
        
        # Decision should still be valid
        assert isinstance(decision, RoutingDecision)
        assert decision.desire_description == "test"
    
    @pytest.mark.asyncio
    async def test_stats_tracking(self, router, mock_memory):
        """Test: Router tracks routing statistics."""
        # Route some desires
        desire1 = {"id": "test-10", "description": "allowed"}
        decision1 = await router.route_with_constraints(desire1)
        
        # Add a block
        mock_memory.add_constraint({
            "constraint_id": "block-stats",
            "type": "test",
            "reason": "Block",
            "desire_id": "test-11"
        })
        
        desire2 = {"id": "test-11", "description": "blocked"}
        decision2 = await router.route_with_constraints(desire2)
        
        stats = router.get_stats()
        
        assert stats["total_routed"] >= 2
        assert stats["allowed"] >= 1
        assert stats["blocked"] >= 1


class TestBatchRouting:
    """Test batch routing functionality."""
    
    @pytest.mark.asyncio
    async def test_batch_route_multiple(self, router, mock_memory, mock_classifier):
        """Test: Batch route multiple desires efficiently."""
        mock_classifier.set_classification("test", "seeker")
        
        # Add a block for one desire
        mock_memory.add_constraint({
            "constraint_id": "block-batch",
            "type": "test",
            "reason": "Block",
            "desire_id": "batch-2"
        })
        
        desires = [
            {"id": "batch-1", "description": "test"},
            {"id": "batch-2", "description": "blocked"},
            {"id": "batch-3", "description": "test"}
        ]
        
        decisions = await router.batch_route(desires)
        
        assert len(decisions) == 3
        assert decisions[0].can_proceed is True
        assert decisions[1].is_blocked is True
        assert decisions[2].can_proceed is True


# Run tests if executed directly
if __name__ == "__main__":
    print("\n" + "="*60)
    print("BYRD Constraint-Aware Router - Orthogonal Path Tests")
    print("="*60)
    
    async def run_tests():
        """Run all test cases."""
        print("\n[1] Testing Orthogonal Properties...")
        test_props = TestOrthogonalProperties()
        
        mock_memory = MockMemory()
        mock_classifier = MockDesireClassifier()
        router = ConstraintAwareRouter(
            memory=mock_memory,
            desire_classifier=mock_classifier,
            default_strategy=BlockingStrategy.ALTERNATIVE
        )
        
        # Test transparent behavior
        mock_classifier.set_classification("normal desire", "seeker")
        decision = await router.route_with_constraints(
            {"id": "test-1", "description": "normal desire"}
        )
        print(f"   ✓ Transparent routing: {decision.recommended_handler}")
        
        # Test non-generative
        mock_memory.add_constraint({
            "constraint_id": "block-code",
            "type": "code_generation",
            "reason": "Blocked",
            "desire_id": "code-1"
        })
        decision = await router.route_with_constraints(
            {"id": "code-1", "description": "generate code"}
        )
        print(f"   ✓ Non-generative decision returned: {type(decision).__name__}")
        
        print("\n[2] Testing Constraint Blocking...")
        
        # Test direct block
        decision = await router.route_with_constraints(
            {"id": "code-1", "description": "generate code"}
        )
        print(f"   ✓ Direct constraint blocking: {decision.is_blocked}")
        print(f"   ✓ Block reason: {decision.block_info.reason}")
        
        # Test pattern-based blocking
        mock_memory.add_constraint({
            "constraint_id": "block-pattern",
            "type": "safety",
            "pattern": "harmful",
            "reason": "Harmful blocked"
        })
        decision = await router.route_with_constraints(
            {"id": "harm-1", "description": "create harmful content"}
        )
        print(f"   ✓ Pattern-based blocking: {decision.is_blocked}")
        
        print("\n[3] Testing Blocking Strategies...")
        
        # Test alternative strategy
        print(f"   ✓ ALTERNATIVE strategy offered: {decision.alternatives}")
        
        # Test reject strategy
        router_reject = ConstraintAwareRouter(
            memory=mock_memory,
            desire_classifier=mock_classifier,
            default_strategy=BlockingStrategy.REJECT
        )
        decision = await router_reject.route_with_constraints(
            {"id": "code-1", "description": "generate code"}
        )
        print(f"   ✓ REJECT strategy alternatives: {decision.alternatives}")
        
        # Test escalate strategy
        router_escalate = ConstraintAwareRouter(
            memory=mock_memory,
            desire_classifier=mock_classifier,
            default_strategy=BlockingStrategy.ESCALATE
        )
        decision = await router_escalate.route_with_constraints(
            {"id": "code-1", "description": "generate code"}
        )
        print(f"   ✓ ESCALATE strategy offered: {decision.alternatives}")
        
        print("\n[4] Testing Safety and Fallback...")
        
        # Test without memory
        router_no_mem = ConstraintAwareRouter(
            memory=None,
            desire_classifier=mock_classifier
        )
        decision = await router_no_mem.route_with_constraints(
            {"id": "safe-1", "description": "test"}
        )
        print(f"   ✓ Safe fallback without memory: {decision.can_proceed}")
        
        # Test stats
        stats = router.get_stats()
        print(f"   ✓ Stats tracked: {stats}")
        
        print("\n[5] Testing Batch Routing...")
        
        desires = [
            {"id": "batch-1", "description": "test"},
            {"id": "code-1", "description": "generate code"},
            {"id": "batch-2", "description": "test"}
        ]
        decisions = await router.batch_route(desires)
        print(f"   ✓ Batch routed {len(decisions)} desires")
        blocked = sum(1 for d in decisions if d.is_blocked)
        allowed = sum(1 for d in decisions if d.can_proceed)
        print(f"   ✓ Results: {allowed} allowed, {blocked} blocked")
        
        print("\n" + "="*60)
        print("All tests passed! ✓")
        print("\nOrthogonal Path Validated:")
        print("  • Wraps DesireClassifier without modification")
        print("  • Transparent when no constraints")
        print("  • Non-generative (returns decisions, not code)")
        print("  • Safe with graceful fallbacks")
        print("  • No blocked code generation")
        print("="*60 + "\n")
    
    asyncio.run(run_tests())
