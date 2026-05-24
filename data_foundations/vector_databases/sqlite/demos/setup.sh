#!/bin/bash

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is not installed. Please install it first."
  exit 1
fi

echo "Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "Installing dependencies (sqlite-vec, numpy)..."
pip install --upgrade pip
pip install sqlite-vec numpy

echo "Setup complete! Run 'source .venv/bin/activate' and then 'python demo_sqlite_vec.py'."
