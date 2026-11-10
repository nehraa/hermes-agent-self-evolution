---
name: browser-contenteditable-workaround
description: Bypass React/Vue/Tiptap contenteditable editors that reset normal Playwright input — use document.execCommand('insertText', ...)
category: browser-use
---

# Workaround: Text Input on React/Vue Contenteditable Editors

## The Problem
React/Vue/Tiptap/ProseMirror contenteditable editors in modern web apps (e.g., Pixelbin, Notion-style editors) reset or ignore text inserted via:
- `element.innerHTML = text`
- `document.execCommand('insertHTML', ...)`
- `InputEvent` / `KeyboardEvent` dispatch
- `browser_type` tool

The element shows no visible text, and `is-empty` / `is-editor-empty` classes persist even after "inserting" text.

## The Fix
```javascript
const editor = document.querySelector('[contenteditable="true"]');
editor.focus();
document.execCommand('insertText', false, 'your prompt text here');
```

`execCommand('insertText', ...)` bypasses React's synthetic event system and works where everything else fails.

## Full Workflow Example (Pixelbin Image Generator)
```javascript
// 1. Navigate to the app
browser_navigate('https://console.pixelbin.io/organization/<org_id>/studio/ai-image-generator');

// 2. Focus the editor (critical!)
const editor = document.querySelector('[contenteditable="true"]');
editor.focus();

// 3. Insert text via execCommand
document.execCommand('insertText', false, 'a majestic fox in snowy forest, cinematic photography');

// 4. Verify it landed — look for <p>text</p>, NOT the placeholder classes
editor.innerHTML;
// Returns: '<p>a majestic fox in snowy forest, cinematic photography</p>'

// 5. Click Generate button (check snapshot for enabled ref)
browser_click('ref for Generate button');
```

## Why This Works
React 16+ uses synthetic events and bypasses native DOM events for `onChange`/`onInput`. `execCommand('insertText')` is a legacy browser command (deprecated but still functional) that predates React's event system — it writes directly to the DOM selection/clipboard and React can't intercept it.

## Pitfalls
- `editor.innerHTML` still shows placeholder `is-empty is-editor-empty` classes even after text lands — check for the actual `<p>text</p>` node
- The editor MUST be focused (`editor.focus()`) before calling `execCommand`
- After text lands, the "Generate" button may still be disabled — wait or click elsewhere first to trigger React state update
- If `execCommand` returns `false`, the editor may not be focused or may be inside a shadow DOM — verify: `document.activeElement === editor`
- The contenteditable may be a `<div>` with a nested `<p>` placeholder — use the outermost contenteditable element

## Known Apps This Works On
- Pixelbin.io image generator (Tiptap/ProseMirror editor)

## Known Apps This Does NOT Work On
- Google Docs (uses canvas rendering, not DOM)
- Figma (shadow DOM隔离)
- Some React apps that override `execCommand`
