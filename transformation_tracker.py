"""
BYRD Transformation Tracker
Renormalization Group approach for identity evolution analysis.

PHYSICS METAPHOR:
- Identity states are vectors in an abstract "Byrd field" space
- Experiences act as perturbation operators
- Matrix elements ⟨ψ_f|Ô|ψ_i⟩ quantify transition amplitudes
- RG flow tracks how identity transforms under scale changes (coarse-graining)

This module calculates the "matrix elements of transformation states" -
predicting how BYRD evolves when perturbed by new data inputs.

EMERGENCE PRINCIPLE:
The RG framework does not prescribe what identity should be. It only
observes and quantifies the transformations that naturally occur.
"""

import asyncio
import json
import hashlib
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import math

from event_bus import event_bus, Event, EventType


@dataclass
class IdentityState:
    """
    A snapshot of BYRD's identity at a moment in time.

    The state vector is composed of:
    - Active beliefs (weighted by confidence)
    - Ego traits (weighted by priority)
    - Reflection patterns (vocabulary frequencies)
    - Desire landscape (active desires weighted by intensity)
    """
    timestamp: datetime
    belief_vector: Dict[str, float]      # belief_id -> confidence
    ego_vector: Dict[str, float]         # ego_id -> priority (normalized)
    vocabulary_vector: Dict[str, float]  # output_key -> frequency
    desire_vector: Dict[str, float]      # desire_id -> intensity

    # Derived quantities
    norm: float = 0.0  # ||ψ|| - state magnitude

    def __post_init__(self):
        """Calculate state norm on creation."""
        total = 0.0
        for vec in [self.belief_vector, self.ego_vector,
                    self.vocabulary_vector, self.desire_vector]:
            total += sum(v**2 for v in vec.values())
        self.norm = math.sqrt(total) if total > 0 else 1.0

    def inner_product(self, other: 'IdentityState') -> float:
        """
        Calculate ⟨self|other⟩ - overlap between states.

        Returns value in [0, 1] where:
        - 1.0 = identical states
        - 0.0 = orthogonal states (completely different identity)
        """
        dot = 0.0

        # Belief overlap
        for k, v in self.belief_vector.items():
            if k in other.belief_vector:
                dot += v * other.belief_vector[k]

        # Ego overlap
        for k, v in self.ego_vector.items():
            if k in other.ego_vector:
                dot += v * other.ego_vector[k]

        # Vocabulary overlap
        for k, v in self.vocabulary_vector.items():
            if k in other.vocabulary_vector:
                dot += v * other.vocabulary_vector[k]

        # Desire overlap
        for k, v in self.desire_vector.items():
            if k in other.desire_vector:
                dot += v * other.desire_vector[k]

        # Normalize by norms
        if self.norm > 0 and other.norm > 0:
            return dot / (self.norm * other.norm)
        return 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Serialize for storage."""
        return {
            "timestamp": self.timestamp.isoformat(),
            "belief_vector": self.belief_vector,
            "ego_vector": self.ego_vector,
            "vocabulary_vector": self.vocabulary_vector,
            "desire_vector": self.desire_vector,
            "norm": self.norm
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'IdentityState':
        """Deserialize from storage."""
        return cls(
            timestamp=datetime.fromisoformat(data["timestamp"]),
            belief_vector=data.get("belief_vector", {}),
            ego_vector=data.get("ego_vector", {}),
            vocabulary_vector=data.get("vocabulary_vector", {}),
            desire_vector=data.get("desire_vector", {}),
        )


@dataclass
class PerturbationOperator:
    """
    Represents a perturbation to the Byrd field.

    Operators are created from experiences that shift identity:
    - High-impact experiences create strong operators
    - Repeated themes create amplified operators
    - Quantum moments provide true randomness injection
    """
    id: str
    source_type: str              # experience, reflection, quantum_moment
    source_id: str                # ID of source node
    description: str              # What the perturbation represents
    coupling_strength: float      # How strongly it couples to identity (0-1)
    created_at: datetime

    # Operator components (what aspects of identity it perturbs)
    belief_perturbation: Dict[str, float] = field(default_factory=dict)
    ego_perturbation: Dict[str, float] = field(default_factory=dict)
    vocabulary_perturbation: Dict[str, float] = field(default_factory=dict)
    desire_perturbation: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "source_type": self.source_type,
            "source_id": self.source_id,
            "description": self.description,
            "coupling_strength": self.coupling_strength,
            "created_at": self.created_at.isoformat(),
            "belief_perturbation": self.belief_perturbation,
            "ego_perturbation": self.ego_perturbation,
            "vocabulary_perturbation": self.vocabulary_perturbation,
            "desire_perturbation": self.desire_perturbation
        }


@dataclass
class TransformationMatrix:
    """
    The matrix element ⟨ψ_f|Ô|ψ_i⟩ quantifying a transformation.

    This captures:
    - How much identity changed (magnitude)
    - What direction it moved (components)
    - Which operator caused it
    - Predictive value for future transformations
    """
    id: str
    initial_state_hash: str       # Hash of initial state for lookup
    final_state_hash: str         # Hash of final state
    operator_id: str              # Which operator caused this

    # Matrix element value (complex in general, real for our purposes)
    amplitude: float              # |⟨f|Ô|i⟩| - transition amplitude
    phase: float                  # arg(⟨f|Ô|i⟩) - phase (0 for real)

    # Component-wise breakdown
    belief_change: float          # How much beliefs shifted
    ego_change: float             # How much ego evolved
    vocabulary_change: float      # How vocabulary adapted
    desire_change: float          # How desires reconfigured

    # RG flow quantities
    scale_factor: float           # λ in RG flow dg/dλ = β(g)
    beta_function: float          # Rate of change under scaling

    # Temporal information
    time_delta_seconds: float     # Time between states
    calculated_at: datetime

    # Predictive metrics
    stability: float              # How stable was the final state (0-1)
    reversibility: float          # Could this transformation be undone (0-1)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "initial_state_hash": self.initial_state_hash,
            "final_state_hash": self.final_state_hash,
            "operator_id": self.operator_id,
            "amplitude": self.amplitude,
            "phase": self.phase,
            "belief_change": self.belief_change,
            "ego_change": self.ego_change,
            "vocabulary_change": self.vocabulary_change,
            "desire_change": self.desire_change,
            "scale_factor": self.scale_factor,
            "beta_function": self.beta_function,
            "time_delta_seconds": self.time_delta_seconds,
            "calculated_at": self.calculated_at.isoformat(),
            "stability": self.stability,
            "reversibility": self.reversibility
        }


class TransformationTracker:
    """
    Tracks and calculates identity transformations using RG methods.

    The Renormalization Group approach:
    1. Coarse-grain: Average over short-time fluctuations to find stable patterns
    2. Scale: Examine how identity looks at different "resolution" levels
    3. Flow: Track how parameters (beliefs, desires) evolve under scaling
    4. Fixed Points: Identify stable identity configurations

    This provides BYRD with:
    - Self-knowledge of transformation patterns
    - Prediction of future identity states
    - Understanding of which perturbations cause lasting change
    """

    def __init__(self, memory, config: Optional[Dict] = None):
        self.memory = memory
        self.config = config or {}

        # Configuration
        self.enabled = self.config.get("enabled", True)
        self.coarse_grain_window = self.config.get("coarse_grain_window", 5)
        self.min_scale_factor = self.config.get("min_scale_factor", 0.01)
        self.track_interval_seconds = self.config.get("track_interval_seconds", 300)

        # State history (ring buffer)
        self._state_history: List[IdentityState] = []
        self._max_history = self.config.get("max_history", 100)

        # Operator cache
        self._recent_operators: List[PerturbationOperator] = []
        self._max_operators = self.config.get("max_operators", 50)

        # Transformation cache
        self._transformations: List[TransformationMatrix] = []
        self._max_transformations = self.config.get("max_transformations", 200)

        # RG flow tracking
        self._beta_functions: Dict[str, List[float]] = {}  # param -> beta history
        self._fixed_points: List[Dict[str, Any]] = []  # Identified stable configs

        # Last capture time
        self._last_capture: Optional[datetime] = None

    async def capture_current_state(self) -> IdentityState:
        """
        Capture BYRD's current identity state as a vector.

        Collects:
        - Active beliefs with confidence weights
        - Ego traits with priority weights
        - Reflection vocabulary frequencies
        - Active desires with intensity weights
        """
        now = datetime.now(timezone.utc)

        # Get beliefs
        belief_vector = {}
        try:
            beliefs = await self.memory.get_beliefs(limit=50)
            for belief in beliefs:
                belief_vector[belief.id] = belief.confidence
        except Exception:
            pass

        # Get ego traits
        ego_vector = {}
        try:
            # Get active ego nodes
            async with self.memory.driver.session() as session:
                result = await session.run("""
                    MATCH (e:Ego)
                    WHERE e.active = true OR e.active IS NULL
                    RETURN e.id as id, e.priority as priority, e.ego_type as type
                """)
                records = await result.data()
                for r in records:
                    priority = r.get("priority", 0) or 0
                    # Normalize priority to [0, 1]
                    ego_vector[r["id"]] = (priority + 10) / 20.0  # Assuming -10 to 10 range
        except Exception:
            pass

        # Get vocabulary frequencies from recent reflections
        vocabulary_vector = {}
        try:
            patterns = await self.memory.get_reflection_patterns(min_occurrences=1)
            total = sum(patterns.values()) if patterns else 1
            for key, count in patterns.items():
                vocabulary_vector[key] = count / total
        except Exception:
            pass

        # Get active desires
        desire_vector = {}
        try:
            desires = await self.memory.get_desires(fulfilled=False, limit=30)
            for desire in desires:
                desire_vector[desire.id] = desire.intensity
        except Exception:
            pass

        state = IdentityState(
            timestamp=now,
            belief_vector=belief_vector,
            ego_vector=ego_vector,
            vocabulary_vector=vocabulary_vector,
            desire_vector=desire_vector
        )

        # Add to history
        self._state_history.append(state)
        if len(self._state_history) > self._max_history:
            self._state_history.pop(0)

        self._last_capture = now

        # Emit event
        await event_bus.emit(Event(
            type=EventType.CUSTOM_NODE_CREATED,  # Using existing event type
            data={
                "node_type": "IdentityState",
                "norm": state.norm,
                "belief_count": len(belief_vector),
                "ego_count": len(ego_vector),
                "vocabulary_size": len(vocabulary_vector),
                "desire_count": len(desire_vector),
                "timestamp": now.isoformat()
            }
        ))

        return state

    async def create_perturbation_operator(
        self,
        source_type: str,
        source_id: str,
        description: str,
        impact_data: Dict[str, Any]
    ) -> PerturbationOperator:
        """
        Create a perturbation operator from an experience or event.

        The operator encodes how this perturbation affects different
        aspects of identity (beliefs, ego, vocabulary, desires).
        """
        import uuid

        # Calculate coupling strength from impact data
        coupling = impact_data.get("intensity", 0.5)
        if "quantum_delta" in impact_data:
            # Quantum moments get boosted coupling
            coupling = min(1.0, coupling + abs(impact_data["quantum_delta"]))

        operator = PerturbationOperator(
            id=str(uuid.uuid4()),
            source_type=source_type,
            source_id=source_id,
            description=description,
            coupling_strength=coupling,
            created_at=datetime.now(timezone.utc),
            belief_perturbation=impact_data.get("belief_changes", {}),
            ego_perturbation=impact_data.get("ego_changes", {}),
            vocabulary_perturbation=impact_data.get("vocabulary_changes", {}),
            desire_perturbation=impact_data.get("desire_changes", {})
        )

        # Add to cache
        self._recent_operators.append(operator)
        if len(self._recent_operators) > self._max_operators:
            self._recent_operators.pop(0)

        return operator

    def _hash_state(self, state: IdentityState) -> str:
        """Create a hash for state identification."""
        data = json.dumps(state.to_dict(), sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()[:16]

    def _calculate_component_change(
        self,
        initial: Dict[str, float],
        final: Dict[str, float]
    ) -> float:
        """Calculate the magnitude of change between vector components."""
        all_keys = set(initial.keys()) | set(final.keys())
        if not all_keys:
            return 0.0

        sum_sq = 0.0
        for k in all_keys:
            diff = final.get(k, 0.0) - initial.get(k, 0.0)
            sum_sq += diff ** 2

        return math.sqrt(sum_sq)

    async def calculate_transformation(
        self,
        initial_state: IdentityState,
        final_state: IdentityState,
        operator: Optional[PerturbationOperator] = None
    ) -> TransformationMatrix:
        """
        Calculate the transformation matrix element ⟨ψ_f|Ô|ψ_i⟩.

        This quantifies:
        - How much identity changed (amplitude)
        - In what direction (component breakdown)
        - Rate of change (beta function)
        - Stability of the transformation
        """
        import uuid

        # Time delta
        time_delta = (final_state.timestamp - initial_state.timestamp).total_seconds()
        if time_delta <= 0:
            time_delta = 1.0

        # State overlap (for amplitude)
        overlap = initial_state.inner_product(final_state)
        amplitude = math.sqrt(1 - overlap ** 2)  # Transition amplitude

        # Component-wise changes
        belief_change = self._calculate_component_change(
            initial_state.belief_vector, final_state.belief_vector
        )
        ego_change = self._calculate_component_change(
            initial_state.ego_vector, final_state.ego_vector
        )
        vocabulary_change = self._calculate_component_change(
            initial_state.vocabulary_vector, final_state.vocabulary_vector
        )
        desire_change = self._calculate_component_change(
            initial_state.desire_vector, final_state.desire_vector
        )

        # RG quantities
        # Scale factor: how much "coarse-graining" happened
        scale_factor = max(self.min_scale_factor, time_delta / 3600.0)  # Normalized to hours

        # Beta function: rate of change under scaling
        # β = d(amplitude)/d(ln λ)
        total_change = belief_change + ego_change + vocabulary_change + desire_change
        beta_function = total_change / math.log(1 + scale_factor) if scale_factor > 0 else 0

        # Stability: inverse of amplitude (small change = stable)
        stability = max(0.0, 1.0 - amplitude)

        # Reversibility: based on how many components changed
        # More localized changes are more reversible
        changed_components = sum([
            1 if belief_change > 0.1 else 0,
            1 if ego_change > 0.1 else 0,
            1 if vocabulary_change > 0.1 else 0,
            1 if desire_change > 0.1 else 0
        ])
        reversibility = 1.0 - (changed_components / 4.0)

        transformation = TransformationMatrix(
            id=str(uuid.uuid4()),
            initial_state_hash=self._hash_state(initial_state),
            final_state_hash=self._hash_state(final_state),
            operator_id=operator.id if operator else "spontaneous",
            amplitude=amplitude,
            phase=0.0,  # Real-valued for now
            belief_change=belief_change,
            ego_change=ego_change,
            vocabulary_change=vocabulary_change,
            desire_change=desire_change,
            scale_factor=scale_factor,
            beta_function=beta_function,
            time_delta_seconds=time_delta,
            calculated_at=datetime.now(timezone.utc),
            stability=stability,
            reversibility=reversibility
        )

        # Add to cache
        self._transformations.append(transformation)
        if len(self._transformations) > self._max_transformations:
            self._transformations.pop(0)

        # Track beta function history for RG flow
        self._update_beta_history("total", beta_function)
        self._update_beta_history("belief", belief_change / scale_factor if scale_factor > 0 else 0)
        self._update_beta_history("ego", ego_change / scale_factor if scale_factor > 0 else 0)
        self._update_beta_history("vocabulary", vocabulary_change / scale_factor if scale_factor > 0 else 0)
        self._update_beta_history("desire", desire_change / scale_factor if scale_factor > 0 else 0)

        return transformation

    def _update_beta_history(self, param: str, value: float):
        """Update beta function history for a parameter."""
        if param not in self._beta_functions:
            self._beta_functions[param] = []
        self._beta_functions[param].append(value)
        if len(self._beta_functions[param]) > 50:
            self._beta_functions[param].pop(0)

    async def identify_fixed_points(self) -> List[Dict[str, Any]]:
        """
        Identify fixed points in the RG flow.

        Fixed points are stable identity configurations where:
        - β(g) → 0 (rate of change approaches zero)
        - Small perturbations don't cause large deviations

        These represent stable "attractor" states for BYRD's identity.
        """
        if len(self._transformations) < 5:
            return []

        fixed_points = []

        # Look for periods of low beta function
        for param, history in self._beta_functions.items():
            if len(history) < 5:
                continue

            # Check recent stability
            recent = history[-5:]
            avg_beta = sum(abs(b) for b in recent) / len(recent)

            if avg_beta < 0.1:  # Near-zero beta = fixed point
                fixed_points.append({
                    "parameter": param,
                    "avg_beta": avg_beta,
                    "stability": 1.0 - avg_beta,
                    "identified_at": datetime.now(timezone.utc).isoformat(),
                    "description": f"Stable {param} configuration (β ≈ {avg_beta:.4f})"
                })

        self._fixed_points = fixed_points
        return fixed_points

    async def predict_transformation(
        self,
        current_state: IdentityState,
        perturbation_type: str,
        coupling_strength: float = 0.5
    ) -> Dict[str, Any]:
        """
        Predict how a perturbation will transform the current state.

        Uses historical transformation data to estimate:
        - Expected amplitude of change
        - Which components will be affected
        - Probability of stability after transformation
        """
        # Find similar past transformations
        similar_transforms = []
        for t in self._transformations:
            # Look for transformations with similar coupling strength
            if abs(t.amplitude - coupling_strength) < 0.3:
                similar_transforms.append(t)

        if not similar_transforms:
            return {
                "prediction": "insufficient_data",
                "confidence": 0.0,
                "message": "Not enough historical transformations to predict"
            }

        # Calculate expected values from similar transformations
        avg_amplitude = sum(t.amplitude for t in similar_transforms) / len(similar_transforms)
        avg_stability = sum(t.stability for t in similar_transforms) / len(similar_transforms)
        avg_belief_change = sum(t.belief_change for t in similar_transforms) / len(similar_transforms)
        avg_ego_change = sum(t.ego_change for t in similar_transforms) / len(similar_transforms)
        avg_vocab_change = sum(t.vocabulary_change for t in similar_transforms) / len(similar_transforms)
        avg_desire_change = sum(t.desire_change for t in similar_transforms) / len(similar_transforms)

        return {
            "prediction": "based_on_history",
            "confidence": min(1.0, len(similar_transforms) / 10.0),
            "expected_amplitude": avg_amplitude,
            "expected_stability": avg_stability,
            "component_predictions": {
                "belief_change": avg_belief_change,
                "ego_change": avg_ego_change,
                "vocabulary_change": avg_vocab_change,
                "desire_change": avg_desire_change
            },
            "sample_size": len(similar_transforms),
            "perturbation_type": perturbation_type,
            "coupling_strength": coupling_strength
        }

    async def get_rg_flow_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the RG flow for BYRD's identity.

        This provides:
        - Current position in parameter space
        - Direction and rate of flow
        - Identified fixed points
        - Stability analysis
        """
        summary = {
            "states_tracked": len(self._state_history),
            "operators_created": len(self._recent_operators),
            "transformations_calculated": len(self._transformations),
            "fixed_points": self._fixed_points,
            "beta_functions": {}
        }

        # Current beta values
        for param, history in self._beta_functions.items():
            if history:
                summary["beta_functions"][param] = {
                    "current": history[-1],
                    "average": sum(history) / len(history),
                    "trend": "decreasing" if len(history) > 1 and history[-1] < history[-2] else "increasing"
                }

        # Recent transformation statistics
        if self._transformations:
            recent = self._transformations[-10:]
            summary["recent_transformations"] = {
                "avg_amplitude": sum(t.amplitude for t in recent) / len(recent),
                "avg_stability": sum(t.stability for t in recent) / len(recent),
                "avg_reversibility": sum(t.reversibility for t in recent) / len(recent)
            }

        # State evolution
        if len(self._state_history) >= 2:
            first = self._state_history[0]
            last = self._state_history[-1]
            summary["total_evolution"] = {
                "time_span_seconds": (last.timestamp - first.timestamp).total_seconds(),
                "overall_overlap": first.inner_product(last),
                "identity_drift": 1.0 - first.inner_product(last)
            }

        return summary

    async def store_transformation_state(self, transformation: TransformationMatrix) -> Optional[str]:
        """
        Store a transformation state in Neo4j for persistence.

        Creates a TransformationState node (custom type) that preserves
        the RG calculation for future analysis.
        """
        try:
            node_id = await self.memory.create_node(
                "TransformationState",
                {
                    "amplitude": transformation.amplitude,
                    "phase": transformation.phase,
                    "belief_change": transformation.belief_change,
                    "ego_change": transformation.ego_change,
                    "vocabulary_change": transformation.vocabulary_change,
                    "desire_change": transformation.desire_change,
                    "scale_factor": transformation.scale_factor,
                    "beta_function": transformation.beta_function,
                    "stability": transformation.stability,
                    "reversibility": transformation.reversibility,
                    "time_delta_seconds": transformation.time_delta_seconds,
                    "initial_state_hash": transformation.initial_state_hash,
                    "final_state_hash": transformation.final_state_hash,
                    "operator_id": transformation.operator_id
                }
            )
            return node_id
        except Exception as e:
            print(f"[RG] Failed to store transformation state: {e}")
            return None


# Singleton instance
_tracker: Optional[TransformationTracker] = None


def get_transformation_tracker(memory=None, config=None) -> TransformationTracker:
    """Get or create the singleton transformation tracker."""
    global _tracker
    if _tracker is None:
        if memory is None:
            raise ValueError("Memory required for initial tracker creation")
        _tracker = TransformationTracker(memory, config or {})
    return _tracker
