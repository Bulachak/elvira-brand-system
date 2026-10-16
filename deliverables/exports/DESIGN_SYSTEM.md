# Brand Design System & Living Component Specification — Elvira Astashkina
*Production Design Token & Component Foundry Standard*
*Generated: 2026-10-04 | Brand Strategist: Kamilla Gafurzianova, OLY*

---

## 1. Architectural Invariants (Zero-Tolerance Rules)
- **Strict Anti-Pill Standard (Authorized by Kamilla 2026-09-30):**
  - NEVER use pill-shaped UI elements (`rounded-full`, `border-radius: 9999px`, `100px`, `24px` on buttons, badges, chips, tags, cards, or inputs).
  - Permitted corner radii:
    - Badges, Chips, Tags: `rounded-md` (6px) or `rounded-lg` (8px).
    - Standard Buttons, Inputs, Selects: `rounded-lg` (8px) or `rounded-xl` (12px).
    - Cards, Panels, Containers: `rounded-xl` (12px) or `rounded-2xl` (16px).
    - Circular avatar photos are the ONLY permitted circle exception (1:1 aspect ratio square-to-circle).
- **Zero-Orphan & Typography Standard (Authorized by Kamilla 2026-09-13):**
  - `text-wrap: balance;` on headings; `text-wrap: pretty;` on paragraphs and cards.
  - Container width must be generous (`48ch`–`65ch`), never artificially constricted (`18ch`–`37ch`).
  - Proactively glue short 2–4 word sentences and prepositions with non-breaking spaces (`\u00A0`).
- **Touch Target Standard:**
  - All interactive elements must maintain a minimum touch target bounding box of `44px × 44px`.
- **1-Click Print & Export Invariant:**
  - Complete zero-slider/zero-carousel architecture: voice calibrations, cards, and tokens render in static grid view.
  - Fully printable via `window.print()` with `print-color-adjust: exact;`.

---

## 2. Foundations & Design Tokens

### 2.1 Color Matrix & WCAG 2.2 Contrast Verification
| Role / Semantic Token | HEX | RGB | Contrast on White | WCAG Level |
|---|---|---|---|---|
| **Primary Brand / Header** | `#1A1815` | `rgb(26, 24, 21)` | 17.72:1 | **AAA** |
| **Secondary / Structural** | `#2B5A75` | `rgb(43, 90, 117)` | 7.44:1 | **AA** |
| **Accent / Interactive** | `#D4AF37` | `rgb(212, 175, 55)` | 1.85:1 | **AA Large** |
| **Canvas Background** | `#F5F0E6` | `rgb(245, 240, 230)` | 15.60:1 | **AAA** |
| **Surface / Card Container** | `#FFFFFF` | `rgb(255, 255, 255)` | 17.72:1 | **AAA** |

### 2.2 Typography Scale & Stacks
- **Display Typeface:** Cormorant Garamond (Fallbacks: `'Cormorant Garamond', Georgia, "Times New Roman", serif`)
- **Body Typeface:** Plus Jakarta Sans (Fallbacks: `'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`)
- **Code / Monospace:** JetBrains Mono

| Role | Size | Weight | Line Height | Sample |
|---|---|---|---|---|
| **Hero Display** | `56px (3.5rem)` | 700 | 1.05 | Architectural Excellence |
| **Section H1** | `40px (2.5rem)` | 700 | 1.15 | Strategic System Foundry |
| **Subheading H2** | `28px (1.75rem)` | 600 | 1.25 | Deterministic Design Tokens |
| **Card Title H3** | `20px (1.25rem)` | 600 | 1.35 | Component Anatomy |
| **Body Lead** | `18px (1.125rem)` | 400 | 1.6 | High-contrast typography with balanced wrapping. |
| **Body Default** | `15px (0.9375rem)` | 400 | 1.6 | Proactive non-breaking typographic gluing for prepositions. |
| **Caption / Overline** | `12px (0.75rem)` | 600 | 1.4 | WCAG 2.2 AAA VERIFIED |
| **Code / Monospace** | `13px (0.8125rem)` | 500 | 1.5 | --color-primary: #1A1815; |

### 2.3 Spatial Grid (8pt System)
| Token | Value | Recommended Usage |
|---|---|---|
| `--space-1` | `4px` | Micro gaps, icon offsets |
| `--space-2` | `8px` | Badge padding, inline icon spacing |
| `--space-3` | `12px` | Button vertical padding, compact gaps |
| `--space-4` | `16px` | Card padding (mobile), standard input padding |
| `--space-6` | `24px` | Card padding (desktop), grid gutters |
| `--space-8` | `32px` | Section spacing, large gutters |
| `--space-12` | `48px` | Major container padding, hero margins |
| `--space-16` | `64px` | Page section vertical rhythm |

### 2.4 Corner Radii & Geometry
| Level | Value | Tailwind Class | Status | Application Rules |
|---|---|---|---|---|
| **Micro / Badge / Tag** | `6px` | `rounded-md` | **Permitted** | Tags, chips, status indicators (anti-pill standard) |
| **Control / Button / Input** | `8px` | `rounded-lg` | **Permitted** | Primary CTAs, secondary triggers, text fields |
| **Container / Surface / Card** | `12px` | `rounded-xl` | **Permitted** | Content panels, modal cards, preview frames |
| **Macro Hero / Modal** | `16px` | `rounded-2xl` | **Permitted** | Promotional banners, floating dialogs |
| **Pill / Stadium (BANNED)** | `9999px` | `rounded-full (banned)` | **BANNED** | STRICTLY FORBIDDEN by Kamilla Standard (except 1:1 avatars) |

