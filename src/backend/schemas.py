from datetime import datetime
from pydantic import BaseModel, Field


class TokenRequest(BaseModel):
    subject: str = Field(min_length=1)
    role: str = Field(default="user", min_length=1)
    tenant_id: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime


class Principal(BaseModel):
    sub: str
    role: str
    tenant_id: str | None = None


class TenantCreateRequest(BaseModel):
    name: str = Field(min_length=1)
    plan_id: str = Field(min_length=1)


class TenantResponse(BaseModel):
    tenant_id: str
    name: str
    plan_id: str
    created_at: datetime


class WalletCreateRequest(BaseModel):
    label: str = Field(min_length=1)
    tenant_id: str | None = None


class WalletResponse(BaseModel):
    wallet_id: str
    tenant_id: str
    label: str
    created_at: datetime


class TransactionCreateRequest(BaseModel):
    wallet_id: str = Field(min_length=1)
    amount: float
    asset: str = Field(min_length=1)
    tenant_id: str | None = None


class TransactionResponse(BaseModel):
    transaction_id: str
    tenant_id: str
    wallet_id: str
    amount: float
    asset: str
    status: str
    created_at: datetime
    approved_at: datetime | None = None


class SignatureRequest(BaseModel):
    payload: str = Field(min_length=1)


class SignatureResponse(BaseModel):
    signature: str
    algorithm: str


class TokenIntrospectionResponse(BaseModel):
    active: bool
    subject: str | None = None
    role: str | None = None
    tenant_id: str | None = None
    jti: str | None = None


class PlanResponse(BaseModel):
    plan_id: str
    features: list[str]
    analytics_engines: list[str]


class LicenseIssueResponse(BaseModel):
    license_token: str
    expires_at: datetime
    tier: str


class LicenseValidationRequest(BaseModel):
    token: str = Field(min_length=1)


class AnalyticsEventRequest(BaseModel):
    engine: str = Field(min_length=1)
    event_type: str = Field(min_length=1)
    tenant_id: str | None = None


class AnalyticsEventResponse(BaseModel):
    event_id: str
    tenant_id: str
    engine: str
    event_type: str
    created_at: datetime
