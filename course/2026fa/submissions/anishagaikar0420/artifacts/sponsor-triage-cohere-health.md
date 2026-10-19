## Executive summary

This report checks whether **Cohere Health** is worth an application using only the committed sponsorship dataset. It found a record (104.0 approvals, last funding Series C on 2025-05-07). 1 gate(s) raised a flag that a human must read before acting. It deliberately gives no score.

## Gates

| Gate | Status | Detail |
|---|---|---|
| G1 snapshot-age | flag | newest funding date in data is 2025-09-26; 388 days before 2026-10-19. 'Recent' here means recent as of the snapshot, not today. |
| G2 company-match | pass | matched CSV line 6084: COHERE HEALTH INC |
| G3 sponsor-record | pass | 104 approvals on record |
| G4 role-family | pass | 2 sponsored title(s) match role keywords; 1 not senior-flagged |
| G5 timeline | pass | 224 days to opt_end (arithmetic only; no rule about cap-gap/STEM OPT is checked) |

## Record (source: CSV line 6084)

| Field | Value |
|---|---|
| csv_line | 6084 |
| company_name | COHERE HEALTH INC |
| state | MA |
| latest_funding_stage | Series C |
| latest_funding_date | 2025-05-07 |
| latest_funding_amount | 89999876.0 |
| total_approvals | 104.0 |
| total_denials | 2.0 |
| approval_rate | 98.1132075471698 |
| median_salary_offered_all_sponsored_titles | 160000.0 |
| top_job_titles_sponsored | ['Engineering Manager', 'Senior Software Engineer, Platform', 'Senior Machine Learning DevOps Engineer', 'Software Engineer II', 'Machine Learning Engineer'] |
| role_family_matched_titles | ['Senior Machine Learning DevOps Engineer', 'Machine Learning Engineer'] |
| role_family_non_senior_titles | ['Machine Learning Engineer'] |

## Run record

- run_date: 2026-10-19
- csv: data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv (30369 rows)
