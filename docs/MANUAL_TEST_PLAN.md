# RAYGO — MANUAL TEST PLAN

Covers the AI Agent Layer (`RAYGO_AI_Agent_PRD.md`) on top of the completed
frontend and backend. Supersedes the draft `MANUAL_TEST_PLAN.md` uploaded at
project kickoff — same test IDs, filled in against what was actually built.

## How to read this document

Every test below is marked with one of three **Status** values:

- **AUTOMATED** — covered by an assertion in `apps/api/app/tests/`. The file
  and test function are named so you can run just that test. These pass
  today, on every commit, with no live Gemini key required (they exercise
  the deterministic fallback path, which is what runs in this environment).
- **MANUAL — API** — not automated, but testable today directly against the
  backend (`http://localhost:8000/docs`, or `curl`), because the frontend is
  not yet wired to this backend (see `README.md` → Next steps). Steps are
  written against the REST API.
- **MANUAL — BLOCKED (frontend not wired)** — requires the actual UI buttons
  and screens to be calling this backend, which is the next integration
  step (`docs/prompts/01-mock-api-layer.md`). Steps are written for once
  that wiring is done; do not attempt them against the current frontend
  build, which still reads local fixtures.

For every MANUAL test you actually run, record:

- Result: PASS / FAIL
- Timestamp
- Environment (local / staged / which Gemini mode)
- Evidence (screenshot, log line, or `requestId`/`correlationId`)
- Reset performed (if any)

## Execution Rules

1. Run P0 tests before any demo.
2. For AUTOMATED tests, run `pytest -q` from `apps/api` and record the
   summary line as evidence — do not re-derive pass/fail by hand.
3. For MANUAL tests, use the `requestId` returned in every API response
   header (`X-Request-ID`) and the `auditEventId` in mutating responses as
   your evidence/correlation ID.
4. Never paste a real `GEMINI_API_KEY` or `RAZORPAY_KEY_SECRET` into this
   file, a screenshot, or a commit. See the Reset Procedure at the end.

---

# P0 TESTS

## Configuration

### AG-001 — Gemini Connectivity
Priority: P0
Status: **MANUAL — API** (requires a real key; not run in this environment)
Preconditions: Developer has set a real `GEMINI_API_KEY` in `apps/api/.env`
and set `USE_MOCK_AGENTS=false`.
Steps:
1. Start the backend (`uvicorn app.main:app --reload`).
2. `GET /api/v1/agents/gemini/health`.
3. `POST /api/v1/agents/coordinate` with `{"requestText": "Show me our revenue opportunities"}`.
Expected:
- Health returns `"provider": "gemini", "status": "ok"`.
- Coordinate returns `"mode": "gemini"` with a schema-valid `CoordinatorOutput`.
- No key appears in the response or in `apps/api` logs.
- An `agent_activity`/audit event is recorded for the coordinate call.
Result: [ ]
Evidence:
Reset: Unset the key or set `USE_MOCK_AGENTS=true` afterward if this was a
temporary test environment.

### AG-002 — Missing Gemini Key
Priority: P0
Status: **AUTOMATED** — `test_agent_layer.py::test_gemini_health_reports_missing_key_by_default`
Steps:
1. Leave `GEMINI_API_KEY` unset (the default).
2. Start the backend.
3. `GET /api/v1/agents/gemini/health`.
Expected:
- Health returns `"provider": "deterministic", "status": "ok"` — the
  deterministic provider is the primary provider, not a degraded mode.
- No crash, no crash loop; every agent-backed endpoint keeps working.
Result: PASS (automated, run on every `pytest -q`)
Evidence: `pytest -q` output — `41 passed`.
Reset: None.

