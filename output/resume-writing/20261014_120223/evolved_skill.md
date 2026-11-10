---
name: resume-writing
description: Use when writing or tailoring an ATS-optimized resume.
---

# Resume Writing

Class-level skill for producing ATS-optimized, recruiter-scan-friendly resumes. Trigger when the user asks to write, review, rebuild, or tailor a resume — especially for Abhinav, whose reference playbook lives at `/home/Hermes/research/resume_scale/`.

## Workflow (always run in this order)

### 1. Locate the Playbook

Check `/home/Hermes/research/resume_scale/` for the following files:

| File | Purpose |
|------|---------|
| `RESUME_SCALE.md` | Formatting decisions, ATS rules, section order, eye-tracking data |
| `KEYWORD_BANK.md` | Action verbs, hard/soft skills by industry, buzzword blacklist |
| `TAILOR_WORKFLOW.md` | 5-min and 30-min per-job adaptation loop |

**Fallback:** If any playbook file is missing, fall back to the universal rules in this SKILL.md and warn the user that the playbook is incomplete.

### 2. Read the Playbook Fully Before Drafting

Do not skim. Key 2026 ATS rules that come from the playbook:

- **Length:** 1 page for candidates with <10 years of experience
- **Font:** Calibri 11pt
- **Margins:** 1" all sides
- **Layout:** Single-column only
- **Bullets:** XYZ format (Action verb + Task + Outcome/Metric)
- **Keywords:** Mirror job description language

### 3. Gather the Subject's Facts

Collect the following information **before writing anything**:

**Per Role:**
- Company name
- Title/position
- Dates (start month/year – end month/year or "Present")
- Location (City, State)
- 4–8 raw achievement notes (what they did, not how they did it)

**Additional Sections:**
- Education entries with graduation dates
- Skills list (technical + soft)
- Projects with tech stacks

> ⚠️ **Critical:** Do NOT invent metrics, record counts, latency numbers, or scope numbers. Only use what the subject explicitly provides.

### 4. Draft at Slightly Over-Density

Initial drafts typically land at **1,000–1,100 words**. This will render to approximately 1.5 pages.

### 5. Tighten to 1-Page Density

**Target:** ~650–750 words of dense content rendering to a **single page on Letter (8.5" × 11")**.

**Final Formatting Specs:**
- Margins: 0.4"–0.5"
- Font: Calibri 9.5–10pt
- Line-height: 1.2

**Verification:** Run `pdfinfo` and confirm `Pages: 1` before sending.

**Tightening Tactics:**
- Cap projects at 4–5 entries with 1 bullet each
- Drop secondary projects to mentions in a single bullet
- Merge concurrent part-time roles into one block
- Condense older roles to 2–3 bullets

**For New Grads with Deep Project Portfolios:**
- 1 bullet per role (not 2–3)
- 1 paragraph per project (not multi-bullet)
- Dense single-page wins over thorough multi-page

### 6. Write the NOTES File

Use the structure in `references/notes-template.md`. This is the **most important deliverable** — it's where iteration happens.

### 7. Verify ATS Parseability

Before finalizing, confirm:

- [ ] Single column layout
- [ ] No tables
- [ ] No text boxes or graphic elements
- [ ] Standard section headers (Experience, Education, Skills, Projects)
- [ ] Consistent date format: `Mon YYYY – Mon YYYY` (e.g., `Jan 2020 – Dec 2022`)
- [ ] No blacklisted buzzwords (see playbook `KEYWORD_BANK.md` §7)

## Hard Rules (Learned from ATS Failures)

1. **Never use columns** — ATS scanners read left-to-right; multi-column layouts split or drop content
2. **Never use headers/footers** — critical info gets lost in parsing
3. **Never use special characters** — use `&` not `and`, `%` not "percent", etc.
4. **Match job description keywords exactly** — "Python" ≠ "python" ≠ "Python programming"
5. **No images, icons, or graphics** — ATS cannot read them
6. **File format:** Submit as `.docx` when possible; `.pdf` second choice; never `.pages`
7. **Name your file correctly:** `FirstName_LastName_Resume.pdf`

## Output Files

Produce two files for each resume engagement:

1. **`<Name>_Resume.pdf`** — The formatted resume
2. **`<Name>_Resume_NOTES.md`** — The iteration document with:
   - Original facts gathered
   - Decisions made and why
   - Areas flagged for subject confirmation
   - Customization notes for each target role