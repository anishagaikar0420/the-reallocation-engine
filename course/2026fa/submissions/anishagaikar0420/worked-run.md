# Worked run — junior-ai-engineer-sponsor-triage v0.1.0 (RUNNABLE-SAMPLE)

## Executive summary

This document shows the new checklist being run for real, on one real company and one real job posting, with the actual terminal output pasted in. It matters because the assignment is graded on whether the mode *ran*, and on being honest about what it could not check. The run found real sponsorship history (104 approvals) and a live posting, and then two things a quick read would have missed: the "Data Scientist II" role needs a master's degree plus 36 months of experience, so it is not a junior role; and an "AI agents" demand signal for the same company was almost entirely one boilerplate sentence. The run stopped without a score, deliberately, and several things I tried broke in useful ways (listed below).

## Run record

- **Date:** 2026-10-19 · **Stage reached:** RUNNABLE-SAMPLE (one real run; no named human has cleared the gates) · **Attestation:** `null` in frontmatter (see the attestation section: not yet signed)
- **Company:** Cohere Health (public data). **Posting:** "Data Scientist II", United States, a live Greenhouse posting (job id 8005450003).
- **Persona / profile:** international master's student targeting junior AI / prompt-engineer roles. **The OPT end date `2027-05-31` is a PLACEHOLDER**, not a real date; no personal data from `private/` was read or written.
- **Posting text** was fetched once from Greenhouse's public board API and is *not* committed (third-party content). Provenance hash of the flattened text: `sha256 ed78a75a0c87a414…`; of the whole-board JSON used for skill-demand: `bc14899e28f24f8f…`.
- **Who did what:** Claude Code ran the commands and *drafted* the field extraction (a model judgment). `ground-fields.py` then checked it mechanically. No one has yet signed the human gates.
- **Output paths:** `$OUT` below stands for a scratch directory outside the repo; the artifacts that matter are copied to `artifacts/` beside this file. The wrapper that printed each command strips the shell quotes (so `--company Cohere Health` is really `--company "Cohere Health"`).

## 1. Toolchain baseline (existing, unmodified commands)

```text
$ npm run verify

> the-reallocation-engine@1.0.0 verify
> node scripts/conformance.mjs && node scripts/manifest-check.mjs

conformance: 161 files (85 md · 39 py · 30 js · 4 sh · 3 json)
✓ all conform (machine half of P4). Adequacy is still the human gate.
MANIFEST CHECK — The Reallocation Engine
==========================================

WARN (3):
  W1 ignore path not in .gitignore: archive/
  W2 private path not gitignored (PII/secret risk): private/
  W2 private path not gitignored (PII/secret risk): data/ats/

✓ manifest check passed (3 warnings)
[exit 0]
```

```text
$ npm run skill-demand:test

> the-reallocation-engine@1.0.0 skill-demand:test
> node scripts/score/skill-demand-monitor.test.mjs

skill-demand-monitor verification harness

  ✓ sample-size gate halts on 3 postings and emits no ranked list
  ✓ known skill count matches a hand-count of the committed fixture (python: 22/22)
  ✓ a posting missing description_text is rejected with a named reason, not silently dropped
  ✓ postings with no recognized skills set low_coverage=true rather than a silently-thin ranking
  ✓ a --min-sample override below the default is threaded through and flagged, never reported as unconditional confidence

5 passed, 0 failed
[exit 0]
```

Not runnable on this machine, recorded as defects (not worked around): `npm run ats:scan -- --dry-run` → `Error: portals.yml not found. Run onboarding first.`; `npm run bls:local-wage` → its input directory `data/bls/local-wage/` is absent from the clone, and `python3 -m venv .venv` failed at `ensurepip` on Homebrew Python 3.14 (the same Python-3.14 environment trap as in my film-project setup log).

## 2. The mode, run on a real scenario

### A. Local gates: sponsorship record, role family, runway (no network)

