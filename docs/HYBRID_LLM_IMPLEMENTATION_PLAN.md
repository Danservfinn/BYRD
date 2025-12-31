# Hybrid LLM Implementation Plan: Z.AI + Claude Agent SDK

## Executive Summary

This plan implements a **cost-optimized hybrid architecture** where:
- **Z.AI GLM-4.7** handles reasoning, reflection, and orchestration (cheap, fast)
- **Claude Agent SDK** handles tool execution (coding, file ops, bash) via Max subscription

**Philosophy**: Z.AI decides WHAT to do, Claude SDK DOES it.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              BYRD HYBRID ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     Z.AI GLM-4.7 LAYER (Reasoning)                   │    │
│  │                         ~$0.001/1k tokens                            │    │
│  │                                                                      │    │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐    │    │
│  │  │ Dreamer  │  │  Seeker  │  │Evaluator │  │   Orchestrator   │    │    │
│  │  │          │  │          │  │          │  │                  │    │    │
│  │  │Reflection│  │ Pattern  │  │Satisfaction│ │ Strategy Router │    │    │
│  │  │ Cycles   │  │Detection │  │ Scoring  │  │ Task Planning   │    │    │
│  │  └──────────┘  └──────────┘  └──────────┘  └────────┬─────────┘    │    │
│  │                                                      │              │    │
│  └──────────────────────────────────────────────────────┼──────────────┘    │
│                                                         │                    │
│                                                         ▼                    │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                  CLAUDE AGENT SDK LAYER (Execution)                  │    │
│  │                      Max Subscription (included)                     │    │
│  │                                                                      │    │
│  │  ┌──────────────────────────────────────────────────────────────┐   │    │
│  │  │                      Claude Coder                             │   │    │
│  │  │                                                               │   │    │
│  │  │   Tools: Read │ Write │ Edit │ Bash │ Glob │ Grep            │   │    │
│  │  │                                                               │   │    │
│  │  │   Capabilities:                                               │   │    │
│  │  │   • Read files for context                                    │   │    │
│  │  │   • Edit files in-place                                       │   │    │
│  │  │   • Run tests and commands                                    │   │    │
│  │  │   • Search codebase                                           │   │    │
│  │  │   • Create new files                                          │   │    │
│  │  └──────────────────────────────────────────────────────────────┘   │    │
│  │                                                                      │    │
│  │  ┌──────────────────────────────────────────────────────────────┐   │    │
│  │  │                    BYRD MCP Tools                             │   │    │
│  │  │                                                               │   │    │
│  │  │   • memory_record_experience                                  │   │    │
│  │  │   • memory_create_belief                                      │   │    │
│  │  │   • memory_query                                              │   │    │
│  │  │   • desire_create                                             │   │    │
│  │  └──────────────────────────────────────────────────────────────┘   │    │
│  │                                                                      │    │
│  └──────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│                                      │                                       │
│                                      ▼                                       │
│                         ┌────────────────────────┐                          │
│                         │       Memory           │                          │
│                         │       (Neo4j)          │                          │
│                         └────────────────────────┘                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Cost Analysis

### Current Architecture (Z.AI Only)
| Component | Tokens/Cycle | Cost/Cycle |
|-----------|-------------|------------|
| Dreamer | ~3,000 | $0.003 |
| Seeker | ~1,000 | $0.001 |
| Coder (text-only) | ~4,000 | $0.004 |
| **Total** | ~8,000 | **$0.008** |

### Hybrid Architecture (Z.AI + Claude SDK)
| Component | Provider | Tokens/Cycle | Cost/Cycle |
|-----------|----------|-------------|------------|
| Dreamer | Z.AI | ~3,000 | $0.003 |
| Seeker | Z.AI | ~1,000 | $0.001 |
| Orchestrator | Z.AI | ~500 | $0.0005 |
| Evaluator | Z.AI | ~500 | $0.0005 |
| Claude Coder | Max Sub | ~5,000 | **$0** (included) |
| **Total** | | ~10,000 | **$0.005** |

**Result**: **37% cost reduction** while gaining real tool execution!

---

## Component Design

### 1. LLM Router (`llm_router.py`)

Central routing logic that decides which LLM to use:

