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

# Dogfood: Exploratory QA Testing for Web Applications

## Overview

Dogfood is a systematic methodology for exploratory QA testing of web applications. Using the browser toolset, you will systematically navigate through the application, identify bugs and anomalies, capture visual and console evidence, and produce a structured bug report.

This skill focuses on finding real-world issues: broken UI elements, JavaScript errors, accessibility problems, edge case failures, and unexpected behavior.

## Prerequisites

Before starting, ensure the browser toolset is available:

- `browser_navigate` — go to a URL
- `browser_snapshot` — capture DOM structure
- `browser_click` — click elements
- `browser_type` — enter text
- `browser_vision` — analyze page visually
- `browser_console` — check for JS errors
- `browser_scroll` — scroll the page
- `browser_back` / `browser_press` — navigation and interaction

You also need a target URL and testing scope from the user.

## Inputs

The user will provide:

| Input | Required | Description |
|-------|----------|-------------|
| `target_url` | Yes | The entry point URL to test |
| `scope` | No | Specific pages/features to test. If omitted, assume "full site" |
| `output_dir` | No | Directory for screenshots and report (default: `./dogfood-output`) |
| `auth_credentials` | No | Login credentials if the app requires authentication |

## Workflow

Follow this 5-phase methodology:

---

### Phase 1: Plan & Prepare

**Objective:** Establish your testing scope and directory structure.

1. **Create the output directory:**
   ```
   {output_dir}/
   ├── screenshots/       # Visual evidence
   ├── console-logs/      # JS error logs
   └── report.md          # Final bug report
   ```

2. **Build a test plan** based on the target URL and scope:
   - Home/landing page
   - Primary navigation paths (header, footer, sidebar)
   - Key user flows (auth, search, forms, checkout)
   - Interactive elements (buttons, dropdowns, modals)
   - Edge cases (empty states, error pages, 404, slow loading)

3. **If authentication is required:**
   - Locate the login/signup page
   - Use provided credentials or create a test account
   - Document the authenticated session state

**Tip:** Prioritize high-traffic pages and critical user flows first.

---

### Phase 2: Explore & Document

**Objective:** Navigate each page, capture state, and log any anomalies.

For each page in your test plan:

1. **Navigate:**
   ```
   browser_navigate(url="https://example.com/path")
   ```

2. **Wait for the page to settle** — allow dynamic content to load.

3. **Capture console state:**
   ```
   browser_console(clear=true)
   ```
   Log any errors, warnings, or unhandled exceptions. Do this after every navigation.

4. **Take a DOM snapshot:**
   ```
   browser_snapshot()
   ```
   This reveals the page structure and helps identify missing or broken elements.

5. **Capture visual evidence:**
   ```
   browser_vision(question="Describe the page layout, identify any visual issues, broken elements, or accessibility concerns. Note the current URL.", annotate=true)
   ```
   The `annotate=true` flag adds numbered `[1]`, `[2]`, `[3]` labels on interactive elements — use these to reference specific elements in your bug reports.

6. **Document findings immediately** in your notes:
   - Page URL
   - Issue description
   - Screenshot filename
   - Console errors (if any)
   - Element reference number (if applicable)

---

### Phase 3: Interact & Stress Test

**Objective:** Test functionality by interacting with elements and pushing boundaries.

For each interactive element:

1. **Click actions:**
   - Primary buttons (submit, save, continue)
   - Navigation links
   - Icon buttons, toggles, checkboxes
   - Hover states and tooltips

2. **Form inputs:**
   - Enter valid data, submit, verify results
   - Enter invalid data (empty, too long, special characters)
   - Test edge cases (max length, required fields, format validation)
   - Check if error messages are clear and helpful

3. **Keyboard interactions:**
   - Tab navigation order
   - Enter to submit forms
   - Escape to close modals/dropdowns

4. **After each interaction:**
   ```
   browser_console(clear=false)  # Check for new errors
   browser_snapshot()            # Verify state change
   ```

