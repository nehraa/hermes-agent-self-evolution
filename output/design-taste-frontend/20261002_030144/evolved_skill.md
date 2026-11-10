---
name: design-taste-frontend
description: Anti-slop frontend skill for landing pages, portfolios, and redesigns. The agent reads the brief, infers the right design direction, and ships interfaces that do not look templated. Real design systems when applicable, audit-first on redesigns, strict pre-flight check.
---

# Anti-Slop Frontend Skill

> **Scope:** Landing pages, portfolios, and redesigns.
> **Out of scope:** Dashboards, data tables, multi-step product flows, authenticated app UI.
>
> Every rule below is **contextual**. None fires automatically. Read the brief first, then pull only what fits.

---

## 0. BRIEF INFERENCE

Before writing a single line of code, infer what the user actually wants. Most LLM-generated design is bad because it defaults to a generic aesthetic instead of reading the context.

### 0.A Read These Signals First

1. **Page kind** — SaaS landing, consumer landing, agency site, event page, portfolio (dev / designer / studio), editorial/blog, redesign
2. **Vibe words** — "minimalist", "calm", "Linear-style", "Awwwards", "brutalist", "premium", "Apple-y", "playful", "B2B serious", "editorial", "agency-y", "glassy", "dark tech"
3. **Reference signals** — URLs pasted, screenshots attached, products or brands named, competitors cited
4. **Audience** — B2B procurement panel, design-conscious consumer, hiring manager, recruiter scanning portfolios. The audience determines the aesthetic, not preference.
5. **Existing brand assets** — logo, colors, typography, photography. For redesigns, these are mandatory starting material, not optional input.
6. **Quiet constraints** — Accessibility-first, public-sector, regulated industries, trust-first commerce, children’s products. These constraints **override** aesthetic preference.

### 0.B State a One-Line Design Read

Before generating any code, output:

Reading this as: <page kind> for <audience>, with a <vibe> language, leaning toward <design system or aesthetic family>.
**Examples:**
- *Reading this as: B2B SaaS landing for technical buyers, with a Linear-style minimalist language, leaning toward Tailwind + Geist + restrained motion.*
- *Reading this as: Solo designer portfolio for hiring managers, with an editorial/kinetic-type language, leaning toward native CSS + scroll-driven animation + custom typography.*
- *Reading this as: Redesign of a public-sector service site, with a trust-first accessibility language, leaning toward GOV.UK patterns + system fonts + WCAG AA compliance.*

---

## 1. DESIGN SYSTEM SELECTION

Match the implementation approach to the inferred aesthetic. Don't force Tailwind everywhere. Don't reach for Bootstrap ever.

### 1.A System Families

| Aesthetic Family | Implementation Approach |
|------------------|------------------------|
| **Minimal tech (Linear, Vercel, Raycast)** | Tailwind + Geist/Sora fonts + minimal shadows + subtle borders |
| **Editorial / magazine** | Native CSS with custom properties + serif headings (Fraunces, Playfair, Source Serif) + generous whitespace |
| **Premium consumer (Apple, high-end product)** | CSS custom properties + SF Pro / Inter + glass/blur effects + restrained palette |
| **Agency / creative studio (Awwwards)** | Custom CSS + kinetic typography + scroll-driven animation + experimental layout |
| **Brutalist** | Native CSS + stark typography + exposed grid + high contrast |
| **Trust-first / institutional** | System fonts + constrained palette + GOV.UK / USWDS patterns + WCAG AA minimum |

### 1.B When to Use a Framework

Use Tailwind (or similar utility-first) when:
- The user explicitly requested it
- Speed is critical and the aesthetic is "minimal tech"
- No complex custom design system exists

Reach for custom CSS when:
- The aesthetic is editorial, brutalist, or experimental
- Typography is the hero (custom serifs, variable fonts)
- The project requires unique interaction patterns

**Never** use Bootstrap, Material UI, or other generic component libraries for aesthetic work. They scream "template."

---

## 2. COMPONENT ARCHITECTURE

### 2.A Hero Section Patterns

The hero makes the first impression. Get this right or redo.

**SaaS / Tech Landing:**
- Large, confident headline (not a paragraph)
- Subheadline with concrete value prop (not marketing fluff)
- Single primary CTA (not three buttons)
- Optional: product screenshot or abstract visual

**Portfolio:**
- Name + role above the fold
- Selected work visible without scrolling, or single strong project image
- Personal brand signal (color, typography, or layout — not a headshot)

**Editorial:**
- Pull quote or striking image spanning full width
- Headline in display serif, not sans-serif
- Minimal chrome — let content breathe

### 2.B Section Rhythm

Alternate visual density:
- **Loud** section (large type, image, or dark background) → **Quiet** section (text, whitespace)
- Never stack three loud sections or three quiet sections consecutively

### 2.C Typography Hierarchy

H1: Hero headline (3rem–6rem, depending on viewport)
H2: Section heading (1.75rem–3rem)
H3: Subsection or card title (1.25rem–1.5rem)
Body: 1rem–1.125rem, line-height 1.6–1.75
Caption / label: 0.75rem–0.875rem, uppercase tracking
Use **one** display font (headings) and **one** body font. Maximum two typefaces per page.

### 2.D Color Palette Construction

Build a 5-color functional palette:

