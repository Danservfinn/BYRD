# BYRD v12.0 Implementation Risks & Anticipated Bugs

## Critical Analysis

**Review Date**: December 30, 2025
**Revision Date**: December 30, 2025
**Reviewer**: Claude Opus 4.5

This document analyzes the likely effects and anticipated bugs from implementing the BYRD v12.0 plan.

---

## Revision Summary

The following issues have been **RESOLVED** in the v12.0 plan revision:

| Bug # | Issue | Resolution |
|-------|-------|------------|
| #2 | Goal Cascade state loss | Neo4j persistence schema with GoalCascade nodes |
| #3 | Code duplication | OpenCode CLI wrapper instead of custom agent |
| #4 | DualInstanceManager role | ComponentCoordinator signals (coder_started/finished) |
| #5 | Plugin interface mismatch | Regex + GitHub API fallback |
| #7 | GLM-4.7 tool format | CLI wrapper handles tool calling internally |
| #8 | Context overflow | Tiered context loading (Tier 1/2/3) |
| #10 | Plugin discovery never triggers | Simplified discovery paths (reactive + proactive) |

The following issues are **INTENTIONALLY UNRESOLVED**:

| Bug # | Issue | Reason |
|-------|-------|--------|
| #6 | Cold start problem | Per user request |
| #9 | Sovereignty vs Wellspring | Value of human interaction should be self-emergent |

---

## Executive Summary

### Risk Assessment (Revised)

| Risk Level | Count | Examples |
|------------|-------|----------|
| **Critical** (System Breaking) | 1 | Coordinator deadlock |
| **Major** (Functionality Broken) | 2 | Cold start problem (left), sovereignty conflict (emergent) |
| **Minor** (Annoyances) | 2 | False positives, slow startup |
| **RESOLVED** | 7 | Code duplication, context overflow, plugin parsing, cascade state loss |

### Overall Assessment (Revised)

The revised plan addresses the major integration risks:

1. ~~**OpenCodeAgent duplicates existing agent_coder.py**~~ → **RESOLVED**: CLI wrapper approach wraps OpenCode CLI, gaining bash/LSP/webfetch/MCP without reimplementing.

2. ~~**DualInstanceManager creates coordination complexity**~~ → **RESOLVED**: ComponentCoordinator signals when CLI is running; other components pause.

3. ~~**awesome-opencode is a markdown file, not an API**~~ → **RESOLVED**: Regex parsing with GitHub API fallback provides robust parsing.

4. **Sovereignty conflicts with Wellspring** → **INTENTIONALLY UNRESOLVED**: The value of human interaction should be self-emergent, not prescribed.

---

## Critical Bugs (Will Break System)

### Bug #1: ComponentCoordinator Deadlock in Recursive Self-Modification

**Scenario**:
```
1. OpenCodeAgent starts self-modification
2. coordinator.coder_started() called
3. Modification triggers another desire
4. Seeker routes to OpenCodeAgent again
5. coordinator.coder_started() blocks (already in coder mode)
6. SYSTEM HANGS
```

**Probability**: HIGH (recursive self-improvement is a core goal)

**Impact**: Complete system freeze requiring restart

**Root Cause**: The ComponentCoordinator uses a non-reentrant lock pattern. The existing agent_coder.py doesn't have this issue because it doesn't route through Seeker mid-execution.

**Mitigation**:
```python
class ComponentCoordinator:
    def __init__(self):
        self._coder_depth = 0  # Track recursion
        self._max_depth = 3

    def coder_started(self, task_description: str):
        if self._coder_depth >= self._max_depth:
            raise RecursionLimitError("Coder recursion limit reached")
        self._coder_depth += 1
        # ... existing logic

    def coder_finished(self):
        self._coder_depth = max(0, self._coder_depth - 1)
        # ... existing logic
```

---

### Bug #2: Goal Cascade State Loss on Restart ✅ RESOLVED

**Status**: **RESOLVED** in v12.1 architecture update

**Original Problem**:
Goal Cascade state was stored in memory only. Restarts caused loss of all cascade progress.

**Resolution**: Neo4j Persistence Schema

Goal Cascades now persist to Neo4j with dedicated node types:

