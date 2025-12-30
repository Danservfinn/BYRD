# BYRD Combined Implementation Plan v5

## Overview

This plan consolidates optimal components from three source documents, **revised to match actual BYRD interfaces** and **bug-fixed after critical review**.

**Total Scope: ~890 lines | Additional LLM Calls: 0**

---

## Bugs Fixed in v5

| Bug | Severity | Fix |
|-----|----------|-----|
| Missing `Dict` import | MEDIUM | Added `Dict` to typing imports in Part 4 |

## Bugs Fixed in v4

| Bug | Severity | Fix |
|-----|----------|-----|
| Decorator signature mismatch | HIGH | `_seek_knowledge`/`_seek_capability` call `_execute_with_tracking` directly (no decorator) |
| Missing `_strategy_stats` init | MEDIUM | Added to Seeker `__init__` additions |

## Bugs Fixed in v3

| Bug | Severity | Fix |
|-----|----------|-----|
| Prediction timing (post-update) | HIGH | Capture prediction in Seeker, pass through TaskOutcome |
| EMA logic inverted | MEDIUM | Failure bucket moves toward 1.0, not 0.0 |
| `_classify_base()` missing | HIGH | Provide full refactor instructions |
| Part 4/5 conflict | HIGH | Merged into single coherent method |
| Snapshot frequency breaks | MEDIUM | Track `_total_recorded` separately |
| `success_rate` never updates | HIGH | Add `update_goal_outcome()` method |
| Only 1/8 strategies shown | MEDIUM | Use decorator pattern |
| `get_byrd_instance()` missing | MEDIUM | Add singleton accessor |

---

## Actual Interface Summary

| Component | Key Methods |
|-----------|-------------|
| `learned_retriever` | `record_feedback(query, node_id, was_helpful)`, `get_learned_boost(query_type, result_type)` |
| `intuition_network` | `record_outcome(situation, action, success)`, `score_action(situation, action)`, `evaluate_prediction(situation, action, actual_success)` |
| `desire_classifier` | `classify(description)` → ClassificationResult, `record_feedback(desire, outcome, was_correct)` |
| `capability_evaluator` | `evaluate_capability(capability)` → EvaluationResult, `get_trend(capability)` |

---

## Part 1: OutcomeDispatcher (~95 lines)

Central hub using **actual** BYRD interfaces. **Fixed**: Uses pre-captured prediction instead of re-querying.

```python
# src/byrd/core/outcome_dispatcher.py

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from enum import Enum
from datetime import datetime

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
    prediction_before: Optional[float] = None  # FIX: Pre-captured prediction
    error_message: Optional[str] = None

class OutcomeDispatcher:
    """Routes outcomes to learning components using ACTUAL interfaces."""

    def __init__(
        self,
        learned_retriever=None,
        intuition_network=None,
        desire_classifier=None,
        memory_tracker: Optional['MemoryTracker'] = None,
        goal_discoverer: Optional['GoalDiscoverer'] = None,
        learning_progress: Optional['LearningProgressTracker'] = None
    ):
        self._retriever = learned_retriever
        self._intuition = intuition_network
        self._classifier = desire_classifier
        self._memory = memory_tracker
        self._goals = goal_discoverer
        self._progress = learning_progress

    async def dispatch(self, outcome: TaskOutcome) -> Dict[str, bool]:
        """Dispatch outcome to all components."""
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

        # 5. Goal discoverer - FIX: Use pre-captured prediction
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

        return results
```

---

## Part 2: DesireClassifier Learning Enhancement (~70 lines)

**Fixed**: Correct EMA logic, proper `_classify_base` handling.

```python
# Modifications to src/byrd/cognition/desire_classifier.py
#
# REFACTOR STEPS:
# 1. Rename existing classify() method to _classify_base()
# 2. Add the new attributes and methods below
# 3. Add new classify() method that wraps _classify_base()

from datetime import datetime
from typing import Dict

class DesireClassifier:
    def __init__(self, config: Dict = None):
        # Existing init...
        self._routing_stats = {dt: 0 for dt in DesireType}
        self._feedback_buffer = []

        # ADD: Learned routing adjustments
        # Structure: {handler: {'successes': count, 'failures': count, 'score': ema}}
        self._routing_adjustments: Dict[str, Dict[str, float]] = {}
        self._learning_rate = 0.1

    def record_feedback(self, desire: Dict, actual_outcome: str, was_correct_routing: bool):
        """Record feedback AND update routing adjustments."""
        self._feedback_buffer.append({
            'desire': desire,
            'outcome': actual_outcome,
            'correct': was_correct_routing,
            'timestamp': datetime.now().isoformat()
        })

        # Get the handler that was used (use base classification to avoid recursion)
        description = desire.get('description', '')
        result = self._classify_base(description)
        handler = result.handler

        # Initialize if needed
        if handler not in self._routing_adjustments:
            self._routing_adjustments[handler] = {
                'successes': 0,
                'failures': 0,
                'score': 0.5  # Neutral starting point
            }

        adj = self._routing_adjustments[handler]

        # FIX: Track counts and compute proper EMA
        if was_correct_routing:
            adj['successes'] += 1
        else:
            adj['failures'] += 1

        # Compute success rate and EMA update
        total = adj['successes'] + adj['failures']
        if total > 0:
            actual_rate = adj['successes'] / total
            adj['score'] = adj['score'] + self._learning_rate * (actual_rate - adj['score'])

    def _get_routing_boost(self, handler: str) -> float:
        """Get learned boost/penalty for a handler. Range: -0.5 to +0.5"""
        if handler not in self._routing_adjustments:
            return 0.0
        # Score is 0-1, center at 0.5 to get -0.5 to +0.5 range
        return self._routing_adjustments[handler]['score'] - 0.5

    def classify(self, desire_description: str) -> 'ClassificationResult':
        """Classify with learned adjustments applied."""
        # Get base classification (existing logic, now renamed)
        base_result = self._classify_base(desire_description)

        # Apply learned adjustment to confidence (scale by 0.3 to limit impact)
        boost = self._get_routing_boost(base_result.handler)
        adjusted_confidence = max(0.0, min(1.0, base_result.confidence + boost * 0.3))

        return ClassificationResult(
            desire_type=base_result.desire_type,
            confidence=adjusted_confidence,
            handler=base_result.handler,
            keywords_matched=base_result.keywords_matched,
            reason=base_result.reason + (f" [boost: {boost:+.2f}]" if boost != 0 else "")
        )

    # NOTE: The existing classify() method should be renamed to _classify_base()
    # It contains the keyword matching logic and returns ClassificationResult
```

