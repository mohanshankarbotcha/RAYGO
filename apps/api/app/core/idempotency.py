import hashlib
import json
from datetime import datetime, timedelta, timezone
from typing import Any

from app.core.errors import IdempotencyConflictError


def _hash_request(payload: Any) -> str:
    normalized = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


class IdempotencyService:
    """Backed by the `idempotency_records` collection.

    Same key + route + request hash -> return cached response.
    Same key + route + different hash -> 409 IDEMPOTENCY_CONFLICT.
    """

    def __init__(self, collection):
        self.collection = collection

    async def check_and_store(
        self,
        key: str | None,
        route: str,
        method: str,
        payload: Any,
        ttl_hours: int = 24,
    ) -> dict | None:
        """Returns a cached response dict if one exists, else None (caller should
        proceed and call `store_response` once it has a result)."""
        if not key:
            return None
        request_hash = _hash_request(payload)
        existing = await self.collection.find_one({"key": key, "route": route})
        if existing:
            if existing["requestHash"] != request_hash:
                raise IdempotencyConflictError(
                    "Idempotency-Key was reused with a different request body.",
                    {"key": key, "route": route},
                )
            return existing.get("responseBody")
        # reserve the slot so concurrent calls don't double-execute; caller fills body in later
        now = datetime.now(timezone.utc)
        await self.collection.update_one(
            {"key": key, "route": route},
            {
                "$setOnInsert": {
                    "key": key,
                    "route": route,
                    "method": method,
                    "requestHash": request_hash,
                    "responseStatus": None,
                    "responseBody": None,
                    "createdAt": now,
                    "expiresAt": now + timedelta(hours=ttl_hours),
                }
            },
            upsert=True,
        )
        return None

    async def store_response(self, key: str | None, route: str, status_code: int, body: Any) -> None:
        if not key:
            return
        await self.collection.update_one(
            {"key": key, "route": route},
            {"$set": {"responseStatus": status_code, "responseBody": body}},
        )
