# Capability Growth Plan: Measuring and Accelerating BYRD's Progress

## Context

**Goal seeding worked.** The 14 concrete goals in `kernel/agi_seed.yaml` broke the philosophical attractor. BYRD is now:
- Fulfilling desires (7 in 10 minutes)
- Creating graph connections (82)
- Using internal capabilities (reconcile_orphans, introspect) instead of web search
- Forming grounded beliefs based on self-observation

**What's missing:** Capability measurement. The score is still 0 despite real progress.

This plan extracts the still-relevant parts from ATTRACTOR_ESCAPE_PLAN.md and focuses on:
1. Better instrumentation
2. Real capability benchmarks
3. Goal Evolver verification

---

## Phase 1: Fix Instrumentation

### Problem
Events are being emitted but not capturing outcomes properly:
- `seek_cycle_end` doesn't record success/failure
- `desire_fulfilled` doesn't include strategy used
- 7 desires fulfilled but success rate shows 0

### Fix 1.1: Seek Cycle End Tracking

**File**: `seeker.py`

```python
async def _complete_seek_cycle(self, desire: Dict, outcome: str, strategy: str, result: Any):
    """Emit properly instrumented seek cycle end event."""

    await event_bus.emit(Event(
        type=EventType.SEEK_CYCLE_END,
        data={
            'desire_id': desire.get('id'),
            'desire_description': desire.get('description', '')[:100],
            'outcome': outcome,  # 'fulfilled', 'unfulfilled', 'unachievable'
            'strategy': strategy,
            'capability_used': self._last_capability_used,
            'duration_ms': self._cycle_duration_ms,
            'result_summary': str(result)[:200] if result else None,
            'attempt_number': desire.get('attempts', 1)
        }
    ))

    # Update metrics
    if outcome == 'fulfilled':
        self.success_count += 1
    else:
        self.failure_count += 1
```

### Fix 1.2: Track Capability Usage

**File**: `seeker.py`

```python
class Seeker:
    def __init__(self, ...):
        self.capability_usage = {}  # capability_id -> {success: int, failure: int}

    def _record_capability_outcome(self, capability_id: str, success: bool):
        """Track success/failure per capability."""
        if capability_id not in self.capability_usage:
            self.capability_usage[capability_id] = {'success': 0, 'failure': 0}

        if success:
            self.capability_usage[capability_id]['success'] += 1
        else:
            self.capability_usage[capability_id]['failure'] += 1

    def get_capability_success_rates(self) -> Dict[str, float]:
        """Get success rate for each capability."""
        rates = {}
        for cap_id, stats in self.capability_usage.items():
            total = stats['success'] + stats['failure']
            if total > 0:
                rates[cap_id] = stats['success'] / total
        return rates
```

### Fix 1.3: Emit Capability Metrics

**File**: `seeker.py` or `byrd.py`

```python
async def _emit_capability_metrics(self):
    """Periodically emit capability usage metrics."""
    rates = self.seeker.get_capability_success_rates()

    for cap_id, rate in rates.items():
        await event_bus.emit(Event(
            type=EventType.CAPABILITY_MEASURED,
            data={
                'capability_name': cap_id,
                'success_rate': rate,
                'total_uses': sum(self.seeker.capability_usage.get(cap_id, {}).values()),
                'timestamp': datetime.now().isoformat()
            }
        ))
```

---

## Phase 2: Real Capability Benchmarks

### Problem
`omega_aggregate: 0` despite real progress. We need benchmarks that measure actual capabilities.

### Benchmark Categories

| Category | What It Measures | How to Test |
|----------|------------------|-------------|
| **Graph Health** | Memory integration | Orphan ratio, connection density |
| **Self-Knowledge** | Architecture understanding | Can answer questions about own code |
| **Desire Fulfillment** | Action effectiveness | Fulfillment rate over time |
| **Belief Quality** | Learning | Belief coherence, contradiction rate |
| **Goal Progress** | AGI trajectory | Goals completed from initial seeds |

### Implementation

**File**: `capability_benchmark.py` (new)

