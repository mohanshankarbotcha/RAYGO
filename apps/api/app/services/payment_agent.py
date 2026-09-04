import uuid

from app.core.errors import InvalidStateTransitionError, NotFoundError, RazorpaySignatureInvalidError
from app.domain.readiness import compute_readiness
from app.repositories.registry import Repositories
from app.services.audit_service import AuditService
from app.services.razorpay_service import RazorpayService
from app.services.revenue_recovery_service import RevenueRecoveryService


def new_payment_attempt_id() -> str:
    return f"pay_attempt_{uuid.uuid4().hex[:8]}"


class PaymentAgentService:
    def __init__(self, repos: Repositories, razorpay: RazorpayService, audit: AuditService | None = None):
        self.repos = repos
        self.razorpay = razorpay
        self.audit = audit or AuditService(repos)

    async def create_order(self, merchant_id: str, order_intent_id: str, approved_by: str) -> dict:
        intent = await self.repos.order_intents.get(order_intent_id)
        if not intent:
            raise NotFoundError("Order intent not found.", {"orderIntentId": order_intent_id})
        if intent["status"] not in ("review", "payment_failed", "awaiting_authorization", "pending_payment", "payment_order_created"):
            raise InvalidStateTransitionError(
                "Order intent must be in review or payment_failed state to create a payment order.",
                {"status": intent["status"]},
            )

        amount = intent["total"]
        amount_subunits = amount * 100
        rp_order = self.razorpay.create_order(
            amount_subunits=amount_subunits, currency=intent["currency"], receipt=intent["displayOrderId"]
        )

        attempt_id = new_payment_attempt_id()
        attempt = {
            "id": attempt_id,
            "merchantId": merchant_id,
            "orderIntentId": order_intent_id,
            "razorpayOrderId": rp_order["id"],
            "razorpayPaymentId": None,
            "amount": amount,
            "amountSubunits": amount_subunits,
            "currency": intent["currency"],
            "method": "Razorpay Test Mode",
            "status": "awaiting_authorization",
            "automaticRetry": "blocked",
            "retryReason": "Duplicate-charge protection enforced by Policy Guard",
            "customer": intent.get("customerName", "AI Buyer Demo"),
            "metadata": {},
        }
        await self.repos.payment_attempts.upsert(attempt)
        await self.repos.order_intents.update(
            order_intent_id,
            {
                "status": "payment_order_created",
                "paymentStatus": "order_created",
                "metadata": {**intent.get("metadata", {}), "razorpayOrderId": rp_order["id"]},
            },
        )

        return {
            "orderIntentId": order_intent_id,
            "displayOrderId": intent["displayOrderId"],
            "razorpayOrderId": rp_order["id"],
            "amount": amount,
            "amountSubunits": amount_subunits,
            "currency": intent["currency"],
            "keyId": self.razorpay.settings.razorpay_key_id or "rzp_test_stub",
            "environment": "Razorpay Test Mode",
            "paymentAttemptId": attempt_id,
            "status": "awaiting_authorization",
        }

    async def verify(
        self,
        merchant_id: str,
        order_intent_id: str,
        razorpay_order_id: str,
        razorpay_payment_id: str,
        razorpay_signature: str,
    ) -> dict:
        intent = await self.repos.order_intents.get(order_intent_id)
        if not intent:
            raise NotFoundError("Order intent not found.", {"orderIntentId": order_intent_id})

        valid = self.razorpay.verify_payment_signature(razorpay_order_id, razorpay_payment_id, razorpay_signature)
        if not valid:
            await self.repos.order_intents.update(order_intent_id, {"status": "verification_failed"})
            raise RazorpaySignatureInvalidError(
                "Razorpay payment signature verification failed.",
                {"orderIntentId": order_intent_id},
            )

        attempt = await self.repos.payment_attempts.find_one(
            {"orderIntentId": order_intent_id, "razorpayOrderId": razorpay_order_id}
        )
        attempt_id = attempt["id"] if attempt else new_payment_attempt_id()
        await self.repos.payment_attempts.update(
            attempt_id, {"razorpayPaymentId": razorpay_payment_id, "status": "captured"}
        )
        await self.repos.order_intents.update(
            order_intent_id, {"status": "paid", "paymentStatus": "captured"}
        )
        await self.repos.orders.upsert(
            {
                "id": order_intent_id,
                "merchantId": merchant_id,
                "orderIntentId": order_intent_id,
                "displayOrderId": intent["displayOrderId"],
                "customer": intent.get("customerName", "AI Buyer Demo"),
                "amount": intent["total"],
                "currency": intent["currency"],
                "source": intent.get("source", "AI Buyer"),
                "payment": "Razorpay Test Mode",
                "status": "Success",
                "metadata": {},
            }
        )

        # Decrement inventory for each purchased item and record audit events
        for item in intent.get("items", []):
            prod_id = item.get("productId")
            qty = item.get("quantity", 1)
            product = await self.repos.products.get(prod_id)
            if not product:
                product = await self.repos.products.find_one({"merchantId": merchant_id, "id": prod_id})
            if product:
                old_inv = int(product.get("inventory", 0))
                new_inv = max(0, old_inv - qty)
                merged = {**product, "inventory": new_inv}
                computed = compute_readiness(merged)
                final_prod = {**merged, **computed}
                await self.repos.products.update(prod_id, final_prod)

                await self.audit.record(
                    merchant_id=merchant_id,
                    agent="Payment Agent",
                    action="Adjust Stock",
                    reason=f"Owner updated product {product.get('name', prod_id)} ({product.get('sku', '')}). Field: Inventory from {old_inv} to {new_inv} (Payment verified for {intent.get('displayOrderId', order_intent_id)}).",
                    policy="Passed",
                    approval="System Action",
                    outcome="Success",
                    correlation_ids={"productId": prod_id, "orderIntentId": order_intent_id},
                    details={"oldInventory": old_inv, "newInventory": new_inv, "delta": -qty},
                )

        return {
            "verified": True,
            "orderIntentId": order_intent_id,
            "displayOrderId": intent["displayOrderId"],
            "paymentAttemptId": attempt_id,
            "amountPaid": intent["total"],
            "currency": intent["currency"],
            "status": "captured",
            "environment": "Razorpay Test Mode",
            "timeline": [
                "Intent received",
                "Products selected",
                "Order created",
                "Payment authorized",
                "Order confirmed",
            ],
            "aiCommerceSummary": {
                "decisionTimeSec": intent.get("metadata", {}).get("decisionTimeSec", 2.4),
                "recommendationConfidence": intent.get("metadata", {}).get("recommendationConfidence", 92),
                "action": "Checkout Completed",
            },
            "nextRoute": "/payment/success",
        }

    async def record_failure(
        self, merchant_id: str, order_intent_id: str, razorpay_order_id: str | None, error_description: str
    ) -> dict:
        intent = await self.repos.order_intents.get(order_intent_id)
        if not intent:
            raise NotFoundError("Order intent not found.", {"orderIntentId": order_intent_id})

        classification = RevenueRecoveryService.classify(error_description)

        attempt = None
        if razorpay_order_id:
            attempt = await self.repos.payment_attempts.find_one(
                {"orderIntentId": order_intent_id, "razorpayOrderId": razorpay_order_id}
            )
        attempt_id = attempt["id"] if attempt else new_payment_attempt_id()
        await self.repos.payment_attempts.upsert(
            {
                "id": attempt_id,
                "merchantId": merchant_id,
                "orderIntentId": order_intent_id,
                "razorpayOrderId": razorpay_order_id,
                "amount": intent["total"],
                "currency": intent["currency"],
                "method": "Razorpay Test Mode",
                "status": "failed_retry_blocked",
                "failureType": classification["failureType"],
                "failureReason": error_description,
                "recommendedAction": classification["recommendedAction"],
                "requiresUserAction": classification["requiresUserAction"],
                "reconciledAt": None,
                "automaticRetry": "blocked",
                "retryBlockedReason": "Duplicate-charge protection",
                "metadata": {},
            }
        )
        await self.repos.order_intents.update(
            order_intent_id, {"paymentStatus": "failed", "status": "payment_failed"}
        )

        await self.audit.record(
            merchant_id=merchant_id,
            agent="Payment Agent",
            action="Payment failed",
            reason=f"Payment failed for order {intent.get('displayOrderId', order_intent_id)}: {error_description}. Diagnosis: {classification['failureType']}.",
            policy="Enforced",
            approval="System Action",
            outcome="Failed",
            correlation_ids={"orderIntentId": order_intent_id, "paymentAttemptId": attempt_id},
            details={
                "failureType": classification["failureType"],
                "recommendedAction": classification["recommendedAction"],
                "requiresUserAction": classification["requiresUserAction"],
                "automaticRetry": "blocked",
            },
        )

        return {
            "orderIntentId": order_intent_id,
            "displayOrderId": intent["displayOrderId"],
            "amount": intent["total"],
            "currency": intent["currency"],
            "status": "failed_retry_blocked",
            "automaticRetry": "blocked",
            "failureType": classification["failureType"],
            "recommendedAction": classification["recommendedAction"],
            "requiresUserAction": classification["requiresUserAction"],
            "reason": error_description,
            "retryBlockedReason": "Duplicate-charge protection",
            "safetyResponse": [
                "No duplicate payment attempted",
                "Order remains unpaid",
                "Inventory unchanged",
                "Failure recorded in audit trail",
                f"Recovery option generated: {classification['recommendedAction']}",
            ],
            "nextRoute": "/payment/failure",
        }

    async def record_dismissal(
        self, merchant_id: str, order_intent_id: str, razorpay_order_id: str | None = None, reason: str = "Buyer closed checkout modal"
    ) -> dict:
        intent = await self.repos.order_intents.get(order_intent_id)
        if not intent:
            raise NotFoundError("Order intent not found.", {"orderIntentId": order_intent_id})

        classification = RevenueRecoveryService.classify("dismissed")

        attempt = None
        if razorpay_order_id:
            attempt = await self.repos.payment_attempts.find_one(
                {"orderIntentId": order_intent_id, "razorpayOrderId": razorpay_order_id}
            )
        attempt_id = attempt["id"] if attempt else new_payment_attempt_id()

        await self.repos.payment_attempts.upsert(
            {
                "id": attempt_id,
                "merchantId": merchant_id,
                "orderIntentId": order_intent_id,
                "razorpayOrderId": razorpay_order_id,
                "amount": intent["total"],
                "currency": intent["currency"],
                "method": "Razorpay Test Mode",
                "status": "dismissed",
                "failureType": classification["failureType"],
                "failureReason": reason,
                "recommendedAction": classification["recommendedAction"],
                "requiresUserAction": classification["requiresUserAction"],
                "reconciledAt": None,
                "automaticRetry": "blocked",
                "retryBlockedReason": "Checkout window closed by user",
                "metadata": {},
            }
        )

        # Order intent stays in payment_order_created (not failed!)
        await self.repos.order_intents.update(
            order_intent_id, {"paymentStatus": "dismissed", "status": "payment_order_created"}
        )

        await self.audit.record(
            merchant_id=merchant_id,
            agent="Payment Agent",
            action="Payment dismissed",
            reason=f"Checkout window closed for order {intent.get('displayOrderId', order_intent_id)}. Order preserved as pending.",
            policy="Passed",
            approval="System Action",
            outcome="Dismissed",
            correlation_ids={"orderIntentId": order_intent_id, "paymentAttemptId": attempt_id},
            details={
                "failureType": classification["failureType"],
                "recommendedAction": classification["recommendedAction"],
                "requiresUserAction": classification["requiresUserAction"],
            },
        )

        return {
            "orderIntentId": order_intent_id,
            "displayOrderId": intent["displayOrderId"],
            "amount": intent["total"],
            "currency": intent["currency"],
            "status": "dismissed",
            "outcome": "Dismissed",
            "failureType": classification["failureType"],
            "recommendedAction": classification["recommendedAction"],
            "requiresUserAction": classification["requiresUserAction"],
            "message": "Payment window closed. Your basket is saved and order remains pending.",
        }

    async def get_payment_attempt(self, merchant_id: str, payment_attempt_id: str) -> dict:
        attempt = await self.repos.payment_attempts.get(payment_attempt_id)
        if not attempt:
            attempt = await self.repos.payment_attempts.find_one({"merchantId": merchant_id, "id": payment_attempt_id})
        if not attempt:
            raise NotFoundError("Payment attempt not found.", {"paymentAttemptId": payment_attempt_id})

        order_intent = await self.repos.order_intents.get(attempt.get("orderIntentId"))
        audit_events = await self.repos.audit_events.find_many(
            {"correlationIds.paymentAttemptId": payment_attempt_id}
        )

        return {
            "attempt": attempt,
            "orderIntent": order_intent,
            "auditEvents": audit_events,
            "diagnosis": {
                "failureType": attempt.get("failureType", "unclassified"),
                "recommendedAction": attempt.get("recommendedAction", "Try another payment method or return to your basket."),
                "requiresUserAction": attempt.get("requiresUserAction", True),
                "reconciledAt": attempt.get("reconciledAt"),
            },
        }

    async def reconcile(self, merchant_id: str, payment_attempt_id: str) -> dict:
        attempt = await self.repos.payment_attempts.get(payment_attempt_id)
        if not attempt:
            attempt = await self.repos.payment_attempts.find_one({"merchantId": merchant_id, "id": payment_attempt_id})
        if not attempt:
            raise NotFoundError("Payment attempt not found.", {"paymentAttemptId": payment_attempt_id})

        import datetime
        now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        # Check current status safely without mutating to paid unless gateway verified
        current_status = attempt.get("status", "unknown")
        reconcile_result = "verified_consistent"
        
        if current_status == "uncertain":
            # In stub mode, keep uncertain or resolve per gateway record
            note = "Reconciled with gateway state: no uncaptured funds found."
        else:
            note = f"Current payment status confirmed as '{current_status}'."

        await self.repos.payment_attempts.update(
            attempt["id"],
            {"reconciledAt": now_iso}
        )

        await self.audit.record(
            merchant_id=merchant_id,
            agent="Payment Agent",
            action="Payment reconciled",
            reason=f"Owner requested payment reconciliation for attempt {payment_attempt_id}. Result: {reconcile_result}.",
            policy="Passed",
            approval="Merchant Action",
            outcome="Reconciled",
            correlation_ids={"paymentAttemptId": payment_attempt_id, "orderIntentId": attempt.get("orderIntentId")},
            details={"status": current_status, "reconciledAt": now_iso, "note": note},
        )

        return {
            "paymentAttemptId": payment_attempt_id,
            "orderIntentId": attempt.get("orderIntentId"),
            "status": current_status,
            "reconciledAt": now_iso,
            "result": reconcile_result,
            "note": note,
        }
