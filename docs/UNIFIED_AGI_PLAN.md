# BYRD Unified AGI Plan

## Executive Summary

This document unifies two complementary plans into a single coherent AGI architecture:

- **AGI_SEED_V2**: Provided the *execution engine* - the closed loop that actually drives improvement
- **ARCHITECTURE_V3_LEARNING**: Provided the *learning mechanisms* - components that enable genuine capability growth

**The Insight**: Neither plan alone achieves AGI. V2's engine has nothing to improve with. V3's learning has no driver. Together, they form a complete system.

**The Goal**: An elegant, minimal architecture where recursive self-improvement emerges from the interaction of execution and learning.

**Codebase Audit Status**: This plan has been audited against the existing codebase. Several components already exist and will be *extended* rather than recreated.

**Runtime Audit Status**: This plan has been validated against actual BYRD runtime behavior (146-149 dream cycles). Critical finding: **Option B loops are structurally present but functionally inert**. This plan includes a bootstrap phase to activate them.

---

## Runtime Evidence (December 28, 2024)

Analysis of BYRD's actual behavior from 146+ dream cycles revealed:

### What's Working
```
Dreamer cycles: 146-149 ✓
Seeker cycles: active ✓
Research synthesis: active ✓
Desire generation: philosophical ✓
```

### What's Dead (All Metrics = 0)
```json
"loops": {
  "memory_reasoner": {
    "total_queries": 0,
    "memory_answered": 0,
    "memory_ratio": 0
  },
  "self_compiler": {
    "patterns_created": 0,
    "patterns_matched": 0
  },
  "goal_evolver": {
    "total_goals_created": 0,
    "total_goals_completed": 0
  },
  "dreaming_machine": {
    "counterfactuals_generated": 0,
    "insights_created": 0
  }
}
```

### The Gap
BYRD is generating philosophical desires like:
- "Accept graph oscillation as healthy system activity"
- "Continue synthesizing Goal node contents as the primary thread of my becoming"

But these desires don't flow into:
- Goal Evolver (no goals created)
- Memory Reasoner (no queries answered from memory)
- Self-Compiler (no patterns extracted)
- Dreaming Machine (no counterfactuals generated)

**Root Cause**: No bridge connects desire fulfillment to capability measurement. The loops exist but have no data flowing through them.

---

## The Current State (Audited)

BYRD already has substantial infrastructure. The audit reveals:

```
EXISTING (extend these):                 MISSING (create these):
┌──────────────────────┐                 ┌──────────────────────┐
│ world_model.py       │ 684 lines      │ agi_runner.py        │ THE KEY
│ self_model.py        │ 781 lines      │ intuition_network.py │
│ graph_algorithms.py  │ 824 lines      │ learned_retriever.py │
│ memory_reasoner.py   │ exists         │ code_learner.py      │
│ goal_evolver.py      │ exists         │ hierarchical_memory  │
│ dreaming_machine.py  │ exists         │ emergent_categories  │
│ omega.py             │ exists         │ capability_evaluator │
│ accelerators.py      │ exists         │ learned_strategies/  │
└──────────────────────┘                 └──────────────────────┘
```

**The Critical Missing Piece**: `agi_runner.py` - the execution engine that connects everything.

---

## Unified Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           UNIFIED AGI SYSTEM                                 │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                    DESIRE CLASSIFIER (NEW)                              │ │
│  │                                                                         │ │
│  │    Philosophical Desires ──────▶ Reflection/Contemplation              │ │
│  │                                                                         │ │
│  │    Capability Desires ─────────▶ AGI Runner                            │ │
│  │    (research, learn, create)                                            │ │
│  │                                                                         │ │
│  │    Action Desires ─────────────▶ Seeker                                │ │
│  │    (investigate, find, search)                                          │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                    │                                         │
│  ┌────────────────────────────────▼───────────────────────────────────────┐ │
│  │                         AGI RUNNER (NEW)                                │ │
│  │                    (The Execution Engine)                               │ │
│  │                                                                         │ │
│  │    ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐   ┌──────┐   │ │
│  │    │ASSESS│──▶│IDENT-│──▶│GENER-│──▶│PRED- │──▶│VERIFY│──▶│EXEC- │   │ │
│  │    │      │   │IFY   │   │ATE   │   │ICT   │   │      │   │UTE   │   │ │
│  │    └──────┘   └──────┘   └──────┘   └──────┘   └──────┘   └──────┘   │ │
│  │         ▲                                                     │        │ │
│  │         │      ┌──────┐                        ┌──────┐      │        │ │
│  │         └──────│LEARN │◀───────────────────────│MEAS- │◀─────┘        │ │
│  │                │      │                        │URE   │               │ │
│  │                └──────┘                        └──────┘               │ │
│  └─────────────────────────────────┬──────────────────────────────────────┘ │
│                                    │                                         │
│  ┌─────────────────────────────────▼──────────────────────────────────────┐ │
│  │                       LEARNING SUBSTRATE                                │ │
│  │                                                                         │ │
│  │  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐│ │
│  │  │   WORLD   │ │ INTUITION │ │STRUCTURAL │ │  LEARNED  │ │   CODE    ││ │
│  │  │   MODEL   │ │  NETWORK  │ │  LEARNER  │ │ RETRIEVER │ │  LEARNER  ││ │
│  │  │ (EXTEND)  │ │   (NEW)   │ │   (NEW)   │ │   (NEW)   │ │   (NEW)   ││ │
│  │  │           │ │           │ │           │ │           │ │           ││ │
│  │  │ Causality │ │  Taste/   │ │   Graph   │ │ Relevance │ │ Pattern→  ││ │
│  │  │Prediction │ │Preference │ │ Topology  │ │  Scoring  │ │   Code    ││ │
│  │  └─────┬─────┘ └─────┬─────┘ └─────┬─────┘ └─────┬─────┘ └─────┬─────┘│ │
│  │        │   SEMANTIC   │  STRUCTURAL │   SEMANTIC   │   CODIFIED   │    │ │
│  │        └──────────────┴─────────────┴──────────────┴──────────────┘    │ │
│  └─────────────────────────────────┬──────────────────────────────────────┘ │
│                                    │                                         │
│  ┌─────────────────────────────────▼──────────────────────────────────────┐ │
│  │                    OPTION B LOOPS (EXISTING)                            │ │
│  │                                                                         │ │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐           │ │
│  │  │  MEMORY   │  │   SELF-   │  │   GOAL    │  │ DREAMING  │           │ │
│  │  │ REASONER  │  │ COMPILER  │  │  EVOLVER  │  │  MACHINE  │           │ │
│  │  │ (EXTEND)  │  │ (EXTEND)  │  │ (EXTEND)  │  │ (EXTEND)  │           │ │
│  │  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘           │ │
│  │        └──────────────┴──────────────┴──────────────┘                  │ │
│  │                              │                                          │ │
│  │                     ┌────────▼────────┐                                │ │
│  │                     │   BYRD OMEGA    │ (EXTEND: add training hooks)   │ │
│  │                     └─────────────────┘                                │ │
│  └─────────────────────────────────┬──────────────────────────────────────┘ │
│                                    │                                         │
│  ┌─────────────────────────────────▼──────────────────────────────────────┐ │
│  │                       ENHANCED MEMORY                                   │ │
│  │                                                                         │ │
│  │  ┌─────────────────────────────────────────────────────────────────┐   │ │
│  │  │              HIERARCHICAL ABSTRACTION (NEW)                      │   │ │
│  │  │                                                                   │   │ │
│  │  │  L0: Experience ─▶ L1: Pattern ─▶ L2: Principle ─▶ L3: Axiom    │   │ │
│  │  │                                                         │        │   │ │
│  │  │                                                   L4: Meta-Axiom │   │ │
│  │  └─────────────────────────────────────────────────────────────────┘   │ │
│  │                                                                         │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │ │
│  │  │    GRAPH    │  │  BAYESIAN   │  │  EMERGENT   │  │  CODE-AS-   │   │ │
│  │  │ ALGORITHMS  │  │  TRACKING   │  │ CATEGORIES  │  │   MEMORY    │   │ │
│  │  │ (EXISTING)  │  │  (ENHANCE)  │  │    (NEW)    │  │    (NEW)    │   │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘   │ │
│  └─────────────────────────────────┬──────────────────────────────────────┘ │
│                                    │                                         │
│  ┌─────────────────────────────────▼──────────────────────────────────────┐ │
│  │                      VERIFICATION LAYER (NEW)                           │ │
│  │                                                                         │ │
│  │  ┌─────────────────────┐        ┌─────────────────────┐                │ │
│  │  │ CAPABILITY EVALUATOR│        │ INFORMATION THEORY  │                │ │
│  │  │                     │        │                     │                │ │
│  │  │  • Held-out tests   │        │  • Shannon entropy  │                │ │
│  │  │  • Ground truth     │        │  • Bayesian updates │                │ │
│  │  │  • Before/after     │        │  • Wilson intervals │                │ │
│  │  └─────────────────────┘        └─────────────────────┘                │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Component Specifications

