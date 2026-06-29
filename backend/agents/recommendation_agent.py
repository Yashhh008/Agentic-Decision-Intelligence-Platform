"""
ADIP — Recommendation Agent (Decision Layer)

Synthesizes all agent intelligence into final ranked Next Best Actions.
Consumes UnifiedAnalysis, business rules, and memory.
"""
from __future__ import annotations

import uuid
from pathlib import Path

from backend.agents.base_agent import BaseAgent
from backend.core.shared_state import ADIPState, AgentResult, FinalRecommendation
from backend.engine.business_rules import BusinessRulesEngine
from backend.engine.confidence_engine import ConfidenceEngine
from backend.engine.result_aggregator import ResultAggregator
from backend.services.gemini_service import GeminiService
from backend.utils.logger import get_logger

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "recommendation_agent.txt"


class RecommendationAgent(BaseAgent):
    name = "RecommendationAgent"
    description = "Produces ranked, evidence-backed Next Best Actions from unified intelligence."
    category = "decision"
    capabilities = ["generate_recommendation"]
    priority = 90  # Always runs last

    def __init__(self) -> None:
        super().__init__()
        self.gemini = GeminiService()
        self.aggregator = ResultAggregator()
        self.rules_engine = BusinessRulesEngine()
        self.confidence_engine = ConfidenceEngine()
        self._prompt_template = PROMPT_PATH.read_text(encoding="utf-8")

    async def execute(self, state: ADIPState) -> AgentResult:
        """
        Merges all agent results, applies business rules, computes confidence,
        and generates final ranked recommendations.
        """
        customer = state.customer

        # Step 1: Aggregate all agent results
        unified = self.aggregator.aggregate(state)

        # Step 2: Evaluate business rules
        rule_results = self.rules_engine.evaluate(state)
        rules_summary = self.rules_engine.get_summary(rule_results)

        # Step 3: Build prompt
        retrieved_context = "\n".join(
            f"- [{c.document_type}] {c.source}: {c.content[:200]}"
            for c in state.retrieved_chunks[:5]
        ) or "No context retrieved."

        memory_context = "\n".join(
            f"- {m.get('recommendation', '')} → {m.get('decision', '')}"
            for m in state.memory_context
        ) or "No previous decisions."

        prompt = self._prompt_template.format(
            company_name=customer.company_name,
            health_score=customer.health_score,
            renewal_date=customer.renewal_date,
            detected_signals=", ".join(state.detected_signals) or "none",
            risk_summary=unified.risk_summary or "No risk analysis available.",
            opportunity_summary=unified.opportunity_summary or "No opportunity analysis available.",
            renewal_summary=unified.renewal_summary or "No renewal analysis available.",
            retrieved_context=retrieved_context,
            business_rules=rules_summary,
            memory_context=memory_context,
        )

        fallback = {
            "recommendations": [
                {
                    "action": "Schedule a detailed review call with the customer.",
                    "priority": "high",
                    "reasoning": "General customer health review recommended based on available signals.",
                    "evidence_source": [],
                    "business_rule": "",
                    "confidence_inputs": {"evidence_quality": 0.3, "signal_alignment": 0.4},
                }
            ]
        }

        llm_result = await self.gemini.generate_json(prompt, fallback=fallback)

        # Step 4: Compute deterministic confidence
        confidence_score = self.confidence_engine.compute(
            state=state,
            agent_results=list(state.agent_results.values()),
            rule_triggered_count=len(rule_results),
        )

        # Step 5: Apply priority overrides from business rules
        priority_override = None
        for rule in rule_results:
            if rule.priority_override == "critical":
                priority_override = "critical"
                break
            elif rule.priority_override == "high" and priority_override != "critical":
                priority_override = "high"

        # Step 6: Build FinalRecommendation objects
        final_recs: list[FinalRecommendation] = []
        for i, rec in enumerate(llm_result.get("recommendations", [])[:5]):
            ci = rec.get("confidence_inputs", {})
            rec_confidence = (
                ci.get("evidence_quality", 0.5) * 0.5 +
                ci.get("signal_alignment", 0.5) * 0.5
            )
            # Blend with overall confidence engine score
            blended = (rec_confidence * 0.4 + confidence_score.overall * 0.6)

            final_priority = rec.get("priority", "medium")
            if i == 0 and priority_override:
                final_priority = priority_override

            final_recs.append(FinalRecommendation(
                recommendation_id=f"rec_{uuid.uuid4().hex[:10]}",
                action=rec.get("action", ""),
                priority=final_priority,
                confidence=round(blended, 3),
                reasoning=rec.get("reasoning", ""),
                evidence_source=rec.get("evidence_source", []),
                business_rule=rec.get("business_rule", ""),
            ))

        # Step 7: Store in shared state
        state.recommendations = final_recs
        state.confidence_breakdown = confidence_score.breakdown

        self.logger.info(
            f"Generated {len(final_recs)} recommendations | "
            f"confidence: {confidence_score.as_percentage()}%"
        )

        return AgentResult(
            agent_name=self.name,
            status="success",
            confidence=confidence_score.overall,
            reasoning=f"Generated {len(final_recs)} evidence-backed recommendations.",
            evidence=unified.evidence[:5],
            recommendations=[r.model_dump() for r in final_recs],
            metadata={
                "confidence_breakdown": confidence_score.breakdown,
                "rules_triggered": len(rule_results),
            },
        )
