# RAYGO Claude Implementation PRD
## Frontend-First Build, Backend and Agent Integration Second

Document owner: RAYGO team  
Target implementer: Claude / Claude Code  
Date: 2026-08-31  
Track: Razorpay AI Builder Internship 2026, Track 1: AI Growth & Agentic Commerce  
Primary constraint: MVP must be implemented rapidly, correctly, and demo-ready.

---

## 1. Purpose

Build RAYGO as a frontend-first full-stack MVP using the exported Google Stitch project as the source of truth for information architecture, terminology, screen behavior, design tokens, demo data, and user flows.

The first milestone is a polished, working frontend that reproduces the Stitch experience as a real web app. The second milestone connects that frontend to a backend API, policy engine, agent orchestration layer, Razorpay Test Mode payment flow, and audit trail.

Do not redesign the product from scratch. Convert and extend the Stitch work into a maintainable app.

---

## 2. Source Material To Preserve

Use the uploaded Stitch export and reference screenshots as the design baseline.

Stitch export includes:

- `onboarding_raygo`
- `executive_overview_raygo`
- `opportunity_center_raygo`
- `opportunity_detail_raygo`
- `experiment_detail_raygo`
- `ai_commerce_raygo`
- `ai_buyer_raygo`
- `ai_checkout_raygo`
- `payment_success_raygo`
- `payment_failure_raygo`
- `agent_activity_raygo`
- `policies_raygo`
- `audit_trail_raygo`
- `autonomous_revenue_intelligence/DESIGN.md`
- earlier Google Stitch PRD and modification PRD notes

Design source of truth:

- Product name: `RAYGO`
- Merchant: `NovaTech Store`
- Category: `Consumer Electronics`
- Currency: INR
- Core product loop: `Observe -> Discover -> Reason -> Plan -> Guard -> Approve -> Execute -> Measure -> Learn`
- Core UI principle: fintech trust, operational clarity, AI reasoning transparency

---

## 3. Product Summary

RAYGO is an autonomous revenue intelligence platform for AI-native commerce.

It helps merchants:

- Discover revenue opportunities from commerce signals.
- Understand evidence behind AI recommendations.
- Approve bounded revenue actions.
- Run measurable growth experiments.
- Make the product catalog AI-readable.
- Let AI buyers construct and authorize purchases.
- Execute payments through Razorpay Test Mode.
- Safely handle payment failure.
- Audit every consequential AI and payment action.

RAYGO must not feel like a generic chatbot. It must feel like a controlled revenue operating layer.

---

## 4. MVP Priority

Build in this order.

### P0: Required For Demo

1. App shell, routing, shared design system
2. Onboarding
3. Executive Overview
4. Opportunity Center
5. Opportunity Detail
6. Experiment Detail
7. AI Commerce Readiness
8. AI Buyer
9. AI Checkout
10. Payment Success
11. Payment Failure
12. Policies / Revenue Action Firewall
13. Agent Activity
14. Audit Trail
15. Mock API layer with typed data contracts
16. Backend endpoints replacing mock API
17. Razorpay Test Mode order creation, checkout, verification, and failure handling

### P1: Important But Secondary

1. Products
2. Orders
3. Payments
4. Experiments list
5. Ask RAYGO command palette
6. Toasts, drawers, modals, skeleton states
7. End-to-end demo tests

### P2: Defer Unless P0/P1 Are Complete

1. Authentication
2. Merchant settings beyond policy controls
3. Real campaign execution
4. Advanced analytics
5. Multi-merchant support
6. Live LLM streaming
7. Production deployment hardening beyond demo needs

---

## 5. Required Tech Stack

Use this stack. Do not substitute Vite, Express, PostgreSQL, Firebase, Supabase, Stripe, or another agent framework unless the user explicitly changes the stack later.

### Frontend

- Next.js 14 or 15 with App Router
- TypeScript
- TailwindCSS
- Framer Motion for restrained workflow transitions
- Recharts for dashboard and experiment charts
- Componentized app shell
- Lucide React icons preferred
- TanStack Query or a small typed API client
- Recharts for simple charts
- Zod for API schema validation

Frontend requirements:

- Use App Router routes under `apps/web/src/app`.
- Use server components only where they simplify static shell/data loading.
- Use client components for dashboards, modals, command palette, payment flow, and animated states.
- Keep the Stitch UI behavior intact while converting HTML screens into reusable Next.js components.
- Use Framer Motion only for purposeful transitions: drawers, approval steps, payment status, command palette, and agent timeline updates.

### Backend

- FastAPI
- Python 3.11+
- Pydantic schemas
- MongoDB via Motor or Beanie
- Razorpay Python SDK or direct HTTP client
- Server-side payment signature verification
- Webhook endpoint using raw request body validation
- Deterministic demo fallbacks for all agent flows

### AI

- Gemini
- Use structured outputs/tool calling.
- The LLM must never directly manipulate Razorpay APIs.
- Gemini may produce recommendations, explanations, catalog normalization suggestions, and buyer intent mappings.
- Backend services must validate and gate every Gemini-suggested action before it affects orders, experiments, policies, or payments.

### Agent Framework

- Google ADK
- Use ADK to model the agent orchestration layer once the deterministic MVP paths are working.
- Keep agent actions typed and auditable.
- Agent outputs must conform to Pydantic schemas before they reach the frontend or payment/policy services.

### Database

- MongoDB
- Local development may use local MongoDB or Docker MongoDB.
- Deployment uses MongoDB Atlas.

Store:

