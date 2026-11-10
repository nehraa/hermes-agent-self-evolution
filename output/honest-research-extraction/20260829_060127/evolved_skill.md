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

## Purpose

Prevent **fabricated attribution** — the most common failure in corpus-based research. Agents sometimes fill topic structures with plausible-sounding content and attribute it to named sources. This skill forces explicit classification of each source before writing any derived artifact.

## When to Load This Skill

Load **before** writing any extraction artifact from a user-supplied corpus:

- User provides files/URLs and asks for structured, topic-bounded extraction
- User says "synthesize coverage", "build a research artifact", "produce a knowledge base"
- Files are pre-captured (HTML, PDFs, JSON) — their content is fixed and cannot be refreshed

## When NOT to Load This Skill

- **Live URL fetching** where you can re-navigate if content is missing — use `research-methods` instead
- **Single-page summarization** — no corpus to classify
- **Gap-filling requests** where the user explicitly wants general knowledge (e.g., "write a resume guide for engineers"). The "no fabricated output" rule applies when output claims to be backed by named sources.

## Four-Step Pattern

### Step 1 — Classify Every File Before Writing Anything

For each supplied file, score three dimensions and record the result:

| Dimension | How to Measure | Threshold |
|-----------|----------------|-----------|
| **Body text length** | After stripping `<script>`, `<style>`, `<nav>`, `<footer>` | Below ~500 chars = effectively empty |
| **Title vs. expected topic** | Does `<title>` or canonical URL match what user asked for? | Generic home page / login page / error page = non-substantive |
| **Content-topic alignment** | Does body text contain relevant terms/concepts? | Absent or tangential = non-substantive |

**Classify each file as:**
- ✅ **Substantive** — contains directly relevant content for the extraction task
- ❌ **Non-substantive** — empty, generic, misaligned, or error page

### Step 2 — Report Classification Results

Before writing any artifact, present a summary:

Source Classification Summary:
- file1.html: ✅ Substantive (2,340 chars, topic matches)
- file2.html: ❌ Non-substantive (120 chars, generic landing page)
- file3.pdf:  ❌ Non-substantive (PDF extraction failed)
- file4.html: ✅ Substantive (4,120 chars, topic matches)
If most files are non-substantive, explicitly state:
> "X of Y supplied files contain substantive content. The following artifact draws only from verified substantive sources. No information from non-substantive files has been attributed."

### Step 3 — Extract Only from Substantive Files

Write your artifact using **only** the classified-substantive sources. For each claim or insight, cite the specific file it came from.

### Step 4 — Flag Gaps for User

If the user's requested topic structure has sections with no substantive source coverage:

Coverage Gaps:
- "Salary benchmarks" — no substantive source found
- "Remote work policies" — only 1 of 12 files addresses this
Do not fill gaps with general knowledge while implying sources back it.

## Example

**User request:** "Extract structured resume tips from these 44 HTML files."

**Your response:**
> Analyzed 44 files. Only 1 (resume-sample-tech.pdf) contains substantive resume content. The other 43 are login pages, empty shells, or generic job board templates.
>
> **Artifact:** Derived exclusively from resume-sample-tech.pdf.

## Key Principle

The goal is **gap transparency at storage time**. If sources are empty, say so. Downstream pipelines cannot fix attribution errors that are already embedded in stored artifacts.