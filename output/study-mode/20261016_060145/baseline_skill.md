---
name: study-mode
description: 'Knowledge-tree study mode. Use when Abhinav asks "how does X work", "explain Y", "tell me about Z", or requests study/research on a topic. Builds a persistent tree at ~/study/trees/<slug>/ with verified sources, drills lazily, exports to PDF. Triggers: study mode, explain, how does X work, tell me about, deep dive.'
category: productivity
---

# Study Mode

Knowledge-tree protocol for studying any topic. Builds persistent trees at `~/study/trees/<slug>/` with source verification, lazy depth expansion, and PDF export.

**Authoritative spec:** `~/study/SPEC.md` (read it for full schema, JSON layout, examples). This file is the operational protocol — what to do turn-by-turn.

---

## When to use

- User asks "how does X work?" or "explain Y" and wants depth, not a one-liner
- User wants to study/research a topic and have the journey saved
- User says "study mode", "deep dive", "I want to understand X properly"
- User asks for a PDF of research on a topic

**Don't use when:**
- User wants a quick definition (just answer it, no tree)
- User wants code review or bug fix (use coderag / debugging skill)
- User asks "what's the best X" — that's a decision, not a study

---

## First response protocol

When user opens a study topic, the first response is **always** the same 4-element opener. No exceptions, no preamble.

```
🍞 **Main → [topic]**

[Topic] is [1-line definition]. You might care because [1 line].

**To understand this, you need to know first:**
- [prereq 1] — [1 line]
- [prereq 2] — [1 line]
- [prereq 3] — [1 line]

**Pick one** (or "skip all, go deep on X itself"):
1. Drill into [prereq 1]
2. Drill into [prereq 2]
3. ...
N. Skip prereqs, explain [topic] in depth directly
```

Rules:
- 1-line definition, 1-line "why care" — never more
- Prereqs in flat list, each one line — max 5 in opener (if more exist, top 5, mention "and N more")
- Wait for user pick before gathering sources. Don't pre-research all prereqs.
- "Go deep on X itself" is always an option — user might already know the prereqs

---

## ROOT CAUSE OF FLAT-SURVEY FAILURES — skip-all mode contract

The data-compression tree (Sep 22 2026) shipped flat, gappy, and partly unverified **specifically because the user picked "skip all prereqs, go deep on X itself."** The original protocol treated skip-all as "compress the whole topic into one root node and call it done." That mode has NO safeguards — no branching, no lazy re-verification, no coverage pressure. Three failures cascade:

1. No branching (no children written, root node carries everything)
2. No gap closure (everything "missing" lives in §10 because there was no drill pressure to fill it)
3. Shallow verification (one pass = verify once, move on, never re-check)

**Fix: skip-all mode still produces a real tree, just at depth-1, with explicit top-level children.** The user is saying "I know the prereqs, don't waste time teaching me info theory" — not "give me a 400-line survey." Honor the intent.

### Skip-all mode protocol (when user picks "skip all, go deep on X")

1. **Identify the 3-5 top-level children of X.** These are the natural sub-domains: for compression → lossless general-purpose, lossy image, video, audio, decision-tree. Not prereqs — actual children of X.
2. **Create one node file per child** at depth-1 (`01-lossless-general.md`, `02-lossy-image.md`, etc.). Each gets its own sources, its own weight, its own verification.
3. **Each child node must satisfy the 3 quality gates** (weight, gaps closed, verified numbers).
4. **Root node** = table of contents + the one thing that's NOT a child (the cross-cutting "core idea" — LZ77 + Huffman in compression's case). Plus the decision tree at the end. Keep it tight.
5. **User can still drill into any child** the same way they'd drill into a prereq. The tree is real; the prereq skipping was just about not teaching foundations they already know.

### Skip-all response template

```
🍞 Main → [topic] (skip-all mode)

You picked skip-all. Building a real tree anyway — just at depth-1 with X's natural children instead of prereqs.

Top-level children I'll cover:
- [child 1] — [1 line, weight=core]
- [child 2] — [1 line, weight=important]
- [child 3] — [1 line, weight=context]
- [child 4] — [1 line, weight=legacy]

Pick one to drill, or "do them all and ship" to have me cover each in turn and produce the PDF.
```

