from dataclasses import dataclass, field
from datetime import datetime, timezone


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class Tenant:
    tenant_id: str
    name: str
    plan_id: str
    created_at: datetime = field(default_factory=utc_now)


@dataclass
class Wallet:
    wallet_id: str
    tenant_id: str
    label: str
    created_at: datetime = field(default_factory=utc_now)


@dataclass
class Transaction:
    transaction_id: str
    tenant_id: str
    wallet_id: str
    amount: float
    asset: str
    status: str = "pending"
    created_at: datetime = field(default_factory=utc_now)
    approved_at: datetime | None = None
