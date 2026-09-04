import pytest
from httpx import AsyncClient

from app.services.revenue_recovery_service import RevenueRecoveryService, FAILURE_CLASSIFICATION


@pytest.mark.asyncio
async def test_failure_classification_matches_error_code():
    """Parametrized verification of the deterministic classification engine."""
    assert RevenueRecoveryService.classify("BAD_REQUEST_ERROR")["failureType"] == "card_declined"
    assert RevenueRecoveryService.classify("Your card was declined")["failureType"] == "card_declined"
    assert RevenueRecoveryService.classify("GATEWAY_ERROR")["failureType"] == "gateway_issue"
    assert RevenueRecoveryService.classify("SERVER_ERROR")["failureType"] == "gateway_issue"
    assert RevenueRecoveryService.classify("dismissed")["failureType"] == "buyer_cancelled"
    assert RevenueRecoveryService.classify("unknown_random_error")["failureType"] == "unclassified"
    assert RevenueRecoveryService.classify(None)["failureType"] == "unclassified"


@pytest.mark.asyncio
async def test_dismissal_is_distinct_from_failure(client: AsyncClient):
    """Dismiss endpoint produces outcome != 'Failed' and keeps order intent pending."""
    # 1. Create intent and payment order
    basket_res = await client.post(
        "/api/v1/ai-buyer/basket",
        json={"merchantId": "merchant_novatech", "items": [{"productId": "prod_probook", "quantity": 1}]},
    )
    basket_id = basket_res.json()["basketId"]
    intent_res = await client.post(
        "/api/v1/order-intents",
        json={"merchantId": "merchant_novatech", "basketId": basket_id},
    )
    order_intent_id = intent_res.json()["orderIntentId"]

    order_res = await client.post(
        "/api/v1/payments/razorpay/order",
        json={"merchantId": "merchant_novatech", "orderIntentId": order_intent_id, "approvedBy": "merchant_demo_user"},
    )
    razorpay_order_id = order_res.json()["razorpayOrderId"]

    # 2. Dismiss checkout
    dismiss_res = await client.post(
        "/api/v1/payments/razorpay/dismiss",
        json={"merchantId": "merchant_novatech", "orderIntentId": order_intent_id, "razorpayOrderId": razorpay_order_id},
    )
    assert dismiss_res.status_code == 200
    dismiss_data = dismiss_res.json()
    assert dismiss_data["outcome"] == "Dismissed"
    assert dismiss_data["status"] == "dismissed"
    assert dismiss_data["failureType"] == "buyer_cancelled"

    # 3. Verify order intent is NOT payment_failed
    intent_get = await client.get(f"/api/v1/order-intents/{order_intent_id}")
    assert intent_get.status_code == 200
    assert intent_get.json()["status"] == "payment_order_created"
    assert intent_get.json()["status"] != "payment_failed"


@pytest.mark.asyncio
async def test_failure_records_diagnosis_and_blocks_automatic_retry(client: AsyncClient):
    """Failure response includes diagnosis fields and verifies automatic retry is blocked."""
    basket_res = await client.post(
        "/api/v1/ai-buyer/basket",
        json={"merchantId": "merchant_novatech", "items": [{"productId": "prod_mx_master", "quantity": 1}]},
    )
    basket_id = basket_res.json()["basketId"]
    intent_res = await client.post(
        "/api/v1/order-intents",
        json={"merchantId": "merchant_novatech", "basketId": basket_id},
    )
    order_intent_id = intent_res.json()["orderIntentId"]

    await client.post(
        "/api/v1/payments/razorpay/order",
        json={"merchantId": "merchant_novatech", "orderIntentId": order_intent_id, "approvedBy": "merchant_demo_user"},
    )

    failure_res = await client.post(
        "/api/v1/payments/razorpay/failure",
        json={
            "merchantId": "merchant_novatech",
            "orderIntentId": order_intent_id,
            "errorDescription": "BAD_REQUEST_ERROR: Insufficient credit limit on card",
        },
    )
    assert failure_res.status_code == 200
    data = failure_res.json()
    assert data["status"] == "failed_retry_blocked"
    assert data["automaticRetry"] == "blocked"
    assert data["failureType"] == "card_declined"
    assert "Try a different card" in data["recommendedAction"]
    assert data["requiresUserAction"] is True


@pytest.mark.asyncio
async def test_payment_detail_and_reconcile_endpoints(client: AsyncClient):
    """GET /payments/{id} and POST /payments/{id}/reconcile return safe verified state."""
    basket_res = await client.post(
        "/api/v1/ai-buyer/basket",
        json={"merchantId": "merchant_novatech", "items": [{"productId": "prod_ergo_stand", "quantity": 1}]},
    )
    basket_id = basket_res.json()["basketId"]
    intent_res = await client.post(
        "/api/v1/order-intents",
        json={"merchantId": "merchant_novatech", "basketId": basket_id},
    )
    order_intent_id = intent_res.json()["orderIntentId"]

    order_res = await client.post(
        "/api/v1/payments/razorpay/order",
        json={"merchantId": "merchant_novatech", "orderIntentId": order_intent_id, "approvedBy": "merchant_demo_user"},
    )
    attempt_id = order_res.json()["paymentAttemptId"]

    # 1. Detail endpoint
    detail_res = await client.get(f"/api/v1/payments/{attempt_id}")
    assert detail_res.status_code == 200
    detail = detail_res.json()
    assert detail["attempt"]["id"] == attempt_id
    assert "diagnosis" in detail

    # 2. Reconcile endpoint
    reconcile_res = await client.post(f"/api/v1/payments/{attempt_id}/reconcile")
    assert reconcile_res.status_code == 200
    reconcile_data = reconcile_res.json()
    assert reconcile_data["paymentAttemptId"] == attempt_id
    assert reconcile_data["result"] == "verified_consistent"
