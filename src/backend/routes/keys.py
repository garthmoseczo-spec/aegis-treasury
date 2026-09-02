from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from backend.auth import get_current_principal
from backend.schemas import Principal, SignatureRequest, SignatureResponse
from backend.services.plan_service import tenant_has_feature
from backend.services.signing_service import create_signature, verify_signature


router = APIRouter(prefix="/keys", tags=["keys"])


class SignatureVerifyRequest(BaseModel):
    payload: str = Field(min_length=1)
    signature: str = Field(min_length=1)


@router.post("/sign", response_model=SignatureResponse)
def sign_route(
    request: SignatureRequest,
    principal: Principal = Depends(get_current_principal),
) -> SignatureResponse:
    tenant_id = principal.tenant_id or principal.sub
    if not tenant_has_feature(tenant_id, "standard_signing"):
        raise HTTPException(
            status_code=403,
            detail="Plan does not allow signing",
        )
    result = create_signature(request.payload)
    return SignatureResponse(**result)


@router.post("/verify")
def verify_route(
    request: SignatureVerifyRequest,
    principal: Principal = Depends(get_current_principal),
) -> dict:
    tenant_id = principal.tenant_id or principal.sub
    if not tenant_has_feature(tenant_id, "standard_signing"):
        raise HTTPException(
            status_code=403,
            detail="Plan does not allow signing",
        )
    is_valid = verify_signature(request.payload, request.signature)
    return {"valid": is_valid}