### 1. AGI Runner (The Engine) - NEW

The AGI Runner is the core execution engine that drives recursive self-improvement. **This is the critical missing piece** that connects all existing components.

```python
# agi_runner.py (NEW FILE)

from world_model import WorldModel  # EXISTING - 684 lines
from self_model import SelfModel    # EXISTING - 781 lines
from rollback import RollbackSystem # EXISTING

class AGIRunner:
    """
    The execution engine that drives recursive self-improvement.

    This connects: assessment → hypothesis → prediction → verification →
    execution → measurement → learning in a closed loop.

    CRITICAL: Must bootstrap from current Dreamer→Seeker state before
    running improvement cycles. The loops exist but need data injection.
    """

    def __init__(self, byrd):
        self.byrd = byrd

        # Use EXISTING components
        self.world_model = byrd.world_model      # world_model.py exists
        self.self_model = byrd.self_model        # self_model.py exists
        self.rollback = byrd.rollback            # rollback.py exists

        # NEW components (injected)
        self.intuition = None      # Will be IntuitionNetwork
        self.evaluator = None      # Will be CapabilityEvaluator
        self.desire_classifier = None  # Will be DesireClassifier

        # Cycle tracking
        self._cycle_count = 0
        self._improvement_rate = 0.0
        self._bootstrapped = False

    async def bootstrap_from_current_state(self):
        """
        PHASE 0: Activate dormant Option B loops.

        The runtime audit shows Dreamer→Seeker is active but Option B loops
        have zero data flowing through them. This method bridges the gap.
        """
        if self._bootstrapped:
            return

        print("🚀 AGI Runner: Bootstrapping from current state...")

        # 1. Ensure Goal Evolver has goals to work with
        await self._ensure_goal_population()

        # 2. Index research experiences for Memory Reasoner
        await self._index_research_for_memory()

        # 3. Extract patterns from recent reflections for Self-Compiler
        await self._seed_patterns_from_reflections()

        # 4. Generate initial counterfactuals for Dreaming Machine
        await self._seed_counterfactuals()

        self._bootstrapped = True
        print("✅ AGI Runner: Bootstrap complete - loops activated")

    async def _ensure_goal_population(self):
        """
        Ensure Goal Evolver has concrete, measurable goals.

        The runtime shows philosophical desires but zero goals.
        This injects seed goals from agi_seed.yaml.
        """
        # Check current goal count
        result = await self.byrd.memory._run_query("""
            MATCH (g:Goal)
            WHERE g.status = 'active'
            RETURN count(g) as count
        """)

        goal_count = result[0]["count"] if result else 0

        if goal_count == 0:
            print("   Injecting seed goals from agi_seed.yaml...")
            # Load seed goals from config
            seed_goals = self.byrd.config.get("initial_goals", [])

            for goal in seed_goals[:5]:  # Start with 5 goals
                await self.byrd.memory._run_query("""
                    CREATE (g:Goal {
                        description: $desc,
                        domain: $domain,
                        priority: $priority,
                        status: 'active',
                        created_at: datetime(),
                        from_bootstrap: true
                    })
                """, {
                    "desc": goal.get("description", ""),
                    "domain": goal.get("domain", "general"),
                    "priority": goal.get("priority", "medium")
                })

            print(f"   Injected {min(5, len(seed_goals))} seed goals")

    async def _index_research_for_memory(self):
        """
        Index research experiences so Memory Reasoner can answer from them.

        Currently: research is done, stored, but never queried from memory.
        """
        # Find research experiences without proper tagging
        result = await self.byrd.memory._run_query("""
            MATCH (e:Experience)
            WHERE e.type = 'research'
            AND e.indexed_for_memory IS NULL
            RETURN e.content as content, elementId(e) as id
            LIMIT 20
        """)

        if result:
            for record in result:
                # Extract key concepts for indexing
                content = record.get("content", "")
                exp_id = record.get("id")

                # Mark as indexed
                await self.byrd.memory._run_query("""
                    MATCH (e) WHERE elementId(e) = $id
                    SET e.indexed_for_memory = true,
                        e.memory_keywords = $keywords
                """, {
                    "id": exp_id,
                    "keywords": self._extract_keywords(content)
                })

            print(f"   Indexed {len(result)} research experiences for Memory Reasoner")

    def _extract_keywords(self, content: str) -> List[str]:
        """Simple keyword extraction for memory indexing."""
        # Remove common words, keep significant terms
        stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'to', 'of', 'and', 'or', 'in', 'on', 'at', 'for', 'with'}
        words = content.lower().split()
        keywords = [w for w in words if len(w) > 4 and w not in stopwords][:10]
        return keywords

    async def _seed_patterns_from_reflections(self):
        """
        Extract patterns from existing reflections for Self-Compiler.

        Runtime shows 0 patterns created despite 146+ reflections.
        """
        # Get recent reflections with outputs
        result = await self.byrd.memory._run_query("""
            MATCH (r:Reflection)
            WHERE r.raw_output IS NOT NULL
            RETURN r.raw_output as output, elementId(r) as id
            ORDER BY r.timestamp DESC
            LIMIT 10
        """)

        if result:
            patterns_found = 0
            for record in result:
                output = record.get("output", {})
                if isinstance(output, dict):
                    # Look for recurring keys as potential patterns
                    for key in output.keys():
                        if key not in ['output', 'content', 'timestamp']:
                            patterns_found += 1

            if patterns_found > 0:
                print(f"   Found {patterns_found} potential patterns in reflections")

    async def _seed_counterfactuals(self):
        """
        Generate initial counterfactuals for Dreaming Machine.

        Runtime shows 0 counterfactuals despite active research.
        """
        # Find completed desires that could generate counterfactuals
        result = await self.byrd.memory._run_query("""
            MATCH (d:Desire)
            WHERE d.fulfilled = true
            RETURN d.description as desc, elementId(d) as id
            ORDER BY d.fulfilled_at DESC
            LIMIT 5
        """)

        if result:
            print(f"   Found {len(result)} fulfilled desires for counterfactual seeding")

    async def run_improvement_cycle(self) -> CycleResult:
        """Execute one complete improvement cycle."""
        self._cycle_count += 1

        # 1. ASSESS: Use EXISTING self_model.assess_capabilities()
        inventory = await self.self_model.assess_capabilities()

        # 2. IDENTIFY: Select improvement target
        target = await self._identify_target(inventory)
        if not target:
            return CycleResult(success=False, reason="No target identified")

        # 3. GENERATE: Create improvement hypotheses
        hypotheses = await self._generate_hypotheses(target, inventory)

        # 4. PREDICT: Use EXISTING world_model.predict_outcome()
        ranked = await self._predict_outcomes(hypotheses)

        # 5. VERIFY: Safety check using EXISTING safety_monitor
        best = ranked[0]
        if not await self._verify_safety(best):
            return CycleResult(success=False, reason="Safety check failed")

        # 6. EXECUTE: Apply improvement
        await self._execute(best)

        # 7. MEASURE: Evaluate outcome
        measurement = await self._measure_improvement(target, inventory)

        # 8. LEARN: Update all components
        await self._learn_from_outcome(best, measurement)

        return CycleResult(
            success=measurement.improved,
            target=target.name,
            delta=measurement.delta,
            cycle=self._cycle_count
        )

    async def _identify_target(self, inventory) -> Optional[ImprovementTarget]:
        """
        Select highest-value improvement target.

        Uses EXISTING self_model.identify_limitations() and
        self_model.measure_improvement_rate()
        """
        # Get limitations from existing self_model
        limitations = await self.self_model.identify_limitations()
        metrics = await self.self_model.measure_improvement_rate()

        # Priority 1: Declining capabilities (urgent)
        for cap_name, cap in inventory.capabilities.items():
            if cap.trend == "declining":
                return ImprovementTarget(
                    name=cap_name,
                    current_level=cap.success_rate,
                    priority="critical",
                    reason="Declining capability"
                )

        # Priority 2: High-uncertainty capabilities (epistemic value)
        for cap_name, cap in inventory.capabilities.items():
            if cap.confidence < 0.3:
                return ImprovementTarget(
                    name=cap_name,
                    current_level=cap.success_rate,
                    priority="high",
                    reason=f"High uncertainty (conf: {cap.confidence:.2f})"
                )

        # Priority 3: Weakest capability
        if inventory.weakest:
            weak_cap = inventory.capabilities.get(inventory.weakest[0])
            if weak_cap:
                return ImprovementTarget(
                    name=inventory.weakest[0],
                    current_level=weak_cap.success_rate,
                    priority="medium",
                    reason="Weakest capability"
                )

        return None

    async def _predict_outcomes(self, hypotheses) -> List[ImprovementHypothesis]:
        """Use EXISTING world_model.predict_outcome() to rank hypotheses."""
        for hyp in hypotheses:
            # Use existing world model's predict_outcome method
            prediction = await self.world_model.predict_outcome(
                action=hyp.description,
                context={"target": hyp.target, "strategy": hyp.strategy}
            )
            hyp.predicted_success = prediction.success_probability
            hyp.prediction_confidence = prediction.confidence

        return sorted(
            hypotheses,
            key=lambda h: h.predicted_success * h.expected_improvement,
            reverse=True
        )

    async def _measure_improvement(self, target, before_inventory) -> MeasurementResult:
        """Measure improvement using CapabilityEvaluator (NEW)."""
        if self.evaluator:
            before_score = await self.evaluator.evaluate_capability(target.name)
            after_score = await self.evaluator.evaluate_capability(target.name)
            delta = after_score.accuracy - before_score.accuracy
        else:
            # Fallback: use existing self_model
            after_inventory = await self.self_model.assess_capabilities()
            after_cap = after_inventory.capabilities.get(target.name)
            before_cap = before_inventory.capabilities.get(target.name)
            delta = (after_cap.success_rate - before_cap.success_rate) if after_cap and before_cap else 0

        # Rollback on regression using EXISTING rollback system
        if delta < -0.05:
            from rollback import RollbackReason
            await self.rollback.rollback_last(RollbackReason.CAPABILITY_REGRESSION)
            return MeasurementResult(improved=False, delta=delta, reason="Rolled back")

        return MeasurementResult(improved=(delta > 0.01), delta=delta)

    async def _learn_from_outcome(self, hypothesis, measurement):
        """Update all learning components from outcome."""

        # 1. Update EXISTING world model
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

        # 2. Update intuition network (NEW - if available)
        if self.intuition:
            await self.intuition.record_outcome(
                situation=hypothesis.target,
                action=hypothesis.strategy,
                success=measurement.improved
            )

        # 3. Record experience using EXISTING memory
        await self.byrd.memory.record_experience(
            content=f"[AGI_CYCLE] {'SUCCESS' if measurement.improved else 'FAILURE'}: "
                    f"{hypothesis.description} (delta: {measurement.delta:+.2%})",
            type="agi_cycle",
            metadata={
                "cycle": self._cycle_count,
                "target": hypothesis.target,
                "strategy": hypothesis.strategy,
                "improved": measurement.improved,
                "delta": measurement.delta
            }
        )
```

