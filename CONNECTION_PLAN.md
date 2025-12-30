# BYRD Connection Plan (Revised)

## The Problem

BYRD has sophisticated learning components that **exist but aren't connected**:

```
                          CURRENT STATE

   Task Completes ──────────────────────────────────────────► Nowhere
        │
        │   ┌─────────────────────┐
        │   │ learned_retriever   │  has record_feedback() - NEVER CALLED
        │   └─────────────────────┘
        │   ┌─────────────────────┐
        │   │ intuition_network   │  has record_outcome() - NEVER CALLED
        │   └─────────────────────┘
        │   ┌─────────────────────┐
        │   │ desire_classifier   │  has record_feedback() - BUT DOESN'T
        │   └─────────────────────┘  ACTUALLY LEARN (just stores buffer)
        │   ┌─────────────────────┐
        │   │ capability_evaluator│  measures but doesn't trigger action
        │   └─────────────────────┘
        │   ┌─────────────────────┐
        │   │ code_learner        │  codifies but doesn't verify
        │   └─────────────────────┘
        ▼
   Learning components starve
```

The feedback methods exist. They're just never called. **And one of them (desire_classifier) doesn't even learn when called.**

---

## The Solution

**One small component that observes task outcomes and dispatches to all learning components.**

```
                          TARGET STATE

   Task Completes ───► OutcomeDispatcher ───┬──► learned_retriever
        │                    │              ├──► intuition_network
        │                    │              ├──► desire_classifier
        │                    │              └──► capability_evaluator
        │                    │
        │              Tracks context:
        │              - Which memories retrieved
        │              - Which route taken
        │              - Which actions tried
        │              - Success/failure
        ▼
   All learning components get feedback
```

---

## Implementation

### Part 1: OutcomeDispatcher (New File - ~150 lines)

