"""
ADIP — Planner

The Planner is the heart of ADIP orchestration.
It reads the current state, queries the agent registry,
and generates a dynamic ExecutionPlan.

The Planner NEVER performs business analysis.
Its sole responsibility is orchestration.

Two-phase strategy:
  Phase 1 — Deterministic: map signals → required capabilities
  Phase 2 — LLM Reasoning: refine plan with customer context and memory
"""
from __future__ import annotations

import json
import time

from backend.core.agent_registry import get_registry
from backend.core.shared_state import ADIPState, ExecutionPlan
from backend.services.gemini_service import GeminiService
from backend.utils.helpers import extract_json_from_text
from backend.utils.logger import get_logger

logger = get_logger(__name__)

# Signal → capability mapping (deterministic Phase 1)
SIGNAL_CAPABILITY_MAP: dict[str, list[str]] = {
    "churn_risk": ["retrieve_context", "assess_risk"],
    "renewal_risk": ["retrieve_context", "analyze_renewal"],
    "upsell_opportunity": ["retrieve_context", "detect_opportunity"],
    "onboarding_friction": ["retrieve_context", "assess_risk"],
    "dissatisfaction": ["retrieve_context", "assess_risk"],
    "feature_confusion": ["retrieve_context", "assess_risk"],
    "cancellation_intent": ["retrieve_context", "assess_risk", "analyze_renewal"],
    "champion_resigned": ["retrieve_context", "analyze_renewal", "assess_risk"],
    "low_adoption": ["retrieve_context", "assess_risk", "detect_opportunity"],
    "expansion_interest": ["retrieve_context", "detect_opportunity"],
}

# Agents that can run in parallel (after retrieval completes)
PARALLELIZABLE_AGENTS = {"RiskAgent", "OpportunityAgent", "RenewalAgent"}


