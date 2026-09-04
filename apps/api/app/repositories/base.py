from datetime import datetime, timezone
from typing import Any

from motor.motor_asyncio import AsyncIOMotorCollection


def utcnow_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def strip_mongo_id(doc: dict | None) -> dict | None:
    if doc is None:
        return None
    doc = dict(doc)
    doc.pop("_id", None)
    return doc


class MongoRepository:
    """Thin wrapper around a Motor collection. Documents use `id` as the
    public identifier; API responses must never leak Mongo's `_id`."""

    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def get(self, doc_id: str) -> dict | None:
        return strip_mongo_id(await self.collection.find_one({"id": doc_id}))

    async def find_one(self, query: dict) -> dict | None:
        return strip_mongo_id(await self.collection.find_one(query))

    async def find_many(
        self, query: dict, limit: int = 50, sort: list[tuple[str, int]] | None = None, skip: int = 0
    ) -> list[dict]:
        cursor = self.collection.find(query)
        if sort:
            cursor = cursor.sort(sort)
        if skip:
            cursor = cursor.skip(skip)
        cursor = cursor.limit(limit)
        return [strip_mongo_id(doc) async for doc in cursor]

    async def count(self, query: dict) -> int:
        return await self.collection.count_documents(query)

    async def upsert(self, doc: dict) -> dict:
        now = utcnow_iso()
        doc.setdefault("createdAt", now)
        doc["updatedAt"] = now
        await self.collection.update_one({"id": doc["id"]}, {"$set": doc}, upsert=True)
        return await self.get(doc["id"])

    async def update(self, doc_id: str, patch: dict) -> dict | None:
        patch = dict(patch)
        patch["updatedAt"] = utcnow_iso()
        await self.collection.update_one({"id": doc_id}, {"$set": patch})
        return await self.get(doc_id)

    async def insert(self, doc: dict) -> dict:
        now = utcnow_iso()
        doc.setdefault("createdAt", now)
        doc.setdefault("updatedAt", now)
        await self.collection.insert_one(dict(doc))
        return strip_mongo_id(doc)

    async def delete_all(self) -> None:
        await self.collection.delete_many({})
