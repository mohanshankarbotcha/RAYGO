# 02 — Build the FastAPI Backend

## Goal

Stand up `apps/api` as a real FastAPI service implementing the `/api/v1`
contract in `docs/RAYGO_Claude_Frontend_First_Implementation_PRD.md` section
13, backed by MongoDB, so `apps/web`'s `lib/api-client.ts` (built in
`01-mock-api-layer.md`) can be pointed at it instead of in-memory fixtures.

## Requirements

1. Scaffold per PRD section 5's "Detailed Folder Architecture":
   `apps/api/app/{main.py, core/{config.py,security.py},
   api/v1/{router.py,dashboard.py,opportunities.py,experiments.py,
   ai_commerce.py,ai_buyer.py,payments.py,policies.py,agents.py,audit.py},
   domain/{models.py,schemas.py,states.py}, services/, db/{mongo.py,seed.py},
   tests/}`. Use Pydantic schemas for every request/response body.

2. Implement every endpoint from PRD section 13 against MongoDB (via Motor or
   Beanie — your choice). Persist the entities in PRD section 12: Merchant,
   Product, Opportunity, Experiment, Policy, PolicyEvaluation, Approval,
   AgentRun, AuditEvent, BuyerIntent, Cart, OrderIntent, RazorpayOrder,
   PaymentAttempt, WebhookEvent — every document gets `id`, `created_at`,
   `updated_at`, `status`, `metadata` at minimum.

3. Write `db/seed.py` to seed MongoDB with exactly the demo dataset from PRD
   section 9 (same merchant, products, opportunity, experiment, order intent
   values already used in the frontend's `demo-scenario.ts` — keep the two
   in sync so the demo is identical whether the frontend hits mock or real
   API).

4. Leave payment endpoints (`/payments/razorpay/*`, `/webhooks/razorpay`) as
   stubs that return realistic shapes but don't call Razorpay yet — that's
   `03-razorpay-integration.md`. Leave agent-driving logic
   (`revenue_intelligence.py`, `growth_strategist.py`, etc.) as deterministic
   functions returning the seeded demo data for now — that's
   `04-agents-and-policy-guard.md`. This phase is about the CRUD/read
   surface and correct data modeling, not yet about policy/agent behavior.

5. CORS: allow only `FRONTEND_ORIGIN` from `.env.example`.

6. Add `apps/api/requirements.txt` and a `apps/api/README.md` with local run
   instructions (`uvicorn app.main:app --reload`, plus how to point it at
   local vs. Atlas MongoDB).

7. Update `apps/web/src/lib/api-client.ts` so its functions call
   `NEXT_PUBLIC_API_BASE_URL` when set, falling back to the phase-1 mock
   implementation only if the env var is absent — do not delete the mock
   path, it's useful for frontend-only development.

8. Write basic tests under `apps/api/app/tests/` for at least: dashboard
   overview shape, opportunity approve state transition, policy update.

## Acceptance criteria

- `uvicorn app.main:app --reload` serves all PRD section 13 routes.
- `apps/web` running against `NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1`
  renders identically to how it renders against the mock client.
- Seeded MongoDB data matches the frontend fixture values exactly (same IDs,
  same numbers) so switching between mock and real backend is invisible in
  the demo.
