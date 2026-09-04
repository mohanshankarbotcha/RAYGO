from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Request

from app.api.deps import get_audit_service, get_product_service
from app.core.security import resolve_merchant_id
from app.domain.schemas import (
    ProductCreateRequest,
    ProductPatchRequest,
    StockAdjustRequest,
)
from app.services.audit_service import AuditService
from app.services.product_service import ProductService

router = APIRouter(tags=["products"])


@router.get("/categories")
async def list_categories(
    service: ProductService = Depends(get_product_service),
):
    categories = await service.list_categories()
    return {"items": categories, "total": len(categories)}


@router.get("/products")
async def list_products(
    request: Request,
    category: Optional[str] = Query(None, description="Category filter (e.g. CPU, GPU, RAM)"),
    search: Optional[str] = Query(None, description="Search term across name, sku, brand"),
    stock: Optional[str] = Query(None, description="Stock status: in_stock, low_stock, out_of_stock, all"),
    active: Optional[bool] = Query(None, description="Filter active products"),
    min_readiness: Optional[int] = Query(None, description="Minimum AI readiness score threshold"),
    status: Optional[str] = Query(None, description="Status filter: ready, needs_attention, inactive"),
    sort: Optional[str] = Query(None, description="Sort field: name, price, aiReadiness, inventory"),
    sort_dir: Optional[str] = Query("desc", description="Sort direction: asc, desc"),
    limit: int = Query(50, ge=1, le=200),
    skip: int = Query(0, ge=0),
    service: ProductService = Depends(get_product_service),
):
    merchant_id = resolve_merchant_id(request)
    items, total = await service.list(
        merchant_id=merchant_id,
        category=category,
        search=search,
        stock=stock,
        active=active,
        min_readiness=min_readiness,
        status=status,
        sort=sort,
        sort_dir=sort_dir,
        limit=limit,
        skip=skip,
    )
    return {"items": items, "total": total, "limit": limit, "skip": skip, "nextCursor": None}


@router.get("/products/{product_id}")
async def get_product(
    product_id: str,
    request: Request,
    service: ProductService = Depends(get_product_service),
):
    merchant_id = resolve_merchant_id(request)
    product = await service.get_by_id(merchant_id, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/products", status_code=201)
async def create_product(
    payload: ProductCreateRequest,
    request: Request,
    service: ProductService = Depends(get_product_service),
    audit_service: AuditService = Depends(get_audit_service),
):
    merchant_id = resolve_merchant_id(request) or payload.merchant_id
    created = await service.create(merchant_id, payload, audit_service)
    return created


@router.patch("/products/{product_id}")
async def patch_product(
    product_id: str,
    payload: ProductPatchRequest,
    request: Request,
    service: ProductService = Depends(get_product_service),
    audit_service: AuditService = Depends(get_audit_service),
):
    merchant_id = resolve_merchant_id(request) or payload.merchant_id
    updated = await service.patch(merchant_id, product_id, payload, audit_service)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated


@router.post("/products/{product_id}/stock-adjust")
async def adjust_stock(
    product_id: str,
    payload: StockAdjustRequest,
    request: Request,
    service: ProductService = Depends(get_product_service),
    audit_service: AuditService = Depends(get_audit_service),
):
    merchant_id = resolve_merchant_id(request) or payload.merchant_id
    updated = await service.adjust_stock(
        merchant_id=merchant_id,
        product_id=product_id,
        quantity=payload.quantity,
        adjustment=payload.adjustment,
        reason=payload.reason,
        audit_service=audit_service,
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated


@router.post("/products/{product_id}/activate")
async def activate_product(
    product_id: str,
    request: Request,
    service: ProductService = Depends(get_product_service),
    audit_service: AuditService = Depends(get_audit_service),
):
    merchant_id = resolve_merchant_id(request)
    updated = await service.set_active_status(merchant_id, product_id, active=True, audit_service=audit_service)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated


@router.post("/products/{product_id}/deactivate")
async def deactivate_product(
    product_id: str,
    request: Request,
    service: ProductService = Depends(get_product_service),
    audit_service: AuditService = Depends(get_audit_service),
):
    merchant_id = resolve_merchant_id(request)
    updated = await service.set_active_status(merchant_id, product_id, active=False, audit_service=audit_service)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated
