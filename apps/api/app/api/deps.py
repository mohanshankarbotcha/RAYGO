from fastapi import Request

from app.core.config import Settings, get_settings
from app.core.idempotency import IdempotencyService
from app.db.mongo import get_db
from app.repositories.registry import Repositories, get_repositories
from app.services.ai_buyer_service import AiBuyerService
from app.services.ai_commerce_agent import AiCommerceAgentService
from app.services.approval_gateway import ApprovalGateway
from app.services.audit_service import AuditService
from app.services.dashboard_service import DashboardService
from app.services.experiment_agent import ExperimentAgentService
from app.services.growth_strategist import GrowthStrategistService
from app.services.merchant_service import MerchantService
from app.services.order_intent_service import OrderIntentService
from app.services.payment_agent import PaymentAgentService
from app.services.policy_guard import PolicyGuard
from app.services.product_service import ProductService
from app.services.razorpay_service import RazorpayService
from app.services.revenue_intelligence import RevenueIntelligenceService


def get_repos(request: Request) -> Repositories:
    db = getattr(request.app.state, "db", None) or get_db()
    return get_repositories(db)


def get_settings_dep() -> Settings:
    return get_settings()


def get_idempotency(request: Request) -> IdempotencyService:
    return IdempotencyService(get_repos(request).idempotency_records)


def get_audit_service(request: Request) -> AuditService:
    return AuditService(get_repos(request))


def get_policy_guard(request: Request) -> PolicyGuard:
    return PolicyGuard(get_repos(request))


def get_approval_gateway(request: Request) -> ApprovalGateway:
    return ApprovalGateway(get_repos(request))


def get_merchant_service(request: Request) -> MerchantService:
    return MerchantService(get_repos(request))


def get_dashboard_service(request: Request) -> DashboardService:
    return DashboardService(get_repos(request))


def get_product_service(request: Request) -> ProductService:
    return ProductService(get_repos(request))


def get_revenue_intelligence(request: Request) -> RevenueIntelligenceService:
    return RevenueIntelligenceService(get_repos(request))


def get_growth_strategist(request: Request) -> GrowthStrategistService:
    return GrowthStrategistService(get_repos(request))


def get_experiment_agent(request: Request) -> ExperimentAgentService:
    return ExperimentAgentService(get_repos(request))


def get_ai_commerce_agent(request: Request) -> AiCommerceAgentService:
    return AiCommerceAgentService(get_repos(request))


def get_ai_buyer_service(request: Request) -> AiBuyerService:
    return AiBuyerService(get_repos(request))


def get_order_intent_service(request: Request) -> OrderIntentService:
    return OrderIntentService(get_repos(request))


def get_razorpay_service(request: Request) -> RazorpayService:
    cached = getattr(request.app.state, "razorpay_service", None)
    if cached:
        return cached
    return RazorpayService(get_settings())


def get_payment_agent(request: Request) -> PaymentAgentService:
    return PaymentAgentService(get_repos(request), get_razorpay_service(request))