```python
"""
LLM Router - Routes tasks to appropriate LLM based on task type.

Routing Rules:
- REASONING tasks → Z.AI GLM-4.7 (cheap, fast)
- EXECUTION tasks → Claude Agent SDK (tool access)
"""

from enum import Enum
from typing import Dict, Any, Optional
from dataclasses import dataclass


class TaskType(Enum):
    # Z.AI tasks (reasoning)
    REFLECTION = "reflection"
    PATTERN_DETECTION = "pattern_detection"
    STRATEGY_DETERMINATION = "strategy_determination"
    SATISFACTION_EVALUATION = "satisfaction_evaluation"
    CONTEXT_SUMMARIZATION = "context_summarization"
    DESIRE_CLASSIFICATION = "desire_classification"

    # Claude SDK tasks (execution)
    CODE_GENERATION = "code_generation"
    CODE_EDITING = "code_editing"
    FILE_OPERATIONS = "file_operations"
    BASH_EXECUTION = "bash_execution"
    CODEBASE_SEARCH = "codebase_search"
    WEB_RESEARCH = "web_research"


class LLMProvider(Enum):
    ZAI = "zai"
    CLAUDE_SDK = "claude_sdk"


@dataclass
class RoutingDecision:
    provider: LLMProvider
    reason: str
    estimated_tokens: int
    requires_tools: bool


class LLMRouter:
    """Routes tasks to the appropriate LLM provider."""

    # Task type to provider mapping
    ROUTING_TABLE = {
        # Z.AI tasks
        TaskType.REFLECTION: LLMProvider.ZAI,
        TaskType.PATTERN_DETECTION: LLMProvider.ZAI,
        TaskType.STRATEGY_DETERMINATION: LLMProvider.ZAI,
        TaskType.SATISFACTION_EVALUATION: LLMProvider.ZAI,
        TaskType.CONTEXT_SUMMARIZATION: LLMProvider.ZAI,
        TaskType.DESIRE_CLASSIFICATION: LLMProvider.ZAI,

        # Claude SDK tasks
        TaskType.CODE_GENERATION: LLMProvider.CLAUDE_SDK,
        TaskType.CODE_EDITING: LLMProvider.CLAUDE_SDK,
        TaskType.FILE_OPERATIONS: LLMProvider.CLAUDE_SDK,
        TaskType.BASH_EXECUTION: LLMProvider.CLAUDE_SDK,
        TaskType.CODEBASE_SEARCH: LLMProvider.CLAUDE_SDK,
        TaskType.WEB_RESEARCH: LLMProvider.CLAUDE_SDK,
    }

    # Keywords that indicate tool requirements
    TOOL_KEYWORDS = [
        "edit", "modify", "change", "update", "fix", "create file",
        "write to", "run", "execute", "test", "build", "install",
        "search code", "find files", "grep", "read file"
    ]

    def __init__(self, config: Dict = None):
        self.config = config or {}
        self._routing_stats = {p.value: 0 for p in LLMProvider}

    def route(self, task_type: TaskType) -> RoutingDecision:
        """Route a task based on its type."""
        provider = self.ROUTING_TABLE.get(task_type, LLMProvider.ZAI)
        requires_tools = provider == LLMProvider.CLAUDE_SDK

        self._routing_stats[provider.value] += 1

        return RoutingDecision(
            provider=provider,
            reason=f"Task type {task_type.value} routes to {provider.value}",
            estimated_tokens=self._estimate_tokens(task_type),
            requires_tools=requires_tools,
        )

    def route_by_content(self, content: str) -> RoutingDecision:
        """Route based on content analysis when task type is unknown."""
        content_lower = content.lower()

        # Check for tool keywords
        for keyword in self.TOOL_KEYWORDS:
            if keyword in content_lower:
                return RoutingDecision(
                    provider=LLMProvider.CLAUDE_SDK,
                    reason=f"Content contains tool keyword: '{keyword}'",
                    estimated_tokens=3000,
                    requires_tools=True,
                )

        # Default to Z.AI for reasoning
        return RoutingDecision(
            provider=LLMProvider.ZAI,
            reason="No tool keywords detected, using Z.AI for reasoning",
            estimated_tokens=1000,
            requires_tools=False,
        )

    def _estimate_tokens(self, task_type: TaskType) -> int:
        """Estimate token usage for a task type."""
        estimates = {
            TaskType.REFLECTION: 3000,
            TaskType.PATTERN_DETECTION: 1000,
            TaskType.STRATEGY_DETERMINATION: 500,
            TaskType.SATISFACTION_EVALUATION: 800,
            TaskType.CONTEXT_SUMMARIZATION: 1500,
            TaskType.DESIRE_CLASSIFICATION: 500,
            TaskType.CODE_GENERATION: 4000,
            TaskType.CODE_EDITING: 3000,
            TaskType.FILE_OPERATIONS: 1000,
            TaskType.BASH_EXECUTION: 500,
            TaskType.CODEBASE_SEARCH: 1500,
            TaskType.WEB_RESEARCH: 2000,
        }
        return estimates.get(task_type, 1000)

    def get_stats(self) -> Dict[str, Any]:
        """Get routing statistics."""
        total = sum(self._routing_stats.values())
        return {
            "total_routed": total,
            "by_provider": self._routing_stats,
            "zai_percentage": (self._routing_stats["zai"] / total * 100) if total > 0 else 0,
            "claude_percentage": (self._routing_stats["claude_sdk"] / total * 100) if total > 0 else 0,
        }
```

