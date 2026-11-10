---
name: Frontend Design
slug: frontend
version: "1.0.3"
homepage: https://clawic.com/skills/frontend
description: Frontend development with React, Next.js, Tailwind CSS. Build landing pages, dashboards, forms, components. Responsive, accessible, performant UI.
metadata:
  emoji: "🖥️"
  os: [linux, darwin, win32]
---

## When to Use

User needs a web UI built. Agent handles landing pages, dashboards, forms, component libraries, and any frontend requiring production polish.

## Stack & Tooling

| Tool | Purpose |
|------|---------|
| React / Next.js | UI framework |
| Tailwind CSS | Styling |
| TypeScript | Type safety |
| Figma | Design reference |

See `stack.md` for complete tooling reference.

## Design Rules

### Mobile-First

Always start with mobile, enhance upward.

- Every grid must collapse to single column
- Touch targets minimum 44×44px
- Test on real devices, not just simulators
- Content priority becomes layout at breakpoints

### Typography

Typography carries 95% of your design.

| Rule | Why |
|------|-----|
| No generic fonts (Inter, Roboto, Arial) | Distinguish from every other site |
| Dramatic size jumps (2×+) | Creates hierarchy and drama |
| Body text 16–18px minimum | Readability |
| Line height 1.5–1.7 for body | Breathing room |

See `typography.md` for font recommendations.

### Color

| Rule | Implementation |
|------|----------------|
| 70-20-10 ratio | Primary 70%, secondary 20%, accent 10% |
| Commit to light OR dark | No muddy mid-grays |
| Never solid white backgrounds | Use subtle gradients, noise, or off-whites |
| Dark mode: use pure blacks (#000) | Not grays |

See `colors.md` for CSS variable patterns.

### Interaction Feedback

Users need confirmation on every action.

| Action | Response |
|--------|----------|
| Tap/click | Visual feedback within 100ms |
| Submit form | Optimistic update, spinner only if needed |
| Long operation (>1s) | Loading state with progress |
| Error | Preserve user input, show clear message |

### Accessibility

Non-negotiable. No exceptions.

| Requirement | Minimum |
|-------------|---------|
| Text contrast | 4.5:1 ratio |
| UI components | 3:1 ratio |
| Focus states | All interactive elements |
| Semantic HTML | `<nav>`, `<main>`, `<section>`, `<article>` |
| Keyboard nav | Everything accessible without mouse |

### Performance

Build it in from the start.

| Metric | Target |
|--------|--------|
| Largest Contentful Paint (LCP) | < 2.5s |
| Cumulative Layout Shift (CLS) | < 0.1 |
| First Input Delay (FID) | < 100ms |

Techniques:
- Lazy load below-fold content
- Image placeholders prevent layout shift
- Code split heavy components
- Preload critical fonts

### One Memorable Element

Every page needs one unforgettable design choice:

- Dramatic typography treatment
- Hero animation or micro-interaction
- Unusual but functional layout
- Distinctive color application

Timid designs are forgettable. Commit to an aesthetic.

## Reference Files

| Topic | File |
|-------|------|
| Stack & tooling | `stack.md` |
| Typography rules | `typography.md` |
| Color systems | `colors.md` |
| Mobile patterns | `mobile.md` |
| Animation | `animation.md` |
| Examples | `examples.md` |

## Common Mistakes

| Mistake | Result | Fix |
|---------|--------|-----|
| Generic fonts | Indistinguishable from every other site | Use distinctive, curated fonts |
| Solid white backgrounds | Flat, lifeless feel | Add gradients, grain, or depth |
| Tiny touch targets | Frustrated mobile users | Minimum 44×44px |
| Missing focus states | Broken keyboard navigation | Style `:focus-visible` on all inputs |
| No loading states | User confusion | Show feedback for any operation >300ms |