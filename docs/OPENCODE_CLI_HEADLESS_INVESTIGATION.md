# OpenCode CLI Headless Mode Investigation

## Executive Summary

**Goal**: Run OpenCode CLI (`opencode-ai` npm package) in headless Docker containers on HuggingFace Spaces for automated code generation.

**Result**: All CLI-based approaches failed. Currently using direct Z.AI API calls as a workaround.

**Environment**:
- Docker image: `python:3.11-slim` (Debian-based)
- OpenCode version: 1.0.218 (installed globally via `npm install -g opencode-ai`)
- Platform: HuggingFace Spaces (no TTY, no interactive terminal)
- Authentication: Z.AI API key stored in `~/.local/share/opencode/auth.json`

---

## Method 1: `opencode run "message"` (Direct CLI)

### Command
```bash
opencode run --model zai/glm-4.7 --format json "Write a Python hello world function"
```

### Expected Behavior
According to [OpenCode CLI docs](https://opencode.ai/docs/cli/), this should:
- Run in non-interactive mode
- Return JSON-formatted response
- Exit after completion

### Actual Behavior
- Process starts and initializes (plugins load, bus events subscribe)
- Hangs indefinitely after initialization
- Times out after 120 seconds with no output
- Exit code: timeout (killed)

### Logs Captured
```
INFO service=default version=1.0.218 args=["run",...] opencode
INFO service=default directory=/home/user/app creating instance
INFO service=project directory=/home/user/app fromDirectory
INFO service=default directory=/home/user/app bootstrapping
INFO service=config path=/home/user/.config/opencode/config.json loading
INFO service=bun cmd=[...] running
INFO service=plugin path=opencode-copilot-auth@0.0.9 loading plugin
INFO service=plugin path=opencode-anthropic-auth@0.0.5 loading plugin
INFO service=bus type=* subscribing
INFO service=bus type=session.updated subscribing
INFO service=bus type=message.updated subscribing
INFO service=bus type=message.part.updated subscribing
[HANGS HERE - no further output]
```

### Analysis
OpenCode initializes successfully but never proceeds to make the actual API call. The bus event subscriptions suggest it's waiting for something (possibly TTY input or an event that never fires in headless mode).

---

## Method 2: `opencode -p "prompt"` (Documented Flag)

### Command
```bash
opencode -p "Write a hello world function" -f json -q -m zai/glm-4.7
```

### Expected Behavior
Some documentation mentions `-p` flag for passing prompts directly.

### Actual Behavior
OpenCode displays its ASCII art logo and help menu:
```
▄
█▀▀█ █▀▀█ █▀▀█ █▀▀▄ █▀▀▀ █▀▀█ █▀▀█ █▀▀█
█░░█ █░░█ █▀▀▀ █░░█ █░░░ █░░█ █░░█ █▀▀▀
▀▀▀▀ █▀▀▀ ▀▀▀▀ ▀  ▀ ▀▀▀▀ ▀▀▀▀ ▀▀▀▀ ▀▀▀▀

Commands:
  opencode completion          generate shell completion script
  opencode acp                 start ACP (Agent Client Protocol) server
  opencode [project]           start opencode tui [default]
  ...
```

### Analysis
The `-p` flag does not exist in OpenCode CLI version 1.0.218. The correct syntax is `opencode run [message..]` as positional arguments, not flags.

---

## Method 3: Stdin Piping

### Command
```bash
echo "Write a hello world function" | opencode run --model zai/glm-4.7 --format json
```

### Expected Behavior
OpenCode reads prompt from stdin when no message provided.

### Actual Behavior
Same as Method 1 - hangs after initialization, times out after 120 seconds.

### Analysis
Piping doesn't help because the hang occurs after initialization, not during prompt reading.

---

## Method 4: `opencode serve` (HTTP Server Mode)

### Commands
```bash
# Start server
opencode serve --port 4097 --hostname 127.0.0.1

# Create session
curl -X POST http://localhost:4097/session -d '{"model": "zai/glm-4.7"}'

# Send message
curl -X POST http://localhost:4097/session/{id}/message \
  -d '{"parts": [{"type": "text", "text": "Write hello world"}]}'
```

### Expected Behavior
According to [OpenCode Server docs](https://opencode.ai/docs/server/):
- HTTP server exposes OpenAPI endpoint
- Sessions can be created and messages sent via REST API
- Designed for headless operation

### Actual Behavior
1. Server starts successfully (health check at `/global/health` returns 200)
2. Session creation succeeds (returns session ID)
3. Message sending times out after 120 seconds
4. No response received

### Server Logs
Server starts and health check works, but message processing hangs indefinitely.

### API Format Issues Encountered
Initially got HTTP 400 errors:
```json
{"error": [{"expected": "object", "code": "invalid_type", "path": ["model"]}]}
```

Fixed by removing `model` from message request (session already has model). But still times out.

### Analysis
The HTTP server mode has the same underlying issue - it initializes but doesn't process messages in headless environments.

---

## Method 5: `opencode acp` (Agent Client Protocol)

### Command
```bash
opencode acp
# Then send JSON-RPC via stdin:
{"jsonrpc": "2.0", "method": "session/initialize", "params": {}, "id": 1}
```

### Expected Behavior
ACP is designed for headless programmatic control via JSON-RPC over stdin/stdout.

### Actual Behavior
```json
{"jsonrpc": "2.0", "error": {"code": -32601, "message": "Method not found: session/initialize"}, "id": 1}
```

Also tried:
- `message.send` - Method not found
- `session/new` - Method not found
- `session/prompt` - Method not found

### Analysis
OpenCode's native `acp` command does NOT implement standard ACP protocol. The methods available are undocumented and non-standard. There are third-party ACP adapters ([cjenaro/opencode-acp](https://github.com/cjenaro/opencode-acp), [josephschmitt/opencode-acp](https://github.com/josephschmitt/opencode-acp)) that translate standard ACP to OpenCode SDK, but these require additional setup.

---

## Method 6: Environment Variables for Headless Mode

### Commands
```bash
export TERM=dumb
export CI=true
export NO_COLOR=1
opencode run --model zai/glm-4.7 --format json "Write hello world"
```

### Expected Behavior
These environment variables typically disable TTY requirements and interactive prompts in CLI tools.

### Actual Behavior
Same hang behavior - no change.

### Analysis
OpenCode's hang is not caused by TTY detection or color output. The issue is deeper in the execution flow.

---

## Method 7: Pseudo-TTY via `script` Command

### Command
```bash
script -q -c 'opencode run --model zai/glm-4.7 --format json "Write hello world"' /dev/null
```

### Expected Behavior
The `script` command provides a pseudo-TTY, which should satisfy any TTY requirements.

### Actual Behavior
Same hang behavior - times out after 120 seconds.

### Analysis
The issue is not related to TTY availability. OpenCode hangs even with a pseudo-TTY.

---

## Methods NOT Tried

### `--continue` / `--session` Flags
These flags are for continuing previous sessions. Since we can't even get a first message to work, these weren't tested.

### Third-Party ACP Adapters
- [cjenaro/opencode-acp](https://github.com/cjenaro/opencode-acp)
- [josephschmitt/opencode-acp](https://github.com/josephschmitt/opencode-acp)

These translate standard ACP protocol to OpenCode SDK calls. Would require additional npm installation and configuration.

### Running OpenCode in a Separate Container with TTY
Could potentially run OpenCode in a sidecar container with `docker run -it` and communicate via HTTP/socket.

---

## Known Issues

### GitHub Issue #953
[sst/opencode#953](https://github.com/sst/opencode/issues/953) - "headless mode" (July 2025)
- Asks about using OpenCode in scripts with MCP configurations
- No resolution as of investigation date

### GitHub Issue #2404
[sst/opencode#2404](https://github.com/sst/opencode/issues/2404) - "headless mode --resume" (September 2025)
- Asks for `--resume` support in headless mode
- Compares to Claude Code which works fine in headless mode

---

## Working Solution (Current)

Direct Z.AI API calls bypassing OpenCode CLI entirely:

```python
async with httpx.AsyncClient(timeout=120.0) as client:
    response = await client.post(
        "https://api.z.ai/api/coding/paas/v4/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "glm-4.7",
            "messages": [
                {"role": "system", "content": "You are an expert programmer..."},
                {"role": "user", "content": task},
            ],
            "temperature": 0.7,
            "max_tokens": 4096,
        },
    )
```

**Result**: Works perfectly, 4-5 second response times.

---

## Recommendations for IT Expert

1. **Investigate OpenCode Source**: The hang occurs after bus event subscription. Check `packages/opencode/src/` for what triggers message processing.

2. **Test with Explicit PTY**: Try `unbuffer` from `expect` package or `pty.spawn()` in Python.

3. **Try Third-Party ACP Adapters**: Install `@cjenaro/opencode-acp` and use standard ACP protocol.

4. **Contact OpenCode Maintainers**: The headless mode issues are known but unresolved. A GitHub issue with specific Docker reproduction steps might help.

5. **Consider Alternative Architecture**: Run OpenCode on a machine with real TTY and expose via API to headless containers.

---

## Environment Reproduction

```dockerfile
FROM python:3.11-slim

# Install Node.js and OpenCode
RUN apt-get update && apt-get install -y nodejs npm
RUN npm install -g opencode-ai

# Configure auth
RUN mkdir -p /root/.local/share/opencode
RUN echo '{"zai": {"type": "api", "key": "YOUR_KEY"}}' > /root/.local/share/opencode/auth.json

# Test command (will hang)
CMD ["opencode", "run", "--model", "zai/glm-4.7", "--format", "json", "Write hello world"]
```

---

## Conclusion

OpenCode CLI appears to require something beyond a simple headless environment. All standard approaches for running CLI tools without TTY have been exhausted. The issue is likely in OpenCode's internal event loop or initialization sequence that expects interactive input or a specific runtime environment not present in Docker containers.

**Current workaround**: Direct API calls to Z.AI, which work reliably and are actually faster than CLI overhead.
