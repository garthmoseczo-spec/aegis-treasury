from __future__ import annotations

from dataclasses import asdict
from threading import Lock
from uuid import uuid4

from backend.models import Wallet


_wallet_lock = Lock()
_wallets: dict[str, Wallet] = {}


def create_wallet(tenant_id: str, label: str) -> dict:
    with _wallet_lock:
        wallet = Wallet(wallet_id=str(uuid4()), tenant_id=tenant_id, label=label)
        _wallets[wallet.wallet_id] = wallet
        return asdict(wallet)


def list_wallets(tenant_id: str) -> list[dict]:
    with _wallet_lock:
        return [asdict(item) for item in _wallets.values() if item.tenant_id == tenant_id]