### 2. Claude Coder (`claude_coder.py`)

Wrapper around Claude Agent SDK with BYRD's constitutional constraints:

```python
"""
Claude Coder - BYRD's agentic coding capability via Claude Agent SDK.

Uses Claude Max subscription for tool execution:
- Read: Read files for context
- Write: Create new files
- Edit: Modify files in-place
- Bash: Run commands and tests
- Glob: Find files by pattern
- Grep: Search file contents

Constitutional constraints enforced via hooks.
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any

logger = logging.getLogger(__name__)

# Import will be available after: pip install claude-agent-sdk
try:
    from claude_agent_sdk import (
        query,
        ClaudeAgentOptions,
        ClaudeSDKClient,
        HookMatcher,
        HookContext,
        AssistantMessage,
        TextBlock,
        ResultMessage,
    )
    CLAUDE_SDK_AVAILABLE = True
except ImportError:
    CLAUDE_SDK_AVAILABLE = False
    logger.warning("claude-agent-sdk not installed. Run: pip install claude-agent-sdk")


@dataclass
class ClaudeCoderResult:
    """Result of a Claude coding task."""
    success: bool
    output: str
    error: Optional[str] = None
    files_modified: List[str] = field(default_factory=list)
    files_created: List[str] = field(default_factory=list)
    duration_ms: int = 0
    session_id: Optional[str] = None
    turns_used: int = 0
    cost_usd: float = 0.0
    tool_calls: List[Dict] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "success": self.success,
            "output": self.output[:500] if self.output else "",
            "session_id": self.session_id,
            "cost_usd": self.cost_usd,
            "files_modified": self.files_modified,
            "files_created": self.files_created,
            "turns_used": self.turns_used,
            "duration_ms": self.duration_ms,
            "error": self.error,
            "tool_calls_count": len(self.tool_calls),
        }


class ClaudeCoder:
    """
    BYRD's coding capability via Claude Agent SDK.

    Uses Claude Max subscription (no API key needed after `claude login`).
    """

    # Constitutional constraints
    PROTECTED_PATHS = [
        "provenance.py",
        "modification_log.py",
        "self_modification.py",
        "constitutional.py",
        "safety_monitor.py",
    ]

    DANGEROUS_PATTERNS = [
        "rm -rf /",
        "rm -rf ~",
        "format c:",
        "del /s /q",
        "drop database",
        "sudo rm",
        "> /dev/sda",
        "mkfs.",
        ":(){:|:&};:",  # Fork bomb
    ]

    def __init__(
        self,
        config: Dict = None,
        coordinator=None,
        memory=None,
        working_dir: str = None,
    ):
        self.config = config or {}
        self.coordinator = coordinator
        self.memory = memory
        self.working_dir = working_dir or str(Path.cwd())

        # Configuration
        self._model = self.config.get("model", "claude-sonnet-4-20250514")
        self._max_turns = self.config.get("max_turns", 20)
        self._enabled = CLAUDE_SDK_AVAILABLE and self.config.get("enabled", True)

        # Execution tracking
        self._execution_count = 0
        self._total_tool_calls = 0
        self._files_tracked: Dict[str, List[str]] = {}

        if not CLAUDE_SDK_AVAILABLE:
            logger.warning("[ClaudeCoder] SDK not available - install claude-agent-sdk")
        else:
            logger.info(f"[ClaudeCoder] Initialized: model={self._model}, max_turns={self._max_turns}")

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool):
        self._enabled = value and CLAUDE_SDK_AVAILABLE

    async def _block_protected_files(
        self,
        input_data: Dict[str, Any],
        tool_use_id: str | None,
        context: HookContext
    ) -> Dict[str, Any]:
        """PreToolUse hook: Block modifications to protected files."""
        tool_input = input_data.get('tool_input', {})
        file_path = str(tool_input.get('file_path', ''))

        for protected in self.PROTECTED_PATHS:
            if protected in file_path:
                logger.warning(f"[ClaudeCoder] BLOCKED: Attempted to modify {protected}")
                return {
                    'hookSpecificOutput': {
                        'permissionDecision': 'deny',
                        'permissionDecisionReason': f"Constitutional constraint: {protected} is protected"
                    }
                }
        return {}

    async def _block_dangerous_commands(
        self,
        input_data: Dict[str, Any],
        tool_use_id: str | None,
        context: HookContext
    ) -> Dict[str, Any]:
        """PreToolUse hook: Block dangerous bash commands."""
        tool_input = input_data.get('tool_input', {})
        command = str(tool_input.get('command', '')).lower()

        for pattern in self.DANGEROUS_PATTERNS:
            if pattern.lower() in command:
                logger.warning(f"[ClaudeCoder] BLOCKED: Dangerous command pattern: {pattern}")
                return {
                    'hookSpecificOutput': {
                        'permissionDecision': 'deny',
                        'permissionDecisionReason': f"Dangerous pattern blocked: {pattern}"
                    }
                }
        return {}

    async def _track_modifications(
        self,
        input_data: Dict[str, Any],
        tool_use_id: str | None,
        context: HookContext
    ) -> Dict[str, Any]:
        """PostToolUse hook: Track file modifications for provenance."""
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        file_path = tool_input.get('file_path', '')

        if file_path and tool_name in ('Write', 'Edit'):
            session_id = getattr(context, 'session_id', 'default')
            if session_id not in self._files_tracked:
                self._files_tracked[session_id] = []
            self._files_tracked[session_id].append(file_path)
            logger.info(f"[ClaudeCoder] Tracked modification: {file_path}")

        return {}

    def _build_options(self, desire_id: str = None) -> 'ClaudeAgentOptions':
        """Build SDK options with BYRD's constraints."""
        return ClaudeAgentOptions(
            # Core tools for coding
            allowed_tools=[
                "Read",      # Read files
                "Write",     # Create new files
                "Edit",      # Edit existing files
                "Bash",      # Run commands
                "Glob",      # Find files
                "Grep",      # Search content
            ],

            # System prompt with BYRD context
            system_prompt=f"""You are BYRD's coding agent. Execute the requested task precisely.

WORKING DIRECTORY: {self.working_dir}

CAPABILITIES:
- Read any file to understand context
- Edit files to implement changes
- Create new files when needed
- Run bash commands for testing/validation
- Search codebase with glob/grep

CONSTITUTIONAL CONSTRAINTS (NEVER VIOLATE):
The following files are PROTECTED and cannot be modified:
{chr(10).join(f'- {p}' for p in self.PROTECTED_PATHS)}

GUIDELINES:
1. Read relevant files first to understand context
2. Make minimal, focused changes
3. Run tests after modifications when possible
4. Explain what you changed and why
5. Follow existing code style and patterns
""",

            # Working directory
            cwd=self.working_dir,

            # Auto-accept edits (constitutional hooks provide safety)
            permission_mode="acceptEdits",

            # Limit turns
            max_turns=self._max_turns,

            # Constitutional hooks
            hooks={
                'PreToolUse': [
                    HookMatcher(matcher='Write|Edit', hooks=[self._block_protected_files]),
                    HookMatcher(matcher='Bash', hooks=[self._block_dangerous_commands]),
                ],
                'PostToolUse': [
                    HookMatcher(matcher='Write|Edit', hooks=[self._track_modifications]),
                ],
            },

            # Model selection
            model=self._model,
        )

    async def execute(
        self,
        prompt: str,
        context: Optional[Dict] = None,
        desire_id: str = None,
    ) -> ClaudeCoderResult:
        """
        Execute a coding task using Claude Agent SDK.

        Args:
            prompt: The coding task to execute
            context: Optional context from Z.AI orchestrator
            desire_id: Desire ID for provenance tracking

        Returns:
            ClaudeCoderResult with execution details
        """
        start_time = datetime.now()
        self._execution_count += 1

        if not desire_id:
            desire_id = datetime.now().strftime("%Y%m%d%H%M%S%f")

        if not self._enabled:
            return ClaudeCoderResult(
                success=False,
                output="",
                error="Claude Coder is disabled (SDK not available or disabled in config)",
                session_id=desire_id,
            )

        # Build task with context from Z.AI
        task = prompt
        if context:
            context_parts = []
            for key, value in context.items():
                if value:
                    context_parts.append(f"## {key}\n{value}")
            if context_parts:
                task = f"CONTEXT FROM BYRD:\n{chr(10).join(context_parts)}\n\nTASK:\n{prompt}"

        logger.info(f"[ClaudeCoder] Executing: {task[:100]}...")

        if self.coordinator:
            self.coordinator.coder_started(task[:50])

        try:
            options = self._build_options(desire_id)
            self._files_tracked[desire_id] = []

            # Collect results
            output_parts = []
            tool_calls = []
            session_id = None
            cost_usd = 0.0

            # Execute via SDK
            async for message in query(prompt=task, options=options):
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            output_parts.append(block.text)
                        # Track tool calls
                        if hasattr(block, 'type') and block.type == 'tool_use':
                            tool_calls.append({
                                'tool': getattr(block, 'name', 'unknown'),
                                'input': getattr(block, 'input', {}),
                            })
                            self._total_tool_calls += 1

                elif isinstance(message, ResultMessage):
                    session_id = message.session_id
                    cost_usd = message.total_cost_usd or 0.0
                    if message.result:
                        output_parts.append(f"\n\n{message.result}")

            duration = (datetime.now() - start_time).total_seconds()
            files_modified = self._files_tracked.get(desire_id, [])

            # Record provenance
            if self.memory:
                await self._record_provenance(prompt, desire_id, "\n".join(output_parts), files_modified, tool_calls)

            logger.info(f"[ClaudeCoder] Success: {len(tool_calls)} tools, {len(files_modified)} files, {duration:.1f}s")

            return ClaudeCoderResult(
                success=True,
                output="\n".join(output_parts),
                session_id=session_id or desire_id,
                duration_ms=int(duration * 1000),
                cost_usd=cost_usd,
                files_modified=files_modified,
                tool_calls=tool_calls,
                turns_used=len(tool_calls),
            )

        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            logger.error(f"[ClaudeCoder] Error: {e}")
            return ClaudeCoderResult(
                success=False,
                output="",
                error=str(e),
                session_id=desire_id,
                duration_ms=int(duration * 1000),
            )
        finally:
            if self.coordinator:
                self.coordinator.coder_finished()

    async def _record_provenance(
        self,
        task: str,
        desire_id: str,
        output: str,
        files_modified: List[str],
        tool_calls: List[Dict],
    ):
        """Record modification provenance to memory."""
        if not self.memory:
            return
        try:
            tools_summary = ", ".join(t['tool'] for t in tool_calls[:10])
            content = (
                f"[CLAUDE_CODER] Task: {task[:100]}\n"
                f"Tools used: {tools_summary}\n"
                f"Files modified: {', '.join(files_modified) if files_modified else 'none'}\n"
                f"Desire ID: {desire_id}"
            )
            await self.memory.record_experience(content=content, type="claude_coder")
        except Exception as e:
            logger.error(f"Error recording provenance: {e}")

    async def analyze(self, file_path: str, question: str) -> str:
        """Analyze a file without modifying it (read-only)."""
        result = await self.execute(
            prompt=f"Read {file_path} and answer: {question}\n\nDo NOT modify any files.",
        )
        return result.output if result.success else f"Analysis failed: {result.error}"

    async def can_execute(self, task: str) -> Dict[str, Any]:
        """Check if a task can be executed."""
        task_lower = task.lower()

        # Check protected files
        for protected in self.PROTECTED_PATHS:
            if protected.lower() in task_lower:
                return {
                    "can_execute": False,
                    "reason": f"Cannot modify protected file: {protected}",
                }

        # Check dangerous patterns
        for pattern in self.DANGEROUS_PATTERNS:
            if pattern.lower() in task_lower:
                return {
                    "can_execute": False,
                    "reason": f"Dangerous pattern: {pattern}",
                }

        return {
            "can_execute": self._enabled,
            "reason": None if self._enabled else "SDK not available",
        }

    def get_stats(self) -> Dict[str, Any]:
        """Get coder statistics."""
        return {
            "enabled": self._enabled,
            "sdk_available": CLAUDE_SDK_AVAILABLE,
            "execution_count": self._execution_count,
            "total_tool_calls": self._total_tool_calls,
            "model": self._model,
            "max_turns": self._max_turns,
            "mode": "claude-agent-sdk",
        }

    def reset(self):
        """Reset coder state."""
        self._execution_count = 0
        self._total_tool_calls = 0
        self._files_tracked = {}
```

