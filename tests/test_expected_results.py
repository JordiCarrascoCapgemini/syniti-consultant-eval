"""End-to-end check that the server path agrees with the file path.

Seeds all 34 synthetic evaluations, reads them back through the API, and asserts
the figures recorded in test-data/EXPECTED_RESULTS.md.

Scope note: every assertion here reads the `summary` and `feedback` blocks that
the apps' own JS already computed and stored. This test deliberately does not
recompute any score, delta, band or expectation, because reimplementing the
scoring rules in Python would create the fourth copy of that logic that LIM-5
and CLAUDE.md decision 3 exist to prevent. What it proves is the pipeline:
seeding, JSONB round-trip fidelity, latest-revision dedupe, and that documents
come back through HTTP exactly as the tool wrote them.

The one documented figure not asserted is the pooled "at or above expectation"
percentage of 70%. It is pooled across individual ratings rather than averaged
per consultant (the per-consultant mean is 68.0), so deriving it requires the
expected-value lookup, which is scoring logic.
"""
import os

from server import seed

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_DATA = os.path.join(ROOT, "test-data")

TOTAL_FILES = 34
TOTAL_CONSULTANTS = 20
TOTAL_GAPS = 46
EXPECTED_BANDS = {"below": 4, "exceeds": 3, "meets": 9, "partial": 4}


def latest_per_consultant(docs):
    """What the team app does client-side: one document per consultant."""
    newest = {}
    for doc in docs:
        name = doc["meta"]["consultant"]
        if name not in newest or doc["meta"]["date"] > newest[name]["meta"]["date"]:
            newest[name] = doc
    return list(newest.values())


def test_seed_loads_every_file(auth_client):
    assert seed.seed(TEST_DATA) == TOTAL_FILES

    listed = auth_client.get("/api/evaluations").json()
    # All 34 are distinct (consultant, date) pairs, so none are deduped away.
    assert len(listed) == TOTAL_FILES
    assert len({row["consultant"] for row in listed}) == TOTAL_CONSULTANTS


def test_expected_team_kpis(auth_client):
    seed.seed(TEST_DATA)
    docs = auth_client.get("/api/evaluations/all").json()
    assert len(docs) == TOTAL_FILES

    current = latest_per_consultant(docs)
    assert len(current) == TOTAL_CONSULTANTS

    scores = [d["summary"]["avgScore"] for d in current]
    deltas = [d["summary"]["avgD"] for d in current]

    # EXPECTED_RESULTS.md: team average competency score 3.01
    assert round(sum(scores) / len(scores), 2) == 3.01
    # EXPECTED_RESULTS.md: team average delta to level -0.18
    assert round(sum(deltas) / len(deltas), 2) == -0.18
    # EXPECTED_RESULTS.md: total material gaps 46
    assert sum(d["summary"]["gaps"] for d in current) == TOTAL_GAPS


def test_expected_band_distribution(auth_client):
    seed.seed(TEST_DATA)
    docs = auth_client.get("/api/evaluations/all").json()

    counts = {}
    for doc in latest_per_consultant(docs):
        band = doc["feedback"]["classification"]
        counts[band] = counts.get(band, 0) + 1

    # EXPECTED_RESULTS.md: 4 below, 3 exceeds, 9 meets, 4 partially meets.
    assert counts == EXPECTED_BANDS


def test_seeded_documents_survive_the_round_trip(auth_client):
    """Spot-check one document against the file it came from, field for field."""
    import json

    seed.seed(TEST_DATA)
    path = os.path.join(TEST_DATA, "Evaluation_Ingrid_Larsen_2026-07-01.json")
    with open(path, encoding="utf-8") as fh:
        original = json.load(fh)

    docs = auth_client.get("/api/evaluations/all").json()
    stored = [
        d
        for d in docs
        if d["meta"]["consultant"] == "Ingrid Larsen"
        and d["meta"]["date"] == "2026-07-01"
    ]
    assert len(stored) == 1
    assert stored[0] == original
