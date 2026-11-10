---
name: browser-contenteditable-workaround
description: Bypass React/Vue/Tiptap contenteditable editors that reset normal Playwright input — use document.execCommand('insertText', ...)
category: browser-use
---

# Workaround: Text Input on React/Vue Contenteditable Editors

## The Problem

Modern contenteditable editors built with React, Vue, Tiptap, or ProseMirror (e.g., Notion-style editors, Pixelbin) reset or ignore text inserted via standard methods:

- `element.innerHTML = text`
- `document.execCommand('insertHTML', ...)`
- `InputEvent` or `KeyboardEvent` dispatch
- `browser_type` tool

The editor appears empty, and `is-empty` / `is-editor-empty` placeholder classes persist even after "inserting" text.

## The Solution

javascript
const editor = document.querySelector('[contenteditable="true"]');
editor.focus();
document.execCommand('insertText', false, 'your prompt text here');
`execCommand('insertText', ...)` bypasses React's synthetic event system and works where everything else fails.

## Full Workflow Example

javascript
// 1. Navigate to the app
browser_navigate('https://console.pixelbin.io/organization/<org_id>/studio/ai-image-generator');

// 2. Focus the editor (CRITICAL — execCommand fails without focus)
const editor = document.querySelector('[contenteditable="true"]');
editor.focus();

// 3. Insert text via execCommand
document.execCommand('insertText', false, 'a majestic fox in snowy forest, cinematic photography');

// 4. Verify text landed — check for <p>text</p> nodes, NOT placeholder classes
editor.innerHTML;
// Expected: '<p>a majestic fox in snowy forest, cinematic photography</p>'

// 5. Click Generate button (check snapshot for enabled ref)
browser_click('ref for Generate button');
## Why This Works

React 16+ uses synthetic events and bypasses native DOM events for `onChange`/`onInput`. The `execCommand('insertText')` command predates React's event system — it writes directly to the DOM selection/clipboard, and React cannot intercept it.

## Pitfalls and Gotchas

| Issue | Fix |
|-------|-----|
| `execCommand` returns `false` | Verify the editor is focused (`editor.focus()`) |
| Editor inside shadow DOM | Use `document.querySelector('your-element').shadowRoot.querySelector('[contenteditable]')` |
| Placeholder classes still visible | Check for `<p>text</p>` nodes instead — classes may lag behind DOM state |
| Generate button stays disabled | Click elsewhere first or add a small wait to let React update its state |

## Selector Tips

javascript
// Common contenteditable selectors
document.querySelector('[contenteditable="true"]');
document.querySelector('[data-slate-editor="true"]');       // Slate editors
document.querySelector('.ProseMirror');                     // ProseMirror/Tiptap
document.querySelector('[role="textbox"][aria-multiline]'); // Accessibility-based
## Summary

When standard browser input fails on contenteditable editors:
1. Focus the editor element first
2. Use `document.execCommand('insertText', false, text)` instead of direct DOM manipulation
3. Verify insertion by checking actual `<p>` nodes, not placeholder class state