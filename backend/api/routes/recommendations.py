"""
ADIP — Recommendations Routes

GET /sessions/{session_id}/recommendations — list recommendations for session
GET /recommendations/{recommendation_id}   — get single recommendation detail
"""
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.memory.database import RecommendationDB, SessionDB, get_db
from backend.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/sessions/{session_id}/recommendations")
async def get_session_recommendations(session_id: str, db: Session = Depends(get_db)):
    """Returns ranked recommendations for a session."""
    session = db.query(SessionDB).filter(SessionDB.session_id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    recs = (
        db.query(RecommendationDB)
        .filter(RecommendationDB.session_id == session_id)
        .order_by(RecommendationDB.confidence.desc())
        .all()
    )

    def _parse_sources(val):
        if not val:
            return []
        try:
            return json.loads(val)
        except Exception:
            return [val]

    return {
        "success": True,
        "data": [
            {
                "recommendation_id": r.recommendation_id,
                "session_id": r.session_id,
                "action": r.action,
                "priority": r.priority,
                "confidence": r.confidence,
                "reasoning": r.reasoning,
                "evidence_source": _parse_sources(r.evidence_source),
                "business_rule": r.business_rule,
                "decision": r.decision or "pending",
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in recs
        ],
    }


@router.get("/recommendations/{recommendation_id}")
async def get_recommendation(recommendation_id: str, db: Session = Depends(get_db)):
    """Returns complete recommendation details."""
    rec = db.query(RecommendationDB).filter(
        RecommendationDB.recommendation_id == recommendation_id
    ).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Recommendation not found.")

    def _parse_sources(val):
        if not val:
            return []
        try:
            return json.loads(val)
        except Exception:
            return [val]

    return {
        "success": True,
        "data": {
            "recommendation_id": rec.recommendation_id,
            "session_id": rec.session_id,
            "action": rec.action,
            "priority": rec.priority,
            "confidence": rec.confidence,
            "reasoning": rec.reasoning,
            "evidence_source": _parse_sources(rec.evidence_source),
            "business_rule": rec.business_rule,
            "decision": rec.decision or "pending",
            "override_text": rec.override_text,
            "created_at": rec.created_at.isoformat() if rec.created_at else None,
        },
    }
