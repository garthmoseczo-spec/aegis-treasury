from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from backend.auth import get_current_principal, require_role
from backend.schemas import (
    LicenseIssueResponse,
    LicenseValidationRequest,
    PlanResponse,
    Principal,
    TenantCreateRequest,
    TenantResponse,
)
from backend.services.license_service import (
    issue_enterprise_license,
    validate_enterprise_license,
)
from backend.services.plan_service import PLAN_CATALOG, plan_exists
from backend.services.secrets_service import get_git_secret_status
from backend.services.billing_service import get_tenant_plan, set_tenant_plan
from backend.services.tenant_service import create_tenant, list_tenants


router = APIRouter(prefix="/admin", tags=["admin"])


class TenantPlanUpdateRequest(BaseModel):
    plan_id: str = Field(min_length=1)


class LicenseIssueRequest(BaseModel):
    ttl_days: int = Field(default=365, ge=1, le=3650)


@router.post("/tenants", response_model=TenantResponse)
def create_tenant_route(
    request: TenantCreateRequest,
    principal: Principal = Depends(get_current_principal),
) -> TenantResponse:
    require_role(principal, "admin")
    if not plan_exists(request.plan_id):
        raise HTTPException(status_code=400, detail="Unknown plan")
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
    if not plan_exists(request.plan_id):
        raise HTTPException(status_code=400, detail="Unknown plan")
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


@router.get("/plans", response_model=list[PlanResponse])
def list_plans_route(
    principal: Principal = Depends(get_current_principal),
) -> list[PlanResponse]:
    require_role(principal, "admin")
    return [
        PlanResponse(
            plan_id=plan_id,
            features=sorted(data["features"]),
            analytics_engines=sorted(data["analytics_engines"]),
        )
        for plan_id, data in PLAN_CATALOG.items()
    ]


@router.get("/secrets/status")
def get_secrets_status_route(
    principal: Principal = Depends(get_current_principal),
) -> dict:
    require_role(principal, "admin")
    return get_git_secret_status()


@router.post(
    "/tenants/{tenant_id}/license",
    response_model=LicenseIssueResponse,
)
def issue_tenant_license_route(
    tenant_id: str,
    request: LicenseIssueRequest,
    principal: Principal = Depends(get_current_principal),
) -> LicenseIssueResponse:
    require_role(principal, "admin")
    plan = get_tenant_plan(tenant_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="Tenant plan not found")
    if plan["plan_id"] != "enterprise":
        raise HTTPException(
            status_code=403,
            detail="Enterprise licensing is available only to enterprise tier",
        )
    license_data = issue_enterprise_license(
        tenant_id,
        ttl_days=request.ttl_days,
    )
    return LicenseIssueResponse(**license_data)


@router.post("/license/validate")
def validate_license_route(
    request: LicenseValidationRequest,
    principal: Principal = Depends(get_current_principal),
) -> dict:
    require_role(principal, "admin")
    return validate_enterprise_license(request.token)
