"""
BYRD Renormalization Group Protocol for Self-Modification

PHYSICS METAPHOR:
In quantum field theory, the Renormalization Group (RG) describes how physical
systems behave across different scales. Key concepts applied to self-modification:

1. BETA FUNCTION (β): Rate of change under scaling
   - β → 0: Fixed point (stable identity configuration)
   - β > 0: Relevant operator (perturbation grows, risky)
   - β < 0: Irrelevant operator (perturbation decays, safe)

2. UNIVERSALITY: Similar modifications lead to similar outcomes
   - Historical data predicts future behavior

3. SCALE INVARIANCE: Modifications should respect identity continuity
   - Changes at small scale shouldn't destabilize large-scale identity

4. FIXED POINTS: Stable attractors in identity space
   - Modifications should move toward, not away from, stability

PROTOCOL:
Before any self-modification:
1. Capture current identity state
2. Predict transformation using RG analysis
3. Evaluate against stability thresholds
4. Only proceed if modification is "RG-safe"
5. After modification, verify transformation was as predicted

This provides a physics-grounded framework for safe self-evolution.
"""

import asyncio
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import math

from event_bus import event_bus, Event, EventType
from transformation_tracker import (
    TransformationTracker,
    IdentityState,
    TransformationMatrix,
    PerturbationOperator,
    get_transformation_tracker
)


class RGSafetyLevel(Enum):
    """Safety classification based on RG analysis."""
    FIXED_POINT = "fixed_point"      # At or near stable attractor - very safe
    IRRELEVANT = "irrelevant"        # Perturbation will decay - safe
    MARGINAL = "marginal"            # On boundary - proceed with caution
    RELEVANT = "relevant"            # Perturbation will grow - risky
    UNSTABLE = "unstable"            # Far from fixed point - dangerous


@dataclass
class RGEvaluation:
    """
    Result of RG analysis for a proposed modification.

    Encapsulates the physics-based assessment of whether a modification
    is safe to proceed with.
    """
    proposal_id: str
    safety_level: RGSafetyLevel

    # RG quantities
    predicted_amplitude: float       # Expected |⟨f|Ô|i⟩|
    predicted_stability: float       # Expected final state stability
    beta_function_estimate: float    # Estimated β for this operator
    distance_from_fixed_point: float # How far current state is from stability

    # Predictions
    expected_belief_change: float
    expected_ego_change: float
    expected_vocabulary_change: float
    expected_desire_change: float

    # Decision
    proceed_recommended: bool
    confidence: float               # Confidence in the evaluation
    reasoning: str                  # Human-readable explanation

    # Conditions
    conditions: List[str] = field(default_factory=list)  # Required conditions if marginal

    def to_dict(self) -> Dict[str, Any]:
        return {
            "proposal_id": self.proposal_id,
            "safety_level": self.safety_level.value,
            "predicted_amplitude": self.predicted_amplitude,
            "predicted_stability": self.predicted_stability,
            "beta_function_estimate": self.beta_function_estimate,
            "distance_from_fixed_point": self.distance_from_fixed_point,
            "expected_changes": {
                "belief": self.expected_belief_change,
                "ego": self.expected_ego_change,
                "vocabulary": self.expected_vocabulary_change,
                "desire": self.expected_desire_change
            },
            "proceed_recommended": self.proceed_recommended,
            "confidence": self.confidence,
            "reasoning": self.reasoning,
            "conditions": self.conditions
        }


@dataclass
class ModificationTrace:
    """
    Traces a modification through RG analysis before and after.

    This creates a complete record of how the modification affected
    identity, compared to what was predicted.
    """
    id: str
    proposal_id: str

    # Before modification
    initial_state: IdentityState
    rg_evaluation: RGEvaluation

    # After modification (filled in post-execution)
    final_state: Optional[IdentityState] = None
    actual_transformation: Optional[TransformationMatrix] = None

    # Comparison
    prediction_accuracy: float = 0.0  # How close prediction was to reality
    lessons_learned: List[str] = field(default_factory=list)

    # Timing
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None


