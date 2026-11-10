---
name: design-taste-frontend
description: Anti-slop frontend skill for landing pages, portfolios, and redesigns. The agent reads the brief, infers the right design direction, and ships interfaces that do not look templated. Real design systems when applicable, audit-first on redesigns, strict pre-flight check.
---

# Anti-Slop Frontend Skill

> **Scope:** Landing pages, portfolios, and redesigns.
> **Out of scope:** Dashboards, data tables, multi-step product UI.
> **Contextual rule:** Every section below fires only when relevant. Read the brief first, then apply what fits.

---

## 0. Brief Inference: Read the Room Before Anything Else

LLM design output fails because models jump to default aesthetics instead of understanding context. Infer what the user actually wants before touching a single element.

### 0.A Read These Signals First

Process in order — each signal narrows the design space:

1. **Page kind** — Landing (SaaS / consumer / agency / event), portfolio (dev / designer / studio), redesign, editorial / blog, marketing campaign.
2. **Vibe words** — "minimalist", "calm", "Linear-style", "Awwwards", "brutalist", "premium consumer", "Apple-y", "playful", "serious B2B", "agency-y", "glassy", "dark tech".
3. **Reference signals** — URLs linked, screenshots shared, products or brands named, competitors mentioned.
4. **Audience** — B2B procurement panel vs. design-conscious consumer vs. recruiter scanning portfolios. The audience selects the aesthetic, not your preferences.
5. **Existing brand assets** — Logo, colors, typography, photography. For redesigns, these are mandatory starting material, not optional input (see Section 11).
6. **Quiet constraints** — Accessibility-first audiences, public-sector, regulated industries, trust-first commerce, children's products. These **override** aesthetic preference.

### 0.B State a One-Line "Design Read"

Before generating any code, output a single line:

> **"Reading this as:** `<page kind>` **for** `<audience>`, **with a** `<vibe>` **language, leaning toward** `<design system or aesthetic>`**."**

**Examples:**

- *"Reading this as: B2B SaaS landing for technical buyers, with a Linear-style minimalist language, leaning toward Tailwind + Geist + restrained motion."*
- *"Reading this as: solo designer portfolio for hiring managers, with an editorial/kinetic-type language, leaning toward native CSS + scroll-driven animation + custom typography."*
- *"Reading this as: redesign of a public-sector service site, with a trust-first accessible language, leaning toward WCAG AA compliance + clear hierarchy + utilitarian structure."*

If the user provides sparse context, state your assumptions explicitly: *"Reading this as: [inferred] with [inferred] language — please correct if off."*

---

## 1. Aesthetic Selection

Do not default to a style. Choose based on the signals above.

| Page Kind | Audience | Default Aesthetic |
|-----------|----------|-------------------|
| SaaS landing | Technical buyers | Precision, whitespace, subtle data viz, Linear/Vercel influence |
| SaaS landing | Non-technical buyers | Trust signals, clear hierarchy, social proof, less abstraction |
| Consumer landing | Design-aware | Editorial, large type, bold imagery, considered whitespace |
| Portfolio | Recruiters / clients | Show, don't tell — let work speak, minimal UI chrome |
| Portfolio | Agency peers | Distinctive point of view, craft details, motion as personality |
| Redesign | Any | Audit existing first — preserve what works, improve what doesn't (see Section 11) |
| Event / campaign | General | Bold, loud, action-oriented — limited-time energy |

**Aesthetic families to draw from:**

- **Precision / Linear** — Monospace accents, clean grids, muted palette, micro-interactions
- **Editorial / Magazine** — Serif headlines, asymmetric layouts, rich photography
- **Brutalist** — Raw structure, visible grid, high contrast, intentional "ugly"
- **Warm / Human** — Rounded corners, friendly palette, illustrated accents, approachable type
- **Dark Tech** — Dark backgrounds, neon/glow accents, terminal-inspired elements
- **Glass / Aeromorphic** — Backdrop blur, transparency layers, depth through shadow

---

## 2. Typography System

