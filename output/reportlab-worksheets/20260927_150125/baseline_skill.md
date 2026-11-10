---
name: reportlab-worksheets
description: A4 worksheets and writing-line handouts via reportlab
version: 1.0.0
tags: [PDF, reportlab, worksheets, education]
metadata:
  hermes:
    category: productivity
    related_skills: [pdf, ocr-and-documents]
---

# Reportlab Worksheets

Generate A4 PDFs with mixed text + color + interactive zones (handwriting lines, checkboxes, blank areas). Captures the patterns proven by building 100-sentence grammar worksheets, rapid-fire oral prompt sheets, and dense study handouts.

## When to use

- A user wants a printable handout (worksheet, study sheet, practice exercise)
- Color-coded content where each word or section has its own role indicator
- Need handwriting zones, checkboxes, or other non-text interactive elements
- Want a clean two-column dense layout on A4
- Need TENSE indicators, question prompts, or numbered items

NOT for: standard text reports, OCR scans, fillable AcroForm PDFs (use `pdf` skill instead), heavy visual layouts with images and animation.

## Core architecture

```python
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus.flowables import HRFlowable, Flowable

# 1. Tight A4 margins for maximum content
doc = SimpleDocTemplate(
    "out.pdf", pagesize=A4,
    leftMargin=0.8*cm, rightMargin=0.8*cm,
    topMargin=0.5*cm, bottomMargin=0.5*cm,
)
# 2. Custom Flowable for handwriting lines (NOT underscore strings)
# 3. Multi-column Table layout with [ [left_cells], [right_cells] ] row structure
# 4. Color spans via <font color="#HEX"><b>WORD</b></font> inside Paragraph
```

## Custom Flowables (essential)

**Underscore strings do not render as writing lines.** `Paragraph("_" * 50, ...)` produces tiny dashes that do not reach page edge and do not look like handwriting rules. Build a proper Flowable:

```python
class WriteLine(Flowable):
    """Full-width horizontal rule for handwriting."""
    def __init__(self, width=8*cm, thickness=0.6, color=HexColor("#9CA3AF")):
        Flowable.__init__(self)
        self.width = width
        self.thickness = thickness
        self.color = color
        self.height = thickness + 4
    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, self.thickness/2, self.width, self.thickness/2)
```

For a blank writing zone (no visible line, just whitespace):

```python
class BlankSpace(Flowable):
    def __init__(self, width, height):
        Flowable.__init__(self)
        self.width = width
        self.height = height
    def draw(self):
        pass  # pure white space
```

Use `BlankSpace` when the student should write freely without a baseline. Use `WriteLine` when they need a guided line.

## Color coding — word by word

Each word gets its own color via `<font>` tag inside a Paragraph:

```python
COLOR_SUBJ = "#1D4ED8"   # blue
COLOR_VERB = "#B91C1C"   # red
COLOR_OBJ  = "#15803D"   # green
COLOR_ART  = "#7C3AED"   # purple
COLOR_PREP = "#EA580C"   # orange
COLOR_ADV  = "#0891B2"   # cyan

def colorize_words(tagged_sentence):
    """tagged = [(word, tag), ...] → HTML with per-word color."""
    parts = []
    for word, tag in tagged_sentence:
        color = COLOR_MAP[tag]
        parts.append(f'<font color="{color}"><b>{word}</b></font>')
    return " ".join(parts)
```

The `<b>` tag keeps color saturated even when overlapping with other rendering. Plain `<font color=...>` may render washed out.

## Multi-column dense layout

For 14-28 items per page (worksheets, rapid-fire prompts):

```python
SENTENCES_PER_PAGE = 28
PER_COL = 14  # split left/right
COL_W = 9.0   # cm each column

for batch_start in range(0, total, SENTENCES_PER_PAGE):
    batch = items[batch_start:batch_start+SENTENCES_PER_PAGE]
    left_cells = [build_cell(batch_start + i + 1, batch[i]) for i in range(PER_COL)]
    right_cells = [build_cell(batch_start + PER_COL + i + 1, batch[PER_COL+i]) for i in range(PER_COL - (len(batch) - PER_COL))]

    tbl = Table([[left_cells[i], right_cells[i]] for i in range(max(len(left_cells), len(right_cells)))],
                colWidths=[COL_W*cm, COL_W*cm])
    tbl.setStyle(TableStyle([
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('BACKGROUND',(0,0),(0,-1),HexColor("#FFFFFF")),
        ('BACKGROUND',(1,0),(1,-1),HexColor("#FAFAFA")),  # subtle stripe
        ('LINEAFTER',(0,0),(0,-1),0.5,HexColor("#D1D5DB")),  # column divider
        ('TOPPADDING',(0,0),(-1,-1),2),
        ('BOTTOMPADDING',(0,0),(-1,-1),2),
    ]))
    story.append(tbl)
    story.append(PageBreak())
```

Density tuning rules of thumb (A4, margins 0.8cm/0.5cm):
- 5 items/page, full width, 2-line writing zone → ~20 pages for 100 items
- 7 items/page, 2 columns, single line → ~15 pages
- 14 items/page, 2 columns, single line → ~7-8 pages
- 28 items/page, 2 columns, single tight line → ~4 pages

