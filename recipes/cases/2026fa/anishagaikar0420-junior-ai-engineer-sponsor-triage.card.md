# junior-ai-engineer-sponsor-triage — Human Card

*Read this before trusting a triage report. It is the human half of the recipe
`anishagaikar0420-junior-ai-engineer-sponsor-triage.md`.*

## Executive summary

This card explains, in plain language, what the triage checklist can and cannot tell you about one company and one job posting. It is for a student choosing where to spend a limited number of applications while their work authorization runs down. It found that the stored data can confirm a company's petition history and whether a posting page is still up, but it cannot tell you that the company will sponsor *you*, or that a job is really entry-level.

## Purpose

Before you apply, check one company and one posting against stored evidence: sponsorship history, role fit, posting liveness, whether each fact you believe about the posting is actually written in it, and days left on your timeline.

## What it can verify

- The company's row in the sponsorship dataset, quoted with its line number.
- How old the newest funding record in the dataset is (the data stops in 2025).
- Whether the posting URL still resolves.
- Whether each fact you extracted has a verbatim quote in the posting.

## What it cannot verify

- That the company will sponsor you for this job. A history of petitions is not a promise.
- Whether the sponsored work was entry-level; the dataset lists top titles only.
- Immigration rules (cap-gap, STEM OPT, lottery, cap-exempt status). Ask your school's international office.
- That a quote *supports* the claim attached to it. You read the `seniority` and `skills` quotes.
- That anyone is actually hiring for a live posting.

## Failure modes (named, with who is hurt)

1. **Title-level seniority.** "Data Scientist II" reads as junior. The posting required a master's degree plus 36 months of experience. A new graduate filtering on titles applies to a role they cannot meet and does not learn why. Hardest to catch for someone new to US job-title conventions.
2. **Boilerplate-inflated demand.** A one-sentence company description made "agentic AI" appear in 80% of one company's postings, including auditors and sales; 56 of the 61 hits disappear when that sentence is removed. The count is right; the meaning is wrong. Hardest to catch for a newcomer who has no baseline for what a real AI posting looks like.
3. **"No record" read as "no".** A blank approval count is absence of evidence. Startups that have never filed will look identical to ones that refuse to.

## Annotated commands

```bash
# 1. Local gates (no network). OPT date is required; the run refuses without it.
python3 scripts/contrib/2026fa/anishagaikar0420-jobpost-triage/sponsor-triage.py \
  --company "Cohere Health" --opt-end 2027-05-31 --json out.json --md out.md
# 2. Is the posting live? (exit code 1 if expired)
npm run ats:liveness -- https://job-boards.greenhouse.io/coherehealth/jobs/8005450003
# 3. Ground the facts you extracted (exit code 1 on any ungrounded field)
python3 scripts/contrib/2026fa/anishagaikar0420-jobpost-triage/ground-fields.py extraction.json
```

Exit codes: `sponsor-triage.py` 0 = ran (gates may be flagged), 2 = a gate stopped the run; `ground-fields.py` 0 = all grounded, 1 = any failure, 2 = bad input.

## Added in v0.2.0: seniority check

```bash
python3 scripts/contrib/2026fa/anishagaikar0420-jobpost-triage/seniority-gate.py posting.txt   # exit 0 pass · 1 flag/none (read the quote) · 2 bad input
```
It prints every "N years/months of experience" line it finds. A flag means the posting asks for more than 24 months: read the quote, and default to Skip.
