async def test_idempotency_key_reuse_with_different_body_conflicts(client):
    r1 = await client.post(
        "/api/v1/opportunities/opp_probook_bundle/approve",
        json={"merchantId": "merchant_novatech", "approvedBy": "merchant_demo_user"},
        headers={"Idempotency-Key": "conflict-test-1"},
    )
    assert r1.status_code == 200, r1.text

    r2 = await client.post(
        "/api/v1/opportunities/opp_probook_bundle/approve",
        json={"merchantId": "merchant_novatech", "approvedBy": "a_completely_different_approver"},
        headers={"Idempotency-Key": "conflict-test-1"},
    )
    assert r2.status_code == 409
    assert r2.json()["error"]["code"] == "IDEMPOTENCY_CONFLICT"


async def test_not_found_returns_stable_envelope(client):
    r = await client.get("/api/v1/opportunities/opp_does_not_exist")
    assert r.status_code == 404
    body = r.json()
    assert body["error"]["code"] == "NOT_FOUND"
    assert "requestId" in body["error"]
