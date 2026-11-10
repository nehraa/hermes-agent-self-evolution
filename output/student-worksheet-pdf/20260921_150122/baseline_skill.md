---
name: student-worksheet-pdf
description: Generate printable ESL/IELTS worksheets as PDFs.
---

# Student Worksheet / Handout PDF Generator

## Class of work
Printable ESL/IELTS materials: sentence drills, vocabulary sheets, grammar worksheets, cloze tests, listening transcripts. Output is always a PDF the teacher prints and gives to a student. Multi-version layouts (Version A vs Version B side by side) are common.

## Hard rules (user preference, non-negotiable)

**NEVER include the student's name, the teacher's name, or framing language that calls out the recipient.** No titles like "Get back your attention", "For [Name]'s recovery", "Dopamine detox sheet", or any text that singles out the student. The material should look generic — a worksheet any student could pick up and use. If it has a heading at all, it's a neutral description like "6-Word Sentence Worksheet" or "Past Simple Drill".

Reason: the worksheet gets handed to the student. Anything that reads as "we know what's wrong with you" turns them off before they even start.

## Standard layout patterns

### Side-by-side dual-version (single PDF)
Two columns on A4 portrait:
- Left = Version A (plain / prompt)
- Right = Version B (enhanced — color-coded, with checklist, etc.)
- Header row with cream/blue tint distinguishing the two
- 5 entries per page is the sweet spot on A4 at 12.5pt body font
- 2 writing lines per entry (underscores, ~58 chars wide for left col, ~52 for right)

### Separate-PDF dual-version (when user prefers)
User sometimes says "put each version in its own PDF so each is small." Pattern:
- Version A → one PDF with single column, plain
- Version B → one PDF with single column, color-coded
- Both share same legend + tense reference on page 1
- Density: 7 sentences/page with writing lines, 10 with short lines, **28 with blank writing zone matching sentence dims**

### Single-version with answer space
Sentence on top, blank writing zone below. Use `BlankSpace` flowable sized to match the sentence itself:
```python
class BlankSpace(Flowable):
    def __init__(self, width, height):
        Flowable.__init__(self)
        self.width = width
        self.height = height
    def draw(self):
        pass  # pure white space
# Sentence is 10pt, leading=12pt → ~0.42cm tall
# Match: BlankSpace(width=8.5*cm, height=0.5*cm)
```
**Don't use underscore characters for writing zones** — they render short and pale when wrapped in a Paragraph. BlankSpace produces a proper full-width writing area. User asked to remove the lines and just keep one writing zone "same width and height as the actual sentence" — this is the right primitive.

### Rapid-fire oral question sheets
For students with short attention spans who can't sustain written work — single page, 2 columns, ~38 short prompts (15-second oral drills). Each row = `[number]. [category] [letter]` header + short instruction text. No writing zone. Teacher reads aloud, student answers out loud, teacher moves on. Density target: 38 fit on A4. Examples: "Name 5 animals starting with A", "Count backwards from 20 to 1", "Name 5 yellow things you see every day". Mix alphabet drills + category drills + math for variety.

### Single-version with answer space
Sentence on top, 2-3 blank writing lines below. Use for reading comprehension, sentence construction, dictation.

### Color-coded grammar — 6-color POS (full role distinction)
For students who confuse grammatical roles (common when their first language lacks articles or has freer word order), use **6 distinct colors** instead of 3:

