---
category: software-development
name: Frontend Design
slug: frontend
version: "1.0.3"
homepage: https://clawic.com/skills/frontend
description: Frontend development with React, Next.js, Tailwind CSS. Build landing pages, dashboards, forms, components. Responsive, accessible, performant UI.
metadata:
  clawdbot:
    emoji: "🖥️"
    requires:
      bins: []
    os: [linux, darwin, win32]
---

## When to Use

User needs web UI built, modified, or debugged. Handle landing pages, dashboards, forms, component libraries, design systems, and any frontend requiring production polish.

## Stack Reference

| Topic | File |
|-------|------|
| Tech stack & tooling | `stack.md` |
| Typography rules | `typography.md` |
| Color systems | `colors.md` |
| Mobile patterns | `mobile.md` |
| Animation & motion | `animation.md` |
| Component examples | `examples.md` |

---

## Core Rules

### 1. Mobile-First Always

Start with mobile layout, enhance upward. Never assume desktop.

- Every multi-column grid must collapse to single column at 768px
- Touch targets minimum 44×44px (buttons, links, form controls)
- Tap feedback on all interactive elements
- Test on real devices when possible — simulators miss scroll bounce, font rendering, and performance issues

### 2. Typography Creates Hierarchy

Don't use safe defaults. Typography is 95% of visual design.

- Avoid generic fonts: Inter, Roboto, Arial, Open Sans, Lato
- Use dramatic size jumps: 14px → 32px → 64px (not 14, 16, 18, 20)
- Body text minimum 16px, preferably 18px for long-form content
- Line height 1.5–1.7 for body, 1.1–1.3 for headings
- Letter spacing: tight on headlines (-0.02em), normal on body
- See `typography.md` for font pairings and scale systems

### 3. Color with Purpose

Color communicates meaning. Random palettes create noise.

- Follow 70-20-10 rule: 70% dominant color, 20% secondary, 10% accent
- Choose light OR dark theme — avoid muddy mid-grays
- Never use pure white (#FFFFFF) backgrounds — use #F8F9FA or add subtle gradients
- Create depth with shadows, borders, and texture, not just color
- See `colors.md` for CSS variable patterns and accessible combinations

### 4. Feedback on Every Interaction

Users must never wonder "did that work?"

- Visual feedback within 100ms of any tap/click (scale, opacity, color change)
- Optimistic UI updates for instant perceived performance
- Skeleton loaders for content loading >500ms
- Full loading states for operations >1s
- Never lose user input on errors — preserve forms, show inline validation
- Toast notifications for actions outside current view

### 5. Accessibility Is Not Optional

Accessible design is good design. It benefits everyone.

- Color contrast ratio 4.5:1 minimum for text, 3:1 for UI components
- Visible focus states on all interactive elements (`:focus-visible`)
- Semantic HTML: `<nav>`, `<main>`, `<section>`, `<article>`, `<button>`
- Every `<button>` and `<a>` must have descriptive text (not "click here")
- Skip-to-content link for keyboard users
- ARIA labels only when semantic HTML isn't sufficient
- Test with keyboard-only navigation before shipping

### 6. Performance From the Start

Slow UIs feel broken. Optimize on the way, not after.

- Lazy load images and components below the fold
- Always include image dimensions or aspect-ratio to prevent layout shift
- Code-split heavy components (modals, charts, rich text editors)
- Target metrics:
  - LCP < 2.5s
  - CLS < 0.1
  - INP < 200ms
- Use web fonts wisely: `font-display: swap`, preload critical fonts

### 7. One Signature Element

Every page needs a memorable moment. Timid designs are forgettable.

- One bold typography treatment, hero animation, or unusual layout choice
- This doesn't mean clutter — restraint elsewhere to make the signature element shine
- Examples: dramatic headline scale, subtle parallax, unique illustration style, signature color usage

---

## Common Traps

| Trap | Consequence | Fix |
|------|-------------|-----|
| Generic fonts (Inter, Roboto) | Indistinguishable from every other site | Choose 1 display + 1 body font from Google Fonts or commercial foundry |
| Solid white backgrounds | Flat, institutional feel | Use off-whites, subtle gradients, or texture layers |
| Uniform spacing | Boring, no visual hierarchy | Vary padding/margin dramatically: 8px vs 48px vs 96px |
| Too many font sizes | Visual noise | Limit to 3–4 sizes: small, body, h2, h1 |
| Decorative-only elements | Distraction without function | Remove or make functional (tooltip, animation) |
| Form without validation states | Confusing errors | Show error/success states inline, never alert() dialogs |
| Ignoring focus styles | Broken keyboard UX | Style `:focus-visible` with visible outline or background change |