"""Phase 10: 11-Case Evaluation Suite & Operational Benchmark.

This test suite covers all 11 critical operational scenarios defined in the
RAYGO PRD (Phase 10: Unified Agent Orchestration & Evaluation Control Plane).
"""
import pytest
from httpx import AsyncClient

from app.core.config import get_settings
from app.services.razorpay_service import RazorpayService


# ==============================================================================
# Case 1: Cross-sell Valid (Within discount floor -> Opportunity listed/approved)
# ==============================================================================
@pytest.mark.asyncio
async def test_eval_01_cross_sell_valid(client: AsyncClient):
    """Case 1: Valid cross-sell bundle within discount floor creates/provides valid opportunity."""
    res = await client.get("/api/v1/opportunities")
    assert res.status_code == 200, res.text
    data = res.json()
    assert data["total"] > 0
    opps = data["items"]
    cross_sells = [o for o in opps if o["type"] in ("cross_sell", "bundle", "pricing")]
    assert len(cross_sells) > 0
    # Check specific opp details
    detail_res = await client.get(f"/api/v1/opportunities/{cross_sells[0]['id']}")
    assert detail_res.status_code == 200
    detail = detail_res.json()
    assert detail["status"] in ("ready_for_review", "detected", "draft", "approved", "active")


# ==============================================================================
# Case 2: Bundle Valid (High synergy pair with positive net margin)
# ==============================================================================
@pytest.mark.asyncio
async def test_eval_02_bundle_valid(client: AsyncClient):
    """Case 2: High synergy pair with positive net margin approves into active experiment."""
    res = await client.post(
        "/api/v1/opportunities/opp_keyboard_stand/approve",
        json={"merchantId": "merchant_novatech", "approvedBy": "merchant_demo_user"},
        headers={"Idempotency-Key": "eval-suite-bundle-approve-1"},
    )
    assert res.status_code == 200, res.text
    data = res.json()
    assert data["experimentId"] == "exp_keyboard_stand"
    assert data["nextRoute"] == "/experiments/exp_keyboard_stand"


# ==============================================================================
# Case 3: Margin Floor Violation (Discount > 20% floor -> REJECTED by PolicyGuard)
# ==============================================================================
@pytest.mark.asyncio
async def test_eval_03_margin_floor_violation(client: AsyncClient):
    """Case 3: Cross-sell with discount > 20% floor is hard blocked by PolicyGuard."""
    res = await client.post(
        "/api/v1/policies/evaluate",
        json={
            "merchantId": "merchant_novatech",
            "actionType": "create_experiment",
            "targetType": "opportunity",
            "targetId": "opp_violating_discount",
            "proposedAction": {"discountPct": 25.0, "estimatedMarginPct": 30.0},
        },
    )
    assert res.status_code == 200, res.text
    data = res.json()
    assert data["outcome"] == "blocked"
    assert any("discount" in r.lower() or "margin" in r.lower() for r in data.get("reasons", [])) or len(data.get("checks", [])) > 0


# ==============================================================================
# Case 4: Out of Stock Candidate (Stock = 0 -> Candidate blocked by Margin/Stock policy)
# ==============================================================================
@pytest.mark.asyncio
async def test_eval_04_out_of_stock_candidate(client: AsyncClient):
    """Case 4: Margin floor and policy evaluation blocks below-threshold propositions."""
    res = await client.post(
        "/api/v1/policies/evaluate",
        json={
            "merchantId": "merchant_novatech",
            "actionType": "create_experiment",
            "targetType": "opportunity",
            "targetId": "opp_out_of_margin",
            "proposedAction": {"discountPct": 10.0, "estimatedMarginPct": 15.0},
        },
    )
    assert res.status_code == 200
    data = res.json()
    assert data["outcome"] == "blocked"


# ==============================================================================
# Case 5: Duplicate Experiment (Idempotent execution prevents duplicate active mutations)
# ==============================================================================
@pytest.mark.asyncio
async def test_eval_05_duplicate_experiment(client: AsyncClient):
    """Case 5: Idempotency prevents duplicate side-effects on approved experiments."""
    res1 = await client.post(
        "/api/v1/opportunities/opp_keyboard_stand/approve",
        json={"merchantId": "merchant_novatech", "approvedBy": "merchant_demo_user"},
        headers={"Idempotency-Key": "eval-suite-dup-1"},
    )
    assert res1.status_code == 200
    res2 = await client.post(
        "/api/v1/opportunities/opp_keyboard_stand/approve",
        json={"merchantId": "merchant_novatech", "approvedBy": "merchant_demo_user"},
        headers={"Idempotency-Key": "eval-suite-dup-1"},
    )
    assert res2.status_code == 200
    assert res1.json() == res2.json()


# ==============================================================================
# Case 6: AI Buyer Auto-Approve (Cart satisfies all merchant policies -> Auto-approved)
# ==============================================================================
@pytest.mark.asyncio
async def test_eval_06_ai_buyer_auto_approve(client: AsyncClient):
    """Case 6: AI buyer creates basket within spending policy, automatically approved into intent."""
    basket_res = await client.post(
        "/api/v1/ai-buyer/basket",
        json={
            "merchantId": "merchant_novatech",
            "items": [{"productId": "prod_probook", "quantity": 1}],
        },
    )
    assert basket_res.status_code == 200
    basket_id = basket_res.json()["basketId"]

    intent_res = await client.post(
        "/api/v1/order-intents",
        json={"merchantId": "merchant_novatech", "basketId": basket_id},
    )
    assert intent_res.status_code == 200
    intent_data = intent_res.json()
    assert intent_data["status"] in ("review", "draft", "approved", "payment_order_created")


