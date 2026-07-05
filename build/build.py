#!/usr/bin/env python3
"""
Single clean builder for the Skills Evaluation & Enablement tool.

Source of truth:
  data/competencies.json     -> const COMPS  (converted to short keys ref,area,t,d,e)
  data/learning-catalog.json -> const LEARNING
  build/template.html        -> HTML/CSS/JS shell (logo already embedded; 2 placeholders)

Output:
  tool/Syniti_Skills_Evaluation_and_Enablement.html   (runnable, self-contained)

Run:  python3 build/build.py     (from the project root)
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMPS_SRC = os.path.join(ROOT, "data", "competencies.json")
LEARN_SRC = os.path.join(ROOT, "data", "learning-catalog.json")
TEMPLATE  = os.path.join(ROOT, "build", "template.html")
OUT       = os.path.join(ROOT, "tool", "Syniti_Skills_Evaluation_and_Enablement.html")


def load_comps():
    data = json.load(open(COMPS_SRC))
    out = []
    for c in data:
        out.append({
            "ref":  c["ref"],
            "area": c["area"].strip(),
            "t":    c["title"].strip(),
            "d":    c["desc"].strip(),
            "e":    c["exp"],
        })
    return out


def main():
    comps = load_comps()
    learning = json.load(open(LEARN_SRC))
    template = open(TEMPLATE).read()

    html = (template
            .replace("__COMPS__",    json.dumps(comps, ensure_ascii=False))
            .replace("__LEARNING__", json.dumps(learning, ensure_ascii=False)))

    left = re.findall(r"__[A-Z_]+__", html)
    if left:
        sys.exit(f"ERROR: unsubstituted placeholders remain: {sorted(set(left))}")
    if "—" in html:  # em dash guard (standing formatting rule)
        sys.exit("ERROR: em dash found in output; use a hyphen")

    open(OUT, "w").write(html)
    print(f"Built {OUT}")
    print(f"  {len(comps)} competencies | {len([k for k in learning if not k.startswith('_')])} learning areas | {len(html):,} bytes")


if __name__ == "__main__":
    main()
