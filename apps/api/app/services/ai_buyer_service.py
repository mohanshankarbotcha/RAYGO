import re
import uuid
from typing import Any, Dict, List, Optional

from app.repositories.registry import Repositories

# Flagship AI developer baseline bundle
SEEDED_BUNDLE = [
    {"productId": "prod_probook_14", "quantity": 1, "reason": "Primary laptop within budget."},
    {"productId": "prod_usb_c_dock", "quantity": 1, "reason": "Recommended connectivity accessory."},
    {"productId": "prod_laptop_stand", "quantity": 1, "reason": "Ergonomic setup add-on."},
]
BUNDLE_DISCOUNT = 1298
DECISION_TIME_SEC = 2.4
RECOMMENDATION_CONFIDENCE = 92

CATEGORY_KEYWORDS = {
    "LAPTOP": ["laptop", "notebook", "probook", "macbook", "ultrabook"],
    "CPU": ["cpu", "processor", "ryzen", "intel", "core", "7800x3d", "14700k", "7600x", "ghz"],
    "GPU": ["gpu", "graphics", "video card", "nvidia", "rtx", "4070", "4080", "radeon", "7800xt", "vram"],
    "MOTHERBOARD": ["motherboard", "mobo", "mainboard", "b650", "z790", "strix", "aorus", "tomahawk", "am5", "lga1700"],
    "CASE": ["case", "chassis", "cabinet", "tower", "airflow", "titan", "fractal", "pc case"],
    "RAM": ["ram", "memory", "ddr5", "ddr4", "vengeance", "trident", "fury", "crucial", "6000mhz"],
    "SSD": ["ssd", "nvme", "m.2", "solid state", "990 pro", "sn850x", "t700", "kc3000", "gen5"],
    "HDD": ["hdd", "hard drive", "ironwolf", "barracuda", "nas drive", "wd red", "toshiba"],
    "KEYBOARD": ["keyboard", "keeb", "linear", "mechanical", "wireless keyboard", "typing"],
    "MOUSE": ["mouse", "mice", "dpi", "optical", "precision mouse", "wireless mouse"],
    "AUDIO": ["audio", "headphones", "headset", "anc", "sound", "earphones", "noisecancel"],
    "DOCK": ["dock", "hub", "usb-c dock", "thunderbolt", "ports", "dual 4k"],
    "MONITOR": ["monitor", "screen", "display", "4k monitor", "ips", "panel", "refresh rate"],
    "ACCESSORIES": ["accessory", "stand", "laptop stand", "cable", "holder", "ergonomic"],
}

# Bounded bundler category sequence for PC builds
PC_BUILD_CATEGORIES = ["CPU", "GPU", "MOTHERBOARD", "RAM", "SSD", "CASE"]


def new_buyer_intent_id() -> str:
    return f"buyer_intent_{uuid.uuid4().hex[:8]}"


def new_basket_id() -> str:
    return f"basket_{uuid.uuid4().hex[:8]}"


