# SearXNG for HuggingFace Spaces
FROM searxng/searxng:latest

# HuggingFace requires non-root user
USER root

# Create settings directory
RUN mkdir -p /etc/searxng

# Copy custom settings
COPY settings.yml /etc/searxng/settings.yml

# HuggingFace uses port 7860
ENV SEARXNG_PORT=7860
ENV SEARXNG_BIND_ADDRESS=0.0.0.0:7860
ENV SEARXNG_SECRET_KEY=byrd-searxng-secret-key

# Expose port
EXPOSE 7860

# Start SearXNG
CMD ["python", "-m", "searx.webapp"]