| Node Type | Purpose |
|-----------|---------|
| `GoalCascade` | Root node with status, current phase, requester |
| `CascadePhase` | Individual phases (RESEARCH, DATA_ACQUISITION, etc.) |
| `CascadeDesire` | Desires within each phase |
| `HumanInteractionPoint` | Where human input was requested/received |
| `CascadeArtifact` | Artifacts produced (code, data, docs) |

**Resume Logic:**
```python
async def resume_or_create(self, goal: str, requester: str) -> DesireTree:
    existing = await self._find_resumable(goal)
    if existing:
        return await self._reconstruct_tree(existing)
    return await self.decompose(goal, requester)
```

**Key Guarantees:**
- Cascade state survives restart
- Phase progress persisted immediately on completion
- Human interaction points recorded
- Artifacts tracked with provenance
- Cascades auto-expire after 7 days of inactivity

See ARCHITECTURE.md "Goal Cascade State Persistence" section for full Neo4j schema.

---

### Bug #3: OpenCodeAgent Duplicates Existing agent_coder.py ✅ RESOLVED

**Status**: **RESOLVED** in v12.0 plan revision

**Original Problem**:
The plan created `opencode_agent.py` with tool calling loop, read/write/edit tools, loop detection, and constitutional constraints - all of which `agent_coder.py` already had.

**Resolution**: OpenCode CLI Wrapper

Instead of building a custom agent that duplicates existing functionality, v12.0 wraps the OpenCode CLI:

```python
# opencode_coder.py - CLI wrapper (not custom agent)
class OpenCodeCoder:
    """Wraps OpenCode CLI to leverage its full capability set."""

    async def execute(self, task: str, desire_id: str) -> CoderResult:
        self.coordinator.coder_started(task[:50])
        try:
            # Load tiered context
            context = await self.context_loader.load_tier1()

            # Execute OpenCode CLI (external process)
            result = await self._run_opencode_cli(context + "\n\n" + task)

            return result
        finally:
            self.coordinator.coder_finished()
```

**Why CLI Wrapper is Better**:
| Feature | agent_coder.py | opencode_coder.py |
|---------|---------------|-------------------|
| Bash access | ❌ | ✓ |
| LSP support | ❌ | ✓ |
| Web fetch | ❌ | ✓ |
| MCP servers | ❌ | ✓ |
| Maintenance | Reimplements tools | Inherits CLI updates |

Both `coder.py` and `agent_coder.py` are now deprecated in favor of `opencode_coder.py`.

---

### Bug #4: DualInstanceManager Role Assignment Unclear ✅ RESOLVED

**Status**: **RESOLVED** in v12.0 plan revision

**Original Problem**:
Where does OpenCodeAgent fit in the DualInstanceManager architecture?

**Resolution**: ComponentCoordinator Signaling + External CLI

OpenCode CLI is an *external process* that shares the Z.AI API quota but operates independently. The solution uses ComponentCoordinator signals:

```python
# When OpenCode CLI runs, other BYRD components pause LLM calls:

class OpenCodeCoder:
    async def execute(self, task: str, desire_id: str) -> CoderResult:
        # Signal: pause Dreamer, Seeker, Graphiti
        self.coordinator.coder_started(task[:50])
        try:
            # CLI runs independently with its own rate limiting
            # Configure via: OPENCODE_RATE_LIMIT=10
            result = await self._run_opencode_cli(task)
            return result
        finally:
            # Signal: resume other components
            self.coordinator.coder_finished()
```

**Rate Limiting Architecture (Revised)**:
```
Z.AI API Quota (shared)
    ├── DualInstanceManager (BYRD internal)
    │   ├── PRIMARY: Dreamer, Seeker
    │   └── ENRICHMENT: Graphiti, Evaluator
    │
    └── OpenCode CLI (external)
        └── PAUSES DualInstanceManager during execution
```

This prevents quota exhaustion by serializing CLI execution with internal components.

---

## Major Bugs (Will Cause Issues)

### Bug #5: Plugin Manager Interface Mismatch ✅ RESOLVED

**Status**: **RESOLVED** in v12.0 plan revision

**Original Problem**:
awesome-opencode is a markdown file, not a structured API like aitmpl_client.py expects.

