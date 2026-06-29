"""
ADIP — Context Agent (Perception Layer)

Converts raw customer interaction text into structured business signals.
This is the first agent to execute in every analysis.
"""
from __future__ import annotations

from pathlib import Path

from backend.agents.base_agent import BaseAgent
from backend.core.shared_state import ADIPState, AgentResult
from backend.services.gemini_service import GeminiService
from backend.utils.logger import get_logger

logger = get_logger(__name__)

PROMPT_PATH = Path(__file__).parent.parent / "prompts" / "context_agent.txt"


class ContextAgent(BaseAgent):
    name = "ContextAgent"
    description = "Extracts structured business signals from raw customer interaction text."
    category = "perception"
    capabilities = ["extract_context", "detect_signals"]
    priority = 10  # Runs first

    def __init__(self) -> None:
        super().__init__()
        self.gemini = GeminiService()
        self._prompt_template = PROMPT_PATH.read_text(encoding="utf-8")

    def validate_input(self, state: ADIPState) -> None:
        if not state.interaction_text:
            raise ValueError("ContextAgent requires interaction_text to be set.")

    async def execute(self, state: ADIPState) -> AgentResult:
        """Extracts signals, intent, and entities from interaction text."""
        customer = state.customer

        prompt = self._prompt_template.format(
            company_name=customer.company_name if customer else "Unknown",
            health_score=customer.health_score if customer else "N/A",
            renewal_date=customer.renewal_date if customer else "N/A",
            active_users=customer.active_users if customer else 0,
            licensed_users=customer.licensed_users if customer else 0,
            champion_status=customer.champion_status if customer else "unknown",
            industry=customer.industry if customer else "unknown",
            interaction_type=state.interaction_type,
            interaction_text=state.interaction_text,
        )

        fallback = {
            "detected_signals": ["churn_risk"],
            "customer_intent": "Customer interaction requires review",
            "priority_level": "medium",
            "extracted_entities": {"mentioned_features": [], "mentioned_issues": [], "key_quotes": []},
            "summary": "Unable to extract context automatically.",
        }

        result = await self.gemini.generate_json(prompt, fallback=fallback)

        # Update shared state with extracted context
        state.detected_signals = result.get("detected_signals", [])
        state.customer_intent = result.get("customer_intent", "")
        state.priority_level = result.get("priority_level", "medium")
        state.extracted_entities = result.get("extracted_entities", {})

        signals_str = ", ".join(state.detected_signals) or "none"
        self.logger.info(f"Context extracted — signals: {signals_str}")

        return AgentResult(
            agent_name=self.name,
            status="success",
            confidence=0.85 if state.detected_signals else 0.5,
            reasoning=result.get("summary", ""),
            evidence=[state.interaction_text[:200]],
            metadata={"entities": result.get("extracted_entities", {})},
        )
