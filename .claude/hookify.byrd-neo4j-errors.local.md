---
name: byrd-neo4j-errors
enabled: true
event: bash
pattern: Neo4j.*error|AuthError.*neo4j|ServiceUnavailable|neo4j\.exceptions
action: warn
---

**Neo4j Connection Error Detected**

BYRD requires Neo4j to be running. Check:

1. **Is Neo4j running?**
   ```bash
   docker ps | grep neo4j
   # If not running:
   docker-compose up -d
   ```

2. **Check credentials** in `config.yaml` or environment:
   ```bash
   echo $NEO4J_URI $NEO4J_USER $NEO4J_PASSWORD
   ```

3. **Test connection:**
   ```bash
   python -c "from neo4j import GraphDatabase; d=GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j','prometheus')); d.verify_connectivity(); print('OK')"
   ```