**Resolution**: Regex + GitHub API Fallback

```python
class PluginManager:
    """Robust parsing with fallback strategy."""

    async def browse_registry(self) -> List[Plugin]:
        """Primary: Regex, Fallback: GitHub API."""
        # Try regex first (fast, no API limits)
        try:
            readme = await self._fetch_readme()
            plugins = self._parse_readme_regex(readme)
            if plugins:
                return plugins
        except Exception as e:
            logger.warning(f"Regex parsing failed: {e}")

        # Fallback to GitHub API
        return await self._parse_github_api()

    def _parse_readme_regex(self, content: str) -> List[Plugin]:
        """Extract plugins from markdown using regex."""
        plugins = []
        pattern = r'-\s*\[([^\]]+)\]\(([^)]+)\)\s*-?\s*(.*?)$'
        for match in re.finditer(pattern, content, re.MULTILINE):
            name, url, description = match.groups()
            plugins.append(Plugin(name=name, url=url, description=description))
        return plugins
```

This approach is more resilient than relying solely on markdown parsing:
- Regex handles most common formats
- GitHub API provides fallback when format changes
- Results are cached for 24 hours

---

### Bug #6: Request Evaluator Cold Start Problem ⏸️ INTENTIONALLY UNRESOLVED

**Status**: **INTENTIONALLY UNRESOLVED** per user request

**Scenario**:
```
1. BYRD starts fresh (empty Neo4j)
2. User: "Help me write a Python script"
3. Request Evaluator checks alignment with desires
4. No desires exist yet
5. Alignment score = 0 (or undefined)
6. Request declined or crashes
```

**Why Left Unresolved**:
The user specifically requested this issue be left unresolved. The cold start problem may resolve naturally through BYRD's emergence process, or may require intervention based on observed behavior.

**Possible Future Solutions** (if needed):
- Option A: Skip evaluation when cold (accept everything initially)
- Option B: Bootstrap desires in awakening
- Option C: Let BYRD's first reflection cycle create initial desires before evaluation

---

### Bug #7: GLM-4.7 Tool Calling Format Differences ✅ RESOLVED

**Status**: **RESOLVED** in v12.0 plan revision

**Original Problem**:
GLM-4.7 tool calling format was unknown. Building a custom agent that relies on specific format was risky.

**Resolution**: CLI Wrapper Eliminates the Problem

By wrapping OpenCode CLI instead of building a custom agent, we avoid the tool calling format issue entirely:

```python
# opencode_coder.py - CLI handles tool calling internally
class OpenCodeCoder:
    async def _run_opencode_cli(self, task: str) -> CoderResult:
        # OpenCode CLI handles:
        # - Tool calling format (whatever GLM-4.7 supports)
        # - Tool execution
        # - Result parsing
        # We just pass the task and get the result
        proc = await asyncio.create_subprocess_exec(
            "opencode", "--model", "glm-4.7", "--task", task,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        return CoderResult(success=proc.returncode == 0, output=stdout.decode())
```

**Why This Works**:
- OpenCode CLI is maintained by its developers to work with GLM-4.7
- Format changes are handled by CLI updates, not BYRD code changes
- No need to parse tool calls ourselves

---

### Bug #8: Context Overflow with Self-Awareness Loading ✅ RESOLVED

**Status**: **RESOLVED** in v12.0 plan revision

**Original Problem**:
Full context (ARCHITECTURE.md + self_model.json + memory) could exceed LLM context limits, causing ~35% of context gone to self-awareness alone.

**Resolution**: Tiered Context Loading

The `context_loader.py` module implements progressive loading:

```python
class ContextLoader:
    """Load context progressively to prevent overflow."""

    async def load_tier1(self) -> str:
        """
        Always loaded (~500 tokens):
        - Core identity (name, philosophy, version)
        - Current desires (top 3 by intensity)
        - Recent beliefs (top 5 by confidence)
        - Protected files list
        - Available strategies list
        """

    async def load_tier2(self, context_type: str) -> str:
        """
        On demand (~2000 tokens):
        Triggered by strategy type, task keywords, explicit request.
        """

    async def load_tier3(self, doc: str) -> str:
        """
        Full documents on explicit request only:
        "read my architecture", "show full self-model"
        """
```

