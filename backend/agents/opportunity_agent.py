"""
ADIP — Opportunity Agent (Reasoning Layer)

Identifies upsell and expansion opportunities based on
customer behavior, signals, and retrieved enterprise knowledge.
"""
from __future__ import annotations

from pathlib import Path

from backend.agents.base_agent import BaseAgent
from backend.core.shared_state import ADIPState, AgentResult
from backend.services.gemini_service import GeminiService

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "opportunity_agent.txt"


class OpportunityAgent(BaseAgent):
    name = "OpportunityAgent"
    description = "Identifies upsell and expansion opportunities."
    category = "reasoning"
    capabilities = ["detect_opportunity"]
    priority = 35

    def __init__(self) -> None:
        super().__init__()
        self.gemini = GeminiService()
        self._prompt_template = PROMPT_PATH.read_text(encoding="utf-8")

    async def execute(self, state: ADIPState) -> AgentResult:
        customer = state.customer
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
            active_users=customer.active_users,
            licensed_users=customer.licensed_users,
            contract_value=customer.contract_value,
            industry=customer.industry,
            detected_signals=", ".join(state.detected_signals) or "none",
            retrieved_context=retrieved_context,
            memory_context=memory_context,
        )

        fallback = {
            "opportunity_detected": False,
            "opportunity_type": "none",
            "estimated_value_increase": "0%",
            "key_indicators": [],
            "reasoning": "No clear expansion opportunity identified.",
            "confidence_inputs": {"signal_strength": 0.3, "evidence_quality": 0.3},
            "recommended_actions": [],
        }

        result = await self.gemini.generate_json(prompt, fallback=fallback)
        ci = result.get("confidence_inputs", {})
        confidence = (ci.get("signal_strength", 0.3) + ci.get("evidence_quality", 0.3)) / 2

        self.logger.info(
            f"Opportunity detected: {result.get('opportunity_detected')} | "
            f"type: {result.get('opportunity_type')}"
        )

        return AgentResult(
            agent_name=self.name,
            status="success",
            confidence=confidence if result.get("opportunity_detected") else 0.2,
            reasoning=result.get("reasoning", ""),
            evidence=result.get("key_indicators", []),
            recommendations=result.get("recommended_actions", []),
            metadata={
                "opportunity_detected": result.get("opportunity_detected"),
                "opportunity_type": result.get("opportunity_type"),
                "estimated_value_increase": result.get("estimated_value_increase"),
            },
        )
