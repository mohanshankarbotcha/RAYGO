import time

import pytest


# ---------------------------------------------------------------------------
# AG-063 Campaign budget exceeded (Daily Budget policy, now enforced)
# ---------------------------------------------------------------------------

async def test_campaign_budget_within_limit_passes(client):
    r = await client.post(
        "/api/v1/policies/evaluate",
        json={
            "merchantId": "merchant_novatech",
            "actionType": "create_campaign",
            "targetType": "opportunity",
            "targetId": "opp_recovery_campaign",
            "proposedAction": {"campaignSpend": 4000},
        },
    )
    assert r.status_code == 200, r.text
    assert r.json()["outcome"] != "blocked"


async def test_campaign_budget_exceeded_is_blocked(client):
    r = await client.post(
        "/api/v1/policies/evaluate",
        json={
            "merchantId": "merchant_novatech",
            "actionType": "create_campaign",
            "targetType": "opportunity",
            "targetId": "opp_recovery_campaign",
            "proposedAction": {"campaignSpend": 12000},
        },
    )
    assert r.status_code == 200, r.text
    assert r.json()["outcome"] == "blocked"


async def test_campaign_budget_accumulates_across_calls_same_day(client):
    # Two separate proposals that individually fit, but together exceed
    # the ₹10,000 daily limit, must be blocked on the second call.
    r1 = await client.post(
        "/api/v1/policies/evaluate",
        json={
            "merchantId": "merchant_novatech",
            "actionType": "create_campaign",
            "targetType": "opportunity",
            "targetId": "opp_headphones_upsell",
            "proposedAction": {"campaignSpend": 6000},
        },
    )
    assert r1.json()["outcome"] != "blocked"

    r2 = await client.post(
        "/api/v1/policies/evaluate",
        json={
            "merchantId": "merchant_novatech",
            "actionType": "create_campaign",
            "targetType": "opportunity",
            "targetId": "opp_monitor_bundle",
            "proposedAction": {"campaignSpend": 5000},
        },
    )
    assert r2.json()["outcome"] == "blocked"


# ---------------------------------------------------------------------------
# AG-072 Approval rejected / AG-074 Unauthorized approval rejected
# ---------------------------------------------------------------------------

async def test_opportunity_rejection_is_recorded(client):
    r = await client.post(
        "/api/v1/opportunities/opp_probook_bundle/reject",
        json={"merchantId": "merchant_novatech", "rejectedBy": "merchant_demo_user", "reason": "Not this month."},
        headers={"Idempotency-Key": "reject-opp-1"},
    )
    assert r.status_code == 200, r.text
    assert r.json()["status"] == "declined"

    detail = await client.get("/api/v1/opportunities/opp_probook_bundle")
    assert detail.json()["status"] == "declined"

    audit = await client.get("/api/v1/audit")
    actions = [e["action"] for e in audit.json()["items"]]
    assert "Opportunity rejected" in actions


async def test_experiment_reject_keeps_it_running(client):
    r = await client.post(
        "/api/v1/experiments/exp_keyboard_stand/reject",
        json={"merchantId": "merchant_novatech", "rejectedBy": "merchant_demo_user"},
        headers={"Idempotency-Key": "reject-exp-1"},
    )
    assert r.status_code == 200, r.text
    exp = await client.get("/api/v1/experiments/exp_keyboard_stand")
    assert exp.json()["status"] == "running"


async def test_unauthorized_approver_is_rejected(client):
    r = await client.post(
        "/api/v1/opportunities/opp_recovery_campaign/approve",
        json={"merchantId": "merchant_novatech", "approvedBy": "random_unverified_user"},
        headers={"Idempotency-Key": "unauth-approve-1"},
    )
    assert r.status_code == 403, r.text
    assert r.json()["error"]["code"] == "UNAUTHORIZED_APPROVER"

    # And nothing was mutated as a side effect of the rejected attempt.
    opp = await client.get("/api/v1/opportunities/opp_recovery_campaign")
    assert opp.json()["status"] != "experiment_created"


async def test_unauthorized_rejecter_is_rejected(client):
    r = await client.post(
        "/api/v1/opportunities/opp_recovery_campaign/reject",
        json={"merchantId": "merchant_novatech", "rejectedBy": "some_other_person"},
        headers={"Idempotency-Key": "unauth-reject-1"},
    )
    assert r.status_code == 403
    assert r.json()["error"]["code"] == "UNAUTHORIZED_APPROVER"


# ---------------------------------------------------------------------------
# AG-045 Insufficient-data handling
# ---------------------------------------------------------------------------

async def test_experiment_recommendation_for_low_confidence_opportunity_stays_conservative(client):
    # opp_seasonal_reactivation is seeded with confidence 63 and no
    # evidence/attach-rate data -- the deterministic template must not
    # invent a confident SCALE recommendation from nothing.
    r = await client.get("/api/v1/opportunities/opp_seasonal_reactivation/reasoning")
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["confidence"] == pytest.approx(0.63)
    assert body["requiresApproval"] is True


# ---------------------------------------------------------------------------
# AG-091 Event ordering / AG-104 Correlation ID consistency
# ---------------------------------------------------------------------------

async def test_agent_activity_events_are_chronologically_ordered(client):
    r = await client.get("/api/v1/agents/activity")
    assert r.status_code == 200
    times = [e["time"] for e in r.json()["items"]]
    assert times == sorted(times)


