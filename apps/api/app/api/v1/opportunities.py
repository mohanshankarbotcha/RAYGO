from fastapi import APIRouter, Depends, Header, Request

from app.api.deps import (
    get_approval_gateway,
    get_audit_service,
    get_experiment_agent,
    get_growth_strategist,
    get_policy_guard,
    get_repos,
    get_revenue_intelligence,
)
from app.core.errors import NotFoundError, PolicyBlockedError
from app.core.idempotency import IdempotencyService
from app.core.security import resolve_merchant_id
from app.core.config import Settings, get_settings
from app.domain.constants import (
    AGENT_APPROVAL_GATEWAY,
    AGENT_EXPERIMENT,
    AGENT_GROWTH_STRATEGIST,
    AGENT_POLICY_GUARD,
    OUTCOME_BLOCKED,
)
from app.domain.schemas import OpportunityApproveRequest, OpportunityRejectRequest
from app.repositories.registry import Repositories
from app.services.approval_gateway import ApprovalGateway
from app.services.audit_service import AuditService
from app.services.experiment_agent import ExperimentAgentService
from app.services.growth_strategist import GrowthStrategistService
from app.services.policy_guard import PolicyGuard
from app.services.revenue_intelligence import RevenueIntelligenceService
from app.services.providers.factory import generate_with_fallback

router = APIRouter(tags=["opportunities"])


@router.get("/opportunities")
async def list_opportunities(
    request: Request,
    status: str | None = None,
    risk: str | None = None,
    limit: int = 50,
    service: RevenueIntelligenceService = Depends(get_revenue_intelligence),
):
    merchant_id = resolve_merchant_id(request)
    items = await service.ranked_opportunities(merchant_id, status=status, risk=risk, limit=limit)
    slim = [
        {
            "id": o["id"],
            "title": o["title"],
            "shortTitle": o["shortTitle"],
            "type": o["type"],
            "expectedMonthlyImpact": o["expectedMonthlyImpact"],
            "confidence": o["confidence"],
            "risk": o["risk"],
            "status": o["status"],
            "targetSegment": o["targetSegment"],
        }
        for o in items
    ]
    return {"items": slim, "total": len(slim), "nextCursor": None}


@router.get("/opportunities/{opportunity_id}")
async def get_opportunity(opportunity_id: str, repos: Repositories = Depends(get_repos)):
    opp = await repos.opportunities.get(opportunity_id)
    if not opp:
        raise NotFoundError("Opportunity not found.", {"opportunityId": opportunity_id})
    return {
        **{k: v for k, v in opp.items() if k not in ("createdAt", "updatedAt", "merchantId", "metadata")},
        "policyPreview": {
            "budget": "Within policy",
            "merchantApprovalRequired": True,
            "outcome": "requires_approval",
        },
    }


@router.get("/opportunities/{opportunity_id}/reasoning")
async def get_opportunity_reasoning(
    opportunity_id: str,
    repos: Repositories = Depends(get_repos),
    settings: Settings = Depends(get_settings),
):
    from app.domain.agent_schemas import OpportunityReasoning

    opp = await repos.opportunities.get(opportunity_id)
    if not opp:
        raise NotFoundError("Opportunity not found.", {"opportunityId": opportunity_id})

    result, mode, fallback_reason = await generate_with_fallback(
        settings,
        task="opportunity_reasoning",
        context={"opportunity": opp},
        schema=OpportunityReasoning,
    )
    return {
        **result.model_dump(by_alias=True),
        "mode": mode,
        "fallbackReason": fallback_reason,
    }