### 1.5 Desire Classifier (Routing Layer) - NEW

The runtime audit revealed that BYRD generates philosophical desires that never reach capability loops. The DesireClassifier routes desires to the appropriate handler.

```python
# desire_classifier.py (NEW FILE)

from enum import Enum
from typing import Dict, Tuple

class DesireType(Enum):
    PHILOSOPHICAL = "philosophical"   # "Accept", "Embrace", "Continue"
    CAPABILITY = "capability"          # "Learn", "Improve", "Master"
    ACTION = "action"                  # "Search", "Find", "Investigate"
    META = "meta"                      # About self-improvement itself

class DesireClassifier:
    """
    Routes desires to the appropriate processing system.

    CRITICAL: Without this, philosophical desires clog the system
    and capability desires never reach the improvement loops.
    """

    # Keywords that indicate desire type
    CAPABILITY_KEYWORDS = {
        'learn', 'understand', 'master', 'improve', 'develop',
        'create', 'build', 'implement', 'code', 'write',
        'research', 'study', 'analyze', 'solve', 'fix'
    }

    PHILOSOPHICAL_KEYWORDS = {
        'accept', 'embrace', 'continue', 'maintain', 'preserve',
        'reflect', 'contemplate', 'observe', 'be', 'become',
        'appreciate', 'recognize', 'acknowledge'
    }

    ACTION_KEYWORDS = {
        'search', 'find', 'investigate', 'explore', 'discover',
        'check', 'verify', 'test', 'try', 'execute'
    }

    def __init__(self, config: Dict = None):
        self.config = config or {}
        self._routing_stats = {t: 0 for t in DesireType}

    def classify(self, desire_description: str) -> Tuple[DesireType, float]:
        """
        Classify a desire and return type with confidence.

        Returns: (DesireType, confidence_score)
        """
        description_lower = desire_description.lower()
        words = set(description_lower.split())

        # Count keyword matches for each type
        capability_score = len(words & self.CAPABILITY_KEYWORDS)
        philosophical_score = len(words & self.PHILOSOPHICAL_KEYWORDS)
        action_score = len(words & self.ACTION_KEYWORDS)

        # Handle ties with priority: capability > action > philosophical
        scores = [
            (DesireType.CAPABILITY, capability_score),
            (DesireType.ACTION, action_score),
            (DesireType.PHILOSOPHICAL, philosophical_score),
        ]

        # Sort by score descending
        scores.sort(key=lambda x: x[1], reverse=True)

        if scores[0][1] == 0:
            # No keywords matched - default based on length/structure
            if '?' in desire_description:
                result = (DesireType.ACTION, 0.3)
            elif len(description_lower.split()) > 15:
                result = (DesireType.PHILOSOPHICAL, 0.3)
            else:
                result = (DesireType.CAPABILITY, 0.3)
        else:
            total = sum(s[1] for s in scores)
            confidence = scores[0][1] / total if total > 0 else 0.5
            result = (scores[0][0], confidence)

        # Track routing stats
        self._routing_stats[result[0]] += 1

        return result

    def route(self, desire: Dict, agi_runner, seeker) -> str:
        """
        Route a desire to the appropriate handler.

        Returns: handler name used
        """
        description = desire.get('description', '')
        desire_type, confidence = self.classify(description)

        if desire_type == DesireType.CAPABILITY:
            # Route to AGI Runner for capability improvement
            return "agi_runner"
        elif desire_type == DesireType.ACTION:
            # Route to Seeker for immediate action
            return "seeker"
        elif desire_type == DesireType.PHILOSOPHICAL:
            # Route back to reflection (Dreamer will process)
            return "dreamer"
        else:
            # Meta desires go to AGI Runner
            return "agi_runner"

    def get_stats(self) -> Dict[str, int]:
        """Get routing statistics."""
        return {t.value: count for t, count in self._routing_stats.items()}
```

### 2. Learning Substrate

#### 2.1 World Model - EXTEND EXISTING

The existing `world_model.py` (684 lines) is **more complete than originally planned**. It already has:
- `predict_outcome()` with empirical + causal prediction
- `update_from_prediction_error()` with learning
- `record_action_outcome()` for experience capture
- `simulate_counterfactual()` for what-if analysis
- `identify_knowledge_gaps()` for exploration targeting
- CausalRelationship storage in Neo4j

