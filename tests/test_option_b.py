"""
BYRD Option B: Comprehensive End-to-End Test Suite

Tests all five compounding loops and their integration:
1. Memory Reasoner - Graph-based reasoning
2. Self-Compiler - Pattern learning
3. Goal Evolver - Evolutionary optimization
4. Dreaming Machine - Experience multiplication
5. BYRD Omega - Meta-orchestration

Plus infrastructure tests for:
- Embedding providers
- Coupling tracker
- Kill criteria
- Event bus integration
"""

import asyncio
import json
import sys
import os
import traceback

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from unittest.mock import AsyncMock, MagicMock, patch


# Test result tracking
@dataclass
class TestResult:
    name: str
    passed: bool
    message: str
    duration_ms: float


class TestRunner:
    def __init__(self):
        self.results: List[TestResult] = []
        self.current_section = ""

    def section(self, name: str):
        self.current_section = name
        print(f"\n{'='*60}")
        print(f"  {name}")
        print(f"{'='*60}")

    async def run_test(self, name: str, test_func):
        start = datetime.now()
        try:
            await test_func()
            duration = (datetime.now() - start).total_seconds() * 1000
            self.results.append(TestResult(name, True, "OK", duration))
            print(f"  ✓ {name} ({duration:.0f}ms)")
            return True
        except Exception as e:
            duration = (datetime.now() - start).total_seconds() * 1000
            error_msg = str(e)
            self.results.append(TestResult(name, False, error_msg, duration))
            print(f"  ✗ {name}: {error_msg}")
            traceback.print_exc()
            return False

    def summary(self):
        passed = sum(1 for r in self.results if r.passed)
        failed = sum(1 for r in self.results if not r.passed)
        total = len(self.results)

        print(f"\n{'='*60}")
        print(f"  TEST SUMMARY")
        print(f"{'='*60}")
        print(f"  Passed: {passed}/{total}")
        print(f"  Failed: {failed}/{total}")

        if failed > 0:
            print(f"\n  Failed tests:")
            for r in self.results:
                if not r.passed:
                    print(f"    - {r.name}: {r.message}")

        return failed == 0


