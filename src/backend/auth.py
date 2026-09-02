from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.config import settings
from backend.schemas import Principal


bearer_scheme = HTTPBearer(auto_error=False)


def create_access_token(
    subject: str,
    role: str,
    tenant_id: str | None = None,
) -> tuple[str, datetime]:
    now = datetime.now(timezone.utc)
    expiry = now + timedelta(minutes=settings.access_token_ttl_minutes)
    payload = {
        "iss": settings.jwt_issuer,
        "sub": subject,
        "role": role,
        "tenant_id": tenant_id,
        "iat": int(now.timestamp()),
        "exp": int(expiry.timestamp()),
    }
    token = jwt.encode(
        payload,
        settings.jwt_secret,
        algorithm=settings.jwt_algorithm,
    )
    return token, expiry


def decode_access_token(token: str) -> Principal:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
            issuer=settings.jwt_issuer,
        )
    except jwt.InvalidTokenError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from error
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
