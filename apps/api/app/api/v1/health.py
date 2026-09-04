from fastapi import APIRouter, Depends, Request

from app.core.config import Settings, get_settings

router = APIRouter(tags=["health"])


@router.get("/health")
async def health(settings: Settings = Depends(get_settings)):
    gemini_configured = bool(settings.gemini_api_key and not settings.use_mock_agents)
    razorpay_configured = bool(settings.razorpay_key_id and settings.razorpay_key_secret)

    return {
        "status": "ok",
        "service": "raygo-api",
        "version": "0.1.0",
        "environment": settings.environment,
        "database": "mongodb",
        "supabaseStatus": "scaffolded_not_active",
        "services": {
            "database": "mongodb_active",
            "ai": "gemini_connected" if gemini_configured else "deterministic_active",
            "razorpay": "live_test_mode" if razorpay_configured else "stub_active",
        },
    }


@router.get("/health/db")
async def health_db(request: Request, settings: Settings = Depends(get_settings)):
    db = getattr(request.app.state, "db", None)
    mongo_connected = False
    if db is not None:
        try:
            await db.command("ping")
            mongo_connected = True
        except Exception:
            mongo_connected = False

    return {
        "status": "ok" if mongo_connected else "error",
        "database": "mongodb",
        "databaseName": settings.mongodb_db,
        "supabaseStatus": "scaffolded_not_active",
        "connected": mongo_connected,
    }

