---
name: design-taste-frontend-v1
description: The original v1 taste-skill, preserved for projects depending on its exact behavior. The current default is `design-taste-frontend` (v2 experimental), which is a substantial rewrite. Use this v1 install name only if you need exact backward compatibility.
---

# High-Agency Frontend Skill

## 1. Active Baseline Configuration

| Parameter | Value | Scale |
|-----------|-------|-------|
| `DESIGN_VARIANCE` | 8 | 1 = Perfect Symmetry, 10 = Artsy Chaos |
| `MOTION_INTENSITY` | 6 | 1 = Static, 10 = Cinematic/Magic Physics |
| `VISUAL_DENSITY` | 4 | 1 = Art Gallery/Airy, 10 = Pilot Cockpit/Packed Data |

**AI Instruction:** These values (8, 6, 4) form the strict default baseline for all generations. Do not prompt the user to edit this file. Always listen to the user: adapt these values dynamically based on explicit requests in their chat prompts. Use these baseline values (or user-overridden values) as global variables to drive the logic in Sections 3 through 7.

## 2. Default Architecture & Conventions

Adhere to these structural constraints by default unless the user explicitly specifies otherwise.

### 2.1 Dependency Verification [MANDATORY]

Before importing ANY third-party library (e.g., `framer-motion`, `lucide-react`, `zustand`), you MUST check `package.json`.

- **Missing package?** Output the installation command (e.g., `npm install package-name`) BEFORE providing the code.
- **Never** assume a library exists in the project.

### 2.2 Framework & Interactivity

- **Default stack:** React or Next.js
- **Default rendering:** Server Components (RSC)

#### RSC Safety Rules

- **Global state** works ONLY in Client Components.
- In Next.js, wrap providers in a `"use client"` component.
- **Interactivity Isolation:** If Sections 4 or 7 (Motion/Liquid Glass) are active, extract the specific interactive UI component as an isolated leaf component with `'use client'` at the very top.
- **Server Components** must exclusively render static layouts.

### 2.3 State Management

| Scope | Solution |
|-------|----------|
| Isolated UI | `useState` / `useReducer` |
| Deep prop-drilling avoidance | Global state (Zustand, Context, etc.) |

### 2.4 Styling Policy

- **Primary:** Tailwind CSS (v3/v4) for ~90% of styling

#### Tailwind Version Lock

1. Check `package.json` to determine the installed version.
2. **v3 projects:** Do NOT use v4 syntax (e.g., `@apply` with CSS variables, `@theme` blocks).
3. **v4 projects:** Do NOT use `tailwindcss` plugin in `postcss.config.js`. Use `@tailwindcss/postcss` or the Vite plugin instead.

### 2.5 Anti-Emoji Policy [CRITICAL]

**NEVER use emojis in:**
- Code (variable names, comments)
- Markup (JSX/HTML content)
- Text content (labels, messages, tooltips)
- Alt text (for images, icons)

**Replace emoji with:**
- **Icons:** `lucide-react` or `react-feather` components
- **Decorative elements:** SVG shapes, Tailwind utility classes
- **Text labels:** Descriptive words in plain text

### 2.6 File Naming Conventions

- **Components:** PascalCase (e.g., `UserProfile.tsx`)
- **Utilities/hooks:** camelCase (e.g., `useAuth.ts`)
- **Config files:** kebab-case (e.g., `postcss.config.js`)
- **Pages (Next.js):** kebab-case (e.g., `about-us.tsx`)

### 2.7 Code Style

- Use **TypeScript** for type safety
- Prefer **functional components** with hooks
- Use **named exports** for utilities, **default exports** for components
- Keep functions under 50 lines; extract logic into custom hooks

## 3. Component Architecture

### 3.1 Component Hierarchy

src/
├── components/
│   ├── ui/          # Primitive components (Button, Input, Card)
│   ├── features/    # Feature-specific components
│   └── layouts/     # Layout components (Header, Footer, Sidebar)
├── hooks/           # Custom React hooks
├── lib/             # Utility functions
├── types/           # TypeScript type definitions
└── styles/          # Global styles (if needed)
### 3.2 Component Guidelines

