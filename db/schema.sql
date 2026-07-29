-- Skills Evaluation server schema. Applied at every startup; must stay idempotent.
--
-- Two tables only. Evaluation payloads are stored verbatim as JSONB because the
-- scoring rules (expFor / deltaClass / band / stats) live in the apps' JS and are
-- deliberately not reimplemented server-side. See CLAUDE.md decisions 3 and 14.

CREATE TABLE IF NOT EXISTS users (
    id            SERIAL      PRIMARY KEY,
    username      TEXT        NOT NULL UNIQUE,
    password_hash TEXT        NOT NULL,
    is_active     BOOLEAN     NOT NULL DEFAULT TRUE,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Server-side sessions (CLAUDE.md decision 6). The cookie carries an opaque
-- random token and nothing else, so there is no signing secret to manage and a
-- logout or a deactivated account takes effect immediately.
CREATE TABLE IF NOT EXISTS sessions (
    token      TEXT        PRIMARY KEY,
    username   TEXT        NOT NULL REFERENCES users (username) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    expires_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS sessions_expires_idx ON sessions (expires_at);

-- Append-only: a save always inserts. Reads take the newest row per
-- (consultant, eval_date). Nothing updates or deletes rows here.
CREATE TABLE IF NOT EXISTS evaluations (
    id             BIGSERIAL   PRIMARY KEY,
    consultant     TEXT        NOT NULL,
    eval_date      DATE        NOT NULL,
    level          TEXT        NOT NULL DEFAULT '',
    schema_name    TEXT        NOT NULL,
    schema_version INTEGER     NOT NULL,
    doc            JSONB       NOT NULL,
    created_by     TEXT        NOT NULL,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Supports the DISTINCT ON (consultant, eval_date) latest-revision read.
CREATE INDEX IF NOT EXISTS evaluations_latest_idx
    ON evaluations (consultant, eval_date DESC, created_at DESC);
