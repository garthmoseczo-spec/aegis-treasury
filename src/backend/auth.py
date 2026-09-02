from datetime import datetime, timedelta, timezone
from threading import Lock
from uuid import uuid4

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.algorithms import ensure_allowed_jwt_algorithm
from backend.config import settings
from backend.schemas import Principal


bearer_scheme = HTTPBearer(auto_error=False)
_revocation_lock = Lock()
_revoked_jti: set[str] = set()


def create_access_token(
    subject: str,
    role: str,
    tenant_id: str | None = None,
) -> tuple[str, datetime]:
    algorithm = ensure_allowed_jwt_algorithm(settings.jwt_algorithm)
    now = datetime.now(timezone.utc)
    expiry = now + timedelta(minutes=settings.access_token_ttl_minutes)
    jti = str(uuid4())
    payload = {
        "iss": settings.jwt_issuer,
        "aud": settings.token_audience,
        "sub": subject,
        "role": role,
        "tenant_id": tenant_id,
        "jti": jti,
        "iat": int(now.timestamp()),
        "nbf": int(now.timestamp()),
        "exp": int(expiry.timestamp()),
    }
    token = jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=algorithm,
    )
    return token, expiry


def decode_access_token(token: str) -> Principal:
    algorithm = ensure_allowed_jwt_algorithm(settings.jwt_algorithm)
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[algorithm],
            issuer=settings.jwt_issuer,
            audience=settings.token_audience,
            options={
                "require": ["sub", "role", "exp", "iat", "jti"],
            },
        )
    except jwt.InvalidTokenError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from error
    if is_token_revoked(payload["jti"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token revoked",
        )
    return Principal(
        sub=payload["sub"],
        role=payload["role"],
        tenant_id=payload.get("tenant_id"),
    )


def get_current_principal(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> Principal:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token",
        )
    return decode_access_token(credentials.credentials)


def require_role(principal: Principal, required_role: str) -> None:
    if principal.role != required_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )


def revoke_token_id(jti: str) -> None:
    with _revocation_lock:
        _revoked_jti.add(jti)


def is_token_revoked(jti: str) -> bool:
    with _revocation_lock:
        return jti in _revoked_jti


def decode_token_claims(token: str) -> dict:
    algorithm = ensure_allowed_jwt_algorithm(settings.jwt_algorithm)
    return jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[algorithm],
        issuer=settings.jwt_issuer,
        audience=settings.token_audience,
    )


def resolve_tenant_access(
    principal: Principal,
    requested_tenant_id: str | None,
) -> str:
    principal_tenant = principal.tenant_id or principal.sub
    if requested_tenant_id is None:
        return principal_tenant
    if principal.role == "admin":
        return requested_tenant_id
    if requested_tenant_id != principal_tenant:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cross-tenant access denied",
        )
    return requested_tenant_id
