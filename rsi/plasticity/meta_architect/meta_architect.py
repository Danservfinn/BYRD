"""
MetaArchitect - Learns to Design Better Architectures.

The recursive improvement of improvement - Level 4 plasticity.

See docs/IMPLEMENTATION_PLAN_ASI.md Section 3.2 for specification.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timezone
import logging

from .patterns import (
    DesignPattern,
    PatternType,
    PatternLibrary
)
from .learner import (
    PatternLearner,
    ArchitectureOutcome
)
from .proposer import (
    ArchitectureProposer,
    ArchitectureProposal,
    ProposalConstraints
)
from ..nas import (
    ArchitectureSpec,
    ArchitectureSpace,
    ArchitectureScore,
    NeuralArchitectureSearch
)

logger = logging.getLogger("rsi.plasticity.meta_architect")


@dataclass
class Outcome:
    """Generic outcome for pattern learning."""
    success: bool
    score: float
    metrics: Dict[str, float] = field(default_factory=dict)
    context: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'success': self.success,
            'score': self.score,
            'metrics': self.metrics,
            'context': self.context
        }


@dataclass
class MetaArchitectState:
    """State of the MetaArchitect."""
    patterns_learned: int = 0
    proposals_generated: int = 0
    outcomes_processed: int = 0
    improvement_cycles: int = 0
    current_level: int = 4  # Level 4 plasticity = MetaArchitect
    active: bool = True

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'patterns_learned': self.patterns_learned,
            'proposals_generated': self.proposals_generated,
            'outcomes_processed': self.outcomes_processed,
            'improvement_cycles': self.improvement_cycles,
            'current_level': self.current_level,
            'active': self.active
        }


class MetaArchitect:
    """
    Learns design patterns from architectural outcomes.
    Uses patterns to propose better architectures.

    This is the recursive improvement of improvement - the component
    that learns how to design better architectures by observing
    which architectural choices lead to successful outcomes.
    """

    def __init__(
        self,
        nas: NeuralArchitectureSearch = None,
        config: Dict = None
    ):
        """
        Initialize MetaArchitect.

        Args:
            nas: NeuralArchitectureSearch instance (optional)
            config: Configuration options
        """
        self.config = config or {}

        # Initialize components
        self.library = PatternLibrary(self.config.get('library', {}))
        self.learner = PatternLearner(
            library=self.library,
            config=self.config.get('learner', {})
        )
        self.space = ArchitectureSpace(config=self.config.get('space', {}))
        self.proposer = ArchitectureProposer(
            library=self.library,
            space=self.space,
            config=self.config.get('proposer', {})
        )

        # NAS integration
        self.nas = nas or NeuralArchitectureSearch(
            space=self.space,
            config=self.config.get('nas', {})
        )

        # State tracking
        self._state = MetaArchitectState()

        # Performance tracking
        self._proposal_outcomes: Dict[str, Outcome] = {}

        logger.info("MetaArchitect initialized")

    async def learn_from_outcome(
        self,
        architecture: ArchitectureSpec,
        outcome: Outcome
    ) -> List[DesignPattern]:
        """
        Extract patterns from architecture outcome.

        This is the core learning method - it observes which
        architectural decisions led to success or failure
        and extracts reusable patterns.

        Args:
            architecture: The evaluated architecture
            outcome: The evaluation outcome

        Returns:
            List of newly learned patterns
        """
        # Build architecture data for learner
        architecture_data = {
            'node_count': architecture.node_count,
            'connection_count': architecture.connection_count,
            'node_types': [n.node_type.value for n in architecture.nodes],
            'operation_types': [n.operation.value for n in architecture.nodes],
            'connection_types': [c.connection_type.value for c in architecture.connections],
            'context': outcome.context,
            'metadata': architecture.metadata
        }

        # Determine success threshold
        success_threshold = self.config.get('success_threshold', 0.7)
        success = outcome.success if outcome.success is not None else outcome.score >= success_threshold

        # Learn from outcome
        new_patterns = await self.learner.learn_from_outcome(
            architecture_id=architecture.id,
            goal=outcome.context.get('goal', 'unknown'),
            success=success,
            score=outcome.score,
            architecture_data=architecture_data
        )

        self._state.outcomes_processed += 1
        self._state.patterns_learned += len(new_patterns)

        if new_patterns:
            logger.info(
                f"MetaArchitect learned {len(new_patterns)} patterns from "
                f"architecture {architecture.id} (score={outcome.score:.2f})"
            )

        return new_patterns

    async def propose_architecture(
        self,
        goal: str,
        context: Dict = None
    ) -> ArchitectureProposal:
        """
        Propose architecture using learned patterns.

        This is the recursive improvement of improvement - using
        patterns learned from past architectures to design
        better future architectures.

        Args:
            goal: What the architecture should achieve
            context: Additional context

        Returns:
            Architecture proposal with rationale
        """
        context = context or {}

        # Build constraints if provided
        constraints = None
        if 'constraints' in context:
            constraints = ProposalConstraints(**context['constraints'])

        # Generate proposal using learned patterns
        proposal = await self.proposer.propose_architecture(
            goal=goal,
            context=context,
            constraints=constraints
        )

        self._state.proposals_generated += 1

        logger.info(
            f"MetaArchitect proposed architecture {proposal.id} "
            f"for goal '{goal[:50]}' (confidence={proposal.confidence:.2f})"
        )

        return proposal

    async def improve_proposal(
        self,
        proposal: ArchitectureProposal,
        feedback: Outcome
    ) -> ArchitectureProposal:
        """
        Improve a proposal based on feedback.

        Learns from the feedback and generates an improved proposal.

        Args:
            proposal: Original proposal
            feedback: Feedback on the proposal

        Returns:
            Improved proposal
        """
        # Learn from feedback
        await self.learn_from_outcome(
            architecture=proposal.architecture,
            outcome=feedback
        )

        # Track proposal outcome
        self._proposal_outcomes[proposal.id] = feedback

        # Generate improved proposal
        improved_context = {
            **proposal.metadata.get('context', {}),
            'previous_proposal_id': proposal.id,
            'previous_score': feedback.score,
            'improvement_iteration': proposal.metadata.get('improvement_iteration', 0) + 1
        }

        improved = await self.propose_architecture(
            goal=proposal.goal,
            context=improved_context
        )

        self._state.improvement_cycles += 1

        logger.info(
            f"MetaArchitect improved proposal {proposal.id} -> {improved.id} "
            f"(score improvement: {feedback.score:.2f} -> targeting higher)"
        )

        return improved

    async def search_with_patterns(
        self,
        goal: str,
        budget: Dict = None
    ) -> List[ArchitectureProposal]:
        """
        Search for architectures using patterns to guide the search.

        Combines NAS with learned patterns for smarter search.

        Args:
            goal: Search goal
            budget: Search budget constraints

        Returns:
            List of promising proposals
        """
        proposals = []

        # Generate initial proposal using patterns
        initial_proposal = await self.propose_architecture(goal=goal)
        proposals.append(initial_proposal)

        # Use NAS to explore variations
        from ..nas import SearchBudget
        search_budget = SearchBudget(
            max_evaluations=budget.get('max_evaluations', 20) if budget else 20,
            max_time_seconds=budget.get('max_time_seconds', 60.0) if budget else 60.0
        )

        # Run NAS search
        result = await self.nas.search(
            goal=goal,
            budget=search_budget
        )

        # Learn from all discovered architectures
        for discovered in result.all_discovered:
            outcome = Outcome(
                success=discovered.score.overall_score >= 0.7,
                score=discovered.score.overall_score,
                context={'goal': goal}
            )

            await self.learn_from_outcome(
                architecture=discovered.architecture,
                outcome=outcome
            )

        # Generate additional proposals using newly learned patterns
        if result.best_architecture:
            additional = await self.propose_architecture(
                goal=goal,
                context={'informed_by_search': True}
            )
            proposals.append(additional)

        return proposals

    def get_learned_patterns(self) -> List[DesignPattern]:
        """Return all learned design patterns."""
        return self.library.get_all_patterns()

    def get_patterns_by_type(
        self,
        pattern_type: PatternType
    ) -> List[DesignPattern]:
        """Get patterns of specific type."""
        return self.library.get_patterns_by_type(pattern_type)

    def get_strong_patterns(self) -> List[DesignPattern]:
        """Get patterns with high confidence."""
        from .patterns import PatternStrength
        return self.library.get_strong_patterns(PatternStrength.MODERATE)

    def get_pattern_insights(self) -> Dict:
        """Get insights about learned patterns."""
        return self.learner.get_learning_insights()

    def get_state(self) -> MetaArchitectState:
        """Get current MetaArchitect state."""
        return self._state

    def get_stats(self) -> Dict:
        """Get comprehensive statistics."""
        return {
            'state': self._state.to_dict(),
            'library': self.library.get_stats(),
            'learner': self.learner.get_stats(),
            'proposer': self.proposer.get_stats(),
            'space': self.space.get_stats(),
            'proposal_outcomes': len(self._proposal_outcomes),
            'avg_proposal_score': (
                sum(o.score for o in self._proposal_outcomes.values()) /
                len(self._proposal_outcomes)
                if self._proposal_outcomes else 0.0
            )
        }

    def reset(self) -> None:
        """Reset MetaArchitect state."""
        self.library.reset()
        self.learner.reset()
        self.proposer.reset()
        self.space.reset()
        self._state = MetaArchitectState()
        self._proposal_outcomes.clear()
        logger.info("MetaArchitect reset")
