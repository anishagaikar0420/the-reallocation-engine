#!/usr/bin/env python3
"""Verification harness for seniority-gate.py (run: python3 seniority-gate.test.py)."""
import importlib.util, sys
from pathlib import Path
spec = importlib.util.spec_from_file_location("sg", Path(__file__).with_name("seniority-gate.py"))
sg = importlib.util.module_from_spec(spec); spec.loader.exec_module(sg)

def st(text, mx=24): return sg.run(text, mx)
CASES = [
 ("real Cohere quote: 36 months of experience -> flag",
  lambda: st("Must have a Master’s degree in Data Science and 36 months of experience as Analyst or related position")["status"] == "flag"),
 ("0-2 years of experience -> pass (minimum is 0)",
  lambda: st("0-2 years of relevant experience required")["status"] == "pass"),
 ("3+ years of experience -> flag",
  lambda: st("3+ years of professional experience in ML")["status"] == "flag"),
 ("word number: three years experience -> flag",
  lambda: st("at least three years of hands-on experience")["status"] == "flag"),
 ("2 years -> pass at the boundary (24 <= 24)",
  lambda: st("2 years of experience with Python")["status"] == "pass"),
 ("BREAK: no number at all is NOT a pass (status none)",
  lambda: st("Seasoned engineer with a proven track record")["status"] == "none"),
 ("BREAK: largest wins when a junior line hides a senior line",
  lambda: st("1 year of experience with SQL. 5 years of experience leading ML teams.")["status"] == "flag"),
 ("--max-months is honored (36 months passes at 36)",
  lambda: st("36 months of experience", 36)["status"] == "pass"),
 ("KNOWN GAP: boilerplate 'over 20 years of experience' in the company blurb causes a false flag (human reads quotes)",
  lambda: st("We bring over 20 years of experience to healthcare. Entry level welcome.")["status"] == "flag"),
]
ok = 0
print("seniority-gate verification harness\n")
for name, fn in CASES:
    good = bool(fn()); ok += good
    print(f"  {'✓' if good else '✗'} {name}")
print(f"\n{ok} passed, {len(CASES)-ok} failed")
sys.exit(0 if ok == len(CASES) else 1)
