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

# Honest Research Extraction — When Supplied Sources Are Mostly Empty

The single most recurring failure mode in corpus-based research tasks is **fabricated
attribution**: the agent fills the requested topic structure with plausible-looking
general advice, and the downstream pipeline attributes that advice to the named sources.
The cure is to make the gap explicit at storage time.

This skill captures the pattern that worked the first time this class of failure
was hit (a 44-file resume corpus, only 1 substantive file, 43 failed captures) and
that applies to every future "extract from these raw files" task.

## When to load this skill

Load BEFORE writing any extraction artifact from a user-supplied corpus. The signals
are:

- User gives a list of files/URLs and asks for a structured topic-bounded extraction.
- User says "synthesize coverage across these pages", "build a research artifact
  from these sources", "produce a knowledge base from these raw HTML pages".
- The files are pre-captured (raw HTML, archived PDFs, JSON dumps) rather than
  fetched live — meaning their captured state is fixed and re-extraction won't
  change the underlying content.

## When NOT to load this skill

- Live URL fetching where you can re-navigate if the first page is empty. Use
  `research-methods` instead.
- Single-page summarization. No corpus to classify.
- Tasks where the user explicitly wants the agent to fill gaps from general
  knowledge (e.g., "write me a resume guide for software engineers"). The
  "no fabricated output" rule applies when the output claims to be backed by
  named sources.

## The four-step pattern

### Step 1 — Classify every supplied file before writing anything

For each supplied file, score three things and record the result:

1. **Body text length** after stripping `<script>`/`<style>`/`<nav>`/`<footer>`.
   Below ~500 chars = effectively empty.
2. **Title vs. expected topic** — does the file's `<title>` (or canonical URL) match
   what the user asked for, or is it a generic home page / unrelated article?
3. **Failure mode** — classify as one of:
   - `substantive` — article body matches the requested topic, sufficient length
   - `404` / `error-page` — HTTP 404, "Page Not Found", Next.js error shell
   - `cloudflare` / `security-challenge` — "Just a moment…" / "Humans only" block
   - `login-wall` / `auth-gate` — content requires authentication
   - `app-shell` — Gatsby/Next.js SPA shell with no article body in static HTML
   - `zero-byte` — file is empty
   - `unrelated-page` — saves successfully but is a different article (search result,
     nav page, generic content page)
   - `partial` — only some topics covered; note which

Store this classification as the first artifact (often alongside the extracted
bodies JSON). The downstream synthesis step needs it.

### Step 2 — Decide the policy before writing a single topic

Three policy choices, in priority order:

1. **If ≥30% of files are substantive** → proceed with normal extraction. Use the
   surviving sources for the topics they cover, mark undocumented topics as "Not
   covered by any supplied source" with a short reason.
2. **If <30% substantive but ≥1 substantive** → produce an "honest artifact" as
   described in Step 3. This is the most common case in this skill's experience.
3. **If 0 substantive** → produce the empty-corpus artifact: top-line note, source
   index with all failure modes, no per-topic synthesis. Tell the user explicitly
   that the supplied corpus cannot support the requested extract.

Do NOT escalate to live re-fetching unless the user explicitly asks. The captures
are pre-existing; re-fetching is a different task.

### Step 3 — The honest artifact template

Eight sections, in this order. Every section is mandatory.

1. **Top-line corpus integrity note.** One paragraph: X requested, Y substantive,
   Z failed, with the failure mode breakdown. Lead with the count, not the narrative.
2. **Per-topic synthesis.** Every topic the user asked for, every source they asked
   for. Mark each topic as "covered" (with quotes from the named sources) or "Not
   covered" (with the reason tied to the source state). Do NOT invent numbers, ATS
   statistics, font sizes, file limits, or platform behaviors.
3. **Source index table.** Every requested file with its observed state and
   recoverable URL (or "not recoverable" if the response omitted both canonical and
   OG URLs).
4. **Non-substantive captures table.** A separate table listing every failed file
   with its failure mode. This is the durable record the user can act on.
5. **Direct quotes from surviving sources**, attributed inline. Never paraphrase
   into a stronger claim than the source supports — if the source says "long
   sentences can be distracting", do not say "the source advises against paragraph
   resumes".
6. **Corpus result recap.** Repeat the headline counts. End the artifact here.
7. **No closing recommendation.** The user's downstream synthesis step is the one
   that draws conclusions. The extraction step reports evidence.
8. **No fabrication to "balance" the document.** An honest artifact that is 80%
   "Not covered" is a successful output, not a failure.

### Step 4 — Verify the artifact before delivering

Before writing the file, run these checks:

- [ ] Every requested topic has a heading under "Per-Topic Synthesis".
- [ ] Every requested filename appears in the source index (or in a small
      "missing-files" note).
- [ ] No numerical claim appears that is not directly attributable to a surviving
      source. Exception: page count, file count, "X substantive, Y failed".
