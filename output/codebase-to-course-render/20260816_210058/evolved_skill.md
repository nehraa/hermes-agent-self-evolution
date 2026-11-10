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

Transform any codebase (or curated file subset) into an interactive HTML course that explains how it works to non-technical readers.

**Self-contained:** Open `index.html` in any browser — no server required. External dependency: Google Fonts CDN only.

## Output Structure

The skill generates a complete course directory containing:

_course/
├── index.html          # Course homepage (assembled from parts)
├── modules/
│   ├── 01.html         # One HTML file per teaching module
│   ├── 02.html
│   └── 0N.html
├── styles.css          # Design system styling
└── main.js             # Interactivity (quizzes, code explanations, navigation, diagrams)
### Enforced Constraints

- **4-6 modules** per curriculum
- **Vibe-coder tone**: friendly, accessible, plain-English explanations
- **Specific design system**: consistent styling, animations, and layout

## When to Use

| Scenario | Description |
|----------|-------------|
| Interactive walkthrough | User wants to explain how their codebase works to others |
| Contributor onboarding | Generate teaching material for new team members |
| PR/diff documentation | Document a specific change in human-readable form |
| Branch-based course | "Make a course from this branch" — teach the diff, not the whole repo |

## How to Invoke

### Prerequisites

The skill is **not bundled with Hermes**. Install or invoke via Claude Code.

bash
# Step 1: Clone the skill (one-time setup)
git clone --depth=1 https://github.com/zarazhangrui/codebase-to-course.git /tmp/codebase-to-course

# Step 2: Read the full skill documentation
cat /tmp/codebase-to-course/SKILL.md
### Running the Skill

bash
# Invoke via Claude Code with skill context
cd /tmp/codebase-to-course
claude --print --dangerously-skip-permissions "$(cat SKILL.md)"
### Generating a Course

bash
# Point Claude Code at a codebase with context
claude --print --dangerously-skip-permissions "Generate an interactive
single-page HTML course from /home/Hermes/repos/OPENMAIC/core/ using the
codebase-to-course skill (SKILL.md is in /tmp/codebase-to-course/).

CONTEXT — what to teach:
[domain description, target learner, modules to cover]

OUTPUT:
Generate the full course directory per SKILL.md Phase 3, then run build.sh.
Final output at /path/to/_course/ with index.html + modules/*.html + styles.css + main.js."
## Curated Subset Pattern

For **"make a course from this PR"** requests:

1. Do **not** run the skill against the entire repo
2. Instead, identify the specific files and diff relevant to the PR
3. Provide a curated file list + PR context as input
4. The output teaches the change, not the codebase

Example input for PR walkthrough:
- Files changed: [list specific files]
- PR description: [what this PR does]
- Target learner: [audience]
- Key concepts: [what to emphasize]
## Skill Phases

1. **Phase 1 — Discovery**: Analyze codebase structure, identify key modules
2. **Phase 2 — Curriculum Design**: Define 4-6 teaching modules with learning objectives
3. **Phase 3 — Content Generation**: Create module HTML files with explanations, quizzes, and diagrams
4. **Phase 4 — Assembly**: Build final `index.html` and run `build.sh`

## Tips for Best Results

- **Be specific about audience**: "backend engineers new to TypeScript" vs. "non-technical stakeholders"
- **Define scope clearly**: Which files/folders to include? Which to skip?
- **For PR courses**: Include the PR description and diff context as input
- **Module naming**: Use action-oriented titles like "How Authentication Works" not just "Auth Module"