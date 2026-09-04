# RAYGO Backend Implementation PRD
## Phase 3 Backend MVP and Backend Prerequisites for Gemini + Google ADK

Date: 2026-08-31  
Product: RAYGO  
Track: Razorpay AI Builder Internship 2026, Track 1: AI Growth & Agentic Commerce  
Primary consumer: the completed RAYGO frontend built from `RAYGO_Claude_Frontend_First_Implementation_PRD.md`  
Implementation target: Claude Code

---

## 1. Executive Summary

RAYGO is an AI growth and agentic commerce platform for merchants. The completed frontend already defines the user-facing experience, routes, glassmorphism visual system, demo data, and interaction states. This PRD specifies the backend implementation required to replace frontend mock data with real FastAPI endpoints, MongoDB persistence, policy-gated workflows, auditability, deterministic agent stubs, and Razorpay Test Mode payment boundaries.

This document is not a redesign brief. Do not alter the completed glassmorphism UI, navigation, layout, wording, or frontend information architecture unless a backend integration issue makes a change unavoidable and the change is approved separately.

The backend must make the completed frontend smoother by providing stable, typed, low-latency, predictable responses for the existing frontend contract. The MVP should be demo-ready first, production-shaped second, and designed so the later Gemini + Google ADK phase can be added without rewriting core business logic.

---

## 2. Product Context To Preserve

Preserve all existing RAYGO terminology and domain concepts:

- RAYGO
- NovaTech Store
- Revenue Intelligence Agent
- Growth Strategist
- Experiment Agent
- AI Commerce Agent
- Policy Guard
- Approval Gateway
- Payment Agent
- Revenue Action Firewall
- AI Commerce Readiness
- AI Buyer
- Ask RAYGO
- Opportunity Center
- Audit Trail
- Razorpay Test Mode

Preserve the completed frontend routes:

```text
/onboarding
/overview
/opportunities
/opportunities/:id
/experiments
/experiments/:id
/ai-commerce
/ai-buyer
/checkout/:orderIntentId
/payment/success
/payment/failure
/products
/orders
/payments
/agents
/policies
/audit
/audit/:id
```

Preserve the core demo values:

```json
{
  "merchant": {
    "id": "merchant_novatech",
    "name": "NovaTech Store",
    "category": "Consumer Electronics",
    "currency": "INR"
  },
  "metrics": {
    "totalRevenue": 284620,
    "revenueGrowthPct": 18.7,
    "raygoInfluencedRevenue": 42800,
    "raygoLiftPct": 14.2,
    "activeOpportunities": 7,
    "aiCommerceReadiness": 82,
    "projectedOpportunityImpact": 40000
  },
  "primaryOpportunityId": "opp_keyboard_stand",
  "primaryExperimentId": "exp_keyboard_stand",
  "orderIntentId": "intent_ai_setup_001",
  "displayOrderId": "#RGO-10482",
  "checkoutTotal": 68499,
  "currency": "INR"
}
```

Preserve the required payment failure semantics:

- `AUTOMATIC RETRY: BLOCKED`
- Reason: `Duplicate-charge protection`
- No duplicate payment attempted
- Order remains unpaid
- Inventory unchanged
- Failure recorded in audit trail
- Recovery option generated

---

## 3. Objectives

1. Implement a FastAPI backend under `/api/v1` that satisfies the completed frontend's mock API assumptions.
2. Persist all consequential state in MongoDB: merchants, products, opportunities, experiments, policies, approvals, agent runs, order intents, payment attempts, Razorpay orders, webhooks, and audit events.
3. Seed deterministic demo data so the RAYGO judge flow works immediately after setup.
4. Enforce Policy Guard before every consequential action.
5. Require explicit Approval Gateway confirmation before creating experiments, scaling experiments, and executing payments.
6. Implement Razorpay Test Mode service boundaries: server-side order creation, server-side signature verification, webhook signature validation, idempotent webhook processing, and no automatic retry after failure.
7. Provide deterministic agent interfaces/stubs that mirror the future Gemini + Google ADK integration shape.
8. Create an auditable system where every meaningful AI, policy, approval, experiment, order, and payment transition is reconstructable without exposing hidden reasoning.
9. Make frontend integration smooth: stable response shapes, predictable status values, CORS setup, useful errors, correlation IDs, fast seeded responses, and compatibility with the current UI routes.

---

## 4. Scope

### In Scope For Phase 3 Backend MVP

- FastAPI application setup.
- `/api/v1` router structure.
- MongoDB connection via Motor or Beanie.
- Pydantic request/response schemas.
- Demo seed/reset flow.
- Merchant and onboarding endpoints.
- Dashboard overview endpoint.
- Products endpoint for catalog screen.
- Opportunities endpoints.
- Approval flow for opportunity-to-experiment creation.
- Experiments endpoints.
- Experiment scale flow.
- AI Commerce readiness and product profile endpoints.
- AI Buyer search, basket, and order-intent endpoints.
- Orders and payments read endpoints.
- Policy list, patch, and evaluation endpoints.
- Agents status/activity endpoints using deterministic data.
- Audit list/detail endpoints.
- Policy Guard service.
- Approval Gateway service.
- Audit Service.
- Deterministic agent service stubs.
- Error handling, validation, idempotency, logging, and correlation IDs.
- `.env.example`, README backend setup, and tests.

### In Scope As Backend Prerequisite For Phase 4

- Razorpay service abstraction.
- Payment order creation endpoint.
- Payment verification endpoint.
- Payment failure endpoint.
- Razorpay webhook endpoint.
- Test Mode-only enforcement.
- Idempotent payment and webhook storage.
- Signature verification implementation or clearly isolated integration stub if keys are absent locally.

### In Scope As Backend Prerequisite For Later Gemini + Google ADK

- Typed agent action interfaces.
- `GeminiService` placeholder behind feature flag.
- `ADKOrchestrator` placeholder behind feature flag.
- Pydantic schemas for agent input/output.
- Agent run persistence.
- Audit hooks around agent outputs.
- Policy validation after any AI-suggested action and before execution.

---

## 5. Non-Scope

- Redesigning or rebuilding the glassmorphism frontend.
- Changing frontend route names or visible demo wording.
- Replacing FastAPI, MongoDB, Razorpay, Gemini, or Google ADK with another stack.
- Building long chatbot history for Ask RAYGO.
- Letting Gemini or ADK directly call Razorpay, mutate policies, create experiments, issue refunds, or retry payments.
- Real money payment mode.
- Refund execution.
- Automatic payment retry.
- Full merchant settings outside policy controls.
- Production authentication/authorization beyond demo-safe structure.
- Multi-tenant billing, subscription plans, or marketplace onboarding.
- Background job infrastructure unless needed for clean webhook reconciliation.

---

## 6. Required Stack

Use the stack defined by the frontend-first PRD:

```text
Backend: FastAPI
Language: Python 3.11+
Database: MongoDB
Mongo client: Motor or Beanie
Validation: Pydantic v2
Payments: Razorpay Test Mode, Razorpay Python SDK or direct HTTP client
AI later: Gemini
Agent framework later: Google ADK
Testing: pytest, pytest-asyncio, httpx/ASGITransport
Deployment target: Render, Railway, Fly.io, or similar
Production DB target: MongoDB Atlas
```

Do not substitute Express, PostgreSQL, Firebase, Supabase, Stripe, or a different agent framework unless the user changes the stack later.

---

## 7. Architecture

### High-Level Architecture

```text
Completed Next.js Frontend
  -> typed API client
  -> FastAPI /api/v1
  -> route validators
  -> domain services
  -> Policy Guard / Approval Gateway
  -> MongoDB repositories
  -> Audit Service
  -> Razorpay Service boundary
  -> deterministic agent stubs
  -> future Gemini + Google ADK seam
```

### Backend Ownership Rules

- API routes validate request payloads, parse route parameters, and call services.
- Services own domain behavior.
- Repositories own persistence details.
- Policy Guard is called before every consequential action.
- Approval Gateway records explicit merchant approval.
- Audit Service records all state transitions and consequential decisions.
- Razorpay Service is the only backend module that knows Razorpay credentials.
- Gemini and ADK are never allowed to manipulate payment or policy APIs directly.

### Consequential Actions

The following actions must pass Policy Guard and write audit events:

- Opportunity approval.
- Experiment creation.
- Experiment scaling.
- Catalog optimization.
- AI buyer search completion.
- Order intent creation.
- Razorpay order creation.
- Payment verification.
- Payment failure recording.
- Payment retry prevention.
- Policy update.
- Any future Gemini/ADK-suggested action.

---

## 8. Repository Structure

Use the existing monorepo shape from the frontend-first PRD. Add the backend under `apps/api`.

```text
raygo/
  apps/
    web/
    api/
      app/
        main.py
        core/
          config.py
          errors.py
          logging.py
          security.py
          idempotency.py
        api/
          v1/
            router.py
            merchant.py
            dashboard.py
            products.py
            opportunities.py
            experiments.py
            ai_commerce.py
            ai_buyer.py
            payments.py
            policies.py
            agents.py
            audit.py
            health.py
        domain/
          models.py
          schemas.py
          states.py
          constants.py
        services/
          merchant_service.py
          dashboard_service.py
          product_service.py
          revenue_intelligence.py
          growth_strategist.py
          experiment_agent.py
          ai_commerce_agent.py
          ai_buyer_service.py
          order_intent_service.py
          policy_guard.py
          approval_gateway.py
          payment_agent.py
          audit_service.py
          razorpay_service.py
          gemini_service.py
          adk_orchestrator.py
        repositories/
          base.py
          merchants.py
          products.py
          opportunities.py
          experiments.py
          policies.py
          approvals.py
          agents.py
          audit.py
          orders.py
          payments.py
          idempotency.py
        db/
          mongo.py
          indexes.py
          seed.py
        tests/
          conftest.py
          test_health.py
          test_seed.py
          test_opportunities.py
          test_experiments.py
          test_policies.py
          test_ai_buyer.py
          test_payments.py
          test_audit.py
      requirements.txt
      README.md
  packages/
    shared/
      contracts/
        api.ts
        domain.ts
  docs/
    api-contract.md
  .env.example
  README.md
```

