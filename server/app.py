"""FastAPI app for the Skills Evaluation tool.

Serves the two existing single-file apps unchanged and adds the optional
save/load API they feature-detect. All scoring stays in the apps' JS; this
server stores and returns documents verbatim (CLAUDE.md decision 3).
"""
import datetime as dt
import os
from contextlib import asynccontextmanager

from fastapi import Cookie, Depends, FastAPI, HTTPException, Response, status
from fastapi.responses import FileResponse
from pydantic import BaseModel

import refdata

from . import auth, db

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVAL_APP = os.path.join(ROOT, "tool", "Syniti_Skills_Evaluation_and_Enablement.html")
TEAM_APP = os.path.join(ROOT, "tool", "Syniti_Team_Skills_Summary.html")

# Matches validateDoc() in the team app and the eval app's import handler.
ALLOWED_SCHEMAS = ("syniti-skills-eval", "syniti-perf-assessment")


@asynccontextmanager
async def lifespan(_app):
    db.apply_schema()
    if auth.ensure_admin():
        print("Created bootstrap admin account.")
    yield
    db.close_pool()


app = FastAPI(title="Syniti Skills Evaluation", lifespan=lifespan)


# Declared before anything else so it can never end up behind auth. The
# container healthcheck depends on this staying unauthenticated.
@app.get("/api/health")
def health():
    return {"status": "ok"}


class LoginBody(BaseModel):
    username: str
    password: str


@app.post("/api/auth/login")
def api_login(body: LoginBody, response: Response):
    username = auth.login(response, body.username, body.password)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )
    return {"username": username}


@app.post("/api/auth/logout")
def api_logout(response: Response, syniti_session: str = Cookie(default=None)):
    auth.logout(response, syniti_session)
    return {"status": "signed out"}


@app.get("/api/auth/me")
def api_me(username: str = Depends(auth.current_user)):
    return {"username": username}


@app.get("/api/reference")
def api_reference(_username: str = Depends(auth.current_user)):
    """The same data build.py bakes in, so a served app needs no embedded copy."""
    return {
        "competencies": refdata.load_competencies(),
        "learning": refdata.load_learning(),
    }


def _extract_keys(doc):
    """Pull the indexed columns out of a payload, or explain why it is unusable."""
    if not isinstance(doc, dict):
        raise HTTPException(422, "Body must be an evaluation document object.")
    if doc.get("schema") not in ALLOWED_SCHEMAS:
        raise HTTPException(
            422, f"Unrecognised schema. Expected one of {', '.join(ALLOWED_SCHEMAS)}."
        )
    meta = doc.get("meta")
    if not isinstance(meta, dict):
        raise HTTPException(422, "Document is missing its meta block.")

    consultant = (meta.get("consultant") or "").strip()
    raw_date = (meta.get("date") or "").strip()
    if not consultant:
        raise HTTPException(422, "Cannot save without a consultant name.")
    if not raw_date:
        raise HTTPException(422, "Cannot save without an evaluation date.")
    try:
        eval_date = dt.date.fromisoformat(raw_date)
    except ValueError:
        raise HTTPException(422, f"Evaluation date '{raw_date}' is not YYYY-MM-DD.")

    version = doc.get("version")
    return {
        "consultant": consultant,
        "eval_date": eval_date,
        "level": (meta.get("level") or "").strip(),
        "schema_name": doc["schema"],
        "schema_version": version if isinstance(version, int) else 0,
    }


@app.post("/api/evaluations", status_code=status.HTTP_201_CREATED)
def api_save_evaluation(doc: dict, username: str = Depends(auth.current_user)):
    keys = _extract_keys(doc)
    return db.insert_evaluation(created_by=username, doc=doc, **keys)


@app.get("/api/evaluations")
def api_list_evaluations(_username: str = Depends(auth.current_user)):
    """Newest revision per consultant and date, newest date first."""
    return db.list_evaluations()


@app.get("/api/evaluations/all")
def api_all_evaluations(_username: str = Depends(auth.current_user)):
    """Full documents for the team app, deduped to the newest revision."""
    return db.all_evaluation_docs()


@app.get("/api/evaluations/{evaluation_id}")
def api_get_evaluation(evaluation_id: int, _username: str = Depends(auth.current_user)):
    doc = db.get_evaluation_doc(evaluation_id)
    if doc is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No such evaluation.")
    return doc


# The two apps are self-contained single files (logo is base64-embedded), so
# there are no other static assets to mount.
@app.get("/")
def serve_eval_app():
    return FileResponse(EVAL_APP, media_type="text/html")


@app.get("/team")
def serve_team_app():
    return FileResponse(TEAM_APP, media_type="text/html")
