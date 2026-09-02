from fastapi import APIRouter, Depends, HTTPException

from backend.auth import get_current_principal, resolve_tenant_access
from backend.schemas import (
    AnalyticsEventRequest,
    AnalyticsEventResponse,
    Principal,
)
from backend.services.analytics_service import (
    get_engine_events,
    get_tenant_analytics_snapshot,
    record_event,
)
from backend.services.plan_service import (
    allowed_analytics_engines,
    tenant_has_feature,
)


router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.post("/events", response_model=AnalyticsEventResponse)
def record_analytics_event_route(
    request: AnalyticsEventRequest,
    principal: Principal = Depends(get_current_principal),
) -> AnalyticsEventResponse:
    tenant_id = resolve_tenant_access(principal, request.tenant_id)
    if not tenant_has_feature(tenant_id, "analytics_basic"):
        raise HTTPException(status_code=403, detail="Analytics not enabled")
    if request.engine != "core":
        if not tenant_has_feature(tenant_id, "analytics_isolated"):
            raise HTTPException(
                status_code=403,
                detail="Isolated analytics engines not enabled",
            )
    if request.engine not in allowed_analytics_engines(tenant_id):
        raise HTTPException(
            status_code=403,
            detail="Analytics engine not allowed for tenant plan",
        )
    event = record_event(
        tenant_id=tenant_id,
        engine=request.engine,
        event_type=request.event_type,
    )
    return AnalyticsEventResponse(**event)


@router.get("/engines/{engine}")
def list_engine_events_route(
    engine: str,
    principal: Principal = Depends(get_current_principal),
) -> dict:
    tenant_id = principal.tenant_id or principal.sub
    if engine not in allowed_analytics_engines(tenant_id):
        raise HTTPException(
            status_code=403,
            detail="Analytics engine not allowed for tenant plan",
        )
    return {
        "tenant_id": tenant_id,
        "engine": engine,
        "events": get_engine_events(tenant_id, engine),
    }


@router.get("/snapshot")
def get_snapshot_route(
    principal: Principal = Depends(get_current_principal),
) -> dict:
    tenant_id = principal.tenant_id or principal.sub
    return get_tenant_analytics_snapshot(tenant_id)
