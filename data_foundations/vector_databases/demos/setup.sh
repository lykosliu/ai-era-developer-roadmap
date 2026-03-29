#!/bin/bash

# setup.sh: Install dependencies for the vector database demo

# Check for Python
if ! command -v python3 &> /dev/null
then
    echo "Python 3 is not installed. Please install it first."
    exit 1
fi

# Create a virtual environment (optional but recommended)
echo "Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install required packages
echo "Installing dependencies (chromadb, sentence-transformers)..."
pip install chromadb sentence-transformers

echo "Setup complete! Run 'source .venv/bin/activate' and then 'python demo_query.py'."
