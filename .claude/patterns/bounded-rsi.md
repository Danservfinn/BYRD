---
title: Bounded RSI Pattern
link: bounded-rsi
type: pattern
uuid: 868D53C0-9927-4367-A888-C353A5C69A88
created_at: 2026-01-07T01:30:00Z
ontological_relations:
  - rsi_patterns
  - verification-lattice
  - emergence_patterns
tags:
  - rsi
  - bounded-improvement
  - digital-asi
  - research-findings
---

# Bounded RSI Pattern

The Bounded RSI pattern emerged from 29 research iterations as the validated path to Digital ASI (35-45% probability).

## Core Principle

**Unbounded RSI has zero validated instances in 60 years of AI research.**

Bounded RSI targets verifiable improvement within tractable domains:
- Accepts architectural ceilings as design constraints
- Focuses effort where verification is possible
- Preserves emergence within bounded improvement cycles

## Domain Stratification

Focus RSI effort according to verification tractability:

| Stratum | Verifiability | Weight | Examples |
|---------|--------------|--------|----------|
| 1 | Fully verifiable | 60% | Code, math, logic |
| 2 | Partially verifiable | 30% | Planning, reasoning |
| 3 | Weakly verifiable | 10% | Creative, open-ended |

## Implementation

```python
DOMAIN_WEIGHTS = {
    "stratum_1": 0.60,  # Fully verifiable
    "stratum_2": 0.30,  # Partially verifiable
    "stratum_3": 0.10,  # Weakly verifiable
}

class BoundedRSIEngine:
    async def allocate_improvement_effort(self) -> Dict[str, float]:
        return DOMAIN_WEIGHTS

    async def propose_improvement(self, domain: str) -> Optional[Improvement]:
        stratum = self.classify_domain(domain)

        if stratum == 1:
            # Full verification required
            return await self.propose_with_full_verification(domain)
        elif stratum == 2:
            # Partial verification + human spot-checks
            return await self.propose_with_partial_verification(domain)
        else:
            # Conservative: emergent strategy competition only
            return await self.propose_via_competition(domain)
```

## Key Constraints

### 1. Complexity-Aware Orchestration
Detect complexity threshold before "reasoning collapse" (Apple research):

```python
COLLAPSE_THRESHOLD = 0.45

async def should_decompose(self, task: Task) -> bool:
    complexity = await self.estimate_complexity(task)
    return complexity > COLLAPSE_THRESHOLD
```

### 2. 45% Threshold Routing
Multi-agent orchestration only when beneficial (DeepMind research):

```python
async def should_use_multi_agent(self, task: Task) -> bool:
    predicted_accuracy = await self.predict_accuracy(task)
    # Above 45% accuracy, more agents = worse
    return predicted_accuracy < 0.45
```

### 3. Entropic Drift Detection
Monitor for the GV-Gap (generalization vs validation gap):

```python
class EntropicDriftMonitor:
    def detect_drift(self, metrics: RSIMetrics) -> bool:
        return (
            metrics.solution_diversity < 0.3 or
            metrics.held_out_benchmark_delta < -0.02 or
            metrics.generalization_gap > 0.15 or
            metrics.strategy_entropy < 0.5
        )
```

## Research Origin

- **Iterations 1-4**: Identified verification ceiling
- **Iterations 5-10**: Developed Verification Lattice
- **Iterations 11-20**: Discovered domain stratification
- **Iterations 21-29**: Validated bounded approach (35-45% stable)

## Probability Assessment

| Outcome | Probability |
|---------|-------------|
| Digital ASI via Bounded RSI | 35-45% |
| Capable Assistant (high confidence) | 55-65% |
| Unbounded Intelligence Explosion | ~0% (no validated path) |

## Related Patterns

- [Verification Lattice](verification-lattice.md): Multi-verifier composition
- [RSI Patterns](rsi_patterns.md): Measurement framework
- [Emergence Patterns](emergence_patterns.md): Preserving genuine emergence
