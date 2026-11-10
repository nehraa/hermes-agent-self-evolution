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

# ReportLab Worksheets

Generate printable A4 PDFs with mixed text, color-coded content, and interactive zones (handwriting lines, checkboxes, blank areas). Purpose-built for educational handouts, study sheets, and practice exercises.

Tested patterns from 100-sentence grammar worksheets, rapid-fire oral prompt sheets, and dense study handouts.

## When to Use This Skill

### Ideal For
- Printable handouts (worksheets, study sheets, practice exercises)
- Color-coded content where words/sections have distinct roles
- Handwriting zones with proper ruled lines (not underscore characters)
- Checkboxes, blank response areas, or other non-text interactive elements
- Dense two-column A4 layouts
- TENSE indicators, question prompts, or numbered items

### Not Suitable For
- Standard text reports or document generation
- OCR scans or document processing
- Fillable AcroForm PDFs (use `pdf` skill instead)
- Heavy visual layouts with images and animations

## Core Architecture

python
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus.flowables import HRFlowable, Flowable

# 1. Tight A4 margins for maximum content density
doc = SimpleDocTemplate(
    "output.pdf",
    pagesize=A4,
    leftMargin=0.8 * cm,
    rightMargin=0.8 * cm,
    topMargin=0.5 * cm,
    bottomMargin=0.5 * cm,
)

# 2. Build content with Paragraph, Table, and custom Flowables
# 3. Multi-column layout via Table with [[left_cell], [right_cell]] row structure
# 4. Color spans via <font color="#HEX"><b>TEXT</b></font> in Paragraph
## Custom Flowables

> **Important:** Never use underscore strings for writing lines. `Paragraph("_" * 50, ...)` produces tiny dashes that don't reach the page edge and look nothing like handwriting rules.

### Handwriting Line

python
class WriteLine(Flowable):
    """Full-width horizontal rule for handwriting zones."""
    
    def __init__(self, width=None, thickness=0.6, color=HexColor("#9CA3AF"), space_after=8):
        Flowable.__init__(self)
        self.width = width
        self.thickness = thickness
        self.color = color
        self.height = thickness + space_after
    
    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, self.thickness / 2, self.width, self.thickness / 2)
### Checkbox

python
class Checkbox(Flowable):
    """Interactive checkbox for worksheets."""
    
    def __init__(self, size=10, checked=False, color=HexColor("#374151")):
        Flowable.__init__(self)
        self.size = size
        self.checked = checked
        self.color = color
        self.width = size
        self.height = size
    
    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(1.2)
        self.canv.rect(0, 0, self.size, self.size)
        if self.checked:
            self.canv.setLineWidth(1.5)
            self.canv.line(1, self.size - 2, self.size / 3, 2)
            self.canv.line(self.size / 3, 2, self.size - 1, self.size - 1)
## Two-Column Layout Pattern

python
from reportlab.platypus import Table, TableStyle

# Create content lists for each column
left_content = [
    Paragraph("<b>Exercise 1</b>", heading_style),
    Paragraph("Complete the sentence:", body_style),
    WriteLine(width=7 * cm),
    WriteLine(width=7 * cm),
]

right_content = [
    Paragraph("<b>Exercise 2</b>", heading_style),
    Paragraph("Circle the correct answer:", body_style),
    Paragraph("A) option one", option_style),
    Paragraph("B) option two", option_style),
]

# Build two-column table
two_column_table = Table(
    [[left_content, right_content]],
    colWidths=[9.4 * cm, 9.4 * cm],
    hAlign='CENTER'
)

story = [two_column_table]
doc.build(story)
## Color Coding Pattern

Use inline font colors to distinguish grammatical elements:

python
# Define color palette
COLORS = {
    'verb': HexColor("#2563EB"),      # Blue - verbs
    'noun': HexColor("#16A34A"),       # Green - nouns
    'adjective': HexColor("#DC2626"),  # Red - adjectives
    'tense': HexColor("#9333EA"),      # Purple - tense markers
    'prompt': HexColor("#374151"),     # Gray - instructions
}

# Apply via Paragraph markup
def colored_word(word, color_key):
    return f'<font color="#{COLORS[color_key].hexval()[2:]}"><b>{word}</b></font>'

paragraph = Paragraph(
    f"She {colored_word('visit', 'verb')} the {colored_word('museum', 'noun')} yesterday.",
    body_style
)
## Common Use Cases

### Grammar Worksheet with Writing Lines

python
class GrammarWorksheetBuilder:
    def __init__(self, filename):
        self.doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            leftMargin=0.8 * cm,
            rightMargin=0.8 * cm,
            topMargin=0.5 * cm,
            bottomMargin=0.5 * cm,
        )
        self.story = []
        self.styles = getSampleStyleSheet()
    
    def add_title(self, title):
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            alignment=1,  # Center
            spaceAfter=12
        )
        self.story.append(Paragraph(title, title_style))
    
    def add_prompt_with_lines(self, prompt, num_lines=3):
        self.story.append(Paragraph(prompt, self.styles['BodyText']))
        for _ in range(num_lines):
            self.story.append(WriteLine(width=18 * cm))
            self.story.append(Spacer(1, 4))
    
    def build(self):
        self.doc.build(self.story)
### Numbered Exercise Grid

python
def create_exercise_grid(exercises, cols=2):
    """Create a grid of numbered exercises."""
    cells = []
    for i, exercise in enumerate(exercises, 1):
        cell_content = [
            Paragraph(f"<b>{i}.</b> {exercise['question']}", body_style),
            Spacer(1, 6),
        ]
        for _ in range(exercise.get('lines', 2)):
            cell_content.append(WriteLine(width=8 * cm))
            cell_content.append(Spacer(1, 4))
        cells.append(cell_content)
    
    # Pair items into rows
    rows = []
    for i in range(0, len(cells), cols):
        row = cells[i:i + cols]
        while len(row) < cols:
            row.append([Paragraph("", body_style)])  # Empty cell
        rows.append(row)
    
    return Table(rows, colWidths=[9.4 * cm] * cols)
## Best Practices

1. **Use proper Flowables** — Never substitute underscores or repeated characters for ruled lines
2. **Set margins early** — 0.8cm horizontal, 0.5cm vertical for dense A4 layouts
3. **Use Tables for columns** — Simple `[[col1], [col2]]` structure scales cleanly
4. **Define color constants** — Centralize your color palette for consistency
5. **Style at the point of use** — Inline markup (`<font>`, `<b>`) for dynamic content, style definitions for structure
6. **Add spacing explicitly** — Use `Spacer` between flowables, not padding