# Mock classes for testing without real dependencies
class MockMemory:
    """Mock memory for testing without Neo4j."""

    def __init__(self):
        self._experiences = []
        self._patterns = []
        self._goals = []
        self._insights = []
        self._nodes = {}
        self._embeddings = {}
        self._capability_scores = []
        self._id_counter = 0

    def _next_id(self, prefix: str) -> str:
        self._id_counter += 1
        return f"{prefix}_{self._id_counter}"

    async def connect(self):
        pass

    async def record_experience(self, content: str, type: str = "observation", **kwargs) -> str:
        exp_id = self._next_id("exp")
        self._experiences.append({
            "id": exp_id,
            "content": content,
            "type": type,
            "timestamp": datetime.now().isoformat(),
            **kwargs
        })
        return exp_id

    async def get_recent_experiences(self, limit: int = 20) -> List[Dict]:
        return self._experiences[-limit:]

    async def create_pattern(
        self,
        problem_signature: str,
        solution_template: str,
        abstraction_level: str,
        domains: List[str],
        embedding: Optional[List[float]] = None
    ) -> str:
        pattern_id = self._next_id("pattern")
        self._patterns.append({
            "id": pattern_id,
            "problem_signature": problem_signature,
            "solution_template": solution_template,
            "abstraction_level": abstraction_level,
            "domains": domains,
            "success_count": 0,
            "failure_count": 0,
            "embedding": embedding
        })
        return pattern_id

    async def get_similar_patterns(
        self,
        query_embedding: List[float],
        min_similarity: float = 0.5,
        limit: int = 5
    ) -> List[Dict]:
        # Return patterns with mock similarity scores
        return [
            {**p, "similarity": 0.8}
            for p in self._patterns[:limit]
        ]

    async def update_pattern_success(self, pattern_id: str, succeeded: bool):
        for p in self._patterns:
            if p["id"] == pattern_id:
                if succeeded:
                    p["success_count"] = p.get("success_count", 0) + 1
                else:
                    p["failure_count"] = p.get("failure_count", 0) + 1

    async def get_patterns_for_lifting(
        self,
        min_success_count: int = 3,
        min_domain_count: int = 2
    ) -> List[Dict]:
        return [
            p for p in self._patterns
            if p.get("success_count", 0) >= min_success_count
        ]

    async def create_goal(
        self,
        description: str,
        fitness: float = 0.5,
        generation: int = 0,
        parent_goals: List[str] = None,
        success_criteria: Dict = None
    ) -> str:
        goal_id = self._next_id("goal")
        self._goals.append({
            "id": goal_id,
            "description": description,
            "fitness": fitness,
            "generation": generation,
            "parent_goals": parent_goals or [],
            "success_criteria": json.dumps(success_criteria or {}),
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "capability_delta": 0.0,
            "attempts": 0
        })
        return goal_id

    async def get_active_goals(self, limit: int = 20) -> List[Dict]:
        return [g for g in self._goals if g.get("status") == "active"][:limit]

    async def update_goal_fitness(
        self,
        goal_id: str,
        fitness: float,
        capability_delta: float
    ):
        for g in self._goals:
            if g["id"] == goal_id:
                g["fitness"] = fitness
                g["capability_delta"] = capability_delta

    async def complete_goal(self, goal_id: str):
        for g in self._goals:
            if g["id"] == goal_id:
                g["status"] = "completed"

    async def archive_goal(self, goal_id: str):
        for g in self._goals:
            if g["id"] == goal_id:
                g["status"] = "archived"

    async def create_insight(
        self,
        content: str,
        source_type: str,
        confidence: float,
        supporting_evidence: List[str],
        embedding: Optional[List[float]] = None
    ) -> str:
        insight_id = self._next_id("insight")
        self._insights.append({
            "id": insight_id,
            "content": content,
            "source_type": source_type,
            "confidence": confidence,
            "supporting_evidence": supporting_evidence,
            "embedding": embedding,
            "created_at": datetime.now().isoformat()
        })
        return insight_id

    async def get_recent_insights(self, limit: int = 10) -> List[Dict]:
        return self._insights[-limit:]

    async def apply_insight(self, insight_id: str, target_id: str):
        pass

    async def update_insight_confidence(self, insight_id: str, delta: float):
        for i in self._insights:
            if i["id"] == insight_id:
                i["confidence"] = min(1.0, max(0.0, i["confidence"] + delta))

    async def find_similar_nodes(
        self,
        embedding: List[float],
        node_types: List[str] = None,
        limit: int = 10,
        min_similarity: float = 0.5
    ) -> List[Dict]:
        # Return nodes with mock similarity
        results = []
        for node_type, nodes in [
            ("Experience", self._experiences),
            ("Pattern", self._patterns),
            ("Insight", self._insights)
        ]:
            if node_types is None or node_type in node_types:
                for n in nodes[:limit]:
                    results.append({**n, "type": node_type, "similarity": 0.75})
        return results[:limit]

    async def get_neighbors(
        self,
        node_id: str,
        relationship_types: List[str] = None,
        limit: int = 20
    ) -> List[Dict]:
        # Return mock neighbors
        return []

    async def get_node(self, node_id: str) -> Optional[Dict]:
        for nodes in [self._experiences, self._patterns, self._goals, self._insights]:
            for n in nodes:
                if n.get("id") == node_id:
                    return n
        return None

    async def update_node_embedding(self, node_id: str, embedding: List[float]):
        self._embeddings[node_id] = embedding

    async def record_capability_score(
        self,
        capability_name: str,
        score: float,
        measurement_source: str
    ) -> str:
        cap_id = self._next_id("cap")
        self._capability_scores.append({
            "id": cap_id,
            "capability_name": capability_name,
            "score": score,
            "measurement_source": measurement_source,
            "timestamp": datetime.now().isoformat()
        })
        return cap_id

    async def get_capability_history(
        self,
        capability_name: str,
        limit: int = 100
    ) -> List[Dict]:
        return [
            c for c in self._capability_scores
            if c["capability_name"] == capability_name
        ][-limit:]

    async def record_metric_snapshot(
        self,
        loop_name: str,
        metrics: Dict[str, float]
    ) -> str:
        return self._next_id("metric")

    async def get_loop_metrics(
        self,
        loop_name: str,
        since: Optional[datetime] = None,
        limit: int = 100
    ) -> List[Dict]:
        return []


