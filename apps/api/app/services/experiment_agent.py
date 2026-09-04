from app.repositories.base import utcnow_iso
from app.repositories.registry import Repositories


class ExperimentAgentService:
    def __init__(self, repos: Repositories):
        self.repos = repos

    async def create_from_proposal(self, merchant_id: str, opportunity_id: str, proposal: dict) -> dict:
        existing = await self.repos.experiments.get(proposal["id"])
        if existing:
            return existing
        doc = {
            "id": proposal["id"],
            "merchantId": merchant_id,
            "opportunityId": opportunity_id,
            "name": proposal["name"],
            "status": "running",
            "hypothesis": proposal["hypothesis"],
            "controlConversion": proposal["controlConversion"],
            "variantConversion": proposal["variantConversion"],
            "conversionUplift": proposal["conversionUplift"],
            "revenueUplift": proposal["revenueUplift"],
            "aovUplift": proposal["aovUplift"],
            "confidence": proposal["confidence"],
            "recommendation": proposal["recommendation"],
            "decisionReason": (
                "Variant performance exceeds control while remaining within the "
                "merchant's margin policy."
            ),
            "metadata": {"discountPct": proposal["discountPct"]},
        }
        return await self.repos.experiments.upsert(doc)

    async def scale(self, experiment_id: str) -> dict | None:
        return await self.repos.experiments.update(experiment_id, {"status": "scaled"})
