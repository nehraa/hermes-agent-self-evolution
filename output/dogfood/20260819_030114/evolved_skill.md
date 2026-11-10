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

- Browser toolset must be available (`browser_navigate`, `browser_snapshot`, `browser_click`, `browser_type`, `browser_vision`, `browser_console`, `browser_scroll`, `browser_back`, `browser_press`)
- A target URL and testing scope from the user

## Inputs

The user provides:

| Input | Required | Description |
|-------|----------|-------------|
| Target URL | Yes | The entry point for testing (e.g., `https://example.com`) |
| Scope | Yes | What areas/features to focus on, or "full site" for comprehensive testing |
| Output directory | No | Where to save screenshots and the report (default: `./dogfood-output`) |

## Workflow

Follow this 5-phase systematic workflow:

### Phase 1: Plan

1. **Create the output directory structure:**
   ```
   {output_dir}/
   ├── screenshots/
   │   ├── 001_homepage.png
   │   ├── 002_login_form.png
   │   └── ...
   └── report.md
   ```

2. **Identify the testing scope** based on user input. Confirm scope if ambiguous.

3. **Build a sitemap plan** listing pages and features to test:
   - Landing/home page
   - Navigation links (header, footer, sidebar)
   - Key user flows (sign up, login, search, checkout, settings, etc.)
   - Forms and interactive elements
   - Edge cases (empty states, error pages, 404s, timeout handling)

4. **Prioritize** high-impact areas first: auth flows, payment/checkout, data submission forms.

---

### Phase 2: Explore

For each page or feature in your plan, follow this sequence:

**1. Navigate to the page:**
bash
browser_navigate(url="https://example.com/page")
**2. Capture console errors (baseline):**
bash
browser_console(clear=true)
**3. Take a DOM snapshot to understand structure:**
bash
browser_snapshot()
**4. Take an annotated screenshot to identify interactive elements:**
bash
browser_vision(question="Describe the page layout. Identify any visual issues, broken elements, or accessibility concerns.", annotate=true)
> The `annotate=true` flag overlays numbered `[N]` labels on interactive elements. Use these numbers with `browser_click` and `browser_type` to target specific elements.

**5. Scroll through the page** to capture full content:
bash
browser_scroll(direction="down", amount=3)
# Take snapshots/screenshots at key scroll positions
---

### Phase 3: Test

Systematically test functionality and interactions:

**Navigation & Links:**
- Click all navigation items (header, footer, sidebar)
- Verify links go to correct destinations
- Check for broken links (404s, 500s)
bash
browser_click(element="[N]")  # Use annotation numbers
browser_back()
**Forms & Inputs:**
- Fill out each form field
- Test validation (required fields, format requirements)
- Submit forms and verify success/error states
- Test edge cases: special characters, very long input, empty submission
bash
browser_type(element="[N]", text="test input")
browser_press(key="Enter")
**User Flows:**
- Complete critical journeys end-to-end (registration, login, purchase, etc.)
- Verify data persists correctly across steps
- Check redirect behavior

**Error Handling:**
- Trigger error states deliberately
- Verify error messages are clear and actionable
- Check if errors break the UI or leak sensitive information

**Console Monitoring:**
After every navigation and every significant interaction, check for JavaScript errors:
bash
browser_console(clear=false)
> Silent JS errors are high-value findings. Log each error with a screenshot for evidence.

---

### Phase 4: Document

For every issue found, capture structured evidence:

**Required evidence per bug:**

| Evidence Type | Tool | When to Capture |
|---------------|------|-----------------|
| Screenshot (annotated) | `browser_vision(annotate=true)` | Every page state with issues |
| Console output | `browser_console(clear=false)` | Every JS error |
| DOM snapshot | `browser_snapshot()` | Complex DOM-related bugs |
| Console logs | `browser_console()` | Warnings, info messages |

**Bug entry format:**
markdown
### Bug #[N]: [Short Title]

**Severity:** Critical / High / Medium / Low
**Category:** UI/Visual, Functionality, Performance, Accessibility, Security, Other
**Page:** [URL where found]
**Environment:** [Browser/OS if relevant]

**Steps to Reproduce:**
1. Navigate to [URL]
2. Click on [element]
3. Observe [result]

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Evidence:**
- Screenshot: `screenshots/xxx.png`
- Console: [relevant console output]

**Notes:**
[Additional context, impact, workaround]
**Naming convention for screenshots:**
{issue_type}_{page}_{action}.png
Examples:
- bug_login_validation_error.png
- ui_homepage_broken_image.png
- perf_search_slow_response.png
---

### Phase 5: Report

Compile findings into a structured report.

**Report structure:**

markdown
# QA Test Report: [Application Name]

**Test Date:** [Date]
**Tester:** [Identifier]
**Target URL:** [URL]
**Scope:** [Scope description]
**Total Bugs Found:** [N]

---

## Executive Summary

[Brief overview of testing results, overall quality assessment, critical findings requiring immediate attention]

## Testing Scope

- Pages tested: [list]
- Features tested: [list]
- User flows covered: [list]

## Severity Summary

| Severity | Count | Description |
|----------|-------|-------------|
| Critical | N | Data loss, security vulnerabilities, complete feature breakage |
| High | N | Major functionality broken, significant UX impact |
| Medium | N | Partial functionality affected, workaround available |
| Low | N | Minor issues, cosmetic defects, improvements |

## Detailed Findings

[Include all bug entries from Phase 4]

---

## Recommendations

1. [Priority fixes]
2. [Process improvements]
3. [Testing gaps to address]

## Appendix

- Screenshots: `{output_dir}/screenshots/`
- Tools used: Browser toolset
- Session duration: [approximate time]
---

## Quick Reference

### Essential Commands

bash
# Navigation
browser_navigate(url="<url>")
browser_back()

# Screenshot & Vision
browser_vision(question="<question>", annotate=true)
browser_snapshot()

# Interaction
browser_click(element="[N]")
browser_type(element="[N]", text="<text>")
browser_scroll(direction="down|up", amount=<N>)

# Diagnostics
browser_console(clear=<true|false>)
browser_press(key="<key>")
### Common Bug Patterns to Watch For

- **Visual:** Broken images, misaligned layouts, overlapping elements, clipped text, missing fonts
- **Functional:** Buttons not responding, forms not submitting, data not saving, broken redirects
- **Accessibility:** Low contrast, missing alt text, keyboard traps, missing focus indicators
- **Performance:** Slow page loads, hanging requests, infinite loading states
- **Console:** JavaScript errors, failed API calls, unhandled promise rejections, warnings

### Severity Guidelines

| Level | Definition | Example |
|-------|------------|---------|
| **Critical** | Data loss, security issue, complete breakage | Payment processing fails, user data exposed |
| **High** | Major feature broken, no workaround | Login broken, checkout fails |
| **Medium** | Feature partially works, workaround exists | Search returns partial results |
| **Low** | Cosmetic, no functional impact | Typos, minor misalignment |