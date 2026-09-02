import os


REQUIRED_GIT_SECRETS = (
    "GITHUB_WEBHOOK_SECRET",
    "AEGIS_JWT_SECRET",
    "AEGIS_LICENSE_SIGNING_KEY",
)


def get_git_secret_status() -> dict:
    return {
        "required": list(REQUIRED_GIT_SECRETS),
        "configured": {
            name: bool(os.getenv(name))
            for name in REQUIRED_GIT_SECRETS
        },
    }
