---
name: byrd-import-errors
enabled: true
event: bash
pattern: ImportError:|ModuleNotFoundError:|circular import|cannot import name
action: warn
---

**Import Error Detected in BYRD**

Common causes:
1. **`types.py` shadowing** - Check if a `types.py` file exists (shadows Python's built-in)
2. **Missing dependency** - Run `pip install -r requirements.txt`
3. **Circular import** - Check import order in the affected modules

Quick fix:
```bash
# Check for shadowing types.py
ls -la types.py 2>/dev/null && echo "DELETE THIS FILE - it shadows Python's types module"

# Reinstall dependencies
pip install -r requirements.txt
```
