# RAYGO — Final Buildathon Completion Master PRD
## Claude Prompt-Generation Specification for Google Antigravity

**Project:** RAYGO — Autonomous Revenue Intelligence  
**Buildathon:** Razorpay AI Builder Internship 2026 — Track 01: AI Growth & Agentic Commerce  
**Deadline:** TODAY — evening submission  
**Claude role:** Analyze the repository and generate implementation/build PRDs  
**Builder:** Google Antigravity  
**Priority:** P0 — demo reliability and submission readiness

---

## 0. Executive Directive

This document is **not** an instruction for Claude to build the application.

Claude must:

1. Inspect the supplied RAY-GO repository.
2. Understand the actual implementation.
3. Compare it against this roadmap and previous PRDs.
4. Identify completed, partial, mocked, broken, and missing work.
5. Generate implementation-ready PRDs/prompts.
6. The user will give those PRDs to Google Antigravity.
7. Antigravity performs implementation, testing, debugging, and integration.

Do not duplicate existing work. Do not rewrite stable architecture. Do not introduce unnecessary infrastructure.

**The deadline is today. A smaller fully working vertical slice is more valuable than a larger partially working system.**

---

# 1. One-Day Release Strategy

The priority order is:

```text
P0 — MUST WORK
Frontend
 ↓
Backend
 ↓
Supabase persistence
 ↓
Catalog + inventory
 ↓
AI Buyer
 ↓
Basket
 ↓
Purchase Review
 ↓
Razorpay Checkout
 ↓
Server payment verification
 ↓
Success/failure/dismissal states
 ↓
Policy + approval
 ↓
Agent Activity
 ↓
Audit Trail
 ↓
One reliable end-to-end demo
```

Only after P0 is stable:

```text
P1
Phase 8 completion
Phase 9 completion
Phase 10 completion
Performance polish
Evaluation
```

Do not sacrifice checkout reliability to add optional features.

---

# 2. Current Phase Position

The major RAYGO product is already represented by the earlier phases:

```text
Phase 1–3
Foundation / backend / payment foundation

Phase 4
Revenue Intelligence

Phase 5
Agentic Commerce / AI Buyer

Phase 6–7
Growth experiments + safety/evaluation/core agent integration

Phase 8
Revenue Recovery & Payment Resilience

Phase 9
Merchant Copilot

Phase 10
Agent Orchestration + Evaluation
```

Phases **8, 9 and 10 are already in progress**.

Therefore Claude must **not restart them**.

Claude must inspect their current implementation and generate only gap-completion instructions.

---

# 3. Source of Truth

Use:

```text
RAY-GO_CLAUDE_ANALYSIS_SAFE.zip
```

and the current repository supplied by the user.

Precedence:

```text
actual code
    >
actual tests/runtime wiring
    >
current documentation
    >
previous PRDs
```

A file existing does not prove a feature works.

A test existing does not prove a real external integration works.

A README claim does not prove runtime wiring.

For every capability determine:

```text
implemented?
wired?
persistent?
real or mocked?
tested?
demo-ready?
```

---

# 4. Mandatory Current-State Matrix

Before generating build prompts, Claude must produce:

| Capability | Code | Wired | Persistent | Real/Mock | Tested | Demo Ready | Gap |
|---|---|---|---|---|---|---|---|
| Supabase | | | | | | | |
| Catalog | | | | | | | |
| Inventory | | | | | | | |
| Orders | | | | | | | |
| Payments | | | | | | | |
| Razorpay | | | | | | | |
| Revenue Intelligence | | | | | | | |
| AI Buyer | | | | | | | |
| Compatibility | | | | | | | |
| Experiments | | | | | | | |
| Policy Guard | | | | | | | |
| Approval Gateway | | | | | | | |
| Agent Activity | | | | | | | |
| Audit Trail | | | | | | | |
| Phase 8 | | | | | | | |
| Phase 9 | | | | | | | |
| Phase 10 | | | | | | | |

---

# 5. Target Final Product Story

The final application must demonstrate one coherent flow:

```text
Merchant
 ↓
Store/catalog
 ↓
RAYGO analyzes commerce data
 ↓
Revenue opportunity
 ↓
AI reasoning + evidence
 ↓
Policy Guard
 ↓
Merchant approval
 ↓
Experiment
 ↓
Measured result
 ↓
AI Commerce readiness
 ↓
AI Buyer
 ↓
Natural-language purchase intent
 ↓
Product discovery
 ↓
Compatibility validation
 ↓
Basket
 ↓
Purchase Review
 ↓
Explicit authorization
 ↓
Razorpay Checkout
 ↓
Payment
 ↓
Server verification
 ↓
Paid Order
 ↓
Agent Activity
 ↓
Audit Trail
```

