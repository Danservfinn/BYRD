# HuggingFace Spaces Dockerfile for BYRD
# Deploy at: https://huggingface.co/spaces

FROM python:3.11-slim

# Install minimal dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user (HuggingFace requirement)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Install dependencies first (better caching)
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Clear any Python cache from previous builds
RUN find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Cache bust (updated on each deploy) - increment to force rebuild
ARG CACHEBUST=45

# Copy application code
COPY --chown=user . .

# HuggingFace uses port 7860
ENV PORT=7860
EXPOSE 7860

# Environment variables are set via HuggingFace Secrets
# Required: NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, ZAI_API_KEY
# Optional: ELEVENLABS_API_KEY (for voice), ANTHROPIC_API_KEY (for Actor)

# Start server
CMD ["python", "server.py"]
