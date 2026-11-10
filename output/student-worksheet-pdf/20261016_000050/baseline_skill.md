---
name: student-worksheet-pdf
description: Generate printable ESL/IELTS worksheets as PDFs.
---

# Student Worksheet / Handout PDF Generator

## Class of work
Printable ESL/IELTS materials: sentence drills, vocabulary sheets, grammar worksheets, cloze tests, listening transcripts. Output is always a PDF the teacher prints and gives to a student. Multi-version layouts (Version A vs Version B side by side) are common.

**Hard rules (user preference, non-negotiable)**

**NEVER include the student's name, the teacher's name, or framing language that calls out the recipient.** No titles like "Get back your attention", "For [Name]'s recovery", "Dopamine detox sheet", or any text that singles out the student. The material should look generic — a worksheet any student could pick up and use. If it has a heading at all, it's a neutral description like "6-Word Sentence Worksheet" or "Past Simple Drill".

Reason: the worksheet gets handed to the student. Anything that reads as "we know what's wrong with you" turns them off before they even start.

**When the user says output is wrong, work manually one step at a time FIRST, then encode as a script.** This came up directly on 21 Sept 2026: "Maybe u don't use scripts for everything and sometimes if I say u are getting it incorrect u try to do it manually one step at a time and later when it all works then u make script something to know for future." The pattern that triggers this:

1. User reports an output is wrong
2. They want to see the agent iterate by hand — fix THIS sentence, verify by eye, fix the NEXT sentence — not "let me rewrite the auto-expander and run again"
3. Only AFTER manual iteration produces a known-good output should the agent generalize it into a script

Concrete: when building the 15-word corpus, the agent kept auto-pad-trimming with smart expanders and the user kept saying "worse" / "it doesn't work". The user wanted each sentence hand-written, hand-counted, and verified visually one at a time. The right move was: write 10 sentences in a Python file, run a check that asserts each is 15 words, fix the ones that fail by hand, write 10 more, repeat. THEN, once 100 verified-good sentences exist, write the build script that consumes them. The script is a downstream artifact of a manually-verified corpus, not a generator that the agent hopes will produce good output.

**Don't overengineer when user asks for plain.** When the user says "make a black and white version no color no marking nothing," give them black ink and plain text — no legend, no checkboxes, no decorations, no per-sentence tense checklist, no POS coloring, no BlankSpace write zones. Strip everything that wasn't asked for. The agent kept trying to salvage the colored version with "the legend still names them" rationalization; the user wanted the colors gone entirely. When the user simplifies, simplify. The skill should err on the side of "ship the minimum" rather than "ship what was working before."

**NEVER claim "shipped" or "ready" until you've visually verified every page.** User has caught the agent claiming the worksheet was correct while sentences were entirely miscolored — "It's not accurate there are issues some sentences are entirely blue and I are saying it's working so idk how can I trust u." The rule:

- After `doc.build()` produces the PDF, the deliverable is NOT done.
- The deliverable is done when you've rendered each page to PNG, run `vision_analyze` with a per-page audit query, and produced a specific list of (page, sentence number, wrong word, observed color, expected color) findings.
- "Looks good" or "I think it's right" is not a verification — it's a guess. Either list what you actually checked or don't ship.
- If the PDF was built from a heuristic that might fail (plural -s mis-tagging, legend rendering as HTML strings, etc.), the audit is even more important. Heuristics drift; visual review is the only ground truth.

## Standard layout patterns

### Vocabulary sheet / pre-reading word cards

A different class of handout from the sentence drills below. Output is a single PDF where each entry = word + plain-English definition + example sentence using the word. Used as a "study these words before you read the passage" deck.

