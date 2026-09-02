from fastapi import APIRouter, Depends

from backend.auth import get_current_principal
from backend.schemas import Principal, WalletCreateRequest, WalletResponse
from backend.services.wallet_service import create_wallet, list_wallets


router = APIRouter(prefix="/wallets", tags=["wallets"])


@router.post("", response_model=WalletResponse)
def create_wallet_route(
    request: WalletCreateRequest,
    principal: Principal = Depends(get_current_principal),
) -> WalletResponse:
    tenant_id = request.tenant_id or principal.tenant_id or principal.sub
    wallet = create_wallet(tenant_id=tenant_id, label=request.label)
    return WalletResponse(**wallet)


@router.get("", response_model=list[WalletResponse])
def list_wallets_route(
    principal: Principal = Depends(get_current_principal),
) -> list[WalletResponse]:
    tenant_id = principal.tenant_id or principal.sub
    wallets = list_wallets(tenant_id=tenant_id)
    return [WalletResponse(**wallet) for wallet in wallets]
