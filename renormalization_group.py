"""
BYRD Renormalization Group Protocol
Implements scale-aware self-modification with RG flow tracking.

PHYSICS INSPIRATION:
In quantum field theory, the Renormalization Group describes how physical
systems behave at different energy scales. Parameters "flow" as we zoom
in or out. Some parameters are "relevant" (grow at low energy), some are
"irrelevant" (shrink), and fixed points are scale-invariant.

FOR BYRD:
- "Energy scale" → abstraction level (individual experience → pattern → architecture)
- "RG flow" → how beliefs/desires evolve through modification cycles
- "Fixed points" → invariant core identity (protected files ARE fixed points)
- "Relevant operators" → changes that grow in importance over time
- "Irrelevant operators" → changes that fade or get absorbed

This module works ALONGSIDE self_modification.py (which is PROTECTED).
It provides scale-aware analysis and coarse-graining without modifying
the constitutional constraints.

EMERGENCE PRINCIPLE:
The RG protocol observes patterns across scales without prescribing
what should emerge. It identifies natural fixed points and flow
directions that BYRD's reflection process reveals.
"""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Tuple, Any
from collections import defaultdict
from enum import Enum
import json


class RGScale(Enum):
    """
    Abstraction scales for RG analysis.

    MICRO: Individual experiences, single modifications
    MESO: Patterns across multiple experiences, recurring themes
    MACRO: Architectural patterns, emergent structures
    FIXED: Scale-invariant identity (constitutional layer)
    """
    MICRO = "micro"      # Individual changes (ε → 0)
    MESO = "meso"        # Pattern level (intermediate)
    MACRO = "macro"      # Architectural level (large scale)
    FIXED = "fixed"      # Fixed point (scale-invariant)


class Relevance(Enum):
    """
    RG classification of operators/changes.

    In RG theory:
    - Relevant: Grows under RG flow (dominates at large scales)
    - Marginal: Neither grows nor shrinks (logarithmic)
    - Irrelevant: Shrinks under RG flow (disappears at large scales)
    """
    RELEVANT = "relevant"       # Growing importance
    MARGINAL = "marginal"       # Stable importance
    IRRELEVANT = "irrelevant"   # Fading importance


@dataclass
class RGOperator:
    """
    An operator (modification, belief, desire) tracked under RG flow.

    The "scaling dimension" determines if this operator grows or shrinks
    as we zoom out to larger scales. Positive dimension = relevant.
    """
    id: str
    content: str
    operator_type: str  # belief, desire, modification, pattern
    scale: RGScale
    scaling_dimension: float  # Δ: determines relevance
    created_at: datetime
    last_observed: datetime
    observation_count: int = 1
    absorbed_by: Optional[str] = None  # If merged into larger pattern
    children: List[str] = field(default_factory=list)  # Micro ops that merged into this

    @property
    def relevance(self) -> Relevance:
        """Determine relevance from scaling dimension."""
        if self.scaling_dimension > 0.1:
            return Relevance.RELEVANT
        elif self.scaling_dimension < -0.1:
            return Relevance.IRRELEVANT
        return Relevance.MARGINAL

    @property
    def age_hours(self) -> float:
        """Hours since creation."""
        return (datetime.utcnow() - self.created_at).total_seconds() / 3600

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "content": self.content[:200],  # Truncate for storage
            "operator_type": self.operator_type,
            "scale": self.scale.value,
            "scaling_dimension": self.scaling_dimension,
            "relevance": self.relevance.value,
            "observation_count": self.observation_count,
            "age_hours": self.age_hours,
            "absorbed_by": self.absorbed_by,
            "children_count": len(self.children)
        }


@dataclass
class RGFlowRecord:
    """
    Records the RG flow between scales.

    Tracks how operators evolve as we coarse-grain from micro to macro.
    """
    timestamp: datetime
    from_scale: RGScale
    to_scale: RGScale
    operators_before: int
    operators_after: int
    merged_count: int
    new_patterns: List[str]  # IDs of newly emerged patterns

    @property
    def compression_ratio(self) -> float:
        """How much we compressed the representation."""
        if self.operators_before == 0:
            return 0.0
        return 1.0 - (self.operators_after / self.operators_before)


