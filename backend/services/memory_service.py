"""
ADIP — Memory Service

Retrieves and stores organizational memory.
Memory is NOT conversation history — it is organizational learning.

The Planner retrieves memory BEFORE planning.
Human decisions are persisted to memory AFTER approval.
"""
from __future__ import annotations

from sqlalchemy.orm import Session

from backend.memory.database import MemoryDB
from backend.config.settings import settings
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class MemoryService:
    """
    Manages organizational memory retrieval and storage.

    Memory records include: recommendation, decision, outcome, health scores.
    The Planner uses the last N records to improve plan quality.
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    def retrieve_for_customer(self, customer_id: str) -> list[dict]:
        """
        Retrieves recent memory records for a customer.

        Args:
            customer_id: The customer to look up.

        Returns:
            List of memory record dicts, newest first.
        """
        records = (
            self.db.query(MemoryDB)
            .filter(MemoryDB.customer_id == customer_id)
            .order_by(MemoryDB.timestamp.desc())
            .limit(settings.memory_max_records)
            .all()
        )

        memory_list = [
            {
                "memory_id": r.memory_id,
                "recommendation": r.recommendation,
                "decision": r.decision,
                "outcome": r.outcome,
                "health_score_before": r.health_score_before,
                "health_score_after": r.health_score_after,
                "timestamp": r.timestamp.isoformat() if r.timestamp else None,
            }
            for r in records
        ]

        logger.info(f"Retrieved {len(memory_list)} memory records for customer: {customer_id}")
        return memory_list

    def format_for_planner(self, memory_list: list[dict]) -> str:
        """
        Formats memory records as a readable string for LLM prompt injection.

        Args:
            memory_list: List of memory record dicts.

        Returns:
            Human-readable memory context string.
        """
        if not memory_list:
            return "No previous decisions on record."

        lines = ["Previous decisions for this customer:"]
        for i, m in enumerate(memory_list, 1):
            lines.append(
                f"{i}. Action: {m['recommendation']} | Decision: {m['decision']} | "
                f"Outcome: {m.get('outcome') or 'Not recorded yet'}"
            )
        return "\n".join(lines)