async def test_correlation_ids_are_consistent_across_the_payment_chain(client):
    order_resp = await client.post(
        "/api/v1/payments/razorpay/order",
        json={
            "merchantId": "merchant_novatech",
            "orderIntentId": "intent_ai_setup_001",
            "approvedBy": "merchant_demo_user",
        },
        headers={"Idempotency-Key": "corr-order-1"},
    )
    assert order_resp.status_code == 200
    order_body = order_resp.json()
    razorpay_order_id = order_body["razorpayOrderId"]
    payment_attempt_id = order_body["paymentAttemptId"]

    audit = await client.get("/api/v1/audit")
    create_order_events = [e for e in audit.json()["items"] if e["action"] == "Create Order"]
    assert create_order_events, "expected a 'Create Order' audit event"

    detail = await client.get(f"/api/v1/audit/{create_order_events[0]['id']}")
    correlation_ids = detail.json()["correlationIds"]
    assert correlation_ids["orderId"] == razorpay_order_id
    assert correlation_ids["paymentAttemptId"] == payment_attempt_id
    assert correlation_ids["orderIntentId"] == "intent_ai_setup_001"


# ---------------------------------------------------------------------------
# AG-114 Database unavailable
# ---------------------------------------------------------------------------

async def test_health_db_reports_disconnected_when_db_ping_fails(client, monkeypatch):
    class FailingDb:
        async def command(self, *args, **kwargs):
            raise ConnectionError("simulated database outage")

    import app.main as main_module

    original_db = main_module.app.state.db
    main_module.app.state.db = FailingDb()
    try:
        r = await client.get("/api/v1/health/db")
        assert r.status_code == 200  # health endpoint itself never crashes
        body = r.json()
        assert body["connected"] is False
        assert body["status"] == "error"
    finally:
        main_module.app.state.db = original_db


# ---------------------------------------------------------------------------
# AG-125 Sensitive data exposure — no response body ever contains a secret
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "method,path,json_body",
    [
        ("GET", "/api/v1/merchant", None),
        ("GET", "/api/v1/dashboard/overview", None),
        ("GET", "/api/v1/opportunities", None),
        ("GET", "/api/v1/opportunities/opp_keyboard_stand", None),
        ("GET", "/api/v1/experiments/exp_keyboard_stand", None),
        ("GET", "/api/v1/policies", None),
        ("GET", "/api/v1/payments", None),
        ("GET", "/api/v1/orders", None),
        ("GET", "/api/v1/audit", None),
        ("GET", "/api/v1/agents/status", None),
        ("GET", "/api/v1/agents/gemini/health", None),
    ],
)
async def test_no_response_body_leaks_secrets(client, method, path, json_body):
    r = await client.request(method, path, json=json_body)
    text = r.text.lower()
    for forbidden in ("gemini_api_key", "razorpay_key_secret", "razorpay_webhook_secret"):
        assert forbidden not in text


# ---------------------------------------------------------------------------
# PERF-* smoke tests. These measure our own code path over mongomock, i.e.
# they catch accidental O(n^2)/N+1 regressions and unbounded loops — they
# are not a substitute for real network-latency measurement against a real
# MongoDB/Gemini, which needs a live environment this sandbox doesn't have.
# Thresholds are generous on purpose: the point is regression detection,
# not asserting a specific production SLA.
# ---------------------------------------------------------------------------

async def _timed(coro_fn):
    started = time.perf_counter()
    result = await coro_fn()
    elapsed_ms = (time.perf_counter() - started) * 1000
    return result, elapsed_ms


@pytest.mark.parametrize(
    "path",
    [
        "/api/v1/dashboard/overview",
        "/api/v1/opportunities",
        "/api/v1/opportunities/opp_keyboard_stand",
        "/api/v1/experiments",
        "/api/v1/policies",
        "/api/v1/payments",
        "/api/v1/orders",
        "/api/v1/agents/activity",
        "/api/v1/audit",
    ],
)
async def test_read_endpoint_responds_quickly_against_mongomock(client, path):
    _, elapsed_ms = await _timed(lambda: client.get(path))
    # Generous local ceiling (mongomock + in-process ASGI transport, no real
    # network) -- this is a regression guard against an accidental N+1 or
    # unbounded loop, not a production latency claim.
    assert elapsed_ms < 500, f"{path} took {elapsed_ms:.1f}ms against mongomock (ceiling 500ms)"


async def test_policy_evaluate_is_fast(client):
    _, elapsed_ms = await _timed(
        lambda: client.post(
            "/api/v1/policies/evaluate",
            json={
                "merchantId": "merchant_novatech",
                "actionType": "create_experiment",
                "targetType": "opportunity",
                "targetId": "opp_keyboard_stand",
                "proposedAction": {"discountPct": 10, "estimatedMarginPct": 30},
            },
        )
    )
    assert elapsed_ms < 200, f"policy evaluate took {elapsed_ms:.1f}ms (ceiling 200ms)"


async def test_coordinator_route_is_fast_on_deterministic_path(client):
    _, elapsed_ms = await _timed(
        lambda: client.post(
            "/api/v1/agents/coordinate",
            json={"merchantId": "merchant_novatech", "requestText": "show me revenue opportunities"},
        )
    )
    # Deterministic path only -- no network call -- should be near-instant.
    assert elapsed_ms < 200, f"coordinate took {elapsed_ms:.1f}ms (ceiling 200ms) on deterministic path"


async def test_payments_list_avoids_sequential_n_plus_one(client):
    # Create several payment attempts against the same seeded order intent
    # so list_payments has repeated orderIntentId values to dedupe/batch.
    for i in range(5):
        await client.post(
            "/api/v1/payments/razorpay/order",
            json={
                "merchantId": "merchant_novatech",
                "orderIntentId": "intent_ai_setup_001",
                "approvedBy": "merchant_demo_user",
            },
            headers={"Idempotency-Key": f"perf-order-{i}"},
        )
    _, elapsed_ms = await _timed(lambda: client.get("/api/v1/payments"))
    assert elapsed_ms < 300, f"payments list took {elapsed_ms:.1f}ms (ceiling 300ms)"
