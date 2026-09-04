# 00 — Context: Phase 1 Frontend Is Already Built

Read this first. It is not a task — it orients you before you run `01-mock-api-layer.md`.

## What exists

`apps/web` is a working Next.js 14 App Router + TypeScript + Tailwind app. It
implements every P0 screen from `docs/RAYGO_Claude_Frontend_First_Implementation_PRD.md`
section 4, plus the P1 Products/Orders/Payments screens, all reading from
`apps/web/src/data/fixtures/demo-scenario.ts`.

Verified: `npm run build` compiles all 20 routes with zero type errors.

Structure:

```text
apps/web/src/
  app/                  one folder per route, matches PRD section 8 exactly
  components/
    app-shell/          Sidebar, Topbar, AppShell wrapper
    shared/primitives.tsx   GlassPanel, SolidPanel, KpiCard, StatusBadge, PageHeader
  data/fixtures/
    types.ts             domain types
    demo-scenario.ts      the actual mock dataset (PRD section 9)
  lib/
    formatters.ts         formatINR, formatPct, formatCompactDate
    routes.ts              typed route builders + sidebar nav config
```

Design tokens (`tailwind.config.ts`, `globals.css`) are copied verbatim from
the Stitch export's `DESIGN.md` and `code.html` files, including the glass
tokens from PRD section 6. Do not redefine or rename these tokens in later
phases — extend them if needed.

## What is intentionally not built yet

- No `lib/api-client.ts` — screens import fixture data directly.
- No backend (`apps/api` is an empty stub folder).
- No real Razorpay integration — `/checkout` simulates the flow client-side
  with a `setTimeout` state machine and a "simulate failure" button for demo
  purposes.
- No Ask RAYGO command palette (PRD section 10.18) — sidebar button and
  topbar search input are present but inert.
- No toasts/skeleton loading states beyond the two ad-hoc ones already in
  `products/page.tsx` and `ai-commerce/page.tsx`.
- No tests.

## Conventions to preserve going forward

- Components own rendering/interaction state only; business rules belong in
  services once the backend exists (PRD section 5, "Frontend ownership").
- Currency is always formatted with `formatINR` from `lib/formatters.ts` —
  never inline `₹` string concatenation.
- Route strings are always built from `lib/routes.ts`, never hand-written.
- Status colors go through `<StatusBadge status="..." />` in
  `components/shared/primitives.tsx` — extend `statusStyles` there rather
  than adding one-off color classes.
- Glass surfaces (`GlassPanel` / `.glass-surface`) are reserved for: topbar,
  sidebar overlay, KPI cards, reasoning panels, drawers, payment status
  cards, AI Buyer recommendation card, approval/policy panels — per PRD
  section 6. Tables, forms, and audit rows stay solid (`SolidPanel`).

Now proceed to `01-mock-api-layer.md`.
