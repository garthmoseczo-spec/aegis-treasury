from __future__ import annotations

from dataclasses import asdict
from threading import Lock
from uuid import uuid4

from backend.models import Tenant


_tenant_lock = Lock()
_tenants: dict[str, Tenant] = {}


def create_tenant(name: str, plan_id: str) -> dict:
    with _tenant_lock:
        tenant = Tenant(tenant_id=str(uuid4()), name=name, plan_id=plan_id)
        _tenants[tenant.tenant_id] = tenant
        return asdict(tenant)


def list_tenants() -> list[dict]:
    with _tenant_lock:
        return [asdict(item) for item in _tenants.values()]