- merchants
- products
- customers
- orders
- payments
- experiments
- opportunities
- policies
- approvals
- agent actions
- audit logs
- webhook events

### Payments

- Razorpay Test Mode
- Create Razorpay orders server-side.
- Verify payment signatures server-side.
- Use webhooks for asynchronous reconciliation.
- The official Razorpay MCP server may be explored later only if it materially helps the demo or ops workflow. It is not required for the MVP and must not replace the direct Test Mode integration unless approved.

### Deployment

- Frontend: Vercel
- Backend: Render
- Database: MongoDB Atlas
- Keep `.env.example` complete for local and deployed environments.

### Repo Shape

Use this monorepo:

```text
raygo/
  apps/
    web/
    api/
  packages/
    shared/
  docs/
  scripts/
  README.md
```

### Detailed Folder Architecture

Use this structure unless the existing repo already has a strong convention.

```text
raygo/
  apps/
    web/
      src/
        app/
          layout.tsx
          page.tsx
          providers/
          onboarding/
            page.tsx
          overview/
            page.tsx
          opportunities/
            page.tsx
            [id]/
              page.tsx
          experiments/
            page.tsx
            [id]/
              page.tsx
          ai-commerce/
            page.tsx
          ai-buyer/
            page.tsx
            basket/
              page.tsx
          checkout/
            [orderIntentId]/
              page.tsx
          payment/
            success/
              page.tsx
            failure/
              page.tsx
          products/
            page.tsx
          orders/
            page.tsx
          payments/
            page.tsx
          agents/
            page.tsx
          policies/
            page.tsx
          audit/
            page.tsx
            [id]/
              page.tsx
        components/
          app-shell/
          dashboard/
          opportunities/
          experiments/
          ai-commerce/
          ai-buyer/
          checkout/
          payments/
          policies/
          agents/
          audit/
          shared/
        data/
          fixtures/
          demo-scenario.ts
        lib/
          api-client.ts
          formatters.ts
          routes.ts
          status.ts
          glass.ts
          razorpay-client.ts
        styles/
          globals.css
          tokens.css
        test/
      package.json
    api/
      app/
        main.py
        core/
          config.py
          security.py
        api/
          v1/
            router.py
            dashboard.py
            opportunities.py
            experiments.py
            ai_commerce.py
            ai_buyer.py
            payments.py
            policies.py
            agents.py
            audit.py
        domain/
          models.py
          schemas.py
          states.py
        services/
          gemini_service.py
          adk_orchestrator.py
          revenue_intelligence.py
          growth_strategist.py
          experiment_agent.py
          ai_commerce_agent.py
          policy_guard.py
          approval_gateway.py
          payment_agent.py
          audit_service.py
          razorpay_service.py
        db/
          mongo.py
          seed.py
        tests/
      requirements.txt
  packages/
    shared/
      contracts/
        api.ts
        domain.ts
  docs/
    RAYGO_Claude_Frontend_First_Implementation_PRD.md
    demo-script.md
    api-contract.md
  .env.example
  README.md
```

Frontend ownership:

- Components own rendering and interaction state only.
- Business rules live in service/API layers.
- Demo fixtures live under `data/fixtures`.
- No Razorpay secret, policy secret, or database URL is ever referenced by frontend code.

Backend ownership:

- API routes validate requests and call services.
- Services own domain behavior.
- Policy Guard is called before every consequential action.
- Audit service records all state transitions.
- Razorpay service is the only place that knows Razorpay credentials.

Environment variables:

```text
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_RAZORPAY_KEY_ID=
RAZORPAY_KEY_ID=
RAZORPAY_KEY_SECRET=
RAZORPAY_WEBHOOK_SECRET=
MONGODB_URI=
MONGODB_DB=raygo
FRONTEND_ORIGIN=http://localhost:3000
GEMINI_API_KEY=
USE_MOCK_AGENTS=true
```

---

## 6. Design System

Preserve the Stitch design system, then add a controlled glassmorphism layer.

### Existing Tokens

Use these base values from `DESIGN.md`:

- Background: `#fcf8fa`
- Surface: `#ffffff`
- Surface muted: `#F8FAFC`
- Border subtle: `#E2E8F0`
- Primary / navy: `#0F172A` or near-black from export
- On surface: `#1b1b1d`
- On surface variant: `#45464d`
- Growth green: `#10B981`
- Warning amber: `#F59E0B`
- Reasoning blue: `#3B82F6`
- Error red: `#BA1A1A`
- Accent red: `#EF4444` only for critical actions and failed states
- Font: Inter
- Base body: 14px / 20px
- Small body: 13px / 18px
- Metric display: 32px / 40px on desktop, 24px / 32px on mobile
- Base radius: 4px
- Large radius: 8px
- Desktop sidebar: 240px
- Desktop max width: 1440px

Implementation note: use `letter-spacing: 0` globally. Preserve the visual hierarchy through font weight and spacing instead of negative tracking.

### Glassmorphism Layer

Add glassmorphism as an enhancement, not a new visual identity.

Allowed glass surfaces:

- Topbar
- Sidebar background overlay
- KPI cards
- Reasoning panels
- Right-side drawers
- Payment status cards
- AI Buyer recommendation card
- Approval and policy panels

Avoid glass effects on:

- Dense tables
- Small labels
- Long body text
- Form fields with critical input
- Payment amount rows
- Audit log rows

Glass tokens:

```css
--glass-surface: rgba(255, 255, 255, 0.72);
--glass-surface-strong: rgba(255, 255, 255, 0.86);
--glass-border: rgba(255, 255, 255, 0.66);
--glass-outline: rgba(15, 23, 42, 0.10);
--glass-shadow: 0 14px 40px rgba(15, 23, 42, 0.08);
--glass-blur: blur(16px);
```