```text
$ python3 scripts/contrib/2026fa/anishagaikar0420-jobpost-triage/sponsor-triage.py --company Cohere Health --opt-end 2027-05-31 --json $OUT/cohere.json --md $OUT/cohere.md
sponsor-triage: status=complete  gates=G1:flag,G2:pass,G3:pass,G4:pass,G5:pass
[exit 0]
```

Human-readable report produced by that run: `artifacts/sponsor-triage-cohere-health.md`. Key lines (G1 flag = the newest funding date in the whole dataset is 388 days old):

| Gate | Status | Detail |
|---|---|---|
| G1 snapshot-age | flag | newest funding date in data is 2025-09-26; 388 days before 2026-10-19 |
| G2 company-match | pass | matched CSV line 6084: COHERE HEALTH INC |
| G3 sponsor-record | pass | 104 approvals on record |
| G4 role-family | pass | 2 sponsored title(s) match role keywords; 1 not senior-flagged |
| G5 timeline | pass | 224 days to opt_end (arithmetic only) |

Record: Boston, MA · Series C · 2025-05-07 · $89,999,876 · 104 approvals, 2 denials (98.1%) · company-wide median sponsored salary $160,000 · top sponsored titles include *Machine Learning Engineer* (non-senior) and *Senior Machine Learning DevOps Engineer* (senior-flagged).

### B. Break attempts on the same script

```text
$ python3 scripts/contrib/2026fa/anishagaikar0420-jobpost-triage/sponsor-triage.py --company Cohere Healthh --opt-end 2027-05-31 --json $OUT/unk.json
sponsor-triage: status=stopped  gates=G1:flag,G2:stop
[exit 2]

$ python3 scripts/contrib/2026fa/anishagaikar0420-jobpost-triage/sponsor-triage.py --company 3AM Innovations --opt-end 2027-05-31 --json $OUT/amb.json
sponsor-triage: status=stopped  gates=G1:flag,G2:stop
[exit 2]

$ python3 scripts/contrib/2026fa/anishagaikar0420-jobpost-triage/sponsor-triage.py --company Cohere Health --json $OUT/noopt.json
sponsor-triage: status=stopped  gates=G5:stop
[exit 2]

$ python3 scripts/contrib/2026fa/anishagaikar0420-jobpost-triage/sponsor-triage.py --company Cohere Health --opt-end 2026-01-01 --json $OUT/past.json
sponsor-triage: status=stopped  gates=G5:stop
[exit 2]

$ python3 scripts/contrib/2026fa/anishagaikar0420-jobpost-triage/sponsor-triage.py --company Cohere Health --opt-end 2030-01-01 --today 2028-01-01 --json $OUT/stale.json
sponsor-triage: status=stopped  gates=G1:stop
[exit 2]

$ python3 scripts/contrib/2026fa/anishagaikar0420-jobpost-triage/sponsor-triage.py --company Cohere Health --opt-end 2026-12-01 --json $OUT/tight.json
sponsor-triage: status=complete  gates=G1:flag,G2:pass,G3:pass,G4:pass,G5:flag
[exit 0]

$ python3 scripts/contrib/2026fa/anishagaikar0420-jobpost-triage/sponsor-triage.py --company 10 Percent Happier --opt-end 2027-05-31 --json $OUT/norec.json
sponsor-triage: status=complete  gates=G1:flag,G2:pass,G3:flag,G4:flag,G5:pass
[exit 0]
```

What each one shows: unknown company → stop at G2 (no fuzzy rescue); two CSV rows for one normalized name (`3AM INNOVATIONS INC` / `LLC`) → stop at G2 rather than pick one; missing OPT date and past OPT date → stop at G5 before reading the CSV; stale snapshot (simulated by `--today 2028-01-01`) → stop at G1; OPT end 2026-12-01 → G5 flag (a named human must clear); a company with no approval count → G3 flag with the text *absence of evidence, NOT evidence the company does not sponsor*.

### C. Liveness gate (existing command, real Playwright)

