"""
ADIP — FAISS Vector Store

Manages the FAISS index for enterprise knowledge retrieval.
Stores vectors + metadata separately (FAISS stores vectors, JSON stores metadata).
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

import faiss
import numpy as np

from backend.config.settings import settings
from backend.utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class VectorChunk:
    """A stored knowledge chunk with its vector and metadata."""
    chunk_id: str
    content: str
    source: str
    document_type: str
    customer_id: str | None = None


class FAISSVectorStore:
    """
    Manages FAISS index and parallel metadata store.

    The FAISS index stores float32 vectors.
    A JSON file stores the corresponding metadata (content, source, type).
    Both are indexed by integer position.
    """

    def __init__(self) -> None:
        self.index_path = Path(settings.faiss_index_path)
        self.metadata_path = Path(settings.faiss_metadata_path)
        self._index: faiss.Index | None = None
        self._metadata: list[dict] = []
        self._embedding_dim: int = 384  # all-MiniLM-L6-v2 output dim

    def load(self) -> bool:
        """
        Loads the FAISS index and metadata from disk.

        Returns:
            True if loaded successfully, False if index doesn't exist.
        """
        if not self.index_path.exists():
            logger.warning(f"FAISS index not found at: {self.index_path}")
            return False

        self._index = faiss.read_index(str(self.index_path))
        with open(self.metadata_path, "r", encoding="utf-8") as f:
            self._metadata = json.load(f)

        logger.info(f"FAISS index loaded: {self._index.ntotal} vectors from {self.index_path}")
        return True

    def save(self, vectors: np.ndarray, metadata: list[dict]) -> None:
        """
        Saves vectors and metadata to disk.

        Args:
            vectors: numpy array of shape (n, embedding_dim)
            metadata: list of dicts with content, source, document_type, etc.
        """
        self.index_path.parent.mkdir(parents=True, exist_ok=True)

        # Build flat L2 index (cosine similarity via normalized vectors)
        dim = vectors.shape[1]
        index = faiss.IndexFlatIP(dim)  # Inner Product for normalized vectors = cosine similarity
        index.add(vectors.astype(np.float32))

        faiss.write_index(index, str(self.index_path))
        with open(self.metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        self._index = index
        self._metadata = metadata
        logger.info(f"FAISS index saved: {index.ntotal} vectors → {self.index_path}")

    def search(
        self, query_vector: np.ndarray, top_k: int = 5
    ) -> list[dict]:
        """
        Searches for the most similar chunks.

        Args:
            query_vector: Normalized embedding of shape (embedding_dim,)
            top_k: Number of results to return.

        Returns:
            List of dicts with content, source, document_type, similarity_score.
        """
        if self._index is None:
            logger.error("FAISS index is not loaded. Call load() first.")
            return []

        query = query_vector.reshape(1, -1).astype(np.float32)
        scores, indices = self._index.search(query, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0 or idx >= len(self._metadata):
                continue
            entry = dict(self._metadata[idx])
            entry["similarity_score"] = float(score)
            results.append(entry)

        return results

    def is_loaded(self) -> bool:
        return self._index is not None


# ── Singleton ─────────────────────────────────────────────────────────────────

_store: FAISSVectorStore | None = None


def get_vector_store() -> FAISSVectorStore:
    """Returns the singleton FAISS store, loading from disk on first call."""
    global _store
    if _store is None:
        _store = FAISSVectorStore()
        _store.load()
    return _store