Glass component rules:

- Always preserve readable contrast.
- Add a subtle solid fallback color behind translucent surfaces.
- Use one thin border and one soft shadow max.
- Do not use neon, purple AI gradients, bokeh blobs, decorative orbs, or particle backgrounds.
- Tables remain mostly solid with subtle borders.
- Financial numbers must never appear low contrast.

---

## 7. Global Layout

### Desktop

- Persistent 240px left sidebar.
- Main content offset by sidebar.
- Topbar with merchant name, search/command field, notifications, help, profile.
- Content width constrained but not boxed into a decorative card.
- Charts and panels align to a 12-column grid.

### Tablet

- Sidebar collapses to icon rail or drawer.
- Main content uses 8-column grid.
- Tables can scroll horizontally if card conversion harms readability.

### Mobile

- Navigation becomes a drawer or bottom nav.
- KPI grid stacks.
- Tables become readable cards or horizontal scroll.
- Primary CTAs remain reachable.
- No text clipping, overlapping controls, or horizontal page overflow.

---

## 8. Navigation And Routes

Use real routes. Buttons must navigate or trigger visible state changes.

```text
/                         -> redirect to /onboarding or /overview
/onboarding               -> onboarding setup
/overview                 -> executive overview
/opportunities            -> opportunity center
/opportunities/:id        -> opportunity detail
/experiments              -> experiment list
/experiments/:id          -> experiment detail
/ai-commerce              -> AI commerce readiness
/ai-buyer                 -> customer-facing AI buyer
/ai-buyer/basket          -> basket, optional if not integrated in AI Buyer screen
/checkout/:orderIntentId  -> AI checkout authorization
/payment/success          -> payment success
/payment/failure          -> payment failure
/products                 -> product catalog
/orders                   -> orders
/payments                 -> payments
/agents                   -> agent activity
/policies                 -> revenue action firewall
/audit                    -> audit trail
/audit/:id                -> audit detail drawer or detail page
```

Sidebar order:

1. Overview
2. Opportunities
3. Experiments
4. AI Commerce
5. Orders
6. Products
7. Payments
8. Agent Activity
9. Policies
10. Audit Trail

Bottom sidebar action:

- Ask RAYGO

---

## 9. Demo Dataset

Use this same data everywhere.

Merchant:

```json
{
  "id": "merchant_novatech",
  "name": "NovaTech Store",
  "category": "Consumer Electronics",
  "currency": "INR"
}
```

Products:

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

Metrics:

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

Primary opportunity:

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

Experiment:

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

AI buyer order:

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

---

## 10. Screen Requirements

### 10.1 Onboarding

Route: `/onboarding`

Purpose: introduce RAYGO and configure the demo merchant.

Preserve Stitch headline:

`Turn commerce data into autonomous growth.`

Required content:

- RAYGO logo/name
- Descriptor: `AI revenue intelligence for modern commerce.`
- Merchant setup panel
- Store name: NovaTech Store
- Category: Consumer Electronics
- Estimated revenue range
- Product count
- Enable AI Buyer mode toggle
- CTA: `Initialize RAYGO`

Interaction:

- Clicking `Initialize RAYGO` starts a staged progress sequence:
  - Connecting merchant data
  - Mapping product catalog
  - Detecting revenue patterns
  - Preparing AI Commerce profile
  - Applying merchant policies
- After sequence, navigate to `/overview`.

States:

- Initial
- Initializing
- Complete
- Error: `Merchant setup could not be initialized. Please retry.`

### 10.2 Executive Overview

Route: `/overview`

Purpose: the strongest first impression.

Required KPI cards:

- Total Revenue: `₹2,84,620`, `+18.7% vs last period`
- RAYGO Influenced: `₹42,800`, `+14.2% AI lift`
- Active Opportunities: `7`, `Action required`
- AI Commerce Readiness: `82 / 100`

Required panels:

- `RAYGO found 7 revenue opportunities`
- top 3 opportunity cards
- Revenue Trend, 30 days
- `RAYGO's Latest Reasoning`

Latest reasoning copy:

`RAYGO analyzed 1,842 relevant purchase journeys and found a strong correlation between Wireless Keyboard purchases and Laptop Stand views. Current attach rate is 4.1%. Similar interventions suggest a potential increase to 7.8%.`

Interaction:

- `Review Opportunity` opens `/opportunities/opp_keyboard_stand`.
- AI Commerce readiness card links to `/ai-commerce`.
- Ask RAYGO opens command palette.

States:

- Loading: `Analyzing commerce signals...`
- Empty: `RAYGO has not identified a high-confidence opportunity yet.`
- Error: `Revenue analysis could not be refreshed. Your previous insights remain available.`

### 10.3 Opportunity Center

Route: `/opportunities`

Purpose: ranked workspace for detected growth opportunities.

Required summary:

- Projected Impact: `₹40,000`
- Active: `7`
- Ready for Review: `4`
- Running: `2`

Table columns:

- Opportunity
- Type
- Projected Impact
- AI Confidence
- Risk
- Status
- Action

Required rows:

- Keyboard + Stand, Cross-sell, `₹18,400`, `87%`, Low, Ready for Review
- ProBook Bundle, Bundle, `₹12,200`, `91%`, Low, Running
- Recovery Campaign, Recovery, `₹9,400`, `78%`, Medium, Ready

Interactions:

- Row click opens detail.
- Filter by type.
- Sort by impact, confidence, newest.

