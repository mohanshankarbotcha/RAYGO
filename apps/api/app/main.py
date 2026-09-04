import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.errors import register_exception_handlers
from app.core.logging import configure_logging, get_logger
from app.core.security import request_id_middleware
from app.db.indexes import ensure_indexes
from app.db.mongo import close_mongo_connection, connect_to_mongo
from app.db.seed import seed as run_seed

settings = get_settings()
configure_logging(settings.log_level)
logger = get_logger("raygo.main")

app = FastAPI(title="RAYGO API", version="0.1.0", docs_url="/docs", redoc_url="/redoc")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin, "http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID"],
)

app.middleware("http")(request_id_middleware)

register_exception_handlers(app)

app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
async def on_startup() -> None:
    db = connect_to_mongo()
    try:
        await db.command("ping")
        app.state.db = db
        await ensure_indexes(db)
        if settings.seed_on_startup:
            await run_seed(db)
    except Exception as e:
        logger.warning(
            f"Could not connect to MongoDB at {settings.mongodb_uri}: {e}. Falling back to in-memory mock database."
        )
        from mongomock_motor import AsyncMongoMockClient
        from app.db.mongo import set_db
        mock_client = AsyncMongoMockClient()
        db = mock_client[settings.mongodb_db]
        set_db(db)
        app.state.db = db
        await ensure_indexes(db)
        if settings.seed_on_startup:
            await run_seed(db)
    logger.info(
        "RAYGO API started",
        extra={
            "route": "startup",
            "method": "SYSTEM",
        },
    )
    print(
        f"[raygo-api] environment={settings.environment} "
        f"mockAgents={settings.use_mock_agents} "
        f"database=mongodb (authoritative: {settings.mongodb_db}) "
        f"supabaseStatus=scaffolded_not_active "
        f"razorpayMode={settings.razorpay_mode} "
        f"razorpayConfigured={bool(settings.razorpay_key_id)}"
    )


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await close_mongo_connection()


@app.middleware("http")
async def log_requests(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration_ms = round((time.time() - start) * 1000, 2)
    logger.info(
        f"{request.method} {request.url.path} -> {response.status_code}",
        extra={
            "requestId": getattr(request.state, "request_id", None),
            "route": request.url.path,
            "method": request.method,
            "statusCode": response.status_code,
            "durationMs": duration_ms,
        },
    )
    return response