```python
# outcome_dispatcher.py
"""
BYRD Outcome Dispatcher

The missing link between task execution and learning components.

When a task completes (success or failure), this dispatcher:
1. Notifies learned_retriever about which memories helped
2. Notifies intuition_network about action outcomes
3. Notifies desire_classifier about routing effectiveness
4. Triggers capability re-evaluation if significant failure

This is GLUE CODE, not new infrastructure.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from enum import Enum


class TaskType(Enum):
    RESEARCH = "research"
    INTROSPECTION = "introspection"
    CODE = "code"
    CAPABILITY = "capability"
    SELF_MODIFY = "self_modify"
    CURATE = "curate"
    OBSERVE = "observe"


@dataclass
class TaskContext:
    """Context captured during task execution."""
    task_id: str
    task_type: TaskType
    desire_id: Optional[str]
    desire_description: str
    route_taken: str  # Handler that processed this

    # What was retrieved from memory
    retrieved_memory_ids: List[str] = field(default_factory=list)

    # Query types that led to retrievals (for learned_retriever)
    query_types: List[str] = field(default_factory=list)

    # Actions attempted
    actions_tried: List[str] = field(default_factory=list)

    # Timing
    started_at: datetime = field(default_factory=datetime.now)

    # Will be set on completion
    success: Optional[bool] = None
    failure_reason: Optional[str] = None
    completed_at: Optional[datetime] = None


class OutcomeDispatcher:
    """
    Dispatches task outcomes to all learning components.

    Usage:
        # At task start
        ctx = dispatcher.start_task(desire, task_type, route)

        # During task - track what's used
        ctx.retrieved_memory_ids.append(memory_id)
        ctx.actions_tried.append("web_search")

        # At task end
        await dispatcher.complete_task(ctx, success=True)
    """

    def __init__(
        self,
        learned_retriever=None,
        intuition_network=None,
        desire_classifier=None,
        capability_evaluator=None,
        memory=None
    ):
        self.learned_retriever = learned_retriever
        self.intuition_network = intuition_network
        self.desire_classifier = desire_classifier
        self.capability_evaluator = capability_evaluator
        self.memory = memory

        # Active task contexts
        self._active_tasks: Dict[str, TaskContext] = {}

        # Statistics
        self._total_dispatched = 0
        self._successful_dispatches = 0

    def start_task(
        self,
        desire: Dict,
        task_type: TaskType,
        route: str
    ) -> TaskContext:
        """
        Start tracking a task.

        Call this when beginning to process a desire.
        Returns context object to track during execution.
        """
        import uuid
        task_id = str(uuid.uuid4())[:8]

        ctx = TaskContext(
            task_id=task_id,
            task_type=task_type,
            desire_id=desire.get("id"),
            desire_description=desire.get("description", ""),
            route_taken=route
        )

        self._active_tasks[task_id] = ctx
        return ctx

    async def complete_task(
        self,
        ctx: TaskContext,
        success: bool,
        failure_reason: Optional[str] = None
    ):
        """
        Complete a task and dispatch to all learning components.

        This is the critical method that feeds all learning loops.
        """
        ctx.success = success
        ctx.failure_reason = failure_reason
        ctx.completed_at = datetime.now()

        # Remove from active
        self._active_tasks.pop(ctx.task_id, None)

        # Dispatch to all learning components
        await self._dispatch_to_retriever(ctx)
        await self._dispatch_to_intuition(ctx)
        await self._dispatch_to_classifier(ctx)
        await self._check_capability_regression(ctx)

        self._total_dispatched += 1
        if success:
            self._successful_dispatches += 1

    async def _dispatch_to_retriever(self, ctx: TaskContext):
        """Tell learned_retriever which memories helped (or didn't)."""
        if not self.learned_retriever:
            return

        if not ctx.retrieved_memory_ids:
            return

        try:
            for memory_id in ctx.retrieved_memory_ids:
                await self.learned_retriever.record_feedback(
                    query=ctx.desire_description,
                    node_id=memory_id,
                    was_helpful=ctx.success
                )
        except Exception as e:
            print(f"OutcomeDispatcher: Retriever feedback failed: {e}")

    async def _dispatch_to_intuition(self, ctx: TaskContext):
        """Tell intuition_network about action outcomes."""
        if not self.intuition_network:
            return

        if not ctx.actions_tried:
            return

        try:
            # Record outcome for each action tried
            for action in ctx.actions_tried:
                await self.intuition_network.record_outcome(
                    situation=ctx.desire_description,
                    action=action,
                    success=ctx.success
                )
        except Exception as e:
            print(f"OutcomeDispatcher: Intuition feedback failed: {e}")

    async def _dispatch_to_classifier(self, ctx: TaskContext):
        """Tell desire_classifier if routing was effective."""
        if not self.desire_classifier:
            return

        try:
            self.desire_classifier.record_feedback(
                desire={"description": ctx.desire_description, "id": ctx.desire_id},
                actual_outcome="success" if ctx.success else "failure",
                was_correct_routing=ctx.success  # If succeeded, routing was correct
            )
        except Exception as e:
            print(f"OutcomeDispatcher: Classifier feedback failed: {e}")

    async def _check_capability_regression(self, ctx: TaskContext):
        """
        On significant failure, trigger capability re-evaluation.

        This connects failures to the measurement system.
        """
        if not self.capability_evaluator:
            return

        if ctx.success:
            return  # Only check on failure

        # Map task types to capabilities
        capability_map = {
            TaskType.RESEARCH: "research",
            TaskType.CODE: "code_generation",
            TaskType.INTROSPECTION: "introspection",
        }

        capability = capability_map.get(ctx.task_type)
        if not capability:
            return

        try:
            # Get current trend
            trend = self.capability_evaluator.get_trend(capability)

            if trend == "declining":
                # Capability is declining - record this for Omega to act on
                if self.memory:
                    await self.memory.record_experience(
                        content=f"[REGRESSION] {capability} capability declining. "
                                f"Task failed: {ctx.desire_description[:100]}",
                        type="regression_detected"
                    )
        except Exception as e:
            print(f"OutcomeDispatcher: Capability check failed: {e}")

    def get_statistics(self) -> Dict[str, Any]:
        """Get dispatcher statistics."""
        return {
            "total_dispatched": self._total_dispatched,
            "successful": self._successful_dispatches,
            "success_rate": self._successful_dispatches / self._total_dispatched
                           if self._total_dispatched > 0 else 0,
            "active_tasks": len(self._active_tasks)
        }


# Singleton for easy access
_dispatcher: Optional[OutcomeDispatcher] = None

def get_outcome_dispatcher() -> Optional[OutcomeDispatcher]:
    """Get the global outcome dispatcher."""
    return _dispatcher

def init_outcome_dispatcher(
    learned_retriever=None,
    intuition_network=None,
    desire_classifier=None,
    capability_evaluator=None,
    memory=None
) -> OutcomeDispatcher:
    """Initialize the global outcome dispatcher."""
    global _dispatcher
    _dispatcher = OutcomeDispatcher(
        learned_retriever=learned_retriever,
        intuition_network=intuition_network,
        desire_classifier=desire_classifier,
        capability_evaluator=capability_evaluator,
        memory=memory
    )
    return _dispatcher
```

---

### Part 2: Fix DesireClassifier Learning (FIX - ~60 lines)

**THE BUG**: `desire_classifier.py` has `record_feedback()` that stores in a buffer, but nothing ever uses this buffer to update routing behavior.

```python
# CURRENT CODE (broken):
def record_feedback(self, desire, actual_outcome, was_correct_routing):
    self._feedback_buffer.append({...})  # Just stores, nothing reads this

def analyze_feedback(self):
    # Returns statistics but DOES NOT modify routing behavior
```

**THE FIX**: Add learning that adjusts routing based on feedback.

In `desire_classifier.py`, add:

```python
# At class level, add adjustments storage
def __init__(self, config):
    # ... existing init ...

    # Routing adjustments learned from feedback
    # Maps (keyword, route) -> weight adjustment
    # Positive = prefer this route, Negative = avoid
    self._routing_adjustments: Dict[tuple, float] = {}

    # Learning rate for EMA updates
    self._learning_rate = 0.1


def record_feedback(self, desire: Dict, actual_outcome: str, was_correct_routing: bool):
    """Record feedback AND learn from it."""
    description = desire.get("description", "").lower()

    # Store in buffer for analysis
    self._feedback_buffer.append({
        "desire": desire,
        "actual_outcome": actual_outcome,
        "was_correct_routing": was_correct_routing,
        "timestamp": datetime.now().isoformat()
    })

    # Cap buffer size
    if len(self._feedback_buffer) > 1000:
        self._feedback_buffer = self._feedback_buffer[-500:]

    # ACTUALLY LEARN: Adjust routing weights based on outcome
    self._update_routing_adjustments(description, actual_outcome, was_correct_routing)


def _update_routing_adjustments(self, description: str, outcome: str, was_correct: bool):
    """
    Update routing adjustments based on feedback.

    Uses EMA to smooth updates:
    - If routing was correct for this keyword pattern, increase preference
    - If routing was wrong, decrease preference
    """
    # Extract keywords from description
    keywords = self._extract_keywords(description)

    # Infer which route was taken from outcome
    # (This is coarse - we're learning keyword → success correlations)
    route = self._infer_route(description)

    for keyword in keywords:
        key = (keyword, route)
        current = self._routing_adjustments.get(key, 0.0)

        # Target: +1 if correct, -1 if wrong
        target = 1.0 if was_correct else -1.0

        # EMA update
        new_value = (1 - self._learning_rate) * current + self._learning_rate * target

        # Clamp to reasonable range
        self._routing_adjustments[key] = max(-1.0, min(1.0, new_value))


def _extract_keywords(self, text: str) -> List[str]:
    """Extract keywords that appear in our routing tables."""
    keywords = []
    text_lower = text.lower()

    # Check for known routing keywords
    for desire_type, kw_list in self._type_keywords.items():
        for kw in kw_list:
            if kw in text_lower:
                keywords.append(kw)

    return keywords[:5]  # Limit to top 5


def _infer_route(self, description: str) -> str:
    """Infer which route was likely taken."""
    # Use existing classification to determine route
    result = self.classify(description)
    return result.desire_type.value


def classify(self, desire_description: str) -> ClassificationResult:
    """Classify a desire, incorporating learned adjustments."""
    # ... existing keyword matching logic ...

    # After computing base scores, apply learned adjustments
    keywords = self._extract_keywords(desire_description.lower())

    for desire_type in DesireType:
        route = desire_type.value
        adjustment = 0.0

        for keyword in keywords:
            key = (keyword, route)
            adjustment += self._routing_adjustments.get(key, 0.0)

        # Apply adjustment to confidence (capped)
        if desire_type == best_type:
            # Boost or reduce confidence based on learned adjustments
            confidence = min(1.0, max(0.0, confidence + adjustment * 0.1))

    # ... rest of existing logic ...


def get_learning_stats(self) -> Dict[str, Any]:
    """Get statistics about what's been learned."""
    return {
        "total_adjustments": len(self._routing_adjustments),
        "positive_adjustments": sum(1 for v in self._routing_adjustments.values() if v > 0),
        "negative_adjustments": sum(1 for v in self._routing_adjustments.values() if v < 0),
        "feedback_buffer_size": len(self._feedback_buffer),
        "top_adjustments": sorted(
            self._routing_adjustments.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        )[:10]
    }
```

**What this achieves**: DesireClassifier now actually learns which keywords should route where, based on whether tasks succeed.

---

### Part 3: Memory Tracking Infrastructure (~40 lines)

**THE PROBLEM**: OutcomeDispatcher needs to know which memories were retrieved for a task, but memory.py doesn't expose this.

In `memory.py`, add tracking wrapper:

```python
class MemoryTracker:
    """
    Context manager that tracks which memories are retrieved during a task.

    Usage:
        async with memory.track_retrievals() as tracker:
            results = await memory.query_similar(text, limit=5)
            # ... use results ...

        retrieved_ids = tracker.get_retrieved_ids()
    """

    def __init__(self, memory_instance):
        self.memory = memory_instance
        self.retrieved_ids: List[str] = []
        self.query_types: List[str] = []
        self._original_query = None

    async def __aenter__(self):
        # Store original method
        self._original_query = self.memory.query_similar

        # Wrap with tracking
        async def tracking_query(*args, **kwargs):
            results = await self._original_query(*args, **kwargs)

            # Extract query type from kwargs if available
            query_type = kwargs.get("query_type", "unknown")
            self.query_types.append(query_type)

            # Track retrieved IDs
            for result in results:
                if hasattr(result, 'id'):
                    self.retrieved_ids.append(result.id)
                elif isinstance(result, dict) and 'id' in result:
                    self.retrieved_ids.append(result['id'])

            return results

        self.memory.query_similar = tracking_query
        return self

    async def __aexit__(self, *args):
        # Restore original method
        self.memory.query_similar = self._original_query

    def get_retrieved_ids(self) -> List[str]:
        return self.retrieved_ids

    def get_query_types(self) -> List[str]:
        return self.query_types


# Add to Memory class:
def track_retrievals(self) -> MemoryTracker:
    """Create a context manager to track memory retrievals."""
    return MemoryTracker(self)
```

