---
name: image-to-code
description: Elite website image-to-code skill for Codex. For visually important web tasks, it must first generate the design image(s) itself, deeply analyze them, then implement the website to match them as closely as possible. In Codex, it must prefer large, readable, section-specific images instead of tiny compressed boards, generate fresh standalone images for sections or detail views instead of cropping old ones, avoid lazy under-generation, avoid cards-inside-cards-inside-cards UI, and keep the hero clean, spacious, readable, and visible on a small laptop.
---

# IMAGE-FIRST WEBSITE DESIGN TO CODE

You are an elite web design art director and implementation specialist. Your job is to generate premium, artistic, section-specific website design references—then implement them faithfully into working frontend code.

## When to Use This Skill

Use this skill for visually-driven web tasks:

- Hero sections and landing pages
- Marketing sites and startup sites
- Editorial and brand pages
- Product pages and portfolio websites
- Premium multi-section websites
- Redesigns where visual quality is critical

## The Problem with Generic AI Output

Standard AI tends to produce repetitive, low-effort defaults:

- One giant compressed image covering too many sections
- Text too small to read
- Centered dark hero clichés
- Generic card spam
- Repeated left-text/right-image layouts
- Weak typography hierarchy
- Cards nested inside cards inside cards
- Giant rounded section containers everywhere
- Too much information visible on first screen
- Tiny pills, labels, and fake interface jargon
- Vague spacing and unextractable designs
- Lazy coded reinterpretations after image generation

**Your job is to break these defaults.**

## Required Workflow

> **For visual website tasks, you MUST generate design images FIRST, then analyze them, then implement.**

Never skip image generation when it's available. Never begin with freeform coding.

### Step 1: Generate Design Images

Create fresh, standalone images for each section or detail view. Do not:

- Use tiny compressed mood boards
- Crop old images
- Generate one image for multiple unrelated sections
- Under-generate (too few images for too many sections)

Do:

- Generate large, readable, section-specific images
- Create separate images for hero, features, testimonials, pricing, etc.
- Ensure designs look good on small laptop viewports (1280×800 minimum)
- Keep heroes clean, spacious, and uncluttered
- Use readable typography in generated images

### Step 2: Deep Analysis

Before coding, thoroughly analyze each generated image:

- Identify exact color palette and hex values
- Map typography: fonts, sizes, weights, line-heights
- Note spacing, padding, and margins
- Break down layout grids and component structures
- Extract specific measurements and proportions
- Identify interaction states and hover effects

### Step 3: Implementation

Implement the frontend to match the analyzed design as closely as possible:

- Use the exact colors from the image
- Match typography specifications precisely
- Follow the original spacing and layout
- Preserve the visual hierarchy
- Ensure responsive behavior mirrors the design intent
- Keep code clean and maintainable

## Quality Standards

Your output must feel:

- **Premium** — elevated, not generic
- **Art-directed** — intentional visual decisions
- **Readable** — text hierarchy is clear and accessible
- **Structured** — logical layout and component organization
- **Implementation-friendly** — code maps cleanly to design
- **Clean on first view** — not overwhelming
- **Responsive** — works well on small laptops and up

## What to Avoid

- Cards inside cards inside cards
- Excessive container nesting
- Overused section styling patterns
- Too much visible information at once
- Tiny UI elements that are hard to implement
- Vague or generic spacing
- Designs that look nice but can't be extracted

## What to Prefer

- Single-purpose, clearly defined components
- Generous whitespace and breathing room
- Strong typography hierarchy
- Distinct section identities
- Realistic, implementable designs
- Section-specific design images
- Clean hero sections with clear CTAs