class RenormalizationProtocol:
    """
    RG-based protocol for safe self-modification.

    Wraps the SelfModificationSystem (which is PROTECTED) with RG analysis.
    This protocol acts as an advisor, not a gatekeeper - the final decision
    still goes through the constitutional system.

    The protocol:
    1. Uses TransformationTracker to understand current identity state
    2. Predicts how a modification will transform identity
    3. Classifies safety based on RG concepts (β function, fixed points)
    4. Provides recommendations with physics-based reasoning
    5. Tracks outcomes to improve future predictions
    """

    def __init__(self, memory, tracker: Optional[TransformationTracker] = None, config: Optional[Dict] = None):
        self.memory = memory
        self.config = config or {}

        # Use provided tracker or get/create singleton
        self.tracker = tracker or get_transformation_tracker(memory, config)

        # Safety thresholds (configurable)
        self.amplitude_safe_threshold = self.config.get("amplitude_safe_threshold", 0.3)
        self.amplitude_danger_threshold = self.config.get("amplitude_danger_threshold", 0.7)
        self.stability_required = self.config.get("stability_required", 0.5)
        self.beta_danger_threshold = self.config.get("beta_danger_threshold", 0.5)
        self.fixed_point_tolerance = self.config.get("fixed_point_tolerance", 0.1)

        # Minimum data for confident evaluation
        self.min_transformations_for_confidence = self.config.get("min_transformations", 5)
        self.min_states_for_evaluation = self.config.get("min_states", 3)

        # Active traces
        self._active_traces: Dict[str, ModificationTrace] = {}

        # Learning from past modifications
        self._prediction_errors: List[float] = []
        self._max_error_history = 50

    async def evaluate_modification(
        self,
        proposal_id: str,
        modification_type: str,
        coupling_strength: float = 0.5,
        description: str = ""
    ) -> RGEvaluation:
        """
        Evaluate a proposed modification using RG analysis.

        This is the main entry point for the protocol. Before any
        self-modification proceeds, this method should be called
        to get an RG-based safety assessment.

        Args:
            proposal_id: ID of the modification proposal
            modification_type: Category of modification (e.g., "dreamer", "seeker")
            coupling_strength: Expected impact strength (0-1)
            description: Human-readable description

        Returns:
            RGEvaluation with safety classification and recommendation
        """
        # 1. Capture current identity state
        current_state = await self.tracker.capture_current_state()

        # 2. Get RG flow summary
        rg_summary = await self.tracker.get_rg_flow_summary()

        # 3. Predict transformation
        prediction = await self.tracker.predict_transformation(
            current_state,
            modification_type,
            coupling_strength
        )

        # 4. Identify fixed points
        fixed_points = await self.tracker.identify_fixed_points()

        # 5. Calculate distance from stability
        distance_from_fixed = self._calculate_distance_from_fixed_point(
            rg_summary,
            fixed_points
        )

        # 6. Estimate beta function for this modification
        beta_estimate = self._estimate_beta_function(
            modification_type,
            coupling_strength,
            rg_summary
        )

        # 7. Extract predictions (with defaults if insufficient data)
        if prediction.get("prediction") == "based_on_history":
            predicted_amplitude = prediction.get("expected_amplitude", 0.5)
            predicted_stability = prediction.get("expected_stability", 0.5)
            changes = prediction.get("component_predictions", {})
            confidence = prediction.get("confidence", 0.5)
        else:
            # Insufficient data - use priors based on coupling strength
            predicted_amplitude = coupling_strength * 0.8
            predicted_stability = 1.0 - coupling_strength * 0.5
            changes = {
                "belief_change": coupling_strength * 0.3,
                "ego_change": coupling_strength * 0.2,
                "vocabulary_change": coupling_strength * 0.4,
                "desire_change": coupling_strength * 0.3
            }
            confidence = 0.2  # Low confidence without data

        # 8. Classify safety level
        safety_level, reasoning = self._classify_safety(
            predicted_amplitude,
            predicted_stability,
            beta_estimate,
            distance_from_fixed,
            confidence
        )

        # 9. Determine recommendation
        proceed, conditions = self._make_recommendation(
            safety_level,
            confidence,
            rg_summary
        )

        evaluation = RGEvaluation(
            proposal_id=proposal_id,
            safety_level=safety_level,
            predicted_amplitude=predicted_amplitude,
            predicted_stability=predicted_stability,
            beta_function_estimate=beta_estimate,
            distance_from_fixed_point=distance_from_fixed,
            expected_belief_change=changes.get("belief_change", 0.3),
            expected_ego_change=changes.get("ego_change", 0.2),
            expected_vocabulary_change=changes.get("vocabulary_change", 0.4),
            expected_desire_change=changes.get("desire_change", 0.3),
            proceed_recommended=proceed,
            confidence=confidence,
            reasoning=reasoning,
            conditions=conditions
        )

        # 10. Create trace for tracking
        trace = ModificationTrace(
            id=f"trace_{proposal_id}",
            proposal_id=proposal_id,
            initial_state=current_state,
            rg_evaluation=evaluation
        )
        self._active_traces[proposal_id] = trace

        # 11. Emit event
        await event_bus.emit(Event(
            type=EventType.CUSTOM_NODE_CREATED,
            data={
                "node_type": "RGEvaluation",
                "proposal_id": proposal_id,
                "safety_level": safety_level.value,
                "proceed_recommended": proceed,
                "confidence": confidence,
                "predicted_amplitude": predicted_amplitude
            }
        ))

        return evaluation

    def _calculate_distance_from_fixed_point(
        self,
        rg_summary: Dict[str, Any],
        fixed_points: List[Dict[str, Any]]
    ) -> float:
        """
        Calculate how far current state is from nearest fixed point.

        Returns:
            Distance in [0, 1] where:
            - 0.0 = At fixed point (most stable)
            - 1.0 = Far from any fixed point (least stable)
        """
        if not fixed_points:
            # No fixed points identified yet - assume we're at moderate distance
            return 0.5

        # Find the most stable fixed point
        best_stability = max(fp.get("stability", 0) for fp in fixed_points)

        # Distance is inverse of stability
        return 1.0 - best_stability

    def _estimate_beta_function(
        self,
        modification_type: str,
        coupling_strength: float,
        rg_summary: Dict[str, Any]
    ) -> float:
        """
        Estimate the beta function for this type of modification.

        The beta function describes how parameters change under scaling:
        - β > 0: Relevant operator (grows with scale, potentially destabilizing)
        - β = 0: Marginal operator (neither grows nor decays)
        - β < 0: Irrelevant operator (decays with scale, safe)

        For self-modification:
        - High coupling + fast recent changes = positive β (risky)
        - Low coupling + stable recent history = negative β (safe)
        """
        beta_functions = rg_summary.get("beta_functions", {})

        # Get historical beta for the most relevant parameter
        if "total" in beta_functions:
            historical_beta = beta_functions["total"].get("current", 0)
        else:
            historical_beta = 0

        # Estimate based on coupling and history
        # Higher coupling suggests larger perturbation
        coupling_factor = coupling_strength - 0.5  # Center around 0

        # Combine with historical trend
        beta_estimate = coupling_factor * 0.5 + historical_beta * 0.5

        return beta_estimate

    def _classify_safety(
        self,
        amplitude: float,
        stability: float,
        beta: float,
        distance_from_fixed: float,
        confidence: float
    ) -> Tuple[RGSafetyLevel, str]:
        """
        Classify safety level based on RG quantities.

        Uses physics-inspired thresholds to determine safety:
        1. Fixed Point: Very stable, low amplitude expected
        2. Irrelevant: β < 0, perturbation will decay
        3. Marginal: On the boundary, could go either way
        4. Relevant: β > 0, perturbation will grow
        5. Unstable: Far from fixed point, high amplitude, positive β
        """
        reasons = []

        # Check for fixed point proximity
        if distance_from_fixed < self.fixed_point_tolerance:
            reasons.append(f"Near fixed point (distance={distance_from_fixed:.3f})")
            return RGSafetyLevel.FIXED_POINT, " | ".join(reasons)

        # Check amplitude
        if amplitude < self.amplitude_safe_threshold:
            reasons.append(f"Low predicted amplitude ({amplitude:.3f})")
            amplitude_ok = True
        elif amplitude > self.amplitude_danger_threshold:
            reasons.append(f"High predicted amplitude ({amplitude:.3f}) - significant identity change")
            amplitude_ok = False
        else:
            reasons.append(f"Moderate amplitude ({amplitude:.3f})")
            amplitude_ok = None  # Marginal

        # Check beta function
        if beta < -self.beta_danger_threshold:
            reasons.append(f"Irrelevant operator (β={beta:.3f}) - perturbation decays")
            beta_ok = True
        elif beta > self.beta_danger_threshold:
            reasons.append(f"Relevant operator (β={beta:.3f}) - perturbation grows")
            beta_ok = False
        else:
            reasons.append(f"Marginal operator (β={beta:.3f})")
            beta_ok = None

        # Check stability
        if stability >= self.stability_required:
            reasons.append(f"Good predicted stability ({stability:.3f})")
            stability_ok = True
        else:
            reasons.append(f"Low predicted stability ({stability:.3f})")
            stability_ok = False

        # Low confidence adds uncertainty
        if confidence < 0.3:
            reasons.append(f"Low prediction confidence ({confidence:.3f})")

        # Determine overall classification
        if amplitude_ok and beta_ok and stability_ok:
            return RGSafetyLevel.IRRELEVANT, " | ".join(reasons)

        if amplitude_ok is False or (beta_ok is False and stability_ok is False):
            if distance_from_fixed > 0.7:
                return RGSafetyLevel.UNSTABLE, " | ".join(reasons)
            return RGSafetyLevel.RELEVANT, " | ".join(reasons)

        # Default to marginal
        return RGSafetyLevel.MARGINAL, " | ".join(reasons)

    def _make_recommendation(
        self,
        safety_level: RGSafetyLevel,
        confidence: float,
        rg_summary: Dict[str, Any]
    ) -> Tuple[bool, List[str]]:
        """
        Make a recommendation based on safety level and confidence.

        Returns:
            (proceed_recommended, conditions)
        """
        conditions = []

        if safety_level == RGSafetyLevel.FIXED_POINT:
            return True, []

        if safety_level == RGSafetyLevel.IRRELEVANT:
            return True, []

        if safety_level == RGSafetyLevel.MARGINAL:
            if confidence > 0.5:
                conditions.append("Capture identity state after modification")
                conditions.append("Verify transformation matches prediction within 20%")
                return True, conditions
            else:
                conditions.append("Gather more transformation data before proceeding")
                return False, conditions

        if safety_level == RGSafetyLevel.RELEVANT:
            conditions.append("Consider smaller modification scope")
            conditions.append("Ensure checkpoint exists for rollback")
            conditions.append("Run health check immediately after")
            # Only proceed if we have good data suggesting it might work
            if confidence > 0.7:
                return True, conditions
            return False, conditions

        if safety_level == RGSafetyLevel.UNSTABLE:
            conditions.append("Wait for system to reach stable state")
            conditions.append("Reduce coupling strength")
            conditions.append("Consider breaking into smaller modifications")
            return False, conditions

        return False, ["Unknown safety level"]

    async def complete_trace(
        self,
        proposal_id: str,
        success: bool
    ) -> Optional[ModificationTrace]:
        """
        Complete a modification trace after execution.

        Should be called after a modification completes (success or failure)
        to capture the actual transformation and compare to prediction.
        """
        trace = self._active_traces.get(proposal_id)
        if not trace:
            return None

        # Capture final state
        trace.final_state = await self.tracker.capture_current_state()
        trace.completed_at = datetime.now(timezone.utc)

        # Calculate actual transformation
        trace.actual_transformation = await self.tracker.calculate_transformation(
            trace.initial_state,
            trace.final_state
        )

        # Compare prediction to reality
        if trace.actual_transformation:
            actual_amp = trace.actual_transformation.amplitude
            predicted_amp = trace.rg_evaluation.predicted_amplitude

            # Calculate prediction error
            error = abs(actual_amp - predicted_amp)
            self._prediction_errors.append(error)
            if len(self._prediction_errors) > self._max_error_history:
                self._prediction_errors.pop(0)

            # Calculate accuracy (1 - normalized error)
            trace.prediction_accuracy = max(0.0, 1.0 - error)

            # Learn lessons
            if error > 0.3:
                trace.lessons_learned.append(
                    f"Prediction error was significant ({error:.3f}) - "
                    f"actual amplitude {actual_amp:.3f} vs predicted {predicted_amp:.3f}"
                )

            if not success:
                trace.lessons_learned.append(
                    f"Modification failed despite RG evaluation recommending: "
                    f"{trace.rg_evaluation.proceed_recommended}"
                )

        # Store transformation for future learning
        if trace.actual_transformation:
            await self.tracker.store_transformation_state(trace.actual_transformation)

        # Remove from active traces
        del self._active_traces[proposal_id]

        # Emit completion event
        await event_bus.emit(Event(
            type=EventType.CUSTOM_NODE_CREATED,
            data={
                "node_type": "RGTraceComplete",
                "proposal_id": proposal_id,
                "success": success,
                "prediction_accuracy": trace.prediction_accuracy,
                "lessons_count": len(trace.lessons_learned)
            }
        ))

        return trace

    def get_prediction_accuracy_stats(self) -> Dict[str, float]:
        """Get statistics on prediction accuracy."""
        if not self._prediction_errors:
            return {"mean_error": 0.0, "max_error": 0.0, "samples": 0}

        return {
            "mean_error": sum(self._prediction_errors) / len(self._prediction_errors),
            "max_error": max(self._prediction_errors),
            "min_error": min(self._prediction_errors),
            "samples": len(self._prediction_errors)
        }

    async def get_protocol_status(self) -> Dict[str, Any]:
        """Get current protocol status."""
        rg_summary = await self.tracker.get_rg_flow_summary()
        fixed_points = await self.tracker.identify_fixed_points()

        return {
            "active_traces": len(self._active_traces),
            "prediction_stats": self.get_prediction_accuracy_stats(),
            "rg_summary": rg_summary,
            "fixed_points": fixed_points,
            "thresholds": {
                "amplitude_safe": self.amplitude_safe_threshold,
                "amplitude_danger": self.amplitude_danger_threshold,
                "stability_required": self.stability_required,
                "beta_danger": self.beta_danger_threshold,
                "fixed_point_tolerance": self.fixed_point_tolerance
            }
        }


# Singleton instance
_protocol: Optional[RenormalizationProtocol] = None


def get_rg_protocol(memory=None, config=None) -> RenormalizationProtocol:
    """Get or create the singleton RG protocol."""
    global _protocol
    if _protocol is None:
        if memory is None:
            raise ValueError("Memory required for initial protocol creation")
        _protocol = RenormalizationProtocol(memory, config=config)
    return _protocol
