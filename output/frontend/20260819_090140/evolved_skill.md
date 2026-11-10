---
category: software-development
description: '---'
name: frontend
---

---
name: Frontend Design
slug: frontend
version: "1.0.3"
homepage: https://clawic.com/skills/frontend
description: Frontend development with React, Next.js, Tailwind CSS. Build landing pages, dashboards, forms, components. Responsive, accessible, performant UI.
changelog: "Renamed to better reflect design-focused capabilities and guidance. Expanded traps section and added concrete examples."
metadata: {"clawdbot":{"emoji":"🖥️","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## When to Use

User needs a web interface built or improved. Agent handles:

- Landing pages and marketing sites
- Dashboards and admin panels
- Forms and data entry interfaces
- Component libraries and design systems
- Any frontend requiring production polish

## Quick Reference

| Topic | File |
|-------|------|
| Stack & tooling | `stack.md` |
| Typography rules | `typography.md` |
| Color systems | `colors.md` |
| Mobile patterns | `mobile.md` |
| Animation & motion | `animation.md` |
| Code examples | `examples.md` |

## Core Principles

### 1. Mobile-First Always

Design for mobile first, then enhance upward for larger screens.

- Every grid must collapse cleanly to single column
- Touch targets minimum **44×44px** (Apple) or **48×48dp** (Material)
- Test on real devices — simulators miss hardware-specific issues
- Content hierarchy must work without horizontal scrolling

### 2. Typography Creates Impact

Avoid generic, overused fonts that make sites look identical.

**Rules:**
- Never use Inter, Roboto, Arial, Open Sans, or Lato
- Use dramatic size jumps (2×+ scale), not timid 1.1× increments
- Body text minimum **16px**, preferably **18px** for long-form
- Line height **1.5–1.7** for body, tighter for headings
- See `typography.md` for font pairings and specific recommendations

### 3. Color with Purpose

Choose colors deliberately — every shade must earn its place.

**70-20-10 Rule:**
- **70%** — Dominant color (usually neutral backgrounds)
- **20%** — Secondary color (sections, cards)
- **10%** — Accent color (CTAs, highlights, alerts)

**Additional rules:**
- Commit to light OR dark theme — avoid muddy mid-grays
- Never use pure white (`#FFFFFF`) backgrounds — add subtle gradient or depth
- Build a cohesive palette using CSS custom properties
- See `colors.md` for CSS variables and palette patterns

### 4. Feedback on Every Interaction

Users must never wonder "did that work?"

| Delay | Response |
|-------|----------|
| <100ms | Instant visual acknowledgment (state change, color shift) |
| 100ms–1s | Optimistic UI update |
| >1s | Visible loading state with spinner or skeleton |

**Critical:** Preserve all user input on errors — never clear form fields.

### 5. Accessibility is Non-Negotiable

Build for everyone from the start — retrofitting is expensive.

- **Color contrast:** 4.5:1 minimum for text, 3:1 for UI components
- **Focus states:** Visible outline on all interactive elements (`:focus-visible`)
- **Semantic HTML:** Use `<nav>`, `<main>`, `<section>`, `<article>` appropriately
- **Keyboard navigation:** Every action accessible via Tab, Enter, Escape, Arrow keys
- **ARIA labels:** Only when semantic HTML isn't sufficient
- **Motion:** Respect `prefers-reduced-motion`

### 6. Performance from Day One

Don't ship slow sites and hope to fix them later.

- Lazy load all below-fold content (images, components, routes)
- Image placeholders (skeleton or blur-up) prevent layout shift
- Code split heavy components (charts, editors, modals)
- **Target metrics:**
  - LCP < 2.5s
  - CLS < 0.1
  - INP < 200ms

### 7. One Memorable Element

Every page needs a distinctive design choice — without it, you blend into noise.

Ideas:
- Dramatic typography treatment (oversized, rotated, stacked)
- Hero section with subtle animation
- Unusual layout rhythm (not a standard 12-column grid)
- Signature interaction pattern
- Custom cursor or micro-interaction

Timid designs fail. Commit to an aesthetic direction.

## Common Traps

| Trap | Consequence | Solution |
|------|-------------|----------|
| Generic fonts | Indistinguishable from every other site | Use distinctive, intentional typography |
| Flat white backgrounds | Flat, lifeless, cheap-feeling | Add gradients, grain texture, or subtle depth |
| Tiny touch targets | Frustrated mobile users, failed taps | Minimum 44×44px for all interactive elements |
| No loading states | Users double-click, assume it's broken | Always show feedback for operations >100ms |
| Ignoring contrast | Text unreadable, legal liability | Use tools to verify 4.5:1 ratio minimum |
| Generic stock photos | Unprofessional, forgettable | Use real product shots, illustrations, or none |
| Skeleton screens missing | Layout shifts, jarring experience | Show placeholder before content loads |
| Accessibility as afterthought | Excludes users, expensive to fix later | Build it in from the start |

## Output Checklist

Before marking frontend work complete:

- [ ] Mobile layout tested on real device
- [ ] Touch targets ≥44px
- [ ] All fonts loaded and rendering
- [ ] Color contrast verified
- [ ] Focus states visible on all interactive elements
- [ ] Keyboard navigation works end-to-end
- [ ] Loading states implemented
- [ ] Images have `alt` text and lazy loading
- [ ] No console errors
- [ ] Lighthouse performance ≥90