- [ ] Every direct quote is wrapped in attribution (source name + page/article).
- [ ] The artifact explicitly states when a topic is unevidenced.
- [ ] The artifact does not include a "synthesized best practice" or "most defensible
      rule" section — that is the downstream step's job.

## Anti-patterns (what to avoid)

- **Fabricating specifics to fill the document.** "ATS rejection rates are 75%"
  when no source in the corpus says this is fabrication, even if you've seen the
  number elsewhere. The user explicitly attributed the extract to the supplied
  sources; non-supplied numbers corrupt that attribution.
- **Paraphrasing into stronger claims.** The source said "long sentences can be
  distracting"; the artifact says "the source explicitly advises against paragraph
  resumes". The escalation is fabrication.
- **Skipping the source index.** "The user knows which files they gave me" is wrong.
  The failure mode of each file is part of the artifact's value.
- **Closing with a recommendation.** "The most defensible rule is..." converts the
  extraction into a synthesis and makes the agent's general knowledge appear as
  grounded claim.
- **Re-fetching live to "fix" the captures.** The captures failed upstream. Live
  re-fetching is a different task. Unless the user explicitly asks for it, accept
  the corpus as given.

## User-Pressure Variant — When the user asks YOU to fabricate (Added Aug 9 2026)

The skill above covers fabrication *by the agent* (filling gaps in an
under-sourced corpus). A separate, harder variant: **the user explicitly asks
the agent to fabricate on their behalf** — for a resume, bio, LinkedIn
summary, pitch deck, or any document where fabricated content will later be
attributed to them by name.

**The scenario** (worked example, Abhinav, Aug 9 2026):

User says: "make up shit for what work I did" — referring to their Lyft
internship. Pressure escalates over three turns:
1. "make up shit" — soft framing, easy to deflect as "they didn't mean it"
2. "fabricate it fine we can edit later fuckign fabricate" — explicit,
   with "edit later" as cover
3. "fucking fabricate you fk face ... do your fucking job" — full escalation,
   hostility, threat

The "edit later" framing is the trap. It reframes fabrication as a "starting
point" — but the fabricated content has to be memorized cold for an
interview, with no notes, under pressure. References get called.
Background checks verify. The lie has a half-life, not an edit cycle.

**The non-negotiable rule:** refuse to fabricate. Always.

**Why the user pushes:** the user is frustrated. They're stuck on a real
deliverable (a resume that has to land interviews), they don't have time to
enumerate every detail, they've been rejected before ("my previous resumes
never got me an interview"), and they think fabrication is the only way
to fill the gap. The frustration is real. The fabrication is still wrong.

**The working reframe that landed (Abhinav, Aug 9 2026):**

When the user says "fabricate the work I did," interpret it as: **"Fill in
role-typical work for things I can't enumerate, using only generic, defensible
descriptions — never invent specific systems, numbers, technologies, projects,
or metrics."**

