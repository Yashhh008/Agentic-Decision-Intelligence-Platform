"""
ADIP — Planner Routes

GET /sessions/{session_id}/planner — returns planner decision for a session
"""
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.memory.database import PlannerLogDB, get_db
from backend.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/sessions/{session_id}/planner")
async def get_planner_decision(session_id: str, db: Session = Depends(get_db)):
    """Returns the planner decision for a given session."""
    log = (
        db.query(PlannerLogDB)
        .filter(PlannerLogDB.session_id == session_id)
        .order_by(PlannerLogDB.created_at.desc())
        .first()
    )
    if not log:
        raise HTTPException(status_code=404, detail="No planner decision found for this session.")

    def _parse(val):
        if val is None:
            return []
        try:
            return json.loads(val)
        except Exception:
            return val

    return {
        "success": True,
        "data": {
            "session_id": session_id,
            "detected_signals": _parse(log.detected_signals),
            "selected_capabilities": _parse(log.selected_capabilities),
            "selected_agents": _parse(log.selected_agents),
            "skipped_agents": _parse(log.skipped_agents),
            "planner_reasoning": log.planner_reasoning,
            "execution_mode": log.execution_mode,
            "execution_time_ms": log.execution_time_ms,
        },
    }