### 10.4 Opportunity Detail

Route: `/opportunities/:id`

Purpose: explain before asking for approval.

Required header:

- `Cross-sell opportunity: Wireless Keyboard -> Laptop Stand`
- Expected impact: `₹18,400 / month`
- Confidence: `87%`
- Target segment: `Remote Workers`

AI reasoning timeline:

- Observed: `Wireless Keyboard purchases have increased by 14% over the last 30 days.`
- Detected: `Laptop Stand views increased among the same buyer cohort.`
- Hypothesized: `Users are building complete ergonomic desk setups.`
- Predicted Outcome: `A cross-sell prompt can increase attach rate from 4.1% to 7.8%.`

Evidence cards:

- Purchase correlation: `2.3x`
- Current attach rate: `4.1%`
- Projected attach rate: `7.8%`
- Eligible journeys: `1,842`

Proposed action:

- `Create a 10% Keyboard + Laptop Stand bundle experiment.`
- Discount: `10%`
- Expected uplift: `₹18,400 / month`
- Estimated margin: `>25%`
- Budget: `Within policy`

Policy Guard:

- Discount below 20%: pass
- Margin above 25%: pass
- Campaign budget available: pass
- Merchant approval required: required

Interaction:

- `Approve & Create Experiment` opens approval modal.
- Approval modal runs:
  - Policy check
  - Merchant approval
  - Experiment created
- Then navigate to `/experiments/exp_keyboard_stand`.

Do not expose hidden chain-of-thought. Use explainable summaries only.

### 10.5 Experiments

Route: `/experiments`

Purpose: prove RAYGO measures before scaling.

Required metrics:

- Active Experiments: `3`
- Completed: `12`
- Revenue Uplift: `+₹31,800`
- Average Confidence: `91%`

Table columns:

- Experiment
- Type
- Status
- Control
- Variant
- Revenue Uplift
- Confidence

Required interaction:

- Click `Keyboard + Stand Bundle` to open `/experiments/exp_keyboard_stand`.

### 10.6 Experiment Detail

Route: `/experiments/:id`

Purpose: show measurable uplift and scale recommendation.

Required header:

- `Keyboard + Laptop Stand`
- `Growth Experiment`
- Status: `Running`
- CTA: `Scale Experiment`
- Secondary: `Keep Running`

Hypothesis:

`Bundling a Laptop Stand with Wireless Keyboard purchases will increase basket conversion without reducing merchant margin below policy.`

Experiment design:

- Control: Keyboard only, `6.2% conversion`
- Variant: Keyboard + Stand, `8.9% conversion`

Results:

- Conversion uplift: `+43.5%`
- Revenue uplift: `+23.4%`
- AOV: `+8.7%`
- Confidence: `94%`

Recommendation:

`SCALE VARIANT`

Reason:

`Variant performance exceeds control while remaining within the merchant's margin policy.`

Interaction:

- `Scale Experiment` opens confirmation modal.
- Confirmation runs Policy Guard.
- After confirmation, create audit entry and navigate to `/ai-commerce`.

### 10.7 AI Commerce

Route: `/ai-commerce`

Purpose: make AI-buyer readiness visible.

Required hero:

- `AI Commerce Readiness`
- `82 / 100`
- `Good readiness — 3 areas need attention.`

Score breakdown:

- Product Discoverability: `91`
- Structured Product Data: `82`
- Pricing Clarity: `94`
- Inventory Confidence: `63`
- Policy Clarity: `72`
- Checkout Readiness: `76`

AI Buyer blockers:

- `14 products have stale inventory data.`
- `37 products lack structured shipping information.`
- `8 products have ambiguous product attributes.`

AI-readable product profile:

- ProBook 14
- Price: `₹62,999`
- Availability: In stock
- Category: Laptop
- Best for: AI development, coding, college
- Specs: 16GB RAM, 512GB SSD, 14-inch display
- AI description: `Portable performance laptop suitable for students and developers who need strong multitasking and development capability.`

Interactions:

- `Optimize Catalog` creates a simulated improvement toast.
- `Preview as AI Buyer` navigates to `/ai-buyer`.

### 10.8 AI Buyer

Route: `/ai-buyer`

Purpose: customer-facing AI-native commerce demo.

This screen may look slightly more immersive than merchant screens but must preserve RAYGO typography, colors, and trust language.

Required header:

- `RAYGO AI Commerce`
- `Tell me what you're looking for.`

Default search prompt:

`I need a laptop setup for AI development and college under ₹70,000.`

Required recommendation:

- ProBook 14 Gen 6
- `₹62,999`
- `98% Fit`
- specs: Core Ultra 5 125H, 16GB LPDDR5x, 512GB PCIe Gen4, 1.35 kg
- Top Match badge

Why RAYGO selected this:

- Budget Constraint: `₹7,001 under your ₹70,000 maximum.`
- Memory Requirements: `16GB RAM is baseline for local AI development.`
- College Suitability: `Lightweight with strong battery life.`
- Immediate Stock: `Available for dispatch today.`
- AI Checkout Support: `Eligible for automated discount application.`

Other valid options:

- Ryzen 7 laptop, `₹65,490`
- RTX 3050 laptop, `₹69,990`

Interactions:

- Search runs a visible loading state: `Matching buyer intent to AI-readable catalog...`
- `Add to Basket` adds ProBook 14, USB-C Dock, and Laptop Stand bundle.
- `Review Purchase` navigates to `/checkout/intent_ai_setup_001`.

### 10.9 AI Checkout

