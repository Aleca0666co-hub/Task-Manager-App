FROM python:3.12-slim

# ---------------------------
# Basic environment
# ---------------------------
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
# Render (and many PaaS) inject a `PORT` environment variable at runtime.
ENV PORT=8000

# App metadata / configuration requested by user
ENV APP_NAME="TodoApp"
ENV VERSION="0.2.1"

# Database (default to a local sqlite file; override in Render dashboard if needed)
ENV DATABASE_URL="sqlite:///./todo_app.db"

# Logging
ENV LOG_DIR="logs"
ENV LOG_FILE="app.log"
ENV LOG_LEVEL="INFO"

WORKDIR /app

# ---------------------------
# System deps and tooling
# ---------------------------
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry (used by this project) and make it available system-wide.
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 \
    && ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry

# Copy dependency files first to leverage Docker layer caching.
COPY pyproject.toml poetry.lock* /app/

# Install Python dependencies into the system interpreter (no virtualenvs).
RUN poetry config virtualenvs.create false \
    && (poetry install --no-interaction --no-ansi --no-root --without dev \
         || poetry install --no-interaction --no-ansi --no-root)

# ---------------------------
# Copy application code
# ---------------------------
# Copy everything after deps so code changes don't bust the dependency cache.
COPY . /app

# Ensure logs directory exists and has correct permissions for the container process.
RUN mkdir -p ${LOG_DIR} \
    && chown -R root:root ${LOG_DIR}

# Expose the runtime port (Render will map its external port here via $PORT)
EXPOSE ${PORT}

# Entrypoint/command: run the FastAPI app with Uvicorn. Use the PORT env var injected by Render.
# The `sh -c` wrapper allows the `${PORT}` substitution to work when passed in JSON array form.
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1"]

# ---------------------------
# Notes for developers (in-Dockerfile guidance):
# - To build locally: `docker build -t todoapp:local .`
# - To run locally:  `docker run -e PORT=8000 -p 8000:8000 todoapp:local`
# - On Render: push this repo and select Docker deployment or use a Render Dockerfile service.
# - Adjust `DATABASE_URL` in Render's Web Service -> Environment to point to a managed DB if needed.
# - If you prefer pip/requirements.txt, replace the Poetry install steps accordingly.