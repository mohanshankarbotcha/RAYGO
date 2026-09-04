from app.repositories.registry import Repositories

READINESS_DIMENSIONS = [
    {"name": "Catalog Completeness", "score": 88, "status": "ready"},
    {"name": "Policy Clarity", "score": 72, "status": "needs_attention"},
    {"name": "Payment Readiness", "score": 86, "status": "ready"},
]

PRODUCT_PROFILES: dict[str, dict] = {
    "prod_laptop_stand": {
        "category": "Laptop accessory",
        "buyerUseCases": ["Remote work", "College setup", "Desk ergonomics"],
        "compatibleProducts": ["prod_wireless_keyboard", "prod_probook_14", "prod_usb_c_dock"],
        "missingMetadata": ["Shipping metadata"],
    },
    "prod_probook_14": {
        "category": "Laptop",
        "buyerUseCases": ["AI development", "Coding", "College"],
        "compatibleProducts": ["prod_usb_c_dock", "prod_laptop_stand", "prod_wireless_keyboard"],
        "missingMetadata": [],
    },
}


class AiCommerceAgentService:
    """MVP behavior: readiness score is fixed at 82 per the demo dataset;
    product profiles and catalog optimization are deterministic lookups."""

    def __init__(self, repos: Repositories):
        self.repos = repos

    async def readiness(self, merchant_id: str) -> dict:
        merchant = await self.repos.merchants.get(merchant_id)
        score = (merchant or {}).get("metrics", {}).get("aiCommerceReadiness", 82)
        return {
            "score": score,
            "label": "AI Commerce Readiness",
            "dimensions": READINESS_DIMENSIONS,
            "recommendedActions": [
                {
                    "id": "optimize_laptop_stand_metadata",
                    "label": "Optimize Laptop Stand shipping metadata",
                    "route": "/products",
                }
            ],
        }

    async def product_profile(self, product_id: str) -> dict | None:
        product = await self.repos.products.get(product_id)
        if not product:
            return None
        profile = PRODUCT_PROFILES.get(
            product_id,
            {
                "category": "General",
                "buyerUseCases": [],
                "compatibleProducts": [],
                "missingMetadata": product.get("issues", []),
            },
        )
        return {
            "productId": product_id,
            "name": product["name"],
            "aiReadiness": product.get("aiReadiness", 0),
            "profile": profile,
            "status": product.get("status", "ready"),
        }

    async def optimize_catalog(self, product_ids: list[str]) -> list[dict]:
        optimized = []
        for pid in product_ids:
            product = await self.repos.products.get(pid)
            if not product:
                continue
            previous = product.get("aiReadiness", 0)
            new_readiness = min(previous + 5, 100)
            await self.repos.products.update(
                pid, {"aiReadiness": new_readiness, "status": "ready", "issues": []}
            )
            optimized.append(
                {
                    "productId": pid,
                    "previousReadiness": previous,
                    "newReadiness": new_readiness,
                    "status": "ready",
                }
            )
        return optimized
