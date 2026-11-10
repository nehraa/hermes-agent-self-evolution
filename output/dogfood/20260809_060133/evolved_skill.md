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

### Phase 1: Plan

1. Create the output directory structure:

   ```
   {output_dir}/
   ├── screenshots/       # Evidence screenshots
   │   ├── 001-home-page.png
   │   ├── 002-login-form.png
   │   └── ...
   └── report.md          # Final report (generated in Phase 5)
   ```

2. Identify the testing scope based on user input.
3. Build a rough sitemap by planning which pages and features to test:
   - Landing/home page
   - Navigation links (header, footer, sidebar)
   - Key user flows (sign up, login, search, checkout, settings)
   - Forms and interactive elements
   - Edge cases (empty states, error pages, 404s)

### Phase 2: Explore

For each page or feature in your plan:

1. **Navigate** to the page:
   ```bash
   browser_navigate(url="https://example.com/page")
   ```

2. **Take a snapshot** to understand the DOM structure:
   ```bash
   browser_snapshot()
   ```

3. **Check the console** for JavaScript errors:
   ```bash
   browser_console(clear=true)
   ```
   Do this after every navigation and after every significant interaction. Silent JS errors are high-value findings.

4. **Take an annotated screenshot** to visually assess the page and identify interactive elements:
   ```bash
   browser_vision(question="Describe the page layout, identify any visual issues, broken elements, or accessibility concerns", annotate=true)
   ```
   The `annotate=true` flag overlays numbered `[N]` labels on interactive elements. Each `[N]` maps to a specific element you can reference.

5. **Save the screenshot** for evidence:
   ```bash
   # Use browser_vision with save option or external tool
   browser_vision(question="Save this screenshot", save_path="{output_dir}/screenshots/XXX-description.png")
   ```

### Phase 3: Interact

Systematically test interactions:

1. **Click elements** and verify behavior:
   ```bash
   browser_click(selector="[N]")  # Use the [N] from annotation
   ```

2. **Type in forms** with both valid and invalid data:
   ```bash
   browser_type(selector="[N]", text="test input")
   ```

3. **Test edge cases**:
   - Submit empty forms
   - Enter special characters (`<`, `>`, `'`, `"`, `&`, emoji)
   - Enter very long strings
   - Enter SQL injection / XSS patterns
   - Test boundary values (max length, min values)

4. **Press keys** for keyboard navigation:
   ```bash
   browser_press(key="Enter")
   browser_press(key="Tab")
   ```

5. **Scroll** to test lazy loading and infinite scroll:
   ```bash
   browser_scroll(direction="down", amount=3)
   ```

6. **Navigate back** to test state preservation:
   ```bash
   browser_back()
   ```

### Phase 4: Document

For each bug found, record:

| Field | Description | Example |
|-------|-------------|---------|
| **ID** | Sequential bug number | `BUG-001` |
| **Title** | Brief summary | "Login form accepts invalid email format" |
| **Severity** | Impact level | Critical / High / Medium / Low |
| **Page** | Where found | `/login` |
| **Steps to Reproduce** | How to trigger | 1. Navigate to /login 2. Type `notanemail` 3. Click Submit |
| **Expected** | What should happen | "Error: Please enter a valid email" |
| **Actual** | What happened | "Form submitted with invalid email" |
| **Evidence** | Screenshots/logs | `screenshots/bug-001.png`, console log snippet |
| **Console Errors** | JS errors if any | `Uncaught TypeError: Cannot read property 'value' of null` |

### Phase 5: Report

Generate `report.md` with this structure:

markdown
# QA Test Report: {Application Name}

**Test Date:** {date}
**Tester:** {agent}
**URL Tested:** {target_url}
**Scope:** {scope}

## Summary

- Total bugs found: N
- Critical: N
- High: N
- Medium: N
- Low: N

## Bug Details

### BUG-001: {Title}
- **Severity:** {level}
- **Page:** {page}
- **Steps to Reproduce:**
  1. ...
- **Expected:** ...
- **Actual:** ...
- **Evidence:** {screenshot path}
- **Console Errors:** {any errors}

---

<!-- Repeat for each bug -->

## Browser Console Log Summary

<!-- Copy relevant console errors -->
## Quick Reference

### Test Checklist

- [ ] Homepage loads without errors
- [ ] All navigation links work
- [ ] Forms validate input correctly
- [ ] Error states display properly
- [ ] Empty states handled gracefully
- [ ] 404/500 pages exist and look correct
- [ ] Console has no JS errors
- [ ] Responsive elements work (mobile if applicable)

### Severity Definitions

| Level | Description |
|-------|-------------|
| **Critical** | Data loss, security vulnerability, app crash, blocked user flow |
| **High** | Major feature broken, workarounds needed |
| **Medium** | Feature degraded, non-blocking issue |
| **Low** | Cosmetic, minor UX annoyance, typographical |

### Common Bug Patterns to Look For

1. **Visual**: Broken images, misaligned elements, overlapping text, cut-off content
2. **Functional**: Buttons don't work, forms don't submit, data doesn't save
3. **Validation**: Missing/inadequate input validation
4. **Navigation**: Dead links, missing back buttons, broken breadcrumbs
5. **Accessibility**: Missing alt text, low contrast, no keyboard navigation
6. **Performance**: Slow page loads, spinner that never stops
7. **Security**: Unprotected inputs, sensitive data in URL params
8. **Responsive**: Layout breaks on resize, horizontal scroll on mobile