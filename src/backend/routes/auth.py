from fastapi import APIRouter

from backend.auth import create_access_token
from backend.schemas import TokenRequest, TokenResponse


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=TokenResponse)
def issue_token(request: TokenRequest) -> TokenResponse:
    token, expires_at = create_access_token(
        subject=request.subject,
        role=request.role,
        tenant_id=request.tenant_id,
    )
    return TokenResponse(access_token=token, expires_at=expires_at)
