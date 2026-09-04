import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_experiment_timeline_endpoint(client: AsyncClient):
    res = await client.get("/api/v1/experiments/exp_keyboard_stand/timeline")
    assert res.status_code == 200
    data = res.json()
    assert data["experimentId"] == "exp_keyboard_stand"
    assert "timeline" in data
    assert len(data["timeline"]) >= 1


@pytest.mark.asyncio
async def test_policy_guard_sample_size(client: AsyncClient):
    # Test evaluation with insufficient sample size (< 100)
    res_under = await client.post(
        "/api/v1/policies/evaluate",
        json={
            "actionType": "scale_experiment",
            "targetType": "experiment",
            "targetId": "exp_keyboard_stand",
            "proposedAction": {
                "discountPct": 10.0,
                "estimatedMarginPct": 30.0,
                "sampleSize": 45,
            },
        },
    )
    assert res_under.status_code == 200
    data_under = res_under.json()
    assert data_under["outcome"] == "blocked"
    assert any("Sample size" in str(c) for c in data_under["checks"])

    # Test evaluation with sufficient sample size (>= 100)
    res_valid = await client.post(
        "/api/v1/policies/evaluate",
        json={
            "actionType": "scale_experiment",
            "targetType": "experiment",
            "targetId": "exp_keyboard_stand",
            "proposedAction": {
                "discountPct": 10.0,
                "estimatedMarginPct": 30.0,
                "sampleSize": 250,
            },
        },
    )
    assert res_valid.status_code == 200
    data_valid = res_valid.json()
    assert data_valid["outcome"] == "requires_approval"


@pytest.mark.asyncio
async def test_ai_buyer_custom_pc_build_bundler(client: AsyncClient):
    res = await client.post(
        "/api/v1/ai-buyer/search",
        json={"buyerRequest": "I want to build a gaming PC with RTX 4070 and Ryzen processor", "budget": 200000},
    )
    assert res.status_code == 200
    data = res.json()
    assert len(data["matchedProducts"]) >= 3
    matched_names = " ".join([p["name"] for p in data["matchedProducts"]])
    assert "RTX" in matched_names or "Super" in matched_names or "7800" in matched_names or "AMD" in matched_names or "Intel" in matched_names
