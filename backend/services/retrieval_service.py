"""
ADIP — Retrieval Service

Combines EmbeddingService + FAISSVectorStore to provide
semantic enterprise knowledge retrieval.

Used by the RetrievalAgent.
"""
from __future__ import annotations

from backend.core.shared_state import RetrievedChunk
from backend.services.embedding_service import EmbeddingService
from backend.vectorstore.faiss_store import get_vector_store
from backend.config.settings import settings
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class RetrievalService:
    """
    Provides semantic search over the enterprise knowledge base.

    Workflow:
        Query text → embed → FAISS search → RetrievedChunk list
    """

    def __init__(self) -> None:
        self.embedder = EmbeddingService()
        self.store = get_vector_store()

    def retrieve(
        self,
        query: str,
        top_k: int | None = None,
        document_type_filter: str | None = None,
        customer_id_filter: str | None = None,
    ) -> list[RetrievedChunk]:
        """
        Performs semantic retrieval against the FAISS knowledge base.

        Args:
            query: Natural language search query.
            top_k: Number of chunks to return.
            document_type_filter: Optional filter by document type.
            customer_id_filter: Optional filter by customer ID.

        Returns:
            List of RetrievedChunk objects ranked by similarity.
        """
        if not self.store.is_loaded():
            logger.warning("Vector store not loaded — returning empty results.")
            return []

        k = top_k or settings.retrieval_top_k
        query_vector = self.embedder.embed(query)
        raw_results = self.store.search(query_vector, top_k=k * 2)  # Over-fetch for filtering

        chunks: list[RetrievedChunk] = []
        for result in raw_results:
            # Apply optional filters
            if document_type_filter and result.get("document_type") != document_type_filter:
                continue
            if customer_id_filter and result.get("customer_id") not in (customer_id_filter, None):
                continue

            chunks.append(RetrievedChunk(
                content=result.get("content", ""),
                source=result.get("source", "Unknown"),
                document_type=result.get("document_type", "unknown"),
                similarity_score=result.get("similarity_score", 0.0),
                chunk_id=result.get("chunk_id", ""),
            ))

            if len(chunks) >= k:
                break

        logger.info(f"Retrieved {len(chunks)} chunks for query: '{query[:60]}...'")
        return chunks
