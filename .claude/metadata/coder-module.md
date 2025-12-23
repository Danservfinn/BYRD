---
title: Coder Module
link: coder-module
type: metadata
ontological_relations: []
tags: [coder, claude-code-cli, autonomous-coding, constitutional]
created_at: 2025-12-23T05:40:00Z
updated_at: 2025-12-23T05:40:00Z
uuid: c0d3r-m0du-1e00-0000-000000000001
---

## Purpose
Autonomous code generation via Claude Code CLI. BYRD's "coding limb" for implementing features and self-modifications.

## Configuration
```yaml
coder:
  enabled: true
  cli_path: "claude"
  max_turns: 10
  timeout_seconds: 300
  max_cost_per_day_usd: 10.0
  max_cost_per_invocation_usd: 2.0
  allowed_tools:
    - Read
    - Edit
    - Bash
    - Glob
    - Grep
  output_format: json
```

## CLI Invocation Pattern
```bash
claude -p "{prompt}" \
  --output-format json \
  --allowedTools "Read,Edit,Bash,Glob,Grep" \
  --permission-mode acceptEdits \
  --max-turns 10 \
  --add-dir "{project_root}"
```

## Core Class: Coder

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
| `execute(prompt, context)` | Run Claude Code CLI with prompt |
| `analyze(file_path, question)` | Analyze a file with a question |
| `debug(error_description, context)` | Debug an error |
| `validate_result(result)` | Check constitutional constraints |
| `get_statistics()` | Get usage stats (invocations, cost, etc.) |

## Constitutional Safety

Post-validation ensures Claude Code doesn't violate protected files:

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

The Seeker routes coding and self-modification desires to the Coder:

```python
# In seeker.py _seek_cycle()
elif desire_type == "coding":
    await self._seek_with_coder(desire)
elif desire_type == "self_modification":
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
