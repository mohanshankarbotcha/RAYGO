OPPORTUNITY_STATUSES = {
    "detected",
    "ready_for_review",
    "policy_evaluated",
    "approved",
    "experiment_created",
    "blocked",
    "failed",
    "declined",
}

EXPERIMENT_STATUSES = {
    "draft",
    "running",
    "scale_review",
    "policy_evaluated",
    "approval_required",
    "scaled",
    "completed",
    "blocked",
    "failed",
}

ORDER_INTENT_STATUSES = {
    "created",
    "review",
    "payment_order_created",
    "payment_authorized",
    "paid",
    "payment_failed",
    "payment_uncertain",
    "verification_failed",
    "cancelled",
}

PAYMENT_ATTEMPT_STATUSES = {
    "created",
    "awaiting_authorization",
    "authorized",
    "captured",
    "failed",
    "failed_retry_blocked",
    "verification_failed",
    "dismissed",
    "uncertain",
}

APPROVAL_STATUSES = {"requested", "approved", "rejected", "expired"}

CONSEQUENTIAL_ACTION_STATE = (
    "proposed",
    "policy_evaluated",
    "approval_required",
    "merchant_approved",
    "execution_pending",
    "executed",
    "blocked",
    "failed",
)