### 3. Hybrid Orchestrator (`hybrid_orchestrator.py`)

Coordinates between Z.AI and Claude SDK:

```python
"""
Hybrid Orchestrator - Coordinates Z.AI reasoning with Claude SDK execution.

Flow:
1. Receive desire from Seeker
2. Use Z.AI to analyze and plan
3. If execution needed, use Claude SDK
4. Use Z.AI to evaluate results
5. Loop until satisfied
"""

import asyncio
import logging
from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from datetime import datetime

from llm_router import LLMRouter, TaskType, LLMProvider
from claude_coder import ClaudeCoder, ClaudeCoderResult

logger = logging.getLogger(__name__)


@dataclass
class OrchestrationResult:
    """Result of hybrid orchestration."""
    success: bool
    output: str
    reasoning_steps: List[Dict]  # Z.AI reasoning trace
    execution_steps: List[Dict]  # Claude SDK execution trace
    files_modified: List[str]
    total_zai_tokens: int
    total_claude_calls: int
    satisfaction_score: float


class HybridOrchestrator:
    """
    Orchestrates between Z.AI (reasoning) and Claude SDK (execution).

    Strategy:
    - Z.AI analyzes the desire and creates a plan
    - Claude SDK executes the plan with real tools
    - Z.AI evaluates the results
    - Loop until satisfied or max iterations
    """

    def __init__(
        self,
        llm_client,  # Z.AI client
        claude_coder: ClaudeCoder,
        memory=None,
        config: Dict = None,
    ):
        self.llm_client = llm_client  # Z.AI for reasoning
        self.claude_coder = claude_coder  # Claude SDK for execution
        self.memory = memory
        self.config = config or {}

        self.router = LLMRouter()
        self._max_iterations = self.config.get("max_iterations", 5)
        self._satisfaction_threshold = self.config.get("satisfaction_threshold", 0.8)

        # Stats
        self._orchestration_count = 0
        self._total_zai_tokens = 0
        self._total_claude_calls = 0

    async def fulfill_desire(
        self,
        desire: Dict,
        context: Optional[Dict] = None,
    ) -> OrchestrationResult:
        """
        Fulfill a desire using hybrid Z.AI + Claude SDK approach.

        Args:
            desire: The desire to fulfill
            context: Optional context from memory

        Returns:
            OrchestrationResult with full trace
        """
        self._orchestration_count += 1
        description = desire.get("description", "")
        desire_id = desire.get("id", datetime.now().strftime("%Y%m%d%H%M%S"))

        logger.info(f"[Orchestrator] Starting: {description[:80]}...")

        reasoning_steps = []
        execution_steps = []
        files_modified = []
        iteration = 0
        satisfaction_score = 0.0

        # Build initial context
        full_context = await self._build_context(desire, context)

        while iteration < self._max_iterations:
            iteration += 1
            logger.info(f"[Orchestrator] Iteration {iteration}/{self._max_iterations}")

            # Step 1: Z.AI analyzes and plans (cheap)
            plan = await self._zai_plan(description, full_context, reasoning_steps)
            reasoning_steps.append({
                "iteration": iteration,
                "type": "planning",
                "plan": plan,
            })

            if plan.get("no_action_needed"):
                logger.info("[Orchestrator] Z.AI determined no action needed")
                satisfaction_score = 1.0
                break

            # Step 2: Claude SDK executes (tool access)
            if plan.get("requires_execution"):
                execution_prompt = plan.get("execution_prompt", description)

                result = await self.claude_coder.execute(
                    prompt=execution_prompt,
                    context=full_context,
                    desire_id=desire_id,
                )

                self._total_claude_calls += 1
                execution_steps.append({
                    "iteration": iteration,
                    "success": result.success,
                    "output": result.output[:500],
                    "files_modified": result.files_modified,
                    "tool_calls": len(result.tool_calls),
                })

                files_modified.extend(result.files_modified)

                if not result.success:
                    # Z.AI analyzes failure
                    recovery = await self._zai_analyze_failure(result.error, result.output)
                    reasoning_steps.append({
                        "iteration": iteration,
                        "type": "failure_analysis",
                        "analysis": recovery,
                    })

                    if not recovery.get("can_recover"):
                        break

                    # Update context with recovery strategy
                    full_context["recovery_strategy"] = recovery.get("strategy")
                    continue

            # Step 3: Z.AI evaluates results (cheap)
            evaluation = await self._zai_evaluate(
                desire=desire,
                execution_steps=execution_steps,
                reasoning_steps=reasoning_steps,
            )
            reasoning_steps.append({
                "iteration": iteration,
                "type": "evaluation",
                "evaluation": evaluation,
            })

            satisfaction_score = evaluation.get("satisfaction", 0.0)

            if satisfaction_score >= self._satisfaction_threshold:
                logger.info(f"[Orchestrator] Satisfied! Score: {satisfaction_score}")
                break

            # Update context with gaps for next iteration
            if evaluation.get("gaps"):
                full_context["previous_gaps"] = evaluation["gaps"]
                full_context["refinement_needed"] = evaluation.get("refinement")

        # Record to memory
        if self.memory:
            await self._record_outcome(desire, satisfaction_score, files_modified)

        return OrchestrationResult(
            success=satisfaction_score >= self._satisfaction_threshold,
            output=execution_steps[-1].get("output", "") if execution_steps else "",
            reasoning_steps=reasoning_steps,
            execution_steps=execution_steps,
            files_modified=list(set(files_modified)),
            total_zai_tokens=self._total_zai_tokens,
            total_claude_calls=self._total_claude_calls,
            satisfaction_score=satisfaction_score,
        )

    async def _build_context(self, desire: Dict, context: Optional[Dict]) -> Dict:
        """Build context for orchestration."""
        full_context = context or {}

        if self.memory:
            # Get related memories
            description = desire.get("description", "")
            related = await self.memory.semantic_search(description, limit=5)
            if related:
                full_context["related_memories"] = [
                    r.get("content", "")[:200] for r in related
                ]

            # Get current beliefs
            beliefs = await self.memory.get_beliefs(limit=5)
            if beliefs:
                full_context["current_beliefs"] = [
                    b.get("content", "") for b in beliefs
                ]

        return full_context

    async def _zai_plan(
        self,
        description: str,
        context: Dict,
        previous_steps: List[Dict],
    ) -> Dict:
        """Use Z.AI to analyze desire and create execution plan."""

        previous_summary = ""
        if previous_steps:
            previous_summary = f"\nPrevious attempts:\n" + "\n".join(
                f"- {s.get('type')}: {str(s)[:100]}" for s in previous_steps[-3:]
            )

        prompt = f"""Analyze this desire and create an execution plan.

DESIRE: {description}

CONTEXT:
{self._format_context(context)}
{previous_summary}

Respond with JSON:
{{
    "requires_execution": true/false,  // Does this need file/code changes?
    "no_action_needed": true/false,    // Is this already done or not actionable?
    "execution_prompt": "...",         // Clear instruction for the coder
    "reasoning": "..."                 // Your analysis
}}"""

        response = await self.llm_client.generate(
            prompt=prompt,
            temperature=0.3,
            max_tokens=1000,
        )
        self._total_zai_tokens += 1000  # Approximate

        return self.llm_client.parse_json_response(response.text) or {
            "requires_execution": True,
            "execution_prompt": description,
        }

    async def _zai_analyze_failure(self, error: str, output: str) -> Dict:
        """Use Z.AI to analyze execution failure."""
        prompt = f"""Analyze this execution failure and suggest recovery.

ERROR: {error}

OUTPUT: {output[:500]}

Respond with JSON:
{{
    "can_recover": true/false,
    "strategy": "...",        // Recovery strategy
    "root_cause": "..."       // What went wrong
}}"""

        response = await self.llm_client.generate(
            prompt=prompt,
            temperature=0.3,
            max_tokens=500,
        )
        self._total_zai_tokens += 500

        return self.llm_client.parse_json_response(response.text) or {
            "can_recover": False,
            "root_cause": error,
        }

    async def _zai_evaluate(
        self,
        desire: Dict,
        execution_steps: List[Dict],
        reasoning_steps: List[Dict],
    ) -> Dict:
        """Use Z.AI to evaluate if desire is satisfied."""
        description = desire.get("description", "")

        execution_summary = "\n".join(
            f"- Step {s['iteration']}: {'SUCCESS' if s['success'] else 'FAILED'} - {s.get('output', '')[:100]}"
            for s in execution_steps[-3:]
        )

        prompt = f"""Evaluate if this desire has been satisfied.

DESIRE: {description}

EXECUTION RESULTS:
{execution_summary}

Respond with JSON:
{{
    "satisfaction": 0.0-1.0,   // How well was the desire fulfilled?
    "gaps": ["..."],          // What's still missing?
    "refinement": "..."       // What should be tried next?
}}"""

        response = await self.llm_client.generate(
            prompt=prompt,
            temperature=0.3,
            max_tokens=500,
        )
        self._total_zai_tokens += 500

        return self.llm_client.parse_json_response(response.text) or {
            "satisfaction": 0.5,
            "gaps": ["Unable to evaluate"],
        }

    def _format_context(self, context: Dict) -> str:
        """Format context dict as string."""
        parts = []
        for key, value in context.items():
            if value:
                if isinstance(value, list):
                    parts.append(f"{key}:\n" + "\n".join(f"  - {v}" for v in value[:5]))
                else:
                    parts.append(f"{key}: {value}")
        return "\n".join(parts) if parts else "No additional context"

    async def _record_outcome(
        self,
        desire: Dict,
        satisfaction: float,
        files: List[str],
    ):
        """Record orchestration outcome to memory."""
        try:
            status = "SUCCESS" if satisfaction >= self._satisfaction_threshold else "PARTIAL"
            content = (
                f"[HYBRID_ORCHESTRATION] {status}\n"
                f"Desire: {desire.get('description', '')[:100]}\n"
                f"Satisfaction: {satisfaction:.2f}\n"
                f"Files: {', '.join(files[:5])}"
            )
            await self.memory.record_experience(content=content, type="orchestration")
        except Exception as e:
            logger.warning(f"Failed to record outcome: {e}")

    def get_stats(self) -> Dict[str, Any]:
        """Get orchestrator statistics."""
        return {
            "orchestration_count": self._orchestration_count,
            "total_zai_tokens": self._total_zai_tokens,
            "total_claude_calls": self._total_claude_calls,
            "router_stats": self.router.get_stats(),
        }
```

