---
name: browser-contenteditable-workaround
description: Bypass React/Vue/Tiptap contenteditable editors that reset normal Playwright input — use document.execCommand('insertText', ...)
category: browser-use
---

# Workaround: Text Input on React/Vue Contenteditable Editors

## The Problem

Modern contenteditable editors (React, Vue, Tiptap, ProseMirror, Slate) use synthetic event systems that intercept and ignore most text insertion methods:

| Method | Works? | Reason |
|--------|--------|--------|
| `element.innerHTML = text` | ❌ | Editor resets/rejects changes |
| `document.execCommand('insertHTML')` | ❌ | Bypassed by synthetic events |
| `InputEvent`/`KeyboardEvent` dispatch | ❌ | Detected as synthetic |
| `browser_type` tool default behavior | ❌ | Triggered as programmatic input |
| `document.execCommand('insertText')` | ✅ | Legacy command bypasses React |

The element appears empty, and placeholder classes (`is-empty`, `is-editor-empty`) persist even after attempted text insertion.

## The Solution

javascript
// 1. Get the contenteditable element
const editor = document.querySelector('[contenteditable="true"]');

// 2. Focus MUST precede the command
editor.focus();

// 3. Insert text via deprecated-but-functional command
document.execCommand('insertText', false, 'your text here');
## Why This Works

React 16+ implements a synthetic event system that intercepts native DOM events. `execCommand('insertText')` is a legacy browser command predating React's event architecture — it writes directly to the DOM selection/clipboard layer where React cannot intercept it.

## Complete Workflow Example

### Scenario: Pixelbin AI Image Generator

javascript
// Step 1: Navigate to the app
browser_navigate('https://console.pixelbin.io/organization/<org_id>/studio/ai-image-generator');

// Step 2: Locate the contenteditable editor
const editor = document.querySelector('[contenteditable="true"]');

// Step 3: Focus the editor (critical — no focus means no insert)
editor.focus();

// Step 4: Insert text
document.execCommand('insertText', false, 'a majestic fox in snowy forest, cinematic photography');

// Step 5: Verify text landed
// Look for actual <p> nodes, NOT placeholder classes
editor.innerHTML;
// Expected: '<p>a majestic fox in snowy forest, cinematic photography</p>'

// Step 6: Click the Generate button
browser_click('ref for Generate button');
## Pitfalls and Troubleshooting

### Pitfall 1: Placeholder Classes Persist
The `is-empty is-editor-empty` classes may remain even after text successfully inserts. Check for actual `<p>` content instead:

javascript
// ❌ Don't check this
editor.classList.contains('is-empty'); // Still true

// ✅ Do check this
editor.querySelector('p') !== null; // True when text present
### Pitfall 2: Editor Must Be Focused First
Calling `execCommand` without focus returns `false` and does nothing:

javascript
// ❌ Wrong order
document.execCommand('insertText', false, 'text');
editor.focus();

// ✅ Correct order
editor.focus();
document.execCommand('insertText', false, 'text');
### Pitfall 3: Generate Button Stays Disabled
After text lands, the button may remain disabled while React updates state:

javascript
// Option A: Wait briefly
await new Promise(r => setTimeout(r, 500));

// Option B: Click elsewhere to trigger state update
editor.blur();
await new Promise(r => setTimeout(r, 100));
browser_click('ref for Generate button');
### Pitfall 4: Shadow DOM Containment
If `execCommand` returns `false`, the editor may be inside a shadow DOM:

javascript
// Verify focusability
editor === document.activeElement; // Should be true

// Check for shadow DOM
editor.shadowRoot !== null; // If true, target shadowRoot instead

// Retry targeting shadow root
const shadowEditor = document.querySelector('your-web-component').shadowRoot.querySelector('[contenteditable="true"]');
shadowEditor.focus();
document.execCommand('insertText', false, 'text');
## Edge Cases

| Scenario | Solution |
|----------|----------|
| Multiple contenteditable elements | Target the specific one with additional selectors: `document.querySelector('[contenteditable="true"][data-placeholder="prompt"]')` |
| Nested editors (comments, replies) | Click the specific reply field first, then follow the workflow |
| Tiptap/ProseMirror with extensions | May require additional state triggers after insert |
| Mobile contenteditable | Test behavior — some mobile editors intercept at different layers |

## Summary Checklist

- [ ] Query for `[contenteditable="true"]` element
- [ ] Call `.focus()` before `execCommand`
- [ ] Use `document.execCommand('insertText', false, 'text')`
- [ ] Verify with `innerHTML` containing `<p>` nodes, not just class checks
- [ ] Handle disabled button state with blur/wait if needed
- [ ] Check for shadow DOM if command returns `false`