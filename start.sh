#!/usr/bin/env bash
set -e

echo "=== [STARTUP] Apex Expeditions Unified Service Initializing ==="

PORT="${PORT:-5000}"

# Navigate to backend directory so all modules, tasks, and configurations resolve directly
cd backend
export PYTHONPATH="${PYTHONPATH}:${PWD}"

# Start Celery background worker
echo "[STARTUP] Launching background Celery worker..."
celery -A tasks.celery_app worker --loglevel=info --concurrency=1 &
CELERY_WORKER_PID=$!

# Start Celery Beat periodic scheduler
echo "[STARTUP] Launching Celery Beat scheduler..."
celery -A tasks.celery_app beat --loglevel=info &
CELERY_BEAT_PID=$!

# Ensure graceful shutdown of background processes upon container termination
cleanup() {
    echo "[SHUTDOWN] Terminating Celery services..."
    kill -TERM "$CELERY_WORKER_PID" 2>/dev/null || true
    kill -TERM "$CELERY_BEAT_PID" 2>/dev/null || true
    exit 0
}
trap cleanup SIGTERM SIGINT

# Launch Gunicorn HTTP WSGI web server in foreground
echo "[STARTUP] Launching Gunicorn WSGI server on port ${PORT}..."
exec gunicorn app:app --bind "0.0.0.0:${PORT}" --workers 2 --threads 4 --timeout 120