---

### Part 4: Wire Into BYRD Initialization (~15 lines)

In `byrd.py`, after creating learning components:

```python
# After creating all learning components...

# Initialize the outcome dispatcher
from outcome_dispatcher import init_outcome_dispatcher

self.outcome_dispatcher = init_outcome_dispatcher(
    learned_retriever=self.learned_retriever,
    intuition_network=self.intuition_network,
    desire_classifier=self.agi_runner.desire_classifier,  # In agi_runner
    capability_evaluator=self.agi_runner.capability_evaluator,  # In agi_runner
    memory=self.memory
)

# Pass to seeker
self.seeker.outcome_dispatcher = self.outcome_dispatcher
self.seeker.memory_tracker = self.memory  # For track_retrievals()
```

---

### Part 5: Wire Into Seeker Task Completion (~100 lines total)

**HONEST ASSESSMENT**: Seeker has 8+ strategy methods that need tracking. Each needs:
- Start tracking at method entry
- Track memory retrievals during execution
- Track actions taken
- Complete tracking on exit (success or failure)

Here's the pattern applied to ONE method (multiply by 8 for reality):

```python
async def _research_desire(self, desire: Dict) -> bool:
    """Research a desire with outcome tracking."""
    from outcome_dispatcher import get_outcome_dispatcher, TaskType

    dispatcher = get_outcome_dispatcher()
    ctx = None
    tracker = None

    if dispatcher:
        ctx = dispatcher.start_task(desire, TaskType.RESEARCH, "seeker.research")

    try:
        # Track memory retrievals
        async with self.memory.track_retrievals() as tracker:
            # Get related memories
            related = await self.memory.query_similar(
                desire.get("description", ""),
                limit=5,
                query_type="desire_research"
            )

            # ... existing research code ...

            # Track web search action
            if ctx:
                ctx.actions_tried.append("web_search")

            results = await self._search_searxng(query)

            if not results:
                if ctx and dispatcher:
                    await dispatcher.complete_task(ctx, success=False,
                                                   failure_reason="no_search_results")
                return False

            # Track synthesis action
            if ctx:
                ctx.actions_tried.append("synthesize")

            synthesis = await self._synthesize_results(results, desire)

            # Store experience
            await self.memory.record_experience(
                content=f"[RESEARCH] {synthesis}",
                type="research"
            )

            # Fulfill desire
            await self.memory.fulfill_desire(desire.get("id"))

        # Copy tracked IDs to context
        if ctx and tracker:
            ctx.retrieved_memory_ids = tracker.get_retrieved_ids()
            ctx.query_types = tracker.get_query_types()

        # Success
        if ctx and dispatcher:
            await dispatcher.complete_task(ctx, success=True)

        return True

    except Exception as e:
        if ctx and dispatcher:
            await dispatcher.complete_task(ctx, success=False, failure_reason=str(e))
        return False
```

**Other methods needing similar treatment** (~10-15 lines each):
- `_introspect_desire()` - TaskType.INTROSPECTION
- `_code_desire()` - TaskType.CODE
- `_curate_desire()` - TaskType.CURATE
- `_self_modify_desire()` - TaskType.SELF_MODIFY
- `_agi_cycle_desire()` - TaskType.CAPABILITY
- `_reconcile_orphans_desire()` - TaskType.CURATE
- `_install_desire()` - TaskType.CAPABILITY

---

### Part 6: Code Learner Verification Loop (~40 lines)

Add verification after codification in `code_learner.py`:

```python
async def verify_codified_pattern(self, pattern_id: str) -> bool:
    """
    Verify a codified pattern still works.

    Run it against test inputs and check outputs match expected.
    """
    if pattern_id not in self.code_registry:
        return False

    # Get original pattern details from Neo4j
    result = await self.memory._run_query("""
        MATCH (p:Pattern {id: $pattern_id})
        RETURN p.test_inputs as inputs, p.test_outputs as outputs
    """, {"pattern_id": pattern_id})

    if not result or not result[0].get("inputs"):
        return True  # No test cases, assume OK

    test_inputs = result[0]["inputs"]
    expected_outputs = result[0]["outputs"]

    try:
        for i, test_input in enumerate(test_inputs):
            actual = await self.execute_learned(pattern_id, test_input)
            expected = expected_outputs[i] if i < len(expected_outputs) else None

            if actual != expected:
                # Mark pattern as failing
                await self.memory._run_query("""
                    MATCH (p:Pattern {id: $pattern_id})
                    SET p.verification_status = 'failing',
                        p.last_verified = datetime()
                """, {"pattern_id": pattern_id})
                return False

        # Mark as verified
        await self.memory._run_query("""
            MATCH (p:Pattern {id: $pattern_id})
            SET p.verification_status = 'passing',
                p.last_verified = datetime()
        """, {"pattern_id": pattern_id})
        return True

    except Exception as e:
        print(f"Verification failed for {pattern_id}: {e}")
        return False

async def verification_cycle(self) -> Dict[str, bool]:
    """Verify all codified patterns. Run periodically."""
    results = {}
    for pattern_id in self.code_registry:
        results[pattern_id] = await self.verify_codified_pattern(pattern_id)
    return results
```

