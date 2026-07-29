"""Postgres access: one connection pool, plus the queries the API needs.

Sync psycopg3 on purpose. FastAPI runs sync endpoints in a threadpool, which is
ample for a handful of leads and avoids an async layer nobody needs here.
"""
import os

from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from .config import get_settings

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA_PATH = os.path.join(ROOT, "db", "schema.sql")

_pool = None


def pool():
    global _pool
    if _pool is None:
        _pool = ConnectionPool(
            get_settings().database_url,
            min_size=1,
            max_size=8,
            kwargs={"row_factory": dict_row},
            open=True,
        )
    return _pool


def close_pool():
    global _pool
    if _pool is not None:
        _pool.close()
        _pool = None


def apply_schema():
    with open(SCHEMA_PATH, encoding="utf-8") as fh:
        ddl = fh.read()
    with pool().connection() as conn:
        conn.execute(ddl)


# -- users ----------------------------------------------------------------

def get_user(username):
    with pool().connection() as conn:
        return conn.execute(
            "SELECT username, password_hash, is_active FROM users WHERE username = %s",
            (username,),
        ).fetchone()


def create_user_if_absent(username, password_hash):
    """Insert an account only when it does not exist. Never overwrites a password."""
    with pool().connection() as conn:
        row = conn.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s) "
            "ON CONFLICT (username) DO NOTHING RETURNING username",
            (username, password_hash),
        ).fetchone()
    return row is not None


# -- sessions -------------------------------------------------------------

def create_session(token, username, max_age_seconds):
    with pool().connection() as conn:
        conn.execute("DELETE FROM sessions WHERE expires_at < now()")
        conn.execute(
            "INSERT INTO sessions (token, username, expires_at) "
            "VALUES (%s, %s, now() + make_interval(secs => %s))",
            (token, username, max_age_seconds),
        )


def get_session_user(token):
    """Return the active username for a live session token, else None."""
    with pool().connection() as conn:
        row = conn.execute(
            "SELECT s.username FROM sessions s "
            "JOIN users u ON u.username = s.username "
            "WHERE s.token = %s AND s.expires_at > now() AND u.is_active",
            (token,),
        ).fetchone()
    return row["username"] if row else None


def delete_session(token):
    with pool().connection() as conn:
        conn.execute("DELETE FROM sessions WHERE token = %s", (token,))


# -- evaluations ---------------------------------------------------------

# Newest revision per (consultant, eval_date). The inner ORDER BY is what
# DISTINCT ON selects on; the outer one is the picker's display order.
_LATEST = """
SELECT {cols} FROM (
    SELECT DISTINCT ON (consultant, eval_date)
           id, consultant, eval_date, level, created_by, created_at{doc}
    FROM evaluations
    ORDER BY consultant, eval_date DESC, created_at DESC
) latest
ORDER BY eval_date DESC, consultant
"""


def insert_evaluation(consultant, eval_date, level, schema_name, schema_version, doc, created_by):
    from psycopg.types.json import Jsonb

    with pool().connection() as conn:
        return conn.execute(
            "INSERT INTO evaluations "
            "(consultant, eval_date, level, schema_name, schema_version, doc, created_by) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s) "
            "RETURNING id, consultant, eval_date, level, created_by, created_at",
            (consultant, eval_date, level, schema_name, schema_version, Jsonb(doc), created_by),
        ).fetchone()


def list_evaluations():
    sql = _LATEST.format(
        cols="id, consultant, eval_date, level, created_by, created_at", doc=""
    )
    with pool().connection() as conn:
        return conn.execute(sql).fetchall()


def all_evaluation_docs():
    sql = _LATEST.format(cols="doc", doc=", doc")
    with pool().connection() as conn:
        return [r["doc"] for r in conn.execute(sql).fetchall()]


def get_evaluation_doc(evaluation_id):
    with pool().connection() as conn:
        row = conn.execute(
            "SELECT doc FROM evaluations WHERE id = %s", (evaluation_id,)
        ).fetchone()
    return row["doc"] if row else None
