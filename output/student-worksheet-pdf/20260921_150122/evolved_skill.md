---
name: student-worksheet-pdf
description: Generate printable ESL/IELTS worksheets as PDFs.
---

# Student Worksheet / Handout PDF Generator

## Class of Work

Printable ESL/IELTS teaching materials for student use, including:

- Sentence drills and transformation exercises
- Vocabulary practice sheets
- Grammar worksheets and pattern exercises
- Cloze tests and gap-fills
- Listening transcripts and dictation materials

**Output format:** Always a PDF. The teacher prints and distributes to students.

**Typical layout:** Multi-version designs (Version A vs. Version B side by side) are common for differentiated instruction.

---

## Hard Rules — Non-Negotiable

**Never include identifying information or framing language.**

- No student names, teacher names, or school references
- No titles like "For [Name]'s Recovery," "Your Attention," or "Dopamine Detox Sheet"
- No text that singles out the student or implies a problem

**If the worksheet has a heading at all, use only a neutral, generic description:**

- ✅ "6-Word Sentence Worksheet"
- ✅ "Past Simple Drill"
- ❌ "For Sarah's Grammar Recovery"

**Why:** The worksheet gets handed directly to the student. Anything that reads as "we know what's wrong with you" creates resistance before they start. Keep materials professional and generic — any student could pick it up and use it.

---

## Layout Patterns

### Pattern 1: Side-by-Side Dual-Version (Single PDF)

Use for presenting two difficulty levels or answer/key on one page.

**Specifications:**

| Property | Value |
|----------|-------|
| Page size | A4 portrait |
| Columns | 2 (left = Version A, right = Version B) |
| Body font | 12.5pt |
| Entries per page | 5 |
| Writing lines per entry | 2 |
| Writing line width | ~58 chars (left column), ~52 chars (right column) |
| Header row | Cream tint (left), blue tint (right) |

**Version A:** Plain format — sentence prompt only
**Version B:** Enhanced format — color-coded elements, checklist, additional scaffolding

---

### Pattern 2: Separate-PDF Dual-Version

Use when the user wants smaller individual files or plans to distribute versions separately.

**Structure:**

1. **Version A PDF**
   - Single column, plain format
   - Version A legend + tense reference on page 1

2. **Version B PDF**
   - Single column, color-coded format
   - Same legend + tense reference on page 1

**Density options:**

| Format | Sentences per page |
|--------|-------------------|
| With writing lines | 7 |
| With short lines | 10 |
| With blank writing zone | 28 |

> **Tip:** Blank writing zone dimensions should match sentence dimensions for visual consistency.

---

### Pattern 3: Single-Version with Answer Space

Use for standard practice worksheets where students write their answers below the prompt.

**Structure:**

- Sentence prompt at top
- Blank writing zone below sized to match the sentence

**Implementation — use `BlankSpace` flowable, not underscores:**

python
class BlankSpace(Flowable):
    def __init__(self, width, height):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        pass  # Pure white space
**Sizing guidance:**

- Sentence text: 10pt, leading = 12pt → approximately 0.42cm tall
- BlankSpace sizing example: `BlankSpace(width=8.5*cm, height=0.5*cm)`

**Why not underscores?** Underscore characters render short and pale when wrapped in a Paragraph. `BlankSpace` produces a proper full-width writing area that renders cleanly.

---

## Quick Reference

| Scenario | Recommended Pattern |
|----------|---------------------|
| Differentiated instruction (same class, two levels) | Pattern 1 or 2 |
| Small file size required | Pattern 2 (separate PDFs) |
| Standard practice / homework | Pattern 3 |
| Answer key + student version combined | Pattern 1 |