from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("AEGIS_APP_NAME", "Aegis Treasury Backend")
    environment: str = os.getenv("AEGIS_ENV", "development")
    jwt_issuer: str = os.getenv("AEGIS_JWT_ISSUER", "aegis-treasury")
    jwt_algorithm: str = os.getenv("AEGIS_JWT_ALGORITHM", "HS256")
    jwt_secret: str = os.getenv("AEGIS_JWT_SECRET", "replace_me_in_production")
    token_audience: str = os.getenv("AEGIS_TOKEN_AUDIENCE", "aegis-api")
    license_issuer: str = os.getenv("AEGIS_LICENSE_ISSUER", "aegis-treasury")
    license_algorithm: str = os.getenv("AEGIS_LICENSE_ALGORITHM", "HS256")
    license_signing_key: str = os.getenv(
        "AEGIS_LICENSE_SIGNING_KEY",
        "replace_me_in_production",
    )
    github_webhook_secret: str = os.getenv("GITHUB_WEBHOOK_SECRET", "")
    access_token_ttl_minutes: int = int(
        os.getenv("AEGIS_ACCESS_TOKEN_TTL_MINUTES", "60")
    )
    database_url: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./aegis_treasury.db",
    )


settings = Settings()