class Planner:
    """
    Generates dynamic ExecutionPlans based on customer signals,
    available capabilities, and organizational memory.
    """

    def __init__(self) -> None:
        self.gemini = GeminiService()

    async def plan(self, state: ADIPState) -> ExecutionPlan:
        """
        Generates an ExecutionPlan for the current state.

        Args:
            state: ADIPState with detected signals and customer context.

        Returns:
            ExecutionPlan directing the Execution Engine.
        """
        start = time.time()
        registry = get_registry()
        all_capabilities = registry.get_all_capabilities()

        # Phase 1 — Deterministic capability selection
        required_capabilities = self._determine_capabilities(state.detected_signals)
        selected_agents = self._map_capabilities_to_agents(required_capabilities, all_capabilities)
        skipped_agents = [
            name for name in registry.get_all_names()
            if name not in selected_agents and name not in ("ContextAgent",)
        ]

        # Phase 2 — LLM plan refinement
        reasoning = await self._llm_refine_plan(
            state, selected_agents, skipped_agents, required_capabilities
        )

        # Build execution order: Retrieval always first, then parallel reasoning agents, then Recommendation
        execution_order = self._build_execution_order(selected_agents)
        parallel_groups = self._build_parallel_groups(selected_agents)

        plan = ExecutionPlan(
            goal=self._determine_goal(state.detected_signals),
            selected_agents=selected_agents,
            execution_order=execution_order,
            parallel_groups=parallel_groups,
            skipped_agents=skipped_agents,
            planner_reasoning=reasoning,
            execution_mode="parallel" if len(parallel_groups) > 0 else "sequential",
        )

        elapsed = (time.time() - start) * 1000
        logger.info(
            f"Planner generated plan in {elapsed:.1f}ms — "
            f"agents: {selected_agents}, skipped: {skipped_agents}"
        )
        return plan

    # ── Phase 1 — Deterministic ────────────────────────────────────────────

    def _determine_capabilities(self, signals: list[str]) -> set[str]:
        """Maps detected signals to required capabilities."""
        capabilities: set[str] = {"retrieve_context"}  # always required
        for signal in signals:
            caps = SIGNAL_CAPABILITY_MAP.get(signal, [])
            capabilities.update(caps)
        # Always generate recommendations
        capabilities.add("generate_recommendation")
        return capabilities

    def _map_capabilities_to_agents(
        self, capabilities: set[str], all_caps: dict[str, list[str]]
    ) -> list[str]:
        """Maps capabilities to agent names."""
        selected: set[str] = set()
        for agent_name, agent_caps in all_caps.items():
            if any(cap in capabilities for cap in agent_caps):
                selected.add(agent_name)
        return sorted(selected)

    def _determine_goal(self, signals: list[str]) -> str:
        if not signals:
            return "General customer health analysis"
        primary = signals[0].replace("_", " ").title()
        return f"Address {primary} and provide next best actions"

    # ── Phase 2 — LLM Refinement ───────────────────────────────────────────

    async def _llm_refine_plan(
        self,
        state: ADIPState,
        selected_agents: list[str],
        skipped_agents: list[str],
        capabilities: set[str],
    ) -> str:
        """Uses Gemini to generate planner reasoning text."""
        customer = state.customer
        prompt = f"""You are the Planner for an enterprise AI platform.
Based on the analysis below, explain your execution plan in 2-3 sentences.

Customer: {customer.company_name if customer else "Unknown"}
Health Score: {customer.health_score if customer else "N/A"}
Renewal: {customer.renewal_date if customer else "N/A"}
Detected Signals: {', '.join(state.detected_signals) or 'none'}
Selected Agents: {', '.join(selected_agents)}
Skipped Agents: {', '.join(skipped_agents)}
Previous Memory Records: {len(state.memory_context)}

Respond with a concise explanation of WHY these agents were selected and what will be analyzed.
Keep it to 2-3 sentences. Do not use JSON."""

        try:
            signals_str = ", ".join(state.detected_signals) or "general analysis"
            skipped_str = ", ".join(skipped_agents) or "none"
            fallback_reasoning = (
                f"Detected signals [{signals_str}] triggered selection of "
                f"{', '.join(selected_agents)}. "
                f"Agents {skipped_str} were skipped as their capabilities "
                f"(risk assessment, opportunity detection, renewal analysis) "
                f"were not required by the current signal profile. "
                f"Retrieved knowledge will be cross-referenced to generate "
                f"evidence-backed recommendations."
            )
            reasoning = await self.gemini.generate_text(prompt, fallback=fallback_reasoning)
            return reasoning.strip()
        except Exception as exc:
            logger.warning(f"Planner LLM refinement failed: {exc}")
            signals_str = ", ".join(state.detected_signals) or "general analysis"
            return (
                f"Executing agents {', '.join(selected_agents)} based on detected signals: "
                f"{signals_str}. Skipped {', '.join(skipped_agents) or 'none'} as no relevant "
                f"signals were detected for those capabilities."
            )

    # ── Execution ordering ─────────────────────────────────────────────────

    def _build_execution_order(self, agents: list[str]) -> list[str]:
        """Builds ordered execution list: Retrieval → Reasoning → Recommendation."""
        order = []
        if "RetrievalAgent" in agents:
            order.append("RetrievalAgent")
        for agent in ["RiskAgent", "OpportunityAgent", "RenewalAgent"]:
            if agent in agents:
                order.append(agent)
        if "RecommendationAgent" in agents:
            order.append("RecommendationAgent")
        # Add any not yet included
        for agent in agents:
            if agent not in order and agent != "ContextAgent":
                order.append(agent)
        return order

    def _build_parallel_groups(self, agents: list[str]) -> list[list[str]]:
        """Identifies agents that can run in parallel (after retrieval)."""
        parallel = [a for a in agents if a in PARALLELIZABLE_AGENTS]
        if len(parallel) > 1:
            return [parallel]
        return []
