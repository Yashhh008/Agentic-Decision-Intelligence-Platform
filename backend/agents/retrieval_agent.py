"""
ADIP — Retrieval Agent (Knowledge Layer)

Retrieves relevant enterprise knowledge chunks from the FAISS vector store.
Populates state.retrieved_chunks for use by all reasoning agents.
"""
from __future__ import annotations

from backend.agents.base_agent import BaseAgent
from backend.core.shared_state import ADIPState, AgentResult
from backend.services.retrieval_service import RetrievalService
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class RetrievalAgent(BaseAgent):
    name = "RetrievalAgent"
    description = "Retrieves relevant enterprise knowledge from the FAISS knowledge base."
    category = "perception"
    capabilities = ["retrieve_context"]
    priority = 20

    def __init__(self) -> None:
        super().__init__()
        self.retrieval_service = RetrievalService()

    async def execute(self, state: ADIPState) -> AgentResult:
        """
        Builds a retrieval query from signals + interaction text,
        then retrieves top-k knowledge chunks.
        """
        customer = state.customer
        signals_str = " ".join(state.detected_signals)

        # Build a rich query combining signals and interaction text
        query = (
            f"{signals_str} "
            f"{state.customer_intent} "
            f"{state.interaction_text[:300]}"
        ).strip()

        chunks = self.retrieval_service.retrieve(
            query=query,
            top_k=6,
            customer_id_filter=customer.customer_id if customer else None,
        )

        if not chunks:
            # Fallback: search without customer filter
            chunks = self.retrieval_service.retrieve(query=query, top_k=5)

        # Update shared state
        state.retrieved_chunks = chunks

        evidence = [f"[{c.document_type}] {c.source} (similarity: {c.similarity_score:.2f})"
                    for c in chunks]
        avg_similarity = sum(c.similarity_score for c in chunks) / len(chunks) if chunks else 0.0

        self.logger.info(f"Retrieved {len(chunks)} chunks, avg similarity: {avg_similarity:.2f}")

        return AgentResult(
            agent_name=self.name,
            status="success",
            confidence=min(avg_similarity, 1.0),
            reasoning=f"Retrieved {len(chunks)} relevant knowledge chunks for analysis.",
            evidence=evidence,
            metadata={"chunk_count": len(chunks), "avg_similarity": avg_similarity},
        )
