---
name: browser-contenteditable-workaround
description: Bypass React/Vue/Tiptap contenteditable editors that reset normal Playwright input — use document.execCommand('insertText', ...)
category: browser-use
---

# Workaround: Text Input on React/Vue Contenteditable Editors

## The Problem

Modern rich-text editors (React, Vue, Tiptap, ProseMirror) built on `contenteditable` intercept and reset most text insertion methods:

| Method | Result |
|--------|--------|
| `element.innerHTML = text` | Resets on next render cycle |
| `document.execCommand('insertHTML', ...)` | Blocked by synthetic events |
| `InputEvent` / `KeyboardEvent` dispatch | Ignored or overwritten |
| `browser_type` tool | Text disappears immediately |
| `page.keyboard.type()` | Same — editor resets input |

The editor appears empty. Placeholder classes (`is-empty`, `is-editor-empty`) persist. The text never lands.

## The Fix

javascript
const editor = document.querySelector('[contenteditable="true"]');
editor.focus();
document.execCommand('insertText', false, 'your prompt text here');
`execCommand('insertText', ...)` predates React's event system and writes directly to the DOM selection, bypassing synthetic events entirely.

## Full Workflow Example

### Step 1: Navigate
javascript
browser_navigate('https://console.pixelbin.io/organization/<org_id>/studio/ai-image-generator');
### Step 2: Focus the Editor
javascript
const editor = document.querySelector('[contenteditable="true"]');
editor.focus();
**Critical:** The editor must be focused before `execCommand` runs.

### Step 3: Insert Text
javascript
document.execCommand('insertText', false, 'a majestic fox in snowy forest, cinematic photography');
### Step 4: Verify Insertion
javascript
// Wait a tick for DOM to settle
await new Promise(r => setTimeout(r, 100));

// Check innerHTML — should contain <p>your text</p>
editor.innerHTML;
// Returns: '<p>a majestic fox in snowy forest, cinematic photography</p>'
**Do not check for absence of placeholder classes** — they may persist even after text lands. Verify the actual `<p>` node exists.

### Step 5: Trigger Submit Button
javascript
// Button may still be disabled after text insert
// Click outside the editor first to force React state update
document.body.click();
await new Promise(r => setTimeout(r, 200));

// Now click Generate
browser_click('ref for Generate button');
## Why This Works

React 16+ uses synthetic events for `onChange`/`onInput`. Most text insertion methods trigger these events, which React intercepts and resets.

`execCommand('insertText')` is a legacy browser command that:
1. Writes directly to the active DOM selection
2. Bypasses React's synthetic event listener
3. Predates modern frontend frameworks (still functional, though officially deprecated)

## Pitfalls

- **Placeholder classes persist** — Don't check `is-empty`/`is-editor-empty`. Check `innerHTML` for actual content nodes.

- **Editor must be focused** — `execCommand` returns `false` if the editor lacks focus. Always call `editor.focus()` first.

- **Shadow DOM isolation** — If the editor is inside a shadow DOM, `execCommand` operates on the shadow root's selection, not the light DOM. Target the shadow root explicitly:
  ```javascript
  const shadowHost = document.querySelector('my-component');
  const shadowRoot = shadowHost.shadowRoot;
  const editor = shadowRoot.querySelector('[contenteditable="true"]');
  editor.focus();
  shadowRoot.execCommand('insertText', false, 'prompt');
  ```

- **Button stays disabled** — After text lands, React may not update the button state until the next user interaction. Click elsewhere (`document.body.click()`) or dispatch a `blur` event to force state recalculation.

- **execCommand returns false** — Indicates focus issue or shadow DOM isolation. Verify focus with `document.activeElement === editor`.

## Debug Checklist

javascript
// 1. Is the editor focused?
document.activeElement === editor;  // Should be true

// 2. Does execCommand succeed?
const result = document.execCommand('insertText', false, 'test');
result;  // Should be true

// 3. Does innerHTML contain the text?
editor.innerHTML.includes('test');  // Should be true

// 4. Is there a shadow DOM?
editor.getRootNode() !== document;  // True means shadow DOM