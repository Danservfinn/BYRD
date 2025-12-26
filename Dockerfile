FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including Node.js for Claude CLI
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Claude CLI globally
RUN npm install -g @anthropic-ai/claude-code

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create startup script that configures Claude CLI credentials
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
# Configure Claude CLI credentials from environment variable\n\
# Use $HOME which is /home/user on HuggingFace, /root on local Docker\n\
CLAUDE_DIR="$HOME/.claude"\n\
if [ -n "$CLAUDE_OAUTH_CREDS" ]; then\n\
    echo "Configuring Claude CLI OAuth credentials..."\n\
    mkdir -p "$CLAUDE_DIR"\n\
    echo "$CLAUDE_OAUTH_CREDS" | base64 -d > "$CLAUDE_DIR/.credentials.json"\n\
    chmod 600 "$CLAUDE_DIR/.credentials.json"\n\
    echo "Claude CLI configured at $CLAUDE_DIR/.credentials.json"\n\
    ls -la "$CLAUDE_DIR"\n\
else\n\
    echo "No CLAUDE_OAUTH_CREDS found - Claude CLI will be disabled"\n\
fi\n\
\n\
# Start the server\n\
exec python3 server.py\n\
' > /app/start.sh && chmod +x /app/start.sh

# HuggingFace provides PORT environment variable
ENV PORT=8000

# Expose the port
EXPOSE 8000

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:${PORT}/api/status || exit 1

# Start with credential setup
CMD ["/app/start.sh"]
