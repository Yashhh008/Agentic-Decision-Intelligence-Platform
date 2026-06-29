"""
ADIP — Analytics Routes

GET /analytics/dashboard — platform-wide operational metrics
"""
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.memory.database import (
    RecommendationDB, ApprovalDB, CustomerDB, MemoryDB, get_db
)
from backend.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/analytics/dashboard")
async def get_dashboard_analytics(db: Session = Depends(get_db)):
    """Returns platform-wide operational metrics for the Platform Insights dashboard."""
    total_customers = db.query(func.count(CustomerDB.customer_id)).scalar() or 0
    avg_health = db.query(func.avg(CustomerDB.health_score)).scalar() or 0

    total_recs = db.query(func.count(RecommendationDB.recommendation_id)).scalar() or 0
    avg_confidence = db.query(func.avg(RecommendationDB.confidence)).scalar() or 0

    approvals = db.query(ApprovalDB).all()
    total_decisions = len(approvals)
    approved = sum(1 for a in approvals if a.decision == "approved")
    rejected = sum(1 for a in approvals if a.decision == "rejected")
    overridden = sum(1 for a in approvals if a.decision == "overridden")
    approval_rate = round((approved / total_decisions * 100), 1) if total_decisions > 0 else 0

    memory_count = db.query(func.count(MemoryDB.memory_id)).scalar() or 0

    return {
        "success": True,
        "data": {
            "total_customers": total_customers,
            "average_health_score": round(avg_health, 1),
            "total_recommendations": total_recs,
            "average_confidence": round((avg_confidence or 0) * 100, 1),
            "total_decisions": total_decisions,
            "approved_count": approved,
            "rejected_count": rejected,
            "overridden_count": overridden,
            "approval_rate": approval_rate,
            "memory_records": memory_count,
        },
    }