---

## Part 3: Memory Tracker (~40 lines)

Self-contained, no changes from v2.

```python
# src/byrd/core/memory_tracker.py

from dataclasses import dataclass
from typing import Dict, List, Any
from datetime import datetime
import json

@dataclass
class LearningEvent:
    timestamp: datetime
    component: str
    event_type: str
    details: Dict[str, Any]

class MemoryTracker:
    """Tracks learning events across all components."""

    def __init__(self, max_events: int = 10000):
        self._events: List[LearningEvent] = []
        self._max_events = max_events
        self._component_stats: Dict[str, Dict[str, int]] = {}

    def record(self, outcome: 'TaskOutcome') -> bool:
        event = LearningEvent(
            timestamp=datetime.now(),
            component="outcome_dispatcher",
            event_type=outcome.outcome_type.value,
            details={
                'task_id': outcome.task_id,
                'strategy': outcome.strategy,
                'execution_time': outcome.execution_time_ms
            }
        )
        self._events.append(event)
        self._update_stats(event)
        self._trim_if_needed()
        return True

    def _update_stats(self, event: LearningEvent):
        if event.component not in self._component_stats:
            self._component_stats[event.component] = {}
        stats = self._component_stats[event.component]
        stats[event.event_type] = stats.get(event.event_type, 0) + 1

    def _trim_if_needed(self):
        if len(self._events) > self._max_events:
            self._events = self._events[-self._max_events:]

    def get_stats(self) -> Dict[str, Any]:
        return {
            'total_events': len(self._events),
            'by_component': self._component_stats,
            'oldest_event': self._events[0].timestamp.isoformat() if self._events else None,
            'newest_event': self._events[-1].timestamp.isoformat() if self._events else None
        }

    def export(self, limit: int = 1000) -> str:
        return json.dumps([{
            'timestamp': e.timestamp.isoformat(),
            'component': e.component,
            'type': e.event_type,
            'details': e.details
        } for e in self._events[-limit:]])
```

---

## Part 4: Seeker Integration with Strategy Tracking (~120 lines)

**Fixed**: Merged Part 4 + Part 5, includes prediction capture, uses decorator pattern for all strategies.

