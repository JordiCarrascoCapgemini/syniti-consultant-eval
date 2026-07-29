"""Password hashing, server-side sessions, and the current-user dependency.

Visibility model is a shared pool (CLAUDE.md decision 2): every authenticated
lead may read and write every evaluation. There is no per-row ownership check,
only an authentication check. created_by is recorded for audit, not for access
control.
"""
import secrets

from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError
from fastapi import Cookie, HTTPException, Response, status

from . import db
from .config import get_settings

COOKIE_NAME = "syniti_session"
_hasher = PasswordHasher()


def hash_password(plain):
    return _hasher.hash(plain)


def verify_password(plain, hashed):
    try:
        return _hasher.verify(hashed, plain)
    except (VerifyMismatchError, VerificationError):
        return False


def ensure_admin():
    """Create the bootstrap admin if absent. Never overwrites an existing one."""
    settings = get_settings()
    return db.create_user_if_absent(
        settings.admin_username, hash_password(settings.admin_password)
    )


def login(response, username, password):
    user = db.get_user(username)
    # Verify even when the user is missing would be better for timing, but a
    # fixed dummy hash adds more surface than it removes here; the endpoint
    # returns an identical error either way.
    if user is None or not user["is_active"]:
        return None
    if not verify_password(password, user["password_hash"]):
        return None

    settings = get_settings()
    token = secrets.token_urlsafe(32)
    db.create_session(token, username, settings.session_max_age)
    response.set_cookie(
        COOKIE_NAME,
        token,
        max_age=settings.session_max_age,
        httponly=True,
        samesite="strict",
        secure=settings.cookie_secure,
        path="/",
    )
    return username


def logout(response, token):
    if token:
        db.delete_session(token)
    response.delete_cookie(COOKIE_NAME, path="/")


def current_user(syniti_session: str = Cookie(default=None)):
    """FastAPI dependency. 401 unless the cookie maps to a live session."""
    username = db.get_session_user(syniti_session) if syniti_session else None
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required"
        )
    return username
