# BYRD v11.0 Implementation Plan

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
- `OpenCodeAgent` must use `coordinator.llm_operation()` for all LLM calls
- Must call `coordinator.coder_started()`/`coder_finished()` around tasks
- Cannot just replace Coder - must preserve coordination semantics

**Fix**:
```python
# opencode_agent.py
class OpenCodeAgent:
    def __init__(self, ..., coordinator: ComponentCoordinator):
        self.coordinator = coordinator

    async def execute(self, task: str, context: Dict) -> AgentResult:
        # Notify coordinator
        self.coordinator.coder_started(task[:50])
        try:
            async with self.coordinator.llm_operation("opencode_execute"):
                return await self._tool_loop(task, context)
        finally:
            self.coordinator.coder_finished()
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

**Fix**: Interface-compatible replacement:
```python
# plugin_manager.py must implement:
class PluginManager:
    async def search(self, query: str) -> List[Plugin]:
        """Match AitmplClient.search() signature."""

    async def get_template(self, name: str) -> Optional[Plugin]:
        """Match AitmplClient.get_template() signature."""

    def get_trust_score(self, plugin: Plugin) -> float:
        """Match trust scoring pattern."""

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

### Issue #5: self_model.json Reading Location

**Question**: Where should BYRD read self_model.json?

**Options**:
1. **byrd.py:start()** - Once at startup
2. **dreamer.py:_reflect()** - Every dream cycle
3. **agi_runner.py:assess()** - Every improvement cycle
4. **All of the above** - Different consumers, different purposes

**Recommendation**: Layered reading:
```python
# byrd.py:start() - Load once, store reference
self.self_model = await self._load_self_model()

# dreamer.py:_build_reflection_context() - Include in context
context["self_model_summary"] = self._summarize_self_model(self.byrd.self_model)

# agi_runner.py:assess() - Read for architectural decisions
architecture = await self._read_self_model()  # May have changed
```

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

### Issue #7: Coder Selection Logic (byrd.py:265-296)

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

**Impact on Plan**:
- OpenCodeAgent is a 4th option, not a replacement
- Need to add "opencode" type
- Should it be default or opt-in?

**Fix**:
```python
# byrd.py - Add OpenCode option
if coder_type == "opencode":
    self.coder = OpenCodeAgent(
        config=coder_config,
        memory=self.memory,
        llm_client=self.llm_client,
        coordinator=self.coordinator
    )
    print(f"💻 Coder: OpenCode (GLM-4.7)")
elif coder_type == "agent":
    # Existing agent coder
elif coder_type == "cli":
    # Existing CLI coder
else:
    # Auto-detect: OpenCode > CLI > Agent
```

---

## Revised Implementation Approach

Based on the critical review, the implementation should follow this order:

### Phase 0: Interface Compatibility Layer (Sprint 0)
1. Create abstract `CoderInterface` that all coders implement
2. Create abstract `CapabilitySourceInterface` for aitmpl/plugin_manager
3. Add `goal_cascade` to strategy routing (placeholder)
4. Add OpenCode option to coder selection

### Phase 1: OpenCode Agent (Sprint 1)
- Implement with ComponentCoordinator integration
- Add as 4th coder option (opt-in first)
- Preserve all existing coder interfaces

### Phase 2: Plugin Manager (Sprint 2)
- Implement with AitmplClient-compatible interface
- Add feature flag for gradual migration
- Keep aitmpl as fallback

### Phase 3: Goal Cascade (Sprint 3)
- Implement with strategy routing integration
- Add to `_execute_pattern_strategy()`
- Add `_is_complex_task()` detection

### Phase 4: Request Evaluator (Sprint 4)
- Integrate in Dreamer reflection (Option B)
- Add evaluation metadata to desires
- Optional: Add to handle_message for explicit requests

### Phase 5: Self-Model Integration (Sprint 5)
- Load in byrd.py:start()
- Pass to components that need it
- Add to reflection context

---

## Overview

This plan implements the ZEUS philosophy merge into BYRD, including:
- **OpenCode Agent**: Unified coding/self-modification engine (replaces coder.py, actor.py, agent_coder.py)
- **Plugin Manager**: Emergent plugin discovery from awesome-opencode
- **Goal Cascade**: Complex task decomposition
- **Request Evaluator**: Autonomous sovereignty layer
- **Self-Model Integration**: BYRD reads self_model.json every cycle

---

## Phase 1: Core Infrastructure (Sprint 1-2)

### 1.1 OpenCode Agent (`opencode_agent.py`)

**Purpose**: Unified coding and self-modification engine powered by GLM-4.7

**Dependencies**: `llm_client.py`, `self_modification.py`, `memory.py`

**Implementation**:

```python
# opencode_agent.py - Core structure

class OpenCodeAgent:
    """
    BYRD's unified coding and self-modification engine.
    Powered by GLM-4.7 via ZAI API.

    Replaces: coder.py, actor.py, agent_coder.py
    """

    def __init__(self, config: Dict, memory: Memory, llm_client: LLMClient):
        self.config = config
        self.memory = memory
        self.llm = llm_client
        self.tools = self._initialize_tools()
        self.max_iterations = 100
        self.files_modified = []

    async def execute(self, task: str, context: Dict = None) -> AgentResult:
        """
        Execute a coding/modification task.

        1. Load self-awareness context (ARCHITECTURE.md, self_model.json)
        2. Run tool-calling loop until completion or loop detection
        3. Return result with provenance
        """

    async def _load_self_awareness(self) -> Dict:
        """Read BYRD's own architecture for context."""
        return {
            "architecture": await self._read_file("ARCHITECTURE.md"),
            "self_model": await self._read_file("self_model.json"),
            "instructions": await self._read_file("CLAUDE.md"),
        }

    async def _tool_loop(self, task: str, context: Dict) -> AgentResult:
        """
        Tool-calling loop with:
        - Loop detection (repeated actions, ping-pong)
        - Constitutional constraints (protected files)
        - Provenance tracking
        """

    def _detect_loop(self, history: List[ToolCall]) -> bool:
        """Detect repeated tool+args (3x) or ping-pong patterns."""

    def _check_constitutional(self, tool: str, args: Dict) -> bool:
        """Verify action doesn't violate protected files."""
```

**Tools to Implement**:
| Tool | Purpose |
|------|---------|
| `read_file` | Read file contents |
| `write_file` | Create/overwrite file |
| `edit_file` | Surgical edit with old/new string |
| `list_files` | List directory contents |
| `search_code` | Grep/ripgrep for patterns |
| `run_python` | Execute Python in sandbox |
| `finish` | Signal completion |

**Tests** (`tests/test_opencode_agent.py`):
```python
class TestOpenCodeAgent:
    async def test_simple_file_read(self):
        """Agent can read a file."""

    async def test_file_edit_with_provenance(self):
        """Edits are tracked with originating desire."""

    async def test_constitutional_protection(self):
        """Cannot modify protected files."""

    async def test_loop_detection_repeated(self):
        """Stops on 3x repeated tool+args."""

    async def test_loop_detection_pingpong(self):
        """Stops on A-B-A-B pattern."""

    async def test_self_awareness_loading(self):
        """Loads ARCHITECTURE.md and self_model.json."""

    async def test_sandbox_execution(self):
        """run_python executes in isolated subprocess."""
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

*Plan version: 1.0*
*Created: December 30, 2025*
*For: BYRD v11.0 (ZEUS Philosophy Merge)*
