"""
ADIP — Business Rules Engine

Deterministic rules that operate independently of the LLM.
These rules override or boost recommendations based on hard business thresholds.
No AI involved — fully predictable and auditable.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from backend.core.shared_state import ADIPState, CustomerContext
from backend.utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class RuleResult:
    triggered: bool
    rule_name: str
    rule_description: str
    priority_override: str | None = None  # forces this priority if triggered
    action_required: str | None = None


class BusinessRulesEngine:
    """
    Evaluates deterministic business rules against customer context and signals.

    Rules are evaluated in order. Multiple rules may fire simultaneously.
    """

    def evaluate(self, state: ADIPState) -> list[RuleResult]:
        """
        Evaluates all business rules against the current state.

        Returns:
            List of RuleResult objects for rules that fired.
        """
        results: list[RuleResult] = []
        customer = state.customer

        if customer is None:
            logger.warning("BusinessRulesEngine: No customer context — skipping rule evaluation.")
            return results

        rules = [
            self._rule_critical_health,
            self._rule_renewal_imminent,
            self._rule_champion_resigned,
            self._rule_low_adoption,
            self._rule_high_churn_signals,
        ]

        for rule_fn in rules:
            result = rule_fn(customer, state)
            if result.triggered:
                logger.info(f"Business rule fired: {result.rule_name}")
                results.append(result)

        return results

    def get_summary(self, results: list[RuleResult]) -> str:
        """Returns a human-readable summary of triggered rules."""
        if not results:
            return "No business rules triggered."
        lines = [f"• {r.rule_name}: {r.rule_description}" for r in results]
        return "\n".join(lines)

    # ── Individual Rules ────────────────────────────────────────────────────

    @staticmethod
    def _rule_critical_health(customer: CustomerContext, state: ADIPState) -> RuleResult:
        """Health Score < 30 → Executive Escalation Required."""
        triggered = customer.health_score < 30
        return RuleResult(
            triggered=triggered,
            rule_name="CRITICAL_HEALTH_SCORE",
            rule_description=f"Health score {customer.health_score} < 30 — executive escalation required.",
            priority_override="critical" if triggered else None,
            action_required="Escalate to executive sponsor immediately." if triggered else None,
        )

    @staticmethod
    def _rule_renewal_imminent(customer: CustomerContext, state: ADIPState) -> RuleResult:
        """Renewal within 30 days → High Priority."""
        from datetime import datetime, date
        triggered = False
        try:
            renewal = datetime.strptime(customer.renewal_date, "%Y-%m-%d").date()
            days_to_renewal = (renewal - date.today()).days
            triggered = 0 <= days_to_renewal <= 30
        except Exception:
            pass
        return RuleResult(
            triggered=triggered,
            rule_name="RENEWAL_IMMINENT",
            rule_description=f"Renewal within 30 days — high priority engagement required.",
            priority_override="high" if triggered else None,
            action_required="Initiate formal renewal process immediately." if triggered else None,
        )

    @staticmethod
    def _rule_champion_resigned(customer: CustomerContext, state: ADIPState) -> RuleResult:
        """Champion resigned → Stakeholder engagement required."""
        triggered = customer.champion_status in ("resigned", "departed", "left")
        return RuleResult(
            triggered=triggered,
            rule_name="CHAMPION_RESIGNED",
            rule_description="Customer champion has left — stakeholder re-engagement required.",
            priority_override="high" if triggered else None,
            action_required="Identify and engage new executive sponsor." if triggered else None,
        )

    @staticmethod
    def _rule_low_adoption(customer: CustomerContext, state: ADIPState) -> RuleResult:
        """Active users < 50% of licensed → Adoption risk."""
        if customer.licensed_users == 0:
            return RuleResult(triggered=False, rule_name="LOW_ADOPTION", rule_description="")
        adoption_rate = customer.active_users / customer.licensed_users
        triggered = adoption_rate < 0.5
        return RuleResult(
            triggered=triggered,
            rule_name="LOW_ADOPTION",
            rule_description=(
                f"Only {customer.active_users}/{customer.licensed_users} users active "
                f"({adoption_rate:.0%}) — adoption intervention required."
            ),
            action_required="Schedule adoption enablement session." if triggered else None,
        )

    @staticmethod
    def _rule_high_churn_signals(customer: CustomerContext, state: ADIPState) -> RuleResult:
        """Multiple churn signals detected → Urgent review."""
        churn_signals = {"churn_risk", "dissatisfaction", "cancellation_intent"}
        detected = set(state.detected_signals) & churn_signals
        triggered = len(detected) >= 2
        return RuleResult(
            triggered=triggered,
            rule_name="HIGH_CHURN_SIGNALS",
            rule_description=f"Multiple churn signals detected: {', '.join(detected)}",
            priority_override="critical" if triggered else None,
            action_required="Initiate churn prevention playbook immediately." if triggered else None,
        )