```python
# Modifications to src/byrd/cognition/seeker.py

import time
import random
from typing import Optional, List, Callable, Any, Dict
from functools import wraps

# Import at module level (not inside functions)
from core.outcome_dispatcher import OutcomeDispatcher, TaskOutcome, OutcomeType

def track_strategy(strategy_name: str):
    """Decorator to add outcome tracking to any strategy method."""
    def decorator(fn: Callable):
        @wraps(fn)
        async def wrapper(self, description: str, desire_id: str = None, **kwargs) -> bool:
            return await self._execute_with_tracking(
                strategy=strategy_name,
                description=description,
                execute_fn=lambda: fn(self, description, desire_id, **kwargs),
                desire_id=desire_id
            )
        return wrapper
    return decorator


class Seeker:
    def __init__(self, memory, llm_client, config, coordinator=None):
        # Existing init...

        # ADD: Learning integration
        self._dispatcher: Optional[OutcomeDispatcher] = None
        self._intuition_network = None  # Injected later
        self._current_task_id: Optional[str] = None

        # FIX v4: Initialize strategy stats dict (may already exist in Seeker)
        if not hasattr(self, '_strategy_stats'):
            self._strategy_stats: Dict[str, Dict[str, int]] = {}

    def set_dispatcher(self, dispatcher: OutcomeDispatcher):
        """Inject outcome dispatcher for learning."""
        self._dispatcher = dispatcher

    def set_intuition_network(self, network):
        """Inject intuition network for prediction capture."""
        self._intuition_network = network

    async def _execute_with_tracking(
        self,
        strategy: str,
        description: str,
        execute_fn: Callable,
        desire_id: str = None,
        query: str = None,
        retrieved_ids: List[str] = None
    ) -> bool:
        """Core tracking wrapper - captures prediction BEFORE execution."""
        self._current_task_id = f"seek_{int(time.time() * 1000)}_{random.randint(1000, 9999)}"
        start_time = time.time()

        # FIX: Capture prediction BEFORE execution
        prediction_before = None
        if self._intuition_network:
            try:
                intuition = await self._intuition_network.score_action(
                    situation=description,
                    action=strategy
                )
                prediction_before = intuition.score
            except Exception:
                prediction_before = 0.5

        try:
            # Execute the actual strategy
            result = await execute_fn()
            success = bool(result)

            # Update existing strategy stats
            if strategy not in self._strategy_stats:
                self._strategy_stats[strategy] = {'attempts': 0, 'successes': 0}
            self._strategy_stats[strategy]['attempts'] += 1
            if success:
                self._strategy_stats[strategy]['successes'] += 1

            # FIX: Validate prediction AFTER execution
            if self._intuition_network and prediction_before is not None:
                await self._intuition_network.evaluate_prediction(
                    situation=description,
                    action=strategy,
                    actual_success=success
                )

            # Dispatch to learning components with pre-captured prediction
            if self._dispatcher:
                outcome = TaskOutcome(
                    task_id=self._current_task_id,
                    outcome_type=OutcomeType.SUCCESS if success else OutcomeType.FAILURE,
                    strategy=strategy,
                    description=description,
                    query_used=query,
                    retrieved_node_ids=retrieved_ids or [],
                    execution_time_ms=int((time.time() - start_time) * 1000),
                    prediction_before=prediction_before  # FIX: Pass pre-captured prediction
                )
                await self._dispatcher.dispatch(outcome)

            return success

        except Exception as e:
            if self._dispatcher:
                outcome = TaskOutcome(
                    task_id=self._current_task_id,
                    outcome_type=OutcomeType.FAILURE,
                    strategy=strategy,
                    description=description,
                    query_used=query,
                    retrieved_node_ids=retrieved_ids or [],
                    execution_time_ms=int((time.time() - start_time) * 1000),
                    prediction_before=prediction_before,
                    error_message=str(e)
                )
                await self._dispatcher.dispatch(outcome)
            raise

    # Apply decorator to all strategy methods:

    @track_strategy('code')
    async def _execute_code_strategy(self, description: str, desire_id: str = None) -> bool:
        """Generate and execute code."""
        # ... existing implementation unchanged ...
        pass

    @track_strategy('curate')
    async def _execute_curate_strategy(self, description: str, desire_id: str = None) -> bool:
        """Optimize graph."""
        # ... existing implementation unchanged ...
        pass

    @track_strategy('orphan_reconciliation')
    async def _execute_orphan_reconciliation(self, description: str, desire_id: str = None) -> bool:
        """Integrate orphaned nodes."""
        # ... existing implementation unchanged ...
        pass

    @track_strategy('self_modify')
    async def _execute_self_modify_strategy(self, description: str, desire_id: str = None) -> bool:
        """Modify BYRD's code."""
        # ... existing implementation unchanged ...
        pass

    @track_strategy('introspect')
    async def _execute_introspect_strategy(self, description: str, desire_id: str = None) -> bool:
        """Internal reflection."""
        # ... existing implementation unchanged ...
        pass

    @track_strategy('edit_document')
    async def _execute_edit_document_strategy(self, description: str, desire_id: str = None) -> bool:
        """Edit docs in memory."""
        # ... existing implementation unchanged ...
        pass

    # FIX v4: Methods with different signatures (desire: Dict) must NOT use decorator.
    # Instead, wrap the existing logic manually inside _execute_with_tracking.

    async def _seek_knowledge(self, desire: Dict) -> bool:
        """Web research - FIX: Manual tracking wrapper for Dict signature."""
        description = desire.get('description', str(desire))
        desire_id = desire.get('id')

        async def _do_research():
            # === EXISTING IMPLEMENTATION GOES HERE ===
            # Move the existing _seek_knowledge logic into this inner function.
            # Example structure:
            query = desire.get('description', '')
            results = await self._search_searxng(query)
            if results:
                await self.memory.record_experience(
                    content=f"Research on: {query}\nFindings: {results[:500]}",
                    type="research"
                )
                return True
            return False
            # === END EXISTING IMPLEMENTATION ===

        return await self._execute_with_tracking(
            strategy='research',
            description=description,
            execute_fn=_do_research,
            desire_id=desire_id
        )

    async def _seek_capability(self, desire: Dict) -> bool:
        """Search for installable tools - FIX: Manual tracking wrapper for Dict signature."""
        description = desire.get('description', str(desire))
        desire_id = desire.get('id')

        async def _do_capability_search():
            # === EXISTING IMPLEMENTATION GOES HERE ===
            # Move the existing _seek_capability logic into this inner function.
            # Example structure:
            query = desire.get('description', '')
            # Search aitmpl registry, evaluate results, install if trusted
            results = await self._search_aitmpl(query)
            if results:
                # ... installation logic ...
                return True
            return False
            # === END EXISTING IMPLEMENTATION ===

        return await self._execute_with_tracking(
            strategy='capability',
            description=description,
            execute_fn=_do_capability_search,
            desire_id=desire_id
        )
```