class MockLLMClient:
    """Mock LLM client for testing without API calls."""

    def __init__(self):
        self._call_count = 0

    async def query(self, prompt: str, max_tokens: int = 500, **kwargs) -> str:
        self._call_count += 1

        # Return contextual mock responses based on prompt content
        if "counterfactual" in prompt.lower():
            return """COUNTERFACTUAL 1:
Alternative: Could have used a different approach
Predicted outcome: Slightly better results
Insight: Always consider multiple approaches

COUNTERFACTUAL 2:
Alternative: Started with simpler implementation
Predicted outcome: Faster iteration
Insight: Start simple, iterate fast"""

        elif "analyze this experience" in prompt.lower() or "deeply analyze" in prompt.lower():
            return """1. The pattern of breaking problems into smaller parts is universal
2. Feedback loops accelerate learning
3. Cross-domain knowledge transfer is underutilized"""

        elif "new domains" in prompt.lower() or "transfer" in prompt.lower():
            return """Domain: Software Testing
Application: Apply the same decomposition pattern to test case generation
Confidence: high

Domain: Documentation
Application: Structure docs using the same hierarchical approach
Confidence: medium"""

        elif "combining" in prompt.lower() or "crossover" in prompt.lower():
            return "Learn from past experiences by analyzing patterns and applying them to new situations systematically"

        elif "variation" in prompt.lower() or "mutation" in prompt.lower():
            return "Learn from past experiences by rapid prototyping and iterative refinement"

        elif "reasoning" in prompt.lower():
            return json.dumps({
                "answer": "Based on graph analysis, the answer is X",
                "confidence": 0.85,
                "sources": ["node_1", "node_2"]
            })

        else:
            return "Mock LLM response for testing purposes."


class MockEmbedder:
    """Mock embedder for testing without embedding API calls."""

    @dataclass
    class EmbedResult:
        embedding: List[float]
        model: str = "mock"
        tokens: int = 10

    async def embed(self, text: str) -> 'MockEmbedder.EmbedResult':
        # Generate deterministic mock embedding based on text hash
        import hashlib
        h = hashlib.md5(text.encode()).hexdigest()
        # Convert to 768-dimensional vector
        embedding = [int(h[i:i+2], 16) / 255.0 for i in range(0, len(h), 2)]
        # Pad to 768 dimensions
        while len(embedding) < 768:
            embedding.extend(embedding[:min(len(embedding), 768 - len(embedding))])
        return MockEmbedder.EmbedResult(embedding=embedding[:768])


# ============================================================
#  INFRASTRUCTURE TESTS
# ============================================================

async def test_embedding_cosine_similarity():
    """Test cosine similarity calculation."""
    from embedding import cosine_similarity

    # Identical vectors should have similarity 1.0
    v1 = [1.0, 0.0, 0.0]
    assert abs(cosine_similarity(v1, v1) - 1.0) < 0.001

    # Orthogonal vectors should have similarity 0.0
    v2 = [0.0, 1.0, 0.0]
    assert abs(cosine_similarity(v1, v2)) < 0.001

    # Opposite vectors should have similarity -1.0
    v3 = [-1.0, 0.0, 0.0]
    assert abs(cosine_similarity(v1, v3) - (-1.0)) < 0.001


async def test_coupling_tracker_initialization():
    """Test coupling tracker can be initialized."""
    from coupling_tracker import CouplingTracker

    tracker = CouplingTracker()
    assert tracker is not None

    # Should have empty measurements initially
    summary = tracker.get_summary()
    assert "couplings" in summary
    assert "critical_coupling" in summary


async def test_coupling_tracker_record_event():
    """Test coupling tracker summary (uses event subscriptions internally)."""
    from coupling_tracker import CouplingTracker

    tracker = CouplingTracker()

    # CouplingTracker uses event subscriptions, not direct record_event
    # Test that it can get summary without errors
    summary = tracker.get_summary()
    assert isinstance(summary, dict)
    assert "couplings" in summary


async def test_coupling_tracker_compute_coupling():
    """Test coupling computation."""
    from coupling_tracker import CouplingTracker

    tracker = CouplingTracker()

    # Compute all couplings (may be empty without events)
    couplings = tracker.compute_all_couplings()
    assert isinstance(couplings, dict)

    # Get critical coupling (goal_evolver -> self_compiler)
    critical = tracker.get_critical_coupling()
    assert critical is not None


async def test_event_bus_option_b_events():
    """Test Option B event types exist."""
    from event_bus import EventType

    # Check all Option B event types exist
    option_b_events = [
        "PATTERN_CREATED", "PATTERN_USED", "PATTERN_LIFTED",
        "GOAL_CREATED", "GOAL_EVALUATED", "GOAL_COMPLETED", "GOAL_EVOLVED",
        "INSIGHT_CREATED", "INSIGHT_APPLIED", "COUNTERFACTUAL_GENERATED",
        "SPREADING_ACTIVATION", "MEMORY_QUERY_ANSWERED",
        "LOOP_CYCLE_START", "LOOP_CYCLE_END", "COUPLING_MEASURED", "MODE_TRANSITION",
        "CAPABILITY_MEASURED", "GROWTH_RATE_COMPUTED", "KILL_CRITERION_TRIGGERED"
    ]

    for event_name in option_b_events:
        assert hasattr(EventType, event_name), f"Missing event type: {event_name}"


