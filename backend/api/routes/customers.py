"""
ADIP — Customer Routes

GET /customers         — list all customers
GET /customers/{id}    — get customer detail
GET /customers/{id}/history — customer history
GET /customers/{id}/memory  — customer memory timeline
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.memory.database import CustomerDB, get_db
from backend.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.get("/customers")
async def list_customers(db: Session = Depends(get_db)):
    """Returns all available customers."""
    customers = db.query(CustomerDB).all()
    return {
        "success": True,
        "data": [
            {
                "customer_id": c.customer_id,
                "company_name": c.company_name,
                "industry": c.industry,
                "health_score": c.health_score,
                "renewal_date": c.renewal_date,
                "active_users": c.active_users,
                "licensed_users": c.licensed_users,
                "contract_value": c.contract_value,
                "champion_status": c.champion_status,
                "months_active": c.months_active,
            }
            for c in customers
        ],
    }


@router.get("/customers/{customer_id}")
async def get_customer(customer_id: str, db: Session = Depends(get_db)):
    """Returns full customer profile."""
    customer = db.query(CustomerDB).filter(CustomerDB.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found.")
    return {
        "success": True,
        "data": {
            "customer_id": customer.customer_id,
            "company_name": customer.company_name,
            "industry": customer.industry,
            "health_score": customer.health_score,
            "renewal_date": customer.renewal_date,
            "active_users": customer.active_users,
            "licensed_users": customer.licensed_users,
            "contract_value": customer.contract_value,
            "champion_status": customer.champion_status,
            "months_active": customer.months_active,
        },
    }


@router.get("/customers/{customer_id}/history")
async def get_customer_history(customer_id: str, db: Session = Depends(get_db)):
    """Returns historical recommendations and outcomes for the customer."""
    customer = db.query(CustomerDB).filter(CustomerDB.customer_id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found.")

    sessions = customer.sessions
    history = []
    for session in sessions:
        for rec in session.recommendations:
            history.append({
                "session_id": session.session_id,
                "interaction_type": session.interaction_type,
                "action": rec.action,
                "priority": rec.priority,
                "confidence": rec.confidence,
                "decision": rec.decision,
                "created_at": rec.created_at.isoformat() if rec.created_at else None,
            })

    return {"success": True, "data": history}
