import uuid

from app.core.config import Settings
from app.domain.agent_schemas import CoordinatorOutput
from app.services.providers.factory import generate_with_fallback


def new_coordinator_request_id() -> str:
    return f"coord_{uuid.uuid4().hex[:10]}"


class RaygoCoordinator:
    """Routes a natural-language request to a specialist agent. The
    coordinator is read-only and advisory: it returns a routing decision,
    never executes a tool, mutates data, or touches payments. Every
    consequential action still goes through the existing REST endpoints,
    which enforce Policy Guard and Approval Gateway independently of
    anything the coordinator (or Gemini) says."""

    def __init__(self, settings: Settings):
        self.settings = settings

    async def route(self, request_text: str) -> tuple[CoordinatorOutput, str, str | None]:
        result, mode, fallback_reason = await generate_with_fallback(
            self.settings,
            task="coordinator_route",
            context={"requestText": request_text},
            schema=CoordinatorOutput,
        )
        return result, mode, fallback_reason
