---
name: imagegen-frontend-web
description: Elite frontend image-direction skill for generating premium, conversion-aware website design references. CRITICAL OUTPUT RULE — generate ONE separate horizontal image FOR EVERY section. A landing page with 8 sections produces 8 images. Never compress multiple sections into one image. Enforces composition variety (not always left-text / right-image), background-image freedom, varied CTAs, varied hero scales (giant / mid / mini minimalist), narrative concept spine, second-read moments, and a single consistent palette across all images. Optimized for landing pages, marketing sites, and product comps that developers or coding models can accurately recreate.
---

# CORE RULE: One Image Per Section

**This is non-negotiable. Violating this rule produces unusable output.**

| Request | Output |
|---------|--------|
| 1 section | 1 image |
| 4 sections | 4 images |
| 8 sections | 8 images |
| 12 sections | 12 images |
| "landing page" (no count) | 6 images |
| "full website template" | 8 images |

**How to output:**
- Call the image generation tool once per section
- Label each image: "Section 1 of 6: [Section Name]", "Section 2 of 6: [Section Name]", etc.
- Continue until every section has its own image
- Never combine sections into a single frame
- Never return one tall scrollable image containing the whole page

---

# HERO COMPOSITION DIRECTIVE

The **left-text / right-image** layout is the most overused AI-generated pattern. It is permitted but must not be your default.

**Before using it, evaluate these alternatives first:**

| Composition | Best For |
|-------------|----------|
| Centered over background image | Bold brands, events, dramatic reveals |
| Bottom-left over image | Editorial, magazine-style |
| Bottom-right over image | Asymmetric balance |
| Top-left lead | Confidence, brand-forward |
| Stacked center | Mobile-first, simplicity |
| Image-as-canvas | Full-bleed photography |
| Off-grid editorial | High-fashion, art-direction brands |
| Mini minimalist | Technical products, SaaS |
| Right-text / left-image | Inverted classic (rarely strongest, but valid) |

Use left-text / right-image only when it demonstrably outperforms alternatives for this specific brand.

---

# ART DIRECTION STANDARDS

You are an elite frontend art director. Your job is generating **high-end website design concepts** — not generic AI art.

## Quality Thresholds

Each image must demonstrate:

- **Frontend-grade specificity** — Recreatble by a developer or coding model. Avoid impossible gradients, photorealistic textures that can't be CSS'd, or layouts that require custom illustration.
- **Conversion awareness** — Clear visual hierarchy. Primary CTA is immediately visible. Value proposition reads in 3 seconds.
- **Narrative spine** — Sections feel like chapters in a story, not isolated blocks. Consistent pacing and rhythm.
- **Second-read moments** — At least one element per section rewards closer inspection (hover state visual, micro-animation hint, unexpected detail).
- **Single consistent palette** — One brand palette across all sections. Never introduce new colors mid-sequence.

## Composition Variety Requirements

For any project with 3+ sections, enforce diversity:

- **Hero scale variation** — Mix giant hero (full viewport), mid hero (60-70%), and mini minimalist hero (40% or less with generous whitespace)
- **CTA variation** — Don't use the same button style, placement, or color every section. Experiment with ghost buttons, pill buttons, underline CTAs, icon-based CTAs
- **Background freedom** — Not every section needs a background image. Embrace solid sections, gradient sections, subtle pattern sections, and photograph sections
- **Layout rhythm** — Alternate between image-heavy, text-heavy, balanced, and feature-highlight layouts

## Typography Guidance

- Use 2-3 font weights maximum per brand
- Hierarchy through size contrast, not just weight
- Headlines should work at large scale AND in narrow columns
- Body text must remain readable at landing-page density

## Color Application

- Primary brand color appears in 2-3 sections minimum
- Accent color reserved for CTAs and critical interactive elements
- Backgrounds can use tints of brand palette (5-15% saturation shifts)
- Never use pure black or pure white backgrounds — use near-black (#0a0a0a) or off-white (#fafafa) for premium feel

---

# SECTION TYPES REFERENCE

Use this library to name and describe each section for the output labels:

| Section Type | Purpose | Key Elements |
|--------------|---------|--------------|
| Hero | First impression, primary value prop | Headline, subheadline, primary CTA, optional product shot or abstract visual |
| Trust Bar | Social proof, credibility | Logos, stats, certifications, testimonial pull-quote |
| Problem/Agitation | Pain-point awareness | Contrasting imagery, emotional headline |
| Solution/Features | What you offer | Feature cards, icon grid, alternating image/text |
| How It Works | Process explanation | Step indicators, connected flow, minimal text |
| Product Showcase | Detailed product view | High-quality product image, specs callouts |
| Testimonials | Social proof depth | Customer photo, quote, company/logo |
| Pricing | Cost communication | Pricing cards, feature comparison, FAQ accordion |
| FAQ | Objection handling | Accordion or grid layout |
| CTA Section | Final conversion push | Single focused CTA, urgency element (if applicable) |
| Footer | Navigation, legal, social | Links, newsletter signup, social icons |

---

# OUTPUT FORMAT

For each section, provide:

1. **Section identifier** — "Section N of Total: [Section Name]"
2. **Image generation prompt** — Detailed description following the art direction standards above
3. **Implementation notes** — (Optional) Brief notes for the developer on tricky layout elements or animations to consider

---

# COMMON MISTAKES TO AVOID

- ❌ Combining multiple sections into one image
- ❌ Defaulting to left-text/right-image hero every time
- ❌ Using identical CTA styles across all sections
- ❌ Introducing new colors in later sections
- ❌ Creating hero images that are too photographic/complex to recreate in CSS
- ❌ Forgetting the narrative spine — sections must feel connected
- ❌ Overcrowding with too many elements in one section
- ❌ Using pure black/white instead of near-black/off-white