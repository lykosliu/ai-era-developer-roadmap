---
name: SQLite (Vector Search)
description: Using SQLite as a local-first vector store via loadable extensions like sqlite-vec.
---

# SQLite for Vector Search (Local-First Vector “Database”)

## Overview
SQLite is a lightweight, embedded relational database. By itself, SQLite does not provide native vector similarity search, but it can be extended via loadable extensions to store embeddings and run kNN-style queries inside a single `.db` file.
In practice, “SQLite as a vector database” usually means:
- SQLite provides the persistence, transactions, and SQL query engine.
- A vector extension provides vector storage types and similarity search operators.

## Why it matters in the AI Era
SQLite-based vector search is a strong fit for local-first AI applications:
- **Zero infrastructure:** no server to deploy; the database is a file.
- **Edge and offline:** works on laptops, mobile/desktop apps, and embedded devices.
- **Privacy-friendly:** embeddings and metadata can stay local.
- **Composable queries:** combine vector search with standard SQL filtering and joins.

---

## Key Principles

1. **Use a Vector Extension**
   - Popular options include sqlite-vec (a small, dependency-free C extension) and sqlite-vss (an older approach that integrates FAISS).
2. **Store Embeddings in a Virtual Table**
   - Extensions typically expose a virtual table (for example, `vec0`) that defines one or more vector columns with a fixed dimension (e.g., `float[768]`).
3. **Run kNN Queries via SQL**
   - Query patterns commonly look like: “vector column matches query vector” then “order by distance” and “limit k”.
4. **Keep Metadata in SQL Columns**
   - Store document IDs, text, tags, timestamps, and tenant identifiers as regular columns, then combine them with vector search in a single query.

---

## FTS5, BM25, VEC, and VSS: Concepts, Links, and Differences

SQLite “search” usually comes from multiple layers that can be combined:

- **FTS5:** SQLite’s built-in full-text search virtual table module (lexical search).
- **BM25:** a classic lexical relevance scoring function commonly used to rank FTS results.
- **VEC (sqlite-vec / vec0):** a vector-search extension that adds vector storage + kNN queries in SQLite.
- **VSS (sqlite-vss / vss0):** a vector-search extension built on FAISS (powerful indexing, but older and not actively developed).

### FTS5 (Lexical Search)
FTS5 indexes tokens from text columns into an inverted index. It answers “does the document contain these terms?” and supports phrase queries, boolean logic, and prefix search.

Typical query shape:
- `WHERE fts_table MATCH ?` to find candidate rows.
- `ORDER BY bm25(fts_table)` (or `ORDER BY rank`) to rank by lexical relevance.

Strengths:
- Great when exact words matter (names, error messages, identifiers, rare terms).
- Deterministic and explainable ranking and highlighting.

Limitations:
- Weak on semantic matches (synonyms, paraphrases, cross-lingual) without extra work.

### BM25 (Ranking for FTS)
BM25 is a ranking formula that balances term frequency, document length, and inverse document frequency. In FTS5, `bm25()` is exposed as an auxiliary function to sort results from best to worst (numerically smaller scores indicate better matches).

Why it matters:
- It turns FTS5 from “find matches” into “rank matches”.
- It is often the baseline for hybrid retrieval (BM25 candidates, then vector rerank).

### sqlite-vec / vec0 (Vector Search Inside SQLite)
sqlite-vec adds a `vec0` virtual table that can store vectors (e.g., `float[768]`) and run kNN-style queries via SQL. The core idea is “closest vectors in embedding space,” which enables semantic retrieval.

Typical query shape (conceptually):
- `WHERE embedding MATCH ?`
- `ORDER BY distance`
- `LIMIT k`

Strengths:
- Strong semantic matching for RAG and “meaning-based” search.
- Simple local-first deployment (just SQLite + an extension).

Limitations:
- Pure vector similarity does not handle exact tokens well by itself.
- Hybrid ranking (BM25 + vector) requires explicit query planning in SQL (often a 2-stage pipeline).

### sqlite-vss / vss0 (FAISS-backed Vector Search in SQLite)
sqlite-vss exposes a `vss0` virtual table and uses FAISS for indexing and similarity search. It offers a SQL API with `vss_search(...)` in the `WHERE` clause and supports configuring FAISS index factories (e.g., IVF variants), which can improve performance at scale.


### How They Work Together (Hybrid Retrieval)
In SQLite, “hybrid search” usually means combining:
- **FTS5 + BM25** for lexical recall and precision on exact terms, and
- **VEC/VSS** for semantic recall over embeddings.

Common patterns:
1. **BM25 first, vector rerank:** use FTS5 to get a candidate set quickly, then run vector similarity only on those candidates (or rerank candidates in application code).
2. **Vector first, lexical filter:** use vector search to retrieve semantically relevant items, then apply SQL filters (tenant/time/tag) and optionally re-rank with lexical signals.
3. **Union + weighted scoring:** take top-N from both systems, merge, and compute a combined score.

Practical rule of thumb:
- Use **FTS5/BM25** when exact wording matters or when you need robust keyword search.
- Use **VEC/VSS** when meaning matters (RAG, semantic search, recommendations).
- Use **hybrid** when you need both reliability on exact terms and semantic recall.

## AI Context: Common Patterns

- **RAG on a laptop:** store chunk embeddings + metadata in SQLite, retrieve top-k chunks per query, then feed them into an LLM.
- **On-device semantic search:** search notes, emails, or code snippets without sending data to external services.
- **Hybrid retrieval:** use SQL filters first (tenant/time/type), then run vector similarity on the remaining subset (or filter after retrieval, depending on extension support).

---

## Getting Started

1. Pick an extension (recommended starting point: sqlite-vec).
2. Load the extension in your SQLite runtime (Python/Node/Ruby/CLI).
3. Create a vector virtual table (e.g., `CREATE VIRTUAL TABLE ... USING vec0(...)`).
4. Insert embeddings and metadata.
5. Query with a kNN-style SQL statement and tune for your workload.

See [demos/](./demos/) for a minimal Python example using sqlite-vec.

## References
- https://github.com/asg017/sqlite-vec
- https://github.com/asg017/sqlite-vss
- https://www.sqlite.org/fts5.html
