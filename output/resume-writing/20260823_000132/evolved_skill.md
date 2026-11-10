---
name: resume-writing
description: Use when writing or tailoring an ATS-optimized resume.
---

# Resume Writing

Class-level skill for producing ATS-optimized, recruiter-scan-friendly resumes. Trigger when the user asks to write, review, rebuild, or tailor a resume.

## Playbook Location

Reference materials live at `/home/Hermes/research/resume_scale/`. Check for:

| File | Purpose |
|------|---------|
| `RESUME_SCALE.md` | Formatting rules, ATS standards, section order, eye-tracking data |
| `KEYWORD_BANK.md` | Action verbs, hard/soft skills by industry, buzzword blacklist |
| `TAILOR_WORKFLOW.md` | 5-minute and 30-minute per-job adaptation loops |

**If playbook files are missing:** Fall back to the rules in this SKILL.md, but warn the user that the playbook is unavailable.

---

## Workflow (Run in Order)

### 1. Read the Playbook First

Do not skip or skim. The playbook contains:

- 2026 ATS rules (1-page for <10 years experience)
- Typography specs: Calibri 11pt, 1" margins, single-column
- XYZ bullet format guidelines
- Mirror-job-description keyword injection rules

### 2. Gather Subject Facts

Collect for each role:

- **Company name, title, dates, location**
- **4–8 raw achievement notes** (don't editorialize yet)
- **Education** with graduation dates
- **Skills list**
- **Projects** with tech stacks

> **Critical:** Do NOT invent metrics, record counts, latency numbers, or scope figures. Use only what the subject provides.

### 3. Draft at Over-Density

First pass typically lands at 1,000–1,100 words (~1.5 pages). This gives you material to cut.

### 4. Tighten to Single-Page Density

**Target:** 650–750 words rendering to **one Letter page (8.5" × 11")** with:
- Margins: 0.4"–0.5"
- Font: Calibri 9.5–10pt
- Line height: 1.2

**Verification:** Run `pdfinfo` and confirm `Pages: 1` before delivery.

**Condensation tactics:**

| Situation | Action |
|-----------|--------|
| Projects exceeding 4–5 entries | Keep top 4–5 with 1 bullet each; mention remainder in a single secondary bullet |
| Concurrent part-time roles | Merge into one block |
| Older roles | Trim to 2–3 bullets |
| New grad with heavy project portfolio | 1 bullet per role; 1 paragraph per project (no multi-bullet) |

> **Principle:** Dense single-page beats thorough multi-page. Recruiters spend 6–7 seconds on first scan.

### 5. Write the NOTES File

Create `NOTES.md` using the structure in `references/notes-template.md`.

This is the primary iteration artifact. The user reviews and approves here before final rendering.

### 6. Verify ATS Parseability

Before sending, confirm:

- ✅ Single-column layout (no multi-column regions)
- ✅ No tables, text boxes, or graphic elements
- ✅ Standard section headers (Experience, Education, Skills)
- ✅ Consistent date format: `Mon YYYY – Mon YYYY`
- ✅ Zero blacklisted buzzwords (see `KEYWORD_BANK.md` §7)

---

## Hard Rules

1. **Never fabricate data.** Metrics and numbers must come from the subject.
2. **Mirror keywords.** Inject job-description language naturally into bullets.
3. **One page maximum** for candidates under 10 years experience.
4. **Verify before sending.** `pdfinfo` must report `Pages: 1`.
5. **NOTES precedes final output.** User approval happens in the iteration file.

---

## Output Sequence

1. Playbook review (silent step)
2. Fact-gathering questions (if data incomplete)
3. Draft → NOTES file → user review
4. User-approved edits → final PDF
5. Delivery confirmation