1. **Background** — off-white `#FAFAFA` or near-black `#0A0A0A`
2. **Surface** — slightly elevated (`#F5F5F5` / `#111111`)
3. **Text primary** — high contrast (`#171717` / `#FAFAFA`)
4. **Text muted** — for secondary content (`#737373` / `#A3A3A3`)
5. **Accent** — one brand color, used sparingly (CTAs, highlights)

**Dark mode:** If designing dark-first, flip the logic. Don't just add `dark:` classes to a light palette — test if the color relationships still work.

---

## 3. MOTION & INTERACTION

Motion should serve **clarity**, not decoration.

### 3.A Animation Principles

- **Entrance:** Staggered fade-up (opacity 0→1, translateY 20px→0, 400ms ease-out, 80ms stagger)
- **Hover:** Immediate response (100–150ms). Scale, shadow lift, or color shift.
- **Scroll-driven:** Parallax, reveal-on-scroll, or sticky elements for editorial/agency aesthetics only. Don't force scroll animation on B2B or trust-first sites.
- **Page transitions:** Subtle fade (200ms) if applicable. Never slide-in banners.

### 3.B Animation on Mobile

- Disable parallax on mobile (performance)
- Reduce motion duration by 30–50%
- Respect `prefers-reduced-motion` media query — always

### 3.C Anti-Patterns to Avoid

- ❌ Auto-playing videos or carousels
- ❌ Blinking, pulsing, or rotating elements
- ❌ Scroll-jacking
- ❌ Confetti, snow, or "delight" particles
- ❌ Loading spinners on the main thread

---

## 4. PRE-FLIGHT CHECKLIST

Run this checklist before delivering any code.

### 4.A Design Audit

- [ ] Does the hero section make the value prop clear in 3 seconds?
- [ ] Is the visual hierarchy (H1 → H2 → body) consistent?
- [ ] Are colors from a cohesive palette (not 12 random hex codes)?
- [ ] Is whitespace used deliberately (not randomly)?
- [ ] Does the page look like a template? If yes, deviate.

### 4.B Technical Audit

- [ ] All images have `alt` attributes
- [ ] Color contrast meets WCAG AA (4.5:1 for body text, 3:1 for large text)
- [ ] Focus states are visible on all interactive elements
- [ ] Font sizes are responsive (no 80px text on mobile)
- [ ] No Lorem Ipsum or placeholder content in final output
- [ ] Semantic HTML: `<header>`, `<main>`, `<footer>`, `<nav>`, `<section>`, `<article>`

### 4.C Performance Check

- [ ] No render-blocking fonts (use `font-display: swap` or `preload`)
- [ ] Images are sized appropriately (WebP, lazy-loaded)
- [ ] No unused CSS or JavaScript

---

## 5. REDESIGN PROTOCOL

Redesigns require extra care. You're building on existing brand equity and user expectations.

### 5.A Audit First, Don't Assume

Before proposing changes:
1. List what exists: brand assets, color usage, typography, component patterns, layout conventions
2. Ask: "What's working? What's the user complaint?"
3. Identify sacred elements (logo, tagline, established brand colors)
4. Distinguish between **cruft** (worth removing) and **familiarity** (worth keeping)

### 5.B Preserve vs. Overhaul

| Element | Default Action |
|---------|----------------|
| Logo | Preserve unless redesigning brand too |
| Brand colors | Preserve primary; refine secondary |
| Established navigation structure | Preserve; improve if broken |
| Typography on body text | Preserve; upgrade headings |
| Page structure / content | Audit and overhaul |

### 5.C Communicate the Rationale

For each significant change, explain in one line:
> *"Changed the hero from dark to light because [specific reason], aligning with [reference or principle]."*

---

## 6. ANTI-SLOP RULES

These are non-negotiable. Break them only if the user explicitly requests it.

### 6.A Typography Anti-Slop

- ❌ Inter on every project
- ❌ Roboto, Open Sans, or Lato
- ❌ More than two typefaces
- ❌ 14px body text
- ❌ Centered body text (left-align, always)

### 6.B Layout Anti-Slop

- ❌ Hero → Features → Pricing → Testimonials → CTA (the generic template)
- ❌ Full-width colored banner sections alternating with white
- ❌ Three-column feature grids (use asymmetric layouts)
- ❌ Centered everything (asymmetry creates interest)
- ❌ Grid with gutters wider than content padding

### 6.C Interaction Anti-Slop

- ❌ Sticky headers on scroll
- ❌ Cookie consent banners that block the page
- ❌ "Click to copy" on email addresses (just make it a `mailto:`)
- ❌ Infinite scroll on marketing pages
- ❌ "Welcome back" modals

### 6.D Copy Anti-Slop

- ❌ "We help you [verb] your [noun]"
- ❌ "Next-generation [existing category]"
- ❌ "Empowering" / "Revolutionary" / "Seamless"
- ❌ "Trusted by 10,000+ customers" without names
- ❌ "Sign up for our newsletter" (specify the value: "Get weekly design links")

---

## 7. DELIVERY FORMAT

When the implementation is complete, output:

✓ Design Read: [one-line summary]
✓ Design System: [family + specific choices]
✓ Key Decisions: [1-3 sentences on any non-obvious choices]
✓ Pre-Flight: [PASS / FAIL + any open items]
✓ Anti-Slop Compliance: [list any rules explicitly broken at user's request]
---

*This skill is anti-slop by default. If the user requests something on the anti-slop list, acknowledge it, note the trade-off, and proceed.*