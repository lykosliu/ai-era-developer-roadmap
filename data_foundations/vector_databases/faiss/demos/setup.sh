#!/bin/bash

# setup.sh: Install dependencies for FAISS demo

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is not installed. Please install it first."
  exit 1
fi

echo "Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "Installing dependencies (faiss-cpu, numpy)..."
pip install --upgrade pip
pip install faiss-cpu numpy

echo "Setup complete! Run 'source .venv/bin/activate' and then 'python demo_faiss_search.py'."
