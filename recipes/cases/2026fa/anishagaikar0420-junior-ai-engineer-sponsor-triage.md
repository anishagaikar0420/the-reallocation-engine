---
status: RUNNABLE-SAMPLE
todos_open: 6
last_gate: "sample-run v0.2.0, 2026-10-19, logs/runs/2026fa-anishagaikar0420-2.md"
attestation: null
recipe_version: 0.2.0
---

# junior-ai-engineer-sponsor-triage — Is this posting, at this company, worth one of my applications?

## Executive summary

This is a step-by-step checklist for an international master's student who wants a **junior AI or prompt-engineering job** and needs an employer that can sponsor a work visa. For one company and one job posting it answers five questions using stored data and tested scripts rather than a chatbot's guess: Does this company have any sponsorship history? Does that history include work like mine? Is the posting still open? Does every fact I think I know about the posting actually appear in it? Do I have enough time left on my work authorization?

The first run, on a real Boston health-tech company, found real sponsorship history and a live posting. It also found two traps a quick read would miss: the posting is titled "Data Scientist II" but asks for a master's degree **plus 36 months of experience**, so it is not a junior role; and the engine's "AI demand" signal for that company was inflated by one boilerplate sentence in the company description. The mode stops short of a score on purpose, because the repository has no agreed way to turn sponsorship history into a probability.

Read this if you are choosing where to spend a limited number of applications before your work authorization ends.

## 1. Purpose and when to use it

- **Who:** international master's student (F-1 / OPT; STEM OPT where it applies), target role family = junior AI engineer, prompt engineer, LLM application developer, or adjacent data-science roles.
- **When:** you have a *specific* company and a *specific* posting URL and are about to spend an application on it. Not for discovering companies (use `npm run ats:scan` once `portals.yml` exists) and not for ranking dozens of roles (use `npm run score`).
- **Prime directive:** local verified data and tested scripts first. An LLM may *propose* the field extraction that `ground-fields.py` then checks; it never supplies a count, a rate, or a pass.

## 2. Source inventory (everything below was run; see the worked run)

| What | Exact command / path | Layer | Ran? |
|---|---|---|---|
| Company funding + H-1B history | `data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv` (30,369 rows; 1,557 with approval counts) | 80 Days | yes |
| Per-company gates (new) | `python3 scripts/contrib/2026fa/anishagaikar0420-jobpost-triage/sponsor-triage.py --company "<name>" --opt-end YYYY-MM-DD` | 80 Days | yes |
| Posting liveness | `npm run ats:liveness -- <job-url>` (Playwright; needs `npx playwright install chromium`) | Job-Ops | yes |
| Field grounding (new) | `python3 scripts/contrib/2026fa/anishagaikar0420-jobpost-triage/ground-fields.py <extraction.json>` | Job-Ops | yes |
| Grounding tests (new) | `python3 scripts/contrib/2026fa/anishagaikar0420-jobpost-triage/ground-fields.test.py` | Job-Ops | yes, 10/10 |
| Skill mentions across a board | `npm run skill-demand -- <postings.json> [--role-filter "..."]`; tests: `npm run skill-demand:test` | Cognitive Pivot | yes |
| Taxonomy | `scripts/score/taxonomy/ai-engineering-skills.json` (36 skills, curated 2026-08-14) | Cognitive Pivot | yes |
| Seniority gate (new in v0.2.0) | `python3 scripts/contrib/2026fa/anishagaikar0420-jobpost-triage/seniority-gate.py <posting.txt> [--max-months 24]`; tests: `seniority-gate.test.py` (9/9) | Job-Ops | yes |
| Conformance | `npm run verify`, `npm run doctor`, `node scripts/pii-scan.mjs` | — | yes |
| Posting text | Greenhouse public board API (`boards-api.greenhouse.io`), fetched by hand with `curl` — **not** a stored ingest script | — | yes, ad hoc |

Existing commands that were **tried and could not run here**, recorded as defects rather than worked around: `npm run ats:scan -- --dry-run` (needs a private `portals.yml`); `npm run bls:local-wage` (its inputs under `data/bls/local-wage/` are absent from the clone, and the documented venv step fails on Homebrew Python 3.14 at `ensurepip`).

## 3. Proposed additions (typed TODOs; none of these exist or run)

