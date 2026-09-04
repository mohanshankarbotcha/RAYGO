"""Revenue Recovery Classification & Guidance Service.

Provides deterministic-first classification of payment failures, dismissals,
and gateway exceptions into safe, actionable next steps for buyers and merchants.
"""

from typing import Any

FAILURE_CLASSIFICATION: dict[str, tuple[str, str, bool]] = {
    # Razorpay error codes / keywords -> (failureType, recommendedAction, requiresUserAction)
    "BAD_REQUEST_ERROR": ("card_declined", "Try a different card or payment method.", True),
    "GATEWAY_ERROR": ("gateway_issue", "Wait a moment and try again with the same method.", True),
    "SERVER_ERROR": ("gateway_issue", "Wait a moment and try again with the same method.", True),
    "dismissed": ("buyer_cancelled", "Resume checkout when ready — your basket is saved.", True),
    "card_declined": ("card_declined", "Try a different card or payment method.", True),
    "insufficient_funds": ("card_declined", "Check account balance or use another payment instrument.", True),
    "payment_cancelled": ("buyer_cancelled", "Resume checkout when ready — your basket is saved.", True),
    "unknown": ("unclassified", "Try another payment method or return to your basket.", True),
}


class RevenueRecoveryService:
    """Classifies payment failures deterministically and generates safe recovery guidance."""

    @staticmethod
    def classify(error_code_or_description: str | None = None) -> dict[str, Any]:
        """Classify error string into a structured diagnosis and recommended action."""
        if not error_code_or_description:
            code = "unknown"
        else:
            raw = error_code_or_description.strip().upper()
            if "BAD_REQUEST" in raw or "DECLINED" in raw or "INVALID_CARD" in raw or "EXPIRED" in raw:
                code = "BAD_REQUEST_ERROR"
            elif "GATEWAY" in raw or "TIMED_OUT" in raw or "TIMEOUT" in raw:
                code = "GATEWAY_ERROR"
            elif "SERVER" in raw or "INTERNAL" in raw or "500" in raw:
                code = "SERVER_ERROR"
            elif "DISMISS" in raw or "CANCEL" in raw or "CLOSE" in raw:
                code = "dismissed"
            else:
                code = error_code_or_description.strip().lower()

        failure_type, recommended_action, requires_user_action = FAILURE_CLASSIFICATION.get(
            code, FAILURE_CLASSIFICATION["unknown"]
        )

        return {
            "failureType": failure_type,
            "recommendedAction": recommended_action,
            "requiresUserAction": requires_user_action,
            "automaticRetryAllowed": False,
            "policyLock": "Automatic payment retry is permanently blocked to prevent duplicate charges.",
        }