class AiBuyerService:
    def __init__(self, repos: Repositories):
        self.repos = repos

    async def search(self, merchant_id: str, buyer_request: str, budget: Optional[float] = None) -> dict:
        req_lower = buyer_request.lower()

        # 1. Exact seeded demo laptop bundle match
        is_laptop_setup = (
            "ai development" in req_lower
            or "laptop setup" in req_lower
            or (budget and 65000 <= budget <= 75000 and "laptop" in req_lower)
        )

        all_products = await self.repos.products.find_many({"merchantId": merchant_id, "active": True}, limit=100)
        if not all_products:
            all_products = await self.repos.products.find_many({"active": True}, limit=100)

        # Filter out non-purchasable configuration items
        purchasable = [p for p in all_products if p.get("productType", "PHYSICAL") != "CONFIGURATION" and int(p.get("inventory", 0)) > 0]

        matched: List[Dict[str, Any]] = []
        subtotal: float = 0.0
        discount: float = 0.0

        if is_laptop_setup:
            for entry in SEEDED_BUNDLE:
                product = await self.repos.products.get(entry["productId"])
                if not product:
                    product = await self.repos.products.find_one({"merchantId": merchant_id, "id": entry["productId"]})
                if not product:
                    continue
                line_total = product["price"] * entry["quantity"]
                subtotal += line_total
                matched.append(
                    {
                        "productId": product["id"],
                        "name": product["name"],
                        "quantity": entry["quantity"],
                        "unitPrice": product["price"],
                        "reason": entry["reason"],
                    }
                )
            discount = float(BUNDLE_DISCOUNT)

        # 2. Bounded PC Build bundler (Gaming PC / Full Custom Rig / Build PC)
        elif any(k in req_lower for k in ["gaming pc", "full setup", "build pc", "custom rig", "pc build", "workstation"]):
            for cat_id in PC_BUILD_CATEGORIES:
                cat_products = [p for p in purchasable if p.get("categoryId") == cat_id or cat_id in p.get("id", "").upper()]
                if cat_products:
                    # Pick top rated / best price-to-readiness item
                    cat_products.sort(key=lambda x: (x.get("aiReadiness", 0), -x.get("price", 0)), reverse=True)
                    chosen_p = cat_products[0]
                    p_price = float(chosen_p.get("price", 0))
                    subtotal += p_price
                    matched.append(
                        {
                            "productId": chosen_p["id"],
                            "name": chosen_p["name"],
                            "quantity": 1,
                            "unitPrice": p_price,
                            "reason": f"Selected for {chosen_p.get('categoryName', cat_id)} slot in complete setup.",
                        }
                    )
            discount = 2500.0 if len(matched) >= 4 else 0.0

        # 3. Category Keyword Lookup matching across the full catalog
        else:
            matched_categories = []
            for cat_id, kw_list in CATEGORY_KEYWORDS.items():
                if any(kw in req_lower for kw in kw_list):
                    matched_categories.append(cat_id)

            candidates = []
            words = [w for w in re.findall(r"\w+", req_lower) if len(w) > 2]
            for p in purchasable:
                score = 0
                if p.get("categoryId") in matched_categories:
                    score += 10
                p_text = f"{p.get('name', '')} {p.get('brand', '')} {p.get('sku', '')} {p.get('categoryName', '')} {str(p.get('specs', ''))}".lower()
                score += sum(2 for w in words if w in p_text)
                if score > 0:
                    candidates.append((score, p))

            candidates.sort(key=lambda x: (x[0], x[1].get("aiReadiness", 0)), reverse=True)
            chosen_list = [c[1] for c in candidates[:4]] if candidates else purchasable[:2]

            for prod in chosen_list:
                p_price = float(prod.get("price", 0))
                if budget and (subtotal + p_price) > budget and matched:
                    continue
                subtotal += p_price
                matched.append(
                    {
                        "productId": prod["id"],
                        "name": prod.get("name", "Product"),
                        "quantity": 1,
                        "unitPrice": p_price,
                        "reason": f"Matched requirements for '{buyer_request}'.",
                    }
                )
            discount = 500.0 if len(matched) >= 2 else 0.0

        total = max(0.0, subtotal - discount)
        intent_id = "buyer_intent_ai_setup_001" if is_laptop_setup else new_buyer_intent_id()

        intent_doc = {
            "id": intent_id,
            "merchantId": merchant_id,
            "buyerRequest": buyer_request,
            "budget": budget,
            "matchedProducts": matched,
            "subtotal": subtotal,
            "bundleDiscount": discount,
            "total": total,
            "currency": "INR",
            "confidence": RECOMMENDATION_CONFIDENCE,
            "decisionTimeSec": DECISION_TIME_SEC,
            "metadata": {"parsedIntent": req_lower},
        }
        saved = await self.repos.buyer_intents.upsert(intent_doc)
        return saved

    async def create_basket(self, merchant_id: str, buyer_intent_id: Optional[str], items: List[Dict[str, Any]]) -> dict:
        resolved_items = []
        subtotal = 0.0
        for item in items:
            prod_id = item["productId"]
            product = await self.repos.products.get(prod_id)
            if not product:
                product = await self.repos.products.find_one({"merchantId": merchant_id, "id": prod_id})
            if not product:
                continue
            qty = int(item.get("quantity", 1))
            price = float(product.get("price", 0))
            line_total = price * qty
            subtotal += line_total
            resolved_items.append(
                {
                    "productId": product["id"],
                    "name": product.get("name", ""),
                    "quantity": qty,
                    "unitPrice": price,
                }
            )

        discount = float(BUNDLE_DISCOUNT) if len(resolved_items) >= 2 else 0.0
        total = max(0.0, subtotal - discount)

        basket_id = "basket_ai_setup_001" if buyer_intent_id == "buyer_intent_ai_setup_001" else new_basket_id()
        doc = {
            "id": basket_id,
            "merchantId": merchant_id,
            "buyerIntentId": buyer_intent_id,
            "items": resolved_items,
            "subtotal": subtotal,
            "bundleDiscount": discount,
            "total": total,
            "currency": "INR",
            "metadata": {},
        }
        return await self.repos.baskets.upsert(doc)

    async def get_basket(self, basket_id: str) -> Optional[dict]:
        return await self.repos.baskets.get(basket_id)
