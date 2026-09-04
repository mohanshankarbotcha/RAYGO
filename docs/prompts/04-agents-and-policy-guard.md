# 04 — Agent Services and Policy Guard

> **STATUS: superseded — this is done.** Policy Guard, Approval Gateway, and
> the full AI Agent Layer (Gemini + deterministic provider abstraction,
> RAYGO Coordinator, typed tool registry) are implemented and tested — see
> `apps/api/README.md` → AI Agent Architecture and `docs/MANUAL_TEST_PLAN.md`.
> What's left is closing the gaps documented in `MANUAL_TEST_PLAN.md` →
> Known Gaps (merchant auth/session layer, an explicit approval-reject
> endpoint, and Daily Budget enforcement against actual spend). The
> remainder of this file is kept for historical reference.

## Goal

Implement the seven logical agents and the Policy Guard state machine from
PRD sections 14–15 as real backend services in `apps/api`, replacing the
deterministic stubs from `02-fastapi-backend.md` with actual policy-gated
logic (still deterministic for MVP — Gemini/ADK integration is explicitly
optional and behind a feature flag per the PRD).

## Requirements

1. Implement each agent as a service module under `apps/api/app/services/`:
   - `revenue_intelligence.py` — ranks opportunities from orders/products/
     cart-behavior/margins/abandonment inputs; for MVP, return the seeded
     demo opportunities with their evidence intact.
   - `growth_strategist.py` — given an approved opportunity, proposes an
     experiment (hypothesis, discount, expected uplift) that Policy Guard
     will evaluate.
   - `experiment_agent.py` — runs/measures experiments; for MVP, return the
     seeded control/variant metrics.
   - `ai_commerce_agent.py` — computes AI Commerce readiness score,
     blockers, and AI-readable product profiles.
   - `policy_guard.py` — the core gate. Implement the state flow from PRD
     section 15 exactly:
     `proposed -> policy_evaluated -> approval_required -> merchant_approved
     -> execution_pending -> executed | blocked | failed`.
     Hard rules to enforce unconditionally, not just in the UI:
     - discount above 20% → blocked
     - margin below 25% → blocked
     - payment retry after failure → blocked, always
     - refund execution → not allowed in MVP
     - merchant approval required before any experiment or payment execution
   - `approval_gateway.py` — records approval events once a merchant
     confirms, tying together `PolicyEvaluation` + click confirmation into
     an `Approval` record and an audit event.
   - `payment_agent.py` — wraps the Razorpay flow from `03-razorpay-
     integration.md` behind the same proposed→executed state machine; must
     call `policy_guard.py` before any retry attempt and hard-block it.

2. Wire `POST /api/v1/opportunities/{id}/approve`,
   `POST /api/v1/experiments/{id}/scale`, and `PATCH /api/v1/policies/{id}`
   to actually run through `policy_guard.py` and `approval_gateway.py`
   rather than unconditionally succeeding — a discount that would violate
   the 20% limit, or a scale action that would violate the margin floor,
   must be rejected with a clear reason the frontend can display (reuse the
   Policy Guard pass/fail copy already shown in
   `apps/web/src/app/opportunities/[id]/page.tsx`).

3. Write every policy evaluation to `audit_service.py` per the PRD section
   17 audit contract, including correlation IDs for order, payment, policy
   check, agent run, and audit event as required by PRD section 10.14.

4. Add `GET /api/v1/agents/status` and `GET /api/v1/agents/activity` backed
   by real `AgentRun` records this phase produces (each agent call above
   should write one), rather than the static list currently in the
   frontend's `agentTimeline` fixture. The frontend's `/agents` screen
   should keep working unchanged once pointed at these endpoints.

5. Optional (behind `USE_MOCK_AGENTS` / a `GEMINI_API_KEY` feature flag, per
   PRD section 5 "AI"): let `growth_strategist.py` and `ai_commerce_agent.py`
   call Gemini for the natural-language hypothesis/explanation text, with
   structured output validated by the same Pydantic schemas the deterministic
   path produces. Gemini must never call Razorpay or bypass `policy_guard.py`
   — it can only produce content that a schema-validated response contains,
   which the existing gate logic then evaluates identically either way.

## Acceptance criteria

- Attempting to approve an opportunity whose proposed discount exceeds 20%
  (construct a test fixture for this) is rejected with a `blocked` policy
  outcome, not silently approved.
- A second payment retry after a recorded failure is rejected by
  `policy_guard.py` even if called directly (not just prevented by the UI
  disabling the button).
- `GET /api/v1/audit` shows a full, correlated chain for at least one
  end-to-end approve→experiment→payment flow.