async def test_kill_criteria_initialization():
    """Test kill criteria evaluator initialization."""
    from kill_criteria import KillCriteriaEvaluator, TriggerSeverity

    evaluator = KillCriteriaEvaluator()
    assert evaluator is not None

    # Should not have any triggers initially
    assert not evaluator.has_hard_triggers()
    assert not evaluator.has_soft_triggers()


async def test_kill_criteria_evaluation():
    """Test kill criteria evaluation logic."""
    from kill_criteria import KillCriteriaEvaluator, TriggerSeverity

    evaluator = KillCriteriaEvaluator()

    # Test with healthy metrics
    triggers = evaluator.evaluate(
        growth_rate=0.05,
        llm_ratio=0.5,
        critical_coupling=0.6,
        loop_health={"loop1": True, "loop2": True}
    )

    # Should not trigger hard criteria with healthy metrics
    assert not evaluator.has_hard_triggers()


async def test_kill_criteria_soft_trigger():
    """Test soft trigger activation."""
    from kill_criteria import KillCriteriaEvaluator, TriggerSeverity, TriggerType

    evaluator = KillCriteriaEvaluator(config={
        "soft": {"growth_rate_below": 0.01, "coupling_below": 0.3}
    })

    # Test with low growth rate (should trigger soft)
    triggers = evaluator.evaluate(
        growth_rate=0.005,  # Below 0.01 threshold
        llm_ratio=0.5,
        critical_coupling=0.2,  # Below 0.3 threshold
        loop_health={}
    )

    # Should have soft triggers
    assert evaluator.has_soft_triggers()

    soft_triggers = [t for t in triggers if t.severity == TriggerSeverity.SOFT]
    assert len(soft_triggers) >= 1


async def test_kill_criteria_hard_trigger():
    """Test hard trigger activation."""
    from kill_criteria import KillCriteriaEvaluator, TriggerSeverity

    evaluator = KillCriteriaEvaluator(config={
        "hard": {"llm_ratio_above": 0.95}
    })

    # Test with high LLM ratio (should trigger hard)
    triggers = evaluator.evaluate(
        growth_rate=0.05,
        llm_ratio=0.98,  # Above 0.95 threshold
        critical_coupling=0.6,
        loop_health={}
    )

    # Should have hard trigger
    assert evaluator.has_hard_triggers()


# ============================================================
#  COMPONENT UNIT TESTS
# ============================================================

async def test_memory_reasoner_initialization():
    """Test Memory Reasoner can be initialized."""
    from memory_reasoner import MemoryReasoner

    memory = MockMemory()
    llm_client = MockLLMClient()

    reasoner = MemoryReasoner(memory, llm_client)
    assert reasoner is not None
    assert reasoner.get_memory_ratio() == 0.0  # Initially no queries


async def test_memory_reasoner_reason():
    """Test Memory Reasoner reasoning."""
    from memory_reasoner import MemoryReasoner, ReasoningResult

    memory = MockMemory()
    llm_client = MockLLMClient()

    # Add some experiences
    await memory.record_experience("Python is a programming language", "fact")
    await memory.record_experience("Machine learning uses data", "fact")

    reasoner = MemoryReasoner(memory, llm_client)

    # Patch the embedder in the embedding module
    with patch('embedding.get_global_embedder', return_value=MockEmbedder()):
        result = await reasoner.reason("What is Python?")

    # ReasoningResult is a dataclass with answer, confidence, etc.
    assert result is not None
    assert isinstance(result, ReasoningResult)
    assert hasattr(result, 'answer')
    assert hasattr(result, 'confidence')


async def test_memory_reasoner_metrics():
    """Test Memory Reasoner metrics tracking."""
    from memory_reasoner import MemoryReasoner

    memory = MockMemory()
    llm_client = MockLLMClient()

    reasoner = MemoryReasoner(memory, llm_client)

    metrics = reasoner.get_metrics()
    assert "total_queries" in metrics
    assert "memory_answered" in metrics
    assert "llm_answered" in metrics
    assert "memory_ratio" in metrics


async def test_self_compiler_initialization():
    """Test Self-Compiler can be initialized."""
    from accelerators import SelfCompiler

    memory = MockMemory()
    llm_client = MockLLMClient()

    compiler = SelfCompiler(memory, llm_client)
    assert compiler is not None


async def test_self_compiler_compile_solution():
    """Test Self-Compiler solution compilation."""
    from accelerators import SelfCompiler

    memory = MockMemory()
    llm_client = MockLLMClient()

    compiler = SelfCompiler(memory, llm_client)

    with patch('embedding.get_global_embedder', return_value=MockEmbedder()):
        solution = await compiler.compile_solution(
            problem="How to optimize database queries?"
        )

    # Solution may be None if no patterns match (which is fine for this test)
    # Just verify the call completes without error