**Layout that worked** (Plant Wars, 159 entries in 6 pages, A4):
- A4 portrait, margins 0.9 cm sides / 0.6 cm top-bottom
- 2-column Table layout: left col entry → right col entry, pair by index
- 14 entries per column block (28 per page) keeps density high without truncation
- Per-entry stack (4 Paragraphs in one Table cell):
  1. tiny tier tag (`T2` / `T3`) in the tier color, 8 pt
  2. **word** in accent color, 11.5 pt
  3. plain-English definition, 9.5 pt, indented 4
  4. `Ex:` sentence with the word bolded, 9.5 pt, indented 4
- Tier background fills the whole cell: amber `#FEF3C7` for T2 concepts, light blue `#DBEAFE` for T3 passage-specific. Border in matching hex (`#FCD34D` / `#93C5FD`).
- Section header before each tier group with word count: `Tier 2 — Concepts to learn (110 words)`
- Last page may have whitespace at the bottom — fine, do NOT pad with an orphan entry
- Padding: TOPPADDING 0 / BOTTOMPADDING 0 between rows; Spacer(1, 0.12–0.15 cm) between blocks — sets the rhythm
- Inter-column divider LINEAFTER (col 0) 0.4 pt `#D1D5DB`

**Density math** (so you don't iterate blindly):
At 0.9/0.6 cm margins, 11.5 pt word + 9.5 pt def + 9.5 pt example ≈ 1.4 cm tall per entry. A4 body height ≈ 27 cm. Two columns × ~14 entries per column-block fits cleanly (≈ 19.6 cm) with a header above. So **~28 entries/page** is the natural ceiling. Bigger entries (long definitions, longer examples) drop to ~24/page; ultra-short fits ~32.

### Vocabulary list tied to a specific sentence worksheet (ordered by sentence #)

When the user asks for "vocabulary from the sentences" / "words from those sentences" / "vocab for the worksheet" — they don't want the full corpus alphabetized. They want:

1. **Scope:** only words that actually appear in the sentence PDF they're studying.
2. **Order:** by sentence number, not alphabetized. Read sentence 1, see its words, move to sentence 2, see its words, etc. User correction (Sept 22 2026): "read every single sentence and extract difficult vocabulary from that then move to next sentence then next then next and then at last write all of them down."
3. **Definitions in simple English.** User correction: "try using easy words to explain what it means." Default to plain language — "happens slowly" beats "occurs gradually." Avoid academic-sounding definitions the student won't understand either.
4. **Layout:** 2 columns per page to fit more. Truncate the sentence reference to ~60 chars + "..." so the cell isn't dominated by the sentence text.

**Recipe (Sept 22 2026, the working pattern):**

- Per-sentence cell content:
  1. `Paragraph` with `Sent {N}` (bold, dark gray) + the sentence itself (italic, muted gray, truncated to 60 chars)
  2. For each hard word: `Paragraph` with bold word + "— {simple meaning}"
  3. For each hard word: `Paragraph` with `Ex: {short example using the word}`
  4. `Spacer(1, 0.15*cm)` between sentences
- Pack into a 2-column Table: ~10 sentence blocks per column, 20 per page.
- Skip basic/function words (the, is, of, pronouns, common verbs like make/get/go) using a `SKIP` set. Don't include words a student can already read in context.
- Skip proper nouns and years (1893, Marie, Paris) — they're not vocabulary, they're just names.

**What counts as "hard enough" to include:** any content word (noun, adjective, complex verb, complex adverb) that:
- Isn't in the basic skip list
- A student preparing for IELTS Academic would benefit from studying

If the same word appears in multiple sentences, only include it once (under the first sentence that uses it) — keeps the vocab list from being 80% repeats. Don't alphabetize across sentences — duplicates in different sentence blocks are fine and actually reinforce the word's multiple contexts.

**Reference:** `references/vocab-by-sentence-layout.md` for the full code pattern + the "simple explanation" guidance table (academic → simple translations for ~50 common IELTS words).

**Tier convention:**

| Tier | What it is | Box color |
|---|---|---|
| Tier 1 | basic nouns/verbs the learner already knows (plant, tree, fight, grow) | gray `#F3F4F6` |
| Tier 2 | concepts to learn (soil, mechanism, intricate, lethal) | amber `#FEF3C7` |
| Tier 3 | passage-specific vocabulary (allelopathy, DIBOA, clinical trials) | blue `#DBEAFE` |

**Drop Tier 1 by default.** User pattern: asks "give me the words they need to know," gets a full T1+T2+T3 PDF, then complains "that's just a few words" or "I don't want tier 1, that way you can fit in more tier 2 and tier 3 words." Build the first version **T2+T3 only** unless they explicitly ask for T1. If you build T1 first and they push back, the rebuild is ~30 s.

**Expand the list aggressively.** When the source passage has lots of concept words the learner genuinely needs (e.g. the Plant Wars passage has 100+ T2 + ~50 T3 candidates), exhaustive coverage beats the small curated list. Read the passage paragraph by paragraph, extract every word above Tier 1 register, and include it. Have plenty; the user will not complain about volume in this class of task.

**Section header per tier.** Before each tier's entries, add a `Heading2`-ish row that names the tier AND gives the word count. Lets the teacher see at a glance how many are in each bucket.

**Good example sentence pattern.** Each example sentence should:
- be short enough to read at a glance (~5–12 words)
- **bold the headword** so the learner sees it in context
- be generic enough that the learner won't confuse it with the source passage (don't quote the passage)
- never contain content that would embarrass or single-out the student

