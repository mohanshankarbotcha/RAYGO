# RAYGO — Application Guide

A plain-language companion to `README.md` (which is developer-facing). This
document answers three questions: what does each button do, what feature
does it demonstrate, and how would someone actually use this day to day.

## What RAYGO is

RAYGO is an AI revenue-intelligence layer for an online store. It watches a
merchant's sales data, finds specific opportunities to grow revenue (like
"customers who buy X often want Y too"), proposes a concrete action, checks
that action against the merchant's own safety rules, waits for the
merchant to say yes, then runs a small controlled experiment and reports
whether it worked. Separately, it also lets an AI shopping assistant help a
buyer find and purchase the right product from the same store, with the
same safety rules protecting every payment.

## Current state, honestly

There are two halves to this application, and they're not connected to
each other yet:

- **The backend** (`apps/api`) is complete, tested, and works — 75/75
  automated tests pass. Every capability described below is real and
  callable today via `http://localhost:8000/docs` (an interactive page
  where you can click "Try it out" on any button description below and
  actually run it — no coding required).
- **The frontend** (`apps/web`) is a complete, polished set of screens with
  every button below actually present and clickable — but it's still
  wired to sample data on the frontend itself, not to the backend. Clicking
  "Approve & Create Experiment" in the running frontend today will animate
  and navigate, but the actual policy check and experiment record happen
  against local sample data, not the real backend logic.

Practically: if you want to *see* the polished screens, run the frontend
(`README.md` → Running the frontend). If you want to *actually exercise*
the real logic described below — real policy blocking, real approval
tracking, real audit trail — use the backend's `/docs` page directly. The
next engineering step (tracked in `docs/prompts/01-mock-api-layer.md`)
connects the two so the polished screens drive the real backend.

## Every button: what it does, what it proves

### Onboarding

**Initialize RAYGO** — Loads a sample merchant ("NovaTech Store") with a
realistic product catalog, past sales, and history into the system.
*Feature it supports:* getting from zero to a working demo in one click,
with real numbers behind every screen from that point on.

### Overview (the merchant's home screen)

**Review Opportunity** (clicking any opportunity card) — Opens the detail
of a specific revenue opportunity RAYGO found — for example, "customers
buying a keyboard often also want a laptop stand, but we're not suggesting
it." *Feature:* RAYGO doesn't just show a dashboard number, it shows its
reasoning: what it observed, what it detected, what it concluded, and what
it recommends — with a plain link back to the actual sales data behind
each claim.

### Opportunity detail

**Approve & Create Experiment** — The merchant says "yes, try this." Behind
the button: the proposed discount and margin are checked against the
merchant's own rules (no more than 20% discount, no less than 25% margin),
the approval is recorded as a real authorization event, and only then is an
experiment actually created. *Feature:* nothing happens automatically —
every consequential action requires this explicit human approval, and the
system proves it checked the rules first.

*(New this round)* **Decline** — The merchant says "not this one." Records
that decision explicitly, same as an approval — so there's a real trail of
what was turned down and why, not just silence.

### Experiment detail

**Scale Experiment** — Once an experiment shows a winning result, this
commits to rolling it out more broadly — again gated by the same policy
check and approval record.

**Keep Running** — Declines to scale yet, keeps collecting data. *Feature:*
the choice not to act is recorded just as carefully as the choice to act.

### AI Commerce (catalog readiness)

**Optimize Catalog** — Finds products with incomplete or unclear
information (missing shipping details, vague specs) and fixes their
readiness score so an AI shopping assistant can recommend them accurately.
*Feature:* the "AI Commerce Readiness" score isn't decorative — it reflects
real gaps in real product data, and this button really closes them.

**Preview as AI Buyer** — Switches to the buyer's point of view to try the
shopping assistant yourself.

### AI Buyer (the shopping assistant, buyer-facing)

