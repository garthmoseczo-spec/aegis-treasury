import hashlib
import hmac

from backend.config import settings


SIGNATURE_ALGORITHM = "HMAC-SHA256"


def sign_payload(payload: str) -> str:
    digest = hmac.new(
        settings.jwt_secret.encode("utf-8"),
        msg=payload.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).hexdigest()
    return digest


def verify_payload_signature(payload: str, signature: str) -> bool:
    expected = sign_payload(payload)
    return hmac.compare_digest(expected, signature)

