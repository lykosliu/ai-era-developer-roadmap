from __future__ import annotations

import asyncio
from typing import Optional

from reme.core.embedding.base_embedding_model import BaseEmbeddingModel
from reme.core.registry_factory import R


class LocalSentenceTransformerEmbeddingModel(BaseEmbeddingModel):
    """In-process local embedding backend using sentence-transformers."""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2", **kwargs):
        super().__init__(model_name=model_name, **kwargs)
        self._model = None
        self._resolved_dims: Optional[int] = None

    def _ensure_model(self):
        if self._model is not None:
            return
        try:
            from sentence_transformers import SentenceTransformer
        except ModuleNotFoundError as exc:  # pragma: no cover
            raise RuntimeError(
                "sentence-transformers is required for semantic-local mode.\n"
                "Install it with: pip install sentence-transformers"
            ) from exc
        except Exception as exc:  # pragma: no cover
            raise RuntimeError(
                "Failed to initialize sentence-transformers runtime.\n"
                f"Reason: {exc}\n"
                "Please check compatible versions of torch/numpy/transformers in this environment."
            ) from exc

        self._model = SentenceTransformer(self.model_name)
        if hasattr(self._model, "get_sentence_embedding_dimension"):
            dim = self._model.get_sentence_embedding_dimension()
            if isinstance(dim, int) and dim > 0:
                self._resolved_dims = dim
                self.dimensions = dim

    def _encode_sync(self, input_text: list[str]) -> list[list[float]]:
        self._ensure_model()
        vectors = self._model.encode(input_text, normalize_embeddings=True)
        return [list(map(float, vec)) for vec in vectors]

    async def _get_embeddings(self, input_text: list[str], **_kwargs) -> list[list[float]]:
        return await asyncio.to_thread(self._encode_sync, input_text)

    def _get_embeddings_sync(self, input_text: list[str], **_kwargs) -> list[list[float]]:
        return self._encode_sync(input_text)

    async def start(self):
        self._ensure_model()
        await super().start()

    async def close(self):
        self._model = None
        await super().close()


def register_local_embedding_backend() -> None:
    """Register local backend key for ReMe embedding model registry."""
    R.embedding_models.register("local_st")(LocalSentenceTransformerEmbeddingModel)