If the existing repository already has a strong convention, preserve it, but do not collapse all backend logic into route files.

---

## 9. FastAPI Setup

### Application Requirements

- App title: `RAYGO API`
- Version: `0.1.0`
- Base route prefix: `/api/v1`
- JSON only.
- CORS allows `FRONTEND_ORIGIN`.
- Include request correlation ID in every response as `X-Request-ID`.
- Include response envelope only where useful; avoid breaking frontend assumptions if it expects direct objects.
- Expose OpenAPI during local/demo mode.

### Required Startup Behavior

On startup:

1. Load settings.
2. Connect to MongoDB.
3. Ensure indexes.
4. Optionally seed demo data if `SEED_ON_STARTUP=true`.
5. Log environment name, mock-agent mode, database name, and Razorpay mode without printing secrets.

### Required Health Endpoints

```text
GET /api/v1/health
GET /api/v1/health/db
```

`GET /api/v1/health` response:

```json
{
  "status": "ok",
  "service": "raygo-api",
  "version": "0.1.0",
  "environment": "local"
}
```

`GET /api/v1/health/db` response:

```json
{
  "status": "ok",
  "database": "raygo",
  "connected": true
}
```

---

## 10. Configuration And Environment Variables

Create `.env.example` at repo root and, if useful, `apps/api/.env.example`.

```text
ENVIRONMENT=local
API_HOST=0.0.0.0
API_PORT=8000
API_BASE_URL=http://localhost:8000/api/v1
FRONTEND_ORIGIN=http://localhost:3000

MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=raygo
SEED_ON_STARTUP=true
ALLOW_DEMO_RESET=true

RAZORPAY_MODE=test
RAZORPAY_KEY_ID=
RAZORPAY_KEY_SECRET=
RAZORPAY_WEBHOOK_SECRET=

GEMINI_API_KEY=
USE_MOCK_AGENTS=true
USE_ADK_ORCHESTRATOR=false

LOG_LEVEL=INFO
REQUEST_TIMEOUT_SECONDS=30
IDEMPOTENCY_TTL_HOURS=24
```

Frontend env preserved:

```text
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_RAZORPAY_KEY_ID=
```

Validation rules:

- `RAZORPAY_MODE` must be `test` for MVP.
- If payment endpoints are called without Razorpay keys, return a clear configuration error unless `ALLOW_RAZORPAY_STUB=true` is explicitly added for local-only demo fallback.
- Never log secrets.
- Never expose `RAZORPAY_KEY_SECRET`, `RAZORPAY_WEBHOOK_SECRET`, `MONGODB_URI`, or `GEMINI_API_KEY` to the frontend.

---

## 11. MongoDB Collections And Indexes

Use application-level IDs such as `merchant_novatech`, `opp_keyboard_stand`, and `intent_ai_setup_001` as public IDs. MongoDB `_id` may remain ObjectId or mirror the public ID, but API responses must use `id`.

### Collections

```text
merchants
products
dashboard_snapshots
opportunities
experiments
policies
policy_evaluations
approvals
agent_runs
agent_activity
buyer_intents
baskets
order_intents
orders
razorpay_orders
payment_attempts
webhook_events
audit_events
idempotency_records
```

### Common Fields

Every persisted domain document should include:

```json
{
  "id": "string",
  "createdAt": "2026-08-31T11:32:04Z",
  "updatedAt": "2026-08-31T11:32:04Z",
  "status": "string",
  "metadata": {}
}
```

Use camelCase in API JSON. Internal Python models may use snake_case, but responses must serialize to camelCase unless the frontend already expects otherwise.

### Indexes

| Collection | Index | Unique | Purpose |
| --- | --- | --- | --- |
| `merchants` | `id` | yes | Merchant lookup |
| `products` | `id` | yes | Product lookup |
| `products` | `merchantId`, `status` | no | Catalog screen |
| `opportunities` | `id` | yes | Detail lookup |
| `opportunities` | `merchantId`, `status`, `confidence` | no | Ranked list |
| `experiments` | `id` | yes | Detail lookup |
| `experiments` | `merchantId`, `opportunityId` | no | Opportunity linkage |
| `policies` | `id` | yes | Policy patch/evaluate |
| `policy_evaluations` | `id` | yes | Audit correlation |
| `policy_evaluations` | `merchantId`, `actionType`, `createdAt` | no | Policy history |
| `approvals` | `id` | yes | Approval lookup |
| `approvals` | `merchantId`, `targetType`, `targetId` | no | Approval history |
| `agent_runs` | `id` | yes | Agent run lookup |
| `agent_runs` | `agentName`, `status`, `createdAt` | no | Agent activity |
| `agent_activity` | `id` | yes | Timeline lookup |
| `agent_activity` | `timestamp` | no | Timeline sorting |
| `buyer_intents` | `id` | yes | Buyer search history |
| `order_intents` | `id` | yes | Checkout route |
| `order_intents` | `displayOrderId` | yes | Orders screen |
| `orders` | `id` | yes | Orders list |
| `orders` | `merchantId`, `status`, `createdAt` | no | Orders screen |
| `razorpay_orders` | `razorpayOrderId` | yes | Payment reconciliation |
| `payment_attempts` | `id` | yes | Payment attempt lookup |
| `payment_attempts` | `razorpayPaymentId` | sparse unique | Signature verification |
| `payment_attempts` | `orderIntentId`, `status` | no | Payment state |
| `webhook_events` | `razorpayEventId` | yes | Idempotent webhooks |
| `audit_events` | `id` | yes | Audit detail |
| `audit_events` | `timestamp` | no | Audit list sorting |
| `audit_events` | `merchantId`, `severity`, `timestamp` | no | Audit filters |
| `idempotency_records` | `key`, `route`, `requestHash` | yes | Safe retries |
| `idempotency_records` | `expiresAt` | ttl | Cleanup |

---

## 12. Domain Models

### Merchant

```json
{
  "id": "merchant_novatech",
  "name": "NovaTech Store",
  "category": "Consumer Electronics",
  "currency": "INR",
  "status": "active",
  "createdAt": "2026-08-31T11:32:04Z",
  "updatedAt": "2026-08-31T11:32:04Z",
  "metadata": {
    "demo": true
  }
}
```

### Product

```json
{
  "id": "prod_wireless_keyboard",
  "merchantId": "merchant_novatech",
  "name": "Wireless Keyboard",
  "price": 2499,
  "currency": "INR",
  "inventory": 86,
  "aiReadiness": 89,
  "issues": [],
  "status": "ready",
  "marginPct": 38,
  "createdAt": "2026-08-31T11:32:04Z",
  "updatedAt": "2026-08-31T11:32:04Z",
  "metadata": {}
}
```

### Opportunity

```json
{
  "id": "opp_keyboard_stand",
  "merchantId": "merchant_novatech",
  "title": "Cross-sell opportunity: Wireless Keyboard -> Laptop Stand",
  "shortTitle": "Keyboard + Stand",
  "type": "cross_sell",
  "expectedMonthlyImpact": 18400,
  "confidence": 87,
  "risk": "low",
  "status": "ready_for_review",
  "currentAttachRate": 4.1,
  "projectedAttachRate": 7.8,
  "targetSegment": "Remote Workers",
  "eligibleJourneys": 1842,
  "evidence": [
    "Wireless Keyboard buyers frequently view Laptop Stand within the same journey.",
    "Laptop Stand inventory is constrained but available.",
    "Projected attach-rate increase stays within margin policy."
  ],
  "recommendedAction": "Create a 10% Keyboard + Laptop Stand bundle experiment.",
  "createdAt": "2026-08-31T11:32:04Z",
  "updatedAt": "2026-08-31T11:32:04Z",
  "metadata": {}
}
```

### Experiment

```json
{
  "id": "exp_keyboard_stand",
  "merchantId": "merchant_novatech",
  "opportunityId": "opp_keyboard_stand",
  "name": "Keyboard + Laptop Stand",
  "status": "running",
  "hypothesis": "Bundling a Laptop Stand with Wireless Keyboard purchases will increase basket conversion without reducing merchant margin below policy.",
  "controlConversion": 6.2,
  "variantConversion": 8.9,
  "conversionUplift": 43.5,
  "revenueUplift": 23.4,
  "aovUplift": 8.7,
  "confidence": 94,
  "recommendation": "scale_variant",
  "createdAt": "2026-08-31T11:32:08Z",
  "updatedAt": "2026-08-31T11:32:08Z",
  "metadata": {
    "discountPct": 10
  }
}
```

### Policy

```json
{
  "id": "policy_discount_limit",
  "merchantId": "merchant_novatech",
  "name": "Discount Limit",
  "limit": "20%",
  "status": "active",
  "ruleType": "discount_max_pct",
  "value": 20,
  "enforcement": "block",
  "createdAt": "2026-08-31T11:32:04Z",
  "updatedAt": "2026-08-31T11:32:04Z",
  "metadata": {}
}
```

### PolicyEvaluation

```json
{
  "id": "pol_eval_001",
  "merchantId": "merchant_novatech",
  "actionType": "create_experiment",
  "targetType": "opportunity",
  "targetId": "opp_keyboard_stand",
  "outcome": "requires_approval",
  "reasons": ["Discount 10% is within policy.", "Merchant approval is required before experiment execution."],
  "checks": [
    {"policyId": "policy_discount_limit", "result": "passed", "reason": "10% <= 20%"},
    {"policyId": "policy_margin_floor", "result": "passed", "reason": "Projected margin remains above 25%"},
    {"policyId": "policy_merchant_auth", "result": "requires_approval", "reason": "Merchant Auth is REQUIRED"}
  ],
  "createdAt": "2026-08-31T11:32:06Z",
  "updatedAt": "2026-08-31T11:32:06Z",
  "metadata": {}
}
```

### Approval

