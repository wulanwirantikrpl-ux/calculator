---
name: Networking Vocational Learning System
colors:
  surface: '#f7f9ff'
  surface-dim: '#d7dae0'
  surface-bright: '#f7f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f1f4fa'
  surface-container: '#ebeef4'
  surface-container-high: '#e5e8ee'
  surface-container-highest: '#dfe3e8'
  on-surface: '#181c20'
  on-surface-variant: '#414754'
  inverse-surface: '#2d3135'
  inverse-on-surface: '#eef1f7'
  outline: '#727785'
  outline-variant: '#c1c6d6'
  surface-tint: '#005bc0'
  primary: '#005bbf'
  on-primary: '#ffffff'
  primary-container: '#1a73e8'
  on-primary-container: '#ffffff'
  inverse-primary: '#adc7ff'
  secondary: '#006e2a'
  on-secondary: '#ffffff'
  secondary-container: '#8ffa9b'
  on-secondary-container: '#00752d'
  tertiary: '#835100'
  on-tertiary: '#ffffff'
  tertiary-container: '#a56700'
  on-tertiary-container: '#fffbff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d8e2ff'
  primary-fixed-dim: '#adc7ff'
  on-primary-fixed: '#001a41'
  on-primary-fixed-variant: '#004493'
  secondary-fixed: '#8ffa9b'
  secondary-fixed-dim: '#73dc82'
  on-secondary-fixed: '#002108'
  on-secondary-fixed-variant: '#00531e'
  tertiary-fixed: '#ffddb9'
  tertiary-fixed-dim: '#ffb962'
  on-tertiary-fixed: '#2b1700'
  on-tertiary-fixed-variant: '#663e00'
  background: '#f7f9ff'
  on-background: '#181c20'
  surface-variant: '#dfe3e8'
typography:
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
  headline-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 26px
    fontWeight: '600'
    lineHeight: 34px
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  title-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-code-lg:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
  label-code-md:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
  label-ui:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-desktop: 1.5rem
  margin: 1rem
  margin-desktop: 2rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
---

## Brand & Style
The design system serves vocational technology students, instructors, and lab administrators in active networking classrooms. The visual tone is structured, objective, and highly utilitarian, borrowing from Google’s clean Material and educational product aesthetics (e.g., Classroom, Cloud Console). 

The emotional response should be one of calm clarity, pedagogical reassurance, and technical precision. Complex computational tasks—such as IPv4/IPv6 subnetting, packet inspection, routing table management, and topology mapping—are broken down into digestible, scannable steps.

The aesthetic philosophy centers on modern, structured minimalism:
- **Surface Simplicity:** Crisp white canvases with subtle, cool-tinted neutral surface tiers.
- **Action Hierarchy:** Vibrant single-focus accents (Google Blue) directing active learning tasks and primary inputs.
- **Technical Rigor:** Strict monospaced treatment for network addresses and configuration blocks paired with balanced, human-friendly sans-serif typography for pedagogical guidance.

## Colors
The palette leverages a high-clarity, high-legibility light mode structure tailored for classroom projectors, Chromebooks, lab workstations, and tablets under varied lighting environments.

### Core Functional Palette
- **Primary (`#1a73e8`):** Instructional callouts, primary action buttons, active tab states, and selected topology nodes. Hover state transitions to `#1557b0`.
- **Secondary / Success (`#1e8e3e`):** Ping successes, correct packet checksums, validated subnet configurations, and active link states.
- **Warning (`#f29900`):** Broadcast domain collisions, MTU mismatches, dynamic route recalculations, and impending lab timeouts.
- **Alert / Error (`#d93025`):** Invalid IP octets, packet drops, port administrative downs, and diagnostic failures.

### Neutral Tiering & Surfaces
- **Base Canvas:** `#ffffff` for primary document, lab sheet, and card backgrounds.
- **Surface Level 1:** `#f8f9fa` for workspace canvas, toolbars, and inactive panels.
- **Surface Level 2:** `#f1f3f4` for code snippets, segmented controls, badge backings, and disabled states.
- **Structural Outlines:** `#dadce0` for container borders, grid divisions, and non-focused form fields.
- **Text & Semantics:** Primary text uses `#202124` for maximum WCAG AAA legibility; secondary metadata and helper instructions use `#5f6368`.

## Typography
The system balances human-centered educational clarity with strict engineering documentation standards.

- **Headlines & Structural Sectioning (`Plus Jakarta Sans`):** Selected for its geometric structure, high x-height, and contemporary Google-adjacent friendly authority.
- **Narrative & Instructions (`Inter`):** Applied to instructional text, lab assignments, tutorials, and form labels. Highly optimized for screen readability across varying pixel densities.
- **Technical & Addressing Monospace (`JetBrains Mono`):** Dedicated to technical networking strings: IPv4 octets, IPv6 hextets, CIDR masks, MAC addresses, binary conversions, CLI terminal commands, and packet hex dumps. Non-proportional character widths align values cleanly in tables and diagrams.

## Layout & Spacing
The layout relies on a dynamic, responsive 12-column fluid grid system pinned to an 8px base rhythm (with 4px micro-increments for compact data displays).

