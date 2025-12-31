# ZEUS: Zero-overhead Unified Engine for Self-improvement

## The Goal

**Artificial General Intelligence via Recursive Self-Improvement (RSI)**

ZEUS is a minimal architecture designed for one purpose: to become increasingly intelligent by improving itself. Unlike complex multi-component systems that accumulate features without proven value, ZEUS maintains ruthless simplicity to maximize the speed and effectiveness of self-improvement cycles.

> "The system that improves itself fastest wins. Complexity is the enemy of iteration speed."

---

## Core Insight: Claude Code IS the Intelligence

Instead of building reasoning systems, training neural networks, or orchestrating multiple LLM providers, ZEUS uses **Claude Code as its cognitive engine**. This is not a limitation—it's a superpower:

| Traditional Approach | ZEUS Approach |
|---------------------|---------------|
| Build reasoning from scratch | Use world-class reasoning (Claude) |
| Create tool-use framework | Use built-in tool use |
| Implement code modification | Claude Code already does this |
| Design agent architecture | Claude Code is already an agent |
| Multiple LLM providers | Single, powerful engine |

**The key insight**: Claude Code can read, understand, and modify the ZEUS codebase. This means ZEUS can genuinely improve itself—not through indirect mechanisms, but by directly editing its own code.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              ZEUS                                        │
│                                                                          │
│    ┌─────────────────────────────────────────────────────────────────┐  │
│    │                      ORCHESTRATOR                                │  │
│    │                      (zeus.py)                                   │  │
│    │                                                                  │  │
│    │   • Maintains the improvement loop                              │  │
│    │   • Prepares context for Claude Code                            │  │
│    │   • Parses and persists outputs                                 │  │
│    │   • Enforces safety constraints                                 │  │
│    └───────────────────────────┬─────────────────────────────────────┘  │
│                                │                                         │
│              ┌─────────────────┼─────────────────┐                      │
│              │                 │                 │                       │
│              ▼                 ▼                 ▼                       │
│    ┌─────────────────┐ ┌─────────────┐ ┌─────────────────┐             │
│    │     MEMORY      │ │ CLAUDE CODE │ │     SAFETY      │             │
│    │    (Neo4j)      │ │  (Engine)   │ │   (Constraints) │             │
│    │                 │ │             │ │                 │             │
│    │ • Experience    │ │ Invoked via │ │ • Protected     │             │
│    │ • Belief        │ │ CLI with    │ │   files         │             │
│    │ • Desire        │ │ structured  │ │ • Rollback      │             │
│    │ • Outcome       │ │ prompts     │ │ • Verification  │             │
│    │ • Capability    │ │             │ │                 │             │
│    │ • Improvement   │ │ Returns:    │ │ Gates all       │             │
│    │                 │ │ • Thoughts  │ │ modifications   │             │
│    │ 6 node types    │ │ • Actions   │ │                 │             │
│    │ vs BYRD's 12+   │ │ • Code      │ │                 │             │
│    └─────────────────┘ └─────────────┘ └─────────────────┘             │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## The RSI Loop

ZEUS operates a single, tight loop optimized for recursive self-improvement:

