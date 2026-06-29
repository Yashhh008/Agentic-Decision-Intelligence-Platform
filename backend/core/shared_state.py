"""
ADIP — Shared State

ADIPState is the single communication medium between all agents.
Agents read from and write to this object exclusively.
Agents NEVER call each other directly.
"""
from __future__ import annotations

from typing import Any, Optional
from pydantic import BaseModel, Field


class CustomerContext(BaseModel):
    """Structured customer profile used throughout analysis."""
    customer_id: str
    company_name: str
    health_score: int
    renewal_date: str
    active_users: int
    licensed_users: int
    contract_value: float
    champion_status: str
    months_active: int
    industry: str


class RetrievedChunk(BaseModel):
    """A single retrieved knowledge chunk from FAISS."""
    content: str
    source: str
    document_type: str
    similarity_score: float
    chunk_id: str = ""


class AgentResult(BaseModel):
    """Standardized output from every agent."""
    agent_name: str
    status: str = "success"        # success | failed | skipped
    confidence: float = 0.0        # 0.0 – 1.0
    reasoning: str = ""
    evidence: list[str] = Field(default_factory=list)
    recommendations: list[dict[str, Any]] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    execution_time_ms: float = 0.0


class ExecutionPlan(BaseModel):
    """The Planner's output — drives the Execution Engine."""
    goal: str
    selected_agents: list[str] = Field(default_factory=list)
    execution_order: list[str] = Field(default_factory=list)
    parallel_groups: list[list[str]] = Field(default_factory=list)
    skipped_agents: list[str] = Field(default_factory=list)
    planner_reasoning: str = ""
    execution_mode: str = "sequential"  # sequential | parallel


class FinalRecommendation(BaseModel):
    """A single ranked recommendation presented to the human."""
    recommendation_id: str = ""
    action: str
    priority: str           # critical | high | medium | low
    confidence: float       # 0.0 – 1.0
    reasoning: str
    evidence_source: list[str] = Field(default_factory=list)
    business_rule: str = ""


class ADIPState(BaseModel):
    """
    Central shared state that flows through the entire analysis pipeline.

    Every component reads from and writes to this object.
    This is the ONLY way agents communicate.
    """

    # ── Session context ────────────────────────────────────────────────────
    session_id: str
    customer: Optional[CustomerContext] = None
    interaction_type: str = ""
    interaction_text: str = ""

    # ── Perception output ──────────────────────────────────────────────────
    detected_signals: list[str] = Field(default_factory=list)
    customer_intent: str = ""
    priority_level: str = "medium"
    extracted_entities: dict[str, Any] = Field(default_factory=dict)

    # ── Memory context (loaded before planning) ────────────────────────────
    memory_context: list[dict[str, Any]] = Field(default_factory=list)

    # ── Orchestration ──────────────────────────────────────────────────────
    execution_plan: Optional[ExecutionPlan] = None

    # ── Knowledge retrieval ────────────────────────────────────────────────
    retrieved_chunks: list[RetrievedChunk] = Field(default_factory=list)

    # ── Agent outputs ──────────────────────────────────────────────────────
    agent_results: dict[str, AgentResult] = Field(default_factory=dict)

    # ── Final outputs ──────────────────────────────────────────────────────
    recommendations: list[FinalRecommendation] = Field(default_factory=list)
    confidence_breakdown: dict[str, float] = Field(default_factory=dict)

    # ── Error tracking ─────────────────────────────────────────────────────
    errors: list[str] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True