**Search** (typing a plain-English request like "a laptop for college under
₹70,000") — The assistant reads the request, figures out the budget and
use case, and matches it against real catalog data — price, stock, specs —
never invented numbers. *Feature:* natural-language shopping that's still
grounded in real inventory.

**Add to Basket / Review Purchase** — Builds a real basket with real prices
and a real bundle discount, then moves to checkout.

### Checkout

**Confirm & Pay** — The buyer explicitly authorizes the purchase. Only
*after* this click does RAYGO create a real payment order (Razorpay Test
Mode) and wait for the result. *Feature:* the AI never charges anyone
without this explicit confirmation step.

**Simulate payment failure (demo)** — Lets you see what happens when a
payment fails, without needing an actual failing card.

### Payment result

Nothing to click here — this screen exists to prove a specific safety
guarantee: **if a payment fails, RAYGO will not automatically retry it.**
The order stays unpaid, no duplicate charge is possible, and the failure is
written to the audit trail. This is one of the most important things this
application demonstrates — many "helpful" automated systems make payment
failures worse by retrying blindly; this one deliberately doesn't.

### Policies (the safety rules themselves)

**Pause / Activate** on a policy card — Turns a safety rule on or off — for
every rule except one: **Payment Retry can never be turned off.** Trying to
unlock it is rejected outright. *Feature:* this screen proves the rules
aren't just suggestions the AI happens to follow — some of them are
genuinely un-overridable, even by the merchant, even by direct API call.

### Agent Activity

Nothing to click — a live timeline of what each of the seven specialist AI
agents actually did, in order, with timestamps. *Feature:* you can watch
the system think, not just see its conclusions.

### Audit Trail

**Row click** — Opens the full decision record for one consequential
action: what was proposed, what the policy check found, whether it was
approved, and what actually happened. *Feature:* every action that moved
money or changed a recommendation can be fully reconstructed after the
fact — this is what makes the "safe AI" claims checkable rather than just
asserted.

---

## Real-world usage scenarios

These walk through how someone would actually use RAYGO, end to end,
against the real backend (`http://localhost:8000/docs`) as it stands today.

### Scenario 1 — "What should I focus on this week?" (merchant)

1. Open the Overview equivalent: `GET /dashboard/overview`. You see total
   revenue, how much of it RAYGO can take credit for, and the
   highest-confidence opportunity RAYGO has found.
2. Open that opportunity: `GET /opportunities/{id}` and
   `GET /opportunities/{id}/reasoning` for RAYGO's plain-language
   explanation of why it's confident.
3. Decide: `POST /opportunities/{id}/approve` if it looks right, or
   `POST /opportunities/{id}/reject` if not. Either way, the decision is
   now permanently on the record (`GET /audit`).

### Scenario 2 — "Did that experiment actually work?" (merchant)

1. After approving an opportunity, an experiment now exists:
   `GET /experiments/{id}`.
2. Check the numbers directly — control conversion vs. variant conversion,
   real percentages, not a vibe.
3. `POST /experiments/{id}/scale` to commit, or
   `POST /experiments/{id}/reject` to keep it running longer. Both are
   gated by the same policy check as everything else.

### Scenario 3 — "A customer wants help finding a laptop" (buyer, via AI)

1. `POST /ai-buyer/search` with their plain-English request and budget.
2. RAYGO returns a specific, real product with a real price and a plain
   explanation of why it fits — not a generic "here are some laptops."
3. `POST /ai-buyer/basket` to build the order, `POST /order-intents` to
   move to checkout.
4. `POST /payments/razorpay/order` then `POST /payments/razorpay/verify`
   to actually pay — Razorpay Test Mode, safe to run repeatedly.

### Scenario 4 — "A payment just failed — is my customer's money safe?"

1. `POST /payments/razorpay/failure` (or a real failed test-card attempt).
2. Immediately check `GET /audit` — you'll see the failure recorded *and* a
   second entry proving the automatic retry was blocked, with the reason
   ("Duplicate-charge protection") spelled out.
3. The order intent (`GET /order-intents/{id}`) is still `payment_failed`,
   not silently retried into a duplicate charge.

### Scenario 5 — "I want to change how aggressive the AI can be"

1. `GET /policies` to see all six rules and their current limits.
2. `PATCH /policies/{id}` to pause or adjust most of them.
3. Try it on Payment Retry (`policy_payment_retry`) — this one is
   deliberately rejected (`403`), no matter what you set it to. That's not
   a bug; it's the one rule this MVP has decided a merchant shouldn't be
   able to loosen from the API alone.

### Scenario 6 — "I need to explain an AI decision to someone"

1. `GET /audit` to find the action in question.
2. `GET /audit/{id}` for the full record: what was proposed, what policy
   check ran, whether a human approved it, and the outcome — everything
   needed to answer "why did the AI do that?" without guessing.

### What this doesn't cover yet

Two things aren't real-world-ready yet, and it's worth knowing that before
relying on this: there's no real login/authentication (anyone calling the
API is trusted as the demo merchant — see `docs/MANUAL_TEST_PLAN.md` →
Known Gaps), and the polished frontend screens aren't calling this backend
yet (see "Current state, honestly" above). Both are the clearly-scoped next
steps, not surprises.
