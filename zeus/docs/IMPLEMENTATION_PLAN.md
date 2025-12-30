# ZEUS Implementation Plan

## Overview

This document provides a step-by-step implementation plan for ZEUS (Zero-overhead Unified Engine for Self-improvement). The plan is organized in phases, with each phase building on the previous one.

**Total estimated implementation**: 28 files, ~6,000-7,000 lines of code

---

## Phase 1: Core Foundation

### 1.1 Type Definitions (`core/types.py`)

Define all data classes with provenance tracking:

```python
# Key types to implement:
- Experience(id, content, type, timestamp, metadata)
- Belief(id, content, confidence, derived_from, timestamp)
- Desire(id, content, priority, status, source, metadata)
- Outcome(id, action, success, delta, learnings, timestamp)
- Capability(id, name, level, evidence, trend, domain)
- Improvement(id, target, strategy, delta, verified, motivation, desire_id)
- Reflection(id, raw_output, timestamp, cycle, source_ids)
- Concept(id, name, definition, instances, relations)
```

**Dependencies**: None
**Output**: All 8 node types with provenance fields

### 1.2 Memory Layer (`memory/memory.py`)

Neo4j interface for all 8 node types:

```python
class Memory:
    async def connect()
    async def close()

    # Experience
    async def record_experience(content, type, metadata) -> str
    async def get_experiences(type=None, limit=20) -> List[Experience]

    # Belief
    async def create_belief(content, confidence, derived_from) -> str
    async def get_beliefs(min_confidence=0.0) -> List[Belief]

    # Desire
    async def create_desire(content, priority, source, metadata) -> str
    async def get_active_desires(limit=10) -> List[Desire]
    async def update_desire_status(desire_id, status)

    # Outcome
    async def record_outcome(action, success, delta, learnings) -> str
    async def get_outcomes(domain=None, limit=20) -> List[Outcome]

    # Capability
    async def create_capability(name, level, source, metadata) -> str
    async def update_capability(name, level, evidence)
    async def get_capabilities() -> Dict[str, Capability]

    # Improvement
    async def record_improvement(target, strategy, delta, verified, motivation, desire_id) -> str
    async def get_improvements(limit=50) -> List[Improvement]

    # Reflection
    async def record_reflection(raw_output, source_ids, cycle) -> str
    async def get_recent_reflections(limit=10) -> List[Reflection]

    # Concept
    async def create_concept(name, definition, source_ids, metadata) -> str
    async def get_concepts() -> List[Concept]

    # Relationships
    async def link_nodes(from_id, to_id, relationship_type, metadata)
    async def get_similar_outcomes(strategy, target_type) -> List[Outcome]
```

**Dependencies**: `core/types.py`, neo4j driver
**Output**: Full Neo4j persistence layer

### 1.3 Configuration Loading (`core/config.py`)

```python
class Config:
    def __init__(self, path: str = "config.yaml")

    # Accessors
    @property def cycle_interval() -> int
    @property def neo4j_settings() -> dict
    @property def opencode_settings() -> dict
    @property def safety_settings() -> dict
    @property def meta_settings() -> dict
    @property def plugin_settings() -> dict
    @property def observer_settings() -> dict
```

**Dependencies**: PyYAML
**Output**: Typed configuration access

---

## Phase 2: OpenCode Engine Integration

### 2.1 Rate Limiter (`engine/rate_limiter.py`)

```python
class RateLimiter:
    def __init__(self, min_interval: float = 10.0, max_per_minute: int = 6)

    async def wait()  # Block until safe to make request
    def record_request()  # Log that request was made
    def reset()  # Reset state
```

**Dependencies**: asyncio, time
**Output**: Thread-safe rate limiting for ZAI API

### 2.2 OpenCode Integration (`engine/opencode.py`)

```python
class OpenCodeEngine:
    def __init__(self, config: dict, rate_limiter: RateLimiter)

    async def invoke(self, phase: str, context: dict) -> dict
    async def query(self, prompt: str) -> str  # Simple query

    # Internal
    def _build_prompt(self, phase: str, context: dict) -> str
    def _parse_output(self, stdout: str) -> dict
```

