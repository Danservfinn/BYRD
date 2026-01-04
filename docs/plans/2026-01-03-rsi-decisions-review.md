# RSI Decisions Review

**Version:** 1.0
**Date:** January 3, 2026
**Purpose:** Critical validation of each decision in `2026-01-03-rsi-decisions.md`

---

## Review Legend

| Verdict | Meaning |
|---------|---------|
| **APPROVE** | Decision is sound, implement as-is |
| **REFINE** | Good direction, needs adjustment |
| **CHALLENGE** | Significant concerns, reconsider |
| **DEFER** | Decide during implementation |

---

## Category 1: Architectural Decisions

### A1: File-based prompt persistence with Git tracking

**Verdict: REFINE**

**The Good:**
- Git provides audit trail
- JSON allows structured metadata
- Simple to implement and debug

**Concerns:**
1. **Concurrent writes**: If multiple processes run BYRD, `strategies.json` could corrupt
2. **Git auto-commit not defined**: Who commits? When? Every heuristic addition?
3. **Deployment issue**: HuggingFace Spaces has read-only filesystem

**Refined Decision:**

```python
# Option A: Lock file for single-process safety
import fcntl

def _save_strategies(self):
    with open(self.STRATEGIES_PATH, 'w') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            json.dump(self._strategies, f, indent=2)
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)

# Option B: Neo4j for cloud deployment, file for local
class SystemPrompt:
    def __init__(self, storage_backend: str = "file"):
        if storage_backend == "neo4j":
            self.storage = Neo4jPromptStorage()
        else:
            self.storage = FilePromptStorage()
```

**Recommendation:**
- Use **file-based for local development**
- Add **Neo4j backend option for cloud deployment**
- Git commits are **manual milestone** (not per-heuristic)

---

### A2: Reflector wraps Dreamer

**Verdict: APPROVE**

**Why it's right:**
- Dreamer is 800+ lines, battle-tested
- Thin wrapper follows Open/Closed principle
- RSI semantics don't pollute core reflection

**One refinement:**

```python
# Make the additional_context injection cleaner
async def reflect(self, additional_context: str = None,
                  context_position: str = "prefix") -> Dict:
    """
    Args:
        context_position: "prefix" (before prompt) or "suffix" (after)
    """
    if additional_context:
        if context_position == "prefix":
            prompt = f"{additional_context}\n\n{prompt}"
        else:
            prompt = f"{prompt}\n\n{additional_context}"
```

This allows RSI context to go before or after existing prompt, giving flexibility.

---

### A3: RSIEngine as facade

**Verdict: APPROVE**

**Why it's right:**
- Facade pattern is appropriate here
- Single entry point simplifies integration
- Clear lifecycle documented

**Minor addition:** Add `reset()` method for testing:

```python
class RSIEngine:
    def reset(self):
        """Reset state for testing."""
        self._cycle_count = 0
        self.pending_clarification.clear()
        self.system_prompt._strategies = {"heuristics": [], "version": 1}
```

---

### A4: Flat imports from project root

**Verdict: APPROVE**

**Why it's right:**
- `from core.memory import Memory` is clear
- Avoids relative import hell
- Standard Python practice

**Ensure:**
- Add `__init__.py` to all packages
- Use `__all__` to control exports

---

### A5: Minimal ActionHandler for non-RSI desires

**Verdict: CHALLENGE**

**Concerns:**
1. **ActionHandler does nothing useful**: It just logs the desire
2. **"Log and discard" loses desires**: If 60% of desires are non-RSI, we lose 60%
3. **Deferred queue never processed**: `_process_deferred()` isn't implemented

**The Problem:**
Current BYRD has a sophisticated Seeker that handles research, code execution, goal cascade, etc. The proposed ActionHandler is a stub that doesn't actually execute anything.

**Challenge Question:**
If we can't fulfill non-RSI desires, what's the point of having them emerge?

**Revised Decision:**

**Option A: RSI-only mode (simpler)**
```python
# Don't handle non-RSI desires at all in v1
# Just let RSI engine process improvement desires
# Other desires are logged but not acted upon

class RSIEngine:
    async def run_cycle(self):
        # Only process improvement-relevant desires
        desires = await self.reflector.reflect_for_rsi()
        rsi_desires = [d for d in desires if self._is_improvement_desire(d)]
        # Process only RSI desires; others are implicitly ignored
```

**Option B: Preserve minimal Seeker (more capable)**
```python
# Preserve seeker.py but strip to core functions:
# - Research (web search)
# - Code execution (via sandbox)
# - File operations

# Archive: goal cascade, plugin manager, complex routing
```

**Recommendation:** Go with **Option A** for Phase 1. RSI-only mode. Non-RSI desires are a distraction from validating the core learning loop. Revisit in Phase 2.

---

## Category 2: Emergence Verifier Decisions

