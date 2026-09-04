import uuid
from datetime import datetime, timezone

from app.domain.constants import (
    DAILY_BUDGET_LIMIT,
    DISCOUNT_MAX_PCT,
    MARGIN_MIN_PCT,
    OUTCOME_BLOCKED,
    OUTCOME_PASSED,
    OUTCOME_REQUIRES_APPROVAL,
)
from app.repositories.registry import Repositories


def new_policy_evaluation_id() -> str:
    return f"pol_eval_{uuid.uuid4().hex[:8]}"


class PolicyGuard:
    """Called before every consequential action. Outcome is one of:
    passed | requires_approval | blocked. Hard rules (discount > 20%,
    margin < 25%, payment retry, refunds) always block, regardless of
    caller intent."""

    def __init__(self, repos: Repositories):
        self.repos = repos

    async def evaluate(
        self,
        merchant_id: str,
        action_type: str,
        target_type: str,
        target_id: str,
        proposed_action: dict | None = None,
    ) -> dict:
        proposed_action = proposed_action or {}
        checks: list[dict] = []
        reasons: list[str] = []
        outcome = OUTCOME_REQUIRES_APPROVAL

        if action_type == "retry_payment":
            checks.append(
                {"policy": "Payment Retry", "result": "blocked", "reason": "Duplicate-charge protection"}
            )
            reasons.append("Automatic payment retry is blocked after a failed attempt.")
            outcome = OUTCOME_BLOCKED

        elif action_type == "refund":
            checks.append(
                {"policy": "Refund", "result": "blocked", "reason": "Refund execution is not allowed in MVP."}
            )
            reasons.append("Refund execution is not allowed in MVP.")
            outcome = OUTCOME_BLOCKED

        else:
            discount_pct = proposed_action.get("discountPct")
            if discount_pct is not None:
                if discount_pct > DISCOUNT_MAX_PCT:
                    checks.append(
                        {
                            "policy": "Discount Limit",
                            "result": "blocked",
                            "reason": f"{discount_pct}% exceeds the {DISCOUNT_MAX_PCT}% limit.",
                        }
                    )
                    reasons.append(f"Discount {discount_pct}% exceeds policy limit of {DISCOUNT_MAX_PCT}%.")
                    outcome = OUTCOME_BLOCKED
                else:
                    checks.append(
                        {"policy": "Discount Limit", "result": "passed", "reason": f"{discount_pct}% <= {DISCOUNT_MAX_PCT}%"}
                    )
                    reasons.append(f"Discount {discount_pct}% is within policy.")

            margin_pct = proposed_action.get("estimatedMarginPct")
            if margin_pct is not None and outcome != OUTCOME_BLOCKED:
                if margin_pct < MARGIN_MIN_PCT:
                    checks.append(
                        {
                            "policy": "Margin Floor",
                            "result": "blocked",
                            "reason": f"{margin_pct}% is below the {MARGIN_MIN_PCT}% floor.",
                        }
                    )
                    reasons.append(f"Projected margin {margin_pct}% falls below policy floor of {MARGIN_MIN_PCT}%.")
                    outcome = OUTCOME_BLOCKED
                else:
                    checks.append(
                        {"policy": "Margin Floor", "result": "passed", "reason": f"{margin_pct}% >= {MARGIN_MIN_PCT}%"}
                    )
                    reasons.append(f"Projected margin remains above the {MARGIN_MIN_PCT}% floor.")

            campaign_spend = proposed_action.get("campaignSpend")
            if campaign_spend is not None and outcome != OUTCOME_BLOCKED:
                already_committed = await self._committed_campaign_spend_today(merchant_id, action_type)
                projected_total = already_committed + campaign_spend
                if projected_total > DAILY_BUDGET_LIMIT:
                    checks.append(
                        {
                            "policy": "Daily Budget",
                            "result": "blocked",
                            "reason": (
                                f"₹{projected_total} (₹{already_committed} already committed today + "
                                f"₹{campaign_spend} proposed) exceeds the ₹{DAILY_BUDGET_LIMIT} daily limit."
                            ),
                        }
                    )
                    reasons.append(
                        f"Campaign spend would bring today's total to ₹{projected_total}, "
                        f"exceeding the ₹{DAILY_BUDGET_LIMIT} Daily Budget limit."
                    )
                    outcome = OUTCOME_BLOCKED
                else:
                    checks.append(
                        {
                            "policy": "Daily Budget",
                            "result": "passed",
                            "reason": f"₹{projected_total} <= ₹{DAILY_BUDGET_LIMIT}",
                        }
                    )
                    reasons.append(f"Campaign spend stays within the ₹{DAILY_BUDGET_LIMIT} Daily Budget limit.")

            sample_size = proposed_action.get("sampleSize")
            if sample_size is not None and outcome != OUTCOME_BLOCKED:
                if sample_size < 100:
                    checks.append(
                        {
                            "policy": "Sample Size Guardrail",
                            "result": "blocked",
                            "reason": f"Sample size of {sample_size} is below the 100-visitor threshold required for statistical validity.",
                        }
                    )
                    reasons.append(f"Insufficient sample size ({sample_size} < 100) to safely scale experiment.")
                    outcome = OUTCOME_BLOCKED
                else:
                    checks.append(
                        {
                            "policy": "Sample Size Guardrail",
                            "result": "passed",
                            "reason": f"Sample size {sample_size} >= 100 threshold.",
                        }
                    )
                    reasons.append(f"Sample size ({sample_size}) meets statistical confidence requirements.")

            if outcome != OUTCOME_BLOCKED:
                checks.append(
                    {"policy": "Merchant Auth", "result": "requires_approval", "reason": "Merchant Auth is REQUIRED"}
                )
                reasons.append("Merchant approval is required before this action executes.")
                outcome = OUTCOME_REQUIRES_APPROVAL

        evaluation = {
            "id": new_policy_evaluation_id(),
            "merchantId": merchant_id,
            "actionType": action_type,
            "targetType": target_type,
            "targetId": target_id,
            "outcome": outcome,
            "reasons": reasons,
            "checks": checks,
            "metadata": {"proposedAction": proposed_action},
        }
        saved = await self.repos.policy_evaluations.upsert(evaluation)
        return saved

    async def _committed_campaign_spend_today(self, merchant_id: str, action_type: str) -> float:
        """Sums campaign spend from today's non-blocked evaluations of this
        action type, so a Daily Budget check reflects cumulative spend
        rather than evaluating each proposal in isolation."""
        today_prefix = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        query = {
            "merchantId": merchant_id,
            "actionType": action_type,
            "outcome": {"$ne": OUTCOME_BLOCKED},
            "createdAt": {"$regex": f"^{today_prefix}"},
        }
        todays_evaluations = await self.repos.policy_evaluations.find_many(query, limit=500)
        return sum(
            (e.get("metadata", {}).get("proposedAction", {}) or {}).get("campaignSpend", 0) or 0
            for e in todays_evaluations
        )