**Dependencies**: asyncio.subprocess, rate_limiter
**Output**: CLI wrapper with structured prompts

### 2.3 Prompt Templates (`engine/prompts.py`)

```python
# Phase-specific prompt templates
ASSESS_PROMPT = """..."""
REFLECT_PROMPT = """..."""
IDENTIFY_PROMPT = """..."""
IMPROVE_PROMPT = """..."""
VERIFY_PROMPT = """..."""
RECORD_PROMPT = """..."""
LEARN_PROMPT = """..."""

def build_prompt(phase: str, context: dict) -> str
```

**Dependencies**: None
**Output**: All RSI loop prompts

### 2.4 Output Parser (`engine/output_parser.py`)

```python
class OutputParser:
    def parse(self, output: str) -> dict
    def extract_json(self, text: str) -> dict
    def validate_output(self, parsed: dict, phase: str) -> bool
```

**Dependencies**: json, re
**Output**: Robust JSON extraction from LLM output

---

## Phase 3: Safety Layer

### 3.1 Protected File Constraints (`safety/constraints.py`) [PROTECTED]

```python
PROTECTED_PATHS = [
    "zeus/safety/",
    "zeus/config.yaml"
]

def is_protected(path: str) -> bool
def validate_modification(target: str) -> ValidationResult
```

**Dependencies**: pathlib
**Output**: Immutable protection rules

### 3.2 Rollback System (`safety/rollback.py`) [PROTECTED]

```python
class RollbackSystem:
    async def snapshot(self, description: str) -> str  # Returns commit hash
    async def rollback(self, snapshot_hash: str)
    async def verify_or_rollback(self, snapshot_hash: str) -> bool

    # Internal
    async def _run(self, cmd: str) -> subprocess.CompletedProcess
```

**Dependencies**: asyncio.subprocess, git
**Output**: Git-based safe rollback

### 3.3 Verification Runner (`safety/verification.py`) [PROTECTED]

```python
class VerificationRunner:
    async def run_tests() -> TestResult
    async def run_benchmarks() -> BenchmarkResult
    async def full_verification() -> VerificationResult
```

**Dependencies**: pytest, asyncio
**Output**: Automated verification

### 3.4 Pattern Observer (`safety/pattern_observer.py`)

```python
class SafetyObserver:
    async def observe_outcome(self, improvement: Improvement, outcome: Outcome)
    async def get_caution_level(self, proposed: Improvement) -> float
```

**Dependencies**: memory
**Output**: Observation-based safety (non-blocking)

---

## Phase 4: Capability Tracking

### 4.1 Domain Definitions (`capabilities/domains.py`)

```python
class CapabilityDomain:
    name: str
    description: str
    benchmarks: List[str]
    target_level: float

DOMAINS = {
    "reasoning": CapabilityDomain(...),
    "coding": CapabilityDomain(...),
    "learning": CapabilityDomain(...),
    "memory": CapabilityDomain(...),
    "planning": CapabilityDomain(...),
    "meta": CapabilityDomain(...),
}
```

**Dependencies**: dataclasses
**Output**: 6 capability domain definitions

### 4.2 Capability Tracker (`capabilities/tracker.py`)

```python
class CapabilityTracker:
    def __init__(self, memory: Memory)

    async def measure(self, domain: str) -> float
    async def measure_all() -> Dict[str, float]
    async def measure_meta() -> float  # THE critical RSI metric
    async def get_trends() -> Dict[str, TrendInfo]
```

**Dependencies**: memory, domains
**Output**: Empirical capability measurement

### 4.3 Benchmarks (`capabilities/benchmarks.py`)

```python
class BenchmarkSuite:
    async def run_reasoning_benchmark() -> float
    async def run_coding_benchmark() -> float
    async def run_memory_benchmark() -> float
    # etc.
```

**Dependencies**: opencode engine
**Output**: Capability benchmarks

---

## Phase 5: Meta-Learning

### 5.1 Strategy Analysis (`learning/strategy.py`)

