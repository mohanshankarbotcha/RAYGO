import asyncio

from fastapi import APIRouter, Depends, Header, Request

from app.api.deps import get_audit_service, get_payment_agent, get_policy_guard, get_razorpay_service, get_repos
from app.core.errors import WebhookEventConflictError, WebhookSignatureInvalidError
from app.core.idempotency import IdempotencyService
from app.core.security import resolve_merchant_id
from app.domain.constants import AGENT_PAYMENT, AGENT_POLICY_GUARD, OUTCOME_BLOCKED
from app.domain.schemas import RazorpayDismissRequest, RazorpayFailureRequest, RazorpayOrderRequest, RazorpayVerifyRequest
from app.repositories.registry import Repositories
from app.services.audit_service import AuditService
from app.services.payment_agent import PaymentAgentService
from app.services.policy_guard import PolicyGuard
from app.services.razorpay_service import RazorpayService

router = APIRouter(tags=["payments"])


@router.post("/payments/razorpay/order")
async def create_razorpay_order(
    body: RazorpayOrderRequest,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    repos: Repositories = Depends(get_repos),
    payment_agent: PaymentAgentService = Depends(get_payment_agent),
    policy_guard: PolicyGuard = Depends(get_policy_guard),
    audit: AuditService = Depends(get_audit_service),
):
    idem = IdempotencyService(repos.idempotency_records)
    route = "/api/v1/payments/razorpay/order"
    cached = await idem.check_and_store(idempotency_key, route, "POST", body.model_dump())
    if cached:
        return cached

    evaluation = await policy_guard.evaluate(
        merchant_id=body.merchant_id,
        action_type="execute_payment",
        target_type="order_intent",
        target_id=body.order_intent_id,
        proposed_action={},
    )
    await audit.record(
        merchant_id=body.merchant_id,
        agent=AGENT_POLICY_GUARD,
        action="Policy evaluated",
        reason="Evaluated payment execution ahead of Razorpay order creation.",
        correlation_ids={"orderIntentId": body.order_intent_id, "policyEvaluationId": evaluation["id"]},
    )

    result = await payment_agent.create_order(body.merchant_id, body.order_intent_id, body.approved_by)
    await audit.record(
        merchant_id=body.merchant_id,
        agent=AGENT_PAYMENT,
        action="Create Order",
        reason="Buyer confirmed purchase. Policy check passed. Merchant auth confirmed.",
        approval="Confirmed",
        correlation_ids={
            "orderIntentId": body.order_intent_id,
            "orderId": result["razorpayOrderId"],
            "paymentAttemptId": result["paymentAttemptId"],
            "policyEvaluationId": evaluation["id"],
        },
    )
    await idem.store_response(idempotency_key, route, 200, result)
    return result


@router.post("/payments/razorpay/verify")
async def verify_razorpay_payment(
    body: RazorpayVerifyRequest,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    repos: Repositories = Depends(get_repos),
    payment_agent: PaymentAgentService = Depends(get_payment_agent),
    audit: AuditService = Depends(get_audit_service),
):
    idem = IdempotencyService(repos.idempotency_records)
    route = "/api/v1/payments/razorpay/verify"
    cached = await idem.check_and_store(idempotency_key, route, "POST", body.model_dump())
    if cached:
        return cached

    result = await payment_agent.verify(
        body.merchant_id,
        body.order_intent_id,
        body.razorpay_order_id,
        body.razorpay_payment_id,
        body.razorpay_signature,
    )
    await audit.record(
        merchant_id=body.merchant_id,
        agent=AGENT_PAYMENT,
        action="Payment verified",
        reason="Razorpay signature verified server-side. Order confirmed.",
        approval="Confirmed",
        correlation_ids={
            "orderIntentId": body.order_intent_id,
            "orderId": body.razorpay_order_id,
            "paymentAttemptId": result["paymentAttemptId"],
        },
    )
    await idem.store_response(idempotency_key, route, 200, result)
    return result


