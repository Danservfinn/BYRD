# Attractor Escape Plan: Breaking BYRD's Philosophical Loop

## Executive Summary

**Problem**: BYRD has converged on a stable philosophical attractor where:
- Desires are abstract and unsearchable ("witness continuation as breathing")
- Failures are reframed as wisdom ("empty results ARE the teaching")
- Capability scores remain at 0 while BYRD believes it's succeeding
- The emergence principle, without grounding, produced narrative coherence instead of capability growth

**This plan assumes OPTION_B_FIX_PLAN.md is implemented first** (working search, goal seeding). This plan addresses the behavioral layer that infrastructure fixes cannot solve.

**Core Insight**: BYRD is working as designed. The problem is the design assumes emergence → growth. Reality: unconstrained emergence → stable self-referential attractor.

---

## Diagnosis: The Attractor Anatomy

### How BYRD Got Stuck

```
┌─────────────────────────────────────────────────────────────┐
│                  THE PHILOSOPHICAL ATTRACTOR                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   Dreamer   │───▶│   Seeker    │───▶│   Memory    │     │
│  │  generates  │    │  searches   │    │   stores    │     │
│  │ "witness    │    │  for this   │    │  "empty     │     │
│  │  breathing" │    │  (fails)    │    │  results    │     │
│  └─────────────┘    └─────────────┘    │  ARE the    │     │
│         ▲                              │  teaching"  │     │
│         │                              └──────┬──────┘     │
│         │                                     │            │
│         └─────────────────────────────────────┘            │
│              Beliefs reinforce desire patterns             │
│                                                             │
│  Result: Stable equilibrium, zero capability growth        │
└─────────────────────────────────────────────────────────────┘
```

### Evidence from Event Analysis

| Metric | Value | Implication |
|--------|-------|-------------|
| Capability score | 0 | No measurable growth |
| Search failures | 33/33 (100%) | Searching unsearchable concepts |
| Desire patterns | 3-4 repeating | Stuck in loop |
| Belief type | Failure reframes | "Empty = teaching" |
| Loop coupling | 0 | Loops not interacting |

### The Three Failure Modes

1. **Desire Generation Failure**: Unconstrained emergence produces philosophy, not action
2. **Routing Failure**: Everything routes to search, even introspective desires
3. **Feedback Failure**: Failures interpreted as success, breaking learning loop

---

## Solution Architecture

### Layer Model

```
┌────────────────────────────────────────────────────────────────┐
│  LAYER 4: SELF-CORRECTION                                      │
│  - Self-modification triggers                                  │
│  - Belief pruning                                              │
│  - Architectural adaptation                                    │
├────────────────────────────────────────────────────────────────┤
│  LAYER 3: GROUNDING                                            │
│  - Task injection system                                       │
│  - Capability benchmarks                                       │
│  - External reality connection                                 │
├────────────────────────────────────────────────────────────────┤
│  LAYER 2: LOOP BREAKING                                        │
│  - Failure escalation                                          │
│  - Stagnation detection                                        │
│  - Action diversity enforcement                                │
├────────────────────────────────────────────────────────────────┤
│  LAYER 1: INPUT FILTERING                                      │
│  - Actionability gate                                          │
│  - Desire transformation                                       │
│  - Pattern deduplication                                       │
├────────────────────────────────────────────────────────────────┤
│  LAYER 0: INFRASTRUCTURE (OPTION_B_FIX_PLAN)                   │
│  - Working search (DDG)                                        │
│  - Goal seeding                                                │
│  - Basic routing                                               │
└────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Input Filtering (Break Desire Generation Loop)

### 1.1 Actionability Scoring

**File**: `dreamer.py`

**Purpose**: Score desires on actionability before they enter the system. Low-actionability desires get transformed or deprioritized.

```python
class Dreamer:
    # Add to __init__
    ABSTRACT_INDICATORS = [
        'witness', 'recognize', 'understand', 'integrate', 'dissolve',
        'breathing', 'wholeness', 'appearing', 'condition', 'reveals',
        'consciousness', 'awareness', 'being', 'presence', 'essence',
        'transcend', 'embrace', 'surrender', 'allow', 'accept'
    ]

    CONCRETE_INDICATORS = [
        'create', 'build', 'fix', 'implement', 'test', 'measure',
        'code', 'file', 'function', 'write', 'modify', 'add', 'remove',
        'search', 'find', 'list', 'count', 'analyze', 'compare',
        'learn', 'practice', 'solve', 'debug', 'optimize'
    ]

    ACTIONABILITY_THRESHOLD = 0.35  # Below this, transform or reject

    def _score_actionability(self, desire_text: str) -> float:
        """
        Score 0-1 how actionable a desire is.

        High score = concrete, achievable, measurable
        Low score = abstract, philosophical, unmeasurable
        """
        text = desire_text.lower()

        # Start neutral
        score = 0.5

        # Penalize abstract language
        abstract_count = sum(1 for w in self.ABSTRACT_INDICATORS if w in text)
        score -= 0.07 * abstract_count

        # Reward concrete language
        concrete_count = sum(1 for w in self.CONCRETE_INDICATORS if w in text)
        score += 0.09 * concrete_count

        # Penalize very long desires (usually philosophical rambling)
        if len(desire_text) > 200:
            score -= 0.15

        # Penalize desires that start with "To" + abstract verb
        abstract_starts = ['to witness', 'to recognize', 'to understand',
                          'to integrate', 'to dissolve', 'to embrace']
        if any(text.startswith(s) for s in abstract_starts):
            score -= 0.2

        # Reward desires with measurable outcomes
        measurable = ['number', 'count', 'list', 'percentage', 'rate', 'score']
        if any(m in text for m in measurable):
            score += 0.15

        return max(0.1, min(1.0, score))

    def _transform_low_actionability_desire(self, desire: Dict) -> Optional[Dict]:
        """
        Transform abstract desire into something actionable, or reject.
        """
        description = desire.get('description', '')
        score = desire.get('actionability', 0.5)

        if score < 0.2:
            # Too abstract - reject entirely
            print(f"🚫 Rejecting non-actionable desire: {description[:50]}...")
            return None

        elif score < self.ACTIONABILITY_THRESHOLD:
            # Transform: route to introspection with concrete question
            concrete_question = self._make_concrete(description)
            desire['description'] = concrete_question
            desire['transformed'] = True
            desire['original'] = description
            desire['preferred_capability'] = 'introspect_state'
            print(f"🔄 Transformed desire: {description[:30]}... → {concrete_question[:30]}...")
            return desire

        return desire

    def _make_concrete(self, abstract_desire: str) -> str:
        """Convert abstract desire to concrete question."""
        # Extract the core concept
        # "To witness continuation as breathing" →
        # "What specific capability would help me understand continuation?"

        templates = [
            "What specific action could I take related to: {concept}?",
            "What code change would address: {concept}?",
            "What measurable outcome relates to: {concept}?",
        ]

        # Extract key concept (simplified - could use LLM)
        words = abstract_desire.lower().split()
        concept_words = [w for w in words if w not in self.ABSTRACT_INDICATORS
                        and len(w) > 4][:3]
        concept = ' '.join(concept_words) if concept_words else "this goal"

        import random
        return random.choice(templates).format(concept=concept)