5. **Common edge cases to test:**
   - Empty search results
   - Form submission with missing required fields
   - Network timeout or slow loading
   - Session expiration during form entry
   - Browser back button behavior

---

### Phase 4: Capture Evidence

**Objective:** Gather irrefutable proof for every bug found.

For each issue identified:

1. **Screenshot** — capture the visual state at the moment the bug occurs.

2. **Console log** — record all errors and warnings:
   ```
   browser_console(clear=false)
   ```

3. **DOM context** — note the element structure:
   ```
   browser_snapshot()
   ```
   Identify CSS classes, IDs, and hierarchy for developer reference.

4. **Steps to reproduce** — document the exact sequence:
   - URL at start
   - Actions taken (click, type, scroll)
   - Expected behavior
   - Actual behavior

5. **Name your files descriptively:**
   ```
   screenshots/
   ├── home-page-broken-layout.png
   ├── login-form-missing-validation-error.png
   ├── checkout-console-error.png
   └── search-empty-state-missing.png
   ```

---

### Phase 5: Compile Report

**Objective:** Produce a structured, actionable bug report.

Generate `report.md` with this structure:

markdown
# Dogfood QA Report

**Target URL:** [url]
**Test Date:** [date]
**Scope:** [pages/features tested]
**Tester:** [agent identifier]

---

## Summary

- **Total issues found:** [N]
- **Critical:** [N] (issues blocking core functionality)
- **High:** [N] (significant UX/functionality problems)
- **Medium:** [N] (visual or minor functional issues)
- **Low:** [N] (cosmetic or minor inconveniences)

---

## Critical Issues

### [Bug Title]

**URL:** [page where found]
**Severity:** Critical
**Element:** [.class-name or #id from snapshot]

**Steps to reproduce:**
1. Navigate to [url]
2. [Action 1]
3. [Action 2]
4. [Bug occurs]

**Expected behavior:** [what should happen]
**Actual behavior:** [what happens instead]

**Evidence:**
- Screenshot: `screenshots/filename.png`
- Console: `console-logs/filename.txt`

---

## High Issues

[... same structure ...]

---

## Medium Issues

[... same structure ...]

---

## Low Issues

[... same structure ...]

---

## Console Errors Summary

[List all unique JS errors encountered across the session]

---

## Notes

[Any additional observations, patterns noticed, or recommendations]
---

## Severity Classification

| Level | Criteria |
|-------|----------|
| **Critical** | App crash, data loss, security vulnerability, blocking core user flows |
| **High** | Major feature broken, data corruption risk, significant UX failure |
| **Medium** | Visual glitch, suboptimal UX, partial feature failure |
| **Low** | Typo, spacing issue, minor inconvenience, non-blocking |

---

## Common Bugs to Watch For

- **Visual:** Missing images, broken layout, overlapping elements, cut-off text, wrong fonts/colors
- **Functional:** Buttons that don't work, forms that don't submit, data that doesn't save, redirects that fail
- **Console:** JavaScript errors, unhandled exceptions, failed network requests, warnings about deprecated APIs
- **Accessibility:** Missing alt text, low contrast, no keyboard navigation, missing form labels
- **Edge cases:** Empty states with no message, error pages that crash, data that overflows containers

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Page doesn't load | Check URL, network connectivity, and if the site is down |
| Element not found in snapshot | Wait longer for JS to render, or the element may be in a shadow DOM |
| Click doesn't work | Use `browser_press` with Enter, or scroll to element first |
| Console shows no errors but bug exists | Check network tab, try triggering the bug differently |
| Screenshots look different than expected | The app may be A/B testing or rendering differently — document both states |

---

## Notes

- **Be thorough but efficient:** Focus on high-impact areas first. You can always go deeper if time permits.
- **Document everything:** If in doubt, capture it. Screenshots are cheap; missed bugs are expensive.
- **Test mobile viewport:** If the user didn't specify, consider testing at mobile width (375px) since responsive bugs are common.
- **Stay objective:** Report what you observe, not interpretations of intent. Let the developers decide if it's a bug.