1. [TODO DEFINE] **Sponsorship tier → probability.** `scripts/score/role-scorer.mjs` needs a numeric sponsorship `p`, but no file in the repo maps approval counts to a tier or a tier to a probability. Why it belongs: without it the composite score cannot honestly include the 80 Days layer, so this mode refuses to emit one.
2. [TODO DATA SOURCE] **`data/bls/local-wage/` inputs** (metro OEWS, BEA RPP, crosswalk). Why: a salary floor for a *junior* title needs a wage band by metro; the H-1B `median_salary_offered` field is company-wide across all sponsored titles (here $160,000, driven by senior roles), which is the wrong anchor for a new graduate.
3. [TODO DEFINE] **Time window of the H-1B counts.** The dataset README says "historical" and the audit documents funding dates only. Why: "104 approvals" means something different over 2 years than over 10.
4. [TODO DEV] **Boilerplate stripping for `skill-demand`.** Evidence: on Cohere Health's board, "Agentic / AI agents" is counted in 61 of 76 postings (80%), but 56 of those 61 vanish when one sentence of the company "About" paragraph ("agentic AI-powered solutions") is removed; the other 5 are senior, staff or AI-engineer roles. The inflated hits include claims-auditor and sales postings. Why: the monitor counts mentions, so a junior applicant could read company marketing as a skill requirement.
5. ~~[TODO DEV] Seniority extraction from requirements.~~ **CLOSED v0.2.0:** `seniority-gate.py` exists, 9/9 tests pass, and on the real Cohere Health posting it exits 1 with `largest_min=36mo allowed=24mo` and prints the quote (evidence: `course/2026fa/submissions/anishagaikar0420/worked-run.md` §7). Residual limit: it matches numbers only ("seasoned" passes as `none`) and can false-flag company boilerplate (tested known gap).
6. [TODO DEV] **Company entity resolution for the lookup.** 208 normalized company names map to more than one CSV row (e.g. `3AM INNOVATIONS INC` and `3AM INNOVATIONS LLC`), so exact matching can only refuse. `scripts/sec/entity-resolution.py` exists and is the likely home for a safe disambiguation.
7. [TODO APPROVE] **Named-human gate clearance** of G1–G8 on a live (non-sample) run; required to move this recipe to RUNNABLE-LIVE.

## 4. Phase gates (hard stops; a closed gate produces no recommendation)

Run order is local-first: G1–G5 read only the CSV, then network gates.

| Gate | Test (testable, from the scripts) | Pass | Flag (human must read) | Stop (refuse) |
|---|---|---|---|---|
| G0 timeline input | `--opt-end` is a valid future date | yes | — | missing / past → stop, no CSV read |
| G1 snapshot age | newest `latest_funding_date` in CSV vs today | ≤ 365 days | 366–730 days | > 730 days |
| G2 company match | exactly one CSV row after deterministic normalization (uppercase, punctuation out, trailing INC/LLC/CORP… out); **no fuzzy match** | 1 match | — | 0 or ≥ 2 matches |
| G3 sponsor record | `Total Approvals` non-blank | count present | blank = "no record" (never "does not sponsor") | — |
| G4 role family | a sponsored title contains a role keyword and is not senior-flagged (senior/staff/lead/principal/manager/director/head/VP) | ≥ 1 non-senior match | only senior matches, or none | — |
| G4b seniority (v0.2.0) | `seniority-gate.py`: largest stated minimum experience in the posting | ≤ 24 months | no number found (`none`, never a pass) | > 24 months → human must read quote; default action Skip |
| G5 runway | days from today to `--opt-end` | ≥ 90 days | < 90 days — a **named human** must clear | ≤ 0 days |
| G6 liveness | `npm run ats:liveness -- <url>` → `active` | active | `uncertain` | `expired` → Skip |
| G7 grounding | `ground-fields.py`: every field has a verbatim quote or is "not stated" with no quote; and a human has read `seniority` and `skills` quotes | all PASS + human read | any quote exists but does not support its claim | any FAIL |
| G8 human release | a named human writes who/what/when in the run log | cleared | — | not cleared → nothing is applied to |

Thresholds 365 / 730 / 90 days and the 8-character minimum quote are authorial choices ([DEFINE]-style, documented in the scripts); they are not statistical results.

## 5. What it can and cannot verify