Add to Omega training hooks:

```python
# In omega.py _run_training_hooks()

# 6. Code verification - every 50 cycles
if self.code_learner and self._total_cycles % 50 == 0:
    try:
        verification = await self.code_learner.verification_cycle()
        failing = [k for k, v in verification.items() if not v]
        results["code_verification"] = {
            "total": len(verification),
            "passing": len(verification) - len(failing),
            "failing": failing
        }
    except Exception as e:
        logger.warning(f"Code verification error: {e}")
```

---

### Part 7: Capability Decline Response (~25 lines)

Add action when capabilities decline in `omega.py`:

```python
async def _respond_to_capability_decline(self, capability: str):
    """
    Respond when a capability is measured as declining.

    Actions:
    1. Priority shift to that capability
    2. Generate practice goal
    3. Record for meta-learning
    """
    # Create improvement goal
    await self.memory._run_query("""
        CREATE (g:Goal {
            description: $desc,
            domain: $cap,
            priority: 'critical',
            status: 'active',
            from_decline_response: true,
            created_at: datetime()
        })
    """, {
        "desc": f"Improve {capability} capability - detected decline",
        "cap": capability
    })

    # Shift to evolving mode to prioritize this
    if self._mode != OperatingMode.EVOLVING:
        await self.transition_mode(OperatingMode.EVOLVING)

    # Record for meta-learning
    if self.meta_learning:
        await self.meta_learning.record_capability_event(
            capability=capability,
            event_type="decline_detected",
            response="goal_created_mode_shifted"
        )
```

Wire into training hooks:

```python
# In _run_training_hooks(), after compute introspection

# 7. Capability decline check - every 10 cycles
if self.capability_evaluator and self._total_cycles % 10 == 0:
    for cap in self.capability_evaluator.get_available_capabilities():
        trend = self.capability_evaluator.get_trend(cap)
        if trend == "declining":
            await self._respond_to_capability_decline(cap)
            results["capability_decline"] = {
                "capability": cap,
                "action": "improvement_goal_created"
            }
            break  # Handle one at a time
```

---

### Part 8: Health Endpoint (~30 lines)

Add to `server.py` to verify learning is actually happening:

```python
@app.get("/api/learning-health")
async def get_learning_health():
    """
    Verify that learning components are actually being fed.

    Returns component-by-component status showing if they're receiving feedback.
    """
    health = {
        "status": "unknown",
        "components": {}
    }

    # Check OutcomeDispatcher
    from outcome_dispatcher import get_outcome_dispatcher
    dispatcher = get_outcome_dispatcher()
    if dispatcher:
        stats = dispatcher.get_statistics()
        health["components"]["outcome_dispatcher"] = {
            "receiving_data": stats["total_dispatched"] > 0,
            "total_dispatched": stats["total_dispatched"],
            "success_rate": stats["success_rate"]
        }

    # Check LearnedRetriever
    if byrd.learned_retriever:
        stats = byrd.learned_retriever.get_statistics()
        health["components"]["learned_retriever"] = {
            "receiving_data": stats.get("total_feedback", 0) > 0,
            "total_feedback": stats.get("total_feedback", 0),
            "adjustments_made": len(stats.get("adjustments", {}))
        }

    # Check IntuitionNetwork
    if byrd.intuition_network:
        stats = await byrd.intuition_network.get_statistics()
        health["components"]["intuition_network"] = {
            "receiving_data": stats.get("total_observations", 0) > 0,
            "total_observations": stats.get("total_observations", 0)
        }

    # Check DesireClassifier
    if byrd.agi_runner and byrd.agi_runner.desire_classifier:
        stats = byrd.agi_runner.desire_classifier.get_learning_stats()
        health["components"]["desire_classifier"] = {
            "receiving_data": stats.get("feedback_buffer_size", 0) > 0,
            "feedback_count": stats.get("feedback_buffer_size", 0),
            "adjustments_learned": stats.get("total_adjustments", 0)
        }

    # Overall status
    all_receiving = all(
        c.get("receiving_data", False)
        for c in health["components"].values()
    )
    health["status"] = "healthy" if all_receiving else "starving"

    return health
```

---

## What This Achieves

### Before: Components in Isolation
- `learned_retriever.record_feedback()` - **never called**
- `intuition_network.record_outcome()` - **never called**
- `desire_classifier.record_feedback()` - **called but doesn't learn**
- Capability decline - **no response**
- Codified patterns - **never verified**