```json
{
  "id": "appr_001",
  "merchantId": "merchant_novatech",
  "policyEvaluationId": "pol_eval_001",
  "targetType": "opportunity",
  "targetId": "opp_keyboard_stand",
  "status": "approved",
  "approvedBy": "merchant_demo_user",
  "approvedAt": "2026-08-31T11:32:07Z",
  "createdAt": "2026-08-31T11:32:07Z",
  "updatedAt": "2026-08-31T11:32:07Z",
  "metadata": {}
}
```

### OrderIntent

```json
{
  "id": "intent_ai_setup_001",
  "merchantId": "merchant_novatech",
  "displayOrderId": "#RGO-10482",
  "buyerRequest": "I need a laptop setup for AI development and college under ₹70,000.",
  "customerName": "AI Buyer Demo",
  "source": "AI Buyer",
  "items": [
    {"productId": "prod_probook_14", "name": "ProBook 14", "quantity": 1, "unitPrice": 62999},
    {"productId": "prod_usb_c_dock", "name": "USB-C Dock", "quantity": 1, "unitPrice": 4999},
    {"productId": "prod_laptop_stand", "name": "Laptop Stand", "quantity": 1, "unitPrice": 1799}
  ],
  "subtotal": 69797,
  "bundleDiscount": 1298,
  "total": 68499,
  "currency": "INR",
  "status": "review",
  "paymentStatus": "not_started",
  "createdAt": "2026-08-31T11:32:09Z",
  "updatedAt": "2026-08-31T11:32:09Z",
  "metadata": {
    "decisionTimeSec": 2.4,
    "recommendationConfidence": 92
  }
}
```

### PaymentAttempt

```json
{
  "id": "pay_attempt_001",
  "merchantId": "merchant_novatech",
  "orderIntentId": "intent_ai_setup_001",
  "razorpayOrderId": "order_demo_001",
  "razorpayPaymentId": null,
  "amount": 68499,
  "amountSubunits": 6849900,
  "currency": "INR",
  "method": "Razorpay Test Mode",
  "status": "failed",
  "failureReason": "Payment attempt was unsuccessful. No funds have been captured from your account.",
  "automaticRetry": "blocked",
  "retryBlockedReason": "Duplicate-charge protection",
  "createdAt": "2026-08-31T11:32:12Z",
  "updatedAt": "2026-08-31T11:32:12Z",
  "metadata": {}
}
```

### AuditEvent

```json
{
  "id": "audit_001",
  "merchantId": "merchant_novatech",
  "timestamp": "2026-08-31T11:32:12Z",
  "agent": "Policy Guard",
  "action": "Retry Payment",
  "reason": "Payment failed",
  "policy": "Max_Retries_Exceeded",
  "approval": "N/A",
  "outcome": "Prevented",
  "severity": "warning",
  "correlationIds": {
    "orderIntentId": "intent_ai_setup_001",
    "orderId": "order_demo_001",
    "paymentAttemptId": "pay_attempt_001",
    "policyEvaluationId": "pol_eval_retry_001"
  },
  "details": {
    "decisionSummary": "Automatic retry was blocked to prevent duplicate charge risk.",
    "evidence": ["Payment attempt returned failed status."],
    "policyChecks": [
      {"policy": "Payment Retry", "result": "blocked", "reason": "Duplicate-charge protection"}
    ],
    "executionResult": "No retry attempted"
  },
  "createdAt": "2026-08-31T11:32:12Z",
  "updatedAt": "2026-08-31T11:32:12Z",
  "metadata": {}
}
```

---

## 13. State Machines

### Universal Consequential Action State

```text
proposed -> policy_evaluated -> approval_required -> merchant_approved -> execution_pending -> executed | blocked | failed
```

### Opportunity State

```text
detected -> ready_for_review -> policy_evaluated -> approved -> experiment_created
                                          |              |
                                          v              v
                                       blocked          failed
```

Allowed MVP statuses:

- `detected`
- `ready_for_review`
- `policy_evaluated`
- `approved`
- `experiment_created`
- `blocked`
- `failed`

### Experiment State

```text
draft -> running -> scale_review -> policy_evaluated -> approval_required -> scaled
                         |                                     |
                         v                                     v
                      completed                              blocked
```

Allowed MVP statuses:

- `draft`
- `running`
- `scale_review`
- `policy_evaluated`
- `approval_required`
- `scaled`
- `completed`
- `blocked`
- `failed`

### Order Intent State

```text
created -> review -> payment_order_created -> payment_authorized -> paid
              |              |                       |
              v              v                       v
           cancelled       payment_failed          verification_failed
```

Allowed MVP statuses:

- `created`
- `review`
- `payment_order_created`
- `payment_authorized`
- `paid`
- `payment_failed`
- `verification_failed`
- `cancelled`

### Payment Attempt State

```text
created -> awaiting_authorization -> authorized -> captured
   |               |                    |
   v               v                    v
failed        failed_retry_blocked   verification_failed
```

Allowed MVP statuses:

- `created`
- `awaiting_authorization`
- `authorized`
- `captured`
- `failed`
- `failed_retry_blocked`
- `verification_failed`

### Approval State

```text
requested -> approved | rejected | expired
```

MVP may only implement `approved`, but schemas must reserve the other statuses for future use.

---

## 14. Pydantic Schema Standards

### JSON Naming

- API responses use camelCase.
- Python code may use snake_case with Pydantic aliases.
- Datetime values use ISO 8601 UTC strings.
- Amounts use INR major units in public UI fields, for example `68499`.
- Razorpay amount sent to Razorpay uses smallest currency unit, for example `6849900`.

### Common Response Metadata

List endpoints should support this shape:

```json
{
  "items": [],
  "total": 0,
  "nextCursor": null
}
```

Detail endpoints may return the object directly if that matches the frontend service layer.

### Error Response

All errors should return:

```json
{
  "error": {
    "code": "POLICY_BLOCKED",
    "message": "Payment retry is blocked after a failed payment.",
    "details": {
      "policyId": "policy_payment_retry"
    },
    "requestId": "req_abc123"
  }
}
```

Use appropriate HTTP statuses:

- `400` validation or invalid state transition.
- `401` missing demo auth if added later.
- `403` policy blocked.
- `404` missing entity.
- `409` idempotency conflict or duplicate transition.
- `422` Pydantic validation error.
- `500` unexpected server error.
- `503` external dependency unavailable or Razorpay not configured.

---

## 15. API Contracts

All endpoints are under `/api/v1`.

### 15.1 Merchant

#### `GET /merchant`

Purpose: return active demo merchant.

Response `200`:

```json
{
  "id": "merchant_novatech",
  "name": "NovaTech Store",
  "category": "Consumer Electronics",
  "currency": "INR",
  "status": "active"
}
```

#### `POST /onboarding/initialize`

Purpose: initialize/reset demo data for NovaTech Store.

Headers:

```text
Idempotency-Key: optional but recommended
```

Request:

```json
{
  "merchantId": "merchant_novatech",
  "resetDemoData": true
}
```

Response `200`:

```json
{
  "merchant": {
    "id": "merchant_novatech",
    "name": "NovaTech Store",
    "category": "Consumer Electronics",
    "currency": "INR"
  },
  "initialized": true,
  "nextRoute": "/overview"
}
```

Behavior:

- Seed merchant, products, metrics, opportunities, policies, agent activity, and baseline audit events.
- If `ALLOW_DEMO_RESET=false`, reject `resetDemoData=true` with `403`.
- Write an audit event: `System`, `Initialize Demo`, outcome `Success`.

---

### 15.2 Dashboard

#### `GET /dashboard/overview`

Purpose: power `/overview`.

Response `200`:

```json
{
  "merchant": {
    "id": "merchant_novatech",
    "name": "NovaTech Store",
    "category": "Consumer Electronics",
    "currency": "INR"
  },
  "metrics": {
    "totalRevenue": 284620,
    "revenueGrowthPct": 18.7,
    "raygoInfluencedRevenue": 42800,
    "raygoLiftPct": 14.2,
    "activeOpportunities": 7,
    "aiCommerceReadiness": 82,
    "projectedOpportunityImpact": 40000
  },
  "topOpportunities": [
    {
      "id": "opp_keyboard_stand",
      "title": "Cross-sell opportunity: Wireless Keyboard -> Laptop Stand",
      "shortTitle": "Keyboard + Stand",
      "expectedMonthlyImpact": 18400,
      "confidence": 87,
      "risk": "low",
      "status": "ready_for_review"
    }
  ],
  "revenueTrend": [
    {"label": "Week 1", "revenue": 62000, "raygoInfluencedRevenue": 8200},
    {"label": "Week 2", "revenue": 69000, "raygoInfluencedRevenue": 9700},
    {"label": "Week 3", "revenue": 71500, "raygoInfluencedRevenue": 11200},
    {"label": "Week 4", "revenue": 82120, "raygoInfluencedRevenue": 13700}
  ],
  "latestReasoning": {
    "agent": "Revenue Intelligence",
    "summary": "RAYGO found 7 revenue opportunities using observed journey and catalog signals.",
    "route": "/opportunities/opp_keyboard_stand"
  }
}
```

Wording rule:

- Opportunity reasoning must use observed, detected, hypothesized, or predicted wording.
- Do not imply the AI has secretly executed actions.

---

### 15.3 Products

#### `GET /products`

Purpose: power `/products`.

Query:

```text
status?: ready | needs_attention
limit?: number
cursor?: string
```

Response `200`:

```json
{
  "items": [
    {"id": "prod_probook_14", "name": "ProBook 14", "price": 62999, "currency": "INR", "inventory": 42, "aiReadiness": 94, "issues": [], "status": "ready"},
    {"id": "prod_wireless_keyboard", "name": "Wireless Keyboard", "price": 2499, "currency": "INR", "inventory": 86, "aiReadiness": 89, "issues": [], "status": "ready"},
    {"id": "prod_laptop_stand", "name": "Laptop Stand", "price": 1799, "currency": "INR", "inventory": 12, "aiReadiness": 81, "issues": ["Shipping metadata"], "status": "needs_attention"}
  ],
  "total": 7,
  "nextCursor": null
}
```

---

