## Executive summary

A first sample run of a new checklist for choosing which job postings are worth an application, for an international master's student targeting junior AI or prompt-engineering roles. It was run on one real company and one real posting. It found real sponsorship history and a live posting, but also that the "II" role requires 36 months of experience and that an "AI agents" demand signal was 92% boilerplate. It stopped without a score on purpose. Nothing here is personal data.

## Run record

- **date:** 2026-10-19
- **recipe:** `recipes/cases/2026fa/anishagaikar0420-junior-ai-engineer-sponsor-triage.md` v0.1.0 · status reached **RUNNABLE-SAMPLE** · attestation: none (unsigned)
- **inputs:** company "Cohere Health" (public record in `mapped_student_employment_targets_v3.csv`, line 6084); posting `https://job-boards.greenhouse.io/coherehealth/jobs/8005450003` (live, fetched once via the public Greenhouse API, not committed); whole board of 76 postings; `--opt-end 2027-05-31` is a **PLACEHOLDER**, not a real date. No `private/` data was read.
- **commands:** `npm run verify`; `npm run skill-demand:test`; `sponsor-triage.py --company "Cohere Health" --opt-end 2027-05-31` plus 7 break/edge variants; `npm run ats:liveness -- <live url> <invented url>`; `ground-fields.test.py`; `ground-fields.py` on the real posting; `npm run skill-demand -- <board.json>` with and without `--role-filter "ai engineer"`; `node scripts/pii-scan.mjs`; `npm run doctor`. Verbatim output: `course/2026fa/submissions/anishagaikar0420/worked-run.md`.
- **outputs:** `course/2026fa/submissions/anishagaikar0420/artifacts/` (triage JSON+MD, grounding JSON+MD, refused skill-demand report, whole-board skill-demand JSON).
- **gates:** G1 flag (newest funding date in data is 388 days old) · G2 pass (one exact match) · G3 pass (104 approvals) · G4 pass (1 of 2 matched titles not senior-flagged) · G5 pass (224 days, placeholder) · G6 `active` · G7 7/7 grounded, human reading of `seniority` quote required · G8 **not cleared** (no named human). No score emitted.
- **result:** needs-human. Machine evidence: sponsor record present, posting live. Human reading of one quote shows the role is not entry-level.
- **new code (contrib):** `scripts/contrib/2026fa/anishagaikar0420-jobpost-triage/` — `sponsor-triage.py`, `ground-fields.py`, `ground-fields.test.py` (10/10; a mutant that disables the quote check fails 1/10).
- **open issues / defects logged:**
  1. `npm run ats:scan -- --dry-run` fails: `portals.yml not found`.
  2. `npm run bls:local-wage` cannot run: `data/bls/local-wage/` absent from the clone; `python3 -m venv` fails at `ensurepip` on Homebrew Python 3.14.
  3. `node scripts/pii-scan.mjs` reports 1 finding in `package-lock.json`: an npm package maintainer's email in package metadata (tracked since the Fall 2026 fresh cut; not changed by this work; email not repeated here).
  4. `DOMAIN.md` states 42 recipes; `npm run doctor` counts 33.
  5. No tier→probability mapping exists, so `role-scorer.mjs` cannot be fed an honest sponsorship `p` (recipe TODO 1).
  6. Skill-demand counted "agentic" in 61 of 76 postings; 56 vanish if one company boilerplate sentence is removed (recipe TODO 4).
  7. Posting text was fetched with an ad hoc `curl`, not a stored ingest script.
