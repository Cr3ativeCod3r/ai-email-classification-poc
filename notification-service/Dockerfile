FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:0.4.15 /uv /bin/uv
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev || true
COPY src/ ./src/
RUN uv sync --frozen --no-dev
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src"
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "notification_service.main:app", "--host", "0.0.0.0", "--port", "8000"]
