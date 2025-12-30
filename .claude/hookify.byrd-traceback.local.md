---
name: byrd-traceback
enabled: true
event: bash
pattern: Traceback \(most recent call last\):|^\w+Error:|^\w+Exception:
action: warn
---

**Python Exception in BYRD**

An error occurred. Before fixing:

1. **Read the full traceback** - The last line shows the actual error
2. **Check the file and line number** - Usually in `File "...", line X`
3. **Look for BYRD-specific issues:**
   - `types.py` shadowing (delete if exists)
   - Missing async/await
   - Neo4j connection issues
   - LLM API rate limits

Use systematic debugging:
```
/systematic-debugging
```