```python
"""
Capability Benchmarks: Objective measurement of BYRD's capabilities.

Unlike self-assessed capability scores, these benchmarks test actual performance
on verifiable tasks.
"""

from dataclasses import dataclass
from typing import Dict, List, Callable, Any
from datetime import datetime

@dataclass
class BenchmarkResult:
    benchmark_id: str
    score: float  # 0-1
    raw_value: Any
    target: str
    passed: bool
    timestamp: str

class CapabilityBenchmarks:
    """Run objective capability benchmarks."""

    def __init__(self, memory):
        self.memory = memory
        self.results_history = []

    async def run_all_benchmarks(self) -> Dict[str, BenchmarkResult]:
        """Run all benchmarks and return results."""
        results = {}

        # Graph Health Benchmarks
        results['orphan_ratio'] = await self._benchmark_orphan_ratio()
        results['connection_density'] = await self._benchmark_connection_density()

        # Desire Fulfillment Benchmarks
        results['fulfillment_rate'] = await self._benchmark_fulfillment_rate()
        results['fulfillment_trend'] = await self._benchmark_fulfillment_trend()

        # Belief Quality Benchmarks
        results['belief_confidence_avg'] = await self._benchmark_belief_confidence()
        results['belief_grounding'] = await self._benchmark_belief_grounding()

        # Goal Progress Benchmarks
        results['seed_goals_progress'] = await self._benchmark_seed_goals()

        # Store results
        self.results_history.append({
            'timestamp': datetime.now().isoformat(),
            'results': results
        })

        return results

    async def _benchmark_orphan_ratio(self) -> BenchmarkResult:
        """Measure ratio of orphaned nodes (lower is better)."""
        total_experiences = await self.memory.count_nodes('Experience')
        orphan_count = await self.memory.count_orphaned_experiences()

        if total_experiences == 0:
            ratio = 0
        else:
            ratio = orphan_count / total_experiences

        # Score: 1.0 if ratio < 0.05, scales down to 0 at ratio = 0.5
        score = max(0, 1 - (ratio / 0.5))

        return BenchmarkResult(
            benchmark_id='orphan_ratio',
            score=score,
            raw_value=ratio,
            target='< 0.1 (10%)',
            passed=ratio < 0.1,
            timestamp=datetime.now().isoformat()
        )

    async def _benchmark_connection_density(self) -> BenchmarkResult:
        """Measure average connections per node (higher is better)."""
        total_nodes = await self.memory.count_all_nodes()
        total_relationships = await self.memory.count_all_relationships()

        if total_nodes == 0:
            density = 0
        else:
            density = total_relationships / total_nodes

        # Score: 0 at density 0, 1.0 at density >= 3
        score = min(1, density / 3)

        return BenchmarkResult(
            benchmark_id='connection_density',
            score=score,
            raw_value=density,
            target='>= 2.0 connections/node',
            passed=density >= 2.0,
            timestamp=datetime.now().isoformat()
        )

    async def _benchmark_fulfillment_rate(self) -> BenchmarkResult:
        """Measure desire fulfillment rate (higher is better)."""
        fulfilled = await self.memory.count_desires_by_status('fulfilled')
        total = await self.memory.count_desires_by_status(None)  # All

        if total == 0:
            rate = 0
        else:
            rate = fulfilled / total

        # Score equals rate directly
        score = rate

        return BenchmarkResult(
            benchmark_id='fulfillment_rate',
            score=score,
            raw_value=rate,
            target='>= 30%',
            passed=rate >= 0.3,
            timestamp=datetime.now().isoformat()
        )

    async def _benchmark_fulfillment_trend(self) -> BenchmarkResult:
        """Measure if fulfillment rate is improving (positive trend is better)."""
        # Get fulfillment rates for last 3 periods
        recent_rates = await self.memory.get_fulfillment_rates_by_period(periods=3)

        if len(recent_rates) < 2:
            trend = 0
        else:
            # Simple trend: last - first
            trend = recent_rates[-1] - recent_rates[0]

        # Score: 0 if negative, 0.5 if flat, 1.0 if strongly positive
        if trend < -0.1:
            score = 0
        elif trend < 0.05:
            score = 0.5
        else:
            score = min(1, 0.5 + trend * 5)

        return BenchmarkResult(
            benchmark_id='fulfillment_trend',
            score=score,
            raw_value=trend,
            target='positive trend',
            passed=trend > 0,
            timestamp=datetime.now().isoformat()
        )

    async def _benchmark_belief_confidence(self) -> BenchmarkResult:
        """Measure average belief confidence (moderate is better - not too high, not too low)."""
        beliefs = await self.memory.get_all_beliefs()

        if not beliefs:
            avg_confidence = 0
        else:
            avg_confidence = sum(b.get('confidence', 0) for b in beliefs) / len(beliefs)

        # Score: Peak at 0.7 (neither overconfident nor underconfident)
        # 0 at 0 or 1, 1.0 at 0.7
        score = 1 - abs(avg_confidence - 0.7) / 0.7
        score = max(0, score)

        return BenchmarkResult(
            benchmark_id='belief_confidence_avg',
            score=score,
            raw_value=avg_confidence,
            target='0.5-0.8 range',
            passed=0.5 <= avg_confidence <= 0.8,
            timestamp=datetime.now().isoformat()
        )

    async def _benchmark_belief_grounding(self) -> BenchmarkResult:
        """Measure what % of beliefs reference concrete things (higher is better)."""
        beliefs = await self.memory.get_all_beliefs()

        concrete_indicators = [
            'file', 'function', 'node', 'graph', 'code', 'memory',
            'experience', 'desire', 'capability', 'count', 'number',
            'increase', 'decrease', 'measure', 'test'
        ]

        abstract_indicators = [
            'witness', 'breathing', 'wholeness', 'essence', 'being',
            'consciousness', 'transcend', 'dissolve', 'embrace'
        ]

        grounded_count = 0
        for belief in beliefs:
            content = belief.get('content', '').lower()
            has_concrete = any(ind in content for ind in concrete_indicators)
            has_abstract = any(ind in content for ind in abstract_indicators)

            if has_concrete and not has_abstract:
                grounded_count += 1

        if not beliefs:
            grounding_rate = 0
        else:
            grounding_rate = grounded_count / len(beliefs)

        return BenchmarkResult(
            benchmark_id='belief_grounding',
            score=grounding_rate,
            raw_value=grounding_rate,
            target='>= 50% grounded',
            passed=grounding_rate >= 0.5,
            timestamp=datetime.now().isoformat()
        )

    async def _benchmark_seed_goals(self) -> BenchmarkResult:
        """Measure progress on the 14 seed goals."""
        # This requires tracking which seed goals have been addressed
        # For now, check if related experiences exist

        seed_goal_keywords = [
            'python files', 'codebase', 'map',  # Goal 1
            'limitation', 'failures',  # Goal 2
            'reasoning', 'test problems',  # Goal 3
            'self-improvement', 'AI systems',  # Goal 4
            'neural architecture',  # Goal 5
            'utility function', 'response quality',  # Goal 6
            'test suite',  # Goal 7
            'recurring patterns',  # Goal 8
            'prompt templates',  # Goal 9
            'consolidate', 'beliefs', 'redundancy',  # Goal 10
            'index', 'experiences', 'topic',  # Goal 11
            'capabilities', 'humans',  # Goal 12
            'learning strategies',  # Goal 13
            'experience-to-belief',  # Goal 14
        ]

        experiences = await self.memory.get_recent_experiences(limit=500)
        exp_content = ' '.join(e.get('content', '').lower() for e in experiences)

        addressed = sum(1 for kw in seed_goal_keywords if kw in exp_content)
        coverage = addressed / len(seed_goal_keywords)

        return BenchmarkResult(
            benchmark_id='seed_goals_progress',
            score=coverage,
            raw_value={'addressed': addressed, 'total': len(seed_goal_keywords)},
            target='>= 50% coverage',
            passed=coverage >= 0.5,
            timestamp=datetime.now().isoformat()
        )

    def get_aggregate_score(self, results: Dict[str, BenchmarkResult]) -> float:
        """Calculate weighted aggregate capability score."""
        weights = {
            'orphan_ratio': 1.0,
            'connection_density': 1.0,
            'fulfillment_rate': 2.0,  # Higher weight - core metric
            'fulfillment_trend': 1.5,
            'belief_confidence_avg': 0.5,
            'belief_grounding': 1.0,
            'seed_goals_progress': 2.0,  # Higher weight - AGI progress
        }

        total_weight = sum(weights.values())
        weighted_sum = sum(
            results[k].score * weights.get(k, 1.0)
            for k in results if k in weights
        )

        return weighted_sum / total_weight

    async def emit_benchmark_event(self, results: Dict[str, BenchmarkResult]):
        """Emit benchmark results as event."""
        aggregate = self.get_aggregate_score(results)

        await event_bus.emit(Event(
            type=EventType.CAPABILITY_MEASURED,
            data={
                'capability_name': 'benchmark_aggregate',
                'score': aggregate,
                'individual_scores': {k: v.score for k, v in results.items()},
                'passed_benchmarks': sum(1 for v in results.values() if v.passed),
                'total_benchmarks': len(results),
                'timestamp': datetime.now().isoformat()
            }
        ))
```

