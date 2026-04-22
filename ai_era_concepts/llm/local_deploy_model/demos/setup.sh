#!/bin/bash

# setup.sh: Install dependencies for Sentence Transformers embedding demos

set -e

if ! command -v python3 >/dev/null 2>&1; then
    echo "Python 3 is not installed. Please install it first."
    exit 1
fi

echo "Creating virtual environment in .venv ..."
python3 -m venv .venv
source .venv/bin/activate

echo "Installing dependencies ..."
pip install --upgrade pip
pip install sentence-transformers

echo "Setup complete."
echo "Next steps:"
echo "1) source .venv/bin/activate"
echo "2) python demo_sentence_transformers_embedding_collection.py"
