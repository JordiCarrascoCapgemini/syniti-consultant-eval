#!/usr/bin/env python3
"""Single clean builder for the Skills Evaluation & Enablement tools.

Source of truth:
  data/competencies.json     -> const COMPS  (short keys ref,area,t,d,e via refdata)
  data/learning-catalog.json -> const LEARNING
  build/template.html        -> eval app shell (logo embedded; 2 placeholders)
  build/template-team.html   -> team summary shell (1 placeholder: COMPS only,
                                because exports do not carry expectations)

Output:
  tool/Syniti_Skills_Evaluation_and_Enablement.html   (runnable, self-contained)
  tool/Syniti_Team_Skills_Summary.html                (runnable, self-contained)

Both apps are generated, so data/competencies.json is the only place to edit the
matrix. That is what closes LIM-5. Do not hand-edit either file in tool/.

Templates are read and written with newline="" so the output preserves the
template's own line endings byte-for-byte on every platform. Without that, the
same template produces CRLF output on Windows and LF output inside the Linux
container, and "rebuild and diff" stops being a usable check.

Run:  python3 build/build.py     (from the project root)
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import refdata

TEMPLATE      = os.path.join(ROOT, "build", "template.html")
TEMPLATE_TEAM = os.path.join(ROOT, "build", "template-team.html")
OUT           = os.path.join(ROOT, "tool", "Syniti_Skills_Evaluation_and_Enablement.html")
OUT_TEAM      = os.path.join(ROOT, "tool", "Syniti_Team_Skills_Summary.html")


def render(template_path, out_path, substitutions):
    with open(template_path, encoding="utf-8", newline="") as fh:
        html = fh.read()
    for token, value in substitutions.items():
        html = html.replace(token, value)

    left = re.findall(r"__[A-Z_]+__", html)
    if left:
        sys.exit(f"ERROR: unsubstituted placeholders remain in {out_path}: {sorted(set(left))}")
    if "\u2014" in html:  # em dash guard (standing formatting rule)
        sys.exit(f"ERROR: em dash found in {out_path}; use a hyphen")

    with open(out_path, "w", encoding="utf-8", newline="") as fh:
        fh.write(html)
    return html


def main():
    comps = refdata.load_competencies()
    learning = refdata.load_learning()
    comps_json = json.dumps(comps, ensure_ascii=False)

    html = render(TEMPLATE, OUT, {
        "__COMPS__":    comps_json,
        "__LEARNING__": json.dumps(learning, ensure_ascii=False),
    })
    team = render(TEMPLATE_TEAM, OUT_TEAM, {"__COMPS__": comps_json})

    areas = len([k for k in learning if not k.startswith("_")])
    print(f"Built {OUT}")
    print(f"  {len(comps)} competencies | {areas} learning areas | {len(html):,} bytes")
    print(f"Built {OUT_TEAM}")
    print(f"  {len(comps)} competencies | {len(team):,} bytes")


if __name__ == "__main__":
    main()