---

## Part 5: Learning Progress Tracker (~40 lines)

**Fixed**: Track `_total_recorded` separately to fix snapshot frequency.

```python
# src/byrd/core/learning_progress.py

from collections import deque
from dataclasses import dataclass
from typing import List, Deque
import time

@dataclass
class ProgressSnapshot:
    timestamp: float
    success_rate: float
    total_attempts: int

class LearningProgressTracker:
    """Tracks learning progress over time."""

    def __init__(self, window_size: int = 100, snapshot_interval: int = 10):
        self._window_size = window_size
        self._snapshot_interval = snapshot_interval
        self._outcomes: Deque[bool] = deque(maxlen=window_size)
        self._snapshots: List[ProgressSnapshot] = []
        self._total_recorded = 0  # FIX: Track total separately

    def record(self, outcome: 'TaskOutcome') -> bool:
        from core.outcome_dispatcher import OutcomeType
        success = outcome.outcome_type == OutcomeType.SUCCESS
        self._outcomes.append(success)
        self._total_recorded += 1  # FIX: Increment total

        # FIX: Use total_recorded for snapshot frequency
        if self._total_recorded % self._snapshot_interval == 0:
            self._snapshots.append(ProgressSnapshot(
                timestamp=time.time(),
                success_rate=self.current_success_rate,
                total_attempts=self._total_recorded
            ))
        return True

    @property
    def current_success_rate(self) -> float:
        if not self._outcomes:
            return 0.0
        return sum(self._outcomes) / len(self._outcomes)

    @property
    def learning_velocity(self) -> float:
        """Rate of improvement over recent snapshots."""
        if len(self._snapshots) < 2:
            return 0.0
        recent = self._snapshots[-5:]
        if len(recent) < 2:
            return 0.0
        return (recent[-1].success_rate - recent[0].success_rate) / len(recent)

    def get_stats(self) -> dict:
        return {
            'success_rate': self.current_success_rate,
            'velocity': self.learning_velocity,
            'total_recorded': self._total_recorded,
            'window_size': len(self._outcomes),
            'snapshots': len(self._snapshots)
        }

    def reset(self):
        """Reset for fresh start."""
        self._outcomes.clear()
        self._snapshots.clear()
        self._total_recorded = 0
```

---

## Part 6: Emergent Goal Discovery (~160 lines)

**Fixed**: `success_rate` now updates, `update_goal_outcome()` added.

```python
# src/byrd/emergence/goal_discoverer.py

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from collections import defaultdict
import time

@dataclass
class EmergentGoal:
    """A goal that emerged from prediction error patterns."""
    id: str
    description: str
    trigger_pattern: str
    discovery_timestamp: float
    activation_count: int = 0
    success_count: int = 0  # FIX: Track successes
    failure_count: int = 0  # FIX: Track failures

    @property
    def success_rate(self) -> float:
        """FIX: Computed property instead of static field."""
        total = self.success_count + self.failure_count
        if total == 0:
            return 0.0
        return self.success_count / total

@dataclass
class PredictionError:
    """Record of a prediction that didn't match reality."""
    category: str
    predicted: float
    actual: float
    error_magnitude: float
    timestamp: float
    direction: str

class GoalDiscoverer:
    """Discovers emergent goals from prediction error patterns."""

    def __init__(
        self,
        error_threshold: float = 0.3,
        pattern_threshold: int = 5,
        max_goals: int = 50,
        time_window: float = 3600.0
    ):
        self._error_threshold = error_threshold
        self._pattern_threshold = pattern_threshold
        self._max_goals = max_goals
        self._time_window = time_window

        self._errors: List[PredictionError] = []
        self._error_patterns: Dict[str, List[PredictionError]] = defaultdict(list)
        self._emergent_goals: Dict[str, EmergentGoal] = {}
        self._goal_counter = 0

    def process_prediction_error(
        self,
        category: str,
        predicted: float,
        actual: float,
        was_success: bool = None  # FIX: Accept success signal
    ) -> bool:
        """Process a prediction vs actual outcome."""
        error_magnitude = abs(predicted - actual)

        # FIX: Update existing goal outcomes if we have one for this category
        self._update_relevant_goals(category, was_success)

        if error_magnitude > self._error_threshold:
            direction = "over" if predicted > actual else "under"
            error = PredictionError(
                category=category,
                predicted=predicted,
                actual=actual,
                error_magnitude=error_magnitude,
                timestamp=time.time(),
                direction=direction
            )
            self._record_error(error)
            self._check_for_emergent_goal(error)
            return True
        return False

    def _update_relevant_goals(self, category: str, was_success: bool):
        """FIX: Update success/failure counts for relevant goals."""
        if was_success is None:
            return

        for direction in ["over", "under"]:
            key = f"{category}:{direction}"
            if key in self._emergent_goals:
                goal = self._emergent_goals[key]
                goal.activation_count += 1
                if was_success:
                    goal.success_count += 1
                else:
                    goal.failure_count += 1

    def _record_error(self, error: PredictionError):
        """Record error and update patterns."""
        self._errors.append(error)
        pattern_key = f"{error.category}:{error.direction}"
        self._error_patterns[pattern_key].append(error)

        if len(self._errors) > 1000:
            self._errors = self._errors[-1000:]

    def _check_for_emergent_goal(self, error: PredictionError):
        """Check if error pattern should spawn a goal."""
        pattern_key = f"{error.category}:{error.direction}"
        now = time.time()

        recent_errors = [
            e for e in self._error_patterns[pattern_key]
            if now - e.timestamp < self._time_window
        ]

        if len(recent_errors) >= self._pattern_threshold:
            if pattern_key not in self._emergent_goals:
                self._spawn_goal(pattern_key, recent_errors)

    def _spawn_goal(self, pattern_key: str, errors: List[PredictionError]):
        """Spawn a new emergent goal from error pattern."""
        if len(self._emergent_goals) >= self._max_goals:
            self._prune_goals()

        self._goal_counter += 1
        category, direction = pattern_key.split(":")

        goal = EmergentGoal(
            id=f"goal_{self._goal_counter}",
            description=f"Improve {direction}-prediction accuracy in {category}",
            trigger_pattern=pattern_key,
            discovery_timestamp=time.time(),
            activation_count=len(errors)
        )

        self._emergent_goals[pattern_key] = goal

    def _prune_goals(self):
        """Remove lowest-performing goals."""
        if not self._emergent_goals:
            return

        # FIX: Use computed success_rate property
        scored = [
            (k, g.activation_count * (g.success_rate + 0.1))
            for k, g in self._emergent_goals.items()
        ]
        scored.sort(key=lambda x: x[1])

        to_remove = max(1, len(scored) // 5)
        for key, _ in scored[:to_remove]:
            del self._emergent_goals[key]

    def get_active_goals(self) -> List[EmergentGoal]:
        """Get currently active emergent goals."""
        return list(self._emergent_goals.values())

    def get_goal_for_strategy(self, strategy: str) -> Optional[EmergentGoal]:
        """Get relevant goal for current strategy."""
        for direction in ["over", "under"]:
            key = f"{strategy}:{direction}"
            if key in self._emergent_goals:
                return self._emergent_goals[key]
        return None

    def get_stats(self) -> dict:
        goals = list(self._emergent_goals.values())
        return {
            'total_errors': len(self._errors),
            'active_goals': len(goals),
            'patterns_tracked': len(self._error_patterns),
            'goals_by_success_rate': [
                {'id': g.id, 'pattern': g.trigger_pattern, 'success_rate': g.success_rate}
                for g in sorted(goals, key=lambda x: x.success_rate, reverse=True)
            ][:5]
        }

    def reset(self):
        """Reset for fresh start."""
        self._errors.clear()
        self._error_patterns.clear()
        self._emergent_goals.clear()
        self._goal_counter = 0
```

