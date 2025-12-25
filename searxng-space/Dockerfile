# SearXNG for HuggingFace Spaces
FROM searxng/searxng:latest

# Copy custom settings
COPY settings.yml /etc/searxng/settings.yml

# HuggingFace uses port 7860
ENV SEARXNG_PORT=7860
ENV BIND_ADDRESS=0.0.0.0:7860
ENV SEARXNG_SECRET=byrd-searxng-secret-key-2024

# Expose port
EXPOSE 7860

# Use the default entrypoint
CMD ["/sbin/tini", "--", "/usr/local/searxng/dockerfiles/docker-entrypoint.sh"]
