---
name: byrd-websocket-errors
enabled: true
event: bash
pattern: WebSocket.*error|WebSocket.*closed|ConnectionRefusedError.*8000
action: warn
---
**WebSocket Connection Error**

The BYRD visualization server may not be running.

**Fix:**
```bash
# Start the server
python server.py

# Or check if already running
lsof -i :8000
```

**If port is in use:**
```bash
# Find and kill existing process
kill $(lsof -t -i :8000)
python server.py
```
