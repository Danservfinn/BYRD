# BYRD Free Cloud Deployment Guide

Deploy BYRD online for free using free-tier cloud services.

## Live Instance

**BYRD is currently deployed at:**
- **Space**: https://huggingface.co/spaces/omoplatapus/byrd
- **Visualization**: https://omoplatapus-byrd.hf.space/byrd-3d-visualization.html
- **API**: https://omoplatapus-byrd.hf.space/api/status
- **Neo4j Aura**: neo4j+s://9b21f7a8.databases.neo4j.io

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     FREE TIER SERVICES                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐ │
│  │  Neo4j Aura  │     │  HuggingFace │     │   Z.AI API   │ │
│  │    Free      │◄───►│    Spaces    │◄───►│  (or Groq)   │ │
│  │              │     │              │     │              │ │
│  │ Graph DB     │     │ Docker Host  │     │ LLM Provider │ │
│  │ 200k nodes   │     │ Unlimited    │     │              │ │
│  │ 400k rels    │     │ Free tier    │     │              │ │
│  └──────────────┘     └──────────────┘     └──────────────┘ │
│                              │                               │
│                              ▼                               │
│                       ┌──────────────┐                       │
│                       │ Public URL   │                       │
│                       │ *.hf.space   │                       │
│                       └──────────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

## Free Tier Limits

| Service | Free Tier | BYRD Usage |
|---------|-----------|------------|
| Neo4j Aura | 200k nodes, 400k relationships | Memory graph |
| HuggingFace Spaces | Unlimited Docker containers | Python server |
| Z.AI | ~1M tokens/day free | Dreamer + Seeker |
| Groq | 6k tokens/min (backup) | Alternative LLM |

## Quick Deploy (Recommended)

### Step 1: Neo4j Aura Free (Database)

1. Go to [Neo4j Aura](https://neo4j.com/cloud/aura-free/)
2. Create a free account
3. Create a new **Free** instance
4. Save your credentials:
   - Connection URI: `neo4j+s://xxxxx.databases.neo4j.io`
   - Username: `neo4j`
   - Password: (generated)

### Step 2: Z.AI API Key (LLM)

1. Go to [Z.AI/BigModel](https://open.bigmodel.cn/)
2. Create account and get API key
3. Free tier includes generous token allowance

**Alternative: Groq (Free)**
1. Go to [Groq Cloud](https://console.groq.com/)
2. Get free API key

### Step 3: HuggingFace Spaces Deployment

#### Option A: Automated Script (Recommended)

```bash
# Get HuggingFace token from: https://huggingface.co/settings/tokens
export HF_TOKEN="hf_your_token_here"

# Run deployment script
python deploy_huggingface.py
```

The script will:
1. Create a new Space on HuggingFace
2. Upload all necessary files
3. Configure the Docker container

#### Option B: Manual Deployment

1. Go to [HuggingFace Spaces](https://huggingface.co/spaces)
2. Create new Space → Docker SDK
3. Upload files from this repository
4. Use `Dockerfile.huggingface` as the Dockerfile

### Step 4: Configure Secrets

In your HuggingFace Space settings, add these secrets:

| Secret Name | Value |
|-------------|-------|
| `NEO4J_URI` | `neo4j+s://xxxxx.databases.neo4j.io` |
| `NEO4J_USER` | `neo4j` |
| `NEO4J_PASSWORD` | Your Neo4j password |
| `ZAI_API_KEY` | Your Z.AI API key |
| `CLOUD_DEPLOYMENT` | `true` |

Or use the API:
```python
from huggingface_hub import HfApi
api = HfApi(token="hf_your_token")
api.add_space_secret(repo_id="username/byrd-ai", key="NEO4J_URI", value="...")
```

### Step 5: Verify Deployment

```bash
# Check status
curl https://username-byrd-ai.hf.space/api/status

# Start BYRD
curl -X POST https://username-byrd-ai.hf.space/api/start

# Awaken (if fresh database)
curl -X POST https://username-byrd-ai.hf.space/api/awaken
```

## Files for Deployment

| File | Purpose |
|------|---------|
| `Dockerfile.huggingface` | HuggingFace-specific Dockerfile (port 7860) |
| `Dockerfile` | Generic Dockerfile (port 8000, for Koyeb/Render) |
| `deploy_huggingface.py` | Automated deployment script |

## Alternative Platforms

### Koyeb

```bash
# Install CLI
brew install koyeb/tap/koyeb

# Deploy
koyeb deploy github.com/username/BYRD \
  --name byrd \
  --instance-type nano \
  --port 8000 \
  --env NEO4J_URI="..." \
  --env ZAI_API_KEY="..."
```

### Render

1. Connect GitHub repo
2. Select Docker environment
3. Set environment variables
4. Deploy

### Platform Comparison

| Platform | Free Tier | WebSocket | Idle Timeout |
|----------|-----------|-----------|--------------|
| **HuggingFace** | Unlimited | ✅ | 48h sleep |
| Koyeb | 2 nano instances | ✅ | None |
| Render | 750 hrs/month | ✅ | 15 min |
| Railway | $5 credit/month | ✅ | None |
| Fly.io | 3 shared VMs | ✅ | None (needs CC) |

## Cost Summary

| Component | Monthly Cost |
|-----------|-------------|
| Neo4j Aura Free | $0 |
| HuggingFace Spaces | $0 |
| Z.AI Free Tier | $0 |
| **Total** | **$0** |

## Monitoring

Access BYRD endpoints:
- Status: `/api/status`
- Start: `POST /api/start`
- Stop: `POST /api/stop`
- Awaken: `POST /api/awaken`
- Events: `/ws/events` (WebSocket)
- Visualization: `/byrd-3d-visualization.html`

## Troubleshooting

**Connection refused to Neo4j**
- Ensure using `neo4j+s://` (not `bolt://`) for Aura
- Check credentials in secrets/environment variables
- On macOS, SSL certificates may need `certifi` package

**Space fails to start**
- Check build logs in HuggingFace Space page
- Ensure all Python files are uploaded
- Verify secrets are configured

**LLM timeouts**
- Z.AI can be slow; increase timeout in config
- Consider Groq for faster responses

**Neo4j Aura pauses**
- Free tier pauses after 3 days of inactivity
- BYRD's keep-alive ping should prevent this
- Set `CLOUD_DEPLOYMENT=true` to enable ping

## Local Development

For local development with cloud Neo4j:

```bash
# Create .env file
cp .env.example .env

# Edit with your credentials
NEO4J_URI=neo4j+s://xxxxx.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password
ZAI_API_KEY=your-key

# Start server
python server.py
```
