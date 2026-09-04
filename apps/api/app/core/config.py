from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "local"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_base_url: str = "http://localhost:8000/api/v1"
    frontend_origin: str = "http://localhost:3000"

    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db: str = "raygo"
    seed_on_startup: bool = True
    allow_demo_reset: bool = True

    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_role_key: str = ""
    supabase_db_password: str = ""

    razorpay_mode: str = "test"
    razorpay_key_id: str = ""
    razorpay_key_secret: str = ""
    razorpay_webhook_secret: str = ""
    allow_razorpay_stub: bool = True

    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"
    gemini_temperature: float = 0.2
    gemini_timeout_seconds: int = 30
    gemini_max_retries: int = 2
    use_mock_agents: bool = True
    use_adk_orchestrator: bool = False

    log_level: str = "INFO"
    request_timeout_seconds: int = 30
    idempotency_ttl_hours: int = 24


@lru_cache
def get_settings() -> Settings:
    return Settings()
