from pydantic import BaseModel, ConfigDict, Field

from app.domain.schemas import to_camel


class AgentCamelModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class CoordinatorOutput(AgentCamelModel):
    """Structured routing decision. Advisory only — the coordinator never
    executes a financial or consequential action itself."""

    intent: str
    agent: str
    action: str
    requires_approval: bool = True
    confidence: float = Field(ge=0.0, le=1.0)
    reason: str
    next_step: str


class OpportunityReasoning(AgentCamelModel):
    """Narrative explanation of an opportunity. `estimated_impact` and
    `confidence` must echo the backend-calculated values passed in as
    context — the model interprets them, it does not invent them."""

    opportunity_id: str
    type: str
    title: str
    evidence: list[str]
    estimated_impact: float
    confidence: float = Field(ge=0.0, le=1.0)
    risk: str
    recommended_action: str
    requires_approval: bool = True


class GrowthHypothesisOutput(AgentCamelModel):
    hypothesis: str
    action_type: str
    expected_impact: float
    risk: str
    policy_requirements: list[str] = Field(default_factory=list)
    requires_approval: bool = True


class ExperimentRecommendationOutput(AgentCamelModel):
    recommendation: str  # SCALE | KEEP_RUNNING | STOP
    reason: str
    confidence: float = Field(ge=0.0, le=1.0)


class CommerceIntentOutput(AgentCamelModel):
    category: str
    budget_max: float | None = None
    use_cases: list[str] = Field(default_factory=list)


class CopilotResponse(AgentCamelModel):
    answer: str
    intent: str
    evidence: list[str] = Field(default_factory=list)
    related_entities: list[dict] = Field(default_factory=list)
    recommended_action: str | None = None
    action_status: str = "none"
    policy_status: str | None = None
    approval_required: bool = False
    correlation_id: str