@router.post("/opportunities/{opportunity_id}/approve")
async def approve_opportunity(
    opportunity_id: str,
    request: Request,
    body: OpportunityApproveRequest,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    repos: Repositories = Depends(get_repos),
    policy_guard: PolicyGuard = Depends(get_policy_guard),
    approval_gateway: ApprovalGateway = Depends(get_approval_gateway),
    growth_strategist: GrowthStrategistService = Depends(get_growth_strategist),
    experiment_agent: ExperimentAgentService = Depends(get_experiment_agent),
    audit: AuditService = Depends(get_audit_service),
    settings: Settings = Depends(get_settings),
):
    idem = IdempotencyService(repos.idempotency_records)
    route = f"/api/v1/opportunities/{opportunity_id}/approve"
    cached = await idem.check_and_store(idempotency_key, route, "POST", body.model_dump())
    if cached:
        return cached

    opp = await repos.opportunities.get(opportunity_id)
    if not opp:
        raise NotFoundError("Opportunity not found.", {"opportunityId": opportunity_id})

    proposal, reasoning_mode, reasoning_fallback_reason = await growth_strategist.propose_experiment_with_mode(
        opp, settings
    )

    evaluation = await policy_guard.evaluate(
        merchant_id=body.merchant_id,
        action_type="create_experiment",
        target_type="opportunity",
        target_id=opportunity_id,
        proposed_action={
            "discountPct": proposal["discountPct"],
            "estimatedMarginPct": proposal["estimatedMarginPct"],
        },
    )
    await audit.record(
        merchant_id=body.merchant_id,
        agent=AGENT_POLICY_GUARD,
        action="Policy evaluated",
        reason="Evaluated proposed experiment against Discount Limit, Margin Floor, and Merchant Auth.",
        outcome="Success" if evaluation["outcome"] != OUTCOME_BLOCKED else "Prevented",
        severity="info" if evaluation["outcome"] != OUTCOME_BLOCKED else "warning",
        correlation_ids={"opportunityId": opportunity_id, "policyEvaluationId": evaluation["id"]},
    )

    if evaluation["outcome"] == OUTCOME_BLOCKED:
        await repos.opportunities.update(opportunity_id, {"status": "blocked"})
        raise PolicyBlockedError(
            "This experiment proposal violates policy and cannot be approved.",
            {"policyEvaluationId": evaluation["id"], "reasons": evaluation["reasons"]},
        )

    approval = await approval_gateway.record_approval(
        merchant_id=body.merchant_id,
        policy_evaluation_id=evaluation["id"],
        target_type="opportunity",
        target_id=opportunity_id,
        approved_by=body.approved_by,
    )
    await audit.record(
        merchant_id=body.merchant_id,
        agent=AGENT_APPROVAL_GATEWAY,
        action="Opportunity approved",
        reason=f"Merchant confirmed: {body.confirmation_text}",
        approval="Confirmed",
        correlation_ids={"opportunityId": opportunity_id, "approvalId": approval["id"]},
    )

    experiment = await experiment_agent.create_from_proposal(body.merchant_id, opportunity_id, proposal)
    await repos.opportunities.update(opportunity_id, {"status": "experiment_created"})
    await audit.record(
        merchant_id=body.merchant_id,
        agent=AGENT_EXPERIMENT,
        action="Experiment created",
        reason="Merchant approved recommendation. Policy check passed. Experiment created.",
        approval="Confirmed",
        correlation_ids={"opportunityId": opportunity_id, "experimentId": experiment["id"]},
        details={
            "decisionSummary": "Merchant approved recommendation. Policy check passed. Experiment created.",
            "reasoningMode": reasoning_mode,
            "reasoningFallbackReason": reasoning_fallback_reason,
        },
    )

    result = {
        "approvalId": approval["id"],
        "policyEvaluationId": evaluation["id"],
        "experimentId": experiment["id"],
        "status": "approved",
        "reasoningMode": reasoning_mode,
        "nextRoute": f"/experiments/{experiment['id']}",
    }
    await idem.store_response(idempotency_key, route, 200, result)
    return result


@router.post("/opportunities/{opportunity_id}/reject")
async def reject_opportunity(
    opportunity_id: str,
    body: OpportunityRejectRequest,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    repos: Repositories = Depends(get_repos),
    approval_gateway: ApprovalGateway = Depends(get_approval_gateway),
    audit: AuditService = Depends(get_audit_service),
):
    idem = IdempotencyService(repos.idempotency_records)
    route = f"/api/v1/opportunities/{opportunity_id}/reject"
    cached = await idem.check_and_store(idempotency_key, route, "POST", body.model_dump())
    if cached:
        return cached

    opp = await repos.opportunities.get(opportunity_id)
    if not opp:
        raise NotFoundError("Opportunity not found.", {"opportunityId": opportunity_id})

    rejection = await approval_gateway.record_rejection(
        merchant_id=body.merchant_id,
        policy_evaluation_id="",
        target_type="opportunity",
        target_id=opportunity_id,
        rejected_by=body.rejected_by,
        reason=body.reason,
    )
    await repos.opportunities.update(opportunity_id, {"status": "declined"})
    await audit.record(
        merchant_id=body.merchant_id,
        agent=AGENT_APPROVAL_GATEWAY,
        action="Opportunity rejected",
        reason=body.reason,
        approval="Rejected",
        correlation_ids={"opportunityId": opportunity_id, "approvalId": rejection["id"]},
    )

    result = {"approvalId": rejection["id"], "status": "declined", "nextRoute": "/opportunities"}
    await idem.store_response(idempotency_key, route, 200, result)
    return result
