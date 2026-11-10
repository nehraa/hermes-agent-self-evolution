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

Generate printable A4 worksheets, study sheets, and practice handouts with mixed text, color-coded content, and interactive elements like handwriting lines, checkboxes, and blank response zones.

This skill captures patterns proven through building grammar worksheets, oral prompt sheets, and dense study handouts.

## When to Use

Choose this skill when you need:

- **Printable educational handouts** — worksheets, practice exercises, study guides
- **Color-coded content** — each word or section with distinct formatting (e.g., tense indicators, part-of-speech labels)
- **Handwriting zones** — ruled lines for written responses
- **Interactive checkboxes** — for multiple-choice or task completion
- **Dense two-column layouts** — maximize content on A4 paper
- **Numbered items** — question prompts, exercise sequences
- **TENSE/POS indicators** — grammatical markers integrated into content

## When NOT to Use

- Standard text reports or documents (use standard reportlab or the `pdf` skill)
- OCR document processing or scanned page handling
- Fillable AcroForm PDFs with form fields
- Heavy visual layouts with images, graphics, or animation

## Core Architecture

python
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus.flowables import Flowable

# Tight A4 margins maximize usable space
doc = SimpleDocTemplate(
    "output.pdf",
    pagesize=A4,
    leftMargin=0.8*cm,
    rightMargin=0.8*cm,
    topMargin=0.5*cm,
    bottomMargin=0.5*cm,
)
### Layout Strategy

Use `Table` with two-element row structure for two-column layouts:

python
two_column_content = [
    [left_cell_content, right_cell_content],  # Row 1
    [left_cell_content, right_cell_content],  # Row 2
]

table = Table(two_column_content, colWidths=[8.5*cm, 8.5*cm])
### Color-Coded Text

Apply inline styling via XML tags within Paragraph text:

python
style = ParagraphStyle('custom', fontName='Helvetica', fontSize=11)

paragraph = Paragraph(
    '<font color="#2563EB"><b>PAST</b></font> they <font color="#059669">walk</font> home',
    style
)
## Custom Flowables

### Handwriting Lines

**Important:** Do not use underscore strings for writing lines. `"_" * 50` renders as tiny disconnected dashes, not full-width rules.

Use a custom `Flowable` instead:

python
class WriteLine(Flowable):
    """Full-width horizontal rule for handwriting responses."""
    def __init__(self, width=17*cm, thickness=0.6, color=HexColor("#9CA3AF"), spacing=20):
        Flowable.__init__(self)
        self.width = width
        self.thickness = thickness
        self.color = color
        self.height = spacing  # Space between lines

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        self.canv.line(0, 0, self.width, 0)
### Multiple Writing Lines

python
class WritingZone(Flowable):
    """Block of horizontal rules for extended writing responses."""
    def __init__(self, width=17*cm, lines=5, thickness=0.5, color=HexColor("#D1D5DB"), spacing=18):
        Flowable.__init__(self)
        self.width = width
        self.lines = lines
        self.thickness = thickness
        self.color = color
        self.height = lines * spacing

    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        for i in range(self.lines):
            y = i * (self.height / self.lines)
            self.canv.line(0, y, self.width, y)
### Checkbox Flowable

python
class Checkbox(Flowable):
    """Interactive checkbox for worksheets."""
    def __init__(self, size=10, checked=False):
        Flowable.__init__(self)
        self.size = size
        self.checked = checked
        self.width = size
        self.height = size

    def draw(self):
        self.canv.setStrokeColor(HexColor("#374151"))
        self.canv.setLineWidth(1)
        self.canv.rect(0, 0, self.size, self.size)
        if self.checked:
            self.canv.setFillColor(HexColor("#374151"))
            self.canv.setLineWidth(1.5)
            self.canv.line(1, self.size - 2, self.size/3, self.size/3)
            self.canv.line(self.size/3, self.size/3, self.size - 1, self.size - 1)
## Common Patterns

### Grammar Worksheet Item

python
def make_grammar_item(number, prompt, blank_count=3):
    """Single grammar worksheet item with prompt and writing lines."""
    items = [
        Paragraph(f"<b>{number}.</b> {prompt}", item_style),
    ]
    for _ in range(blank_count):
        items.append(WriteLine())
    items.append(Spacer(1, 0.3*cm))
    return items
### Two-Column Dense Layout

python
table_data = []
for i in range(0, len(items), 2):
    left = items[i]
    right = items[i + 1] if i + 1 < len(items) else ""
    table_data.append([left, right])

table = Table(table_data, colWidths=[8.5*cm, 8.5*cm])
table.setStyle(TableStyle([
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('LEFTPADDING', (0, 0), (-1, -1), 3),
    ('RIGHTPADDING', (0, 0), (-1, -1), 3),
]))
### Color-Coded Vocabulary Item

python
def vocab_item(word, translation, part_of_speech):
    """Vocabulary entry with color-coded part of speech."""
    pos_colors = {
        'noun': "#2563EB",      # Blue
        'verb': "#DC2626",      # Red
        'adjective': "#059669", # Green
        'adverb': "#7C3AED",    # Purple
    }
    color = pos_colors.get(part_of_speech, "#374151")
    return Paragraph(
        f'<font color="{color}"><b>{word}</b></font> — {translation}',
        vocab_style
    )
## Style Setup

python
styles = getSampleStyleSheet()

item_style = ParagraphStyle(
    'Item',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=10,
    leading=14,
    spaceAfter=4,
)

prompt_style = ParagraphStyle(
    'Prompt',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=11,
    leading=15,
)
## Building and Saving

python
from reportlab.platypus import SimpleDocTemplate

doc = SimpleDocTemplate(
    "worksheet.pdf",
    pagesize=A4,
    leftMargin=0.8*cm,
    rightMargin=0.8*cm,
    topMargin=0.5*cm,
    bottomMargin=0.5*cm,
)

story = [
    # Add your content here
]

doc.build(story)