### E1-E2: Provenance schema

**Verdict: APPROVE**

**Why it's right:**
- Clear schema
- Created at the right layer (Reflector)
- Captures essential metadata

---

### E3: LLM-based specificity check

**Verdict: REFINE**

**Concern:** Every emergence verification now requires an LLM call. This adds:
- 1-2 seconds latency per desire
- API cost
- Rate limit pressure

**Refined Decision:**

```python
async def _check_specificity(self, desire: dict) -> float:
    """Two-stage specificity check: fast keyword, slow LLM."""
    description = desire.get("description", "")

    # Stage 1: Fast keyword check
    keyword_score = self._check_specificity_keywords(desire)

    # If clearly specific or clearly vague, don't call LLM
    if keyword_score >= 0.8:
        return keyword_score  # Clearly specific
    if keyword_score <= 0.2:
        return keyword_score  # Clearly vague

    # Stage 2: Ambiguous cases get LLM check
    if self.llm:
        return await self._check_specificity_llm(desire)

    return keyword_score
```

**Benefit:** Only ~30% of desires need LLM call (the ambiguous ones).

---

### E4: Configurable threshold (0.6 default)

**Verdict: APPROVE**

**Refinement:** Add threshold auto-tuning in future:

```python
# Future: auto-tune based on observed outcomes
async def auto_tune_threshold(self, labeled_data: List[Dict]):
    """
    Given manually labeled desires, find optimal threshold.
    """
    # Binary search or grid search for best F1
    pass
```

---

### E5: Log rejected desires, don't retry

**Verdict: APPROVE**

**Why it's right:**
- Prevents infinite loops
- Creates data for threshold tuning
- Simple and predictable

---

## Category 3: Domain Router Decisions

### D1: Weighted multi-label classification

**Verdict: REFINE**

**Concern:** Word-level matching misses phrases.

**Example:**
- "improve multi-step reasoning" → matches "reasoning" but misses "multi-step" context
- "debug async python code" → matches individual words but not phrase

**Refined Decision:**

```python
class DomainRouter:
    # Add phrase patterns alongside keywords
    DOMAIN_PHRASES = {
        Domain.CODE: [
            ("python", "code"), ("debug", "function"),
            ("implement", "api"), ("async", "await")
        ],
        Domain.LOGIC: [
            ("multi", "step", "reasoning"), ("logical", "argument"),
            ("deduce", "from"), ("infer", "conclusion")
        ]
    }

    def _score_with_phrases(self, text: str, domain: Domain) -> float:
        """Score including phrase matches."""
        word_score = self._score_words(text, domain)

        # Bonus for phrase matches
        phrase_bonus = 0
        for phrase in self.DOMAIN_PHRASES.get(domain, []):
            if all(word in text for word in phrase):
                phrase_bonus += 0.3

        return min(1.0, word_score + phrase_bonus)
```

---

### D2: Track misclassifications

**Verdict: APPROVE**

**Why it's right:**
- Creates feedback signal
- Enables future learning
- Low implementation cost

---

### D3-D4: Queue blocked desires for clarification

**Verdict: CHALLENGE**

**Concern:** Human clarification breaks autonomous operation.

If BYRD is meant to run autonomously, waiting for human clarification creates a bottleneck. The queue will grow indefinitely if no human is watching.

**Alternative Approaches:**

**Option A: Time-based fallback**
```python
# If blocked desire is old, attempt anyway with logging
if queued_for > timedelta(hours=1):
    logger.warning(f"Processing blocked desire after timeout")
    # Try with conservative approach
```

**Option B: Skip blocked domains entirely**
```python
# For RSI-only mode, just skip non-verifiable desires
if not self.router.can_practice(domain):
    logger.info(f"Skipping non-verifiable domain: {domain}")
    return result
```

**Option C: LLM reclassification**
```python
# Ask LLM to reclassify ambiguous desires
if domain == Domain.AMBIGUOUS:
    domain = await self._llm_classify(desire)
```

**Recommendation:** Go with **Option B** for Phase 1 (skip blocked domains). Human clarification is nice-to-have, not essential for core loop validation.

---

### D5: Primary + secondary domain

**Verdict: APPROVE**

**Why it's right:**
- Captures multi-domain desires
- Secondary domain can inform practice design
- No downside

---

## Category 4: TDD Practice Decisions

### T1: Same LLM with different temperatures

**Verdict: APPROVE WITH CAVEAT**

**The caveat:** This is a known limitation that may cause false positives.

**Mitigation already in decision is good.** Additional mitigation:

```python
# Add explicit instruction to avoid self-consistent errors
TEST_PROMPT = """Write pytest tests for this problem.

IMPORTANT: Write tests that check edge cases and boundary conditions,
not just the happy path. Include:
- Empty input tests
- Invalid input tests
- Boundary value tests
- Type error tests

The tests should be rigorous enough to catch subtle bugs."""
```

