# Genes Platform - Agente_Constructor
FROM python:3.11-slim

LABEL platform="genes"
LABEL component="agente_constructor"
LABEL maintainer="AFS Capital"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY agente_constructor/ ./agente_constructor/
COPY shared/ ./shared/
COPY config/ ./config/

# Create necessary directories
RUN mkdir -p /app/agents/generated /app/logs

# Expose API port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["python", "-m", "uvicorn", "agente_constructor.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
