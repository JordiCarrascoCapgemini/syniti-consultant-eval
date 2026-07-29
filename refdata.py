"""Shared loaders for the reference data in data/.

Both build/build.py (which bakes the data into the HTML) and the server's
/api/reference endpoint read through here, so the short-key conversion exists
in exactly one place. See LIM-5 in issues.md for why that matters.
"""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
COMPS_SRC = os.path.join(ROOT, "data", "competencies.json")
LEARN_SRC = os.path.join(ROOT, "data", "learning-catalog.json")


def load_competencies():
    """data/competencies.json -> the short-key shape the apps embed as COMPS."""
    with open(COMPS_SRC, encoding="utf-8") as fh:
        data = json.load(fh)
    return [
        {
            "ref": c["ref"],
            "area": c["area"].strip(),
            "t": c["title"].strip(),
            "d": c["desc"].strip(),
            "e": c["exp"],
        }
        for c in data
    ]


def load_learning():
    """data/learning-catalog.json verbatim, keyed by competency area string."""
    with open(LEARN_SRC, encoding="utf-8") as fh:
        return json.load(fh)
