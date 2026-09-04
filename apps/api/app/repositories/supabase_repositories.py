"""
NOT ACTIVE AT RUNTIME — Reference implementation for a future Supabase/Postgres migration.
See docs/DATABASE_DECISION.md for details. Authoritative runtime database is MongoDB.
"""
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

from app.db.supabase_client import SupabaseClient, get_supabase_client


class SupabaseBaseRepository:
    def __init__(self, table_name: str, client: Optional[SupabaseClient] = None):
        self.table_name = table_name
        self.client = client or get_supabase_client()

    async def find_one(self, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        results = await self.client.select(self.table_name, query, limit=1)
        return results[0] if results else None

    async def find_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        return await self.find_one({"id": item_id})

    async def find_many(
        self,
        query: Optional[Dict[str, Any]] = None,
        limit: int = 100,
        sort: Optional[List[tuple]] = None,
    ) -> List[Dict[str, Any]]:
        return await self.client.select(self.table_name, query, limit=limit)

    async def insert_one(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        if "created_at" not in doc and "createdAt" not in doc:
            doc["created_at"] = datetime.now(timezone.utc).isoformat()
        return await self.client.insert(self.table_name, doc)

    async def update_one(self, query: Dict[str, Any], updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if "updated_at" not in updates and "updatedAt" not in updates:
            updates["updated_at"] = datetime.now(timezone.utc).isoformat()
        updated = await self.client.update(self.table_name, query, updates)
        return updated[0] if updated else None

    async def count(self, query: Optional[Dict[str, Any]] = None) -> int:
        items = await self.find_many(query, limit=1000)
        return len(items)


class SupabaseMerchantRepository(SupabaseBaseRepository):
    def __init__(self, client: Optional[SupabaseClient] = None):
        super().__init__("merchants", client)


class SupabaseStoreRepository(SupabaseBaseRepository):
    def __init__(self, client: Optional[SupabaseClient] = None):
        super().__init__("stores", client)


class SupabaseCategoryRepository(SupabaseBaseRepository):
    def __init__(self, client: Optional[SupabaseClient] = None):
        super().__init__("categories", client)


class SupabaseProductRepository(SupabaseBaseRepository):
    def __init__(self, client: Optional[SupabaseClient] = None):
        super().__init__("products", client)


class SupabaseInventoryRepository(SupabaseBaseRepository):
    def __init__(self, client: Optional[SupabaseClient] = None):
        super().__init__("inventory", client)


class SupabaseProductRelationshipRepository(SupabaseBaseRepository):
    def __init__(self, client: Optional[SupabaseClient] = None):
        super().__init__("product_relationships", client)

    async def get_relationships_for_product(self, product_id: str) -> List[Dict[str, Any]]:
        return await self.find_many({"source_product_id": product_id})


class SupabaseOrderRepository(SupabaseBaseRepository):
    def __init__(self, client: Optional[SupabaseClient] = None):
        super().__init__("orders", client)


class SupabaseOrderItemRepository(SupabaseBaseRepository):
    def __init__(self, client: Optional[SupabaseClient] = None):
        super().__init__("order_items", client)


class SupabasePaymentRepository(SupabaseBaseRepository):
    def __init__(self, client: Optional[SupabaseClient] = None):
        super().__init__("payments", client)


class SupabaseOpportunityRepository(SupabaseBaseRepository):
    def __init__(self, client: Optional[SupabaseClient] = None):
        super().__init__("opportunities", client)


class SupabaseExperimentRepository(SupabaseBaseRepository):
    def __init__(self, client: Optional[SupabaseClient] = None):
        super().__init__("experiments", client)


class SupabasePolicyRepository(SupabaseBaseRepository):
    def __init__(self, client: Optional[SupabaseClient] = None):
        super().__init__("policies", client)


class SupabaseAgentActivityRepository(SupabaseBaseRepository):
    def __init__(self, client: Optional[SupabaseClient] = None):
        super().__init__("agent_activity", client)


class SupabaseAuditRepository(SupabaseBaseRepository):
    def __init__(self, client: Optional[SupabaseClient] = None):
        super().__init__("audit_events", client)


class SupabaseBuyerSessionRepository(SupabaseBaseRepository):
    def __init__(self, client: Optional[SupabaseClient] = None):
        super().__init__("buyer_sessions", client)


class SupabaseBasketRepository(SupabaseBaseRepository):
    def __init__(self, client: Optional[SupabaseClient] = None):
        super().__init__("baskets", client)


class SupabaseCheckoutIntentRepository(SupabaseBaseRepository):
    def __init__(self, client: Optional[SupabaseClient] = None):
        super().__init__("checkout_intents", client)
