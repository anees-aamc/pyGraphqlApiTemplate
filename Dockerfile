# ---------- Base Image ----------
FROM python:3.11-slim AS base

# Prevent Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies for psycopg2/asyncpg
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ---------- Dependencies Layer ----------
FROM base AS deps

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---------- Runtime Layer ----------
FROM base AS runtime

COPY --from=deps /usr/local /usr/local

# Copy application code
COPY . .

# Default command (can be overridden in docker-compose or ECS)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
