from fastapi import APIRouter, Depends, Header, Request

from app.api.deps import get_ai_commerce_agent, get_audit_service, get_repos
from app.core.errors import NotFoundError
from app.core.idempotency import IdempotencyService
from app.core.security import resolve_merchant_id
from app.domain.constants import AGENT_AI_COMMERCE
from app.domain.schemas import OptimizeCatalogRequest
from app.repositories.registry import Repositories
from app.services.ai_commerce_agent import AiCommerceAgentService
from app.services.audit_service import AuditService

router = APIRouter(tags=["ai-commerce"])


@router.get("/ai-commerce/readiness")
async def readiness(request: Request, service: AiCommerceAgentService = Depends(get_ai_commerce_agent)):
    merchant_id = resolve_merchant_id(request)
    return await service.readiness(merchant_id)


@router.get("/ai-commerce/products/{product_id}/profile")
async def product_profile(product_id: str, service: AiCommerceAgentService = Depends(get_ai_commerce_agent)):
    profile = await service.product_profile(product_id)
    if not profile:
        raise NotFoundError("Product not found.", {"productId": product_id})
    return profile


@router.post("/ai-commerce/optimize-catalog")
async def optimize_catalog(
    request: Request,
    body: OptimizeCatalogRequest,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    repos: Repositories = Depends(get_repos),
    service: AiCommerceAgentService = Depends(get_ai_commerce_agent),
    audit: AuditService = Depends(get_audit_service),
):
    idem = IdempotencyService(repos.idempotency_records)
    route = "/api/v1/ai-commerce/optimize-catalog"
    cached = await idem.check_and_store(idempotency_key, route, "POST", body.model_dump())
    if cached:
        return cached

    optimized = await service.optimize_catalog(body.product_ids)
    event = await audit.record(
        merchant_id=body.merchant_id,
        agent=AGENT_AI_COMMERCE,
        action="Optimize Catalog",
        reason=f"Optimized AI readiness metadata for {len(optimized)} product(s).",
    )
    result = {"optimizedProducts": optimized, "auditEventId": event["id"]}
    await idem.store_response(idempotency_key, route, 200, result)
    return result
