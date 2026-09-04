from fastapi import APIRouter, Depends, Request

from app.api.deps import get_repos
from app.core.errors import NotFoundError
from app.core.security import resolve_merchant_id
from app.repositories.registry import Repositories

router = APIRouter(tags=["audit"])


@router.get("/audit")
async def list_audit(
    request: Request,
    agent: str | None = None,
    severity: str | None = None,
    outcome: str | None = None,
    limit: int = 50,
    repos: Repositories = Depends(get_repos),
):
    merchant_id = resolve_merchant_id(request)
    query: dict = {"merchantId": merchant_id}
    if agent:
        query["agent"] = agent
    if severity:
        query["severity"] = severity
    if outcome:
        query["outcome"] = outcome
    items = await repos.audit_events.find_many(query, limit=limit, sort=[("timestamp", -1)])
    slim = [
        {
            "id": e["id"],
            "timestamp": e["timestamp"],
            "agent": e["agent"],
            "action": e["action"],
            "reason": e["reason"],
            "policy": e["policy"],
            "approval": e["approval"],
            "outcome": e["outcome"],
            "severity": e["severity"],
        }
        for e in items
    ]
    return {"items": slim, "total": len(slim), "nextCursor": None}


@router.get("/audit/{audit_event_id}")
async def get_audit_event(audit_event_id: str, repos: Repositories = Depends(get_repos)):
    event = await repos.audit_events.get(audit_event_id)
    if not event:
        raise NotFoundError("Audit event not found.", {"auditEventId": audit_event_id})
    return {
        "id": event["id"],
        "timestamp": event["timestamp"],
        "agent": event["agent"],
        "action": event["action"],
        "reason": event["reason"],
        "policy": event["policy"],
        "approval": event["approval"],
        "outcome": event["outcome"],
        "severity": event["severity"],
        "correlationIds": event.get("correlationIds", {}),
        "details": event.get("details", {}),
    }
