"""Placeholder seam for the future Google ADK orchestrator.

Per PRD section 20: ADK may orchestrate agent sequencing only after
deterministic MVP flows pass tests, and only inside the backend's typed,
policy-gated, auditable boundaries. It must never bypass Policy Guard,
directly execute payments, or hide decisions from Audit Trail.
"""

from app.core.config import Settings


class AdkOrchestrator:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.enabled = settings.use_adk_orchestrator

    async def run_sequence(self, sequence_name: str, context: dict) -> dict:
        if not self.enabled:
            raise NotImplementedError(
                "AdkOrchestrator is a Phase 4 seam. Set USE_ADK_ORCHESTRATOR=true "
                "and implement orchestration here once deterministic flows are stable."
            )
        raise NotImplementedError("ADK orchestration is implemented in a later phase.")