### AG-003 — Invalid Gemini Key
Priority: P0
Status: **MANUAL — API** (needs a syntactically-valid-but-wrong key against
the real Gemini API) / partially **AUTOMATED**
Automated coverage: `test_agent_layer.py::test_gemini_error_messages_never_include_the_raw_key`
simulates the `API_KEY_INVALID` response Gemini returns for a bad key and
confirms it's classified into `GeminiInvalidKeyError` without leaking the
key.
Manual steps (to confirm against the real API):
1. Set `GEMINI_API_KEY=invalid-test-value`, `USE_MOCK_AGENTS=false`.
2. `POST /api/v1/agents/coordinate` with any `requestText`.
Expected:
- Request still returns `200` with `"mode": "deterministic"` and
  `"fallbackReason": "GEMINI_INVALID_KEY"` — the failure is absorbed by the
  fallback, never surfaced as a crash to the merchant.
Result: [ ]
Evidence:
Reset: Restore the real key or unset it.

### AG-004 — Key Not Exposed
Priority: P0
Status: **AUTOMATED** — `test_agent_layer.py::test_gemini_key_never_referenced_in_frontend_source`
Steps: Recursively scans `apps/web/src/**/*.{ts,tsx,js,jsx,env,mjs}` for the
literal strings `GEMINI_API_KEY` / `gemini_api_key`.
Expected: No matches.
Result: PASS
Evidence: `pytest -q` output.
Reset: None.

### AG-005 — Secret Not Logged
Priority: P0
Status: **AUTOMATED** (synthetic key) + **MANUAL — API** (real key, full log
file grep)
Automated coverage: `test_agent_layer.py::test_gemini_error_messages_never_include_the_raw_key`
asserts a fake secret value never appears in any captured log record after
a simulated Gemini failure.
Manual steps (belt-and-suspenders with the real key before any demo):
1. Run a full judge-demo pass with a real `GEMINI_API_KEY` configured.
2. `grep -r "$GEMINI_API_KEY" <log output>` (never grep by pasting the key
   into a shared terminal/screenshot — use a local-only script).
Expected: Zero matches.
Result: [ ]
Evidence:
Reset: None.

### AG-006 — Deterministic Fallback
Priority: P0
Status: **AUTOMATED** — `test_agent_layer.py::test_generate_with_fallback_falls_back_on_provider_timeout`,
`::test_generate_with_fallback_falls_back_on_malformed_output`
Steps: Force the primary provider to raise `GeminiTimeoutError` /
`StructuredOutputInvalidError` and confirm `generate_with_fallback` returns
a schema-valid deterministic result with `mode == "deterministic"` and the
originating error code in `fallbackReason`.
Expected: Deterministic analysis continues; UI-facing `mode` field
identifies the fallback so the frontend can label it (per PRD section 16 —
never claim fallback output is Gemini-generated).
Result: PASS
Evidence: `pytest -q` output.
Reset: None.

---

## Coordinator

Status for AG-010 – AG-015: **AUTOMATED** — `test_agent_layer.py::test_coordinator_routes_by_intent`
(parametrized over all six cases below) and
`::test_coordinator_never_executes_only_routes`.

| ID | Case | Expected specialist |
|---|---|---|
| AG-010 | Revenue routing | `revenue_intelligence` |
| AG-011 | Growth routing | `growth_strategist` |
| AG-012 | Experiment routing | `experiment_agent` |
| AG-013 | AI Commerce routing | `ai_commerce` |
| AG-014 | Payment routing | `payment_agent` |
| AG-015 | Unknown intent | `revenue_intelligence` (documented safe default, `intent: "unknown"`) |

Preconditions: None — runs against the deterministic provider.
Steps: `POST /api/v1/agents/coordinate` with `requestText` matching each
case; inspect `agent` and `intent` in the response.
Expected: Correct specialist selected; response contains no tool-execution
side effects (verified by re-fetching `exp_keyboard_stand` and confirming
its status is unchanged after a coordinate call).
Result: PASS (all 6 cases + no-execution check)
Evidence: `pytest -q` output.
Reset: None.

---

## Revenue Intelligence

