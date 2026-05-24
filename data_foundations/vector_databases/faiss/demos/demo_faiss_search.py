"""
Minimal FAISS similarity search demo.

What this script shows:
- How to build a FAISS index in memory (no persistence, no metadata store).
- How to add vectors (embeddings) and query for top-k nearest neighbors.
- How to do cosine similarity search using an inner-product index:
  1) L2-normalize vectors
  2) use IndexFlatIP (Inner Product)
  3) the returned scores become cosine similarities in [-1, 1]
"""

import numpy as np

try:
    import faiss
except ImportError as exc:
    raise SystemExit(
        "faiss is not installed. Run 'bash setup.sh' first."
    ) from exc


def l2_normalize(vectors: np.ndarray) -> np.ndarray:
    """
    L2-normalize vectors row-wise.

    After normalization:
    - cosine_similarity(a, b) == dot(a, b)
    - using a FAISS inner-product index is equivalent to cosine retrieval
    """
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors / np.clip(norms, 1e-12, None)


def run_demo() -> None:
    # "labels" act like document IDs. In real systems, you keep an external mapping
    # from FAISS integer IDs -> your document/row metadata.
    labels = [
        "llm_memory",
        "prompt_engineering",
        "vector_database",
        "rag_pipeline",
        "agent_planning",
        "embedding_model",
        "semantic_search",
        "fine_tuning",
    ]
    # Sample embeddings (8 vectors, dim=4). Real embeddings are typically
    # 384/768/1024+ dimensions produced by an embedding model.
    vectors = np.array(
        [
            [0.90, 0.10, 0.20, 0.10],
            [0.88, 0.05, 0.30, 0.15],
            [0.10, 0.92, 0.25, 0.20],
            [0.12, 0.89, 0.18, 0.30],
            [0.30, 0.20, 0.85, 0.10],
            [0.22, 0.15, 0.80, 0.18],
            [0.14, 0.95, 0.12, 0.25],
            [0.40, 0.25, 0.75, 0.35],
        ],
        dtype=np.float32,
    )

    # FAISS expects float32 and prefers contiguous arrays.
    vectors = np.ascontiguousarray(vectors, dtype=np.float32)

    # Normalize so inner product == cosine similarity.
    vectors = l2_normalize(vectors)
    dim = vectors.shape[1]

    # IndexFlatIP is an exact (brute-force) index using inner product.
    # For larger datasets, you typically switch to IVF/HNSW/PQ variants.
    index = faiss.IndexFlatIP(dim)
    index.add(vectors)
    print(f"Indexed vectors: {index.ntotal}")

    # Query vector close to semantic retrieval topics.
    # In practice, this comes from embedding("your query text").
    query = np.array([[0.08, 0.96, 0.10, 0.22]], dtype=np.float32)
    query = np.ascontiguousarray(query, dtype=np.float32)
    query = l2_normalize(query)

    k = 3
    # search() returns:
    # - scores: shape (n_queries, k)
    # - indices: shape (n_queries, k), each is the integer ID of the matched vector
    scores, indices = index.search(query, k)

    print("\nTop-3 nearest labels:")
    for rank, (idx, score) in enumerate(zip(indices[0], scores[0]), start=1):
        print(f"{rank}. {labels[idx]} (cosine={score:.4f})")


if __name__ == "__main__":
    run_demo()
