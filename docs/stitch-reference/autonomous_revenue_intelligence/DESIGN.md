---
name: Autonomous Revenue Intelligence
colors:
  surface: '#fcf8fa'
  surface-dim: '#dcd9db'
  surface-bright: '#fcf8fa'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f6f3f5'
  surface-container: '#f0edef'
  surface-container-high: '#eae7e9'
  surface-container-highest: '#e4e2e4'
  on-surface: '#1b1b1d'
  on-surface-variant: '#45464d'
  inverse-surface: '#303032'
  inverse-on-surface: '#f3f0f2'
  outline: '#76777d'
  outline-variant: '#c6c6cd'
  surface-tint: '#565e74'
  primary: '#000000'
  on-primary: '#ffffff'
  primary-container: '#131b2e'
  on-primary-container: '#7c839b'
  inverse-primary: '#bec6e0'
  secondary: '#b61722'
  on-secondary: '#ffffff'
  secondary-container: '#da3437'
  on-secondary-container: '#fffbff'
  tertiary: '#000000'
  on-tertiary: '#ffffff'
  tertiary-container: '#271901'
  on-tertiary-container: '#98805d'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dae2fd'
  primary-fixed-dim: '#bec6e0'
  on-primary-fixed: '#131b2e'
  on-primary-fixed-variant: '#3f465c'
  secondary-fixed: '#ffdad7'
  secondary-fixed-dim: '#ffb3ad'
  on-secondary-fixed: '#410004'
  on-secondary-fixed-variant: '#930013'
  tertiary-fixed: '#fcdeb5'
  tertiary-fixed-dim: '#dec29a'
  on-tertiary-fixed: '#271901'
  on-tertiary-fixed-variant: '#574425'
  background: '#fcf8fa'
  on-background: '#1b1b1d'
  surface-variant: '#e4e2e4'
  growth-green: '#10B981'
  warning-amber: '#F59E0B'
  reasoning-blue: '#3B82F6'
  surface-muted: '#F8FAFC'
  border-subtle: '#E2E8F0'
typography:
  metric-display:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 28px
  body-base:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
  label-bold:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.01em
  data-mono:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 18px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  container-max: 1440px
  gutter: 1.5rem
  margin-mobile: 1rem
  stack-compact: 0.5rem
  stack-default: 1rem
  section-gap: 2rem
---

## Brand & Style

The design system is engineered for the high-stakes environment of autonomous revenue operations. It moves away from the whimsical aesthetics often associated with AI to establish a brand personality rooted in **Professionalism, Transparency, and Precision.** The UI treats AI as a dependable financial operator, positioning intelligence as an objective tool rather than a novelty.

The visual direction follows a **Corporate / Modern** style with a focus on functional clarity. By utilizing a "Restrained Light-First" approach, the system prioritizes readability and cognitive ease, ensuring that revenue leaders can interpret complex data-dense tables and AI-driven reasoning at a glance. The aesthetic is "Production-Grade," favoring crisp lines, high-contrast typography, and purposeful whitespace over decorative trends. Every pixel is intended to foster trust and facilitate rapid decision-making in a fintech context.

## Colors

The palette is intentionally restrained to maintain an authoritative fintech environment. 

