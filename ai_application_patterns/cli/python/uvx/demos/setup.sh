#!/usr/bin/env bash
set -euo pipefail

echo "[1/3] Checking Python..."
if command -v python3 >/dev/null 2>&1; then
  python3 --version
else
  echo "python3 is required but not found."
  exit 1
fi

echo "[2/3] Checking uv..."
if command -v uv >/dev/null 2>&1; then
  uv --version
else
  echo "uv not found. Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh

  if [ -f "$HOME/.local/bin/env" ]; then
    # shellcheck source=/dev/null
    . "$HOME/.local/bin/env"
  fi

  if command -v uv >/dev/null 2>&1; then
    uv --version
  else
    echo "uv installation finished, but uv is not in current PATH."
    echo "Please restart your shell and run: uv --version"
    exit 1
  fi
fi

echo "[3/3] Checking uvx..."
uvx --version

echo "Environment is ready."
