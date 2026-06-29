"""
ADIP — Session Routes

POST /sessions                        — create session
GET  /sessions/{session_id}           — get session state
POST /sessions/{session_id}/analyze   — trigger full AI analysis
GET  /sessions/{session_id}/planner   — get planner decision
GET  /sessions/{session_id}/knowledge — get retrieved knowledge
GET  /sessions/{session_id}/recommendations — get recommendations
"""
import uuid
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.memory.database import SessionDB, CustomerDB, PlannerLogDB, RecommendationDB, get_db
from backend.utils.logger import get_logger
from backend.utils.helpers import utc_now_iso

logger = get_logger(__name__)
router = APIRouter()


class CreateSessionRequest(BaseModel):
    customer_id: str
    interaction_type: str  # meeting_transcript | crm_update | email | support_ticket
    interaction_text: str


@router.post("/sessions")
async def create_session(body: CreateSessionRequest, db: Session = Depends(get_db)):
    """Creates a new analysis session."""
    customer = db.query(CustomerDB).filter(CustomerDB.customer_id == body.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found.")

    session_id = f"sess_{uuid.uuid4().hex[:12]}"
    session = SessionDB(
        session_id=session_id,
        customer_id=body.customer_id,
        interaction_type=body.interaction_type,
        interaction_text=body.interaction_text,
        status="created",
    )
    db.add(session)
    db.commit()
    logger.info(f"Session created: {session_id} for customer: {body.customer_id}")
    return {"success": True, "data": {"session_id": session_id, "status": "created"}}


@router.get("/sessions/{session_id}")
async def get_session(session_id: str, db: Session = Depends(get_db)):
    """Returns current session state."""
    session = db.query(SessionDB).filter(SessionDB.session_id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    return {
        "success": True,
        "data": {
            "session_id": session.session_id,
            "customer_id": session.customer_id,
            "interaction_type": session.interaction_type,
            "status": session.status,
            "planner_summary": session.planner_summary,
            "created_at": session.created_at.isoformat() if session.created_at else None,
        },
    }


@router.post("/sessions/{session_id}/analyze")
async def analyze_session(session_id: str, db: Session = Depends(get_db)):
    """
    Triggers the full AI analysis workflow:
    Context Extraction → Planner → Retrieval → Agents → Recommendations
    """
    from backend.graph.adip_graph import run_analysis

    session = db.query(SessionDB).filter(SessionDB.session_id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    if session.status == "running":
        raise HTTPException(status_code=409, detail="Analysis already running.")

    session.status = "running"
    db.commit()

    try:
        await run_analysis(session_id=session_id, db=db)
        session.status = "completed"
        db.commit()
        logger.info(f"Analysis completed for session: {session_id}")
        return {"success": True, "data": {"status": "completed", "session_id": session_id}}
    except Exception as exc:
        session.status = "failed"
        db.commit()
        logger.error(f"Analysis failed for session {session_id}: {exc}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(exc)}")
