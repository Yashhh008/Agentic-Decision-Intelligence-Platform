"""
ADIP — Knowledge Routes

GET /sessions/{session_id}/knowledge — retrieved enterprise knowledge chunks
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.memory.database import SessionDB, get_db
from backend.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/sessions/{session_id}/knowledge")
async def get_session_knowledge(session_id: str, db: Session = Depends(get_db)):
    """
    Returns retrieved knowledge chunks for a session.
    These are stored in the session's planner_summary JSON blob.
    """
    import json

    session = db.query(SessionDB).filter(SessionDB.session_id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    if session.status not in ("completed",):
        return {"success": True, "data": {"chunks": [], "status": session.status}}

    # Knowledge chunks are stored serialized in planner_summary
    try:
        summary = json.loads(session.planner_summary or "{}")
        chunks = summary.get("retrieved_chunks", [])
    except Exception:
        chunks = []

    return {"success": True, "data": {"chunks": chunks}}