- Subject (who/what does it) = blue (#1D4ED8)
- Verb (the action) = red (#B91C1C)
- Object / complement (what is affected) = green (#15803D)
- Article (a, an, the) = purple (#7C3AED)
- Preposition (in, on, at, to, for, with, by, from...) = orange (#EA580C)
- Adverb / time marker (today, yesterday, daily, here, often) = cyan (#0891B2)

Bold all colored words. Always include a legend on page 1 with all 6 color labels so the student can self-reference while working.

**Why 6 and not 3:** Student who sees "The cat drinks fresh water" with everything-after-verb in green thinks "in/on/at" are also objects. Coloring articles and prepositions separately makes each role visually distinct — student learns each word's function by its color, not by guessing what "the rest of the sentence" is.

### Color-coded grammar — 7+ category refinement (when user demands word-by-word exhaustiveness)

When the user pushes back on coloring quality (e.g. "are u looking at the right pdf?" / "I still see adv on top and some words in cyan"), they want every word correctly classified into a category that EXISTS in the legend. **Hard rule: every word in the sentence must have exactly one valid grammatical category from the legend.** If "and" appears and there's no CONJUNCTION category, the coloring is wrong by definition — not a stylistic choice.

Extended scheme (switch to this when user explicitly audits the coloring):

| Category | Color | Hex | Examples |
|---|---|---|---|
| SUBJ | blue | #1D4ED8 | she, the boy, soil nutrients |
| VERB | red | #B91C1C | runs, is, will be, studied |
| OBJ | green | #15803D | a book, the door, my car |
| DET | purple | #7C3AED | my, our, his, this, that, all |
| PREP | orange | #EA580C | in, on, at, to, for, with, by |
| ADV | cyan | #0891B2 | yesterday, today, outside, heavily, forever, ago |
| CONJ | pink/magenta | #DB2777 | and, but, or |

**DET vs ART split:** if the legend distinguishes "articles only (a, an, the)" from "all determiners (including my, our, his, this, that, all)", use light-purple #A855F7 for ART and dark-purple #7C3AED for DET. Otherwise lump them as DET and use purple for both. Always include a sub-legend explaining the distinction when both are used: "DET = determiners (a, an, the, my, our, his, her, their, this, that, all) · ART = articles only".

**Adjective merge pattern:** when the user says "remove the adj entirely" or wants minimal categories, merge adjectives into the OBJ color of the noun they modify. Do NOT keep adjectives as a separate category — it confuses students. `"heavy door"` → `heavy` and `door` both green (same color, no separate label). Strip any "(incl. adjectives)" note from the legend when doing this.

**Adjective-vs-adverb context disambiguation** (same word, different tag depending on context):

| Word | Context | Tag |
|---|---|---|
| daily | "daily life" (modifies noun) | OBJ |
| daily | "arrives daily" (modifies verb) | ADV |
| last | "last night" / "last Sunday" (adverbial time) | ADV |
| last | "last week" (noun phrase) | OBJ |
| home | "near home" (object of prep) | OBJ |
| home | "drive home" (adverb of place) | ADV |
| fast | "a fast car" (adjective) | OBJ |
| fast | "drives fast" (manner adverb) | ADV |
| right | "the right answer" (adjective) | OBJ |
| right | "right outside" (degree adverb) | ADV |
| tomorrow, yesterday, today, tonight, now | time adverbs | ADV |
| forever | time adverb | ADV |

**Possessives must be DET, not S:** `My mother cooks` → `My` is DET (purple), `mother` is SUBJ (blue). Otherwise the possessive looks identical to the subject word and confuses the student about what makes a subject. Apply consistently: `My`, `our`, `his`, `her`, `their`, `your`, `its` are all DET.

**Common exhaustiveness audit points** (user will flag these if missed):

| Word | Default that FAILS | Correct tag |
|---|---|---|
| every (before noun, e.g. "every night") | OBJ | ADV (adverbial time phrase) |
| last (before day/night/week, e.g. "last night") | OBJ | ADV |
| next (before week, e.g. "next week") | OBJ | ADV |
| tonight, yesterday, tomorrow | OBJ | ADV |
| home (after preposition, e.g. "near home") | ADV | OBJ |
| out (after verb, e.g. "move out") | PREP | ADV (particle) |
| twenty minutes, two hours (duration) | OBJ | ADV |
| right (before adverb, e.g. "right outside") | OBJ | ADV |
| nearby | OBJ | ADV |
| and | OBJ | CONJ |
| forever | OBJ | ADV |
| home (after verb of motion, e.g. "drive home") | OBJ | ADV |

### Multi-pass verification loop (mandatory when user pushes back)

When the user has already flagged errors once, they will flag them again if the next iteration has new ones. The minimum bar is **all 100 sentences, word by word, on every page**. Default workflow after building the PDF:

1. `pdf2image.convert_from_path(pdf, dpi=120)` → save all pages
2. For each page, run vision_analyze with: "Look at every word on this page. Is the subject (blue) and verb (red) clearly visible in every sentence? Any sentence with missing blue/red? Any wrong color?"
3. Spot-check the specific sentence numbers the user flagged in the previous turn
4. If any wrong color found, fix the tag, rebuild, repeat — don't claim done after one round

**User signals the audit isn't over yet** (any of these = keep iterating):
- "I still see [wrong color] on [N]"
- "are u sure we are working on the right pdf?"
- "[N] is still wrong"
- "you missed [N]"

When user gives an enumerated list of corrections ("#3, #17, #20, #23..."), execute EXACTLY that list — don't add extra fixes beyond what was asked. Extra unrequested fixes = friction.

### Tense / category checklist
All six IELTS tenses fit on two lines at 8pt with `[ ] Present Simple   [ ] Past Simple   [ ] Future Simple   [ ] Present Continuous   [ ] Past Continuous   [ ] Future Continuous`. Use `[ ]` not `☐` — ZapfDingbats fallback renders as filled black square in default Helvetica. `[ ]` always works.

## Sentence content (when generating with an LLM)

When the LLM gives you sentences, **always verify word count programmatically** with `len(sentence.split())`. Counted multiple times this session — MiniMax M2.7 returns 7-8 word "6-word" sentences ~40% of the time. Treat the LLM output as a draft and count before shipping.

Better: for known-constrained corpora (exactly N words, exactly N sentences, specific tense mix), **generate deterministically in Python instead of via LLM**. Word count is mechanical; the LLM adds no value here.

For MiniMax M2.7 specifically, **avoid the `/v1/chat/completions` endpoint** for structured JSON output — the response is wrapped in thinking blocks (`<think>...</think>`) that eat the entire response if max_tokens is too low, and even with max_tokens=8000 the JSON often comes out empty after fence-stripping. Use `/anthropic/v1/messages` with `X-Api-Key` + `anthropic-version: 2023-06-01` for reliable JSON. Or skip the LLM entirely for word-counted corpora.

## POS tagging for color coding (when LLM isn't doing it)

### 6-role full tagging pipeline

For 6-color grammar worksheets, classify each word into ART / PREP / ADV / S / V / O:

1. **Direct lookup first** (cheapest, most accurate):
   - `ARTICLES = {"a", "an", "the"}` → ART
   - `PREPOSITIONS` (curated set of ~30 common ones: in/on/at/to/for/with/by/from/of/into/onto/upon/about/over/under/between/among/through/across/around/before/after/during/until/since/against/without/within/near/behind/beside/beyond/toward/towards/via/per/off/out) → PREP
   - `ADVERBS` (time + manner: today/yesterday/tomorrow/now/daily/here/outside/inside/always/never/often/quickly/slowly/carefully/together/next/last/...) → ADV

2. **Find verb chain** in remaining words:
   - First, scan forward from index 0 for any verb-form word (auxiliary, known verb, -ed/-ing/-s ending)
   - If it's an auxiliary (`is/are/was/were/will/be`), continue forward to find the **main verb after it** — so "She is studying" tags `is` + `studying` both as V
   - Include preceding `not`/`n't` in verb span too — "She is not studying" → V = `is not studying`
   - Multiple verb forms in a row (e.g. "will be traveling") → all tagged V

3. **What comes before the verb chain = S** (subject — could be pronoun, single word, or noun phrase like "The boy" / "My mother")
4. **What comes after = O** (object / complement)

### Verb-detection heuristic order — stop at first match

1. Skip articles/determiners/pronouns (`the`, `a`, `my`, `she`, `it`, `every`, `some`...)
2. Skip pure `-ly` adverbs (`always`, `really`, `daily` when not modifying a noun)
3. Skip false-positive `-ing` nouns — needs explicit NOT_VERBS_ING set: `morning, evening, king, wedding, ceiling, ring, string, building, feeling, meaning, clothing, everything, nothing, something, climbing, training, greeting, meeting, listening, opening, ending, beginning, reading`
4. Skip false-positive `-s` nouns — needs explicit NOT_VERBS_S set: `bus, plus, gas, glass, grass, yes, class, pass, press, process, dress, kiss, miss, boss, loss, mess, news, this, his, hers, its, success, progress, focus, lens, chaos, canvas, atlas, corps, cosmos, fuss, bias, always, news`
5. Skip **plural agent nouns** that end in -s (farmers, workers, scientists, investors, researchers, teachers, children, parents, students, doctors) — these are common subjects but suffix rules mis-tag them as verbs
6. Direct match against a curated KNOWN_VERBS list (50-80 verbs for a fixed corpus)
7. Past tense `-ed` ending
8. Present participle `-ing` ending
9. 3rd-person `-s`/`-es` ending

**Curate a KNOWN_VERBS list for the actual corpus.** For 100 sentences, building a 50-80 verb dictionary + hand-tagging the 5-10 sentences where the heuristic fails is faster than perfecting the rule. Save the override map to `tagged_full.pkl` and reuse it.

### Density stats (typical 100-sentence 6-word corpus)

```
ART:  ~78  (articles are frequent)
S:    ~109 (subjects)
V:    ~140 (verbs incl. aux chains like "will be traveling" = 3 V tags)
O:    ~194 (objects — biggest category)
ADV:  ~44  (time + manner)
PREP: ~37
```

Total: 600 words for 100 sentences = 6 each ✓

### Audit pass after tagging — mandatory before PDF build

After applying overrides, run a sentence-vs-tag match check. **Caught a real bug this way:** applying corrections using sentence numbers (1-indexed: "fix sentence #23") when the array is 0-indexed silently overwrites the wrong rows, AND copying one sentence's tags to fix a neighboring sentence duplicates content. Symptom: PDF shows the same sentence twice on consecutive rows.

```python
mismatches = 0
for i in range(100):
    expected = arr[i]["sentence"]
    actual = " ".join(w for _, w in tagged_all[i])
    if actual != expected:
        print(f"  ⚠ idx {i}: expected '{expected}' but got '{actual}'")
        mismatches += 1
if mismatches == 0:
    print("✓ ALL 100 sentences match their text correctly")
```

Fix the mismatches by re-reading each affected `arr[i]["sentence"]` and re-tagging by hand. Don't trust override-by-index mappings blindly — the offset-by-one bug propagates silently until you actually compare string output.

## ReportLab patterns

```python
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER

doc = SimpleDocTemplate(
    "out.pdf", pagesize=A4,
    leftMargin=0.9*cm, rightMargin=0.9*cm,
    topMargin=0.6*cm, bottomMargin=0.6*cm,
)
```

Font sizes that print well at A4:
- Body sentences: 12-13pt
- Numbering: 10-11pt bold
- Tense checklist: 8-9pt
- Header row labels: 8pt bold
- Writing lines: 9pt underscore chars

Page-margin budget: 0.9cm sides + 0.6cm top/bottom leaves enough body area for 5 dual-version entries without overflow.

## Verification

Always render at least the first 2 pages to PNG via `pdf2image` and **visually inspect via vision_analyze** before claiming done. Things that look fine in the data but break visually:
- Checkboxes rendered as filled black squares (ZapfDingbats missing — use `[ ]` not `☐`)
- Text getting clipped at the bottom of the last entry
- Color coding splitting inside noun phrases ("The cat" → "The" blue / "cat" green instead of both blue)
- Header legend wrapping awkwardly
- Page count off by one (28-per-page target → 5 pages instead of 4)
- **Writing lines/areas too short** — underscore chars in Paragraphs render short. Use `BlankSpace` flowable with explicit width/height matching the sentence dims
- Color codes bleeding across categories — e.g. "farmers" mis-tagged as V because suffix rules miss plural-agent nouns

**Iterate on the visual.** User will ask for: split into 2 PDFs, 7 per row, 14 per page, 28 per page, single line, no lines, BlankSpace zones, different colors, color articles/prepositions separately, separate CONJUNCTION category, DET vs ART split, adjective-vs-adverb context fixes. Each is a small adjustment to the layout, not a redesign. Ship the version, wait for the next ask.

**Multi-pass loop when user audits:** when user gives word-by-word color corrections (their enumerated list of "this word should be X, that word should be Y"), fix exactly what they listed, rebuild, and re-verify ALL pages — not just the ones they flagged. New errors often appear in nearby sentences from the same auto-tag logic. Don't stop after one fix round; iterate until user explicitly says "ship it" or moves on. See the multi-pass verification loop section under "7+ category refinement" for the exact protocol.

## Output delivery

Always deliver as `MEDIA:/absolute/path/to/file.pdf` in the response so the user gets it natively on Telegram. Don't make them download from a link.

## Reference data

- `references/6-word-sentence-corpus.md` — the 100-sentence 6-word corpus (verified, 6 words each, all 600 word-tags hand-curated), plus the 38-question rapid-fire oral drill list, plus the override map for the heuristic POS classifier. Use as the canonical data when regenerating either PDF.
- `references/7-category-color-scheme.md` — the full 7-category (SUBJ/VERB/OBJ/DET/PREP/ADV/CONJ) color palette with hex codes, the adjective-vs-adverb context disambiguation table, and the audit-findings list of words that get misclassified (and, every, last, next, home, out, etc.). Use this when the user pushes back on color quality and demands word-by-word exhaustiveness.