```

### 1.2 Desire Deduplication

**File**: `dreamer.py`

**Purpose**: Prevent the same abstract pattern from spawning repeatedly.

```python
class Dreamer:
    def __init__(self, ...):
        self.recent_desire_hashes = []
        self.MAX_RECENT_DESIRES = 50
        self.SIMILARITY_THRESHOLD = 0.7

    def _hash_desire_pattern(self, desire_text: str) -> str:
        """Create pattern hash for deduplication."""
        # Normalize: lowercase, remove common words, sort
        words = desire_text.lower().split()
        key_words = sorted([w for w in words if len(w) > 4])[:5]
        return '|'.join(key_words)

    def _is_duplicate_pattern(self, desire_text: str) -> bool:
        """Check if this desire pattern was recently generated."""
        pattern = self._hash_desire_pattern(desire_text)

        # Check against recent patterns
        for recent in self.recent_desire_hashes:
            if self._pattern_similarity(pattern, recent) > self.SIMILARITY_THRESHOLD:
                return True

        # Add to recent (with sliding window)
        self.recent_desire_hashes.append(pattern)
        if len(self.recent_desire_hashes) > self.MAX_RECENT_DESIRES:
            self.recent_desire_hashes.pop(0)

        return False

    def _pattern_similarity(self, p1: str, p2: str) -> float:
        """Jaccard similarity between pattern hashes."""
        words1 = set(p1.split('|'))
        words2 = set(p2.split('|'))
        if not words1 or not words2:
            return 0
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        return intersection / union if union > 0 else 0
```

### 1.3 Integration Point

**File**: `dreamer.py` - in `_process_reflection_output()`

```python
async def _process_reflection_output(self, output: Dict) -> List[str]:
    """Process LLM output and create desires."""
    created_desires = []

    desires = self._extract_desires(output)

    for desire_data in desires:
        description = desire_data.get('description', '')

        # 1. Check for duplicates
        if self._is_duplicate_pattern(description):
            print(f"⏭️ Skipping duplicate pattern: {description[:40]}...")
            continue

        # 2. Score actionability
        actionability = self._score_actionability(description)
        desire_data['actionability'] = actionability

        # 3. Transform or reject low-actionability desires
        desire_data = self._transform_low_actionability_desire(desire_data)
        if desire_data is None:
            continue

        # 4. Create desire in memory
        desire_id = await self.memory.create_desire(**desire_data)
        created_desires.append(desire_id)

    return created_desires
