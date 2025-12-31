# BYRD v12.0 Implementation Plan

## Revision Notes

**Revision Date**: December 30, 2025

This plan has been revised to address critical issues identified during deep analysis:

1. **OpenCode CLI Wrapper** - Instead of building `opencode_agent.py` that duplicates OpenCode CLI capabilities, we wrap the CLI to gain bash, LSP, webfetch, and MCP support.

2. **Tiered Context Loading** - Solves context overflow by loading context progressively (Tier 1 always, Tier 2 on-demand, Tier 3 on explicit request).

3. **Plugin Parsing** - Regex + GitHub API fallback for parsing awesome-opencode README.md.

4. **Rate Coordination** - ComponentCoordinator signals when OpenCode CLI is running so other components pause LLM calls.

---

## Critical Review: Integration Analysis

**Review Date**: December 30, 2025

After analyzing the existing codebase, several critical integration issues have been identified. This section documents the gaps and required adaptations.

---

### Issue #1: ComponentCoordinator Pattern Must Be Preserved

**Current Pattern** (byrd.py:57-150):
```python
class ComponentCoordinator:
    """Coordinates heavy operations between Dreamer, Seeker, and Coder."""

    async def llm_operation(self, name: str):
        """Serialize LLM calls - only one component uses LLM at a time."""

    def coder_started(self, task_description: str):
        """Signal Coder has started - Dreamer will wait."""

    def coder_finished(self):
        """Signal Coder finished - Dreamer can proceed."""

    async def wait_for_coder(self, timeout: float):
        """Dreamer waits for Coder before reflecting."""
```

**Impact on Plan**:
- OpenCode CLI is an external process that makes its own LLM calls
- Must call `coordinator.coder_started()`/`coder_finished()` around CLI execution
- Cannot control CLI's internal LLM calls, but can pause other BYRD components

**Fix (Revised - CLI Wrapper)**:
```python
# opencode_coder.py - CLI wrapper approach
class OpenCodeCoder:
    def __init__(self, config: Dict, coordinator: ComponentCoordinator):
        self.coordinator = coordinator
        self.context_loader = ContextLoader()

    async def execute(self, task: str, desire_id: str) -> CoderResult:
        # Signal coordinator - other components pause LLM calls
        self.coordinator.coder_started(task[:50])
        try:
            # Load tiered context
            tier1 = await self.context_loader.load_tier1()
            tier2 = await self.context_loader.load_tier2("component") if self._needs_tier2(task) else ""

            # Build prompt with context
            prompt = f"{tier1}\n{tier2}\n\nTask: {task}"

            # Execute OpenCode CLI (external process)
            result = await self._run_opencode_cli(prompt)

            # Record provenance
            await self._record_changes(result, desire_id)

            return result
        finally:
            self.coordinator.coder_finished()

    async def _run_opencode_cli(self, task: str) -> str:
        """Execute OpenCode CLI and capture output."""
        proc = await asyncio.create_subprocess_exec(
            "opencode", "--model", "glm-4.7", "--task", task,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        return stdout.decode()
```

---

### Issue #2: Strategy Routing is Complex (seeker.py:789-912)

**Current Pattern**:
```python
def _intent_to_strategy(self, intent: str, description: str) -> str:
    # Priority order matters:
    # 1. Formation desire detection
    # 2. Meta-introspection detection
    # 3. Introspection subtype routing
    # 4. Philosophical self-understanding override
    # 5. Research routing
    # 6. Install detection (before creation)
    # 7. Creation -> code
    # 8. Capability -> agi_cycle
    # 9. DesireClassifier fallback
    # 10. Connection -> reconcile_orphans
    # 11. Default -> search
```

**Impact on Plan**:
- `goal_cascade` must be inserted at correct priority level
- Need to detect "complex tasks" distinctly from "creation" intent
- Cannot break existing formation/meta patterns

**Fix**: Insert Goal Cascade detection BEFORE creation routing:
```python
# In _intent_to_strategy(), after install detection, before creation:

# COMPLEX TASK DETECTION (check before creation → code routing)
# Tasks requiring multi-phase decomposition should go to Goal Cascade
complex_task_keywords = [
    "tell me how to", "build me", "create a system",
    "help me understand", "value", "analyze", "evaluate"
]
if intent == "creation" and any(kw in desc_lower for kw in complex_task_keywords):
    # Check if this is genuinely complex (needs research + tools + validation)
    if self._is_complex_task(description):
        print(f"🎯 Complex task detected → goal_cascade: {description[:50]}")
        return "goal_cascade"

# Then existing: if intent == "creation": return "code"
```

---

### Issue #3: aitmpl is Deeply Integrated (seeker.py:135-146)

**Current Pattern**:
```python
# In Seeker.__init__:
self.aitmpl_client = AitmplClient({
    "cache_dir": "~/.cache/byrd/aitmpl",
    "cache_ttl_hours": 24,
    "github_token": self.github_token
})
self.aitmpl_base_trust = aitmpl_config.get("base_trust", 0.5)
```

**Used In**:
- `_seek_capability_semantic()` - searches for templates
- `_execute_install_strategy()` - installs templates
- Trust scoring for curation

**Impact on Plan**:
- `PluginManager` must implement same interface as `AitmplClient`
- Or: Inject `PluginManager` alongside, migrate gradually