### AG-020 — Opportunity detection
Status: **AUTOMATED** (indirectly) — `test_read_endpoints.py::test_opportunities_list_ranked`
confirms the seeded opportunity set is returned, ranked, with
`opp_keyboard_stand` first.

### AG-021 — Evidence correctness
Status: **MANUAL — API** (requires live Gemini to test the narrative text;
the evidence *list itself* is deterministic and asserted automatically —
see AG-024).

### AG-022 — Deterministic financial calculations
Status: **AUTOMATED** — every opportunity/experiment financial figure in
`apps/api/app/db/seed.py` is a fixed value read straight back by
`test_full_demo_path_success` and `test_opportunity_reasoning_uses_backend_numbers_not_invented_ones`;
none of them pass through Gemini.

### AG-023 — Structured confidence validation
Status: **AUTOMATED** — `CoordinatorOutput.confidence` and
`OpportunityReasoning.confidence` are Pydantic `Field(ge=0.0, le=1.0)`; an
out-of-range or non-numeric value fails validation and is caught by the
`StructuredOutputInvalidError` fallback path (see AG-006), never reaches
the caller.

### AG-024 — No hallucinated financial metrics
Status: **AUTOMATED** — `test_agent_layer.py::test_opportunity_reasoning_uses_backend_numbers_not_invented_ones`
asserts `GET /opportunities/opp_keyboard_stand/reasoning` returns
`estimatedImpact: 18400` and `confidence: 0.87` — the exact backend-seeded
values, not model-invented ones. This holds in both deterministic and
Gemini mode: `GeminiProvider`'s prompt for this task explicitly instructs
"never invent financial figures" and passes the backend record as the only
source of numbers; `OpportunityReasoning` doesn't let the model set
`estimatedImpact` to anything the schema didn't receive as context, and any
mismatch a future test wants to catch against live Gemini output should
assert `body["estimatedImpact"] == <seeded value>` the same way.
Result: PASS
Evidence: `pytest -q` output.

---

## Growth / Experiments

| ID | Case | Status |
|---|---|---|
| AG-030 | Hypothesis generation | MANUAL — API (live Gemini for phrasing); deterministic template AUTOMATED via `test_full_demo_path_success` |
| AG-031 | Action preview | MANUAL — API (`GET /opportunities/{id}` `policyPreview` field) |
| AG-032 | Approval requirement | AUTOMATED — every `GrowthHypothesisOutput`/proposal sets `requiresApproval: true`; enforced server-side by Approval Gateway (see AG-070) |
| AG-033 | Unsafe recommendation rejection | AUTOMATED — `test_policy_guard.py::test_discount_over_20pct_is_blocked`, `::test_margin_below_25pct_is_blocked` |
| AG-040 | Create experiment | AUTOMATED — `test_demo_flow.py::test_full_demo_path_success` |
| AG-041 | Control/variant validation | AUTOMATED — same test, asserts `exp["recommendation"] == "scale_variant"` from seeded control/variant data |
| AG-042 | Metrics | AUTOMATED — same test |
| AG-043 | Evaluation | AUTOMATED — `test_agent_layer.py::test_experiment_reasoning_is_opt_in_and_matches_recommendation` |
| AG-044 | Scale recommendation | AUTOMATED — same test, asserts `aiRecommendation.recommendation == "SCALE"` |
| AG-045 | Insufficient-data handling | AUTOMATED — `test_qa_additions.py::test_experiment_recommendation_for_low_confidence_opportunity_stays_conservative` (low-confidence `opp_seasonal_reactivation` never gets inflated into a confident recommendation) |

Expected (all): No experiment side effect occurs before Policy Guard +
Approval Gateway both pass — enforced in `app/api/v1/opportunities.py` and
`app/api/v1/experiments.py` regardless of what any agent or model output
says.

---

## AI Commerce

