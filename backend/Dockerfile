# Backend Dockerfile for FillyTrckr API
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for PostgreSQL
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy common module files
COPY common/*.py ./common/

# Copy backend files
COPY backend/*.py ./

# Create logs directory
RUN mkdir -p /app/logs

# Expose the API port (default 8000)
EXPOSE 8000

# Set Python path to include common directory
ENV PYTHONPATH=/app:/app/common

# Run the application
CMD ["python", "main.py"]
