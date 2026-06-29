"""
ADIP — Customer Seed Data Script

Seeds the SQLite database with 4 mock enterprise customers for NimbusCRM.
Run this once before starting the backend:
    python -m backend.scripts.seed_customers
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from backend.memory.database import CustomerDB, init_db, SessionLocal
from backend.utils.logger import get_logger

logger = get_logger(__name__)

CUSTOMERS = [
    {
        "customer_id": "acme_corp",
        "company_name": "Acme Corp",
        "industry": "Manufacturing",
        "contract_value": 48000.0,
        "renewal_date": "2026-07-16",  # ~20 days from now
        "months_active": 14,
        "health_score": 32,
        "active_users": 8,
        "licensed_users": 25,
        "champion_status": "at_risk",
    },
    {
        "customer_id": "techflow_inc",
        "company_name": "TechFlow Inc",
        "industry": "Technology",
        "contract_value": 120000.0,
        "renewal_date": "2026-11-15",
        "months_active": 22,
        "health_score": 87,
        "active_users": 142,
        "licensed_users": 150,
        "champion_status": "strong",
    },
    {
        "customer_id": "buildify",
        "company_name": "Buildify",
        "industry": "Construction",
        "contract_value": 36000.0,
        "renewal_date": "2026-12-01",
        "months_active": 3,
        "health_score": 55,
        "active_users": 12,
        "licensed_users": 30,
        "champion_status": "stable",
    },
    {
        "customer_id": "novasoft",
        "company_name": "NovaSoft",
        "industry": "Software",
        "contract_value": 95000.0,
        "renewal_date": "2026-07-30",  # ~34 days from now
        "months_active": 18,
        "health_score": 61,
        "active_users": 67,
        "licensed_users": 80,
        "champion_status": "resigned",
    },
]


def seed_customers() -> None:
    """Seeds the database with mock customers. Skips if already exists."""
    init_db()
    db = SessionLocal()
    try:
        added = 0
        for data in CUSTOMERS:
            existing = db.query(CustomerDB).filter(
                CustomerDB.customer_id == data["customer_id"]
            ).first()
            if existing:
                logger.info(f"Customer already exists, skipping: {data['customer_id']}")
                continue
            customer = CustomerDB(**data)
            db.add(customer)
            added += 1
        db.commit()
        logger.info(f"Seeded {added} customers successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    seed_customers()
    print("[OK] Customer data seeded.")
