---
name: honest-research-extraction
description: Use when extracting from sources. Classify, never fabricate.
category: research
tags: [research, extraction, methodology, anti-fabrication, source-quality]
version: 1.0.0
triggers:
  - "extract from these HTML files"
  - "produce a research artifact from these sources"
  - "synthesize coverage across these pages"
  - "build a knowledge base from this corpus"
  - "extract structured data from these raw pages"
---

# Honest Research Extraction

The most common failure in corpus-based extraction: **fabricated attribution**. The agent fills the topic structure with plausible content, and downstream systems attribute it to named sources that don't actually contain it.

This skill prevents that by forcing explicit classification of source quality *before* any extraction begins.

## When to Use This Skill

Load this skill when:

- User provides files/URLs and asks for structured extraction bounded by specific topics
- User says: "synthesize coverage," "build a research artifact," "produce a knowledge base from these raw HTML pages"
- Files are pre-captured (raw HTML, archived PDFs, JSON dumps) — their content is fixed and re-fetching won't help

## When NOT to Use This Skill

- **Live URL fetching** where you can re-navigate if a page is empty → use `research-methods` instead
- **Single-page summarization** — no corpus to classify
- **Explicit gap-filling requests** where the user wants general knowledge filled in (e.g., "write a resume guide for software engineers")

> **Note:** The "no fabricated output" rule applies when your output claims to be backed by named sources. If the user wants expert-level content from a sparse corpus, clarify this before proceeding.

## The Four-Step Pattern

### Step 1 — Classify Every Source Before Writing Anything

For each supplied file, score three dimensions:

| Dimension | What to Check | Threshold |
|-----------|---------------|-----------|
| **Body text length** | Strip `<script>`, `<style>`, `<nav>`, `<footer>`, then count characters | Below ~500 chars = effectively empty |
| **Topic relevance** | Does the `<title>`, `<meta>`, or canonical URL match what the user asked for? | Generic home page / login wall / redirect page = irrelevant |
| **Content density** | After stripping noise, what proportion is substantive vs. boilerplate? | A 50KB page with 200 chars of actual content = empty |

Classify each file into one of:

[RELEVANT]     — Contains extractable content on the requested topic
[IRRELEVANT]   — Wrong topic, redirect, login page, etc.
[EMPTY]        — Technically accessible but no substantive content
Record this classification. **Do not proceed to extraction until all files are classified.**

### Step 2 — Report the Corpus State Explicitly

Before writing any artifact, state what you found:

Corpus of {N} files classified:
  - {X} RELEVANT (extracting from these)
  - {Y} IRRELEVANT (excluding from artifact)
  - {Z} EMPTY (excluding from artifact)

Topic coverage: {brief characterization}
**Why this matters:** Downstream systems (and users) need to know what the artifact actually represents. A "knowledge base" built from 1 relevant file out of 44 is not the same as one built from 43.

### Step 3 — Extract ONLY from RELEVANT Sources

Extract structured content only from files classified as `[RELEVANT]`. For each piece of content, track its source file.

If your extraction would require content from `[EMPTY]` or `[IRRELEVANT]` files:

- Mark that section as `[NO-SOURCE]` or `[CORPUS-GAP]`
- Do not fabricate attribution
- Do not generalize from adjacent files unless the content explicitly crosses that boundary

### Step 4 — Mark Artifact Boundaries Clearly

At the top of your output artifact, include:

## Source Attribution

This artifact was produced from a corpus of {N} files.
{X} files contained relevant content on the requested topics.
{Y} files were empty or inaccessible.
{Z} files were off-topic.

### Files with Extracted Content
- [file-01.html] — {topic summary}
- [file-03.json] — {topic summary}
...

### Files Without Extracted Content
- [file-02.pdf] — EMPTY (captured as login wall)
- [file-05.html] — IRRELEVANT (site homepage, not article)
...
If the corpus has significant gaps relative to the user's request, say so explicitly:

> "The corpus contains limited coverage of [topic]. The following sections reflect what was found in the sources. Additional topics requested are not represented due to insufficient source material."

## Anti-Fabrication Checklist

Before finalizing any extraction artifact, verify:

- [ ] Every piece of specific information has a cited source file
- [ ] No section heading exists without corresponding source content
- [ ] Statements about what the corpus *doesn't* contain are accurate
- [ ] The artifact header accurately reflects corpus composition
- [ ] No generalization from one file's content to cover another file's absence

## Example: Before and After

**Bad output** (fabricated attribution):
## Resume Formatting Best Practices

According to the corpus, recruiters spend 6 seconds scanning a resume...
**Good output** (honest extraction):
## Resume Formatting Best Practices

**Source coverage:** Found in 1 of 44 corpus files.

[file-12.html] mentions that hiring managers often scan resumes quickly, but does not provide specific timing data.

**Gap:** The corpus does not contain quantitative data on resume scan times. No fabricated statistics included.