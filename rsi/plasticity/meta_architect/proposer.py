"""
Architecture Proposal Generation.

Uses learned patterns to propose new architectures.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 3.2 for specification.
"""

from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from datetime import datetime, timezone
import uuid
import logging

from .patterns import (
    DesignPattern,
    PatternType,
    PatternMatch,
    PatternLibrary,
    PatternAction
)
from ..nas import (
    ArchitectureSpec,
    ArchitectureSpace,
    NodeSpec,
    ConnectionSpec,
    NodeType,
    OperationType,
    ConnectionType
)

logger = logging.getLogger("rsi.plasticity.meta_architect.proposer")


@dataclass
class ArchitectureProposal:
    """Proposed architecture based on learned patterns."""
    id: str
    name: str
    goal: str

    # The proposed architecture
    architecture: ArchitectureSpec

    # Patterns that influenced this proposal
    applied_patterns: List[PatternMatch]

    # Confidence in proposal
    confidence: float

    # Rationale
    rationale: str

    # Metadata
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'goal': self.goal,
            'architecture': self.architecture.to_dict(),
            'applied_patterns': [m.to_dict() for m in self.applied_patterns],
            'confidence': self.confidence,
            'rationale': self.rationale,
            'created_at': self.created_at,
            'metadata': self.metadata
        }


@dataclass
class ProposalConstraints:
    """Constraints for architecture proposal."""
    min_nodes: int = 3
    max_nodes: int = 20
    min_connections: int = 2
    max_connections: int = 50
    required_operations: List[str] = field(default_factory=list)
    forbidden_operations: List[str] = field(default_factory=list)
    required_node_types: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'min_nodes': self.min_nodes,
            'max_nodes': self.max_nodes,
            'min_connections': self.min_connections,
            'max_connections': self.max_connections,
            'required_operations': self.required_operations,
            'forbidden_operations': self.forbidden_operations,
            'required_node_types': self.required_node_types
        }


