from datetime import datetime, timedelta, timezone

import jwt

from backend.algorithms import ensure_allowed_jwt_algorithm
from backend.config import settings
from backend.services.plan_service import PLAN_CATALOG, get_tenant_plan_id


def issue_enterprise_license(tenant_id: str, ttl_days: int = 365) -> dict:
    algorithm = ensure_allowed_jwt_algorithm(settings.license_algorithm)
    now = datetime.now(timezone.utc)
    exp = now + timedelta(days=ttl_days)
    plan_id = get_tenant_plan_id(tenant_id)
    claims = {
        "iss": settings.license_issuer,
        "sub": tenant_id,
        "tier": plan_id,
        "entitlements": sorted(PLAN_CATALOG[plan_id]["features"]),
        "iat": int(now.timestamp()),
        "exp": int(exp.timestamp()),
    }
    token = jwt.encode(
        claims,
        settings.license_signing_key,
        algorithm=algorithm,
    )
    return {"license_token": token, "expires_at": exp, "tier": plan_id}


def validate_enterprise_license(token: str) -> dict:
    algorithm = ensure_allowed_jwt_algorithm(settings.license_algorithm)
    try:
        claims = jwt.decode(
            token,
            settings.license_signing_key,
            algorithms=[algorithm],
            issuer=settings.license_issuer,
        )
    except jwt.ExpiredSignatureError:
        return {"valid": False, "reason": "expired"}
    except jwt.InvalidTokenError:
        return {"valid": False, "reason": "invalid"}
    return {"valid": True, "claims": claims}