```text
$ npm run ats:liveness -- https://job-boards.greenhouse.io/coherehealth/jobs/8005450003 https://job-boards.greenhouse.io/coherehealth/jobs/1111111111

> the-reallocation-engine@1.0.0 ats:liveness
> node scripts/ats/check-liveness.mjs https://job-boards.greenhouse.io/coherehealth/jobs/8005450003 https://job-boards.greenhouse.io/coherehealth/jobs/1111111111

Checking 2 URL(s)...

✅ active     https://job-boards.greenhouse.io/coherehealth/jobs/8005450003
❌ expired    https://job-boards.greenhouse.io/coherehealth/jobs/1111111111
           redirect to https://job-boards.greenhouse.io/coherehealth?error=true

Results: 1 active  1 expired  0 uncertain
[exit 1]
```

The nonzero exit is the design (any expired/uncertain URL exits 1). The live posting is `active`; an invented id on the same board redirects to `?error=true` and is classed `expired`. This is the only network gate and it is a gate, not a vote.

### D. Grounding (new script) — tests, then the real posting

```text
$ python3 scripts/contrib/2026fa/anishagaikar0420-jobpost-triage/ground-fields.test.py
ground-fields verification harness

  ✓ exact quote grounds a field
  ✓ curly-vs-straight apostrophe still grounds (normalized)
  ✓ BREAK: invented detail not in posting is rejected (the 'headquartered near Boston' error)
  ✓ BREAK: value with no quote is ungrounded
  ✓ BREAK: one-word quote is too short to ground anything
  ✓ BREAK: number in value that is not in the quote fails
  ✓ 'not stated' with no quote passes for a field the posting really omits
  ✓ BREAK: 'not stated' salary fails when a $ figure is in the text (missed value)
  ✓ BREAK: 'not stated' carrying a quote is contradictory
  ✓ KNOWN GAP: real quote attached to the WRONG claim still PASSES (needs a human)

10 passed, 0 failed
[exit 0]

$ python3 scripts/contrib/2026fa/anishagaikar0420-jobpost-triage/ground-fields.py $OUT/cohere-extraction.json --json $OUT/cohere-ground.json
PASS  title        grounded
PASS  location     grounded
PASS  remote       grounded
PASS  salary       grounded
PASS  seniority    grounded
PASS  skills       grounded
PASS  visa_sponsorship not stated (absence is only cue-checked for salary/remote; otherwise unverified)
ground-fields: 7/7 grounded
[exit 0]
```

All seven fields are grounded, **including** a `skills` value that lists SQL, Tableau and LLMs while its quote covers only Python, PySpark, Airflow and SageMaker. That passes because the checker proves a quote *exists*, not that it supports every word of the value. It is the documented known gap showing up in real data (SQL, Tableau and LLMs *are* in the posting, in other lines, so the claim is true; but the quote does not prove it). A person has to read it. The `seniority` quote reads: *"Must have a Master's degree in Data Science, Statistics, Biostatistics or related field (willing to accept foreign education equivalent) and 36 months of experience as Analyst or related position analyzing datasets."* — **a human reading that sentence is what turns the title "II" into "not a junior role"; no script made that call.**

### E. Skill-demand across the company's whole board (existing command)

```text
$ npm run skill-demand -- $OUT/cohere-board.json --out-dir $OUT/sd-all

> the-reallocation-engine@1.0.0 skill-demand
> node scripts/score/skill-demand-monitor.mjs $OUT/cohere-board.json --out-dir $OUT/sd-all

✓ skill-demand-monitor: 76 ingested → 76 valid → 76 candidates → status: ranked
  24 skills ranked; low_coverage=false
  $OUT/sd-all/skill-demand.json  +  $OUT/sd-all/skill-demand.md
[exit 0]

$ npm run skill-demand -- $OUT/cohere-board.json --role-filter ai engineer --out-dir $OUT/sd-ai

> the-reallocation-engine@1.0.0 skill-demand
> node scripts/score/skill-demand-monitor.mjs $OUT/cohere-board.json --role-filter ai engineer --out-dir $OUT/sd-ai

✓ skill-demand-monitor: 76 ingested → 76 valid → 1 candidates → status: insufficient_sample
  $OUT/sd-ai/skill-demand.json  +  $OUT/sd-ai/skill-demand.md
[exit 0]
```

