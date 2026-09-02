from fastapi import APIRouter, Depends, HTTPException

from backend.auth import get_current_principal, resolve_tenant_access
from backend.schemas import Principal, WalletCreateRequest, WalletResponse
from backend.services.plan_service import tenant_has_feature
from backend.services.wallet_service import create_wallet, list_wallets


router = APIRouter(prefix="/wallets", tags=["wallets"])


@router.post("", response_model=WalletResponse)
def create_wallet_route(
    request: WalletCreateRequest,
    principal: Principal = Depends(get_current_principal),
) -> WalletResponse:
    tenant_id = resolve_tenant_access(principal, request.tenant_id)
    if not tenant_has_feature(tenant_id, "wallets"):
        raise HTTPException(
            status_code=403,
            detail="Plan does not allow wallets",
        )
    wallet = create_wallet(tenant_id=tenant_id, label=request.label)
    return WalletResponse(**wallet)


@router.get("", response_model=list[WalletResponse])
def list_wallets_route(
    principal: Principal = Depends(get_current_principal),
) -> list[WalletResponse]:
    tenant_id = principal.tenant_id or principal.sub
    if not tenant_has_feature(tenant_id, "wallets"):
        raise HTTPException(
            status_code=403,
            detail="Plan does not allow wallets",
        )
    wallets = list_wallets(tenant_id=tenant_id)
    return [WalletResponse(**wallet) for wallet in wallets]