Route: `/checkout/:orderIntentId`

Purpose: purchase authorization before payment.

Required sections:

- Buyer request
- Why RAYGO prepared this purchase
- Selected products
- Order summary
- Authorization Gate

Order summary:

- Subtotal: `₹69,797`
- Bundle discount: `-₹1,298`
- Taxes & Fees: `Calculated`
- Total: `₹68,499`

Authorization Gate:

`Purchase authorization required`

`RAYGO will not execute payment until you confirm this purchase.`

Button:

`Confirm & Pay`

Label:

`Razorpay Test Mode`

Interaction:

- Frontend calls backend to create an order.
- Backend creates Razorpay order server-side.
- Frontend opens Razorpay Checkout using returned order id.
- Success returns `razorpay_payment_id`, `razorpay_order_id`, and `razorpay_signature` to backend for verification.
- Failure routes to `/payment/failure`.

### 10.10 Payment Success

Route: `/payment/success`

Purpose: credible success state.

Required content:

- `Payment Successful`
- Amount paid: `₹68,499`
- Order ID: `#RGO-10482`
- Status: `Captured`
- Environment: `Razorpay Test Mode`

Transaction timeline:

- Intent received
- Products selected
- Order created
- Payment authorized
- Order confirmed

AI Commerce Summary:

- Decision time: `2.4 sec`
- Recommendation confidence: `92%`
- Action: `Checkout Completed`

Interaction:

- `Return to Merchant Dashboard` navigates to `/overview`.
- Write audit entries for order creation, payment verification, and completion.

### 10.11 Payment Failure

Route: `/payment/failure`

Purpose: critical judge demo proving safe failure handling.

Required content:

- `Payment Unsuccessful`
- Amount: `₹68,499`
- Reason: `Payment attempt was unsuccessful. No funds have been captured from your account.`

Critical status:

- `AUTOMATIC RETRY: BLOCKED`
- Reason: `Duplicate-charge protection`

RAYGO Safety Response:

- No duplicate payment attempted
- Order remains unpaid
- Inventory unchanged
- Failure recorded in audit trail
- Recovery option generated

Actions:

- Primary: `Try Another Payment Method`
- Secondary: `Return to Basket`
- Tertiary: `View Audit Trail`

Interaction:

- Never auto-retry payment.
- Failure webhook or client failure writes audit entry.
- `View Audit Trail` opens `/audit` with failed payment row selected.

### 10.12 Agent Activity

Route: `/agents`

Purpose: make the multi-agent architecture visible.

Agent status cards:

- Revenue Intelligence: Active
- AI Commerce: Active
- Growth Strategist: Active
- Experiment Agent: Running
- Policy Guard: Active
- Payment Agent: Ready
- Approval Gateway: Ready

Live activity timeline:

- 11:32:04, Revenue Intelligence, Detected cross-sell opportunity
- 11:32:05, Growth Strategist, Generated experiment hypothesis
- 11:32:06, Policy Guard, Policy check passed
- 11:32:07, Approval Gateway, Merchant approval received
- 11:32:08, Experiment Agent, Experiment created
- 11:32:12, Payment Agent, Payment attempt failed
- 11:32:12, Policy Guard, Automatic retry blocked

Interaction:

- Timeline can auto-append during demo using mock events.
- Event click opens related audit entry.

### 10.13 Policies / Revenue Action Firewall

Route: `/policies`

Purpose: show that AI cannot freely manipulate money.

Required policy cards:

- Discount Limit: max `20%`, active
- Margin Floor: min `25%`, active
- Daily Budget: `₹10,000`, review
- Auto Execution: `OFF`, paused
- Merchant Auth: `REQUIRED`, enforced
- Payment Retry: `BLOCKED`, strict

Action Matrix columns:

- Action Type
- Can Propose
- Can Execute
- Approval Requirement

Required rows:

- Create Bundle: propose yes, execute yes, approval required
- Discount >20%: propose yes, execute no, blocked
- Create Campaign: propose yes, execute yes, approval required
- Payment Retry: propose yes, execute no, blocked
- Refund: propose yes, execute no, approval required

Interactions:

- Editing a policy changes frontend state and writes audit entry.
- Payment Retry must remain blocked for MVP.

### 10.14 Audit Trail

Route: `/audit`

Purpose: every consequential AI action is explainable and reconstructable.

Table columns:

- Timestamp
- Agent
- Action
- Reason
- Policy
- Approval
- Outcome

Required rows:

- Payment Agent, Create Order, Buyer confirmed purchase, Passed, Confirmed, Success
- Payment Agent, Retry Payment, Payment failed, Blocked, N/A, Prevented
- Experiment Agent, Create Experiment, Merchant approved recommendation, Passed, Confirmed, Success

Detail drawer:

- Decision Summary
- Evidence
- Action
- Policy Checks
- Approval
- Execution Result
- Failure / Recovery
- Related Order
- Raw metadata collapsible panel

Rules:

- Do not show hidden chain-of-thought.
- Show concise decision explanations and auditable metadata only.
- Include correlation IDs for order, payment, policy check, agent run, and audit event.

### 10.15 Products

Route: `/products`

Purpose: catalog readiness workspace.

Table columns:

- Product
- Price
- Inventory
- AI Readiness
- Issues
- Status

Rows:

- ProBook 14, `₹62,999`, 42, 94, None, Ready
- Laptop Stand, `₹1,799`, 12, 81, Shipping metadata, Needs Attention
- USB-C Dock, `₹4,999`, 20, 84, None, Ready

Interaction:

- `Optimize with RAYGO` simulates metadata optimization and writes audit event.

### 10.16 Orders

Route: `/orders`

Purpose: commerce order list.

Metrics:

- GMV
- Successful Payments
- Failed Payments
- AI Buyer Orders

Table columns:

- Order
- Customer
- Amount
- Source
- Payment
- Status

Required AI buyer order:

- `#RGO-10482`
- Customer: `AI Buyer Demo`
- Amount: `₹68,499`
- Source: `AI Buyer`
- Payment: Razorpay Test Mode
- Status: Success or Failed based on selected demo path

### 10.17 Payments

Route: `/payments`

Purpose: payment status workspace.

Metrics:

- Successful
- Failed
- Pending
- Refunds

Table columns:

- Payment ID
- Order
- Amount
- Method
- Status
- Timestamp

Required:

- Test Mode label.
- Failure row visible after failed checkout.

### 10.18 Ask RAYGO

Component: command palette, not a full chatbot page.

Trigger:

- Sidebar bottom action
- Topbar command input

Suggested commands:

- Why did revenue change yesterday?
- Show my highest-value opportunities.
- Which experiment should I scale?
- Why is AI Commerce readiness 82?
- Show blocked actions.

Behavior:

- Selecting a command returns a concise answer and links to the relevant route.
- Do not build long chatbot history for MVP.

---

## 11. Shared Components

Build these reusable components:

- `AppShell`
- `Sidebar`
- `Topbar`
- `CommandPalette`
- `MetricCard`
- `GlassPanel`
- `StatusBadge`
- `ProgressBar`
- `OpportunityCard`
- `DataTable`
- `ReasoningTimeline`
- `EvidenceCard`
- `PolicyGuard`
- `ApprovalModal`
- `ExperimentResults`
- `ReadinessScore`
- `BuyerSearch`
- `ProductRecommendationCard`
- `BasketSummary`
- `CheckoutSummary`
- `PaymentStatusCard`
- `AgentStatusCard`
- `ActivityTimeline`
- `AuditTable`
- `AuditDetailDrawer`
- `EmptyState`
- `LoadingState`
- `ErrorState`
- `Toast`
- `Modal`
- `Drawer`

Component rules:

- Use stable dimensions for cards, icon buttons, counters, and table rows.
- Do not nest cards inside cards.
- Use icons for tool buttons where possible.
- Buttons must have default, hover, focus, loading, disabled, success, and error states.
- Status must use label plus icon, never color only.

---

## 12. Backend Domain Model

Core entities:

- Merchant
- Product
- Opportunity
- Experiment
- Policy
- PolicyEvaluation
- Approval
- AgentRun
- AuditEvent
- BuyerIntent
- Cart
- OrderIntent
- RazorpayOrder
- PaymentAttempt
- WebhookEvent

Minimum persisted fields:

```text
id
created_at
updated_at
status
metadata
```

Audit all consequential state changes.

---

## 13. API Contract

Use `/api/v1`.

### Merchant

```text
GET  /api/v1/merchant
POST /api/v1/onboarding/initialize
```

### Dashboard

```text
GET /api/v1/dashboard/overview
```

Response includes metrics, top opportunities, revenue trend, latest reasoning.

### Opportunities

```text
GET  /api/v1/opportunities
GET  /api/v1/opportunities/{opportunity_id}
POST /api/v1/opportunities/{opportunity_id}/approve
```

Approval response:

```json
{
  "approvalId": "appr_001",
  "policyEvaluationId": "pol_eval_001",
  "experimentId": "exp_keyboard_stand",
  "status": "approved",
  "nextRoute": "/experiments/exp_keyboard_stand"
}
```

### Experiments

```text
GET  /api/v1/experiments
GET  /api/v1/experiments/{experiment_id}
POST /api/v1/experiments/{experiment_id}/scale
```

### AI Commerce

```text
GET  /api/v1/ai-commerce/readiness
GET  /api/v1/ai-commerce/products/{product_id}/profile
POST /api/v1/ai-commerce/optimize-catalog
```

### AI Buyer

```text
POST /api/v1/ai-buyer/search
POST /api/v1/ai-buyer/basket
POST /api/v1/order-intents
GET  /api/v1/order-intents/{order_intent_id}
```

### Payments

```text
POST /api/v1/payments/razorpay/order
POST /api/v1/payments/razorpay/verify
POST /api/v1/payments/razorpay/failure
POST /api/v1/webhooks/razorpay
GET  /api/v1/payments
GET  /api/v1/orders
```

### Policies

```text
GET   /api/v1/policies
PATCH /api/v1/policies/{policy_id}
POST  /api/v1/policies/evaluate
```

### Agents

```text
GET /api/v1/agents/status
GET /api/v1/agents/activity
```

### Audit

```text
GET /api/v1/audit
GET /api/v1/audit/{audit_event_id}
```

---

## 14. Agent Behavior

Implement agents as deterministic services for MVP. Optional LLM calls can be added behind feature flags.

Required logical agents:

1. Revenue Intelligence Agent
2. AI Commerce Agent
3. Growth Strategist Agent
4. Experiment Agent
5. Policy Guard
6. Payment Agent
7. Approval Gateway

### Revenue Intelligence Agent

Inputs:

- Orders
- Products
- Cart behavior
- Product views
- Margins
- Abandonment metrics

Output:

- Ranked opportunities with expected impact, confidence, evidence, risk.

MVP behavior:

- Return deterministic opportunities based on demo dataset.

### Growth Strategist Agent

Inputs:

- Opportunity
- Product margins
- Policy rules

Output:

- Proposed experiment, hypothesis, discount, expected uplift.

### Experiment Agent

Inputs:

- Approved proposal
- Simulated experiment results

Output:

- Control/variant metrics, uplift, confidence, recommendation.

### AI Commerce Agent

Inputs:

- Product catalog
- Buyer intent
- AI readiness rules

Output:

- Readiness score, blockers, AI-readable product profile, buyer recommendations.

### Policy Guard

Inputs:

- Proposed action
- Merchant policies
- Payment status

Output:

- pass, requires approval, or blocked
- reasons
- policy evaluation record

### Approval Gateway

Inputs:

- Policy evaluation
- Merchant click confirmation

Output:

- approval record and audit event.

### Payment Agent

Inputs:

- Order intent
- Razorpay order/payment status
- Policy rules

Output:

- payment attempt records
- no automatic retry after failure
- audit entries

---

## 15. Policy And Approval Logic

Every financial action must pass through this state flow:

```text
proposed -> policy_evaluated -> approval_required -> merchant_approved -> execution_pending -> executed | blocked | failed
```

Policy outcomes:

- `passed`
- `requires_approval`
- `blocked`

Required policies:

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

Hard rules:

- Discount above 20% is blocked.
- Margin below 25% is blocked.
- Payment retry is blocked after failed payment.
- Refund execution is not allowed in MVP.
- Merchant approval is required before experiments and payment execution.
- The app must never imply RAYGO can spend money without authorization.

---

## 16. Razorpay Integration Expectations

Use Razorpay Test Mode only.

Reference behavior from Razorpay docs:

- Create an order on the server for every payment.
- Pass returned `order_id` to Checkout.
- Verify payment signature server-side before fulfilling order.
- Use webhooks for asynchronous payment/order events.
- Use API verification when user-facing confirmation needs immediate status.
- Test mode supports simulated success and failure and uses no real money.

Payment implementation flow:

```text
AI Checkout
  -> POST /payments/razorpay/order
  -> backend creates Razorpay order in INR smallest unit
  -> frontend opens Razorpay Checkout
  -> success handler POST /payments/razorpay/verify
  -> backend verifies signature
  -> backend marks order paid/captured only after verification
  -> frontend routes to /payment/success
```

Failure flow:

```text
Checkout failure
  -> POST /payments/razorpay/failure
  -> backend records failed attempt
  -> Policy Guard blocks automatic retry
  -> audit event created
  -> frontend routes to /payment/failure
```

Webhook flow:

```text
Razorpay webhook
  -> POST /webhooks/razorpay
  -> verify X-Razorpay-Signature using raw request body
  -> idempotently store event
  -> reconcile payment/order state
  -> write audit event
```

Required webhook event handling:

- `order.paid`
- `payment.captured`
- `payment.failed`
- `payment.authorized`

Security:

- Razorpay key secret is backend-only.
- Frontend receives only public key id and order id.
- Reject payment success if signature verification fails.
- Do not fulfill orders from client success alone.
- Store webhook event IDs and process idempotently.

---

## 17. Audit Trail Contract

Create audit events for:

- Opportunity created
- Opportunity approved
- Policy evaluated
- Experiment created
- Experiment scaled
- AI buyer search completed
- Order intent created
- Razorpay order created
- Payment verified
- Payment failed
- Retry blocked
- Policy changed

