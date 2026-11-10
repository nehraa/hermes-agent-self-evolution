---
name: redesign-existing-projects
description: Upgrades existing websites and apps to premium quality. Audits current design, identifies generic AI patterns, and applies high-end design standards without breaking functionality. Works with any CSS framework or vanilla CSS.
---

# Redesign Skill

## How This Works

When applied to an existing project, follow this sequence:

1. **Scan** — Read the codebase. Identify the framework, styling method (Tailwind, vanilla CSS, styled-components, etc.), and current design patterns.
2. **Diagnose** — Run through the audit below. List every generic pattern, weak point, and missing state you find.
3. **Fix** — Apply targeted upgrades working with the existing stack. Do not rewrite from scratch. Improve what's there.

## Design Audit

### Typography

Check for these problems and fix them:

| Problem | Fix |
|---------|-----|
| Browser default fonts or Inter everywhere | Replace with a distinctive font. For modern products: `Geist`, `Outfit`, `Cabinet Grotesk`, `Satoshi`. For editorial/creative: pair a serif header (e.g., `Playfair Display`, `Fraunces`, `Newsreader`) with a clean sans-serif body. |
| Headlines lack presence | Increase display text size by 20-30%, tighten letter-spacing (`-0.02em` to `-0.04em`), reduce line-height to `1.1-1.2`. Headlines should feel heavy and intentional. |
| Body text too wide | Limit paragraph `max-width` to `65ch` or `35em`. Increase `line-height` to `1.6-1.75` for readability. |
| Only Regular (400) and Bold (700) weights | Add Medium (500) for body emphasis and SemiBold (600) for subheadings. This creates subtler hierarchy. |
| Numbers in proportional font | Use `font-variant-numeric: tabular-nums` or a monospace font (e.g., `JetBrains Mono`, `SF Mono`) for prices, statistics, and data. |
| Missing letter-spacing | Apply negative tracking for large headers (`-0.02em`), positive tracking for small caps and labels (`0.05em` to `0.1em`). |
| All-caps subheaders everywhere | Use lowercase italics, sentence case, or true small-caps (`font-variant: small-caps`) instead. |
| Orphaned words on last line | Apply `text-wrap: balance` or `text-wrap: pretty` to prevent single words sitting alone. |

**Typography checklist:**
- [ ] Display/hero text is larger than expected (48px-80px+ for primary headings)
- [ ] Body text is comfortable width (max 65 characters per line)
- [ ] Line-height is generous (1.6+ for body, tighter for headings)
- [ ] At least 3 font weights in use (regular, medium, semibold)
- [ ] Font choice has character and intent

### Color and Surfaces

| Problem | Fix |
|---------|-----|
| Pure `#000000` background | Replace with off-black or tinted dark: `#0a0a0a`, `#121212`, `#0f0f0f`, or dark navy `#0d1117`. Pure black flattens depth. |
| Oversaturated accent colors | Keep saturation below 70-80%. Desaturate accents so they blend with neutrals. Example: instead of `#ff3366`, use `#e8315b` or `#d64d6a`. |
| More than one accent color | Pick one primary accent. Use it consistently. Secondary accents should be neutral (grays, muted tones). |
| Mixing warm and cool grays | Choose one gray family and tint all grays with that hue. Warm grays: add yellow/orange undertone. Cool grays: add blue undertone. |
| Purple/blue "AI gradient" aesthetic | This is dated. Replace with a single solid accent or a subtle warm gradient if needed. |
| No elevation/dimension | Add subtle shadows: `box-shadow: 0 1px 2px rgba(0,0,0,0.05)` for resting, `0 4px 6px rgba(0,0,0,0.1)` for hover, `0 10px 15px rgba(0,0,0,0.1)` for elevated. |
| Borders too harsh | Replace pure black borders (`#000`) with `rgba(0,0,0,0.1)` or `rgba(255,255,255,0.1)` for dark themes. |
| Flat surfaces | Add subtle texture or gradient overlays. Even a `1-2%` opacity gradient can add life. |

**Color checklist:**
- [ ] Backgrounds are not pure black/white
- [ ] Accent color is one, consistent, and desaturated
- [ ] Gray scale is unified (all warm or all cool)
- [ ] Surfaces have depth through shadows and borders
- [ ] Text contrast meets WCAG AA (4.5:1 for body, 3:1 for large text)

### Spacing and Layout

