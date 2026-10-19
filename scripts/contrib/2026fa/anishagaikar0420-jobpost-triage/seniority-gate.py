#!/usr/bin/env python3
"""seniority-gate.py — gate G4b: does the posting's own text ask for more experience than a junior has?

Closes recipe TODO 5. Pure regex over posting text: no network, no LLM.
It finds statements of required experience ("36 months of experience", "3+ years",
"2-4 years", "three years") and converts the LARGEST minimum found to months.

  pass  : at least one experience requirement found and the largest minimum <= --max-months
  flag  : largest minimum > --max-months  (a named human must read the quotes; likely not entry level)
  none  : no experience requirement found. NOT a pass: absence of a number is not evidence of
          an entry-level role. Reported as 'no-requirement-found', human reads the posting.

Cannot catch: seniority written without a number ("seasoned", "proven track record"), experience
numbers in the company boilerplate ("20 years of innovation") that match the pattern, or a
requirement the posting words in a way the pattern misses. Every match is printed with its quote.

Usage: seniority-gate.py <posting.txt> [--max-months 24] [--json out.json]
Exit: 0 pass · 1 flag or none (human must read) · 2 bad input.
"""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

MAX_MONTHS_DEFAULT = 24  # [DEFINE] two years is the usual ceiling for "entry level / junior"; an authorial choice, not a statistic.
WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}
NUM = r"(\d{1,2}|" + "|".join(WORDS) + r")"
PAT = re.compile(
    NUM + r"(?:\s*(?:\+|-|–|to)\s*" + NUM + r")?\s*\+?\s*(years?|yrs?|months?)\b[^.\n]{0,60}?\bexperience",
    re.I,
)


def to_int(tok: str) -> int:
    t = tok.lower()
    return WORDS[t] if t in WORDS else int(t)


def find_requirements(text: str) -> list[dict]:
    text = re.sub(r"\s+", " ", text.replace("’", "'"))
    out = []
    for m in PAT.finditer(text):
        lo = to_int(m.group(1))  # the MINIMUM stated is what gates entry
        unit = m.group(3).lower()
        months = lo * (1 if unit.startswith("month") else 12)
        a, b = max(0, m.start() - 60), min(len(text), m.end() + 40)
        out.append({"min_months": months, "match": m.group(0), "context": text[a:b]})
    return out


def run(text: str, max_months: int) -> dict:
    reqs = find_requirements(text)
    if not reqs:
        return {"schema": "seniority-gate/1", "status": "none", "reason": "no-requirement-found",
                "max_months_allowed": max_months, "requirements": []}
    top = max(r["min_months"] for r in reqs)
    return {"schema": "seniority-gate/1", "status": "pass" if top <= max_months else "flag",
            "largest_min_months": top, "max_months_allowed": max_months, "requirements": reqs}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("posting")
    ap.add_argument("--max-months", type=int, default=MAX_MONTHS_DEFAULT)
    ap.add_argument("--json")
    a = ap.parse_args(argv)
    p = Path(a.posting)
    if not p.is_file() or not p.read_text(errors="ignore").strip():
        print(f"seniority-gate: cannot read posting text at {a.posting}", file=sys.stderr)
        return 2
    res = run(p.read_text(errors="ignore"), a.max_months)
    if a.json:
        Path(a.json).write_text(json.dumps(res, indent=2))
    print(f"seniority-gate: status={res['status']}"
          + (f" largest_min={res['largest_min_months']}mo allowed={a.max_months}mo" if "largest_min_months" in res else " (no requirement found: human must read)"))
    for r in res["requirements"]:
        print(f"  {r['min_months']:>3} mo  \"…{r['context']}…\"")
    return 0 if res["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