**Can verify (script or data established it):**
- A company name has exactly one exact-normalized row in the committed CSV, and what that row says (approvals, denials, rate, last funding stage/date/amount, top sponsored titles).
- How old the newest funding signal in the dataset is relative to today (388 days at the first run).
- Whether a sponsored title in that row matches the role keywords, and whether it is senior-flagged.
- Whether a Greenhouse-style posting URL still resolves to a live posting (`active` / `expired` / `uncertain`).
- Whether each extracted field's quote appears verbatim in the posting text, and whether numbers in the value appear in the quote.
- Day arithmetic between today and an OPT end date you supply.

- Whether the posting *states* a minimum-experience number above 24 months (G4b), with the quote printed.

**Cannot verify (labelled inferred or out of scope, never presented as a result):**
- **That the company will sponsor *you*, for *this* job.** The CSV is a history of petitions, not a policy. Absence of a row proves nothing.
- **The H-1B time window** of the counts (TODO 3), or whether approvals were for entry-level roles. The title list is "top titles" only.
- **That "recent Form D" is recent.** The newest funding date in the data is 2025-09-26. The audit reports a median funding age of 5.94 years. "Recent" is relative to the snapshot.
- **Immigration rules.** G5 is subtraction. Nothing here checks cap-gap, STEM OPT eligibility, E-Verify status, lottery odds or cap-exempt status. A designated school official or an attorney decides those.
- **That a quote supports its claim.** `ground-fields.py` proves existence, not support: a real sentence attached to the wrong field passes (this is asserted as a known gap in the test file). A person reads the `seniority` and `skills` quotes.
- **That a posting is genuine or not a pipeline-filler ("ghost") posting.** Liveness says the page resolves, not that anyone is hiring.
- **Role quality / AI-resilience.** `role_quality` carries weight 0.0 in `role-scorer.mjs`; this mode does not use it.
- **What the job pays *you*.** Posted salary ranges are quoted; wage data for a metro is not available here (TODO 2).
- **Postings behind logins or non-Greenhouse ATSs** that `ats:liveness` cannot classify.

## 6. Output contract (two customers, P5)

**Agent log** — `logs/triage-<company-slug>-<YYYY-MM-DD>.json` (JSON). Concatenate the machine outputs; never hand this to the student:

```json
{
  "recipe": "junior-ai-engineer-sponsor-triage", "recipe_version": "0.2.0", "run_date": "YYYY-MM-DD",
  "sponsor_triage": { "...": "output of sponsor-triage.py (schema sponsor-triage/1): gates[], record{csv_line,...}" },
  "liveness": { "url": "...", "result": "active|expired|uncertain" },
  "grounding": { "...": "output of ground-fields.py (schema ground-fields/1)" },
  "gates_cleared_by": { "G5": null, "G7": null, "G8": null },
  "score": null,
  "score_refusal": "tier->probability undefined (TODO 1)"
}
```

**Human report** — `reports/generated/triage-<company-slug>-<YYYY-MM-DD>.md`. Opens with an executive summary (what this is, why read it, what it found), then:

| Question | Answer | Established by | Read this before acting |
|---|---|---|---|
| Sponsorship history? | e.g. "104 approvals on record" | CSV line N | window unknown |
| Evidence for my role? | titles matched / senior-only | CSV line N | top titles only |
| Posting live? | active / expired | `ats:liveness` | not proof anyone is hiring |
| Facts grounded? | k of n fields | `ground-fields.py` | I read `seniority` + `skills` quotes: ✓/✗ |
| Runway? | N days to OPT end | arithmetic | no rules checked |
| **Decision** | **Apply / Skip / needs human** | **human only** | name + date |

The report never prints a probability or a composite score while TODO 1 is open.

## 7. Stop conditions (refuse, do not guess)

The mode must stop and say why when any of these holds: `--opt-end` missing or not in the future; CSV snapshot older than 730 days; company name matches zero or more than one row; liveness result is `expired`; any grounding FAIL; a request to output a sponsorship probability, composite score, or "likelihood of getting a visa"; a request to infer sponsorship for a company with no approval record; or the student asks for legal advice on status.

## 8. Run log template (`logs/runs/<term>-<handle>-<n>.md`)

```markdown
## Executive summary
<what was run, for whom (persona), what it found — no paths>

## Run record
- date / recipe / recipe_version / status reached
- inputs: company, posting URL, opt_end (PLACEHOLDER or real: say which), keywords
- commands: <verbatim>
- outputs: <artifact paths>, gate results G0–G8
- result: Apply | Skip | needs-human, and who decided
- open issues: <TODOs, defects found, commands that could not run>
```
