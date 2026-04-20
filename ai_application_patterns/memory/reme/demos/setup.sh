#!/usr/bin/env bash
set -euo pipefail

echo "[1/3] Checking Python..."
if command -v python3 >/dev/null 2>&1; then
  python3 --version
else
  echo "python3 is required but not found."
  exit 1
fi

echo "[2/3] Creating virtual environment..."
python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate

echo "[3/3] Installing dependencies..."
python -m pip install --upgrade pip

echo "Removing conflicting PyPI package named 'reme' (if installed)..."
python -m pip uninstall -y reme >/dev/null 2>&1 || true

echo "Installing AgentScope ReMe from GitHub..."
python -m pip install "git+https://github.com/agentscope-ai/ReMe.git"
python -m pip install agentscope

echo "Installing optional semantic-local dependency..."
if ! python -m pip install "sentence-transformers>=3,<4"; then
  echo "Warning: sentence-transformers install failed on this platform."
  echo "You can still run:"
  echo "  python demo_local_file_memory.py --mode fts"
  echo "or use semantic mode with OpenAI-compatible embedding API:"
  echo "  python demo_local_file_memory.py --mode semantic"
fi

echo "Verifying ReMeLight import path..."
python - <<'PY'
import sys

try:
    from reme.reme_light import ReMeLight  # noqa: F401
except Exception as exc:  # pragma: no cover
    print("ERROR: reme.reme_light is not available.")
    print(f"Reason: {exc}")
    print("Please check network access to github.com and rerun: bash setup.sh")
    sys.exit(1)
print("Import check passed: reme.reme_light")
PY

echo "Setup complete."
echo "Run:"
echo "  source .venv/bin/activate"
echo "  python demo_local_file_memory.py"
