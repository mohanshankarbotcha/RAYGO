# RAYGO API

FastAPI backend implementing `docs/RAYGO_Backend_Implementation_PRD.md` against
MongoDB. Pairs with the `apps/web` frontend from Phase 1.

## Status

Fully implemented and tested:

- All routers from PRD section 13: merchant/onboarding, dashboard, products,
  opportunities (with approve flow), experiments (with scale flow),
  AI Commerce, AI Buyer + order intents, payments (Razorpay Test Mode order/
  verify/failure/webhook), policies (with the Payment Retry hard-lock),
  agents, audit.
- **AI Agent Layer** (`RAYGO_AI_Agent_PRD.md`): a Gemini/deterministic
  provider abstraction, a RAYGO Coordinator that routes requests to
  specialist agents, a typed/allow-listed tool registry with side-effect
  classification, and Gemini-or-deterministic reasoning wired into
  opportunity detail, experiment detail, and AI Buyer search — with every
  financial number still coming from deterministic backend calculation,
  never from model output. Full detail below.
- Policy Guard hard rules (discount > 20%, margin < 25%, payment retry,
  refunds) enforced server-side, not just in UI copy.
- Approval Gateway records explicit merchant confirmation as its own
  persisted record.
- Audit Service records every consequential transition with a stable,
  reconstructable decision summary.
- Idempotency-Key support on every mutating endpoint (same key + route +
  body → cached replay; same key + different body → `409
  IDEMPOTENCY_CONFLICT`).
- Deterministic seed script reproducing the exact demo dataset from the PRD
  (NovaTech Store, 7 products, 7 opportunities, the keyboard+stand
  experiment, all 6 policies, agent activity, the seeded AI-buyer basket/
  order intent).
- Razorpay integration is real (signature verification, order creation) but
  runs in a **local stub mode** when no live Test Mode keys are configured,
  so the full demo works out of the box — see "Razorpay modes" below.
- 75 passing tests (`app/tests/`) — the original 41 (backend CRUD/payments/
  policy surface + AI Agent Layer basics) plus 34 more added in a QA
  hardening pass (Daily Budget enforcement, explicit approval rejection,
  approver allow-list, event ordering, correlation-ID consistency, DB-
  unavailable handling, secret-exposure scanning, and performance
  regression guards). Full accounting in `docs/QA_FINAL_REPORT.md`; full
  `AG-*`/`PERF-*` traceability in `docs/MANUAL_TEST_PLAN.md`.
- Verified booting as a real `uvicorn` process over an actual TCP socket
  (not just the test client) and serving live HTTP correctly, including the
  new agent endpoints.

## Requirements

- Python 3.11+
- MongoDB (local, Docker, or Atlas) for actually running the service —
  tests do not need it (they use `mongomock-motor`).

## Setup

```bash
cd apps/api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp ../../.env.example .env   # then fill in what you need
```

## Run

```bash
uvicorn app.main:app --reload --port 8000
```

On startup the app connects to MongoDB, ensures indexes, and — if
`SEED_ON_STARTUP=true` (the default) — seeds the deterministic demo dataset.
Swagger docs: `http://localhost:8000/docs`.

To seed manually instead:

```bash
python -m app.db.seed
```

## AI Agent Architecture

```text
Frontend
   ↓
FastAPI routers (app/api/v1/*)
   ↓
Specialist services (revenue_intelligence, growth_strategist,
experiment_agent, ai_commerce_agent, policy_guard, approval_gateway,
payment_agent)
   ↓
Provider abstraction (app/services/providers/)
   ├── GeminiProvider       — calls Gemini, returns schema-validated output
   └── DeterministicProvider — hand-written logic, always available, no network
   ↓
Existing backend services (unchanged) → MongoDB / Razorpay Service → Audit Service
```