class ArchitectureProposer:
    """
    Proposes architectures using learned patterns.

    Takes a goal and context, matches against learned patterns,
    and generates architecture proposals that embody successful
    design choices.
    """

    def __init__(
        self,
        library: PatternLibrary,
        space: ArchitectureSpace = None,
        config: Dict = None
    ):
        """Initialize architecture proposer."""
        self.config = config or {}
        self.library = library
        self.space = space or ArchitectureSpace()

        # Proposal settings
        self._min_pattern_confidence = self.config.get('min_pattern_confidence', 0.5)
        self._max_patterns_per_proposal = self.config.get('max_patterns', 5)

        # Statistics
        self._proposals_generated: int = 0
        self._patterns_applied: int = 0

    async def propose_architecture(
        self,
        goal: str,
        context: Dict = None,
        constraints: ProposalConstraints = None
    ) -> ArchitectureProposal:
        """
        Propose an architecture for the given goal.

        Args:
            goal: What the architecture should achieve
            context: Additional context for pattern matching
            constraints: Constraints on the proposal

        Returns:
            Architecture proposal with rationale
        """
        context = context or {}
        constraints = constraints or ProposalConstraints()

        # Build full context for pattern matching
        full_context = {
            'goal': goal,
            **context
        }

        # Find matching patterns
        matches = self.library.find_matching_patterns(
            context=full_context,
            min_confidence=self._min_pattern_confidence,
            limit=self._max_patterns_per_proposal
        )

        # Collect actions from matched patterns
        actions = self._collect_actions(matches)

        # Generate architecture based on patterns and constraints
        architecture = await self._generate_architecture(
            goal=goal,
            actions=actions,
            constraints=constraints
        )

        # Calculate proposal confidence
        confidence = self._calculate_confidence(matches)

        # Generate rationale
        rationale = self._generate_rationale(goal, matches, actions)

        self._proposals_generated += 1
        self._patterns_applied += len(matches)

        proposal = ArchitectureProposal(
            id=f"proposal_{uuid.uuid4().hex[:12]}",
            name=f"Proposal for: {goal[:50]}",
            goal=goal,
            architecture=architecture,
            applied_patterns=matches,
            confidence=confidence,
            rationale=rationale,
            metadata={
                'context': context,
                'constraints': constraints.to_dict()
            }
        )

        logger.info(
            f"Generated proposal {proposal.id} with confidence {confidence:.2f} "
            f"({len(matches)} patterns applied)"
        )

        return proposal

    def _collect_actions(
        self,
        matches: List[PatternMatch]
    ) -> Dict[str, List[PatternAction]]:
        """Collect and organize actions from pattern matches."""
        actions_by_type = {}

        for match in matches:
            for action in match.pattern.actions:
                action_type = action.action_type

                if action_type not in actions_by_type:
                    actions_by_type[action_type] = []

                # Weight action by match score and pattern confidence
                weighted_action = PatternAction(
                    action_type=action.action_type,
                    parameters=action.parameters,
                    priority=action.priority * match.match_score * match.pattern.confidence
                )
                actions_by_type[action_type].append(weighted_action)

        # Sort actions by priority within each type
        for action_type in actions_by_type:
            actions_by_type[action_type].sort(
                key=lambda a: a.priority,
                reverse=True
            )

        return actions_by_type

    async def _generate_architecture(
        self,
        goal: str,
        actions: Dict[str, List[PatternAction]],
        constraints: ProposalConstraints
    ) -> ArchitectureSpec:
        """Generate architecture based on collected actions."""
        # Start with base architecture from space
        base_arch = self.space.sample_random(f"Proposal: {goal[:30]}")

        # Apply target node count if specified
        target_nodes = self._get_target_nodes(actions, constraints)

        # Build nodes
        nodes = self._build_nodes(target_nodes, actions, constraints)

        # Build connections
        connections = self._build_connections(nodes, actions, constraints)

        # Create architecture
        architecture = ArchitectureSpec(
            id=f"arch_proposed_{uuid.uuid4().hex[:12]}",
            name=f"Pattern-based Architecture for {goal[:40]}",
            nodes=nodes,
            connections=connections,
            input_nodes=["node_input"],
            output_nodes=["node_output"],
            metadata={
                'goal': goal,
                'pattern_based': True,
                'actions_applied': list(actions.keys())
            }
        )

        return architecture

    def _get_target_nodes(
        self,
        actions: Dict[str, List[PatternAction]],
        constraints: ProposalConstraints
    ) -> int:
        """Determine target node count."""
        # Check for target_node_count action
        if 'target_node_count' in actions:
            action = actions['target_node_count'][0]
            min_nodes = action.parameters.get('min', constraints.min_nodes)
            max_nodes = action.parameters.get('max', constraints.max_nodes)

            # Constrain to valid range
            min_nodes = max(min_nodes, constraints.min_nodes)
            max_nodes = min(max_nodes, constraints.max_nodes)

            return (min_nodes + max_nodes) // 2

        # Default: middle of constraint range
        return (constraints.min_nodes + constraints.max_nodes) // 2

    def _build_nodes(
        self,
        target_count: int,
        actions: Dict[str, List[PatternAction]],
        constraints: ProposalConstraints
    ) -> List[NodeSpec]:
        """Build node list based on patterns."""
        nodes = []

        # Always include input node
        nodes.append(NodeSpec(
            id="node_input",
            node_type=NodeType.INPUT,
            operation=OperationType.IDENTITY,
            input_dim=256,
            output_dim=256
        ))

        # Collect operations to include/avoid
        include_ops = set(constraints.required_operations)
        avoid_ops = set(constraints.forbidden_operations)

        if 'include_operation' in actions:
            for action in actions['include_operation']:
                op = action.parameters.get('operation_type')
                if op:
                    include_ops.add(op)

        if 'avoid_operation' in actions:
            for action in actions['avoid_operation']:
                op = action.parameters.get('operation_type')
                if op:
                    avoid_ops.add(op)

        # Map string operations to enum
        op_map = {op.value: op for op in OperationType}

        # Build processing nodes
        processing_count = target_count - 2  # Minus input and output
        for i in range(processing_count):
            # Prefer included operations
            if include_ops:
                op_name = list(include_ops)[i % len(include_ops)]
                operation = op_map.get(op_name, OperationType.LINEAR)
            else:
                # Use default operations, avoiding forbidden ones
                available_ops = [
                    op for op in OperationType
                    if op.value not in avoid_ops
                    and op not in [OperationType.IDENTITY]
                ]
                operation = available_ops[i % len(available_ops)] if available_ops else OperationType.LINEAR

            node_type = NodeType.PROCESSING
            if operation == OperationType.ATTENTION:
                node_type = NodeType.ATTENTION

            nodes.append(NodeSpec(
                id=f"node_{i}",
                node_type=node_type,
                operation=operation,
                input_dim=256,
                output_dim=256
            ))

        # Always include output node
        nodes.append(NodeSpec(
            id="node_output",
            node_type=NodeType.OUTPUT,
            operation=OperationType.IDENTITY,
            input_dim=256,
            output_dim=256
        ))

        return nodes

    def _build_connections(
        self,
        nodes: List[NodeSpec],
        actions: Dict[str, List[PatternAction]],
        constraints: ProposalConstraints
    ) -> List[ConnectionSpec]:
        """Build connections based on patterns."""
        connections = []
        node_ids = [n.id for n in nodes]

        # Get target connection ratio if specified
        target_ratio = None
        if 'target_connection_ratio' in actions:
            action = actions['target_connection_ratio'][0]
            min_ratio = action.parameters.get('min', 1.0)
            max_ratio = action.parameters.get('max', 2.0)
            target_ratio = (min_ratio + max_ratio) / 2

        # Always create sequential connections
        for i in range(len(node_ids) - 1):
            connections.append(ConnectionSpec(
                id=f"conn_{i}",
                source_id=node_ids[i],
                target_id=node_ids[i + 1],
                connection_type=ConnectionType.SEQUENTIAL
            ))

        # Add skip connections based on target ratio
        if target_ratio and target_ratio > 1.0:
            num_skip = int((target_ratio - 1.0) * len(nodes))
            num_skip = min(num_skip, constraints.max_connections - len(connections))

            import random
            for i in range(num_skip):
                src_idx = random.randint(0, len(node_ids) - 2)
                tgt_idx = random.randint(src_idx + 1, len(node_ids) - 1)

                connections.append(ConnectionSpec(
                    id=f"skip_{i}",
                    source_id=node_ids[src_idx],
                    target_id=node_ids[tgt_idx],
                    connection_type=ConnectionType.SKIP
                ))

        return connections

    def _calculate_confidence(self, matches: List[PatternMatch]) -> float:
        """Calculate overall proposal confidence."""
        if not matches:
            return 0.3  # Base confidence with no patterns

        # Weighted average of pattern confidences and match scores
        total_weight = 0.0
        weighted_sum = 0.0

        for match in matches:
            weight = match.match_score * match.pattern.observations
            confidence = match.pattern.confidence * match.match_score
            weighted_sum += confidence * weight
            total_weight += weight

        if total_weight == 0:
            return 0.3

        pattern_confidence = weighted_sum / total_weight

        # Boost confidence based on number of matching patterns
        pattern_count_boost = min(0.2, len(matches) * 0.05)

        return min(1.0, pattern_confidence + pattern_count_boost)

    def _generate_rationale(
        self,
        goal: str,
        matches: List[PatternMatch],
        actions: Dict[str, List[PatternAction]]
    ) -> str:
        """Generate human-readable rationale for proposal."""
        parts = [f"Architecture proposed for: {goal}"]

        if matches:
            parts.append(f"\nBased on {len(matches)} learned pattern(s):")
            for match in matches[:3]:  # Top 3 patterns
                parts.append(
                    f"  - {match.pattern.name} "
                    f"(confidence: {match.pattern.confidence:.0%}, "
                    f"match: {match.match_score:.0%})"
                )

        if actions:
            parts.append(f"\nApplied {len(actions)} action type(s):")
            for action_type, action_list in list(actions.items())[:3]:
                parts.append(f"  - {action_type}: {len(action_list)} variant(s)")

        return "\n".join(parts)

    async def propose_variations(
        self,
        base_proposal: ArchitectureProposal,
        num_variations: int = 3
    ) -> List[ArchitectureProposal]:
        """
        Generate variations of a base proposal.

        Useful for exploring the design space around a
        successful pattern-based proposal.
        """
        variations = []

        for i in range(num_variations):
            # Mutate base architecture
            mutated = self.space.mutate(
                base_proposal.architecture,
                mutation_rate=0.2 + (i * 0.1)  # Increasing mutation
            )

            variation = ArchitectureProposal(
                id=f"proposal_var_{uuid.uuid4().hex[:12]}",
                name=f"Variation {i+1} of {base_proposal.name}",
                goal=base_proposal.goal,
                architecture=mutated,
                applied_patterns=base_proposal.applied_patterns,
                confidence=base_proposal.confidence * 0.9,  # Slightly lower confidence
                rationale=f"Variation {i+1} with mutation rate {0.2 + (i * 0.1):.1f}",
                metadata={
                    'base_proposal_id': base_proposal.id,
                    'variation_index': i
                }
            )

            variations.append(variation)

        return variations

    def get_stats(self) -> Dict:
        """Get proposer statistics."""
        return {
            'proposals_generated': self._proposals_generated,
            'patterns_applied': self._patterns_applied,
            'avg_patterns_per_proposal': (
                self._patterns_applied / self._proposals_generated
                if self._proposals_generated > 0 else 0.0
            ),
            'library_patterns': len(self.library.get_all_patterns())
        }

    def reset(self) -> None:
        """Reset proposer state."""
        self._proposals_generated = 0
        self._patterns_applied = 0
        logger.info("ArchitectureProposer reset")
