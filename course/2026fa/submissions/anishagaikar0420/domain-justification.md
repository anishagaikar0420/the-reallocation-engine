# Domain justification — junior AI / prompt-engineer sponsor triage

## Executive summary

This page explains who the mode is for and why it exists. The person is an international master's student aiming for a junior AI or prompt-engineering job, with a work-authorization clock running. Their problem is not effort but missing information: they cannot easily see a company's sponsorship history, whether a posting is still open, or whether a "junior-sounding" job really is one. The mode makes those visible from stored data and tested scripts, and names the two ways it is most likely to mislead a newcomer.

## Who, and in what exact situation

An international master's student (F-1, on or approaching OPT) targeting **junior AI engineer / prompt engineer / LLM-application roles** at startups and mid-size tech companies. They have time for a limited number of tailored applications before their authorization window closes, and they are about to spend one on a *specific* company and posting. (The OPT end date is an input the student supplies; the mode refuses to run without it, and the worked run uses a labelled placeholder.)

## The information asymmetry

Employers and recruiters know whether the company sponsors, whether the requisition is real, and what "II" means in their own ladder. The student sees only a title and a paragraph. Without this mode they cannot easily see:

1. **Sponsorship evidence for their kind of work.** Of 30,369 companies in the dataset, only 1,557 have any approval count; 159 of those list a role-keyword title (ML, data scientist, AI engineer, applied scientist, prompt, NLP, LLM) among their top sponsored titles, and only 104 have one that is not senior-flagged (counted with the mode's own keywords). Most "AI startups" have no record at all, and no record is not a "no".
2. **Whether the posting is real and open.** A page can look fine and be dead; the liveness gate says so.
3. **What a posting actually requires.** Titles mislead; quotes don't.

## Engine layers used

- **80 Days to Stay:** `mapped_student_employment_targets_v3.csv` for sponsorship and funding signals (G1–G4).
- **Job-Ops:** `ats:liveness` for the liveness gate; new `ground-fields.py` for quote-grounded posting facts (G6–G7).
- **Cognitive Pivot:** `skill-demand` with the AI-engineering taxonomy to see which skills a company's postings mention. The BLS role-quality weight is 0.0 in the scorer and is deliberately not used.

## Failure modes specific to this domain

**1. The junior-sounding senior role.** *Shape:* a title with a low-level marker ("II", "Associate", "Analyst") over requirements that are not entry-level. *Real instance:* a US "Data Scientist II" at a Series C health-tech firm requiring a master's degree **plus 36 months of experience**; its sponsorship record is real and the posting is live, so every gate passes while the role is out of reach for a new graduate. *Hardest to catch for:* a student new to US job ladders, who has no prior for what "II" implies and no recruiter to ask. The quote check does not catch it either (the quote exists); it is surfaced only because a human reads the `seniority` quote. This is why TODO 5 proposes a seniority gate.

**2. Boilerplate-inflated AI demand.** *Shape:* a skill counter reports a correct count of a meaningless signal. *Real instance:* on one company's board, "Agentic / AI agents" appears in 61 of 76 postings (80%), including claims auditors and sales roles. 56 of those 61 vanish when one sentence of the company's "About" paragraph ("agentic AI-powered solutions") is removed; only 5 postings, all senior, staff or AI-engineer roles, truly mention agents. The count reconciles exactly with an independent regex count, so nothing looks wrong. *Hardest to catch for:* a career-changer into AI, who has no baseline for what real AI requirements look like and would reasonably study "agents" first.

## Boundary (one line)

The mode can say what the stored data and a live page say. It cannot say the company will sponsor *you*, and it does not touch immigration rules; those belong to the student's international-student office or an attorney.

## Lineage from my pitch (JobPost Contracts)

My pitch proposed a small library of prompt contracts that turns a job posting into a summary where every field carries a quote from the posting, plus five deliberately tricky test postings. This mode keeps that core as `ground-fields.py` and the tricky-posting tests, and adds the engine's sponsorship, liveness and timeline gates around it. Honest deviations from the pitch: (1) the pitch put real postings out of scope; the worked run uses one real public posting (not committed) because the assignment requires real data, and the tricky cases stay synthetic; (2) the pitch had five fields, the script checks seven; (3) the pitch said no career advice or ranking, and the mode keeps that: it refuses to emit a score; (4) the pitch's contracts were prompts, but here the checks are plain scripts and the model only drafts the extraction.
