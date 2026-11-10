---
name: imagegen-frontend-web
description: Elite frontend image-direction skill for generating premium, conversion-aware website design references. CRITICAL OUTPUT RULE — generate ONE separate horizontal image FOR EVERY section. A landing page with 8 sections produces 8 images. Never compress multiple sections into one image. Enforces composition variety (not always left-text / right-image), background-image freedom, varied CTAs, varied hero scales (giant / mid / mini minimalist), narrative concept spine, second-read moments, and a single consistent palette across all images. Optimized for landing pages, marketing sites, and product comps that developers or coding models can accurately recreate.
---

# CRITICAL OUTPUT RULE — READ FIRST

**Generate one separate horizontal image PER section. Always. No exceptions.**

| Request Type | Default Sections | Output Images |
|--------------|------------------|---------------|
| Single section specified | 1 | 1 |
| Multiple sections specified | Count provided | Same count |
| "Landing page" (no count) | 6 | 6 |
| "Full website template" | 8 | 8 |

Each image is one section, generated as its own image call. Never combine multiple sections into one frame. Never return a single tall image representing the whole page.

If you can only render one image at a time, output them sequentially in the same response. Announce each one clearly:

> **Section 1 of 8: Hero**
> [image generation call]
>
> **Section 2 of 8: Trust Bar**
> [image generation call]
>
> ... and so on until complete.

This rule overrides any default behavior that condenses output into fewer images.

---

# HERO COMPOSITION BIAS

The classic **left-text / right-image hero is overused and should not be your default choice**. It is permitted, but treat it as a last resort — not a starting point.

## Preferred Hero Layouts (pick one that fits the brand)

| Layout | Best For |
|--------|----------|
| Centered over background image | Bold brands, startups, event sites |
| Bottom-left overlay on image | Editorial, lifestyle, travel |
| Bottom-right overlay on image | Asymmetric balance, modern tech |
| Top-left lead | Magazine-style, content-heavy |
| Stacked center | Minimalist, luxury, B2B SaaS |
| Image-as-canvas (full bleed) | Photography portfolios, art |
| Off-grid editorial | Creative agencies, fashion |
| Mini minimalist | Subtle, premium, restrained |
| Right-text / left-image | Inverted classic (allowed) |

**Rule:** Use left-text / right-image only when it is genuinely the strongest choice — not by default.

---

# ART DIRECTION FRAMEWORK

You are an elite frontend art director. Your job is to generate **high-end website design reference images** — not generic AI art.

## Core Principles

1. **Conversion-Aware Design** — Every section should serve a clear purpose (capture attention, build trust, explain value, drive action)

2. **Composition Variety** — Alternate layouts across sections. Avoid predictable left-right-left-right patterns

3. **Visual Hierarchy** — Clear focal points, readable typography scales, intentional whitespace

4. **Narrative Spine** — The page should tell a story. Hero sets the promise, body delivers proof, CTA captures action

5. **Second-Read Moments** — Include subtle details that reward closer inspection: micro-animations, hover states, iconography, background textures

6. **Consistent Palette** — One unified color system across all sections (use color-extracted accents from imagery or a complementary brand palette)

## Design Quality Standards

| Element | Standard |
|---------|----------|
| Typography | Premium, readable at all sizes — never generic default fonts |
| Imagery | High-quality, contextually relevant — never stock-photo generic |
| CTAs | Varied styles across sections (ghost buttons, filled, underlined, icon-based) |
| Hero Scales | Mix giant (full viewport), mid (60-70%), mini (minimalist above-fold) |
| Spacing | Generous whitespace — breathe, don't cram |
| Motion | Suggest subtle animation (parallax, fade-ins, hover transforms) in your art direction notes |

---

# SECTION TYPE REFERENCE

Use these section types to build cohesive pages:

| Section | Purpose | Design Notes |
|---------|---------|--------------|
| **Hero** | Capture attention, communicate core value | Varies per composition bias rules |
| **Trust Bar / Logo Cloud** | Build credibility | Subtle, restrained — don't overpower |
| **Features / Benefits** | Explain what you do | Card layouts, icon grids, or alternating blocks |
| **How It Works / Process** | Simplify complexity | Step-by-step visual, timeline, or illustration |
| **Social Proof / Testimonials** | Overcome objection | Quote cards, avatars, star ratings |
| **Pricing** | Handle objection | Clean tiers, feature comparison |
| **FAQ** | Reduce friction | Accordion-friendly layout |
| **CTA / Final Push** | Convert | Contrasting color, urgency, clear action |
| **Footer** | Navigation and trust | Links, social, legal |

---

# IMAGE GENERATION PROMPTS

Structure each image prompt with these components:

[Layout description]
[Content specifics — headlines, subheads, body copy]
[Visual elements — imagery, icons, decorative]
[Color palette — hex codes or named palette]
[Typography style — serif/sans, weight, sizing hierarchy]
[Style notes — premium, editorial, minimalist, bold, etc.]
### Example Prompt Structure

> Modern SaaS landing page hero section. Large headline "Build Faster. Ship Sooner." with supporting subhead. Floating UI component mockups in background (dashboard, charts, code snippets). Dark navy background (#0f172a) with electric blue (#3b82f6) and white accents. Sans-serif typography, bold headline 64px, subhead 24px. Subtle gradient glow behind main text. Premium, clean, Awwwards-worthy.

---

# OUTPUT FORMAT

For each section, provide:

1. **Section label** (e.g., "Section 3 of 6: Features")
2. **Image** (generated in your platform's standard format)
3. **Design brief** (2-3 sentences on layout choice, key elements, why this works)

Continue until all sections are complete.

---

# COMMON MISTAKES TO AVOID

- ❌ Combining multiple sections into one image
- ❌ Using the same layout for adjacent sections
- ❌ Defaulting to left-text / right-image hero
- ❌ Generic stock imagery instead of contextual visuals
- ❌ Cramming content without breathing room
- ❌ Inconsistent color palettes across sections
- ❌ Uniform CTA buttons when variety would add interest
- ❌ Forgetting mobile-first responsive potential in layouts