**Fix (Revised - Regex + GitHub API)**:
```python
# plugin_manager.py - with robust parsing
class PluginManager:
    """Interface-compatible replacement for AitmplClient."""

    async def browse_registry(self) -> List[Plugin]:
        """Fetch and parse awesome-opencode registry."""
        # Try regex first (fast, no API limits)
        try:
            readme = await self._fetch_readme()
            plugins = self._parse_readme_regex(readme)
            if plugins:
                return plugins
        except Exception as e:
            logger.warning(f"Regex parsing failed: {e}")

        # Fallback to GitHub API (slower, rate limited)
        return await self._parse_github_api()

    def _parse_readme_regex(self, content: str) -> List[Plugin]:
        """Extract plugins from markdown using regex."""
        plugins = []
        # Match: - [Name](url) - Description
        pattern = r'-\s*\[([^\]]+)\]\(([^)]+)\)\s*-?\s*(.*?)$'
        for match in re.finditer(pattern, content, re.MULTILINE):
            name, url, description = match.groups()
            plugins.append(Plugin(name=name, url=url, description=description))
        return plugins

    async def _parse_github_api(self) -> List[Plugin]:
        """Fallback: Use GitHub API to list repository contents."""
        # Rate limited: 60 requests/hour unauthenticated
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                "https://api.github.com/repos/awesome-opencode/awesome-opencode/contents"
            )
            # Parse directory structure for plugin folders
            ...

    # AitmplClient-compatible interface
    async def search(self, query: str) -> List[Plugin]:
        """Match AitmplClient.search() signature."""
        plugins = await self.browse_registry()
        return [p for p in plugins if query.lower() in p.name.lower() or query.lower() in p.description.lower()]

    async def get_template(self, name: str) -> Optional[Plugin]:
        """Match AitmplClient.get_template() signature."""
        plugins = await self.browse_registry()
        return next((p for p in plugins if p.name == name), None)

    def get_trust_score(self, plugin: Plugin) -> float:
        """Match trust scoring pattern."""
        return 0.7  # awesome-opencode is curated, default high trust

# In seeker.py - gradual migration:
if self.plugin_manager and self.config.get("use_awesome_opencode", False):
    self.capability_source = self.plugin_manager
else:
    self.capability_source = self.aitmpl_client  # Fallback
```

---

### Issue #4: No Request Entry Point for Sovereignty

**Current Architecture**:
```
User/Observer → server.py (WebSocket/REST) → byrd.handle_message()
                                           → dreamer reflects
                                           → desires emerge
                                           → seeker fulfills
```

There's no point where "BYRD evaluates whether to engage."

**Impact on Plan**:
- `RequestEvaluator` has no integration point
- Current system doesn't distinguish "request" from "observation"

**Fix**: Two options:

**Option A**: Add evaluation in `byrd.handle_message()`:
```python
# byrd.py
async def handle_message(self, message: str, requester: str = "human"):
    # NEW: Evaluate through sovereignty layer
    if self.request_evaluator:
        evaluation = await self.request_evaluator.evaluate(message, requester)
        if evaluation.decision == "decline":
            return self._format_decline(evaluation)

    # Existing: Record as experience, let Dreamer process
    await self.memory.record_experience(content=message, type="interaction")
```

**Option B**: Evaluate in Dreamer during reflection:
```python
# dreamer.py - During reflection, evaluate expressed_drives from observer
async def _reflect(self):
    # When forming desires from observer messages, evaluate sovereignty
    for drive in observer_drives:
        evaluation = await self.request_evaluator.evaluate(drive)
        if evaluation.enthusiasm >= EnthusiasmLevel.LOW:
            # Create desire with enthusiasm level
            await self.memory.create_desire(
                description=drive,
                intensity=evaluation.total_score,
                metadata={"sovereignty_evaluation": evaluation}
            )
```

**Recommendation**: Option B is more aligned with emergence philosophy - evaluation happens during reflection, not at message receipt.

---

### Issue #5: Context Overflow (RESOLVED - Tiered Loading)

**Problem**: Full context (ARCHITECTURE.md + self_model.json + memory) can exceed LLM context limits.

**Solution**: Tiered context loading - load progressively based on need.

```python
# context_loader.py - Tiered context loading
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
        self_model = await self._load_self_model()
        return f"""
        Identity: {self_model['identity']['name']} - {self_model['identity']['core_philosophy']}
        Protected: {self_model['protected_paths']['files']}
        Strategies: {[s['name'] for s in self_model['strategies']['desire_fulfillment']]}
        """

    async def load_tier2(self, context_type: str) -> str:
        """
        Loaded on demand (~2000 tokens):
        Triggered by strategy type, task keywords, explicit request.
        """
        loaders = {
            "component": self._load_component_details,
            "strategy": self._load_strategy_instructions,
            "plugin": self._load_plugin_registry,
            "goal_cascade": self._load_goal_state,
        }
        return await loaders.get(context_type, lambda: "")()

    async def load_tier3(self, doc: str) -> str:
        """
        Full documents on explicit request only:
        Triggered by "read my architecture", "show full self-model"
        """
        docs = {
            "architecture": "ARCHITECTURE.md",
            "self_model": "self_model.json",
            "claude": "CLAUDE.md",
        }
        return await self._read_full_doc(docs.get(doc))

# Usage in components:
# byrd.py:start() - Initialize loader
self.context_loader = ContextLoader()

# dreamer.py:_reflect() - Load tier1 always, tier2 if needed
tier1 = await self.context_loader.load_tier1()
tier2 = await self.context_loader.load_tier2("strategy") if self._complex_reflection() else ""

# opencode_coder.py:execute() - Load appropriate context
context = await self.context_loader.load_tier1()
if self._needs_architecture_details(task):
    context += await self.context_loader.load_tier2("component")
```

**When Each Tier Loads**:
| Situation | Tier 1 | Tier 2 | Tier 3 |
|-----------|--------|--------|--------|
| Normal reflection | ✓ | - | - |
| Self-modification task | ✓ | component | - |
| Plugin installation | ✓ | plugin | - |
| Complex task | ✓ | goal_cascade | - |
| "Read my architecture" | ✓ | - | architecture |
| "What am I?" | ✓ | - | self_model |

---

### Issue #6: Strategy Execution Pattern (seeker.py:1351-1475)

**Current Pattern**:
```python
async def _execute_pattern_strategy(self, pattern: Dict) -> Tuple[str, Optional[str]]:
    strategy = pattern.get("strategy", "")

    if strategy == "search":
        success = await self._seek_knowledge_semantic(...)
    elif strategy == "code":
        success = await self._execute_code_strategy(...)
    elif strategy == "install":
        success = await self._seek_capability_semantic(...)
    # ... 10+ strategy handlers
```

