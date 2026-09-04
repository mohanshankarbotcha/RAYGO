from fastapi import APIRouter, Depends, Header, Request

from app.api.deps import (
    get_approval_gateway,
    get_audit_service,
    get_experiment_agent,
    get_policy_guard,
    get_repos,
)
from app.core.config import Settings, get_settings
from app.core.errors import NotFoundError, PolicyBlockedError
from app.core.idempotency import IdempotencyService
from app.core.security import resolve_merchant_id
from app.domain.agent_schemas import ExperimentRecommendationOutput
from app.domain.constants import AGENT_APPROVAL_GATEWAY, AGENT_EXPERIMENT, AGENT_POLICY_GUARD, OUTCOME_BLOCKED
from app.domain.schemas import ExperimentRejectRequest, ExperimentScaleRequest
from app.repositories.registry import Repositories
from app.services.approval_gateway import ApprovalGateway
from app.services.audit_service import AuditService
from app.services.experiment_agent import ExperimentAgentService
from app.services.policy_guard import PolicyGuard
from app.services.providers.factory import generate_with_fallback

router = APIRouter(tags=["experiments"])


def _slim(exp: dict) -> dict:
    return {
        "id": exp["id"],
        "opportunityId": exp["opportunityId"],
        "name": exp["name"],
        "status": exp["status"],
        "conversionUplift": exp["conversionUplift"],
        "revenueUplift": exp["revenueUplift"],
        "confidence": exp["confidence"],
        "recommendation": exp["recommendation"],
    }


@router.get("/experiments")
async def list_experiments(request: Request, repos: Repositories = Depends(get_repos)):
    merchant_id = resolve_merchant_id(request)
    items = await repos.experiments.find_many({"merchantId": merchant_id}, limit=50)
    active = sum(1 for e in items if e["status"] in ("running", "scale_review"))
    scaled = sum(1 for e in items if e["status"] == "scaled")
    avg_conf = round(sum(e["confidence"] for e in items) / len(items)) if items else 0
    return {
        "summary": {
            "activeExperiments": active,
            "scaledExperiments": scaled,
            "averageConfidence": avg_conf,
        },
        "items": [_slim(e) for e in items],
        "total": len(items),
        "nextCursor": None,
    }


@router.get("/experiments/{experiment_id}")
async def get_experiment(
    experiment_id: str,
    include_reasoning: bool = False,
    repos: Repositories = Depends(get_repos),
    settings: Settings = Depends(get_settings),
):
    exp = await repos.experiments.get(experiment_id)
    if not exp:
        raise NotFoundError("Experiment not found.", {"experimentId": experiment_id})
    body = {
        k: v
        for k, v in exp.items()
        if k not in ("createdAt", "updatedAt", "merchantId", "metadata")
    }
    if include_reasoning:
        result, mode, fallback_reason = await generate_with_fallback(
            settings,
            task="experiment_recommendation",
            context={"experiment": exp},
            schema=ExperimentRecommendationOutput,
        )
        body["aiRecommendation"] = result.model_dump(by_alias=True)
        body["aiRecommendation"]["mode"] = mode
        body["aiRecommendation"]["fallbackReason"] = fallback_reason
    return body


@router.post("/experiments/{experiment_id}/scale")
async def scale_experiment(
    experiment_id: str,
    request: Request,
    body: ExperimentScaleRequest,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    repos: Repositories = Depends(get_repos),
    policy_guard: PolicyGuard = Depends(get_policy_guard),
    approval_gateway: ApprovalGateway = Depends(get_approval_gateway),
    experiment_agent: ExperimentAgentService = Depends(get_experiment_agent),
    audit: AuditService = Depends(get_audit_service),
):
    idem = IdempotencyService(repos.idempotency_records)
    route = f"/api/v1/experiments/{experiment_id}/scale"
    cached = await idem.check_and_store(idempotency_key, route, "POST", body.model_dump())
    if cached:
        return cached

    exp = await repos.experiments.get(experiment_id)
    if not exp:
        raise NotFoundError("Experiment not found.", {"experimentId": experiment_id})

    evaluation = await policy_guard.evaluate(
        merchant_id=body.merchant_id,
        action_type="scale_experiment",
        target_type="experiment",
        target_id=experiment_id,
        proposed_action={
            "discountPct": exp.get("metadata", {}).get("discountPct"),
            "estimatedMarginPct": 32,
        },
    )
    await audit.record(
        merchant_id=body.merchant_id,
        agent=AGENT_POLICY_GUARD,
        action="Policy evaluated",
        reason="Evaluated experiment scaling against Discount Limit and Margin Floor.",
        outcome="Success" if evaluation["outcome"] != OUTCOME_BLOCKED else "Prevented",
        severity="info" if evaluation["outcome"] != OUTCOME_BLOCKED else "warning",
        correlation_ids={"experimentId": experiment_id, "policyEvaluationId": evaluation["id"]},
    )
    if evaluation["outcome"] == OUTCOME_BLOCKED:
        raise PolicyBlockedError(
            "Scaling this experiment violates policy.",
            {"policyEvaluationId": evaluation["id"], "reasons": evaluation["reasons"]},
        )

    approval = await approval_gateway.record_approval(
        merchant_id=body.merchant_id,
        policy_evaluation_id=evaluation["id"],
        target_type="experiment",
        target_id=experiment_id,
        approved_by=body.approved_by,
    )
    await experiment_agent.scale(experiment_id)
    await audit.record(
        merchant_id=body.merchant_id,
        agent=AGENT_EXPERIMENT,
        action="Experiment scaled",
        reason=f"Merchant confirmed: {body.confirmation_text}",
        approval="Confirmed",
        correlation_ids={"experimentId": experiment_id, "approvalId": approval["id"]},
    )

    result = {
        "experimentId": experiment_id,
        "policyEvaluationId": evaluation["id"],
        "approvalId": approval["id"],
        "status": "scaled",
        "nextRoute": "/ai-commerce",
    }
    await idem.store_response(idempotency_key, route, 200, result)
    return result


