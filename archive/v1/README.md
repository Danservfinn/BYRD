# BYRD v1 Archive

This directory contains the original BYRD codebase before the Q-DE-RSI
implementation. Archived on January 3, 2026.

## Why Archived

The v1 codebase accumulated 282 Python files over development, including
debugging scripts, one-off fixes, and experimental code. The Q-DE-RSI
architecture requires a clean implementation focused on:

1. Dispositional Emergence
2. Oracle-Constrained Practice
3. Heuristic Crystallization
4. Prompt Evolution

## What's Here

All Python files from the root directory that weren't preserved for v2.
See the implementation plan for details on what was preserved vs archived.

## Can I Use This Code?

Yes, for reference. Some patterns may be useful:
- `memory.py` patterns (preserved in core/)
- `llm_client.py` patterns (preserved in core/)
- `dreamer.py` reflection logic (reference for rsi/emergence/)
- `seeker.py` routing logic (reference for rsi/learning/)

Do NOT copy-paste. Understand and reimplement cleanly.
