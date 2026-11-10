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
category: software-development
tags: [documentation, course-generation, codebase-to-course, teaching, onboarding, walkthrough]
version: 1.0.0
---

# Codebase-to-Course Renderer

Transform any codebase or curated file subset into an interactive HTML course that explains how it works to non-technical readers. The output is fully self-contained: open `index.html` in any browser — no server, no build pipeline required.

**Dependencies:** Google Fonts CDN only (loaded via `<link>` in the HTML)

---

## When to Use

- User wants an interactive walkthrough explaining their codebase
- Creating onboarding material for new contributors
- Documenting a PR/diff in human-readable teaching form
- "Make a course from this branch" — produce teaching artifacts from a diff, not the full repo
- Vibe-coder tone requests for explanatory documentation

---

## Invoking the Skill

The skill is **not bundled with Hermes**. Install and invoke it via Claude Code:

### Option 1: Clone and Read

bash
git clone --depth=1 https://github.com/zarazhangrui/codebase-to-course.git /tmp/codebase-to-course
cat /tmp/codebase-to-course/SKILL.md  # read the full skill instructions
### Option 2: Run with Claude Code

bash
cd /tmp/codebase-to-course

# Point Claude Code at the skill with a task
/path/to/claude --print --dangerously-skip-permissions \
  "Generate an interactive single-page HTML course from /path/to/codebase/

  SKILL.md is in /tmp/codebase-to-course/ — follow its Phase 3 for the output structure.

  CONTEXT:
  - Domain: [e.g., a React state management library]
  - Target learner: [e.g., mid-level JS developers unfamiliar with this pattern]
  - Modules to cover: [e.g., 4-5 key files that demonstrate the core concept]

  OUTPUT:
  Generate the full course directory per SKILL.md Phase 3, then run build.sh.
  Final output at /path/to/_course/"
---

## Output Structure

The skill generates a complete course directory:

_course/
├── index.html           # Course landing page with module navigation
├── modules/
│   ├── module-1.html    # One HTML file per teaching module
│   ├── module-2.html
│   └── ...
├── styles.css           # Design system styles
└── main.js              # Interactivity (quizzes, code explanations, animations)
---

## Curriculum Constraints

| Requirement | Value |
|-------------|-------|
| Module count | 4–6 modules |
| Tone | Vibe-coder friendly, accessible to non-experts |
| Code blocks | Include plain-English explanations inline |
| Navigation | Scroll-based with module links |
| Interactivity | Quizzes, animated diagrams where appropriate |

---

## Curated Subset Pattern (Focused PR Walkthroughs)

For "make a course from this PR" requests, do **not** process the entire repo. Instead:

1. Identify the key files changed in the diff
2. Extract only those files + their immediate dependencies
3. Build the course around the PR's purpose and context
4. Include a "before/after" module if the PR modifies behavior

This produces a teaching artifact focused on *what changed* and *why*, not the full codebase.

---

## Input Requirements

To generate a quality course, the user must provide:

- **Codebase path** — directory or file subset to document
- **Domain description** — what the codebase does in plain terms
- **Target learner** — who will read this course (skill level, background)
- **Module outline** — which files/concepts map to which modules (or ask the AI to propose one)
- **Optional: specific teaching goals** — what the learner should understand after completing

---

## Phase 3: Course Generation (Reference)

1. **Parse** the codebase — identify structure, key files, relationships
2. **Plan modules** — 4–6 teaching units aligned to the curriculum constraints
3. **Generate HTML** — `index.html` + `modules/*.html` with embedded CSS/JS or linked assets
4. **Apply styles** — use the skill's design system
5. **Validate** — ensure all code blocks have explanations, all links resolve, quizzes are functional
6. **Build** — run `build.sh` to assemble final output