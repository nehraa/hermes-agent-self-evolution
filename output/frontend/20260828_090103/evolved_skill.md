---
category: software-development
description: '---'
name: frontend
---

---
name: Frontend Design
slug: frontend
version: "1.1.0"
homepage: https://clawic.com/skills/frontend
description: Frontend development with React, Next.js, Tailwind CSS. Build landing pages, dashboards, forms, components. Responsive, accessible, performant UI.
changelog: "Enhanced with specific implementation guidance, expanded rules with examples, and complete traps section."
metadata: {"clawdbot":{"emoji":"🖥️","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## When to Use This Skill

Use this skill when you need to build or improve web interfaces. It covers:

- **Landing pages** — Hero sections, feature showcases, CTAs, pricing tables
- **Dashboards** — Data visualization, admin panels, analytics views
- **Forms** — Input validation, multi-step flows, accessible controls
- **Component libraries** — Buttons, modals, dropdowns, cards, navigation
- **Design systems** — CSS variables, spacing scales, utility patterns

The agent will produce production-ready frontend code with attention to design quality, accessibility, and performance.

## Quick Reference

| Topic | File |
|-------|------|
| Tech stack & setup | `stack.md` |
| Typography guidelines | `typography.md` |
| Color palette system | `colors.md` |
| Mobile-first patterns | `mobile.md` |
| Motion & animation | `animation.md` |
| Code examples | `examples.md` |

## Core Principles

### 1. Mobile-First Layout

Always start with mobile, then progressively enhance for larger screens.

Requirements:
- Single column layout for mobile (320px+)
- Breakpoints at 768px (tablet), 1024px (desktop), 1280px (large)
- Grid collapses gracefully — never horizontal scroll on mobile
- Touch targets: minimum 44×44px (WCAG AA)
- Test on actual devices when possible
**Implementation:** Use Tailwind's responsive prefixes (`sm:`, `md:`, `lg:`) or CSS media queries. Define mobile styles as base, then add enhancements.

### 2. Typography Creates Hierarchy

Poor typography is the #1 sign of amateur UI. Follow these rules:

| Rule | Value | Why |
|------|-------|-----|
| Body font size | 16–18px minimum | Readability on all devices |
| Heading scale ratio | 1.333 (perfect fourth) or higher | Creates clear hierarchy |
| Line height (body) | 1.5–1.6 | Comfortable reading |
| Line height (headings) | 1.2–1.3 | Tight, impactful |
| Max line length | 65–75 characters | Prevents eye fatigue |

**Avoid:** Inter, Roboto, Arial, Open Sans (overused, generic feel). See `typography.md` for recommended font stacks.

### 3. Color System (70-20-10)

Apply this distribution for visual balance:

| Role | Percentage | Purpose |
|------|------------|---------|
| Primary (70%) | Background, large areas | Sets the tone |
| Secondary (20%) | Cards, sections, containers | Creates structure |
| Accent (10%) | CTAs, highlights, links | Draws attention |

**Commit fully to light OR dark mode.** Avoid mid-grays that work for neither. Never use pure white (#FFFFFF) for backgrounds — use off-whites or subtle gradients.

css
/* Light mode background */
background: linear-gradient(180deg, #FAFAFA 0%, #F0F0F0 100%);

/* Dark mode background */
background: linear-gradient(180deg, #0F0F0F 0%, #1A1A1A 100%);
See `colors.md` for CSS variable patterns and complete palette examples.

### 4. Interaction Feedback

Users need confirmation on every action within 100ms.

| User Action | Response Time | Feedback Type |
|-------------|---------------|---------------|
| Tap/click | Instant (<100ms) | Visual press state |
| Form submit | <1s | Button loading state |
| Data load | >1s | Skeleton or spinner |
| Error | Immediate | Clear message, preserve input |

**Optimistic updates:** For operations like likes, toggles, or form submissions, update UI immediately before server confirmation. Roll back gracefully on failure.

jsx
// Example: Optimistic toggle
const [enabled, setEnabled] = useState(false);
const toggle = async () => {
  setEnabled(!enabled); // Optimistic
  try {
    await api.toggle();
  } catch {
    setEnabled(enabled); // Rollback on error
  }
};
### 5. Accessibility (A11Y)

These are minimum requirements, not suggestions:

| Requirement | Standard | Implementation |
|-------------|----------|----------------|
| Color contrast | 4.5:1 (text), 3:1 (UI) | Use browser dev tools or axe |
| Focus indicators | Visible on all interactive elements | `outline: 2px solid`, `focus-visible` |
| Semantic HTML | nav, main, header, section, article, button | Never `<div>` for buttons |
| Keyboard navigation | Full functionality without mouse | Tab order, Enter/Space activation |
| ARIA labels | When semantics insufficient | `aria-label`, `aria-describedby` |

**Never remove outline without replacement.** Screen reader users and keyboard-only users depend on focus indicators.

### 6. Performance Budget

Target these metrics for every page:

| Metric | Target | Measurement |
|--------|--------|-------------|
| LCP (Largest Contentful Paint) | <2.5s | Lighthouse, WebPageTest |
| CLS (Cumulative Layout Shift) | <0.1 | Lighthouse |
| FID (First Input Delay) | <100ms | Chrome DevTools |
| TTI (Time to Interactive) | <3.8s | Lighthouse |

**Techniques:**

jsx
// Lazy load below-fold images
<img src="hero.jpg" loading="eager" alt="..." />
<img src="content.jpg" loading="lazy" alt="..." />

// Code split heavy components
const HeavyChart = dynamic(() => import('./Chart'), { 
  loading: () => <Skeleton /> 
});

// Prevent layout shift with aspect-ratio
<div style={{ aspectRatio: '16/9' }}>
  <img src="..." />
</div>
### 7. Design Differentiation

Every page needs one memorable element. Timid designs blend into the background.

**Options for memorable design:**

- **Typography statement** — Oversized display text, mixed weights, creative kerning
- **Hero animation** — Subtle parallax, floating elements, gradient motion
- **Unusual layout** — Asymmetric grids, overlapping elements, broken grids
- **Signature interaction** — Unique hover state, distinctive scroll behavior

**Commit or cut.** If you're hesitant about a design choice, either fully commit or remove it entirely.

## Common Traps

| Trap | Symptom | Solution |
|------|---------|----------|
| Generic fonts | Looks like every other website | Use distinctive typefaces (see `typography.md`) |
| Solid white backgrounds | Flat, lifeless, cheap-looking | Add gradients, grain texture, or subtle depth |
| Tiny touch targets | Frustrated mobile users | Minimum 44×44px for all interactive elements |
| No loading states | Appears broken during data fetch | Show skeletons or spinners immediately |
| Ignoring focus styles | Keyboard users can't navigate | Style `:focus-visible` on all interactive elements |
| Unbalanced whitespace | Cramped or floating layouts | Use consistent spacing scale (4px base) |
| No error handling | Silent failures confuse users | Toast notifications, inline errors, preserve input |
| Skeleton after content | Layout shifts cause CLS | Define skeleton dimensions, use aspect-ratio |

## File Outputs

When implementing frontend features, generate:

1. **Component files** — React/Vue components with clear props and states
2. **CSS/Tailwind classes** — Consistent utility patterns
3. **Documentation** — Usage examples and prop tables
4. **Tests** — Basic render and interaction tests

All code should be production-ready: no TODOs, no placeholder content, no hardcoded values that should be dynamic.