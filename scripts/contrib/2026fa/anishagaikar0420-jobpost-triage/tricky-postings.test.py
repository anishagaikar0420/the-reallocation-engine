#!/usr/bin/env python3
"""Runs ground-fields.py and seniority-gate.py over the synthetic tricky postings (fixtures/tricky-postings.json).
All companies are fictional; no real posting or personal data. Failures show up as a mismatch with the expectation
written next to each fixture. Cases tagged human_must_read are DOCUMENTED GAPS: the script says PASS (or FAIL) and a person must judge."""
import importlib.util, json, sys
from pathlib import Path
here = Path(__file__).parent
def load(n, f):
    s = importlib.util.spec_from_file_location(n, here / f); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
gf, sg = load("gf", "ground-fields.py"), load("sg", "seniority-gate.py")
fx = json.loads((here / "fixtures/tricky-postings.json").read_text())["fixtures"]
print("tricky-postings verification harness (synthetic fixtures)\n")
bad = 0
for f in fx:
    rep = gf.run({"posting_text": f["posting_text"], "fields": f["fields"]})
    got = {r["field"]: r["verdict"] for r in rep["results"]}
    sen = sg.run(f["posting_text"], sg.MAX_MONTHS_DEFAULT)["status"]
    ok = got == f["expect_fields"] and sen == f["expect_seniority"]
    bad += not ok
    tag = f"  [human must read: {', '.join(f['human_must_read'])}]" if f.get("human_must_read") else ""
    print(f"  {'✓' if ok else '✗'} {f['id']}: fields={got} seniority={sen}{tag}")
    if not ok: print(f"      expected fields={f['expect_fields']} seniority={f['expect_seniority']}")
print(f"\n{len(fx)-bad} passed, {bad} failed")
sys.exit(1 if bad else 0)
