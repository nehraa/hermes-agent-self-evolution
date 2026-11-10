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
  - "make a tutorial from this code"
  - "generate a learning module from this"
category: software-development
tags: [documentation, course-generation, codebase-to-course, teaching, onboarding, walkthrough]
version: 1.0.0
---

# Codebase-to-Course Renderer

Transform any codebase (or curated file subset) into a self-contained, interactive HTML course that explains how it works to non-technical readers.

**No server required.** Open `index.html` in any browser. External dependency: Google Fonts CDN only.

## Output Structure

The skill generates a complete course directory:

_course/
├── index.html          # Main entry point, course overview, navigation
├── modules/
│   ├── module-1.html   # One HTML file per teaching module
│   ├── module-2.html
│   └── ...
├── styles.css          # Design system: colors, typography, layout
└── main.js             # Interactivity: quizzes, code explanations, navigation, animations
### Design Constraints

- **4–6 modules maximum** per course
- **Vibe-coder tone**: friendly, accessible, plain-English explanations
- **Specific design system**: consistent colors, typography, component styles (defined in `styles.css`)

## When to Use This Skill

Use this skill when the user wants to:

1. Create an interactive walkthrough explaining how their codebase works
2. Generate onboarding material for new contributors
3. Document a specific PR/diff in human-readable teaching form
4. Produce a teaching artifact from a branch or diff (not necessarily the whole repo)
5. Create a "make a course from this PR" request

## Invocation Methods

### Option 1: Clone and Read (One-Time Setup)

bash
git clone --depth=1 https://github.com/zarazhangrui/codebase-to-course.git /tmp/codebase-to-course
cat /tmp/codebase-to-course/SKILL.md  # Read the full skill documentation
### Option 2: Invoke via Claude Code

bash
cd /tmp/codebase-to-course

# Load the skill context
/path/to/claude --print --dangerously-skip-permissions "$(cat SKILL.md)"

# Generate a course from a codebase
/path/to/claude --print --dangerously-skip-permissions "Generate an interactive single-page HTML course from /home/user/repos/project/ using the codebase-to-course skill.

CONTEXT:
- Domain: [e.g., a React state management library]
- Target learner: [e.g., junior developers familiar with JavaScript]
- Modules to cover: [e.g., 5 modules: setup, core concepts, hooks, patterns, testing]

OUTPUT:
Generate the full course directory per SKILL.md Phase 3, then run build.sh.
Final output at /path/to/_course/ with index.html + modules/*.html + styles.css + main.js."
## Curated Subset Pattern (Focused PR Walkthroughs)

For "make a course from this PR" requests:

1. **Extract the relevant files** from the diff — do not process the entire repo
2. **Identify the teaching scope**: What did this PR actually change or introduce?
3. **Curate to 4–6 modules**: Focus on the changed files and their purpose
4. **Generate the course** from the subset, not the full codebase

This pattern is ideal for:
- Documenting architectural decisions
- Teaching teammates about a new feature
- Creating a review artifact for a complex change

## What the Skill Generates

### `index.html`

- Course title and description
- Module list with navigation
- Progress tracking
- Clean entry point for the entire course

### `modules/*.html`

Each module includes:
- **Learning objectives**: What the learner will understand after this module
- **Code blocks with plain-English explanations**: Annotated code that explains *why*, not just *what*
- **Interactive elements**: Quizzes, toggles, or diagrams where appropriate
- **Navigation**: Previous/Next module controls

### `styles.css`

Design system includes:
- Consistent color palette (brand + neutral tones)
- Typography scale (headings, body, code)
- Component styles (cards, code blocks, quiz UI)
- Responsive layout breakpoints

### `main.js`

Interactivity features:
- **Scroll-based navigation**: Smooth transitions between sections
- **Quiz functionality**: Multiple choice or fill-in for comprehension checks
- **Code explanations**: Clickable/toggleable annotations on code blocks
- **Animated diagrams**: SVG-based visualizations where useful
- **Progress persistence**: Track completion in localStorage

## Phase 3: Course Generation Process

1. **Analyze**: Parse the codebase structure and identify key concepts
2. **Plan**: Outline 4–6 modules with learning objectives
3. **Draft**: Generate HTML content for each module with code annotations
4. **Style**: Apply the design system via `styles.css`
5. **Interact**: Add JavaScript functionality via `main.js`
6. **Assemble**: Combine into the final `_course/` directory
7. **Build**: Run `build.sh` to validate and package the output

## Example Usage

**Request**: "Make a course from this PR that adds authentication"

**Approach**:
1. Extract only the auth-related files from the diff
2. Create 5 modules:
   - Module 1: What is authentication? (conceptual)
   - Module 2: The auth flow (with annotated code)
   - Module 3: Key files and their roles
   - Module 4: How to test it
   - Module 5: Common patterns and gotchas
3. Generate the course with the curated subset

**Output**: A self-contained `_course/` directory ready to share or host.

---

## Tips for Best Results

- **Be specific about the audience**: "Senior engineers" vs "bootcamp graduates" changes the tone
- **Scope carefully**: 4–6 modules is ideal; more becomes overwhelming
- **Focus on the "why"**: Code explanations should teach reasoning, not just syntax
- **Use real code**: Annotated real snippets are more valuable than simplified examples
- **Test locally**: Open `index.html` in a browser to verify before sharing