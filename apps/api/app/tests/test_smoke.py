async def test_health(client):
    r = await client.get("/api/v1/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


async def test_health_db(client):
    r = await client.get("/api/v1/health/db")
    assert r.status_code == 200
    assert r.json()["connected"] is True


async def test_merchant(client):
    r = await client.get("/api/v1/merchant")
    assert r.status_code == 200, r.text
    assert r.json()["id"] == "merchant_novatech"
