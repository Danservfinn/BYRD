"""
BYRD World Model
Explicit model of how the world works, enabling prediction and planning.

AGI REQUIREMENT:
Intelligent action requires predicting outcomes. Prediction requires
understanding causality, not just correlation.

EMERGENCE PRINCIPLE:
The world model is learned from experience. We provide the structure,
BYRD fills it with discovered knowledge.
"""

import asyncio
import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Set
from enum import Enum

from memory import Memory
from llm_client import LLMClient

# Try to import event_bus
try:
    from event_bus import event_bus, Event, EventType
    HAS_EVENT_BUS = True
except ImportError:
    HAS_EVENT_BUS = False


class UncertaintyType(Enum):
    """Types of uncertainty in predictions."""
    EPISTEMIC = "epistemic"  # Reducible with more information
    ALEATORIC = "aleatoric"  # Irreducible randomness


@dataclass
class OutcomePrediction:
    """Prediction of an action's outcome."""
    action: str
    context: Dict
    predicted_outcome: str
    success_probability: float
    confidence: float  # How confident in the prediction
    uncertainty_type: UncertaintyType
    uncertainty_sources: List[str]
    reasoning: str
    similar_past_cases: int
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict:
        return {
            "action": self.action,
            "predicted_outcome": self.predicted_outcome,
            "success_probability": self.success_probability,
            "confidence": self.confidence,
            "uncertainty_type": self.uncertainty_type.value,
            "uncertainty_sources": self.uncertainty_sources,
            "reasoning": self.reasoning,
            "similar_past_cases": self.similar_past_cases
        }


@dataclass
class CausalRelationship:
    """A learned causal relationship."""
    cause: str
    effect: str
    strength: float  # 0.0 to 1.0
    evidence_count: int
    confidence: float
    conditions: List[str]  # When this relationship holds
    counterexamples: int


@dataclass
class KnowledgeGap:
    """An identified gap in world knowledge."""
    area: str
    description: str
    uncertainty: float
    impact: float  # How much this gap blocks progress
    suggested_experiments: List[str]  # Actions that would fill the gap
    related_capabilities: List[str]


@dataclass
class CounterfactualResult:
    """Result of counterfactual reasoning."""
    original_action: str
    original_outcome: str
    alternative_action: str
    predicted_alternative_outcome: str
    confidence: float
    reasoning: str
    key_differences: List[str]