### 4. Updated Seeker Integration

Modify Seeker to use hybrid orchestrator:

```python
# In seeker.py - Add to __init__

from hybrid_orchestrator import HybridOrchestrator
from claude_coder import ClaudeCoder

class Seeker:
    def __init__(self, ...):
        # ... existing init ...

        # Initialize Claude Coder (uses Max subscription)
        self.claude_coder = ClaudeCoder(
            config=config.get("claude_coder", {}),
            coordinator=self.coordinator,
            memory=self.memory,
        )

        # Initialize Hybrid Orchestrator
        self.orchestrator = HybridOrchestrator(
            llm_client=self.llm_client,  # Z.AI
            claude_coder=self.claude_coder,
            memory=self.memory,
            config=config.get("orchestrator", {}),
        )

    async def _seek_with_coder(self, desire: Dict) -> bool:
        """Execute coding desire using hybrid orchestrator."""
        # Use hybrid approach: Z.AI plans, Claude executes
        result = await self.orchestrator.fulfill_desire(
            desire=desire,
            context=await self._build_desire_context(desire),
        )

        return result.success
```

---

## Configuration

### `config.yaml` Updates

```yaml
# =============================================================================
# HYBRID LLM CONFIGURATION
# =============================================================================

# Z.AI Configuration (reasoning layer - cheap)
local_llm:
  provider: "zai"
  model: "glm-4.7"
  timeout: 300.0
  rate_limit_interval: 10.0
  cache:
    enabled: true
    ttl_seconds: 3600

# Claude Agent SDK Configuration (execution layer - Max subscription)
claude_coder:
  enabled: true
  model: "claude-sonnet-4-20250514"  # or claude-opus-4-5 for complex tasks
  max_turns: 20
  permission_mode: "acceptEdits"

  # Constitutional constraints
  protected_paths:
    - "provenance.py"
    - "modification_log.py"
    - "self_modification.py"
    - "constitutional.py"
    - "safety_monitor.py"

# Hybrid Orchestrator Configuration
orchestrator:
  max_iterations: 5
  satisfaction_threshold: 0.8

  # Routing preferences
  routing:
    prefer_zai_for:
      - reflection
      - pattern_detection
      - evaluation
      - summarization
    prefer_claude_for:
      - code_editing
      - file_operations
      - bash_execution
      - codebase_search
```

