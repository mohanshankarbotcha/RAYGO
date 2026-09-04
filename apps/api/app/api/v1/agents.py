from fastapi import APIRouter, Depends

from app.api.deps import get_audit_service, get_repos
from app.core.config import Settings, get_settings
from app.db.seed import AGENT_STATUS
from app.domain.agent_schemas import CoordinatorOutput
from app.domain.constants import AGENT_SYSTEM
from app.domain.schemas import CamelModel
from app.domain.tool_registry import list_tools
from app.repositories.registry import Repositories
from app.services.audit_service import AuditService
from app.services.coordinator import RaygoCoordinator
from app.services.providers.factory import build_primary_provider

router = APIRouter(tags=["agents"])


class CoordinateRequest(CamelModel):
    merchant_id: str = "merchant_novatech"
    request_text: str


@router.get("/agents/status")
async def agents_status(settings: Settings = Depends(get_settings)):
    return {"items": AGENT_STATUS, "mockAgents": settings.use_mock_agents}


@router.get("/agents/activity")
async def agents_activity(limit: int = 50, repos: Repositories = Depends(get_repos)):
    items = await repos.agent_activity.find_many({}, limit=limit, sort=[("time", 1)])
    slim = [
        {
            "id": e["id"],
            "time": e["time"],
            "agent": e["agent"],
            "message": e["message"],
            "auditEventId": e.get("auditEventId"),
            "agentRunId": e.get("agentRunId") or f"run_{e['id'][:8]}",
            "correlationId": e.get("correlationId"),
        }
        for e in items
    ]
    return {"items": slim, "total": len(slim), "nextCursor": None}


@router.get("/agents/runs")
async def get_agent_runs(
    correlation_id: str | None = None,
    limit: int = 50,
    repos: Repositories = Depends(get_repos),
):
    query = {"correlationId": correlation_id} if correlation_id else {}
    runs = await repos.agent_runs.find_many(query, limit=limit, sort=[("startedAt", -1)])
    return {"items": runs, "total": len(runs)}


@router.get("/agents/tools")
async def agents_tools():
    return {"items": list_tools(), "total": len(list_tools())}


@router.get("/agents/gemini/health")
async def gemini_health(settings: Settings = Depends(get_settings)):
    provider = build_primary_provider(settings)
    health = await provider.health()
    return {
        **health,
        "mockAgents": settings.use_mock_agents,
        "model": settings.gemini_model if health["provider"] == "gemini" else None,
    }


@router.post("/agents/coordinate")
async def coordinate(
    body: CoordinateRequest,
    settings: Settings = Depends(get_settings),
    repos: Repositories = Depends(get_repos),
    audit: AuditService = Depends(get_audit_service),
):
    """Advisory routing only. Never executes a tool, mutates data, or
    touches payments — see RaygoCoordinator docstring."""
    from app.services.agent_run_tracker import AgentRunTracker

    async with AgentRunTracker(
        repos,
        agent_name="RAYGO Coordinator",
        task_type="coordinator_route",
        input_reference=body.request_text,
    ) as run:
        run.record_tool_call("coordinator_route", "READ_ONLY")
        coordinator = RaygoCoordinator(settings)
        result, mode, fallback_reason = await coordinator.route(body.request_text)
        run.set_output_reference(result.agent)

        event = await audit.record(
            merchant_id=body.merchant_id,
            agent=AGENT_SYSTEM,
            action="Coordinator routed request",
            reason=result.reason,
            outcome="Success",
            correlation_ids={"agentRunId": run.agent_run_id},
            details={
                "decisionSummary": result.reason,
                "intent": result.intent,
                "routedAgent": result.agent,
                "reasoningMode": mode,
                "reasoningFallbackReason": fallback_reason,
            },
        )
        return {
            **result.model_dump(by_alias=True),
            "mode": mode,
            "fallbackReason": fallback_reason,
            "auditEventId": event["id"],
            "agentRunId": run.agent_run_id,
        }


class CopilotAskRequest(CamelModel):
    merchant_id: str = "merchant_novatech"
    question: str


@router.post("/agents/copilot/ask")
async def copilot_ask(
    body: CopilotAskRequest,
    repos: Repositories = Depends(get_repos),
    audit: AuditService = Depends(get_audit_service),
):
    from app.services.copilot_service import CopilotService
    from app.services.agent_run_tracker import AgentRunTracker

    async with AgentRunTracker(
        repos,
        agent_name="RAYGO Copilot",
        task_type="copilot_ask",
        input_reference=body.question[:60],
    ) as run:
        run.record_tool_call("copilot_ask", "READ_ONLY")
        copilot = CopilotService(repos=repos, audit=audit)
        response = await copilot.ask(body.merchant_id, body.question)
        run.set_output_reference(response.intent)
        return response.model_dump(by_alias=True)