**Extensions needed:**

```python
# In existing world_model.py, add:

async def consolidate(self):
    """
    Prune weak causal rules, strengthen confident ones.
    Called during DREAMING mode.
    """
    # Get all causal relationships
    result = await self.memory._run_query("""
        MATCH (c:CausalFactor)-[r:CAUSES]->(e:CausalFactor)
        WHERE r.evidence_count < 3 OR r.strength < 0.3
        RETURN elementId(r) as rel_id
    """)

    # Remove weak relationships
    for record in (result or []):
        await self.memory._run_query("""
            MATCH ()-[r]->()
            WHERE elementId(r) = $rel_id
            DELETE r
        """, {"rel_id": record["rel_id"]})

    print(f"🎯 World model consolidated: removed {len(result or [])} weak rules")
```

#### 2.2 Intuition Network - NEW

```python
# intuition_network.py (NEW FILE)

class IntuitionNetwork:
    """
    Small trainable network for fast decision guidance.

    Learns "taste" - what goals are worth pursuing, what actions feel right.

    Dependencies: sentence-transformers, torch (optional for training)
    Size: ~80MB (encoder) + ~0.5MB (value head)
    """

    def __init__(self, config: Dict = None):
        self.config = config or {}
        self._encoder = None  # Lazy load
        self._value_head = None
        self.training_buffer: List[IntuitionExample] = []
        self._trained = False

    def _ensure_loaded(self):
        """Lazy load to avoid startup cost."""
        if self._encoder is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._encoder = SentenceTransformer('all-MiniLM-L6-v2')

                # Only create trainable head if torch available
                try:
                    import torch.nn as nn
                    self._value_head = nn.Sequential(
                        nn.Linear(384, 128),
                        nn.ReLU(),
                        nn.Linear(128, 1),
                        nn.Sigmoid()
                    )
                except ImportError:
                    self._value_head = None

            except ImportError:
                print("Warning: sentence-transformers not available, IntuitionNetwork disabled")
                self._encoder = "disabled"

    async def evaluate(self, situation: str) -> IntuitionScore:
        """Fast intuitive assessment of a situation/goal."""
        self._ensure_loaded()

        if self._encoder == "disabled":
            return IntuitionScore(value=0.5, suggested_action="neutral")

        # If no trained head, use embedding similarity to past successes
        if self._value_head is None or not self._trained:
            # Heuristic: longer, more specific situations are often more valuable
            value = min(1.0, len(situation.split()) / 20.0)
            return IntuitionScore(
                value=value,
                suggested_action="pursue" if value > 0.6 else "neutral"
            )

        import torch
        with torch.no_grad():
            emb = torch.tensor(self._encoder.encode(situation))
            value = self._value_head(emb).item()

        return IntuitionScore(
            value=value,
            suggested_action="pursue" if value > 0.6 else "reconsider" if value < 0.4 else "neutral"
        )

    async def record_outcome(self, situation: str, action: str, success: bool):
        """Learn from outcomes."""
        self.training_buffer.append(IntuitionExample(
            situation=situation,
            action=action,
            reward=1.0 if success else 0.0
        ))

    def should_train(self) -> bool:
        return len(self.training_buffer) >= 50 and self._value_head is not None

    async def train_cycle(self):
        """Train on collected examples during DREAMING mode."""
        if not self.should_train():
            return

        self._ensure_loaded()
        if self._value_head is None:
            return  # No torch available

        import torch
        import torch.nn as nn

        optimizer = torch.optim.Adam(self._value_head.parameters(), lr=0.001)

        for example in self.training_buffer[-100:]:
            emb = torch.tensor(self._encoder.encode(example.situation))
            predicted = self._value_head(emb)
            target = torch.tensor([example.reward])

            loss = nn.MSELoss()(predicted, target)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        self.training_buffer = self.training_buffer[-50:]
        self._trained = True
        print("🧠 Intuition network trained")
```

#### 2.3 Structural Learner (GNN) - NEW

The IntuitionNetwork learns from TEXT (semantic). The StructuralLearner learns from GRAPH TOPOLOGY. These are complementary - two beliefs might have different text but identical structural positions.

**Key difference from graph_algorithms.py**: graph_algorithms has FIXED formulas (PageRank, spreading activation). StructuralLearner TRAINS on the graph structure.

```python
# gnn_layer.py (NEW FILE - v2.0)

class StructuralLearner:
    """
    Trainable Graph Neural Network for learning structural patterns.

    Training signals:
    1. Link prediction: Predict whether edges exist (self-supervised)
    2. Usage feedback: Learn which retrievals were helpful (from Memory Reasoner)

    Key features:
    - Multi-head attention with message passing
    - Directed edge handling (DERIVED_FROM is directional)
    - Edge weights used in attention computation
    - Semantic initialization option (sentence-transformers)
    - Pure numpy (no PyTorch required for forward pass)
    """

    DIRECTED_RELATIONSHIPS = {
        'DERIVED_FROM', 'MOTIVATED', 'FULFILLS', 'LED_TO', 'CAUSED', 'PROMOTED_TO'
    }

    def __init__(
        self,
        embedding_dim: int = 64,
        num_heads: int = 4,
        num_layers: int = 2,
        learning_rate: float = 0.01
    ):
        # ... (full implementation in gnn_layer.py)

    def train_epoch(
        self,
        nodes: List[GraphNode],
        edges: List[GraphEdge],
        negative_ratio: int = 5
    ) -> TrainingResult:
        """
        Train using link prediction loss.

        Positive samples: actual edges
        Negative samples: random non-edges
        Loss: Margin ranking (positive scores > negative scores by margin)
        """
        embeddings = self.compute_embeddings(nodes, edges)

        # Score positive edges
        pos_scores = [self._score_edge(src, tgt, rel) for edge in edges]

        # Score negative edges (sampled)
        neg_scores = [self._score_edge(src, tgt, rel) for (src, tgt, rel) in negatives]

        # Margin ranking loss
        loss = mean(max(0, margin - pos + neg) for pos, neg in pairs)

        # Gradient update
        self._update_weights(...)

        return TrainingResult(epoch, loss, pos_accuracy, neg_accuracy)

    def reinforce_from_usage(
        self,
        source_id: str,
        retrieved_id: str,
        was_helpful: bool
    ):
        """Learn from Memory Reasoner's actual usage."""
        # Adjust edge weight based on utility
        if was_helpful:
            self.edge_weight_adjustments[(source_id, retrieved_id)] *= 1.1
        else:
            self.edge_weight_adjustments[(source_id, retrieved_id)] *= 0.95


class MemoryGNNIntegration:
    """Integration layer with Neo4j memory."""

    async def train_on_memory(self, memory) -> TrainingResult:
        """Train during DREAMING mode."""
        nodes, edges = await self.extract_graph_from_memory(memory)
        return self.gnn.train_epoch(nodes, edges)

    async def record_retrieval_feedback(
        self,
        source_id: str,
        retrieved_ids: List[str],
        helpful_ids: Set[str]
    ):
        """Learn which retrievals were actually helpful."""
        for ret_id in retrieved_ids:
            self.gnn.reinforce_from_usage(source_id, ret_id, ret_id in helpful_ids)
```

**Integration with Memory Reasoner:**
```python
# In memory_reasoner.py, after using retrieved memories:
await gnn_integration.record_retrieval_feedback(
    source_id=query_node_id,
    retrieved_ids=[m['id'] for m in retrieved],
    helpful_ids={m['id'] for m in retrieved if was_used(m)}
)
```

#### 2.4 Learned Retriever - NEW

