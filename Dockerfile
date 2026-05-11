FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements_unified.txt .
RUN pip install --no-cache-dir -r requirements_unified.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data styles utils

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run the application
CMD ["streamlit", "run", "app/unified_app.py", "--server.headless", "true", "--server.port", "8501", "--server.address", "0.0.0.0"]