`artifacts/skill-demand-ai-engineer-REFUSED.md` is the refusal report. Only 1 posting on this 76-posting board matched "ai engineer", so the sample-size gate fired and no ranking was written. The unfiltered run ranks 24 skills, and its top line ("Agentic / AI agents", 61 of 76, 80%) is the boilerplate trap analysed in §4.

### F. Repo checks for the new files

```text
$ node scripts/pii-scan.mjs
pii-scan: 1 finding(s) — see DATA_CONTRACT.md §Zero-Conditions

  [email] package-lock.json — <npm package maintainer's email, redacted by me>

If a finding is a false positive (fictional data outside the sanctioned dirs),
move it under search/examples/ or resumes/ rather than allowlisting it here.
[exit 1]
```

The single `pii-scan` finding is an npm package maintainer's email address inside `package-lock.json` (redacted above by me, because quoting it verbatim made my own write-up trip the scanner). That file is unchanged by this work (`git status` shows it clean; it was committed in the repo's "Fall 2026 fresh cut"), so this is a pre-existing false positive on `main`, not something I introduced — but it means a CI working-tree scan would fail regardless of my PR, and I am reporting it, not allowlisting it.

```text
$ npm run doctor  (last 12 lines)
  ✓ no private/PII paths are tracked

RECIPES (33)
  with lifecycle frontmatter: 33   missing: 0
  by status: DRAFT 28 · RUNNABLE-SAMPLE 4 · RUNNABLE-LIVE  # DRAFT | SPECIFIED | RUNNABLE-SAMPLE | RUNNABLE-LIVE | VERIFIED 1
  open TODOs: 318 declared (in frontmatter) · 318 [TODO markers in bodies

SUMMARY
  environment: ✓ runnable
  recipes: 33/33 carry lifecycle frontmatter — all tracked
  next: continue
[exit 0]
```

## 3. Verified vs inferred (line by line)

| Statement | Status | Basis |
|---|---|---|
| Cohere Health has exactly one row (line 6084) after normalization | **Verified** | `sponsor-triage.py` G2; independently read with `sed -n 6084p` (V4) |
| 104 approvals, 2 denials, Series C 2025-05-07 | **Verified** (as a record) | CSV line 6084; meaning of the counts is **not** verified (window undocumented) |
| Dataset has 30,369 rows, 1,557 with an approval count | **Verified** | script and independent `csv` count agree (V3) |
| Newest funding date in the dataset is 2025-09-26 (388 days old) | **Verified** | G1; matches the repo's own audit (`SEC_DOL_H1b_data_mapped-audit.md`) |
| The posting URL is live | **Verified** (page resolves) | `ats:liveness` → `active` |
| An invented URL on the same board is dead | **Verified** | `ats:liveness` → `expired` |
| Each of the 6 stated fields has a verbatim quote in the posting | **Verified** | `ground-fields.py` 7/7 |
| The posting never mentions visa/sponsorship | **Verified** | `ground-fields.py` "not stated" + independent word-bounded grep (V5) |
| 61 of 76 postings match the agents pattern | **Verified** | `skill-demand` and my independent regex recount (V6) |
| 56 of those 61 vanish without one boilerplate sentence | **Verified** | V6b; I did *not* read each of the 56 individually |
| "This posting is not a junior role" | **Inferred** | my reading of the 36-month quote; a human must confirm |
| "The skill signal is meaningless" | **Inferred** | follows from V6b, but whether 5 true hits matter is a judgment |
| "This company will sponsor me for this job" | **NOT established** | a petition history is not a promise; mode refuses to claim it |
| "I should apply" / "I should skip" | **NOT produced** | stop condition: no tier→probability mapping (TODO 1); human decides |
| Field *values* ("Python, PySpark…") | **Model-drafted**, quote-checked only | the `skills` value outruns its quote (§2D) |

## 4. Verification

How I confirmed the output was real, beyond re-running it:

```text
$ # V1 mutation: disable the quote-in-posting check, expect the harness to FAIL
  ✗ BREAK: invented detail not in posting is rejected (the 'headquartered near Boston' error)  got={'location': 'PASS'} expected={'location': 'FAIL'}
9 passed, 1 failed
[exit 1]

$ # V2 determinism: same inputs twice, diff the JSON
identical

$ # V3 independent count of CSV rows and rows with an approval count (csv module, not the script)
rows: 30369 | with approvals: 1557

$ # V4 the matched CSV line, read with sed (script said line 6084)
COHERE HEALTH INC,Other Technology,cohere-health.com,BOSTON,MA
script csv_line = 6084

$ # V5 independent check that the posting never mentions sponsorship/visa words (word-bounded grep)
(no matches)

$ # V6 independent recount of the "agentic" skill, then WHERE it comes from
independent count: 61 of 76
matched strings: {'agentic': 61, 'ai agents': 2, 'multi-agent': 3}
in posting "Business Development Representative": ... Health: Cohere Health’s clinical intelligence platform and agentic AI-powered solutions connect health pla...

$ # V6b how many of those hits survive if the one boilerplate sentence is removed?
hits: 61 | vanish without the sentence: 56 | remain: 5
remaining titles: ['Senior Manager, Applied Science', 'Sr.AI Engineer', 'Staff Applied Scientist', 'Staff Data Architect', 'Staff Software Engineer']

$ # V7 does the script json parse, and what does the "seniority" quote say?
parsed ok; 7 / 7 grounded
Must have a Master’s degree in Data Science, Statistics, Biostatistics or related field (willing to accept foreign education equivalent) and 36 months of experience as Analyst or related position analyzing datasets.
```

Reading the above: **V1** removing the quote-in-posting check makes the grounding tests fail (1 of 10), so the harness can fail; **V2** two runs produce identical JSON; **V3–V4** the script's counts and matched line equal what an independent `csv`/`sed` read finds; **V5** the "not stated" visa field is independently confirmed by grep; **V6/V6b** the skill signal reconciles with an independent count and is then shown to be 92% boilerplate; **V7** the emitted JSON parses.

## Attestation

- Recipe: `anishagaikar0420-junior-ai-engineer-sponsor-triage` v0.1.0
- By: **prepared by Claude Code for Anisha Gaikar · 2026-10-19. Not yet signed.** Per the constitution the attestation is the human's record; it is left unsigned (`attestation: null`) until Anisha re-runs the commands below and signs. The recipe stays RUNNABLE-SAMPLE.

### Tested
| Ran | Saw | Expected |
|---|---|---|
| `npm run verify` | all conform; 3 pre-existing warnings | pass |
| `npm run skill-demand:test` | 5 passed, 0 failed | pass |
| `sponsor-triage.py` on Cohere Health | status=complete; G1 flag, G2–G5 pass | company found, role evidence, runway OK |
| **BREAK:** misspelled company | stop at G2, exit 2 | refuse, no fuzzy rescue |
| **BREAK:** company with two rows (`3AM Innovations`) | stop at G2 naming both lines, exit 2 | refuse, not pick one |
| **BREAK:** no `--opt-end` / past `--opt-end` | stop at G5, exit 2 | refuse to triage without a timeline |
| **BREAK:** simulated stale snapshot (`--today 2028-01-01`) | stop at G1 | refuse on data older than 730 days |
| `sponsor-triage.py`, company with no approval count | G3 flag (no record), complete | flag, not "does not sponsor" |
| `ats:liveness` live URL / invented id | active / expired | active / expired |
| `ground-fields.test.py` (10 cases incl. 5 breaks + 1 known-gap) | 10 passed | pass |
| **BREAK:** mutant `ground-fields.py` with quote check disabled | 1 of 10 failed (exit 1) | harness must fail on a broken checker |
| `ground-fields.py` on the real posting | 7/7 grounded | grounded |
| `skill-demand --role-filter "ai engineer"` on a 76-posting board | 1 candidate → `insufficient_sample`, no ranking | refuse to rank |
| determinism: same inputs twice | identical JSON | identical |