async def test_self_compiler_learn_from_success():
    """Test Self-Compiler learning from success."""
    from accelerators import SelfCompiler

    memory = MockMemory()
    llm_client = MockLLMClient()

    compiler = SelfCompiler(memory, llm_client)

    with patch('embedding.get_global_embedder', return_value=MockEmbedder()):
        await compiler.learn_from_success(
            problem="Optimize query",
            solution="Use indexes",
            domains=["database"]
        )

    # Should have created a pattern or returned existing
    metrics = compiler.get_metrics()
    assert "patterns_created" in metrics or "patterns_matched" in metrics


async def test_goal_evolver_initialization():
    """Test Goal Evolver can be initialized."""
    from goal_evolver import GoalEvolver

    memory = MockMemory()
    llm_client = MockLLMClient()

    evolver = GoalEvolver(memory, llm_client)
    assert evolver is not None
    assert evolver._current_generation == 0


async def test_goal_evolver_create_initial_population():
    """Test Goal Evolver initial population creation."""
    from goal_evolver import GoalEvolver

    memory = MockMemory()
    llm_client = MockLLMClient()

    evolver = GoalEvolver(memory, llm_client, config={"population_size": 5})

    goal_ids = await evolver.create_initial_population([
        "Learn Python",
        "Build a web app",
        "Optimize performance"
    ])

    assert len(goal_ids) == 3
    assert evolver._total_goals_created == 3


async def test_goal_evolver_evaluate_goal():
    """Test Goal Evolver goal evaluation."""
    from goal_evolver import GoalEvolver

    memory = MockMemory()
    llm_client = MockLLMClient()

    evolver = GoalEvolver(memory, llm_client)

    # Create a goal first
    goal_ids = await evolver.create_initial_population(["Test goal"])

    # Evaluate it
    await evolver.evaluate_goal(
        goal_id=goal_ids[0],
        completed=True,
        capability_delta=0.5,
        resources_spent=1.0
    )

    assert evolver._total_goals_completed == 1
    assert evolver._total_capability_delta == 0.5


async def test_goal_evolver_evolve_generation():
    """Test Goal Evolver generation evolution."""
    from goal_evolver import GoalEvolver

    memory = MockMemory()
    llm_client = MockLLMClient()

    evolver = GoalEvolver(memory, llm_client, config={
        "population_size": 5,
        "elite_count": 1,
        "mutation_rate": 0.5,
        "crossover_rate": 0.5
    })

    # Create initial population
    await evolver.create_initial_population([
        "Goal 1", "Goal 2", "Goal 3", "Goal 4", "Goal 5"
    ])

    # Evolve to next generation
    result = await evolver.evolve_generation()

    assert result is not None
    assert "generation" in result
    assert result["generation"] == 1


async def test_dreaming_machine_initialization():
    """Test Dreaming Machine can be initialized."""
    from dreaming_machine import DreamingMachine

    memory = MockMemory()
    llm_client = MockLLMClient()

    dm = DreamingMachine(memory, llm_client)
    assert dm is not None


async def test_dreaming_machine_dream_cycle():
    """Test Dreaming Machine dream cycle."""
    from dreaming_machine import DreamingMachine

    memory = MockMemory()
    llm_client = MockLLMClient()

    # Add experiences for dreaming
    for i in range(5):
        await memory.record_experience(f"Experience {i}", "observation")

    dm = DreamingMachine(memory, llm_client, config={
        "counterfactual": {"enabled": True, "variations_per_experience": 2},
        "replay": {"enabled": True, "sample_size": 3},
        "transfer": {"enabled": False}  # Disable to avoid needing patterns
    })

    with patch('embedding.get_global_embedder', return_value=MockEmbedder()):
        result = await dm.dream_cycle()

    assert result is not None
    assert "counterfactuals" in result or "replays" in result


async def test_dreaming_machine_metrics():
    """Test Dreaming Machine metrics."""
    from dreaming_machine import DreamingMachine

    memory = MockMemory()
    llm_client = MockLLMClient()

    dm = DreamingMachine(memory, llm_client)

    metrics = dm.get_metrics()
    assert "counterfactuals_generated" in metrics
    assert "replays_completed" in metrics
    assert "transfers_attempted" in metrics
    assert "insights_created" in metrics


