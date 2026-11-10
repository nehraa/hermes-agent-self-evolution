---
name: redesign-existing-projects
description: Upgrades existing websites and apps to premium quality. Audits current design, identifies generic AI patterns, and applies high-end design standards without breaking functionality. Works with any CSS framework or vanilla CSS.
---

# Redesign Existing Projects

Transform generic, AI-generated, or outdated designs into premium-quality interfaces. This skill audits the current state, identifies weak patterns, and applies targeted improvements—never a full rewrite.

## The Process

Follow this three-step sequence for every project:

1. **Scan** — Read the codebase. Identify the framework, styling approach (Tailwind, vanilla CSS, CSS-in-JS), component structure, and existing design tokens.
2. **Diagnose** — Run the audit below. Document every generic pattern, weak point, and missing state.
3. **Fix** — Apply targeted upgrades using the existing stack. Preserve functionality. Improve what's there.

## Design Audit

Work through each section systematically. Mark findings and fixes.

---

### Typography

**Font Choices**
- ❌ Browser defaults (system-ui) or Inter used everywhere
- ❌ Generic sans-serif with no personality
- ✅ Replace with a distinctive font: `Geist`, `Outfit`, `Instrument Sans`, `Cabinet Grotesk`, or `Satoshi`
- ✅ For editorial/brand-forward projects: pair a serif header (e.g., `Playfair Display`, `Fraunces`, `Lora`) with a clean sans-serif body

**Headlines**
- ❌ Headlines the same size as body text
- ❌ Loose letter-spacing and line-height that feels academic
- ✅ Increase display sizes significantly (48px–80px+ for H1)
- ✅ Tighten letter-spacing: `-0.03em` to `-0.05em` for large text
- ✅ Reduce line-height to `1.1–1.2` for headlines

**Body Text**
- ❌ Full-width paragraphs spanning 100+ characters
- ❌ Line-height too tight (1.2–1.4)
- ✅ Cap paragraph width at ~65 characters (`max-width: 65ch`)
- ✅ Increase line-height to `1.6–1.75` for body copy

**Font Weights**
- ❌ Only Regular (400) and Bold (700) used
- ✅ Add Medium (500) and SemiBold (600) for hierarchy
- ✅ Use weight strategically—don't make everything medium

**Numbers and Data**
- ❌ Numbers in proportional font causing alignment issues
- ✅ Use monospace font or enable `font-variant-numeric: tabular-nums` for tables, stats, prices, and codes

**Letter-Spacing**
- ❌ No tracking adjustments anywhere
- ✅ Add negative tracking to large headlines: `letter-spacing: -0.03em`
- ✅ Add subtle tracking to labels and all-caps text: `letter-spacing: 0.05em–0.1em`

**Subheaders**
- ❌ All-caps subheaders used for emphasis
- ✅ Try lowercase italics, sentence case, or small-caps instead

**Orphans**
- ❌ Single words stranded on the last line
- ✅ Use `text-wrap: balance` for headings, `text-wrap: pretty` for body text

---

### Color and Surfaces

**Backgrounds**
- ❌ Pure `#000000` or `#ffffff` backgrounds
- ✅ Use off-black (`#0a0a0a`, `#121212`) or charcoal (`#1a1a1a`)
- ✅ Use warm whites (`#fafaf9`, `#f8f8f7`) or cool whites (`#f5f5f7`) instead of pure white

**Gray Palette**
- ❌ Warm grays mixed with cool grays in the same UI
- ✅ Pick one temperature and stick with it across all grays
- ✅ Use a tool like Suru's 10-step scale or create a consistent 10-step neutral ramp

**Accent Colors**
- ❌ Oversaturated blues, purples, or brand colors (saturation >80%)
- ✅ Desaturate accents so they harmonize with neutrals
- ✅ Pick one primary accent color. Remove the rest.
- ❌ Multiple accent colors competing for attention
- ✅ Consistency and restraint beat variety

**AI Aesthetic Red Flags**
- ❌ Purple-to-blue gradients as backgrounds or accents
- ❌ Glowing effects, glassmorphism, or rainbow borders
- ❌ Rounded avatar images or circular UI elements everywhere
- ❌ Neon or electric accent colors
- ✅ Use solid, muted colors with intentional contrast

**Shadows and Depth**
- ❌ `box-shadow: 0 2px 8px rgba(0,0,0,0.1)` on everything
- ❌ Flat design with no depth cues
- ✅ Use layered shadows: a subtle ambient shadow + a directional drop shadow
- ✅ For elevated cards: `0 1px 2px rgba(0,0,0,0.05), 0 4px 12px rgba(0,0,0,0.08)`
- ✅ Use borders instead of shadows for subtle separation: `border: 1px solid rgba(0,0,0,0.08)`