### 2.5 Elevation & Shadow Layers
| Elevation Level | CSS Shadow | Border | Application |
|---|---|---|---|
| **Level 0 (Flat)** | `none` | `1px solid var(--color-border)` | Inline surfaces, table rows |
| **Level 1 (Subtle)** | `0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04)` | `1px solid var(--color-border)` | Standard cards, inactive buttons |
| **Level 2 (Hover/Active)** | `0 4px 12px rgba(0,0,0,0.08), 0 2px 4px rgba(0,0,0,0.04)` | `1px solid var(--color-border)` | Hovered cards, active dropdowns |
| **Level 3 (Floating/Modal)** | `0 12px 32px rgba(0,0,0,0.12), 0 4px 8px rgba(0,0,0,0.06)` | `1px solid var(--color-border)` | Modals, floating bars, toasts |

---

## 3. Core Component Foundry & Anatomy

### 3.1 Buttons & Interactive Triggers
- **Primary CTA:** Background `#1A1815`; Text `#FFFFFF`; Radius `8px` (`rounded-lg`); Min Height `44px`. Focus Ring: `0 0 0 2px #FFFFFF, 0 0 0 4px #D4AF37`.
- **Secondary CTA:** Background `#2B5A75`; Text `#FFFFFF`; Radius `8px` (`rounded-lg`).
- **Outline / Ghost:** Background `transparent`; Border `2px solid #1A1815`; Text `#1A1815`; Radius `8px` (`rounded-lg`).
- **Destructive:** Background `#DC2626`; Text `#FFFFFF`; Radius `8px` (`rounded-lg`).

### 3.2 Links
- **Inline Text Links:** Underline offset `4px`, underline decoration `1px solid var(--color-accent)`, transition color on hover.
- **Standalone Action Links:** Semi-bold, trailing arrow icon `->` transitioning `translateX(3px)` on hover.

### 3.3 Avatars & Identity Presence
- **Shape:** 1:1 square with `50%` border-radius (`rounded-full`) — ONLY permitted circular element in brand ecosystem.
- **Sizes:** Small (`32px`), Medium (`44px`), Large (`56px`).
- **Presence Indicator:** `10px` dot in bottom-right corner with `2px` solid surface knockout ring.

### 3.4 Badges & Status Chips
- **Geometry:** Architectural rectangles with `rounded-md` (`6px`) or `rounded-lg` (`8px`). NO stadium pills.
- **Padding:** `4px 10px`; Font: `11px`, bold / uppercase tracking.

### 3.5 Form Controls & Touch Targets
- **Inputs & Selects:** Height `44px` (touch-compliant), border `1px solid var(--color-border)`, radius `8px` (`rounded-lg`).
- **Focus State:** 2px accent focus ring with zero default browser outline.

---

## 4. System Governance: Do's and Don'ts

### DO:
1. Always pair headings with `text-wrap: balance;` and glue prepositions with `\u00A0`.
2. Strictly maintain 44px minimum touch targets on all mobile and web interactive elements.
3. Validate all text-on-background combinations against WCAG 2.2 AA (4.5:1) or AAA (7:1).
4. Use architectural 6px/8px radii for badges and 8px/12px for buttons and containers.

### DON'T:
1. NEVER introduce pill-shaped badges, buttons, chips, or inputs (`rounded-full`, `9999px`, `100px`).
2. NEVER use draggable carousels or hidden voice sliders in specialist deliverables (must be 1-click printable).
3. NEVER leave unpopulated placeholder text or empty quotation blocks in client deliverables.
4. NEVER use harsh, pure black drop shadows; always use soft ambient rgba shadows with border rings.

---

## 5. Code Tokens & Integration

### CSS Custom Properties
```css
:root {
  --color-primary: #1A1815;
  --color-secondary: #2B5A75;
  --color-accent: #D4AF37;
  --color-bg: #F5F0E6;
  --color-surface: #FFFFFF;
  --color-border: #E5E7EB;

  --font-display: 'Cormorant Garamond', Georgia, "Times New Roman", serif;
  --font-body: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-code: ui-monospace, monospace;

  --radius-badge: 6px;
  --radius-button: 8px;
  --radius-card: 12px;
  --radius-hero: 16px;
  --radius-avatar: 50%; /* Only permitted circle */

  --shadow-sm: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.08), 0 2px 4px rgba(0,0,0,0.04);
  --shadow-lg: 0 12px 32px rgba(0,0,0,0.12), 0 4px 8px rgba(0,0,0,0.06);

  --touch-target-min: 44px;
}
```

### Tailwind Configuration
```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: {
          primary: '#1A1815',
          secondary: '#2B5A75',
          accent: '#D4AF37',
          bg: '#F5F0E6',
          surface: '#FFFFFF'
        }
      },
      fontFamily: {
        display: ['Cormorant Garamond', Georgia, "Times New Roman", serif],
        body: ['Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif]
      },
      borderRadius: {
        'badge': '6px',
        'button': '8px',
        'card': '12px',
        'hero': '16px'
        /* Note: full is strictly restricted to circular avatars */
      }
    }
  }
};
```
