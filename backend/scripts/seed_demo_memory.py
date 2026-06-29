"""
ADIP — Demo Memory Seeder

Stages pre-approved decisions in organizational memory for the demo
so that the "memory learning loop" demo moment works immediately.

Run: python -m backend.scripts.seed_demo_memory

This creates memory records for Acme Corp and NovaSoft that will visibly
influence a second-run analysis, demonstrating adaptive decision intelligence.
"""

import sys
import os
import uuid
from datetime import datetime, timezone, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from backend.memory.database import SessionLocal, MemoryDB, init_db
import json


DEMO_MEMORIES = [
    # ── Acme Corp — 3 prior decisions ─────────────────────────────────────────
    {
        "customer_id": "acme_corp",
        "recommendation": "Conduct an onboarding training workshop to help the operations team understand core NimbusCRM workflows. Schedule a 2-hour hands-on session.",
        "decision": "approved",
        "outcome": "Training session completed. Some improvement in user logins but adoption still below 50%.",
        "health_score_before": 28,
        "health_score_after": 32,
        "signals": json.dumps(["low_adoption", "onboarding_friction"]),
        "timestamp": datetime.now(timezone.utc) - timedelta(days=14),
    },
    {
        "customer_id": "acme_corp",
        "recommendation": "Schedule a Business Value Review call with the Acme Corp operations leadership team to identify their core use cases and demonstrate ROI.",
        "decision": "approved",
        "outcome": "BVR conducted. Customer acknowledged value but flagged unresolved support tickets as blocking adoption.",
        "health_score_before": 32,
        "health_score_after": 32,
        "signals": json.dumps(["low_adoption", "churn_risk"]),
        "timestamp": datetime.now(timezone.utc) - timedelta(days=7),
    },
    {
        "customer_id": "acme_corp",
        "recommendation": "Escalate unresolved support ticket #ACME-0041 through standard engineering channels.",
        "decision": "rejected",
        "outcome": "CSM chose to escalate directly to VP of Engineering instead. Ticket still unresolved.",
        "health_score_before": 32,
        "health_score_after": 32,
        "signals": json.dumps(["churn_risk", "dissatisfaction"]),
        "timestamp": datetime.now(timezone.utc) - timedelta(days=3),
    },

    # ── NovaSoft — 2 prior decisions ──────────────────────────────────────────
    {
        "customer_id": "novasoft",
        "recommendation": "Send a formal introduction email from the VP of Customer Success to the new IT Director Marcus Vega, acknowledging the leadership change.",
        "decision": "approved",
        "outcome": "Email sent. Marcus Vega responded positively and agreed to a renewal review call.",
        "health_score_before": 58,
        "health_score_after": 61,
        "signals": json.dumps(["champion_resigned", "renewal_risk"]),
        "timestamp": datetime.now(timezone.utc) - timedelta(days=10),
    },
    {
        "customer_id": "novasoft",
        "recommendation": "Prepare a comprehensive ROI analysis report showing NovaSoft's productivity and pipeline improvements over the past 12 months.",
        "decision": "approved",
        "outcome": "ROI report delivered to Marcus Vega. Renewal call scheduled for June 22.",
        "health_score_before": 61,
        "health_score_after": 61,
        "signals": json.dumps(["champion_resigned", "renewal_risk"]),
        "timestamp": datetime.now(timezone.utc) - timedelta(days=5),
    },
]


def seed_demo_memory() -> int:
    """Insert pre-staged demo memory records into MemoryDB."""
    init_db()
    db = SessionLocal()
    count = 0
    try:
        for record in DEMO_MEMORIES:
            # Avoid duplicates — check by recommendation text + customer
            existing = db.query(MemoryDB).filter(
                MemoryDB.customer_id == record["customer_id"],
                MemoryDB.recommendation == record["recommendation"],
            ).first()

            if existing:
                print(f"  [SKIP] Already exists: {record['recommendation'][:55]}...")
                continue

            mem = MemoryDB(
                memory_id=str(uuid.uuid4()),
                customer_id=record["customer_id"],
                recommendation=record["recommendation"],
                decision=record["decision"],
                outcome=record.get("outcome"),
                health_score_before=record.get("health_score_before"),
                health_score_after=record.get("health_score_after"),
                signals=record.get("signals"),
                timestamp=record["timestamp"],
            )
            db.add(mem)
            count += 1
            decision_icon = "OK" if record["decision"] == "approved" else "NO"
            print(f"  [{decision_icon}] {record['customer_id']:12} | {record['decision']:9} | {record['recommendation'][:55]}...")

        db.commit()
    finally:
        db.close()

    return count


if __name__ == "__main__":
    print("Seeding demo memory records...\n")
    n = seed_demo_memory()
    print(f"\n[DONE] {n} new memory records added.")
    if n > 0:
        print("\nDemo memory loop is ready:")
        print("  Acme Corp  — training done, BVR done, ticket escalation rejected")
        print("  NovaSoft   — champion outreach done, ROI report delivered")
        print("\nWhen you run analysis again on these customers, the AI will")
        print("avoid repeating actions already taken and escalate appropriately.")
