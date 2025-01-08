FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy files into the container
COPY entrypoint.sh /app/entrypoint.sh
COPY generate_svg/ /app/generate_svg/
COPY requirements.txt /app/requirements.txt

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Run the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