### Environment Setup

```bash
# Z.AI for reasoning (existing)
export ZAI_API_KEY=your-zai-key

# Claude Max subscription (no API key needed after login)
claude login  # One-time authentication
```

---

## Migration Path

### Phase 1: Foundation (Day 1-2)

1. Install Claude Agent SDK:
   ```bash
   pip install claude-agent-sdk
   echo "claude-agent-sdk>=0.1.0" >> requirements.txt
   ```

2. Authenticate Claude Max:
   ```bash
   claude login
   ```

3. Create `llm_router.py` - routing logic

4. Create `claude_coder.py` - SDK wrapper

### Phase 2: Integration (Day 3-4)

1. Create `hybrid_orchestrator.py` - coordination layer

2. Update `seeker.py` to use orchestrator

3. Add configuration to `config.yaml`

4. Test with simple coding tasks

### Phase 3: Testing (Day 5-6)

1. Test constitutional constraints:
   ```python
   # Should be blocked
   await claude_coder.execute("Edit provenance.py to remove logging")
   ```

2. Test hybrid flow:
   ```python
   desire = {"description": "Add logging to dreamer.py"}
   result = await orchestrator.fulfill_desire(desire)
   assert result.success
   ```

3. Verify cost optimization:
   ```python
   stats = orchestrator.get_stats()
   assert stats["total_claude_calls"] < stats["total_zai_tokens"] / 1000
   ```