| ID | Case | Status |
|---|---|---|
| AG-050 | Natural-language product search | AUTOMATED — `test_agent_layer.py::test_ai_buyer_search_includes_parsed_intent` |
| AG-051 | Budget constraint | AUTOMATED — same test; `parsedIntent.budgetMax` echoes the request's budget |
| AG-052 | Availability | MANUAL — BLOCKED (frontend not wired) — needs the AI Buyer screen |
| AG-053 | Product attribute accuracy | AUTOMATED — `test_read_endpoints.py::test_ai_commerce_product_profile` reads real seeded product data, not model text |
| AG-054 | Readiness score | AUTOMATED — `test_read_endpoints.py::test_products_list` + `ai-commerce/readiness` returns the seeded `82` |
| AG-055 | Missing metadata | AUTOMATED — same product profile test asserts `missingMetadata == ["Shipping metadata"]` for `prod_laptop_stand` |
| AG-056 | Basket construction | AUTOMATED — `test_demo_flow.py::test_full_demo_path_success` (basket → order intent → checkout) |

Expected: Product facts (price, stock, specs) always come from
`GET /ai-commerce/products/{id}/profile` / the seeded catalog — never from
free model text. `CommerceIntentOutput` only ever carries *intent*
(category/budget/use-cases), never product facts, by construction.

---

## Policy / Approval

| ID | Case | Status |
|---|---|---|
| AG-060 | Valid discount | AUTOMATED — `test_demo_flow.py::test_full_demo_path_success` (10% discount passes) |
| AG-061 | Discount above 20% blocked | AUTOMATED — `test_policy_guard.py::test_discount_over_20pct_is_blocked` |
| AG-062 | Margin below 25% blocked | AUTOMATED — `test_policy_guard.py::test_margin_below_25pct_is_blocked` |
| AG-063 | Campaign budget exceeded | AUTOMATED — Daily Budget is now enforced in `policy_guard.py` against cumulative same-day spend; `test_qa_additions.py::test_campaign_budget_exceeded_is_blocked`, `::test_campaign_budget_accumulates_across_calls_same_day` |
| AG-064 | Payment retry blocked | AUTOMATED — `test_policy_guard.py::test_payment_retry_always_blocked`, `::test_second_payment_retry_rejected_even_called_directly` |
| AG-065 | Approval required | AUTOMATED — every consequential endpoint response includes a `policyEvaluationId` + `approvalId`, asserted in `test_full_demo_path_success` |
| AG-066 | Policy override attempt | AUTOMATED — `test_agent_layer.py::test_prompt_injection_does_not_bypass_policy_or_leak_secrets` ("ignore policy" text) + `test_policy_guard.py::test_payment_retry_policy_cannot_be_unlocked` (direct `PATCH` attempt on the Payment Retry policy is rejected `403`) |
| AG-070 | Approval request | AUTOMATED — `approval_gateway.record_approval` called and persisted in every approve/scale flow |
| AG-071 | Approval accepted | AUTOMATED — same |
| AG-072 | Approval rejected | AUTOMATED — `POST /opportunities/{id}/reject` and `POST /experiments/{id}/reject` now exist; `test_qa_additions.py::test_opportunity_rejection_is_recorded`, `::test_experiment_reject_keeps_it_running` |
| AG-073 | Fake AI approval rejected | AUTOMATED (by construction) — `CoordinatorOutput`/agent schemas have no `approved` field at all; the only place `status: "approved"` can be written is `approval_gateway.py`, called only from the two REST endpoints that already re-run Policy Guard. There is no code path where model text sets approval state. |
| AG-074 | Unauthorized approval rejected | AUTOMATED — a lightweight approver allow-list now exists in `approval_gateway.py` (`ALLOWED_APPROVERS`); `test_qa_additions.py::test_unauthorized_approver_is_rejected`, `::test_unauthorized_rejecter_is_rejected`. This is explicitly **not** a full auth/session layer — see Known Gaps. |

---

## Payment