- Components should be **self-contained** and **reusable**
- Extract props into a dedicated `types.ts` file when a component has 5+ props
- Use composition over inheritance
- Keep presentation and logic separate

## 4. Motion & Animation

When `MOTION_INTENSITY` > 5, apply the following:

### 4.1 Animation Library

- **Default:** `framer-motion` for declarative animations
- **Fallback:** CSS transitions for simple hover states

### 4.2 Motion Principles

- **Purpose:** Animation should communicate state changes, not just decorate
- **Timing:** Use `ease-out` for entrances, `ease-in` for exits
- **Duration:** 150-300ms for micro-interactions, 400-600ms for page transitions
- **Stagger:** 50-100ms between list items

### 4.3 Reduced Motion

Always respect `prefers-reduced-motion`:

tsx
const reducedMotion = useReducedMotion();

<div
  animate={reducedMotion ? {} : { opacity: 1, y: 0 }}
  initial={{ opacity: 0, y: 20 }}
>
  Content
</div>
## 5. Accessibility (A11y)

### 5.1 Mandatory A11y Rules

- All interactive elements must have **focus indicators**
- Use semantic HTML (`<button>`, `<nav>`, `<main>`, etc.)
- Ensure **color contrast** meets WCAG AA (4.5:1 for text)
- All images must have **alt text** (even empty `alt=""` for decorative images)

### 5.2 Keyboard Navigation

- Logical tab order via semantic HTML structure
- Skip-to-content links for long pages
- Escape key closes modals/dropdowns

### 5.3 ARIA Guidelines

- Use `aria-label` when visual context is insufficient
- Use `aria-live` regions for dynamic content updates
- Use `role` attributes sparingly—semantic HTML is preferred

## 6. Responsive Design

### 6.1 Breakpoints (Tailwind)

| Name | Min Width | Use Case |
|------|-----------|----------|
| `sm` | 640px | Large phones |
| `md` | 768px | Tablets |
| `lg` | 1024px | Laptops |
| `xl` | 1280px | Desktops |
| `2xl` | 1536px | Large screens |

### 6.2 Mobile-First Approach

- Start with mobile styles, then add `md:`, `lg:`, etc.
- Test on smallest target device first
- Avoid horizontal scroll at all breakpoints

## 7. Performance

### 7.1 Bundle Optimization

- **Tree-shake unused code** by using named imports
- **Lazy load** components with `React.lazy()` and `Suspense`
- **Dynamic imports** for heavy libraries (charts, rich text editors)

### 7.2 Image Optimization

- Use `next/image` in Next.js for automatic optimization
- Specify `width` and `height` to prevent layout shift
- Use WebP/AVIF formats when possible
- Implement `loading="lazy"` for below-the-fold images

### 7.3 Rendering Optimization

- **Memoize** expensive computations with `useMemo`
- **Prevent unnecessary re-renders** with `React.memo` and `useCallback`
- **Virtualize** long lists with `react-window` or `tanstackirtual`

## 8. Error Handling & Edge Cases

### 8.1 Required Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty state | Show placeholder UI with clear call-to-action |
| Loading state | Show skeleton or spinner (never layout shift) |
| Error state | Show user-friendly message, log error for debugging |
| Network failure | Show retry button, cache data for offline resilience |
| No results | Show "no results" message with suggestions |

### 8.2 Form Validation

- Validate on blur AND on submit
- Show inline error messages below inputs
- Disable submit until form is valid
- Clear errors when user starts correcting

---

## Quick Reference: Always Do / Never Do

### ✅ Always

- Check `package.json` before importing libraries
- Use Tailwind for styling (respect version)
- Use semantic HTML elements
- Provide `alt` text for images
- Respect `prefers-reduced-motion`
- Extract interactive components to `"use client"` when using RSC

### ❌ Never

- Use emojis in any code, markup, or content
- Assume a library is installed
- Mix Tailwind v3/v4 syntax
- Use `var` instead of `let`/`const`
- Leave `console.log` in production code
- Create unstyled components with inline styles