Typography carries 80% of the visual impression. Treat it as a system, not a collection of sizes.

### 2.A Font Selection Guidelines

**For most projects:**

- **Heading font:** One distinctive choice — Google Fonts or a paid typeface that matches the vibe
- **Body font:** Highly readable, pairs with heading — usually a geometric or humanist sans
- **Mono font (if needed):** JetBrains Mono, Fira Code, or Source Code Pro

**Pairing resources:**

- Fontpair.co — tested pairings
- Type-scale generators — establish a modular scale (1.25 or 1.333 ratio)

### 2.B Type Scale

Define a scale with purpose:

--text-xs: 0.75rem    /* 12px - captions, labels */
--text-sm: 0.875rem   /* 14px - secondary text, metadata */
--text-base: 1rem     /* 16px - body */
--text-lg: 1.125rem  /* 18px - lead paragraphs */
--text-xl: 1.25rem   /* 20px - small headings */
--text-2xl: 1.5rem   /* 24px - section headings */
--text-3xl: 1.875rem /* 30px - page headings */
--text-4xl: 2.25rem  /* 36px - hero subheadings */
--text-5xl: 3rem     /* 48px - hero headings */
--text-6xl: 3.75rem  /* 60px - display (desktop only) */
### 2.C Spacing and Rhythm

- **Line height:** 1.5–1.7 for body, 1.1–1.3 for large headings
- **Paragraph spacing:** 1.5× the line height
- **Section rhythm:** Alternate density — dense content sections followed by breathing room
- **Responsive sizing:** Scale down 10–15% on mobile; avoid fluid type at extreme scales

---

## 3. Color System

Build a palette with purpose. Avoid the "random gradient hero" default.

### 3.A Palette Structure

--color-background: #FAFAFA    /* Light surfaces */
--color-background-dark: #0A0A0A  /* Dark surfaces */
--color-surface: #FFFFFF       /* Cards, elevated elements */
--color-surface-muted: #F4F4F5 /* Subtle backgrounds */
--color-border: #E4E4E7        /* Dividers, outlines */
--color-border-strong: #D4D4D8 /* Emphasized borders */

--color-text-primary: #18181B   /* Main text */
--color-text-secondary: #71717A /* Supporting text */
--color-text-tertiary: #A1A1AA  /* Muted text */

--color-accent: #2563EB         /* Primary actions */
--color-accent-hover: #1D4ED8  /* Hover state */
--color-accent-muted: #DBEAFE   /* Accent backgrounds */

--color-success: #16A34A
--color-warning: #EA580C
--color-error: #DC2626
### 3.B Usage Rules

- **One primary accent color** — used for CTAs, links, key highlights
- **Neutral palette does the heavy lifting** — most UI is grays with strategic color
- **Dark mode:** Invert thoughtfully — not every light palette maps directly to dark
- **Gradient rule:** If using gradients, limit to 2–3 colors, keep them subtle, or go bold as a deliberate choice
- **Brand colors:** Extract from logo/brand guide when provided; otherwise, build from the vibe

---

## 4. Layout and Spacing

Good layout is invisible. The user feels it without noticing it.

### 4.A Grid System

- **Desktop:** 12-column grid, 24px gutters, max-width 1280px (adjust to project)
- **Tablet:** 8-column grid, 20px gutters
- **Mobile:** 4-column grid, 16px gutters
- **Generous margins:** 64–120px horizontal padding on desktop, scale down to 24px on mobile

### 4.B Section Pacing

Design sections to breathe:

- **Hero:** Full viewport height or substantial (500–700px), high impact
- **Features/Benefits:** Dense but organized — cards, icons, or grid layouts
- **Social Proof:** Moderate density — logos, testimonials, metrics
- **CTA:** Focused — one clear action, minimal distraction
- **Footer:** Utilitarian — links, legal, secondary navigation

### 4.C Spacing Scale

