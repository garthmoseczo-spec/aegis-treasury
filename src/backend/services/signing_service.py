from backend.crypto import (
    SIGNATURE_ALGORITHM,
    sign_payload,
    verify_payload_signature,
)


def create_signature(payload: str) -> dict:
    return {
        "signature": sign_payload(payload),
        "algorithm": SIGNATURE_ALGORITHM,
    }


def verify_signature(payload: str, signature: str) -> bool:
    return verify_payload_signature(payload, signature)
