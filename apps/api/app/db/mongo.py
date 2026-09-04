from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import get_settings

_client: AsyncIOMotorClient | None = None
_db: AsyncIOMotorDatabase | None = None


def connect_to_mongo() -> AsyncIOMotorDatabase:
    global _client, _db
    if _db is not None:
        return _db
    settings = get_settings()
    _client = AsyncIOMotorClient(settings.mongodb_uri, serverSelectionTimeoutMS=500)
    _db = _client[settings.mongodb_db]
    return _db


def get_db() -> AsyncIOMotorDatabase:
    if _db is None:
        return connect_to_mongo()
    return _db


def set_db(db: AsyncIOMotorDatabase) -> None:
    """Allows tests to inject an in-memory database."""
    global _db
    _db = db


async def close_mongo_connection() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None


async def ping_db() -> bool:
    try:
        await get_db().command("ping")
        return True
    except Exception:
        return False
