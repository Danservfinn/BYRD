FROM python:3.11-slim

WORKDIR /app

# Install curl for health checks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Koyeb provides PORT environment variable
ENV PORT=8000

# Expose the port
EXPOSE 8000

# Health check endpoint for Koyeb
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:${PORT}/api/status || exit 1

# Start server
CMD ["sh", "-c", "python3 server.py"]
