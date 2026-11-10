---
name: study-mode
description: 'Knowledge-tree study mode. Use when Abhinav asks "how does X work", "explain Y", "tell me about Z", or requests study/research on a topic. Builds a persistent tree at ~/study/trees/<slug>/ with verified sources, drills lazily, exports to PDF. Triggers: study mode, explain, how does X work, tell me about, deep dive.'
category: productivity
---

# Study Mode

Knowledge-tree protocol for studying any topic. Builds persistent trees at `~/study/trees/<slug>/` with source verification, lazy depth expansion, and PDF export.

**Authoritative spec:** `~/study/SPEC.md` (read it for full schema, JSON layout, examples). This file is the operational protocol — what to do turn-by-turn.

---

## When to Use

**Activate study mode when user:**
- Asks "how does X work?" or "explain Y" and wants depth, not a one-liner
- Says "study mode", "deep dive", or "I want to understand X properly"
- Wants to study/research a topic and have the journey saved
- Asks for a PDF of research on a topic

**Do NOT activate when user:**
- Wants a quick definition (just answer it, no tree)
- Wants code review or bug fix (use coderag / debugging skill)
- Asks "what's the best X" — that's a decision, not a study
- Needs immediate troubleshooting (answer directly, build tree later if they want the full picture)

---

## First Response Protocol

When user opens a study topic, the first response is **always** the same 4-element opener. No exceptions, no preamble.

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
**Rules:**
- 1-line definition, 1-line "why care" — never more
- Prereqs in flat list, each one line — max 5 in opener (if more exist, show top 5, mention "and N more")
- Wait for user pick before gathering sources. Don't pre-research all prereqs.
- "Go deep on X itself" is always an option — user might already know the prereqs

---

## Skip-All Mode Contract

**Why this contract exists:**

Flat, gappy, unverified trees result from treating "skip all prereqs, go deep on X itself" as "compress the whole topic into one root node." That approach has no safeguards — no branching, no lazy re-verification, no coverage pressure.

**The solution:**

When user skips prereqs, you MUST still build a proper tree structure:

1. **Create root node** for the main topic
2. **Branch immediately** into 4-6 sub-topics (facets of the main topic, not prereqs)
3. **Mark depth levels explicitly**: root = L0, sub-topics = L1
4. **Apply lazy expansion**: give L1 overview + one L2 drill per sub-topic
5. **Flag coverage gaps**: note any sub-topics that need future drilling
6. **Verify sources** as you go — at least 2 sources per claim at L0/L1

**Skip-all does NOT mean:**
- ❌ One monolithic root node with everything compressed
- ❌ No branching structure
- ❌ Skip source verification
- ❌ No depth levels marked

**Skip-all DOES mean:**
- ✅ User knows the prereqs already
- ✅ Go straight to main topic depth
- ✅ Still build proper tree with branches
- ✅ Still verify sources
- ✅ Still mark depth levels

---

## Lazy Depth Expansion

Trees grow on demand, not upfront:

1. User picks a node (or we recommend one)
2. We drill that node: gather sources, write content, mark as "expanded"
3. Unexpanded nodes show only title + one-line description
4. Tree never pre-loads all content — only what's requested

**Drill workflow:**
1. User (or we) selects a node to expand
2. Gather 2-3 verified sources on that sub-topic
3. Write content: 200-500 words, structured with headers
4. Add sub-nodes if topic branches further (max 5 children)
5. Update tree JSON, mark node as expanded

---

## Source Verification

Every factual claim needs a source. Rules:

- **Minimum:** 2 sources per expanded node
- **Types accepted:** official docs, peer-reviewed papers, reputable tutorials, well-voted Stack Overflow answers
- **Types rejected:** random blog posts, opinion pieces, single-source claims
- **Format:** `[Source Name](URL)` inline, full citation in node footer
- **Flag uncertain claims:** mark as `[UNVERIFIED - needs confirmation]`

---

## Tree Structure

Trees live at `~/study/trees/<slug>/` where `<slug>` is the topic URL-safe:

~/study/trees/<slug>/
├── tree.json        # Full tree data (see SPEC.md for schema)
├── sources.md       # Consolidated source list
├── exports/
│   └── <slug>.pdf   # Generated PDF exports
└── notes/
    └── <node-id>.md # Expanded node content (if stored separately)
**Node structure (JSON):**
json
{
  "id": "unique-id",
  "title": "Node Title",
  "depth": 0,
  "parent": null,
  "definition": "One-line definition",
  "expanded": false,
  "content": null,
  "sources": [],
  "children": ["child-id-1", "child-id-2"]
}
---

## PDF Export

User can request PDF at any time:

1. Run export command (see SPEC.md)
2. PDF includes: full tree outline + all expanded content
3. Unexpanded nodes show as: `[Topic Name] — expand to see content`
4. Sources appended at end
5. Save to `exports/<slug>.pdf`

---

## Error Handling

- **User picks non-existent node:** show available nodes, ask to re-pick
- **No sources found for claim:** mark `[UNVERIFIED]`, note "no reliable sources found"
- **Tree file corrupted:** show error, offer to rebuild from scratch
- **User wants to stop:** save current state, note what's expanded vs unexpanded
- **User wants to continue later:** tree persists, they can say "continue studying X"