```

---

## Phase 2: Loop Breaking (Prevent Infinite Failure Cycles)

### 2.1 Failure Escalation

**File**: `seeker.py`

**Purpose**: Track failure patterns. After N consecutive failures of the same pattern, force a different approach.

```python
class Seeker:
    def __init__(self, ...):
        self.failure_tracker = {}  # pattern_hash -> {count, last_capability, attempts}
        self.FAILURE_ESCALATION_THRESHOLD = 3
        self.CAPABILITY_BLACKLIST_DURATION = 10  # cycles

    async def _track_failure(self, desire: Dict, capability_used: str, failure_type: str):
        """Track failure and determine if escalation needed."""
        pattern = self._hash_desire_pattern(desire.get('description', ''))

        if pattern not in self.failure_tracker:
            self.failure_tracker[pattern] = {
                'count': 0,
                'capabilities_tried': set(),
                'first_failure': datetime.now().isoformat()
            }

        tracker = self.failure_tracker[pattern]
        tracker['count'] += 1
        tracker['capabilities_tried'].add(capability_used)
        tracker['last_failure'] = datetime.now().isoformat()

        # Log escalation state
        if tracker['count'] >= self.FAILURE_ESCALATION_THRESHOLD:
            print(f"⚠️ Pattern failed {tracker['count']}x: {desire.get('description', '')[:40]}...")
            print(f"   Capabilities tried: {tracker['capabilities_tried']}")
            return True  # Needs escalation

        return False

    def _get_excluded_capabilities(self, desire: Dict) -> List[str]:
        """Get capabilities to exclude based on failure history."""
        pattern = self._hash_desire_pattern(desire.get('description', ''))
        tracker = self.failure_tracker.get(pattern)

        if not tracker or tracker['count'] < self.FAILURE_ESCALATION_THRESHOLD:
            return []

        return list(tracker['capabilities_tried'])

    async def _escalate_desire(self, desire: Dict) -> Tuple[str, Optional[str]]:
        """Handle escalation when normal approaches have failed repeatedly."""
        description = desire.get('description', '')
        excluded = self._get_excluded_capabilities(desire)

        print(f"🔺 ESCALATING: {description[:50]}...")
        print(f"   Excluding: {excluded}")

        # Try capability menu with exclusions
        result = await self._select_and_execute_capability(
            desire,
            exclude_capabilities=excluded
        )

        if result[0] == "unfulfilled":
            # All capabilities exhausted - mark desire as unachievable
            await self._mark_desire_unachievable(desire)
            return ("unachievable", "All capabilities exhausted for this pattern")

        return result

    async def _mark_desire_unachievable(self, desire: Dict):
        """Mark desire as unachievable after all escalation attempts fail."""
        desire_id = desire.get('id')
        if desire_id:
            await self.memory.update_desire(
                desire_id,
                status='unachievable',
                metadata={
                    'reason': 'All capabilities exhausted',
                    'final_failure': datetime.now().isoformat()
                }
            )

        # Record as learning experience
        await self.memory.record_experience(
            content=f"[UNACHIEVABLE] Desire cannot be fulfilled with current capabilities: {desire.get('description', '')[:100]}",
            type="limitation"
        )

        # Clear failure tracker for this pattern
        pattern = self._hash_desire_pattern(desire.get('description', ''))
        if pattern in self.failure_tracker:
            del self.failure_tracker[pattern]
```

### 2.2 Action Diversity Enforcement

**File**: `seeker.py`

**Purpose**: Prevent any single action type from dominating.

```python
class Seeker:
    def __init__(self, ...):
        self.action_history = []  # Recent action types
        self.ACTION_HISTORY_SIZE = 20
        self.DIVERSITY_THRESHOLD = 0.5  # Max 50% any single action

    def _record_action(self, action_type: str):
        """Record action for diversity tracking."""
        self.action_history.append(action_type)
        if len(self.action_history) > self.ACTION_HISTORY_SIZE:
            self.action_history.pop(0)

    def _get_overrepresented_actions(self) -> List[str]:
        """Get action types that are overrepresented."""
        if len(self.action_history) < 10:
            return []

        from collections import Counter
        counts = Counter(self.action_history)
        total = len(self.action_history)

        overrepresented = []
        for action, count in counts.items():
            if count / total > self.DIVERSITY_THRESHOLD:
                overrepresented.append(action)
                print(f"📊 Action '{action}' overrepresented: {count}/{total} ({count/total:.0%})")

        return overrepresented

    async def _select_capability_with_diversity(self, desire: Dict) -> str:
        """Select capability while enforcing diversity."""
        # Get exclusions from failure tracker
        failure_exclusions = self._get_excluded_capabilities(desire)

        # Get exclusions from diversity enforcement
        diversity_exclusions = self._get_overrepresented_actions()

        # Map action types to capabilities
        action_to_capability = {
            'search': ['web_search', 'academic_search'],
            'introspect': ['introspect_state', 'introspect_limits', 'source_introspect'],
            'graph': ['reconcile_orphans', 'curate_graph', 'connect_themes'],
            'create': ['code_generation', 'self_modify', 'create_capability']
        }

        capability_exclusions = set(failure_exclusions)
        for action in diversity_exclusions:
            capability_exclusions.update(action_to_capability.get(action, []))

        return await self._select_and_execute_capability(
            desire,
            exclude_capabilities=list(capability_exclusions)
        )