**What Gemini actually does here.** Gemini's role is strictly *advisory and
narrative*: the RAYGO Coordinator (`POST /agents/coordinate`) classifies a
request and names a specialist agent, and three endpoints
(`GET /opportunities/{id}/reasoning`, `GET /experiments/{id}?include_reasoning=true`,
`POST /ai-buyer/search`) ask it to phrase an explanation or parse a buyer's
free-text intent. Every response is validated against a Pydantic schema
(`app/domain/agent_schemas.py`) before it's trusted, and every number in
those responses (impact, confidence, control/variant metrics, prices) is
read from the same deterministic backend records the REST API already
serves — Gemini interprets them, it never invents or overwrites them.

**What Gemini never does.** It never calls a tool directly, never writes to
MongoDB, never sees a Razorpay credential, and never decides whether an
action is approved. Every consequential action (`create_experiment`,
`scale_experiment`, `create_order`, `verify_payment`) still runs through the
exact same REST endpoints built in the previous phase, which re-run Policy
Guard and Approval Gateway independently of anything the coordinator or any
agent said. This is why prompt injection can't work here by construction
(see `MANUAL_TEST_PLAN.md` → AG-123): there is no code path from "text the
model produced" to "money moved" — only from "merchant clicked confirm" →
REST endpoint → Policy Guard → Approval Gateway → execution.