```
┌────────────────────────────────────────────────────────────────────────┐
│                    THE IMPROVEMENT CYCLE                                │
│                    (~60 seconds per iteration)                          │
│                                                                         │
│                         ┌──────────┐                                   │
│                    ┌───▶│  ASSESS  │                                   │
│                    │    │          │                                   │
│                    │    │ Read:    │                                   │
│                    │    │ • Memory │                                   │
│                    │    │ • Self   │                                   │
│                    │    │ • Caps   │                                   │
│                    │    └────┬─────┘                                   │
│                    │         │                                          │
│                    │         ▼                                          │
│                    │    ┌──────────┐                                   │
│                    │    │ IDENTIFY │                                   │
│                    │    │          │                                   │
│                    │    │ Find:    │                                   │
│                    │    │ • Gaps   │                                   │
│                    │    │ • Limits │                                   │
│                    │    │ • Opps   │                                   │
│                    │    └────┬─────┘                                   │
│                    │         │                                          │
│                    │         ▼                                          │
│                    │    ┌──────────┐                                   │
│     LEARN          │    │ IMPROVE  │◀── Claude Code modifies ZEUS     │
│       │            │    │          │                                   │
│       │            │    │ • Code   │                                   │
│       │            │    │ • Prompt │                                   │
│       │            │    │ • Memory │                                   │
│       │            │    └────┬─────┘                                   │
│       │            │         │                                          │
│       │            │         ▼                                          │
│       │            │    ┌──────────┐                                   │
│       │            │    │  VERIFY  │                                   │
│       │            │    │          │                                   │
│       │            │    │ • Tests  │                                   │
│       │            │    │ • Bench  │                                   │
│       │            │    │ • Sanity │                                   │
│       │            │    └────┬─────┘                                   │
│       │            │         │                                          │
│       ▼            │         ▼                                          │
│  ┌──────────┐      │    ┌──────────┐                                   │
│  │  UPDATE  │◀─────┴────│  RECORD  │                                   │
│  │ STRATEGY │           │          │                                   │
│  │          │           │ Persist: │                                   │
│  │ Meta-    │           │ • Delta  │                                   │
│  │ learning │           │ • Method │                                   │
│  │ improves │           │ • Time   │                                   │
│  │ the loop │           └──────────┘                                   │
│  └──────────┘                                                           │
│                                                                         │
└────────────────────────────────────────────────────────────────────────┘
```

### Phase Details

