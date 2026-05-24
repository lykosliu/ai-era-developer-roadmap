---
name: vector_databases
description: Vector storage and semantic retrieval systems.
---

# Vector Databases: The Long-Term Memory of AI

## Overview
Vector databases are specialized storage systems designed to store, index, and efficiently search through high-dimensional vector representations (embeddings). They are the cornerstone of Retrieval-Augmented Generation (RAG) and semantic search.

## Why it matters in the AI Era
LLMs have limited context windows and lack real-time access to private or fresh data. Vector databases act as an external "long-term memory," allowing models to retrieve relevant context from vast amounts of data in milliseconds.

---

## Key Principles

1. **Embeddings:** Data (text, images, audio) is transformed into numerical vectors by an embedding model.
2. **Similarity Search:** Instead of exact keyword matching, vector databases use algorithms like ANN (Approximate Nearest Neighbors) to find vectors that are semantically similar.
3. **Dimensionality:** Vectors typically have hundreds or thousands of dimensions, representing complex semantic relationships.

---

## AI Context: Powering RAG and Beyond
Vector databases are not just "fast search engines"—they are the foundation for:
- **Semantic Retrieval:** Finding content by meaning, not just words.
- **Multimodal Search:** Connecting text queries to images or video through shared embedding spaces.
- **Agent Memory:** Enabling AI agents to remember past interactions or reference specific documentation.

---

## Getting Started
Check out our [demos/](./demos/) directory to see a simple vector search in action using **ChromaDB**.

## Popular Tools
- **Managed:** Pinecone, Weaviate Cloud, Milvus.
- **Self-Hosted/Local:** ChromaDB, FAISS, Qdrant, SQLite (via extensions like sqlite-vec).

---

## Vector Databases vs Vector Search Engines
Vector databases and vector search engines overlap in the user-facing goal (nearest-neighbor retrieval), but they differ in scope:

### Definitions (Scope Boundary)
- **Vector search engine:** a library or service primarily focused on fast kNN/ANN over vectors (indexing + search).
- **Vector database:** a system of record that combines vector search with database capabilities (data model, filtering, durability, operations).

### Core Responsibilities
- **Vector search engine typically provides**
  - Similarity search primitives (L2 / inner product; cosine via normalization).
  - Index types and tuning knobs (Flat, IVF, HNSW, PQ/SQ) to trade recall for latency/memory.
  - CPU/GPU acceleration and high-throughput batch search.
  - Optional index serialization (save/load), usually without full DB semantics.
- **Vector database typically adds**
  - Persistent storage for vectors + documents/metadata as first-class records.
  - Metadata filtering (multi-tenant isolation, tags, time windows) and richer query APIs.
  - Operational guarantees (safe concurrent reads/writes, durability, backups/restore, compaction).
  - Service features (authentication/authorization, observability, clustering, sharding, replication).

### Where FAISS Fits
FAISS is best understood as a **vector search engine / indexing library**. It stores vectors inside an in-memory (or GPU) index and returns integer IDs; applications commonly maintain an external mapping from those IDs to documents and metadata.

### Memory Model (Practical Implications)
Many vector search engines (including FAISS) are optimized for **in-memory (or in-GPU) retrieval**. When data is too large for memory, common approaches are:
- **Compression (PQ/SQ):** reduce bytes per vector so the index fits with acceptable recall.
- **Disk-backed variants / memory mapping:** trade latency for capacity by paging parts of the index from disk.

### Practical Rule of Thumb
- Choose a **vector search engine** when you want maximum performance/control and are willing to build metadata filtering, persistence workflows, and service operations yourself.
- Choose a **vector database** when you want an out-of-the-box system that includes filtering, durability, and operational tooling as part of the product.