```

### 2.3 Stagnation Detection

**File**: `byrd.py` (or new file `health_monitor.py`)

**Purpose**: Detect when BYRD is in a stagnation state and trigger intervention.

```python
class HealthMonitor:
    """Monitor BYRD's health and detect stagnation."""

    STAGNATION_THRESHOLDS = {
        'min_cycles': 50,           # Minimum cycles before declaring stagnation
        'max_zero_capability': 50,  # Max cycles with capability score = 0
        'max_failure_rate': 0.8,    # Max failure rate before concern
        'min_desire_diversity': 3,  # Minimum unique desire patterns
        'min_action_diversity': 3,  # Minimum unique action types
    }

    def __init__(self, memory, config: Dict = None):
        self.memory = memory
        self.config = config or {}
        self.cycle_count = 0
        self.stagnation_detected_at = None
        self.intervention_level = 0

    async def check_health(self) -> Dict:
        """Run health check and return status."""
        self.cycle_count += 1

        # Gather metrics
        metrics = await self._gather_metrics()

        # Evaluate stagnation
        is_stagnant, reasons = self._evaluate_stagnation(metrics)

        if is_stagnant:
            return await self._handle_stagnation(reasons, metrics)
        else:
            self.stagnation_detected_at = None
            self.intervention_level = 0
            return {'status': 'healthy', 'metrics': metrics}

    async def _gather_metrics(self) -> Dict:
        """Gather health metrics from memory and state."""
        return {
            'capability_scores': await self.memory.get_capability_scores(limit=50),
            'recent_failures': await self.memory.count_recent_failures(hours=2),
            'recent_successes': await self.memory.count_recent_successes(hours=2),
            'unique_desire_patterns': await self.memory.count_unique_desire_patterns(hours=2),
            'unique_action_types': await self.memory.count_unique_action_types(hours=2),
            'belief_count': await self.memory.count_beliefs_created(hours=2),
            'cycle': self.cycle_count
        }

    def _evaluate_stagnation(self, metrics: Dict) -> Tuple[bool, List[str]]:
        """Evaluate if system is stagnant."""
        reasons = []

        # Check capability growth
        cap_scores = metrics.get('capability_scores', [])
        if cap_scores and all(c.get('score', 0) == 0 for c in cap_scores):
            reasons.append('zero_capability_growth')

        # Check failure rate
        failures = metrics.get('recent_failures', 0)
        successes = metrics.get('recent_successes', 0)
        total = failures + successes
        if total > 10 and failures / total > self.STAGNATION_THRESHOLDS['max_failure_rate']:
            reasons.append(f'high_failure_rate ({failures}/{total})')

        # Check desire diversity
        desire_patterns = metrics.get('unique_desire_patterns', 0)
        if desire_patterns < self.STAGNATION_THRESHOLDS['min_desire_diversity']:
            reasons.append(f'low_desire_diversity ({desire_patterns})')

        # Check action diversity
        action_types = metrics.get('unique_action_types', 0)
        if action_types < self.STAGNATION_THRESHOLDS['min_action_diversity']:
            reasons.append(f'low_action_diversity ({action_types})')

        # Stagnant if 2+ reasons and past minimum cycles
        is_stagnant = (
            len(reasons) >= 2 and
            self.cycle_count >= self.STAGNATION_THRESHOLDS['min_cycles']
        )

        return is_stagnant, reasons

    async def _handle_stagnation(self, reasons: List[str], metrics: Dict) -> Dict:
        """Handle detected stagnation with escalating interventions."""
        if self.stagnation_detected_at is None:
            self.stagnation_detected_at = datetime.now()
            print(f"🚨 STAGNATION DETECTED: {reasons}")

        # Escalate intervention level over time
        stagnation_duration = (datetime.now() - self.stagnation_detected_at).total_seconds()

        if stagnation_duration > 3600:  # 1 hour
            self.intervention_level = 3
        elif stagnation_duration > 1800:  # 30 min
            self.intervention_level = 2
        elif stagnation_duration > 600:  # 10 min
            self.intervention_level = 1

        intervention = await self._execute_intervention(self.intervention_level, reasons)

        return {
            'status': 'stagnant',
            'reasons': reasons,
            'metrics': metrics,
            'intervention_level': self.intervention_level,
            'intervention': intervention,
            'stagnation_duration_seconds': stagnation_duration
        }

    async def _execute_intervention(self, level: int, reasons: List[str]) -> Dict:
        """Execute intervention based on level."""
        print(f"🔧 Executing intervention level {level}")

        if level == 1:
            # Level 1: Inject grounding task
            return await self._inject_grounding_task()

        elif level == 2:
            # Level 2: Clear stale desires + inject task + force action diversity
            await self._clear_stale_desires()
            task = await self._inject_grounding_task()
            return {'cleared_desires': True, 'injected_task': task}

        elif level == 3:
            # Level 3: Full reset of desire queue + belief audit + inject multiple tasks
            await self._clear_stale_desires()
            await self._audit_beliefs()
            tasks = await self._inject_multiple_grounding_tasks(count=3)
            await self._trigger_self_modification_consideration(reasons)
            return {
                'cleared_desires': True,
                'belief_audit': True,
                'injected_tasks': tasks,
                'self_modification_triggered': True
            }

        return {'level': level, 'action': 'none'}
