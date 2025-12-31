# Simple Dockerfile for deploying to Render using Poetry
FROM python:3.11-slim

# Keep Python output unbuffered (useful for container logs)
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Default port (Render provides $PORT at runtime)
ENV PORT=8000

WORKDIR /app

# Install system deps required by some Python packages and curl to install Poetry
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry (official installer) and make it available in PATH
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python \
    && ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry

# Copy dependency metadata first for layer caching
COPY pyproject.toml poetry.lock* /app/

# Install dependencies system-wide (disable creating virtualenvs so packages are available in container)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copy the application code
COPY . /app

# Expose the port (informational)
EXPOSE ${PORT}

# Use uvicorn directly for simplicity. Render will set $PORT at runtime.
# The shell form allows $PORT to be substituted by the runtime environment.
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