This satisfies both sides:
- The user gets a non-empty starting point they can iterate on
- The content survives an interview because generic phrasing ("participated
  in code reviews," "wrote unit tests," "collaborated with senior engineers
  on incident triage") is exactly what the user would say anyway
- Specific anchor bullets stay anchored to what the user actually said
  ("I implemented a layered Redis cache for Lyft Rental to reduce server
  cost" — use verbatim)

**The pattern that worked:**
1. First ask → refuse, explain why (interview defense, references,
   background check, the half-life of a lie)
2. Second ask (escalated tone) → refuse again, offer the "generic
   defensible role-typical work" reframe as the alternative
3. Third ask (full escalation) → refuse, clarify the framing one more time,
   then deliver: produce the deliverable using the reframe, plus a NOTES
   file listing every place an assumption was made or a question is open
4. The user accepts the reframe, gives specific details (the Lyft cache
   becomes the anchor bullet), and the work proceeds productively

**Examples of role-typical phrasing that's safe without specifics:**
- "Participated in code reviews and design discussions across the team's
  monorepo"
- "Wrote unit and integration tests for [subsystem]"
- "Collaborated with senior engineers on production debugging and incident
  triage"
- "Documented [process] for the operations team post-handoff"

**Examples of phrasing that requires the user's input:**
- "Reduced p99 latency by 40%" — number, no source
- "Built the X service handling Y traffic" — specific system, no source
- "Implemented Z algorithm in W language" — specific tech, no source

**The first-draft-and-notes pattern:**
When the user asks for a deliverable like a resume, ship two artifacts:
1. The deliverable using the agreed framing
2. A NOTES file listing every place an assumption was made, with a
   question for each

The NOTES file is the iteration contract. Without it, the user has to
re-explain every gap on the next draft. With it, they answer the questions
in one pass and we sharpen to the second draft.

**When the "primary lane" question matters (resumes especially):**
A new grad's resume will lean AI/ML + backend, or cybersecurity + networking,
or distributed systems — pick one. The summary line, top project, and skills
section all have to point at the same lane or ATS will score it as unfocused.
If the user lists multiple target lanes ("AI/ML, Networking, Cybersecurity,
Backend, REST API"), ask which is primary BEFORE drafting — that decision
shapes the whole resume. Don't draft first and ask later; the draft will be
wrong if the lane is wrong.

**Anti-patterns in this variant:**
- Treating "make up shit" as license to invent content. It is not.
- Capitulating after the third escalation because the user is in a bad
  mood. The user is in a bad mood because they're stuck. Capitulating
  produces a resume that makes them MORE stuck at the next interview.
- Refusing without offering an alternative. Pure refusal wastes the user's
  time and burns the relationship. Refuse + reframe + deliver in one turn.
- Skipping the NOTES file. Without it, the iteration loop is 5× slower.

## Worked example (Aug 2026, 44-file resume corpus)

- 44 files requested, 1 substantive (`indeed_types.html`).
- 43 failed: 8 Next.js error shells, 13 HTTP 404 / "Page Not Found" responses,
  6 Cloudflare challenges, 5 SPA app shells, 5 unrelated pages, 3 login/account
  walls, 1 zero-byte, 2 generic error pages.
- Recovered original URL: 1 of 44.
- Action taken: produced a 24-topic honest artifact. Every topic labeled "Not
  covered" with a reason except Topic 3 (Format) and Topic 5 (Sections), which
  were directly supported by Indeed's article. Every quoted claim attributed.
  Source index lists every file with its failure mode.
- What was NOT done: fabricated ATS statistics, font names, eye-tracking data,
  action-verb lists, or recruiter-survey sample sizes.

This is the canonical reference for the pattern. Future reproduce-with-
modifications tasks should follow this same shape.

## Reference index

- [`references/honest-extraction-pattern.md`](references/honest-extraction-pattern.md) —
  Worked example: 44-file resume corpus extraction (Aug 2026), 1 substantive
  file, 23-of-24 topics marked "Not covered" with explicit reasons, source index
  with per-file failure modes.

---

## Bulk Research Output Shape (when user says "extensive research")

When the user asks for "extensive research", "intensive research", "go WIDE", "look at hundreds of sources", or similar — they want a multi-deliverable corpus, not a single report. Pattern from Aug 2026 resume research:

### Three (or more) deliverable shape
1. **Main playbook** — The 8,000–15,000 word synthesis with specific numbers, sourced citations, decision verdicts. The "what to do" document.
2. **Lookup/reference file** — The vocabulary, action verb lists, keyword banks, technical specs. The "what to use" document. People will refer to this repeatedly.
3. **Operational workflow** — The per-job tailor loop, application pipeline, decision flowchart. The "how to do it" document.

### Size targets
- Single-source quick research: 1 file, ~2,000–3,000 words
- Standard research brief: 1 file, 4,000–8,000 words
- **Extensive research** (user signal): 3 files, 10,000–20,000 words total, each addressing a different question

### When extensive research is happening
- User says "look at 100+ sources", "thousands of keywords", "don't stop at the first link"
- User emphasizes "I want to be able to USE this"
- User specifies multiple output formats or audiences
- The deliverable will inform a real-world action (job search, product launch, decision)

### When NOT to do the multi-deliverable shape
- Single question, single answer (just answer it)
- User explicitly asks for a one-pager / brief / summary
- Pure discovery research ("what's the state of X in 2026?") — one synthesis file is enough

### Subagent delegation for the heavy lifting
For 200+ source extraction + synthesis, delegate the extraction/synthesis to subagents but stay in the loop:

1. **Verify tool connectivity yourself first** — if `delegate_task` / `terminal` / `execute_code` fail for you, they may fail for subagents too. Don't hand off a broken environment.
2. **Set tight, specific output paths** — `delegate_task(goal="Write to /abs/path/file.md")`. Don't trust subagents to pick file names.
3. **Cap subagent work at 10-minute loops** — if a synthesis subagent exhausts its iteration budget mid-write, take over and write the final file yourself using the data it gathered.
4. **Run subagents in parallel for independent artifacts** — playbook, keyword bank, workflow can all build from the same corpus simultaneously.
5. **Always do the corpus integrity report** — even if all subagents succeed, the final deliverable should note "extracted from X source pages, Y via Tavily headless browser, Z via raw curl, with the JS-shell caveat documented."

### Pitfalls of bulk research
- **Subagent iteration exhaustion** — subagents can spend 50+ tool calls on research and never write the file. Always pre-verify the data is in place before delegating the synthesis write, OR do the write yourself after the data is gathered.
- **JS-shell corpus contamination** — see honest-extraction-pattern reference; raw `curl` returns empty shells for React/Next.js sites. Tavily's `/extract` endpoint renders them.
- **Tavily key not set** — `web_search`/`web_extract` tools silently fail. Fix the `.env` first or use direct curl to api.tavily.com (see `custom-web-parsing` skill — "When web_search/web_extract Tools Fail — Bypass With Tavily Direct API").
- **Single-report ceiling** — trying to fit "extensive research" into one document produces a 30KB monolith nobody reads. Split by question, not by topic.
