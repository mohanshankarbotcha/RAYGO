import uuid
from typing import Any

from app.domain.constants import AUDIT_OUTCOME_SUCCESS, SEVERITY_INFO
from app.repositories.registry import Repositories


def new_audit_id() -> str:
    return f"audit_{uuid.uuid4().hex[:10]}"


class AuditService:
    """Product-visible record of every consequential decision. Never stores
    hidden chain-of-thought — only concise, reconstructable decision summaries."""

    def __init__(self, repos: Repositories):
        self.repos = repos

    async def record(
        self,
        merchant_id: str,
        agent: str,
        action: str,
        reason: str,
        policy: str = "Passed",
        approval: str = "N/A",
        outcome: str = AUDIT_OUTCOME_SUCCESS,
        severity: str = SEVERITY_INFO,
        correlation_ids: dict[str, Any] | None = None,
        details: dict[str, Any] | None = None,
        event_id: str | None = None,
    ) -> dict:
        doc = {
            "id": event_id or new_audit_id(),
            "merchantId": merchant_id,
            "timestamp": None,  # set to createdAt by upsert below
            "agent": agent,
            "action": action,
            "reason": reason,
            "policy": policy,
            "approval": approval,
            "outcome": outcome,
            "severity": severity,
            "correlationIds": correlation_ids or {},
            "details": details or {"decisionSummary": reason},
            "metadata": {},
        }
        saved = await self.repos.audit_events.upsert(doc)
        # timestamp mirrors createdAt for the audit list/detail contract
        if saved and not saved.get("timestamp"):
            saved = await self.repos.audit_events.update(saved["id"], {"timestamp": saved["createdAt"]})
        return saved
