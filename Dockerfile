FROM python:3.12-slim

# Unbuffered stdout/stderr, no pyc files
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PORT=8000

WORKDIR /app

# Install required system packages (add libpq-dev if you use psycopg2)
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry and make it available system-wide
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 \
    && ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry

# Copy dependency files first (cache layer)
COPY pyproject.toml poetry.lock* /app/

# Install dependencies into the system Python (disable virtualenv creation)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root --no-dev

# Copy application code
COPY . /app

# Informational port
EXPOSE ${PORT}

# Run the app with uvicorn (Render provides PORT at runtime)
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