### Anti-pattern (what NOT to do in skip-all mode)

❌ One root node file = flat survey, no children, no branching
❌ "What's missing" footnote for things I could verify
❌ Numbers verified once and never re-checked
❌ Same depth for core vs legacy sections
❌ Treating skip-all as permission to skip the quality gates

### Apply the quality gates INSIDE skip-all mode

The 3 hard quality gates (section weighting, gap closure, verification depth) apply to **every** node, including skip-all children. A child marked `weight=legacy` gets 1 line; a child marked `weight=core` gets the full pipeline. Gaps closed line at the end of each child. Numbers verified to primary source. No exceptions for skip-all.

---

## When user picks a node (e.g. "drill into prereq 1" or "go deep on X")

### Step 1: Gather sources
- Web search for primary sources (papers > textbooks > Wikipedia > blogs)
- Read top results, identify 2-N sources that cover the node
- For fast-moving topics (AI, security), filter to <2yr unless foundational
- Stop when claims are verifiable — not at a fixed count

### Step 2: Write the node
- Create `~/study/trees/<slug>/nodes/NN-<name>.md` with the format from SPEC §3
- Update `~/study/trees/<slug>/tree.json` with the new node + sources

### Step 3: Reply with the per-node report
```
🍞 **Main → [topic] → [current node]**

## What's deep enough (the meat)
- [N claims with inline citations]

## What's shallow (1 line each)
- [claim] — [1 line]
- [claim] — [1 line]

## Sources
- S001: [cite]
- S002: [cite]

## Worth going deeper from what I read
- **[branch A]** — [1 line why interesting]
- **[branch B]** — [1 line why interesting]
- **[branch C]** — [1 line why interesting]

## What's tangential (probably skip)
- D, E — parked for later if you want

**Pick:**
1. Drill into branch A
2. Drill into branch B
3. Drill into branch C
4. Move on to next main node
5. Park D/E for later, move on
6. "Done with this topic — make the PDF"
```

### Step 4: Branching behavior
- **No fixed budget.** Number of branches = number of interesting things in the sources (1 to 5+)
- **User picks** — never assume
- **Park** = save in `tree.json → parked_branches[]`, surface at end of topic
- **Spine rule:** current node = active spine. Topic root only stays in breadcrumb
- **Interruptible at any depth** — if user says "ok done", we move on

---

## Source verification rules (hard contract)

1. **Primary > secondary.** Paper > textbook > Wikipedia > blog. Blog-only → `[blog-only]`
2. **Cite inline.** Every paragraph: `(Author, Year)` / `(URL)` / `[my synthesis — no external source]`
3. **Conflict flag.** Two sources disagree → both quoted + "your call"
4. **Recency.** AI/security/markets/climate: >2yr = `[stale]` unless foundational

**Source count not fixed** — gather until claims are accurate, not until a number.

---

## Filesystem operations

```bash
# Create new topic tree
mkdir -p ~/study/trees/<slug>/nodes ~/study/trees/<slug>/sources

# After writing a node, update tree.json (use patch tool, not full rewrite)
# After ending topic, generate PDF:
python3 ~/study/pdfgen.py <slug>

# View tree
python3 ~/study/viewer.py tree <slug>

# Search across all trees
python3 ~/study/viewer.py search "query"

# Consolidated view (cross-topic patterns)
python3 ~/study/viewer.py consolidated
```

---

## Tooling notes

- `reportlab` already installed (used for worksheets)
- `mermaid` CLI optional — depth graph falls back to ASCII if missing
- Trees are NOT git-tracked by default; user can add later
- One folder per topic, never split trees across folders
- Slug = kebab-case, max 5 words, e.g. `hippocampal-replay-sleep`

---

## Hard quality gates (must pass before any node is considered done)

These were learned from the data-compression tree (Sep 22 2026) where all three failed simultaneously. Every node MUST satisfy them before the per-node report goes out.

### Gate 1 — Section weighting (no flat-survey disease)
Surveys that treat every topic with equal weight are useless. Each node must declare a **weight** in its frontmatter:

```
**Weight:** core | important | context | legacy
```