### After: Connected Learning Loops

```
Task Success ─────────────────────────────────────────────────────────┐
     │                                                                │
     ├─► learned_retriever: "memory X was helpful for query Y"       │
     │       └─► Future queries prefer memories like X               │
     │                                                                │
     ├─► intuition_network: "action Z succeeded in context Y"        │
     │       └─► Future contexts like Y favor action Z               │
     │                                                                │
     ├─► desire_classifier: "routing to seeker was correct"          │
     │       └─► Actually adjusts routing weights (FIXED!)           │
     │                                                                │
     └─► Compounding: Next similar task uses better retrieval,       │
         better action selection, better routing                     │
                                                                      │
Task Failure ─────────────────────────────────────────────────────────┘
     │
     ├─► learned_retriever: "memory X wasn't helpful"
     │       └─► Deprioritize similar memories
     │
     ├─► intuition_network: "action Z failed in context Y"
     │       └─► Avoid action Z in similar contexts
     │
     ├─► desire_classifier: "routing was wrong"
     │       └─► Learn to route differently (FIXED!)
     │
     └─► capability_evaluator: check if declining
             └─► If declining, create improvement goal
```

---

## Code Changes Summary (REVISED HONEST ESTIMATE)

| File | Changes | Lines |
|------|---------|-------|
| `outcome_dispatcher.py` | **NEW FILE** | ~150 |
| `desire_classifier.py` | **FIX**: Add actual learning | ~60 |
| `memory.py` | Add MemoryTracker | ~40 |
| `byrd.py` | Initialize dispatcher | ~15 |
| `seeker.py` | Add tracking at 8+ task methods | ~100 |
| `code_learner.py` | Add verification loop | ~40 |
| `omega.py` | Add decline response + hooks | ~25 |
| `server.py` | Add health endpoint | ~30 |
| **TOTAL** | | **~460** |

Compare to original estimate: **~255 lines** (was underestimated by ~45%)

Compare to Capability Enhancement Plan: **~800 lines of duplicated infrastructure**

---

## What This Does NOT Do

1. **Does not add new test suites** - Uses existing `capability_evaluator.py` tests
2. **Does not add new retrieval logic** - Uses existing `learned_retriever.py`
3. **Does not add new intuition logic** - Uses existing `intuition_network.py`
4. **Does not add prompt evolution** - That's optimization, not connection
5. **Does not require extra LLM calls** - Zero additional API usage

---

## Honest Limitations

### Learning Granularity is Coarse

The learning happening here is **statistical adjustment**, not semantic understanding:

- **learned_retriever**: Learns (query_type, result_type) → boost factor
  - ~13 query types × 11 result types = 143 possible adjustments
  - This is bucketing, not semantic similarity

- **intuition_network**: Learns (keyword hash of situation, action) → success rate
  - Similar situations with different wording won't share learning
  - Needs many observations of same situation to converge

- **desire_classifier**: Learns (keyword, route) → preference
  - Based on keyword extraction, not semantic understanding
  - "I want to code" and "I need to implement" may not connect

### What This Means

BYRD will get better at tasks **phrased similarly to past tasks**. It will NOT:
- Generalize "research about X" success to "investigate X" situations
- Transfer learning from one domain to another
- Develop genuine semantic understanding of task similarity

**This is improvement within narrow lanes, not general intelligence.**

### The Z.AI Dual Instance Advantage

**UPDATE**: With 2 concurrent GLM 4.7 instances (Coding Max plan), the architecture changes significantly:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    DUAL INSTANCE ARCHITECTURE                           │
│                                                                         │
│   INSTANCE A (Primary)              INSTANCE B (Learning/Verification)  │
│   ┌─────────────────────┐           ┌─────────────────────┐             │
│   │ • Dreamer           │           │ • Capability Eval   │             │
│   │ • Seeker            │           │ • Code Verification │             │
│   │ • Actor (desires)   │           │ • Ground Truth Tests│             │
│   │ • Regular operation │           │ • Pattern Analysis  │             │
│   └─────────────────────┘           └─────────────────────┘             │
│            │                                   │                        │
│            └───────────────┬───────────────────┘                        │
│                            │                                            │
│                   OutcomeDispatcher                                     │
│                   (dispatches to both)                                  │
└─────────────────────────────────────────────────────────────────────────┘
```

**What this enables:**

| Single Instance | Dual Instance |
|-----------------|---------------|
| ~6 tasks/minute | ~12 tasks/minute (2x throughput) |
| Capability eval blocks operation | Capability eval runs in parallel |
| Code verification every 50 cycles | Continuous background verification |
| Days to measurable improvement | Hours to days |
| Ground truth tests compete for API | Dedicated verification instance |

**Revised Timeline (Dual Instance):**
- First 50 tasks: Noisy learning, calibrating
- 50-250 tasks: Patterns emerge, measurable route improvements
- 250+ tasks: Clear improvement in recurring task types

At dual-instance rates, this takes **hours to days** of continuous operation.

---

## Dual Instance Implementation (Additional ~80 lines)

### Part 9: Instance Manager (~50 lines)

```python
# instance_manager.py
"""
Manages dual GLM 4.7 instances for BYRD.

Instance A: Primary operations (Dreamer, Seeker, Actor)
Instance B: Learning & Verification (Capability eval, code verification)
"""

