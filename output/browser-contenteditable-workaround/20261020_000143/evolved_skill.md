---
name: browser-contenteditable-workaround
description: Bypass React/Vue/Tiptap contenteditable editors that reset normal Playwright input — use document.execCommand('insertText', ...)
category: browser-use
---

# Workaround: Text Input on React/Vue/Tiptap Contenteditable Editors

## The Problem

React 16+, Vue 2+, Tiptap, and ProseMirror contenteditable editors in modern web apps (e.g., Notion-style editors, Pixelbin, SaaS rich-text fields) silently discard or reset text inserted via standard Playwright/DOM methods:

- `element.innerHTML = text`
- `document.execCommand('insertHTML', ...)`
- `InputEvent` / `KeyboardEvent` dispatch
- `browser_type` tool

The editor appears visually empty afterward, and internal state classes like `is-empty`, `is-editor-empty`, or `is-empty--true` persist — preventing form submission, triggering validation errors, or keeping "Generate" buttons disabled.

## The Fix

javascript
const editor = document.querySelector('[contenteditable="true"]');
editor.focus();
document.execCommand('insertText', false, 'your prompt text here');
`execCommand('insertText', ...)` bypasses React's synthetic event system entirely and writes directly to the native DOM selection.

## Full Workflow Example: Pixelbin AI Image Generator

javascript
// 1. Navigate to the app
browser_navigate('https://console.pixelbin.io/organization/<org_id>/studio/ai-image-generator');

// 2. Locate and focus the contenteditable editor
const editor = document.querySelector('[contenteditable="true"]');
editor.focus();

// 3. Insert text via execCommand
document.execCommand('insertText', false, 'a majestic fox in snowy forest, cinematic photography');

// 4. Verify text landed — check for <p>text</p> nodes, NOT class attributes
editor.innerHTML;
// Returns: '<p>a majestic fox in snowy forest, cinematic photography</p>'

// 5. Wait for React state to update (editor may need blur or delay)
await new Promise(r => setTimeout(r, 300));

// 6. Click the Generate button
browser_click('ref for Generate button');
## Why This Works

| Approach | React Behavior |
|----------|----------------|
| `innerHTML` assignment | Overwrites DOM but does NOT fire `onChange`/`onInput` — React state remains unchanged |
| `dispatchEvent(new InputEvent(...))` | Synthetic events bypass native handlers — React ignores them |
| `execCommand('insertText')` | Legacy browser command predating React — writes directly to native selection/clipboard, React cannot intercept |

React 16+ uses synthetic event pooling and does not rely on native DOM events for its internal state. The `onChange` handler only fires on browser-native input events. `execCommand` is a legacy API (deprecated but universally functional) that writes directly to the native text layer.

## Common Pitfalls and Fixes

### 1. Editor not focused — `execCommand` returns `false`

javascript
// Wrong: calling execCommand without focus
document.execCommand('insertText', false, 'text'); // false — no effect

// Right: ensure focus first
editor.focus();
document.execCommand('insertText', false, 'text'); // true — success
### 2. Text lands but button still disabled

After text insertion, React's internal state may not update immediately. The button stays disabled until a native `input` event fires.

javascript
// Option A: blur then focus
editor.focus();
document.execCommand('insertText', false, 'prompt');
editor.blur();
await new Promise(r => setTimeout(r, 100));
editor.focus();

// Option B: wait for state propagation
await new Promise(r => setTimeout(r, 500));
### 3. `is-empty` class persists after text is inserted

The class attribute on the DOM element may lag behind React state. Check the actual content instead:

javascript
// Instead of:
editor.classList.contains('is-empty'); // unreliable

// Check actual DOM content:
editor.innerHTML.includes('<p>') && !editor.innerHTML.includes('placeholder');
### 4. Editor inside Shadow DOM

If `querySelector` returns `null`, the editor may be inside a shadow root:

javascript
// Find shadow root
const host = document.querySelector('custom-editor-element');
const shadowRoot = host.shadowRoot;
const editor = shadowRoot.querySelector('[contenteditable="true"]');
### 5. Multiple contenteditable elements

Narrow your selector to avoid inserting into the wrong editor:

javascript
// Instead of broad selector:
document.querySelector('[contenteditable="true"]');

// Use contextual targeting:
document.querySelector('.prompt-section [contenteditable="true"]');
// or
document.querySelector('[data-placeholder="Enter prompt"]');
## Selector Cheatsheet

javascript
// By attribute
document.querySelector('[contenteditable="true"]');

// By placeholder text
document.querySelector('[data-placeholder*="prompt"]');

// By class near editor
document.querySelector('.editor-wrapper [contenteditable="true"]');

// By aria label
document.querySelector('[aria-label="Prompt editor"]');
## Troubleshooting Checklist

- [ ] `editor.focus()` called before `execCommand`
- [ ] `execCommand` returns `true` (not `false`)
- [ ] `innerHTML` contains `<p>text</p>` after insertion
- [ ] Wait/delay added after insertion for React state propagation
- [ ] Editor is not inside shadow DOM (or shadow root is traversed)
- [ ] Correct editor selected (not a secondary hidden editor)
- [ ] Button enabled after interaction (not still disabled)

## Compatibility

- `document.execCommand('insertText')` works in all modern browsers
- Deprecated since 2015 but no deprecation removal scheduled
- Alternative: Clipboard API + `paste` event (more complex setup, same effect)