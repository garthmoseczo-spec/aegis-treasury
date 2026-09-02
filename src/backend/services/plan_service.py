from __future__ import annotations

from backend.services.billing_service import get_tenant_plan


PLAN_CATALOG: dict[str, dict] = {
    "starter": {
        "features": {
            "wallets",
            "transactions",
            "standard_signing",
            "analytics_basic",
        },
        "analytics_engines": {"core"},
    },
    "growth": {
        "features": {
            "wallets",
            "transactions",
            "standard_signing",
            "analytics_basic",
            "analytics_isolated",
        },
        "analytics_engines": {"core", "fraud"},
    },
    "enterprise": {
        "features": {
            "wallets",
            "transactions",
            "standard_signing",
            "analytics_basic",
            "analytics_isolated",
            "enterprise_licensing",
            "zero_trust_tokens",
        },
        "analytics_engines": {"core", "fraud", "risk", "compliance"},
    },
}


def plan_exists(plan_id: str) -> bool:
    return plan_id in PLAN_CATALOG


def get_plan(plan_id: str) -> dict:
    return PLAN_CATALOG[plan_id]


def get_tenant_plan_id(tenant_id: str) -> str:
    mapping = get_tenant_plan(tenant_id)
    if mapping is None:
        return "starter"
    return mapping["plan_id"]


def tenant_has_feature(tenant_id: str, feature_name: str) -> bool:
    plan_id = get_tenant_plan_id(tenant_id)
    return feature_name in PLAN_CATALOG.get(plan_id, {}).get("features", set())


def allowed_analytics_engines(tenant_id: str) -> set[str]:
    plan_id = get_tenant_plan_id(tenant_id)
    return set(PLAN_CATALOG.get(plan_id, {}).get("analytics_engines", set()))