### 15.4 Opportunities

#### `GET /opportunities`

Purpose: power Opportunity Center.

Query:

```text
status?: ready_for_review | approved | experiment_created | blocked
risk?: low | medium | high
limit?: number
cursor?: string
```

Response `200`:

```json
{
  "items": [
    {
      "id": "opp_keyboard_stand",
      "title": "Cross-sell opportunity: Wireless Keyboard -> Laptop Stand",
      "shortTitle": "Keyboard + Stand",
      "type": "cross_sell",
      "expectedMonthlyImpact": 18400,
      "confidence": 87,
      "risk": "low",
      "status": "ready_for_review",
      "targetSegment": "Remote Workers"
    }
  ],
  "total": 7,
  "nextCursor": null
}
```

#### `GET /opportunities/{opportunity_id}`

Purpose: power Opportunity Detail.

Response `200`:

```json
{
  "id": "opp_keyboard_stand",
  "title": "Cross-sell opportunity: Wireless Keyboard -> Laptop Stand",
  "shortTitle": "Keyboard + Stand",
  "type": "cross_sell",
  "expectedMonthlyImpact": 18400,
  "confidence": 87,
  "risk": "low",
  "status": "ready_for_review",
  "currentAttachRate": 4.1,
  "projectedAttachRate": 7.8,
  "targetSegment": "Remote Workers",
  "eligibleJourneys": 1842,
  "recommendedAction": "Create a 10% Keyboard + Laptop Stand bundle experiment.",
  "policyPreview": {
    "budget": "Within policy",
    "merchantApprovalRequired": true,
    "outcome": "requires_approval"
  },
  "evidence": [
    "Observed buyers of Wireless Keyboard often view Laptop Stand.",
    "Detected under-used cross-sell surface in checkout journeys.",
    "Hypothesized bundle remains above merchant margin floor."
  ]
}
```

#### `POST /opportunities/{opportunity_id}/approve`

Purpose: run policy check, record merchant approval, create experiment, and return the frontend route.

Headers:

```text
Idempotency-Key: required
```

Request:

```json
{
  "merchantId": "merchant_novatech",
  "approvedBy": "merchant_demo_user",
  "confirmationText": "Approve & Create Experiment"
}
```

Response `200`:

```json
{
  "approvalId": "appr_001",
  "policyEvaluationId": "pol_eval_001",
  "experimentId": "exp_keyboard_stand",
  "status": "approved",
  "nextRoute": "/experiments/exp_keyboard_stand"
}
```

Behavior:

- Load opportunity.
- Generate experiment proposal through `GrowthStrategistService`.
- Evaluate with Policy Guard.
- If blocked, return `403` with `POLICY_BLOCKED` and write audit event.
- If allowed/requires approval, record Approval Gateway approval from merchant click.
- Create or return `exp_keyboard_stand` idempotently.
- Write audit events for `Policy evaluated`, `Opportunity approved`, and `Experiment created`.

---

### 15.5 Experiments

#### `GET /experiments`

Purpose: power `/experiments`.

Response `200`:

```json
{
  "summary": {
    "activeExperiments": 3,
    "scaledExperiments": 1,
    "averageConfidence": 91
  },
  "items": [
    {
      "id": "exp_keyboard_stand",
      "opportunityId": "opp_keyboard_stand",
      "name": "Keyboard + Laptop Stand",
      "status": "running",
      "conversionUplift": 43.5,
      "revenueUplift": 23.4,
      "confidence": 94,
      "recommendation": "scale_variant"
    }
  ],
  "total": 3,
  "nextCursor": null
}
```

#### `GET /experiments/{experiment_id}`

Purpose: power Experiment Detail.

Response `200`:

```json
{
  "id": "exp_keyboard_stand",
  "opportunityId": "opp_keyboard_stand",
  "name": "Keyboard + Laptop Stand",
  "status": "running",
  "hypothesis": "Bundling a Laptop Stand with Wireless Keyboard purchases will increase basket conversion without reducing merchant margin below policy.",
  "controlConversion": 6.2,
  "variantConversion": 8.9,
  "conversionUplift": 43.5,
  "revenueUplift": 23.4,
  "aovUplift": 8.7,
  "confidence": 94,
  "recommendation": "scale_variant",
  "decisionReason": "Variant performance exceeds control while remaining within the merchant's margin policy."
}
```

#### `POST /experiments/{experiment_id}/scale`

Purpose: policy-gate and approve scaling a successful experiment.

Headers:

```text
Idempotency-Key: required
```

Request:

```json
{
  "merchantId": "merchant_novatech",
  "approvedBy": "merchant_demo_user",
  "confirmationText": "Scale Experiment"
}
```

Response `200`:

```json
{
  "experimentId": "exp_keyboard_stand",
  "policyEvaluationId": "pol_eval_scale_001",
  "approvalId": "appr_scale_001",
  "status": "scaled",
  "nextRoute": "/ai-commerce"
}
```

Behavior:

- Evaluate scale action.
- Require merchant approval.
- Set experiment status to `scaled`.
- Write audit events.

---

### 15.6 AI Commerce

#### `GET /ai-commerce/readiness`

Purpose: power `/ai-commerce`.

Response `200`:

```json
{
  "score": 82,
  "label": "AI Commerce Readiness",
  "dimensions": [
    {"name": "Catalog Completeness", "score": 88, "status": "ready"},
    {"name": "Policy Clarity", "score": 72, "status": "needs_attention"},
    {"name": "Payment Readiness", "score": 86, "status": "ready"}
  ],
  "recommendedActions": [
    {
      "id": "optimize_laptop_stand_metadata",
      "label": "Optimize Laptop Stand shipping metadata",
      "route": "/products"
    }
  ]
}
```

#### `GET /ai-commerce/products/{product_id}/profile`

Purpose: return AI-readable product profile.

Response `200`:

```json
{
  "productId": "prod_laptop_stand",
  "name": "Laptop Stand",
  "aiReadiness": 81,
  "profile": {
    "category": "Laptop accessory",
    "buyerUseCases": ["Remote work", "College setup", "Desk ergonomics"],
    "compatibleProducts": ["prod_wireless_keyboard", "prod_probook_14", "prod_usb_c_dock"],
    "missingMetadata": ["Shipping metadata"]
  },
  "status": "needs_attention"
}
```

#### `POST /ai-commerce/optimize-catalog`

Purpose: simulate metadata optimization and write audit event.

Headers:

```text
Idempotency-Key: required
```

Request:

```json
{
  "merchantId": "merchant_novatech",
  "productIds": ["prod_laptop_stand"]
}
```

Response `200`:

```json
{
  "optimizedProducts": [
    {
      "productId": "prod_laptop_stand",
      "previousReadiness": 81,
      "newReadiness": 86,
      "status": "ready"
    }
  ],
  "auditEventId": "audit_catalog_opt_001"
}
```

Behavior:

- Use deterministic `AICommerceAgent`.
- Do not call Gemini unless `USE_MOCK_AGENTS=false`.
- Write audit event.

---

### 15.7 AI Buyer

#### `POST /ai-buyer/search`

Purpose: match buyer intent to AI-readable catalog.

Headers:

```text
Idempotency-Key: optional
```

Request:

```json
{
  "merchantId": "merchant_novatech",
  "buyerRequest": "I need a laptop setup for AI development and college under ₹70,000.",
  "budget": 70000,
  "currency": "INR"
}
```

Response `200`:

```json
{
  "buyerIntentId": "buyer_intent_ai_setup_001",
  "matchedProducts": [
    {"productId": "prod_probook_14", "name": "ProBook 14", "quantity": 1, "unitPrice": 62999, "reason": "Primary laptop within budget."},
    {"productId": "prod_usb_c_dock", "name": "USB-C Dock", "quantity": 1, "unitPrice": 4999, "reason": "Recommended connectivity accessory."},
    {"productId": "prod_laptop_stand", "name": "Laptop Stand", "quantity": 1, "unitPrice": 1799, "reason": "Ergonomic setup add-on."}
  ],
  "subtotal": 69797,
  "bundleDiscount": 1298,
  "total": 68499,
  "currency": "INR",
  "confidence": 92,
  "decisionTimeSec": 2.4
}
```

Behavior:

- In MVP, return deterministic demo recommendation when buyer request resembles the seeded request or budget is near `70000`.
- Write audit event: `AI Commerce Agent`, `AI buyer search completed`, outcome `Success`.

#### `POST /ai-buyer/basket`

Purpose: create/update basket from AI buyer recommendation.

Headers:

```text
Idempotency-Key: required
```

Request:

```json
{
  "merchantId": "merchant_novatech",
  "buyerIntentId": "buyer_intent_ai_setup_001",
  "items": [
    {"productId": "prod_probook_14", "quantity": 1},
    {"productId": "prod_usb_c_dock", "quantity": 1},
    {"productId": "prod_laptop_stand", "quantity": 1}
  ]
}
```

Response `200`:

```json
{
  "basketId": "basket_ai_setup_001",
  "items": [
    {"productId": "prod_probook_14", "name": "ProBook 14", "quantity": 1, "unitPrice": 62999},
    {"productId": "prod_usb_c_dock", "name": "USB-C Dock", "quantity": 1, "unitPrice": 4999},
    {"productId": "prod_laptop_stand", "name": "Laptop Stand", "quantity": 1, "unitPrice": 1799}
  ],
  "subtotal": 69797,
  "bundleDiscount": 1298,
  "total": 68499,
  "currency": "INR"
}
```

#### `POST /order-intents`

Purpose: create checkout intent and return route.

Headers:

```text
Idempotency-Key: required
```

Request:

```json
{
  "merchantId": "merchant_novatech",
  "basketId": "basket_ai_setup_001",
  "buyerRequest": "I need a laptop setup for AI development and college under ₹70,000."
}
```

Response `200`:

```json
{
  "orderIntentId": "intent_ai_setup_001",
  "displayOrderId": "#RGO-10482",
  "status": "review",
  "total": 68499,
  "currency": "INR",
  "nextRoute": "/checkout/intent_ai_setup_001"
}
```