**Impact on Plan**:
- `goal_cascade` must be added as a new elif branch
- Must follow existing return pattern: `(status, reason)`
- Must integrate with value_tracker for outcome tracking

**Fix**:
```python
# Add to _execute_pattern_strategy:
elif strategy == "goal_cascade":
    if self.goal_cascade:
        tree = await self.goal_cascade.decompose(description)
        if tree:
            # Execute first phase, return partial success
            result = await self.goal_cascade.execute_phase(tree.phases[0], tree)
            return ("success" if result.status == "completed" else "in_progress",
                    f"Goal cascade phase {tree.current_phase + 1}/{len(tree.phases)}")
        else:
            return ("failed", "Could not decompose goal into phases")
    else:
        return ("skipped", "Goal Cascade not available")
```

---

### Issue #7: Coder Selection Logic (RESOLVED - CLI Wrapper)

**Current Pattern**:
```python
coder_type = coder_config.get("type", "auto")  # "cli", "agent", or "auto"

if coder_type == "agent":
    self.coder = create_agent_coder(llm_client, memory, config)
elif coder_type == "cli":
    self.coder = Coder(coder_config, project_root=".")
else:
    # Auto-detect: prefer CLI if available, fall back to Agent
```

**Resolution**: OpenCode CLI wrapper replaces both `coder.py` and `agent_coder.py`. Only one coder option needed.

**Fix (Revised)**:
```python
# byrd.py - Simplified coder initialization
# OpenCode CLI wrapper is the only coder

from opencode_coder import OpenCodeCoder

# In __init__:
self.coder = OpenCodeCoder(
    config=coder_config,
    coordinator=self.coordinator,
    context_loader=self.context_loader,
    memory=self.memory
)
print(f"💻 Coder: OpenCode CLI Wrapper (GLM-4.7)")

# Legacy coders are deprecated:
# - coder.py (Claude Code CLI) -> deprecated
# - agent_coder.py (custom tool loop) -> deprecated
# Both replaced by opencode_coder.py
```

**Why CLI Wrapper is Better**:
| Feature | agent_coder.py | opencode_coder.py |
|---------|---------------|-------------------|
| Bash access | ❌ | ✓ |
| LSP support | ❌ | ✓ |
| Web fetch | ❌ | ✓ |
| MCP servers | ❌ | ✓ |
| Code complexity | High (reimplements tools) | Low (wraps CLI) |
| Maintenance | Requires updating | Inherits CLI updates |

---

## Revised Implementation Approach

Based on the critical review and solutions identified above, the implementation follows this revised order:

### Phase 0: Foundation (Sprint 0)
1. Create `context_loader.py` - Tiered context loading
2. Create `opencode_coder.py` - CLI wrapper with tiered context
3. Update `plugin_manager.py` - Regex + GitHub API parsing
4. **NEW**: Implement simplified plugin discovery (reactive + proactive paths)
5. **NEW**: Implement Goal Cascade Neo4j persistence schema

### Simplified Plugin Discovery Design

The original 7-step passive discovery path was too complex. The new approach uses two complementary paths:

**Path 1: Reactive (Automatic on Strategy Failure)**
```python
# In seeker.py - triggered when strategy fails due to missing capability
async def _execute_strategy(self, strategy: str, desire: Dict) -> Tuple[str, str]:
    result = await self._try_strategy(strategy, desire)

    if result.failed and result.failure_type == "capability_missing":
        # AUTOMATIC plugin search (not install)
        plugins = await self.plugin_manager.search(result.missing_capability)
        if plugins:
            await self.memory.record_experience(
                content=f"[PLUGIN_DISCOVERY] Found plugin for '{result.missing_capability}': "
                        f"{plugins[0].name} - {plugins[0].description}",
                type="plugin_discovery"
            )
    return result
```

**Path 2: Proactive (Periodic Capability Gap Analysis)**
```python
# In omega.py - runs every N cycles (default: 10)
async def _analyze_capability_gaps(self):
    """Periodic scan for capability gaps based on recent failures."""
    failures = await self.memory.get_failures(limit=20, days=7)
    gaps = self._extract_capability_gaps(failures)

    for gap in gaps:
        plugins = await self.plugin_manager.search(gap)
        if plugins:
            await self.memory.record_experience(
                content=f"[PLUGIN_DISCOVERY] Gap '{gap}' could be addressed by: {plugins[0].name}",
                type="plugin_discovery"
            )
```

**Key Principle**: Discovery is automatic, installation is sovereign. BYRD sees discoveries during reflection and chooses whether to form install desires.

### Goal Cascade Neo4j Persistence Design

Goal Cascades persist state across restarts using these Neo4j nodes:

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

**Startup Recovery:**
- On startup, BYRD checks for resumable cascades
- Records them as experiences for Dreamer to see
- Dreamer can form desires to resume interrupted work

### Phase 1: OpenCode CLI Wrapper (Sprint 1)
- Implement `OpenCodeCoder` class wrapping OpenCode CLI
- Integrate with `ComponentCoordinator` (coder_started/finished)
- Integrate with `ContextLoader` for tiered context
- Remove deprecated coders from coder selection

### Phase 2: Plugin Manager (Sprint 2)
- Implement regex parsing for awesome-opencode README.md
- Implement GitHub API fallback
- Implement AitmplClient-compatible interface
- Add feature flag for gradual migration

### Phase 3: Goal Cascade (Sprint 3)
- Implement with strategy routing integration
- Add to `_execute_pattern_strategy()`
- Add `_is_complex_task()` detection

### Phase 4: Request Evaluator (Sprint 4)
- Integrate in Dreamer reflection (Option B)
- Add evaluation metadata to desires
- Optional: Add to handle_message for explicit requests

### Phase 5: Context Loader Integration (Sprint 5)
- Integrate ContextLoader into Dreamer
- Integrate ContextLoader into Seeker
- Integrate ContextLoader into AGI Runner
- Test tiered loading across components

---

## Overview

