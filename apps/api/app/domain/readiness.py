from typing import Any, Dict
from app.domain.constants import CATEGORY_MAP


def compute_readiness(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Computes a 6-dimension AI-commerce readiness score and breakdown

    derived from concrete fields (never fixed magic numbers).
    """
    specs = doc.get("specs") or doc.get("attributes") or {}
    shipping = doc.get("shipping") or {}
    price = float(doc.get("price") or 0)
    inventory = int(doc.get("inventory") or 0)
    sku = doc.get("sku") or ""
    brand = doc.get("brand") or ""
    margin_pct = float(doc.get("marginPct") or doc.get("margin_pct") or 0)

    # 1. Attribute completeness (20 pts)
    attr_count = len(specs) if isinstance(specs, dict) else 0
    if attr_count >= 3:
        attr_score = 20
    elif attr_count >= 1:
        attr_score = 12
    else:
        attr_score = 0

    # 2. Pricing validity (15 pts)
    price_score = 15 if price > 0 else 0

    # 3. Inventory health (20 pts)
    if inventory > 10:
        inv_score = 20
        inv_status = "IN_STOCK"
    elif inventory >= 1:
        inv_score = 10
        inv_status = "LOW_STOCK"
    else:
        inv_score = 0
        inv_status = "OUT_OF_STOCK"

    # 4. Shipping metadata completeness (15 pts)
    has_weight = bool(shipping.get("weightKg"))
    has_dims = bool(shipping.get("dimensionsCm"))
    has_tier = bool(shipping.get("tier"))
    shipping_complete = has_weight and has_dims and has_tier
    if shipping_complete:
        ship_score = 15
    elif has_weight or has_dims or has_tier:
        ship_score = 8
    else:
        ship_score = 0

    # 5. SKU & Brand completeness (15 pts)
    id_score = 0
    if sku:
        id_score += 8
    if brand:
        id_score += 7

    # 6. Margin & Policy compliance (15 pts)
    margin_score = 15 if margin_pct >= 25 else (8 if margin_pct >= 15 else 0)

    total_score = attr_score + price_score + inv_score + ship_score + id_score + margin_score

    issues = []
    if attr_score < 20:
        issues.append("Ambiguous attributes")
    if ship_score < 15:
        issues.append("Shipping metadata")
    if inv_status == "OUT_OF_STOCK":
        issues.append("Out of stock")
    if margin_score < 15:
        issues.append("Margin below floor")

    active = doc.get("active", True)
    if not active:
        status = "inactive"
    elif total_score >= 80 and inventory > 0 and len(issues) == 0:
        status = "ready"
    else:
        status = "needs_attention"

    category_id = doc.get("categoryId") or doc.get("category_id") or "ACCESSORIES"
    category_meta = CATEGORY_MAP.get(category_id, {})
    category_name = doc.get("categoryName") or doc.get("category") or category_meta.get("name", "Accessories")

    # Update shipping metadataComplete flag
    shipping_dict = dict(shipping) if isinstance(shipping, dict) else {}
    shipping_dict["metadataComplete"] = shipping_complete

    return {
        "aiReadiness": total_score,
        "inventoryStatus": inv_status,
        "status": status,
        "issues": issues,
        "categoryId": category_id,
        "categoryName": category_name,
        "shipping": shipping_dict,
        "readinessBreakdown": {
            "attributes": attr_score,
            "pricing": price_score,
            "inventory": inv_score,
            "shipping": ship_score,
            "identifiers": id_score,
            "marginCompliance": margin_score,
            "total": total_score,
        },
    }
