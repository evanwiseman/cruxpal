#!/usr/bin/env bash
set -e

# Ensure we're at project root
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# Activate venv if not already active
if [ -z "$VIRTUAL_ENV" ]; then
  source .venv/bin/activate
fi

echo "Starting FastAPI dev server..."

exec uvicorn backend.app.main:app \
  --reload \
  --host 127.0.0.1 \
  --port 8000