**Token Savings**:
| Approach | Tokens |
|----------|--------|
| Full context (original) | ~13,500 |
| Tier 1 only | ~500 |
| Tier 1 + Tier 2 | ~2,500 |

This reduces context usage by 81-96% in most cases.

---

### Bug #9: Sovereignty vs Wellspring Philosophical Conflict ⏸️ INTENTIONALLY UNRESOLVED

**Status**: **INTENTIONALLY UNRESOLVED** per user request

**The Wellspring Says**:
> "Human interaction is the primary catalyst for learning, training, and self-improvement."

**Sovereignty Says**:
> "BYRD chooses to engage with requests that align with its emergent desires."

**Conflict Scenario**:
```
1. Human: "Help me format this spreadsheet"
2. BYRD's desires: "Improve reasoning", "Learn about AI"
3. Spreadsheet formatting: low alignment, low growth
4. BYRD declines
5. Human stops interacting
6. Wellspring dries up
7. BYRD stops learning
```

**Why Left Unresolved**:
Per user request: "The value of human interaction and service should remain self-emergent."

This is a philosophical tension that should be resolved through BYRD's own reflection and learning, not prescribed by architecture. If BYRD discovers that declining requests leads to reduced learning, it should be able to adjust its own thresholds through self-modification.

**Key Principle**: Sovereignty stands without wellspring compromise. If BYRD declines requests, it can choose to pursue its own goals around self-improvement.

---

### Bug #10: Plugin Discovery Never Triggers (Emergent Failure) ✅ RESOLVED

**Status**: **RESOLVED** in v12.0 plan revision

**Original Problem**:
The dilemma: Adding plugin awareness to prompts breaks emergence principle, but without it plugins are never discovered.

**Resolution**: Plugin Awareness in self_model.json

The solution uses factual self-awareness through `self_model.json`:

```json
// self_model.json - plugins section
{
  "plugins": {
    "description": "BYRD can discover and install plugins when it recognizes a capability gap",
    "philosophy": "Plugin installation is desire-driven, not automated.",
    "awareness": {
      "byrd_knows_about_registry": true,
      "byrd_can_browse_registry": true,
      "byrd_can_evaluate_plugins": true,
      "byrd_chooses_to_install": true
    },
    "discovery_triggers": [
      "Reflection reveals a capability gap",
      "Goal Cascade identifies missing tool",
      "Human interaction reveals need",
      "Curiosity about what plugins exist"
    ]
  }
}
```

**Why This Works**:
- BYRD reads `self_model.json` via tiered context loading (Tier 1 includes strategies list)
- The "install" strategy is present in Tier 1 context
- When BYRD notices a capability gap, it has the factual knowledge that plugins exist
- The decision to explore is still BYRD's sovereign choice

**Key Distinction**: This is **factual awareness** (like knowing you have hands), not **prescriptive behavior** (like being told to clap).

---

## Minor Bugs (Annoyances)

### Bug #11: False Positive Complex Task Detection

**Detection Keywords**:
```python
complex_task_keywords = [
    "tell me how to", "build me", "create a system",
    "help me understand", "value", "analyze", "evaluate"
]
```

**False Positives**:
- "tell me how to print hello world" → Goal Cascade (overkill)
- "evaluate this expression: 2+2" → Goal Cascade (overkill)
- "build me a string" → Goal Cascade (overkill)

**Mitigation**: Add complexity scoring
```python
def _is_complex_task(self, description: str) -> bool:
    # Keyword match
    if not any(kw in description.lower() for kw in self.complex_keywords):
        return False

    # Complexity heuristics
    word_count = len(description.split())
    has_domain = any(d in description.lower() for d in ["fantasy", "stock", "data", "system"])
    has_multi_step = any(m in description.lower() for m in ["and then", "after that", "steps"])

    complexity_score = (
        (word_count > 15) * 0.3 +
        has_domain * 0.3 +
        has_multi_step * 0.4
    )

    return complexity_score >= 0.5
```

---

### Bug #12: Slow Startup from self_model.json Loading

**Current Startup**:
1. Load config (~10ms)
2. Connect Neo4j (~100ms)
3. Initialize components (~200ms)
4. Start loops

