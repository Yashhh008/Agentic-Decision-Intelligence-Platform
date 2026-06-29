"""
ADIP — Database Module

Defines all SQLAlchemy ORM models and initializes the SQLite database.
Embeddings are NEVER stored here — they live in the FAISS index.
"""
import json
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.orm import DeclarativeBase, Session, relationship, sessionmaker

from backend.config.settings import settings
from backend.utils.logger import get_logger

logger = get_logger(__name__)

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},  # SQLite only
    echo=settings.debug,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


# ── ORM Models ────────────────────────────────────────────────────────────────


class CustomerDB(Base):
    """Stores customer master data."""

    __tablename__ = "customers"

    customer_id = Column(String, primary_key=True, index=True)
    company_name = Column(String, nullable=False)
    industry = Column(String, nullable=False)
    contract_value = Column(Float, nullable=False)
    renewal_date = Column(String, nullable=False)
    months_active = Column(Integer, default=0)
    health_score = Column(Integer, default=50)
    active_users = Column(Integer, default=0)
    licensed_users = Column(Integer, default=0)
    champion_status = Column(String, default="stable")
    created_at = Column(DateTime, default=datetime.utcnow)

    sessions = relationship("SessionDB", back_populates="customer")
    memory_records = relationship("MemoryDB", back_populates="customer")


class SessionDB(Base):
    """Represents a single AI analysis workflow."""

    __tablename__ = "sessions"

    session_id = Column(String, primary_key=True, index=True)
    customer_id = Column(String, ForeignKey("customers.customer_id"), nullable=False)
    interaction_type = Column(String, nullable=False)
    interaction_text = Column(Text, nullable=False)
    planner_summary = Column(Text, nullable=True)
    status = Column(String, default="created")  # created | running | completed | failed
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("CustomerDB", back_populates="sessions")
    recommendations = relationship("RecommendationDB", back_populates="session")
    planner_logs = relationship("PlannerLogDB", back_populates="session")


class RecommendationDB(Base):
    """Stores recommendations generated during a session."""

    __tablename__ = "recommendations"

    recommendation_id = Column(String, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.session_id"), nullable=False)
    action = Column(Text, nullable=False)
    priority = Column(String, nullable=False)  # critical | high | medium | low
    reasoning = Column(Text, nullable=True)
    confidence = Column(Float, default=0.0)
    evidence_source = Column(Text, nullable=True)  # JSON string of sources
    business_rule = Column(Text, nullable=True)
    decision = Column(String, nullable=True)  # approved | rejected | overridden | pending
    override_text = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("SessionDB", back_populates="recommendations")
    approval = relationship("ApprovalDB", back_populates="recommendation", uselist=False)


class ApprovalDB(Base):
    """Stores human decisions on recommendations."""

    __tablename__ = "approvals"

    approval_id = Column(String, primary_key=True, index=True)
    recommendation_id = Column(
        String, ForeignKey("recommendations.recommendation_id"), nullable=False
    )
    decision = Column(String, nullable=False)  # approved | rejected | overridden
    override_text = Column(Text, nullable=True)
    reviewer = Column(String, default="CSM")
    timestamp = Column(DateTime, default=datetime.utcnow)

    recommendation = relationship("RecommendationDB", back_populates="approval")


class MemoryDB(Base):
    """
    Represents organizational learning.
    Each record stores a previous decision that may influence future recommendations.
    """

    __tablename__ = "memory"

    memory_id = Column(String, primary_key=True, index=True)
    customer_id = Column(String, ForeignKey("customers.customer_id"), nullable=False)
    recommendation = Column(Text, nullable=False)
    decision = Column(String, nullable=False)
    outcome = Column(Text, nullable=True)
    health_score_before = Column(Integer, nullable=True)
    health_score_after = Column(Integer, nullable=True)
    signals = Column(Text, nullable=True)  # JSON string of detected signals
    timestamp = Column(DateTime, default=datetime.utcnow)

    customer = relationship("CustomerDB", back_populates="memory_records")


class PlannerLogDB(Base):
    """Stores planner reasoning for transparency and the Planner Decision Panel."""

    __tablename__ = "planner_logs"

    planner_log_id = Column(String, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.session_id"), nullable=False)
    detected_signals = Column(Text, nullable=True)   # JSON string
    selected_capabilities = Column(Text, nullable=True)  # JSON string
    selected_agents = Column(Text, nullable=True)    # JSON string
    skipped_agents = Column(Text, nullable=True)     # JSON string
    planner_reasoning = Column(Text, nullable=True)
    execution_mode = Column(String, default="sequential")
    execution_time_ms = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("SessionDB", back_populates="planner_logs")


class AnalyticsDB(Base):
    """Stores lightweight operational metrics."""

    __tablename__ = "analytics"

    analytics_id = Column(Integer, primary_key=True, autoincrement=True)
    recommendation_count = Column(Integer, default=0)
    approval_count = Column(Integer, default=0)
    rejection_count = Column(Integer, default=0)
    override_count = Column(Integer, default=0)
    average_confidence = Column(Float, default=0.0)
    average_execution_time_ms = Column(Float, default=0.0)
    agents_executed = Column(Integer, default=0)
    recorded_at = Column(DateTime, default=datetime.utcnow)


# ── DB Lifecycle ──────────────────────────────────────────────────────────────


def init_db() -> None:
    """Creates all tables if they do not exist."""
    Base.metadata.create_all(bind=engine)
    logger.info("All database tables ensured.")


def get_db():
    """
    FastAPI dependency that yields a database session.

    Usage:
        db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
