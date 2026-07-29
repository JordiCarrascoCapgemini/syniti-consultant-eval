"""Load test-data/*.json into Postgres.

Explicit command only. This is never wired into startup: test-data holds 34
synthetic named consultants, and auto-seeding would put them into whatever
database happens to boot empty, including a real one.

Usage (from the repo root, with DATABASE_URL set):
    python -m server.seed
    python -m server.seed --dir test-data
"""
import argparse
import glob
import json
import os
import sys

from . import db
from .app import _extract_keys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEED_USER = "seed"


def seed(directory):
    pattern = os.path.join(directory, "Evaluation_*.json")
    paths = sorted(glob.glob(pattern))
    if not paths:
        print(f"No files matched {pattern}")
        return 0

    db.apply_schema()
    loaded = 0
    for path in paths:
        with open(path, encoding="utf-8") as fh:
            doc = json.load(fh)
        try:
            keys = _extract_keys(doc)
        except Exception as exc:  # HTTPException carries .detail
            print(f"  skipped {os.path.basename(path)}: {getattr(exc, 'detail', exc)}")
            continue
        db.insert_evaluation(created_by=SEED_USER, doc=doc, **keys)
        loaded += 1

    print(f"Seeded {loaded} of {len(paths)} evaluations from {directory}")
    return loaded


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dir",
        default=os.path.join(ROOT, "test-data"),
        help="directory of Evaluation_*.json files (default: test-data/)",
    )
    args = parser.parse_args()
    seed(args.dir)
    db.close_pool()
    return 0


if __name__ == "__main__":
    sys.exit(main())