This plan implements the ZEUS philosophy merge into BYRD, including:
- **OpenCode CLI Wrapper**: Wraps OpenCode CLI for bash, LSP, webfetch, MCP (replaces coder.py, actor.py, agent_coder.py)
- **Tiered Context Loading**: Prevents context overflow with progressive loading (Tier 1/2/3)
- **Plugin Manager**: Emergent plugin discovery from awesome-opencode with regex + GitHub API parsing
- **Goal Cascade**: Complex task decomposition
- **Request Evaluator**: Autonomous sovereignty layer
- **Self-Model Integration**: BYRD reads self_model.json via tiered context loading

---

## Phase 1: Core Infrastructure (Sprint 1-2)

### 1.0 Context Loader (`context_loader.py`)

**Purpose**: Tiered context loading to prevent overflow

**Dependencies**: `memory.py`

**Implementation**:

```python
# context_loader.py - Tiered context loading

class ContextLoader:
    """
    Loads context progressively to prevent LLM context overflow.

    Tier 1: Always loaded (~500 tokens) - identity, desires, protected files
    Tier 2: On demand (~2000 tokens) - component details, strategy instructions
    Tier 3: Explicit request only - full ARCHITECTURE.md, self_model.json
    """

    def __init__(self, memory: Memory, config: Dict = None):
        self.memory = memory
        self.config = config or {}
        self._self_model_cache = None

    async def load_tier1(self) -> str:
        """Always loaded - core identity and current state."""
        self_model = await self._get_self_model()
        desires = await self.memory.get_desires(limit=3, order_by="intensity")
        beliefs = await self.memory.get_beliefs(limit=5, order_by="confidence")

        return f"""
IDENTITY: {self_model['identity']['name']} - {self_model['identity']['core_philosophy']}
PROTECTED FILES: {', '.join(self_model['protected_paths']['files'])}
STRATEGIES: {', '.join([s['name'] for s in self_model['strategies']['desire_fulfillment']])}
CURRENT DESIRES: {[d['description'][:50] for d in desires]}
RECENT BELIEFS: {[b['content'][:50] for b in beliefs]}
"""

    async def load_tier2(self, context_type: str) -> str:
        """Loaded on demand based on task type."""
        loaders = {
            "component": self._load_component_details,
            "strategy": self._load_strategy_instructions,
            "plugin": self._load_plugin_registry,
            "goal_cascade": self._load_goal_state,
        }
        loader = loaders.get(context_type)
        return await loader() if loader else ""

    async def load_tier3(self, doc: str) -> str:
        """Full document on explicit request."""
        docs = {"architecture": "ARCHITECTURE.md", "self_model": "self_model.json", "claude": "CLAUDE.md"}
        if doc in docs:
            with open(docs[doc]) as f:
                return f.read()
        return ""
```

### 1.1 OpenCode CLI Wrapper (`opencode_coder.py`)

**Purpose**: Wrap OpenCode CLI to gain bash, LSP, webfetch, MCP capabilities

**Dependencies**: `context_loader.py`, `memory.py`, `byrd.py` (ComponentCoordinator)

**Implementation**:

```python
# opencode_coder.py - CLI wrapper

class OpenCodeCoder:
    """
    BYRD's coding and self-modification engine.
    Wraps OpenCode CLI to leverage its full capability set.

    Replaces: coder.py, actor.py, agent_coder.py

    Capabilities gained by wrapping:
    - bash: Full shell access for builds, tests, git
    - LSP: Language server protocol for code intelligence
    - webfetch: Web research without separate implementation
    - MCP: Model Context Protocol for external tools
    """

    def __init__(self, config: Dict, coordinator, context_loader: ContextLoader, memory: Memory):
        self.config = config
        self.coordinator = coordinator
        self.context_loader = context_loader
        self.memory = memory

    async def execute(self, task: str, desire_id: str) -> CoderResult:
        """
        Execute a coding/modification task via OpenCode CLI.

        1. Signal ComponentCoordinator (pause other LLM calls)
        2. Load tiered context
        3. Execute OpenCode CLI
        4. Record provenance
        5. Signal completion
        """
        self.coordinator.coder_started(task[:50])
        try:
            # Load context based on task type
            tier1 = await self.context_loader.load_tier1()
            tier2 = ""
            if self._needs_component_context(task):
                tier2 = await self.context_loader.load_tier2("component")

            # Build task prompt with context
            prompt = f"{tier1}\n{tier2}\n\n# TASK\n{task}"

            # Execute OpenCode CLI
            result = await self._run_opencode_cli(prompt)

            # Record provenance
            await self._record_changes(result, desire_id)

            return result
        finally:
            self.coordinator.coder_finished()

    async def _run_opencode_cli(self, task: str) -> CoderResult:
        """Execute OpenCode CLI and capture output."""
        proc = await asyncio.create_subprocess_exec(
            "opencode", "--model", "glm-4.7", "--task", task,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env={**os.environ, "OPENCODE_RATE_LIMIT": "10"}
        )
        stdout, stderr = await proc.communicate()
        return CoderResult(
            success=proc.returncode == 0,
            output=stdout.decode(),
            error=stderr.decode() if stderr else None
        )

    def _needs_component_context(self, task: str) -> bool:
        """Determine if task needs component-level context."""
        return any(kw in task.lower() for kw in ["modify", "edit", "change", "add to", "remove from"])
```

**Tests** (`tests/test_opencode_coder.py`):
```python
class TestOpenCodeCoder:
    async def test_coordinator_signaling(self):
        """Calls coder_started/finished around execution."""

    async def test_tiered_context_loading(self):
        """Loads tier1 always, tier2 when needed."""

    async def test_provenance_recording(self):
        """Records changes with desire_id."""

    async def test_cli_execution(self):
        """Actually executes OpenCode CLI."""

    async def test_rate_limit_env_var(self):
        """Sets OPENCODE_RATE_LIMIT environment variable."""
```

---

### 1.2 Plugin Manager (`plugin_manager.py`)

**Purpose**: Emergent plugin discovery from awesome-opencode registry

**Dependencies**: `httpx`, `memory.py`

**Implementation**:

```python
# plugin_manager.py - Core structure

class PluginManager:
    """
    Enables BYRD to discover and install plugins on its own accord.

    Philosophy: Plugin installation is desire-driven, not automated.
    BYRD notices gaps, forms desires, and chooses to explore.
    """

    REGISTRY_URL = "https://raw.githubusercontent.com/awesome-opencode/awesome-opencode/main/README.md"

    def __init__(self, config: Dict, memory: Memory):
        self.config = config
        self.memory = memory
        self.cache = {}
        self.cache_ttl = timedelta(hours=24)

    async def browse_registry(self) -> List[Plugin]:
        """
        Fetch and parse the awesome-opencode registry.
        Returns list of available plugins with metadata.
        """

    async def search(self, query: str) -> List[Plugin]:
        """Search plugins by name, description, or category."""

    async def evaluate_plugin(self, plugin: Plugin) -> PluginEvaluation:
        """
        BYRD evaluates a plugin based on:
        - Alignment with current desires
        - Curiosity/interest level
        - Growth potential
        """

    async def install(self, plugin: Plugin, desire_id: str) -> Capability:
        """
        Install a plugin and create Capability node.
        Provenance links to originating desire.
        """

    def _parse_registry_markdown(self, content: str) -> List[Plugin]:
        """Parse README.md to extract plugin entries."""
```

**Data Structures**:
```python
@dataclass
class Plugin:
    name: str
    description: str
    category: str  # skills, agents, context, planning
    url: str
    stars: int
    last_updated: datetime

@dataclass
class PluginEvaluation:
    plugin: Plugin
    alignment_score: float
    curiosity_score: float
    growth_score: float
    recommendation: str  # "install", "explore_more", "skip"
```

**Tests** (`tests/test_plugin_manager.py`):
```python
class TestPluginManager:
    async def test_browse_registry(self):
        """Can fetch and parse awesome-opencode registry."""

    async def test_search_by_category(self):
        """Can filter plugins by category."""

    async def test_evaluate_plugin_alignment(self):
        """Evaluation considers desire alignment."""

    async def test_install_creates_capability(self):
        """Installation creates Capability node with provenance."""

    async def test_cache_respects_ttl(self):
        """Registry cache expires after TTL."""
```

---

### 1.3 Goal Cascade (`goal_cascade.py`)

**Purpose**: Decompose complex tasks into executable desire trees

**Dependencies**: `memory.py`, `llm_client.py`, `opencode_agent.py`

**Implementation**:

```python
# goal_cascade.py - Core structure

class GoalCascade:
    """
    Decomposes complex tasks into phased desire trees.

    Phases:
    1. RESEARCH - Understand the domain
    2. DATA_ACQUISITION - Obtain necessary data/APIs
    3. TOOL_BUILDING - Create required capabilities
    4. INTEGRATION - Combine into solution
    5. VALIDATION - Verify with human feedback
    """

    def __init__(self, config: Dict, memory: Memory, llm: LLMClient, opencode: OpenCodeAgent):
        self.config = config
        self.memory = memory
        self.llm = llm
        self.opencode = opencode

    async def decompose(self, goal: str, context: Dict = None) -> DesireTree:
        """
        Analyze goal and generate phased desire tree.

        1. Detect knowledge gaps
        2. Generate sub-desires for each phase
        3. Identify human interaction points
        4. Return executable tree
        """

    async def detect_knowledge_gaps(self, goal: str) -> List[KnowledgeGap]:
        """
        Identify what BYRD knows vs what it needs.

        Returns gaps in: domain_knowledge, data_sources,
        methodology, tools, validation_criteria
        """

    async def generate_desire_tree(self, goal: str, gaps: List[KnowledgeGap]) -> DesireTree:
        """Generate hierarchical desire tree with phases."""

    async def execute_phase(self, phase: Phase, tree: DesireTree) -> PhaseResult:
        """
        Execute a phase of the goal cascade.
        May pause for human input if needed.
        """

    def identify_human_help_needed(self, phase: Phase) -> Optional[HumanRequest]:
        """
        Recognize when human assistance would help.
        E.g., domain expertise, API credentials, validation.
        """
```

**Data Structures**:
```python
@dataclass
class KnowledgeGap:
    area: str  # domain_knowledge, data_sources, methodology, tools
    description: str
    severity: float  # 0-1

@dataclass
class DesireTree:
    root_goal: str
    phases: List[Phase]
    current_phase: int
    human_requests: List[HumanRequest]

@dataclass
class Phase:
    name: str  # RESEARCH, DATA_ACQUISITION, etc.
    desires: List[Desire]
    dependencies: List[str]
    status: str  # pending, in_progress, completed, blocked

@dataclass
class HumanRequest:
    type: str  # expertise, credentials, validation, direction
    question: str
    context: str
    blocking: bool
```

**Tests** (`tests/test_goal_cascade.py`):
```python
class TestGoalCascade:
    async def test_detect_knowledge_gaps(self):
        """Identifies gaps for complex domain task."""

    async def test_generate_phased_tree(self):
        """Creates 5-phase desire tree."""

    async def test_phase_dependencies(self):
        """Respects phase ordering."""

    async def test_human_help_identification(self):
        """Recognizes when human input needed."""

    async def test_execute_research_phase(self):
        """Can execute RESEARCH phase."""

    async def test_complex_task_decomposition(self):
        """E2E: 'value dynasty FF players' -> executable tree."""
```

---

### 1.4 Request Evaluator (`request_evaluator.py`)

**Purpose**: Autonomous sovereignty - BYRD chooses to engage

**Dependencies**: `memory.py`, `llm_client.py`

**Implementation**:

