---
name: Demos
description: Minimal sqlite-vec (vec0) demo for creating a vector table and running top-k similarity queries.
---

# SQLite Vector Search Demos

This directory contains a minimal, runnable example of using SQLite for vector search via a loadable extension.

## Demo Included

1. `demo_sqlite_vec.py`
   - Creates a local SQLite database file.
   - Loads the sqlite-vec extension.
   - Creates a `vec0` virtual table with an embedding column and metadata columns.
   - Inserts sample embeddings and runs a top-k similarity query.

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
python demo_sqlite_vec.py
```

## Prerequisites

- Python 3.9+
- `pip`
