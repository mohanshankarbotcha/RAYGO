async def test_full_demo_path_success(client):
    # 1. Overview
    r = await client.get("/api/v1/dashboard/overview")
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["metrics"]["aiCommerceReadiness"] == 82
    assert body["merchant"]["id"] == "merchant_novatech"

    # 2. Opportunity detail
    r = await client.get("/api/v1/opportunities/opp_keyboard_stand")
    assert r.status_code == 200, r.text

    # 3. Approve opportunity -> creates experiment
    r = await client.post(
        "/api/v1/opportunities/opp_keyboard_stand/approve",
        json={"merchantId": "merchant_novatech", "approvedBy": "merchant_demo_user"},
        headers={"Idempotency-Key": "test-approve-1"},
    )
    assert r.status_code == 200, r.text
    approve_body = r.json()
    assert approve_body["experimentId"] == "exp_keyboard_stand"
    assert approve_body["nextRoute"] == "/experiments/exp_keyboard_stand"

    # Idempotent replay returns the same result
    r2 = await client.post(
        "/api/v1/opportunities/opp_keyboard_stand/approve",
        json={"merchantId": "merchant_novatech", "approvedBy": "merchant_demo_user"},
        headers={"Idempotency-Key": "test-approve-1"},
    )
    assert r2.status_code == 200
    assert r2.json() == approve_body

    # 4. Experiment detail
    r = await client.get("/api/v1/experiments/exp_keyboard_stand")
    assert r.status_code == 200, r.text
    assert r.json()["recommendation"] == "scale_variant"

    # 5. Scale experiment
    r = await client.post(
        "/api/v1/experiments/exp_keyboard_stand/scale",
        json={"merchantId": "merchant_novatech", "approvedBy": "merchant_demo_user"},
        headers={"Idempotency-Key": "test-scale-1"},
    )
    assert r.status_code == 200, r.text
    assert r.json()["nextRoute"] == "/ai-commerce"

    # 6. AI Commerce readiness
    r = await client.get("/api/v1/ai-commerce/readiness")
    assert r.status_code == 200
    assert r.json()["score"] == 82

    # 7. AI buyer search
    r = await client.post(
        "/api/v1/ai-buyer/search",
        json={
            "merchantId": "merchant_novatech",
            "buyerRequest": "I need a laptop setup for AI development and college under 70000.",
            "budget": 70000,
        },
    )
    assert r.status_code == 200, r.text
    search_body = r.json()
    assert search_body["total"] == 68499

    # 8. Basket
    r = await client.post(
        "/api/v1/ai-buyer/basket",
        json={
            "merchantId": "merchant_novatech",
            "buyerIntentId": search_body["buyerIntentId"],
            "items": [{"productId": p["productId"], "quantity": 1} for p in search_body["matchedProducts"]],
        },
        headers={"Idempotency-Key": "test-basket-1"},
    )
    assert r.status_code == 200, r.text
    basket_body = r.json()

    # 9. Order intent
    r = await client.post(
        "/api/v1/order-intents",
        json={"merchantId": "merchant_novatech", "basketId": basket_body["basketId"]},
        headers={"Idempotency-Key": "test-intent-1"},
    )
    assert r.status_code == 200, r.text
    intent_id = r.json()["orderIntentId"]

    # Checkout route loads the seeded order intent directly
    r = await client.get("/api/v1/order-intents/intent_ai_setup_001")
    assert r.status_code == 200
    assert r.json()["total"] == 68499

    # 10. Razorpay order (stub mode, no live keys required)
    r = await client.post(
        "/api/v1/payments/razorpay/order",
        json={"merchantId": "merchant_novatech", "orderIntentId": intent_id, "approvedBy": "merchant_demo_user"},
        headers={"Idempotency-Key": "test-rp-order-1"},
    )
    assert r.status_code == 200, r.text
    order_body = r.json()
    assert order_body["environment"] == "Razorpay Test Mode"

    # 11. Verify with a stub-mode signature
    from app.services.razorpay_service import RazorpayService
    from app.core.config import get_settings

    rp = RazorpayService(get_settings())
    fake_payment_id = "pay_demo_success_001"
    signature = rp.sign_stub_payment(order_body["razorpayOrderId"], fake_payment_id)

    r = await client.post(
        "/api/v1/payments/razorpay/verify",
        json={
            "merchantId": "merchant_novatech",
            "orderIntentId": intent_id,
            "razorpayOrderId": order_body["razorpayOrderId"],
            "razorpayPaymentId": fake_payment_id,
            "razorpaySignature": signature,
        },
        headers={"Idempotency-Key": "test-rp-verify-1"},
    )
    assert r.status_code == 200, r.text
    verify_body = r.json()
    assert verify_body["verified"] is True
    assert verify_body["nextRoute"] == "/payment/success"

    # 12. Audit trail reflects the chain
    r = await client.get("/api/v1/audit")
    assert r.status_code == 200
    actions = [e["action"] for e in r.json()["items"]]
    assert "Experiment created" in actions
    assert "Create Order" in actions
    assert "Payment verified" in actions


async def test_payment_failure_path_blocks_retry(client):
    r = await client.post(
        "/api/v1/payments/razorpay/order",
        json={
            "merchantId": "merchant_novatech",
            "orderIntentId": "intent_ai_setup_001",
            "approvedBy": "merchant_demo_user",
        },
        headers={"Idempotency-Key": "test-fail-order-1"},
    )
    assert r.status_code == 200, r.text
    order_body = r.json()

    r = await client.post(
        "/api/v1/payments/razorpay/failure",
        json={
            "merchantId": "merchant_novatech",
            "orderIntentId": "intent_ai_setup_001",
            "razorpayOrderId": order_body["razorpayOrderId"],
            "errorCode": "BAD_REQUEST_ERROR",
            "errorDescription": "Payment attempt was unsuccessful. No funds have been captured from your account.",
        },
        headers={"Idempotency-Key": "test-fail-1"},
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["automaticRetry"] == "blocked"
    assert body["retryBlockedReason"] == "Duplicate-charge protection"
    assert body["nextRoute"] == "/payment/failure"

    r = await client.get("/api/v1/order-intents/intent_ai_setup_001")
    assert r.json()["paymentStatus"] == "failed"

    r = await client.get("/api/v1/audit")
    actions = [e["action"] for e in r.json()["items"]]
    assert "Payment failed" in actions
    assert "Retry Payment" in actions