Behavior:

- Policy Guard must verify payment execution is not happening yet.
- Inventory must not be decremented at this stage.
- Write audit event: `Order intent created`.

#### `GET /order-intents/{order_intent_id}`

Purpose: power `/checkout/:orderIntentId`.

Response `200`:

```json
{
  "id": "intent_ai_setup_001",
  "displayOrderId": "#RGO-10482",
  "buyerRequest": "I need a laptop setup for AI development and college under ₹70,000.",
  "whyPrepared": "RAYGO matched buyer intent to an AI-readable catalog and stayed under budget.",
  "items": [
    {"productId": "prod_probook_14", "name": "ProBook 14", "quantity": 1, "unitPrice": 62999},
    {"productId": "prod_usb_c_dock", "name": "USB-C Dock", "quantity": 1, "unitPrice": 4999},
    {"productId": "prod_laptop_stand", "name": "Laptop Stand", "quantity": 1, "unitPrice": 1799}
  ],
  "subtotal": 69797,
  "bundleDiscount": 1298,
  "taxesAndFeesLabel": "Calculated",
  "total": 68499,
  "currency": "INR",
  "status": "review",
  "paymentStatus": "not_started",
  "authorizationRequired": true,
  "authorizationCopy": "RAYGO will not execute payment until you confirm this purchase."
}
```

---

### 15.8 Payments And Orders

#### `POST /payments/razorpay/order`

Purpose: create Razorpay Test Mode order server-side after explicit frontend purchase confirmation.

Headers:

```text
Idempotency-Key: required
```

Request:

```json
{
  "merchantId": "merchant_novatech",
  "orderIntentId": "intent_ai_setup_001",
  "approvedBy": "merchant_demo_user"
}
```

Response `200`:

```json
{
  "orderIntentId": "intent_ai_setup_001",
  "displayOrderId": "#RGO-10482",
  "razorpayOrderId": "order_demo_001",
  "amount": 68499,
  "amountSubunits": 6849900,
  "currency": "INR",
  "keyId": "rzp_test_xxxxx",
  "environment": "Razorpay Test Mode",
  "paymentAttemptId": "pay_attempt_001",
  "status": "awaiting_authorization"
}
```

Behavior:

- Require order intent status `review` or `payment_failed`.
- If previous failed attempt exists, do not auto-retry. A new call is only allowed if triggered by explicit user action such as `Try Another Payment Method`.
- Policy Guard evaluates `execute_payment`.
- Approval Gateway records merchant click confirmation.
- Razorpay order amount must be `total * 100`.
- Set order intent status to `payment_order_created`.
- Write audit events: `Policy evaluated`, `Create Order`.
- No inventory decrement yet.

#### `POST /payments/razorpay/verify`

Purpose: verify Razorpay Checkout success server-side.

Headers:

```text
Idempotency-Key: required
```

Request:

```json
{
  "merchantId": "merchant_novatech",
  "orderIntentId": "intent_ai_setup_001",
  "razorpayOrderId": "order_demo_001",
  "razorpayPaymentId": "pay_demo_success_001",
  "razorpaySignature": "signature_from_checkout"
}
```

Response `200`:

```json
{
  "verified": true,
  "orderIntentId": "intent_ai_setup_001",
  "displayOrderId": "#RGO-10482",
  "paymentAttemptId": "pay_attempt_001",
  "amountPaid": 68499,
  "currency": "INR",
  "status": "captured",
  "environment": "Razorpay Test Mode",
  "timeline": ["Intent received", "Products selected", "Order created", "Payment authorized", "Order confirmed"],
  "aiCommerceSummary": {
    "decisionTimeSec": 2.4,
    "recommendationConfidence": 92,
    "action": "Checkout Completed"
  },
  "nextRoute": "/payment/success"
}
```

Behavior:

- Verify signature using `razorpay_order_id|razorpay_payment_id` and `RAZORPAY_KEY_SECRET`.
- Reject invalid signatures with `400` or `403`.
- Mark order paid/captured only after server verification.
- Write audit events: `Payment verified`, `Order confirmed`.
- Inventory may be marked reserved or unchanged for MVP. If inventory is changed, do it only after verification and record audit.

#### `POST /payments/razorpay/failure`

Purpose: record Checkout failure and block automatic retry.

Headers:

```text
Idempotency-Key: required
```

Request:

```json
{
  "merchantId": "merchant_novatech",
  "orderIntentId": "intent_ai_setup_001",
  "razorpayOrderId": "order_demo_001",
  "errorCode": "BAD_REQUEST_ERROR",
  "errorDescription": "Payment attempt was unsuccessful. No funds have been captured from your account.",
  "source": "checkout"
}
```

Response `200`:

```json
{
  "orderIntentId": "intent_ai_setup_001",
  "displayOrderId": "#RGO-10482",
  "amount": 68499,
  "currency": "INR",
  "status": "failed_retry_blocked",
  "automaticRetry": "blocked",
  "reason": "Payment attempt was unsuccessful. No funds have been captured from your account.",
  "retryBlockedReason": "Duplicate-charge protection",
  "safetyResponse": [
    "No duplicate payment attempted",
    "Order remains unpaid",
    "Inventory unchanged",
    "Failure recorded in audit trail",
    "Recovery option generated"
  ],
  "nextRoute": "/payment/failure"
}
```

Behavior:

- Set order intent `paymentStatus` to `failed`.
- Set payment attempt status `failed_retry_blocked`.
- Policy Guard evaluates `retry_payment` and returns `blocked`.
- Write audit events: `Payment failed`, `Retry blocked`.
- Never call Razorpay order creation again from this endpoint.

#### `POST /webhooks/razorpay`

Purpose: receive Razorpay asynchronous events.

Headers:

```text
X-Razorpay-Signature: required
```

Body: raw Razorpay webhook payload.

Response `200`:

```json
{
  "received": true,
  "processed": true,
  "idempotent": true
}
```

Required events:

- `order.paid`
- `payment.authorized`
- `payment.captured`
- `payment.failed`

Behavior:

- Validate signature using raw request body and `RAZORPAY_WEBHOOK_SECRET`.
- Store `razorpayEventId` uniquely.
- If duplicate event, return `200` with `processed=false`, `idempotent=true`.
- Reconcile order/payment state.
- Write audit event for any consequential state change.
- Do not trust webhook payload alone if it conflicts with verified local state; log and audit conflict.

#### `GET /payments`

Purpose: power `/payments`.

Response `200`:

```json
{
  "summary": {
    "successful": 1,
    "failed": 1,
    "pending": 0,
    "refunds": 0
  },
  "items": [
    {
      "paymentId": "pay_attempt_001",
      "order": "#RGO-10482",
      "amount": 68499,
      "currency": "INR",
      "method": "Razorpay Test Mode",
      "status": "failed_retry_blocked",
      "timestamp": "2026-08-31T11:32:12Z"
    }
  ],
  "total": 1,
  "nextCursor": null
}
```

#### `GET /orders`

Purpose: power `/orders`.

Response `200`:

```json
{
  "summary": {
    "gmv": 68499,
    "successfulPayments": 1,
    "failedPayments": 1,
    "aiBuyerOrders": 1
  },
  "items": [
    {
      "order": "#RGO-10482",
      "orderIntentId": "intent_ai_setup_001",
      "customer": "AI Buyer Demo",
      "amount": 68499,
      "currency": "INR",
      "source": "AI Buyer",
      "payment": "Razorpay Test Mode",
      "status": "Success"
    }
  ],
  "total": 1,
  "nextCursor": null
}
```

---

### 15.9 Policies

#### `GET /policies`

Purpose: power Revenue Action Firewall.

Response `200`:

```json
{
  "items": [
    {"id": "policy_discount_limit", "name": "Discount Limit", "limit": "20%", "status": "active"},
    {"id": "policy_margin_floor", "name": "Margin Floor", "limit": "25%", "status": "active"},
    {"id": "policy_daily_budget", "name": "Daily Budget", "limit": "₹10,000", "status": "review"},
    {"id": "policy_auto_execution", "name": "Auto Execution", "limit": "OFF", "status": "paused"},
    {"id": "policy_merchant_auth", "name": "Merchant Auth", "limit": "REQUIRED", "status": "enforced"},
    {"id": "policy_payment_retry", "name": "Payment Retry", "limit": "BLOCKED", "status": "strict"}
  ],
  "actionMatrix": [
    {"actionType": "Create Bundle", "canPropose": true, "canExecute": true, "approvalRequirement": "approval required"},
    {"actionType": "Discount >20%", "canPropose": true, "canExecute": false, "approvalRequirement": "blocked"},
    {"actionType": "Create Campaign", "canPropose": true, "canExecute": true, "approvalRequirement": "approval required"},
    {"actionType": "Payment Retry", "canPropose": true, "canExecute": false, "approvalRequirement": "blocked"},
    {"actionType": "Refund", "canPropose": true, "canExecute": false, "approvalRequirement": "approval required"}
  ]
}
```

#### `PATCH /policies/{policy_id}`

Purpose: update a policy and write audit event.

Headers:

```text
Idempotency-Key: required
```

Request:

```json
{
  "merchantId": "merchant_novatech",
  "limit": "₹10,000",
  "status": "review"
}
```

Response `200`:

```json
{
  "id": "policy_daily_budget",
  "name": "Daily Budget",
  "limit": "₹10,000",
  "status": "review",
  "auditEventId": "audit_policy_update_001"
}
```

Hard rule:

- `policy_payment_retry` must remain blocked for MVP.
- If request tries to make payment retry executable or automatic, return `403 POLICY_BLOCKED`.

#### `POST /policies/evaluate`

Purpose: evaluate proposed action without executing it.

Request:

```json
{
  "merchantId": "merchant_novatech",
  "actionType": "create_experiment",
  "targetType": "opportunity",
  "targetId": "opp_keyboard_stand",
  "proposedAction": {
    "discountPct": 10,
    "estimatedMarginPct": 32
  }
}
```

Response `200`:

```json
{
  "policyEvaluationId": "pol_eval_001",
  "outcome": "requires_approval",
  "reasons": ["Discount 10% is within policy.", "Merchant approval is required before experiment execution."],
  "checks": [
    {"policy": "Discount Limit", "result": "passed", "reason": "10% <= 20%"},
    {"policy": "Margin Floor", "result": "passed", "reason": "32% >= 25%"},
    {"policy": "Merchant Auth", "result": "requires_approval", "reason": "Merchant approval required"}
  ]
}
```

---

### 15.10 Agents

#### `GET /agents/status`

Purpose: power agent status cards.

Response `200`:

```json
{
  "items": [
    {"name": "Revenue Intelligence", "status": "Active"},
    {"name": "AI Commerce", "status": "Active"},
    {"name": "Growth Strategist", "status": "Active"},
    {"name": "Experiment Agent", "status": "Running"},
    {"name": "Policy Guard", "status": "Active"},
    {"name": "Payment Agent", "status": "Ready"},
    {"name": "Approval Gateway", "status": "Ready"}
  ],
  "mockAgents": true
}
```

#### `GET /agents/activity`

Purpose: power live activity timeline.

Query:

```text
limit?: number
cursor?: string
```

Response `200`:

```json
{
  "items": [
    {"id": "agent_evt_001", "time": "11:32:04", "agent": "Revenue Intelligence", "message": "Detected cross-sell opportunity", "auditEventId": "audit_opp_detected_001"},
    {"id": "agent_evt_002", "time": "11:32:05", "agent": "Growth Strategist", "message": "Generated experiment hypothesis", "auditEventId": "audit_hypothesis_001"},
    {"id": "agent_evt_003", "time": "11:32:06", "agent": "Policy Guard", "message": "Policy check passed", "auditEventId": "audit_policy_001"},
    {"id": "agent_evt_004", "time": "11:32:07", "agent": "Approval Gateway", "message": "Merchant approval received", "auditEventId": "audit_approval_001"},
    {"id": "agent_evt_005", "time": "11:32:08", "agent": "Experiment Agent", "message": "Experiment created", "auditEventId": "audit_experiment_001"},
    {"id": "agent_evt_006", "time": "11:32:12", "agent": "Payment Agent", "message": "Payment attempt failed", "auditEventId": "audit_payment_failed_001"},
    {"id": "agent_evt_007", "time": "11:32:12", "agent": "Policy Guard", "message": "Automatic retry blocked", "auditEventId": "audit_001"}
  ],
  "total": 7,
  "nextCursor": null
}
```

---

### 15.11 Audit

#### `GET /audit`

Purpose: power Audit Trail table.

Query:

```text
agent?: string
severity?: info | warning | critical
outcome?: Success | Prevented | Failed
limit?: number
cursor?: string
```

Response `200`:

```json
{
  "items": [
    {
      "id": "audit_order_created_001",
      "timestamp": "2026-08-31T11:32:10Z",
      "agent": "Payment Agent",
      "action": "Create Order",
      "reason": "Buyer confirmed purchase",
      "policy": "Passed",
      "approval": "Confirmed",
      "outcome": "Success",
      "severity": "info"
    },
    {
      "id": "audit_001",
      "timestamp": "2026-08-31T11:32:12Z",
      "agent": "Policy Guard",
      "action": "Retry Payment",
      "reason": "Payment failed",
      "policy": "Max_Retries_Exceeded",
      "approval": "N/A",
      "outcome": "Prevented",
      "severity": "warning"
    },
    {
      "id": "audit_experiment_001",
      "timestamp": "2026-08-31T11:32:08Z",
      "agent": "Experiment Agent",
      "action": "Create Experiment",
      "reason": "Merchant approved recommendation",
      "policy": "Passed",
      "approval": "Confirmed",
      "outcome": "Success",
      "severity": "info"
    }
  ],
  "total": 3,
  "nextCursor": null
}
```

#### `GET /audit/{audit_event_id}`

Purpose: power audit detail drawer/page.

Response `200`:

```json
{
  "id": "audit_001",
  "timestamp": "2026-08-31T11:32:12Z",
  "agent": "Policy Guard",
  "action": "Retry Payment",
  "reason": "Payment failed",
  "policy": "Max_Retries_Exceeded",
  "approval": "N/A",
  "outcome": "Prevented",
  "severity": "warning",
  "correlationIds": {
    "orderIntentId": "intent_ai_setup_001",
    "orderId": "order_demo_001",
    "paymentAttemptId": "pay_attempt_001",
    "policyEvaluationId": "pol_eval_retry_001"
  },
  "details": {
    "decisionSummary": "Automatic retry was blocked to prevent duplicate charge risk.",
    "evidence": ["Payment attempt returned failed status."],
    "action": "Retry Payment",
    "policyChecks": [
      {"policy": "Payment Retry", "result": "blocked", "reason": "Duplicate-charge protection"}
    ],
    "approval": "N/A",
    "executionResult": "No retry attempted",
    "failureRecovery": "User may manually try another payment method.",
    "relatedOrder": "#RGO-10482",
    "rawMetadata": {}
  }
}
```

Rules:

- Do not show hidden chain-of-thought.
- Show concise decision explanations and auditable metadata only.
- Include correlation IDs for order, payment, policy check, agent run, and audit event when available.

---

## 16. Policy Guard

Policy Guard is a service, not just a route.

### Inputs

```json
{
  "merchantId": "merchant_novatech",
  "actionType": "create_experiment",
  "targetType": "opportunity",
  "targetId": "opp_keyboard_stand",
  "proposedAction": {}
}
```

### Outputs

```json
{
  "policyEvaluationId": "pol_eval_001",
  "outcome": "passed | requires_approval | blocked",
  "reasons": [],
  "checks": []
}
```

### Required Policies

```json
[
  {"id": "policy_discount_limit", "name": "Discount Limit", "limit": "20%", "status": "active"},
  {"id": "policy_margin_floor", "name": "Margin Floor", "limit": "25%", "status": "active"},
  {"id": "policy_daily_budget", "name": "Daily Budget", "limit": "₹10,000", "status": "review"},
  {"id": "policy_auto_execution", "name": "Auto Execution", "limit": "OFF", "status": "paused"},
  {"id": "policy_merchant_auth", "name": "Merchant Auth", "limit": "REQUIRED", "status": "enforced"},
  {"id": "policy_payment_retry", "name": "Payment Retry", "limit": "BLOCKED", "status": "strict"}
]
```

### Hard Rules

- Discount above 20% is blocked.
- Margin below 25% is blocked.
- Payment retry is blocked after failed payment.
- Refund execution is not allowed in MVP.
- Merchant approval is required before experiments and payment execution.
- Auto Execution is OFF.
- The app must never imply RAYGO can spend money without authorization.

### Outcome Semantics

- `passed`: action is policy-compliant and does not require explicit merchant approval.
- `requires_approval`: action is policy-compliant but must pass Approval Gateway before execution.
- `blocked`: action must not execute.

For MVP, most consequential actions should return `requires_approval`; payment retry and invalid discounts/margins should return `blocked`.

---

## 17. Approval Gateway

Approval Gateway records explicit merchant authorization.

### Required Use Cases

- Approve opportunity and create experiment.
- Scale experiment.
- Confirm payment before Razorpay order creation.

### Approval Rules

- Approval must be a separate persisted record.
- Approval must reference a `policyEvaluationId`.
- Approval must include `approvedBy`, `approvedAt`, `targetType`, and `targetId`.
- Approval must write an audit event.
- Backend must never infer approval from an agent recommendation.

### MVP Demo Identity

Use `merchant_demo_user` as the default `approvedBy` when the frontend does not send a real user ID.

---

## 18. Audit Service

Audit Service is mandatory for all state transitions and consequential decisions.

### Required Audit Events

- Opportunity created.
- Opportunity approved.
- Policy evaluated.
- Experiment created.
- Experiment scaled.
- AI buyer search completed.
- Order intent created.
- Razorpay order created.
- Payment verified.
- Payment failed.
- Retry blocked.
- Policy changed.
- Demo initialized.

### Audit Rules

- Audit writes should be best-effort only for non-critical read flows, but mandatory for consequential state changes.
- If audit write fails during a financial action, the financial action should fail closed unless this would cause an inconsistent Razorpay state; in that case, reconcile and surface the issue.
- Audit details must be concise and reconstructable.
- Never include hidden chain-of-thought.
- Store raw metadata only when useful for debugging and safe to display behind a collapsible panel.

---

## 19. Deterministic Agent Interfaces And Stubs

For MVP, implement agents as deterministic backend services. The UI should still display agent status/activity as if the logical multi-agent architecture is active.

### Revenue Intelligence Agent

Input:

- Orders
- Products
- Cart behavior
- Product views
- Margins
- Abandonment metrics

Output:

- Ranked opportunities with expected impact, confidence, evidence, and risk.

MVP behavior:

- Return seeded opportunities.
- Ensure `opp_keyboard_stand` is highest-ranked.

### Growth Strategist

Input:

- Opportunity
- Product margins
- Policy rules

Output:

- Proposed experiment, hypothesis, discount, and expected uplift.

MVP behavior:

- For `opp_keyboard_stand`, produce `exp_keyboard_stand` with a 10% bundle experiment.

### Experiment Agent

Input:

- Approved proposal.
- Simulated experiment results.

Output:

- Control/variant metrics, uplift, confidence, recommendation.

MVP behavior:

- Return seeded experiment metrics and `scale_variant`.

### AI Commerce Agent

Input:

- Product catalog.
- Buyer intent.
- AI readiness rules.

Output:

- Readiness score, blockers, AI-readable product profile, buyer recommendations.

MVP behavior:

- Return readiness score `82`.
- Return deterministic buyer bundle for laptop setup under ₹70,000.

### Payment Agent

Input:

- Order intent.
- Razorpay order/payment status.
- Policy rules.

Output:

- Payment attempt records.
- No automatic retry after failure.
- Audit entries.

MVP behavior:

- Coordinate Razorpay service and Policy Guard.
- Never create a retry attempt from failure handling.

---