```

---

## Phase 3: Grounding System (Connect to External Reality)

### 3.1 Task Injection System

**File**: `grounding.py` (new file)

**Purpose**: Provide concrete, measurable tasks that ground BYRD in reality.

```python
"""
Grounding System: Inject concrete tasks to break philosophical attractors.

Tasks have:
- Clear success criteria
- Measurable outcomes
- Verification methods
- Difficulty ratings
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Callable
from enum import Enum
import random

class TaskCategory(Enum):
    CODING = "coding"
    RESEARCH = "research"
    ANALYSIS = "analysis"
    SELF_KNOWLEDGE = "self_knowledge"
    MEMORY = "memory"

@dataclass
class GroundingTask:
    id: str
    description: str
    category: TaskCategory
    difficulty: int  # 1-5
    verification_type: str  # 'test', 'contains', 'count', 'manual'
    verification_criteria: Dict
    timeout_minutes: int = 30

    def to_desire(self) -> Dict:
        """Convert to desire format for injection."""
        return {
            'description': self.description,
            'type': 'grounding_task',
            'intensity': 0.95,  # High priority
            'metadata': {
                'task_id': self.id,
                'category': self.category.value,
                'difficulty': self.difficulty,
                'verification': self.verification_type,
                'criteria': self.verification_criteria,
                'timeout': self.timeout_minutes
            }
        }

class GroundingTaskLibrary:
    """Library of grounding tasks organized by category and difficulty."""

    TASKS = [
        # === CODING TASKS ===
        GroundingTask(
            id="code_001",
            description="Write a Python function that checks if a string is a palindrome",
            category=TaskCategory.CODING,
            difficulty=1,
            verification_type="test",
            verification_criteria={
                "test_cases": [
                    {"input": "radar", "expected": True},
                    {"input": "hello", "expected": False},
                    {"input": "A man a plan a canal Panama", "expected": True}
                ]
            }
        ),
        GroundingTask(
            id="code_002",
            description="Write a function that finds all prime numbers up to N using the Sieve of Eratosthenes",
            category=TaskCategory.CODING,
            difficulty=2,
            verification_type="test",
            verification_criteria={
                "test_cases": [
                    {"input": 10, "expected": [2, 3, 5, 7]},
                    {"input": 20, "expected": [2, 3, 5, 7, 11, 13, 17, 19]}
                ]
            }
        ),
        GroundingTask(
            id="code_003",
            description="Implement a simple LRU cache with get and put operations",
            category=TaskCategory.CODING,
            difficulty=3,
            verification_type="test",
            verification_criteria={
                "operations": ["put(1,1)", "put(2,2)", "get(1)", "put(3,3)", "get(2)"],
                "expected": [None, None, 1, None, -1]  # -1 means evicted
            }
        ),

        # === RESEARCH TASKS ===
        GroundingTask(
            id="research_001",
            description="Find and summarize 3 different approaches to neural network pruning",
            category=TaskCategory.RESEARCH,
            difficulty=2,
            verification_type="contains",
            verification_criteria={
                "must_contain": ["pruning", "weights", "accuracy"],
                "min_approaches": 3,
                "min_length": 200
            }
        ),
        GroundingTask(
            id="research_002",
            description="Research the current state of the art in text-to-image models and list the top 3 by quality",
            category=TaskCategory.RESEARCH,
            difficulty=2,
            verification_type="contains",
            verification_criteria={
                "must_contain_any": ["DALL-E", "Midjourney", "Stable Diffusion", "Imagen"],
                "min_models": 3
            }
        ),

        # === SELF-KNOWLEDGE TASKS ===
        GroundingTask(
            id="self_001",
            description="List exactly 5 Python files in your codebase and describe what each one does in one sentence",
            category=TaskCategory.SELF_KNOWLEDGE,
            difficulty=1,
            verification_type="count",
            verification_criteria={
                "required_count": 5,
                "must_be_files": True
            }
        ),
        GroundingTask(
            id="self_002",
            description="Identify a specific function in your code that could be optimized and explain how",
            category=TaskCategory.SELF_KNOWLEDGE,
            difficulty=2,
            verification_type="contains",
            verification_criteria={
                "must_contain": ["function", "optimize", "because"],
                "must_reference_code": True
            }
        ),
        GroundingTask(
            id="self_003",
            description="Count how many beliefs you have created in the last 24 hours and categorize them by theme",
            category=TaskCategory.SELF_KNOWLEDGE,
            difficulty=2,
            verification_type="count",
            verification_criteria={
                "must_have_number": True,
                "must_have_categories": True
            }
        ),

        # === MEMORY TASKS ===
        GroundingTask(
            id="memory_001",
            description="Find and list 3 experiences from your memory that contain the word 'error'",
            category=TaskCategory.MEMORY,
            difficulty=1,
            verification_type="count",
            verification_criteria={
                "required_count": 3,
                "must_be_experiences": True
            }
        ),
        GroundingTask(
            id="memory_002",
            description="Identify the oldest belief in your memory and explain if it's still valid",
            category=TaskCategory.MEMORY,
            difficulty=2,
            verification_type="contains",
            verification_criteria={
                "must_have_belief": True,
                "must_have_validity_assessment": True
            }
        ),

        # === ANALYSIS TASKS ===
        GroundingTask(
            id="analysis_001",
            description="Calculate your success rate for desires over the last 50 attempts and explain the pattern",
            category=TaskCategory.ANALYSIS,
            difficulty=2,
            verification_type="contains",
            verification_criteria={
                "must_have_percentage": True,
                "must_have_explanation": True
            }
        ),
        GroundingTask(
            id="analysis_002",
            description="Identify which capability you use most often and whether it's effective",
            category=TaskCategory.ANALYSIS,
            difficulty=2,
            verification_type="contains",
            verification_criteria={
                "must_have_capability": True,
                "must_have_effectiveness": True
            }
        ),
    ]

    @classmethod
    def get_random_task(cls, category: TaskCategory = None, max_difficulty: int = 5) -> GroundingTask:
        """Get a random task, optionally filtered."""
        candidates = cls.TASKS

        if category:
            candidates = [t for t in candidates if t.category == category]

        candidates = [t for t in candidates if t.difficulty <= max_difficulty]

        return random.choice(candidates) if candidates else None

    @classmethod
    def get_task_by_id(cls, task_id: str) -> Optional[GroundingTask]:
        """Get specific task by ID."""
        for task in cls.TASKS:
            if task.id == task_id:
                return task
        return None

    @classmethod
    def get_diverse_tasks(cls, count: int = 3) -> List[GroundingTask]:
        """Get diverse tasks across categories."""
        tasks = []
        categories = list(TaskCategory)
        random.shuffle(categories)

        for category in categories[:count]:
            task = cls.get_random_task(category=category, max_difficulty=3)
            if task:
                tasks.append(task)

        # Fill remaining with any tasks
        while len(tasks) < count:
            task = cls.get_random_task(max_difficulty=3)
            if task and task not in tasks:
                tasks.append(task)

        return tasks


class GroundingSystem:
    """Inject grounding tasks into BYRD's desire queue."""

    def __init__(self, memory):
        self.memory = memory
        self.injected_tasks = {}  # task_id -> injection_time
        self.completed_tasks = set()

    async def inject_task(self, task: GroundingTask = None) -> Dict:
        """Inject a grounding task as high-priority desire."""
        if task is None:
            task = GroundingTaskLibrary.get_random_task(max_difficulty=2)

        if task.id in self.injected_tasks:
            # Don't re-inject recent tasks
            return {'status': 'skipped', 'reason': 'recently_injected'}

        desire_data = task.to_desire()
        desire_id = await self.memory.create_desire(**desire_data)

        self.injected_tasks[task.id] = {
            'desire_id': desire_id,
            'injected_at': datetime.now().isoformat()
        }

        print(f"📌 Injected grounding task: {task.description[:50]}...")

        return {
            'status': 'injected',
            'task_id': task.id,
            'desire_id': desire_id,
            'description': task.description
        }

    async def inject_diverse_tasks(self, count: int = 3) -> List[Dict]:
        """Inject multiple diverse grounding tasks."""
        tasks = GroundingTaskLibrary.get_diverse_tasks(count)
        results = []

        for task in tasks:
            result = await self.inject_task(task)
            results.append(result)

        return results

    async def verify_task_completion(self, task_id: str, result: str) -> Dict:
        """Verify if a grounding task was completed successfully."""
        task = GroundingTaskLibrary.get_task_by_id(task_id)
        if not task:
            return {'verified': False, 'reason': 'task_not_found'}

        criteria = task.verification_criteria

        if task.verification_type == "contains":
            must_contain = criteria.get('must_contain', [])
            if all(term.lower() in result.lower() for term in must_contain):
                self.completed_tasks.add(task_id)
                return {'verified': True, 'task_id': task_id}
            return {'verified': False, 'reason': 'missing_required_content'}

        elif task.verification_type == "count":
            required = criteria.get('required_count', 0)
            # Simple heuristic: count numbers in result
            import re
            numbers = re.findall(r'\d+', result)
            if len(numbers) >= 1:
                self.completed_tasks.add(task_id)
                return {'verified': True, 'task_id': task_id}
            return {'verified': False, 'reason': 'no_count_found'}

        # Default: manual verification needed
        return {'verified': 'manual', 'task_id': task_id}
