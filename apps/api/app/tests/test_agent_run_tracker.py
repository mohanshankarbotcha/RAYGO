import pytest
from httpx import AsyncClient

from app.services.agent_run_tracker import AgentRunTracker


@pytest.mark.asyncio
async def test_agent_run_tracker_lifecycle(test_db):
    from app.repositories.registry import get_repositories

    repos = get_repositories(test_db)
    correlation_id = "corr_lifecycle_test"

    async with AgentRunTracker(
        repos=repos,
        agent_name="Test Agent",
        task_type="unit_test_run",
        correlation_id=correlation_id,
        input_reference="test_input_1",
    ) as tracker:
        tracker.record_tool_call("sample_tool", "READ_ONLY")
        tracker.link_policy_evaluation("eval_123")
        tracker.link_approval("appr_456")
        tracker.set_output_reference("test_output_1")

    # Verify run persisted in database
    run = await repos.agent_runs.get(tracker.agent_run_id)
    assert run is not None
    assert run["agentName"] == "Test Agent"
    assert run["status"] == "completed"
    assert run["correlationId"] == correlation_id
    assert run["policyEvaluationId"] == "eval_123"
    assert run["approvalId"] == "appr_456"
    assert run["outputReference"] == "test_output_1"
    assert len(run["toolCalls"]) == 1
    assert run["toolCalls"][0]["toolName"] == "sample_tool"


@pytest.mark.asyncio
async def test_agent_run_tracker_records_failure_on_exception(test_db):
    from app.repositories.registry import get_repositories
    from app.core.errors import NotFoundError

    repos = get_repositories(test_db)

    with pytest.raises(NotFoundError):
        async with AgentRunTracker(
            repos=repos,
            agent_name="Failing Agent",
            task_type="fail_test",
        ) as tracker:
            raise NotFoundError("Resource not found.")

    run = await repos.agent_runs.get(tracker.agent_run_id)
    assert run is not None
    assert run["status"] == "failed"
    assert run["errorCode"] is not None


@pytest.mark.asyncio
async def test_get_agent_runs_api(client: AsyncClient):
    # Trigger an agent action
    coord_res = await client.post(
        "/api/v1/agents/coordinate",
        json={"merchantId": "merchant_novatech", "requestText": "How can I increase sales on keyboards?"},
    )
    assert coord_res.status_code == 200
    agent_run_id = coord_res.json()["agentRunId"]

    # Query /agents/runs
    runs_res = await client.get("/api/v1/agents/runs")
    assert runs_res.status_code == 200
    runs = runs_res.json()
    assert runs["total"] >= 1
    assert any(r["id"] == agent_run_id or r.get("agentRunId") == agent_run_id for r in runs["items"])