**Source-passage extraction.** When the vocabulary sheet is paired with a specific reading passage, pull the clean text via `pdftotext -layout <source.pdf> -` — NOT from an OCR'd image of a screenshot. PDF text extraction is accurate enough; the OCR-on-screenshot pipeline silently drops words and re-orders sentences. See `references/ocr-pitfall-pdf-extraction.md` for the trap.

### Side-by-side dual-version (single PDF)
Two columns on A4 portrait:
- Left = Version A (plain / prompt)
- Right = Version B (enhanced — color-coded, with checklist, etc.)
- Header row with cream/blue tint distinguishing the two
- 5 entries per page is the sweet spot on A4 at 12.5pt body font
- 2 writing lines per entry (underscores, ~58 chars wide for left col, ~52 for right)

### Plain text variant (when user wants no decorations at all)

When the user asks for "just text", "no colors", "no marking", "no checkboxes", or "black and white" — give them plain black text on white paper. Specifically:

- No color coding (drop the entire 6/7-color scheme)
- No legend row (no SUBJ/VERB/OBJ header bar)
- No per-sentence tense checklist
- No BlankSpace write zones (sentence + write-line together is bloat when there's no color context to justify the write zone)
- No section headers beyond a neutral page title like "15-Word Sentence Worksheet" (if a title is wanted at all)

Density target for plain text: pack as many sentences per page as the layout allows without crowding. For 15-word sentences, 2 columns × 10 rows = 20 sentences/page gives a full-but-not-cramped page in 5 pages total. Bump up to 2 columns × 13-14 rows if the user explicitly asks for more density. The plain variant exists specifically so teachers can hand out a clean reading-and-discussion sheet without the visual crutches of the colored version.

Build pattern:

```python
body_style = ParagraphStyle("body", parent=styles["Normal"],
    fontName="Helvetica", fontSize=11, leading=14)
doc = SimpleDocTemplate("out.pdf", pagesize=A4,
    leftMargin=1.5*cm, rightMargin=1.5*cm,
    topMargin=1.5*cm, bottomMargin=1.5*cm)
# 2 col Table with `num. sentence` text, no other decoration
```

Ship the minimum. When the user asks for plain, don't try to keep the colored version's legend as a "fallback reference" — that's not what they asked for.

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
    def wrap(self, *args):
        return (self.width, self.height)
    def draw(self):
        self.canv.setStrokeColor(HexColor("#D1D5DB"))
        self.canv.setLineWidth(0.4)
        self.canv.rect(0, 0, self.width, self.height, stroke=1, fill=0)
# Sentence is 10pt, leading=12pt → ~0.42cm tall
# Match: BlankSpace(width=8.5*cm, height=0.6*cm)
```
**Don't use underscore characters for writing zones** — they render short and pale when wrapped in a Paragraph. BlankSpace produces a proper full-width writing area.

**Two critical BlankSpace rules (Sept 21 2026, learned the hard way):**

1. **`Canvas.rect(strokeColor=...)` and `strokeWidth=` kwargs are gone in modern ReportLab.** The old API accepted them; current reportlab raises `TypeError: Canvas.rect() got an unexpected keyword argument 'strokeColor'`. Always use `setStrokeColor()` + `setLineWidth()` first, then call `rect(..., stroke=1, fill=0)`. The `wrap()` method is also required — without it the Flowable reports zero size and the rest of the table collapses.

2. **Don't add a write-line per sentence when sentences wrap to 2+ lines.** Hit this building the 15-word corpus: every sentence wraps in a 2-column × 10-sentence/page layout, so a write-line column = vertical space that exceeds the page. Symptom: sentences get truncated (column 3's BlankSpace row consumes the row height, sentence cell overflows). Either drop the write-line entirely (color-coded reading worksheet, no rewrite) OR give each sentence its own page. Don't try to share rows between sentence + write-line when sentence length is ≥10 words.

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

**Critical legend pitfall (Sept 21 2026):** when putting the legend in a Table row, pass `Paragraph` objects into the cells — NOT raw HTML strings. A raw `'<font color="#1D4ED8"><b>SUBJ</b></font>'` in a Table cell renders the literal text including the tags. Always: `Paragraph(f'<font color="{hex}"><b>{tag}</b></font>...', cell_style)`. The Table is just a layout container; it doesn't render HTML in string cells.

**Why 6 and not 3:** Student who sees "The cat drinks fresh water" with everything-after-verb in green thinks "in/on/at" are also objects. Coloring articles and prepositions separately makes each role visually distinct — student learns each word's function by its color, not by guessing what "the rest of the sentence" is.

**Plural noun mis-tagging pitfall (Sept 21 2026, 15-word corpus):** the `-s` heuristic step (rule 9 above) tags any word ending in `s` (length > 3, not in NOT_VERBS_S) as a verb. That bites on plural subject nouns like `Birds`, `Children`, `Workers` — "Birds build nests" gets tagged `Birds=VERB, build=VERB, nests=OBJ`, so the FIRST verb (Birds) is taken as the verb and everything before it is empty. The post-process flips all O before first V → S, which produces empty SUBJ + Birds-as-verb (red). Symptom: plural subjects render RED instead of BLUE.

**Three-step fix:**

1. **Whitelist plural -s nouns in NOT_VERBS_S:** add the obvious ones — `birds, animals, books, cars, trees, doors, windows, pens, pencils, students, children, workers, people, boxes, bottles, machines, engines, tables, flowers, leaves, knives, wives, lives, boys, girls, men, women, days, nights, ways`. Plus the plural-agent nouns (farmers, scientists, ...) already covered in step 5 of the heuristic. The list will never be exhaustive — that's fine, it's a heuristic.

2. **Post-process the tags:** after the standard "O before first V → S" rule, look at the first V. If it ends in `s`, isn't in NOT_VERBS_S or KNOWN_VERBS, isn't a base verb (is/was/has/does), and the SECOND V in the sentence is a base form (not ending in -s), then the first V is actually a plural subject — flip it to S. Heuristic, but catches "Birds build", "Children played", "Workers fixed" where the second verb is clearly base-form.

3. **Audit visually** — if "Workers"/"Children"/"Birds" render RED, the heuristic missed; extend the whitelist or hand-tag that sentence.

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

**Audit EVERY sentence on EVERY page. No exceptions.** When the user says "I want every single sentence check using vision tools see the color is accurate," they mean EVERY sentence on EVERY page. Don't sample 5 per page and declare victory. Don't spot-check only the sentences you think are problematic. Iterate one page at a time, listing every wrong color found per page, fixing the tagger, rebuilding, and re-auditing until zero wrong colors across all pages.

**The right audit query per page (copy-paste-ready):**
> "Page N of the PDF. For each sentence on this page, list every word and verify its color is correct per the legend: SUBJ=blue, VERB=red, OBJ=green, DET=purple, PREP=orange, ADV=cyan, CONJ=pink. (1) Are plural subject nouns like 'Birds' / 'Children' / 'Investors' BLUE not RED? (2) Are adverbs like 'today' / 'yesterday' / 'now' CYAN? (3) Are first words of sentences always BLUE? (4) List specific sentence numbers where colors are wrong. Be brutally honest."

**Batched reporting wins:** instead of "the PDF looks correct," the user wants "page 1: sentence #9 'Birds' is RED (should be BLUE); sentence #24 same issue. Page 2: #40 'Children' is RED." A list of specific bad sentences lets the user verify you actually looked.

**User pushback patterns that mean "you didn't actually verify":**
- "It's not accurate there are issues some sentences are entirely blue"
- "I are saying it's working so idk how can I trust u"
- "Use ur fucking eyes dawg like cmon"
- "look at they eat lunch" (pointing to one specific sentence and asking you to confirm)

These are FIRST-CLASS signals that the previous output claimed success without actual per-sentence verification. The fix: stop claiming "shipped" until you've literally viewed each page via vision and listed the result.

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

**Deterministic N-word corpus recipe (Sept 21 2026, works for any N ≤ ~20):**

1. Hand-write the corpus as a Python list of strings. Mark every sentence with its current word count in the comment. Don't try to count by eye — you'll be off by 1-2 on ~80% of them.
2. Build script asserts at the top: `assert all(c == N for c in counts)`. First failure stops the build, prints the offending sentence, tells you the actual count.
3. If many sentences are off (typical), run `scripts/auto_fix_corpus.py`. It regex-extracts every literal string in the corpus, pads to N words with curated filler (`daily / today / now / every day / always...`), OR trims trailing tokens. ~85 fix rate on first pass for N=15.
4. After auto-fix, re-run the script. Any remaining failures are usually awkward compositions (e.g. "outside in every afternoon") — the fix may damage readability. Manually rewrite those 5-10 sentences with cleaner constructions, then verify again.

**Why not just call an LLM with strict instructions?** The LLM drifts even with "exactly 15 words" in the prompt — M2.7 returns 14-17 word range ~30% of the time. Deterministic Python guarantees the constraint; readability you trade away only on the 10-15 sentences auto-fix can't handle. Use LLM only when the corpus has no quantitative constraint.

### Source authentic IELTS passages from the local corpus (preferred over LLM fabrication)

User correction (Sept 22 2026): "Maybe u can even use real Ielts passages from web of reading random passages and take sentences from that don't just put one passage in sentences that's stupid random sentences. And then don't use the old corpus they are fucked u fucked them."

This is now the DEFAULT source for any IELTS-level worksheet, not hand-written or LLM-generated. Both alternatives produce text that *looks* like IELTS but doesn't read like actual IELTS — the vocabulary register is too clean, the sentence rhythm too uniform, the topic distribution too narrow.

**Local source (always preferred):** `/home/Hermes/repos/IELTS_Trainer/passages/` — 159 files `Test_001.txt` through `Test_159.txt`, each containing real Cambridge IELTS Academic Reading passages (extracted from ieltsfever practice tests). Topic spread: biology, history, agriculture, technology, sociology, environment, linguistics, etc. Each file has ~1500-3000 words across 3 passages (Passage 1/2/3).

**Extraction pattern (works for any N-word worksheet):**

1. Sample 12-15 tests spread across the 159 (NOT clustered — pick 1 every ~10 tests, e.g. `Test_001, Test_007, Test_012, Test_019, ...`). Clustered picks give you duplicate topics.
2. Read each file, strip page-header noise: `=== Test_NNN-NN.png ===`, `https://...`, `help @ ieltsfever.com`, `IELTSFEVER`, `Academic Reading Practice Test N`, `SECTION N`, `Reading passage N`, `Spend N minutes`, `Questions N-N`, `Do the following`, `Choose the correct letter`, etc.
3. Split on sentence terminators (`(?<=[.!?])\s+`), filter out anything <50 chars (test instructions, bullet fragments).
4. Trim each long sentence to exactly N words: take the first 15 words, append period if missing. Preserves the original Cambridge vocabulary + register — no fabricated filler words.
5. Deduplicate (the same passage can appear in adjacent page files), then randomly sample 100.
6. Assert `len(s.split()) == N` for every sentence. The script must abort if any fail.

**Yield from a 15-test sample: ~800-900 unique 15-word sentences** (way more than 100 needed). Variety comes for free.

**Why this beats web scraping / PDF extraction for IELTS content:** the local repo has already done the heavy lifting — the passages are clean Cambridge test material, no OCR artifacts, no paywalls, no copyright risk on this server. Web fallback (IELTS official PDF, ielts-up, ielts-mentor, etc.) only if the local repo is missing or stale.

**Curly-quote tokenization pitfall (Sept 22 2026):** `sentence.split()` on `"The decision..." says X` treats the entire `"decision..."` chunk as ONE word because the curly quotes stay attached to the adjacent text. The word count comes out wrong (off by 1 if there's exactly one quoted phrase). **Fix:** before any word-count check, run `s.replace("\u201c","").replace("\u201d","").replace("\u2018","").replace("\u2019","")` on the sentence. Real IELTS passages from ieltsfever have lots of curly-quoted interview text ("…", says researcher) — this trap will fire on every third sentence if not stripped.

### "Pretty" plain variant (Times-Roman serif, no header chrome)

When the user says "make a pretty PDF" (not "color-coded", not "with legend", just pretty) — interpret as: clean serif body type, muted sentence numbers, no per-sentence checkboxes, no color legend. Distinct from the Helvetica plain variant documented above.

**Working recipe (Sept 22 2026):**
- Font: `Times-Roman` body, `Times-Italic` for sentence numbers
- Sentence number: muted gray `#9CA3AF`, italic, right-aligned to width 3 chars (`{num:>3}.`)
- Body text: dark gray `#111827`, font size 11.5pt, leading 15.5pt
- Margins: 1.4cm sides, 1.6cm top/bottom (slightly tighter than the 1.5/1.5 plain variant to fit 20 sentences comfortably)
- Layout: 2 columns × 10 rows = 20 sentences/page (15-word sentences wrap to 2-3 lines each — 20 is the practical ceiling)
- Each cell: `Paragraph(f'<font color="#9CA3AF"><i>{num:>3}.</i></font> <font color="#111827">{sent}</font>', body_style)`
- Table style: `VALIGN=TOP`, `LEFTPADDING=4`, `RIGHTPADDING=8`, `TOPPADDING=3`, `BOTTOMPADDING=6`
- Column widths: 9.2cm each (A4 - 2×1.4cm margins = 18.2cm body, split evenly)

This produces a printable, professional-looking handout that looks like editorial copy rather than a worksheet. Same data as the plain variant, different visual register.

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

**Trailing period trap (Sept 21 2026):** when the POS tagger normalizes words via `clean = wl.rstrip(".,;:!?")`, the period on the last word gets stripped and never put back. The HTML rebuild `" ".join(word for _, word in tagged)` then renders sentences like `"... afternoon"` with no period. Fix in `sentence_html()`:

```python
def sentence_html(tagged):
    parts = [f'<font color="{COLORS[tag].hexval()}"><b>{word}</b></font>'
             for tag, word in tagged]
    # Only add a period if the last token doesn't already end in "."
    last = tagged[-1][1] if tagged else ""
    suffix = "" if last.endswith(".") else "."
    return " ".join(parts) + suffix
```

Caught visually on the 15-word PDF — sentences rendered without final periods, made the worksheet look unfinished. Same fix applies to comma/question-mark/exclamation endings.

**Auto-pad/trim pitfalls (Sept 21 2026, 15-word corpus):** when expanding a shorter corpus to N words via auto-padding (inserting time adverbs like `today / now / every day` at the end), three bug classes showed up:

1. **Stripping the period instead of inserting** — first version of `auto_fix_corpus.py` did `kept = words[:-to_remove]` thinking the period was on `words[-1]`. The last word with the period (`"shift."`) was removed entirely. The sentence ended up incomplete. **Fix:** keep the last word attached to the period, remove interior words: `body = words[:-1]; kept = body[:-to_remove] + [last_word]`.

2. **Removing determiners instead of optional adverbs** — second version stripped articles (`his`, `the`) to hit the count. Sentences rendered ungrammatical ("fresh rice in large flooded field" missing "his"). **Fix:** prioritize removals — drop optional adverbs (`very / really / quite / carefully`) FIRST, articles LAST. Order: adv > time-adv > article.

3. **Duplicate insertions** — third version picked the first matching insertion combination without checking for duplicate words already in the sentence. Result: "every single day every single morning" appended to many sentences — function-wise correct (15 words) but reads badly. **Fix:** when iterating insertion combos, skip any that share a word with the existing sentence. Or: cap at most one insertion of each time adverb.

**Net result for the 15-word corpus:** the auto-expander produced ~85 correct sentences + ~15 that read awkwardly. The awkward 15 are still shipped (they're 15 words, they don't break the worksheet) but flagged as a known limitation in `references/15-word-sentence-corpus.md`. For future corpora at this complexity, hand-write the 15-word sentences from scratch instead of auto-padding — better naturalness at the same determinism cost.

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

**Density is real, measure it.** When the user says "we can fit many more sentences on each page," they're right — assume there's wasted vertical space and PROVE IT with vision before deciding. Default sequence:

1. Render page 1 to PNG via `pdftoppm -r 200`
2. `vision_analyze` with: "Where is unused space? Bottom of page? Between sentences? Estimate how much is wasted."
3. The actual answer is usually 30-50% of the page (A4 = 29.7cm tall, your 10-sentence layout uses ~15cm).
4. Bump density: 10/page → 14/page → 20/page. Drop per-sentence tense checklist first if it's bloating each row. Stop when sentences start wrapping awkwardly (sentences > 12 words wrap to 3 lines, kill density).
5. Re-render and re-audit. Don't claim "fully packed" until you've actually checked.

For 15-word sentences (which wrap to 2-3 lines each), the practical ceiling is 20 sentences/page in 2 columns × 10 rows, dropping the per-sentence tense checklist (the legend at top of every page already names them). 5 pages total for 100 sentences. Going denser than 20 starts eating into readability.

**Iterate on the visual.** User will ask for: split into 2 PDFs, 7 per row, 14 per page, 28 per page, single line, no lines, BlankSpace zones, different colors, color articles/prepositions separately, separate CONJUNCTION category, DET vs ART split, adjective-vs-adverb context fixes. Each is a small adjustment to the layout, not a redesign. Ship the version, wait for the next ask.

**Multi-pass loop when user audits:** when user gives word-by-word color corrections (their enumerated list of "this word should be X, that word should be Y"), fix exactly what they listed, rebuild, and re-verify ALL pages — not just the ones they flagged. New errors often appear in nearby sentences from the same auto-tag logic. Don't stop after one fix round; iterate until user explicitly says "ship it" or moves on. See the multi-pass verification loop section under "7+ category refinement" for the exact protocol.

## Output delivery

Always deliver as `MEDIA:/absolute/path/to/file.pdf` in the response so the user gets it natively on Telegram. Don't make them download from a link.

## Reference data

- `references/6-word-sentence-corpus.md` — the 100-sentence 6-word corpus (verified, 6 words each, all 600 word-tags hand-curated), plus the 38-question rapid-fire oral drill list, plus the override map for the heuristic POS classifier. Use as the canonical data when regenerating either PDF.
- `references/15-word-sentence-corpus.md` — the 100-sentence 15-word corpus (verified, 15 words each), generated for Bhawna's working-memory ladder (15 → 20 → 25). Same POS tagging pipeline, no BlankSpace write-line (sentences wrap to 2-3 lines each). Current layout is 2 col × 10 row = 20 sentences/page, 5 pages total. Reference doc records known limitations: plural -s noun mis-tagging (rule documented in SKILL.md) and auto-padding filler artifacts in ~15 sentences.
- `scripts/build_15word_pdf.py` — generator for the COLORED POS version. Hand-written 100-sentence corpus inline. 5 pages, 20 sentences/page. Use this when the user wants POS color coding for grammar learning.
- `scripts/build_15word_plain.py` — generator for the PLAIN TEXT version. Same 100 sentences, no colors/legend/checkboxes/decorations. 3 pages, 40/40/20 sentences per page. Use this when the user says "no color," "no marking," "black and white," "plain text," or just wants a clean reading-and-discussion sheet.
- `scripts/auto_fix_corpus.py` — INTENTIONALLY DISABLED. The original smart auto-pad/trim script that produced broken sentences. Retained only as a stub pointing to the manual-first/script-second iteration pattern. Do NOT use for new corpora — hand-write them and verify with Python's word count.
- `references/15-word-density-and-color-audit.md` — Sept 21 2026 session notes: density patterns for long sentences (20/page color, 40/page plain), the plural -s noun mis-tagging fix, the manual-first/script-second iteration loop, auto-pad failure modes, the 15-word corpus tense distribution, the high-level vocabulary preference for ESL materials, and the plain-text variant layout.
- `references/7-category-color-scheme.md` — the full 7-category (SUBJ/VERB/OBJ/DET/PREP/ADV/CONJ) color palette with hex codes, the adjective-vs-adverb context disambiguation table, and the audit-findings list of words that get misclassified (and, every, last, next, home, out, etc.). Use this when the user pushes back on color quality and demands word-by-word exhaustiveness.
- `references/vocab-sheet-density-and-layout.md` — the canonical 2-column dense vocab-sheet pattern (Plant Wars, 159 entries, 6 pages, T2+T3 only). Includes the density math, working margins, tier-color hex values, and example-generation rules. Use as the starting template for any "list these words with definitions" handout.
- `references/local-corpus-ielts-source.md` — Sept 22 2026: the local `/home/Hermes/repos/IELTS_Trainer/passages/` (159 real Cambridge IELTS tests) is now the canonical source for any IELTS-level worksheet. Covers extraction pipeline, topic spread, pitfalls (curly quotes, OCR artifacts, dedup), and when to fall back to web. Use this before any hand-written or LLM-generated corpus.
- `references/pretty-plain-variant-layout.md` — Sept 22 2026: the "pretty PDF" interpretation when user asks for a clean printable handout. Times-Roman serif, muted gray italic sentence numbers, 2 col × 10 row = 20 sentences/page, density math, code pattern. Distinct from both the Helvetica plain variant and the 6-color coded variant.
- `scripts/extract_ielts_corpus.py` — Sept 22 2026: the working extraction script. Configurable (WORD_COUNT, TOTAL, SAMPLE_TESTS), strips ieltsfever page-header noise, trims to N words, asserts word count, deduplicates, writes output to `/tmp/ielts_corpus/final_corpus_wN.txt`. Use as the starting template for any IELTS worksheet corpus.
- `references/ocr-noise-filter-checklist.md` — Sept 22 2026: the regex patterns + word-ending blacklist for rejecting OCR-broken / truncated sentences from scraped IELTS sources. Curly-quote stripping, paragraph-label detection, joined-word detection, sentence-boundary detection for multi-line pdftotext output. Apply ALL of these when extracting from any non-clean source.
