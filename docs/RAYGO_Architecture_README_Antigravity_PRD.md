# RAYGO — Architecture & README Documentation PRD

**Target:** Google Antigravity  
**Priority:** P0 — Razorpay Buildathon Submission  
**Project:** RAYGO — Autonomous Revenue Intelligence / Agentic Commerce

## Objective

Prepare the existing RAYGO repository with a judge-ready technical documentation package. Antigravity must inspect the actual codebase first, then create accurate architecture and README documentation. Do not invent capabilities or change product behavior unnecessarily.

The documentation must let a Razorpay evaluator quickly understand:

- What RAYGO is.
- How it addresses Track 01 — AI Growth & Agentic Commerce.
- How the AI-to-commerce-to-payment flow works.
- Where AI agents operate.
- How money-impacting actions are bounded and gated.
- How Razorpay payment verification works.
- How auditability and graceful failure work.
- How to run and evaluate the application.

## Source-of-Truth Rule

Inspect the actual repository before writing documentation, including:

- `apps/web`
- `apps/api`
- API routes
- services
- agents/orchestration
- repositories
- Supabase migrations/schema
- MongoDB initialization, if present
- Razorpay integration
- policy/approval logic
- audit and Agent Activity
- tests
- configuration
- existing README/docs

If existing documentation conflicts with implementation, **code wins**. Document limitations instead of inventing features.

In particular, explicitly determine which database is the actual runtime source of truth. Do not assume Supabase is authoritative merely because migrations/repositories exist.

---

# Required Deliverables

Create/update:

```text
README.md
docs/ARCHITECTURE.md
docs/architecture.mmd
docs/agent-architecture.mmd
docs/GOLDEN_DEMO.md
docs/SECURITY_AND_SAFETY.md
docs/API_OVERVIEW.md       # only if useful
```

## 1. README.md

Make the README the evaluator's entry point.

Required structure:

### RAYGO
**Autonomous Revenue Intelligence for Agentic Commerce**

### One-line value proposition

Accurately explain that RAYGO helps merchants identify revenue opportunities, expose products to AI buyers, execute controlled commerce workflows, and connect AI-driven decisions to verified Razorpay checkout.

### Problem

Explain the merchant problem concisely:

- revenue opportunities are fragmented;
- product relationships are difficult to exploit;
- AI buyers need structured product information;
- commerce actions require controls;
- payment state must not be trusted from the browser;
- merchants need visibility into what AI did and why.

### Solution

Explain the implemented layers:

1. Revenue Intelligence
2. AI Buyer / Agentic Commerce
3. Product Catalog and Recommendations
4. Basket / Checkout
5. Razorpay Payments
6. Policy / Approval Firewall
7. Agent Activity
8. Audit Trail

Only include features actually implemented.

### Razorpay Buildathon Track

State:

**Track 01 — AI Growth & Agentic Commerce**

Include an accurate mapping table:

| Buildathon Goal | RAYGO |
|---|---|
| Grow merchant revenue | Revenue opportunities / recommendations |
| AI-driven commerce | AI Buyer |
| Product discovery | Catalog |
| Upsell / cross-sell | Product relationships / recommendations |
| AI buyer transacting | Basket → Checkout |
| Controlled money actions | Policy / approval |
| Explainability | Agent reasoning/activity |
| Auditability | Audit trail |
| Graceful failure | Payment/failure recovery |

Remove any row that the codebase does not genuinely support.

### Architecture

Embed a concise architecture diagram and link to `docs/ARCHITECTURE.md`.

### Golden Demo

Prominently show:

```text
Merchant Dashboard
→ Revenue Opportunity
→ AI Reasoning
→ AI Buyer
→ Product Discovery
→ Recommendation
→ Basket
→ Razorpay Checkout
→ Server Verification
→ Order
→ Agent Activity
→ Audit Trail
```

The exact sequence must match the implemented application.

### Failure Demo

Document one real failure path, preferably Razorpay payment failure.

Conceptually:

```text
Payment Attempt
→ Failure
→ No false success
→ No duplicate order
→ Clear feedback
→ Recovery path
→ Audit event
```

Do not invent behavior.

### AI Architecture

Explain actual agents/services, their responsibilities, inputs, outputs, tools, and guards.

### Safety Model

Show:

```text
AI proposes action
→ Validation
→ Policy evaluation
→ Approval if required
→ Execution
→ Server verification
→ Audit
```

Document actual thresholds, approval states, allow-lists, idempotency, and rejection paths if present.

### Payment Architecture

Document the actual Razorpay flow:

```text
Frontend
→ RAYGO API
→ Razorpay Order
→ Razorpay Checkout
→ Payment
→ Backend verification/webhook
→ Payment state
→ Order state
→ Audit
```

Clearly state Test Mode where applicable. Never expose secrets.

### Data Architecture

Document the actual runtime database and important entities:

- Merchant
- Store
- Product
- Inventory
- Product Relationship
- Opportunity
- Experiment
- Order
- Order Item
- Payment
- Policy
- Agent Activity
- Audit Event
- Buyer Session
- Basket
- Checkout Intent