**Deterministic fallback.** Whenever Gemini is unconfigured
(`GEMINI_API_KEY` unset), in mock mode (`USE_MOCK_AGENTS=true`, the
default), or fails for any reason (timeout, rate limit, invalid key,
malformed output), `generate_with_fallback()` transparently falls back to
`DeterministicProvider` and tags the response with `"mode": "deterministic"`
and a `fallbackReason` error code. The frontend is expected to surface this
(e.g. "AI reasoning temporarily unavailable — deterministic analysis is
active") rather than claim the fallback text came from Gemini.

**Why no Google ADK yet.** The PRD scopes ADK as "where appropriate." Given
this MVP's actual call pattern — one schema-validated Gemini call per
task, no multi-step tool-calling loop — a hand-rolled provider abstraction
with explicit fallback is more reliable and easier to verify than adopting
ADK's own orchestration runtime for a shape of problem it isn't needed for
yet (engineering rule: "prefer reliable agents over unnecessary agent
proliferation"). `app/services/adk_orchestrator.py` remains the documented
seam, behind `USE_ADK_ORCHESTRATOR=false`, for when the agent layer grows
into something that actually needs multi-step orchestration.

### Agent Responsibility Matrix

| Agent | Responsibility | Reads | Writes | Approval |
|---|---|---|---|---|
| RAYGO Coordinator | Routes a request to one specialist; advisory only | Request text | Agent activity + audit event | N/A — never executes |
| Revenue Intelligence | Ranks opportunities, explains evidence | `opportunities` collection | Nothing (read-only) | N/A |
| Growth Strategist | Turns an approved opportunity into an experiment proposal + hypothesis narrative | `opportunities` | Nothing directly — proposal is passed to Experiment Agent | Required before Experiment Agent creates anything |
| Experiment Agent | Creates/scales experiments, explains recommendation | `experiments` | `experiments` (via `create_from_proposal`/`scale`) | Required (Policy Guard + Approval Gateway) |
| AI Commerce Agent | Readiness scoring, product profiles, catalog optimization, buyer-intent parsing | `products`, catalog | `products` (AI-readiness metadata only) | Not required (`SAFE_WRITE`) |
| Policy Guard | Evaluates every consequential action deterministically | Proposed action | `policy_evaluations` | N/A — it IS the gate |
| Approval Gateway | Records explicit merchant authorization | Policy evaluation | `approvals` | N/A — it IS the approval record |
| Payment Agent | Orchestrates Razorpay order/verify/failure; never sees secrets outside `razorpay_service.py` | `order_intents`, `payment_attempts` | `payment_attempts`, `orders` | Required (`FINANCIAL`) |
| Audit Service | Records every consequential transition | — | `audit_events` | N/A |

### Gemini Setup

1. Get a Gemini API key from Google AI Studio.
2. Set it **only** as a server-side environment variable in `apps/api/.env`:
   ```text
   GEMINI_API_KEY=your-real-key-here
   GEMINI_MODEL=gemini-2.0-flash
   GEMINI_TEMPERATURE=0.2
   GEMINI_TIMEOUT_SECONDS=30
   GEMINI_MAX_RETRIES=2
   USE_MOCK_AGENTS=false
   ```
3. **Never** put the key in `apps/web`, in any `NEXT_PUBLIC_*` variable, in
   this README, in a commit, in a screenshot, or in a log line. The key is
   read in exactly one place in the whole codebase:
   `app/services/providers/gemini_provider.py`. `GET /api/v1/agents/gemini/health`
   tells you whether it's configured and reachable without ever echoing it
   back.
4. Leave `USE_MOCK_AGENTS=true` (the default) to run entirely on the
   deterministic provider — useful for demos where you don't want any
   dependency on Gemini being reachable.

### UI Operation Map

Keys (environment variables) that gate what runs:

| Key | Where read | Effect |
|---|---|---|
| `GEMINI_API_KEY` | `gemini_provider.py` only | Unset/empty → deterministic provider is primary, always |
| `USE_MOCK_AGENTS` | `providers/factory.py` | `true` (default) → deterministic even if a key is set |
| `RAZORPAY_KEY_ID` / `RAZORPAY_KEY_SECRET` | `razorpay_service.py` only | Unset → local stub mode (see main README) |
| `ALLOW_RAZORPAY_STUB` | `razorpay_service.py` | Must be `true` for stub mode to be allowed |
| `USE_ADK_ORCHESTRATOR` | `adk_orchestrator.py` | `false` (default) → seam raises `NotImplementedError` if called |

Buttons in the frontend (`apps/web`) and what they do once wired to this
backend (see main README → Next steps for current wiring status):

| UI Button | Screen | Backend endpoint | Agent | Tool | Result |
|---|---|---|---|---|---|
| Initialize RAYGO | Onboarding | `POST /onboarding/initialize` | System | — | Seeds demo data, routes to Overview |
| Review Opportunity (card click) | Overview / Opportunity Center | `GET /opportunities/{id}`, `GET /opportunities/{id}/reasoning` | Revenue Intelligence | `get_opportunity_candidates` | Evidence + AI reasoning narrative |
| Approve & Create Experiment | Opportunity detail | `POST /opportunities/{id}/approve` | Growth Strategist + Policy Guard + Approval Gateway + Experiment Agent | `create_experiment` | New experiment, or `403 POLICY_BLOCKED` |
| Scale Experiment | Experiment detail | `POST /experiments/{id}/scale` | Experiment Agent + Policy Guard + Approval Gateway | `recommend_scale` | Experiment status → `scaled`, or blocked |
| Keep Running | Experiment detail | `POST /experiments/{id}/reject` | Approval Gateway | — | Rejection recorded, experiment stays `running` |
| Optimize Catalog | AI Commerce | `POST /ai-commerce/optimize-catalog` | AI Commerce Agent | `optimize_product_metadata` | Product AI-readiness scores updated |
| Preview as AI Buyer | AI Commerce | Navigates to `/ai-buyer` | — | — | — |
| Search (buyer request box) | AI Buyer | `POST /ai-buyer/search` | AI Commerce Agent | `search_products` | Matched products + `parsedIntent` |
| Add to Basket | AI Buyer | `POST /ai-buyer/basket` | AI Commerce Agent | `construct_basket` | Basket totals |
| Review Purchase | AI Buyer | `POST /order-intents` | — | — | Routes to Checkout |
| Confirm & Pay | Checkout | `POST /payments/razorpay/order` → `POST /payments/razorpay/verify` | Payment Agent | `create_order`, `verify_payment` | Payment success/failure screen |
| Simulate payment failure (demo) | Checkout | `POST /payments/razorpay/failure` | Payment Agent + Policy Guard | — | Failure screen, retry blocked |
| Pause / Activate (policy card) | Policies | `PATCH /policies/{id}` | System | — | Policy status updated (Payment Retry is locked — see below) |
| Agent Activity (page load) | Agent Activity | `GET /agents/activity`, `GET /agents/status` | Coordinator | `get_agent_activity` | Timeline of real events |
| Audit Trail (page load / row click) | Audit Trail | `GET /audit`, `GET /audit/{id}` | Audit Service | `get_audit_record` | Full decision trace |

All approve/reject actions above require `approvedBy`/`rejectedBy` to be
`"merchant_demo_user"` — any other value is rejected with
`403 UNAUTHORIZED_APPROVER`. This is a lightweight allow-list, not a real
auth system; see "What's deliberately still a stub" below.

### Performance

| Symptom | Cause | What happens | Fix |
|---|---|---|---|
| `GET /agents/gemini/health` → `"status": "missing_key"` | `GEMINI_API_KEY` unset | Deterministic provider used everywhere (not an error) | Set the key if you want live Gemini reasoning; otherwise this is expected |
| `"fallbackReason": "GEMINI_INVALID_KEY"` in a response | Key set but rejected by Google | Falls back to deterministic automatically | Check the key in Google AI Studio; regenerate if needed |
| `"fallbackReason": "GEMINI_RATE_LIMIT"` | Too many requests too fast | Falls back to deterministic automatically | Wait, or lower request volume; `GEMINI_MAX_RETRIES` bounds retries |
| `"fallbackReason": "GEMINI_TIMEOUT"` | Slow/unreachable network | Falls back after `GEMINI_TIMEOUT_SECONDS` | Increase the timeout, or check connectivity |
| `"fallbackReason": "STRUCTURED_OUTPUT_INVALID"` | Gemini returned non-JSON or schema-mismatched output | Falls back to deterministic; failure is logged (never the raw output verbatim if it might contain echoed prompt injection attempts) | Usually transient; if persistent, check `GEMINI_MODEL` supports structured output |
| `403 POLICY_BLOCKED` on approve/scale | Discount > 20% or margin < 25% in the proposal | Action rejected, no experiment/scale created | Expected behavior — adjust the proposal, not the policy |
| `403 POLICY_BLOCKED` on `PATCH /policies/policy_payment_retry` | Attempted to unlock Payment Retry | Rejected — this policy is hard-locked for MVP | Expected behavior — not configurable |
| Payment failure not blocking retry | Check you're calling `/payments/razorpay/failure`, not re-calling `/order` directly | — | Retrying via `/order` on an intent in `payment_failed` state is allowed *once* (to try again with a new attempt) — the block is specifically on *automatic* retry, not the merchant choosing to try again |

### Manual Testing

Reference: `docs/MANUAL_TEST_PLAN.md` — every `AG-*` and `PERF-*` test ID
from the AI Agent PRD, marked AUTOMATED (with the exact `pytest` test
name), testable today against the API directly, or blocked pending
frontend wiring, plus a "Known Gaps" section listing what's genuinely not
covered yet — no test is silently marked passing without a real assertion
backing it.

### Final Test Status

**75/75 automated tests passing, 0 failures, 0 skipped, 0 known
regressions** — full accounting (what was tested, what was fixed, what
performance numbers do and don't prove, and five plainly-stated remaining
limitations) in `docs/QA_FINAL_REPORT.md`. Re-run it yourself any time with
`pytest -q` from this directory.

## Test

```bash
pytest -q
```

Tests use `mongomock-motor`, an in-memory MongoDB double, wired in via
`app/tests/conftest.py`. No real MongoDB connection is required or attempted
during tests — `app.state.db` is set directly to the mock database and the
app's real startup/shutdown lifecycle is not triggered (the test transport
doesn't run ASGI lifespan events).

## Razorpay modes

Controlled by `RAZORPAY_MODE` (must be `test` — anything else is rejected),
`RAZORPAY_KEY_ID` / `RAZORPAY_KEY_SECRET`, and `ALLOW_RAZORPAY_STUB`:

- **Real Razorpay Test Mode** (`RAZORPAY_KEY_ID`/`SECRET` set): orders are
  created via the real Razorpay API and payment signatures are verified with
  Razorpay's own `utility.verify_payment_signature`. Use this to demo with
  Razorpay's actual Test Mode checkout and test cards.
- **Local stub mode** (no keys set, `ALLOW_RAZORPAY_STUB=true`, the
  default): `RazorpayService` generates a `order_stub_...` id and verifies
  payments against an HMAC signature it can also generate itself
  (`RazorpayService.sign_stub_payment`, used by the test suite). This lets
  the full onboarding → checkout → payment success/failure path run and be
  demoed without needing live Razorpay credentials, while keeping the same
  code path (server-side order creation + server-side signature
  verification) that real mode uses.

`RAZORPAY_KEY_SECRET` and `RAZORPAY_WEBHOOK_SECRET` are only ever read inside
`app/services/razorpay_service.py` — no router or other service imports them
directly, and they're never included in any API response.

## Project layout

```text
app/
  main.py                 FastAPI app, middleware, startup/shutdown
  core/                    config, errors, logging, security, idempotency
  api/
    deps.py                 FastAPI dependency wiring
    v1/                      one router module per resource
  domain/                  constants, state machines, Pydantic schemas,
                            agent_schemas.py (AI structured outputs),
                            tool_registry.py (typed, allow-listed tools)
  services/                business logic: policy guard, approval gateway,
                            audit, razorpay, payment agent, deterministic
                            agent stubs, coordinator.py (RAYGO Coordinator)
    providers/               AgentProvider abstraction: gemini_provider.py,
                              deterministic_provider.py, factory.py
                              (generate_with_fallback)
  repositories/            generic Mongo repository + per-collection registry
  db/                      connection, indexes, seed script
  tests/                   pytest suite (mongomock-motor, no real DB needed)
```

## What's deliberately still a stub

Per the PRD's explicit MVP scope:

- `services/adk_orchestrator.py` — a seam only, raises `NotImplementedError`
  unless `USE_ADK_ORCHESTRATOR=true` is set and it's implemented. See
  "AI Agent Architecture" above for why.
- Refund execution is not implemented — Policy Guard blocks it unconditionally.
- Auto Execution policy stays `paused` — every consequential action requires
  explicit merchant approval, enforced server-side.
- There is no *real* merchant auth/session layer — a lightweight approver
  allow-list (`ALLOWED_APPROVERS` in `approval_gateway.py`) rejects any
  unrecognized `approvedBy`/`rejectedBy`, but `merchantId` itself is still a
  caller-supplied field, not tied to a logged-in session. See
  `docs/MANUAL_TEST_PLAN.md` → Known Gaps.

## Next steps

- Point `apps/web`'s `lib/api-client.ts` (from the frontend prompt file
  `01-mock-api-layer.md`) at `NEXT_PUBLIC_API_BASE_URL` instead of the mock
  fixtures — this is what unblocks every "MANUAL — BLOCKED (frontend not
  wired)" row in `docs/MANUAL_TEST_PLAN.md`.
- Set a real `GEMINI_API_KEY` and `USE_MOCK_AGENTS=false` in a non-shared
  environment and run through AG-001/003/111 manually.
- Deploy: backend to Render, MongoDB to Atlas, set real `FRONTEND_ORIGIN` and
  Razorpay Test Mode keys for a hosted demo.
- Close the "Known Gaps" in `docs/MANUAL_TEST_PLAN.md` (real auth/session
  layer, live Gemini/MongoDB/Razorpay verification) — AG-063/072/074 are
  now automated against the allow-list/reject-endpoint stand-ins; AG-122
  and real external-service verification are what's left.
