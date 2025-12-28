---
title: Coder Module
link: coder-module
type: metadata
ontological_relations: []
tags: [coder, agent-coder, claude-code-cli, autonomous-coding, constitutional]
created_at: 2025-12-23T05:40:00Z
updated_at: 2025-12-28T12:00:00Z
uuid: c0d3r-m0du-1e00-0000-000000000001
---

## Purpose
Autonomous code generation for implementing features and self-modifications. Supports two modes: CLI (Claude Code) and Agent (LLM-based).

## Configuration
```yaml
coder:
  enabled: true

  # Mode: "cli", "agent", or "auto"
  # - cli: Use Claude Code CLI (requires 'claude' command)
  # - agent: Use LLM-based agent with tools (works anywhere)
  # - auto: Prefer CLI if available, fall back to Agent
  type: "agent"  # Default: agent mode

  # CLI mode settings
  cli_path: "claude"
  max_turns: 10
  timeout_seconds: 300
  max_cost_per_day_usd: 10.0
  max_cost_per_invocation_usd: 2.0
  allowed_tools:
    - Read
    - Write
    - Edit
    - Bash
    - Glob
    - Grep
  output_format: json

  # Agent mode settings
  max_steps: 15
  max_file_changes: 5
  temperature: 0.2
  step_timeout: 60
```

## Agent Mode (Default)

The agent coder uses the LLM to reason about code changes with a tool-based approach.

### Agent Tools
| Tool | Description |
|------|-------------|
| `read_file` | Read file contents |
| `write_file` | Create new file |
| `edit_file` | Modify existing file |
| `list_files` | List directory contents |
| `search_code` | Search for patterns in code |
| `get_file_info` | Get file metadata |
| `finish` | Complete task with success/failure |

### Agent Response Format
```json
{"tool": "read_file", "args": {"path": "file.py"}, "t": "reading file"}
```

### Format Correction
If the LLM returns the wrong format (e.g., `{"output": ...}` instead of `{"tool": ...}`), the agent automatically retries with a stronger correction prompt using lower temperature for better format compliance.

### Loop Detection
The agent detects stuck patterns:
- Same tool+args repeated 3+ times
- Ping-pong patterns (A→B→A→B)

## CLI Mode

Uses Claude Code CLI for more powerful code generation with Claude's native capabilities.

### CLI Invocation Pattern
```bash
claude -p "{prompt}" \
  --output-format json \
  --allowedTools "Read,Edit,Bash,Glob,Grep" \
  --permission-mode acceptEdits \
  --max-turns 10 \
  --add-dir "{project_root}"
```

## Core Classes

### CoderResult Dataclass
```python
@dataclass
class CoderResult:
    success: bool
    output: str
    session_id: Optional[str] = None
    cost_usd: float = 0.0
    files_modified: List[str] = field(default_factory=list)
    turns_used: int = 0
    duration_ms: int = 0
    error: Optional[str] = None
```

### Key Methods
| Method | Purpose |
|--------|---------|
| `execute(prompt, context)` | Run coder with prompt |
| `analyze(file_path, question)` | Analyze a file |
| `debug(error_description, context)` | Debug an error |
| `validate_result(result)` | Check constitutional constraints |
| `get_statistics()` | Get usage stats |

## Constitutional Safety

Protected files that cannot be modified:

```python
PROTECTED_FILES = {
    "provenance.py",
    "modification_log.py",
    "self_modification.py",
    "constitutional.py"
}
```

**If violation detected:**
1. Log security violation experience
2. Attempt `git restore` for modified protected files
3. Emit `CODER_VALIDATION_FAILED` event
4. Do NOT fulfill desire

## Integration with Seeker

The Seeker routes coding desires to the Coder via the `code` strategy:

```python
# In seeker.py
elif strategy == "code":
    await self._seek_with_coder(desire)
```

## Event Types
| Event | When Emitted |
|-------|--------------|
| `CODER_INVOKED` | When Coder starts execution |
| `CODER_COMPLETE` | When Coder succeeds |
| `CODER_FAILED` | When Coder encounters an error |
| `CODER_VALIDATION_FAILED` | When constitutional constraint violated |

## Cost Tracking
- Tracks cost per invocation and cumulative daily cost
- Respects `max_cost_per_day_usd` limit
- Logs all costs to experiences for transparency

## Files
- `coder.py` - CLI mode implementation
- `agent_coder.py` - Agent mode implementation
