from datetime import datetime, timedelta, timezone
import os

import jwt

from backend.algorithms import ensure_allowed_jwt_algorithm


JWT_SIGNING_KEY = os.getenv(
    "AEGIS_LICENSE_SIGNING_KEY",
    "replace_this_in_production",
)
JWT_ISSUER = os.getenv("AEGIS_LICENSE_ISSUER", "aegis-treasury")
JWT_ALGORITHM = ensure_allowed_jwt_algorithm(
    os.getenv("AEGIS_LICENSE_ALGORITHM", "HS256")
)


def issue_license(
    org_id: str,
    plan_id: str,
    ttl_days: int = 365,
    features: dict | None = None,
) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "iss": JWT_ISSUER,
        "sub": org_id,
        "plan": plan_id,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(days=ttl_days)).timestamp()),
        "features": features or {},
    }
    return jwt.encode(payload, JWT_SIGNING_KEY, algorithm=JWT_ALGORITHM)


def validate_license(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            JWT_SIGNING_KEY,
            algorithms=[JWT_ALGORITHM],
            issuer=JWT_ISSUER,
        )
    except jwt.ExpiredSignatureError:
        return {"valid": False, "reason": "expired"}
    except jwt.InvalidTokenError:
        return {"valid": False, "reason": "invalid"}
    return {"valid": True, "payload": payload}