---

## Part 7: Dual Instance Manager (~50 lines)

No changes from v2.

```python
# src/byrd/core/instance_manager.py

import asyncio
from enum import Enum
from typing import Dict, Any
import time

class InstanceRole(Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"

class DualInstanceManager:
    """Manages two concurrent GLM instances with rate limiting."""

    RATE_LIMIT_SECONDS = 10.0

    def __init__(self, llm_client):
        self._client = llm_client
        self._instance_locks: Dict[InstanceRole, asyncio.Lock] = {
            InstanceRole.PRIMARY: asyncio.Lock(),
            InstanceRole.SECONDARY: asyncio.Lock()
        }
        self._last_call: Dict[InstanceRole, float] = {
            InstanceRole.PRIMARY: 0,
            InstanceRole.SECONDARY: 0
        }
        self._call_counts: Dict[InstanceRole, int] = {
            InstanceRole.PRIMARY: 0,
            InstanceRole.SECONDARY: 0
        }

    async def call(self, role: InstanceRole, prompt: str, **kwargs) -> Any:
        """Make rate-limited call on specified instance."""
        async with self._instance_locks[role]:
            elapsed = time.time() - self._last_call[role]
            if elapsed < self.RATE_LIMIT_SECONDS:
                await asyncio.sleep(self.RATE_LIMIT_SECONDS - elapsed)

            result = await self._client.generate(prompt, **kwargs)

            self._last_call[role] = time.time()
            self._call_counts[role] += 1

            return result

    async def call_parallel(self, primary_prompt: str, secondary_prompt: str, **kwargs) -> tuple:
        """Make parallel calls on both instances."""
        primary_task = self.call(InstanceRole.PRIMARY, primary_prompt, **kwargs)
        secondary_task = self.call(InstanceRole.SECONDARY, secondary_prompt, **kwargs)
        return await asyncio.gather(primary_task, secondary_task)

    def get_stats(self) -> Dict[str, Any]:
        return {
            'primary_calls': self._call_counts[InstanceRole.PRIMARY],
            'secondary_calls': self._call_counts[InstanceRole.SECONDARY],
            'total_calls': sum(self._call_counts.values())
        }

    def reset(self):
        """Reset for fresh start."""
        for role in InstanceRole:
            self._call_counts[role] = 0
            self._last_call[role] = 0
```

---

## Part 8: Wikipedia Backend (~70 lines)

No changes from v2.

