# demo_sentence_transformers_embedding_collection.py
# Simple demo: query the most similar documents with Sentence Transformers.

import argparse
from sentence_transformers import SentenceTransformer, util
import torch


def print_section(title: str) -> None:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def show_top_k(query: str, doc_texts: list[str], doc_embeddings: torch.Tensor, model: SentenceTransformer, k: int = 3) -> None:
    # `encode()` converts text to dense vectors.
    # - `convert_to_tensor=True`: returns a torch.Tensor instead of Python list.
    # - `normalize_embeddings=True`: L2-normalizes vectors so cosine similarity is stable and comparable.
    query_embedding = model.encode(query, convert_to_tensor=True, normalize_embeddings=True)

    # `util.cos_sim(a, b)` returns cosine-similarity matrix.
    # Here shape is [1, N], so `[0]` extracts the single query's scores against N docs.
    scores = util.cos_sim(query_embedding, doc_embeddings)[0]

    # `torch.topk()` picks the highest-k similarity scores and their doc indices.
    top_scores, top_indices = torch.topk(scores, k=min(k, len(doc_texts)))

    print(f"Query: {query}")
    for rank, (score, idx) in enumerate(zip(top_scores, top_indices), start=1):
        print(f"{rank}. score={score.item():.4f} | doc={doc_texts[idx]}")


def parse_args() -> argparse.Namespace:
    # `argparse` exposes runtime params so model/query are not hardcoded in script logic.
    parser = argparse.ArgumentParser(
        description="Simple semantic retrieval demo with Sentence Transformers."
    )
    parser.add_argument(
        "--model",
        type=str,
        default="sentence-transformers/all-MiniLM-L6-v2",
        help="Model name or local path compatible with SentenceTransformer.",
    )
    parser.add_argument(
        "--query",
        type=str,
        default="What improves retrieval relevance in RAG systems?",
        help="User query for semantic retrieval.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=3,
        help="Number of most similar documents to return.",
    )
    return parser.parse_args()


def main(model_name: str, query: str, top_k: int) -> None:
    # `SentenceTransformer(model_name)` loads an embedding model from:
    # - Hugging Face model id, or
    # - Local model directory path.
    model = SentenceTransformer(model_name)

    documents = [
        "RAG combines retrieval and generation to improve answer grounding.",
        "Vector databases store embeddings for semantic search.",
        "Prompt engineering helps control model behavior with better instructions.",
        "Cross-encoders are often used for final-stage reranking.",
        "Chunking strategy strongly affects retrieval quality in long documents.",
        "GPU memory and KV cache planning are critical in local LLM serving.",
        "vLLM improves throughput with continuous batching and paged attention.",
        "Ollama is useful for quick local model prototyping and testing.",
    ]

    print_section("1) Build Embedding Collection")
    # Batch encode document collection to build the retrieval index in memory.
    doc_embeddings = model.encode(documents, convert_to_tensor=True, normalize_embeddings=True)
    print(f"Model: {model_name}")
    print(f"Document count: {len(documents)}")
    print(f"Embedding tensor shape: {tuple(doc_embeddings.shape)}")

    print_section("2) Query Top-K Similar Documents")
    show_top_k(query, documents, doc_embeddings, model, k=max(1, top_k))


if __name__ == "__main__":
    args = parse_args()
    main(model_name=args.model, query=args.query, top_k=args.top_k)
