from fastapi import APIRouter

from app.api.v1 import (
    agents,
    ai_buyer,
    ai_commerce,
    audit,
    dashboard,
    experiments,
    health,
    merchant,
    opportunities,
    payments,
    policies,
    products,
)

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(merchant.router)
api_router.include_router(dashboard.router)
api_router.include_router(products.router)
api_router.include_router(opportunities.router)
api_router.include_router(experiments.router)
api_router.include_router(ai_commerce.router)
api_router.include_router(ai_buyer.router)
api_router.include_router(payments.router)
api_router.include_router(policies.router)
api_router.include_router(agents.router)
api_router.include_router(audit.router)
