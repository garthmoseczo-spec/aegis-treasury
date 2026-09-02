from threading import Lock


_plan_lock = Lock()
_tenant_plan_map: dict[str, str] = {}


def set_tenant_plan(tenant_id: str, plan_id: str) -> dict:
    with _plan_lock:
        _tenant_plan_map[tenant_id] = plan_id
        return {"tenant_id": tenant_id, "plan_id": plan_id}


def get_tenant_plan(tenant_id: str) -> dict | None:
    with _plan_lock:
        plan_id = _tenant_plan_map.get(tenant_id)
        if plan_id is None:
            return None
        return {"tenant_id": tenant_id, "plan_id": plan_id}