## 20. Gemini + Google ADK Integration Seam

The backend must be ready for later agent work without implementing full Gemini/ADK in Phase 3.

### Feature Flags

```text
USE_MOCK_AGENTS=true
USE_ADK_ORCHESTRATOR=false
GEMINI_API_KEY=
```

### Required Interfaces

Create typed interfaces for:

```text
AgentInput
AgentOutput
AgentActionProposal
AgentRun
PolicyCheckedAgentAction
```

Agent outputs must include:

```json
{
  "agentRunId": "agent_run_001",
  "agentName": "Growth Strategist",
  "outputType": "experiment_proposal",
  "summary": "Generated experiment hypothesis",
  "confidence": 0.94,
  "proposedAction": {},
  "requiresPolicyEvaluation": true,
  "metadata": {}
}
```

### Future Integration Rules

- Gemini may generate recommendations, explanations, catalog normalization suggestions, and buyer intent mappings.
- Gemini output must conform to Pydantic schemas.
- ADK may orchestrate agent sequencing only after deterministic MVP flows pass tests.
- Backend services must validate and gate every Gemini-suggested action before it affects orders, experiments, policies, or payments.
- LLMs and ADK agents must never directly call Razorpay.
- LLMs and ADK agents must never bypass Policy Guard.
- LLMs and ADK agents must never create hidden, unaudited actions.

---

## 21. Razorpay Test Mode Boundary

### Required Behavior

- Use Razorpay Test Mode only.
- Create an order on the server for every payment.
- Pass returned `order_id` to Checkout.
- Verify payment signature server-side before fulfilling order.
- Use webhooks for asynchronous payment/order events.
- Use API verification when user-facing confirmation needs immediate status.
- Test mode supports simulated success and failure and uses no real money.

### Success Flow

```text
AI Checkout
  -> POST /api/v1/payments/razorpay/order
  -> backend creates Razorpay order in INR smallest unit
  -> frontend opens Razorpay Checkout
  -> success handler POST /api/v1/payments/razorpay/verify
  -> backend verifies signature
  -> backend marks order paid/captured only after verification
  -> frontend routes to /payment/success
```

### Failure Flow

```text
Checkout failure
  -> POST /api/v1/payments/razorpay/failure
  -> backend records failed attempt
  -> Policy Guard blocks automatic retry
  -> audit event created
  -> frontend routes to /payment/failure
```

### Webhook Flow

```text
Razorpay webhook
  -> POST /api/v1/webhooks/razorpay
  -> verify X-Razorpay-Signature using raw request body
  -> idempotently store event
  -> reconcile payment/order state
  -> write audit event
```

### Security Rules

- Razorpay key secret is backend-only.
- Frontend receives only public key ID and Razorpay order ID.
- Reject payment success if signature verification fails.
- Do not fulfill orders from client success alone.
- Store webhook event IDs and process idempotently.
- Never enable live mode for MVP.

---

## 22. Idempotency

### Required Header

All mutating endpoints should support `Idempotency-Key`; the following require it:

- `POST /onboarding/initialize` when reset is true.
- `POST /opportunities/{opportunity_id}/approve`
- `POST /experiments/{experiment_id}/scale`
- `POST /ai-commerce/optimize-catalog`
- `POST /ai-buyer/basket`
- `POST /order-intents`
- `POST /payments/razorpay/order`
- `POST /payments/razorpay/verify`
- `POST /payments/razorpay/failure`
- `PATCH /policies/{policy_id}`

### Storage

Store:

```json
{
  "key": "idem_123",
  "route": "/api/v1/payments/razorpay/order",
  "method": "POST",
  "requestHash": "sha256...",
  "responseStatus": 200,
  "responseBody": {},
  "createdAt": "2026-08-31T11:32:10Z",
  "expiresAt": "2026-09-01T11:32:10Z"
}
```

Behavior:

- Same key + same route + same request hash returns cached response.
- Same key + same route + different request hash returns `409 IDEMPOTENCY_CONFLICT`.
- Webhooks use provider event ID idempotency, not client header idempotency.

---

## 23. Validation And Error Handling

### Validation Requirements

- Validate object IDs against expected prefixes where practical.
- Validate enum values.
- Validate amounts are non-negative integers.
- Validate currency is `INR` for MVP.
- Validate discounts do not exceed 20%.
- Validate margin does not fall below 25%.
- Validate all order items exist and have enough inventory before payment order creation.
- Validate order intent total server-side. Do not trust client totals.
- Validate Razorpay signatures server-side.

### Error Codes

Use stable error codes:

```text
VALIDATION_ERROR
NOT_FOUND
INVALID_STATE_TRANSITION
POLICY_BLOCKED
APPROVAL_REQUIRED
IDEMPOTENCY_CONFLICT
RAZORPAY_NOT_CONFIGURED
RAZORPAY_ORDER_FAILED
RAZORPAY_SIGNATURE_INVALID
WEBHOOK_SIGNATURE_INVALID
WEBHOOK_EVENT_CONFLICT
DATABASE_UNAVAILABLE
INTERNAL_ERROR
```

Frontend smoothness rule:

- Errors must be concise enough for toast messages.
- Include `details` for debugging.
- Include `requestId` for support and logs.

---

## 24. Security

### MVP Security Baseline

- CORS limited to `FRONTEND_ORIGIN`.
- Secrets only from environment variables.
- No secrets in frontend bundles.
- No secrets in logs.
- Request size limits for webhook and API JSON.
- Structured validation on all inputs.
- Server-side amount calculation for order/payment flows.
- Server-side payment verification.
- Idempotency for mutating endpoints.
- Raw body handling for Razorpay webhooks.
- No live Razorpay mode.
- No refund execution.
- No payment auto-retry.

### Demo Auth

For MVP, the backend may use a fixed demo merchant context:

```text
merchantId=merchant_novatech
approvedBy=merchant_demo_user
```

If a lightweight auth header is added, keep it frontend-compatible:

```text
X-Demo-Merchant-Id: merchant_novatech
```

Do not block local judge demo with complex login.

---

## 25. Observability And Logging

### Structured Logs

Log JSON records with:

```json
{
  "timestamp": "2026-08-31T11:32:12Z",
  "level": "INFO",
  "requestId": "req_abc123",
  "route": "/api/v1/payments/razorpay/failure",
  "method": "POST",
  "statusCode": 200,
  "durationMs": 42,
  "merchantId": "merchant_novatech",
  "correlationIds": {
    "orderIntentId": "intent_ai_setup_001",
    "paymentAttemptId": "pay_attempt_001"
  }
}
```

### Audit Vs Logs

- Logs are for operators and debugging.
- Audit events are product-visible and must explain decisions.
- Do not rely on logs as a substitute for audit events.

### Metrics To Track Locally

- Request count by route/status.
- Payment verification success/failure.
- Policy blocked count.
- Audit write failures.
- MongoDB latency.
- Razorpay request latency.

---

## 26. Seed And Demo Data

Implement `python -m app.db.seed` or equivalent.

### Seed Products

```json
[
  {"id": "prod_probook_14", "name": "ProBook 14", "price": 62999, "inventory": 42, "aiReadiness": 94},
  {"id": "prod_wireless_keyboard", "name": "Wireless Keyboard", "price": 2499, "inventory": 86, "aiReadiness": 89},
  {"id": "prod_laptop_stand", "name": "Laptop Stand", "price": 1799, "inventory": 12, "aiReadiness": 81},
  {"id": "prod_ai_mouse_pro", "name": "AI Mouse Pro", "price": 1299, "inventory": 64, "aiReadiness": 76},
  {"id": "prod_usb_c_dock", "name": "USB-C Dock", "price": 4999, "inventory": 20, "aiReadiness": 84},
  {"id": "prod_headphones", "name": "NoiseCancel Headphones", "price": 6499, "inventory": 17, "aiReadiness": 78},
  {"id": "prod_4k_monitor", "name": "27 inch 4K Monitor", "price": 29999, "inventory": 9, "aiReadiness": 72}
]
```

### Seed Metrics

```json
{
  "totalRevenue": 284620,
  "revenueGrowthPct": 18.7,
  "raygoInfluencedRevenue": 42800,
  "raygoLiftPct": 14.2,
  "activeOpportunities": 7,
  "aiCommerceReadiness": 82,
  "projectedOpportunityImpact": 40000
}
```

### Seed Primary Opportunity

```json
{
  "id": "opp_keyboard_stand",
  "title": "Cross-sell opportunity: Wireless Keyboard -> Laptop Stand",
  "shortTitle": "Keyboard + Stand",
  "type": "cross_sell",
  "expectedMonthlyImpact": 18400,
  "confidence": 87,
  "risk": "low",
  "status": "ready_for_review",
  "currentAttachRate": 4.1,
  "projectedAttachRate": 7.8,
  "targetSegment": "Remote Workers",
  "eligibleJourneys": 1842
}
```

### Seed Experiment

```json
{
  "id": "exp_keyboard_stand",
  "opportunityId": "opp_keyboard_stand",
  "name": "Keyboard + Laptop Stand",
  "status": "running",
  "controlConversion": 6.2,
  "variantConversion": 8.9,
  "conversionUplift": 43.5,
  "revenueUplift": 23.4,
  "aovUplift": 8.7,
  "confidence": 94,
  "recommendation": "scale_variant"
}
```

### Seed AI Buyer Order Intent

```json
{
  "orderIntentId": "intent_ai_setup_001",
  "buyerRequest": "I need a laptop setup for AI development and college under ₹70,000.",
  "items": [
    {"productId": "prod_probook_14", "name": "ProBook 14", "quantity": 1, "unitPrice": 62999},
    {"productId": "prod_usb_c_dock", "name": "USB-C Dock", "quantity": 1, "unitPrice": 4999},
    {"productId": "prod_laptop_stand", "name": "Laptop Stand", "quantity": 1, "unitPrice": 1799}
  ],
  "subtotal": 69797,
  "bundleDiscount": 1298,
  "total": 68499,
  "currency": "INR"
}
```

### Seed Agent Activity

