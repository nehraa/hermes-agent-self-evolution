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
| **Target URL** | Yes | The entry point for testing |
| **Scope** | Yes | What areas/features to focus on (or "full site" for comprehensive testing) |
| **Output directory** | No | Where to save screenshots and the report (default: `./dogfood-output`) |

## Workflow

Follow this 5-phase systematic workflow:

---

### Phase 1: Plan

1. **Create the output directory structure:**

bash
{output_dir}/
├── screenshots/       # Evidence screenshots
│   ├── 01-home-page.png
│   ├── 02-signup-form.png
│   └── 03-login-error.png
└── report.md          # Final report (generated in Phase 5)
2. **Identify testing scope** based on user input:
   - Specific pages/features requested
   - General areas (e-commerce checkout, dashboard, etc.)
   - Full site coverage

3. **Build a testing checklist** covering:

   | Category | Examples |
   |----------|----------|
   | Landing/Home | Hero section, CTAs, branding |
   | Navigation | Header links, footer links, breadcrumbs, mobile menu |
   | User Flows | Sign up, login/logout, password reset |
   | Forms | Input validation, required fields, submission |
   | Search | Search bar, filters, results display |
   | Data Display | Tables, lists, pagination, empty states |
   | Error Handling | 404 pages, 500 errors, network failures |
   | Accessibility | Keyboard navigation, screen reader labels |

---

### Phase 2: Explore

For each page or feature in your plan:

1. **Navigate** to the page:
   ```
   browser_navigate(url="https://example.com/page")
   ```

2. **Capture DOM snapshot** to understand structure:
   ```
   browser_snapshot()
   ```

3. **Check for JavaScript errors**:
   ```
   browser_console(clear=true)
   ```
   > **Critical:** Do this after every navigation and after every significant interaction. Silent JS errors are high-value findings.

4. **Take an annotated screenshot** to visually assess the page:
   ```
   browser_vision(
     question="Describe the page layout, identify any visual issues, broken elements, or accessibility concerns",
     annotate=true
   )
   ```
   The `annotate=true` flag overlays numbered `[N]` labels on interactive elements. Use these numbers to reference elements in `browser_click` and `browser_type` commands.

5. **Save the screenshot** with a descriptive filename:
   ```
   screenshots/{sequence}-{page-name}-{context}.png
   ```
   Example: `03-home-hero-section.png`

---

### Phase 3: Interact

Systematically test interactive elements:

1. **Click navigation and links** to verify routing:
   ```
   browser_click(ref="[N]")
   browser_snapshot()
   browser_console(clear=true)
   ```
   Then `browser_back()` to return to the previous page.

2. **Fill out forms** with various inputs:
   ```
   browser_type(ref="[N]", text="test value")
   ```

   Test these input categories:

   | Test Type | Values to Try |
   |-----------|---------------|
   | Valid input | Normal user data (e.g., "test@example.com") |
   | Empty input | Leave blank, submit |
   | Boundary values | Max/min length strings, zero, negative numbers |
   | Special characters | `<script>`, SQL fragments, Unicode, emojis |
   | Format variations | Invalid emails, wrong phone formats |

3. **Test edge cases:**

   - **Empty states**: Products with no reviews, search with no results
   - **Loading states**: Slow networks, timeout handling
   - **Error states**: Disconnect network mid-request
   - **Concurrent actions**: Multiple rapid clicks, double submissions

4. **Verify responsive behavior** (if scope includes):
   - Resize browser window and observe layout shifts
   - Test touch/click targets on mobile-sized viewports

---

### Phase 4: Document Findings

For each bug discovered:

1. **Capture evidence immediately:**
   - Screenshots (annotated if helpful)
   - Console logs (copy relevant errors)
   - Network request/response (if accessible)

2. **Document with this structure:**

markdown
### [BUG-##] Title

**Severity:** Critical / High / Medium / Low  
**Page:** URL or location  
**Environment:** Browser, OS (if known)

**Steps to Reproduce:**
1. Navigate to...
2. Click on...
3. Enter...

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Evidence:**
![screenshot](screenshots/filename.png)

**Console Output:**
[paste relevant console errors]
**Notes:**
[Any additional context]
---

### Phase 5: Report

Compile all findings into a structured report:

markdown
# QA Test Report: {Application Name}

**Date:** {timestamp}  
**Tester:** {agent identifier}  
**Scope:** {testing scope}  
**Target URL:** {entry point}

## Summary

- **Total Issues Found:** N
- **Critical:** N | **High:** N | **Medium:** N | **Low:** N

## Findings

[All documented bugs, ordered by severity]

## Out of Scope

[Features/pages not tested]

## Recommendations

[Suggested priority fixes, testing improvements for next iteration]
**Deliver to the user:**
1. The final report markdown
2. The screenshots directory (or paths to saved screenshots)
3. Summary of critical/high severity issues found

---

## Quick Reference: Browser Commands

| Command | Purpose |
|---------|---------|
| `browser_navigate(url="...")` | Go to a URL |
| `browser_snapshot()` | Capture DOM structure |
| `browser_click(ref="[N]")` | Click annotated element |
| `browser_type(ref="[N]", text="...")` | Type into input field |
| `browser_vision(question="...", annotate=true)` | Analyze page with annotated labels |
| `browser_console(clear=true)` | Check for JS errors |
| `browser_scroll(direction="down\|up", distance=N)` | Scroll the page |
| `browser_back()` | Navigate to previous URL |
| `browser_press(key="...")` | Press keyboard key (Enter, Tab, etc.) |