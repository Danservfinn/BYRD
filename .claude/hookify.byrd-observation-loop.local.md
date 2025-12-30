---
name: byrd-observation-loop
enabled: true
event: bash
pattern: observation.*BROKEN|observation_loop.*failed|produces no observable data|broken transmission|transmission.*blocked|no.*observable
action: warn
---

**BYRD Observation/Transmission Issue Detected**

This indicates the core observation system isn't producing or transmitting data.

**Common causes:**
1. **Import system broken** - Check for `types.py` shadowing Python's built-in
2. **Neo4j not connected** - Observations can't be stored
3. **LLM not responding** - Check API keys and rate limits
4. **Event bus not emitting** - Check event_bus.py
5. **Transmission path blocked** - Check parallel_observation_path.py buffer

**Diagnostic steps:**
```bash
# Check for types.py shadowing
ls types.py 2>/dev/null && echo "FOUND - DELETE THIS FILE"

# Check Neo4j
docker ps | grep neo4j

# Check for buffered observations (transmission blocked)
ls parallel_observations/*.pending.json 2>/dev/null | wc -l

# Run semantic monitor
python semantic_monitor.py --check-now
```

**Full monitoring:**
```bash
# Watch for semantic issues (beliefs about broken systems)
python semantic_monitor.py --watch-beliefs --auto-fix
```