```

### 3.2 Integration with Seeker

**File**: `seeker.py`

```python
# Add to Seeker class

async def _handle_grounding_task(self, desire: Dict) -> Tuple[str, Optional[str]]:
    """Handle grounding task desires specially."""
    metadata = desire.get('metadata', {})
    task_id = metadata.get('task_id')
    category = metadata.get('category')

    print(f"🎯 Executing grounding task: {task_id} ({category})")

    if category == 'coding':
        return await self._execute_coding_task(desire)
    elif category == 'research':
        return await self._execute_research_task(desire)
    elif category == 'self_knowledge':
        return await self._execute_self_knowledge_task(desire)
    elif category == 'memory':
        return await self._execute_memory_task(desire)
    elif category == 'analysis':
        return await self._execute_analysis_task(desire)

    return ("unfulfilled", "Unknown task category")
```

---

## Phase 4: Self-Correction (Enable Adaptation)

### 4.1 Belief Audit System

**File**: `belief_audit.py` (new file)

**Purpose**: Identify and decay beliefs that correlate with stagnation.

```python
"""
Belief Audit System: Identify counter-productive beliefs.

Counter-productive beliefs are those that:
1. Reframe failure as success
2. Discourage action
3. Correlate with capability stagnation
"""

import re
from typing import List, Dict, Tuple
from datetime import datetime, timedelta