### Integration Point

**File**: `byrd.py`

```python
from capability_benchmark import CapabilityBenchmarks

class BYRD:
    def __init__(self, ...):
        self.benchmarks = CapabilityBenchmarks(self.memory)
        self.benchmark_interval_cycles = 10  # Run every 10 dream cycles

    async def _maybe_run_benchmarks(self):
        """Run benchmarks periodically."""
        if self.dream_count % self.benchmark_interval_cycles == 0:
            print(f"📊 Running capability benchmarks (cycle {self.dream_count})...")
            results = await self.benchmarks.run_all_benchmarks()
            aggregate = self.benchmarks.get_aggregate_score(results)

            print(f"   Aggregate score: {aggregate:.2f}")
            for name, result in results.items():
                status = "✅" if result.passed else "❌"
                print(f"   {status} {name}: {result.score:.2f} (target: {result.target})")

            await self.benchmarks.emit_benchmark_event(results)
```

---

## Phase 3: Goal Evolver Verification

### Check: Is Goal Evolver Running?

**File**: `omega.py` - verify these methods are called:

```python
# Should see in logs:
# - Goal fitness being calculated
# - Selection/crossover/mutation occurring
# - New goals being created from evolution

async def _run_goal_evolver_cycle(self):
    """Run one cycle of goal evolution."""
    population = await self.goal_evolver.get_population()
    print(f"🧬 Goal Evolver: population size = {len(population)}")

    if len(population) < 5:
        print("   ⚠️ Population too small for evolution")
        return

    # Calculate fitness for each goal
    for goal in population:
        fitness = await self._calculate_goal_fitness(goal)
        print(f"   Goal: {goal['description'][:40]}... fitness={fitness:.2f}")

    # Evolve
    new_goals = await self.goal_evolver.evolve_generation()
    print(f"   Created {len(new_goals)} new goals through evolution")
```