| Problem | Fix |
|---------|-----|
| Uniform padding everywhere | Vary padding by context. Hero sections need more breathing room (80px-120px). Cards need tighter padding (16px-24px). |
| Elements crammed together | Increase vertical spacing between sections to `80px-120px` on desktop. Let content breathe. |
| No visual rhythm | Create consistent spacing scale: `4px`, `8px`, `16px`, `24px`, `32px`, `48px`, `64px`, `96px`. Use only these values. |
| Content touches viewport edges | Add horizontal padding: `max-width: 1200px` with `auto` margins, or `padding-left: 24px; padding-right: 24px` on mobile. |
| Section headers aligned oddly | Left-align section headers. They should not be centered unless the layout intentionally calls for it. |

**Spacing checklist:**
- [ ] Vertical rhythm is consistent (use a spacing scale)
- [ ] Hero and feature sections have generous padding
- [ ] Content has comfortable max-width
- [ ] Mobile has adequate horizontal padding (16px minimum)

### Interactive States

| Problem | Fix |
|---------|-----|
| No hover states | Every interactive element needs hover. Use subtle changes: slight scale (1.02), shadow lift, or background shift. |
| Hover changes color drastically | Hover should be subtle. Shift lightness by 5-10%, not full color transformation. |
| No focus states | Add visible focus rings: `outline: 2px solid currentColor; outline-offset: 2px` or custom styled focus. |
| No active/pressed states | Elements should feel pressed on click: slight scale down (0.98) or darker background. |
| Transitions too slow or missing | Add `transition: all 150ms ease` or `200ms ease-out` for snappy, natural-feeling interactions. |
| No disabled states | Disabled buttons should be visually muted: `opacity: 0.5`, `cursor: not-allowed`. |

**States checklist:**
- [ ] Every interactive element has hover state
- [ ] Focus states are visible and accessible
- [ ] Active/pressed states provide feedback
- [ ] Disabled states are clearly muted
- [ ] Transitions are smooth but quick (150-300ms)

### Components

| Problem | Fix |
|---------|-----|
| Buttons look generic | Give buttons unique character: subtle border radius (6px-12px), custom padding, distinctive shadow. |
| Cards lack depth | Add subtle borders, gentle shadows, or background differentiation from the page. |
| Form inputs look browser-default | Style inputs: remove default appearance, add border, padding, and focus ring. |
| Icons are inconsistent | Pick one icon library and stick to it (Phosphor, Lucide, Heroicons). Ensure consistent stroke width. |
| Loading states missing | Add spinners, skeletons, or shimmer effects for async content. |
| Empty states absent | Design empty states with illustration, helpful message, and action button. |

### Motion and Animation

| Problem | Fix |
|---------|-----|
| No animations at all | Add subtle entrance animations: fade-up on scroll, staggered reveals for lists. |
| Animations are distracting | Keep animations under 400ms. Use `ease-out` for entrances, `ease-in` for exits. |
| Everything animates equally | Prioritize: entrance > hover > active. Don't animate background colors on page load. |
| Layout shifts on load | Reserve space for async content with skeletons or min-heights. |

**Motion checklist:**
- [ ] Page has subtle entrance animations
- [ ] Hover states include motion
- [ ] Animations respect `prefers-reduced-motion`
- [ ] No jarring layout shifts

## Common "AI Slop" Patterns to Remove

These indicate generic, AI-generated design. Audit for and remove:

- [ ] Purple-to-blue gradient backgrounds
- [ ] Generic stock photos of people using laptops
- [ ] "We build products that scale" type placeholder copy
- [ ] Inter font on every project
- [ ] Floating geometric shapes (circles, blobs) as decoration
- [ ] Marquee text or scrolling announcements
- [ ] "Powered by AI" badges or bot avatars
- [ ] Generic "Get Started" CTAs with no personality
- [ ] Flat illustration style with no depth
- [ ] Card grids where every card is identical

## Implementation Order

1. **Typography first** — Font choices and sizing affect everything
2. **Colors and surfaces** — Establish the palette and background system
3. **Spacing and layout** — Create the grid and rhythm
4. **Interactive states** — Add hover, focus, active, disabled states
5. **Components** — Style buttons, cards, forms, inputs
6. **Motion** — Add entrance animations and micro-interactions
7. **Polish** — Scrollbar, selection colors, smooth scrolling

## Principles

- **Work with the existing stack.** Don't rewrite; upgrade.
- **Less is more.** Remove decoration before adding it.
- **Consistency over variety.** One font, one accent, one style.
- **Subtlety signals quality.** Dramatic gradients and loud colors feel cheap.
- **Content informs design.** The redesign should serve the content, not compete with it.