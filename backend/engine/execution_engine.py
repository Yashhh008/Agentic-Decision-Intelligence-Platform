"""
ADIP — Execution Engine

Executes the Planner's ExecutionPlan by running selected agents.
Contains NO business logic — only coordination.

Supports:
- Sequential execution
- Parallel execution for independent reasoning agents
"""
from __future__ import annotations

import asyncio
import time

from backend.core.agent_registry import get_registry
from backend.core.shared_state import ADIPState, ExecutionPlan
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class ExecutionEngine:
    """
    Reads an ExecutionPlan and executes agents accordingly.

    Agents are resolved from the registry — never imported directly.
    Shared state is updated after each agent completes.
    """

    async def execute(self, plan: ExecutionPlan, state: ADIPState) -> ADIPState:
        """
        Executes the plan, running agents in the specified order.

        Retrieval runs first (sequential prerequisite).
        Reasoning agents run in parallel if parallel_groups is populated.
        Recommendation Agent always runs last.

        Args:
            plan: ExecutionPlan from the Planner.
            state: Shared ADIPState to read from and write to.

        Returns:
            Updated ADIPState.
        """
        registry = get_registry()

        logger.info(
            f"Execution Engine starting — mode: {plan.execution_mode}, "
            f"agents: {plan.execution_order}"
        )

        if plan.execution_mode == "parallel" and plan.parallel_groups:
            state = await self._execute_parallel(plan, state, registry)
        else:
            state = await self._execute_sequential(plan, state, registry)

        return state

    # ── Sequential ────────────────────────────────────────────────────────

    async def _execute_sequential(
        self, plan: ExecutionPlan, state: ADIPState, registry
    ) -> ADIPState:
        """Executes agents one at a time in execution_order."""
        for agent_name in plan.execution_order:
            if agent_name == "ContextAgent":
                continue  # Context already extracted before planning
            state = await self._run_agent(agent_name, state, registry)
        return state

    # ── Parallel ──────────────────────────────────────────────────────────

    async def _execute_parallel(
        self, plan: ExecutionPlan, state: ADIPState, registry
    ) -> ADIPState:
        """
        Executes retrieval first, then reasoning agents in parallel,
        then recommendation agent last.
        """
        # Step 1: Always run retrieval first
        if "RetrievalAgent" in plan.execution_order:
            state = await self._run_agent("RetrievalAgent", state, registry)

        # Step 2: Run parallel reasoning agents concurrently
        for group in plan.parallel_groups:
            tasks = [
                self._run_agent(agent_name, state, registry)
                for agent_name in group
                if agent_name in plan.execution_order
            ]
            if tasks:
                logger.info(f"Running parallel group: {group}")
                results = await asyncio.gather(*tasks, return_exceptions=True)
                # Merge results back into state
                for result in results:
                    if isinstance(result, ADIPState):
                        state.agent_results.update(result.agent_results)
                    elif isinstance(result, Exception):
                        logger.error(f"Parallel agent failed: {result}")
                        state.errors.append(str(result))

        # Step 3: Run Recommendation Agent last
        if "RecommendationAgent" in plan.execution_order:
            state = await self._run_agent("RecommendationAgent", state, registry)

        return state

    # ── Agent runner ──────────────────────────────────────────────────────

    async def _run_agent(
        self, agent_name: str, state: ADIPState, registry
    ) -> ADIPState:
        """Resolves an agent from the registry, runs it, and updates state."""
        agent = registry.get_by_name(agent_name)
        if agent is None:
            logger.warning(f"Agent '{agent_name}' not found — skipping.")
            return state

        start = time.time()
        try:
            result = await agent.run(state)
            state.agent_results[agent_name] = result
            logger.info(
                f"Agent '{agent_name}' complete — "
                f"status={result.status}, confidence={result.confidence:.2f}, "
                f"time={result.execution_time_ms:.1f}ms"
            )
        except Exception as exc:
            logger.error(f"Agent '{agent_name}' raised exception: {exc}")
            state.errors.append(f"{agent_name}: {str(exc)}")

        return state
