from fastapi import APIRouter, Depends, Header, Request

from app.api.deps import get_audit_service, get_idempotency, get_merchant_service, get_repos
from app.core.errors import PolicyBlockedError
from app.core.security import resolve_merchant_id
from app.core.config import Settings, get_settings
from app.db.indexes import ensure_indexes
from app.db.seed import seed as run_seed
from app.domain.constants import AGENT_SYSTEM
from app.domain.schemas import OnboardingInitializeRequest
from app.repositories.registry import Repositories
from app.services.audit_service import AuditService
from app.services.merchant_service import MerchantService

router = APIRouter(tags=["merchant"])


@router.get("/merchant")
@router.get("/merchant/me")
async def get_merchant(request: Request, service: MerchantService = Depends(get_merchant_service)):
    merchant_id = resolve_merchant_id(request)
    merchant = await service.get(merchant_id)
    if not merchant:
        from app.core.errors import NotFoundError

        raise NotFoundError("Merchant not found.", {"merchantId": merchant_id})
    return {
        "id": merchant["id"],
        "name": merchant["name"],
        "category": merchant["category"],
        "currency": merchant["currency"],
        "status": merchant["status"],
    }


@router.post("/onboarding/initialize")
async def initialize_onboarding(
    request: Request,
    body: OnboardingInitializeRequest,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    repos: Repositories = Depends(get_repos),
    audit: AuditService = Depends(get_audit_service),
    settings: Settings = Depends(get_settings),
):
    if body.reset_demo_data and not settings.allow_demo_reset:
        raise PolicyBlockedError("Demo reset is disabled.", {"allowDemoReset": False})

    if body.reset_demo_data:
        await ensure_indexes(repos.db)
        await run_seed(repos.db)

    await audit.record(
        merchant_id=body.merchant_id,
        agent=AGENT_SYSTEM,
        action="Initialize Demo",
        reason="Merchant onboarding initialized demo data.",
        outcome="Success",
    )

    return {
        "merchant": {
            "id": "merchant_novatech",
            "name": "NovaTech Store",
            "category": "Consumer Electronics",
            "currency": "INR",
        },
        "initialized": True,
        "nextRoute": "/overview",
    }
