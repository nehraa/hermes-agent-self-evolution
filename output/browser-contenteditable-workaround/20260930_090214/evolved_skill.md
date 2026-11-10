---
name: browser-contenteditable-workaround
description: Bypass React/Vue/Tiptap contenteditable editors that reset normal Playwright input — use document.execCommand('insertText', ...)
category: browser-use
---

# Workaround: Text Input on React/Vue Contenteditable Editors

## The Problem

Modern web apps (Pixelbin, Notion, Tiptap, ProseMirror, etc.) use `contenteditable` editors built with React, Vue, or similar frameworks. These editors **ignore or reset** text inserted via common methods:

| Method | Result |
|--------|--------|
| `element.innerHTML = text` | Text appears briefly, then gets cleared |
| `document.execCommand('insertHTML', ...)` | Text stripped or ignored |
| `InputEvent` / `KeyboardEvent` dispatch | React synthetic events don't fire |
| `browser_type` tool with keyboard input | Characters rejected or lost |
| `element.sendKeys()` | Same issue — framework blocks it |

**Symptoms:** The editor shows no visible text, and `is-empty` / `is-editor-empty` placeholder classes persist even after "insertion."

## The Solution

javascript
// 1. Locate the contenteditable element
const editor = document.querySelector('[contenteditable="true"]');

// 2. Focus it — REQUIRED
editor.focus();

// 3. Insert text directly into the DOM selection
document.execCommand('insertText', false, 'your text here');
`execCommand('insertText', ...)` bypasses React's synthetic event system because it's a legacy browser command that writes directly to the DOM selection.

## Full Workflow Example

javascript
// Navigate to the app
browser_navigate('https://console.pixelbin.io/organization/<org_id>/studio/ai-image-generator');

// Wait for editor to be present and visible
await page.waitForSelector('[contenteditable="true"]', { state: 'visible' });

// Focus the editor (critical!)
const editor = page.locator('[contenteditable="true"]').first();
await editor.focus();

// Insert text via execCommand
await page.evaluate(() => {
  document.execCommand('insertText', false, 'a majestic fox in snowy forest, cinematic photography');
});

// Verify text landed — look for <p>text</p> nodes, NOT placeholder classes
const html = await page.evaluate(() => {
  return document.querySelector('[contenteditable="true"]')?.innerHTML;
});
console.log('Editor HTML:', html);
// Expected: '<p>a majestic fox in snowy forest, cinematic photography</p>'

// Click Generate button
browser_click('ref for Generate button');
## Why This Works

React 16+ uses a synthetic event pool and bypasses native DOM events for `onChange` and `onInput` handlers. The `execCommand('insertText')` command:

1. Predates React's event system (introduced in browsers before 2015)
2. Writes directly to the DOM selection/clipboard layer
3. React cannot intercept or reset it

> **Note:** `execCommand` is deprecated but still functional in all modern browsers.

## Common Pitfalls

### Placeholder classes persist

javascript
// DON'T check for this — it often stays even after text is inserted
editor.classList.contains('is-empty')  // Still true even with text!

// DO check for actual content nodes
const hasTextNode = await page.evaluate(() => {
  const p = document.querySelector('[contenteditable="true"] p');
  return p && p.textContent.length > 0;
});
### Editor not focused

javascript
// This fails silently
document.execCommand('insertText', false, 'text');  // Returns false if not focused

// Always focus first
editor.focus();
const success = document.execCommand('insertText', false, 'text');
console.log('Insertion succeeded:', success);  // true = worked
### Button still disabled after text insertion

React's state may not update immediately after DOM changes. Solutions:

javascript
// Option 1: Wait briefly
await page.waitForTimeout(500);

// Option 2: Click outside to trigger blur/focus cycle
await editor.click();
await page.keyboard.press('Tab');

// Option 3: Use keyboard input after focus
await editor.focus();
await page.keyboard.type('prompt text', { delay: 10 });
### Editor inside Shadow DOM

If `execCommand` returns `false` and focus works, the editor may be in a shadow root:

javascript
// Find shadow root
const shadowHost = document.querySelector('custom-editor');
const shadowRoot = shadowHost.shadowRoot;
const editor = shadowRoot.querySelector('[contenteditable="true"]');
editor.focus();
document.execCommand('insertText', false, 'text');
## Troubleshooting Checklist

- [ ] Editor element exists: `document.querySelector('[contenteditable="true"]')`
- [ ] Editor is visible and rendered
- [ ] `editor.focus()` was called before `execCommand`
- [ ] `execCommand` returned `true`
- [ ] Actual DOM contains `<p>text</p>` or similar nodes
- [ ] Button is enabled (if not, try blur/click cycle)
- [ ] No JS errors in console

## Alternative Approaches

If `execCommand` fails, try these in order:

1. **Triple-click + paste:**
   ```javascript
   await editor.click({ clickCount: 3 });
   await page.paste('your text');
   ```

2. **Dispatch keyboard events with proper composition:**
   ```javascript
   await editor.focus();
   await page.keyboard.type('text', { delay: 50 });
   ```

3. **Simulate IME input:**
   ```javascript
   await page.evaluate(() => {
     const inputEvent = new InputEvent('input', {
       bubbles: true,
       cancelable: true,
       data: 'text'
     });
     editor.dispatchEvent(inputEvent);
   });
   ```

4. **Click-based position + paste:**
   ```javascript
   await editor.click();
   await page.paste('text');