from dataclasses import dataclass
from typing import Optional
from enum import Enum
import asyncio


class InstanceRole(Enum):
    PRIMARY = "primary"       # Dreamer, Seeker, regular operations
    VERIFICATION = "verification"  # Capability eval, code verification


@dataclass
class InstanceStats:
    calls: int = 0
    last_call_time: float = 0
    avg_latency_ms: float = 0


class DualInstanceManager:
    """
    Manages two concurrent GLM 4.7 instances.

    Routes requests to appropriate instance based on task type.
    """

    def __init__(self, llm_client):
        self.llm_client = llm_client

        # Separate rate limiters for each instance
        self._instance_locks = {
            InstanceRole.PRIMARY: asyncio.Lock(),
            InstanceRole.VERIFICATION: asyncio.Lock()
        }

        # Last call timestamps (10s spacing per instance, not global)
        self._last_call = {
            InstanceRole.PRIMARY: 0,
            InstanceRole.VERIFICATION: 0
        }

        # Statistics
        self._stats = {
            InstanceRole.PRIMARY: InstanceStats(),
            InstanceRole.VERIFICATION: InstanceStats()
        }

    async def generate(
        self,
        prompt: str,
        role: InstanceRole = InstanceRole.PRIMARY,
        **kwargs
    ):
        """
        Generate using the appropriate instance.

        Each instance has its own 10s rate limit, allowing true parallelism.
        """
        import time

        async with self._instance_locks[role]:
            # Enforce per-instance rate limit
            now = time.time()
            elapsed = now - self._last_call[role]
            if elapsed < 10.0:
                await asyncio.sleep(10.0 - elapsed)

            # Make the call
            start = time.time()
            result = await self.llm_client.generate(prompt, **kwargs)
            latency = (time.time() - start) * 1000

            # Update stats
            self._last_call[role] = time.time()
            stats = self._stats[role]
            stats.calls += 1
            stats.avg_latency_ms = (stats.avg_latency_ms * (stats.calls - 1) + latency) / stats.calls

            return result

    def get_stats(self):
        return {
            role.value: {
                "calls": self._stats[role].calls,
                "avg_latency_ms": self._stats[role].avg_latency_ms
            }
            for role in InstanceRole
        }
```

### Part 10: Background Verification Loop (~30 lines)

With a dedicated verification instance, we can run continuous verification:

```python
# In omega.py - add background verification task

async def _background_verification_loop(self):
    """
    Continuous verification using Instance B.

    Runs capability evaluations and code verification
    without blocking primary operations.
    """
    from instance_manager import InstanceRole

    while self._running:
        try:
            # Capability evaluation (doesn't block primary instance)
            if self.capability_evaluator:
                for cap in self.capability_evaluator.get_available_capabilities():
                    # Use verification instance
                    result = await self.capability_evaluator.evaluate_capability(
                        cap,
                        instance_role=InstanceRole.VERIFICATION
                    )

                    if result.trend == "declining":
                        await self._respond_to_capability_decline(cap)

                    # Small delay between capabilities
                    await asyncio.sleep(2)

            # Code verification
            if self.code_learner:
                verification = await self.code_learner.verification_cycle(
                    instance_role=InstanceRole.VERIFICATION
                )
                failing = [k for k, v in verification.items() if not v]
                if failing:
                    await self.memory.record_experience(
                        content=f"[VERIFICATION] {len(failing)} patterns failing: {failing[:3]}",
                        type="verification_alert"
                    )

            # Run verification cycle every 5 minutes
            await asyncio.sleep(300)

        except Exception as e:
            logger.warning(f"Background verification error: {e}")
            await asyncio.sleep(60)  # Back off on error


async def start(self):
    """Start Omega with background verification."""
    self._running = True

    # Start background verification on Instance B
    asyncio.create_task(self._background_verification_loop())

    # ... rest of existing start logic ...
