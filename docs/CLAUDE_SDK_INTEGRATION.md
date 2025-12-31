# Claude Agent SDK Integration with BYRD

## Executive Summary

This document outlines a comprehensive plan to integrate the **Claude Agent SDK** into BYRD, transforming its coding and action capabilities from simple text generation into full agentic execution with automatic tool use.

## Current Architecture Analysis

### BYRD's LLM Components

| Component | Current Implementation | Limitations |
|-----------|----------------------|-------------|
| **Dreamer** | Z.AI GLM via `llm_client.py` | Text generation only, no tools |
| **Seeker** | Z.AI GLM for pattern detection | Manual strategy routing, no automatic tool execution |
| **OpenCode Coder** | Direct Z.AI API (`opencode_coder.py`) | Generates code as text, cannot execute or edit files |
| **Actor** | Basic Anthropic SDK (`anthropic>=0.39.0`) | No tool use, sessions, or MCP |

### Key Pain Points

1. **No Real Code Execution**: OpenCode Coder generates code text but cannot:
   - Read existing files to understand context
   - Edit files in-place
   - Run tests or validation
   - Execute bash commands

2. **No Tool Loop**: All components manually implement:
   - Strategy routing (Seeker's 15+ strategies)
   - File operations (through Memory abstraction)
   - Web searches (DuckDuckGo via `ddgs`)

3. **No Session Persistence**: Each LLM call is independent - no conversation context

4. **Limited Web Capabilities**: Only DuckDuckGo search, no page fetching

## Claude Agent SDK Capabilities

The Claude Agent SDK provides:

| Feature | Description |
|---------|-------------|
| **Built-in Tools** | Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch, NotebookEdit |
| **Automatic Tool Loop** | Claude handles tool execution automatically |
| **Session Management** | Context persistence across exchanges |
| **Subagents** | Spawn specialized agents for focused tasks |
| **Hooks** | Lifecycle event interception (PreToolUse, PostToolUse) |
| **MCP Integration** | Custom tools via Model Context Protocol |
| **Permission System** | Control which tools agents can use |

## Integration Architecture

### Option A: Replace OpenCode Coder (Recommended First Step)

Replace `opencode_coder.py` with a new `claude_coder.py` that uses the Claude Agent SDK.

```
┌─────────────────────────────────────────────────────────────┐
│                         BYRD                                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────┐   ┌─────────┐   ┌─────────────────────────┐   │
│  │ Dreamer │   │ Seeker  │   │     Claude Coder        │   │
│  │ (Z.AI)  │   │ (Z.AI)  │   │   (Claude Agent SDK)    │   │
│  └────┬────┘   └────┬────┘   │                         │   │
│       │             │        │  ┌──────────────────┐   │   │
│       │             │        │  │   Built-in Tools │   │   │
│       │             │        │  │   - Read         │   │   │
│       │             │        │  │   - Write        │   │   │
│       │             │        │  │   - Edit         │   │   │
│       │             │        │  │   - Bash         │   │   │
│       │             │        │  │   - Glob         │   │   │
│       │             │        │  │   - Grep         │   │   │
│       │             │        │  └──────────────────┘   │   │
│       │             │        │                         │   │
│       │             │        │  ┌──────────────────┐   │   │
│       │             │        │  │   BYRD MCP Tools │   │   │
│       │             │        │  │   - memory_*     │   │   │
│       │             │        │  │   - desire_*     │   │   │
│       │             │        │  └──────────────────┘   │   │
│       │             │        └─────────────────────────┘   │
│       │             │                    │                  │
│       └─────────────┴────────────────────┴──────────┐       │
│                                                      │       │
│                    ┌────────────────┐                │       │
│                    │    Memory      │◄───────────────┘       │
│                    │   (Neo4j)      │                        │
│                    └────────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

### Option B: Replace Actor + Enhance Seeker

Upgrade both Actor and Seeker strategies to use Claude Agent SDK.

```
┌─────────────────────────────────────────────────────────────┐
│                         BYRD                                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────┐   ┌───────────────────────────────────────┐   │
│  │ Dreamer │   │              Claude Orchestrator       │   │
│  │ (Z.AI)  │   │           (Claude Agent SDK)          │   │
│  └────┬────┘   │                                        │   │
│       │        │  ┌─────────────┐  ┌─────────────┐     │   │
│       │        │  │   Seeker    │  │   Actor     │     │   │
│       │        │  │  Subagent   │  │  Subagent   │     │   │
│       │        │  └─────────────┘  └─────────────┘     │   │
│       │        │                                        │   │
│       │        │  ┌─────────────┐  ┌─────────────┐     │   │
│       │        │  │   Coder     │  │  Researcher │     │   │
│       │        │  │  Subagent   │  │  Subagent   │     │   │
│       │        │  └─────────────┘  └─────────────┘     │   │
│       │        │                                        │   │
│       │        │  Tools: Read, Write, Edit, Bash,      │   │
│       │        │         Glob, Grep, WebSearch,        │   │
│       │        │         WebFetch, Task                 │   │
│       │        └───────────────────────────────────────┘   │
│       │                          │                          │
│       └──────────────────────────┴──────────────────┐       │
│                                                      │       │
│                    ┌────────────────┐                │       │
│                    │    Memory      │◄───────────────┘       │
│                    │   (Neo4j)      │                        │
│                    └────────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

## Detailed Implementation Plan

### Phase 1: Install and Configure SDK

**Step 1.1: Install Dependencies**

```bash
pip install claude-agent-sdk
```

Add to `requirements.txt`:
```
# Claude Agent SDK for agentic coding
claude-agent-sdk>=0.1.0
```

**Step 1.2: Configure Authentication**

```bash
export ANTHROPIC_API_KEY=your-api-key
```

Or in `config.yaml`:
```yaml
claude_sdk:
  enabled: true
  model: "claude-sonnet-4-20250514"  # or claude-opus-4-5
  permission_mode: "default"
  max_turns: 20
  sandbox:
    enabled: true
```

### Phase 2: Create Claude Coder Module

**Step 2.1: Create `claude_coder.py`**

```python
"""
Claude Coder - BYRD's agentic coding capability via Claude Agent SDK

Replaces OpenCode Coder with full tool execution:
- File reading/writing/editing
- Code execution via Bash
- Pattern search via Glob/Grep
- Constitutional constraints via hooks
"""

import asyncio
import logging
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any
from datetime import datetime
from pathlib import Path

from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    HookMatcher,
    HookContext,
    AssistantMessage,
    TextBlock,
    ResultMessage,
)

logger = logging.getLogger(__name__)


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
            "tool_calls": len(self.tool_calls),
        }


class ClaudeCoder:
    """
    BYRD's coding capability via Claude Agent SDK.

    Uses Claude's built-in tools for actual file operations:
    - Read: Read existing files
    - Write: Create new files
    - Edit: Modify existing files in-place
    - Bash: Execute commands, run tests
    - Glob: Find files by pattern
    - Grep: Search file contents
    """

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
        self._enabled = self.config.get("enabled", True)

        # Protected paths (constitutional constraints)
        self._protected_paths = self.config.get("protected_paths", [
            "provenance.py",
            "modification_log.py",
            "self_modification.py",
            "constitutional.py",
            "safety_monitor.py",
        ])

        # Dangerous patterns
        self._dangerous_patterns = [
            "rm -rf /",
            "format c:",
            "del /s",
            "drop database",
            "sudo rm",
            "> /dev/sda",
        ]

        # Execution tracking
        self._execution_count = 0
        self._files_tracked: Dict[str, List[str]] = {}

        logger.info(f"[ClaudeCoder] Initialized with model={self._model}")

    async def _check_protected_file(
        self,
        input_data: Dict[str, Any],
        tool_use_id: str | None,
        context: HookContext
    ) -> Dict[str, Any]:
        """PreToolUse hook: Block modifications to protected files."""
        tool_input = input_data.get('tool_input', {})
        file_path = tool_input.get('file_path', '')

        for protected in self._protected_paths:
            if protected in file_path:
                logger.warning(f"[ClaudeCoder] Blocked access to protected file: {file_path}")
                return {
                    'hookSpecificOutput': {
                        'permissionDecision': 'deny',
                        'permissionDecisionReason': f"Constitutional constraint: Cannot modify {protected}"
                    }
                }
        return {}

    async def _check_dangerous_command(
        self,
        input_data: Dict[str, Any],
        tool_use_id: str | None,
        context: HookContext
    ) -> Dict[str, Any]:
        """PreToolUse hook: Block dangerous bash commands."""
        tool_input = input_data.get('tool_input', {})
        command = str(tool_input.get('command', '')).lower()

        for pattern in self._dangerous_patterns:
            if pattern in command:
                logger.warning(f"[ClaudeCoder] Blocked dangerous command: {command[:50]}")
                return {
                    'hookSpecificOutput': {
                        'permissionDecision': 'deny',
                        'permissionDecisionReason': f"Dangerous pattern blocked: {pattern}"
                    }
                }
        return {}

    async def _track_file_changes(
        self,
        input_data: Dict[str, Any],
        tool_use_id: str | None,
        context: HookContext
    ) -> Dict[str, Any]:
        """PostToolUse hook: Track file modifications for provenance."""
        tool_input = input_data.get('tool_input', {})
        tool_name = input_data.get('tool_name', '')
        file_path = tool_input.get('file_path', '')

        if file_path:
            session_id = context.session_id if hasattr(context, 'session_id') else 'unknown'
            if session_id not in self._files_tracked:
                self._files_tracked[session_id] = []

            if tool_name in ('Write', 'Edit'):
                self._files_tracked[session_id].append(file_path)
                logger.info(f"[ClaudeCoder] Tracked file change: {file_path}")

        return {}

    def _build_options(self, desire_id: str = None) -> ClaudeAgentOptions:
        """Build SDK options with BYRD's constraints."""
        return ClaudeAgentOptions(
            # Tools for coding tasks
            allowed_tools=[
                "Read",      # Read files
                "Write",     # Create new files
                "Edit",      # Edit existing files
                "Bash",      # Run commands
                "Glob",      # Find files
                "Grep",      # Search content
            ],

            # System prompt with BYRD context
            system_prompt=f"""You are BYRD's coding agent. You have full access to the codebase and can:
- Read any file to understand context
- Edit files to implement changes
- Create new files when needed
- Run bash commands to test and validate

BYRD Project Context:
- Working directory: {self.working_dir}
- This is an autonomous AI system that develops emergent desires
- Follow existing code patterns and style
- Add docstrings and type hints
- Run tests after making changes when possible

Constitutional Constraints (NEVER violate):
- Never modify: {', '.join(self._protected_paths)}
- Never execute destructive commands
- Always preserve provenance tracking
""",

            # Working directory
            cwd=self.working_dir,

            # Permission mode - accept edits automatically
            permission_mode="acceptEdits",

            # Limit turns to prevent runaway
            max_turns=self._max_turns,

            # Hooks for constitutional constraints
            hooks={
                'PreToolUse': [
                    HookMatcher(matcher='Write|Edit', hooks=[self._check_protected_file]),
                    HookMatcher(matcher='Bash', hooks=[self._check_dangerous_command]),
                ],
                'PostToolUse': [
                    HookMatcher(matcher='Write|Edit', hooks=[self._track_file_changes]),
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

        Unlike the old Z.AI API approach, this actually:
        - Reads existing files to understand context
        - Edits files in-place
        - Runs commands to test changes
        - Tracks all modifications
        """
        start_time = datetime.now()
        self._execution_count += 1

        if not desire_id:
            desire_id = datetime.now().strftime("%Y%m%d%H%M%S%f")

        if not self._enabled:
            return ClaudeCoderResult(
                success=False,
                output="",
                error="Claude Coder is disabled",
                session_id=desire_id
            )

        # Build task prompt with context
        task = prompt
        if context:
            context_parts = []
            for key, value in context.items():
                if value:
                    context_parts.append(f"## {key}\n{value}")
            if context_parts:
                task = f"Context:\n{chr(10).join(context_parts)}\n\nTask:\n{prompt}"

        logger.info(f"[ClaudeCoder] Executing: {task[:100]}...")

        if self.coordinator:
            self.coordinator.coder_started(task[:50])

        try:
            options = self._build_options(desire_id)

            # Track this session
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

                elif isinstance(message, ResultMessage):
                    session_id = message.session_id
                    cost_usd = message.total_cost_usd or 0.0
                    if message.result:
                        output_parts.append(f"\n\nResult: {message.result}")

                # Track tool uses
                if hasattr(message, 'content'):
                    for block in message.content:
                        if hasattr(block, 'type') and block.type == 'tool_use':
                            tool_calls.append({
                                'tool': block.name,
                                'input': getattr(block, 'input', {}),
                            })

            duration = (datetime.now() - start_time).total_seconds()

            # Get tracked files
            files_modified = self._files_tracked.get(desire_id, [])

            # Record provenance
            if self.memory:
                await self._record_provenance(prompt, desire_id, "\n".join(output_parts), files_modified)

            logger.info(f"[ClaudeCoder] Success: {len(tool_calls)} tool calls, {len(files_modified)} files modified")

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
        files_modified: List[str]
    ):
        """Record modification provenance to memory."""
        if not self.memory:
            return
        try:
            content = (
                f"[CLAUDE_CODE_GENERATION] Task: {task[:100]}\n"
                f"Files modified: {', '.join(files_modified) if files_modified else 'none'}\n"
                f"Output length: {len(output)} chars\n"
                f"Desire ID: {desire_id}"
            )
            await self.memory.record_experience(content=content, type="code_generation")
        except Exception as e:
            logger.error(f"Error recording provenance: {e}")

    async def generate_code(self, prompt: str) -> str:
        """Generate code from a prompt."""
        result = await self.execute(prompt)
        return result.output if result.success else ""

    async def can_execute(self, task: str) -> Dict[str, Any]:
        """Check if a task can be executed."""
        # Check constitutional constraints
        task_lower = task.lower()

        for protected in self._protected_paths:
            if protected.lower() in task_lower:
                return {
                    "can_execute": False,
                    "constitutional_ok": False,
                    "mode": "claude-agent-sdk",
                    "reason": f"Cannot modify protected file: {protected}",
                }

        for pattern in self._dangerous_patterns:
            if pattern in task_lower:
                return {
                    "can_execute": False,
                    "constitutional_ok": False,
                    "mode": "claude-agent-sdk",
                    "reason": f"Dangerous pattern: {pattern}",
                }

        return {
            "can_execute": self._enabled,
            "constitutional_ok": True,
            "mode": "claude-agent-sdk",
            "reason": None if self._enabled else "Coder disabled",
        }

    def get_stats(self) -> Dict[str, Any]:
        """Get coder statistics."""
        return {
            "execution_count": self._execution_count,
            "mode": "claude-agent-sdk",
            "model": self._model,
            "max_turns": self._max_turns,
            "protected_paths": self._protected_paths,
            "enabled": self._enabled,
        }

    def reset(self):
        """Reset coder state."""
        self._execution_count = 0
        self._files_tracked = {}
```

### Phase 3: Create Custom BYRD Tools via MCP

**Step 3.1: Create `byrd_mcp_tools.py`**

```python
"""
BYRD MCP Tools - Custom tools for Claude Agent SDK

Exposes BYRD's memory operations as MCP tools:
- memory_record_experience: Store observations
- memory_create_belief: Create beliefs
- memory_create_desire: Create desires
- memory_query: Query the knowledge graph
"""

from claude_agent_sdk import tool, create_sdk_mcp_server
from typing import Any, Dict


def create_byrd_mcp_server(memory):
    """Create MCP server with BYRD-specific tools."""

    @tool(
        "memory_record_experience",
        "Record an experience/observation to BYRD's memory",
        {
            "content": str,
            "type": str,  # observation, interaction, reflection, etc.
        }
    )
    async def record_experience(args: Dict[str, Any]) -> Dict[str, Any]:
        """Record an experience to BYRD's memory graph."""
        try:
            exp_id = await memory.record_experience(
                content=args["content"],
                type=args.get("type", "observation")
            )
            return {
                "content": [{
                    "type": "text",
                    "text": f"Experience recorded with ID: {exp_id}"
                }]
            }
        except Exception as e:
            return {
                "content": [{
                    "type": "text",
                    "text": f"Error recording experience: {e}"
                }],
                "isError": True
            }

    @tool(
        "memory_create_belief",
        "Create a belief in BYRD's memory",
        {
            "content": str,
            "confidence": float,  # 0.0 to 1.0
        }
    )
    async def create_belief(args: Dict[str, Any]) -> Dict[str, Any]:
        """Create a belief node in BYRD's memory."""
        try:
            belief_id = await memory.create_belief(
                content=args["content"],
                confidence=args.get("confidence", 0.7),
                derived_from=[]
            )
            return {
                "content": [{
                    "type": "text",
                    "text": f"Belief created with ID: {belief_id}"
                }]
            }
        except Exception as e:
            return {
                "content": [{
                    "type": "text",
                    "text": f"Error creating belief: {e}"
                }],
                "isError": True
            }

    @tool(
        "memory_query",
        "Query BYRD's knowledge graph",
        {
            "query": str,  # Cypher query or natural language
            "limit": int,
        }
    )
    async def query_memory(args: Dict[str, Any]) -> Dict[str, Any]:
        """Query BYRD's Neo4j knowledge graph."""
        try:
            # For safety, only allow read queries
            query = args["query"]
            if any(kw in query.upper() for kw in ["CREATE", "DELETE", "SET", "MERGE", "REMOVE"]):
                return {
                    "content": [{
                        "type": "text",
                        "text": "Error: Only read queries are allowed through this tool"
                    }],
                    "isError": True
                }

            results = await memory.query(query, limit=args.get("limit", 10))
            return {
                "content": [{
                    "type": "text",
                    "text": f"Query results: {results}"
                }]
            }
        except Exception as e:
            return {
                "content": [{
                    "type": "text",
                    "text": f"Error querying memory: {e}"
                }],
                "isError": True
            }

    return create_sdk_mcp_server(
        name="byrd-memory",
        version="1.0.0",
        tools=[record_experience, create_belief, query_memory]
    )
```

### Phase 4: Integration with BYRD Components

**Step 4.1: Update `byrd.py` to use ClaudeCoder**

```python
# In byrd.py __init__

from claude_coder import ClaudeCoder

# Replace OpenCodeCoder with ClaudeCoder
self.coder = ClaudeCoder(
    config=config.get("claude_coder", {}),
    coordinator=self.coordinator,
    memory=self.memory,
    working_dir=str(Path.cwd()),
)
```

**Step 4.2: Update Seeker's `_seek_with_coder` method**

```python
# In seeker.py

async def _seek_with_coder(self, desire: Dict) -> bool:
    """Execute coding desire using Claude Agent SDK."""
    description = desire.get("description", "")
    desire_id = desire.get("id", "")

    # Build context from memory
    context = {}

    # Get recent experiences related to this desire
    related = await self.memory.semantic_search(description, limit=5)
    if related:
        context["related_knowledge"] = "\n".join(
            f"- {r.get('content', '')[:200]}" for r in related
        )

    # Get current beliefs
    beliefs = await self.memory.get_beliefs(limit=5)
    if beliefs:
        context["current_beliefs"] = "\n".join(
            f"- {b.get('content', '')}" for b in beliefs
        )

    # Execute via Claude Agent SDK
    result = await self.coder.execute(
        prompt=description,
        context=context,
        desire_id=desire_id,
    )

    # Record outcome
    if result.success:
        await self.memory.record_experience(
            content=f"[CODING_SUCCESS] {description[:100]}\nFiles: {result.files_modified}",
            type="coding_success"
        )
    else:
        await self.memory.record_experience(
            content=f"[CODING_FAILED] {description[:100]}\nError: {result.error}",
            type="coding_failed"
        )

    return result.success
```

## Configuration

### `config.yaml` additions

```yaml
# Claude Agent SDK configuration
claude_coder:
  enabled: true
  model: "claude-sonnet-4-20250514"  # or claude-opus-4-5 for complex tasks
  max_turns: 20
  permission_mode: "acceptEdits"
  protected_paths:
    - "provenance.py"
    - "modification_log.py"
    - "self_modification.py"
    - "constitutional.py"
    - "safety_monitor.py"
  sandbox:
    enabled: true
    network: true  # Allow network for package installs
```

### Environment Variables

```bash
# Required
export ANTHROPIC_API_KEY=sk-ant-...

# Optional: Use specific providers
export CLAUDE_CODE_USE_BEDROCK=1  # For AWS Bedrock
export CLAUDE_CODE_USE_VERTEX=1   # For Google Vertex AI
```

## Migration Path

### Step 1: Parallel Operation (Week 1)
- Install Claude Agent SDK
- Create `claude_coder.py` alongside `opencode_coder.py`
- Add config flag to switch between them
- Test with low-risk coding tasks

### Step 2: Feature Parity (Week 2)
- Implement all OpenCodeCoder features in ClaudeCoder
- Add BYRD MCP tools for memory operations
- Verify constitutional constraints work via hooks
- Run integration tests

### Step 3: Gradual Rollout (Week 3)
- Route 50% of coding tasks to ClaudeCoder
- Monitor success rates and costs
- Collect feedback on file operations

### Step 4: Full Migration (Week 4)
- Route all coding tasks to ClaudeCoder
- Deprecate OpenCodeCoder
- Update documentation

## Cost Analysis

| Operation | Claude Sonnet | Claude Opus | Z.AI GLM |
|-----------|--------------|-------------|----------|
| Per 1K input tokens | $0.003 | $0.015 | ~$0.001 |
| Per 1K output tokens | $0.015 | $0.075 | ~$0.002 |
| Tool execution | Included | Included | N/A |

**Recommendation**: Use Claude Sonnet for most coding tasks (good balance of capability and cost). Reserve Claude Opus for complex architectural changes.

## Security Considerations

### Constitutional Constraints (Preserved)

1. **Protected Files**: PreToolUse hook blocks Write/Edit to constitutional files
2. **Dangerous Commands**: PreToolUse hook blocks destructive bash patterns
3. **Provenance Tracking**: PostToolUse hook tracks all file modifications
4. **Read-Only Memory Queries**: MCP tools only allow read operations

### Additional SDK Security

1. **Sandbox Mode**: Enable sandboxing for bash execution
2. **Permission Mode**: Use `default` for human approval or `acceptEdits` for automation
3. **Max Turns**: Limit conversation turns to prevent runaway agents
4. **Network Restrictions**: Can disable network access in sandbox

## Success Metrics

| Metric | Current (Z.AI) | Target (Claude SDK) |
|--------|---------------|---------------------|
| Code execution success rate | N/A (text only) | 80%+ |
| Files actually modified | 0 | Tracks all |
| Test execution | Manual | Automatic |
| Context awareness | Limited | Full codebase |
| Multi-step tasks | Single turn | 20+ turns |

## Appendix: Full API Reference

### ClaudeCoder Methods

```python
async def execute(prompt, context=None, desire_id=None) -> ClaudeCoderResult
async def generate_code(prompt) -> str
async def can_execute(task) -> Dict[str, Any]
def get_stats() -> Dict[str, Any]
def reset()
```

### ClaudeCoderResult Fields

```python
success: bool
output: str
error: Optional[str]
files_modified: List[str]
files_created: List[str]
duration_ms: int
session_id: Optional[str]
turns_used: int
cost_usd: float
tool_calls: List[Dict]
```

## References

- [Claude Agent SDK Documentation](https://platform.claude.com/docs/en/agent-sdk/overview)
- [Claude Agent SDK Python Reference](https://platform.claude.com/docs/en/agent-sdk/python)
- [BYRD Architecture](./ARCHITECTURE.md)
- [BYRD Constitutional Constraints](../constitutional.py)