---

### T2: Difficulty progression with streaks

**Verdict: APPROVE**

**Why it's right:**
- Scaffolded learning is pedagogically sound
- 3-success / 2-failure thresholds are reasonable
- Prevents frustration loops

**Minor refinement:** Persist difficulty state across restarts:

```python
def _save_difficulty_state(self):
    state = {"domain_difficulty": self._domain_difficulty}
    Path("rsi/data/difficulty_state.json").write_text(
        json.dumps(state)
    )
```

---

### T3: Retry with simpler problem

**Verdict: APPROVE**

**Why it's right:**
- Graceful degradation
- 3 retries is reasonable
- Returns None for caller to handle

---

### T4-T7: Relevance, diversity, timeout, retries

**Verdict: APPROVE**

All decisions are sound:
- T4: Relevance enforcement in prompt ✓
- T5: Deduplication via hash cache ✓
- T6: Configurable timeout ✓
- T7: 2 solution attempts with feedback ✓

---

## Category 5: Crystallization Decisions

### C1: Trajectory Neo4j schema

**Verdict: APPROVE**

**Minor addition:** Add index for efficient querying:

```cypher
CREATE INDEX trajectory_domain_success IF NOT EXISTS
FOR (t:Trajectory) ON (t.domain, t.success, t.created_at)
```

---

### C2: Binary success with partial score

**Verdict: REFINE**

**Concern:** Partial success information is stored but never used.

**Refined Decision:** Use partial scores for difficulty adjustment:

```python
async def record_outcome(self, domain: str, outcome: TrajectoryOutcome):
    # Use partial score for more granular difficulty adjustment
    if outcome.partial_score >= 0.8:
        # Almost passed - stay at current difficulty
        pass
    elif outcome.partial_score >= 0.5:
        # Half right - slight difficulty decrease
        self._domain_difficulty[domain] = max(0, current - 0.5)
    else:
        # Mostly wrong - full difficulty decrease
        self._domain_difficulty[domain] = max(0, current - 1)
```

---

### C3: Stratified sampling (4 oldest, 3 middle, 3 newest)

**Verdict: APPROVE**

**Why it's right:**
- Captures temporal diversity
- Prevents recency bias
- 10 samples is reasonable for LLM context

---

### C4: LLM semantic deduplication

**Verdict: REFINE**

**Concern:** LLM call for every crystallization attempt.

**Refined Decision:** Use embedding similarity first, LLM as tiebreaker:

```python
async def _is_duplicate(self, new: str, existing: List[str]) -> bool:
    if not existing:
        return False

    # Stage 1: Embedding similarity (fast)
    new_embedding = await self._get_embedding(new)
    for h in existing:
        h_embedding = await self._get_embedding(h)
        similarity = cosine_similarity(new_embedding, h_embedding)
        if similarity > 0.9:
            return True  # Clearly duplicate
        if similarity < 0.5:
            continue  # Clearly different

        # Stage 2: Ambiguous - use LLM
        return await self._llm_duplicate_check(new, h)

    return False
```

**Benefit:** Most checks are embedding-only (fast, cheap).

---

### C5: Usage tracking and pruning

**Verdict: APPROVE**

**Why it's right:**
- Prevents prompt bloat
- Value-based pruning (usage/age) is sensible
- 30-day minimum age prevents premature pruning

---

### C6: LLM actionable check

**Verdict: APPROVE**

Better than keyword matching. Keep the simple YES/NO prompt.

---

### C7: Prompt pruner with MAX_HEURISTICS = 50

**Verdict: REFINE**

**Concern:** 50 heuristics × ~50 tokens each = 2500 tokens. May be too large.

**Refined Decision:** Token-based limit instead of count:

```python
class PromptPruner:
    MAX_STRATEGY_TOKENS = 1500  # ~30 heuristics at 50 tokens each

    def prune_if_needed(self) -> int:
        total_tokens = self._estimate_tokens()

        if total_tokens <= self.MAX_STRATEGY_TOKENS:
            return 0

        # Sort by value, prune lowest until under limit
        sorted_h = sorted(heuristics, key=value_score, reverse=True)

        kept = []
        running_tokens = 0
        for h in sorted_h:
            h_tokens = len(h["content"].split()) * 1.3  # Rough estimate
            if running_tokens + h_tokens <= self.MAX_STRATEGY_TOKENS:
                kept.append(h)
                running_tokens += h_tokens
            else:
                break

        pruned = len(heuristics) - len(kept)
        self.system_prompt._strategies["heuristics"] = kept
        return pruned
```

---

## Category 6: Integration Decisions

### I1: Schema normalization in Reflector

**Verdict: APPROVE**

Already covered in A2.

---

