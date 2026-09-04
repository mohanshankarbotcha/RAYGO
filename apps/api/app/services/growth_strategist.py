from app.core.config import Settings
from app.domain.agent_schemas import GrowthHypothesisOutput
from app.repositories.registry import Repositories
from app.services.providers.factory import generate_with_fallback

# MVP deterministic mapping: opportunity -> experiment proposal.
# For opp_keyboard_stand this reproduces exp_keyboard_stand exactly.
_EXPERIMENT_TEMPLATES: dict[str, dict] = {
    "opp_keyboard_stand": {
        "id": "exp_keyboard_stand",
        "name": "Keyboard + Laptop Stand",
        "hypothesis": (
            "Bundling a Laptop Stand with Wireless Keyboard purchases will increase "
            "basket conversion without reducing merchant margin below policy."
        ),
        "discountPct": 10,
        "estimatedMarginPct": 32,
        "controlConversion": 6.2,
        "variantConversion": 8.9,
        "conversionUplift": 43.5,
        "revenueUplift": 23.4,
        "aovUplift": 8.7,
        "confidence": 94,
        "recommendation": "scale_variant",
    }
}


class GrowthStrategistService:
    def __init__(self, repos: Repositories):
        self.repos = repos

    def propose_experiment(self, opportunity: dict) -> dict:
        template = _EXPERIMENT_TEMPLATES.get(opportunity["id"])
        if template:
            return dict(template)
        # generic fallback for any future opportunity
        return {
            "id": f"exp_{opportunity['id'].removeprefix('opp_')}",
            "name": opportunity.get("shortTitle", opportunity["id"]),
            "hypothesis": f"Testing {opportunity.get('recommendedAction', 'the proposed action')}.",
            "discountPct": 10,
            "estimatedMarginPct": 30,
            "controlConversion": opportunity.get("currentAttachRate", 5.0),
            "variantConversion": opportunity.get("projectedAttachRate", 8.0),
            "conversionUplift": 20.0,
            "revenueUplift": 15.0,
            "aovUplift": 5.0,
            "confidence": opportunity.get("confidence", 80),
            "recommendation": "keep_running",
        }

    async def propose_experiment_with_mode(
        self, opportunity: dict, settings: Settings
    ) -> tuple[dict, str, str | None]:
        """Returns (proposal, mode, fallback_reason). The proposal's numeric
        fields always come from `propose_experiment` (deterministic); only
        the `hypothesis` narrative may be replaced with Gemini's phrasing,
        and only after schema validation succeeds."""
        proposal = self.propose_experiment(opportunity)
        result, mode, fallback_reason = await generate_with_fallback(
            settings,
            task="growth_hypothesis",
            context={"opportunity": opportunity, "proposal": proposal},
            schema=GrowthHypothesisOutput,
        )
        proposal = dict(proposal)
        proposal["hypothesis"] = result.hypothesis
        return proposal, mode, fallback_reason