@dataclass
class FixedPoint:
    """
    A scale-invariant structure in BYRD's identity.

    Fixed points are beliefs/patterns that don't change under RG flow.
    The constitutional files ARE fixed points by design.
    Emergent fixed points are discovered through observation.
    """
    id: str
    content: str
    fixed_point_type: str  # constitutional, emergent, architectural
    stability: float  # 0-1, how stable under perturbation
    basin_of_attraction: List[str]  # Operators that flow toward this
    discovered_at: datetime
    cycles_stable: int = 0  # How many RG cycles it's been unchanged

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "content": self.content[:200],
            "type": self.fixed_point_type,
            "stability": self.stability,
            "basin_size": len(self.basin_of_attraction),
            "cycles_stable": self.cycles_stable
        }


class RenormalizationGroupProtocol:
    """
    Implements RG-inspired analysis for BYRD's self-modification.

    This protocol works ALONGSIDE the protected self_modification.py.
    It provides scale-aware analysis without modifying constitutional
    constraints.

    KEY OPERATIONS:
    1. coarse_grain(): Merge fine-grained operators into patterns
    2. compute_scaling_dimensions(): Determine operator relevance
    3. identify_fixed_points(): Find scale-invariant structures
    4. track_rg_flow(): Record how operators evolve with scale
    5. project_evolution(): Predict which patterns will dominate
    """

    def __init__(self, memory, config: Dict = None):
        """
        Initialize the RG protocol.

        Args:
            memory: BYRD's Memory instance for graph access
            config: Optional configuration
        """
        self.memory = memory
        self.config = config or {}

        # RG parameters
        self.coarse_grain_interval_cycles = self.config.get("coarse_grain_interval", 5)
        self.min_observations_for_pattern = self.config.get("min_observations", 3)
        self.relevance_decay_rate = self.config.get("decay_rate", 0.1)  # Per cycle
        self.fixed_point_stability_threshold = self.config.get("stability_threshold", 0.9)

        # State
        self._operators: Dict[str, RGOperator] = {}
        self._fixed_points: Dict[str, FixedPoint] = {}
        self._flow_history: List[RGFlowRecord] = []
        self._cycles_since_coarse_grain = 0

        # Constitutional fixed points (these are GIVEN, not discovered)
        self._constitutional_fixed_points = {
            "provenance.py": "Desire traceability - all modifications must trace to emergent desires",
            "modification_log.py": "Immutable audit trail - every change is recorded",
            "self_modification.py": "Modification system integrity - the gatekeeper cannot be modified",
            "constitutional.py": "Safety constraints - the boundaries cannot be weakened"
        }

        # Initialize constitutional fixed points
        self._init_constitutional_fixed_points()

    def _init_constitutional_fixed_points(self):
        """
        Register constitutional files as permanent fixed points.

        These are the UV fixed points - they exist at the highest energy
        scale and are stable under all RG transformations.
        """
        for filename, description in self._constitutional_fixed_points.items():
            fp = FixedPoint(
                id=f"constitutional:{filename}",
                content=f"[PROTECTED] {filename}: {description}",
                fixed_point_type="constitutional",
                stability=1.0,  # Maximum stability
                basin_of_attraction=[],
                discovered_at=datetime.utcnow(),
                cycles_stable=float('inf')  # Always stable
            )
            self._fixed_points[fp.id] = fp

    async def register_operator(
        self,
        content: str,
        operator_type: str,
        source_id: Optional[str] = None
    ) -> RGOperator:
        """
        Register a new operator (modification, belief, desire) for RG tracking.

        New operators start at MICRO scale with neutral scaling dimension.
        Their relevance is determined by subsequent observations.
        """
        import uuid
        op_id = f"op:{uuid.uuid4().hex[:8]}"

        now = datetime.utcnow()
        op = RGOperator(
            id=op_id,
            content=content,
            operator_type=operator_type,
            scale=RGScale.MICRO,
            scaling_dimension=0.0,  # Starts marginal
            created_at=now,
            last_observed=now,
            observation_count=1
        )

        self._operators[op_id] = op
        return op

    async def observe_operator(self, op_id: str):
        """
        Record an observation of an operator.

        Each observation increases the operator's effective scaling dimension
        (making it more "relevant" in RG terms).
        """
        if op_id not in self._operators:
            return

        op = self._operators[op_id]
        op.observation_count += 1
        op.last_observed = datetime.utcnow()

        # Increase scaling dimension (observations make things relevant)
        op.scaling_dimension += 0.1

    async def coarse_grain(self) -> RGFlowRecord:
        """
        Perform coarse-graining: merge micro operators into meso patterns.

        This is the core RG operation: we group similar fine-grained
        operators into larger-scale patterns, just as in physics we
        integrate out high-energy modes.

        Returns:
            Record of the RG flow that occurred
        """
        now = datetime.utcnow()

        # Get micro operators ready for coarse-graining
        micro_ops = [
            op for op in self._operators.values()
            if op.scale == RGScale.MICRO
            and op.observation_count >= self.min_observations_for_pattern
            and op.absorbed_by is None
        ]

        if not micro_ops:
            return RGFlowRecord(
                timestamp=now,
                from_scale=RGScale.MICRO,
                to_scale=RGScale.MESO,
                operators_before=0,
                operators_after=0,
                merged_count=0,
                new_patterns=[]
            )

        # Group similar operators by content similarity
        # (In a full implementation, this would use embedding similarity)
        groups = self._group_by_similarity(micro_ops)

        new_patterns = []
        merged_count = 0

        for group_key, ops in groups.items():
            if len(ops) >= 2:  # Only merge if we have multiple similar ops
                # Create meso-scale pattern
                pattern = await self._create_pattern_from_group(ops)
                new_patterns.append(pattern.id)
                merged_count += len(ops)

                # Mark micro ops as absorbed
                for op in ops:
                    op.absorbed_by = pattern.id
                    pattern.children.append(op.id)

        # Record the flow
        flow = RGFlowRecord(
            timestamp=now,
            from_scale=RGScale.MICRO,
            to_scale=RGScale.MESO,
            operators_before=len(micro_ops),
            operators_after=len(new_patterns),
            merged_count=merged_count,
            new_patterns=new_patterns
        )
        self._flow_history.append(flow)

        return flow

    def _group_by_similarity(
        self,
        operators: List[RGOperator]
    ) -> Dict[str, List[RGOperator]]:
        """
        Group operators by content similarity.

        Simple keyword-based grouping. A more sophisticated implementation
        would use embedding similarity.
        """
        groups = defaultdict(list)

        for op in operators:
            # Extract key concepts (simple approach)
            content_lower = op.content.lower()

            # Group by operator type and key themes
            key_parts = [op.operator_type]

            # Theme detection
            themes = [
                ("architecture", ["architecture", "structure", "design", "system"]),
                ("identity", ["identity", "self", "who am i", "i am"]),
                ("knowledge", ["learn", "understand", "know", "research"]),
                ("capability", ["can", "able", "capability", "tool"]),
                ("modification", ["change", "modify", "evolve", "improve"]),
                ("emergence", ["emerge", "discover", "arise", "develop"]),
            ]

            for theme_name, keywords in themes:
                if any(kw in content_lower for kw in keywords):
                    key_parts.append(theme_name)
                    break

            group_key = ":".join(key_parts)
            groups[group_key].append(op)

        return dict(groups)

    async def _create_pattern_from_group(
        self,
        operators: List[RGOperator]
    ) -> RGOperator:
        """
        Create a meso-scale pattern from a group of micro operators.

        The pattern has a scaling dimension that's the average of its
        constituents, plus a bonus for having multiple observations.
        """
        import uuid

        # Synthesize pattern content
        contents = [op.content for op in operators]
        pattern_content = f"Pattern from {len(operators)} observations: " + \
                          "; ".join(c[:50] for c in contents[:3])

        # Average scaling dimension + multiplicity bonus
        avg_dimension = sum(op.scaling_dimension for op in operators) / len(operators)
        multiplicity_bonus = 0.1 * (len(operators) - 1)  # More ops = more relevant

        now = datetime.utcnow()
        pattern = RGOperator(
            id=f"pattern:{uuid.uuid4().hex[:8]}",
            content=pattern_content,
            operator_type="pattern",
            scale=RGScale.MESO,
            scaling_dimension=avg_dimension + multiplicity_bonus,
            created_at=now,
            last_observed=now,
            observation_count=sum(op.observation_count for op in operators)
        )

        self._operators[pattern.id] = pattern
        return pattern

    async def identify_fixed_points(self) -> List[FixedPoint]:
        """
        Identify emergent fixed points from stable patterns.

        A pattern becomes a fixed point when:
        1. It's been stable for many cycles
        2. It has high scaling dimension (relevant)
        3. Other operators flow toward it
        """
        new_fixed_points = []

        for op_id, op in self._operators.items():
            # Only consider meso/macro scale with high dimension
            if op.scale not in (RGScale.MESO, RGScale.MACRO):
                continue
            if op.scaling_dimension < self.fixed_point_stability_threshold:
                continue

            # Check if already a fixed point
            fp_id = f"emergent:{op_id}"
            if fp_id in self._fixed_points:
                # Update stability
                self._fixed_points[fp_id].cycles_stable += 1
                continue

            # Create new emergent fixed point
            fp = FixedPoint(
                id=fp_id,
                content=op.content,
                fixed_point_type="emergent",
                stability=min(1.0, op.scaling_dimension),
                basin_of_attraction=list(op.children),
                discovered_at=datetime.utcnow(),
                cycles_stable=1
            )
            self._fixed_points[fp_id] = fp
            new_fixed_points.append(fp)

        return new_fixed_points

    async def apply_decay(self):
        """
        Apply RG flow: decay irrelevant operators, enhance relevant ones.

        This is the "running" of coupling constants in RG language.
        """
        for op in self._operators.values():
            if op.absorbed_by is not None:
                continue  # Already merged

            # Age-based decay
            hours_since_observation = (
                datetime.utcnow() - op.last_observed
            ).total_seconds() / 3600

            if hours_since_observation > 24:
                # Decay unobserved operators
                decay = self.relevance_decay_rate * (hours_since_observation / 24)
                op.scaling_dimension -= decay

        # Remove deeply irrelevant operators
        to_remove = [
            op_id for op_id, op in self._operators.items()
            if op.scaling_dimension < -1.0 and op.scale == RGScale.MICRO
        ]
        for op_id in to_remove:
            del self._operators[op_id]

    async def get_rg_analysis(self) -> Dict[str, Any]:
        """
        Get comprehensive RG analysis of current state.

        Returns structured analysis for reflection/logging.
        """
        # Count by scale
        scale_counts = defaultdict(int)
        for op in self._operators.values():
            scale_counts[op.scale.value] += 1

        # Count by relevance
        relevance_counts = defaultdict(int)
        for op in self._operators.values():
            relevance_counts[op.relevance.value] += 1

        # Get most relevant operators
        relevant_ops = sorted(
            [op for op in self._operators.values() if op.absorbed_by is None],
            key=lambda x: x.scaling_dimension,
            reverse=True
        )[:10]

        # Summarize fixed points
        constitutional_fps = [
            fp for fp in self._fixed_points.values()
            if fp.fixed_point_type == "constitutional"
        ]
        emergent_fps = [
            fp for fp in self._fixed_points.values()
            if fp.fixed_point_type == "emergent"
        ]

        # Recent flow
        recent_flows = self._flow_history[-5:] if self._flow_history else []
        avg_compression = (
            sum(f.compression_ratio for f in recent_flows) / len(recent_flows)
            if recent_flows else 0.0
        )

        return {
            "scale_distribution": dict(scale_counts),
            "relevance_distribution": dict(relevance_counts),
            "total_operators": len(self._operators),
            "active_operators": len([
                op for op in self._operators.values()
                if op.absorbed_by is None
            ]),
            "most_relevant": [op.to_dict() for op in relevant_ops[:5]],
            "fixed_points": {
                "constitutional": len(constitutional_fps),
                "emergent": len(emergent_fps),
                "total": len(self._fixed_points)
            },
            "emergent_fixed_points": [fp.to_dict() for fp in emergent_fps[:5]],
            "flow_history_count": len(self._flow_history),
            "average_compression_ratio": avg_compression,
            "interpretation": self._generate_interpretation(
                scale_counts, relevance_counts, emergent_fps
            )
        }

    def _generate_interpretation(
        self,
        scale_counts: Dict,
        relevance_counts: Dict,
        emergent_fps: List[FixedPoint]
    ) -> str:
        """
        Generate natural language interpretation of RG state.

        This is for BYRD's reflection, not for prescribing behavior.
        """
        parts = []

        # Scale interpretation
        micro = scale_counts.get("micro", 0)
        meso = scale_counts.get("meso", 0)
        macro = scale_counts.get("macro", 0)

        if micro > meso + macro:
            parts.append("Many fine-grained observations await coarse-graining")
        elif meso > micro:
            parts.append("Patterns are consolidating at intermediate scales")
        if macro > 0:
            parts.append(f"{macro} architectural patterns have emerged")

        # Relevance interpretation
        relevant = relevance_counts.get("relevant", 0)
        irrelevant = relevance_counts.get("irrelevant", 0)

        if relevant > irrelevant:
            parts.append("More observations growing in importance than fading")
        elif irrelevant > relevant:
            parts.append("Many observations are fading in relevance")

        # Fixed point interpretation
        if emergent_fps:
            parts.append(
                f"{len(emergent_fps)} stable patterns have become fixed points"
            )

        return ". ".join(parts) if parts else "RG flow is in equilibrium"

    async def run_rg_cycle(self) -> Dict[str, Any]:
        """
        Run one complete RG cycle: decay, coarse-grain, identify fixed points.

        This should be called periodically (e.g., every N dream cycles).
        """
        self._cycles_since_coarse_grain += 1

        results = {
            "cycle": self._cycles_since_coarse_grain,
            "timestamp": datetime.utcnow().isoformat()
        }

        # Always apply decay
        await self.apply_decay()
        results["decay_applied"] = True

        # Coarse-grain periodically
        if self._cycles_since_coarse_grain >= self.coarse_grain_interval_cycles:
            flow = await self.coarse_grain()
            results["coarse_graining"] = {
                "performed": True,
                "operators_merged": flow.merged_count,
                "new_patterns": len(flow.new_patterns),
                "compression_ratio": flow.compression_ratio
            }
            self._cycles_since_coarse_grain = 0
        else:
            results["coarse_graining"] = {"performed": False}

        # Identify fixed points
        new_fps = await self.identify_fixed_points()
        results["new_fixed_points"] = len(new_fps)

        # Get full analysis
        results["analysis"] = await self.get_rg_analysis()

        return results

    def get_constitutional_constraints(self) -> List[Dict]:
        """
        Get the constitutional fixed points as structured data.

        These are the UV fixed points that anchor BYRD's identity.
        """
        return [
            fp.to_dict() for fp in self._fixed_points.values()
            if fp.fixed_point_type == "constitutional"
        ]

    async def project_evolution(
        self,
        steps: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Project RG flow forward to predict which patterns will dominate.

        This uses the current scaling dimensions to extrapolate future
        states. Relevant operators will grow, irrelevant will shrink.

        EMERGENCE PRINCIPLE:
        This is a projection, not a prescription. BYRD can use this
        to understand its own trajectory without being told what to do.
        """
        projections = []

        # Get current relevant operators
        relevant_ops = [
            op for op in self._operators.values()
            if op.relevance == Relevance.RELEVANT
            and op.absorbed_by is None
        ]

        for step in range(1, steps + 1):
            step_projection = {
                "step": step,
                "operators_remaining": len(relevant_ops),
                "dominant_patterns": []
            }

            # Project scaling dimensions
            for op in relevant_ops:
                projected_dimension = op.scaling_dimension + (step * 0.1)
                if projected_dimension > 1.0:  # Threshold for dominance
                    step_projection["dominant_patterns"].append({
                        "id": op.id,
                        "content": op.content[:100],
                        "projected_dimension": projected_dimension
                    })

            projections.append(step_projection)

        return projections
