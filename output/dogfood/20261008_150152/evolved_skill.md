---
name: dogfood
description: "Exploratory QA of web apps: find bugs, evidence, reports."
version: 1.0.0
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [qa, testing, browser, web, dogfood]
    related_skills: []
---

# Dogfood: Systematic Web Application QA Testing

## Overview

This skill guides you through systematic exploratory QA testing of web applications using the browser toolset. You will navigate the application, interact with elements, capture evidence of issues, and produce a structured bug report.

## Prerequisites

- Browser toolset must be available: `browser_navigate`, `browser_snapshot`, `browser_click`, `browser_type`, `browser_vision`, `browser_console`, `browser_scroll`, `browser_back`, `browser_press`
- A target URL and testing scope from the user

## Inputs

The user provides:
1. **Target URL** — the entry point for testing
2. **Scope** — what areas/features to focus on (or "full site" for comprehensive testing)
3. **Output directory** (optional) — where to save screenshots and the report (default: `./dogfood-output`)

## Workflow

Follow this 5-phase systematic workflow:

---

### Phase 1: Plan

1. Create the output directory structure:
   ```
   {output_dir}/
   ├── screenshots/       # Evidence screenshots
   │   ├── 01-home-page.png
   │   ├── 02-login-form.png
   │   └── ...
   └── report.md          # Final report (generated in Phase 5)
   ```

2. Identify the testing scope based on user input.

3. Build a test plan listing pages and features to cover:
   - Landing/home page
   - Navigation links (header, footer, sidebar)
   - Key user flows (sign up, login, search, checkout, etc.)
   - Forms and interactive elements
   - Edge cases (empty states, error pages, 404s)
   - Responsive behavior (if applicable)

---

### Phase 2: Explore

For each page or feature in your plan:

#### Navigation

1. **Navigate** to the page:
   ```
   browser_navigate(url="https://example.com/page")
   ```

2. **Check the console** for JavaScript errors:
   ```
   browser_console(clear=true)
   ```
   Do this after every navigation and after significant interactions. Silent JS errors are high-value findings.

3. **Take an annotated screenshot** to visually assess the page:
   ```
   browser_vision(question="Describe the page layout, identify any visual issues, broken elements, or accessibility concerns", annotate=true)
   ```
   The `annotate=true` flag overlays numbered `[N]` labels on interactive elements for easy reference.

#### Interaction Testing

For each interactive element you encounter:

1. **Click** and observe behavior:
   ```
   browser_click(ref="N")
   ```
   Watch for: unexpected redirects, errors, state changes, or no response.

2. **Type** into input fields:
   ```
   browser_type(ref="N", text="test value")
   ```
   Test: normal input, special characters, long strings, SQL/HTML injection attempts, empty submission.

3. **Submit forms** and verify:
   - Success states display correctly
   - Error messages are helpful and accurate
   - Data persists as expected
   - No console errors occur

4. **Scroll** through content to check:
   ```
   browser_scroll(direction="down", amount=3)
   ```
   Verify: lazy-loaded content renders, no layout shifts, infinite scroll works correctly.

5. **Navigate back** to return to previous state:
   ```
   browser_back()
   ```

#### Common Issues to Watch For

| Category | Examples |
|----------|----------|
| **Visual** | Broken images, misaligned elements, overlapping text, unresponsive styling |
| **Functional** | Buttons not working, forms not submitting, data not persisting |
| **Content** | Misspellings, broken links, placeholder text in production |
| **Accessibility** | Missing alt text, low contrast, no keyboard navigation |
| **Performance** | Slow loading, janky scrolling, content jumping |
| **Security** | Input validation errors, exposed data, console warnings |

---

### Phase 3: Capture Evidence

For each issue found:

1. **Screenshot the issue** with context:
   ```
   browser_vision(question="Capture the bug and surrounding area", annotate=false)
   ```
   Save with descriptive filename: `{issue-id}-{description}.png`

2. **Document the steps to reproduce**:
   - URL at time of issue
   - Actions taken before the issue appeared
   - Expected vs. actual behavior
   - Console errors (if any)

3. **Note severity**:
   - **Critical**: Data loss, security vulnerability, complete feature broken
   - **High**: Major feature impaired, workarounds difficult
   - **Medium**: Feature partially working, minor usability impact
   - **Low**: Cosmetic, minor inconvenience, edge case

---

### Phase 4: Analyze

After exploring all planned pages:

1. **Review all console errors** — categorize by source:
   - Third-party scripts (often ignore unless blocking functionality)
   - Application code (always report)
   - Network failures (check if critical resources failed)

2. **Cross-reference issues** — check if one root cause produces multiple symptoms.

3. **Verify reproducibility** — attempt to reproduce each issue a second time to confirm.

4. **Group related issues** into single tickets where appropriate.

---

### Phase 5: Report

Generate `report.md` in the output directory with this structure:

markdown
# QA Test Report: {Application Name}

**Test Date**: {date}
**Tester**: {agent}
**URL Tested**: {target URL}
**Scope**: {scope description}

## Summary

- **Total Issues Found**: {N}
- **Critical**: {N}
- **High**: {N}
- **Medium**: {N}
- **Low**: {N}

## Issues

### {Issue Title}
- **Severity**: {Critical|High|Medium|Low}
- **URL**: {page where found}
- **Steps to Reproduce**:
  1. Navigate to {page}
  2. Click {element}
  3. Observe {behavior}
- **Expected**: {what should happen}
- **Actual**: {what happened}
- **Console Errors**: {any errors captured}
- **Evidence**: `screenshots/{filename}.png`

---

## Recommendations

{Prioritized list of fixes or next steps}

## Test Coverage

- Pages tested: {list}
- User flows tested: {list}
- Edge cases tested: {list}
---

## Tips for Effective Testing

1. **Be methodical** — follow your plan but note interesting paths you discover.

2. **Think like a user** — click where users would click, enter what users would enter.

3. **Push boundaries** — test with empty fields, maximum lengths, unusual characters.

4. **Trust the console** — browser console errors are often overlooked but indicate real problems.

5. **Capture context** — a screenshot alone isn't enough; document the steps to reproduce.

6. **Stay on scope** — note out-of-scope issues but focus effort on requested testing area.