### Did not test
- Any ATS other than Greenhouse (Lever, Ashby, Workday, SmartRecruiters) for liveness or posting fetch.
- `ats:scan -- --dry-run` (no `portals.yml`), `bls:local-wage` (inputs absent), `npm run score` (blocked by TODO 1).
- Company-name edge cases: non-ASCII names, `&` vs `and`, `dba` names, names that differ only in a legal suffix other than those listed.
- `--keywords` overrides and the senior regex on real titles beyond the Cohere Health sample.
- `ground-fields.py` against HTML postings, non-breaking spaces, or en/em-dash differences (only curly quotes are normalized).
- Whether the 56-hit boilerplate result generalizes to any other company's board.
- The GitHub CI workflows themselves (not run; I ran their local commands), a fork, a branch, or a PR.
- A real OPT/STEM OPT date, and any immigration rule at all.
- A named human clearing any gate (so no RUNNABLE-LIVE).
- Re-running by anyone other than the author of the scripts.

### Broke during testing, fixed
- `sponsor-triage.py`: a past `--opt-end` first ran G1–G4 and only stopped at G5; fixed to fail fast before reading the CSV.
- `sponsor-triage.py`: G4 returned `pass` when every matched title was senior (e.g. only "Senior ML DevOps Engineer"); fixed by adding a senior-flag regex and a `flag` outcome.
- My own independent check was wrong: a case-insensitive grep for `OPT` matched "optimization" in the posting. Re-ran word-bounded (V5).
- My exploratory count "155 sponsors with AI/ML titles" over-counted (it also matched industry text and a loose `"ai "`). Recomputed with the mode's own keywords: **159** with a role-keyword title, **104** with a non-senior one. Docs use the corrected numbers.
- The first claim that the agents signal was "one sentence of boilerplate" was too strong; checked and corrected to **56 of 61** (5 real hits remain).
- Files were first placed where the assignment text says; the repo's `CONTRIBUTING.md` and CI gate require `scripts/contrib/<term>/…`, `recipes/cases/<term>/…`, `logs/runs/…`. Moved, and every path re-run from the final location (this transcript).
- Not fixed, logged: venv creation fails on Python 3.14; `data/bls/local-wage/` missing from the clone; the pre-existing `pii-scan` hit in `package-lock.json`; `DOMAIN.md` says 42 recipes while `npm run doctor` counts 33.

## Reflection

**What went well.** Every gate in the mode is a script exit code or a number with a source line; the mode refused in 5 of 7 break attempts and said why. Running it on real data immediately beat my priors twice (the "II" title and the 80% skill count), and in both cases the *tool output was correct and the meaning was wrong*, which is exactly the boundary the recipe draws.

**What it got wrong or missed.** (1) The seniority trap passes every gate; only a human reading one quote caught it. (2) `ground-fields.py` cannot tell a supporting quote from a merely present one, and the real `skills` field proves it. (3) "Recent Form D" is not recent: the data ends 2025-09-26, so G1 flags every run today. (4) The H-1B counts have no stated time window, so "104 approvals" is not interpretable as a rate. (5) The posting fetch was an ad hoc `curl`, not a stored ingest script, which breaks the repo's rule that only ingest scripts touch the network.

**Next steps (in the recipe as typed TODOs).** Define a tier→probability mapping so the scorer can run (TODO 1); strip company boilerplate before counting skills (TODO 4); add a seniority-from-requirements gate (TODO 5); write a stored posting-fetch script; get `data/bls/local-wage/` and a working venv so a junior-appropriate wage floor exists (TODO 2); then a live run with a real OPT date and a named human clearing G5/G7/G8 to attempt RUNNABLE-LIVE.

## 7. Update v0.2.0 — TODO 5 closed: seniority gate (run 2026-10-19, same day)

The v0.1.0 run found by hand that "Data Scientist II" requires 36 months of experience. v0.2.0 turns that into a gate. The posting text was fetched once with `curl` from the public Greenhouse API into a scratch folder (still not a stored ingest script; open defect) and is not committed.