- **Primary Navy (#0F172A):** Utilized for the core structural elements—navigation sidebars, primary typography, and heavy-weight headers. It provides a stable, grounding anchor for the platform.
- **Accent Red (#EF4444):** Used with extreme surgical precision. It is reserved for high-impact primary actions (e.g., "Execute Recovery") and critical error states.
- **Semantic Logic:**
    - **Green (#10B981):** Represents revenue growth, success states, and positive health indicators.
    - **Amber (#F59E0B):** Signifies "Approvals Required" or pending policy checks.
    - **Blue (#3B82F6):** Reserved exclusively for **AI Reasoning**. Whenever the system explains "why" a decision was made, this blue is used as the cognitive signifier.
- **Neutral Backgrounds:** The background uses a crisp white, while `surface-muted` (#F8FAFC) differentiates secondary panels or table headers.

## Typography

This design system leverages **Inter** for its unparalleled legibility and neutral, utilitarian character. The typography system is optimized for "Data Density," where large volumes of information must be parsed quickly.

- **Metric Display:** Specifically for hero revenue numbers (e.g., ₹2,84,620). It uses semi-bold weights and tight tracking for high impact without being decorative.
- **Data-Mono Styling:** While Inter is a sans-serif, it is configured with tabular num (tnum) and lining figures (lnum) for all numeric data. This ensures that columns of numbers in tables align perfectly for easier visual scanning.
- **AI Reasoning Text:** Body text within reasoning blocks uses `body-base` with generous line-height to ensure the "Explain before Execute" logic is easy to digest.
- **Mobile Scale:** On mobile devices, `metric-display` should scale down to 24px to prevent horizontal overflow in dashboard cards.

## Layout & Spacing

The layout is built on a **12-column fluid grid** for desktop, optimized for a 1440px maximum container width. 

- **Density:** The system prioritizes a "Compact but Readable" density. Table rows are tight (40px-48px height) to maximize information on screen, while section gaps are kept at `2rem` to prevent visual clutter.
- **The Sidebar:** On desktop, the primary navigation is a persistent 240px sidebar. On tablet and mobile, this collapses into a drawer or bottom navigation to maximize space for data tables.
- **Responsive Behavior:** 
    - **Desktop (1024px+):** 12 columns, full sidebar.
    - **Tablet (768px - 1023px):** 8 columns, sidebar collapses to icons.
    - **Mobile (<768px):** 4 columns. Tables reflow into "Data Cards" to ensure numeric readability.
- **The Detail Drawer:** A standard 480px right-aligned drawer is used for deep-dives (e.g., Opportunity Details or Audit Trails), allowing the user to view granular data without losing their position on the main dashboard.

## Elevation & Depth

Hierarchy is established through **Tonal Layers** and **Low-Contrast Outlines** rather than dramatic shadows. This maintains the professional, flat aesthetic required for a fintech tool.

- **The Surface System:**
    - **Level 0 (Background):** White (#FFFFFF).
    - **Level 1 (Card/Section):** A 1px border (#E2E8F0) with no shadow. 
    - **Level 2 (Interactive/Focus):** A subtle, ultra-diffused shadow (0px 4px 12px rgba(15, 23, 42, 0.05)) is applied only when an element is hovered or active.
- **Overlays:** Right-side drawers and modals use a soft backdrop dim (rgba(15, 23, 42, 0.4)) to isolate the "Audit Trail" or "Reasoning Timeline" from the background data.
- **AI Reasoning Layers:** AI-generated content is often placed on a light blue-tinted surface (Primary Blue at 5% opacity) to visually separate machine logic from standard system data.

## Shapes

The shape language is **Crisp and Professional.** 

- **Base Radius:** A standard 4px (`0.25rem`) radius is applied to buttons, input fields, and small UI components. This provides a "sharp" fintech feel that communicates precision.
- **Large Radius:** Larger cards or modal containers may use an 8px (`rounded-lg`) radius to slightly soften the layout without appearing informal.
- **Pills:** Status badges (e.g., "Ready," "Blocked," "Active") use a fully rounded "pill" shape to distinguish them clearly from interactive buttons or input fields.

## Components

### Buttons
- **Primary:** Deep Navy (#0F172A) background with White text. 4px radius.
- **Critical Action:** Accent Red (#EF4444) background. Used only for final execution steps.
- **Ghost:** Transparent background with Navy border. Used for secondary navigation or "Cancel" actions.

### Data Tables
- **Styling:** Header background is `surface-muted`. Rows have a subtle bottom border (#E2E8F0).
- **Cells:** Numeric cells use `data-mono` for vertical alignment. High-contrast dividers are used between critical data points in the "Revenue Action Firewall."

### Status Badges
- Used to indicate health. Each badge must include a Lucide icon and a label (e.g., a green `TrendingUp` icon for "Growth"). 
- Backgrounds are 10% opacity of the semantic color with 100% opacity text.

### Reasoning Timeline
- A specialized vertical component that uses `reasoning-blue` for the line and icon accents. It displays AI logic steps chronologically.

### Input Fields
- Flat styling with a 1px border. Focus state uses a 1px Navy border and a subtle 2px glow of the same color at 10% opacity.

### Icons
- **Style:** 20px Lucide-style line icons.
- **Stroke Weight:** 1.5px to 2px for clarity on high-density screens.
- **Constraint:** No emojis. Icons are purely functional (e.g., `ShieldCheck` for Policy, `Bot` for AI Reasoning).