Test render and adjust font/padding iteratively. Do not guess density from code alone.

## Compact legend bar

For color-coded content, add a 1-row legend at the top of page 1:

```python
legend_tbl = Table([[
    Paragraph(f'<font color="{COLOR_SUBJ}"><b>SUBJECT</b></font>', s_legend),
    Paragraph(f'<font color="{COLOR_VERB}"><b>VERB</b></font>', s_legend),
    # ... one cell per color
]], colWidths=[3.0*cm, 2.5*cm, 3.0*cm, 3.0*cm, 2.5*cm, 2.5*cm])
legend_tbl.setStyle(TableStyle([
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('BACKGROUND',(0,0),(-1,-1),HexColor("#F9FAFB")),
    ('BOX',(0,0),(-1,-1),0.8,ACCENT),
    ('TOPPADDING',(0,0),(-1,-1),4),
    ('BOTTOMPADDING',(0,0),(-1,-1),4),
    ('ALIGN',(0,0),(-1,-1),'CENTER'),
]))
story.append(legend_tbl)
story.append(Spacer(1, 0.08*cm))
```

## Checkbox rendering

ZapfDingbats `☐` and Wingdings symbols render as solid black boxes in default Helvetica. Use ASCII instead:

```python
# WRONG — renders as solid black square
TENSE_STR = '<font name="ZapfDingbats">☐</font> Present Simple'

# RIGHT — readable across all platforms
TENSE_STR = '<font color="#6B7280">[ ]</font> Present Simple'
```

For 6 or more checkboxes in a row, separate with `&nbsp;&nbsp;` (two non-breaking spaces) to prevent wrapping.

## Pagination pitfalls

- `PageBreak()` inside a flow that is being kept-together can orphan content. Test rendering before assuming layout.
- Table cells that exceed column width auto-wrap, breaking layouts that expect single-line items. Use `Paragraph` for all cell content (auto-wraps) instead of `String` or `Text`.
- When using `KeepTogether`, the whole block jumps to next page if it does not fit. Fine for short blocks, catastrophic for long tables.

## Verification — word by word

**Critical: never ship a worksheet without visual verification.** The single biggest failure mode is auto-taggers (POS taggers, classifiers) misclassifying words — a verb becomes an object, an adjective becomes an adverb. The user catches this in 3 seconds. You should catch it first.

Workflow before declaring done:

```bash
# 1. Convert to images
python3 -c "from pdf2image import convert_from_path; \
  [im.save(f'/tmp/page_{i+1}.png') for i, im in enumerate(convert_from_path('out.pdf', dpi=120))]"

# 2. Visually inspect each page with vision_analyze
question: "For EVERY word on this page, verify the color coding is correct.
Report any word that looks wrong (e.g., a verb in green, an adjective in cyan,
a word in black when it should be colored)."
```

Sample checklist prompts:
- "Look at every single word on this page. Is the subject blue and verb red in every sentence?"
- "Spot check sentence #N — does it have all expected color components?"
- "Any word appearing in black when it should be colored?"

If you find a wrong word, fix the auto-tag logic and re-render. Iterate until clean. The user is paying attention to every word — you should too.

## Common errors in word-tagging heuristics

When building a grammar tagger for English sentences:

- **Adjective before noun** ("heavy door", "red ball") → must tag as OBJ (or merge with noun), not ADV
- **Time adverbs** ("yesterday", "tomorrow", "daily", "always") → ADV when modifying verb
- **Adjective-as-adverb** ("daily life" = adjective modifying noun, OBJ; "arrives daily" = adverb, ADV)
- **Auxiliary + main verb** ("will travel", "is studying") → both VERB (not OBJ for main)
- **Possessives** ("my", "your", "his") → OBJ when in object position
- **"every", "many", "more", "several"** before noun → OBJ (determiner), not ADV
- **"home", "nearby", "outside", "today"** at end of sentence → ADV (adverb of place/time), not OBJ

Hand-tag 5-10 sentences first to validate your heuristic. Tag a noun ending in -s as plural noun (S or OBJ), not verb (V), unless context confirms verb form.

## Pitfalls (recurring)

- **Auto-tagging heuristics fail on edge cases.** Adverbs ("forever"), adjectives merged with objects ("heavy door"), possessives, compound verbs ("helps overcome") all require context. Hand-validate on a 10-sentence sample before shipping 100.
- **Off-by-one in tag-array indexing** when applying manual corrections. If your tags are 0-indexed but you think of sentence numbers 1-indexed, you can overwrite the wrong sentence with the wrong tags. Always verify after manual edits: print the saved tags and confirm the sentence text matches.
- **`Paragraph("_"*N)` is not a writing line.** Use the custom `WriteLine` Flowable above.
- **ZapfDingbats `☐` renders as solid box.** Use ASCII `[ ]`.
- **Multi-page table overflow** if a row is taller than half the page. Cap row height by trimming the per-cell content (fewer checkboxes, shorter writing line, smaller font).
- **Color contrast too low.** Always use `<b>` (bold) inside the `<font color>` tag to keep colors saturated.
