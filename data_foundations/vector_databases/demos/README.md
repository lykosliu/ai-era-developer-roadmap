---
name: vector database demos
description: Hands-on examples and runnable code for vector databases.
---

# Vector Database Demos

This directory contains simple, runnable examples of how to use a vector database for semantic search.

## 📁 Demos Included

1. **`demo_query.py`**: A Python script that demonstrates:
   - Creating a simple in-memory vector store using **ChromaDB**.
   - Adding text documents with embeddings (using a default local model).
   - Performing a semantic query and retrieving the most relevant results.

---

## 🚀 How to Run

### 1. Setup Environment
We recommend using a virtual environment. Run the setup script to install dependencies:

```bash
bash setup.sh
```

### 2. Run the Demo
Once the dependencies are installed, run the query demo:

```bash
python demo_query.py
```

---

## 🛠️ Prerequisites
- Python 3.9+
- `pip` (Python package manager)
- Internet access (to download the lightweight embedding model)