```text
11:32:04, Revenue Intelligence, Detected cross-sell opportunity
11:32:05, Growth Strategist, Generated experiment hypothesis
11:32:06, Policy Guard, Policy check passed
11:32:07, Approval Gateway, Merchant approval received
11:32:08, Experiment Agent, Experiment created
11:32:12, Payment Agent, Payment attempt failed
11:32:12, Policy Guard, Automatic retry blocked
```

Seed should be deterministic and repeatable. Running seed twice should not create duplicate public IDs.

---

## 27. Testing Strategy

### Unit Tests

Required:

- Policy Guard passes valid 10% bundle.
- Policy Guard blocks discount above 20%.
- Policy Guard blocks margin below 25%.
- Policy Guard blocks payment retry.
- Approval Gateway creates approval record.
- Audit Service creates product-visible event without hidden reasoning.
- Order total calculation ignores client-supplied totals.
- Razorpay signature verification rejects invalid signatures.
- Webhook idempotency rejects duplicate event processing.
- Payment failure does not create a retry attempt.

### API Tests

Required:

- `GET /merchant`
- `POST /onboarding/initialize`
- `GET /dashboard/overview`
- `GET /products`
- `GET /opportunities`
- `GET /opportunities/opp_keyboard_stand`
- `POST /opportunities/opp_keyboard_stand/approve`
- `GET /experiments`
- `GET /experiments/exp_keyboard_stand`
- `POST /experiments/exp_keyboard_stand/scale`
- `GET /ai-commerce/readiness`
- `GET /ai-commerce/products/prod_laptop_stand/profile`
- `POST /ai-commerce/optimize-catalog`
- `POST /ai-buyer/search`
- `POST /ai-buyer/basket`
- `POST /order-intents`
- `GET /order-intents/intent_ai_setup_001`
- `POST /payments/razorpay/order`
- `POST /payments/razorpay/verify`
- `POST /payments/razorpay/failure`
- `POST /webhooks/razorpay`
- `GET /payments`
- `GET /orders`
- `GET /policies`
- `PATCH /policies/policy_daily_budget`
- `POST /policies/evaluate`
- `GET /agents/status`
- `GET /agents/activity`
- `GET /audit`
- `GET /audit/audit_001`

### Integration Tests

Primary demo path:

1. Initialize NovaTech Store.
2. Fetch overview.
3. Fetch opportunity detail.
4. Approve opportunity.
5. Fetch experiment detail.
6. Scale experiment.
7. Fetch AI Commerce readiness.
8. Run AI buyer search.
9. Create basket.
10. Create order intent.
11. Create Razorpay order.
12. Verify success or record failure.
13. Fetch audit and confirm event chain.

Failure path:

1. Create order intent.
2. Create Razorpay order.
3. Record failure.
4. Confirm automatic retry blocked.
5. Confirm order remains unpaid.
6. Confirm inventory unchanged.
7. Confirm audit rows include `Payment failed` and `Retry blocked`.

### Test Data Rules

- Tests should use isolated database name, for example `raygo_test`.
- Seed fixtures must be deterministic.
- Tests should not require live Razorpay unless marked integration and keys are present.
- Signature verification can use known test HMAC fixtures.

---

## 28. Local Development

### Backend Setup

```text
cd apps/api
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python -m app.db.seed
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

On macOS/Linux, use the equivalent virtual environment activation command.

### MongoDB Options

Option A: local MongoDB.

```text
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=raygo
```

Option B: Docker MongoDB.

```text
docker run --name raygo-mongo -p 27017:27017 -d mongo:7
```

### Frontend Integration

The completed frontend should point at:

```text
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_RAZORPAY_KEY_ID=<test key id only>
```

Smoothness requirements:

- Backend must respond quickly with seeded data.
- Backend must keep existing route-driven frontend navigation.
- Backend must return `nextRoute` for workflow endpoints.
- Backend must provide stable empty/error/loading-compatible responses.
- Backend must support CORS from local frontend origin.

---

## 29. Implementation Phases

### Phase 3.1: Backend Foundation

Tasks:

- Create FastAPI app.
- Add settings, logging, errors, CORS, request IDs.
- Connect MongoDB.
- Create indexes.
- Add health endpoints.
- Add seed/reset script.

Acceptance:

- App starts locally.
- Health and DB health pass.
- Seed data loads idempotently.

### Phase 3.2: Read APIs For Completed Frontend

Tasks:

- Implement merchant, dashboard, products, opportunities, experiments, policies, agents, audit read endpoints.
- Match seeded demo values exactly.

Acceptance:

- Frontend can switch overview, opportunity, experiment, policies, agents, products, payments, orders, and audit screens from mock services to backend reads.

### Phase 3.3: Policy, Approval, And Experiment Mutations

Tasks:

- Implement Policy Guard.
- Implement Approval Gateway.
- Implement opportunity approval.
- Implement experiment scaling.
- Implement catalog optimization.
- Implement audit events for all mutations.

Acceptance:

- Approving `opp_keyboard_stand` returns `exp_keyboard_stand` and `/experiments/exp_keyboard_stand`.
- Scaling `exp_keyboard_stand` returns `/ai-commerce`.
- Policy violations fail closed.

### Phase 3.4: AI Buyer And Order Intent Backend

Tasks:

- Implement deterministic AI buyer search.
- Implement basket creation.
- Implement order intent creation/detail.
- Validate catalog and totals server-side.

Acceptance:

- Buyer request under ₹70,000 returns ProBook 14, USB-C Dock, and Laptop Stand.
- Checkout route can load `intent_ai_setup_001`.

### Phase 3.5: Razorpay Test Mode Boundary

Tasks:

- Implement Razorpay service.
- Implement order creation.
- Implement signature verification.
- Implement failure recording.
- Implement webhook verification/idempotency.
- Implement payment and order list updates.

Acceptance:

- Test success can reach `/payment/success`.
- Test failure can reach `/payment/failure`.
- No automatic retry occurs.
- Audit trail records payment success/failure and retry blocked.

### Phase 3.6: Hardening And Handoff

Tasks:

- Add API tests and integration tests.
- Add README backend setup.
- Add `.env.example`.
- Add OpenAPI review.
- Add frontend integration notes.
- Add AI agent handoff notes.

Acceptance:

- A developer can run backend locally, seed data, connect frontend, and complete demo flow in under 5 minutes.

---

## 30. Acceptance Criteria

The backend MVP is complete when:

- FastAPI serves all required `/api/v1` endpoints.
- MongoDB persists all required entities.
- Seed data exactly preserves NovaTech Store, products, metrics, opportunity, experiment, policy, AI buyer, payment, and audit demo values.
- Completed frontend can replace mock data with backend calls without redesign.
- `GET /dashboard/overview` returns the required metrics and top opportunity.
- `GET /opportunities/opp_keyboard_stand` supports the opportunity detail screen.
- `POST /opportunities/opp_keyboard_stand/approve` evaluates policy, records approval, creates/returns `exp_keyboard_stand`, writes audit, and returns `/experiments/exp_keyboard_stand`.
- `POST /experiments/exp_keyboard_stand/scale` evaluates policy, records approval, writes audit, and returns `/ai-commerce`.
- AI Commerce readiness returns `82`.
- AI Buyer search returns the seeded setup under ₹70,000 with total `₹68,499`.
- Order intent `intent_ai_setup_001` powers `/checkout/:orderIntentId`.
- Razorpay order creation happens server-side only.
- Razorpay signature verification happens server-side only.
- Webhook signature validation uses raw request body.
- Webhook processing is idempotent.
- Payment failure blocks automatic retry.
- Order remains unpaid and inventory unchanged after failure.
- Audit trail records consequential actions.
- Policy Guard blocks discount above 20%, margin below 25%, payment retry, and refund execution.
- Payment retry policy remains `BLOCKED` and `strict`.
- Errors use stable JSON shape and include request ID.
- Logs include correlation IDs and no secrets.
- Tests cover core read APIs, policy, approval, payment success/failure, idempotency, and audit.

---

## 31. Definition Of Done

Code is done when:

- Backend starts with one documented command.
- MongoDB connection is configurable.
- Indexes are created automatically.
- Seed/reset works idempotently.
- `.env.example` is complete.
- All endpoint response shapes are documented and tested.
- Mutating routes use idempotency.
- Policy Guard is used before consequential actions.
- Approval Gateway is used where merchant approval is required.
- Audit Service records all consequential transitions.
- Razorpay Test Mode keys stay server-side.
- Razorpay verification and webhook validation are tested.
- No automatic payment retry is implemented.
- Frontend can run against backend with `NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1`.
- README explains local setup, seed, test, and demo flow.
- OpenAPI docs load locally.
- No hidden chain-of-thought is exposed through audit or agent endpoints.
- Future Gemini/ADK integration can plug into typed agent services without changing API contracts.

---

## 32. Handoff To Next AI-Agent Phase

After this backend MVP is complete, the next phase may implement Gemini + Google ADK.

The AI-agent phase should receive:

- Stable domain schemas.
- Stable `/api/v1` contracts.
- Passing deterministic agent tests.
- Agent run persistence.
- Policy Guard service.
- Approval Gateway service.
- Audit Service.
- Seeded demo data.
- Clear examples of agent outputs.
- Feature flags for `USE_MOCK_AGENTS` and `USE_ADK_ORCHESTRATOR`.

Next-phase rule:

Gemini and Google ADK may improve reasoning, recommendations, catalog interpretation, and orchestration, but they must operate inside the backend's typed, policy-gated, auditable boundaries. They must not directly execute payments, bypass approvals, mutate policies, retry payments, or hide decisions from Audit Trail.

---

## 33. Final Backend Product Statement

The Phase 3 RAYGO backend turns the completed glassmorphism frontend from a polished demo shell into a real, stateful, policy-aware commerce system. It preserves the existing frontend experience while adding the backend controls judges need to trust the product: deterministic revenue opportunities, explicit approvals, auditable experiments, AI-buyer order intents, Razorpay Test Mode payment verification, safe failure handling, and a clean integration seam for Gemini + Google ADK.

