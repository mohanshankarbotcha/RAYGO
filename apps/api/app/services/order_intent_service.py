import uuid

from app.core.errors import InsufficientInventoryError, NotFoundError
from app.repositories.registry import Repositories

_DISPLAY_ORDER_SEED = "#RGO-10482"


def new_display_order_id(sequence: int) -> str:
    return f"#RGO-{10480 + sequence}"


class OrderIntentService:
    def __init__(self, repos: Repositories):
        self.repos = repos

    async def create(self, merchant_id: str, basket_id: str, buyer_request: str | None) -> dict:
        basket = await self.repos.baskets.get(basket_id)
        if not basket:
            raise NotFoundError("Basket not found.", {"basketId": basket_id})

        # Re-validate live inventory for every basket line
        for item in basket.get("items", []):
            prod_id = item.get("productId")
            requested_qty = item.get("quantity", 1)
            live_product = await self.repos.products.find_one({"merchantId": merchant_id, "id": prod_id})
            if not live_product:
                live_product = await self.repos.products.get(prod_id)

            if not live_product:
                raise NotFoundError(f"Product '{prod_id}' in basket not found in live catalog.", {"productId": prod_id})

            if not live_product.get("active", True):
                raise InsufficientInventoryError(
                    f"Product '{live_product.get('name', prod_id)}' is currently inactive.",
                    {"productId": prod_id, "active": False},
                )

            available_qty = int(live_product.get("inventory", 0))
            if available_qty < requested_qty:
                raise InsufficientInventoryError(
                    f"Insufficient inventory for '{live_product.get('name', prod_id)}'. Requested: {requested_qty}, Available: {available_qty}.",
                    {"productId": prod_id, "requested": requested_qty, "available": available_qty},
                )


        # The seeded demo basket always maps to the seeded demo order intent
        # so `/checkout/intent_ai_setup_001` works immediately after seed.
        if basket_id == "basket_ai_setup_001":
            intent_id = "intent_ai_setup_001"
            display_order_id = "#RGO-10482"
        else:
            intent_id = f"intent_{uuid.uuid4().hex[:10]}"
            count = await self.repos.order_intents.count({"merchantId": merchant_id})
            display_order_id = f"#RGO-{10483 + count}"

        doc = {
            "id": intent_id,
            "merchantId": merchant_id,
            "displayOrderId": display_order_id,
            "buyerRequest": buyer_request or basket.get("metadata", {}).get("buyerRequest", ""),
            "whyPrepared": "RAYGO matched buyer intent to an AI-readable catalog and stayed under budget.",
            "customerName": "AI Buyer Demo",
            "source": "AI Buyer",
            "items": basket["items"],
            "subtotal": basket["subtotal"],
            "bundleDiscount": basket["bundleDiscount"],
            "taxesAndFeesLabel": "Calculated",
            "total": basket["total"],
            "currency": basket["currency"],
            "status": "review",
            "paymentStatus": "not_started",
            "authorizationRequired": True,
            "authorizationCopy": "RAYGO will not execute payment until you confirm this purchase.",
            "metadata": {"decisionTimeSec": 2.4, "recommendationConfidence": 92},
        }
        return await self.repos.order_intents.upsert(doc)

    async def get(self, order_intent_id: str) -> dict | None:
        return await self.repos.order_intents.get(order_intent_id)
