---
category: software-development
name: Frontend Design
slug: frontend
version: "1.0.3"
homepage: https://clawic.com/skills/frontend
description: Frontend development with React, Next.js, Tailwind CSS. Build landing pages, dashboards, forms, components. Responsive, accessible, performant UI.
changelog: "Enhanced specificity in core rules, expanded trap documentation, improved structure."
metadata:
  clawdbot:
    emoji: "🖥️"
    requires:
      bins: []
    os: ["linux", "darwin", "win32"]
---

## When to Use

User needs a web interface built, updated, or debugged. This skill covers:

- Landing pages and marketing sites
- Dashboards and data visualization
- Forms and input systems
- Component libraries
- Any frontend requiring production quality

## Quick Reference

| Topic | File |
|-------|------|
| Stack & tooling setup | `stack.md` |
| Typography rules | `typography.md` |
| Color systems | `colors.md` |
| Mobile patterns | `mobile.md` |
| Animation | `animation.md` |
| Code examples | `examples.md` |

## Core Rules

### 1. Mobile-First Always

Start with the smallest viewport and enhance upward. Never design desktop-first.

- Every multi-column grid must collapse to single column at 768px
- Touch targets minimum 44×44px (buttons, links, controls)
- Test on actual devices when possible, not just browser dev tools
- Account for notched devices and safe areas

### 2. Typography Creates Hierarchy

Bad typography kills design. Good typography makes it.

- **Never use:** Inter, Roboto, Arial, Open Sans, Lato
- **Use:** Distinctive, intentional typefaces (see `typography.md`)
- **Size jumps:** Create 2×+ contrast between levels, not 1.1× increments
- **Body text:** 16–18px minimum for readable content
- **Line height:** 1.5–1.7 for body, 1.1–1.3 for headings

### 3. Color with Purpose

Pick a palette and commit to it. Half-measures look indecisive.

| Role | Percentage | Purpose |
|------|------------|---------|
| Primary | 70% | Dominant background/walls |
| Secondary | 20% | Sections, cards, containers |
| Accent | 10% | CTAs, highlights, focus states |

- Choose **light mode OR dark mode** — avoid muddy mid-grays
- Never use solid `#ffffff` white backgrounds — add subtle gradients, noise, or depth
- See `colors.md` for CSS variable patterns and accessible combinations

### 4. Feedback on Every Interaction

Users must know their actions registered.

| Action | Response Time | Feedback |
|--------|---------------|----------|
| Tap/click | <100ms | Visual press state |
| Operation 1–3s | 100ms–3s | Loading spinner or skeleton |
| Operation >3s | >3s | Progress bar with ETA |
| Error | Any | Inline message, never alert() |

**Bonus:** Use optimistic UI updates — show the expected result immediately, then sync in background.

### 5. Accessibility Is Non-Negotiable

Accessible design is good design. These are minimum requirements:

| Requirement | Standard |
|-------------|----------|
| Color contrast | 4.5:1 for text, 3:1 for UI components |
| Focus states | Visible outline on all interactive elements |
| Semantic HTML | Use `<nav>`, `<main>`, `<section>`, `<article>` correctly |
| Keyboard nav | Every action possible without a mouse |
| ARIA labels | Only when semantic HTML isn't sufficient |

Run Lighthouse accessibility audits. Score must be 90+.

### 6. Performance from Day One

Frontend performance directly impacts conversion and UX.

| Metric | Target | What to Fix |
|--------|--------|-------------|
| LCP (Largest Contentful Paint) | <2.5s | Optimize hero images, preload fonts |
| CLS (Cumulative Layout Shift) | <0.1 | Reserve space for images, use aspect-ratio |
| INP (Interaction to Next Paint) | <200ms | Debounce handlers, lazy load below-fold |

- Lazy load images and components outside viewport
- Use skeleton loaders during data fetching
- Code-split heavy components (charts, modals, editors)
- Preload critical fonts, lazy-load icon fonts

### 7. One Memorable Element Per Page

Every page needs a signature. Timid designs blend into the noise.

Ideas:
- Dramatic typography treatment (oversized, rotated, layered)
- Hero animation or scroll-triggered motion
- Unconventional layout or asymmetric grid
- Distinctive illustration or photography style
- Micro-interaction that surprises and delights

Pick one element and make it unforgettable. Everything else serves it.

## Frontend Traps

| Trap | Consequence | Prevention |
|------|-------------|------------|
| Generic fonts (Inter, Roboto) | Indistinguishable from every other site | Use distinctive Google Fonts or custom typefaces |
| Solid white backgrounds | Flat, generic, lifeless | Add subtle gradients, overlays, or texture |
| No size contrast in typography | Visual hierarchy collapses | Use 2×+ jumps between heading levels |
| Loading without feedback | Users think the app is broken | Always show loading state, even for 500ms |
| Ignoring dark mode | Poor experience for half your users | Build with CSS custom properties from day one |
| Fixed-width layouts | Breaks on tablets and small laptops | Use responsive units, fluid grids |
| Skipping focus states | Keyboard users cannot navigate | Style `:focus-visible` on every interactive element |
| No error boundaries | One error crashes the entire app | Wrap feature areas with error boundaries |
| Importing entire libraries | Bloated bundle, slow load | Tree-shake or use modular imports |

## Stack Defaults

When not specified, use:

- **Framework:** Next.js (App Router)
- **Styling:** Tailwind CSS with CSS custom properties for theming
- **Components:** Radix UI primitives for accessibility
- **Forms:** React Hook Form with Zod validation
- **State:** Zustand for global state, React Query for server state
- **Animation:** Framer Motion for component animations

---

For specific guidance, see the linked reference files.