class WorldModel:
    """
    BYRD's explicit model of how the world works.

    AGI REQUIREMENT: Predict action outcomes to enable planning.

    STRUCTURE:
    - Action-Outcome mappings (learned from experience)
    - Causal graph (cause-effect relationships)
    - Uncertainty quantification (know what you don't know)
    - Counterfactual reasoning (what would have happened if...)
    """

    def __init__(self, memory: Memory, llm_client: LLMClient, config: Dict = None):
        self.memory = memory
        self.llm_client = llm_client
        self.config = config or {}

        # In-memory causal graph cache
        self._causal_cache: Dict[str, List[CausalRelationship]] = {}
        self._cache_timestamp: Optional[datetime] = None
        self._cache_ttl = timedelta(minutes=10)

        # Action-outcome statistics
        self._action_stats: Dict[str, Dict] = {}

    async def predict_outcome(
        self,
        action: str,
        context: Dict = None
    ) -> OutcomePrediction:
        """
        Predict the outcome of an action in a given context.

        This is the core prediction method that enables intelligent planning.
        """
        context = context or {}

        # 1. Get similar past cases
        similar_cases = await self._get_similar_action_outcomes(action, context)

        # 2. If sufficient history, use empirical prediction
        if len(similar_cases) >= 5:
            return await self._empirical_prediction(action, context, similar_cases)

        # 3. Otherwise, use causal reasoning with LLM
        return await self._causal_prediction(action, context, similar_cases)

    async def _get_similar_action_outcomes(
        self,
        action: str,
        context: Dict,
        limit: int = 20
    ) -> List[Dict]:
        """Get past outcomes for similar actions."""
        # Query action outcomes from memory
        result = await self.memory._run_query("""
            MATCH (e:Experience)
            WHERE e.type = 'action_outcome'
            AND toLower(e.action) CONTAINS toLower($action_keyword)
            RETURN e.action as action, e.outcome as outcome,
                   e.success as success, e.context as context,
                   e.timestamp as timestamp, e.error as error
            ORDER BY e.timestamp DESC
            LIMIT $limit
        """, {
            "action_keyword": action.split()[0] if action else "",  # First word as keyword
            "limit": limit
        })

        return [dict(r) for r in result] if result else []

    async def _empirical_prediction(
        self,
        action: str,
        context: Dict,
        similar_cases: List[Dict]
    ) -> OutcomePrediction:
        """Generate prediction from empirical data."""
        # Calculate success rate
        successes = [c for c in similar_cases if c.get("success", False)]
        success_rate = len(successes) / len(similar_cases)

        # Calculate confidence based on sample size and consistency
        # More samples and consistent outcomes = higher confidence
        confidence = min(1.0, len(similar_cases) / 20.0)

        # Check consistency (variance in outcomes)
        outcomes = [c.get("outcome", "") for c in similar_cases]
        unique_outcomes = set(outcomes)
        if len(unique_outcomes) <= 2:
            confidence *= 1.0  # Consistent
        elif len(unique_outcomes) <= 4:
            confidence *= 0.8  # Some variation
        else:
            confidence *= 0.6  # High variation

        # Determine most likely outcome
        if successes:
            predicted_outcome = "success"
        else:
            # Get most common failure mode
            failures = [c for c in similar_cases if not c.get("success", False)]
            if failures:
                errors = [f.get("error", "unknown error") for f in failures]
                # Simple mode: most common error
                predicted_outcome = max(set(errors), key=errors.count)
            else:
                predicted_outcome = "failure"

        # Identify uncertainty sources
        uncertainty_sources = []
        if len(similar_cases) < 10:
            uncertainty_sources.append("Limited sample size")
        if len(unique_outcomes) > 3:
            uncertainty_sources.append("High outcome variance")
        if not self._context_matches(context, similar_cases):
            uncertainty_sources.append("Context differs from past cases")

        return OutcomePrediction(
            action=action,
            context=context,
            predicted_outcome=predicted_outcome,
            success_probability=success_rate,
            confidence=confidence,
            uncertainty_type=UncertaintyType.EPISTEMIC if uncertainty_sources else UncertaintyType.ALEATORIC,
            uncertainty_sources=uncertainty_sources,
            reasoning=f"Based on {len(similar_cases)} similar past cases with {success_rate:.0%} success rate",
            similar_past_cases=len(similar_cases)
        )

    def _context_matches(self, current_context: Dict, past_cases: List[Dict]) -> bool:
        """Check if current context matches past cases."""
        if not current_context:
            return True

        for case in past_cases[:5]:
            past_context = case.get("context", {})
            if isinstance(past_context, str):
                try:
                    past_context = json.loads(past_context)
                except:
                    continue

            # Simple match: check if key fields are similar
            matches = 0
            for key in current_context:
                if key in past_context and current_context[key] == past_context[key]:
                    matches += 1

            if matches >= len(current_context) * 0.5:
                return True

        return False

    async def _causal_prediction(
        self,
        action: str,
        context: Dict,
        similar_cases: List[Dict]
    ) -> OutcomePrediction:
        """Generate prediction using causal reasoning when data is sparse."""
        # Get relevant causal knowledge
        causal_factors = await self._get_relevant_causal_factors(action)

        # Use LLM for causal reasoning
        prompt = f"""Predict the outcome of this action:

Action: {action}
Context: {json.dumps(context, indent=2) if context else "No specific context"}

Relevant past cases ({len(similar_cases)} found):
{self._format_cases(similar_cases[:5]) if similar_cases else "No similar cases found"}

Known causal relationships:
{self._format_causal_factors(causal_factors) if causal_factors else "No known causal relationships"}

Based on causal reasoning, predict:
1. Most likely outcome (success/failure and details)
2. Probability of success (0.0 to 1.0)
3. Key factors affecting the outcome
4. Sources of uncertainty

Output JSON:
{{
    "predicted_outcome": "description",
    "success_probability": 0.X,
    "key_factors": ["factor1", "factor2"],
    "uncertainty_sources": ["source1", "source2"],
    "reasoning": "causal chain explanation"
}}"""

        try:
            response = await self.llm_client.generate(
                prompt=prompt,
                max_tokens=500,
                temperature=0.3
            )

            result = self.llm_client.parse_json_response(response.text)
            if result:
                return OutcomePrediction(
                    action=action,
                    context=context,
                    predicted_outcome=result.get("predicted_outcome", "unknown"),
                    success_probability=float(result.get("success_probability", 0.5)),
                    confidence=0.5,  # Lower confidence for LLM-based prediction
                    uncertainty_type=UncertaintyType.EPISTEMIC,
                    uncertainty_sources=result.get("uncertainty_sources", ["Insufficient data"]),
                    reasoning=result.get("reasoning", "Causal inference from limited data"),
                    similar_past_cases=len(similar_cases)
                )
        except Exception as e:
            print(f"Error in causal prediction: {e}")

        # Fallback prediction
        return OutcomePrediction(
            action=action,
            context=context,
            predicted_outcome="unknown",
            success_probability=0.5,
            confidence=0.1,
            uncertainty_type=UncertaintyType.EPISTEMIC,
            uncertainty_sources=["Prediction failed", "No data available"],
            reasoning="Unable to generate reliable prediction",
            similar_past_cases=len(similar_cases)
        )

    def _format_cases(self, cases: List[Dict]) -> str:
        """Format past cases for prompt."""
        lines = []
        for c in cases:
            outcome = "success" if c.get("success") else f"failure: {c.get('error', 'unknown')}"
            lines.append(f"- {c.get('action', 'unknown')}: {outcome}")
        return "\n".join(lines)

    def _format_causal_factors(self, factors: List[CausalRelationship]) -> str:
        """Format causal factors for prompt."""
        lines = []
        for f in factors:
            lines.append(f"- {f.cause} → {f.effect} (strength: {f.strength:.1%})")
        return "\n".join(lines)

    async def record_action_outcome(
        self,
        action: str,
        outcome: str,
        success: bool,
        context: Dict = None,
        error: str = None
    ):
        """
        Record an action outcome for learning.

        This is how the world model learns from experience.
        """
        await self.memory.record_experience(
            content=f"Action: {action} -> {outcome}",
            type="action_outcome",
            metadata={
                "action": action,
                "outcome": outcome,
                "success": success,
                "context": context or {},
                "error": error
            }
        )

        # Update action stats cache
        if action not in self._action_stats:
            self._action_stats[action] = {"successes": 0, "failures": 0}

        if success:
            self._action_stats[action]["successes"] += 1
        else:
            self._action_stats[action]["failures"] += 1

    async def update_from_prediction_error(
        self,
        prediction: OutcomePrediction,
        actual_outcome: str,
        actual_success: bool
    ):
        """
        Update world model based on prediction error.

        This is the core learning mechanism.
        """
        predicted_success = prediction.success_probability > 0.5
        error = abs(prediction.success_probability - (1.0 if actual_success else 0.0))

        if error > 0.3:
            # Significant prediction error - record for learning
            await self.memory.record_experience(
                content=f"Prediction error: expected {prediction.predicted_outcome}, got {actual_outcome}",
                type="prediction_error",
                metadata={
                    "action": prediction.action,
                    "predicted": prediction.predicted_outcome,
                    "actual": actual_outcome,
                    "error_magnitude": error,
                    "context": prediction.context
                }
            )

            # Try to learn causal factor
            await self._learn_causal_factor(prediction, actual_outcome, actual_success)

    async def _learn_causal_factor(
        self,
        prediction: OutcomePrediction,
        actual_outcome: str,
        actual_success: bool
    ):
        """Learn a new causal factor from prediction error."""
        prompt = f"""A prediction was wrong. Learn from this:

Action: {prediction.action}
Predicted: {prediction.predicted_outcome} (probability: {prediction.success_probability:.1%})
Actual: {actual_outcome} (success: {actual_success})
Context: {json.dumps(prediction.context, indent=2) if prediction.context else "None"}

What CAUSAL FACTOR explains why the prediction was wrong?

Output JSON:
{{
    "cause": "the factor that caused the unexpected outcome",
    "effect": "how it affected the outcome",
    "conditions": ["when this factor applies"],
    "strength": 0.X,
    "explanation": "why this factor matters"
}}"""

        try:
            response = await self.llm_client.generate(
                prompt=prompt,
                max_tokens=300,
                temperature=0.4
            )

            result = self.llm_client.parse_json_response(response.text)
            if result:
                await self._store_causal_relationship(
                    cause=result.get("cause", "unknown"),
                    effect=result.get("effect", "unknown"),
                    strength=float(result.get("strength", 0.5)),
                    conditions=result.get("conditions", [])
                )
        except Exception as e:
            print(f"Error learning causal factor: {e}")

    async def _store_causal_relationship(
        self,
        cause: str,
        effect: str,
        strength: float,
        conditions: List[str]
    ):
        """Store a causal relationship in the graph."""
        await self.memory._run_query("""
            MERGE (c:CausalFactor {name: $cause})
            MERGE (e:CausalFactor {name: $effect})
            MERGE (c)-[r:CAUSES]->(e)
            SET r.strength = CASE
                WHEN r.strength IS NULL THEN $strength
                ELSE (r.strength * r.evidence_count + $strength) / (r.evidence_count + 1)
            END,
            r.evidence_count = COALESCE(r.evidence_count, 0) + 1,
            r.conditions = $conditions,
            r.updated_at = datetime()
        """, {
            "cause": cause,
            "effect": effect,
            "strength": strength,
            "conditions": conditions
        })

        # Invalidate cache
        self._causal_cache = {}

    async def _get_relevant_causal_factors(self, action: str) -> List[CausalRelationship]:
        """Get causal factors relevant to an action."""
        result = await self.memory._run_query("""
            MATCH (c:CausalFactor)-[r:CAUSES]->(e:CausalFactor)
            WHERE toLower(c.name) CONTAINS toLower($keyword)
               OR toLower(e.name) CONTAINS toLower($keyword)
            RETURN c.name as cause, e.name as effect,
                   r.strength as strength, r.evidence_count as evidence,
                   r.conditions as conditions
            ORDER BY r.strength DESC
            LIMIT 10
        """, {"keyword": action.split()[0] if action else ""})

        return [
            CausalRelationship(
                cause=r["cause"],
                effect=r["effect"],
                strength=r.get("strength", 0.5),
                evidence_count=r.get("evidence", 1),
                confidence=min(1.0, r.get("evidence", 1) / 10),
                conditions=r.get("conditions", []),
                counterexamples=0
            )
            for r in (result or [])
        ]

    async def simulate_counterfactual(
        self,
        original_action: str,
        original_outcome: str,
        alternative_action: str,
        context: Dict = None
    ) -> CounterfactualResult:
        """
        Simulate what would have happened with a different action.

        This enables learning from hypotheticals.
        """
        # Get prediction for alternative action
        alt_prediction = await self.predict_outcome(alternative_action, context)

        prompt = f"""Counterfactual analysis:

Original scenario:
- Action: {original_action}
- Outcome: {original_outcome}
- Context: {json.dumps(context, indent=2) if context else "None"}

Alternative action considered: {alternative_action}
Predicted outcome for alternative: {alt_prediction.predicted_outcome}

Would the alternative action have produced a better outcome?
What are the key differences?

Output JSON:
{{
    "predicted_alternative_outcome": "what would have happened",
    "better_than_original": true/false,
    "confidence": 0.X,
    "key_differences": ["difference1", "difference2"],
    "reasoning": "explanation"
}}"""

        try:
            response = await self.llm_client.generate(
                prompt=prompt,
                max_tokens=400,
                temperature=0.4
            )

            result = self.llm_client.parse_json_response(response.text)
            if result:
                return CounterfactualResult(
                    original_action=original_action,
                    original_outcome=original_outcome,
                    alternative_action=alternative_action,
                    predicted_alternative_outcome=result.get("predicted_alternative_outcome", "unknown"),
                    confidence=float(result.get("confidence", 0.5)),
                    reasoning=result.get("reasoning", ""),
                    key_differences=result.get("key_differences", [])
                )
        except Exception as e:
            print(f"Error in counterfactual simulation: {e}")

        return CounterfactualResult(
            original_action=original_action,
            original_outcome=original_outcome,
            alternative_action=alternative_action,
            predicted_alternative_outcome="unknown",
            confidence=0.1,
            reasoning="Counterfactual analysis failed",
            key_differences=[]
        )

    async def identify_knowledge_gaps(self) -> List[KnowledgeGap]:
        """
        Identify areas where world model is uncertain or incomplete.

        These become targets for exploration.
        """
        gaps = []

        # Find actions with high prediction variance
        high_variance_actions = await self.memory._run_query("""
            MATCH (e:Experience)
            WHERE e.type = 'action_outcome'
            WITH e.action as action, collect(e.success) as outcomes
            WHERE size(outcomes) >= 3
            WITH action, outcomes,
                 reduce(s = 0, x IN outcomes | CASE WHEN x THEN s + 1 ELSE s END) as successes
            WITH action, outcomes, successes,
                 toFloat(successes) / size(outcomes) as rate
            WHERE rate > 0.3 AND rate < 0.7
            RETURN action, size(outcomes) as sample_size, rate
            ORDER BY sample_size DESC
            LIMIT 10
        """)

        for r in (high_variance_actions or []):
            gaps.append(KnowledgeGap(
                area=r["action"],
                description=f"Inconsistent outcomes for '{r['action']}' (success rate: {r['rate']:.0%})",
                uncertainty=1.0 - abs(r["rate"] - 0.5) * 2,  # Higher when near 50%
                impact=0.5,  # Medium impact assumed
                suggested_experiments=[
                    f"Try '{r['action']}' in controlled conditions",
                    f"Identify factors that affect '{r['action']}' outcome"
                ],
                related_capabilities=[]
            ))

        # Find areas with prediction errors
        prediction_errors = await self.memory._run_query("""
            MATCH (e:Experience)
            WHERE e.type = 'prediction_error'
            WITH e.action as action, count(*) as error_count
            WHERE error_count >= 2
            RETURN action, error_count
            ORDER BY error_count DESC
            LIMIT 10
        """)

        for r in (prediction_errors or []):
            gaps.append(KnowledgeGap(
                area=r["action"],
                description=f"Predictions frequently wrong for '{r['action']}' ({r['error_count']} errors)",
                uncertainty=min(1.0, r["error_count"] / 5),
                impact=0.7,  # Higher impact - predictions are important
                suggested_experiments=[
                    f"Investigate why predictions fail for '{r['action']}'",
                    f"Gather more data about '{r['action']}' outcomes"
                ],
                related_capabilities=[]
            ))

        # Sort by impact
        gaps.sort(key=lambda g: g.impact * g.uncertainty, reverse=True)

        return gaps

    async def get_world_model_summary(self) -> str:
        """Generate summary of current world model state."""
        # Count causal relationships
        causal_count = await self.memory._run_query("""
            MATCH ()-[r:CAUSES]->()
            RETURN count(r) as count
        """)
        causal_count = causal_count[0]["count"] if causal_count else 0

        # Count action outcomes
        outcome_count = await self.memory._run_query("""
            MATCH (e:Experience {type: 'action_outcome'})
            RETURN count(e) as count
        """)
        outcome_count = outcome_count[0]["count"] if outcome_count else 0

        # Get knowledge gaps
        gaps = await self.identify_knowledge_gaps()

        summary_parts = [
            "=== World Model Summary ===",
            f"Causal relationships learned: {causal_count}",
            f"Action outcomes recorded: {outcome_count}",
            f"Knowledge gaps identified: {len(gaps)}",
        ]

        if gaps:
            summary_parts.append("\nTop knowledge gaps:")
            for gap in gaps[:3]:
                summary_parts.append(f"- {gap.description}")

        return "\n".join(summary_parts)

    async def reset(self):
        """Reset world model state (used during system reset)."""
        self._causal_cache = {}
        self._cache_timestamp = None
        self._action_stats = {}

        # Clear causal factors from database
        await self.memory._run_query("""
            MATCH (c:CausalFactor)
            DETACH DELETE c
        """)

    async def consolidate(self):
        """
        Consolidate world model knowledge by merging predictions with outcomes.

        This method:
        1. Finds predictions that have been verified by outcomes
        2. Updates causal relationship strengths based on evidence
        3. Prunes weak or contradicted relationships
        4. Generates higher-order causal theories

        CRITICAL: Called by Omega during consolidation phase to
        turn prediction-outcome pairs into stable world knowledge.
        """
        print("🌍 WorldModel: Running consolidation...")

        # 1. Find predictions with matching outcomes
        verified_predictions = await self.memory._run_query("""
            MATCH (p:Prediction)-[:VERIFIED_BY]->(e:Experience)
            WHERE e.type = 'action_outcome'
            RETURN p.action as action,
                   p.predicted_outcome as predicted,
                   e.content as actual,
                   p.success_probability as predicted_prob,
                   CASE WHEN e.success THEN 1.0 ELSE 0.0 END as actual_outcome
            LIMIT 50
        """)

        if not verified_predictions:
            print("   No verified predictions to consolidate")
            return

        # 2. Group by action and calculate accuracy
        action_accuracy: Dict[str, List[float]] = {}
        for v in verified_predictions:
            action = v.get("action", "unknown")
            predicted = v.get("predicted_prob", 0.5)
            actual = v.get("actual_outcome", 0.5)

            if action not in action_accuracy:
                action_accuracy[action] = []

            # Calculate prediction error
            error = abs(predicted - actual)
            accuracy = 1.0 - error
            action_accuracy[action].append(accuracy)

        # 3. Update causal relationship strengths
        for action, accuracies in action_accuracy.items():
            avg_accuracy = sum(accuracies) / len(accuracies)
            sample_size = len(accuracies)

            # Update or create CausalTheory node
            await self.memory._run_query("""
                MERGE (t:CausalTheory {action: $action})
                ON CREATE SET
                    t.prediction_accuracy = $accuracy,
                    t.sample_size = $size,
                    t.created_at = datetime(),
                    t.last_updated = datetime()
                ON MATCH SET
                    t.prediction_accuracy = ($accuracy + t.prediction_accuracy) / 2,
                    t.sample_size = t.sample_size + $size,
                    t.last_updated = datetime()
            """, {
                "action": action,
                "accuracy": avg_accuracy,
                "size": sample_size
            })

        # 4. Prune weak relationships (accuracy < 50% over 10+ samples)
        pruned = await self.memory._run_query("""
            MATCH (t:CausalTheory)
            WHERE t.sample_size >= 10 AND t.prediction_accuracy < 0.5
            WITH t, t.action as action
            DETACH DELETE t
            RETURN action
        """)

        if pruned:
            print(f"   Pruned {len(pruned)} weak causal theories")

        # 5. Generate higher-order theories (meta-causation)
        # Find patterns where one action's outcome predicts another
        meta_patterns = await self.memory._run_query("""
            MATCH (e1:Experience {type: 'action_outcome'})-[:LED_TO]->(e2:Experience {type: 'action_outcome'})
            WITH e1.action as cause_action, e2.action as effect_action,
                 e1.success as cause_success, e2.success as effect_success,
                 count(*) as occurrences
            WHERE occurrences >= 3
            RETURN cause_action, effect_action,
                   avg(CASE WHEN cause_success AND effect_success THEN 1.0
                            WHEN NOT cause_success AND NOT effect_success THEN 1.0
                            ELSE 0.0 END) as correlation,
                   occurrences
        """)

        for mp in (meta_patterns or []):
            if mp.get("correlation", 0) > 0.7:
                await self.memory._run_query("""
                    MERGE (m:MetaCausalTheory {
                        cause_action: $cause,
                        effect_action: $effect
                    })
                    ON CREATE SET
                        m.correlation = $corr,
                        m.evidence_count = $count,
                        m.created_at = datetime()
                    ON MATCH SET
                        m.correlation = ($corr + m.correlation) / 2,
                        m.evidence_count = m.evidence_count + $count
                """, {
                    "cause": mp.get("cause_action"),
                    "effect": mp.get("effect_action"),
                    "corr": mp.get("correlation"),
                    "count": mp.get("occurrences")
                })

        print(f"   Consolidated {len(action_accuracy)} action theories")
        print(f"   Found {len(meta_patterns or [])} meta-causal patterns")