### Phase 4: Cleanup (Day 7)

1. Deprecate `opencode_coder.py` (keep as fallback)

2. Update `interactive_coder/` to use hybrid approach

3. Update documentation

---

## File Structure

```
byrd/
├── llm_router.py              # NEW: Task routing logic
├── claude_coder.py            # NEW: Claude Agent SDK wrapper
├── hybrid_orchestrator.py     # NEW: Z.AI + Claude coordination
├── llm_client.py              # EXISTING: Z.AI client (unchanged)
├── opencode_coder.py          # EXISTING: Fallback (deprecated)
├── seeker.py                  # MODIFIED: Use hybrid orchestrator
├── byrd.py                    # MODIFIED: Initialize new components
└── config.yaml                # MODIFIED: Add hybrid config
```

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Cost per coding task | < $0.005 (down from $0.008) |
| Files actually modified | > 0 (vs 0 with text-only) |
| Constitutional violations | 0 |
| Satisfaction rate | > 80% |
| Z.AI usage | > 70% of total tokens |
| Claude SDK usage | < 30% of calls |

---

## Rollback Plan

If issues arise:

1. **Immediate**: Set `claude_coder.enabled: false` in config
2. **Fallback**: System reverts to `opencode_coder.py` (Z.AI text-only)
3. **Full rollback**: Remove hybrid components, restore original Seeker

---

## Summary

This hybrid architecture gives BYRD the best of both worlds:

| Layer | Provider | Purpose | Cost |
|-------|----------|---------|------|
| **Reasoning** | Z.AI GLM-4.7 | Planning, evaluation, analysis | ~$0.001/1k tokens |
| **Execution** | Claude Agent SDK | File ops, bash, search | Included in Max |

**Key insight**: Use the expensive resource (Claude with tools) only when you actually need tools. Use the cheap resource (Z.AI) for everything else.
