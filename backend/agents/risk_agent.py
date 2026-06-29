"""
ADIP — Risk Agent (Reasoning Layer)

Assesses churn and satisfaction risk using customer context,
retrieved knowledge, and organizational memory.
"""
from __future__ import annotations

from pathlib import Path

from backend.agents.base_agent import BaseAgent
from backend.core.shared_state import ADIPState, AgentResult
from backend.services.gemini_service import GeminiService
from backend.utils.logger import get_logger

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "risk_agent.txt"


class RiskAgent(BaseAgent):
    name = "RiskAgent"
    description = "Assesses churn and customer satisfaction risk."
    category = "reasoning"
    capabilities = ["assess_risk"]
    priority = 30

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
            renewal_date=customer.renewal_date,
            active_users=customer.active_users,
            licensed_users=customer.licensed_users,
            champion_status=customer.champion_status,
            contract_value=customer.contract_value,
            detected_signals=", ".join(state.detected_signals) or "none",
            retrieved_context=retrieved_context,
            memory_context=memory_context,
        )

        fallback = {
            "risk_level": "medium",
            "churn_probability": 0.5,
            "key_risk_factors": ["Insufficient data"],
            "reasoning": "Risk assessment could not be completed at this time.",
            "confidence_inputs": {"signal_strength": 0.3, "evidence_quality": 0.3},
            "recommended_actions": [],
        }

        result = await self.gemini.generate_json(prompt, fallback=fallback)
        self.logger.info(f"Risk level: {result.get('risk_level')} | churn_prob: {result.get('churn_probability')}")

        evidence = [factor for factor in result.get("key_risk_factors", [])]
        ci = result.get("confidence_inputs", {})
        confidence = (ci.get("signal_strength", 0.5) + ci.get("evidence_quality", 0.5)) / 2

        return AgentResult(
            agent_name=self.name,
            status="success",
            confidence=confidence,
            reasoning=result.get("reasoning", ""),
            evidence=evidence,
            recommendations=result.get("recommended_actions", []),
            metadata={
                "risk_level": result.get("risk_level"),
                "churn_probability": result.get("churn_probability"),
            },
        )