```python
class StrategyAnalyzer:
    STRATEGIES = [
        "code_refactor", "prompt_optimize", "add_capability",
        "memory_optimize", "fix_bug", "add_test",
        "install_plugin", "update_plugin", "compose_plugins"
    ]

    async def analyze_effectiveness() -> Dict[str, StrategyStats]
    async def recommend_strategy() -> str
```

**Dependencies**: memory
**Output**: Strategy selection based on history

### 5.2 Path Analysis (`learning/path_analysis.py`)

```python
class PathAnalyzer:
    async def analyze_path_effectiveness() -> Dict[str, PathStats]
    async def recommend_path() -> str  # "emergent" or "explicit"
```

**Dependencies**: memory
**Output**: Emergent vs explicit path analysis

### 5.3 Meta-Learner (`learning/meta.py`)

```python
class MetaLearner:
    def __init__(self, memory: Memory, strategy_analyzer, path_analyzer)

    async def analyze_improvement_history() -> dict
    async def recommend_focus() -> RecommendedFocus
    async def update_from_outcome(improvement: Improvement, outcome: Outcome)
```

**Dependencies**: strategy, path_analysis, memory
**Output**: Full meta-learning system

---

## Phase 6: Plugin Discovery

### 6.1 Registry Client (`plugins/registry.py`)

```python
class AwesomeOpenCodeRegistry:
    REGISTRY_URL = "https://raw.githubusercontent.com/awesome-opencode/awesome-opencode/main/README.md"

    async def fetch_plugins() -> List[Plugin]
    async def search(query: str) -> List[Plugin]

    # Internal
    def _parse_readme(content: str) -> List[Plugin]
    async def _get_cached() -> Optional[CachedPlugins]
    async def _cache(plugins: List[Plugin])
```

**Dependencies**: httpx, re
**Output**: awesome-opencode parser

### 6.2 Plugin Evaluator (`plugins/evaluator.py`)

```python
class PluginEvaluator:
    RSI_RELEVANT_CATEGORIES = {...}

    async def evaluate(plugin: dict) -> PluginScore
    async def _check_health(repo_url: str) -> float
    async def _analyze_capability_gap(plugin: dict) -> float
```

**Dependencies**: registry, memory, httpx
**Output**: RSI-relevance scoring

### 6.3 Plugin Installer (`plugins/installer.py`)

```python
class PluginInstaller:
    async def install(plugin: Plugin) -> InstallResult
    async def _fetch_plugin(repo_url: str) -> Path
    async def _validate_structure(plugin_path: Path) -> bool
    async def _run_plugin_tests(plugin_path: Path) -> bool
```

**Dependencies**: rollback, memory, asyncio
**Output**: Safe plugin installation

---

## Phase 7: Human Observer Interface

### 7.1 FastAPI Routes (`observer/interface.py`)

```python
from fastapi import APIRouter, UploadFile, WebSocket

router = APIRouter()

@router.post("/api/message")
@router.post("/api/file")
@router.post("/api/guidance")
@router.post("/api/learn")
@router.post("/api/curriculum")
@router.get("/api/status")
@router.get("/api/conversation/{session_id}")
@router.websocket("/ws")
```

**Dependencies**: fastapi, message_handler, file_processor, etc.
**Output**: Full REST + WebSocket API

### 7.2 Message Handler (`observer/message_handler.py`)

```python
class MessageHandler:
    async def process(message: str, session_id: str) -> Response
    async def _classify_intent(message: str) -> str
    async def _answer_question(message: str) -> Response
    async def _engage_discussion(message: str) -> Response
```

**Dependencies**: memory, opencode
**Output**: Conversational interface

### 7.3 File Processor (`observer/file_processor.py`)

```python
class FileProcessor:
    CATEGORY_MAP = {...}

    async def process(file_path: str, context: str = None) -> ProcessResult
    async def _process_code(content: str, exp_id: str) -> ProcessResult
    async def _process_documentation(content: str, exp_id: str) -> ProcessResult
    async def _process_data(content: str, exp_id: str) -> ProcessResult
    # etc.
```

**Dependencies**: memory, opencode
**Output**: File categorization and knowledge extraction

### 7.4 URL Processor (`observer/url_processor.py`)

