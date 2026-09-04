from fastapi import APIRouter, Depends, Request

from app.api.deps import get_dashboard_service
from app.core.security import resolve_merchant_id
from app.services.dashboard_service import DashboardService

router = APIRouter(tags=["dashboard"])


@router.get("/dashboard/overview")
@router.get("/dashboard/metrics")
async def dashboard_overview(request: Request, service: DashboardService = Depends(get_dashboard_service)):
    merchant_id = resolve_merchant_id(request)
    return await service.overview(merchant_id)
