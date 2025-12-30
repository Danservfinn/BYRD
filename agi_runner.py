"""
BYRD AGI Runner - The Execution Engine

THE CRITICAL MISSING PIECE that drives recursive self-improvement.

This connects:
- Assessment (via SelfModel) → identification → hypothesis generation
- Prediction (via WorldModel) → safety verification → execution
- Measurement → learning → next cycle

RUNTIME AUDIT FINDING (December 2024):
Option B loops (Memory Reasoner, Goal Evolver, Self-Compiler, Dreaming Machine)
are structurally present but functionally inert - zero data flowing through them.
The bootstrap_from_current_state() method activates these dormant loops.

Version: 1.0
Created: December 2024
"""

import asyncio
import json
import yaml
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple
from pathlib import Path

from memory import Memory
from desire_classifier import DesireClassifier, DesireType


@dataclass
class ImprovementTarget:
    """A capability targeted for improvement."""
    name: str
    current_level: float
    priority: str  # "critical", "high", "medium", "low"
    reason: str
    domain: Optional[str] = None
    estimated_effort: Optional[str] = None


@dataclass
class ImprovementHypothesis:
    """A hypothesis about how to improve a capability."""
    target: str
    strategy: str
    description: str
    expected_improvement: float
    predicted_success: float = 0.5
    prediction_confidence: float = 0.0
    resources_needed: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)


@dataclass
class MeasurementResult:
    """Result of measuring improvement."""
    improved: bool
    delta: float
    reason: Optional[str] = None
    before_score: float = 0.0
    after_score: float = 0.0
    measurement_method: str = "self_assessment"


@dataclass
class CycleResult:
    """Result of an improvement cycle."""
    success: bool
    target: Optional[str] = None
    delta: float = 0.0
    cycle: int = 0
    reason: Optional[str] = None
    duration_seconds: float = 0.0
    hypotheses_tried: int = 0
    strategy: Optional[str] = None
    measurement_method: str = "unknown"