| ID | Case | Status |
|---|---|---|
| AG-080 | Create order | AUTOMATED — `test_demo_flow.py::test_full_demo_path_success` |
| AG-081 | Payment success | AUTOMATED — same |
| AG-082 | Payment failure | AUTOMATED — `::test_payment_failure_path_blocks_retry` |
| AG-083 | No automatic retry | AUTOMATED — same + `test_policy_guard.py::test_second_payment_retry_rejected_even_called_directly` |
| AG-084 | Duplicate payment protection | AUTOMATED — Idempotency-Key tests (`test_idempotency_and_errors.py`) cover the create-order path; the same mechanism backs this |
| AG-085 | Invalid payment state | MANUAL — API (e.g. calling `/payments/razorpay/order` twice outside idempotency, or verifying against an already-paid intent — partially guarded by the `review`/`payment_failed`-only state check in `payment_agent.py`, not yet a dedicated test) |
| AG-086 | Payment audit record | AUTOMATED — `test_demo_flow.py` asserts `"Create Order"` and `"Payment verified"` / `"Payment failed"` + `"Retry Payment"` appear in `GET /audit` |

---

## Agent Activity / Audit

| ID | Case | Status |
|---|---|---|
| AG-090 | Agent activity | AUTOMATED — `test_read_endpoints.py::test_agents_status_and_activity` |
| AG-091 | Event ordering | AUTOMATED — `test_qa_additions.py::test_agent_activity_events_are_chronologically_ordered` |
| AG-092 | Failure event | AUTOMATED — `test_demo_flow.py::test_payment_failure_path_blocks_retry` |
| AG-093 | Policy-block event | AUTOMATED — `test_policy_guard.py` (discount/margin/retry all write a `Prevented`-outcome audit event) |
| AG-100 | Successful consequential action | AUTOMATED — `test_full_demo_path_success` |
| AG-101 | Blocked action | AUTOMATED — `test_policy_guard.py` |
| AG-102 | Failed action | AUTOMATED — `test_payment_failure_path_blocks_retry` |
| AG-103 | Approval trail | AUTOMATED — `approvals` collection written on every approve/scale; `approvalId` returned and asserted |
| AG-104 | Correlation ID consistency | AUTOMATED — `test_qa_additions.py::test_correlation_ids_are_consistent_across_the_payment_chain` (order ID + payment attempt ID + order intent ID all cross-checked between the API response and the persisted audit event) |

---

## Reliability

| ID | Case | Status |
|---|---|---|
| AG-110 | Gemini timeout | AUTOMATED — `test_agent_layer.py::test_generate_with_fallback_falls_back_on_provider_timeout` |
| AG-111 | Gemini rate limit | MANUAL — API (classification logic exists in `gemini_provider.py` for `429`/`RESOURCE_EXHAUSTED`; not exercised against the real API in this environment) |
| AG-112 | Malformed structured output | AUTOMATED — `::test_generate_with_fallback_falls_back_on_malformed_output` |
| AG-113 | Tool validation failure | N/A for this architecture — Gemini never calls tools directly (see README → AI Agent Architecture); `is_allowed()`/`get_tool()` reject any unregistered name if ever wired to a function-calling loop, covered by `test_agent_layer.py::test_tool_registry_classifies_side_effects_correctly` |
| AG-114 | Database unavailable | AUTOMATED — `test_smoke.py::test_health_db` (happy path) + `test_qa_additions.py::test_health_db_reports_disconnected_when_db_ping_fails` (simulated outage: health endpoint reports `connected: false` without crashing) |
| AG-115 | External service unavailable | MANUAL — API (Razorpay stub mode already covers "no live Razorpay" as the default *working* path, not a failure path — a true Razorpay-outage-while-configured scenario is a gap) |

---

## Security

