---
name: FAISS
description: A high-performance library for large-scale vector similarity search.
---

# FAISS: High-Performance Vector Retrieval at Scale

## Overview
FAISS (Facebook AI Similarity Search) is an open-source library for efficient similarity search and clustering over dense vectors. It is widely used when you need nearest-neighbor retrieval across millions to billions of embeddings with strong performance on CPU and GPU.

## Why it matters in the AI Era
Modern AI applications rely on embeddings for semantic retrieval, recommendation, and memory systems. As data volume grows, exact search becomes too slow or expensive. FAISS provides practical indexing strategies that make large-scale vector retrieval feasible with controllable speed-accuracy tradeoffs.

---

## Key Principles

1. **Index Choice Drives Tradeoffs**
   - `IndexFlat` performs exact search with high accuracy but higher compute cost.
   - Inverted-file and graph-based indexes (such as IVF and HNSW) accelerate retrieval by reducing the candidate set.
2. **Compression Enables Scale**
   - Product Quantization (PQ) and related techniques compress vectors to reduce memory usage.
   - Compression usually lowers recall slightly but allows much larger datasets to fit in memory.
3. **Search Parameters Tune Quality vs Latency**
   - Parameters like `nprobe` (for IVF) and graph traversal controls affect recall and latency.
   - Production systems tune these values for workload-specific SLAs.
4. **Batch and GPU Acceleration**
   - FAISS is optimized for batch queries and can leverage GPUs for high-throughput search and training of indexes.

---

## AI Context: Where FAISS Fits
FAISS is often used as the vector retrieval engine inside AI systems:
- **RAG Pipelines:** Retrieve semantically relevant chunks before generation.
- **Recommendation Systems:** Find similar users/items in embedding space.
- **Semantic Deduplication:** Detect near-duplicate content at scale.
- **Agent Memory Backends:** Support fast similarity lookups for historical context.

Compared with full-featured vector databases, FAISS focuses on retrieval primitives rather than metadata filtering, distributed orchestration, or built-in persistence workflows. It is ideal when teams want fine-grained control and maximum performance in custom infrastructure.

---

## Getting Started
1. Install with `pip install faiss-cpu` (or GPU builds where supported by your environment).
2. Generate embeddings using your selected model.
3. Build an index (`IndexFlatL2`, IVF, HNSW, or PQ-based variants) based on scale and latency goals.
4. Add vectors and run `search()` for top-k nearest neighbors.
5. Evaluate recall/latency, then tune index type and parameters.

## References
- [FAISS Documentation](https://faiss.ai/)
- [FAISS GitHub Repository](https://github.com/facebookresearch/faiss)
- [FAISS Indexes Wiki](https://github.com/facebookresearch/faiss/wiki/Faiss-indexes)