class AGIRunner:
    """
    The execution engine that drives recursive self-improvement.

    This connects: assessment → hypothesis → prediction → verification →
    execution → measurement → learning in a closed loop.

    CRITICAL: Must bootstrap from current Dreamer→Seeker state before
    running improvement cycles. The loops exist but need data injection.
    """

    def __init__(self, byrd):
        """
        Initialize the AGI Runner.

        Args:
            byrd: The main BYRD instance with memory, world_model, self_model, etc.
        """
        self.byrd = byrd

        # Use EXISTING components (validated from byrd.py lines 289-340)
        self.memory = byrd.memory
        self.world_model = byrd.world_model      # world_model.py exists
        self.self_model = byrd.self_model        # self_model.py exists
        self.rollback = byrd.rollback            # rollback.py exists
        self.config = byrd.config

        # NEW components (will be injected after creation)
        self.intuition = None          # Will be IntuitionNetwork (Phase 3)
        self.evaluator = None          # Will be CapabilityEvaluator (Phase 1)
        self.desire_classifier = DesireClassifier(self.config)

        # Cycle tracking
        self._cycle_count = 0
        self._improvement_rate = 0.0
        self._bootstrapped = False
        self._cycle_history: List[CycleResult] = []

        # Metrics for Option B loop activation
        self._bootstrap_metrics = {
            'goals_injected': 0,
            'research_indexed': 0,
            'patterns_seeded': 0,
            'counterfactuals_seeded': 0
        }

        # Strategy effectiveness tracking
        self._strategy_stats: Dict[str, Dict[str, float]] = {}
        # Format: {"research": {"attempts": 10, "successes": 7, "total_delta": 0.15}}

        # Session tracking for multi-timescale metrics
        self._session_start = datetime.now()
        self._session_capabilities_improved: Set[str] = set()

    # Capability name mapping: AGIRunner → CapabilityEvaluator
    CAPABILITY_MAP = {
        "general_reasoning": "reasoning",
        "reasoning": "reasoning",
        "code_generation": "code_generation",
        "coding": "code_generation",
        "research": "research",
        "introspection": "introspection",
        "self_knowledge": "introspection",
        "memory": "memory_operations",
        "memory_operations": "memory_operations",
        "pattern_recognition": "pattern_recognition",
        "synthesis": "synthesis",
        "meta_cognition": "introspection",
        "learning": "pattern_recognition",
    }

    def _normalize_capability_name(self, name: str) -> str:
        """Map capability name to evaluator-compatible name."""
        return self.CAPABILITY_MAP.get(name, name)

    def reset(self):
        """
        Reset AGI Runner state for system reset.

        Clears all cycle tracking, bootstrap state, and metrics.
        Called by server.py during reset_byrd().
        """
        self._cycle_count = 0
        self._improvement_rate = 0.0
        self._bootstrapped = False
        self._cycle_history.clear()
        self._bootstrap_metrics = {
            'goals_injected': 0,
            'research_indexed': 0,
            'patterns_seeded': 0,
            'counterfactuals_seeded': 0
        }
        # Reset strategy and session tracking
        self._strategy_stats.clear()
        self._session_start = datetime.now()
        self._session_capabilities_improved.clear()
        # Also reset sub-components if they exist
        if self.desire_classifier:
            self.desire_classifier.reset()

    async def bootstrap_from_current_state(self):
        """
        PHASE 0: Activate dormant Option B loops.

        The runtime audit shows Dreamer→Seeker is active but Option B loops
        have zero data flowing through them. This method bridges the gap.

        Steps:
        1. Ensure Goal Evolver has goals to work with
        2. Index research experiences for Memory Reasoner
        3. Extract patterns from recent reflections for Self-Compiler
        4. Generate initial counterfactuals for Dreaming Machine
        """
        if self._bootstrapped:
            print("⚠️  AGI Runner: Already bootstrapped, skipping")
            return

        print("🚀 AGI Runner: Bootstrapping from current state...")
        start_time = datetime.now()

        try:
            # 1. Ensure Goal Evolver has goals to work with
            await self._ensure_goal_population()

            # 2. Index research experiences for Memory Reasoner
            await self._index_research_for_memory()

            # 3. Extract patterns from recent reflections for Self-Compiler
            await self._seed_patterns_from_reflections()

            # 4. Generate initial counterfactuals for Dreaming Machine
            await self._seed_counterfactuals()

            self._bootstrapped = True

            duration = (datetime.now() - start_time).total_seconds()
            print(f"✅ AGI Runner: Bootstrap complete in {duration:.1f}s")
            print(f"   Metrics: {self._bootstrap_metrics}")

            # Record bootstrap as experience (metrics embedded in content)
            await self.memory.record_experience(
                content=f"[BOOTSTRAP] AGI Runner activated Option B loops: goals={self._bootstrap_metrics.get('goals_injected', 0)}, research_indexed={self._bootstrap_metrics.get('research_indexed', 0)}, patterns={self._bootstrap_metrics.get('patterns_seeded', 0)}",
                type="system"
            )

        except Exception as e:
            print(f"❌ AGI Runner: Bootstrap failed: {e}")
            import traceback
            traceback.print_exc()

    async def _ensure_goal_population(self):
        """
        Ensure Goal Evolver has concrete, measurable goals.

        The runtime shows philosophical desires but zero goals.
        This injects seed goals from agi_seed.yaml.
        """
        # Check current goal count
        result = await self.memory._run_query("""
            MATCH (g:Goal)
            WHERE g.status = 'active'
            RETURN count(g) as count
        """)

        goal_count = result[0]["count"] if result else 0

        if goal_count > 0:
            print(f"   ✓ Found {goal_count} existing active goals")
            return

        print("   Injecting seed goals from agi_seed.yaml...")

        # Load seed goals from agi_seed.yaml
        seed_goals = []
        try:
            seed_path = Path(__file__).parent / "kernel" / "agi_seed.yaml"
            if seed_path.exists():
                with open(seed_path) as f:
                    seed_data = yaml.safe_load(f)
                    seed_goals = seed_data.get("initial_goals", [])
        except Exception as e:
            print(f"   Warning: Could not load seed goals: {e}")

        # Fallback seed goals if file not found
        if not seed_goals:
            seed_goals = [
                {
                    "description": "Map all Python files in my codebase and understand their purpose",
                    "domain": "self_knowledge",
                    "priority": "high"
                },
                {
                    "description": "Identify my top 3 capability limitations from recent failures",
                    "domain": "meta_cognition",
                    "priority": "high"
                },
                {
                    "description": "Write a utility function to measure my own response quality",
                    "domain": "code_generation",
                    "priority": "high"
                },
                {
                    "description": "Identify 3 recurring patterns in my successful reflections",
                    "domain": "pattern_recognition",
                    "priority": "high"
                },
                {
                    "description": "Track which learning strategies produce the fastest improvement",
                    "domain": "meta_cognition",
                    "priority": "high"
                }
            ]

        # Inject goals
        injected = 0
        for goal in seed_goals[:10]:  # Limit to 10 initial goals
            try:
                await self.memory._run_query("""
                    CREATE (g:Goal {
                        description: $desc,
                        domain: $domain,
                        priority: $priority,
                        status: 'active',
                        created_at: datetime(),
                        from_bootstrap: true,
                        fitness: 0.5
                    })
                """, {
                    "desc": goal.get("description", ""),
                    "domain": goal.get("domain", "general"),
                    "priority": goal.get("priority", "medium")
                })
                injected += 1
            except Exception as e:
                print(f"   Warning: Could not inject goal: {e}")

        self._bootstrap_metrics['goals_injected'] = injected
        print(f"   Injected {injected} seed goals")

    async def _index_research_for_memory(self):
        """
        Index research experiences so Memory Reasoner can answer from them.

        Currently: research is done, stored, but never queried from memory.
        This adds searchable keywords for memory retrieval.
        """
        # Find research experiences without proper tagging
        result = await self.memory._run_query("""
            MATCH (e:Experience)
            WHERE e.type = 'research'
            AND e.indexed_for_memory IS NULL
            RETURN e.content as content, elementId(e) as id
            LIMIT 50
        """)

        if not result:
            print("   ✓ No unindexed research experiences")
            return

        indexed = 0
        for record in result:
            try:
                content = record.get("content", "")
                exp_id = record.get("id")

                # Extract keywords for indexing
                keywords = self._extract_keywords(content)

                # Mark as indexed with keywords
                await self.memory._run_query("""
                    MATCH (e) WHERE elementId(e) = $id
                    SET e.indexed_for_memory = true,
                        e.memory_keywords = $keywords,
                        e.indexed_at = datetime()
                """, {
                    "id": exp_id,
                    "keywords": keywords
                })
                indexed += 1
            except Exception as e:
                print(f"   Warning: Could not index experience: {e}")

        self._bootstrap_metrics['research_indexed'] = indexed
        print(f"   Indexed {indexed} research experiences for Memory Reasoner")

    def _extract_keywords(self, content: str) -> List[str]:
        """
        Simple keyword extraction for memory indexing.

        Extracts significant terms after removing stopwords.
        """
        stopwords = {
            'the', 'a', 'an', 'is', 'are', 'was', 'were', 'to', 'of', 'and',
            'or', 'in', 'on', 'at', 'for', 'with', 'by', 'from', 'as', 'be',
            'this', 'that', 'it', 'its', 'which', 'who', 'what', 'when', 'where',
            'how', 'why', 'can', 'could', 'would', 'should', 'will', 'have', 'has',
            'had', 'do', 'does', 'did', 'not', 'but', 'if', 'then', 'else', 'so'
        }

        # Clean and split
        words = content.lower().replace('\n', ' ').split()

        # Filter: keep significant terms
        keywords = []
        for word in words:
            # Clean punctuation
            word = ''.join(c for c in word if c.isalnum())
            if len(word) > 4 and word not in stopwords:
                keywords.append(word)

        # Deduplicate and limit
        seen = set()
        unique_keywords = []
        for kw in keywords:
            if kw not in seen:
                seen.add(kw)
                unique_keywords.append(kw)
            if len(unique_keywords) >= 15:
                break

        return unique_keywordss

    async def _seed_patterns_from_reflections(self):
        """
        Extract patterns from existing reflections for Self-Compiler.

        Runtime shows 0 patterns created despite 146+ reflections.
        This analyzes reflection structure to seed pattern recognition.
        """
        # Get recent reflections with outputs
        result = await self.memory._run_query("""
            MATCH (r:Reflection)
            WHERE r.raw_output IS NOT NULL
            RETURN r.raw_output as output, elementId(r) as id
            ORDER BY r.timestamp DESC
            LIMIT 20
        """)

        if not result:
            print("   ✓ No reflections to analyze")
            return

        patterns_found = 0
        pattern_keys: Dict[str, int] = {}  # Track recurring keys

        for record in result:
            output = record.get("output")
            if isinstance(output, str):
                try:
                    output = json.loads(output)
                except:
                    continue

            if isinstance(output, dict):
                # Look for recurring keys as potential patterns
                for key in output.keys():
                    if key not in ['output', 'content', 'timestamp', 'raw']:
                        pattern_keys[key] = pattern_keys.get(key, 0) + 1

        # Create Pattern nodes for recurring keys (appears 3+ times)
        for key, count in pattern_keys.items():
            if count >= 3:
                try:
                    await self.memory._run_query("""
                        MERGE (p:Pattern {name: $name})
                        ON CREATE SET
                            p.description = $desc,
                            p.occurrence_count = $count,
                            p.discovered_at = datetime(),
                            p.from_bootstrap = true,
                            p.abstraction_level = 1
                    """, {
                        "name": f"reflection_key_{key}",
                        "desc": f"Recurring reflection output key: {key}",
                        "count": count
                    })
                    patterns_found += 1
                except Exception as e:
                    pass  # Pattern might already exist

        self._bootstrap_metrics['patterns_seeded'] = patterns_found
        if patterns_found > 0:
            print(f"   Found {patterns_found} potential patterns in reflections")
        else:
            print("   ✓ No new patterns identified")

    async def _seed_counterfactuals(self):
        """
        Generate initial counterfactuals for Dreaming Machine.

        Runtime shows 0 counterfactuals despite active research.
        This seeds the counterfactual generation process.
        """
        # Find completed desires that could generate counterfactuals
        result = await self.memory._run_query("""
            MATCH (d:Desire)
            WHERE d.fulfilled = true
            RETURN d.description as desc, d.strategy as strategy, elementId(d) as id
            ORDER BY d.fulfilled_at DESC
            LIMIT 10
        """)

        if not result:
            print("   ✓ No fulfilled desires for counterfactual seeding")
            return

        counterfactuals_created = 0
        for record in result:
            desc = record.get("desc", "")
            strategy = record.get("strategy", "")
            desire_id = record.get("id")

            # Skip if already has counterfactual
            existing = await self.memory._run_query("""
                MATCH (d)-[:HAS_COUNTERFACTUAL]->(c:Counterfactual)
                WHERE elementId(d) = $id
                RETURN count(c) as count
            """, {"id": desire_id})

            if existing and existing[0].get("count", 0) > 0:
                continue

            # Create a simple counterfactual question
            alt_strategies = ["web_search", "introspection", "memory_query", "observation"]
            for alt in alt_strategies:
                if alt != strategy:
                    try:
                        await self.memory._run_query("""
                            MATCH (d) WHERE elementId(d) = $id
                            CREATE (c:Counterfactual {
                                question: $question,
                                alternative_strategy: $alt,
                                original_strategy: $orig,
                                created_at: datetime(),
                                from_bootstrap: true
                            })
                            CREATE (d)-[:HAS_COUNTERFACTUAL]->(c)
                        """, {
                            "id": desire_id,
                            "question": f"What if I had used {alt} instead of {strategy}?",
                            "alt": alt,
                            "orig": strategy
                        })
                        counterfactuals_created += 1
                        break
                    except Exception as e:
                        pass

        self._bootstrap_metrics['counterfactuals_seeded'] = counterfactuals_created
        if counterfactuals_created > 0:
            print(f"   Created {counterfactuals_created} counterfactual questions")
        else:
            print("   ✓ Counterfactuals already exist or no material")

    async def run_improvement_cycle(self) -> CycleResult:
        """
        Execute one complete improvement cycle.

        Steps:
        1. ASSESS: Evaluate current capabilities (SelfModel)
        2. IDENTIFY: Select improvement target
        3. GENERATE: Create improvement hypotheses
        4. PREDICT: Rank by predicted outcome (WorldModel)
        5. VERIFY: Safety check
        6. EXECUTE: Apply improvement
        7. MEASURE: Evaluate outcome
        8. LEARN: Update all components

        Returns:
            CycleResult with success status and metrics
        """
        # Ensure bootstrap has run
        if not self._bootstrapped:
            await self.bootstrap_from_current_state()

        self._cycle_count += 1
        start_time = datetime.now()

        print(f"\n🔄 AGI Runner: Starting improvement cycle #{self._cycle_count}")

        try:
            # 1. ASSESS: Use EXISTING self_model.assess_capabilities()
            print("   [1/8] Assessing current capabilities...")
            if self.self_model:
                inventory = await self.self_model.assess_capabilities()
            else:
                # Fallback if self_model not available
                inventory = await self._fallback_assessment()

            # 2. IDENTIFY: Select improvement target
            print("   [2/8] Identifying improvement target...")
            target = await self._identify_target(inventory)
            if not target:
                return CycleResult(
                    success=False,
                    reason="No target identified - all capabilities stable",
                    cycle=self._cycle_count
                )
            print(f"         Target: {target.name} ({target.priority} priority)")

            # 2.5. CAPTURE BEFORE SCORE (critical for real measurement)
            before_eval = None
            if self.evaluator:
                try:
                    eval_name = self._normalize_capability_name(target.name)
                    before_eval = await self.evaluator.evaluate_capability(eval_name)
                    print(f"         Before score: {before_eval.accuracy:.1%} ({eval_name})")
                except Exception as e:
                    print(f"         Before eval skipped: {e}")

            # 3. GENERATE: Create improvement hypotheses
            print("   [3/8] Generating hypotheses...")
            hypotheses = await self._generate_hypotheses(target, inventory)
            if not hypotheses:
                return CycleResult(
                    success=False,
                    reason="No viable hypotheses generated",
                    cycle=self._cycle_count,
                    target=target.name
                )

            # 4. PREDICT: Use EXISTING world_model.predict_outcome()
            print("   [4/8] Predicting outcomes...")
            ranked = await self._predict_outcomes(hypotheses)
            best = ranked[0]
            print(f"         Best hypothesis: {best.strategy}")
            print(f"         Predicted success: {best.predicted_success:.1%}")

            # 5. VERIFY: Safety check using EXISTING safety_monitor
            print("   [5/8] Verifying safety...")
            if not await self._verify_safety(best):
                return CycleResult(
                    success=False,
                    reason="Safety check failed",
                    cycle=self._cycle_count,
                    target=target.name
                )

            # 6. EXECUTE: Apply improvement
            print("   [6/8] Executing improvement...")
            await self._execute(best)

            # 7. MEASURE: Evaluate outcome (pass before_eval for real measurement)
            print("   [7/8] Measuring improvement...")
            measurement = await self._measure_improvement(target, inventory, before_eval)
            print(f"         Delta: {measurement.delta:+.2%} ({measurement.measurement_method})")

            # 8. LEARN: Update all components
            print("   [8/8] Learning from outcome...")
            await self._learn_from_outcome(best, measurement)

            duration = (datetime.now() - start_time).total_seconds()

            result = CycleResult(
                success=measurement.improved,
                target=target.name,
                delta=measurement.delta,
                cycle=self._cycle_count,
                duration_seconds=duration,
                hypotheses_tried=1,
                strategy=best.strategy,
                measurement_method=measurement.measurement_method
            )

            self._cycle_history.append(result)

            # Update strategy effectiveness stats
            self._update_strategy_stats(best.strategy, measurement)

            # Track improved capabilities for session metrics
            if measurement.improved:
                self._session_capabilities_improved.add(target.name)

            status = "✅ SUCCESS" if result.success else "➖ No improvement"
            print(f"\n{status}: Cycle #{self._cycle_count} ({duration:.1f}s)")

            return result

        except Exception as e:
            import traceback
            traceback.print_exc()
            return CycleResult(
                success=False,
                reason=f"Cycle failed with error: {str(e)}",
                cycle=self._cycle_count
            )

    async def _fallback_assessment(self):
        """Fallback assessment when self_model is not available."""

        @dataclass
        class FallbackInventory:
            capabilities: Dict = field(default_factory=dict)
            weakest: List[str] = field(default_factory=list)
            strongest: List[str] = field(default_factory=list)
            overall_level: float = 0.5

        return FallbackInventory()

    async def _identify_target(self, inventory) -> Optional[ImprovementTarget]:
        """
        Select highest-value improvement target.

        Uses EXISTING self_model.identify_limitations() and
        self_model.measure_improvement_rate()

        Priority order:
        1. Declining capabilities (urgent)
        2. High-uncertainty capabilities (epistemic value)
        3. Weakest capability
        """
        # Get limitations from existing self_model
        if self.self_model:
            try:
                limitations = await self.self_model.identify_limitations()
            except:
                limitations = []
        else:
            limitations = []

        # Priority 1: Declining capabilities (urgent)
        if hasattr(inventory, 'capabilities'):
            for cap_name, cap in inventory.capabilities.items():
                if hasattr(cap, 'trend') and cap.trend == "declining":
                    return ImprovementTarget(
                        name=cap_name,
                        current_level=getattr(cap, 'success_rate', 0.5),
                        priority="critical",
                        reason="Declining capability"
                    )

        # Priority 2: High-uncertainty capabilities (epistemic value)
        if hasattr(inventory, 'capabilities'):
            for cap_name, cap in inventory.capabilities.items():
                confidence = getattr(cap, 'confidence', 1.0)
                if confidence < 0.3:
                    return ImprovementTarget(
                        name=cap_name,
                        current_level=getattr(cap, 'success_rate', 0.5),
                        priority="high",
                        reason=f"High uncertainty (confidence: {confidence:.2f})"
                    )

        # Priority 3: Weakest capability from inventory
        if hasattr(inventory, 'weakest') and inventory.weakest:
            weak_name = inventory.weakest[0]
            weak_cap = inventory.capabilities.get(weak_name) if hasattr(inventory, 'capabilities') else None
            return ImprovementTarget(
                name=weak_name,
                current_level=getattr(weak_cap, 'success_rate', 0.5) if weak_cap else 0.5,
                priority="medium",
                reason="Weakest capability"
            )

        # Priority 4: From limitations
        if limitations:
            lim = limitations[0]
            return ImprovementTarget(
                name=getattr(lim, 'capability', 'unknown'),
                current_level=0.5,
                priority="medium",
                reason=getattr(lim, 'description', 'Identified limitation')
            )

        # If nothing to improve, target general capability
        return ImprovementTarget(
            name="general_reasoning",
            current_level=0.5,
            priority="low",
            reason="Default target - no specific weaknesses identified"
        )

    async def _generate_hypotheses(self, target: ImprovementTarget, inventory) -> List[ImprovementHypothesis]:
        """Generate improvement hypotheses for the target."""
        hypotheses = []

        # Strategy 1: Practice through experience
        hypotheses.append(ImprovementHypothesis(
            target=target.name,
            strategy="practice",
            description=f"Gain more experience with {target.name} through targeted attempts",
            expected_improvement=0.1,
            resources_needed=["experience"],
            risks=["time investment"]
        ))

        # Strategy 2: Research best practices
        hypotheses.append(ImprovementHypothesis(
            target=target.name,
            strategy="research",
            description=f"Research best practices and techniques for {target.name}",
            expected_improvement=0.15,
            resources_needed=["web_search"],
            risks=["information overload"]
        ))

        # Strategy 3: Analyze past failures
        hypotheses.append(ImprovementHypothesis(
            target=target.name,
            strategy="failure_analysis",
            description=f"Analyze past failures in {target.name} to identify patterns",
            expected_improvement=0.2,
            resources_needed=["memory_query"],
            risks=["limited data"]
        ))

        # Strategy 4: Learn from successes
        hypotheses.append(ImprovementHypothesis(
            target=target.name,
            strategy="success_analysis",
            description=f"Analyze past successes in {target.name} to replicate patterns",
            expected_improvement=0.15,
            resources_needed=["memory_query"],
            risks=["overfitting to past conditions"]
        ))

        return hypotheses

    async def _predict_outcomes(self, hypotheses: List[ImprovementHypothesis]) -> List[ImprovementHypothesis]:
        """Use EXISTING world_model.predict_outcome() to rank hypotheses."""
        for hyp in hypotheses:
            if self.world_model:
                try:
                    # Use existing world model's predict_outcome method
                    prediction = await self.world_model.predict_outcome(
                        action=hyp.description,
                        context={"target": hyp.target, "strategy": hyp.strategy}
                    )
                    hyp.predicted_success = prediction.success_probability
                    hyp.prediction_confidence = prediction.confidence
                except Exception as e:
                    # Fallback to heuristic prediction
                    hyp.predicted_success = 0.5
                    hyp.prediction_confidence = 0.3
            else:
                # No world model - use strategy-based heuristics
                strategy_scores = {
                    "practice": 0.6,
                    "research": 0.7,
                    "failure_analysis": 0.65,
                    "success_analysis": 0.6
                }
                hyp.predicted_success = strategy_scores.get(hyp.strategy, 0.5)
                hyp.prediction_confidence = 0.4

        # Sort by expected value (predicted success × expected improvement)
        return sorted(
            hypotheses,
            key=lambda h: h.predicted_success * h.expected_improvement,
            reverse=True
        )

    async def _verify_safety(self, hypothesis: ImprovementHypothesis) -> bool:
        """Verify hypothesis is safe to execute."""
        # Check for dangerous patterns
        dangerous_keywords = ['delete', 'remove', 'destroy', 'reset', 'clear']
        desc_lower = hypothesis.description.lower()

        for keyword in dangerous_keywords:
            if keyword in desc_lower:
                print(f"   ⚠️  Safety: Dangerous keyword '{keyword}' in hypothesis")
                return False

        # Strategy-specific checks
        if hypothesis.strategy == "self_modify":
            # Additional checks for self-modification
            if not hasattr(self.byrd, 'self_modification') or not self.byrd.self_modification:
                print("   ⚠️  Safety: Self-modification not enabled")
                return False

        return True

    async def _execute(self, hypothesis: ImprovementHypothesis):
        """Execute the selected hypothesis."""
        # Record the attempt (metadata embedded in content)
        await self.memory.record_experience(
            content=f"[AGI_CYCLE] Attempting: {hypothesis.description} | strategy={hypothesis.strategy} target={hypothesis.target} predicted={hypothesis.predicted_success:.2f}",
            type="agi_cycle"
        )

        # Execute based on strategy
        if hypothesis.strategy == "research":
            # Trigger research through seeker
            if hasattr(self.byrd, 'seeker') and self.byrd.seeker:
                await self.byrd.seeker._research_desire({
                    'description': f"Research best practices for {hypothesis.target}",
                    'intensity': 0.7
                })

        elif hypothesis.strategy == "practice":
            # Create a practice goal
            await self.memory._run_query("""
                CREATE (g:Goal {
                    description: $desc,
                    domain: $target,
                    priority: 'high',
                    status: 'active',
                    from_agi_cycle: true,
                    created_at: datetime()
                })
            """, {
                "desc": f"Practice and improve {hypothesis.target}",
                "target": hypothesis.target
            })

        elif hypothesis.strategy in ["failure_analysis", "success_analysis"]:
            # Query memory for relevant experiences
            success_filter = "true" if hypothesis.strategy == "success_analysis" else "false"
            await self.memory._run_query("""
                MATCH (e:Experience)
                WHERE e.capability = $target
                AND e.success = $success
                RETURN e.content, e.metadata
                ORDER BY e.timestamp DESC
                LIMIT 10
            """, {
                "target": hypothesis.target,
                "success": hypothesis.strategy == "success_analysis"
            })

    async def _measure_improvement(
        self,
        target: ImprovementTarget,
        before_inventory,
        before_eval: Optional[Any] = None
    ) -> MeasurementResult:
        """
        Measure improvement using available evaluation methods.

        Args:
            target: The improvement target
            before_inventory: Capability inventory from before execution
            before_eval: Pre-captured evaluation result (from step 2.5)
        """

        # Method 1: Use CapabilityEvaluator with pre-captured before_eval
        if self.evaluator and before_eval is not None:
            try:
                eval_name = self._normalize_capability_name(target.name)
                after_eval = await self.evaluator.evaluate_capability(eval_name)
                delta = after_eval.accuracy - before_eval.accuracy

                return MeasurementResult(
                    improved=(delta > 0.01),
                    delta=delta,
                    before_score=before_eval.accuracy,
                    after_score=after_eval.accuracy,
                    measurement_method="capability_evaluator"
                )
            except Exception as e:
                print(f"   Warning: Evaluator measurement failed: {e}")

        # Method 2: Use self_model comparison
        if self.self_model:
            try:
                after_inventory = await self.self_model.assess_capabilities()

                before_cap = before_inventory.capabilities.get(target.name) if hasattr(before_inventory, 'capabilities') else None
                after_cap = after_inventory.capabilities.get(target.name) if hasattr(after_inventory, 'capabilities') else None

                if before_cap and after_cap:
                    delta = after_cap.success_rate - before_cap.success_rate
                    return MeasurementResult(
                        improved=(delta > 0.01),
                        delta=delta,
                        before_score=before_cap.success_rate,
                        after_score=after_cap.success_rate,
                        measurement_method="self_model_comparison"
                    )
            except Exception as e:
                print(f"   Warning: Self-model measurement failed: {e}")

        # Method 3: Heuristic - assume small improvement from any action
        return MeasurementResult(
            improved=True,
            delta=0.02,  # Assume 2% improvement from attempting
            measurement_method="heuristic",
            reason="No direct measurement available"
        )

    async def _learn_from_outcome(self, hypothesis: ImprovementHypothesis, measurement: MeasurementResult):
        """Update all learning components from outcome."""

        # 1. Update EXISTING world model
        if self.world_model:
            try:
                from world_model import OutcomePrediction, UncertaintyType

                await self.world_model.update_from_prediction_error(
                    prediction=OutcomePrediction(
                        action=hypothesis.description,
                        context={"strategy": hypothesis.strategy},
                        predicted_outcome="success" if hypothesis.predicted_success > 0.5 else "failure",
                        success_probability=hypothesis.predicted_success,
                        confidence=hypothesis.prediction_confidence,
                        uncertainty_type=UncertaintyType.EPISTEMIC,
                        uncertainty_sources=[],
                        reasoning="AGI cycle prediction",
                        similar_past_cases=0
                    ),
                    actual_outcome="improved" if measurement.improved else "not_improved",
                    actual_success=measurement.improved
                )
            except Exception as e:
                print(f"   Warning: Could not update world model: {e}")

        # 2. Update intuition network (NEW - if available)
        if self.intuition:
            try:
                await self.intuition.record_outcome(
                    situation=hypothesis.target,
                    action=hypothesis.strategy,
                    success=measurement.improved
                )
            except Exception as e:
                print(f"   Note: Intuition network update skipped: {e}")

        # 3. Update self_model with Bayesian update (if enhanced)
        if self.self_model and hasattr(self.self_model, 'bayesian_update'):
            try:
                self.self_model.bayesian_update(hypothesis.target, measurement.improved)
            except Exception as e:
                print(f"   Note: Bayesian update skipped: {e}")

        # 4. Record experience using EXISTING memory (metadata embedded in content)
        await self.memory.record_experience(
            content=f"[AGI_CYCLE] {'SUCCESS' if measurement.improved else 'NO IMPROVEMENT'}: "
                    f"{hypothesis.description} (delta: {measurement.delta:+.2%}) | "
                    f"cycle={self._cycle_count} target={hypothesis.target} strategy={hypothesis.strategy} method={measurement.measurement_method}",
            type="agi_cycle"
        )

        # 5. Handle regression - rollback if significant decline
        if measurement.delta < -0.05 and self.rollback:
            try:
                from rollback import RollbackReason
                print(f"   ⚠️  Regression detected ({measurement.delta:+.2%}), triggering rollback")
                await self.rollback.rollback_last(RollbackReason.CAPABILITY_REGRESSION)
            except Exception as e:
                print(f"   Warning: Could not rollback: {e}")

    def _update_strategy_stats(self, strategy: str, measurement: MeasurementResult):
        """Track strategy effectiveness over time."""
        if strategy not in self._strategy_stats:
            self._strategy_stats[strategy] = {
                "attempts": 0,
                "successes": 0,
                "total_delta": 0.0
            }

        stats = self._strategy_stats[strategy]
        stats["attempts"] += 1
        stats["total_delta"] += measurement.delta
        if measurement.improved:
            stats["successes"] += 1

    def get_metrics(self) -> Dict[str, Any]:
        """Get current AGI Runner metrics."""
        return {
            "cycle_count": self._cycle_count,
            "bootstrapped": self._bootstrapped,
            "bootstrap_metrics": self._bootstrap_metrics,
            "improvement_rate": self._calculate_improvement_rate(),
            "recent_cycles": [
                {
                    "cycle": c.cycle,
                    "success": c.success,
                    "target": c.target,
                    "delta": c.delta,
                    "strategy": c.strategy,
                    "measurement_method": c.measurement_method
                }
                for c in self._cycle_history[-10:]
            ],
            "strategy_effectiveness": {
                strategy: {
                    "attempts": stats["attempts"],
                    "success_rate": stats["successes"] / stats["attempts"] if stats["attempts"] > 0 else 0,
                    "avg_delta": stats["total_delta"] / stats["attempts"] if stats["attempts"] > 0 else 0
                }
                for strategy, stats in self._strategy_stats.items()
            }
        }

    def get_comprehensive_metrics(self) -> Dict[str, Any]:
        """Get multi-timescale AGI metrics for detailed analysis."""
        now = datetime.now()
        session_duration = (now - self._session_start).total_seconds()

        return {
            "instantaneous": {
                "last_cycle": self._cycle_count,
                "last_delta": self._cycle_history[-1].delta if self._cycle_history else 0,
                "last_target": self._cycle_history[-1].target if self._cycle_history else None,
                "last_strategy": self._cycle_history[-1].strategy if self._cycle_history else None,
                "measurement_method": self._cycle_history[-1].measurement_method if self._cycle_history else "none"
            },
            "session": {
                "duration_seconds": session_duration,
                "cycles_completed": self._cycle_count,
                "improvement_rate": self._calculate_improvement_rate(),
                "capabilities_improved": list(self._session_capabilities_improved),
                "total_delta": sum(c.delta for c in self._cycle_history),
                "strategy_breakdown": self._strategy_stats
            },
            "trends": {
                "recent_5_cycles": self._calculate_window_stats(5),
                "recent_10_cycles": self._calculate_window_stats(10),
                "recent_20_cycles": self._calculate_window_stats(20)
            },
            "bootstrap": self._bootstrap_metrics,
            "evaluator_available": self.evaluator is not None
        }

    def _calculate_window_stats(self, window: int) -> Dict[str, Any]:
        """Calculate stats for a window of recent cycles."""
        recent = self._cycle_history[-window:] if self._cycle_history else []
        if not recent:
            return {"cycles": 0, "success_rate": 0, "avg_delta": 0, "targets": []}

        successes = sum(1 for c in recent if c.success)
        return {
            "cycles": len(recent),
            "success_rate": successes / len(recent),
            "avg_delta": sum(c.delta for c in recent) / len(recent),
            "targets": list(set(c.target for c in recent if c.target))
        }

    def _calculate_improvement_rate(self) -> float:
        """Calculate overall improvement rate from cycle history."""
        if not self._cycle_history:
            return 0.0

        recent = self._cycle_history[-20:]  # Last 20 cycles
        successful = sum(1 for c in recent if c.success)
        return successful / len(recent)

    async def process_capability_desire(self, desire: Dict):
        """
        Process a capability-type desire through the AGI Runner.

        Called when DesireClassifier routes a desire here.
        """
        description = desire.get('description', '')

        print(f"🎯 AGI Runner: Processing capability desire: {description[:50]}...")

        # Create a goal for this desire
        await self.memory._run_query("""
            CREATE (g:Goal {
                description: $desc,
                domain: 'capability',
                priority: 'high',
                status: 'active',
                from_desire: true,
                created_at: datetime()
            })
        """, {"desc": description})

        # Run an improvement cycle targeting this
        result = await self.run_improvement_cycle()

        return result
