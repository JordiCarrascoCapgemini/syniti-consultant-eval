"""Test fixtures.

Every test needs a real Postgres, because the queries use DISTINCT ON and JSONB
and a stub would prove nothing. Set TEST_DATABASE_URL to point at a throwaway
database; the whole suite skips if it is absent.

    docker run --rm -e POSTGRES_PASSWORD=test -p 5433:5432 -d postgres:16-alpine
    set TEST_DATABASE_URL=postgresql://postgres:test@localhost:5433/postgres
"""
import os

import pytest

TEST_DB = os.environ.get("TEST_DATABASE_URL", "").strip()

pytestmark = pytest.mark.skipif(not TEST_DB, reason="TEST_DATABASE_URL is not set")

ADMIN_USER = "test-lead"
ADMIN_PASS = "test-password-not-a-real-secret"


@pytest.fixture(scope="session", autouse=True)
def _environment():
    if not TEST_DB:
        pytest.skip("TEST_DATABASE_URL is not set", allow_module_level=True)
    os.environ["DATABASE_URL"] = TEST_DB
    os.environ["ADMIN_USERNAME"] = ADMIN_USER
    os.environ["ADMIN_PASSWORD"] = ADMIN_PASS
    os.environ.pop("COOKIE_SECURE", None)

    from server.config import get_settings

    get_settings.cache_clear()
    yield


@pytest.fixture()
def clean_db(_environment):
    """Drop and recreate the schema so each test starts empty."""
    from server import db

    with db.pool().connection() as conn:
        conn.execute("DROP TABLE IF EXISTS sessions, evaluations, users CASCADE")
    db.apply_schema()
    yield db


@pytest.fixture()
def client(clean_db):
    """TestClient with the lifespan run, so the admin account exists."""
    from starlette.testclient import TestClient

    from server.app import app

    with TestClient(app) as c:
        yield c


@pytest.fixture()
def auth_client(client):
    resp = client.post(
        "/api/auth/login", json={"username": ADMIN_USER, "password": ADMIN_PASS}
    )
    assert resp.status_code == 200, resp.text
    return client