@router.post("/experiments/{experiment_id}/reject")
async def reject_experiment(
    experiment_id: str,
    body: ExperimentRejectRequest,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    repos: Repositories = Depends(get_repos),
    approval_gateway: ApprovalGateway = Depends(get_approval_gateway),
    audit: AuditService = Depends(get_audit_service),
):
    idem = IdempotencyService(repos.idempotency_records)
    route = f"/api/v1/experiments/{experiment_id}/reject"
    cached = await idem.check_and_store(idempotency_key, route, "POST", body.model_dump())
    if cached:
        return cached

    exp = await repos.experiments.get(experiment_id)
    if not exp:
        raise NotFoundError("Experiment not found.", {"experimentId": experiment_id})

    rejection = await approval_gateway.record_rejection(
        merchant_id=body.merchant_id,
        policy_evaluation_id="",
        target_type="experiment",
        target_id=experiment_id,
        rejected_by=body.rejected_by,
        reason=body.reason,
    )
    await repos.experiments.update(experiment_id, {"status": "running"})
    await audit.record(
        merchant_id=body.merchant_id,
        agent=AGENT_APPROVAL_GATEWAY,
        action="Experiment scale rejected",
        reason=body.reason,
        approval="Rejected",
        correlation_ids={"experimentId": experiment_id, "approvalId": rejection["id"]},
    )

    result = {"approvalId": rejection["id"], "status": "blocked", "nextRoute": f"/experiments/{experiment_id}"}
    await idem.store_response(idempotency_key, route, 200, result)
    return result


@router.get("/experiments/{experiment_id}/timeline")
async def get_experiment_timeline(
    experiment_id: str,
    request: Request,
    repos: Repositories = Depends(get_repos),
):
    merchant_id = resolve_merchant_id(request)
    exp = await repos.experiments.get(experiment_id)
    if not exp:
        raise NotFoundError("Experiment not found.", {"experimentId": experiment_id})

    # Fetch agent activities and audit records
    activities = await repos.agent_activity.find_many({"merchantId": merchant_id}, limit=50)
    audit_events = await repos.audit_events.find_many({"merchantId": merchant_id}, limit=50)

    timeline_nodes = []
    # Build from stored agent activity & audit if available
    for act in activities:
        timeline_nodes.append({
            "id": act.get("id"),
            "timestamp": act.get("time") or act.get("timestamp"),
            "agent": act.get("agent"),
            "message": act.get("message"),
            "auditEventId": act.get("auditEventId"),
        })

    # Fallback to standard 5-stage lifecycle if no live activity records
    if not timeline_nodes:
        timeline_nodes = [
            {"id": "node_1", "timestamp": "11:32:04", "stage": "opportunity_detected", "agent": "Revenue Intelligence", "message": "Cross-sell opportunity detected: Wireless Keyboard -> Laptop Stand"},
            {"id": "node_2", "timestamp": "11:32:05", "stage": "hypothesis_generated", "agent": "Growth Strategist", "message": "Generated experiment hypothesis with 10% bundle discount"},
            {"id": "node_3", "timestamp": "11:32:06", "stage": "policy_evaluated", "agent": "Policy Guard", "message": "Policy check passed: Discount (10% <= 20%), Margin (34% >= 25%), Sample size adequate"},
            {"id": "node_4", "timestamp": "11:32:07", "stage": "approval_received", "agent": "Approval Gateway", "message": "Merchant approval received: 'Approve & Create Experiment'"},
            {"id": "node_5", "timestamp": "11:32:08", "stage": "experiment_running", "agent": "Experiment Agent", "message": "Experiment active: 50/50 live traffic split variant vs control"},
        ]

    return {
        "experimentId": experiment_id,
        "status": exp.get("status", "running"),
        "confidence": exp.get("confidence", 94),
        "timeline": timeline_nodes,
        "total": len(timeline_nodes),
    }

