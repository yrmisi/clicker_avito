FROM python:3.13-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        # компилятор C для uv
        build-essential \
        python3-dev \
        curl \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

COPY pyproject.toml uv.lock /app/
RUN uv sync --frozen --no-cache

ENV PATH="/app/.venv/bin:$PATH"

COPY /src .

EXPOSE 8000

# CMD ["uvicorn", "main:app", "--proxy-headers", "--workers", "3", "--host", "0.0.0.0", "--port", "8000"]
CMD ["granian", "--interface", "asgi", "main:app", "--workers", "3", "--host", "0.0.0.0", "--port", "8000"]
