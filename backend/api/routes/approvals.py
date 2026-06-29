"""
ADIP — Approvals Routes

PATCH /recommendations/{recommendation_id} — approve / reject / override
"""
import uuid
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional

from backend.memory.database import (
    ApprovalDB, RecommendationDB, MemoryDB, SessionDB, get_db
)
from backend.utils.logger import get_logger
from backend.utils.helpers import utc_now_iso

logger = get_logger(__name__)
router = APIRouter()


class ApprovalRequest(BaseModel):
    decision: str  # approved | rejected | overridden
    custom_action: Optional[str] = None
    reviewer: Optional[str] = "CSM"


@router.patch("/recommendations/{recommendation_id}")
async def update_recommendation(
    recommendation_id: str,
    body: ApprovalRequest,
    db: Session = Depends(get_db),
):
    """
    Records a human decision (Approve / Reject / Override) on a recommendation.
    Approved decisions are persisted to organizational Memory.
    """
    valid_decisions = {"approved", "rejected", "overridden"}
    if body.decision not in valid_decisions:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid decision. Must be one of: {valid_decisions}",
        )

    rec = db.query(RecommendationDB).filter(
        RecommendationDB.recommendation_id == recommendation_id
    ).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found.")

    # Update recommendation decision
    rec.decision = body.decision
    if body.decision == "overridden" and body.custom_action:
        rec.override_text = body.custom_action

    # Record the approval
    approval = ApprovalDB(
        approval_id=f"appr_{uuid.uuid4().hex[:12]}",
        recommendation_id=recommendation_id,
        decision=body.decision,
        override_text=body.custom_action,
        reviewer=body.reviewer or "CSM",
    )
    db.add(approval)

    # Persist to organizational Memory
    session = db.query(SessionDB).filter(SessionDB.session_id == rec.session_id).first()
    if session:
        memory_entry = MemoryDB(
            memory_id=f"mem_{uuid.uuid4().hex[:12]}",
            customer_id=session.customer_id,
            recommendation=body.custom_action if body.decision == "overridden" else rec.action,
            decision=body.decision,
            outcome=None,  # Outcome recorded later
            health_score_before=None,
            health_score_after=None,
            signals=None,
        )
        db.add(memory_entry)
        logger.info(f"Memory record created for customer: {session.customer_id}")

    db.commit()
    logger.info(f"Decision '{body.decision}' recorded for recommendation: {recommendation_id}")

    return {
        "success": True,
        "data": {
            "recommendation_id": recommendation_id,
            "decision": body.decision,
            "message": f"Decision '{body.decision}' recorded and stored in organizational memory.",
        },
    }
