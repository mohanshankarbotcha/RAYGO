from app.domain.agent_schemas import (
    CommerceIntentOutput,
    CoordinatorOutput,
    ExperimentRecommendationOutput,
    GrowthHypothesisOutput,
    OpportunityReasoning,
)
from app.core.errors import ValidationErrorX
from app.services.providers.base import AgentProvider, SchemaT

_REVENUE_KEYWORDS = ("revenue", "opportunity", "cross-sell", "cross sell", "upsell", "bundle", "sales")
_GROWTH_KEYWORDS = ("growth", "hypothesis", "campaign", "strategy")
_EXPERIMENT_KEYWORDS = ("experiment", "scale", "variant", "control", "a/b", "test")
_COMMERCE_KEYWORDS = ("product", "laptop", "buy", "basket", "catalog", "recommend", "search")
_POLICY_KEYWORDS = ("policy", "discount", "margin", "budget", "override", "approve", "approval")
_PAYMENT_KEYWORDS = ("payment", "pay", "checkout", "razorpay", "retry", "refund", "charge")


def _classify_intent(request_text: str) -> tuple[str, str, str]:
    """Deterministic keyword routing used both as the always-available
    fallback and (for the demo) the default coordinator, since it needs no
    external call and is fully unit-testable. Returns (intent, agent, action)."""
    text = request_text.lower()
    if any(k in text for k in _PAYMENT_KEYWORDS):
        return "payment", "payment_agent", "review_payment_status"
    if any(k in text for k in _POLICY_KEYWORDS):
        return "policy", "policy_guard", "check_policy"
    if any(k in text for k in _EXPERIMENT_KEYWORDS):
        return "experiment", "experiment_agent", "evaluate_experiment"
    if any(k in text for k in _COMMERCE_KEYWORDS):
        return "product_discovery", "ai_commerce", "search_products"
    if any(k in text for k in _GROWTH_KEYWORDS):
        return "growth_opportunity", "growth_strategist", "preview_experiment"
    if any(k in text for k in _REVENUE_KEYWORDS):
        return "revenue_analysis", "revenue_intelligence", "analyze_opportunity"
    return "unknown", "revenue_intelligence", "clarify_request"


class DeterministicProvider(AgentProvider):
    name = "deterministic"

    async def generate_structured(self, task: str, context: dict, schema: type[SchemaT]) -> SchemaT:
        if task == "coordinator_route":
            intent, agent, action = _classify_intent(context.get("requestText", ""))
            confidence = 0.55 if intent == "unknown" else 0.75
            payload = {
                "intent": intent,
                "agent": agent,
                "action": action,
                "requiresApproval": intent not in ("unknown",),
                "confidence": confidence,
                "reason": "Deterministic keyword routing (AI reasoning unavailable).",
                "nextStep": "review_opportunity" if intent == "revenue_analysis" else "clarify_request",
            }
        elif task == "opportunity_reasoning":
            opp = context["opportunity"]
            payload = {
                "opportunityId": opp["id"],
                "type": opp["type"],
                "title": opp["title"],
                "evidence": opp.get("evidence", []),
                "estimatedImpact": opp["expectedMonthlyImpact"],
                "confidence": opp["confidence"] / 100,
                "risk": opp["risk"],
                "recommendedAction": opp.get("recommendedAction") or "Review the evidence and approve if it fits your goals.",
                "requiresApproval": True,
            }
        elif task == "growth_hypothesis":
            opp = context["opportunity"]
            proposal = context["proposal"]
            payload = {
                "hypothesis": proposal["hypothesis"],
                "actionType": opp["type"],
                "expectedImpact": opp["expectedMonthlyImpact"],
                "risk": opp["risk"],
                "policyRequirements": ["Discount Limit", "Margin Floor", "Merchant Auth"],
                "requiresApproval": True,
            }
        elif task == "experiment_recommendation":
            exp = context["experiment"]
            rec = exp.get("recommendation", "keep_running")
            mapped = {"scale_variant": "SCALE", "keep_running": "KEEP_RUNNING", "revert_control": "STOP"}.get(
                rec, "KEEP_RUNNING"
            )
            payload = {
                "recommendation": mapped,
                "reason": exp.get(
                    "decisionReason",
                    "Variant performance is being compared against control under current policy limits.",
                ),
                "confidence": exp.get("confidence", 80) / 100,
            }
        elif task == "commerce_intent":
            request_text = context.get("buyerRequest", "")
            budget = context.get("budget")
            use_cases = []
            lowered = request_text.lower()
            for phrase in ("ai development", "college", "gaming", "work", "school", "coding"):
                if phrase in lowered:
                    use_cases.append(phrase)
            payload = {
                "category": "laptop" if "laptop" in lowered else "general",
                "budgetMax": budget,
                "useCases": use_cases or ["general purchase"],
            }
        else:
            raise ValidationErrorX(f"Unknown deterministic task: {task}")

        return schema.model_validate(payload)

    async def health(self) -> dict:
        return {"provider": self.name, "configured": True, "status": "ok"}
