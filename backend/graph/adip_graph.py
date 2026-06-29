"""
ADIP — LangGraph Orchestration Graph

Wires together the full analysis pipeline using LangGraph.
This is the only place that orchestrates the full workflow end-to-end.

Flow:
    context_extraction → memory_retrieval → planning →
    execution → aggregation → persist_results
"""
from __future__ import annotations

import json
import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from backend.agents.context_agent import ContextAgent
from backend.core.agent_registry import get_registry
from backend.core.shared_state import ADIPState, CustomerContext
from backend.engine.execution_engine import ExecutionEngine
from backend.engine.planner import Planner
from backend.memory.database import (
    CustomerDB, PlannerLogDB, RecommendationDB, SessionDB,
)
from backend.services.memory_service import MemoryService
from backend.utils.logger import get_logger

logger = get_logger(__name__)


async def run_analysis(session_id: str, db: Session) -> None:
    """
    Full ADIP analysis pipeline for a session.

    Steps:
    1. Load session + customer from DB
    2. Extract context (signals, intent)
    3. Retrieve organizational memory
    4. Plan execution
    5. Execute agents
    6. Persist recommendations and planner log

    Args:
        session_id: The session to analyze.
        db: SQLAlchemy DB session.
    """
    # ── Step 1: Load Session & Customer ───────────────────────────────────
    session = db.query(SessionDB).filter(SessionDB.session_id == session_id).first()
    if not session:
        raise ValueError(f"Session not found: {session_id}")

    customer_db = db.query(CustomerDB).filter(CustomerDB.customer_id == session.customer_id).first()
    if not customer_db:
        raise ValueError(f"Customer not found: {session.customer_id}")

    customer_ctx = CustomerContext(
        customer_id=customer_db.customer_id,
        company_name=customer_db.company_name,
        health_score=customer_db.health_score,
        renewal_date=customer_db.renewal_date,
        active_users=customer_db.active_users,
        licensed_users=customer_db.licensed_users,
        contract_value=customer_db.contract_value,
        champion_status=customer_db.champion_status,
        months_active=customer_db.months_active,
        industry=customer_db.industry,
    )

    # ── Initialize Shared State ────────────────────────────────────────────
    state = ADIPState(
        session_id=session_id,
        customer=customer_ctx,
        interaction_type=session.interaction_type,
        interaction_text=session.interaction_text,
    )

    # ── Step 2: Context Extraction ─────────────────────────────────────────
    logger.info(f"[{session_id}] Step 1: Context extraction")
    context_agent = ContextAgent()
    context_result = await context_agent.run(state)
    state.agent_results["ContextAgent"] = context_result

    # ── Step 3: Memory Retrieval ───────────────────────────────────────────
    logger.info(f"[{session_id}] Step 2: Memory retrieval")
    memory_service = MemoryService(db)
    state.memory_context = memory_service.retrieve_for_customer(customer_ctx.customer_id)

    # ── Step 4: Planning ───────────────────────────────────────────────────
    logger.info(f"[{session_id}] Step 3: Planning")
    planner = Planner()
    execution_plan = await planner.plan(state)
    state.execution_plan = execution_plan

    # ── Step 5: Execution ──────────────────────────────────────────────────
    logger.info(f"[{session_id}] Step 4: Executing agents — {execution_plan.execution_order}")
    engine = ExecutionEngine()
    state = await engine.execute(execution_plan, state)

    # ── Step 6: Persist Results ────────────────────────────────────────────
    logger.info(f"[{session_id}] Step 5: Persisting results")

    # Save planner log
    planner_log = PlannerLogDB(
        planner_log_id=f"plan_{uuid.uuid4().hex[:12]}",
        session_id=session_id,
        detected_signals=json.dumps(state.detected_signals),
        selected_capabilities=json.dumps(
            list({cap for name in execution_plan.selected_agents 
                  for cap in get_registry().get_all_capabilities().get(name, [])})
        ),
        selected_agents=json.dumps(execution_plan.selected_agents),
        skipped_agents=json.dumps(execution_plan.skipped_agents),
        planner_reasoning=execution_plan.planner_reasoning,
        execution_mode=execution_plan.execution_mode,
    )
    db.add(planner_log)

    # Save recommendations
    for rec in state.recommendations:
        rec_db = RecommendationDB(
            recommendation_id=rec.recommendation_id or f"rec_{uuid.uuid4().hex[:10]}",
            session_id=session_id,
            action=rec.action,
            priority=rec.priority,
            reasoning=rec.reasoning,
            confidence=rec.confidence,
            evidence_source=json.dumps(rec.evidence_source),
            business_rule=rec.business_rule or "",
            decision="pending",
        )
        db.add(rec_db)

    # Update session planner_summary with retrieved chunks (for knowledge endpoint)
    session.planner_summary = json.dumps({
        "retrieved_chunks": [
            {
                "content": c.content,
                "source": c.source,
                "document_type": c.document_type,
                "similarity_score": c.similarity_score,
            }
            for c in state.retrieved_chunks
        ]
    })

    db.commit()
    logger.info(
        f"[{session_id}] Analysis complete — "
        f"{len(state.recommendations)} recommendations generated"
    )
