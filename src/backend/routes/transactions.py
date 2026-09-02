from fastapi import APIRouter, Depends, HTTPException

from backend.auth import get_current_principal
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


router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.post("", response_model=TransactionResponse)
def create_transaction_route(
    request: TransactionCreateRequest,
    principal: Principal = Depends(get_current_principal),
) -> TransactionResponse:
    tenant_id = request.tenant_id or principal.tenant_id or principal.sub
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
    if transaction["tenant_id"] != tenant_id:
        raise HTTPException(
            status_code=403,
            detail="Transaction does not belong to tenant",
        )
    return TransactionResponse(**transaction)
