"""
ADIP — BaseAgent

Every agent in the platform must inherit this class.
This enforces a consistent interface across all capabilities.
"""
from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import ClassVar

from backend.core.shared_state import ADIPState, AgentResult
from backend.utils.logger import get_logger


class BaseAgent(ABC):
    """
    Abstract base class for all ADIP agents.

    Subclasses must implement:
        - name (str class variable)
        - description (str class variable)
        - version (str class variable)
        - category (str class variable)
        - capabilities (list[str] class variable)
        - execute(state) -> AgentResult
    """

    name: ClassVar[str]
    description: ClassVar[str]
    version: ClassVar[str] = "1.0.0"
    category: ClassVar[str]         # perception | reasoning | decision | memory
    capabilities: ClassVar[list[str]]
    priority: ClassVar[int] = 50    # 1 (high) → 100 (low) for ordering

    def __init__(self) -> None:
        self.logger = get_logger(self.__class__.__name__)

    # ── Public entry point ─────────────────────────────────────────────────

    async def run(self, state: ADIPState) -> AgentResult:
        """
        Full agent lifecycle:
        initialize → validate_input → execute → validate_output → cleanup

        Returns:
            AgentResult with timing metadata attached.
        """
        start = time.time()
        self.logger.info(f"[{self.name}] Starting execution")

        try:
            await self.initialize(state)
            self.validate_input(state)
            result = await self.execute(state)
            self.validate_output(result)
        except Exception as exc:
            self.logger.error(f"[{self.name}] Execution failed: {exc}")
            result = AgentResult(
                agent_name=self.name,
                status="failed",
                reasoning=str(exc),
            )
        finally:
            await self.cleanup()

        elapsed = (time.time() - start) * 1000
        result.execution_time_ms = elapsed
        self.logger.info(f"[{self.name}] Completed in {elapsed:.1f}ms | status={result.status}")
        return result

    # ── Lifecycle hooks (optional override) ───────────────────────────────

    async def initialize(self, state: ADIPState) -> None:
        """Called before execute(). Override for setup logic."""

    async def cleanup(self) -> None:
        """Called after execute(). Override for teardown logic."""

    def validate_input(self, state: ADIPState) -> None:
        """Validates preconditions. Override to add agent-specific checks."""
        if state.customer is None:
            raise ValueError(f"[{self.name}] Customer context is required but missing.")

    def validate_output(self, result: AgentResult) -> None:
        """Validates AgentResult structure after execution."""
        if not result.agent_name:
            raise ValueError(f"AgentResult.agent_name must be set.")

    # ── Abstract ──────────────────────────────────────────────────────────

    @abstractmethod
    async def execute(self, state: ADIPState) -> AgentResult:
        """
        Core agent logic. Must be implemented by every subclass.

        Args:
            state: The shared platform state.

        Returns:
            AgentResult with analysis outputs.
        """

    # ── Metadata ──────────────────────────────────────────────────────────

    def get_metadata(self) -> dict:
        """Returns agent metadata for the registry."""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "category": self.category,
            "capabilities": self.capabilities,
            "priority": self.priority,
        }