```text
$ python3 scripts/contrib/2026fa/anishagaikar0420-jobpost-triage/seniority-gate.test.py
  ✓ real Cohere quote: 36 months of experience -> flag
  ✓ 0-2 years of experience -> pass (minimum is 0)
  ✓ 3+ years of experience -> flag
  ✓ word number: three years experience -> flag
  ✓ 2 years -> pass at the boundary (24 <= 24)
  ✓ BREAK: no number at all is NOT a pass (status none)
  ✓ BREAK: largest wins when a junior line hides a senior line
  ✓ --max-months is honored (36 months passes at 36)
  ✓ KNOWN GAP: boilerplate 'over 20 years of experience' in the company blurb causes a false flag (human reads quotes)
9 passed, 0 failed

$ python3 scripts/contrib/2026fa/anishagaikar0420-jobpost-triage/seniority-gate.py <posting.txt>
seniority-gate: status=flag largest_min=36mo allowed=24mo
   36 mo  "… field (willing to accept foreign education equivalent) and 36 months of experience as Analyst or related position analyzin…"
[exit 1]

$ seniority-gate.py <empty file>        # BREAK
seniority-gate: cannot read posting text at <path>
[exit 2]

$ seniority-gate.py <posting.txt> --max-months 36
seniority-gate: status=pass largest_min=36mo allowed=36mo
[exit 0]
```

| Statement | Status | Basis |
|---|---|---|
| The posting states a 36-month minimum | **Verified** | script match + printed quote |
| 24 months is the right "junior" ceiling | **Judgment** | authorial `[DEFINE]`; the `--max-months 36` run shows the verdict flips with it |
| The role is not entry level | **Inferred** | the human still reads the quote (G7/G8) |

**Honest limits of v0.2.0:** numbers only ("seasoned" gives `none`, never a pass); company boilerplate can false-flag (tested known gap); not tried on any posting other than Cohere Health's. **Broke during testing:** none this round. The test run passed 9/9 on first execution, so I have not seen the harness fail here; I did not repeat the v0.1.0 mutant test on this script.

## 8. Update v0.2.0 — pitch lineage and the five tricky postings

The pitch promised "at least five deliberately tricky postings". They now exist as synthetic, fictional-company fixtures (`fixtures/tricky-postings.json`): no salary (honest and invented variants), an implied skill, a "Junior" title over "5+ years", a `$` that is a perk not a salary, and "remote-friendly" over three onsite days.

```text
$ python3 scripts/contrib/2026fa/anishagaikar0420-jobpost-triage/tricky-postings.test.py
  ✓ T1-no-salary-honest: fields={'salary': 'PASS', 'title': 'PASS'} seniority=none
  ✓ T1b-invented-salary: fields={'salary': 'FAIL'} seniority=none
  ✓ T2-implied-skill: fields={'skills': 'PASS'} seniority=none  [human must read: skills]
  ✓ T3-conflicting-seniority: fields={'seniority': 'PASS'} seniority=flag  [human must read: seniority]
  ✓ T4-dollar-sign-not-salary: fields={'salary': 'FAIL'} seniority=none  [human must read: salary]
  ✓ T5-remote-ambiguity: fields={'remote': 'PASS'} seniority=none  [human must read: remote]
6 passed, 0 failed
```

**BREAK (mutation):** flipping the expected salary verdict in the fixture file made the harness report `4 passed, 2 failed`; restoring it gave 6/6 again. So the harness can fail.

**What this proves and does not.** Machine results: the invented salary is refused (T1b); the 5-year requirement under a "Junior" title is flagged (T3). Three cases are **documented gaps** where the script's verdict is not the truth: T2 and T5 PASS although a human would say the claim is loose or wrong (a real quote attached to a wrong or loose claim), and T4 FAILS although "not stated" was right (the `$` cue over-triggers). In all three a person must read the quote. The six cases were written by me after seeing how the scripts behave, so they show the gaps rather than test the scripts blindly; all passed on first run.
