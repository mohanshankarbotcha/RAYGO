import uuid
from typing import Any, Dict, List, Optional, Tuple

from app.domain.constants import (
    AUDIT_OUTCOME_SUCCESS,
    CATEGORIES,
    CATEGORY_MAP,
    SEVERITY_INFO,
)
from app.domain.readiness import compute_readiness
from app.domain.schemas import ProductCreateRequest, ProductPatchRequest
from app.repositories.registry import Repositories
from app.services.audit_service import AuditService


class ProductService:
    def __init__(self, repos: Repositories):
        self.repos = repos

    async def list_categories(self) -> List[Dict[str, Any]]:
        cats = await self.repos.categories.find_many({}, limit=100)
        if not cats:
            return CATEGORIES
        return cats

    async def list(
        self,
        merchant_id: str,
        category: Optional[str] = None,
        search: Optional[str] = None,
        stock: Optional[str] = None,
        active: Optional[bool] = None,
        min_readiness: Optional[int] = None,
        status: Optional[str] = None,
        sort: Optional[str] = None,
        sort_dir: Optional[str] = "asc",
        limit: int = 50,
        skip: int = 0,
    ) -> Tuple[List[Dict[str, Any]], int]:
        query: Dict[str, Any] = {"merchantId": merchant_id}

        if category:
            cat_upper = category.upper()
            if cat_upper in CATEGORY_MAP:
                query["$or"] = [{"categoryId": cat_upper}, {"category": category}, {"categoryName": category}]
            else:
                query["$or"] = [
                    {"categoryId": {"$regex": category, "$options": "i"}},
                    {"category": {"$regex": category, "$options": "i"}},
                    {"categoryName": {"$regex": category, "$options": "i"}},
                ]

        if status:
            query["status"] = status

        if active is not None:
            query["active"] = active

        if stock:
            stock_lower = stock.lower()
            if stock_lower == "in_stock":
                query["inventory"] = {"$gt": 10}
            elif stock_lower == "low_stock":
                query["inventory"] = {"$gte": 1, "$lte": 10}
            elif stock_lower == "out_of_stock":
                query["inventory"] = {"$lte": 0}

        if min_readiness is not None:
            query["aiReadiness"] = {"$gte": min_readiness}

        if search:
            search_regex = {"$regex": search, "$options": "i"}
            search_or = [
                {"name": search_regex},
                {"sku": search_regex},
                {"brand": search_regex},
                {"category": search_regex},
                {"categoryName": search_regex},
            ]
            if "$or" in query:
                query["$and"] = [{"$or": query.pop("$or")}, {"$or": search_or}]
            else:
                query["$or"] = search_or

        sort_list = None
        if sort:
            direction = 1 if sort_dir and sort_dir.lower() == "asc" else -1
            sort_list = [(sort, direction)]
        else:
            sort_list = [("aiReadiness", -1), ("name", 1)]

        items = await self.repos.products.find_many(query, limit=limit, skip=skip, sort=sort_list)
        total = await self.repos.products.count(query)
        return items, total

    async def get_by_id(self, merchant_id: str, product_id: str) -> Optional[Dict[str, Any]]:
        return await self.repos.products.find_one({"merchantId": merchant_id, "id": product_id})

    async def create(
        self,
        merchant_id: str,
        payload: ProductCreateRequest,
        audit_service: AuditService,
    ) -> Dict[str, Any]:
        prod_id = payload.id or f"prod_{uuid.uuid4().hex[:10]}"
        sku = payload.sku or f"NT-{payload.category_id[:3].upper()}-{uuid.uuid4().hex[:4].upper()}"

        doc = {
            "id": prod_id,
            "merchantId": merchant_id,
            "name": payload.name,
            "categoryId": payload.category_id.upper(),
            "price": payload.price,
            "inventory": payload.inventory,
            "sku": sku,
            "brand": payload.brand or "NovaTech",
            "productType": payload.product_type,
            "marginPct": payload.margin_pct,
            "specs": payload.specs or payload.attributes or {},
            "attributes": payload.attributes or payload.specs or {},
            "shipping": payload.shipping or {},
            "active": payload.active,
            "currency": "INR",
        }
        computed = compute_readiness(doc)
        full_doc = {**doc, **computed}
        saved = await self.repos.products.upsert(full_doc)

        await audit_service.record(
            merchant_id=merchant_id,
            agent="System",
            action="Create Product",
            reason=f"Owner created new product: {payload.name} (SKU: {sku}) in category {full_doc['categoryName']}.",
            policy="Passed",
            approval="Owner Action",
            outcome=AUDIT_OUTCOME_SUCCESS,
            severity=SEVERITY_INFO,
            correlation_ids={"productId": prod_id},
            details={"product": {"id": prod_id, "name": payload.name, "sku": sku, "price": payload.price}},
        )
        return saved

    async def patch(
        self,
        merchant_id: str,
        product_id: str,
        payload: ProductPatchRequest,
        audit_service: AuditService,
    ) -> Optional[Dict[str, Any]]:
        existing = await self.get_by_id(merchant_id, product_id)
        if not existing:
            return None

        update_data = {}
        if payload.name is not None:
            update_data["name"] = payload.name
        if payload.category_id is not None:
            update_data["categoryId"] = payload.category_id.upper()
        if payload.price is not None:
            update_data["price"] = payload.price
        if payload.inventory is not None:
            update_data["inventory"] = payload.inventory
        if payload.sku is not None:
            update_data["sku"] = payload.sku
        if payload.brand is not None:
            update_data["brand"] = payload.brand
        if payload.product_type is not None:
            update_data["productType"] = payload.product_type
        if payload.margin_pct is not None:
            update_data["marginPct"] = payload.margin_pct
        if payload.specs is not None:
            update_data["specs"] = payload.specs
        if payload.attributes is not None:
            update_data["attributes"] = payload.attributes
        if payload.shipping is not None:
            update_data["shipping"] = payload.shipping
        if payload.active is not None:
            update_data["active"] = payload.active

        merged = {**existing, **update_data}
        computed = compute_readiness(merged)
        final_doc = {**merged, **computed}

        updated = await self.repos.products.update(product_id, final_doc)

        changes = list(update_data.keys())
        await audit_service.record(
            merchant_id=merchant_id,
            agent="System",
            action="Update Product",
            reason=f"Owner updated product: {final_doc['name']} ({final_doc.get('sku')}). Modified fields: {', '.join(changes)}.",
            policy="Passed",
            approval="Owner Action",
            outcome=AUDIT_OUTCOME_SUCCESS,
            severity=SEVERITY_INFO,
            correlation_ids={"productId": product_id},
            details={"changes": update_data},
        )
        return updated or final_doc

    async def adjust_stock(
        self,
        merchant_id: str,
        product_id: str,
        quantity: Optional[int] = None,
        adjustment: Optional[int] = None,
        reason: str = "Manual inventory adjustment",
        audit_service: Optional[AuditService] = None,
    ) -> Optional[Dict[str, Any]]:
        existing = await self.get_by_id(merchant_id, product_id)
        if not existing:
            return None

        old_inv = int(existing.get("inventory", 0))
        if quantity is not None:
            new_inv = max(0, quantity)
        elif adjustment is not None:
            new_inv = max(0, old_inv + adjustment)
        else:
            new_inv = old_inv

        merged = {**existing, "inventory": new_inv}
        computed = compute_readiness(merged)
        final_doc = {**merged, **computed}

        updated = await self.repos.products.update(product_id, final_doc)

        if audit_service:
            await audit_service.record(
                merchant_id=merchant_id,
                agent="System",
                action="Adjust Stock",
                reason=f"Owner updated product {final_doc['name']} ({final_doc.get('sku', '')}). Field: Inventory from {old_inv} to {new_inv}. Reason: {reason}.",
                policy="Passed",
                approval="Owner Action",
                outcome=AUDIT_OUTCOME_SUCCESS,
                severity=SEVERITY_INFO,
                correlation_ids={"productId": product_id},
                details={"oldInventory": old_inv, "newInventory": new_inv, "reason": reason},
            )
        return updated or final_doc

    async def set_active_status(
        self,
        merchant_id: str,
        product_id: str,
        active: bool,
        audit_service: AuditService,
    ) -> Optional[Dict[str, Any]]:
        existing = await self.get_by_id(merchant_id, product_id)
        if not existing:
            return None

        merged = {**existing, "active": active}
        computed = compute_readiness(merged)
        final_doc = {**merged, **computed}

        updated = await self.repos.products.update(product_id, final_doc)

        action_word = "activated" if active else "deactivated"
        await audit_service.record(
            merchant_id=merchant_id,
            agent="System",
            action=f"{action_word.capitalize()} Product",
            reason=f"Owner {action_word} product {final_doc['name']} ({final_doc.get('sku', '')}).",
            policy="Passed",
            approval="Owner Action",
            outcome=AUDIT_OUTCOME_SUCCESS,
            severity=SEVERITY_INFO,
            correlation_ids={"productId": product_id},
            details={"active": active},
        )
        return updated or final_doc
