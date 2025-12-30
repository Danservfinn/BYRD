---
name: block-types-py
enabled: true
event: file
conditions:
  - field: file_path
    operator: ends_with
    pattern: /types.py
action: block
---

**BLOCKED: Creating types.py**

Creating a file named `types.py` will **shadow Python's built-in `types` module** and break the entire import system.

This causes:
- Circular import errors
- `cannot import name 'WrapperDescriptorType'`
- BYRD's observation loop to silently fail

**Use `byrd_types.py` instead** for BYRD type definitions.
