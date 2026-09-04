"""
NOT ACTIVE AT RUNTIME — Reference implementation for a future Supabase/Postgres migration.
See docs/DATABASE_DECISION.md for details. Authoritative runtime database is MongoDB.
"""
import logging
from typing import Any, Dict, List, Optional
import httpx

from app.core.config import Settings, get_settings

logger = logging.getLogger("raygo.supabase")

class SupabaseClient:
    """Async Supabase client wrapper providing resilient data operations,

    error normalization, connection health checks, and automatic fallback.
    """

    def __init__(self, url: str = "", key: str = ""):
        self.url = url.rstrip("/") if url else ""
        self.key = key
        self._http_client: Optional[httpx.AsyncClient] = None
        self._in_memory_store: Dict[str, List[Dict[str, Any]]] = {}

    @property
    def is_configured(self) -> bool:
        return bool(self.url and self.key and "supabase.co" in self.url)

    def _get_client(self) -> httpx.AsyncClient:
        if self._http_client is None or self._http_client.is_closed:
            headers = {
                "apikey": self.key,
                "Authorization": f"Bearer {self.key}",
                "Content-Type": "application/json",
                "Prefer": "return=representation",
            }
            self._http_client = httpx.AsyncClient(
                base_url=f"{self.url}/rest/v1",
                headers=headers,
                timeout=10.0,
            )
        return self._http_client

    async def close(self) -> None:
        if self._http_client and not self._http_client.is_closed:
            await self._http_client.aclose()
            self._http_client = None

    async def ping(self) -> bool:
        if not self.is_configured:
            return False
        try:
            client = self._get_client()
            resp = await client.get("/", timeout=2.5)
            return resp.status_code in (200, 206)
        except Exception as e:
            logger.warning(f"Supabase ping failed: {e}")
            return False

    def init_in_memory_collection(self, table: str, initial_data: List[Dict[str, Any]]) -> None:
        self._in_memory_store[table] = [dict(item) for item in initial_data]

    async def select(self, table: str, query: Optional[Dict[str, Any]] = None, limit: int = 100) -> List[Dict[str, Any]]:
        if self.is_configured:
            try:
                client = self._get_client()
                params = {"limit": str(limit)}
                if query:
                    for k, v in query.items():
                        params[f"{k}"] = f"eq.{v}"
                resp = await client.get(f"/{table}", params=params)
                if resp.status_code in (200, 206):
                    return resp.json()
            except Exception as e:
                logger.warning(f"Supabase query failed on {table}: {e}, using local fallback")

        items = self._in_memory_store.get(table, [])
        if not query:
            return items[:limit]
        filtered = [
            item for item in items
            if all(item.get(k) == v for k, v in query.items())
        ]
        return filtered[:limit]

    async def insert(self, table: str, data: Dict[str, Any]) -> Dict[str, Any]:
        if self.is_configured:
            try:
                client = self._get_client()
                resp = await client.post(f"/{table}", json=data)
                if resp.status_code in (200, 201):
                    res = resp.json()
                    return res[0] if isinstance(res, list) and res else data
            except Exception as e:
                logger.warning(f"Supabase insert failed on {table}: {e}, writing to local fallback")

        if table not in self._in_memory_store:
            self._in_memory_store[table] = []
        self._in_memory_store[table].append(data)
        return data

    async def update(self, table: str, query: Dict[str, Any], updates: Dict[str, Any]) -> List[Dict[str, Any]]:
        if self.is_configured:
            try:
                client = self._get_client()
                params = {}
                for k, v in query.items():
                    params[f"{k}"] = f"eq.{v}"
                resp = await client.patch(f"/{table}", params=params, json=updates)
                if resp.status_code in (200, 204):
                    return resp.json() if resp.text else [updates]
            except Exception as e:
                logger.warning(f"Supabase update failed on {table}: {e}, updating local fallback")

        items = self._in_memory_store.get(table, [])
        updated = []
        for item in items:
            if all(item.get(k) == v for k, v in query.items()):
                item.update(updates)
                updated.append(item)
        return updated


def get_supabase_client(settings: Optional[Settings] = None) -> SupabaseClient:
    s = settings or get_settings()
    key = s.supabase_service_role_key or s.supabase_anon_key
    return SupabaseClient(url=s.supabase_url, key=key)
