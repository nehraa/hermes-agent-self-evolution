---
name: resume-writing
description: Use when writing or tailoring an ATS-optimized resume.
---

# Resume Writing

Class-level skill for producing ATS-optimized, recruiter-scan-friendly resumes. Trigger when the user asks to write, review, rebuild, or tailor a resume — especially for Abhinav, whose reference playbook lives at `/home/Hermes/research/resume_scale/`.

## Workflow (always run in this order)

### 1. Locate the Playbook

Check `/home/Hermes/research/resume_scale/` for these files:

| File | Purpose |
|------|---------|
| `RESUME_SCALE.md` | Formatting decisions, ATS rules, section order, eye-tracking data |
| `KEYWORD_BANK.md` | Action verbs, hard/soft skills by industry, buzzword blacklist |
| `TAILOR_WORKFLOW.md` | 5-min and 30-min per-job adaptation loop |

If any file is missing, fall back to the universal rules in this SKILL.md and warn the user that the playbook is incomplete.

### 2. Read the Playbook Fully Before Drafting

Don't skim. The current ATS rules include:

- **Length:** 1 page for candidates with <10 years experience
- **Font:** Calibri 11pt
- **Margins:** 1" all sides
- **Layout:** Single-column only
- **Bullets:** XYZ format (Action verb + metric + outcome)
- **Keywords:** Mirror job description terminology

### 3. Gather the Subject's Facts

Collect the following data **before writing any content**:

- **Per role:** Company name, title, dates (MM/YYYY format), location, 4–8 raw achievement notes
- **Education:** Institution, degree, graduation date, notable coursework/GPA (if impressive)
- **Skills:** Technical and soft skills relevant to target roles
- **Projects:** Name, tech stack, 1-2 sentence description

> **Critical:** Do NOT invent metrics, record counts, latency numbers, or scope numbers. Use only what the subject explicitly provides.

### 4. Draft at Slightly Over-Density

Write an initial draft without worrying about length. Expect to land at **1,000–1,100 words** — this typically renders to ~1.5 pages and gives you material to cut from.

### 5. Tighten to One-Page Density

**Target specification:**

| Parameter | Value |
|-----------|-------|
| Word count | 650–750 words of content |
| Page count | 1 page on Letter (8.5" × 11") |
| Margins | 0.4"–0.5" all sides |
| Font | Calibri 9.5–10pt |
| Line height | 1.2 |

**Verify with `pdfinfo` showing `Pages: 1` before sending.**

**Tightening tactics:**

- Cap projects at 4–5 entries with 1 bullet each
- Move secondary projects to a single bullet mention in Summary
- Merge concurrent or part-time roles into one block
- Condense older roles to 2–3 bullets

**For new grads with deep project portfolios:**

- Use 1 bullet per role (not 2–3)
- Use 1 paragraph per project (not multi-bullet)
- Dense single-page wins over thorough multi-page

### 6. Write the NOTES File

Use the structure from `references/notes-template.md`. This is the primary deliverable for iteration — all user feedback should be captured here first before modifying the resume.

### 7. Verify ATS Parseability

Run these checks before finalizing:

- [ ] Single-column layout only
- [ ] No tables, text boxes, or graphics
- [ ] Standard section headers (Experience, Education, Skills, Projects)
- [ ] Consistent date format: `Mon YYYY – Mon YYYY` (e.g., `Jan 2020 – Mar 2023`)
- [ ] No blacklisted buzzwords (see `KEYWORD_BANK.md` §7)

## Hard Rules

These rules are non-negotiable:

1. **Never fabricate metrics** — if the subject doesn't provide numbers, describe impact qualitatively
2. **Never exceed one page** for <10 years experience unless explicitly requested
3. **Always verify PDF output** — `pdfinfo` must show `Pages: 1`
4. **Mirror job description keywords** — ATS scans for exact phrase matches
5. **Exclude blacklisted terms** — see playbook for current list

## Section Order (Standard)

1. Summary (3–4 lines, targeted to role)
2. Experience (reverse chronological)
3. Education
4. Projects
5. Skills
Move or omit sections based on relevance to the target role. A senior IC may omit Education; a new grad may emphasize Projects over Experience.

## Exit Criteria

A resume is ready when:

- [ ] `pdfinfo` confirms 1 page
- [ ] All experience entries have 2–3 bullets (or 1 for new grads)
- [ ] Keywords match target job description
- [ ] No blacklisted terms present
- [ ] NOTES file created with user feedback captured