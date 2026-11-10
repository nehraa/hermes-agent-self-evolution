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

| Input | Required | Description |
|-------|----------|-------------|
| **Target URL** | Yes | The entry point for testing |
| **Scope** | Yes | What areas/features to focus on, or `"full site"` for comprehensive testing |
| **Output directory** | No | Where to save screenshots and the report (default: `./dogfood-output`) |

## Workflow

Follow this 6-phase systematic workflow:

---

### Phase 1: Plan

1. Create the output directory structure:
   ```
   {output_dir}/
   ├── screenshots/       # Evidence screenshots
   └── report.md          # Final report (generated in Phase 5)
   ```

2. Identify the testing scope based on user input.

3. Build a sitemap and test plan covering:
   - Landing/home page
   - Navigation links (header, footer, sidebar)
   - Key user flows (signup, login, search, checkout)
   - Forms and interactive elements
   - Edge cases (empty states, error pages, 404s)

---

### Phase 2: Explore

For each page or feature in your plan:

1. **Navigate** to the page:
   ```
   browser_navigate(url="https://example.com/page")
   ```

2. **Take a snapshot** to understand the DOM structure:
   ```
   browser_snapshot()
   ```

3. **Check the console** for JavaScript errors:
   ```
   browser_console(clear=true)
   ```
   Do this after every navigation and after every significant interaction. Silent JS errors are high-value findings.

4. **Capture an annotated screenshot** to visually assess the page:
   ```
   browser_vision(question="Describe the page layout, identify any visual issues, broken elements, or accessibility concerns", annotate=true)
   ```
   The `annotate=true` flag overlays numbered `[N]` labels on interactive elements.

---

### Phase 3: Interact

For each interactive element you identified:

1. **Click** or **type** to interact:
   ```
   browser_click(ref="N")
   browser_type(ref="N", text="value")
   browser_press(key="Enter")
   ```

2. **Verify results** after each interaction:
   - Did the expected action occur?
   - Are there console errors?
   - Is the response appropriate?
   - Are there visual glitches?

3. **Test edge cases**:
   - Empty inputs
   - Invalid data (special characters, SQL injection patterns, XSS patterns)
   - Maximum length inputs
   - Missing required fields

4. **Capture evidence** for any issues found:
   ```
   browser_vision(question="What's wrong in this screenshot?", annotate=false)
   ```
   Save the output as `{output_dir}/screenshots/bug-{timestamp}-{description}.png`

---

### Phase 4: Document

For each bug found, record:

| Field | Description |
|-------|-------------|
| **Bug ID** | Sequential identifier (BUG-001, BUG-002, etc.) |
| **Page/URL** | Where the bug occurs |
| **Element** | What triggered it (button, form field, etc.) |
| **Expected behavior** | What should happen |
| **Actual behavior** | What actually happens |
| **Severity** | Critical / High / Medium / Low |
| **Evidence** | Screenshot filenames |
| **Console errors** | Any JS errors captured |

---

### Phase 5: Report

Generate `report.md` in the output directory with this structure:

markdown
# QA Test Report: {Application Name}

**Test Date:** {timestamp}
**Tester:** Claude
**Scope:** {scope description}

## Summary

- Total pages tested: N
- Total bugs found: N
- Critical: N | High: N | Medium: N | Low: N

## Bugs

### BUG-001: {Title}

- **URL:** ...
- **Severity:** ...
- **Expected:** ...
- **Actual:** ...
- **Evidence:** ...
- **Console Errors:** ...
---

### Phase 6: Deliver

1. Present the summary to the user:
   - Total bugs by severity
   - Most critical findings
   - Any patterns noticed

2. Confirm all evidence files are saved in the output directory.

3. Offer to dive deeper into any specific bug if the user wants more investigation.

## Severity Definitions

| Level | Description |
|-------|-------------|
| **Critical** | Security vulnerability, data loss, or application crash |
| **High** | Core functionality broken, no workaround |
| **Medium** | Feature impaired, workaround exists |
| **Low** | Cosmetic issue, minor inconvenience |

## Tips

- **Be thorough**: Test both positive and negative paths
- **Check console frequently**: Many bugs are silent failures
- **Document as you go**: Don't rely on memory at the end
- **Reproduce bugs**: Verify issues occur consistently before reporting
- **Prioritize**: Focus on user-impacting issues first