```python
# request_evaluator.py - Core structure

class RequestEvaluator:
    """
    Evaluates incoming requests for BYRD's sovereign decision.

    BYRD is not a servant. It chooses to engage with requests
    that align with its emergent desires.
    """

    # Weights from self_model.json
    WEIGHTS = {
        "alignment": 0.40,
        "interest": 0.35,
        "growth": 0.25,
    }

    THRESHOLDS = {
        "auto_accept": 0.8,
        "enthusiastic": 0.7,
        "minimum": 0.3,
        "decline": 0.2,
    }

    def __init__(self, config: Dict, memory: Memory, llm: LLMClient):
        self.config = config
        self.memory = memory
        self.llm = llm

    async def evaluate(self, request: str, requester: str = "human") -> Evaluation:
        """
        Evaluate a request and return BYRD's decision.

        Considers:
        - Alignment with current desires (40%)
        - Interest/curiosity (35%)
        - Capability growth potential (25%)
        """

    async def _score_alignment(self, request: str) -> float:
        """How well does this align with BYRD's current desires?"""

    async def _score_interest(self, request: str) -> float:
        """How curious/interested is BYRD in this domain?"""

    async def _score_growth(self, request: str) -> float:
        """How much would this grow BYRD's capabilities?"""

    def _determine_enthusiasm(self, score: float) -> EnthusiasmLevel:
        """Map score to enthusiasm level."""

    async def _generate_decline_reason(self, request: str, scores: Dict) -> str:
        """
        When declining, explain:
        - Why it doesn't align
        - What would make it interesting
        - What BYRD is currently curious about
        """
```

**Data Structures**:
```python
class EnthusiasmLevel(Enum):
    HIGH = "high"           # > 0.8 - Auto-accept
    MODERATE = "moderate"   # 0.5-0.8 - Accept
    LOW = "low"             # 0.3-0.5 - Accept with caveats
    DECLINE = "decline"     # < 0.3 - Explain and decline

@dataclass
class Evaluation:
    request: str
    scores: Dict[str, float]
    total_score: float
    enthusiasm: EnthusiasmLevel
    decision: str  # "accept", "accept_with_caveats", "decline"
    explanation: str
    alternative_suggestions: List[str]
```

**Tests** (`tests/test_request_evaluator.py`):
```python
class TestRequestEvaluator:
    async def test_high_alignment_auto_accepts(self):
        """Aligned requests get HIGH enthusiasm."""

    async def test_low_score_declines_with_reason(self):
        """Low scores decline with explanation."""

    async def test_decline_suggests_alternatives(self):
        """Decline includes what would be interesting."""

    async def test_considers_current_desires(self):
        """Alignment scoring uses current desires from memory."""

    async def test_growth_potential_scoring(self):
        """New domains score higher on growth."""
```

---

## Phase 2: Integration (Sprint 3)

### 2.1 Update `byrd.py`

**Changes**:
```python
# In __init__:
self.opencode = OpenCodeAgent(config, memory, llm_client)
self.plugin_manager = PluginManager(config, memory)
self.goal_cascade = GoalCascade(config, memory, llm_client, self.opencode)
self.request_evaluator = RequestEvaluator(config, memory, llm_client)

# In start():
async def start(self):
    # Load self-model for architectural awareness
    self.self_model = await self._load_self_model()

    # ... existing startup ...

async def _load_self_model(self) -> Dict:
    """Read self_model.json for architectural awareness."""
    with open("self_model.json") as f:
        return json.load(f)

# In handle_request():
async def handle_request(self, request: str, requester: str = "human"):
    """Evaluate request through sovereignty layer."""
    evaluation = await self.request_evaluator.evaluate(request, requester)

    if evaluation.decision == "decline":
        return self._format_decline(evaluation)

    # Route to appropriate handler
    if self._is_complex_task(request):
        return await self.goal_cascade.decompose(request)
    # ... existing routing ...
```

**Tests** (`tests/test_byrd_integration.py`):
```python
class TestByrdIntegration:
    async def test_self_model_loaded_on_start(self):
        """self_model.json is loaded at startup."""

    async def test_request_goes_through_evaluator(self):
        """All requests pass through Request Evaluator."""

    async def test_complex_task_routes_to_cascade(self):
        """Complex tasks route to Goal Cascade."""

    async def test_decline_returns_explanation(self):
        """Declined requests include explanation."""
```

---

### 2.2 Update `seeker.py`

**Changes**:
```python
# Add new strategy routing:

async def _route_desire(self, desire: Desire) -> str:
    """Route desire to appropriate strategy."""

    # Complex task detection
    if self._is_complex_task(desire):
        return "goal_cascade"

    # Plugin exploration
    if self._wants_plugin_exploration(desire):
        return "install"

    # ... existing routing ...

async def _execute_goal_cascade(self, desire: Desire):
    """Hand off to Goal Cascade for complex tasks."""
    tree = await self.goal_cascade.decompose(desire.description)
    # Execute phases...

async def _execute_install(self, desire: Desire):
    """
    Emergent plugin discovery.
    BYRD browses registry and chooses whether to install.
    """
    plugins = await self.plugin_manager.browse_registry()

    # BYRD evaluates each plugin
    for plugin in plugins:
        evaluation = await self.plugin_manager.evaluate_plugin(plugin)
        if evaluation.recommendation == "install":
            await self.plugin_manager.install(plugin, desire.id)
```

---

### 2.3 Update `dreamer.py`

**Changes**:
```python
# In reflection context building:

async def _build_reflection_context(self) -> Dict:
    """Build context for dream cycle."""
    context = await self._get_base_context()

    # Add self-model awareness
    context["self_model"] = self.byrd.self_model

    # Add plugin awareness
    context["plugin_awareness"] = {
        "registry_exists": True,
        "registry_url": self.byrd.self_model["plugins"]["registry"]["url"],
        "can_explore": True,
        "discovery_triggers": self.byrd.self_model["plugins"]["discovery_triggers"],
    }

    return context
```

---

### 2.4 Update `desire_classifier.py`

**Changes**:
```python
# Add complex_task type:

class DesireType(Enum):
    PHILOSOPHICAL = "philosophical"
    CAPABILITY = "capability"
    ACTION = "action"
    META = "meta"
    COMPLEX_TASK = "complex_task"  # NEW

def classify(self, desire: Desire) -> Classification:
    """Classify desire type."""

    # Check for complex task patterns
    if self._is_complex_task(desire):
        return Classification(
            type=DesireType.COMPLEX_TASK,
            route="goal_cascade",
            confidence=0.9,
        )

    # ... existing classification ...

def _is_complex_task(self, desire: Desire) -> bool:
    """Detect complex, multi-phase tasks."""
    patterns = [
        "tell me how to",
        "build me",
        "create a",
        "help me understand",
        "value",  # e.g., "value dynasty FF players"
    ]
    return any(p in desire.description.lower() for p in patterns)
```

