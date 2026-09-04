# 01 — Build the Mock API Abstraction Layer

## Goal

Every screen in `apps/web/src/app/**` currently imports mock data directly
from `data/fixtures/demo-scenario.ts`. Before wiring a real backend, extract
that data behind a typed API client so screens call functions like
`getOverview()` / `getOpportunity(id)` instead of importing fixtures. This is
the seam phase 2's FastAPI backend will slot into later without touching any
screen component.

## Requirements

1. Create `apps/web/src/lib/api-client.ts` exporting one async function per
   endpoint in PRD section 13 ("API Contract"), e.g.:
   - `getMerchant()`
   - `initializeOnboarding(payload)`
   - `getDashboardOverview()`
   - `getOpportunities()`, `getOpportunity(id)`, `approveOpportunity(id)`
   - `getExperiments()`, `getExperiment(id)`, `scaleExperiment(id)`
   - `getAiCommerceReadiness()`, `getProductProfile(productId)`,
     `optimizeCatalog()`
   - `searchAiBuyer(query)`, `addToBasket(items)`, `createOrderIntent(...)`,
     `getOrderIntent(id)`
   - `createRazorpayOrder(orderIntentId)`, `verifyRazorpayPayment(...)`,
     `recordRazorpayFailure(...)`, `getPayments()`, `getOrders()`
   - `getPolicies()`, `updatePolicy(id, patch)`, `evaluatePolicy(payload)`
   - `getAgentStatus()`, `getAgentActivity()`
   - `getAuditTrail()`, `getAuditEvent(id)`

2. Each function's return type must match a Zod schema (add `zod` schemas in
   `apps/web/src/lib/schemas.ts`, one per response shape, derived from the
   types already in `data/fixtures/types.ts`). Parse every response through
   its schema before returning — this is where PRD section 5's "Zod for API
   schema validation" requirement is satisfied.

3. For now, every function's implementation reads from
   `data/fixtures/demo-scenario.ts` and resolves after a small artificial
   delay (150–400ms) to simulate network latency and let loading states be
   exercised. Mutating calls (`approveOpportunity`, `updatePolicy`, etc.)
   should mutate an in-memory copy of the fixture data for the session so the
   UI reflects the change without a real backend.

4. Add `NEXT_PUBLIC_API_BASE_URL` awareness: if that env var is set, the
   client should be structured so a future phase can swap the mock
   implementation for real `fetch(...)` calls behind the same function
   signatures with minimal diff (e.g. one `USE_MOCK` flag or a swappable
   adapter — your call on the exact mechanism, but the function signatures in
   step 1 must not change).

5. Update every screen under `apps/web/src/app/**` to call the new
   `api-client.ts` functions (via `useEffect`/`useState`, or TanStack Query,
   your choice — `@tanstack/react-query` is already installed) instead of
   importing fixtures directly. Show a loading state (skeleton or spinner)
   while the call is pending, and wire the PRD's documented empty/error copy
   where section 10 specifies it (e.g. overview's `Analyzing commerce
   signals...` loading state and `RAYGO has not identified a high-confidence
   opportunity yet.` empty state).

6. Keep `data/fixtures/demo-scenario.ts` as the single source of truth for
   the actual data — the API client wraps it, it doesn't duplicate it.

## Acceptance criteria

- `npm run build` in `apps/web` still compiles with zero errors.
- No screen component under `app/**` imports from `data/fixtures/*` directly
  anymore — only `lib/api-client.ts` does.
- Every mutating action (approve opportunity, scale experiment, update
  policy, optimize catalog) visibly updates the UI without a page reload.
- Loading states are visible on slow-motion network throttling in devtools.
