# BYRD Free Cloud Deployment Guide

Deploy BYRD online for free using free-tier cloud services.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     FREE TIER SERVICES                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐ │
│  │  Neo4j Aura  │     │    Koyeb     │     │   Z.AI API   │ │
│  │    Free      │◄───►│  Free Tier   │◄───►│  (or Groq)   │ │
│  │              │     │              │     │              │ │
│  │ Graph DB     │     │ Python App   │     │ LLM Provider │ │
│  │ 200k nodes   │     │ + WebSocket  │     │              │ │
│  │ 400k rels    │     │ + Static UI  │     │              │ │
│  └──────────────┘     └──────────────┘     └──────────────┘ │
│                              │                               │
│                              ▼                               │
│                       ┌──────────────┐                       │
│                       │ Public URL   │                       │
│                       │ byrd.koyeb.app│                       │
│                       └──────────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

## Free Tier Limits

| Service | Free Tier | BYRD Usage |
|---------|-----------|------------|
| Neo4j Aura | 200k nodes, 400k relationships | Memory graph |
| Koyeb | 2 nano instances, 512MB RAM | Python server |
| Z.AI | ~1M tokens/day free | Dreamer + Seeker |
| Groq | 6k tokens/min (backup) | Alternative LLM |

## Step 1: Neo4j Aura Free (Database)

1. Go to [Neo4j Aura](https://neo4j.com/cloud/aura-free/)
2. Create a free account
3. Create a new **Free** instance
4. Save your credentials:
   - Connection URI: `neo4j+s://xxxxx.databases.neo4j.io`
   - Username: `neo4j`
   - Password: (generated)

**Note**: Neo4j Aura Free pauses after 3 days of inactivity. BYRD's keep-alive ping prevents this.

## Step 2: Z.AI API Key (LLM)

1. Go to [Z.AI/BigModel](https://open.bigmodel.cn/)
2. Create account and get API key
3. Free tier includes generous token allowance
4. Model: `glm-4-flash` (fast) or `glm-4` (better)

**Alternative: Groq (Free)**
1. Go to [Groq Cloud](https://console.groq.com/)
2. Get free API key
3. Models: `llama-3.3-70b-versatile` or `mixtral-8x7b-32768`

## Step 3: Koyeb Deployment (Server)

### Option A: Deploy from GitHub (Recommended)

1. Go to [Koyeb](https://www.koyeb.com/)
2. Sign up (free tier: 2 nano instances)
3. Create new App → Deploy from GitHub
4. Connect your GitHub repo: `your-username/BYRD`
5. Configure:
   - **Builder**: Dockerfile
   - **Port**: 8000
   - **Instance**: Nano (free)

### Option B: Deploy with Koyeb CLI

```bash
# Install Koyeb CLI
curl -fsSL https://raw.githubusercontent.com/koyeb/koyeb-cli/main/install.sh | sh

# Login
koyeb login

# Deploy
koyeb deploy github.com/your-username/BYRD \
  --name byrd \
  --instance-type nano \
  --port 8000 \
  --env NEO4J_URI="neo4j+s://xxxxx.databases.neo4j.io" \
  --env NEO4J_USER="neo4j" \
  --env NEO4J_PASSWORD="your-password" \
  --env ZAI_API_KEY="your-zai-key" \
  --env CLOUD_DEPLOYMENT="true"
```

## Step 4: Environment Variables

Set these in Koyeb dashboard (Settings → Environment Variables):

```
NEO4J_URI=neo4j+s://xxxxx.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-neo4j-password
ZAI_API_KEY=your-zai-api-key
CLOUD_DEPLOYMENT=true
PORT=8000
```

## Step 5: Create Dockerfile

Create this in your repo root:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run server
CMD ["python", "server.py"]
```

## Step 6: Verify Deployment

1. Access your Koyeb URL: `https://byrd-your-username.koyeb.app`
2. Check visualization: `https://byrd-your-username.koyeb.app/byrd-3d-visualization.html`
3. Verify API: `https://byrd-your-username.koyeb.app/api/status`

## Configuration for Cloud

Update `config.yaml` for cloud operation:

```yaml
# Memory - uses environment variables
memory:
  neo4j_uri: "${NEO4J_URI}"
  neo4j_user: "${NEO4J_USER}"
  neo4j_password: "${NEO4J_PASSWORD}"

# LLM Provider
local_llm:
  provider: "zai"  # or "groq"
  model: "glm-4-flash"

# Dreamer - optimized for cloud
dreamer:
  interval_seconds: 120  # Slower to conserve tokens
  context_window: 30

# Seeker - disabled for minimal deployment
seeker:
  research:
    enabled: false  # SearXNG not available in free tier
```

## SearXNG Options

SearXNG requires self-hosting. Options for cloud:

1. **Disable research** (simplest): Set `seeker.research.enabled: false`
2. **Use public instance** (unreliable): `https://searx.be` or similar
3. **Self-host on Koyeb** (uses 2nd free instance): Deploy SearXNG container

## Monitoring

Access BYRD endpoints:
- Status: `/api/status`
- Events: `/api/events` (WebSocket)
- Visualization: `/byrd-3d-visualization.html`

## Cost Summary

| Component | Monthly Cost |
|-----------|-------------|
| Neo4j Aura Free | $0 |
| Koyeb Nano | $0 |
| Z.AI Free Tier | $0 |
| **Total** | **$0** |

## Limitations

- Neo4j Aura pauses after 3 days idle (keep-alive ping prevents this)
- Koyeb free tier: 512MB RAM, shared CPU
- No SearXNG (research disabled unless self-hosted)
- Z.AI token limits (sufficient for 60s dream intervals)

## Alternative Platforms

| Platform | Free Tier | Notes |
|----------|-----------|-------|
| Koyeb | 2 nano instances | Best for BYRD (WebSocket support) |
| Render | 750 hrs/month | Spins down after 15 min idle |
| Railway | $5 credit/month | Good but limited |
| Fly.io | 3 shared VMs | Requires credit card |

## Troubleshooting

**Connection refused to Neo4j**
- Ensure using `neo4j+s://` (not `bolt://`) for Aura
- Check credentials in environment variables

**WebSocket disconnects**
- Koyeb has 60s idle timeout; keep-alive ping handles this
- Ensure `CLOUD_DEPLOYMENT=true` is set

**LLM timeouts**
- Z.AI can be slow; increase timeout in config
- Consider Groq for faster responses

## Next Steps

1. Set up Neo4j Aura Free account
2. Get Z.AI API key
3. Fork/push BYRD to GitHub
4. Deploy on Koyeb
5. Configure environment variables
6. Awaken BYRD: `POST /api/awaken`