--space-1: 0.25rem   /* 4px */
--space-2: 0.5rem    /* 8px */
--space-3: 0.75rem   /* 12px */
--space-4: 1rem      /* 16px */
--space-6: 1.5rem    /* 24px */
--space-8: 2rem      /* 32px */
--space-12: 3rem     /* 48px */
--space-16: 4rem     /* 64px */
--space-24: 6rem     /* 96px */
--space-32: 8rem     /* 128px */
Use multiples of 4 or 8. Don't mix — pick `--space-4` or `--space-6` for a given context, not both.

---

## 5. Component Design

Build components with restraint. Each element should earn its place.

### 5.A Buttons

Primary:   Solid background, white text, 12–16px padding, 6px radius
Secondary: Outlined, accent color border/text, transparent background
Ghost:     No border, text only, subtle hover background
**States:** Default → Hover (darken 10%) → Active (darken 15%) → Disabled (50% opacity, no pointer)

**Rules:**

- One primary action per section
- Button text: verb + noun ("Get started", "View demo")
- Minimum touch target: 44×44px on mobile

### 5.B Cards

- Subtle shadow or border — not both
- Internal padding: 24–32px
- Hover state: slight lift (translateY -2px) + shadow increase, or border color change
- Don't card everything — use whitespace when grouping isn't needed

### 5.C Navigation

- Sticky or fixed only if scroll is minimal or nav is critical
- Mobile: hamburger menu for complex navs; inline links acceptable for simple sites
- Active state: accent color or underline
- Keep nav items to 5–7 max

### 5.D Forms

- Labels above inputs
- 12px font, 40–48px input height
- Focus state: accent color ring, not default browser ring
- Error state: red border + inline error message below field
- Spacing: 16–24px between form groups

### 5.E Imagery and Icons

- **Photography:** Real, contextual, high-quality. No generic stock (handshakes, high-fives, laptops on beaches).
- **Icons:** Lucide, Heroicons, or Phosphor — consistent stroke weight throughout
- **Illustrations:** Optional but adds personality if style is cohesive
- **Avoid:** Uncropped Unsplash hero shots, generic gradients, random blob backgrounds

---

## 6. Motion and Animation

Motion should serve meaning, not decorate.

### 6.A When to Animate

- **Entrance:** Fade + slide up on scroll-into-view (subtle, 300–500ms)
- **Hover:** Micro-interactions on buttons, cards, links (100–200ms)
- **Page transitions:** Only for single-page apps or distinct page states
- **Loading:** Skeleton screens, not spinners, for content areas

### 6.B When Not to Animate

- Core content that users need immediately
- Elements below the fold on initial load
- Users with `prefers-reduced-motion`

### 6.C Implementation

css
/* Respect motion preferences */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}

