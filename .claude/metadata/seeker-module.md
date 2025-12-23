---
title: Seeker Module
link: seeker-module
type: metadata
ontological_relations: []
tags: [seeker, pattern-detection, emergence, research, capabilities]
created_at: 2025-12-23T02:10:00Z
updated_at: 2025-12-23T03:00:00Z
uuid: f3c45d60-3456-6789-abcd-ef0123456789
---

## Purpose
Observe BYRD's reflections, detect stable patterns with action hints, and execute BYRD's own strategies. Follows the **emergence principle**: observe before acting, execute BYRD's reasoning rather than prescribed handlers.

## Philosophy

> Instead of routing desires by type and executing specific handlers, we:
> 1. Observe BYRD's reflections
> 2. Detect patterns that have stabilized (repetition + semantic clustering)
> 3. Find patterns where BYRD has reasoned about strategy
> 4. Execute the strategy BYRD suggested
> 5. Record outcomes as experiences for BYRD to reflect on

## Configuration
```yaml
seeker:
  interval_seconds: 30
  pattern_threshold: 3  # Require N occurrences before acting

  research:
    searxng_url: "http://localhost:8888"
    min_intensity: 0.4
    max_queries: 3
    max_results: 10

  capabilities:
    trust_threshold: 0.5
    max_installs_per_day: 3
    github_token: ""  # Optional
```

## Seek Cycle (Emergence-Compliant)

```python
async def _seek_cycle(self):
    # 1. OBSERVE: Get recent reflections
    reflections = await self.memory.get_recent_reflections(limit=10)

    # 2. DETECT: Find action-ready patterns
    action_patterns = await self._detect_action_ready_patterns(reflections)

    if not action_patterns:
        return  # Keep observing - patience

    # 3. EXECUTE: Run BYRD's strategy
    pattern = action_patterns[0]  # Highest priority
    outcome, reason = await self._execute_pattern_strategy(pattern)

    # 4. RECORD: Store outcome for next reflection
    await self._record_execution_outcome(pattern, outcome, reason)
```

## Pattern Detection (Hybrid)

Combines repetition counting with semantic analysis:

```python
async def _detect_action_ready_patterns(self, reflections):
    """
    A pattern is action-ready when:
    1. It appears >= pattern_threshold times (stability)
    2. It contains action hints (BYRD has reasoned about strategy)
    """
    patterns = []

    for reflection in reflections:
        output = reflection.get("raw_output", {})
        extracted = self._extract_patterns_from_output(output)

        for theme, details in extracted.items():
            # Count occurrences
            self._observed_themes[theme] = self._observed_themes.get(theme, 0) + 1

            # Check stability
            if self._observed_themes[theme] >= self._pattern_threshold:
                # Check for action hints
                if self._has_action_hints(details):
                    patterns.append({
                        "theme": theme,
                        "details": details,
                        "occurrences": self._observed_themes[theme]
                    })

    return sorted(patterns, key=lambda p: p["occurrences"], reverse=True)
```

## Strategy Execution

The Seeker executes what BYRD reasoned, not predetermined handlers:

```python
async def _execute_pattern_strategy(self, pattern):
    """Execute BYRD's own strategy, not ours."""
    details = pattern.get("details", {})

    # Extract BYRD's reasoning about how to fulfill
    strategy = details.get("strategy") or details.get("plan") or details.get("approach")

    if not strategy:
        return "no_strategy", "Pattern lacks strategy"

    # Execute based on BYRD's suggested approach
    # (research, capability search, coding, etc.)
    ...
```

## Trust Computation (Emergence-Based)

**No hardcoded trusted owners.** Trust is learned from experience:

```python
def _compute_trust(self, resource: Dict) -> float:
    """Compute trust based on observable signals and learned experience."""
    score = 0.2  # Base trust

    # Observable signals
    stars = resource.get("stars", 0)
    score += min(stars / 500, 0.3)

    # Recency
    if self._is_recently_updated(resource, days=30):
        score += 0.2
    elif self._is_recently_updated(resource, days=90):
        score += 0.1

    # Learned trust from past experience
    source = resource.get("source", "")
    score += self._source_trust.get(source, 0)

    return min(1.0, score)
```

## Inner Voice Generation (Neutral)

No examples, no style guidance:

```python
async def _generate_seeking_thought_neutral(self, pattern):
    """Generate inner voice without examples or style guidance."""
    prompt = f"""Based on this pattern from reflections, express what you're about to do.

Pattern: {pattern}

Express your intention in first person. One sentence."""

    # No examples like "I feel drawn to..."
    # Let BYRD develop its own voice
```

## Key State

```python
self._observed_themes: Dict[str, int]   # theme -> count
self._pattern_threshold: int = 3         # Require stability
self._source_trust: Dict[str, float]     # Learned trust scores
```

## Legacy Methods

The following methods are deprecated (type-based routing):
- `_seek_knowledge()`: Replaced by pattern-based execution
- `_seek_capability()`: Replaced by pattern-based execution
- Type routing in `_seek_cycle()`: Replaced by pattern detection

These handlers still exist for capability execution but are now invoked through pattern detection rather than type matching.

## Rate Limiting
- Max 3 capability installs per day
- Cooldown resets at midnight
- `_installs_today` counter tracks usage
