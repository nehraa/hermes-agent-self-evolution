---
name: browser-contenteditable-workaround
description: Bypass React/Vue/Tiptap contenteditable editors that reset normal Playwright input — use document.execCommand('insertText', ...)
category: browser-use
---

# Workaround: Text Input on React/Vue Contenteditable Editors

## Problem

React 16+, Vue, Tiptap, and ProseMirror contenteditable editors (used in tools like Pixelbin, Notion-style editors, AI prompt fields) silently reject most text insertion methods:

| Method | Result |
|--------|--------|
| `element.innerHTML = text` | Stripped/ignored |
| `document.execCommand('insertHTML', ...)` | Stripped/ignored |
| `InputEvent` / `KeyboardEvent` dispatch | Silently discarded |
| `browser_type` tool default behavior | Often reset |

The editor visually shows no text, and placeholder classes (`is-empty`, `is-editor-empty`, `placeholder`) persist.

## Solution

javascript
const editor = document.querySelector('[contenteditable="true"]');
editor.focus();
document.execCommand('insertText', false, 'your text here');
`execCommand('insertText')` bypasses React's synthetic event system entirely.

## Full Workflow Example

javascript
// 1. Navigate to the editor
browser_navigate('https://console.pixelbin.io/organization/<org_id>/studio/ai-image-generator');

// 2. Wait for editor to render and focus it
await page.waitForSelector('[contenteditable="true"]');
const editor = page.locator('[contenteditable="true"]').first();
await editor.focus();

// 3. Insert text via execCommand
await page.evaluate(() => {
  document.execCommand('insertText', false, 'a majestic fox in snowy forest, cinematic photography');
});

// 4. Verify text landed — check for <p>text</p>, NOT placeholder classes
const html = await page.evaluate(() => {
  return document.querySelector('[contenteditable="true"]').innerHTML;
});
// Expected: '<p>a majestic fox in snowy forest, cinematic photography</p>'

// 5. Trigger React state update — click outside or wait
await editor.click(); // or await page.waitForTimeout(500);

// 6. Click the action button
browser_click('ref for Generate button');
## Why This Works

- React 16+ uses synthetic events and bypasses native DOM events for `onChange`/`onInput` handlers
- `document.execCommand('insertText')` is a legacy browser command that predates React's event system
- It writes directly to the DOM selection/clipboard layer — React cannot intercept it

> **Note:** `execCommand` is deprecated but still functional in all modern browsers.

## Pitfalls and Fixes

### Empty check shows placeholder classes
- **Cause:** Classes are added based on `innerText` length, not `innerHTML`
- **Fix:** Verify via `page.evaluate(() => editor.innerText.trim())` — check text length, not CSS classes

### Editor must be focused before `execCommand`
- **Cause:** `execCommand` operates on the active selection
- **Fix:** Always call `editor.focus()` first

### Button stays disabled after text lands
- **Cause:** React state hasn't updated yet
- **Fix:** Click elsewhere on the page, then click the button — or add a short wait

### `execCommand` returns `false`
- **Cause:** Editor not focused, element hidden, or inside a shadow DOM
- **Fix:** 
  ```javascript
  // Verify focus state
  const hasFocus = await page.evaluate(() => {
    const el = document.querySelector('[contenteditable="true"]');
    return el === document.activeElement;
  });
  
  // Check for shadow DOM
  const isShadow = await page.evaluate(() => {
    return document.querySelector('[contenteditable="true"]').shadowRoot !== null;
  });
  ```

### Text inserted but not visible
- **Cause:** Editor may have max-height or overflow constraints
- **Fix:** Scroll into view before inserting, or check parent container styles

## Complete Troubleshooting Checklist

1. Editor element exists? → `document.querySelector('[contenteditable="true"]')`
2. Editor is focused? → `document.activeElement === editor`
3. Editor is visible? → Not `display: none` or `visibility: hidden`
4. Editor is not in shadow DOM? → No `shadowRoot` parent
5. Text actually inserted? → Check `editor.innerText` or `editor.innerHTML`
6. React state updated? → Click elsewhere or wait 500ms
7. Button enabled? → Check button's `disabled` attribute or class

## Edge Cases

- **Multiple editors:** Use `page.locator('[contenteditable="true"]').first()` or target by parent container
- **Nested contenteditable:** Find the innermost element: `document.querySelector('[contenteditable="true"]:not([contenteditable="true"] *)')`
- **Tiptap with extensions:** Some extensions intercept `execCommand` — may need to trigger via keyboard shortcut simulation instead