---

### Spacing and Layout

**Spacing Consistency**
- ❌ Random spacing values throughout (8px, 13px, 22px, 37px)
- ✅ Establish a spacing scale: 4, 8, 12, 16, 24, 32, 48, 64, 96, 128
- ✅ Use values from the scale exclusively

**Visual Rhythm**
- ❌ Section padding inconsistent across pages
- ✅ Define standard spacing for section types: hero (96–128px), content (64–96px), compact (32–48px)

**Width and Content**
- ❌ Content stretching to full viewport width on large screens
- ✅ Cap content width: 1280px for layouts, 720px for reading content
- ✅ Use fluid typography and spacing that scales with viewport

**Grid Alignment**
- ❌ Elements slightly off-grid or misaligned
- ✅ Ensure all elements align to the 4px or 8px grid
- ✅ Check icon-to-text alignment (icons should visually center with text)

---

### Components and States

**Buttons**
- ❌ Only one button style used for everything
- ❌ Gradient buttons or 3D beveled buttons
- ✅ Define 2–3 button variants: primary (filled), secondary (outlined), ghost (text only)
- ✅ Add hover, active, focus, and disabled states
- ✅ Use subtle transitions (150–200ms ease)

**Forms and Inputs**
- ❌ Thin, 1px borders on inputs
- ❌ No focus states or generic blue focus rings
- ✅ Use 2px borders that change color on focus
- ✅ Add placeholder text that disappears on focus
- ✅ Provide clear error states with distinct colors and helpful messages

**Empty States**
- ❌ Blank pages or "No data" text only
- ✅ Design empty states with illustrations, helpful copy, and a call-to-action

**Loading States**
- ❌ Spinning wheels or generic loading indicators
- ✅ Use skeleton loaders that match the content shape
- ✅ Add subtle shimmer animation (not aggressive)

**Hover and Interaction Feedback**
- ❌ No visual feedback on interactive elements
- ✅ Add hover states to all clickable elements
- ✅ Use subtle scale, color shift, or shadow lift on hover
- ✅ Add active/pressed states that feel tactile

---

### Motion and Animation

**Animation Quality**
- ❌ No animations or transitions (feels static and cheap)
- ❌ Overly bouncy or playful animations in professional contexts
- ❌ Animations that block user interaction
- ✅ Use subtle entrance animations: fade + slight translate (opacity 0→1, translateY 8px→0, 300ms ease-out)
- ✅ Stagger animations for lists: 50–100ms delay between items
- ✅ Respect `prefers-reduced-motion`—disable or simplify animations

**Transitions**
- ❌ Instant color changes on hover
- ✅ Use `transition: all 150ms ease` or similar for smooth state changes
- ❌ Extremely long transitions (>400ms) for simple interactions
- ✅ Keep micro-interactions under 200ms

---

### Iconography

**Icon Consistency**
- ❌ Mixing icon styles (some filled, some outlined, different stroke widths)
- ❌ Icons that don't align with each other or with text
- ✅ Pick one icon library or style and use it exclusively
- ✅ Standardize stroke width (typically 1.5px–2px)
- ✅ Set icons to the same size or use a consistent grid (16px, 20px, 24px)

**Icon Sizing**
- ❌ Icons that are too small (12px) or too large (32px) for context
- ✅ Use 16px for inline icons, 20–24px for standalone icons

---

### Polish Checklist

Before completing the redesign, verify:

- [ ] All interactive elements have hover, focus, active, and disabled states
- [ ] Typography scale is intentional and hierarchical
- [ ] Colors are consistent and restrained (no more than 3–4 colors total)
- [ ] Spacing follows a defined scale
- [ ] Shadows and borders create appropriate depth
- [ ] Animations are subtle and purposeful
- [ ] No generic "AI aesthetic" patterns remain
- [ ] Content width is capped appropriately
- [ ] Mobile layouts are functional and refined
- [ ] Loading, empty, and error states are designed

---

### What to Avoid

- **Full rewrites** — This skill improves existing projects. Don't rebuild from scratch.
- **Framework conversion** — If the project uses Tailwind, work with Tailwind. Don't convert to CSS modules unless requested.
- **Breaking changes** — Every change should preserve existing functionality. Test after each fix.
- **Over-designing** — Subtle improvements beat dramatic overhauls. Trust the process.
- **AI clichés** — Purple gradients, glassmorphism, glowing effects, and rainbow accents signal low-quality design. Remove them.