# 05 — Polish, Command Palette, and Demo Hardening

## Goal

Close out the P1 backlog and deploy, per PRD sections 4 (P1 list) and 5
(Deployment).

## Requirements

1. **Ask RAYGO command palette** (PRD section 10.18): build a real
   `CommandPalette` component, triggered from the sidebar "Ask RAYGO" button
   and the topbar search input, both already present but inert in
   `components/app-shell/sidebar.tsx` / `topbar.tsx`. Support at minimum the
   five suggested commands from the PRD ("Why did revenue change
   yesterday?", "Show my highest-value opportunities.", "Which experiment
   should I scale?", "Why is AI Commerce readiness 82?", "Show blocked
   actions."). Each selected command returns a concise answer plus a link to
   the relevant route — no persistent chat history for MVP.

2. **Shared component completeness**: cross-check PRD section 11's component
   list against what exists in `apps/web/src/components/`. Fill gaps —
   notably `Toast`, `Modal`/`Drawer` as reusable primitives (currently
   inlined per-screen with Framer Motion in opportunity/experiment detail
   and audit trail), `EmptyState`, `LoadingState`, `ErrorState`, and a
   reusable `DataTable` (currently each table is hand-rolled per screen).
   Refactor existing screens to use the shared versions rather than
   maintaining duplicate table/modal markup.

3. **States coverage**: every screen listed in PRD section 10 with an
   explicit loading/empty/error copy (onboarding, overview, others as
   specified) must actually render that state under the right condition,
   not just the happy path. Use the `LoadingState`/`EmptyState`/`ErrorState`
   components from step 2.

4. **End-to-end demo test**: write a Playwright (or similar) test that walks
   the full judge-demo path: onboarding → overview → opportunity detail →
   approve → experiment detail → scale → AI Commerce → AI Buyer → search →
   add to basket → checkout → payment (success path) → back to overview;
   plus a second test for the payment failure path → audit trail shows the
   blocked retry. Put this under `apps/web/src/test/` (or `apps/web/e2e/` if
   you prefer Playwright's convention — note the change in this file if so).

5. **Deploy**:
   - Frontend to Vercel, backend to Render, database to MongoDB Atlas, per
     PRD section 5.
   - Fill in `.env.example` at the root with every var actually required
     (cross-check against what phases 2–4 introduced beyond the current
     list) and confirm both `apps/web` and `apps/api` read from it
     consistently.
   - Confirm CORS (`FRONTEND_ORIGIN`) and Razorpay webhook URL are updated
     for the deployed domains, not just localhost.

6. **Demo script**: write `docs/demo-script.md` — a beat-by-beat walkthrough
   for a judge demo (which screens to show in which order, what to say at
   each beat, and where the "safe failure" moment happens), matching the
   path tested in step 4.

## Acceptance criteria

- Ask RAYGO responds to all five suggested commands with a real answer and a
  working link.
- No screen shows a broken/blank state when its documented loading, empty,
  or error condition is triggered.
- Both Playwright flows (success and failure) pass against the deployed
  environment, not just localhost.
- A judge can follow `docs/demo-script.md` against the deployed URLs start
  to finish without any step failing.