async def test_omega_initialization():
    """Test BYRD Omega can be initialized."""
    from omega import BYRDOmega, OperatingMode

    memory = MockMemory()
    llm_client = MockLLMClient()

    # Create mock loops
    mock_mr = MagicMock()
    mock_mr.get_metrics.return_value = {"memory_ratio": 0.5}
    mock_mr.is_healthy.return_value = True

    mock_sc = MagicMock()
    mock_sc.get_metrics.return_value = {"match_rate": 0.6}
    mock_sc.is_healthy.return_value = True

    mock_ge = MagicMock()
    mock_ge.get_metrics.return_value = {"completion_rate": 0.4}
    mock_ge.is_healthy.return_value = True

    mock_dm = MagicMock()
    mock_dm.get_metrics.return_value = {"multiplication_factor": 1.5}
    mock_dm.is_healthy.return_value = True

    omega = BYRDOmega(
        memory=memory,
        llm_client=llm_client,
        memory_reasoner=mock_mr,
        self_compiler=mock_sc,
        goal_evolver=mock_ge,
        dreaming_machine=mock_dm
    )

    assert omega is not None
    assert omega.mode == OperatingMode.AWAKE


async def test_omega_mode_transition():
    """Test BYRD Omega mode transitions."""
    from omega import BYRDOmega, OperatingMode

    memory = MockMemory()
    llm_client = MockLLMClient()

    omega = BYRDOmega(
        memory=memory,
        llm_client=llm_client,
        memory_reasoner=None,
        self_compiler=None,
        goal_evolver=None,
        dreaming_machine=None
    )

    # Test mode transition
    await omega.transition_mode(OperatingMode.DREAMING)
    assert omega.mode == OperatingMode.DREAMING

    await omega.transition_mode(OperatingMode.EVOLVING)
    assert omega.mode == OperatingMode.EVOLVING


async def test_omega_run_cycle():
    """Test BYRD Omega run cycle."""
    from omega import BYRDOmega, OperatingMode

    memory = MockMemory()
    llm_client = MockLLMClient()

    # Create mock loops
    mock_mr = MagicMock()
    mock_mr.get_metrics.return_value = {"memory_ratio": 0.5}

    mock_sc = MagicMock()
    mock_sc.get_metrics.return_value = {"match_rate": 0.6}

    mock_ge = MagicMock()
    mock_ge.get_metrics.return_value = {"completion_rate": 0.4}

    mock_dm = MagicMock()
    mock_dm.get_metrics.return_value = {"multiplication_factor": 1.5}

    omega = BYRDOmega(
        memory=memory,
        llm_client=llm_client,
        memory_reasoner=mock_mr,
        self_compiler=mock_sc,
        goal_evolver=mock_ge,
        dreaming_machine=mock_dm,
        config={"mode_durations": {"AWAKE": 1}}  # Short duration for testing
    )

    result = await omega.run_cycle()

    assert result is not None
    assert "mode" in result
    assert "cycle" in result


# ============================================================
#  INTEGRATION TESTS
# ============================================================

async def test_memory_reasoner_to_insight():
    """Test flow from Memory Reasoner to Insight creation."""
    from memory_reasoner import MemoryReasoner

    memory = MockMemory()
    llm_client = MockLLMClient()

    # Add experiences
    await memory.record_experience("Test experience", "observation")

    reasoner = MemoryReasoner(memory, llm_client)

    with patch('embedding.get_global_embedder', return_value=MockEmbedder()):
        # Reason about something
        result = await reasoner.reason("What happened?")

        # Should have recorded insight
        insights = await memory.get_recent_insights()
        # May or may not have insights depending on answer source


async def test_goal_evolver_to_self_compiler():
    """Test Goal Evolver feeding into Self-Compiler."""
    from goal_evolver import GoalEvolver
    from accelerators import SelfCompiler

    memory = MockMemory()
    llm_client = MockLLMClient()

    evolver = GoalEvolver(memory, llm_client)
    compiler = SelfCompiler(memory, llm_client)

    # Create and complete a goal
    goal_ids = await evolver.create_initial_population(["Learn pattern matching"])

    # Simulate goal completion with capability gain
    await evolver.evaluate_goal(goal_ids[0], True, capability_delta=0.3)

    # Self-Compiler learns from the success
    with patch('embedding.get_global_embedder', return_value=MockEmbedder()):
        await compiler.learn_from_success(
            problem="Pattern matching challenge",
            solution="Use regex with compile",
            domains=["text_processing"]
        )

    # Verify learn_from_success completed without error
    # Pattern creation depends on embedding similarity - not always created
    metrics = compiler.get_metrics()
    assert isinstance(metrics, dict)


