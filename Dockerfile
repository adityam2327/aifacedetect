# Use a Python 3.10 slim image as base
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set working directory inside the container
WORKDIR /app

# Install system dependencies needed for OpenCV and TensorFlow
# libgl1-mesa-glx and libglib2.0-0 are critical for OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
# Using --no-cache-dir to keep the image small
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create directories for face processing
RUN mkdir -p faces known unknown temp database

# Expose port for FastAPI
EXPOSE 8000

# Command to run the API
# We use api:app because your FastAPI instance is defined as 'app' in api.py
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
