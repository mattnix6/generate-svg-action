FROM python:3.9-slim

# Install dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy application files
COPY entrypoint.sh /app/entrypoint.sh
COPY generate_svg/ /app/generate_svg/
COPY requirements.txt /app/requirements.txt

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Run as non-root user (optional)
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser /app
USER appuser

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
