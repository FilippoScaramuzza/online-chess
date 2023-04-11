# Use a smaller base image
FROM python:3.8-slim-buster AS base

# Set the working directory in the container
WORKDIR /app

# Copy only requirements.txt file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Use a second stage to copy only necessary files
FROM base AS final

WORKDIR /app

COPY . .

CMD ["python", "server.py"]