"""
ADIP — Memory Routes

GET /customers/{customer_id}/memory — organizational memory timeline
"""
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.memory.database import MemoryDB, CustomerDB, get_db
from backend.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/customers/{customer_id}/memory")
async def get_customer_memory(customer_id: str, db: Session = Depends(get_db)):
    """Returns organizational memory timeline for a customer."""
    customer = db.query(CustomerDB).filter(CustomerDB.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found.")

    records = (
        db.query(MemoryDB)
        .filter(MemoryDB.customer_id == customer_id)
        .order_by(MemoryDB.timestamp.desc())
        .limit(20)
        .all()
    )

    def _parse_signals(val):
        if not val:
            return []
        try:
            return json.loads(val)
        except Exception:
            return []

    return {
        "success": True,
        "data": [
            {
                "memory_id": r.memory_id,
                "customer_id": r.customer_id,
                "recommendation": r.recommendation,
                "decision": r.decision,
                "outcome": r.outcome,
                "health_score_before": r.health_score_before,
                "health_score_after": r.health_score_after,
                "signals": _parse_signals(r.signals),
                "timestamp": r.timestamp.isoformat() if r.timestamp else None,
            }
            for r in records
        ],
    }
