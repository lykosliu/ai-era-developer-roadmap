#!/usr/bin/env bash
set -euo pipefail

echo "[1/5] Checking make..."
if command -v make >/dev/null 2>&1; then
  make --version | head -n 1
else
  echo "make is required but not found."
  exit 1
fi

echo "[2/5] Checking C compiler..."
if command -v cc >/dev/null 2>&1; then
  cc --version | head -n 1
else
  echo "cc is required but not found."
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "[3/5] Running demo_single_file..."
cd "$SCRIPT_DIR/demo_single_file"
make clean
make help
make run
make verify

echo "[4/5] Running demo_incremental_rebuild..."
cd "$SCRIPT_DIR/demo_incremental_rebuild"
make clean
make help
make run

echo "Touching header to trigger incremental rebuild..."
sleep 1
touch math_utils.h
make build
make verify

echo "[5/5] Running demo_task_entrypoint..."
cd "$SCRIPT_DIR/demo_task_entrypoint"
make clean
make help
make pipeline
make verify

echo "All demos completed successfully."
