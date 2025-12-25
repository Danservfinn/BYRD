# HuggingFace Spaces Dockerfile for BYRD
# Deploy at: https://huggingface.co/spaces

FROM python:3.11-slim

# Create non-root user (HuggingFace requirement)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Install dependencies first (better caching)
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Cache bust (updated on each deploy)
ARG CACHEBUST=1

# Copy application code (rebuilt when CACHEBUST changes)
COPY --chown=user . .

# HuggingFace uses port 7860
ENV PORT=7860
EXPOSE 7860

# Environment variables are set via HuggingFace Secrets
# Required secrets: NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, ZAI_API_KEY

# Start server
CMD ["python", "server.py"]
