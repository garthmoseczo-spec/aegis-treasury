from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials

from backend.auth import (
    bearer_scheme,
    create_access_token,
    decode_token_claims,
    is_token_revoked,
    revoke_token_id,
)
from backend.schemas import (
    TokenIntrospectionResponse,
    TokenRequest,
    TokenResponse,
)


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=TokenResponse)
def issue_token(request: TokenRequest) -> TokenResponse:
    token, expires_at = create_access_token(
        subject=request.subject,
        role=request.role,
        tenant_id=request.tenant_id,
    )
    return TokenResponse(access_token=token, expires_at=expires_at)


@router.post("/revoke")
def revoke_own_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> dict:
    if credentials is None:
        return {"revoked": False, "reason": "missing_token"}
    claims = decode_token_claims(credentials.credentials)
    revoke_token_id(claims["jti"])
    return {"revoked": True, "jti": claims["jti"]}


@router.post("/introspect", response_model=TokenIntrospectionResponse)
def introspect_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> TokenIntrospectionResponse:
    if credentials is None:
        return TokenIntrospectionResponse(active=False)
    try:
        claims = decode_token_claims(credentials.credentials)
    except Exception:
        return TokenIntrospectionResponse(active=False)
    revoked = is_token_revoked(claims["jti"])
    if revoked:
        return TokenIntrospectionResponse(active=False, jti=claims["jti"])
    return TokenIntrospectionResponse(
        active=True,
        subject=claims["sub"],
        role=claims["role"],
        tenant_id=claims.get("tenant_id"),
        jti=claims["jti"],
    )
