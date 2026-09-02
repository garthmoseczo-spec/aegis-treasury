from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from backend.auth import get_current_principal, require_role
from backend.schemas import Principal, TenantCreateRequest, TenantResponse
from backend.services.billing_service import get_tenant_plan, set_tenant_plan
from backend.services.tenant_service import create_tenant, list_tenants


router = APIRouter(prefix="/admin", tags=["admin"])


class TenantPlanUpdateRequest(BaseModel):
    plan_id: str = Field(min_length=1)


@router.post("/tenants", response_model=TenantResponse)
def create_tenant_route(
    request: TenantCreateRequest,
    principal: Principal = Depends(get_current_principal),
) -> TenantResponse:
    require_role(principal, "admin")
    tenant = create_tenant(name=request.name, plan_id=request.plan_id)
    set_tenant_plan(tenant["tenant_id"], request.plan_id)
    return TenantResponse(**tenant)


@router.get("/tenants", response_model=list[TenantResponse])
def list_tenants_route(
    principal: Principal = Depends(get_current_principal),
) -> list[TenantResponse]:
    require_role(principal, "admin")
    tenants = list_tenants()
    return [TenantResponse(**tenant) for tenant in tenants]


@router.put("/tenants/{tenant_id}/plan")
def update_plan_route(
    tenant_id: str,
    request: TenantPlanUpdateRequest,
    principal: Principal = Depends(get_current_principal),
) -> dict:
    require_role(principal, "admin")
    plan = set_tenant_plan(tenant_id, request.plan_id)
    return plan


@router.get("/tenants/{tenant_id}/plan")
def get_plan_route(
    tenant_id: str,
    principal: Principal = Depends(get_current_principal),
) -> dict:
    require_role(principal, "admin")
    plan = get_tenant_plan(tenant_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="Tenant plan not found")
    return plan
