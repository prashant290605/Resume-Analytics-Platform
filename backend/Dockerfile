# ---- build stage: install dependencies into a venv ----
FROM python:3.12-slim AS builder

WORKDIR /app
COPY backend/requirements.txt .
RUN python -m venv /opt/venv && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# ---- runtime stage: minimal image, non-root user ----
FROM python:3.12-slim

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    RAP_DATA_DIR=/data

RUN useradd --create-home --uid 1001 appuser && mkdir -p /data && chown appuser /data
COPY --from=builder /opt/venv /opt/venv

WORKDIR /app
COPY backend/ backend/

USER appuser
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/health')" || exit 1

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
