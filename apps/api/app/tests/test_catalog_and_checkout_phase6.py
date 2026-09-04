import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_categories_endpoint(client: AsyncClient):
    res = await client.get("/api/v1/categories")
    assert res.status_code == 200
    data = res.json()
    assert "items" in data
    assert data["total"] >= 15
    category_ids = {c["id"] for c in data["items"]}
    assert "LAPTOP" in category_ids
    assert "CPU" in category_ids
    assert "GPU" in category_ids
    assert "MOTHERBOARD" in category_ids
    assert "RAM" in category_ids
    assert "RAM_SLOT" in category_ids
    assert "SSD" in category_ids
    assert "HDD" in category_ids
    assert "CASE" in category_ids


@pytest.mark.asyncio
async def test_product_filtering_and_sorting(client: AsyncClient):
    # Filter by category
    res = await client.get("/api/v1/products?category=CPU")
    assert res.status_code == 200
    cpus = res.json()
    assert cpus["total"] >= 3
    for item in cpus["items"]:
        assert item["categoryId"] == "CPU"

    # Filter by stock
    res_stock = await client.get("/api/v1/products?stock=in_stock")
    assert res_stock.status_code == 200
    for item in res_stock.json()["items"]:
        assert item["inventory"] > 10

    # Search filter
    res_search = await client.get("/api/v1/products?search=Ryzen")
    assert res_search.status_code == 200
    assert res_search.json()["total"] >= 1

    # Readiness score calculation
    res_readiness = await client.get("/api/v1/products?min_readiness=80")
    assert res_readiness.status_code == 200
    for item in res_readiness.json()["items"]:
        assert item["aiReadiness"] >= 80
        assert "readinessBreakdown" in item
        assert "inventoryStatus" in item


@pytest.mark.asyncio
async def test_product_crud_and_audit(client: AsyncClient):
    # 1. Create product
    create_payload = {
        "name": "Nova Ultra Power Supply 850W",
        "categoryId": "ACCESSORIES",
        "price": 11999,
        "inventory": 25,
        "sku": "NT-PSU-850W",
        "brand": "NovaTech",
        "specs": {"wattage": "850W", "efficiency": "80 Plus Gold", "modular": "Fully Modular"},
        "shipping": {"weightKg": 2.1, "dimensionsCm": "20x15x9", "tier": "Standard"},
    }
    res_create = await client.post("/api/v1/products", json=create_payload)
    assert res_create.status_code == 201
    created = res_create.json()
    assert created["name"] == "Nova Ultra Power Supply 850W"
    assert created["aiReadiness"] >= 80
    prod_id = created["id"]

    # 2. Patch product
    res_patch = await client.patch(f"/api/v1/products/{prod_id}", json={"price": 10999})
    assert res_patch.status_code == 200
    assert res_patch.json()["price"] == 10999

    # 3. Stock adjust
    res_adjust = await client.post(
        f"/api/v1/products/{prod_id}/stock-adjust",
        json={"quantity": 30, "reason": "Restocked inventory shipment from distributor"},
    )
    assert res_adjust.status_code == 200
    assert res_adjust.json()["inventory"] == 30

    # 4. Deactivate and Activate
    res_deact = await client.post(f"/api/v1/products/{prod_id}/deactivate")
    assert res_deact.status_code == 200
    assert res_deact.json()["active"] is False

    res_act = await client.post(f"/api/v1/products/{prod_id}/activate")
    assert res_act.status_code == 200
    assert res_act.json()["active"] is True

    # 5. Verify audit log entries
    res_audit = await client.get("/api/v1/audit?limit=20")
    assert res_audit.status_code == 200
    audit_items = res_audit.json()["items"]
    reasons = [a["reason"] for a in audit_items]
    assert any("Nova Ultra Power Supply" in r for r in reasons)


@pytest.mark.asyncio
async def test_checkout_inventory_revalidation_409(client: AsyncClient):
    # Adjust stock of prod_laptop_stand to 0
    await client.post("/api/v1/products/prod_laptop_stand/stock-adjust", json={"quantity": 0})

    # Create basket containing prod_laptop_stand
    res_basket = await client.post(
        "/api/v1/ai-buyer/basket",
        json={"items": [{"productId": "prod_laptop_stand", "quantity": 1}]},
    )
    assert res_basket.status_code == 200
    basket_id = res_basket.json().get("basketId") or res_basket.json().get("id")

    # Attempting to create order intent must return 409 INSUFFICIENT_INVENTORY
    res_intent = await client.post(
        "/api/v1/ai-buyer/order-intent",
        json={"basketId": basket_id, "buyerRequest": "Laptop stand order"},
    )
    assert res_intent.status_code == 409
    body = res_intent.json()
    assert body.get("error", {}).get("code") == "INSUFFICIENT_INVENTORY"


@pytest.mark.asyncio
async def test_payment_verification_decrements_inventory(client: AsyncClient):
    # Set known inventory for prod_probook_14
    await client.post("/api/v1/products/prod_probook_14/stock-adjust", json={"quantity": 40})
    await client.post("/api/v1/products/prod_usb_c_dock/stock-adjust", json={"quantity": 20})
    await client.post("/api/v1/products/prod_laptop_stand/stock-adjust", json={"quantity": 15})

    # Create basket
    res_basket = await client.post(
        "/api/v1/ai-buyer/basket",
        json={
            "items": [
                {"productId": "prod_probook_14", "quantity": 1},
                {"productId": "prod_usb_c_dock", "quantity": 1},
                {"productId": "prod_laptop_stand", "quantity": 1},
            ]
        },
    )
    assert res_basket.status_code == 200
    basket_id = res_basket.json().get("basketId") or res_basket.json().get("id")

    # Create order intent
    res_intent = await client.post(
        "/api/v1/ai-buyer/order-intent",
        json={"basketId": basket_id, "buyerRequest": "Flagship developer bundle"},
    )
    assert res_intent.status_code == 200
    intent_id = res_intent.json().get("orderIntentId") or res_intent.json().get("id")

    # Create Razorpay payment order
    res_rp = await client.post(
        "/api/v1/payments/razorpay/order",
        json={"orderIntentId": intent_id, "approvedBy": "merchant_demo_user"},
    )
    assert res_rp.status_code == 200
    rp_order_id = res_rp.json()["razorpayOrderId"]

    # Verify payment (valid stub HMAC signature)
    import hashlib
    import hmac
    payload = f"{rp_order_id}|pay_test_verified_123".encode("utf-8")
    stub_sig = hmac.new(b"raygo_local_stub_secret", payload, hashlib.sha256).hexdigest()

    res_verify = await client.post(
        "/api/v1/payments/razorpay/verify",
        json={
            "orderIntentId": intent_id,
            "razorpayOrderId": rp_order_id,
            "razorpayPaymentId": "pay_test_verified_123",
            "razorpaySignature": stub_sig,
        },
    )
    assert res_verify.status_code == 200
    assert res_verify.json()["verified"] is True

    # Confirm inventory was decremented
    res_prod = await client.get("/api/v1/products/prod_probook_14")
    assert res_prod.status_code == 200
    assert res_prod.json()["inventory"] == 39  # 40 - 1