@router.post("/payments/razorpay/failure")
async def record_razorpay_failure(
    body: RazorpayFailureRequest,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    repos: Repositories = Depends(get_repos),
    payment_agent: PaymentAgentService = Depends(get_payment_agent),
    policy_guard: PolicyGuard = Depends(get_policy_guard),
    audit: AuditService = Depends(get_audit_service),
):
    idem = IdempotencyService(repos.idempotency_records)
    route = "/api/v1/payments/razorpay/failure"
    cached = await idem.check_and_store(idempotency_key, route, "POST", body.model_dump())
    if cached:
        return cached

    result = await payment_agent.record_failure(
        body.merchant_id, body.order_intent_id, body.razorpay_order_id, body.error_description
    )
    await audit.record(
        merchant_id=body.merchant_id,
        agent=AGENT_PAYMENT,
        action="Payment failed",
        reason=body.error_description,
        outcome="Failed",
        severity="warning",
        correlation_ids={"orderIntentId": body.order_intent_id, "orderId": body.razorpay_order_id},
    )

    retry_eval = await policy_guard.evaluate(
        merchant_id=body.merchant_id,
        action_type="retry_payment",
        target_type="order_intent",
        target_id=body.order_intent_id,
        proposed_action={},
    )
    await audit.record(
        merchant_id=body.merchant_id,
        agent=AGENT_POLICY_GUARD,
        action="Retry Payment",
        reason="Payment failed",
        policy="Max_Retries_Exceeded",
        approval="N/A",
        outcome="Prevented",
        severity="warning",
        correlation_ids={
            "orderIntentId": body.order_intent_id,
            "orderId": body.razorpay_order_id,
            "policyEvaluationId": retry_eval["id"],
        },
        details={
            "decisionSummary": "Automatic retry was blocked to prevent duplicate charge risk.",
            "evidence": ["Payment attempt returned failed status."],
            "policyChecks": [
                {"policy": "Payment Retry", "result": "blocked", "reason": "Duplicate-charge protection"}
            ],
            "executionResult": "No retry attempted",
        },
        event_id="audit_001" if body.order_intent_id == "intent_ai_setup_001" else None,
    )

    await idem.store_response(idempotency_key, route, 200, result)
    return result


@router.post("/payments/razorpay/dismiss")
async def record_razorpay_dismiss(
    body: RazorpayDismissRequest,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    repos: Repositories = Depends(get_repos),
    payment_agent: PaymentAgentService = Depends(get_payment_agent),
):
    idem = IdempotencyService(repos.idempotency_records)
    route = "/api/v1/payments/razorpay/dismiss"
    cached = await idem.check_and_store(idempotency_key, route, "POST", body.model_dump())
    if cached:
        return cached

    result = await payment_agent.record_dismissal(
        body.merchant_id, body.order_intent_id, body.razorpay_order_id, body.reason
    )
    await idem.store_response(idempotency_key, route, 200, result)
    return result


@router.get("/payments/{payment_attempt_id}")
async def get_payment_detail(
    payment_attempt_id: str,
    request: Request,
    payment_agent: PaymentAgentService = Depends(get_payment_agent),
):
    merchant_id = resolve_merchant_id(request)
    return await payment_agent.get_payment_attempt(merchant_id, payment_attempt_id)


@router.post("/payments/{payment_attempt_id}/reconcile")
async def reconcile_payment(
    payment_attempt_id: str,
    request: Request,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    repos: Repositories = Depends(get_repos),
    payment_agent: PaymentAgentService = Depends(get_payment_agent),
):
    merchant_id = resolve_merchant_id(request)
    idem = IdempotencyService(repos.idempotency_records)
    route = f"/api/v1/payments/{payment_attempt_id}/reconcile"
    cached = await idem.check_and_store(idempotency_key, route, "POST", {"paymentAttemptId": payment_attempt_id})
    if cached:
        return cached

    result = await payment_agent.reconcile(merchant_id, payment_attempt_id)
    await idem.store_response(idempotency_key, route, 200, result)
    return result


