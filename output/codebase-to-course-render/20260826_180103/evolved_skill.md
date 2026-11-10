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

Transform any codebase (or curated file subset) into a self-contained, interactive HTML course that explains how it works to non-technical readers.

**No server required.** Open `index.html` in any browser. Only external dependency: Google Fonts CDN.

## Output Structure

The skill generates a complete course directory containing:

_course/
├── index.html          # Main landing page with curriculum overview
├── modules/
│   ├── 01-introduction.html
│   ├── 02-core-concepts.html
│   ├── 03-deep-dive.html
│   └── ...              # One file per teaching module
├── styles.css          # Course styling and design system
└── main.js             # Interactivity (quizzes, code explanations, navigation)
### Built-in Features

- **Scroll-based navigation** with progress tracking
- **Code blocks** with plain-English explanations on hover/click
- **Interactive quizzes** to reinforce learning
- **Animated diagrams** for visual learners
- **Responsive design** for desktop and mobile

## Curriculum Standards

The skill enforces:
- **4-6 modules** per course (prevents overwhelming learners)
- **Vibe-coder tone** (friendly, accessible, conversational)
- **Specific design system** (consistent look and feel)

## When to Use

Use this skill when the user wants to:

1. **Explain a codebase** to non-technical stakeholders or beginners
2. **Onboard new contributors** with structured, interactive documentation
3. **Document a PR or diff** in human-readable, teachable form
4. **Create teaching artifacts** from a specific branch or feature

### Curated Subset Pattern

For focused walkthroughs (e.g., "make a course from this PR"):

> Do NOT render the entire repository. Instead:
> - Analyze the changed files + commit messages
> - Identify 3-5 key concepts to teach
> - Create a targeted curriculum that explains *what changed* and *why*
> - Focus on the diff, not the whole codebase

## How to Invoke

The skill is not bundled with Hermes. Install or invoke via Claude Code:

### Option 1: Clone the Skill (One-Time Setup)

bash
git clone --depth=1 https://github.com/zarazhangrui/codebase-to-course.git /tmp/codebase-to-course
cat /tmp/codebase-to-course/SKILL.md  # Read the full skill documentation
### Option 2: Invoke with Claude Code

bash
cd /tmp/codebase-to-course

# Read the skill into context
cat SKILL.md

# Generate a course from a codebase
claude --print --dangerously-skip-permissions \
  "Generate an interactive single-page HTML course from /home/Hermes/repos/OPENMAIC/core/

Use the codebase-to-course skill (SKILL.md is in /tmp/codebase-to-course/).

CONTEXT:
- Domain: [e.g., machine learning framework]
- Target learner: [e.g., junior developers new to ML]
- Modules to cover: [e.g., tensor operations, auto-grad, model training]

OUTPUT:
Generate the full course directory per SKILL.md Phase 3, then run build.sh.
Final output at /path/to/_course/ with index.html + modules/*.html + styles.css + main.js."
## Course Generation Phases

### Phase 1: Analyze

- Identify the core purpose and architecture of the codebase
- Determine target audience and their current knowledge level
- Map out 4-6 key concepts to cover
- Select files most relevant to those concepts

### Phase 2: Structure

- Create module outline with learning objectives
- Write plain-English explanations for each concept
- Design quiz questions to reinforce key points
- Plan code examples that illustrate core patterns

### Phase 3: Generate

- Produce `index.html` with curriculum overview
- Create individual module files with explanations and code
- Generate `styles.css` with design system
- Generate `main.js` with interactivity

### Phase 4: Build

- Run `build.sh` to assemble final output
- Verify all resources are self-contained
- Test in browser without network connection

## Tips for Effective Courses

1. **Start with "why"** — Explain the problem the code solves before diving into implementation
2. **Use analogies** — Connect abstract concepts to familiar real-world examples
3. **Limit modules** — 4-6 modules keeps learners engaged; split longer topics into follow-up courses
4. **Include quizzes** — Active recall improves retention
5. **Show, don't just tell** — Use code examples with highlighted annotations