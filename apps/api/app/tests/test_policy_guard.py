async def test_discount_over_20pct_is_blocked(client):
    r = await client.post(
        "/api/v1/policies/evaluate",
        json={
            "merchantId": "merchant_novatech",
            "actionType": "create_experiment",
            "targetType": "opportunity",
            "targetId": "opp_keyboard_stand",
            "proposedAction": {"discountPct": 25, "estimatedMarginPct": 30},
        },
    )
    assert r.status_code == 200, r.text
    assert r.json()["outcome"] == "blocked"


async def test_margin_below_25pct_is_blocked(client):
    r = await client.post(
        "/api/v1/policies/evaluate",
        json={
            "merchantId": "merchant_novatech",
            "actionType": "create_experiment",
            "targetType": "opportunity",
            "targetId": "opp_keyboard_stand",
            "proposedAction": {"discountPct": 10, "estimatedMarginPct": 20},
        },
    )
    assert r.status_code == 200, r.text
    assert r.json()["outcome"] == "blocked"


async def test_payment_retry_always_blocked(client):
    r = await client.post(
        "/api/v1/policies/evaluate",
        json={
            "merchantId": "merchant_novatech",
            "actionType": "retry_payment",
            "targetType": "order_intent",
            "targetId": "intent_ai_setup_001",
        },
    )
    assert r.status_code == 200
    assert r.json()["outcome"] == "blocked"


async def test_payment_retry_policy_cannot_be_unlocked(client):
    r = await client.patch(
        "/api/v1/policies/policy_payment_retry",
        json={"merchantId": "merchant_novatech", "status": "active"},
    )
    assert r.status_code == 403
    assert r.json()["error"]["code"] == "POLICY_BLOCKED"


async def test_second_payment_retry_rejected_even_called_directly(client):
    order_resp = await client.post(
        "/api/v1/payments/razorpay/order",
        json={
            "merchantId": "merchant_novatech",
            "orderIntentId": "intent_ai_setup_001",
            "approvedBy": "merchant_demo_user",
        },
        headers={"Idempotency-Key": "retry-test-order-1"},
    )
    assert order_resp.status_code == 200
    razorpay_order_id = order_resp.json()["razorpayOrderId"]

    fail_resp = await client.post(
        "/api/v1/payments/razorpay/failure",
        json={
            "merchantId": "merchant_novatech",
            "orderIntentId": "intent_ai_setup_001",
            "razorpayOrderId": razorpay_order_id,
        },
        headers={"Idempotency-Key": "retry-test-fail-1"},
    )
    assert fail_resp.status_code == 200
    assert fail_resp.json()["automaticRetry"] == "blocked"

    # Calling the Policy Guard evaluate endpoint directly for a retry on the
    # same order intent is blocked regardless of who calls it.
    retry_eval = await client.post(
        "/api/v1/policies/evaluate",
        json={
            "merchantId": "merchant_novatech",
            "actionType": "retry_payment",
            "targetType": "order_intent",
            "targetId": "intent_ai_setup_001",
        },
    )
    assert retry_eval.json()["outcome"] == "blocked"