```python
# src/byrd/knowledge/wikipedia_backend.py

import aiohttp
from typing import Optional, List
from dataclasses import dataclass

@dataclass
class WikipediaResult:
    title: str
    extract: str
    url: str
    page_id: int

class WikipediaBackend:
    """Wikipedia API backend for factual knowledge."""

    BASE_URL = "https://en.wikipedia.org/w/api.php"

    def __init__(self, cache: Optional['ResultCache'] = None):
        self._cache = cache
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def search(self, query: str, limit: int = 5) -> List[WikipediaResult]:
        """Search Wikipedia for relevant articles."""
        cache_key = f"wiki:search:{query}"
        if self._cache:
            cached = self._cache.get(cache_key)
            if cached:
                return cached

        session = await self._get_session()
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'search',
            'srsearch': query,
            'srlimit': limit
        }

        async with session.get(self.BASE_URL, params=params) as resp:
            data = await resp.json()

        results = []
        for item in data.get('query', {}).get('search', []):
            extract = await self._get_extract(item['pageid'])
            results.append(WikipediaResult(
                title=item['title'],
                extract=extract,
                url=f"https://en.wikipedia.org/?curid={item['pageid']}",
                page_id=item['pageid']
            ))

        if self._cache:
            self._cache.set(cache_key, results, ttl=3600)

        return results

    async def _get_extract(self, page_id: int) -> str:
        """Get article extract by page ID."""
        session = await self._get_session()
        params = {
            'action': 'query',
            'format': 'json',
            'pageids': page_id,
            'prop': 'extracts',
            'exintro': True,
            'explaintext': True,
            'exsentences': 5
        }

        async with session.get(self.BASE_URL, params=params) as resp:
            data = await resp.json()

        pages = data.get('query', {}).get('pages', {})
        page = pages.get(str(page_id), {})
        return page.get('extract', '')

    async def close(self):
        if self._session:
            await self._session.close()
```

---

## Part 9: ArXiv Backend (~65 lines)

No changes from v2.

```python
# src/byrd/knowledge/arxiv_backend.py

import aiohttp
import xml.etree.ElementTree as ET
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class ArxivResult:
    title: str
    abstract: str
    authors: List[str]
    arxiv_id: str
    url: str
    published: str

class ArxivBackend:
    """ArXiv API backend for academic papers."""

    BASE_URL = "http://export.arxiv.org/api/query"

    def __init__(self, cache: Optional['ResultCache'] = None):
        self._cache = cache
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def search(self, query: str, limit: int = 5) -> List[ArxivResult]:
        """Search ArXiv for relevant papers."""
        cache_key = f"arxiv:search:{query}"
        if self._cache:
            cached = self._cache.get(cache_key)
            if cached:
                return cached

        session = await self._get_session()
        params = {
            'search_query': f'all:{query}',
            'start': 0,
            'max_results': limit,
            'sortBy': 'relevance'
        }

        async with session.get(self.BASE_URL, params=params) as resp:
            xml_data = await resp.text()

        results = self._parse_response(xml_data)

        if self._cache:
            self._cache.set(cache_key, results, ttl=3600)

        return results

    def _parse_response(self, xml_data: str) -> List[ArxivResult]:
        """Parse ArXiv API XML response."""
        root = ET.fromstring(xml_data)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}

        results = []
        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns)
            abstract = entry.find('atom:summary', ns)
            arxiv_id = entry.find('atom:id', ns)
            published = entry.find('atom:published', ns)

            authors = [
                a.find('atom:name', ns).text
                for a in entry.findall('atom:author', ns)
                if a.find('atom:name', ns) is not None
            ]

            results.append(ArxivResult(
                title=title.text.strip() if title is not None else '',
                abstract=abstract.text.strip() if abstract is not None else '',
                authors=authors,
                arxiv_id=arxiv_id.text if arxiv_id is not None else '',
                url=arxiv_id.text if arxiv_id is not None else '',
                published=published.text if published is not None else ''
            ))

        return results

    async def close(self):
        if self._session:
            await self._session.close()
```

---

## Part 10: Result Cache (~30 lines)

No changes from v2.

```python
# src/byrd/knowledge/cache.py

from typing import Any, Optional, Dict
from dataclasses import dataclass
import time

@dataclass
class CacheEntry:
    value: Any
    expires_at: float

class ResultCache:
    """Simple TTL cache for knowledge backend results."""

    def __init__(self, max_entries: int = 1000):
        self._cache: Dict[str, CacheEntry] = {}
        self._max_entries = max_entries

    def get(self, key: str) -> Optional[Any]:
        """Get cached value if not expired."""
        entry = self._cache.get(key)
        if entry is None:
            return None
        if time.time() > entry.expires_at:
            del self._cache[key]
            return None
        return entry.value

    def set(self, key: str, value: Any, ttl: int = 3600):
        """Set cached value with TTL in seconds."""
        if len(self._cache) >= self._max_entries:
            self._evict_expired()

        self._cache[key] = CacheEntry(
            value=value,
            expires_at=time.time() + ttl
        )

    def _evict_expired(self):
        """Remove expired entries."""
        now = time.time()
        self._cache = {
            k: v for k, v in self._cache.items()
            if v.expires_at > now
        }

    def stats(self) -> dict:
        return {'entries': len(self._cache), 'max': self._max_entries}

    def clear(self):
        """Clear all entries."""
        self._cache.clear()
```