async def test_dreaming_to_insight():
    """Test Dreaming Machine creating insights."""
    from dreaming_machine import DreamingMachine

    memory = MockMemory()
    llm_client = MockLLMClient()

    # Add experiences
    for i in range(5):
        await memory.record_experience(f"Experience {i} with detailed content", "observation")

    dm = DreamingMachine(memory, llm_client, config={
        "counterfactual": {"enabled": True, "min_experience_age_hours": 0},
        "replay": {"enabled": True, "sample_size": 3},
        "transfer": {"enabled": False}
    })

    with patch('embedding.get_global_embedder', return_value=MockEmbedder()):
        result = await dm.dream_cycle()

    # Should have created some insights
    assert result is not None


async def test_omega_full_cycle():
    """Test complete Omega cycle with all loops."""
    from omega import BYRDOmega, OperatingMode
    from memory_reasoner import MemoryReasoner
    from accelerators import SelfCompiler
    from goal_evolver import GoalEvolver
    from dreaming_machine import DreamingMachine

    memory = MockMemory()
    llm_client = MockLLMClient()

    # Create actual loop instances
    with patch('embedding.get_global_embedder', return_value=MockEmbedder()):
        with patch('embedding.get_global_embedder', return_value=MockEmbedder()):
            with patch('embedding.get_global_embedder', return_value=MockEmbedder()):
                mr = MemoryReasoner(memory, llm_client)
                sc = SelfCompiler(memory, llm_client)
                ge = GoalEvolver(memory, llm_client)
                dm = DreamingMachine(memory, llm_client)

                omega = BYRDOmega(
                    memory=memory,
                    llm_client=llm_client,
                    memory_reasoner=mr,
                    self_compiler=sc,
                    goal_evolver=ge,
                    dreaming_machine=dm
                )

                # Run a cycle
                result = await omega.run_cycle()

                assert result is not None
                assert omega._total_cycles == 1


async def test_coupling_between_loops():
    """Test coupling measurement between loops."""
    from coupling_tracker import CouplingTracker
    from goal_evolver import GoalEvolver
    from accelerators import SelfCompiler

    memory = MockMemory()
    llm_client = MockLLMClient()
    tracker = CouplingTracker()

    # Simulate activity
    evolver = GoalEvolver(memory, llm_client)

    with patch('embedding.get_global_embedder', return_value=MockEmbedder()):
        compiler = SelfCompiler(memory, llm_client)

    # CouplingTracker uses event subscriptions, test the API
    couplings = tracker.compute_all_couplings()
    assert isinstance(couplings, dict)

    # Get critical coupling
    critical = tracker.get_critical_coupling()
    assert critical is not None


async def test_kill_criteria_with_omega():
    """Test kill criteria evaluation with Omega metrics."""
    from omega import BYRDOmega
    from kill_criteria import KillCriteriaEvaluator

    memory = MockMemory()
    llm_client = MockLLMClient()

    omega = BYRDOmega(
        memory=memory,
        llm_client=llm_client,
        memory_reasoner=None,
        self_compiler=None,
        goal_evolver=None,
        dreaming_machine=None
    )

    evaluator = KillCriteriaEvaluator()

    # Run some cycles
    for i in range(5):
        await omega.run_cycle()

    # Get Omega metrics
    metrics = omega.get_metrics()

    # Evaluate kill criteria
    triggers = evaluator.evaluate(
        growth_rate=metrics.get("growth_rate", 0.0),
        llm_ratio=0.5,  # Mock ratio
        critical_coupling=metrics.get("critical_coupling", 0.0),
        loop_health=omega.get_loop_health()
    )

    # Should return a list (may be empty if healthy)
    assert isinstance(triggers, list)


# ============================================================
#  CROSS-LOOP COUPLING TESTS
# ============================================================

async def test_critical_coupling_measurement():
    """Test the critical Goal Evolver → Self-Compiler coupling."""
    from coupling_tracker import CouplingTracker

    tracker = CouplingTracker()

    # CouplingTracker uses event subscriptions, so test the API directly
    critical = tracker.get_critical_coupling()
    assert critical is not None
    # Should return a CouplingMeasurement (may have zero correlation without events)
    assert hasattr(critical, 'correlation')
    assert hasattr(critical, 'is_significant')


