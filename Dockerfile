FROM python:3.12-slim


ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PORT=8000

WORKDIR /app


RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry v2 and make it available
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 \
    && ln -s /opt/poetry/bin/poetry /usr/local/bin/poetry

# Copy dependency files first (layer cache)
COPY pyproject.toml poetry.lock* /app/

# Try to skip dev group if present; if that fails (group not found), fallback to a normal install.
RUN poetry config virtualenvs.create false \
    && (poetry install --no-interaction --no-ansi --no-root --without dev \
         || poetry install --no-interaction --no-ansi --no-root)

# Copy app code
COPY . /app


EXPOSE ${PORT}


CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]