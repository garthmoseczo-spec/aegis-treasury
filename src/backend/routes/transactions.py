from fastapi import APIRouter, Depends, HTTPException

from backend.auth import get_current_principal, resolve_tenant_access
from backend.schemas import (
    Principal,
    TransactionCreateRequest,
    TransactionResponse,
)
from backend.services.transaction_service import (
    approve_transaction,
    create_transaction,
    list_transactions,
)
from backend.services.plan_service import tenant_has_feature


router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("", response_model=TransactionResponse)
def create_transaction_route(
    request: TransactionCreateRequest,
    principal: Principal = Depends(get_current_principal),
) -> TransactionResponse:
    tenant_id = resolve_tenant_access(principal, request.tenant_id)
    if not tenant_has_feature(tenant_id, "transactions"):
        raise HTTPException(
            status_code=403,
            detail="Plan does not allow transactions",
        )
    transaction = create_transaction(
        tenant_id=tenant_id,
        wallet_id=request.wallet_id,
        amount=request.amount,
        asset=request.asset,
    )
    return TransactionResponse(**transaction)


@router.get("", response_model=list[TransactionResponse])
def list_transactions_route(
    principal: Principal = Depends(get_current_principal),
) -> list[TransactionResponse]:
    tenant_id = principal.tenant_id or principal.sub
    if not tenant_has_feature(tenant_id, "transactions"):
        raise HTTPException(
            status_code=403,
            detail="Plan does not allow transactions",
        )
    transactions = list_transactions(tenant_id)
    return [TransactionResponse(**item) for item in transactions]


@router.post("/{transaction_id}/approve", response_model=TransactionResponse)
def approve_transaction_route(
    transaction_id: str, principal: Principal = Depends(get_current_principal)
) -> TransactionResponse:
    transaction = approve_transaction(transaction_id)
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    tenant_id = principal.tenant_id or principal.sub
    if not tenant_has_feature(tenant_id, "transactions"):
        raise HTTPException(
            status_code=403,
            detail="Plan does not allow transactions",
        )
    if transaction["tenant_id"] != tenant_id:
        raise HTTPException(
            status_code=403,
            detail="Transaction does not belong to tenant",
        )
    return TransactionResponse(**transaction)
