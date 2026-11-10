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

Use this skill when extracting structured artifacts from user-supplied source files.

## Purpose

Prevent **fabricated attribution** — the most common failure in corpus-based research. The agent produces plausible content and attributes it to sources that don't actually contain that content. This skill makes content gaps explicit at extraction time rather than allowing them to contaminate downstream outputs.

## When to Load

Load **before** writing any extraction artifact from a user-supplied corpus:

- User provides files/URLs and asks for structured, topic-bounded extraction
- User says: "synthesize coverage", "build a research artifact", "produce a knowledge base", "extract structured data"
- Files are pre-captured (HTML, PDFs, JSON) — content is fixed; you cannot re-fetch

## When NOT to Load

- Live URL fetching where you can re-navigate if a page is empty → use `research-methods` instead
- Single-page summarization with no corpus
- Tasks where user explicitly wants general knowledge filling (e.g., "write a resume guide") — the "no fabricated output" rule applies only when output claims to be backed by named sources

## The Four-Step Pattern

### Step 1 — Classify Every File Before Writing Anything

Score each file on three dimensions and record the result:

1. **Body text length** after stripping `<script>`, `<style>`, `<nav>`, `<footer>`. Below ~500 chars = effectively empty.

2. **Title vs. expected topic** — does the file's `<title>` (or canonical URL) match what the user asked for, or is it a generic home page / login redirect / 404?

3. **Semantic match** — does the visible body text actually address the stated extraction goal, or does it contain only boilerplate, placeholder text, or unrelated content?

Classify each file as:

| Classification | Definition |
|----------------|------------|
| **Substantive** | Has relevant, usable content matching the extraction goal |
| **Empty** | No usable content (failed capture, wall text, redirects) |
| **Off-topic** | Content exists but doesn't match the extraction goal |

### Step 2 — Report Coverage Before Producing Any Artifact

Present a summary before generating output:

## Source Classification

| File | Classification | Notes |
|------|----------------|-------|
| resume_001.html | Substantive | Contains job history, skills |
| resume_002.html | Empty | Login wall, no body text |
| resume_003.html | Off-topic | Contains corporate org chart |
...

Coverage: 1/3 files substantive (33%)
This lets the user:
- Confirm the classification is accurate
- Provide additional sources for gaps
- Adjust the extraction scope

### Step 3 — Extract Only from Substantive Sources

Build the extraction artifact using **only** content from files classified as substantive. For each extracted fact:

- Cite the specific source file it came from
- Include verbatim text for key passages
- Never extrapolate beyond what the source actually says

### Step 4 — Explicitly Flag Uncovered Gaps

List every topic or subtopic from the extraction goal that has **no** corresponding substantive source. Present as:

## Known Gaps (no source coverage)

- Education history: No substantive source found
- Certifications: No substantive source found
Do **not** fill these gaps with general knowledge while implying they came from sources. If the user wants that content, they must provide supporting sources.