"""Environment configuration.

Mandatory values have no defaults and raise on first access, so a misconfigured
container fails at startup with a readable message instead of serving a
half-working app. See .env.example.
"""
import os
from dataclasses import dataclass
from functools import lru_cache

_MISSING = (
    "{name} is not set. Copy .env.example to .env and fill it in "
    "(docker compose reads .env automatically)."
)


def _required(name):
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(_MISSING.format(name=name))
    return value


@dataclass(frozen=True)
class Settings:
    database_url: str
    admin_username: str
    admin_password: str
    # Exact string "true", case-sensitive. Any other value leaves the session
    # cookie non-Secure, which is correct for plain-HTTP local development and
    # wrong for anything holding real evaluations.
    cookie_secure: bool
    session_max_age: int


@lru_cache(maxsize=1)
def get_settings():
    return Settings(
        database_url=_required("DATABASE_URL"),
        admin_username=os.environ.get("ADMIN_USERNAME", "").strip() or "admin",
        admin_password=_required("ADMIN_PASSWORD"),
        cookie_secure=os.environ.get("COOKIE_SECURE", "") == "true",
        session_max_age=int(os.environ.get("SESSION_MAX_AGE", "43200")),
    )