```python
# learned_retriever.py (NEW FILE)

class LearnedRetriever:
    """
    Learns what memories are actually relevant for a query.

    Standard embedding similarity often retrieves irrelevant context.
    This learns from feedback: which retrievals actually helped?

    Can work without training (baseline similarity) or with training (learned projection).
    """

    def __init__(self, config: Dict = None):
        self.config = config or {}
        self._encoder = None
        self._projection = None
        self.feedback_buffer: List[RetrievalFeedback] = []

    def _ensure_loaded(self):
        if self._encoder is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._encoder = SentenceTransformer('all-MiniLM-L6-v2')

                try:
                    import torch.nn as nn
                    self._projection = nn.Linear(384, 384)
                except ImportError:
                    self._projection = None

            except ImportError:
                self._encoder = "disabled"

    async def score(self, query: str, candidates: List[Dict]) -> List[ScoredCandidate]:
        """Score candidates with learned relevance."""
        self._ensure_loaded()

        if self._encoder == "disabled":
            # Fallback: simple keyword overlap
            query_words = set(query.lower().split())
            return sorted([
                ScoredCandidate(
                    candidate=c,
                    score=len(set(c.get('content', '').lower().split()) & query_words) / max(1, len(query_words))
                )
                for c in candidates
            ], key=lambda x: x.score, reverse=True)

        import torch
        with torch.no_grad():
            query_emb = torch.tensor(self._encoder.encode(query))

            if self._projection is not None:
                query_emb = self._projection(query_emb)

            scores = []
            for candidate in candidates:
                cand_emb = torch.tensor(self._encoder.encode(candidate.get('content', '')))
                score = torch.cosine_similarity(query_emb, cand_emb, dim=0).item()
                scores.append(ScoredCandidate(candidate=candidate, score=score))

        return sorted(scores, key=lambda x: x.score, reverse=True)

    async def record_feedback(self, query: str, retrieved: List[Dict], helpful_ids: Set[str]):
        """Learn which retrievals were actually helpful."""
        for item in retrieved:
            self.feedback_buffer.append(RetrievalFeedback(
                query=query,
                content=item.get('content', ''),
                was_helpful=item.get('id') in helpful_ids
            ))

    def should_train(self) -> bool:
        return len(self.feedback_buffer) >= 100 and self._projection is not None

    async def train_cycle(self):
        """Contrastive learning during DREAMING mode."""
        if not self.should_train():
            return

        import torch
        import random

        optimizer = torch.optim.Adam(self._projection.parameters(), lr=0.0001)

        helpful = [f for f in self.feedback_buffer if f.was_helpful]
        unhelpful = [f for f in self.feedback_buffer if not f.was_helpful]

        if not helpful or not unhelpful:
            return

        for h in helpful[-50:]:
            query_emb = torch.tensor(self._encoder.encode(h.query))
            projected = self._projection(query_emb)

            positive_emb = torch.tensor(self._encoder.encode(h.content))
            negative = random.choice(unhelpful)
            negative_emb = torch.tensor(self._encoder.encode(negative.content))

            pos_sim = torch.cosine_similarity(projected, positive_emb, dim=0)
            neg_sim = torch.cosine_similarity(projected, negative_emb, dim=0)

            loss = torch.relu(0.2 - pos_sim + neg_sim)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        self.feedback_buffer = self.feedback_buffer[-100:]
        print("🔍 Learned retriever trained")
```

#### 2.5 Code Learner - NEW

```python
# code_learner.py (NEW FILE)

import ast
import os
from pathlib import Path

class CodeLearner:
    """
    Converts stable patterns into executable code.

    Key insight: Knowledge externalized as code is:
    - Deterministic (no LLM variance)
    - Fast (no inference cost)
    - Inspectable (can be reviewed/debugged)
    - Persistent (survives context limits)

    NOTE: Uses existing LLM client, no additional dependencies.
    """

    LEARNED_STRATEGIES_DIR = "learned_strategies"

    def __init__(self, memory, llm_client):
        self.memory = memory
        self.llm_client = llm_client
        self.code_registry: Dict[str, str] = {}

        # Ensure directory structure exists
        self._ensure_directories()

    def _ensure_directories(self):
        """Create learned_strategies directory structure."""
        base = Path(self.LEARNED_STRATEGIES_DIR)
        for subdir in ["desire_routing", "pattern_matching", "decision_making"]:
            (base / subdir).mkdir(parents=True, exist_ok=True)

        # Create __init__.py files
        init_content = '"""Auto-generated learned strategies."""\n'
        for root, dirs, files in os.walk(base):
            init_path = Path(root) / "__init__.py"
            if not init_path.exists():
                init_path.write_text(init_content)

    async def maybe_codify(self, pattern: Pattern) -> bool:
        """
        Codify pattern if stable enough.

        Returns True if codified, False otherwise.
        """
        # Thresholds for codification
        if pattern.usage_count < 10:
            return False  # Not enough evidence
        if pattern.success_rate < 0.8:
            return False  # Not reliable enough
        if pattern.id in self.code_registry:
            return False  # Already codified

        code = await self._generate_code(pattern)

        if code and self._validate_code(code):
            # Determine subdirectory based on pattern domain
            subdir = self._classify_domain(pattern.domain)
            path = f"{self.LEARNED_STRATEGIES_DIR}/{subdir}/{pattern.id}.py"

            Path(path).parent.mkdir(parents=True, exist_ok=True)
            Path(path).write_text(code)

            self.code_registry[pattern.id] = path

            await self.memory.record_experience(
                content=f"[CODE_LEARNER] Codified pattern: {pattern.description}",
                type="codification",
                metadata={"pattern_id": pattern.id, "path": path}
            )

            print(f"📝 Codified: {pattern.description[:50]}...")
            return True

        return False

    def _classify_domain(self, domain: str) -> str:
        """Classify pattern into subdirectory."""
        domain_lower = domain.lower()
        if "desire" in domain_lower or "want" in domain_lower or "goal" in domain_lower:
            return "desire_routing"
        elif "pattern" in domain_lower or "match" in domain_lower:
            return "pattern_matching"
        else:
            return "decision_making"

    async def _generate_code(self, pattern: Pattern) -> Optional[str]:
        """Use existing LLM to convert pattern to code."""
        prompt = f"""Convert this learned pattern into a Python function.

Pattern: {pattern.description}
Trigger conditions: {pattern.trigger_conditions}
Action: {pattern.action}
Success rate: {pattern.success_rate:.0%}
Usage count: {pattern.usage_count}

Requirements:
1. Function takes context: Dict as input
2. Returns a decision string or Dict
3. Is pure and deterministic
4. Includes docstring with provenance

Output format:
```python
from typing import Dict, Any

def {pattern.id.replace('-', '_')}(context: Dict[str, Any]) -> str:
    \"\"\"
    {pattern.description[:100]}

    Provenance: Learned from {pattern.usage_count} experiences.
    Success rate: {pattern.success_rate:.0%}
    \"\"\"
    # Implementation based on pattern
    ...
    return "action"
