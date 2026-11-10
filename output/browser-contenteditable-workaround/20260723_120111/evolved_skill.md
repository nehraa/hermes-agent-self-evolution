---
name: browser-contenteditable-workaround
description: Bypass React/Vue/Tiptap contenteditable editors that reset normal Playwright input — use document.execCommand('insertText', ...)
category: browser-use
---

# Workaround: Text Input on React/Vue/Tiptap Contenteditable Editors

## Problem

Modern web apps (e.g., Pixelbin, Notion-style editors, Tiptap, ProseMirror) use `contenteditable` editors that ignore or reset text inserted via:

- `element.innerHTML = text`
- `document.execCommand('insertHTML', ...)`
- `InputEvent` / `KeyboardEvent` dispatch
- `browser_type` tool

**Symptoms:**
- Element appears empty after "insertion"
- Placeholder classes persist (`is-empty`, `is-editor-empty`)
- Form submission or state updates don't fire

## Solution

javascript
const editor = document.querySelector('[contenteditable="true"]');
editor.focus();
document.execCommand('insertText', false, 'your prompt text here');
`execCommand('insertText')` bypasses React's synthetic event system entirely.

## Complete Workflow Example

javascript
// 1. Navigate to the app
await browser_navigate('https://console.pixelbin.io/organization/<org_id>/studio/ai-image-generator');

// 2. Locate and focus the contenteditable editor
const editor = document.querySelector('[contenteditable="true"]');
editor.focus();

// 3. Insert text — this bypasses React's event system
document.execCommand('insertText', false, 'a majestic fox in snowy forest, cinematic photography');

// 4. Verify text landed
// Look for actual content nodes, NOT placeholder classes
editor.innerHTML;
// Returns: '<p>a majestic fox in snowy forest, cinematic photography</p>'

// 5. Click the Generate button (use ref from snapshot)
await browser_click('ref for Generate button');
## Why This Works

React 16+ uses synthetic events and **does not** listen to native DOM `input` events for `contenteditable` elements. Instead, it tracks changes via:

- `beforeinput` event
- Selection/range API
- Internal state management

`document.execCommand('insertText')` is a legacy browser command that predates React's event system. It writes directly to the DOM at the current selection, triggering the native input path React can intercept.

## Pitfalls and Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `execCommand` returns `false` | Editor not focused, or inside shadow DOM | Call `editor.focus()` first; check `editor.shadowRoot` |
| `innerHTML` still shows placeholder classes | Text inserted but not rendered yet | Wait 100-200ms for React to re-render |
| Generate button stays disabled | React state not updated after input | Click elsewhere to blur, or wait for debounce |
| Multiple editors on page | Wrong element selected | Use more specific selector: `document.querySelector('[contenteditable="true"][data-placeholder]')` |
| Editor inside iframe | Context mismatch | Switch to iframe first: `document.querySelector('iframe').contentDocument` |

## Verification Checklist

Before proceeding after text insertion:

- [ ] `editor.innerHTML` contains `<p>` tags with your text (not just placeholder)
- [ ] `editor.classList` does NOT contain `is-empty` or `is-editor-empty`
- [ ] Cursor is positioned inside the text (selection range exists)
- [ ] Submit/generate button reflects enabled state

## Fallback: Simulate Native Input

If `execCommand` fails (e.g., inside shadow DOM), try:

javascript
const editor = document.querySelector('[contenteditable="true"]');
editor.focus();

// Dispatch native input event manually
const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
nativeInputValueSetter.call(editor, 'your text here');

const inputEvent = new Event('input', { bubbles: true });
editor.dispatchEvent(inputEvent);
This overrides React's internal value tracker and fires a native `input` event.