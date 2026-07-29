"""Save and load: round-trip fidelity, validation, and append-only semantics."""
import copy
import json
import os

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLE = os.path.join(ROOT, "test-data", "Evaluation_Amara_Okafor_2026-01-15.json")


def load_sample():
    with open(SAMPLE, encoding="utf-8") as fh:
        return json.load(fh)


def test_round_trip_is_byte_identical(auth_client):
    """A saved document must come back exactly as it went in (decision 3)."""
    doc = load_sample()
    created = auth_client.post("/api/evaluations", json=doc)
    assert created.status_code == 201, created.text

    fetched = auth_client.get(f"/api/evaluations/{created.json()['id']}")
    assert fetched.status_code == 200
    assert fetched.json() == doc


def test_save_records_the_indexed_columns(auth_client):
    row = auth_client.post("/api/evaluations", json=load_sample()).json()
    assert row["consultant"] == "Amara Okafor"
    assert row["eval_date"] == "2026-01-15"
    assert row["level"] == "C1"


def test_save_stamps_created_by(auth_client):
    from tests.conftest import ADMIN_USER

    row = auth_client.post("/api/evaluations", json=load_sample()).json()
    assert row["created_by"] == ADMIN_USER


@pytest.mark.parametrize(
    "mutate, fragment",
    [
        (lambda d: d.update(schema="something-else"), "Unrecognised schema"),
        (lambda d: d.pop("meta"), "missing its meta"),
        (lambda d: d["meta"].update(consultant=""), "consultant name"),
        (lambda d: d["meta"].update(date=""), "evaluation date"),
        (lambda d: d["meta"].update(date="14/01/2026"), "YYYY-MM-DD"),
    ],
)
def test_save_rejects_unusable_payloads(auth_client, mutate, fragment):
    doc = load_sample()
    mutate(doc)
    resp = auth_client.post("/api/evaluations", json=doc)
    assert resp.status_code == 422
    assert fragment in resp.json()["detail"]


def test_legacy_schema_is_accepted(auth_client):
    """The apps' importers accept syniti-perf-assessment, so the API must too."""
    doc = load_sample()
    doc["schema"] = "syniti-perf-assessment"
    assert auth_client.post("/api/evaluations", json=doc).status_code == 201


def test_resave_appends_and_list_returns_latest(auth_client):
    """Same consultant and date twice: both rows kept, newest one read back."""
    first = load_sample()
    second = copy.deepcopy(first)
    second["feedback"]["strengths"] = "revised wording"

    id_one = auth_client.post("/api/evaluations", json=first).json()["id"]
    id_two = auth_client.post("/api/evaluations", json=second).json()["id"]
    assert id_two != id_one

    listed = auth_client.get("/api/evaluations").json()
    assert len(listed) == 1, "latest-per-key dedupe failed"
    assert listed[0]["id"] == id_two

    docs = auth_client.get("/api/evaluations/all").json()
    assert len(docs) == 1
    assert docs[0]["feedback"]["strengths"] == "revised wording"

    # The superseded revision is still retrievable by id: append-only, not overwrite.
    assert auth_client.get(f"/api/evaluations/{id_one}").json()["feedback"]["strengths"] \
        == first["feedback"]["strengths"]


def test_distinct_dates_are_both_kept(auth_client):
    early = load_sample()
    late = copy.deepcopy(early)
    late["meta"]["date"] = "2026-05-12"

    auth_client.post("/api/evaluations", json=early)
    auth_client.post("/api/evaluations", json=late)

    listed = auth_client.get("/api/evaluations").json()
    assert [r["eval_date"] for r in listed] == ["2026-05-12", "2026-01-15"], \
        "list must be newest date first"


def test_missing_evaluation_is_404(auth_client):
    assert auth_client.get("/api/evaluations/999999").status_code == 404


def test_reference_matches_the_baked_data(auth_client):
    import refdata

    body = auth_client.get("/api/reference").json()
    assert body["competencies"] == refdata.load_competencies()
    assert body["learning"] == refdata.load_learning()
    assert len(body["competencies"]) == 78
