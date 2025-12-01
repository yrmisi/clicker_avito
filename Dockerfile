# ===== STAGE 1: сборка с компиляцией =====
FROM python:3.14-slim-bookworm AS builder

ENV UV_COMPILE_BYTECODE=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
        libpq5 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./


RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-cache

# ===== STAGE 2: финальный образ =====
FROM python:3.14-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Только runtime-зависимости: libpq — для подключения к PostgreSQL, curl - для отладки/health-check
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Копируем виртуальное окружение из builder
COPY --from=builder /app/.venv ./.venv

ENV PATH="/app/.venv/bin:$PATH"

COPY src/ ./src/
COPY alembic/ ./alembic/
COPY alembic.ini ./

EXPOSE 8000
CMD ["granian", "--interface", "asgi", "src.main:app", "--workers", "2", "--host", "0.0.0.0", "--port", "8000", "--access-log"]
