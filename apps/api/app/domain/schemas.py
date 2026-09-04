from pydantic import BaseModel, ConfigDict, Field


def to_camel(s: str) -> str:
    parts = s.split("_")
    return parts[0] + "".join(p.title() for p in parts[1:])


class CamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class OnboardingInitializeRequest(CamelModel):
    merchant_id: str = "merchant_novatech"
    reset_demo_data: bool = True


class OpportunityApproveRequest(CamelModel):
    merchant_id: str = "merchant_novatech"
    approved_by: str = "merchant_demo_user"
    confirmation_text: str = "Approve & Create Experiment"


class OpportunityRejectRequest(CamelModel):
    merchant_id: str = "merchant_novatech"
    rejected_by: str = "merchant_demo_user"
    reason: str = "Merchant declined the recommendation."


class ExperimentScaleRequest(CamelModel):
    merchant_id: str = "merchant_novatech"
    approved_by: str = "merchant_demo_user"
    confirmation_text: str = "Scale Experiment"


class ExperimentRejectRequest(CamelModel):
    merchant_id: str = "merchant_novatech"
    rejected_by: str = "merchant_demo_user"
    reason: str = "Merchant declined the recommendation."


class OptimizeCatalogRequest(CamelModel):
    merchant_id: str = "merchant_novatech"
    product_ids: list[str] = Field(default_factory=list)


class AiBuyerSearchRequest(CamelModel):
    merchant_id: str = "merchant_novatech"
    buyer_request: str
    budget: float | None = None
    currency: str = "INR"


class BasketItem(CamelModel):
    product_id: str
    quantity: int = 1


class AiBuyerBasketRequest(CamelModel):
    merchant_id: str = "merchant_novatech"
    buyer_intent_id: str | None = None
    items: list[BasketItem]


class OrderIntentCreateRequest(CamelModel):
    merchant_id: str = "merchant_novatech"
    basket_id: str
    buyer_request: str | None = None


class RazorpayOrderRequest(CamelModel):
    merchant_id: str = "merchant_novatech"
    order_intent_id: str
    approved_by: str = "merchant_demo_user"


class RazorpayVerifyRequest(CamelModel):
    merchant_id: str = "merchant_novatech"
    order_intent_id: str
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str


class RazorpayFailureRequest(CamelModel):
    merchant_id: str = "merchant_novatech"
    order_intent_id: str
    razorpay_order_id: str | None = None
    error_code: str | None = None
    error_description: str = "Payment attempt was unsuccessful. No funds have been captured from your account."
    source: str = "checkout"


class RazorpayDismissRequest(CamelModel):
    merchant_id: str = "merchant_novatech"
    order_intent_id: str
    razorpay_order_id: str | None = None
    reason: str = "Buyer closed checkout modal"


class PolicyPatchRequest(CamelModel):
    merchant_id: str = "merchant_novatech"
    limit: str | None = None
    status: str | None = None


class ProposedAction(CamelModel):
    discount_pct: float | None = None
    estimated_margin_pct: float | None = None
    campaign_spend: float | None = None
    sample_size: int | None = None


class PolicyEvaluateRequest(CamelModel):
    merchant_id: str = "merchant_novatech"
    action_type: str
    target_type: str
    target_id: str
    proposed_action: ProposedAction = Field(default_factory=ProposedAction)


class ProductCreateRequest(CamelModel):
    merchant_id: str = "merchant_novatech"
    id: str | None = None
    name: str
    category_id: str
    price: float
    inventory: int = 0
    sku: str | None = None
    brand: str | None = None
    product_type: str = "PHYSICAL"
    margin_pct: float = 30.0
    specs: dict = Field(default_factory=dict)
    attributes: dict = Field(default_factory=dict)
    shipping: dict = Field(default_factory=dict)
    active: bool = True


class ProductPatchRequest(CamelModel):
    merchant_id: str = "merchant_novatech"
    name: str | None = None
    category_id: str | None = None
    price: float | None = None
    inventory: int | None = None
    sku: str | None = None
    brand: str | None = None
    product_type: str | None = None
    margin_pct: float | None = None
    specs: dict | None = None
    attributes: dict | None = None
    shipping: dict | None = None
    active: bool | None = None


class StockAdjustRequest(CamelModel):
    merchant_id: str = "merchant_novatech"
    quantity: int | None = None
    adjustment: int | None = None
    reason: str = "Manual inventory adjustment by merchant"

