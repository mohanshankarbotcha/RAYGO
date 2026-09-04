import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from mongomock_motor import AsyncMongoMockClient

from app.core.config import Settings, get_settings
from app.db.indexes import ensure_indexes
from app.db.seed import seed as run_seed
from app.main import app


@pytest.fixture(autouse=True)
def override_test_settings(monkeypatch):
    """Ensure automated unit test suite runs in deterministic isolation."""
    test_settings = Settings(
        environment="test",
        use_mock_agents=True,
        gemini_api_key="",
        supabase_url="",
        supabase_anon_key="",
        supabase_service_role_key="",
    )
    app.dependency_overrides[get_settings] = lambda: test_settings
    yield test_settings
    app.dependency_overrides.pop(get_settings, None)


@pytest_asyncio.fixture
async def test_db():
    client = AsyncMongoMockClient()
    db = client["raygo_test"]
    await ensure_indexes(db)
    await run_seed(db)
    yield db


@pytest_asyncio.fixture
async def client(test_db):
    app.state.db = test_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