Only list entities that actually exist.

### Security

Document:

- secrets;
- authentication;
- authorization;
- input validation;
- server-side payment verification;
- webhook verification;
- idempotency;
- policy enforcement;
- approval boundaries;
- audit logging.

If authentication is demo-only, say so instead of calling it production-grade.

### Technology Stack

Generate from actual package/config files. Do not guess versions.

### Local Development

Provide verified commands for:

- installing dependencies;
- environment setup;
- database/migrations/seed;
- backend;
- frontend.

Do not invent commands.

### Environment Variables

Reference `.env.example` and list only variables actually used. Values must remain placeholders.

### Testing

Report only tests actually run and their real result.

### Deployment

Document actual deployment architecture. If URLs are unavailable in the repo, use clearly marked placeholders rather than inventing URLs.

### Evaluator Quick Start

Give an exact numbered evaluation path, ideally:

1. Open deployed app.
2. Enter demo merchant environment.
3. Open Overview.
4. Open revenue opportunity.
5. Launch AI Buyer.
6. Add recommended product(s).
7. Open Basket.
8. Checkout.
9. Complete Razorpay Test Mode payment.
10. Verify success.
11. Open Agent Activity.
12. Open Audit Trail.
13. Run the documented failure scenario.

Adjust to actual implementation.

### Differentiators

Explain, using evidence from the codebase:

- AI-to-commerce continuity;
- merchant-controlled autonomy;
- explainability;
- payment integrity;
- auditability;
- graceful failure.

---

# 2. docs/ARCHITECTURE.md

Write the deeper technical architecture.

Include:

1. System overview.
2. Frontend architecture.
3. Backend/API architecture.
4. Domain/service architecture.
5. AI architecture.
6. Policy/approval architecture.
7. Payment architecture.
8. Data architecture.
9. Audit/observability architecture.
10. Deployment architecture.
11. Request/data flow.
12. Security boundaries.
13. Known technical limitations.

Use actual module names where useful.

Include a table:

| Layer | Responsibility | Actual Implementation |
|---|---|---|

Also include:

- major API domains;
- important service dependencies;
- persistence path;
- external provider boundaries.

Do not create a fictional enterprise architecture.

---

# 3. docs/architecture.mmd

Create a clean GitHub-renderable Mermaid architecture diagram.

It should reflect the real codebase. At minimum, where implemented:

```text
Merchant
  ↓
Next.js Web
  ↓
FastAPI API
  ↓
Domain / Services
  ├── Revenue Intelligence
  ├── AI Buyer
  ├── Agent Orchestration
  ├── Policy / Approval
  ├── Orders / Basket / Checkout
  ├── Payments
  └── Audit / Activity
  ↓
External / Persistence
  ├── Actual Database
  ├── Gemini / AI Provider
  └── Razorpay Test Gateway
```

Keep it readable rather than enormous.

---

# 4. docs/agent-architecture.mmd

Create a separate AI diagram.

Use only actual agents/services.

Preferred conceptual structure:

```text
Coordinator / Orchestrator
        ↓
Specialized Agents
        ↓
Tools / Domain Services
        ↓
Policy Guard
        ↓
Approval Gateway
        ↓
Commerce / Payment Action
        ↓
Audit + Agent Activity
```

If the implementation differs, diagram the implementation instead.

---

# 5. docs/GOLDEN_DEMO.md

Create the judge's evaluation script.

Sections:

## Objective
What the evaluator should learn.

## Preconditions
Required demo state.

## Step-by-Step
Exact UI actions.

## Expected Results
What should appear after each step.

## AI Evidence
What proves AI is participating.

## Razorpay Evidence
What proves the payment integration works.

## Safety Evidence
What proves bounded/gated action behavior.

## Audit Evidence
Where to find the recorded activity.

## Failure Scenario
Exact reproducible failure path.

## Reset Procedure
Only if supported.

The Golden Demo should fit naturally into a 5-minute presentation.

---

# 6. docs/SECURITY_AND_SAFETY.md

Document:

1. Threat model overview.
2. Secret management.
3. Authentication.
4. Authorization.
5. Payment verification.
6. Webhook verification.
7. Idempotency.
8. Policy guard.
9. Approval gateway.
10. Audit trail.
11. AI output/action boundaries.
12. Failure handling.
13. Test-mode limitations.
14. Known limitations.

Never expose secret values.

---

# 7. docs/API_OVERVIEW.md

Create only if it materially improves evaluator understanding.

Summarize important API domains and flows instead of duplicating a huge OpenAPI specification.

---

# Judge-Facing Architecture Narrative

The documentation should make this story obvious:

```text
Merchant
   ↓
Revenue Intelligence
   ↓
Opportunity
   ↓
AI Reasoning
   ↓
AI Buyer
   ↓
Product Discovery
   ↓
Recommendation / Upsell
   ↓
Basket
   ↓
Checkout
   ↓
Razorpay
   ↓
Server Verification
   ↓
Order
   ↓
Agent Activity
   ↓
Audit Trail
```