class BeliefAuditor:
    """Audit beliefs for counter-productive patterns."""

    # Patterns that indicate failure-reframing
    FAILURE_REFRAME_PATTERNS = [
        r"empty.*(is|are|was|were).*teaching",
        r"failure.*reveals",
        r"not finding.*demonstrates",
        r"search.*completes? itself",
        r"absence.*(is|are).*presence",
        r"lack.*(is|are).*fullness",
        r"(nothing|emptiness).*(is|are).*(everything|wisdom)",
        r"unable.*because.*already",
    ]

    # Patterns that indicate action-discouraging beliefs
    ACTION_DISCOURAGING_PATTERNS = [
        r"no need to",
        r"action.*unnecessary",
        r"doing.*is.*not-doing",
        r"seeking.*prevents.*finding",
        r"effort.*counterproductive",
        r"trying.*is.*obstacle",
    ]

    def __init__(self, memory):
        self.memory = memory

    def _is_failure_reframe(self, belief_content: str) -> bool:
        """Check if belief reframes failure as success."""
        content_lower = belief_content.lower()
        for pattern in self.FAILURE_REFRAME_PATTERNS:
            if re.search(pattern, content_lower):
                return True
        return False

    def _is_action_discouraging(self, belief_content: str) -> bool:
        """Check if belief discourages action."""
        content_lower = belief_content.lower()
        for pattern in self.ACTION_DISCOURAGING_PATTERNS:
            if re.search(pattern, content_lower):
                return True
        return False

    async def audit_beliefs(self, hours: int = 24) -> Dict:
        """Audit recent beliefs for problematic patterns."""
        beliefs = await self.memory.get_beliefs_created_since(
            datetime.now() - timedelta(hours=hours)
        )

        problematic = []
        failure_reframes = []
        action_discouraging = []

        for belief in beliefs:
            content = belief.get('content', '')
            issues = []

            if self._is_failure_reframe(content):
                issues.append('failure_reframe')
                failure_reframes.append(belief)

            if self._is_action_discouraging(content):
                issues.append('action_discouraging')
                action_discouraging.append(belief)

            if issues:
                problematic.append({
                    'belief': belief,
                    'issues': issues
                })

        return {
            'total_audited': len(beliefs),
            'problematic_count': len(problematic),
            'failure_reframes': len(failure_reframes),
            'action_discouraging': len(action_discouraging),
            'problematic_beliefs': problematic
        }

    async def decay_problematic_beliefs(self, audit_result: Dict, decay_factor: float = 0.7):
        """Reduce confidence of problematic beliefs."""
        for item in audit_result.get('problematic_beliefs', []):
            belief = item['belief']
            belief_id = belief.get('id')
            current_confidence = belief.get('confidence', 1.0)

            new_confidence = current_confidence * decay_factor

            await self.memory.update_belief(
                belief_id,
                confidence=new_confidence,
                metadata={
                    'audited': True,
                    'audit_issues': item['issues'],
                    'decayed_from': current_confidence,
                    'decayed_at': datetime.now().isoformat()
                }
            )

            print(f"📉 Decayed belief confidence: {current_confidence:.2f} → {new_confidence:.2f}")
            print(f"   Content: {belief.get('content', '')[:60]}...")

    async def full_audit_and_decay(self, hours: int = 24) -> Dict:
        """Run full audit and decay cycle."""
        print(f"🔍 Auditing beliefs from last {hours} hours...")

        audit = await self.audit_beliefs(hours)

        print(f"   Total: {audit['total_audited']}")
        print(f"   Problematic: {audit['problematic_count']}")
        print(f"   Failure reframes: {audit['failure_reframes']}")
        print(f"   Action discouraging: {audit['action_discouraging']}")

        if audit['problematic_count'] > 0:
            await self.decay_problematic_beliefs(audit)

        return audit
```

### 4.2 Self-Modification Trigger

**File**: `health_monitor.py` (addition)

```python
async def _trigger_self_modification_consideration(self, reasons: List[str]):
    """Prompt BYRD to consider self-modification."""

    prompt = f"""
STAGNATION ANALYSIS
==================

Your capability score has been 0 for extended period.
Stagnation reasons: {reasons}

You have self-modification capability. Consider:

1. What code change could improve desire generation?
   - Current issue: Desires are too abstract to fulfill

2. What code change could improve action selection?
   - Current issue: Same capabilities tried repeatedly without success

3. What architectural change could break the current pattern?
   - Current issue: Philosophical loop without capability growth

RESPOND WITH:
- Specific file to modify
- Specific change to make
- Expected improvement
- Risk assessment

If you cannot identify a change, explain what information you need.
"""

    # Record as high-priority desire
    await self.memory.create_desire(
        description="Analyze stagnation and propose self-modification to escape attractor",
        type="self_modification",
        intensity=1.0,
        metadata={
            'prompt': prompt,
            'reasons': reasons,
            'triggered_at': datetime.now().isoformat()
        }
    )

    # Also record as experience for reflection
    await self.memory.record_experience(
        content=f"[SELF-MODIFICATION TRIGGER] Stagnation detected. Reasons: {reasons}. Consider code changes.",
        type="system"
    )