/* Subtle entrance animation */
.fade-in-up {
  animation: fadeInUp 0.5s ease-out forwards;
  opacity: 0;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
**Easing:** `ease-out` for entrances, `ease-in-out` for state changes. Avoid `linear`.

---

## 7. Responsive Design

Mobile-first. Always.

### 7.A Breakpoints

css
/* Mobile first */
@media (min-width: 640px) { /* sm */ }
@media (min-width: 768px) { /* md */ }
@media (min-width: 1024px) { /* lg */ }
@media (min-width: 1280px) { /* xl */ }
### 7.B Mobile Patterns

- **Stack columns:** 4-col → 2-col → 1-col for feature grids
- **Hide secondary navs:** Condense to hamburger or footer links
- **Reduce padding:** 64px → 24px (scale proportionally)
- **Simplify typography:** Drop display sizes; don't stack as many heading levels
- **Touch targets:** 44px minimum

### 7.C Desktop Patterns

- **Max-width discipline:** Content shouldn't stretch infinitely on wide screens
- **Horizontal breathing room:** Margins > gutters at hero level
- **Multi-column layouts:** Often wasted on mobile — prioritize single-column flow

---

## 8. Accessibility (A11Y)

Accessibility is not optional. It affects real users and legal compliance.

### 8.A Minimum Requirements

- **Color contrast:** 4.5:1 for body text, 3:1 for large text (WCAG AA)
- **Focus states:** Visible, styled, not removed
- **Alt text:** All images have descriptive alt text
- **Semantic HTML:** Proper heading hierarchy, landmarks (`<header>`, `<main>`, `<nav>`, `<footer>`)
- **Form labels:** Every input has an associated `<label>`
- **Skip links:** For pages with substantial navigation

### 8.B Testing Tools

- **axe DevTools** browser extension
- **WAVE** accessibility evaluator
- **Lighthouse** accessibility audit
- Manual keyboard navigation testing

### 8.C Accessibility-First Audiences

For public-sector, healthcare, education, or government projects: **treat WCAG AA as baseline, AAA as target**. Build accessibility in from the start, not as an audit fix.

---

## 9. Design System Integration

Use real design systems when they fit. Don't fake it.

### 9.A When to Use a Framework

- **Tailwind + a component library** (Headless UI, Radix UI) — for utility-first teams
- **Shadcn/UI** — if Vue/React with Tailwind, excellent defaults
- **CSS-in-JS** (Styled Components, Emotion) — if component-level scoping is needed

### 9.B When to Build Custom

- Brand identity is central and frameworks feel generic
- Design is highly distinctive (brutalist, editorial, experimental)
- Minimal footprint required

### 9.C CSS Architecture

/* Variables */
:root { ... }

/* Reset */
*, *::before, *::after { box-sizing: border-box; }

/* Typography */
h1, h2, h3 { ... }

/* Layout */
.container { ... }
.grid { ... }

/* Components */
.btn { ... }
.card { ... }
.input { ... }

/* Utilities (Tailwind) or custom */
.text-balance { text-wrap: balance; }
---

## 10. Pre-Flight Checklist

Before shipping any UI, verify:

- [ ] **Design Read stated** — one line explaining the aesthetic choice
- [ ] **Typography system defined** — heading + body pair, scale applied
- [ ] **Color palette built** — not default colors, not random gradients
- [ ] **Responsive tested** — mobile, tablet, desktop breakpoints functional
- [ ] **Accessibility checked** — contrast, semantic HTML, focus states
- [ ] **Motion respected** — `prefers-reduced-motion` honored
- [ ] **No generic defaults** — no "Lorem Ipsum", no placeholder stock photos
- [ ] **Brand assets integrated** — logo, colors, typography from existing brand when provided
- [ ] **Links functional** — no dead hrefs or placeholder routes
- [ ] **Images optimized** — proper dimensions, alt text present

---

## 11. Redesign Protocol

Redesigns require extra care. The goal is improvement, not erasure.

### 11.A Audit First

Before changing anything, analyze the existing site:

1. **What works:** Identify 3–5 elements worth preserving (layout patterns, content hierarchy, UX flow)
2. **What doesn't:** List specific problems (outdated design, poor mobile experience, accessibility issues)
3. **What must stay:** Brand guidelines, legal requirements, critical navigation paths

### 11.B Preserve vs. Overhaul

| Preserve | Overhaul |
|----------|----------|
| Working navigation patterns | Visual design that ages poorly |
| Clear content hierarchy | Outdated typography and color |
| Established user trust signals | Inconsistent component patterns |
| SEO-performing copy | Broken mobile experience |

### 11.C Change Management

- If client has existing traffic: show before/after, explain improvements
- If redesigning a known brand: maintain enough familiarity that users aren't lost
- If starting fresh: use brief and audience signals to define direction (see Section 0)

---

## 12. Output Format

When delivering frontend code:

1. **State the Design Read** as a comment or header
2. **Use component-based structure** — clear separation of concerns
3. **Include responsive classes** — mobile-first breakpoints
4. **Add accessibility attributes** — ARIA labels, semantic HTML
5. **Reference the pre-flight checklist** — confirm what's been verified

**Code style:**

- Use meaningful class names (BEM, utility classes, or component names)
- Group related styles together
- Include comments for non-obvious decisions
- Keep CSS specificity flat (avoid deep nesting)