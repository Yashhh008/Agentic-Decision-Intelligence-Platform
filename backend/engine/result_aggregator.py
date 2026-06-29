"""
ADIP — Result Aggregator (Intelligence Fusion Engine)

Merges AgentResult objects from all executed agents into a
single UnifiedAnalysis consumed by the Recommendation Agent.
"""
from __future__ import annotations

from typing import Any

from backend.core.shared_state import ADIPState, AgentResult
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class UnifiedAnalysis:
    """Merged intelligence from all executed agents."""

    def __init__(self) -> None:
        self.evidence: list[str] = []
        self.risk_summary: str = ""
        self.opportunity_summary: str = ""
        self.renewal_summary: str = ""
        self.raw_recommendations: list[dict[str, Any]] = []
        self.agent_confidences: dict[str, float] = {}
        self.signals_confirmed: list[str] = []
        self.metadata: dict[str, Any] = {}

    def to_dict(self) -> dict[str, Any]:
        return {
            "evidence": self.evidence,
            "risk_summary": self.risk_summary,
            "opportunity_summary": self.opportunity_summary,
            "renewal_summary": self.renewal_summary,
            "raw_recommendations": self.raw_recommendations,
            "agent_confidences": self.agent_confidences,
            "signals_confirmed": self.signals_confirmed,
        }


class ResultAggregator:
    """
    Merges outputs from multiple agents into UnifiedAnalysis.

    Responsibilities:
    - Merge evidence from all agents (deduplicated)
    - Extract domain summaries (risk, opportunity, renewal)
    - Collect raw recommendations for the Recommendation Agent
    - Resolve confidence values
    """

    def aggregate(self, state: ADIPState) -> UnifiedAnalysis:
        """
        Combines all agent results from state into a unified analysis.

        Args:
            state: ADIPState containing agent_results dict.

        Returns:
            UnifiedAnalysis with merged intelligence.
        """
        unified = UnifiedAnalysis()
        seen_evidence: set[str] = set()

        for agent_name, result in state.agent_results.items():
            if result.status == "failed":
                logger.warning(f"Aggregator skipping failed agent: {agent_name}")
                continue

            # Merge evidence (deduplicate)
            for ev in result.evidence:
                if ev and ev not in seen_evidence:
                    unified.evidence.append(ev)
                    seen_evidence.add(ev)

            # Extract domain summaries
            if agent_name == "RiskAgent":
                unified.risk_summary = result.reasoning
            elif agent_name == "OpportunityAgent":
                unified.opportunity_summary = result.reasoning
            elif agent_name == "RenewalAgent":
                unified.renewal_summary = result.reasoning

            # Collect raw recommendations
            for rec in result.recommendations:
                if rec not in unified.raw_recommendations:
                    unified.raw_recommendations.append(rec)

            # Track per-agent confidence
            unified.agent_confidences[agent_name] = result.confidence

        # Add retrieved chunk sources as evidence
        for chunk in state.retrieved_chunks:
            source_ref = f"[{chunk.document_type}] {chunk.source}"
            if source_ref not in seen_evidence:
                unified.evidence.append(source_ref)
                seen_evidence.add(source_ref)

        unified.signals_confirmed = state.detected_signals
        logger.info(
            f"Aggregation complete — {len(unified.evidence)} evidence items, "
            f"{len(unified.raw_recommendations)} raw recommendations"
        )
        return unified
