ALLOWED_JWT_ALGORITHMS = {"HS256", "HS384", "HS512"}
ALLOWED_SIGNATURE_ALGORITHMS = {"HMAC-SHA256"}


def ensure_allowed_jwt_algorithm(name: str) -> str:
    if name not in ALLOWED_JWT_ALGORITHMS:
        raise ValueError(f"Unsupported JWT algorithm: {name}")
    return name


def ensure_allowed_signature_algorithm(name: str) -> str:
    if name not in ALLOWED_SIGNATURE_ALGORITHMS:
        raise ValueError(f"Unsupported signature algorithm: {name}")
    return name
