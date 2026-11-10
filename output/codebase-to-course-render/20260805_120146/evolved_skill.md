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
  - "generate course from PR"
  - "onboarding course from codebase"
category: software-development
tags: [documentation, course-generation, codebase-to-course, teaching, onboarding, walkthrough, interactive]
version: 1.0.0
---

# Codebase-to-Course Renderer

Transform any codebase (or curated file subset) into a self-contained, interactive HTML course that explains how it works to non-technical readers. Open `index.html` in any browser — no server required. Single external dependency: Google Fonts CDN.

## What This Produces

The renderer generates a complete course directory:

_course/
├── index.html              # Course landing page with module list
├── modules/
│   ├── module-1.html       # One HTML file per teaching module
│   ├── module-2.html
│   └── ...
├── styles.css              # Course styling and animations
└── main.js                 # Quizzes, code explanations, navigation
### Module Structure (Required)

Each module includes:

1. **Learning objectives** — What the learner will understand after this module
2. **Code walkthrough** — Annotated code blocks with plain-English explanations
3. **Visual diagram** — SVG-based animated diagram explaining key concepts
4. **Knowledge check** — 3-5 question quiz (multiple choice or true/false)
5. **Key takeaways** — 3 bullet points summarizing the module

### Quiz Format

html
<div class="quiz" data-correct="2">
  <p class="quiz-question">Why does the auth module validate tokens on every request?</p>
  <button data-index="0">To improve performance</button>
  <button data-index="1">To prevent replay attacks</button>
  <button data-index="2">Security — tokens can be revoked</button> <!-- correct -->
  <button data-index="3">It's required by the API spec</button>
  <p class="quiz-feedback correct">Correct! Revocable sessions are essential...</p>
  <p class="quiz-feedback incorrect">Not quite. The key reason is security...</p>
</div>
### Design System

| Element | Value |
|---------|-------|
| Primary color | `#4F46E5` (indigo) |
| Background | `#F9FAFB` |
| Code block background | `#1F2937` |
| Accent | `#10B981` (emerald for success) |
| Font | Inter (headings), JetBrains Mono (code) |
| Max content width | `720px` |
| Module completion tracking | localStorage |

## When to Use This

| Use Case | Approach |
|----------|----------|
| General codebase documentation | Run on full repo, 5-6 modules |
| New contributor onboarding | Focus on architecture + contribution workflow |
| PR/diff walkthrough | Use curated subset pattern (see below) |
| Feature explanation | Single focused module on the feature's files |
| "What changed in this branch?" | Generate from diff + commit messages |

## Curated Subset Pattern (PR Walkthroughs)

For "make a course from this PR" requests:

1. **Do NOT** run on the entire repo
2. **Extract** only the changed files + their immediate dependencies
3. **Identify** the "story" — what problem does this PR solve?
4. **Generate** a 2-3 module course covering:
   - Module 1: Context (what existed before, why change was needed)
   - Module 2: Implementation (key changes with explanations)
   - Module 3: Testing/validation (how to verify it works)

### Example: Curated Subset Command

bash
# Identify changed files
git diff --name-only main...feature-branch

# Copy subset to temp directory
mkdir /tmp/pr-course-input
cp -r src/auth/* /tmp/pr-course-input/
cp src/api/handlers/auth.go /tmp/pr-course-input/

# Generate course from subset
claude --print "Generate a course from /tmp/pr-course-input/ with focus on
the new JWT refresh token flow. Target: backend developers new to the auth system.
Output to /tmp/auth-refresh-course/"
## How to Invoke

### Option 1: Clone and Read

bash
# One-time clone
git clone --depth=1 https://github.com/zarazhangrui/codebase-to-course.git /tmp/codebase-to-course

# Read full skill instructions
cat /tmp/codebase-to-course/SKILL.md
### Option 2: Invoke via Claude Code

bash
cd /tmp/codebase-to-course

# Generate course from a codebase
claude --print --dangerously-skip-permissions "\
Generate an interactive single-page HTML course from /path/to/repo/ using the \
codebase-to-course skill. SKILL.md is in /tmp/codebase-to-course/.

CONTEXT:
- Domain: [e.g., real-time collaboration backend]
- Target learner: [e.g., frontend developers joining the team]
- Modules to cover: [e.g., 5 modules covering architecture, data flow, auth, websocket protocol, testing]

OUTPUT:
Generate the full course directory per SKILL.md Phase 3, then run build.sh.
Final output at /path/to/_course/ with index.html + modules/*.html + styles.css + main.js."
## Curriculum Guidelines

### Module Count
- **Minimum**: 3 modules
- **Maximum**: 6 modules
- **Optimal**: 4-5 modules

### Module Naming Convention

module-1-[topic].html
module-2-[topic].html
...
Valid topic prefixes: `overview`, `architecture`, `setup`, `workflow`, `api`, `auth`, `data`, `testing`, `deployment`, `contributing`

### Vibe-Coder Tone

Write for curious beginners, not experts:
- ✅ "Think of this like a traffic cop directing cars"
- ❌ "The round-robin scheduler implements L1 cache eviction"
- ✅ "This function runs every time someone loads the page"
- ❌ "The useEffect hook handles side effects"

## Build Process

1. Generate all HTML modules with proper structure
2. Create `styles.css` with responsive layout
3. Create `main.js` with:
   - Quiz logic (answer validation, feedback display)
   - Module completion tracking
   - Scroll-based navigation highlighting
   - Animated diagram initialization
4. Run `build.sh` to inline CSS/JS into HTML (for single-file distribution)

## Quality Checklist

Before finalizing a course:

- [ ] Each module has learning objectives
- [ ] Every code block has plain-English annotation
- [ ] At least one visual diagram per module
- [ ] Quizzes have correct answers and explanatory feedback
- [ ] Module navigation works (next/prev + sidebar)
- [ ] Progress persists across page reloads
- [ ] Course is usable on mobile (responsive design)
- [ ] All external resources (fonts) use CDN with fallbacks
- [ ] index.html links to all modules correctly
- [ ] No broken relative paths

## Error Handling

| Issue | Resolution |
|-------|------------|
| No files found in codebase | Prompt user to specify files or provide GitHub URL |
| Codebase too large (>10k files) | Suggest curated subset approach |
| Binary files encountered | Skip and note in output |
| No clear module structure | Create overview + 4 feature modules |

## Example: Full Course Generation

bash
# Complete workflow
git clone --depth=1 https://github.com/zarazhangrui/codebase-to-course.git /tmp/c2c
cd /tmp/c2c

claude --print --dangerously-skip-permissions "\
Generate a 5-module interactive course from /home/user/myapp/

DOMAIN: Node.js REST API framework
LEARNER: Junior developers joining the team
MODULES:
1. overview/introduction — What this framework does
2. architecture/routing — How HTTP requests are processed
3. data/database — ORM patterns and migrations
4. api/endpoints — REST conventions used
5. testing/validation — How to write integration tests

OUTPUT: /home/user/_course/
Run build.sh when complete."
The generated course at `/home/user/_course/` opens directly in any browser and requires no server.
---