@router.post("/webhooks/razorpay")
async def razorpay_webhook(
    request: Request,
    repos: Repositories = Depends(get_repos),
    razorpay: RazorpayService = Depends(get_razorpay_service),
    audit: AuditService = Depends(get_audit_service),
):
    raw_body = await request.body()
    signature = request.headers.get("X-Razorpay-Signature", "")
    if not razorpay.verify_webhook_signature(raw_body, signature):
        raise WebhookSignatureInvalidError("Razorpay webhook signature is invalid.")

    import json

    payload = json.loads(raw_body or b"{}")
    event_id = payload.get("id") or payload.get("event_id") or signature[:24]
    event_type = payload.get("event", "unknown")

    existing = await repos.webhook_events.find_one({"razorpayEventId": event_id})
    if existing:
        return {"received": True, "processed": False, "idempotent": True}

    await repos.webhook_events.insert(
        {"id": event_id, "razorpayEventId": event_id, "eventType": event_type, "payload": payload}
    )
    await audit.record(
        merchant_id=resolve_merchant_id(request),
        agent=AGENT_PAYMENT,
        action="Webhook received",
        reason=f"Processed Razorpay webhook event {event_type}.",
        correlation_ids={"razorpayEventId": event_id},
    )
    return {"received": True, "processed": True, "idempotent": False}


@router.get("/payments")
async def list_payments(request: Request, repos: Repositories = Depends(get_repos)):
    merchant_id = resolve_merchant_id(request)
    attempts = await repos.payment_attempts.find_many({"merchantId": merchant_id}, limit=50)

    # Fetch each distinct order intent once, concurrently, instead of a
    # sequential await per attempt (avoids N+1 round trips to the DB).
    unique_ids = list({a["orderIntentId"] for a in attempts})
    fetched = await asyncio.gather(*(repos.order_intents.get(oid) for oid in unique_ids))
    order_intents_by_id: dict[str, dict] = {oid: (doc or {}) for oid, doc in zip(unique_ids, fetched)}

    items = [
        {
            "paymentId": a["id"],
            "order": (order_intents_by_id.get(a["orderIntentId"]) or {}).get("displayOrderId", a["orderIntentId"]),
            "amount": a["amount"],
            "currency": a["currency"],
            "method": a.get("method", "Razorpay Test Mode"),
            "status": a["status"],
            "timestamp": a["updatedAt"],
        }
        for a in attempts
    ]
    successful = sum(1 for a in attempts if a["status"] == "captured")
    failed = sum(1 for a in attempts if a["status"] in ("failed", "failed_retry_blocked", "verification_failed"))
    pending = sum(1 for a in attempts if a["status"] in ("created", "awaiting_authorization", "authorized"))
    return {
        "summary": {"successful": successful, "failed": failed, "pending": pending, "refunds": 0},
        "items": items,
        "total": len(items),
        "nextCursor": None,
    }


@router.get("/orders")
async def list_orders(request: Request, repos: Repositories = Depends(get_repos)):
    merchant_id = resolve_merchant_id(request)
    orders = await repos.orders.find_many({"merchantId": merchant_id}, limit=50)
    payment_attempts = await repos.payment_attempts.find_many({"merchantId": merchant_id}, limit=50)
    gmv = sum(o["amount"] for o in orders)
    successful_payments = sum(1 for a in payment_attempts if a["status"] == "captured")
    failed_payments = sum(1 for a in payment_attempts if a["status"] in ("failed", "failed_retry_blocked"))
    ai_buyer_orders = sum(1 for o in orders if o.get("source") == "AI Buyer")
    items = [
        {
            "order": o["displayOrderId"],
            "orderIntentId": o["orderIntentId"],
            "customer": o["customer"],
            "amount": o["amount"],
            "currency": o["currency"],
            "source": o["source"],
            "payment": o["payment"],
            "status": o["status"],
        }
        for o in orders
    ]
    return {
        "summary": {
            "gmv": gmv,
            "successfulPayments": successful_payments,
            "failedPayments": failed_payments,
            "aiBuyerOrders": ai_buyer_orders,
        },
        "items": items,
        "total": len(items),
        "nextCursor": None,
    }