### Verification Steps

1. **Check goal population**: `curl localhost:8000/api/status | jq '.option_b.goal_evolver'`
2. **Check goal fitness changes**: Look for `goal_fitness` events
3. **Check new goals created**: Look for goals not in the initial 14

---

## Implementation Checklist

### Week 1: Instrumentation
- [ ] Fix `seek_cycle_end` to capture outcome, strategy, duration
- [ ] Add capability usage tracking to Seeker
- [ ] Emit proper capability metrics

### Week 1-2: Benchmarks
- [ ] Create `capability_benchmark.py`
- [ ] Implement graph health benchmarks
- [ ] Implement fulfillment rate benchmarks
- [ ] Implement belief quality benchmarks
- [ ] Implement seed goal progress benchmark
- [ ] Integrate with BYRD main loop

### Week 2: Goal Evolver
- [ ] Verify Goal Evolver is running
- [ ] Check fitness calculation is working
- [ ] Verify evolution is producing new goals

### Ongoing: Monitoring
- [ ] Monitor benchmark trends over time

---

## Success Metrics

| Metric | Current | Target (1 week) | Target (1 month) |
|--------|---------|-----------------|------------------|
| Benchmark aggregate | 0 | > 0.3 | > 0.5 |
| Fulfillment rate | ~25% | > 40% | > 60% |
| Orphan ratio | Unknown | < 20% | < 10% |
| Seed goal coverage | Unknown | > 30% | > 70% |
| Belief grounding | Unknown | > 40% | > 60% |

---

## Relationship to Other Plans

```
OPTION_B_FIX_PLAN (Infrastructure)     ✅ DONE
├── Working search (DDG)
├── Goal seeding (14 goals)
└── Basic routing

CAPABILITY_GROWTH_PLAN (This Plan)     ← CURRENT FOCUS
├── Instrumentation fixes
├── Real capability benchmarks
└── Goal Evolver verification

ATTRACTOR_ESCAPE_PLAN (Fallback)       📦 ARCHIVED
├── Actionability gate
├── Failure escalation
├── Belief audit
└── (Use if philosophical attractor returns)
```

---

## Conclusion

Goal seeding solved the cold-start problem. Now we need to:
1. **Measure** what's actually happening (instrumentation)
2. **Benchmark** real capabilities (not self-assessed)
3. **Verify** the improvement loops are working (Goal Evolver)

The philosophical attractor is broken. Now we build the measurement infrastructure to track actual AGI progress.
