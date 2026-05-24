---
name: Demos
description: Hands-on examples and runnable code.
---

# FAISS Demos

This directory contains a minimal, runnable FAISS example for vector similarity search.

## Demo Included

1. `demo_faiss_search.py`
   - Builds an in-memory FAISS index.
   - Adds sample vectors with labels.
   - Runs a query and returns top-k nearest vectors.

## How to Run

1. Setup environment and install dependencies:

```bash
bash setup.sh
```

2. Activate the virtual environment:

```bash
source .venv/bin/activate
```

3. Run the demo:

```bash
python demo_faiss_search.py
```

## Prerequisites

- Python 3.9+
- `pip`
