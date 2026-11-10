---
name: resume-writing
description: Use when writing or tailoring an ATS-optimized resume.
---

# Resume Writing

Class-level skill for producing ATS-optimized, recruiter-scan-friendly resumes. Trigger when the user asks to write, review, rebuild, or tailor a resume — especially for Abhinav, whose reference playbook lives at `/home/Hermes/research/resume_scale/`.

## Workflow

Run these steps **in order**. Do not skip steps 1-2 even for "quick" edits.

### Step 1: Locate and Read the Playbook

Check `/home/Hermes/research/resume_scale/` for these files:

| File | Purpose |
|------|---------|
| `RESUME_SCALE.md` | Formatting rules, ATS guidelines, section order, eye-tracking data |
| `KEYWORD_BANK.md` | Action verbs, hard/soft skills by industry, buzzword blacklist |
| `TAILOR_WORKFLOW.md` | 5-min and 30-min per-job adaptation loops |

**If files are missing:** Fall back to the universal rules in this SKILL.md. Warn the user that the playbook is missing and note any deviations from their typical format.

Read the playbook **fully** before drafting — do not skim. The 2026 ATS rules (Calibri 11pt, 1" margins, single-column, XYZ bullets, mirror JD keywords) all live there.

### Step 2: Gather Facts from the Subject

Collect **raw, unedited** information for each section:

- **Work history:** Company, title, dates, location, 4–8 raw achievement notes per role
- **Education:** Institution, degree, field, graduation date
- **Skills:** Technical and soft skills as provided
- **Projects:** Name, tech stack, your role, outcomes (if any)

**Critical rule:** Do NOT invent metrics, record counts, latency numbers, or scope numbers. Use only what the subject provides or can verify.

### Step 3: Draft at Over-Density

Write the initial draft with full content density. Expect to land at **1,000–1,100 words**. This will render to approximately 1.5 pages — the raw material for tightening.

### Step 4: Tighten to Single-Page Density

Target **650–750 words of dense content** rendering to a **single page on Letter (8.5" × 11")**.

**Target formatting:**
- Margins: 0.4" – 0.5"
- Font: Calibri, 9.5 – 10pt
- Line-height: 1.2

**Verification:** Run `pdfinfo` on the output. Confirm `Pages: 1` before sending.

**Tightening tactics:**
| Situation | Action |
|-----------|--------|
| Too many projects | Cap at 4–5 entries with 1 bullet each; move secondary projects to a single mention |
| Concurrent part-time roles | Merge into one block |
| Older roles | Condense to 2–3 bullets each |
| New grad with deep project portfolio | 1 bullet per role, 1 paragraph per project — single page beats thorough multi-page |

### Step 5: Write the NOTES File

Create `NOTES.md` using the structure in `references/notes-template.md`.

**This is the primary deliverable for iteration.** It should contain:
- The raw facts collected in Step 2
- Your reasoning for structural decisions
- Open questions for the subject
- Tailoring notes for specific jobs (if applicable)

### Step 6: Verify ATS Parseability

Before finalizing, confirm the resume passes these checks:

- [ ] Single column layout
- [ ] No tables, text boxes, or graphics
- [ ] Standard section headers (Experience, Education, Skills, Projects)
- [ ] Consistent date format: `Mon YYYY – Mon YYYY` (e.g., `Jan 2020 – Mar 2023`)
- [ ] No blacklisted buzzwords (see `KEYWORD_BANK.md` §7)
- [ ] Keywords mirror the target job description (JD)

## Hard Rules

1. **Never fabricate data.** If metrics are missing, write the achievement qualitatively and flag it for the subject to quantify later.

2. **One page is not a suggestion.** Recruiters spend 6–7 seconds on initial scans. A two-page resume for <10 years experience signals poor prioritization.

3. **Mirror the JD.** Every resume is a targeted document. Extract keywords from the job description and weave them naturally into bullets and skills.

4. **XYZ bullets over task lists.** Structure each bullet as:
   - **X** (what you did)
   - **Y** (how you did it / method)
   - **Z** (result, metric, or impact)

   Avoid starting bullets with "Responsible for," "Assisted with," or "Helped with."

5. **No headers or footers.** ATS systems often strip them. Keep all content in the body.

6. **Plain text filenames.** When saving: `FirstName_LastName_Resume.pdf`, not `Abhinav's Resume FINAL v3.pdf`.

## Quick Tailoring (5-Minute Per Job)

For rapid applications, follow `TAILOR_WORKFLOW.md`:
1. Pull the top 5 keywords from the JD
2. Reorder bullets to surface matching achievements first
3. Swap in 2–3 JD keywords into existing bullets
4. Adjust the skills section to include JD terms

## Common Pitfalls to Avoid

| Mistake | Why It Fails |
|---------|--------------|
| Multi-column layouts | ATS cannot parse columns correctly |
| Creative section names ("My Story") | Keywords get missed |
| Personal information (photo, DOB, nationality) | Risk of discrimination; wastes space |
| Generic objective statements | Recruiters ignore them |
| Passive language | Undermines your impact |

---

**Last updated:** Per playbook at `/home/Hermes/research/resume_scale/`