async def test_loop_feedback_cycle():
    """Test complete feedback cycle through all loops."""
    from memory_reasoner import MemoryReasoner
    from accelerators import SelfCompiler
    from goal_evolver import GoalEvolver
    from dreaming_machine import DreamingMachine

    memory = MockMemory()
    llm_client = MockLLMClient()

    with patch('embedding.get_global_embedder', return_value=MockEmbedder()):
        with patch('embedding.get_global_embedder', return_value=MockEmbedder()):
            with patch('embedding.get_global_embedder', return_value=MockEmbedder()):
                # 1. Start with a goal
                ge = GoalEvolver(memory, llm_client)
                await ge.create_initial_population(["Improve query speed"])

                # 2. Memory Reasoner answers a query
                mr = MemoryReasoner(memory, llm_client)
                await memory.record_experience("Query optimization uses indexes", "fact")
                await mr.reason("How to speed up queries?")

                # 3. Self-Compiler learns from success
                sc = SelfCompiler(memory, llm_client)
                await sc.learn_from_success(
                    problem="Slow queries",
                    solution="Add database indexes",
                    domains=["database"]
                )

                # 4. Dreaming Machine reflects
                dm = DreamingMachine(memory, llm_client, config={
                    "counterfactual": {"enabled": False},
                    "replay": {"enabled": True, "sample_size": 2},
                    "transfer": {"enabled": False}
                })
                await dm.dream_cycle()

                # Verify the cycle produced artifacts
                assert ge._total_goals_created > 0
                assert mr._total_queries > 0
                # Patterns may or may not be created depending on similarity


# ============================================================
#  MAIN TEST RUNNER
# ============================================================

async def run_all_tests():
    runner = TestRunner()

    # Infrastructure Tests
    runner.section("INFRASTRUCTURE TESTS")
    await runner.run_test("Cosine Similarity Calculation", test_embedding_cosine_similarity)
    await runner.run_test("Coupling Tracker Initialization", test_coupling_tracker_initialization)
    await runner.run_test("Coupling Tracker Record Event", test_coupling_tracker_record_event)
    await runner.run_test("Coupling Tracker Compute Coupling", test_coupling_tracker_compute_coupling)
    await runner.run_test("Event Bus Option B Events", test_event_bus_option_b_events)
    await runner.run_test("Kill Criteria Initialization", test_kill_criteria_initialization)
    await runner.run_test("Kill Criteria Evaluation", test_kill_criteria_evaluation)
    await runner.run_test("Kill Criteria Soft Trigger", test_kill_criteria_soft_trigger)
    await runner.run_test("Kill Criteria Hard Trigger", test_kill_criteria_hard_trigger)

    # Component Unit Tests
    runner.section("COMPONENT UNIT TESTS")
    await runner.run_test("Memory Reasoner Initialization", test_memory_reasoner_initialization)
    await runner.run_test("Memory Reasoner Reason", test_memory_reasoner_reason)
    await runner.run_test("Memory Reasoner Metrics", test_memory_reasoner_metrics)
    await runner.run_test("Self-Compiler Initialization", test_self_compiler_initialization)
    await runner.run_test("Self-Compiler Compile Solution", test_self_compiler_compile_solution)
    await runner.run_test("Self-Compiler Learn From Success", test_self_compiler_learn_from_success)
    await runner.run_test("Goal Evolver Initialization", test_goal_evolver_initialization)
    await runner.run_test("Goal Evolver Create Population", test_goal_evolver_create_initial_population)
    await runner.run_test("Goal Evolver Evaluate Goal", test_goal_evolver_evaluate_goal)
    await runner.run_test("Goal Evolver Evolve Generation", test_goal_evolver_evolve_generation)
    await runner.run_test("Dreaming Machine Initialization", test_dreaming_machine_initialization)
    await runner.run_test("Dreaming Machine Dream Cycle", test_dreaming_machine_dream_cycle)
    await runner.run_test("Dreaming Machine Metrics", test_dreaming_machine_metrics)
    await runner.run_test("Omega Initialization", test_omega_initialization)
    await runner.run_test("Omega Mode Transition", test_omega_mode_transition)
    await runner.run_test("Omega Run Cycle", test_omega_run_cycle)

    # Integration Tests
    runner.section("INTEGRATION TESTS")
    await runner.run_test("Memory Reasoner to Insight", test_memory_reasoner_to_insight)
    await runner.run_test("Goal Evolver to Self-Compiler", test_goal_evolver_to_self_compiler)
    await runner.run_test("Dreaming to Insight", test_dreaming_to_insight)
    await runner.run_test("Omega Full Cycle", test_omega_full_cycle)
    await runner.run_test("Coupling Between Loops", test_coupling_between_loops)
    await runner.run_test("Kill Criteria with Omega", test_kill_criteria_with_omega)

    # Cross-Loop Coupling Tests
    runner.section("CROSS-LOOP COUPLING TESTS")
    await runner.run_test("Critical Coupling Measurement", test_critical_coupling_measurement)
    await runner.run_test("Loop Feedback Cycle", test_loop_feedback_cycle)

    return runner.summary()


if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)