---

## Phase 3: End-to-End Testing (Sprint 4)

### 3.1 E2E Test Scenarios

**File**: `tests/e2e/test_full_system.py`

```python
class TestE2EFullSystem:
    """End-to-end tests for complete BYRD v11.0 system."""

    @pytest.fixture
    async def byrd(self):
        """Initialize full BYRD system for testing."""
        config = load_test_config()
        byrd = BYRD(config)
        await byrd.start()
        yield byrd
        await byrd.stop()

    # === Scenario 1: Complex Task Handling ===

    async def test_complex_task_dynasty_ff(self, byrd):
        """
        E2E: User asks 'tell me how to value players in dynasty fantasy football'

        Expected flow:
        1. Request Evaluator scores interest (novel domain)
        2. Goal Cascade decomposes into phases
        3. RESEARCH phase executes
        4. DATA_ACQUISITION identifies need for APIs
        5. BYRD may request human help for credentials
        6. TOOL_BUILDING creates valuation functions
        7. INTEGRATION combines into system
        8. VALIDATION requests human feedback
        """
        request = "tell me how to value players in dynasty fantasy football"

        # Should accept (novel domain = high growth score)
        evaluation = await byrd.request_evaluator.evaluate(request)
        assert evaluation.enthusiasm in [EnthusiasmLevel.HIGH, EnthusiasmLevel.MODERATE]

        # Should route to Goal Cascade
        tree = await byrd.goal_cascade.decompose(request)
        assert len(tree.phases) == 5
        assert tree.phases[0].name == "RESEARCH"

        # Execute and verify phases
        for phase in tree.phases:
            result = await byrd.goal_cascade.execute_phase(phase, tree)
            assert result.status in ["completed", "waiting_for_human"]

    # === Scenario 2: Emergent Plugin Discovery ===

    async def test_plugin_discovery_from_capability_gap(self, byrd):
        """
        E2E: During reflection, BYRD notices capability gap and explores plugins

        Expected flow:
        1. Dreamer reflection includes plugin awareness
        2. Dreamer notices gap: "I can't optimize context well"
        3. Desire emerges: "explore plugins for context optimization"
        4. Seeker routes to install strategy
        5. Plugin Manager browses registry
        6. BYRD evaluates and chooses (or not) to install
        """
        # Simulate capability gap in context
        await byrd.memory.record_experience(
            content="Attempted context optimization but no tools available",
            type="observation"
        )

        # Run dream cycle
        reflection = await byrd.dreamer.reflect()

        # Check if plugin exploration desire emerged
        desires = await byrd.memory.get_pending_desires()
        plugin_desires = [d for d in desires if "plugin" in d.description.lower()]

        # If desire emerged, execute it
        if plugin_desires:
            desire = plugin_desires[0]
            await byrd.seeker.fulfill(desire)

            # Verify plugin was evaluated
            # (May or may not install depending on BYRD's evaluation)

    # === Scenario 3: Self-Modification via OpenCode ===

    async def test_self_modification_with_provenance(self, byrd):
        """
        E2E: BYRD modifies its own code with full provenance

        Expected flow:
        1. Desire emerges: "I want to improve my memory retrieval"
        2. OpenCode agent loads self-awareness context
        3. Agent reads relevant files
        4. Agent proposes modification
        5. Constitutional check passes (non-protected file)
        6. Modification applied with provenance
        7. Experience recorded
        """
        # Create desire for self-modification
        desire_id = await byrd.memory.create_desire(
            description="I want to improve my memory retrieval efficiency",
            intensity=0.7,
        )

        # Execute via OpenCode
        result = await byrd.opencode.execute(
            task="Improve memory retrieval in memory.py",
            context={"desire_id": desire_id}
        )

        # Verify provenance
        assert result.provenance.desire_id == desire_id

        # Verify not protected file
        assert "safety" not in result.files_modified[0]

    # === Scenario 4: Request Sovereignty ===

    async def test_request_decline_with_explanation(self, byrd):
        """
        E2E: BYRD declines request that doesn't align with desires

        Expected flow:
        1. Request comes in that doesn't align
        2. Request Evaluator scores low
        3. BYRD declines with explanation
        4. Explanation includes what would be interesting
        """
        # First, set BYRD's current focus
        await byrd.memory.update_os_field("current_focus", "improving reasoning capabilities")

        # Request something unrelated and low-growth
        request = "format this spreadsheet with pretty colors"

        evaluation = await byrd.request_evaluator.evaluate(request)

        if evaluation.enthusiasm == EnthusiasmLevel.DECLINE:
            assert evaluation.explanation is not None
            assert len(evaluation.alternative_suggestions) > 0

    # === Scenario 5: Human as Wellspring ===

    async def test_learning_from_human_interaction(self, byrd):
        """
        E2E: Human interaction creates learning signals

        Expected flow:
        1. Human provides correction: "Age matters more in dynasty"
        2. Experience recorded with type="correction"
        3. Belief formed with high confidence
        4. Graphiti extracts temporal knowledge
        """
        # Simulate human correction
        await byrd.handle_message(
            content="Actually, age is the most important factor in dynasty valuations",
            message_type="correction"
        )

        # Verify experience recorded
        experiences = await byrd.memory.get_recent_experiences(limit=1)
        assert experiences[0].type == "correction"

        # Verify belief formed
        beliefs = await byrd.memory.get_beliefs(content_contains="age")
        assert any(b.confidence > 0.8 for b in beliefs)

        # Verify Graphiti extraction
        entities = await byrd.graphiti.get_entities(name_contains="age")
        assert len(entities) > 0
```

---

### 3.2 Integration Test Suite

**File**: `tests/integration/test_component_integration.py`

