"""
ADIP — Agent Registry

The registry manages all available agents.
The Planner queries the registry — it never imports agents directly.
This enables extensibility: new agents are added without changing the Planner.
"""
from __future__ import annotations

from typing import Optional, Type

from backend.agents.base_agent import BaseAgent
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class AgentRegistry:
    """
    Singleton registry for all platform agents.

    Usage:
        registry = AgentRegistry()
        registry.register(RiskAgent)
        agent = registry.get_by_capability("assess_risk")
    """

    def __init__(self) -> None:
        self._agents: dict[str, Type[BaseAgent]] = {}  # name → class

    def register(self, agent_class: Type[BaseAgent]) -> None:
        """
        Registers an agent class by name.

        Args:
            agent_class: A subclass of BaseAgent.
        """
        if not hasattr(agent_class, "name") or not agent_class.name:
            raise ValueError(f"Agent class {agent_class} must define a 'name' class variable.")
        self._agents[agent_class.name] = agent_class
        logger.info(f"Registered agent: {agent_class.name} (capabilities: {agent_class.capabilities})")

    def get_by_name(self, name: str) -> Optional[BaseAgent]:
        """Returns an instantiated agent by name, or None if not found."""
        cls = self._agents.get(name)
        if cls is None:
            logger.warning(f"Agent '{name}' not found in registry.")
            return None
        return cls()

    def get_by_capability(self, capability: str) -> Optional[BaseAgent]:
        """Returns the first agent that supports the given capability."""
        for cls in self._agents.values():
            if capability in cls.capabilities:
                return cls()
        logger.warning(f"No agent found for capability: '{capability}'")
        return None

    def get_all_capabilities(self) -> dict[str, list[str]]:
        """Returns a mapping of agent_name → capabilities for the Planner."""
        return {name: cls.capabilities for name, cls in self._agents.items()}

    def list_agents(self) -> list[dict]:
        """Returns metadata for all registered agents."""
        return [cls().get_metadata() for cls in self._agents.values()]

    def get_all_names(self) -> list[str]:
        """Returns all registered agent names."""
        return list(self._agents.keys())


# ── Global registry instance ───────────────────────────────────────────────

_registry: Optional[AgentRegistry] = None


def get_registry() -> AgentRegistry:
    """
    Returns the global singleton agent registry.
    Registers all agents on first call.
    """
    global _registry
    if _registry is None:
        _registry = AgentRegistry()
        _register_all_agents(_registry)
    return _registry


def _register_all_agents(registry: AgentRegistry) -> None:
    """
    Registers all platform agents.
    Add new agents here — no other file needs to change.
    """
    from backend.agents.context_agent import ContextAgent
    from backend.agents.retrieval_agent import RetrievalAgent
    from backend.agents.risk_agent import RiskAgent
    from backend.agents.opportunity_agent import OpportunityAgent
    from backend.agents.renewal_agent import RenewalAgent
    from backend.agents.recommendation_agent import RecommendationAgent

    registry.register(ContextAgent)
    registry.register(RetrievalAgent)
    registry.register(RiskAgent)
    registry.register(OpportunityAgent)
    registry.register(RenewalAgent)
    registry.register(RecommendationAgent)
    logger.info(f"All agents registered. Total: {len(registry.get_all_names())}")