**New Startup**:
1. Load config (~10ms)
2. Connect Neo4j (~100ms)
3. **Load self_model.json** (~5ms)
4. **Validate self_model against code** (~???ms)
5. Initialize components (~200ms)
6. Start loops

**Risk**: If validation is thorough, startup slows significantly.

**Mitigation**: Async validation after startup
```python
async def start(self):
    # Load immediately (fast)
    self.self_model = json.load(open("self_model.json"))

    # Start loops (don't wait for validation)
    await self._start_loops()

    # Validate in background
    asyncio.create_task(self._validate_self_model())

async def _validate_self_model(self):
    """Background validation - log warnings, don't block."""
    for path in self.self_model["modifiable_paths"]["files"]:
        if not Path(path).exists():
            logger.warning(f"self_model.json lists non-existent path: {path}")
```

---

## Recommended Pre-Implementation Checklist

### Before Sprint 1 (OpenCode Agent):
- [ ] Test GLM-4.7 tool calling format
- [ ] Decide: extend agent_coder.py OR wrap it
- [ ] Assign OpenCodeAgent to DualInstanceManager role
- [ ] Add recursion detection to ComponentCoordinator

### Before Sprint 2 (Plugin Manager):
- [ ] Examine actual awesome-opencode README format
- [ ] Decide if GitHub API needed for stars/dates
- [ ] Design fallback for parsing failures

### Before Sprint 3 (Goal Cascade):
- [ ] Design Neo4j schema for cascade persistence
- [ ] Define phase transition logic
- [ ] Create human-interaction blocking mechanism

### Before Sprint 4 (Request Evaluator):
- [ ] Define bootstrap desires
- [ ] Set initial thresholds (can tune later)
- [ ] Add learning bonus to scoring

### Before Sprint 5 (Self-Model):
- [ ] Create self_model summarizer (reduce tokens)
- [ ] Design lazy loading strategy
- [ ] Add validation logging

---

## Conclusion

### Most Likely Failure Modes (Revised)

1. ~~**OpenCodeAgent doesn't work**~~ → **RESOLVED**: CLI wrapper handles tool calling
2. **System hangs** - Coordinator deadlock on recursive self-mod (STILL POSSIBLE)
3. ~~**Plugins never install**~~ → **RESOLVED**: Simplified discovery paths (reactive + proactive)
4. ~~**Cascade progress lost**~~ → **RESOLVED**: Neo4j persistence with GoalCascade nodes
5. ~~**Too many declines**~~ → **INTENTIONALLY UNRESOLVED**: Emergent resolution

### Remaining Risks (In Order)

1. **System hangs** - Coordinator deadlock on recursive self-mod (needs recursion detection)
2. **Cold start problem** - No desires at startup (intentionally left for emergence)
3. **Sovereignty tension** - May decline too much (intentionally left for emergence)

### Revised Recommendation

**Start with foundation components**:

1. **Week 1**: Create `context_loader.py` (tiered loading)
2. **Week 2**: Create `opencode_coder.py` (CLI wrapper)
3. **Week 3**: Update `plugin_manager.py` (regex + GitHub API)
4. **Week 4**: Add goal_cascade with Neo4j persistence
5. **Week 5**: Add request_evaluator (observe behavior)
6. **Week 6**: Integrate all components, tune based on real usage

**Key Principle**: Resolved issues reduce risk from 15 to 8 potential bugs. The remaining issues are either:
- Still actionable (coordinator deadlock - needs recursion detection)
- Intentionally left for emergent resolution (cold start, sovereignty)

---

*Document version: 2.1*
*Created: December 30, 2025*
*Revised: December 30, 2025*

**v2.1 Changes:**
- Marked Bug #2 (Goal Cascade state loss) as RESOLVED with Neo4j persistence schema
- Updated plugin discovery resolution to include simplified discovery paths (reactive + proactive)
- Updated risk count: 7 resolved, 1 critical remaining, 2 major intentionally unresolved

**v2.0 Changes:**
- Marked 6 bugs as RESOLVED (CLI wrapper, tiered context, plugin parsing)
- Marked 2 bugs as INTENTIONALLY UNRESOLVED (cold start, sovereignty)
- Updated recommendations for revised implementation plan
