# jobpost-triage — gates for one company and one posting

## Executive summary

Two small tools for a student deciding whether one job posting is worth an application. One checks a company against the stored sponsorship dataset and refuses to guess; the other checks that every fact pulled from a posting appears in the posting. They back the recipe `recipes/cases/2026fa/anishagaikar0420-junior-ai-engineer-sponsor-triage.md`. Neither makes a network call or uses an LLM.

## Files

| File | What it does | Exit codes |
|---|---|---|
| `sponsor-triage.py` | Gates G1–G5 against `data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv` (stdlib only) | 0 ran · 2 a gate stopped the run |
| `ground-fields.py` | Every extracted field needs a verbatim quote from the posting, or "not stated" with no quote | 0 all grounded · 1 any fail · 2 bad input |
| `seniority-gate.py` / `.test.py` | G4b: largest minimum experience in a posting (9 tests) | 0 pass · 1 flag/none · 2 bad input |
| `tricky-postings.test.py` + `fixtures/` | five synthetic tricky postings (6 cases), incl. 3 documented gaps | 0 pass |
| `ground-fields.test.py` | 10 cases: 5 break attempts, 1 asserted known gap | 0 pass |

## Run

```bash
python3 scripts/contrib/2026fa/anishagaikar0420-jobpost-triage/sponsor-triage.py --company "Cohere Health" --opt-end 2027-05-31
python3 scripts/contrib/2026fa/anishagaikar0420-jobpost-triage/ground-fields.test.py
```

## Limits

`sponsor-triage.py` thresholds (365 / 730 / 90 days) are authorial choices. `ground-fields.py` proves a quote exists, not that it supports the claim. Neither checks any immigration rule. Not yet promoted to `scripts/`; no `package.json` target.
