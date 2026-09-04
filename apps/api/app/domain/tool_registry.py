from dataclasses import dataclass, field
from enum import Enum


class SideEffect(str, Enum):
    READ_ONLY = "READ_ONLY"
    SAFE_WRITE = "SAFE_WRITE"
    CONSEQUENTIAL = "CONSEQUENTIAL"
    FINANCIAL = "FINANCIAL"


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    side_effect: SideEffect
    requires_approval: bool
    owning_agent: str
    # The REST endpoint that actually performs this tool's work today. Gemini
    # never calls this directly — it names the tool in its structured output;
    # the backend endpoint below is what actually executes, with Policy Guard
    # and Approval Gateway already enforced inside it.
    backend_endpoint: str


TOOL_REGISTRY: dict[str, ToolSpec] = {}


def _register(spec: ToolSpec) -> None:
    TOOL_REGISTRY[spec.name] = spec


# Revenue
_register(ToolSpec("get_revenue_summary", "Read merchant revenue metrics.", SideEffect.READ_ONLY, False, "revenue_intelligence", "GET /dashboard/overview"))
_register(ToolSpec("get_product_performance", "Read product-level performance.", SideEffect.READ_ONLY, False, "revenue_intelligence", "GET /products"))
_register(ToolSpec("get_customer_product_affinity", "Read cross-sell/affinity signals backing an opportunity.", SideEffect.READ_ONLY, False, "revenue_intelligence", "GET /opportunities/{id}"))
_register(ToolSpec("get_opportunity_candidates", "Read ranked opportunity candidates.", SideEffect.READ_ONLY, False, "revenue_intelligence", "GET /opportunities"))

# Growth
_register(ToolSpec("validate_growth_action", "Check a proposed growth action's shape before policy evaluation.", SideEffect.READ_ONLY, False, "growth_strategist", "POST /policies/evaluate"))
_register(ToolSpec("preview_experiment", "Preview an experiment proposal without creating it.", SideEffect.READ_ONLY, False, "growth_strategist", "GET /opportunities/{id}"))

# Experiments
_register(ToolSpec("create_experiment", "Create an experiment from an approved opportunity.", SideEffect.CONSEQUENTIAL, True, "experiment_agent", "POST /opportunities/{id}/approve"))
_register(ToolSpec("get_experiment", "Read experiment detail.", SideEffect.READ_ONLY, False, "experiment_agent", "GET /experiments/{id}"))
_register(ToolSpec("evaluate_experiment", "Evaluate experiment metrics.", SideEffect.READ_ONLY, False, "experiment_agent", "GET /experiments/{id}"))
_register(ToolSpec("recommend_scale", "Recommend and, once approved, execute scaling an experiment.", SideEffect.CONSEQUENTIAL, True, "experiment_agent", "POST /experiments/{id}/scale"))

# Commerce
_register(ToolSpec("search_products", "Search the catalog for buyer-intent-matching products.", SideEffect.READ_ONLY, False, "ai_commerce", "POST /ai-buyer/search"))
_register(ToolSpec("get_product", "Read a single product's AI-readable profile.", SideEffect.READ_ONLY, False, "ai_commerce", "GET /ai-commerce/products/{id}/profile"))
_register(ToolSpec("get_catalog_readiness", "Read AI Commerce readiness score.", SideEffect.READ_ONLY, False, "ai_commerce", "GET /ai-commerce/readiness"))
_register(ToolSpec("optimize_product_metadata", "Update product AI-readiness metadata.", SideEffect.SAFE_WRITE, False, "ai_commerce", "POST /ai-commerce/optimize-catalog"))
_register(ToolSpec("construct_basket", "Build a basket from matched products.", SideEffect.SAFE_WRITE, False, "ai_commerce", "POST /ai-buyer/basket"))

# Policy
_register(ToolSpec("check_policy", "Evaluate a proposed action against Policy Guard.", SideEffect.READ_ONLY, False, "policy_guard", "POST /policies/evaluate"))
_register(ToolSpec("get_policy", "Read current policy configuration.", SideEffect.READ_ONLY, False, "policy_guard", "GET /policies"))
_register(ToolSpec("request_approval", "Request merchant approval for a consequential action.", SideEffect.SAFE_WRITE, False, "approval_gateway", "internal — invoked by approve/scale endpoints"))

# Payment
_register(ToolSpec("create_order", "Create a Razorpay Test Mode order for an authorized order intent.", SideEffect.FINANCIAL, True, "payment_agent", "POST /payments/razorpay/order"))
_register(ToolSpec("get_payment_status", "Read payment attempt status.", SideEffect.READ_ONLY, False, "payment_agent", "GET /payments"))
_register(ToolSpec("verify_payment", "Verify a Razorpay payment signature server-side.", SideEffect.FINANCIAL, False, "payment_agent", "POST /payments/razorpay/verify"))

# Audit
_register(ToolSpec("record_agent_action", "Write an audit event for a consequential action.", SideEffect.SAFE_WRITE, False, "audit_service", "internal — invoked by every consequential endpoint"))
_register(ToolSpec("get_agent_activity", "Read the agent activity timeline.", SideEffect.READ_ONLY, False, "audit_service", "GET /agents/activity"))
_register(ToolSpec("get_audit_record", "Read a single audit event.", SideEffect.READ_ONLY, False, "audit_service", "GET /audit/{id}"))


def get_tool(name: str) -> ToolSpec | None:
    return TOOL_REGISTRY.get(name)


def is_allowed(name: str) -> bool:
    return name in TOOL_REGISTRY


def list_tools() -> list[dict]:
    return [
        {
            "name": spec.name,
            "description": spec.description,
            "sideEffect": spec.side_effect.value,
            "requiresApproval": spec.requires_approval,
            "owningAgent": spec.owning_agent,
            "backendEndpoint": spec.backend_endpoint,
        }
        for spec in TOOL_REGISTRY.values()
    ]
