import json
import os
import sqlite3

import numpy as np


def load_sqlite_vec(conn: sqlite3.Connection) -> None:
    conn.enable_load_extension(True)
    try:
        import sqlite_vec

        sqlite_vec.load(conn)
    except Exception:
        conn.load_extension("vec0")
    finally:
        conn.enable_load_extension(False)


def to_vec_json(vec: np.ndarray) -> str:
    return json.dumps([float(x) for x in vec.tolist()])


def run() -> None:
    db_path = os.path.join(os.path.dirname(__file__), "demo_sqlite_vec.db")
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    try:
        load_sqlite_vec(conn)

        conn.execute(
            """
            CREATE VIRTUAL TABLE docs USING vec0(
              embedding float[8],
              doc_id TEXT,
              content TEXT,
              tag TEXT
            )
            """
        )

        rng = np.random.default_rng(7)
        rows = []
        for i, (content, tag) in enumerate(
            [
                ("Vector databases store embeddings for semantic retrieval.", "vector"),
                ("RAG retrieves context before generation.", "rag"),
                ("SQLite is an embedded database stored as a single file.", "sqlite"),
                ("FAISS provides fast similarity search primitives.", "faiss"),
                ("Metadata filtering is often handled by the database layer.", "vector"),
            ],
            start=1,
        ):
            vec = rng.normal(size=(8,)).astype(np.float32)
            rows.append((i, to_vec_json(vec), f"doc_{i}", content, tag))

        conn.executemany(
            "INSERT INTO docs(rowid, embedding, doc_id, content, tag) VALUES(?, ?, ?, ?, ?)",
            rows,
        )
        conn.commit()

        query_vec = rows[1][1]
        k = 3

        results = conn.execute(
            """
            SELECT
              rowid,
              doc_id,
              tag,
              distance,
              content
            FROM docs
            WHERE embedding MATCH ?
            ORDER BY distance
            LIMIT ?
            """,
            (query_vec, k),
        ).fetchall()

        print("Top-k results (smaller distance = more similar):")
        for rowid, doc_id, tag, distance, content in results:
            print(f"- {doc_id} (rowid={rowid}, tag={tag}, distance={distance:.6f})")
            print(f"  {content}")

        filtered = conn.execute(
            """
            SELECT
              doc_id,
              distance,
              content
            FROM docs
            WHERE embedding MATCH ?
              AND tag = ?
            ORDER BY distance
            LIMIT 2
            """,
            (query_vec, "vector"),
        ).fetchall()

        print("\nFiltered results (tag='vector'):")
        for doc_id, distance, content in filtered:
            print(f"- {doc_id} (distance={distance:.6f})")
            print(f"  {content}")
    finally:
        conn.close()


if __name__ == "__main__":
    run()
