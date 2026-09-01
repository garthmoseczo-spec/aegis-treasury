from datetime import datetime, timedelta
import jwt
import os

JWT_SIGNING_KEY = os.getenv("JWT_SIGNING_KEY", "replace_this_in_production")
JWT_ALGORITHM = "HS256"  # For production, prefer RS256 with an asymmetric key


def issue_license(org_id: str, plan_id: str, ttl_days: int = 365, features: dict = None) -> str:
    now = datetime.utcnow()
    payload = {
        "iss": "resqconnect-aegis",
        "sub": org_id,
        "plan": plan_id,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(days=ttl_days)).timestamp()),
        "features": features or {}
    }
    token = jwt.encode(payload, JWT_SIGNING_KEY, algorithm=JWT_ALGORITHM)
    return token


def validate_license(token: str) -> dict:
    try:
        payload = jwt.decode(token, JWT_SIGNING_KEY, algorithms=[JWT_ALGORITHM])
        return {"valid": True, "payload": payload}
    except jwt.ExpiredSignatureError:
        return {"valid": False, "reason": "expired"}
    except jwt.InvalidTokenError:
        return {"valid": False, "reason": "invalid"}
