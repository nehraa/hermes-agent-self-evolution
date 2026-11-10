---
name: honest-research-extraction
description: Use when extracting from sources. Classify, never fabricate.
category: research
tags: [research, extraction, methodology, anti-fabrication, source-quality]
version: 1.1.0
triggers:
  - "extract from these HTML files"
  - "produce a research artifact from these sources"
  - "synthesize coverage across these pages"
  - "build a knowledge base from this corpus"
  - "extract structured data from these raw pages"
  - "analyze these documents and summarize"
  - "create a report from these files"
---

# Honest Research Extraction

A methodology for corpus-based research tasks that prevents **fabricated attribution** — the failure mode where an agent fills requested topic structures with plausible-sounding content attributed to named sources that contain nothing relevant.

## Problem Statement

When users supply a corpus of files and ask for structured extraction, a common failure occurs:

1. Agent receives 44 files, only 1 contains relevant content
2. Agent generates structured output covering all requested topics
3. Downstream systems assume the content comes from the corpus
4. 43 files of generic advice get attributed to named sources

**The fix**: Classify source quality *before* writing anything, and make gaps explicit at storage time.

## When to Load This Skill

Load this skill when ALL of these conditions are true:

- User provides a list of files, URLs, or a corpus directory
- Request includes a structured output template (topics, sections, fields)
- The files are pre-captured (HTML archives, PDFs, JSON dumps, local files)
- Downstream systems will attribute output to the named sources

**Typical trigger phrases:**
- "Extract from these HTML files"
- "Synthesize coverage across these pages"
- "Build a knowledge base from this corpus"
- "Produce a research artifact from these sources"
- "Analyze these documents and create a [report/database/artifact]"

## When NOT to Load This Skill

| Scenario | Alternative Skill |
|----------|-------------------|
| Live URL fetching with retry capability | `research-methods` |
| Single-page summarization | None needed — no corpus to classify |
| User explicitly wants general knowledge填充 | None needed — no source attribution claim |
| Refreshing stale cached content | `research-methods` |

## The Four-Step Extraction Pattern

### Step 1 — Classify Every Source Before Writing Anything

For each file in the corpus, evaluate and score THREE dimensions:

#### Dimension A: Body Text Length

python
# Strip noise elements
strip_tags = ['script', 'style', 'nav', 'footer', 'header', 'aside', 'iframe']
# Count remaining text characters
body_length = len(strip_elements(html, strip_tags).get_text())
| Length | Classification | Action |
|--------|----------------|--------|
| < 500 chars | **Empty** | Flag as non-contributory |
| 500–2000 chars | **Sparse** | Include verbatim, low confidence |
| 2000–10000 chars | **Adequate** | Full extraction expected |
| > 10000 chars | **Substantial** | Prioritize for dense topics |

#### Dimension B: Topic Relevance

Compare the file's `<title>`, `<meta description>`, or canonical URL against the user's stated extraction goal.

| Signal | Classification |
|--------|----------------|
| Title matches extraction topic directly | **High relevance** |
| Title partially overlaps or is ambiguous | **Moderate relevance** |
| Title is generic (home, login, error) | **Low relevance** |

#### Dimension C: Content Quality

Examine the first 500 words of body text:

| Signal | Classification |
|--------|----------------|
| Dense paragraphs, topic-specific terminology | **High quality** |
| Lists, summaries, or thin content | **Moderate quality** |
| Placeholder text, lorem ipsum, or boilerplate | **Low quality** |

#### Composite Score

SOURCE_QUALITY = (body_length_score * 0.4) + (topic_relevance_score * 0.35) + (content_quality_score * 0.25)
| Score | Classification | Include in Output? |
|-------|----------------|-------------------|
| 0.0–0.25 | **Non-contributory** | No — document exclusion |
| 0.26–0.50 | **Marginal** | Include verbatim only, no synthesis |
| 0.51–0.75 | **Contributory** | Full extraction |
| 0.76–1.0 | **Primary** | Prioritize for dense topics |

### Step 2 — Build the Gap Map

Before writing any extracted content, produce a matrix:

Topic Coverage Matrix
=====================

Topic: "Machine Learning Model Evaluation"
├── Required sources: 3
├── Contributory sources found: 1 (file-023.txt)
├── Marginal sources: 2 (file-007.txt, file-019.txt)
└── COVERAGE GAP: 2 sources missing

Topic: "Data Pipeline Architecture"
├── Required sources: 2
├── Contributory sources found: 2 (file-012.html, file-031.pdf)
└── COVERAGE COMPLETE
This gap map serves two purposes:

1. **Alert the user** to insufficient corpus coverage before they act on incomplete output
2. **Scope the artifact** — know which sections must be marked as "insufficient data"

### Step 3 — Extract Verbatim, Then Synthesize

#### Extract Phase

For each contributory source:

- Pull relevant passages **verbatim** with `<cite>` tags or source references
- Preserve original phrasing — do not paraphrase during extraction
- Flag any passage that requires interpretation with `[interpretation needed]`

#### Synthesize Phase

For each topic in the extraction template:

| Condition | Synthesis Approach |
|-----------|-------------------|
| Coverage complete | Synthesize freely from contributory sources |
| Coverage partial | Synthesize with marginal sources, flag gaps explicitly |
| Coverage absent | Mark section as `## [Topic Name] — INSUFFICIENT DATA` |

**Never** fill gaps with general knowledge when the output template claims source backing.

### Step 4 — Produce the Artifact with Quality Metadata

Final output must include:

markdown
## Extraction Quality Report

### Corpus Summary
- Total files provided: 44
- Files classified as contributory: 1
- Files classified as marginal: 12
- Files classified as non-contributory: 31

### Topic Coverage
| Topic | Contributory Sources | Coverage Status |
|-------|---------------------|-----------------|
| ML Model Evaluation | 1/3 required | INCOMPLETE |
| Data Pipeline Architecture | 2/2 required | COMPLETE |

### Methodology
Sources were classified by: (1) body text length after noise stripping, 
(2) title/topic relevance, (3) content density. Synthesis was performed 
only where contributory sources existed. Gaps are marked explicitly.
## Anti-Fabrication Rules

1. **No general knowledge injection** when output claims source backing
2. **Verbatim preference** for marginal sources — paraphrase only for contributory+
3. **Gap transparency** — never silently omit topics with no coverage
4. **Source count accuracy** — each claim must map to actual source passages

## Example: Before and After

### Before (Fabrication)

## Decision Trees in Medical Diagnosis

Decision trees are commonly used in medical diagnosis due to their 
interpretability and ability to handle both categorical and numerical data...

[Sourced from: file-001.html, file-002.pdf, file-003.txt]
*Problem*: 3 sources provided, all non-contributory. The content is general knowledge, not extracted from sources.

### After (Honest Extraction)

## Decision Trees in Medical Diagnosis

[INSUFFICIENT DATA — No contributory sources identified]

The extraction request included 3 files for this topic.
Classification results:
- file-001.html: 234 chars body text, generic title → Non-contributory
- file-002.pdf: Password-protected, cannot extract → Non-contributory
- file-003.txt: 89 chars, mostly navigation links → Non-contributory

Recommendation: Provide additional sources or revise extraction scope.
## Quick Reference

IF user provides corpus AND requests structured extraction:
  → LOAD honest-research-extraction
  → Classify every source (Step 1)
  → Build gap map (Step 2)
  → Extract verbatim, then synthesize (Step 3)
  → Include quality metadata (Step 4)
  → NEVER fabricate when source backing is claimed