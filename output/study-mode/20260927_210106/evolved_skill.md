---
name: study-mode
description: 'Knowledge-tree study mode. Use when Abhinav asks "how does X work", "explain Y", "tell me about Z", or requests study/research on a topic. Builds a persistent tree at ~/study/trees/<slug>/ with verified sources, drills lazily, exports to PDF. Triggers: study mode, explain, how does X work, tell me about, deep dive.'
category: productivity
---

# Study Mode

Knowledge-tree protocol for building persistent, source-verified study trees. Creates a branching structure at `~/study/trees/<slug>/` with lazy depth expansion and PDF export capability.

**Spec reference:** Read `~/study/SPEC.md` for the full JSON schema, node structure, and examples. This file is the operational protocol — step-by-step execution.

---

## When to Use

**Activate study mode when user:**
- Asks "how does X work?" or "explain Y" and wants depth, not a one-liner
- Says "study mode", "deep dive", "I want to understand X properly"
- Wants research saved as a persistent, explorable tree
- Requests a PDF of research on a topic

**Do NOT activate when:**
- User wants a quick definition → just answer concisely
- User wants code review or debugging → use coderag or debugging skill
- User asks "what's the best X?" → that's a decision task, not study

---

## First Response Protocol

Every new study topic opens with this exact 4-element structure. No preamble, no exceptions.

🍞 **Main → [topic]**

[Topic] is [1-line definition]. You might care because [1-line relevance].

**To understand this, you need to know first:**
- [Prereq 1] — [1 line]
- [Prereq 2] — [1 line]
- [Prereq 3] — [1 line]

**Pick one** (or "skip all, go deep on [topic] directly"):
1. Drill into [Prereq 1]
2. Drill into [Prereq 2]
3. ...
N. Skip prereqs, explain [topic] in depth
**Rules:**
- Definition: 1 line only
- "Why care" relevance: 1 line only
- Prereqs: flat list, 1 line each, max 5 (if more exist, list top 5 and note "and N more")
- Wait for user selection before researching or gathering sources
- "Skip all, go deep" is always option N — user may already know prereqs

---

## Prerequisite Drilling

When user selects a prereq (e.g., option 1):

1. **Acknowledge the branch** with header `🍞 **[Prereq] → [Topic]` (parent chain visible)
2. **Define it** — what is this prereq, why does it matter for the parent topic
3. **List its own prereqs** (if any), following same 4-element opener format
4. **Wait for next selection**
5. **After user picks from a branch, mark that branch as explored** in the tree structure

**Lazy expansion principle:** Only research the branch the user picks. Don't pre-explore sibling branches. This keeps the tree dense where the user actually goes.

---

## Tree Building Protocol

### Initial Tree Setup

After user picks their first topic:

~/study/trees/<slug>/
├── tree.json          # Full tree structure
├── sources.json       # Verified sources with URLs
└── notes/
    └── <node-id>.md    # Expanded notes per node
**Slug generation:** Lowercase, hyphens, e.g., "kubernetes-networking" from "How does Kubernetes networking work?"

### Node Structure (per SPEC.md)

Each node contains:
- `id`: unique identifier
- `title`: short title
- `content`: synthesized explanation (2-5 paragraphs)
- `sources`: array of verified URLs with claim citations
- `children`: array of child node IDs
- `status`: "collapsed" | "expanded" | "verified"

### Source Verification Rules

- Every factual claim must cite a source
- Preferred sources: official docs, peer-reviewed papers, authoritative tutorials
- Cross-reference claims across 2+ sources when possible
- Mark unverified claims with `[unverified]` tag
- Never fabricate sources

---

## Skip-All Mode (Deep Dive Contract)

When user picks "skip all prereqs, go deep on X directly":

**This mode is risky.** Flat, uncompressed deep dives produce:
- Monolithic root nodes with no branching
- Harder to navigate and review later
- Coverage gaps because no prereqs forced systematic thinking

**To mitigate:**
1. Even in skip-all, **actively identify and list prereqs** as collapsed children in the tree
2. The deep dive itself is the root node, but prereq placeholders exist for future drilling
3. Structure the deep dive with clear H2 sections that map to what would have been prereqs
4. Add a `[skip-all mode]` flag to the root node metadata

**Goal:** Skip-all should produce the same coverage as drilling through prereqs — just faster and in one shot.

---

## PDF Export

When user requests PDF:

1. Generate `README.md` at tree root with:
   - Full tree structure (ASCII or markdown tree)
   - All node content expanded
   - Source citations inline
2. Use available tooling to convert markdown to PDF
3. Place at `~/study/trees/<slug>/export.pdf`
4. Confirm path to user

---

## Session Continuity

- If tree already exists at `~/study/trees/<slug>/`, ask: "You have an existing tree for [topic]. Continue from where you left off, or start fresh?"
- Load existing tree on continue
- Mark the last-explored node as "current" for context

---

## Quick Reference

| Action | Command |
|--------|---------|
| Start new tree | Use 4-element opener format |
| Drill into prereq | Acknowledge → define → list its prereqs → wait |
| Mark verified | Add source citations, update node status |
| Export PDF | Generate README.md → convert → confirm path |