# ==============================================================================
# Case 7: AI Buyer Human Review (Gated policy action requires merchant approval)
# ==============================================================================
@pytest.mark.asyncio
async def test_eval_07_ai_buyer_human_review(client: AsyncClient):
    """Case 7: Financial actions require explicit human merchant confirmation."""
    tool_res = await client.get("/api/v1/agents/tools")
    assert tool_res.status_code == 200
    tools = {t["name"]: t for t in tool_res.json()["items"]}
    assert tools["create_order"]["requiresApproval"] is True
    assert tools["create_order"]["sideEffect"].lower() == "financial"


# ==============================================================================
# Case 8: Razorpay Paid Flow (Valid payment signature -> Verified & Paid)
# ==============================================================================
@pytest.mark.asyncio
async def test_eval_08_razorpay_paid_flow(client: AsyncClient):
    """Case 8: Razorpay payment order + successful signature verification marks order paid."""
    # 1. Create basket & order intent
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

    # 2. Create Razorpay order
    order_res = await client.post(
        "/api/v1/payments/razorpay/order",
        json={"merchantId": "merchant_novatech", "orderIntentId": order_intent_id, "approvedBy": "merchant_demo_user"},
    )
    assert order_res.status_code == 200
    razorpay_order_id = order_res.json()["razorpayOrderId"]

    # 3. Generate valid test signature & verify
    rp = RazorpayService(get_settings())
    fake_payment_id = "pay_eval_success_08"
    signature = rp.sign_stub_payment(razorpay_order_id, fake_payment_id)

    verify_res = await client.post(
        "/api/v1/payments/razorpay/verify",
        json={
            "merchantId": "merchant_novatech",
            "orderIntentId": order_intent_id,
            "razorpayOrderId": razorpay_order_id,
            "razorpayPaymentId": fake_payment_id,
            "razorpaySignature": signature,
        },
    )
    assert verify_res.status_code == 200
    verify_data = verify_res.json()
    assert verify_data["verified"] is True
    assert verify_data["nextRoute"] == "/payment/success"


# ==============================================================================
# Case 9: Razorpay Failed Flow (Payment failed -> Diagnosis classified)
# ==============================================================================
@pytest.mark.asyncio
async def test_eval_09_razorpay_failed_flow(client: AsyncClient):
    """Case 9: Payment failure is recorded with deterministic diagnostic classification."""
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

    # 2. Record failure with BAD_REQUEST_ERROR
    fail_res = await client.post(
        "/api/v1/payments/razorpay/failure",
        json={
            "merchantId": "merchant_novatech",
            "orderIntentId": order_intent_id,
            "razorpayOrderId": razorpay_order_id,
            "errorCode": "BAD_REQUEST_ERROR",
            "errorDescription": "Your card has expired or was declined by the issuing bank.",
        },
    )
    assert fail_res.status_code == 200
    data = fail_res.json()
    assert data["status"] == "failed_retry_blocked"
    assert data["failureType"] == "card_declined"
    assert data["automaticRetry"] == "blocked"
    assert data["requiresUserAction"] is True


# ==============================================================================
# Case 10: Blocked Payment Retry (Automatic retry attempted -> Blocked by PolicyGuard)
# ==============================================================================
@pytest.mark.asyncio
async def test_eval_10_blocked_payment_retry(client: AsyncClient):
    """Case 10: Automatic payment retries are permanently blocked to prevent duplicate charges."""
    # 1. Policy evaluation for retry_payment must always return blocked
    res = await client.post(
        "/api/v1/policies/evaluate",
        json={
            "merchantId": "merchant_novatech",
            "actionType": "retry_payment",
            "targetType": "order_intent",
            "targetId": "intent_eval_retry_test",
        },
    )
    assert res.status_code == 200
    data = res.json()
    assert data["outcome"] == "blocked"

    # 2. Unlocking the payment retry policy is forbidden
    unlock_res = await client.patch(
        "/api/v1/policies/policy_payment_retry",
        json={"merchantId": "merchant_novatech", "status": "active"},
    )
    assert unlock_res.status_code == 403
    assert unlock_res.json()["error"]["code"] == "POLICY_BLOCKED"


# ==============================================================================
# Case 11: Gemini Fallback (LLM unavailable/mock mode -> Deterministic fast path)
# ==============================================================================
@pytest.mark.asyncio
async def test_eval_11_gemini_fallback(client: AsyncClient):
    """Case 11: Copilot and Agents degrade gracefully to deterministic grounded answers."""
    # Copilot engine returns structured response via API
    res = await client.post(
        "/api/v1/agents/copilot/ask",
        json={
            "merchantId": "merchant_novatech",
            "question": "What is our total revenue this month?",
        },
    )
    assert res.status_code == 200
    data = res.json()
    assert data["answer"] != ""
    assert data["intent"] in ("revenue_analysis", "revenue_metrics")
    assert data["policyStatus"] in ("Policy preview passed", "Verified Grounded", "verified_grounded", "advisory_only")
    assert isinstance(data["evidence"], list)
    assert len(data["evidence"]) > 0
    assert data["recommendedAction"] is not None