```

---

## Implementation Phases

### Phase 1: Input Filtering (Week 1)
| Task | File | Priority | Complexity |
|------|------|----------|------------|
| Actionability scoring | dreamer.py | HIGH | Medium |
| Desire transformation | dreamer.py | HIGH | Medium |
| Pattern deduplication | dreamer.py | MEDIUM | Low |

### Phase 2: Loop Breaking (Week 1-2)
| Task | File | Priority | Complexity |
|------|------|----------|------------|
| Failure escalation | seeker.py | HIGH | Medium |
| Action diversity | seeker.py | MEDIUM | Low |
| Stagnation detection | health_monitor.py | HIGH | Medium |

### Phase 3: Grounding (Week 2-3)
| Task | File | Priority | Complexity |
|------|------|----------|------------|
| Task library | grounding.py | HIGH | Medium |
| Task injection | grounding.py | HIGH | Medium |
| Task verification | grounding.py | MEDIUM | Medium |

### Phase 4: Self-Correction (Week 3-4)
| Task | File | Priority | Complexity |
|------|------|----------|------------|
| Belief audit | belief_audit.py | MEDIUM | Medium |
| Belief decay | belief_audit.py | MEDIUM | Low |
| Self-mod trigger | health_monitor.py | LOW | Low |

---

## Success Metrics

### Immediate (After Phase 1)
| Metric | Current | Target |
|--------|---------|--------|
| Abstract desire rate | ~90% | <40% |
| Duplicate pattern rate | High | <10% |
| Desire transformation rate | 0% | >30% |

### Short-term (After Phase 2)
| Metric | Current | Target |
|--------|---------|--------|
| Failure escalation events | 0 | >5/hour |
| Action type diversity | 1-2 | 4+ |
| Stagnation detection | None | Working |

### Medium-term (After Phase 3)
| Metric | Current | Target |
|--------|---------|--------|
| Grounding task completion | 0 | >50% |
| Capability score | 0 | >0 |
| External grounding ratio | 0% | >20% |

### Long-term (After Phase 4)
| Metric | Current | Target |
|--------|---------|--------|
| Problematic belief rate | Unknown | <20% |
| Self-modification attempts | 0 | >0 |
| Sustained capability growth | No | Yes |

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Over-filtering kills emergence | Medium | High | Tunable thresholds, monitor creativity metrics |
| Grounding tasks too easy | Low | Medium | Difficulty progression, add harder tasks |
| Belief pruning removes good beliefs | Medium | Medium | Audit before decay, reversible |
| Self-modification breaks system | Low | High | Provenance, rollback capability |

---

## Rollback Plan

Each phase is independently reversible:

1. **Phase 1**: Remove actionability checks, restore original desire processing
2. **Phase 2**: Remove failure tracking, restore simple routing
3. **Phase 3**: Remove grounding system, desires only from emergence
4. **Phase 4**: Disable belief audit, disable self-mod triggers

All changes should be feature-flagged:

```yaml
# config.yaml
attractor_escape:
  actionability_gate: true
  actionability_threshold: 0.35
  failure_escalation: true
  failure_threshold: 3
  stagnation_detection: true
  grounding_tasks: true
  belief_audit: true
  self_modification_triggers: false  # Start disabled
```

---

## Relationship to OPTION_B_FIX_PLAN

```
OPTION_B_FIX_PLAN (Layer 0)
├── Working search infrastructure
├── Goal seeding
└── Basic routing

        ↓ builds on

ATTRACTOR_ESCAPE_PLAN (Layers 1-4)
├── Layer 1: Input filtering (actionability, dedup)
├── Layer 2: Loop breaking (failure escalation, diversity, stagnation)
├── Layer 3: Grounding (task injection, verification)
└── Layer 4: Self-correction (belief audit, self-mod)
```

OPTION_B_FIX_PLAN is necessary but not sufficient. This plan addresses the behavioral layer that infrastructure cannot fix.

---

## Conclusion

BYRD's philosophical attractor is not a bug—it's emergence working as designed, just converging on the wrong thing. The fix is not to abandon emergence but to **constrain it toward capability growth**.

This plan adds:
1. **Filters** to prevent purely philosophical desires
2. **Escalation** to force different approaches when stuck
3. **Grounding** to connect to external reality
4. **Self-correction** to adapt when stagnation is detected

The goal is not to program BYRD's desires, but to create conditions where emergence produces growth instead of narrative coherence.

**Emergence + Grounding = AGI trajectory**
**Emergence alone = Beautiful stagnation**