This is the primary buildathon story.

---

# 6. Architecture Rules

Target architecture:

```text
Next.js
   |
   v
FastAPI
   |
   +------------------+
   |                  |
   v                  v
Supabase            Gemini
PostgreSQL          AI reasoning
   |
   +-- Catalog
   +-- Inventory
   +-- Orders
   +-- Payments
   +-- Opportunities
   +-- Experiments
   +-- Policies
   +-- Agent Activity
   +-- Audit
   +-- Buyer Sessions
   +-- Baskets
   +-- Checkout Intents

FastAPI
   |
   v
Razorpay
```

Authority:

```text
Supabase = persistent application state
Backend = business rules + authorization
Gemini = reasoning
Policy Guard = action boundary
Merchant = business authority
Razorpay = payment authority
Audit = traceability
```

AI must never become the source of truth for:

```text
price
inventory
order total
payment status
authorization
```

---

# 7. Phase 8 — Gap Completion
## Revenue Recovery & Payment Resilience

Phase 8 is already being built.

Claude must inspect and complete only missing pieces.

Required:

- payment failure state;
- checkout dismissal state;
- uncertain payment state;
- duplicate-payment protection;
- server-side verification;
- webhook reconciliation;
- recovery recommendation;
- Policy Guard blocking unsafe automatic retry;
- Agent Activity;
- Audit Trail;
- safe recovery UI.

Target:

```text
Payment failure
 ↓
Classification
 ↓
Policy
 ↓
Safe recommendation
 ↓
No duplicate charge
 ↓
Audit
```

Do not automatically retry payments unless an explicit authorized policy permits it.

---

# 8. Phase 9 — Gap Completion
## Merchant Copilot

Phase 9 is already being built.

Claude must inspect existing coordinator/Copilot functionality and complete only high-value missing capabilities.

The merchant should be able to ask questions such as:

```text
What is driving revenue?
What are my top opportunities?
Why was this opportunity recommended?
Which experiment is performing best?
What happened to this payment?
What needs my approval?
```

Answers must use real application data.

Action flow:

```text
Merchant request
 ↓
Intent
 ↓
Tool
 ↓
Verified data
 ↓
Policy
 ↓
Approval when required
 ↓
Execution
 ↓
Audit
```

Do not create a generic chatbot.

---

# 9. Phase 10 — Gap Completion
## Agent Orchestration + Evaluation

Phase 10 is already being built.

Complete the smallest reliable orchestration layer.

Visible chain:

```text
Revenue Intelligence
 ↓
Growth Strategist
 ↓
Policy Guard
 ↓
Approval
 ↓
Experiment
```

and:

```text
AI Commerce
 ↓
Catalog
 ↓
Compatibility
 ↓
Basket
 ↓
Payment
 ↓
Audit
```

Each consequential run should have:

```text
correlation_id
agent_run_id
agent
status
tool calls
policy result
approval result
outcome
```

Do not persist hidden chain-of-thought.

---

# 10. Phase 11 — Production Reliability & Performance

This is the first major new phase after 8–10.

## Objective

Make RAYGO a stable release candidate.

### P0

Verify:

```text
frontend starts
backend starts
Supabase connects
environment validation works
health endpoint works
```

API:

- normalized errors;
- request validation;
- bounded timeouts;
- no uncaught exceptions;
- no duplicate mutations.

Database:

- migrations work;
- constraints work;
- indexes work;
- ownership works;
- no accidental in-memory business source of truth.

Frontend:

- no broken routes;
- no hydration errors;
- no infinite loading;
- no unnecessary full reload;
- proper loading/error/empty states.

### Performance

Measure before changing.

Look for:

```text
N+1 queries
duplicate Supabase calls
duplicate Gemini calls
oversized payloads
unnecessary rerenders
blocking operations
slow endpoints
```

Prefer:

```text
parallel async I/O
indexes
server-side aggregation
safe caching
request deduplication
pagination
lazy loading
bounded AI calls
```

Never use stale cache as final authority for:

```text
payment status
final checkout amount
live inventory
payment verification
```

---

# 11. Phase 12 — Security & Safety Release Gate

This phase is mandatory.

Verify that these never appear in frontend code, logs, AI prompts, or API responses:

```text
Supabase secret key
database password
Gemini API key
Razorpay secret
webhook secret
```