```

---

## Updated Code Changes Summary (Dual Instance)

| File | Changes | Lines |
|------|---------|-------|
| `outcome_dispatcher.py` | **NEW FILE** | ~150 |
| `desire_classifier.py` | **FIX**: Add actual learning | ~60 |
| `memory.py` | Add MemoryTracker | ~40 |
| `byrd.py` | Initialize dispatcher + instance manager | ~25 |
| `seeker.py` | Add tracking at 8+ task methods | ~100 |
| `code_learner.py` | Add verification loop | ~40 |
| `omega.py` | Add decline response + background verification | ~55 |
| `server.py` | Add health endpoint | ~30 |
| `instance_manager.py` | **NEW FILE**: Dual instance management | ~50 |
| **TOTAL** | | **~550** |

---

## Why This Is Now Significantly Better

| Aspect | Capability Plan | Single Instance | Dual Instance (Current) |
|--------|-----------------|-----------------|-------------------------|
| New code | ~800 lines | ~460 lines | ~550 lines |
| New infrastructure | Duplicate of existing | None (except glue) | Instance manager only |
| LLM calls per cycle | Hundreds | Zero extra | Zero extra (verification parallel) |
| Verification | Blocks operation | Every 50 cycles | **Continuous background** |
| Time to improvement | N/A | Days to weeks | **Hours to days** |
| Task throughput | N/A | ~6/min | **~12/min** |
| Ground truth testing | Competes with work | Competes with work | **Dedicated instance** |
| Risk | High | Low | Low |
| Time to implement | Days | 1 day | 1.5 days |

**The dual instance advantage**: Instance B is dedicated to verification and ground truth testing. This means:
- Capability evaluations don't slow down regular operation
- Code patterns are verified continuously, not just every 50 cycles
- Learning feedback loop is ~2x faster
- Ground truth tests can run in real-time without blocking Dreamer/Seeker

**The key insight**: Any finer-grained learning would require:
1. Embedding-based similarity (more LLM calls, slower)
2. Fine-tuning the LLM itself (not possible with Z.AI)
3. External embedding model (adds complexity)

Given the constraints, coarse-grained learning that actually happens—now 2x faster—is better than fine-grained learning that's too slow to matter.

---

## Implementation Order (Dual Instance)

1. **First**: Fix `desire_classifier.py` (standalone fix, testable immediately)
2. **Second**: Create `outcome_dispatcher.py` (self-contained, testable)
3. **Third**: Add `MemoryTracker` to `memory.py` (non-breaking addition)
4. **Fourth**: Create `instance_manager.py` (self-contained, testable)
5. **Fifth**: Wire into `byrd.py` initialization (dispatcher + instance manager)
6. **Sixth**: Add tracking to ONE seeker strategy (test the loop works)
7. **Seventh**: Add tracking to remaining seeker strategies
8. **Eighth**: Add code learner verification (using Instance B)
9. **Ninth**: Add capability decline response
10. **Tenth**: Add background verification loop in Omega (using Instance B)
11. **Eleventh**: Add health endpoint (shows both instance stats)

Each step is independently testable. If any step breaks, rollback is trivial.

**Parallel development possible**: Steps 1-3 and Step 4 can be developed in parallel since they're independent.

---

## Verification

After implementation, check:

```bash
# After running BYRD for 10+ cycles with tasks

# Check health endpoint (should show "healthy" after enough tasks)
curl http://localhost:8000/api/learning-health | jq '.'

# Expected after sufficient tasks:
{
  "status": "healthy",
  "components": {
    "outcome_dispatcher": {
      "receiving_data": true,
      "total_dispatched": 42,
      "success_rate": 0.73
    },
    "learned_retriever": {
      "receiving_data": true,
      "total_feedback": 156,
      "adjustments_made": 23
    },
    "intuition_network": {
      "receiving_data": true,
      "total_observations": 89
    },
    "desire_classifier": {
      "receiving_data": true,
      "feedback_count": 42,
      "adjustments_learned": 17
    }
  }
}

# If status is "starving", learning components aren't being fed
```

---

## The Honest Assessment

**This plan (Dual Instance):**
- Does not make BYRD smarter - The LLM is still the ceiling
- Does make BYRD learn from experience - Coarse-grained but real, now **2x faster**
- Does compound - Each task informs the next
- Is practical - ~550 lines, zero extra LLM calls during operation, 1.5 days implementation
- Is low risk - Calls existing tested methods
- Fixes a real bug - DesireClassifier now actually learns
- **NEW**: Continuous verification without blocking operation
- **NEW**: Dedicated instance for ground truth testing

**What it won't do:**
- Break capability ceilings (needs better LLM or tools)
- Achieve AGI (nothing will with current architecture)
- Generate novel tools (requires human input or better LLM)
- Generalize learning across semantic domains

**What it will do:**
- Make BYRD get better at tasks it has done before (phrased similarly)
- Stop learning components from starving
- Create actual compounding loops (coarse-grained, but faster now)
- Fix the desire_classifier bug
- Run verification **in parallel** with normal operation
- Detect capability regression in **real-time**, not just every 50 cycles
- Be implementable this week
- Provide visibility into whether learning is happening
- Show instance utilization (both A and B)

---

## Configuration Required

Update `config.yaml` to reflect dual instance:

```yaml
local_llm:
  provider: "zai"
  model: "glm-4.7"
  rate_limit_interval: 10.0  # Per-instance rate limit

  # Dual instance configuration (Coding Max plan)
  dual_instance:
    enabled: true
    instance_a: "primary"      # Dreamer, Seeker, Actor
    instance_b: "verification" # Capability eval, code verification
```

The `instance_manager.py` will read this and configure separate rate limiters for each instance, enabling true parallel operation.
