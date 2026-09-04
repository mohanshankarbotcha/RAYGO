from fastapi import APIRouter, Depends, Header, Request

from app.api.deps import get_audit_service, get_policy_guard, get_repos
from app.core.errors import NotFoundError, PolicyBlockedError
from app.core.idempotency import IdempotencyService
from app.core.security import resolve_merchant_id
from app.db.seed import ACTION_MATRIX
from app.domain.constants import AGENT_SYSTEM, POLICY_PAYMENT_RETRY
from app.domain.schemas import PolicyEvaluateRequest, PolicyPatchRequest
from app.repositories.registry import Repositories
from app.services.audit_service import AuditService
from app.services.policy_guard import PolicyGuard

router = APIRouter(tags=["policies"])


@router.get("/policies")
async def list_policies(request: Request, repos: Repositories = Depends(get_repos)):
    merchant_id = resolve_merchant_id(request)
    items = await repos.policies.find_many({"merchantId": merchant_id}, limit=20)
    slim = [{"id": p["id"], "name": p["name"], "limit": p["limit"], "status": p["status"]} for p in items]
    return {"items": slim, "actionMatrix": ACTION_MATRIX}


@router.patch("/policies/{policy_id}")
async def patch_policy(
    policy_id: str,
    body: PolicyPatchRequest,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    repos: Repositories = Depends(get_repos),
    audit: AuditService = Depends(get_audit_service),
):
    idem = IdempotencyService(repos.idempotency_records)
    route = f"/api/v1/policies/{policy_id}"
    cached = await idem.check_and_store(idempotency_key, route, "PATCH", body.model_dump())
    if cached:
        return cached

    policy = await repos.policies.get(policy_id)
    if not policy:
        raise NotFoundError("Policy not found.", {"policyId": policy_id})

    if policy_id == POLICY_PAYMENT_RETRY:
        # Hard rule: payment retry must remain blocked/strict for MVP, no matter
        # what the request tries to set.
        requested_status = (body.status or "").lower()
        if requested_status not in ("", "strict"):
            raise PolicyBlockedError(
                "Payment Retry must remain BLOCKED and strict in this MVP.",
                {"policyId": policy_id},
            )

    patch: dict = {}
    if body.limit is not None:
        patch["limit"] = body.limit
    if body.status is not None:
        patch["status"] = body.status
    updated = await repos.policies.update(policy_id, patch) if patch else policy

    event = await audit.record(
        merchant_id=body.merchant_id,
        agent=AGENT_SYSTEM,
        action="Policy changed",
        reason=f"Merchant updated {updated['name']}.",
        correlation_ids={"policyId": policy_id},
    )

    result = {
        "id": updated["id"],
        "name": updated["name"],
        "limit": updated["limit"],
        "status": updated["status"],
        "auditEventId": event["id"],
    }
    await idem.store_response(idempotency_key, route, 200, result)
    return result


@router.post("/policies/evaluate")
async def evaluate_policy(body: PolicyEvaluateRequest, policy_guard: PolicyGuard = Depends(get_policy_guard)):
    evaluation = await policy_guard.evaluate(
        merchant_id=body.merchant_id,
        action_type=body.action_type,
        target_type=body.target_type,
        target_id=body.target_id,
        proposed_action=body.proposed_action.model_dump(by_alias=True),
    )
    return {
        "policyEvaluationId": evaluation["id"],
        "outcome": evaluation["outcome"],
        "reasons": evaluation["reasons"],
        "checks": evaluation["checks"],
    }