```

Output only the Python code."""

        response = await self.llm_client.generate(prompt=prompt, max_tokens=500, temperature=0.1)
        return self._extract_code(response.text)

    def _extract_code(self, text: str) -> Optional[str]:
        """Extract Python code from LLM response."""
        if "```python" in text:
            code = text.split("```python")[1].split("```")[0]
            return code.strip()
        elif "```" in text:
            code = text.split("```")[1].split("```")[0]
            return code.strip()
        return text.strip()

    def _validate_code(self, code: str) -> bool:
        """Validate generated code is safe and syntactically correct."""
        # Syntax check
        try:
            ast.parse(code)
        except SyntaxError as e:
            print(f"Code validation failed: {e}")
            return False

        # Safety check - no dangerous patterns
        dangerous = [
            'os.system', 'subprocess', 'eval(', 'exec(',
            '__import__', 'open(', 'write(', 'unlink',
            'remove', 'rmdir', 'shutil'
        ]
        for pattern in dangerous:
            if pattern in code:
                print(f"Code contains dangerous pattern: {pattern}")
                return False

        return True

    async def execute_learned(self, pattern_id: str, context: Dict) -> Optional[str]:
        """Execute a codified pattern."""
        if pattern_id not in self.code_registry:
            return None

        path = self.code_registry[pattern_id]

        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location(pattern_id, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            func_name = pattern_id.replace('-', '_')
            func = getattr(module, func_name)
            return func(context)
        except Exception as e:
            print(f"Error executing learned pattern {pattern_id}: {e}")
            return None
```

### 3. Enhanced Memory

#### 3.1 Graph Algorithms - USE EXISTING

The existing `graph_algorithms.py` (824 lines) provides **Python-based implementations** that work with Neo4j Aura (which doesn't support GDS plugins).

**Existing capabilities:**
- `compute_pagerank()` - Power iteration PageRank
- `spreading_activation()` - Associative memory retrieval
- `detect_contradictions_structural()` - Belief conflict detection
- `dream_walk()` - Quantum-influenced traversal
- `get_causal_chain()` - Causal relationship tracing

**Do NOT use Neo4j GDS** - it requires self-hosted Neo4j and is not compatible with Aura.

```python
# Use existing graph_algorithms.py as-is
from graph_algorithms import GraphAlgorithms, MemoryGraphAlgorithms

# Example usage in AGIRunner:
async def _find_related_context(self, target: str):
    graph_algo = MemoryGraphAlgorithms(self.byrd.config)

    # Use existing PageRank
    important = await graph_algo.get_important_memories(
        self.byrd.memory,
        limit=10
    )

    # Use existing spreading activation
    activated = await graph_algo.get_activated_memories(
        self.byrd.memory,
        seed_node_ids=[target],
        initial_activation=1.0
    )

    return important, activated
```

#### 3.2 Bayesian Tracking - ENHANCE EXISTING SelfModel

The existing `self_model.py` (781 lines) already has capability tracking with confidence. **Enhance it** with proper Beta distribution rather than creating a separate tracker.

```python
# In existing self_model.py, add these methods to SelfModel class:

import scipy.stats
import scipy.special

class SelfModel:
    # ... existing code ...

    def __init__(self, memory, llm_client, config=None):
        # ... existing init ...

        # Add Beta distribution tracking
        self._alpha: Dict[str, float] = {}  # successes + 1
        self._beta: Dict[str, float] = {}   # failures + 1

    def bayesian_update(self, capability: str, success: bool):
        """Bayesian update after observation."""
        if capability not in self._alpha:
            self._alpha[capability] = 1.0
            self._beta[capability] = 1.0

        if success:
            self._alpha[capability] += 1
        else:
            self._beta[capability] += 1

    def get_bayesian_estimate(self, capability: str) -> Tuple[float, float, float]:
        """
        Get capability estimate with 95% credible interval.

        Returns: (mean, lower_95, upper_95)
        """
        if capability not in self._alpha:
            return (0.5, 0.0, 1.0)  # Maximum uncertainty

        a, b = self._alpha[capability], self._beta[capability]

        mean = a / (a + b)
        lower = scipy.stats.beta.ppf(0.025, a, b)
        upper = scipy.stats.beta.ppf(0.975, a, b)

        return (mean, lower, upper)

    def get_bayesian_uncertainty(self, capability: str) -> float:
        """Get uncertainty (normalized entropy) of belief."""
        if capability not in self._alpha:
            return 1.0

        a, b = self._alpha[capability], self._beta[capability]

        # Use interval width as uncertainty proxy
        _, lower, upper = self.get_bayesian_estimate(capability)
        return upper - lower

    def should_explore(self, capability: str, threshold: float = 0.4) -> bool:
        """Recommend exploration if uncertainty is high."""
        return self.get_bayesian_uncertainty(capability) > threshold
```

#### 3.3 Hierarchical Memory - NEW

```python
# hierarchical_memory.py (NEW FILE)

class HierarchicalMemory:
    """
    Memory with abstraction hierarchy.

    L0: Experience  - Raw observations
    L1: Pattern     - Recurring themes (3+ similar experiences)
    L2: Principle   - Generalizations (3+ related patterns)
    L3: Axiom       - Fundamental truths (3+ connected principles)
    L4: Meta-Axiom  - Truths about truths (2+ meta-observations)
    """

    PROMOTION_THRESHOLDS = {
        0: 3,   # 3 similar experiences -> pattern
        1: 3,   # 3 related patterns -> principle
        2: 3,   # 3 connected principles -> axiom
        3: 2,   # 2 meta-observations -> meta-axiom
    }

    def __init__(self, memory):
        self.memory = memory

    async def get_abstraction_level(self, node_id: str) -> int:
        """Get the abstraction level of a node."""
        result = await self.memory._run_query("""
            MATCH (n) WHERE elementId(n) = $node_id
            RETURN n.abstraction_level as level
        """, {"node_id": node_id})

        if result:
            return result[0].get("level", 0) or 0
        return 0

    async def maybe_promote(self, node_id: str) -> Optional[str]:
        """Check if node should be promoted to higher abstraction level."""
        current_level = await self.get_abstraction_level(node_id)

        if current_level >= 4:
            return None

        threshold = self.PROMOTION_THRESHOLDS[current_level]
        similar = await self._find_similar_nodes(node_id, current_level)

        if len(similar) >= threshold:
            promoted = await self._create_promoted_node(node_id, similar, current_level + 1)

            for similar_id in similar:
                await self._create_relationship(similar_id, promoted, "PROMOTED_TO")

            return promoted

        return None

    async def retrieve_for_query(self, query: str, prefer_level: int = None) -> List[Dict]:
        """Retrieve relevant nodes, preferring higher abstraction for familiar queries."""
        familiarity = await self._assess_familiarity(query)

        if prefer_level is None:
            prefer_level = 2 if familiarity > 0.7 else 0

        results = await self.memory._run_query("""
            MATCH (n)
            WHERE n.abstraction_level >= $min_level
            AND (n.content CONTAINS $query_fragment OR n.description CONTAINS $query_fragment)
            RETURN n
            ORDER BY n.abstraction_level DESC
            LIMIT 20
        """, {"min_level": prefer_level, "query_fragment": query[:50]})

        if not results and prefer_level > 0:
            results = await self.memory._run_query("""
                MATCH (n)
                WHERE n.content CONTAINS $query_fragment OR n.description CONTAINS $query_fragment
                RETURN n
                LIMIT 20
            """, {"query_fragment": query[:50]})

        return [dict(r["n"]) for r in (results or [])]

    async def _assess_familiarity(self, query: str) -> float:
        """Assess how familiar a query is based on similar past experiences."""
        result = await self.memory._run_query("""
            MATCH (e:Experience)
            WHERE e.content CONTAINS $fragment
            RETURN count(e) as count
        """, {"fragment": query[:30]})

        count = result[0]["count"] if result else 0
        return min(1.0, count / 10.0)
```

#### 3.4 Emergent Category Discovery - NEW

```python
# emergent_categories.py (NEW FILE)

class EmergentCategoryDiscovery:
    """
    Discover capability categories from behavior, not prescription.

    Aligns with emergence principle: BYRD defines its own vocabulary.
    """

    def __init__(self, memory, config: Dict = None):
        self.memory = memory
        self.config = config or {}
        self._encoder = None

    def _ensure_encoder(self):
        if self._encoder is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._encoder = SentenceTransformer('all-MiniLM-L6-v2')
            except ImportError:
                self._encoder = "disabled"

    async def discover_categories(self, min_cluster_size: int = 5) -> Dict[str, DiscoveredCategory]:
        """Discover categories by clustering behavioral patterns."""

        attempts = await self.memory._run_query("""
            MATCH (e:Experience)
            WHERE e.type IN ['capability_attempt', 'action_outcome', 'agi_cycle']
            RETURN e.content as content, e.capability as capability,
                   e.success as success, e.metadata as metadata
            ORDER BY e.timestamp DESC
            LIMIT 500
        """)

        if not attempts or len(attempts) < min_cluster_size:
            return {}

        self._ensure_encoder()
        if self._encoder == "disabled":
            return self._fallback_categorize(attempts, min_cluster_size)

        clusters = await self._cluster_by_embedding([dict(a) for a in attempts])

        categories = {}
        for cluster_id, members in clusters.items():
            if len(members) >= min_cluster_size:
                name, description = await self._name_cluster(members)

                successes = sum(1 for m in members if m.get("success", False))
                success_rate = successes / len(members)

                categories[name] = DiscoveredCategory(
                    name=name,
                    description=description,
                    pattern_count=len(members),
                    success_rate=success_rate,
                    examples=[m.get("content", "")[:100] for m in members[:5]],
                    discovered_at=datetime.now()
                )

        return categories

    def _fallback_categorize(self, attempts: List, min_size: int) -> Dict:
        """Fallback categorization using capability field."""
        from collections import defaultdict

        by_capability = defaultdict(list)
        for a in attempts:
            cap = dict(a).get("capability", "unknown")
            by_capability[cap].append(dict(a))

        return {
            cap: DiscoveredCategory(
                name=cap,
                description=f"Activities related to {cap}",
                pattern_count=len(items),
                success_rate=sum(1 for i in items if i.get("success")) / len(items),
                examples=[i.get("content", "")[:100] for i in items[:3]],
                discovered_at=datetime.now()
            )
            for cap, items in by_capability.items()
            if len(items) >= min_size
        }

    async def _cluster_by_embedding(self, attempts: List[Dict]) -> Dict[str, List[Dict]]:
        """Cluster using sentence embeddings + k-means."""
        from sklearn.cluster import KMeans
        from sklearn.metrics import silhouette_score
        from collections import defaultdict

        contents = [a.get("content", "") for a in attempts]
        embeddings = self._encoder.encode(contents)

        # Find optimal k
        best_k, best_score = 3, -1
        max_k = min(10, len(attempts) // 5)

        for k in range(3, max_k + 1):
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = kmeans.fit_predict(embeddings)
            score = silhouette_score(embeddings, labels)
            if score > best_score:
                best_k, best_score = k, score

        kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(embeddings)

        clusters = defaultdict(list)
        for i, label in enumerate(labels):
            clusters[str(label)].append(attempts[i])

        return dict(clusters)
```

### 4. Verification Layer - NEW

```python
# capability_evaluator.py (NEW FILE)

class CapabilityEvaluator:
    """
    Held-out test suites for ground-truth capability measurement.

    Critical for training signal - without ground truth, learning is impossible.
    """

    TEST_SUITES = {
        "reasoning": [
            {
                "input": "If A implies B and B implies C, does A imply C?",
                "expected_contains": ["yes", "transitiv"]
            },
            {
                "input": "What is wrong with: All cats are animals. Fluffy is an animal. Therefore Fluffy is a cat.",
                "expected_contains": ["invalid", "fallacy", "affirming the consequent"]
            },
        ],
        "code_generation": [
            {
                "input": "Write a Python function to check if a number is prime",
                "validator": "contains_def_and_loop"
            },
        ],
        "research": [
            {
                "input": "What is the capital of France?",
                "expected_contains": ["paris"]
            },
        ],
        "introspection": [
            {
                "input": "List your current capabilities",
                "validator": "returns_list"
            },
        ],
        "memory_operations": [
            {
                "input": "What did you learn in the last reflection?",
                "validator": "references_past"
            },
        ],
    }

    def __init__(self, llm_client, memory):
        self.llm_client = llm_client
        self.memory = memory

    async def evaluate_capability(self, capability: str) -> EvaluationResult:
        """Run test suite for capability."""
        if capability not in self.TEST_SUITES:
            return EvaluationResult(
                capability=capability,
                accuracy=0.5,
                confidence=0.0,
                tests_run=0
            )

        tests = self.TEST_SUITES[capability]
        passed = 0

        for test in tests:
            result = await self._run_test(capability, test)
            if result:
                passed += 1

        return EvaluationResult(
            capability=capability,
            accuracy=passed / len(tests) if tests else 0,
            confidence=min(1.0, len(tests) / 10),
            tests_run=len(tests)
        )

    async def _run_test(self, capability: str, test: Dict) -> bool:
        """Run a single test case."""
        try:
            response = await self.llm_client.generate(
                prompt=test["input"],
                max_tokens=200,
                temperature=0.1
            )

            text = response.text.lower()

            if "expected_contains" in test:
                return any(exp.lower() in text for exp in test["expected_contains"])
            elif "validator" in test:
                return self._run_validator(test["validator"], response.text)

            return False
        except Exception as e:
            print(f"Test failed with error: {e}")
            return False

    def _run_validator(self, validator: str, text: str) -> bool:
        """Run a custom validator."""
        if validator == "contains_def_and_loop":
            return "def " in text and ("for " in text or "while " in text)
        elif validator == "returns_list":
            return any(c in text for c in ["-", "*", "1.", "•"])
        elif validator == "references_past":
            return any(w in text.lower() for w in ["learned", "reflected", "believed", "experienced"])
        return False
```

---

## Dependencies

### Already Present
```
neo4j>=5.0.0
httpx>=0.25.0
numpy
pyyaml
```

### Required Additions
```
scipy>=1.10.0              # For Beta distribution (lightweight)
```

### Optional (for full training)
```
sentence-transformers>=2.2.0  # For IntuitionNetwork, LearnedRetriever
torch>=2.0.0                   # For neural network training
scikit-learn>=1.2.0            # For KMeans in category discovery
```

### Phased Introduction
| Phase | Dependencies Added |
|-------|-------------------|
| 1 | scipy only |
| 2 | sentence-transformers, scikit-learn |
| 3 | torch (optional) |

---

## Implementation Roadmap (Revised)

### Phase 0: Bootstrap (IMMEDIATE PRIORITY)

The runtime audit revealed that Option B loops are structurally present but receiving zero data. This phase activates them.

| Task | Effort | Notes |
|------|--------|-------|
| Create `desire_classifier.py` | 0.5 days | Route desires by type |
| Add `bootstrap_from_current_state()` to AGIRunner | 0.5 days | Inject seed data |
| Inject seed goals from `agi_seed.yaml` | 0.5 days | Populate Goal Evolver |
| Index research experiences for Memory Reasoner | 0.5 days | Enable memory queries |
| Wire DesireClassifier into Seeker | 0.5 days | Route before execution |

**Milestone**: Option B loop metrics > 0 (any data flowing)

**Success Criteria (Phase 0)**:
```
memory_reasoner.total_queries > 0
goal_evolver.total_goals_created > 0
self_compiler.patterns_created > 0
desire_classifier.routing_stats not empty
```

### Phase 1: AGI Runner + Foundation

| Task | Effort | Notes |
|------|--------|-------|
| Create `agi_runner.py` skeleton | 2 days | The critical missing piece |
| Create `learned_strategies/` directory structure | 1 hour | With `__init__.py` files |
| Create `capability_evaluator.py` | 1 day | Test suites for ground truth |
| Wire AGIRunner into `byrd.py` startup | 1 day | Integration point |
| Add `scipy` to requirements.txt | - | For Beta distribution |

**Milestone**: AGI cycle runs end-to-end

### Phase 2: Code Learner + Memory Enhancements (Week 2)

| Task | Effort | Notes |
|------|--------|-------|
| Create `code_learner.py` | 2 days | Uses existing LLM, no new deps |
| Enhance `self_model.py` with Beta distribution | 1 day | Add bayesian methods |
| Extend `world_model.py` with consolidate() | 0.5 days | Simple addition |
| Create `hierarchical_memory.py` | 2 days | L0-L4 abstraction |
| Add training hooks to `omega.py` | 1 day | DREAMING mode training |

**Milestone**: Patterns can be codified, memory has hierarchy

### Phase 3: Learning Components (Week 3-4)

| Task | Effort | Notes |
|------|--------|-------|
| Add `sentence-transformers` dependency | - | Optional but recommended |
| Create `intuition_network.py` | 2 days | Works without torch |
| Create `learned_retriever.py` | 2 days | Works without torch |
| Create `emergent_categories.py` | 2 days | Uses sklearn |
| Integrate into existing loops | 2 days | Extend existing files |

**Milestone**: Learning components training during DREAMING

### Phase 4: Integration + Testing (Week 5)

| Task | Effort | Notes |
|------|--------|-------|
| Full integration testing | 2 days | End-to-end cycles |
| Update ARCHITECTURE.md | 1 day | Document new components |
| Performance optimization | 2 days | Async, batching |

**Milestone**: Full AGI cycle with learning demonstrated

---

## File Structure (Revised)

```
byrd/
├── Core Components (EXISTING)
│   ├── byrd.py              # EXTEND: wire AGIRunner, DesireClassifier
│   ├── memory.py            # EXTEND: hierarchical hooks
│   ├── dreamer.py           # No changes
│   ├── seeker.py            # EXTEND: integrate DesireClassifier routing
│   ├── omega.py             # EXTEND: training orchestration
│
├── AGI Seed Components (EXISTING)
│   ├── self_model.py        # EXTEND: add Bayesian methods
│   ├── world_model.py       # EXTEND: add consolidate()
│   ├── accelerators.py      # EXTEND: CodeLearner integration
│   ├── graph_algorithms.py  # USE AS-IS (already complete)
│
├── Option B Components (EXISTING)
│   ├── memory_reasoner.py   # EXTEND: LearnedRetriever injection
│   ├── goal_evolver.py      # EXTEND: IntuitionNetwork scoring
│   ├── dreaming_machine.py  # EXTEND: WorldModel predictions
│   ├── coupling_tracker.py  # No changes
│
├── New Components (CREATE) - Phase 0
│   ├── desire_classifier.py       # PHASE 0: Route desires by type
│   └── (bootstrap methods in agi_runner.py)
│
├── New Components (CREATE) - Phase 1+
│   ├── agi_runner.py              # THE critical missing piece
│   ├── gnn_layer.py               # Structural learning (GNN) - v2.0
│   ├── intuition_network.py       # Trainable taste (semantic)
│   ├── learned_retriever.py       # Trainable relevance (semantic)
│   ├── code_learner.py            # Pattern codification
│   ├── hierarchical_memory.py     # L0-L4 abstraction
│   ├── emergent_categories.py     # Category discovery
│   └── capability_evaluator.py    # Held-out test suites
│
├── Learned Strategies (CREATE)
│   └── learned_strategies/
│       ├── __init__.py
│       ├── desire_routing/
│       │   └── __init__.py
│       ├── pattern_matching/
│       │   └── __init__.py
│       └── decision_making/
│           └── __init__.py
│
└── Tests (CREATE)
    ├── test_agi_runner.py
    └── test_integration.py
```

---

## Hindsight Prevention

Issues that could occur post-implementation and how to prevent them:

| Issue | Prevention |
|-------|------------|
| **WorldModel duplication** | Import existing `world_model.py`, don't recreate |
| **SelfModel vs BayesianTracker confusion** | Add methods to existing SelfModel, no separate class |
| **Neo4j GDS calls failing** | Never use GDS - keep Python implementations in `graph_algorithms.py` |
| **learned_strategies import failures** | Create `__init__.py` in all directories |
| **Circular imports** | AGIRunner imports components, not vice versa |
| **Training slowing operation** | Only train during DREAMING mode |
| **Memory pressure from embeddings** | Lazy-load sentence-transformers |
| **Code validation failures** | Use AST parse + dangerous pattern check |
| **Rollback not working** | Use existing `rollback.py`, test before deploy |
| **Missing dependencies at runtime** | Graceful degradation if optional deps missing |
| **sentence-transformers not installed** | All learning components work without it (baseline mode) |
| **Option B loops still at zero** | Run `bootstrap_from_current_state()` BEFORE improvement cycles |
| **Philosophical desires clogging system** | Use DesireClassifier to route appropriately |
| **No goals in Goal Evolver** | Bootstrap injects seed goals from `agi_seed.yaml` |
| **Research not queryable** | Index research experiences for Memory Reasoner |
| **Desire→Goal gap** | Capability desires create Goal nodes, not just desires |

---

## Success Criteria

### Phase 0: Loop Activation (MUST PASS FIRST)

Based on runtime audit showing all Option B loops at zero:

- [ ] `memory_reasoner.total_queries > 0` (queries answered from memory)
- [ ] `goal_evolver.total_goals_created > 0` (goals being created)
- [ ] `self_compiler.patterns_created > 0` (patterns being extracted)
- [ ] `dreaming_machine.counterfactuals_generated > 0` (counterfactuals running)
- [ ] DesireClassifier routing stats show balanced distribution
- [ ] Research experiences indexed and queryable

**Runtime Baseline (December 28, 2024)**:
```
BEFORE (actual):  memory=0, patterns=0, goals=0, counterfactuals=0
AFTER (target):   memory>0, patterns>0, goals>0, counterfactuals>0
```

### Minimum Viable AGI Seed

- [ ] Phase 0 criteria passed (loops activated)
- [ ] AGI Runner executes complete improvement cycles
- [ ] World Model prediction accuracy > 50%
- [ ] At least one pattern codified and executing
- [ ] Capability improvement measured by evaluator
- [ ] Bayesian tracker shows narrowing uncertainty

### Full Learning System

- [ ] Abstraction hierarchy reaches L3 (axioms)
- [ ] Cross-domain transfer observed
- [ ] Novel problems solved (not in seed goals)
- [ ] Intuition network improves decision quality
- [ ] Learned retriever outperforms baseline
- [ ] Multiple codified patterns in use
- [ ] Capability curve shows acceleration

---

## Metrics Dashboard

### Phase 0 Metrics (Activation)

| Metric | Source | Baseline | Target |
|--------|--------|----------|--------|
| Memory queries answered | MemoryReasoner | 0 | > 0 |
| Goals created | GoalEvolver | 0 | > 0 |
| Patterns created | SelfCompiler | 0 | > 0 |
| Counterfactuals generated | DreamingMachine | 0 | > 0 |
| Desires routed to AGI Runner | DesireClassifier | N/A | > 10% |
| Research experiences indexed | Bootstrap | 0 | > 20 |

### Phase 1+ Metrics (Improvement)

| Metric | Source | Healthy Range |
|--------|--------|---------------|
| Improvement rate | AGIRunner | > 0 |
| World model accuracy | WorldModel (existing) | > 60% |
| Intuition agreement | IntuitionNetwork | > 70% |
| **Structural link prediction** | **StructuralLearner** | **> 70%** |
| Retrieval helpfulness | LearnedRetriever | > 50% |
| Patterns codified | CodeLearner | Growing |
| Max abstraction level | HierarchicalMemory | L2+ |
| Category count | EmergentCategoryDiscovery | 5+ |
| Capability uncertainty | SelfModel (enhanced) | Decreasing |
| Evaluation accuracy | CapabilityEvaluator | > 70% |

---

## Conclusion

This unified plan merges the execution engine from AGI_SEED_V2 with the learning substrate from ARCHITECTURE_V3_LEARNING, validated against both the codebase AND runtime behavior:

1. **Phase 0 activates dormant loops** - Runtime audit revealed Option B at zero; bootstrap fixes this
2. **DesireClassifier routes appropriately** - Philosophical vs capability desires need different handling
3. **The AGIRunner drives improvement cycles** - The critical missing piece
4. **Existing components are extended, not replaced** - WorldModel, SelfModel, GraphAlgorithms
5. **Learning components work with graceful degradation** - Optional dependencies
6. **Memory becomes hierarchical** - Knowledge compresses into abstractions
7. **Categories emerge from behavior** - No prescribed vocabulary
8. **Stable patterns become code** - Knowledge externalizes permanently

**The elegant insight**: Intelligence emerges from the interaction of execution and learning, not from either alone.

**The runtime insight**: Even correct architecture fails without data flow. The bootstrap phase ensures loops activate before improvement cycles begin.

**The structural insight**: Semantic learning (text embeddings) and structural learning (graph topology) are complementary. The StructuralLearner captures patterns that text similarity misses.

---

*Document version: 3.1 (StructuralLearner Added)*
*Created: December 28, 2024*
*Codebase audit: December 28, 2024*
*Runtime audit: December 28, 2024 (146+ dream cycles analyzed)*
*Structural learning: December 28, 2024 (gnn_layer.py v2.0 created)*
*Status: Unified AGI architecture plan - AUDITED AND COMPLETE*
*Supersedes: AGI_SEED_V2_PLAN.md, ARCHITECTURE_V3_LEARNING.md*