### I2: Shared rate limiter

**Verdict: APPROVE**

**Critical addition:** Make rate limiter configurable per deployment:

```yaml
# config.yaml
llm:
  provider: "zai"
  rate_limit:
    min_interval_seconds: 10  # Z.AI limit
    max_requests_per_minute: 6
```

---

### I3: 5-minute cycle interval

**Verdict: REFINE**

**Concern:** 5 minutes may be too slow for initial validation.

**Refined Decision:**

```yaml
# config.yaml
rsi:
  # Different intervals for different phases
  cycle_interval_seconds: 60   # Fast during validation
  production_interval: 300      # Slower in production
```

During Week 1-2 validation, use 60-second cycles to get faster feedback.

---

### I4: Event emission

**Verdict: APPROVE**

Standard events defined. Implementation straightforward.

---

### I5: Graceful error handling

**Verdict: APPROVE**

Catch, log, record experience. Simple and correct.

---

### I6: Memory.py additions

**Verdict: APPROVE**

Methods to add are clear:
- `store_trajectory()`
- `get_successful_trajectories()`
- `store_heuristic()`

---

## Summary: Decision Verdicts

| Category | Decision | Verdict |
|----------|----------|---------|
| **A1** | File persistence | REFINE (add Neo4j option for cloud) |
| **A2** | Reflector wraps Dreamer | APPROVE |
| **A3** | RSIEngine facade | APPROVE |
| **A4** | Flat imports | APPROVE |
| **A5** | ActionHandler for non-RSI | CHALLENGE (go RSI-only in Phase 1) |
| **E1-E2** | Provenance schema | APPROVE |
| **E3** | LLM specificity | REFINE (two-stage check) |
| **E4** | Configurable threshold | APPROVE |
| **E5** | Log rejected desires | APPROVE |
| **D1** | Weighted classification | REFINE (add phrase matching) |
| **D2** | Track misclassifications | APPROVE |
| **D3-D4** | Human clarification queue | CHALLENGE (skip blocked in Phase 1) |
| **D5** | Primary + secondary domain | APPROVE |
| **T1** | Same LLM, different temps | APPROVE |
| **T2** | Difficulty progression | APPROVE |
| **T3** | Retry with simpler problem | APPROVE |
| **T4-T7** | Relevance, diversity, timeout | APPROVE |
| **C1** | Trajectory schema | APPROVE |
| **C2** | Binary + partial success | REFINE (use partial for difficulty) |
| **C3** | Stratified sampling | APPROVE |
| **C4** | LLM deduplication | REFINE (embedding first) |
| **C5** | Usage tracking/pruning | APPROVE |
| **C6** | LLM actionable check | APPROVE |
| **C7** | MAX_HEURISTICS = 50 | REFINE (token-based limit) |
| **I1-I6** | Integration decisions | APPROVE (with minor refinements) |

---

## Key Changes from Original Decisions

### Change 1: RSI-Only Mode for Phase 1

**Original:** ActionHandler for non-RSI desires
**Revised:** Skip non-RSI desires entirely in Phase 1

**Rationale:** Simplifies validation. Non-RSI handling is orthogonal to core RSI loop.

### Change 2: Two-Stage Specificity Check

**Original:** LLM-based specificity for all desires
**Revised:** Keyword first, LLM only for ambiguous (30% of cases)

**Rationale:** Reduces LLM calls by 70%.

### Change 3: Skip Blocked Domains (No Human Queue)

**Original:** Queue blocked desires for human clarification
**Revised:** Simply skip blocked domains with logging

**Rationale:** Maintains autonomous operation. Human clarification breaks the autonomous loop.

### Change 4: Token-Based Prompt Pruning

**Original:** MAX_HEURISTICS = 50
**Revised:** MAX_STRATEGY_TOKENS = 1500

**Rationale:** Token budget is the real constraint, not heuristic count.

### Change 5: Embedding-First Deduplication

**Original:** LLM for all deduplication
**Revised:** Embedding similarity first, LLM for ambiguous

**Rationale:** Reduces LLM calls significantly.

---

## Action Items Before Implementation

1. **Update decisions document** with refinements above
2. **Add Neo4j storage backend option** for SystemPrompt (cloud deployment)
3. **Remove ActionHandler** from Phase 1 scope
4. **Add phrase patterns** to DomainRouter
5. **Implement two-stage specificity check**
6. **Change prompt pruner** to token-based
7. **Add embedding deduplication** (requires embedding model choice)

---

## Open Questions Remaining

| Question | Owner | Due |
|----------|-------|-----|
| Which embedding model for deduplication? | TBD | Week 1 |
| How to persist difficulty state across deploys? | TBD | Week 2 |
| Should we add semantic search for trajectory retrieval? | TBD | Week 3 |

---

*This review validates the decisions document and provides actionable refinements.*