---

## Part 11: Health Endpoint (~50 lines)

**Fixed**: Added `get_byrd_instance()` singleton accessor.

```python
# src/byrd/api/health.py

from fastapi import APIRouter, Depends
from typing import Dict, Any, Optional

router = APIRouter()

# FIX: Singleton pattern for Byrd instance access
_byrd_instance = None

def set_byrd_instance(byrd):
    """Called during app initialization to set the Byrd instance."""
    global _byrd_instance
    _byrd_instance = byrd

def get_byrd_instance():
    """Get the singleton Byrd instance."""
    global _byrd_instance
    return _byrd_instance

def get_learning_components() -> Dict[str, Any]:
    """Dependency injection for learning components."""
    byrd = get_byrd_instance()
    if byrd is None:
        return {}
    return {
        'memory_tracker': getattr(byrd, '_memory_tracker', None),
        'learning_progress': getattr(byrd, '_learning_progress', None),
        'goal_discoverer': getattr(byrd, '_goal_discoverer', None),
        'instance_manager': getattr(byrd, '_instance_manager', None),
        'dispatcher': getattr(byrd, '_dispatcher', None)
    }

@router.get("/health/learning")
async def learning_health(components: dict = Depends(get_learning_components)) -> Dict[str, Any]:
    """Return learning system health metrics."""
    if not components:
        return {"status": "not_initialized", "error": "Byrd instance not set"}

    result = {"status": "healthy"}

    if components.get('memory_tracker'):
        result['memory'] = components['memory_tracker'].get_stats()

    if components.get('learning_progress'):
        result['learning'] = components['learning_progress'].get_stats()

    if components.get('goal_discoverer'):
        result['emergent_goals'] = components['goal_discoverer'].get_stats()

    if components.get('instance_manager'):
        result['instances'] = components['instance_manager'].get_stats()

    return result

@router.post("/health/learning/reset")
async def reset_learning(components: dict = Depends(get_learning_components)) -> Dict[str, str]:
    """Reset learning components for fresh start."""
    if not components:
        return {"status": "error", "message": "Byrd instance not set"}

    reset_count = 0
    for name, component in components.items():
        if component and hasattr(component, 'reset'):
            component.reset()
            reset_count += 1

    return {"status": "ok", "components_reset": reset_count}
```

---

## Part 12: Initialization Wiring (~70 lines)

**Fixed**: Proper component access, health endpoint integration.

```python
# Additions to src/byrd/byrd.py

class Byrd:
    def __init__(self, config: Dict = None):
        # Existing init...
        self.config = config or {}

        # Learning components (initialized later)
        self._dispatcher = None
        self._memory_tracker = None
        self._learning_progress = None
        self._goal_discoverer = None
        self._result_cache = None
        self._wikipedia = None
        self._arxiv = None
        self._instance_manager = None

    async def _initialize_learning_substrate(self):
        """Initialize learning components with proper wiring."""
        from core.outcome_dispatcher import OutcomeDispatcher
        from core.memory_tracker import MemoryTracker
        from core.learning_progress import LearningProgressTracker
        from emergence.goal_discoverer import GoalDiscoverer
        from knowledge.cache import ResultCache
        from knowledge.wikipedia_backend import WikipediaBackend
        from knowledge.arxiv_backend import ArxivBackend
        from api.health import set_byrd_instance

        # Core tracking
        self._memory_tracker = MemoryTracker(
            max_events=self.config.get('learning', {}).get('memory_tracker', {}).get('max_events', 10000)
        )
        self._learning_progress = LearningProgressTracker(
            window_size=self.config.get('learning', {}).get('learning_progress', {}).get('window_size', 100)
        )
        self._goal_discoverer = GoalDiscoverer(
            error_threshold=self.config.get('learning', {}).get('goal_discoverer', {}).get('error_threshold', 0.3),
            pattern_threshold=self.config.get('learning', {}).get('goal_discoverer', {}).get('pattern_threshold', 5),
            max_goals=self.config.get('learning', {}).get('goal_discoverer', {}).get('max_goals', 50)
        )

        # Knowledge backends
        self._result_cache = ResultCache(
            max_entries=self.config.get('cache', {}).get('max_entries', 1000)
        )
        self._wikipedia = WikipediaBackend(cache=self._result_cache)
        self._arxiv = ArxivBackend(cache=self._result_cache)

        # Central dispatcher using ACTUAL component interfaces
        self._dispatcher = OutcomeDispatcher(
            learned_retriever=self.learned_retriever,
            intuition_network=self.intuition_network,
            desire_classifier=self.desire_classifier,
            memory_tracker=self._memory_tracker,
            goal_discoverer=self._goal_discoverer,
            learning_progress=self._learning_progress
        )

        # Inject into Seeker
        self.seeker.set_dispatcher(self._dispatcher)
        self.seeker.set_intuition_network(self.intuition_network)

        # FIX: Register for health endpoint
        set_byrd_instance(self)

    async def start(self):
        """Enhanced start with learning substrate."""
        # Existing startup...
        await self._awaken_if_needed()
        await self._ensure_architecture_loaded()

        # Initialize learning substrate
        await self._initialize_learning_substrate()

        # Start components...
        await self._start_components()

    async def shutdown(self):
        """Clean shutdown."""
        # Close knowledge backends
        if self._wikipedia:
            await self._wikipedia.close()
        if self._arxiv:
            await self._arxiv.close()

        # Existing shutdown...
```

