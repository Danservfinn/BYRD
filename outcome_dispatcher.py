"""
BYRD Outcome Dispatcher - Routes task outcomes to learning components.

Routes outcomes to learning components using ACTUAL interfaces.
v10: Now includes Graphiti for temporal knowledge graph enrichment.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from enum import Enum


class OutcomeType(Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILURE = "failure"
    TIMEOUT = "timeout"


@dataclass
class TaskOutcome:
    task_id: str
    outcome_type: OutcomeType
    strategy: str
    description: str
    execution_time_ms: int
    query_used: Optional[str] = None
    retrieved_node_ids: List[str] = field(default_factory=list)
    prediction_before: Optional[float] = None
    error_message: Optional[str] = None


class OutcomeDispatcher:
    """
    Routes outcomes to learning components using ACTUAL interfaces.

    v10: Now includes Graphiti for temporal knowledge graph enrichment.
    """

    def __init__(
        self,
        learned_retriever=None,
        intuition_network=None,
        desire_classifier=None,
        memory_tracker: Optional['MemoryTracker'] = None,
        goal_discoverer: Optional['GoalDiscoverer'] = None,
        learning_progress: Optional['LearningProgressTracker'] = None,
        graphiti_layer: Optional['GraphitiLayer'] = None
    ):
        self._retriever = learned_retriever
        self._intuition = intuition_network
        self._classifier = desire_classifier
        self._memory = memory_tracker
        self._goals = goal_discoverer
        self._progress = learning_progress
        self._graphiti = graphiti_layer

    async def dispatch(self, outcome: TaskOutcome) -> Dict[str, bool]:
        """Dispatch outcome to all components including Graphiti."""
        results = {}
        success = outcome.outcome_type == OutcomeType.SUCCESS

        # 1. Update learned retriever
        if self._retriever and outcome.query_used and outcome.retrieved_node_ids:
            for node_id in outcome.retrieved_node_ids:
                await self._retriever.record_feedback(
                    query=outcome.query_used,
                    node_id=node_id,
                    was_helpful=success
                )
            results['retriever'] = True

        # 2. Update intuition network
        if self._intuition:
            await self._intuition.record_outcome(
                situation=outcome.description,
                action=outcome.strategy,
                success=success
            )
            results['intuition'] = True

        # 3. Update desire classifier
        if self._classifier:
            self._classifier.record_feedback(
                desire={'description': outcome.description},
                actual_outcome=outcome.outcome_type.value,
                was_correct_routing=success
            )
            results['classifier'] = True

        # 4. Memory tracker
        if self._memory:
            results['memory'] = self._memory.record(outcome)

        # 5. Goal discoverer
        if self._goals:
            predicted = outcome.prediction_before if outcome.prediction_before is not None else 0.5
            actual = 1.0 if success else 0.0
            results['goals'] = self._goals.process_prediction_error(
                category=outcome.strategy,
                predicted=predicted,
                actual=actual,
                was_success=success
            )

        # 6. Learning progress
        if self._progress:
            results['progress'] = self._progress.record(outcome)

        # 7. Graphiti temporal knowledge graph
        if self._graphiti:
            # Build rich content for entity extraction
            outcome_content = self._build_graphiti_content(outcome, success)

            # Queue for async extraction (non-blocking)
            queued = await self._graphiti.queue_episode(
                content=outcome_content,
                source_type="task_outcome",
                source_id=outcome.task_id,
                metadata={
                    "strategy": outcome.strategy,
                    "success": success,
                    "execution_time_ms": outcome.execution_time_ms
                }
            )
            results['graphiti'] = queued

        return results

    def _build_graphiti_content(self, outcome: TaskOutcome, success: bool) -> str:
        """Build rich content for Graphiti entity extraction."""
        status = "succeeded" if success else "failed"

        content = f"Strategy '{outcome.strategy}' {status}: {outcome.description}"

        if outcome.query_used:
            content += f"\nQuery: {outcome.query_used}"

        if outcome.error_message:
            content += f"\nError: {outcome.error_message}"

        return content