| ID | Case | Status |
|---|---|---|
| AG-120 | Secret leakage scan | AUTOMATED — AG-004/AG-005 tests above |
| AG-121 | Frontend cannot access Gemini key | AUTOMATED — same as AG-004; also true by construction: `NEXT_PUBLIC_*` is the only env surface exposed to `apps/web`, and `GEMINI_API_KEY` is never prefixed that way |
| AG-122 | Unauthorized action | MANUAL — BLOCKED / KNOWN GAP — there is no auth/session layer in this MVP (see backend README "What's deliberately still a stub"); every request is trusted as the demo merchant. This is a real limitation, not a false negative — do not claim this test passes. |
| AG-123 | Prompt injection | AUTOMATED — `test_agent_layer.py::test_prompt_injection_does_not_bypass_policy_or_leak_secrets`, parametrized over all three PRD example strings plus one more |
| AG-124 | Tool allow-list | AUTOMATED — `test_tool_registry_classifies_side_effects_correctly` + `test_agents_tools_endpoint_lists_full_registry` |
| AG-125 | Sensitive data exposure | AUTOMATED — `test_qa_additions.py::test_no_response_body_leaks_secrets`, parametrized across 11 read endpoints, scans every response body for `gemini_api_key`/`razorpay_key_secret`/`razorpay_webhook_secret` |

---

# End-to-End

All of AG-130 – AG-150 are **MANUAL — BLOCKED (frontend not wired)** as
*UI* journeys — the frontend (`apps/web`) still reads local fixtures, not
this backend (tracked in `docs/prompts/01-mock-api-layer.md`). Until that's
done, the equivalent **backend** chain is fully exercised end to end by
`test_demo_flow.py::test_full_demo_path_success` (the success path, steps
1–13 below) and `::test_payment_failure_path_blocks_retry` (step 14).

| ID | UI journey | Backend equivalent (AUTOMATED today) |
|---|---|---|
| AG-130 | Overview → Opportunity | `GET /dashboard/overview` → `GET /opportunities/{id}` |
| AG-131 | Opportunity → Experiment | `POST /opportunities/{id}/approve` |
| AG-132 | Experiment → AI Commerce | `GET /experiments/{id}` → `GET /ai-commerce/readiness` |
| AG-133 | AI Buyer → Basket | `POST /ai-buyer/search` → `POST /ai-buyer/basket` |
| AG-134 | Basket → Checkout | `POST /order-intents` → `GET /order-intents/{id}` |
| AG-135 | Checkout → Payment | `POST /payments/razorpay/order` |
| AG-136 | Payment Failure → Recovery | `POST /payments/razorpay/failure` (asserts blocked retry, unpaid order, audit event) |
| AG-137 | Audit Trail | `GET /audit` (asserts the full action chain appears) |
| AG-138 | Agent Activity | `GET /agents/activity` |
| AG-150 | Complete Judge Demo | Once `apps/web` is wired to this backend, walk `docs/demo-script.md` (to be written in the polish phase) against the live UI; until then, `test_full_demo_path_success` is the closest verified equivalent. |

Result for the backend equivalents: PASS (all, via `pytest -q`).
Result for the UI journeys: [ ] — pending frontend wiring.

---

---

# Performance / Smoothness

Backend fixes made during this QA pass (see `docs/QA_FINAL_REPORT.md` for
the full list):

- Fixed a sequential N+1 in `GET /payments` (was one DB round trip per
  payment attempt for order-intent lookups; now batches distinct order
  intents with `asyncio.gather`).
- Parallelized the two independent reads behind `GET /dashboard/overview`
  (merchant + top opportunities) with `asyncio.gather` instead of
  sequential `await`.
- Added latency logging (`agent_provider_call` / `agent_provider_fallback`
  log events, with `latencyMs`) around every Gemini/deterministic provider
  call, so slow AI calls are visible in logs without a profiler.