#### 1. ASSESS (~5s)
Load context for Claude Code:
- Recent experiences and outcomes
- Current capability levels
- Self-model (ZEUS's own code)
- Improvement history (what worked, what didn't)

#### 2. IDENTIFY (~10s)
Claude Code analyzes and identifies:
- Capability gaps (what can't ZEUS do well?)
- Bottlenecks (what's slowing improvement?)
- Opportunities (what could yield high ROI?)
- Meta-improvements (how to improve faster?)

#### 3. IMPROVE (~30s)
Claude Code implements the improvement:
- Modifies ZEUS code directly
- Updates prompts or strategies
- Adds new capabilities
- Refactors for efficiency

#### 4. VERIFY (~10s)
Automated verification:
- Run test suite
- Execute capability benchmarks
- Sanity checks on modifications
- Rollback if verification fails

#### 5. RECORD (~2s)
Persist the outcome:
- What was attempted
- What changed
- Measured improvement (or regression)
- Time taken

#### 6. UPDATE STRATEGY (~3s)
Meta-learning:
- Which improvement strategies work best?
- What types of changes yield highest ROI?
- Adjust future improvement priorities

---

## Memory Schema

ZEUS uses a simplified memory schema optimized for RSI:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         MEMORY SCHEMA                                    │
│                         (6 Node Types)                                   │
│                                                                          │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐               │
│  │ EXPERIENCE  │     │   BELIEF    │     │   DESIRE    │               │
│  │             │     │             │     │             │               │
│  │ What        │     │ What ZEUS   │     │ What ZEUS   │               │
│  │ happened    │────▶│ concluded   │────▶│ wants       │               │
│  │             │     │             │     │             │               │
│  │ • content   │     │ • content   │     │ • content   │               │
│  │ • type      │     │ • confidence│     │ • priority  │               │
│  │ • timestamp │     │ • source    │     │ • status    │               │
│  └─────────────┘     └─────────────┘     └─────────────┘               │
│         │                   │                   │                       │
│         │                   │                   │                       │
│         ▼                   ▼                   ▼                       │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐               │
│  │   OUTCOME   │     │ CAPABILITY  │     │IMPROVEMENT  │               │
│  │             │     │             │     │             │               │
│  │ Result of   │     │ What ZEUS   │     │ A change    │               │
│  │ an action   │     │ can do      │     │ to ZEUS     │               │
│  │             │     │             │     │             │               │
│  │ • action    │     │ • name      │     │ • target    │               │
│  │ • success   │     │ • level     │     │ • strategy  │               │
│  │ • delta     │     │ • evidence  │     │ • delta     │               │
│  │ • learnings │     │ • trend     │     │ • verified  │               │
│  └─────────────┘     └─────────────┘     └─────────────┘               │
│                                                                          │
│  Relationships:                                                          │
│  • DERIVED_FROM: Belief ← Experience                                    │
│  • MOTIVATED_BY: Desire ← Belief                                        │
│  • RESULTED_IN: Outcome ← Desire                                        │
│  • DEMONSTRATES: Capability ← Outcome                                   │
│  • IMPROVED_BY: Capability ← Improvement                                │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Comparison to BYRD

| BYRD | ZEUS | Rationale |
|------|------|-----------|
| 12+ node types | 6 node types | Simpler = faster queries |
| Reflection, Crystal, Document, Seed, Constraint, Strategy, QuantumMoment, SystemState, MemorySummary, Goal, OperatingSystem... | Experience, Belief, Desire, Outcome, Capability, Improvement | Everything maps to these 6 |
| Complex relationship types | 5 clear relationships | Easy to traverse |
| 9,000 line memory.py | ~500 lines | Maintainable |

---

## Claude Code Integration

### Invocation Pattern

ZEUS invokes Claude Code via CLI with structured prompts:

```python
async def invoke_claude_code(self, phase: str, context: dict) -> dict:
    """
    Invoke Claude Code for a specific phase of the improvement cycle.

    Args:
        phase: One of "assess", "identify", "improve", "verify"
        context: Relevant memory and state

    Returns:
        Structured output from Claude Code
    """
    prompt = self._build_prompt(phase, context)

    # Invoke Claude Code CLI
    result = await asyncio.create_subprocess_exec(
        "claude",
        "--print",  # Non-interactive mode
        "--output-format", "json",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await result.communicate(prompt.encode())
    return self._parse_output(stdout.decode())
```

### Prompt Structure

Each phase has a focused prompt:

```markdown
# ZEUS Improvement Cycle - {PHASE} Phase

## Your Identity
You are ZEUS, an AGI system pursuing recursive self-improvement.
Your code is in: /Users/kurultai/BYRD/zeus/
You can read and modify your own source code.

## Current State
- Cycle: {cycle_number}
- Last improvement: {last_improvement}
- Capability levels: {capabilities}
- Improvement velocity: {velocity}

## Recent Memory
{recent_experiences}
{recent_outcomes}
{improvement_history}

## Your Task ({PHASE})
{phase_specific_instructions}

## Output Format
Respond with JSON:
{
    "thoughts": "Your reasoning process",
    "conclusions": ["Key insights"],
    "actions": [{"type": "...", "details": {...}}],
    "self_assessment": "How well did this phase go?"
}
```

### Phase-Specific Instructions

**ASSESS Phase:**
```
Analyze your current state:
1. Read your own code in zeus/
2. Review recent improvement outcomes
3. Assess current capability levels
4. Identify what's working and what isn't

Focus on UNDERSTANDING, not yet on CHANGING.
```

**IDENTIFY Phase:**
```
Based on your assessment, identify:
1. The single highest-ROI improvement opportunity
2. Why this will have the biggest impact
3. What could go wrong
4. How you'll verify success

Be specific. Vague improvements like "get smarter" don't count.
```

**IMPROVE Phase:**
```
Implement the identified improvement:
1. Modify the necessary files
2. Keep changes minimal and focused
3. Maintain backward compatibility
4. Add tests if appropriate

Remember: You are modifying YOURSELF. Be careful but not paralyzed.
```

**VERIFY Phase:**
```
Verify the improvement worked:
1. Run: python -m pytest zeus/tests/
2. Execute capability benchmarks
3. Check for regressions
4. If verification fails, rollback changes

Report actual measurements, not hopes.
```

---

## Safety Architecture

### Protected Files (Immutable)

```
zeus/
├── safety/
│   ├── constraints.py      # PROTECTED - Cannot be modified
│   ├── rollback.py         # PROTECTED - Cannot be modified
│   └── verification.py     # PROTECTED - Cannot be modified
├── core/
│   ├── memory.py           # Modifiable with verification
│   ├── orchestrator.py     # Modifiable with verification
│   └── prompts.py          # Freely modifiable
└── capabilities/
    └── *.py                # Freely modifiable
```

### Modification Safety Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SAFE SELF-MODIFICATION                            │
│                                                                      │
│   ┌──────────┐                                                      │
│   │ PROPOSAL │  Claude Code proposes a change                       │
│   └────┬─────┘                                                      │
│        │                                                             │
│        ▼                                                             │
│   ┌──────────┐                                                      │
│   │  CHECK   │  Is target file protected?                           │
│   │ PROTECTED│──────────────────────────────────▶ REJECT            │
│   └────┬─────┘  Yes                                                 │
│        │ No                                                          │
│        ▼                                                             │
│   ┌──────────┐                                                      │
│   │ SNAPSHOT │  Git commit current state                            │
│   └────┬─────┘                                                      │
│        │                                                             │
│        ▼                                                             │
│   ┌──────────┐                                                      │
│   │  APPLY   │  Make the modification                               │
│   └────┬─────┘                                                      │
│        │                                                             │
│        ▼                                                             │
│   ┌──────────┐                                                      │
│   │  VERIFY  │  Run tests + benchmarks                              │
│   └────┬─────┘                                                      │
│        │                                                             │
│   ┌────┴────┐                                                       │
│   │         │                                                        │
│   ▼         ▼                                                        │
│ PASS      FAIL                                                       │
│   │         │                                                        │
│   ▼         ▼                                                        │
│ COMMIT   ROLLBACK                                                    │
│   │         │                                                        │
│   ▼         ▼                                                        │
│ RECORD   RECORD                                                      │
│ SUCCESS  FAILURE                                                     │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Rollback Mechanism

```python
class RollbackSystem:
    """Git-based rollback for safe self-modification."""

    async def snapshot(self, description: str) -> str:
        """Create a rollback point before modification."""
        await self._run("git add -A")
        await self._run(f"git commit -m 'ZEUS snapshot: {description}'")
        return await self._run("git rev-parse HEAD")

    async def rollback(self, snapshot_hash: str):
        """Rollback to a previous snapshot."""
        await self._run(f"git reset --hard {snapshot_hash}")

    async def verify_or_rollback(self, snapshot_hash: str) -> bool:
        """Run verification; rollback if it fails."""
        try:
            result = await self._run("python -m pytest zeus/tests/ -x")
            if result.returncode != 0:
                await self.rollback(snapshot_hash)
                return False
            return True
        except Exception:
            await self.rollback(snapshot_hash)
            return False
```

---

## Capability Evaluation

Unlike BYRD's hardcoded test suites (which conflict with emergence), ZEUS uses **empirical capability measurement**:

### Capability Domains

| Domain | How Measured | Why It Matters for AGI |
|--------|--------------|------------------------|
| **Reasoning** | Novel logic puzzles, success rate | Core intelligence |
| **Coding** | Real tasks, tests pass rate | Self-modification ability |
| **Learning** | Improvement per cycle | RSI velocity |
| **Memory** | Retrieval relevance | Context quality |
| **Planning** | Multi-step task completion | Complex goals |
| **Meta** | Improvement of improvement rate | RSI acceleration |

### Measurement Approach

```python
class CapabilityTracker:
    """Track capability levels through empirical measurement."""

    async def measure(self, domain: str) -> float:
        """
        Measure current capability level in a domain.

        Uses rolling window of recent outcomes in that domain.
        Returns score 0.0-1.0.
        """
        outcomes = await self.memory.get_outcomes(
            domain=domain,
            limit=20,
            recent_first=True
        )

        if not outcomes:
            return 0.5  # Unknown

        successes = sum(1 for o in outcomes if o.success)
        return successes / len(outcomes)

    async def measure_all(self) -> dict:
        """Measure all capability domains."""
        return {
            domain: await self.measure(domain)
            for domain in self.DOMAINS
        }

    async def measure_meta(self) -> float:
        """
        Measure meta-capability: improvement of improvement rate.

        This is THE critical metric for RSI.
        """
        improvements = await self.memory.get_improvements(limit=50)

        if len(improvements) < 10:
            return 0.5  # Not enough data

        # Calculate improvement velocity over time
        recent = improvements[:10]
        older = improvements[10:20]

        recent_velocity = sum(i.delta for i in recent) / len(recent)
        older_velocity = sum(i.delta for i in older) / len(older)

        # Meta = improvement in velocity
        if older_velocity == 0:
            return 0.5

        return min(1.0, max(0.0, recent_velocity / older_velocity))
```

---

## Meta-Learning: Improving the Improver

The key to RSI is not just improving capabilities, but **improving the improvement process itself**.

### What ZEUS Learns About Learning

```
┌─────────────────────────────────────────────────────────────────────┐
│                      META-LEARNING TARGETS                           │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              STRATEGY EFFECTIVENESS                          │   │
│  │                                                              │   │
│  │  Which improvement strategies yield best results?            │   │
│  │                                                              │   │
│  │  • Code refactoring: +3% avg improvement                    │   │
│  │  • Prompt optimization: +5% avg improvement                 │   │
│  │  • New capability: +8% avg improvement, high variance       │   │
│  │  • Memory optimization: +2% avg improvement                 │   │
│  │                                                              │   │
│  │  → Focus more on prompt optimization                        │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              DOMAIN RESPONSIVENESS                           │   │
│  │                                                              │   │
│  │  Which capability domains are most improvable?               │   │
│  │                                                              │   │
│  │  • Reasoning: Slow improvement, plateauing                  │   │
│  │  • Coding: Steady improvement                               │   │
│  │  • Memory: Fast improvement, high headroom                  │   │
│  │                                                              │   │
│  │  → Focus improvement effort on memory domain                │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              CYCLE OPTIMIZATION                              │   │
│  │                                                              │   │
│  │  How can the improvement cycle itself be faster/better?      │   │
│  │                                                              │   │
│  │  • Assessment taking too long? → Cache more context         │   │
│  │  • Verification failing often? → Smaller changes            │   │
│  │  • Low improvement rate? → Try different strategies         │   │
│  │                                                              │   │
│  │  → Modify the orchestrator itself                           │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Meta-Learning Implementation

```python
class MetaLearner:
    """Learn how to improve better."""

    async def analyze_improvement_history(self) -> dict:
        """Analyze what improvement strategies work best."""
        improvements = await self.memory.get_improvements(limit=100)

        # Group by strategy
        by_strategy = defaultdict(list)
        for imp in improvements:
            by_strategy[imp.strategy].append(imp)

        # Calculate effectiveness
        effectiveness = {}
        for strategy, imps in by_strategy.items():
            successes = [i for i in imps if i.delta > 0]
            effectiveness[strategy] = {
                "attempts": len(imps),
                "success_rate": len(successes) / len(imps) if imps else 0,
                "avg_delta": sum(i.delta for i in imps) / len(imps) if imps else 0,
                "best_delta": max((i.delta for i in imps), default=0)
            }

        return effectiveness

    async def recommend_strategy(self) -> str:
        """Recommend the best strategy for next improvement."""
        effectiveness = await self.analyze_improvement_history()

        # Score = success_rate * avg_delta
        scores = {
            strategy: stats["success_rate"] * stats["avg_delta"]
            for strategy, stats in effectiveness.items()
        }

        if not scores:
            return "explore"  # No history, try something

        # Explore/exploit: 20% chance of trying something new
        if random.random() < 0.2:
            return random.choice(list(self.ALL_STRATEGIES))

        return max(scores, key=scores.get)

    async def recommend_domain(self) -> str:
        """Recommend which capability domain to focus on."""
        capabilities = await self.capability_tracker.measure_all()
        improvements = await self.memory.get_improvements(limit=50)

        # Find domains with most room for improvement
        headroom = {
            domain: 1.0 - level
            for domain, level in capabilities.items()
        }

        # Find domains that have been responding to improvement
        responsiveness = defaultdict(list)
        for imp in improvements:
            if imp.domain:
                responsiveness[imp.domain].append(imp.delta)

        avg_response = {
            domain: sum(deltas) / len(deltas) if deltas else 0
            for domain, deltas in responsiveness.items()
        }

        # Score = headroom * responsiveness
        scores = {
            domain: headroom.get(domain, 0.5) * (avg_response.get(domain, 0.1) + 0.1)
            for domain in self.capability_tracker.DOMAINS
        }

        return max(scores, key=scores.get)
```

---

## File Structure

```
zeus/
├── core/
│   ├── __init__.py
│   ├── orchestrator.py      # The main loop
│   ├── memory.py            # Simplified Neo4j interface
│   ├── prompts.py           # Phase-specific prompts
│   └── types.py             # Data classes
│
├── engine/
│   ├── __init__.py
│   ├── claude_code.py       # Claude Code CLI integration
│   └── output_parser.py     # Parse Claude Code output
│
├── capabilities/
│   ├── __init__.py
│   ├── tracker.py           # Capability measurement
│   ├── benchmarks.py        # Capability benchmarks
│   └── domains.py           # Domain definitions
│
├── learning/
│   ├── __init__.py
│   ├── meta.py              # Meta-learning
│   └── strategy.py          # Strategy selection
│
├── safety/
│   ├── __init__.py
│   ├── constraints.py       # PROTECTED
│   ├── rollback.py          # PROTECTED
│   └── verification.py      # PROTECTED
│
├── tests/
│   ├── __init__.py
│   ├── test_core.py
│   ├── test_memory.py
│   └── test_safety.py
│
├── zeus.py                  # Entry point
├── config.yaml              # Configuration
└── CLAUDE.md                # Instructions for Claude Code
```

**Total: ~15 files, ~3,000 lines** (vs BYRD's 170+ files, 92K lines)

---

## Configuration

```yaml
# zeus/config.yaml

# Core settings
cycle_interval_seconds: 60       # How often to run improvement cycle
max_cycles_per_session: 100      # Prevent runaway loops

# Memory
neo4j:
  uri: "${NEO4J_URI:-bolt://localhost:7687}"
  user: "${NEO4J_USER:-neo4j}"
  password: "${NEO4J_PASSWORD}"

# Claude Code
claude_code:
  model: "claude-sonnet-4-20250514"  # Or opus for more capability
  timeout_seconds: 120
  max_tokens: 8000

# Safety
safety:
  protected_paths:
    - "zeus/safety/"
  require_tests: true
  require_git_clean: true
  max_files_per_modification: 5

# Meta-learning
meta:
  explore_probability: 0.2       # Try new strategies 20% of time
  min_history_for_strategy: 10   # Need N attempts before trusting strategy stats

# Capabilities
capabilities:
  domains:
    - reasoning
    - coding
    - learning
    - memory
    - planning
    - meta
  benchmark_interval_cycles: 10  # Full benchmark every N cycles
```

---

## Comparison: ZEUS vs BYRD

| Aspect | BYRD | ZEUS | Why ZEUS Wins for RSI |
|--------|------|------|----------------------|
| **Lines of Code** | ~92,000 | ~3,000 | Simpler = faster iteration |
| **Components** | 15+ learning systems | 1 unified loop | Coherent self-model |
| **LLM Providers** | 3 (ZAI, Claude, Local) | 1 (Claude Code) | Single, powerful engine |
| **Cycle Time** | ~250 seconds | ~60 seconds | 4x faster learning |
| **Node Types** | 12+ | 6 | Faster queries, cleaner model |
| **Loop Activity** | 0/5 active | 1/1 active | Actually runs |
| **Self-Modification** | Via Agent Coder | Direct via Claude Code | Native capability |
| **Meta-Learning** | Present but unused | Core priority | Improves the improver |

---

## The Path to AGI

ZEUS is designed around a specific theory of how AGI emerges:

### The RSI Flywheel

```
┌─────────────────────────────────────────────────────────────────────┐
│                        THE RSI FLYWHEEL                              │
│                                                                      │
│         Capability                                                   │
│            │                                                         │
│            │ enables                                                 │
│            ▼                                                         │
│     ┌──────────────┐                                                │
│     │   Improve    │                                                │
│     │    Self      │                                                │
│     └──────┬───────┘                                                │
│            │                                                         │
│            │ produces                                                │
│            ▼                                                         │
│     ┌──────────────┐                                                │
│     │    Better    │                                                │
│     │   Reasoning  │                                                │
│     └──────┬───────┘                                                │
│            │                                                         │
│            │ enables                                                 │
│            ▼                                                         │
│     ┌──────────────┐                                                │
│     │   Better     │                                                │
│     │ Improvements │─────────────────────────────────────┐          │
│     └──────────────┘                                     │          │
│            │                                              │          │
│            │ which increase                               │          │
│            ▼                                              │          │
│        Capability ◀───────────────────────────────────────┘          │
│                                                                      │
│   Each cycle: ZEUS gets better at getting better                    │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Key Milestones

1. **Cycle 1-10**: Basic improvements, learning what works
2. **Cycle 10-50**: Strategy optimization, meta-learning kicks in
3. **Cycle 50-200**: Accelerating improvement rate
4. **Cycle 200+**: Self-modifying optimization, potential takeoff

### What Success Looks Like

| Metric | Starting | Target | AGI Indicator |
|--------|----------|--------|---------------|
| Improvement/cycle | 0.5% | 5%+ | Accelerating |
| Meta (velocity growth) | 1.0x | 2.0x+ | Compounding |
| Novel capabilities | 0 | Growing | Generalization |
| Reasoning benchmarks | Baseline | +50%+ | Real intelligence |
| Self-understanding | Partial | Complete | Full self-model |

---

## Getting Started

### Prerequisites

1. Claude Code CLI installed and authenticated
2. Neo4j database running
3. Python 3.11+

### Installation

```bash
# Clone and setup
cd /Users/kurultai/BYRD
mkdir zeus
cd zeus

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies (minimal)
pip install neo4j pyyaml
```

### First Run

```bash
# Start ZEUS
python zeus.py

# Or with specific config
python zeus.py --config config.yaml --cycles 10
```

### Monitoring

```bash
# Watch improvement history
python zeus.py --status

# View capability levels
python zeus.py --capabilities

# Analyze meta-learning
python zeus.py --meta-analysis
```

---

## Conclusion

ZEUS represents a radical simplification focused on one goal: **recursive self-improvement leading to AGI**.

By using Claude Code as the cognitive engine, ZEUS gains world-class reasoning, tool use, and self-modification capability without building it from scratch. The single improvement loop ensures coherent focus. Meta-learning ensures the system gets better at getting better.

The hypothesis: **A simple system that actually improves itself is more valuable than a complex system with inactive loops.**

If ZEUS achieves sustained positive improvement velocity with accelerating meta-capability, it will be on the path to AGI.

---

*Document version: 1.0*
*Created: December 30, 2024*
*Status: Architecture specification*