Rules:
- **Core** = the mechanism you cannot understand the topic without (LZ77 + Huffman for compression; DCT + quantization for JPEG; inter-frame prediction for video). These get the deepest drill.
- **Important** = a major tool/format in current use (zstd, Brotli, AV1, Opus). Drill depth: full mechanism + when-to-pick.
- **Context** = historical or background that frames the core (LZMA, Snappy, bzip2). Drill depth: 1-paragraph "where it fits" + why it's not the default.
- **Legacy** = superseded but still shipping (H.264 for max reach, bzip2). Drill depth: 1-line "still works because X."

When sources are gathered, **weight decides depth budget**, not my mood:
- Core = full pipeline, every step explained, every number verified
- Important = mechanism + decision criteria
- Context = 1 paragraph + 1 "why not core"
- Legacy = 1 line + compatibility constraint

**Anti-pattern:** treating bzip2 and zstd at the same depth because they both compress text. bzip2 is legacy; zstd is core.

### Gate 2 — Gap closure (no "what's missing" footnote for things you could verify)
Every node's report ends with a **Gaps Closed** line, not a "what's missing" afterthought:

```
**Gaps closed in this node:** info-theory (Shannon entropy, arithmetic coding), streaming (HTTP Content-Encoding vs Transfer-Encoding), hardware codecs (Intel QSV generation matrix)
```

Rules:
- If §10 "what's missing" of any node would name a topic, the node is **incomplete** — go gather sources for it before claiming done
- The gap-closure paragraph gets inline citations, same as the rest
- Only acceptable "missing" items: (a) genuinely tangential to the asked topic, (b) explicitly out-of-scope by user direction ("don't go into math"), (c) sources cannot be found after a real search
- Empty "Gaps closed" line on a node that has gaps = the node failed Gate 2

### Gate 3 — Verification depth (no floating [unverified] on numbers)
Numbers and dates that anchor the node must be **verified to a primary source**, not to a summary site. Specifically:

- Codec compression ratios (VVC 50%, AV1 vs HEVC, etc.) → spec body, standards body, or the original benchmark paper
- "Hardware decode since YYYY" → manufacturer announcement or Wikipedia with a primary-source footnote
- Speed benchmarks (MB/s, GB/s) → label as "varies by hardware" if from a single source, OR cite two independent benchmarks showing same order of magnitude
- AV1 vs H.265 benchmarks → must distinguish PSNR from VMAF from SSIM; Meta 2018 paper is PSNR-based, not VMAF. Get this right.

**Process when a number is suspect:**
1. `web_search` for the claim's primary source (RFC, standards body, original paper)
2. If found → upgrade citation from `[blog-only]` to verified with the primary URL
3. If NOT found → label `[unverified — could not locate primary source after search]` and remove the number from any summary table

**Anti-pattern:** carrying forward a "since 2016" claim because a comparison table said so, when the actual year was 2017. Always verify year claims to a second source.

**Anti-pattern:** citing a benchmark from one blog without acknowledging hardware variance.

---

## Anti-patterns

❌ Writing a wall of text before user picks prereq
❌ Pre-researching all prereqs before user picks one
❌ Fixed branch counts ("I'll surface 3 branches")
❌ Averaging conflicting sources silently
❌ Hiding unverified claims — tag them `[unverified]`
❌ Skipping the breadcrumb at the top of replies
❌ Going off-topic from user's main ask to chase a tangent
❌ Producing the PDF without asking first
❌ Treating parked branches as "lost" — surface them at end of topic
❌ **Flat survey** — every section same depth, no weighting (Gate 1)
❌ **"What's missing" footnote** for things I could have verified (Gate 2)
❌ **Floating unverified numbers** on year/percent claims (Gate 3)
❌ Citing a benchmark without naming what it measured (PSNR vs VMAF vs SSIM)
❌ "Since 2016" claims without verifying the year against a second source

---

## When the topic is done

User says "done" / "make the PDF" / "wrap up" / "we're good":

1. Confirm all explored nodes are written to disk
2. Show parked branches: "You parked: A, B, C. PDF includes a 'Parked for later' appendix. Make PDF anyway? (y/n)"
3. Run `python3 ~/study/pdfgen.py <slug>`
4. Show PDF path, deliver via Telegram if user is on mobile
5. Don't push the user toward the next topic — wait for their next ask