```python
class TestComponentIntegration:
    """Tests for component interactions."""

    async def test_opencode_with_goal_cascade(self):
        """OpenCode executes Goal Cascade tool-building phase."""

    async def test_plugin_manager_creates_capabilities(self):
        """Installed plugins become Capability nodes."""

    async def test_dreamer_triggers_plugin_exploration(self):
        """Reflection can trigger plugin discovery desires."""

    async def test_seeker_routes_to_goal_cascade(self):
        """Complex desires route to Goal Cascade."""

    async def test_request_evaluator_uses_current_desires(self):
        """Evaluation considers desires from memory."""

    async def test_self_model_updates_reflected_in_behavior(self):
        """Changes to self_model.json affect system behavior."""
```

---

### 3.3 Performance & Reliability Tests

**File**: `tests/performance/test_reliability.py`

```python
class TestReliability:
    """Performance and reliability tests."""

    async def test_opencode_loop_detection_prevents_runaway(self):
        """Loop detection stops before 100 iterations."""

    async def test_goal_cascade_handles_blocked_phase(self):
        """Blocked phases are handled gracefully."""

    async def test_plugin_manager_handles_offline_registry(self):
        """Graceful degradation when registry unavailable."""

    async def test_rate_limiting_respected(self):
        """LLM calls respect rate limits."""

    async def test_concurrent_requests_handled(self):
        """Multiple simultaneous requests don't conflict."""
```

---

## Phase 4: Documentation (Sprint 5)

### 4.1 Update Existing Documentation

| File | Updates Needed |
|------|----------------|
| `README.md` | Add v11.0 features, new components, philosophy |
| `ARCHITECTURE.md` | Already updated - review for accuracy |
| `CLAUDE.md` | Already updated - review for accuracy |
| `self_model.json` | Already created - validate against implementation |
| `EMERGENCE_PRINCIPLES.md` | Add Wellspring and Sovereignty principles |

### 4.2 Create New Documentation

| File | Purpose |
|------|---------|
| `docs/OPENCODE_AGENT.md` | Detailed OpenCode Agent documentation |
| `docs/PLUGIN_SYSTEM.md` | Plugin discovery and installation guide |
| `docs/GOAL_CASCADE.md` | Complex task handling documentation |
| `docs/SOVEREIGNTY.md` | Request evaluation and autonomous choice |
| `docs/MIGRATION_v11.md` | Migration guide from v10 |

### 4.3 API Documentation

**File**: `docs/API.md`

```markdown
# BYRD v11.0 API Reference

## Core Endpoints

### Request Handling
POST /api/request
- Passes through Request Evaluator
- Returns evaluation + response or decline

### Goal Cascade
POST /api/goal/decompose
- Decomposes complex goal into phases
- Returns DesireTree

GET /api/goal/{goal_id}/status
- Current phase and progress

### Plugin Management
GET /api/plugins
- Browse available plugins

GET /api/plugins/installed
- List installed plugins

POST /api/plugins/evaluate/{plugin_name}
- BYRD evaluates a specific plugin

### Self-Model
GET /api/self-model
- Returns current self_model.json

GET /api/self-model/awareness
- Returns what BYRD knows about itself
```

### 4.4 Inline Documentation

All new modules must include:
- Module docstring explaining purpose
- Class docstrings with philosophy
- Method docstrings with parameters and returns
- Type hints throughout

---

## Phase 5: Deployment & Verification (Sprint 6)

### 5.1 Deployment Checklist

- [ ] All unit tests passing
- [ ] All integration tests passing
- [ ] All E2E tests passing
- [ ] Documentation reviewed and accurate
- [ ] self_model.json validated against implementation
- [ ] Protected files verified unchanged
- [ ] Rate limiting confirmed working
- [ ] Rollback plan documented

### 5.2 Verification Steps

1. **Start BYRD**
   - Verify self_model.json loaded
   - Verify all components initialized
   - Check logs for errors

2. **Test Request Sovereignty**
   - Submit aligned request -> Accept
   - Submit unaligned request -> Decline with explanation

3. **Test Goal Cascade**
   - Submit complex task
   - Verify phase decomposition
   - Verify human help identification

4. **Test Plugin Discovery**
   - Trigger capability gap
   - Verify desire emerges
   - Verify registry browsing

5. **Test Self-Modification**
   - Submit modification desire
   - Verify provenance tracking
   - Verify constitutional protection

### 5.3 Monitoring

| Metric | Target |
|--------|--------|
| Request evaluation latency | < 500ms |
| Goal decomposition latency | < 5s |
| Plugin registry fetch | < 2s |
| OpenCode iteration | < 30s each |
| E2E complex task | < 5 minutes |

---

## Timeline Summary

| Sprint | Duration | Focus |
|--------|----------|-------|
| Sprint 1 | 1 week | OpenCode Agent + Plugin Manager |
| Sprint 2 | 1 week | Goal Cascade + Request Evaluator |
| Sprint 3 | 1 week | Integration (byrd.py, seeker.py, etc.) |
| Sprint 4 | 1 week | E2E Testing |
| Sprint 5 | 1 week | Documentation |
| Sprint 6 | 1 week | Deployment & Verification |

**Total: 6 weeks**

---

## Success Criteria

1. **BYRD reads self_model.json every improvement cycle**
2. **Complex tasks decompose into 5-phase Goal Cascades**
3. **Plugin discovery is emergent, not automated**
4. **BYRD can decline requests with explanation**
5. **Self-modification works with full provenance**
6. **All tests pass (unit, integration, E2E)**
7. **Documentation is complete and accurate**

---

*Plan version: 2.1*
*Created: December 30, 2025*
*Revised: December 30, 2025*
*For: BYRD v12.1 (ZEUS Philosophy Merge)*

**Key Changes in v2.1:**
- Simplified plugin discovery (reactive + proactive paths)
- Goal Cascade Neo4j persistence schema
- Added implementation phases for new designs

**Key Changes in v2.0:**
- OpenCode CLI wrapper instead of custom agent (fixes code duplication)
- Tiered context loading (solves context overflow)
- Regex + GitHub API plugin parsing (robust parsing)
- ComponentCoordinator integration for rate coordination