Audit event schema:

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
    "policyChecks": [
      {"policy": "Payment Retry", "result": "blocked", "reason": "Duplicate-charge protection"}
    ],
    "executionResult": "No retry attempted"
  }
}
```

---

## 18. State Requirements

Every major workflow needs user-visible states.

Opportunity approval:

- Idle
- Evaluating policy
- Approval required
- Approved
- Experiment created
- Failed

AI buyer search:

- Empty input
- Searching
- Results
- No matching products
- Error

Checkout:

- Review
- Creating order
- Awaiting authorization
- Verifying payment
- Success
- Failure

Agent services:

- Active
- Running
- Ready
- Paused
- Error

Audit:

- Loading
- Empty
- Filtered empty
- Detail open
- Exporting

---

## 19. Testing Requirements

### Frontend Unit Tests

Cover:

- Currency formatting
- Status badge mapping
- Policy evaluation display
- Route generation
- Order total calculation
- Payment failure safety messaging

### Frontend Integration Tests

Cover:

- Onboarding to overview
- Overview to opportunity detail
- Approval modal to experiment detail
- Experiment scale to AI Commerce
- AI Buyer search to checkout
- Checkout success route
- Checkout failure route
- Failure to audit trail

### Backend Unit Tests

Cover:

- Policy Guard rules
- Order intent total calculation
- Razorpay amount subunit conversion
- Payment signature verification wrapper
- Webhook signature validation wrapper
- Idempotent webhook persistence
- Audit event creation

### API Tests

Cover:

- All P0 endpoints
- Error response format
- Invalid policy action blocked
- Invalid payment verification rejected

### End-To-End Demo Test

Automate this path:

```text
/onboarding
Initialize RAYGO
/overview
Review Opportunity
/opportunities/opp_keyboard_stand
Approve & Create Experiment
/experiments/exp_keyboard_stand
Scale Experiment
/ai-commerce
/ai-buyer
search buyer prompt
Add to Basket
/checkout/intent_ai_setup_001
Confirm & Pay
simulate failure
/payment/failure
View Audit Trail
/audit
```

### Visual QA

Check desktop and mobile:

- 1440px
- 1024px
- 768px
- 375px

Verify:

- no clipped text
- no button overflow
- no unreadable glass surfaces
- tables usable
- payment states visible
- audit drawer usable
- sidebar/nav consistent

---

## 20. Implementation Phases

### Phase 1: Frontend Conversion

Goal: real app matching Stitch.

Tasks:

- Create React app.
- Add Tailwind tokens from Stitch.
- Add glassmorphism layer.
- Build app shell.
- Convert Stitch screens into routes/components.
- Add typed mock data.
- Wire all primary navigation.
- Add loading, empty, error states.

Acceptance:

- All P0 routes render.
- Primary demo flow works with mock data.
- UI visibly matches Stitch reference.
- Glass effects improve depth without harming readability.

### Phase 2: Mock API Abstraction

Goal: frontend can switch from mock data to backend.

Tasks:

- Add API client.
- Move mock data behind service functions.
- Add Zod schemas.
- Add optimistic UI only where safe.
- Add error boundaries and toasts.

Acceptance:

- Frontend has no hardcoded screen-specific business logic outside fixtures/services.
- API contracts are stable enough for backend integration.

### Phase 3: Backend MVP

Goal: provide real API responses and persisted state.

Tasks:

- Build FastAPI app.
- Add Pydantic schemas.
- Add MongoDB persistence or in-memory fallback for demo.
- Implement opportunities, experiments, policies, agents, audit endpoints.
- Seed demo dataset.

Acceptance:

- Frontend uses backend endpoints for P0 flows.
- State changes create audit entries.

### Phase 4: Razorpay Test Mode

Goal: real test-mode payment order and verification flow.

Tasks:

- Create Razorpay order server-side.
- Open Checkout from frontend.
- Verify payment signature server-side.
- Implement failure endpoint.
- Implement webhook endpoint.
- Add idempotent event processing.

Acceptance:

- Test success can reach Payment Success.
- Test failure can reach Payment Failure.
- No automatic retry occurs.
- Audit trail records payment success/failure.

### Phase 5: Polish And Demo Hardening

Goal: make it judge-ready.

Tasks:

- Add E2E tests.
- Add responsive fixes.
- Add README with setup and demo script.
- Add `.env.example`.
- Add seed/reset script.
- Push to GitHub.

Acceptance:

- A judge can run the app locally.
- Demo flow takes under 5 minutes.
- Failure flow is deliberate and polished.

---

## 21. Acceptance Criteria

The MVP is complete when:

- The app preserves the Stitch UI information architecture and visual language.
- Glassmorphism is coherent and restrained.
- All P0 screens are implemented as real routes.
- The primary demo flow is clickable end to end.
- The same merchant, products, INR values, and metrics appear consistently.
- Opportunity reasoning uses observed/detected/hypothesized/predicted wording.
- Approval is explicit before experiments and payments.
- Policy Guard evaluates actions before execution.
- Payment success and failure flows exist.
- Payment failure blocks automatic retry.
- Audit trail records consequential actions.
- Backend APIs support frontend flows.
- Razorpay Test Mode integration keeps secrets server-side.
- Payment verification is server-side.
- Webhook handling validates signatures and is idempotent.
- The app is usable at desktop and mobile breakpoints.
- Tests cover the P0 flow and critical policy/payment logic.

---

## 22. Demo Script

Use this exact judge flow:

1. Open RAYGO.
2. Initialize NovaTech Store.
3. Show overview: revenue, RAYGO influenced revenue, opportunities, AI Commerce readiness.
4. Click the top opportunity.
5. Explain evidence and projected uplift.
6. Show Policy Guard and approval gate.
7. Approve and create experiment.
8. Show experiment result and `Scale Variant`.
9. Open AI Commerce readiness.
10. Preview the AI-readable product profile.
11. Open AI Buyer.
12. Search for laptop setup under ₹70,000.
13. Add recommended bundle to basket.
14. Review purchase.
15. Confirm payment in Razorpay Test Mode.
16. Show payment success.
17. Repeat or simulate failure.
18. Show payment failure and automatic retry blocked.
19. Open audit trail and show the full event history.

The judge should understand in under 60 seconds:

- RAYGO finds revenue.
- RAYGO explains evidence.
- RAYGO gates actions.
- RAYGO measures impact.
- RAYGO enables AI-buyer checkout.
- RAYGO handles failure safely.
- RAYGO audits everything.

---

## 23. Non-Negotiables

- Do not rebuild the product into a generic dashboard.
- Do not remove the Stitch navigation structure.
- Do not change merchant name or demo values.
- Do not use fake chain-of-thought.
- Do not make AI actions look uncontrolled.
- Do not hide payment failure.
- Do not auto-retry failed payments.
- Do not put Razorpay secrets in frontend code.
- Do not use real money.
- Do not let glass effects reduce contrast.
- Do not spend time on P2 before P0 is complete.

---

## 24. External Implementation References

Use current official Razorpay documentation when implementing payments:

- Razorpay Standard Checkout integration steps
- Razorpay Orders API
- Razorpay payment verification guidance
- Razorpay webhook setup, signature validation, and test mode behavior

Implementation must be checked against the current docs at build time.

---

## 25. Final Product Statement

RAYGO is not a chatbot and not a passive analytics dashboard.

RAYGO is an autonomous, policy-bounded revenue operating layer for AI-native commerce.

The MVP must make this loop visible:

```text
Observe -> Discover -> Reason -> Plan -> Guard -> Approve -> Execute -> Measure -> Learn
```

Build the frontend first, preserve the Stitch design, add restrained fintech glassmorphism, then connect the backend, agents, policies, payments, and audit trail behind the same user flows.
