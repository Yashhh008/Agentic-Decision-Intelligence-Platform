"""
ADIP — Embedding Service

Provides text embedding using SentenceTransformers (all-MiniLM-L6-v2).
Runs locally — no API cost, no rate limits.

Used by:
- RetrievalService (query embedding)
- Knowledge ingestion script (document embedding)
"""
from __future__ import annotations

import numpy as np
from sentence_transformers import SentenceTransformer

from backend.config.settings import settings
from backend.utils.logger import get_logger

logger = get_logger(__name__)

_model_instance: SentenceTransformer | None = None


def get_embedding_model() -> SentenceTransformer:
    """Returns singleton SentenceTransformer model."""
    global _model_instance
    if _model_instance is None:
        logger.info(f"Loading embedding model: {settings.embedding_model}")
        _model_instance = SentenceTransformer(settings.embedding_model)
        logger.info("Embedding model loaded.")
    return _model_instance


class EmbeddingService:
    """
    Generates sentence embeddings for text chunks and queries.

    Usage:
        service = EmbeddingService()
        vector = service.embed("customer struggling with onboarding")
        vectors = service.embed_batch(["text1", "text2"])
    """

    def __init__(self) -> None:
        self.model = get_embedding_model()

    def embed(self, text: str) -> np.ndarray:
        """
        Generates a single embedding vector.

        Args:
            text: Input text to embed.

        Returns:
            numpy array of shape (embedding_dim,)
        """
        vector = self.model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
        return vector

    def embed_batch(self, texts: list[str]) -> np.ndarray:
        """
        Generates embeddings for multiple texts at once.

        Args:
            texts: List of input strings.

        Returns:
            numpy array of shape (len(texts), embedding_dim)
        """
        vectors = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            batch_size=32,
            show_progress_bar=False,
        )
        return vectors