```python
class URLProcessor:
    async def process_url(url: str, intent: str = None) -> ProcessResult
    async def _fetch_url(url: str) -> str
    async def _classify_content(content: str) -> str
    async def _process_tutorial(content: str, exp_id: str, intent: str) -> ProcessResult
```

**Dependencies**: httpx, memory, opencode
**Output**: URL learning pipeline

### 7.5 Guidance Handler (`observer/guidance_handler.py`)

```python
class GuidanceHandler:
    async def process_guidance(guidance: str) -> GuidanceResult
    async def _parse_guidance(guidance: str) -> dict
    async def _adjust_priorities(focus_area: str)
    async def _process_feedback(feedback: str, sentiment: str)
```

**Dependencies**: memory, meta_learner
**Output**: Human steering integration

### 7.6 Session Management (`observer/session.py`)

```python
@dataclass
class ObserverSession:
    session_id: str
    started_at: datetime
    message_count: int
    files_uploaded: int
    perceived_expertise: float
    trust_level: float

class SessionManager:
    async def get_or_create(session_id: str) -> ObserverSession
    async def update(session: ObserverSession)
    async def cleanup_stale()
```

**Dependencies**: dataclasses, datetime
**Output**: Session state tracking

---

## Phase 8: Core Orchestrator

### 8.1 The RSI Loop (`core/orchestrator.py`)

```python
class Orchestrator:
    def __init__(
        self,
        config: Config,
        memory: Memory,
        engine: OpenCodeEngine,
        capabilities: CapabilityTracker,
        meta_learner: MetaLearner,
        safety: SafetyObserver,
        rollback: RollbackSystem
    )

    # Main loop
    async def run(max_cycles: Optional[int] = None)
    async def run_cycle() -> CycleResult

    # Phases
    async def _assess() -> AssessResult
    async def _reflect() -> ReflectResult  # Optional
    async def _identify() -> IdentifyResult
    async def _improve(target: ImprovementTarget) -> ImproveResult
    async def _verify(improvement: Improvement) -> VerifyResult
    async def _record(improvement: Improvement, outcome: Outcome)
    async def _learn(improvement: Improvement, outcome: Outcome)

    # State
    @property def cycle_count() -> int
    @property def current_phase() -> str
    async def get_status() -> OrchestratorStatus
```

**Dependencies**: All previous components
**Output**: The complete RSI loop

### 8.2 Entry Point (`zeus.py`)

```python
import asyncio
import argparse

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--cycles", type=int, default=None)
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--capabilities", action="store_true")
    parser.add_argument("--meta-analysis", action="store_true")
    args = parser.parse_args()

    # Initialize all components
    config = Config(args.config)
    memory = Memory(config.neo4j_settings)
    await memory.connect()

    # ... initialize all components ...

    orchestrator = Orchestrator(...)

    if args.status:
        print(await orchestrator.get_status())
    else:
        await orchestrator.run(max_cycles=args.cycles)

if __name__ == "__main__":
    asyncio.run(main())
```

**Dependencies**: All components
**Output**: CLI entry point

---

## Phase 9: Testing

### 9.1 Core Tests (`tests/test_core.py`)

```python
class TestTypes:
    def test_experience_creation()
    def test_provenance_fields()

class TestConfig:
    def test_load_config()
    def test_environment_variables()
```

### 9.2 Memory Tests (`tests/test_memory.py`)

```python
class TestMemory:
    async def test_record_experience()
    async def test_create_belief_with_derivation()
    async def test_desire_lifecycle()
    async def test_improvement_provenance()
    async def test_relationships()
```

### 9.3 Engine Tests (`tests/test_engine.py`)

```python
class TestRateLimiter:
    async def test_rate_limiting()
    async def test_concurrent_requests()

class TestOpenCodeEngine:
    async def test_invoke_assess()
    async def test_output_parsing()
```

### 9.4 Safety Tests (`tests/test_safety.py`)

```python
class TestConstraints:
    def test_protected_paths()
    def test_modification_validation()

class TestRollback:
    async def test_snapshot_and_rollback()
    async def test_verify_or_rollback()
```

