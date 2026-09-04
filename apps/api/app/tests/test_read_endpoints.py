async def test_products_list(client):
    r = await client.get("/api/v1/products")
    assert r.status_code == 200, r.text
    assert r.json()["total"] >= 7


async def test_opportunities_list_ranked(client):
    r = await client.get("/api/v1/opportunities")
    assert r.status_code == 200
    items = r.json()["items"]
    assert items[0]["id"] == "opp_keyboard_stand"
    assert len(items) == 7


async def test_experiments_list(client):
    r = await client.get("/api/v1/experiments")
    assert r.status_code == 200
    assert r.json()["summary"]["averageConfidence"] == 94


async def test_policies_list_and_action_matrix(client):
    r = await client.get("/api/v1/policies")
    assert r.status_code == 200
    body = r.json()
    assert len(body["items"]) == 6
    assert len(body["actionMatrix"]) == 5


async def test_agents_status_and_activity(client):
    r = await client.get("/api/v1/agents/status")
    assert r.status_code == 200
    assert len(r.json()["items"]) == 8

    r2 = await client.get("/api/v1/agents/activity")
    assert r2.status_code == 200
    assert r2.json()["total"] == 7


async def test_ai_commerce_product_profile(client):
    r = await client.get("/api/v1/ai-commerce/products/prod_laptop_stand/profile")
    assert r.status_code == 200, r.text
    assert r.json()["profile"]["missingMetadata"] == ["Shipping metadata"]


async def test_orders_and_payments_empty_but_valid(client):
    r = await client.get("/api/v1/orders")
    assert r.status_code == 200
    assert r.json()["summary"]["gmv"] == 0

    r2 = await client.get("/api/v1/payments")
    assert r2.status_code == 200
    assert r2.json()["summary"]["successful"] == 0


async def test_openapi_schema_generates(client):
    r = await client.get("/openapi.json")
    assert r.status_code == 200
    assert r.json()["info"]["title"] == "RAYGO API"
