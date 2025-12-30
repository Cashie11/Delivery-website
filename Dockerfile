# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project files
COPY . .

# Make entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Create directories for static and media files
RUN mkdir -p /app/staticfiles /app/media /app/db

# Expose port 80
EXPOSE 80

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Default command
CMD ["/bin/sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn swifttrack.wsgi:application --bind 0.0.0.0:80 --workers 3"]