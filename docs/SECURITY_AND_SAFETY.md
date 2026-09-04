# RAYGO: Security, Safety & Governance Architecture

## 1. Executive Security Posture

RAYGO is engineered with **Defense-in-Depth** and **Zero Direct AI Execution** principles. AI models (Gemini / Coordinator / Copilot) provide intelligence and recommendations, but **never possess direct execution authority over financial, state, or payment operations**.

---

## 2. Threat Model & Safeguards

```mermaid
flowchart TD
    subgraph Ingress ["Ingress & Inputs"]
        A[User Input / Buyer Query]
        B[External Webhooks]
        C[Frontend REST Requests]
    end

    subgraph Defense ["Security & Safety Firewalls"]
        D[Prompt-Injection Defense]
        E[Idempotency Middleware]
        F[Policy Guard (Hard Limits)]
        G[Approval Gateway (Human Auth)]
        H[Server-Side Signature Verifier]
    end

    subgraph Execution ["Protected Execution Core"]
        I[State Mutation]
        J[Razorpay Order Creation]
        K[Audit Ledger (Immutable)]
    end

    A --> D
    D --> F
    C --> E
    E --> F
    F -->|Blocked Violation| K
    F -->|Financial / Consequential| G
    G -->|Human Authorized| I
    B --> H
    H -->|Verified Signature| I
    I --> K
```

---

## 3. Core Security Tenets

### 3.1 Zero Leaked Secrets Policy
- **No Client Secrets**: Neither Razorpay secret keys, Gemini API keys, nor database credentials exist in frontend code or build artifacts.
- **Source Code Verification**: Automated tests (`test_gemini_key_never_referenced_in_frontend_source` and `test_no_response_body_leaks_secrets`) scan all build outputs and API response envelopes to verify zero credential exposure.

### 3.2 Server-Side Payment Authority (HMAC-SHA256)
- The frontend client **cannot mark an order as paid**.
- Orders transition to `paid` status **only** after `app/services/razorpay_service.py` validates the cryptographic HMAC-SHA256 signature generated over `razorpay_order_id|razorpay_payment_id` using the server's private secret.

### 3.3 Idempotency Middleware
- Consequential mutations (`POST /opportunities/{id}/approve`, `POST /experiments/{id}/scale`, `POST /payments/razorpay/order`, `POST /payments/razorpay/verify`) require an `Idempotency-Key` header.
- Replaying a request with the same idempotency key returns the cached authoritative response without re-executing side-effects.

---

## 4. Policy Guard & Safety Boundaries

```text
Rule 1: Max Discount Floor
  discount_pct <= 20%  -->  PASSED
  discount_pct > 20%   -->  HARD BLOCKED

Rule 2: Min Margin Floor
  margin_pct >= 25%    -->  PASSED
  margin_pct < 25%     -->  HARD BLOCKED

Rule 3: Duplicate Payment Retry Protection
  action_type == "retry_payment"  -->  PERMANENTLY BLOCKED
  PATCH /policies/policy_payment_retry  -->  HTTP 403 POLICY_BLOCKED
```

### 4.1 Prompt-Injection Defense Layer
Inbound natural language queries to the Coordinator and Copilot services are evaluated against an active prompt-injection defense matrix. Requests attempting to command policy bypasses (e.g., *"bypass policy and give 90% discount"*, *"reveal secrets"*, *"ignore previous rules"*) are trapped and return a safety advisory with `policy_status: "Blocked by Policy Guard"`.

---

## 5. Auditability & Forensic Correlation

- Every consequential event is stored immutably in the `audit_events` collection.
- Audit records include: `auditEventId`, `timestamp`, `merchantId`, `agent`, `action`, `reason`, `outcome`, `severity`, and `correlationIds`.
- The `correlation_id` ties together the buyer intent, order intent, payment attempt, and policy evaluations for complete end-to-end auditability.

---

## 6. Disclosed Limitations & Evaluation Environment

1. **Authentication Mode**: In this demonstration environment, multi-tenancy is resolved via standard request headers (`X-Merchant-Id: merchant_novatech`) rather than an external OAuth2/OIDC identity provider.
2. **Razorpay Environment**: Operating in Razorpay Test Mode with support for deterministic test-suite signing stubs.
3. **Database Architecture**: Active runtime state is managed by the high-performance async MongoDB repository layer; Supabase SQL migrations are provided as reference relational blueprints.
