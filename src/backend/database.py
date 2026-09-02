from __future__ import annotations

import sqlite3
from urllib.parse import urlparse

from backend.config import settings


def _sqlite_path_from_url(database_url: str) -> str:
    if database_url.startswith("sqlite:///"):
        return database_url.replace("sqlite:///", "", 1)
    parsed = urlparse(database_url)
    if parsed.scheme == "sqlite":
        return parsed.path.lstrip("/")
    raise ValueError("Only sqlite URLs are supported by the default backend core")


def get_sqlite_connection() -> sqlite3.Connection:
    path = _sqlite_path_from_url(settings.database_url)
    connection = sqlite3.connect(path, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    return connection

