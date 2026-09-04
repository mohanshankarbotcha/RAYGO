# RAYGO: Golden Demo & Failure Demo Evaluation Guide

**Buildathon:** Razorpay AI Builder 2026 — Track 01: AI Growth & Agentic Commerce  
**Target Audience:** Judges, Evaluators & Technical Reviewers  
**Estimated Demo Time:** 5 Minutes

---

## 1. Demo Objective
Demonstrate how RAYGO acts as an autonomous revenue engine that:
1. Identifies hidden revenue opportunities in real commerce data.
2. Formulates policy-compliant growth experiments for human approval.
3. Exposes the catalog to autonomous AI Buyer agents for natural language purchasing.
4. Completes verified Razorpay checkout with server-side signature validation.
5. Handles payment failures gracefully without risking duplicate charges.
6. Records complete cryptographic forensic audit trails and agent execution traces.

---

## 2. Preconditions & Environment
- **Backend API Server**: Running at `http://localhost:8000` (FastAPI).
- **Frontend Application**: Running at `http://localhost:3000` (Next.js 14).
- **Merchant Persona**: `NovaTech Electronics` (`merchant_novatech`).
- **Initial State**: Seeded catalog with 19 products, active policies, and detected opportunities.

---

## 3. Step-by-Step Walkthrough: Golden Path (3.5 Minutes)

### Step 1: Open Merchant Dashboard
- **Action**: Navigate to `http://localhost:3000/overview`.
- **Expected UI**:
  - Live revenue metrics: Total Revenue `₹2,84,620`, RAYGO Lift `+14.2%`, AI Commerce Readiness `82/100`.
  - Active opportunities carousel displaying high-synergy recommendations.
  - Live agent status indicators showing all 7 agents operational.
- **AI Evidence**: Real-time aggregation of cross-sell synergies and catalog health score.

---

### Step 2: Review & Approve Revenue Opportunity
- **Action**: Navigate to `http://localhost:3000/opportunities` and click on **`ProBook + Ergonomic Stand Bundle`** (`opp_keyboard_stand`).
- **Expected UI**:
  - Opportunity detail showing expected monthly impact (`+₹1,42,500/mo`), confidence score (`92%`), and risk level (`Low`).
  - **Policy Guard Preview**: Confirms proposed discount (`15%`) is below the 20% ceiling, and projected margin (`32%`) is above the 25% floor.
  - Action button: **"Approve & Create Experiment"**.
- **Action**: Click **"Approve & Create Experiment"**.
- **Expected UI**: System creates experiment and automatically routes to `/experiments/exp_keyboard_stand`.
- **Safety Evidence**: Consequential state change was gated by Policy Guard and required explicit human confirmation.

---

### Step 3: Scale Experiment to AI Catalog
- **Action**: On `http://localhost:3000/experiments/exp_keyboard_stand`, review the A/B test variants.
- **Expected UI**: Live telemetry shows Variant B outperforming Variant A with positive margin lift.
- **Action**: Click **"Scale Variant to AI Catalog"**.
- **Expected UI**: Navigates to `/ai-commerce` confirming new bundle is now indexed for AI buyers.

---

### Step 4: AI Buyer Autonomous Purchasing Flow
- **Action**: Navigate to `http://localhost:3000/ai-commerce`.
- **Action**: In the AI Buyer prompt box, enter:
  > `"I need a laptop setup for AI development and college under 70000"`
- **Action**: Click **"Search with AI Buyer"**.
- **Expected UI**:
  - Semantic matcher returns optimized basket: `ProBook Laptop` + `USB-C Hub` totaling `₹68,499` (within the ₹70,000 budget).
  - Compatibility validation confirms hardware synergy.
- **Action**: Click **"Generate Order Intent"** → System redirects to `/checkout/[orderIntentId]`.

---

### Step 5: Razorpay Checkout & Server Verification
- **Action**: On `/checkout/[orderIntentId]`, review the order intent details (`₹68,499`).
- **Action**: Click **"Pay ₹68,499 with Razorpay"**.
- **Expected UI**:
  - Razorpay Test Mode checkout modal launches.
  - Authorize the test payment.
  - Modal closes, backend verifies HMAC-SHA256 signature server-side.
  - Success screen (`/payment/success`) confirms paid order (`status: "paid"`).
- **Razorpay Evidence**: Server-side verification of payment attempt with Razorpay Order ID and Payment ID.

---

### Step 6: Agent Orchestration & Forensic Audit Trail
- **Action**: Navigate to `http://localhost:3000/agents`.
- **Expected UI**:
  - Live timeline displaying execution steps from Revenue Intelligence → Growth Strategist → Policy Guard → Approval Gateway → Payment Agent.
  - Switch to **"Execution Run Traces"** tab and click any run to inspect the **Trace Drawer** (latencies in ms, tool arguments, policy check outputs).
- **Action**: Navigate to `http://localhost:3000/audit`.
- **Expected UI**:
  - Immutable audit trail listing every state transition correlated by `orderIntentId`.
- **Audit Evidence**: Full end-to-end traceability with cryptographic event IDs.

---

## 4. Step-by-Step Walkthrough: Failure & Resilience Demo (1.5 Minutes)

### Scenario: Payment Card Decline with Blocked Auto-Retry
1. **Trigger**: On `/checkout/[orderIntentId]`, simulate a payment failure (or trigger `POST /api/v1/payments/razorpay/failure` with `BAD_REQUEST_ERROR`).
2. **Deterministic Classification**: `RevenueRecoveryService` analyzes the failure and diagnoses it as `card_declined`.
3. **Hard Policy Boundary**: Policy Guard evaluates `retry_payment` and permanently blocks background automatic retries to protect against duplicate card charges.
4. **Recovery UI**: User is shown clear remediation:
   - *"Payment was declined by issuing bank."*
   - *"Automatic retry blocked by Policy Guard to prevent duplicate billing."*
   - *"Try UPI, Netbanking, or another card."*
5. **Audit Trail Verification**: On `/audit`, confirm that the payment failure and the retry rejection were logged with `outcome: "blocked"`.

---

## 5. Reset Procedure
If you wish to re-run the entire demonstration from clean initial data:
```bash
# Restart backend to reload clean in-memory repository state:
curl -X POST http://localhost:8000/api/v1/onboarding/reset
```
Or simply restart the FastAPI process.
