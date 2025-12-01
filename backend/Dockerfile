# Backend Dockerfile for FillyTrckr API
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create common directory structure
RUN mkdir -p /app/common

# Copy common module files (excluding test, __pycache__, and config.json)
COPY ../common/*.py /app/common/
COPY ../common/*.env /app/common/
COPY ../common/*.md /app/common/
COPY ../common/config_example.json /app/common/

# Copy backend files (excluding test and __pycache__)
COPY *.py /app/
COPY *.env /app/
COPY *.json /app/
COPY *.md /app/

# Create logs directory
RUN mkdir -p /app/logs

# Expose the API port (default 8000)
EXPOSE 8000

# Set Python path to include common directory
ENV PYTHONPATH=/app:/app/common

# Run the application
CMD ["python", "main.py"]
