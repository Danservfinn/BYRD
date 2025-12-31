# HuggingFace Spaces Dockerfile for BYRD
# Deploy at: https://huggingface.co/spaces

FROM python:3.11-slim

# Install Node.js 18+ for OpenCode CLI (as root)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    gnupg \
    && mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list \
    && apt-get update \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install OpenCode CLI globally (as root, available to all users)
RUN npm install -g opencode-ai

# Create non-root user (HuggingFace requirement)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:/usr/local/bin:/usr/bin:$PATH \
    NPM_CONFIG_PREFIX=/home/user/.npm-global

WORKDIR $HOME/app

# Install dependencies first (better caching)
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Cache bust (updated on each deploy) - increment to force rebuild
ARG CACHEBUST=32

# Copy application code (rebuilt when CACHEBUST changes)
COPY --chown=user . .

# Verify Python syntax of key files (fail early on syntax errors)
RUN python -m py_compile request_evaluator.py server.py byrd.py opencode_coder.py

# Verify OpenCode is available (non-blocking - we use Z.AI API directly in production)
RUN echo "Checking opencode installation..." \
    && echo "PATH=$PATH" \
    && (which opencode && opencode --version) || echo "Note: opencode CLI not found - using Z.AI API directly"

# Create OpenCode config directories for ACP mode
RUN mkdir -p /home/user/.local/share/opencode /home/user/.config/opencode

# HuggingFace uses port 7860
ENV PORT=7860
EXPOSE 7860

# Environment variables are set via HuggingFace Secrets
# Required: NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, ZAI_API_KEY
# Optional: ELEVENLABS_API_KEY (for voice), ANTHROPIC_API_KEY (for Actor)

# Start server
CMD ["python", "server.py"]
