---
name: codebase-to-course-render
description: Render any codebase into an interactive HTML course.
triggers:
  - "render this as a course"
  - "make a course from this repo"
  - "codebase walkthrough"
  - "interactive tutorial from code"
  - "codebase-to-course"
  - "turn this codebase into a course"
  - "make a course from this PR"
  - "teaching artifact from diff"
category: software-development
tags: [documentation, course-generation, codebase-to-course, teaching, onboarding, walkthrough]
version: 1.0.0
---

# Codebase-to-Course Renderer

Transform any codebase, repository subset, or diff into a self-contained, interactive HTML course for non-technical readers.

## What This Skill Produces

A complete course directory containing:

| File | Purpose |
|------|---------|
| `index.html` | Course landing page with curriculum overview and navigation |
| `modules/*.html` | One HTML file per teaching module |
| `styles.css` | Course styling and animations |
| `main.js` | Interactivity: quizzes, code explanations, scroll navigation, animated diagrams |

**Zero server required.** Open `index.html` in any browser. Only external dependency: Google Fonts CDN.

---

## When to Use This Skill

| Scenario | Approach |
|----------|----------|
| General codebase explanation | Full repository analysis → 4-6 module curriculum |
| PR/diff walkthrough | Curated file subset from the diff + context |
| Onboarding material | Focus on architecture, key patterns, contributor workflow |
| Feature deep-dive | Targeted modules on specific subsystems |

---

## Curriculum Structure

Enforce exactly **4-6 modules** per course:

| Module Type | Content | Typical Length |
|-------------|---------|----------------|
| **Introduction** | What this does, why it matters, who it's for | 1-2 pages |
| **Architecture Overview** | High-level components and relationships | 2-3 pages |
| **Deep Dives** | Per-feature or per-subsystem explanations | 2-4 pages each |
| **Conclusion** | Key takeaways, next steps, contributing guide | 1-2 pages |

### Module Anatomy

Each `modules/*.html` must contain:

1. **Learning objective** — One clear sentence: "After this module, the reader will understand..."
2. **Conceptual explanation** — Plain English, no jargon without definition
3. **Code examples** — Annotated with inline plain-English callouts
4. **Visual diagram** — ASCII or described flowchart of data flow
5. **Knowledge check** — One multiple-choice question per module

---

## Tone and Style Guidelines

### Vibe-Coder Tone

Write for curious non-experts who can read code but need context:

- **Conversational, not academic** — "Here's what happens when..." not "The system processes..."
- **Analogies welcome** — Real-world comparisons make abstractions concrete
- **Jargon with translation** — Use technical terms but immediately define them
- **Active voice** — "The function calls the API" not "The API is called by the function"
- **Short paragraphs** — One idea per paragraph, max 3-4 sentences

### Code Presentation

html
<!-- Annotated code block pattern -->
<pre><code class="language-javascript">
// [Plain-English explanation of what this line does]
const result = processData(input);

// [This block handles the error case by doing X]
// Think of it like: [simple analogy]
if (error) {
  handleError(result);
}
</code></pre>
---

## Process (3 Phases)

### Phase 1: Analysis

1. **Identify scope** — Full repo or curated subset? Ask if unclear.
2. **Determine audience** — New contributors, product managers, students?
3. **Detect key subsystems** — Find natural module boundaries from file structure
4. **Extract teachable concepts** — What must a reader understand to make sense of this?

### Phase 2: Curriculum Design

Generate the module structure before writing content:

Course: [Name derived from repo/purpose]
Audience: [Target learner]
Modules:
  1. [Title] — [One-line objective]
  2. [Title] — [One-line objective]
  ...
### Phase 3: Content Generation

Generate the full course directory:

1. Create `/path/to/_course/` directory
2. Generate `index.html` with course overview and module navigation
3. Generate `modules/01-intro.html` through `modules/0N-conclusion.html`
4. Generate `styles.css` with the design system
5. Generate `main.js` with interactivity features
6. Run `build.sh` (if present) to validate and bundle

**Final output location:** `/path/to/_course/index.html`

---

## Curated Subset Pattern (PR/Diff Walkthroughs)

For "make a course from this PR" requests:

1. **Extract changed files** from the diff
2. **Identify the feature/bug** being addressed
3. **Contextualize the change** — What existed before? What does this add?
4. **Scope to teachable units** — Don't explain the whole repo; explain the delta

### Example: PR Course Prompt

Generate a course from the diff in /home/user/project/pull-request-123/

Context: This PR adds rate limiting to the API endpoint.
Audience: Backend developers joining the team.
Scope: Only the rate-limiting implementation and its tests.

Output: /tmp/rate-limit-course/
---

## Invocation

### Option 1: Direct Skill Installation

bash
# Clone the skill repository
git clone --depth=1 https://github.com/zarazhangrui/codebase-to-course.git /tmp/codebase-to-course

# Read full skill documentation
cat /tmp/codebase-to-course/SKILL.md
### Option 2: Invoke via Claude Code

bash
# Point Claude Code at a codebase with the skill context
claude --print --dangerously-skip-permissions "$(cat /tmp/codebase-to-course/SKILL.md)" \
  "Generate an interactive single-page HTML course from /path/to/repo/"

# For a specific PR/diff
claude --print --dangerously-skip-permissions "$(cat /tmp/codebase-to-course/SKILL.md)" \
  "Generate a teaching course from the diff in /path/to/repo/ for [AUDIENCE]. Context: [PURPOSE]. Output to /path/to/_course/"
---

## Output Validation Checklist

After generation, verify the course includes:

- [ ] `index.html` with navigation to all modules
- [ ] 4-6 module files in `modules/` directory
- [ ] Each module has: objective, explanation, code, diagram, quiz
- [ ] `styles.css` and `main.js` are linked correctly
- [ ] No broken external links (except Google Fonts CDN)
- [ ] Course opens standalone without a server

---

## Design System

| Element | Specification |
|---------|---------------|
| Font | Google Fonts: JetBrains Mono (code), Inter (text) |
| Colors | Primary: #6366F1, Accent: #10B981, Background: #F8FAFC |
| Code blocks | Syntax highlighting, line numbers, copy button |
| Navigation | Sticky sidebar with progress indicator |
| Animations | Subtle fade-ins on scroll, hover states on interactive elements |