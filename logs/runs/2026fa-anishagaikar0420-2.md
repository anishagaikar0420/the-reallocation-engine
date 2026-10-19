## Executive summary

A follow-up to the first run: the one trap that the checklist could only catch by a person reading (a "junior-sounding" job that requires 36 months of experience) is now caught by a small script. It was run on the same real posting and flagged it, with the quote shown. Nothing here is personal data.

## Run record

- **date:** 2026-10-19 · **recipe:** `recipes/cases/2026fa/anishagaikar0420-junior-ai-engineer-sponsor-triage.md` v0.2.0 · status stays **RUNNABLE-SAMPLE** · attestation: none (unsigned)
- **inputs:** the live "Data Scientist II" posting (public Greenhouse API, fetched once, not committed); default 24-month ceiling and a 36-month override.
- **commands:** `seniority-gate.test.py` (9/9); `seniority-gate.py <posting>` (exit 1, largest_min=36mo); empty-file break (exit 2); `--max-months 36` (exit 0); `npm run verify`; `npm run doctor`.
- **outputs:** `course/2026fa/submissions/anishagaikar0420/worked-run.md` §7.
- **result:** TODO 5 (DEV) closed with evidence; G4b added. Role decision still needs-human.
- **open issues:** posting still fetched by ad hoc `curl`; ceiling of 24 months is an authorial choice; known boilerplate false-flag; `ats:scan` and `bls:local-wage` still not run; no named human has cleared any gate.
- **addendum:** added five synthetic tricky-posting fixtures + `tricky-postings.test.py` (6/6; mutation check made it fail 2, restored 6/6) and a pitch-lineage section (worked-run §8).
