---
category: software-development
name: Frontend Design
slug: frontend
version: "1.1.0"
homepage: https://clawic.com/skills/frontend
description: Frontend development with React, Next.js, Tailwind CSS. Build landing pages, dashboards, forms, components. Responsive, accessible, performant UI.
metadata:
  clawdbot:
    emoji: "🖥️"
    requires:
      bins: []
    os: ["linux", "darwin", "win32"]
---

## When to Use

User needs a web interface built or significantly improved. This skill covers landing pages, dashboards, forms, component libraries, and any frontend requiring production polish.

## Required Reading

Read these files before starting any frontend work:

| File | Purpose |
|------|---------|
| `stack.md` | Tech stack, tooling, and project setup |
| `typography.md` | Font choices, scale, and rhythm |
| `colors.md` | Palette, CSS variables, theming |
| `mobile.md` | Responsive patterns and breakpoints |
| `animation.md` | Transitions, motion principles |
| `examples.md` | Reference implementations |

## Core Principles

### 1. Mobile-First Design

Always start with mobile, then enhance for larger screens.

- Every grid must collapse cleanly to single column
- Minimum touch target: **44×44px**
- Test on real devices — simulators miss critical issues
- Content hierarchy must work without horizontal scroll

### 2. Typography Creates Hierarchy

Generic fonts make generic interfaces.

- **Never use**: Inter, Roboto, Arial, system-ui defaults
- **Use dramatic scale jumps**: 14px → 32px is weak; 16px → 48px has impact
- **Body text minimum**: 16–18px (never below)
- **Line height**: 1.5–1.7 for body, 1.1–1.3 for headings
- See `typography.md` for recommended font pairings

### 3. Color with Confidence

Apply the 70-20-10 rule consistently:

| Usage | Percentage | Example |
|-------|------------|---------|
| Primary/Background | 70% | Deep navy #0a1628 |
| Secondary | 20% | Muted teal #3d7a8c |
| Accent | 10% | Bright coral #ff6b5b |

**Rules:**
- Commit to light OR dark theme — avoid muddy mid-tones
- Never use pure white (#fff) backgrounds — use off-white (#fafafa) with subtle depth
- Every interactive element needs a visible state (hover, focus, active)

### 4. Feedback Is Non-Negotiable

Users must never wonder "did that work?"

- **Tap feedback**: within 100ms (haptic, visual, or state change)
- **Optimistic UI**: update UI immediately, reconcile later
- **Operations >1s**: show loading indicator with context
- **Errors**: preserve all user input, never clear forms
- **Success**: confirm action completion explicitly

### 5. Accessibility Is a Baseline

Inaccessible interfaces are broken interfaces.

| Requirement | Minimum |
|-------------|---------|
| Text contrast | 4.5:1 |
| UI component contrast | 3:1 |
| Touch targets | 44×44px |
| Focus indicators | Visible on all interactive elements |
| Motion | Respects `prefers-reduced-motion` |

**Semantic HTML always:**
html
<!-- Wrong -->
<div onclick="submit()">Submit</div>
<div class="header">...</div>

<!-- Correct -->
<button type="submit">Submit</button>
<header>...</header>
Every interactive element must be keyboard-navigable.

### 6. Performance from Day One

Frontend performance directly impacts conversion and user experience.

| Metric | Target | Measurement |
|--------|--------|-------------|
| LCP (Largest Contentful Paint) | <2.5s | Lighthouse, WebPageTest |
| CLS (Cumulative Layout Shift) | <0.1 | Lighthouse |
| INP (Interaction to Next Paint) | <200ms | Chrome DevTools |

**Implementation checklist:**
- [ ] Lazy load all below-fold content
- [ ] Placeholder skeletons for async content
- [ ] Code-split heavy components
- [ ] Image `srcset` for responsive images
- [ ] Preload critical fonts
- [ ] No layout shift on font load (font-display: swap)

### 7. Design with Conviction

Timid design is forgettable design. Every page needs **one unforgettable element**.

Ideas:
- Dramatic typography scale on the hero
- Micro-interaction on a key button
- Unconventional layout (not the same 3-column grid)
- Motion that surprises (subtle, not distracting)
- A signature color or texture

The element should align with the product's personality — not arbitrary decoration.

## Common Mistakes

| Mistake | Result | Prevention |
|---------|--------|------------|
| Generic fonts | Indistinguishable from every other site | Choose 2–3 distinctive fonts intentionally |
| Pure white backgrounds | Flat, sterile feeling | Add subtle gradients, grain, or depth |
| Inconsistent spacing | Unpolished appearance | Use a spacing scale (4, 8, 16, 24, 32, 48, 64px) |
| Missing loading states | User uncertainty | Always design loading, empty, and error states |
| Ignoring focus states | Broken keyboard navigation | Style `:focus-visible` on every interactive element |
| Skipping mobile testing | Broken layouts in production | Test on actual phones early and often |

## Output Checklist

Before delivering frontend work:

- [ ] Mobile layout verified on real device
- [ ] All interactive elements have hover, focus, active states
- [ ] Loading, empty, and error states designed
- [ ] Keyboard navigation tested
- [ ] Lighthouse accessibility score ≥90
- [ ] LCP <2.5s, CLS <0.1
- [ ] Semantic HTML throughout
- [ ] One memorable design element per page