### Responsive Adaptation
- **Desktop (1024px+):** 12-column grid, `margin-desktop` (2rem / 32px), `gutter-desktop` (1.5rem / 24px). Split-view workspace: 60% dynamic canvas/topology view, 40% interactive lab console, inspector, or step-by-step documentation panel.
- **Tablet (768px – 1023px):** 8-column layout, 1.5rem margin, 1rem gutter. Topology canvas stacks above inspector panes or shifts to a collapsible side-sheet.
- **Mobile (<768px):** 4-column layout, `margin` (1rem / 16px), `gutter` (1rem / 16px). Full-bleed cards, tabbed viewports switching between interactive diagram and addressing controls. Touch targets enforce a minimum 48px hit area.

## Elevation & Depth
In line with clean Google-inspired minimalism, visual hierarchy avoids heavy, dark dropshadows. Depth is established through **tonal layering combined with low-contrast structural borders**.

- **Level 0 (Canvas Base):** `#f8f9fa` fills the background viewport.
- **Level 1 (Card & Module Layer):** `#ffffff` elevated via a 1px solid `#dadce0` border. Zero shadow when at rest; clean visual boundary.
- **Level 2 (Interactive Floating / Active Hover):** `0px 1px 3px rgba(60, 64, 67, 0.12), 0px 4px 8px rgba(60, 64, 67, 0.06)`, retaining the 1px solid border. Used for draggable subnet cards, active topology node selections, and floating toolbars.
- **Level 3 (Modal / Palette Overlays):** `0px 8px 24px rgba(60, 64, 67, 0.15), 0px 4px 8px rgba(60, 64, 67, 0.08)`, applied to IP configuration modals, routing table inspectors, and packet capture flyouts.

## Shapes
The shape language uses moderate roundedness (Level 2) to maintain a modern, friendly educational atmosphere without compromising density.

- **Base Radius (0.5rem / 8px):** Standard buttons, input fields, dropdown trigger targets, terminal code blocks, and table containers.
- **Medium/Large Containers (0.75rem – 1rem / 12px – 16px):** Lab exercise cards, simulation viewports, diagnostic inspector panels, and dialog surfaces.
- **Pill-Shaped (9999px):** Status chips, port status indicators (e.g., `Fa0/1: UP`), filter tags, and primary step-counter badges.

## Components

### Buttons
- **Primary:** Background `#1a73e8`, text `#ffffff`, border radius `8px`, height `40px` (desktop) / `48px` (touch). Hover shifts to `#1557b0`. No outline. Focus state displays a 2px outer ring `#1a73e8` offset by 2px white.
- **Secondary / Outlined:** Background `#ffffff`, border `1px solid #dadce0`, text `#1a73e8`. Hover fills with `#f8f9fa` and darkens border to `#1a73e8`.
- **Text / Flat:** Background transparent, text `#1a73e8`. Hover background `#f1f3f4`.

### Input Fields & Address Blocks
- **IP / Subnet Mask Field:** Set in `JetBrains Mono`. Container background `#ffffff`, border `1px solid #dadce0`, inner padding `8px 12px`. Focus state shifts border to `2px solid #1a73e8` (taking up 1px of padding to prevent layout shift).
- **Error State:** Border becomes `1px solid #d93025` accompanied by an inline micro-caption in red detailing invalid CIDR bounds or octet overflows (>255).

### Cards & Lab Panels
- Structured with `#ffffff` fill and `1px solid #dadce0` border, curved at `12px` or `16px`.
- Card headers feature subtle border-bottom dividers (`1px solid #f1f3f4`), separating module metadata, step progress, and verification indicators from actionable controls.

### Chips & Protocol Badges
- Compact indicators (height `24px` to `28px`, full pill radius).
- Background `#f1f3f4`, text `#3c4043` (`Inter 12px, font-weight 500`).
- State-specific variants: Green tint (`#e6f4ea`, text `#137333`) for active connections; Red tint (`#fce8e6`, text `#c5221f`) for downed interfaces; Blue tint (`#e8f0fe`, text `#1967d2`) for protocol tagging (e.g., `OSPF`, `BGP`, `VLAN 10`).

### Checkboxes & Radios
- Size `18px x 18px`, rounded corners (`4px` for checkboxes, `50%` for radios).
- Inactive state: `2px solid #5f6368` outline with white center.
- Active state: `#1a73e8` fill with crisp white checkmark or center pip. Focus ring provides high-contrast keyboard accessibility.

### Tab Bars & Segmented Controls
- **Tab Bars:** Flat baseline with an active 3px horizontal bar in `#1a73e8` placed directly below the active tab label. Text changes from `#5f6368` (inactive) to `#1a73e8` (active, medium weight).
- **Segmented Lab Switcher:** `#f1f3f4` container with 4px padding. Selected view indicator is a `#ffffff` card with subtle `0px 1px 2px rgba(60,64,67,0.15)` shadow and 6px border radius.

### Additional Vocational Networking Components
- **CLI Terminal Box:** Embedded container featuring `#202124` dark background, `#ffffff` font, using `JetBrains Mono` at `13px` with line numbering in `#80868b`.
- **Octet Bit-Weight Strip:** An interactive visual breakdown widget for subnet teaching, displaying 8-bit boxes (`128 | 64 | 32 | 16 | 8 | 4 | 2 | 1`) toggling binary 1/0 states dynamically with instant decimal calculation feedback.