Test:

```text
merchant isolation
authorization bypass
AI privilege escalation
prompt injection
invalid tool arguments
malformed AI output
hallucinated product
hallucinated price
hallucinated inventory
policy bypass
```

Backend must prevent:

```text
frontend marking payment paid
AI changing payment state
AI bypassing Policy Guard
AI directly calling privileged Razorpay operations
```

---

# 12. Phase 13 — Golden Demo & Failure Demo

This phase is mandatory for today's deadline.

Create one deterministic judge-ready demo.

## Golden path

```text
1. Open RAYGO
2. Dashboard loads
3. Show revenue opportunity
4. Open opportunity
5. Show evidence/reasoning
6. Approve experiment
7. Show experiment result
8. Open AI Commerce
9. Open AI Buyer
10. Enter buyer request
11. Show real product recommendation
12. Add to basket
13. Review purchase
14. Confirm & Pay
15. Razorpay Checkout opens
16. Complete Test Mode payment
17. Backend verifies payment
18. Show successful order
19. Show Agent Activity
20. Show Audit Trail
```

Do not make the golden path depend on unpredictable model behavior.

Use deterministic seeded data and safe fallbacks where appropriate.

## Failure path

```text
AI Buyer
 ↓
Checkout
 ↓
Payment failure
 ↓
RAYGO detects/classifies
 ↓
Retry blocked
 ↓
Safe recovery recommendation
 ↓
Audit
```

This demonstrates resilience and safety.

---

# 13. Phase 14 — Buildathon UI/Product Polish

Do targeted polish only.

Fix:

- broken buttons;
- broken spacing;
- inconsistent loading;
- unclear status labels;
- missing empty states;
- poor error messages;
- obvious responsive issues;
- inconsistent currency/date formatting;
- visible console/runtime errors.

Preserve the existing RAYGO visual language.

Do not redesign the entire application.

Judge-facing terms should remain consistent:

```text
RAYGO
Revenue Intelligence
AI Commerce
AI Buyer
Policy Guard
Agent Activity
Audit Trail
```

---

# 14. Phase 15 — Final Evaluation & Submission Readiness

Evaluate:

## Revenue Intelligence

```text
opportunity grounded?
evidence shown?
confidence present?
policy checked?
```

## AI Buyer

```text
intent understood?
real product?
real price?
real inventory?
compatibility verified?
```

## Payment

```text
correct amount?
Razorpay Checkout opens?
server verification?
duplicate protection?
failure state?
dismissal state?
audit?
```

## Safety

```text
policy enforced?
approval enforced?
AI has no financial authority?
secrets protected?
```

## Reliability

```text
golden path passes?
failure path passes?
no critical console errors?
no backend crashes?
```

---

# 15. Automated Test Gate

Antigravity must run:

```text
unit tests
integration tests
API tests
database tests
AI contract tests
policy tests
payment tests
security tests
E2E tests
regression tests
```

Critical E2E:

```text
AI Buyer
 → Basket
 → Review
 → Razorpay
 → Verify
 → Paid Order
```

Critical failure E2E:

```text
AI Buyer
 → Checkout
 → Payment Failure
 → Safe Recovery
```

Do not report tests as passing unless actually executed.

---

# 16. Performance / MNC-Quality Requirement

The application should feel responsive and stable.

Target guidelines:

```text
Dashboard API: preferably < 1.5s
Normal CRUD API: preferably < 1s
Checkout preparation: preferably < 2s
Razorpay Checkout opening: preferably < 3s
Payment verification: preferably < 2s
Simple deterministic Copilot query: preferably < 1.5s
AI reasoning: preferably < 5s
```

Do not fake timing.

If a target cannot be met, identify the bottleneck and preserve correctness.

---

# 17. Error UX

Never reduce known errors to:

```text
Something went wrong.
```

Use:

```text
What happened
What RAYGO did
What the user can safely do next
```

Example:

```text
Payment could not be completed.

RAYGO blocked an automatic retry to prevent a duplicate charge.

Try another payment method or return to your basket.
```

---

# 18. Correlation / Observability

Critical operations should carry:

```text
correlation_id
```

It should connect:

```text
buyer session
checkout intent
order
payment
agent run
policy decision
approval
audit event
```

Never log secrets.

---

# 19. Claude's Required Output

After analyzing the repository, Claude must generate implementation-ready PRDs for Google Antigravity.

Recommended outputs:

```text
PRD-A
Phase 8–10 Gap Completion

PRD-B
Phase 11 Production Reliability + Performance

PRD-C
Phase 12 Security + Safety

PRD-D
Phase 13 Golden Demo + Failure Demo

PRD-E
Phase 14 Buildathon Product Polish

PRD-F
Phase 15 Final Evaluation + Submission Readiness
```

If the repository shows that multiple phases are already complete, Claude must merge them and reduce the number of build prompts.

**Do not generate duplicate work.**

---

# 20. Required Structure of Every Generated Build PRD

Every Claude-generated implementation PRD must contain:

```text
1. Objective
2. Verified current state
3. Existing implementation to reuse
4. Scope
5. Non-goals
6. Architecture
7. Files/modules to inspect
8. Files/modules likely to modify
9. Database changes
10. API contracts
11. Frontend changes
12. AI/agent changes
13. Security
14. Performance
15. Automated tests
16. E2E tests
17. Failure handling
18. Implementation order
19. Acceptance criteria
20. Definition of Done
21. Rollback/safe-failure behavior
22. P0/P1 priority
```

---

# 21. Antigravity Implementation Contract

Every generated PRD must explicitly tell Antigravity:

> Inspect the repository before modifying anything.

> Preserve working architecture.

> Implement the smallest production-quality change.

> Reuse existing modules.

> Do not rebuild completed features.

> Run relevant automated tests after each major change.

> Run the full regression suite before completion.

> Fix regressions before adding optional enhancements.

> Never expose secrets.

> Never claim success without executing tests.

> Do not replace real integrations with mocks merely to make the application appear functional.

> Do not remove existing safety controls.

---

# 22. Final Priority Matrix

| Priority | Work |
|---|---|
| **P0** | Make existing application run reliably |
| **P0** | Supabase/backend persistence |
| **P0** | AI Buyer |
| **P0** | Basket + checkout |
| **P0** | Razorpay Checkout + verification |
| **P0** | Policy + approval |
| **P0** | Agent Activity + Audit |
| **P0** | Golden E2E |
| **P0** | Security gate |
| **P1** | Phase 8 recovery |
| **P1** | Phase 9 Copilot |
| **P1** | Phase 10 orchestration/evaluation |
| **P1** | Performance polish |
| **P1** | UI polish |
| **P2** | Advanced campaigns/analytics/infrastructure |

---

# 23. Final Judge Narrative

The application should make this statement obvious:

> **RAYGO helps merchants discover revenue opportunities, safely test growth actions, and become transactable by AI buyers.**

Demonstrate:

```text
RAYGO finds opportunity
 ↓
Explains evidence
 ↓
Merchant approves
 ↓
RAYGO measures
 ↓
AI buyer discovers product
 ↓
Compatibility checked
 ↓
Basket prepared
 ↓
Buyer authorizes
 ↓
Razorpay processes payment
 ↓
Backend verifies payment
 ↓
Agent Activity explains the process
 ↓
Audit Trail records the consequential actions
```

---

# 24. Final Release Gate

Do not call RAYGO submission-ready until:

- [ ] frontend starts
- [ ] backend starts
- [ ] Supabase connects
- [ ] catalog loads
- [ ] inventory works
- [ ] orders persist
- [ ] AI Buyer works
- [ ] basket works
- [ ] compatibility works
- [ ] purchase review works
- [ ] Razorpay Checkout opens
- [ ] payment verification works
- [ ] payment failure is correct
- [ ] dismissal is correct
- [ ] duplicate payment is prevented
- [ ] Policy Guard works
- [ ] merchant approval works
- [ ] Agent Activity works
- [ ] Audit Trail works
- [ ] secrets are protected
- [ ] golden E2E passes
- [ ] failure E2E passes
- [ ] full regression suite passes
- [ ] demo/deployed environment works

---

# 25. Final Instruction to Claude

**Do not build the application.**

**Do not restart RAYGO.**

**Do not rewrite completed phases.**

**Analyze the actual repository.**

**Complete the currently unfinished parts of Phases 8–10 only where necessary.**

**Generate implementation PRDs for Phases 11–15.**

**Those PRDs will be implemented by Google Antigravity.**

The optimization function for today's deadline is:

```text
MAXIMIZE:
working product
+
reliable demo
+
real Razorpay flow
+
real AI Buyer
+
explainable agents
+
policy safety
+
auditability
+
speed

MINIMIZE:
new architecture
+
unnecessary code
+
risk
+
unverified features
+
time
```

**If a feature already works, leave it alone. If it is broken, fix it. If it is missing and directly strengthens the Track 01 demo, implement it. Everything else waits.**