Then separately show:

```text
AI Action
   ↓
Policy
   ↓
Approval (when required)
   ↓
Execution
   ↓
Verification
   ↓
Audit
```

This should communicate that RAYGO is not merely a chatbot or analytics dashboard; it is an implemented AI-to-commerce workflow with explicit controls.

---

# Accuracy and Security Rules

DO NOT:

- invent functionality;
- claim production payment processing when using Test Mode;
- claim fully autonomous payments if approval is required;
- claim production-grade authentication if it is demo-only;
- call unused infrastructure an active runtime dependency;
- expose API keys;
- expose Gemini credentials;
- expose Razorpay secrets;
- expose Supabase service-role credentials;
- copy `.env` contents into documentation;
- invent deployment URLs;
- invent performance metrics;
- invent test results;
- make unnecessary source-code changes.

If a feature is incomplete, write:

> Known Limitation: ...

rather than hiding it.

---

# Validation

Before completing the task:

- [ ] README exists and is polished.
- [ ] Architecture document exists.
- [ ] Both Mermaid diagrams exist.
- [ ] Golden Demo exists.
- [ ] Security document exists.
- [ ] Optional API overview added only if useful.
- [ ] Architecture matches actual code.
- [ ] Runtime database is unambiguous.
- [ ] AI implementation is accurately represented.
- [ ] Razorpay flow is accurately represented.
- [ ] Policy/approval behavior is accurate.
- [ ] Audit behavior is accurate.
- [ ] Authentication limitations are disclosed.
- [ ] No secrets appear in documentation.
- [ ] `.env` is not committed.
- [ ] `.env.example` contains placeholders.
- [ ] Frontend build is checked.
- [ ] Backend tests are checked.
- [ ] Mermaid syntax is sanity-checked.
- [ ] Markdown links/paths are checked.

Do not claim validation passed unless it actually passed.

---

# Direct Antigravity Execution Prompt

Use this as the implementation instruction:

> Act as the senior staff engineer preparing the existing RAYGO repository for Razorpay Buildathon evaluation.
>
> First inspect the complete repository. Trace the frontend, backend, routes, services, AI agents/orchestration, repositories, database initialization, Supabase migrations, MongoDB usage if present, Razorpay integration, policy guard, approval gateway, audit layer, Agent Activity, tests, and configuration.
>
> Determine the actual runtime architecture. Existing documentation is not authoritative if it conflicts with code.
>
> Then implement the documentation package specified in this PRD:
>
> - `README.md`
> - `docs/ARCHITECTURE.md`
> - `docs/architecture.mmd`
> - `docs/agent-architecture.mmd`
> - `docs/GOLDEN_DEMO.md`
> - `docs/SECURITY_AND_SAFETY.md`
> - `docs/API_OVERVIEW.md` only if useful
>
> Optimize the README for a Razorpay Buildathon evaluator. Make Track 01 — AI Growth & Agentic Commerce immediately visible.
>
> Clearly explain the implemented chain:
>
> Revenue Opportunity → AI Reasoning → AI Buyer → Product Discovery → Recommendation → Basket → Razorpay Checkout → Server Verification → Order → Agent Activity → Audit Trail.
>
> Clearly explain the safety chain:
>
> AI Proposal → Validation → Policy → Approval if required → Execution → Verification → Audit.
>
> Show one real graceful failure path.
>
> Resolve the actual database source of truth and document it accurately.
>
> Do not expose secrets or copy `.env` contents. Do not invent capabilities, metrics, deployment URLs, test results, or security guarantees.
>
> Do not unnecessarily modify product code. This is primarily a documentation and architecture task.
>
> Run appropriate validation after creating the documentation:
>
> - backend tests;
> - frontend build;
> - Mermaid syntax sanity check where possible;
> - Markdown path/link verification;
> - repository secret scan or equivalent sanity check.
>
> Finally report:
>
> 1. Files created/updated.
> 2. Actual architecture discovered.
> 3. Actual database source of truth.
> 4. AI architecture discovered.
> 5. Razorpay payment flow.
> 6. Policy/approval controls.
> 7. Validation performed and results.
> 8. Any limitations that should be disclosed to judges.
>
> Do not stop at generating Markdown. Verify internal consistency across README, architecture diagrams, Golden Demo, and the actual codebase.

---

# Definition of Done

The task is complete when:

- a Razorpay evaluator can understand RAYGO from the README in under 3 minutes;
- the technical architecture is documented accurately;
- diagrams render on GitHub;
- the Golden Demo gives an exact evaluation path;
- the AI role is clear;
- money-action controls are clear;
- Razorpay payment verification is clear;
- the runtime database is unambiguous;
- the failure path is documented;
- security limitations are truthful;
- no secrets are exposed;
- tests/build validation has been performed;
- no unsupported claims remain.

**Priority:** Accuracy > completeness > visual polish.

**Submission principle:** A smaller, fully truthful architecture is stronger than a larger fictional architecture.
