from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from threading import Lock
from uuid import uuid4

from backend.models import Transaction


_transaction_lock = Lock()
_transactions: dict[str, Transaction] = {}


def create_transaction(
    tenant_id: str,
    wallet_id: str,
    amount: float,
    asset: str,
) -> dict:
    with _transaction_lock:
        transaction = Transaction(
            transaction_id=str(uuid4()),
            tenant_id=tenant_id,
            wallet_id=wallet_id,
            amount=amount,
            asset=asset,
        )
        _transactions[transaction.transaction_id] = transaction
        return asdict(transaction)


def list_transactions(tenant_id: str) -> list[dict]:
    with _transaction_lock:
        return [
            asdict(item)
            for item in _transactions.values()
            if item.tenant_id == tenant_id
        ]


def approve_transaction(transaction_id: str) -> dict | None:
    with _transaction_lock:
        transaction = _transactions.get(transaction_id)
        if transaction is None:
            return None
        transaction.status = "approved"
        transaction.approved_at = datetime.now(timezone.utc)
        return asdict(transaction)
