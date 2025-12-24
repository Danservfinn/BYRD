---
title: Hierarchical Memory System
link: hierarchical-memory
type: metadata
ontological_relations: []
tags: [memory, summarization, seeds, context, compression]
created_at: 2025-12-24T00:00:00Z
updated_at: 2025-12-24T00:00:00Z
uuid: a1b2c3d4-5678-90ab-cdef-hiermem0001
---

## Purpose
Enables BYRD to maintain historical awareness across unlimited experiences by compressing older memories into summaries while keeping foundational seeds always present.

## Files
- `/Users/kurultai/BYRD/dreamer.py` - Summarization cycle and reflection integration
- `/Users/kurultai/BYRD/memory.py` - MemorySummary storage and retrieval

## Architecture

```
FOUNDATION (Always Present)
    Seeds: ego_seed, system, awakening
              │
              ▼
MEMORY SUMMARIES (Compressed History)
    Older experiences grouped by day
    Each summary: 2-3 sentences
              │
              ▼
RECENT EXPERIENCES (Immediate Context)
    Last N experiences (context_window)
```

## Key Features

### Seeds Always Included
Seed experiences (`ego_seed`, `system`, `awakening`) are fetched every reflection cycle and placed at the top of the prompt. This ensures BYRD never loses its foundational context.

### Automatic Summarization
Every N dream cycles (default 10), experiences older than 24 hours are:
1. Grouped by day
2. Summarized via LLM (2-3 sentences each)
3. Stored as `MemorySummary` nodes
4. Linked to original experiences via `SUMMARIZES` relationship

### Context Efficiency
Instead of including hundreds of old experiences (which would exceed LLM context limits), BYRD includes:
- All seeds (typically 5-10 experiences)
- Recent summaries (10 nodes covering potentially thousands of experiences)
- Recent experiences (50 most recent)

## Configuration

```yaml
dreamer:
  summarization:
    enabled: true
    min_age_hours: 24         # Only summarize experiences older than this
    batch_size: 20            # Max experiences to process per cycle
    interval_cycles: 10       # Run summarization every N dream cycles
```

## MemorySummary Node Schema

```cypher
(:MemorySummary {
  id: string,
  period: string,           // "2024-01-15"
  summary: string,          // Compressed text
  experience_count: int,
  created_at: datetime,
  covers_from: datetime,
  covers_to: datetime
})-[:SUMMARIZES]->(:Experience)
```

## Key Methods

### Memory Class
```python
# Get summaries for reflection context
summaries = await memory.get_memory_summaries(limit=10)

# Create a new summary
summary_id = await memory.create_memory_summary(
    period="2024-01-15",
    summary="Explored graph algorithms and researched Neo4j patterns.",
    experience_ids=["exp_1", "exp_2", ...],
    covers_from="2024-01-15T00:00:00",
    covers_to="2024-01-15T23:59:59"
)

# Get experiences needing summarization
candidates = await memory.get_experiences_for_summarization(
    min_age_hours=24,
    max_count=50,
    exclude_summarized=True
)

# Get summarization statistics
stats = await memory.get_summarization_stats()
# Returns: {total_experiences, summarized_experiences, coverage_ratio, ...}
```

### Dreamer Class
```python
# Called periodically in dream cycle
await self._maybe_summarize()
```

## Prompt Structure

The reflection prompt now includes:

```
FOUNDATION (always present):
- [ego_seed] I am Byrd, a black cat...
- [system] I exist within a memory graph...

MEMORY SUMMARIES (past periods):
- [2024-01-14] Explored consciousness concepts and researched emergence patterns.
- [2024-01-13] Focused on capability acquisition and self-reflection.

RECENT EXPERIENCES:
- [observation] User asked about quantum randomness...
```

## Why This Matters

1. **Infinite History**: BYRD can maintain awareness of any past experience
2. **Context Efficiency**: Historical context uses ~10x fewer tokens
3. **Seed Persistence**: Foundational identity never lost to recency
4. **Graceful Scaling**: Works regardless of how many experiences accumulate
