"""Authentication behaviour: the gate, and what stays outside it."""
from tests.conftest import ADMIN_PASS, ADMIN_USER

PROTECTED = [
    ("get", "/api/reference"),
    ("get", "/api/evaluations"),
    ("get", "/api/evaluations/all"),
    ("get", "/api/evaluations/1"),
]


def test_health_needs_no_auth(client):
    """The container healthcheck depends on this staying open."""
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_protected_routes_reject_anonymous(client):
    for method, path in PROTECTED:
        resp = getattr(client, method)(path)
        assert resp.status_code == 401, f"{path} allowed an anonymous request"


def test_save_rejects_anonymous(client):
    resp = client.post("/api/evaluations", json={"schema": "syniti-skills-eval"})
    assert resp.status_code == 401


def test_login_rejects_wrong_password(client):
    resp = client.post(
        "/api/auth/login", json={"username": ADMIN_USER, "password": "wrong"}
    )
    assert resp.status_code == 401


def test_login_rejects_unknown_user(client):
    resp = client.post(
        "/api/auth/login", json={"username": "nobody", "password": ADMIN_PASS}
    )
    assert resp.status_code == 401


def test_login_then_me(auth_client):
    resp = auth_client.get("/api/auth/me")
    assert resp.status_code == 200
    assert resp.json()["username"] == ADMIN_USER


def test_session_cookie_is_httponly(client):
    resp = client.post(
        "/api/auth/login", json={"username": ADMIN_USER, "password": ADMIN_PASS}
    )
    header = resp.headers["set-cookie"].lower()
    assert "httponly" in header
    assert "samesite=strict" in header
    # COOKIE_SECURE unset in tests, so the cookie must not claim Secure.
    assert "secure" not in header


def test_logout_invalidates_the_session(auth_client):
    assert auth_client.get("/api/auth/me").status_code == 200
    assert auth_client.post("/api/auth/logout").status_code == 200
    assert auth_client.get("/api/auth/me").status_code == 401


def test_deactivated_user_loses_access(auth_client, clean_db):
    assert auth_client.get("/api/auth/me").status_code == 200
    with clean_db.pool().connection() as conn:
        conn.execute("UPDATE users SET is_active = FALSE WHERE username = %s", (ADMIN_USER,))
    assert auth_client.get("/api/auth/me").status_code == 401


def test_bootstrap_admin_is_not_recreated(clean_db):
    from server import auth

    assert auth.ensure_admin() is True
    assert auth.ensure_admin() is False