---

## Honest Limitations

### What This Learning System IS

- **EMA weight updates**: Gradual adjustment based on success/failure
- **Situation→action learning**: Intuition network learns what works where
- **Pattern-based goals**: Recurring prediction errors spawn improvement goals
- **Retrieval feedback**: Learns which retrieved nodes are helpful

### What This Learning System IS NOT

- **Semantic understanding**: No comprehension of WHY something works
- **Rapid learning**: Requires hundreds of outcomes to show effect
- **Transfer learning**: Improvements don't cross strategy boundaries
- **Self-improvement**: Cannot modify its own architecture

### Time to Observable Effect

| Metric | Outcomes Required | At 180/hour |
|--------|-------------------|-------------|
| EMA weight shift (0.5→0.6) | ~20-30 per category | ~10-15 min |
| Statistically significant trend | ~100 total | ~30 min |
| Emergent goal spawning | 5+ errors in pattern | Variable |
| Reliable learning velocity | ~500 total | ~3 hours |

---

## Implementation Order

### Phase A: Self-Contained (No Interface Changes)
1. Part 10: Result Cache
2. Part 8: Wikipedia Backend
3. Part 9: ArXiv Backend
4. Part 5: Learning Progress Tracker
5. Part 3: Memory Tracker
6. Part 7: Dual Instance Manager

**Total: ~305 lines, immediate utility**

### Phase B: Core Integration
7. Part 1: OutcomeDispatcher
8. Part 4: Seeker Integration (with decorator pattern)
9. Part 12: Initialization Wiring

**Total: ~285 lines, requires testing**

### Phase C: Learning Enhancement
10. Part 2: DesireClassifier Learning (requires refactor)
11. Part 6: Goal Discoverer
12. Part 11: Health Endpoint

**Total: ~280 lines, extends capabilities**

---

## Configuration

```yaml
# config/byrd.yaml

learning:
  outcome_dispatcher:
    enabled: true

  desire_classifier:
    learning_rate: 0.1

  memory_tracker:
    max_events: 10000

  learning_progress:
    window_size: 100
    snapshot_interval: 10

  goal_discoverer:
    error_threshold: 0.3
    pattern_threshold: 5
    max_goals: 50
    time_window_seconds: 3600

dual_instance:
  enabled: true
  rate_limit_seconds: 10.0

knowledge_backends:
  wikipedia:
    enabled: true
  arxiv:
    enabled: true

cache:
  max_entries: 1000
  default_ttl: 3600
```

---

## Line Count Summary

| Part | Component | Lines |
|------|-----------|-------|
| 1 | OutcomeDispatcher | ~95 |
| 2 | DesireClassifier Learning | ~70 |
| 3 | Memory Tracker | ~40 |
| 4 | Seeker Integration (merged + v4 fix) | ~150 |
| 5 | Learning Progress | ~40 |
| 6 | Goal Discoverer | ~160 |
| 7 | Instance Manager | ~50 |
| 8 | Wikipedia Backend | ~70 |
| 9 | ArXiv Backend | ~65 |
| 10 | Result Cache | ~30 |
| 11 | Health Endpoint | ~50 |
| 12 | Initialization Wiring | ~70 |
| **TOTAL** | | **~890** |

---

## What Changed From v4

| Bug | v4 Problem | v5 Fix |
|-----|------------|--------|
| Missing `Dict` import | `Dict` used in type hints but not imported from `typing` | Added `Dict` to import line |

## What Changed From v3

| Bug | v3 Problem | v4 Fix |
|-----|------------|--------|
| Decorator signature mismatch | `@track_strategy` applied to methods with `desire: Dict` signature | Removed decorator, manual `_execute_with_tracking` wrapper |
| Missing `_strategy_stats` | Dict referenced but never initialized | Added conditional init in `__init__` additions |

## What Changed From v2

| Bug | v2 Problem | v3 Fix |
|-----|------------|--------|
| Prediction timing | `score_action()` called after `record_outcome()` | `prediction_before` field in TaskOutcome, captured in Seeker |
| EMA logic | Failure bucket moved toward 0.0 | Track counts, compute actual rate, EMA on rate |
| `_classify_base()` | Referenced but undefined | Clear refactor instructions provided |
| Part 4/5 conflict | Two incompatible versions | Merged into single method with decorator pattern |
| Snapshot frequency | Fired every time after window filled | Track `_total_recorded` separately |
| `success_rate` | Field never updated | Property computed from `success_count`/`failure_count` |
| Strategy coverage | Only 1 of 8 methods shown | Decorator pattern covers all strategies |
| `get_byrd_instance()` | Function didn't exist | Added singleton pattern in health.py |

---

## Source Documents

- `CONNECTION_PLAN.md` - Core dispatcher concept
- `BYRD_ENHANCEMENT_PROPOSALS_V2.md` - Goal discovery (Priority 2)
- `IMPLEMENTATION_PLAN_v2.md` - Knowledge backends
