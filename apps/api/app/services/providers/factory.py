import logging
import time

from app.core.config import Settings
from app.core.errors import RaygoError
from app.services.providers.base import AgentProvider, SchemaT
from app.services.providers.deterministic_provider import DeterministicProvider

logger = logging.getLogger("raygo.providers")

_deterministic = DeterministicProvider()


def build_primary_provider(settings: Settings) -> AgentProvider:
    """Returns the provider that should be tried first. Never returns None —
    when Gemini isn't configured or mock mode is on, the deterministic
    provider IS the primary, not just a fallback."""
    if settings.gemini_api_key and not settings.use_mock_agents:
        from app.services.providers.gemini_provider import GeminiProvider

        return GeminiProvider(settings)
    return _deterministic


async def generate_with_fallback(
    settings: Settings, task: str, context: dict, schema: type[SchemaT]
) -> tuple[SchemaT, str, str | None]:
    """Returns (result, mode, fallback_reason). mode is "gemini" or
    "deterministic". fallback_reason is set only when Gemini was configured
    but failed and we fell back. Logs latency for every call so slow
    provider calls are visible without needing a profiler (PRD section 14 —
    observability)."""
    primary = build_primary_provider(settings)
    started = time.perf_counter()

    if primary.name == "deterministic":
        result = await primary.generate_structured(task, context, schema)
        latency_ms = round((time.perf_counter() - started) * 1000, 2)
        logger.info(
            "agent_provider_call",
            extra={"task": task, "provider": "deterministic", "latencyMs": latency_ms},
        )
        return result, "deterministic", None

    try:
        result = await primary.generate_structured(task, context, schema)
        latency_ms = round((time.perf_counter() - started) * 1000, 2)
        logger.info(
            "agent_provider_call",
            extra={"task": task, "provider": "gemini", "latencyMs": latency_ms},
        )
        return result, "gemini", None
    except RaygoError as exc:
        gemini_latency_ms = round((time.perf_counter() - started) * 1000, 2)
        logger.warning(
            "agent_provider_fallback",
            extra={
                "task": task,
                "provider": "gemini",
                "errorCode": exc.code,
                "latencyMs": gemini_latency_ms,
            },
        )
        fallback_started = time.perf_counter()
        result = await _deterministic.generate_structured(task, context, schema)
        fallback_latency_ms = round((time.perf_counter() - fallback_started) * 1000, 2)
        logger.info(
            "agent_provider_call",
            extra={"task": task, "provider": "deterministic", "latencyMs": fallback_latency_ms},
        )
        return result, "deterministic", exc.code