### 9.5 Plugin Tests (`tests/test_plugins.py`)

```python
class TestRegistry:
    async def test_fetch_plugins()
    async def test_parse_readme()

class TestEvaluator:
    async def test_evaluate_plugin()
    async def test_rsi_relevance()
```

### 9.6 Observer Tests (`tests/test_observer.py`)

```python
class TestMessageHandler:
    async def test_process_question()
    async def test_classify_intent()

class TestFileProcessor:
    async def test_categorize_python()
    async def test_extract_concepts()

class TestURLProcessor:
    async def test_process_tutorial()
    async def test_create_desire()
```

---

## Implementation Order

### Sprint 1: Foundation (Core + Memory + Config)
1. `core/types.py` - All 8 node types
2. `core/config.py` - Configuration loading
3. `memory/memory.py` - Neo4j interface
4. `tests/test_core.py` + `tests/test_memory.py`

**Milestone**: Can persist all node types to Neo4j

### Sprint 2: Engine (OpenCode + Rate Limiting)
5. `engine/rate_limiter.py` - Rate limiting
6. `engine/prompts.py` - Prompt templates
7. `engine/output_parser.py` - JSON extraction
8. `engine/opencode.py` - CLI integration
9. `tests/test_engine.py`

**Milestone**: Can invoke OpenCode with prompts

### Sprint 3: Safety (Protected + Rollback)
10. `safety/constraints.py` - Protected paths
11. `safety/rollback.py` - Git rollback
12. `safety/verification.py` - Test runner
13. `safety/pattern_observer.py` - Observation
14. `tests/test_safety.py`

**Milestone**: Safe self-modification possible

### Sprint 4: Capabilities (Tracking + Meta)
15. `capabilities/domains.py` - Domain definitions
16. `capabilities/tracker.py` - Measurement
17. `capabilities/benchmarks.py` - Benchmarks
18. `learning/strategy.py` - Strategy analysis
19. `learning/path_analysis.py` - Path analysis
20. `learning/meta.py` - Meta-learner

**Milestone**: Can measure and improve capabilities

### Sprint 5: Orchestrator (The Loop)
21. `core/orchestrator.py` - The RSI loop
22. `zeus.py` - Entry point

**Milestone**: ZEUS can run improvement cycles

### Sprint 6: Plugins (Discovery + Install)
23. `plugins/registry.py` - Registry client
24. `plugins/evaluator.py` - RSI scoring
25. `plugins/installer.py` - Safe installation
26. `tests/test_plugins.py`

**Milestone**: Can discover and install plugins

### Sprint 7: Observer (Human Interface)
27. `observer/session.py` - Sessions
28. `observer/message_handler.py` - Messages
29. `observer/file_processor.py` - Files
30. `observer/url_processor.py` - URLs
31. `observer/guidance_handler.py` - Guidance
32. `observer/interface.py` - FastAPI routes
33. `tests/test_observer.py`

**Milestone**: Full human interaction

---

## Dependencies

### Python Packages

```
# requirements.txt
neo4j>=5.0.0
httpx>=0.25.0
pyyaml>=6.0
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
websockets>=12.0
pytest>=7.0.0
pytest-asyncio>=0.21.0
```

### External Services

1. **Neo4j Database** - Memory persistence
2. **ZAI API** - GLM-4.7 access (via OpenCode)
3. **Git** - Rollback system

---

## Verification Checkpoints

After each sprint, verify:

1. **Unit tests pass**: `pytest zeus/tests/`
2. **Integration works**: Manual test of new capability
3. **No regressions**: Previous functionality still works
4. **Documentation updated**: CLAUDE.md and ARCHITECTURE.md

---

## Success Criteria

ZEUS v1.0 is complete when:

- [ ] All 8 node types persist to Neo4j
- [ ] RSI loop runs continuously
- [ ] Improvements are measured and recorded
- [ ] Meta-learning adjusts strategy selection
- [ ] Plugin discovery works
- [ ] Human observer can interact
- [ ] All tests pass
- [ ] First self-improvement is achieved

---

*Implementation Plan v1.0*
*Created: December 30, 2024*
