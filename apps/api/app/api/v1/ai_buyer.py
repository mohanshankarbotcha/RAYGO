from fastapi import APIRouter, Depends, Header, Request

from app.api.deps import get_ai_buyer_service, get_audit_service, get_order_intent_service, get_repos
from app.core.config import Settings, get_settings
from app.core.errors import NotFoundError
from app.core.idempotency import IdempotencyService
from app.domain.agent_schemas import CommerceIntentOutput
from app.domain.constants import AGENT_AI_COMMERCE
from app.domain.schemas import AiBuyerBasketRequest, AiBuyerSearchRequest, OrderIntentCreateRequest
from app.repositories.registry import Repositories
from app.services.ai_buyer_service import AiBuyerService
from app.services.audit_service import AuditService
from app.services.order_intent_service import OrderIntentService
from app.services.providers.factory import generate_with_fallback

router = APIRouter(tags=["ai-buyer"])


@router.post("/ai-buyer/search")
async def ai_buyer_search(
    body: AiBuyerSearchRequest,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    repos: Repositories = Depends(get_repos),
    service: AiBuyerService = Depends(get_ai_buyer_service),
    audit: AuditService = Depends(get_audit_service),
    settings: Settings = Depends(get_settings),
):
    idem = IdempotencyService(repos.idempotency_records)
    route = "/api/v1/ai-buyer/search"
    cached = await idem.check_and_store(idempotency_key, route, "POST", body.model_dump())
    if cached:
        return cached

    intent, intent_mode, intent_fallback_reason = await generate_with_fallback(
        settings,
        task="commerce_intent",
        context={"buyerRequest": body.buyer_request, "budget": body.budget},
        schema=CommerceIntentOutput,
    )
    matched = await service.search(body.merchant_id, body.buyer_request, body.budget)
    await audit.record(
        merchant_id=body.merchant_id,
        agent=AGENT_AI_COMMERCE,
        action="AI buyer search completed",
        reason="Matched buyer request to AI-readable catalog.",
        correlation_ids={"buyerIntentId": matched["id"]},
        details={
            "decisionSummary": "Matched buyer request to AI-readable catalog.",
            "parsedIntent": intent.model_dump(by_alias=True),
            "reasoningMode": intent_mode,
        },
    )
    result = {
        "buyerIntentId": matched["id"],
        "parsedIntent": intent.model_dump(by_alias=True),
        "reasoningMode": intent_mode,
        "matchedProducts": matched["matchedProducts"],
        "subtotal": matched["subtotal"],
        "bundleDiscount": matched["bundleDiscount"],
        "total": matched["total"],
        "currency": matched["currency"],
        "confidence": matched["confidence"],
        "decisionTimeSec": matched["decisionTimeSec"],
    }
    await idem.store_response(idempotency_key, route, 200, result)
    return result


@router.post("/ai-buyer/basket")
async def ai_buyer_basket(
    body: AiBuyerBasketRequest,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    repos: Repositories = Depends(get_repos),
    service: AiBuyerService = Depends(get_ai_buyer_service),
):
    idem = IdempotencyService(repos.idempotency_records)
    route = "/api/v1/ai-buyer/basket"
    cached = await idem.check_and_store(idempotency_key, route, "POST", body.model_dump())
    if cached:
        return cached

    basket = await service.create_basket(
        body.merchant_id, body.buyer_intent_id, [item.model_dump(by_alias=True) for item in body.items]
    )
    result = {
        "basketId": basket["id"],
        "items": basket["items"],
        "subtotal": basket["subtotal"],
        "bundleDiscount": basket["bundleDiscount"],
        "total": basket["total"],
        "currency": basket["currency"],
    }
    await idem.store_response(idempotency_key, route, 200, result)
    return result


@router.post("/order-intents")
@router.post("/ai-buyer/order-intent")
async def create_order_intent(
    body: OrderIntentCreateRequest,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    repos: Repositories = Depends(get_repos),
    service: OrderIntentService = Depends(get_order_intent_service),
    audit: AuditService = Depends(get_audit_service),
):
    idem = IdempotencyService(repos.idempotency_records)
    route = "/api/v1/order-intents"
    cached = await idem.check_and_store(idempotency_key, route, "POST", body.model_dump())
    if cached:
        return cached

    intent = await service.create(body.merchant_id, body.basket_id, body.buyer_request)
    await audit.record(
        merchant_id=body.merchant_id,
        agent=AGENT_AI_COMMERCE,
        action="Order intent created",
        reason="Buyer basket converted to a checkout order intent awaiting authorization.",
        correlation_ids={"orderIntentId": intent["id"]},
    )
    result = {
        "id": intent["id"],
        "orderIntentId": intent["id"],
        "displayOrderId": intent["displayOrderId"],
        "status": intent["status"],
        "total": intent["total"],
        "currency": intent["currency"],
        "nextRoute": f"/checkout/{intent['id']}",
    }
    await idem.store_response(idempotency_key, route, 200, result)
    return result


@router.get("/order-intents/{order_intent_id}")
@router.get("/ai-buyer/order-intent/{order_intent_id}")
async def get_order_intent(order_intent_id: str, service: OrderIntentService = Depends(get_order_intent_service)):
    intent = await service.get(order_intent_id)
    if not intent:
        raise NotFoundError("Order intent not found.", {"orderIntentId": order_intent_id})
    return {
        k: v
        for k, v in intent.items()
        if k not in ("createdAt", "updatedAt", "merchantId", "metadata")
    }