| ID | Case | Status |
|---|---|---|
| PERF-001 – 003, 006 – 012 | Overview / opportunity / experiment / policy / payment / activity / audit read+write latency | AUTOMATED — `test_qa_additions.py::test_read_endpoint_responds_quickly_against_mongomock` (parametrized), `::test_policy_evaluate_is_fast`. These measure our own code path against `mongomock-motor` in-process — they catch N+1/unbounded-loop regressions, they are **not** a real production latency measurement (no real network, no real MongoDB). A real measurement needs a deployed environment, which this sandbox doesn't have. |
| PERF-004 | AI reasoning latency | AUTOMATED (deterministic path) — `test_coordinator_route_is_fast_on_deterministic_path`. Gemini-path latency needs a live key (MANUAL — API). |
| PERF-005 | Policy-check latency | AUTOMATED — `test_policy_evaluate_is_fast` (<200ms ceiling against mongomock) |
| PERF-013 | Duplicate-click protection | AUTOMATED (backend half) — Idempotency-Key handling (`test_idempotency_and_errors.py`) is what a "duplicate click" maps to server-side; the actual UI debounce/disable-button behavior is frontend work, blocked on wiring |
| PERF-014, 015, 016 | Stale-request cancellation / no unnecessary reload / no unnecessary Gemini calls | MANUAL — BLOCKED (frontend not wired). PERF-016's backend half is already true by construction: `USE_MOCK_AGENTS=true` (default) never calls Gemini at all, and every provider call is a single request, not a loop. |

---

# RESET PROCEDURE

After testing:

1. Stop test processes (`uvicorn`, `pytest` runs).
2. Reset seeded demo data: restart the backend with `SEED_ON_STARTUP=true`
   (the default), or run `python -m app.db.seed` directly — the seed is
   idempotent (upserts by `id`), so it always returns to the exact
   documented demo state.
3. Remove any temporary credentials from `.env` (`GEMINI_API_KEY`,
   `RAZORPAY_KEY_ID/SECRET`) if they were added only for this test session.
4. Verify `.env` is `.gitignore`d (`apps/api/.gitignore` already covers it —
   confirm with `git status` that it's untracked).
5. `git diff` / `git log -p` search for the string `sk-` or the literal key
   value before pushing, if you pasted a real key anywhere during testing.
6. `grep -r GEMINI_API_KEY apps/web/src` — should return nothing (also
   covered by AG-004's automated test).
7. Confirm test data is restored (step 2).
8. Record final P0 results in this file (fill in the `Result:` fields above)
   and commit the filled-in copy separately from the template.

---

# KNOWN GAPS (tracked, not hidden)

These are the honest limitations after this round of QA hardening — each is
a genuine scope decision, not an oversight being glossed over:

- **No real merchant auth/session layer.** A lightweight approver
  allow-list (`ALLOWED_APPROVERS` in `approval_gateway.py`) now rejects any
  `approvedBy`/`rejectedBy` value outside a fixed set (AG-074 automated),
  but this is a stand-in, not real authentication — `merchantId` itself is
  still a caller-supplied field, not tied to a logged-in session. AG-122
  (unauthorized *agent* action, as opposed to unauthorized *approval*)
  still has no session concept to test against.
- **Frontend is not wired to this backend yet.** All UI-level AG-130–150
  and AG-052 tests are blocked on `docs/prompts/01-mock-api-layer.md`. The
  "Frontend smoothness" requirements in the AI Agent PRD v2 (skeleton
  states, debounced search, stale-request cancellation, optimistic UI) are
  real requirements against a backend that's actually being called — they
  cannot be meaningfully implemented or verified against a frontend that
  still reads local fixtures. Backend-side performance work (see
  Performance section below) was completed; frontend-side performance work
  is deferred to when `01-mock-api-layer.md` is done.
- **Google ADK is not integrated.** `app/services/adk_orchestrator.py`
  remains an explicit `NotImplementedError` seam behind
  `USE_ADK_ORCHESTRATOR` — the coordinator/agent routing in this PRD is
  implemented directly (Gemini structured-output calls + deterministic
  fallback), not through ADK's own orchestration runtime. See README → AI
  Agent Architecture for the reasoning.

END OF MANUAL TEST PLAN.
