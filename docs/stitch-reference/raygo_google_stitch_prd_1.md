# RAYGO — Google Stitch UI/UX PRD
## Autonomous Revenue Intelligence for AI-Native Commerce
### Razorpay AI Builder Internship 2026 — Track 1: AI Growth & Agentic Commerce

---

## 0. DOCUMENT PURPOSE

This PRD is the frontend/UI specification for generating the RAYGO prototype in Google Stitch.

IMPORTANT:
- This document is for the UI/UX and frontend prototype phase only.
- Do NOT implement real backend logic, AI calls, databases, authentication, or real payments in Stitch.
- All data may be realistic mock/demo data.
- The extracted frontend will later be connected to a Claude-built backend and AI-agent system.
- The UI must be designed so that API data can replace mock data without redesigning the interface.

RAYGO must feel like a serious fintech/AI operations product, not a generic AI chatbot or a student dashboard.

---

# 1. PRODUCT OVERVIEW

## Product Name

RAYGO

## Product Subtitle

Autonomous Revenue Intelligence for AI-Native Commerce

## One-Line Product Promise

RAYGO discovers merchant revenue opportunities, proposes measurable growth experiments, makes merchant catalogs ready for AI buyers, and executes approved commerce actions through a safe, auditable workflow.

## Core Product Loop

OBSERVE → DISCOVER → REASON → PLAN → GUARD → APPROVE → EXECUTE → MEASURE → LEARN

## Primary Users

### Merchant / Business Operator
Needs to:
- understand where revenue is being lost
- discover actionable growth opportunities
- approve or reject AI recommendations
- monitor experiments
- understand AI decisions
- manage financial/action policies
- see payment and commerce outcomes

### AI Buyer
Needs to:
- describe a shopping goal naturally
- receive relevant product recommendations
- compare products
- build a basket
- review purchase intent
- proceed to checkout

The merchant experience is the primary application. The AI Buyer experience is a secondary but highly polished demo flow.

---

# 2. BUSINESS PROBLEM

Merchants have extensive commerce data but most dashboards are descriptive rather than autonomous.

Existing dashboards tell merchants:
- what happened
- how much revenue was generated
- which products sold

They rarely answer:
- why revenue is being lost
- which opportunity is worth pursuing
- what action should be taken
- what financial risk exists
- whether an intervention actually generated incremental revenue

At the same time, commerce is moving toward AI-native buying, where AI agents can discover products, compare options, construct carts and initiate purchases.

RAYGO connects these two worlds.

Merchant intelligence becomes:
Revenue opportunity → AI reasoning → bounded action → payment/commerce execution → measured result.

---

# 3. PRODUCT GOALS

## Primary Goals

1. Make revenue opportunities immediately visible.
2. Make AI decisions explainable.
3. Make AI actions controlled and merchant-approved.
4. Show measurable experiment outcomes.
5. Make merchant products understandable to AI buyers.
6. Demonstrate a complete AI-buyer-to-checkout journey.
7. Make every important action auditable.
8. Make failures visible and safely handled.
9. Present RAYGO as a production-grade fintech/AI product.

## Non-Goals for the Stitch Prototype

Do not build:
- real authentication
- real database
- real Razorpay payment processing
- real Gemini/Claude calls
- real webhooks
- real campaign execution
- real email/SMS sending
- real financial transfers

These will be connected later.

---

# 4. DESIGN DIRECTION

The interface must look like a premium AI-native fintech operations platform.

Avoid:
- generic SaaS dashboard templates
- excessive glassmorphism
- neon purple AI gradients
- cartoon AI imagery
- oversized decorative illustrations
- excessive rounded cards
- emoji used as icons
- fake "AI magic" visual effects
- cluttered dashboards
- excessive charts with no business meaning

Use:
- strong information hierarchy
- restrained premium fintech visual language
- crisp typography
- subtle borders
- purposeful elevation
- compact but readable data density
- meaningful whitespace
- clear action states
- professional tables
- elegant charts
- operational status indicators
- clear monetary values
- transparent AI reasoning

The product should visually communicate:

TRUST + INTELLIGENCE + CONTROL + ACTION

---

# 5. DESIGN SYSTEM

Use the UI/UX Pro Max design philosophy:
- establish a coherent design system before individual screens
- choose a style appropriate for fintech + AI operations
- use consistent typography hierarchy
- maintain accessible contrast
- use semantic status colors
- avoid anti-patterns
- provide responsive layouts
- use meaningful interaction states
- use real icons rather than emoji

Reference:
https://github.com/nextlevelbuilder/ui-ux-pro-max-skill

The skill emphasizes design-system generation, industry-specific UI reasoning, typography pairing, color systems, anti-pattern filtering and responsive/accessibility checks. Apply those principles to every RAYGO screen.

---

# 6. COLOR SYSTEM

Use a restrained light-first fintech palette.

Primary:
- Deep navy / near-black for major text and navigation
- White / off-white application background
- Cool neutral surfaces

Accent:
- Razorpay-inspired red should be used sparingly for primary brand emphasis and critical commerce actions.
- Do NOT make the entire UI red.

Semantic colors:
- Green = positive growth / successful execution
- Amber = warning / approval required
- Red = blocked / failed / critical
- Blue = information / AI reasoning / neutral action

Important:
Do not use color as the only way to communicate status. Pair status colors with labels and icons.

---

# 7. TYPOGRAPHY

Use a modern professional sans-serif.

Preferred:
- Inter
- Geist
- Manrope

Typography should prioritize:
- highly readable dashboard numbers
- strong section headings
- compact metadata
- readable AI reasoning text
- clear button labels

Large revenue numbers should have strong visual hierarchy without becoming oversized.

---

# 8. ICONOGRAPHY

Use Lucide/Heroicons-style line icons.

Never use emojis as interface icons.

Suggested icon concepts:
- Revenue: TrendingUp
- Opportunity: Sparkles / Lightbulb
- AI: Bot / Brain
- Experiment: FlaskConical
- Commerce: ShoppingBag
- Buyer: UserRound
- Payment: CreditCard
- Policy: ShieldCheck
- Approval: CheckCircle
- Blocked: ShieldAlert
- Audit: ScrollText
- Settings: Settings
- Analytics: BarChart3
- Products: Package
- Search: Search
- Notifications: Bell

---

# 9. RESPONSIVE REQUIREMENTS

Design and prototype for:
- 1440px desktop
- 1024px tablet
- 768px tablet/mobile transition
- 375px mobile

Desktop is the primary judging/demo experience.

Mobile must remain usable:
- navigation collapses
- tables become cards or horizontal scroll
- dashboard grids stack
- action buttons remain reachable
- no clipped text
- no broken labels

---

# 10. APPLICATION INFORMATION ARCHITECTURE

Main navigation:

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

Secondary:
- Notifications
- Settings
- Merchant profile

Primary CTA:
- Review Opportunities

---

# 11. SCREEN 01 — ONBOARDING / MERCHANT SETUP

## Purpose

Introduce RAYGO and establish the merchant context.

## Layout

Minimal premium onboarding screen.

Left:
- RAYGO logo
- headline:
  "Turn commerce data into autonomous growth."

Right:
- setup card

Fields:
- Merchant name
- Business category
- Monthly revenue range
- Product count
- Current commerce platform
- Enable AI Buyer mode

CTA:
"Initialize RAYGO"

After clicking:
show a short initialization state:
- Ingesting commerce data
- Mapping products
- Detecting revenue patterns
- Preparing AI Commerce profile
- Configuring policy guard

Then transition to Overview.

---

# 12. SCREEN 02 — EXECUTIVE OVERVIEW

## Purpose

This is the primary judging screen.

It should immediately communicate what RAYGO has discovered and what it can do.

## Header

RAYGO
Autonomous Revenue Intelligence

Right:
- date range
- notifications
- merchant profile

## Hero Metrics

Four primary KPI cards:

1. Revenue
₹2,84,620
+18.7%

2. Revenue Influenced by RAYGO
₹42,800
+14.2%

3. Active Opportunities
7

4. AI Commerce Readiness
82 / 100

## Main Section

Large panel:

"RAYGO found 7 revenue opportunities"

Show top 3 opportunities.

Example:

Opportunity 01
Cross-sell opportunity
Keyboard → Laptop Stand

Expected monthly impact:
₹18,400

Confidence:
87%

Status:
Ready for review

CTA:
"Review"

Opportunity 02
Abandoned cart recovery
Expected impact:
₹11,200

Opportunity 03
High-margin bundle
Expected impact:
₹7,600

## Revenue Opportunity Chart

A clean line/area chart:
- actual revenue
- revenue influenced by RAYGO
- projected revenue

Keep the chart simple.

## AI Insight Panel

Title:
"RAYGO's latest reasoning"

Example:
"Customers purchasing Wireless Keyboard have a 2.3× higher probability of viewing Laptop Stand. Current attach rate is 4.1%, leaving an estimated ₹18.4K monthly opportunity."

CTA:
"View reasoning"

---

# 13. SCREEN 03 — OPPORTUNITY CENTER

## Purpose

A dedicated workspace for all detected revenue opportunities.

## Header

Revenue Opportunities

Subtext:
"RAYGO continuously scans your commerce signals for measurable growth opportunities."

Filters:
- All
- Cross-sell
- Upsell
- Bundle
- Recovery
- Pricing
- Campaign

Sort:
- Impact
- Confidence
- Newest

## Opportunity Cards/Table

Columns:
- Opportunity
- Type
- Expected Impact
- Confidence
- Risk
- Status
- Action

Example:

Cross-sell:
Keyboard + Laptop Stand
₹18,400
87%
Low
Ready
Review

## Right-side detail drawer

When an opportunity is selected, open a detail panel.

Sections:

WHY RAYGO FOUND THIS

SIGNALS USED

HYPOTHESIS

EXPECTED IMPACT

RISKS

RECOMMENDED ACTION

POLICY STATUS

APPROVAL REQUIREMENT

Buttons:
- Approve
- Reject
- Modify

---

# 14. SCREEN 04 — OPPORTUNITY DETAIL / AI REASONING

This is a major "judge wow" screen.

Title:
"Cross-sell opportunity"

Subtitle:
"Wireless Keyboard → Laptop Stand"

## Impact Summary

Expected revenue:
₹18,400 / month

Confidence:
87%

Estimated margin impact:
+4.8%

## Evidence

Show compact evidence cards:

Purchase correlation:
2.3×

Current attach rate:
4.1%

Target attach rate:
7.8%

Eligible customers:
1,842

## AI Reasoning Timeline

Display:

1. Observed
"Keyboard purchases increased 14%."

2. Detected
"Laptop Stand views increased among keyboard buyers."

3. Compared
"Comparable products show higher attach rates."

4. Hypothesized
"A bundle may increase attach rate."

5. Predicted
"Potential monthly uplift ₹18.4K."

## Action Preview

"Proposed experiment"

Control:
Keyboard only

Variant:
Keyboard + Laptop Stand

Discount:
10%

Expected uplift:
₹18.4K/month

## Policy Guard

Green:
"Action complies with current merchant policy."

Rules:
✓ Discount below 20%
✓ Margin remains above 25%
✓ Campaign budget available
✓ Merchant approval required

Primary CTA:
"Approve & Create Experiment"

Secondary:
"Edit proposal"

---

# 15. SCREEN 05 — EXPERIMENTS

## Purpose

Show that RAYGO doesn't blindly automate growth. It runs measurable experiments.

Header:
"Growth Experiments"

Top metrics:
- Active experiments
- Revenue uplift
- Conversion uplift
- Experiments completed

## Experiment table

Columns:
Experiment
Status
Control
Variant
Revenue uplift
Confidence
Duration

Example:

Keyboard + Stand Bundle
Running
6.2%
8.9%
+23.4%
94%

## Experiment detail

Show:

Hypothesis

"Bundling a laptop stand with keyboard purchases will increase basket value without materially reducing margin."

Timeline:
- Created
- Approved
- Started
- Measuring
- Completed

Results:
Control:
6.2%

Variant:
8.9%

Conversion uplift:
+43.5%

Revenue uplift:
+23.4%

AOV:
+8.7%

Confidence:
94%

Final recommendation:
"Scale variant"

CTA:
"Scale Experiment"

---

# 16. SCREEN 06 — AI COMMERCE READINESS

## Purpose

Show how RAYGO makes merchants ready for AI buyers.

Header:
"AI Commerce"

Hero score:
82 / 100

Subtitle:
"How ready is your catalog for AI-driven commerce?"

## Score dimensions

Product discoverability
91

Structured product data
82

Pricing clarity
94

Inventory confidence
63

Policy clarity
72

Checkout readiness
76

## AI Buyer blockers

Example:

Warning:
14 products have stale inventory data.

Warning:
37 products lack structured shipping information.

Warning:
8 products have ambiguous product attributes.

## CTA

"Optimize Catalog"

## AI-readable product preview

Show a structured product representation:

Product:
ProBook 14

Category:
Laptop

Price:
₹62,999

Availability:
In stock

Best for:
Coding, college, productivity

Specifications:
16GB RAM
512GB SSD
...

This preview should look machine-readable while remaining human-friendly.

---

# 17. SCREEN 07 — AI BUYER EXPERIENCE

## Purpose

Create the most visually impressive customer-facing demo.

This should feel different from the merchant dashboard.

## Header

RAYGO AI Commerce

Text:
"Tell me what you're looking for."

Large conversational search/input:

"I need a laptop setup for AI and college under ₹70,000."

## AI Response

"I found 3 options that fit your budget and usage."

Product recommendation cards.

Each card:
- product image placeholder
- product name
- price
- compatibility
- reason selected
- availability
- AI confidence

Example:

ProBook 14
₹62,999

"Best balance for AI development and portability."

## Compare

Allow selecting up to 3 products.

## Basket

Show:
- product
- quantity
- price
- recommendation reason
- total

CTA:
"Proceed to Checkout"

---

# 18. SCREEN 08 — AI CHECKOUT / PURCHASE INTENT

## Purpose

Demonstrate controlled agentic commerce.

Header:
"Review purchase"

Show:
- buyer intent
- selected products
- quantity
- subtotal
- discount
- total
- merchant
- delivery information

## AI action explanation

"Why this purchase was prepared"

- Matches requested budget
- Meets 16GB RAM requirement
- In stock
- Merchant supports AI checkout
- Price verified

## Authorization gate

Prominent section:

"Purchase authorization required"

"RAYGO will not execute the payment until you confirm the order."

CTA:
"Confirm & Pay"

This reinforces human control.

---

# 19. SCREEN 09 — PAYMENT SUCCESS

## Purpose

Make successful transaction state polished and credible.

Show:

Payment successful

₹68,499

Razorpay Test Mode

Order:
#RGO-10482

Timeline:
Intent received
Product selected
Order created
Payment authorized
Order confirmed

## AI commerce impact

"Purchase completed through an AI-native commerce flow."

Metrics:
- Decision time
- Recommendation confidence
- Checkout completion

CTA:
"Return to Merchant Dashboard"

---

# 20. SCREEN 10 — FAILURE / RECOVERY

This screen is essential.

## Scenario

Payment fails.

Show:

Payment unsuccessful

₹68,499

Reason:
"Payment attempt was unsuccessful."

Do NOT show vague:
"Something went wrong."

## AI response

"RAYGO has stopped automatic retries to avoid duplicate charges."

Show:

✓ Order remains unpaid
✓ No duplicate payment initiated
✓ Merchant inventory unchanged
✓ Transaction recorded in audit trail

## Recovery options

"Try another permitted payment method"

or

"Return to basket"

## Audit entry

Payment attempt:
FAILED

Automatic retry:
BLOCKED

Reason:
Duplicate-charge protection

This screen should make the safety architecture obvious.

---

# 21. SCREEN 11 — AGENT ACTIVITY

## Purpose

Show the multi-agent system operating.

Header:
"Agent Activity"

Live-style status feed.

Agents:

Revenue Intelligence
ACTIVE

AI Commerce
ACTIVE

Growth Strategist
ACTIVE

Experiment Agent
RUNNING

Policy Guard
ACTIVE

Payment Agent
READY

## Activity feed

Example:

11:32:04
Revenue Intelligence
Detected cross-sell opportunity

11:32:05
Growth Strategist
Generated experiment hypothesis

11:32:06
Policy Guard
Action approved by policy

11:32:07
Approval Gateway
Merchant approval received

11:32:08
Experiment Agent
Experiment created

11:32:12
Payment Agent
Payment attempt failed

11:32:12
Policy Guard
Automatic retry blocked

Use subtle status animation, not flashy effects.

---

# 22. SCREEN 12 — POLICIES / REVENUE ACTION FIREWALL

## Purpose

Show that the AI cannot freely manipulate money.

Header:
"Revenue Action Firewall"

Subtitle:
"Define what RAYGO can and cannot do."

Policy cards:

Maximum discount:
20%

Maximum campaign budget:
₹10,000

Minimum margin:
25%

Automatic execution:
OFF

Merchant approval:
REQUIRED

Payment retry:
BLOCKED

## Action permission matrix

Action | AI can propose | AI can execute | Approval

Create bundle | ✓ | ✓ | Required

Discount >20% | ✓ | ✕ | Blocked

Create campaign | ✓ | ✓ | Required

Payment retry | ✓ | ✕ | Blocked

Refund | ✓ | ✕ | Required

Use badges:
Allowed
Approval Required
Blocked

---

# 23. SCREEN 13 — AUDIT TRAIL

## Purpose

Provide full transparency.

Header:
"Audit Trail"

Search:
"Search agent actions..."

Filters:
- Agent
- Action
- Status
- Date

Timeline rows:

Timestamp
Agent
Action
Reason
Policy
Approval
Outcome

Example:

11:32:08
Payment Agent
Create Order
AI buyer confirmed purchase
Passed
Confirmed
Success

11:32:12
Payment Agent
Retry Payment
Payment failed
Blocked
N/A
Prevented

## Detail drawer

When a row is selected:

Decision
Reasoning summary
Tools called
Policy checks
Approval
Execution result
Error/recovery
Related order

Do not expose hidden chain-of-thought. Show concise decision explanations, evidence and action metadata.

---

# 24. SCREEN 14 — PRODUCTS / AI-READABLE CATALOG

## Purpose

Manage product data and AI readiness.

Table:
- Product
- Price
- Inventory
- AI readiness
- Discoverability
- Issues

Product detail:
- normal product information
- structured AI representation
- missing attributes
- optimization suggestions

CTA:
"Optimize with RAYGO"

---

# 25. SCREEN 15 — ORDERS & PAYMENTS

## Purpose

Show commerce transactions.

Tabs:
Orders
Payments

Metrics:
- GMV
- Successful payments
- Failed payments
- Refunds
- Conversion

Table:
Order
Customer
Amount
Payment
AI buyer
Status

Use clear statuses.

---

# 26. GLOBAL AI ASSISTANT

Do NOT make a floating chatbot the central product.

Instead, provide a compact "Ask RAYGO" command interface in the top navigation.

Example commands:

"Why did revenue drop yesterday?"

"Show my highest-value opportunities."

"Which experiment should I scale?"

"Why is my AI Commerce score 82?"

"Show blocked actions."

The assistant should return concise operational answers and links to the relevant workspace.

---

# 27. INTERACTION DESIGN

Every major action needs states:

Default
Hover
Focus
Loading
Success
Warning
Error
Disabled

Approval flow:

Review
→ Preview
→ Policy Check
→ Merchant Approval
→ Execution
→ Result

Do not jump directly from:
"AI recommends"
to
"Action executed."

---

# 28. AI REASONING PRESENTATION

Never display fake internal chain-of-thought.

Instead show:

### Decision Summary

What happened?

### Evidence

What data supported it?

### Recommendation

What does RAYGO propose?

### Expected Impact

What could happen?

### Risk

What could go wrong?

### Policy

Is the action permitted?

### Approval

Who authorized it?

This is more trustworthy and suitable for a fintech product.

---

# 29. MOCK DATA REQUIREMENTS

Use a realistic fictional merchant.

Merchant:
"NovaTech Store"

Category:
Consumer Electronics

Currency:
INR

Example products:
- ProBook 14 — ₹62,999
- Wireless Keyboard — ₹2,499
- Laptop Stand — ₹1,799
- AI Mouse Pro — ₹1,299
- USB-C Dock — ₹4,999
- NoiseCancel Headphones — ₹6,499
- 27" 4K Monitor — ₹29,999

Use realistic transaction numbers.

Do not use lorem ipsum.

Do not use fake generic dashboard labels like:
"Lorem Revenue"
"Sample Product"

---

# 30. DEMO DATA SCENARIO

The entire prototype should support one coherent story.

Merchant:
NovaTech Store

Monthly revenue:
₹2,84,620

Revenue growth:
+18.7%

RAYGO revenue influenced:
₹42,800

AI Commerce score:
82

Top opportunity:
Keyboard + Laptop Stand

Expected monthly impact:
₹18,400

Current attach rate:
4.1%

Predicted attach rate:
7.8%

Experiment:
Control 6.2%
Variant 8.9%

Revenue uplift:
+23.4%

Confidence:
94%

AI buyer order:
₹68,499

Payment:
First attempt failed in demo recovery scenario.

Automatic retry:
Blocked.

This same data must appear consistently across screens.

---

# 31. PRIMARY DEMO FLOW

The prototype must support this exact presentation flow:

1. Open Overview.
2. Show revenue and AI Commerce score.
3. Click "Review Opportunity."
4. Open opportunity reasoning.
5. Show evidence.
6. Show proposed experiment.
7. Show Policy Guard.
8. Click "Approve & Create Experiment."
9. Open Experiment.
10. Show uplift.
11. Open AI Commerce.
12. Open AI Buyer.
13. Enter natural-language shopping request.
14. Show recommendations.
15. Build basket.
16. Review purchase intent.
17. Confirm payment.
18. Show payment failure.
19. Show safe recovery.
20. Open Audit Trail.
21. Show complete action history.

The Stitch prototype should make these transitions visually coherent.

---

# 32. VISUAL STORYTELLING

The dashboard should answer these questions in order:

1. What is happening to my business?
2. What opportunity did RAYGO find?
3. Why does RAYGO believe it?
4. What does RAYGO want to do?
5. Is it safe?
6. What happens if I approve?
7. Did it work?
8. Can an AI buyer transact with my business?
9. What happened during the transaction?
10. Can I audit the entire process?

---

# 33. UX PRINCIPLES

## Principle 1 — Action over analytics

Every major insight should lead to a possible action.

## Principle 2 — Explain before execute

AI must explain its recommendation before requesting approval.

## Principle 3 — Money requires control

Financial actions must show policy and authorization.

## Principle 4 — Evidence over hype

Show metrics and evidence instead of generic "AI-powered" labels.

## Principle 5 — Failure is a product state

Design failure and recovery as first-class experiences.

## Principle 6 — AI should feel operational

RAYGO should feel like a revenue operator, not a chatbot.

---

# 34. PERFORMANCE / ACCESSIBILITY

Follow these requirements:
- WCAG-conscious contrast
- visible keyboard focus
- accessible button labels
- no color-only status
- responsive at 375/768/1024/1440
- reduced-motion support
- avoid unnecessary animation
- no layout shift
- charts must have text summaries
- tables must remain readable
- tooltips must not contain essential information only

---

# 35. ANIMATION

Use subtle, purposeful motion only.

Good:
- KPI count transition
- opportunity drawer transition
- status transition
- experiment progress
- payment state transition
- chart entry

Avoid:
- constant pulsing
- glowing cards
- particle backgrounds
- excessive parallax
- distracting AI animations

The product should feel fast and serious.

---

# 36. COMPONENT LIBRARY

Create reusable components:

- AppShell
- Sidebar
- Topbar
- MetricCard
- OpportunityCard
- OpportunityTable
- ReasoningPanel
- EvidenceCard
- PolicyGuard
- ApprovalModal
- ExperimentCard
- ExperimentChart
- ReadinessScore
- ProductCard
- ProductTable
- BuyerChat
- Basket
- CheckoutSummary
- PaymentStatus
- AgentStatus
- ActivityTimeline
- AuditTable
- AuditDetailDrawer
- StatusBadge
- EmptyState
- LoadingState
- ErrorState
- Toast
- Modal
- Drawer
- Tabs
- FilterBar

Components must share a consistent design language.

---

# 37. NAVIGATION BEHAVIOR

Sidebar navigation should remain persistent on desktop.

Active section:
- strong visual indicator
- clear label
- icon

On mobile:
- collapsible navigation

Topbar:
- merchant selector
- date range
- notification icon
- Ask RAYGO
- profile

---

# 38. EMPTY / LOADING / ERROR STATES

Design these intentionally.

Loading:
"RAYGO is analyzing your latest commerce signals..."

Empty:
"No active opportunities yet. RAYGO is continuing to monitor your commerce data."

Error:
"Revenue analysis could not be refreshed. Your previous insights remain available."

Payment failure:
"Payment unsuccessful. No automatic retry was attempted."

---

# 39. SECURITY / TRUST UX

Never imply that the AI can freely spend money.

Use labels such as:

"Approval required"

"Policy blocked"

"Test Mode"

"Merchant authorized"

"Action preview"

"Execution pending"

"Execution complete"

Trust indicators should be visible but not overwhelming.

---

# 40. RAZORPAY POSITIONING

RAYGO is designed for Razorpay's:
AI Growth & Agentic Commerce track.

The product should demonstrate:
- merchant revenue growth
- AI-readable commerce
- AI buyer journey
- Razorpay-powered transaction flow
- bounded financial actions
- explainability
- auditability
- graceful failure

Do not copy Razorpay branding or claim RAYGO is an official Razorpay product.

Use:
"Built for Razorpay AI Builder Internship — Track 1"

not:
"Official Razorpay product."

---

# 41. JUDGE-FIRST DESIGN REQUIREMENTS

The UI should make these five things obvious within the first 60 seconds:

1. RAYGO finds revenue opportunities.
2. RAYGO explains why.
3. RAYGO proposes measurable actions.
4. RAYGO controls financial actions with policy gates.
5. RAYGO enables an AI buyer to transact.

The judge should not need to read documentation to understand these.

---

# 42. MOST IMPORTANT "WOW" MOMENTS

## WOW 1
Dashboard says:

"RAYGO found ₹42,800 in potential revenue."

## WOW 2
Opportunity detail explains the evidence.

## WOW 3
Policy Guard visibly blocks unsafe actions.

## WOW 4
Experiment shows measurable uplift.

## WOW 5
AI buyer completes a natural-language commerce flow.

## WOW 6
Payment failure is handled safely.

## WOW 7
Audit trail reconstructs the entire agent action.

---

# 43. STITCH GENERATION INSTRUCTION

Generate the RAYGO frontend as a high-fidelity, responsive, production-style web application prototype.

Prioritize:
- desktop executive dashboard quality
- premium fintech visual language
- coherent design system
- strong typography
- realistic INR commerce data
- clear AI reasoning
- policy and approval UX
- agent activity
- experiment analytics
- AI buyer commerce flow
- payment success and failure states
- auditability

Do not generate a generic SaaS dashboard.

Do not make the interface look like an AI chatbot product.

Do not overuse cards.

Do not use excessive gradients.

Do not use emoji icons.

Do not use placeholder lorem ipsum.

Use realistic content and consistent mock data.

Build the screens so the prototype can later be connected to a FastAPI/Claude agent backend without changing the UI architecture.

---

# 44. STITCH OUTPUT EXPECTATION

Generate all core screens and connect them into a coherent clickable prototype.

Minimum required screens:

1. Overview
2. Opportunities
3. Opportunity Detail
4. Experiments
5. AI Commerce
6. AI Buyer
7. Checkout
8. Payment Success
9. Payment Failure
10. Agent Activity
11. Policies
12. Audit Trail

Optional:
13. Products
14. Orders
15. Settings

The prototype must prioritize quality over quantity.

If time or generation constraints require reducing screens, preserve screens 1–12.

---

# 45. FINAL QUALITY BAR

Before considering the UI complete, verify:

[ ] RAYGO immediately communicates its purpose.

[ ] The dashboard feels like a serious fintech product.

[ ] Revenue opportunity is the visual center of the product.

[ ] AI reasoning is understandable.

[ ] Policy controls are prominent.

[ ] Approval flow is explicit.

[ ] Experiment results are measurable.

[ ] AI Commerce Readiness is visually compelling.

[ ] AI buyer flow feels like a real commerce experience.

[ ] Checkout clearly shows authorization.

[ ] Payment success and failure are both designed.

[ ] Failure handling communicates safety.

[ ] Agent activity feels real but not theatrical.

[ ] Audit trail is credible.

[ ] INR values are consistent.

[ ] No fake lorem ipsum exists.

[ ] No emoji are used as UI icons.

[ ] Responsive behavior is considered.

[ ] Accessibility states are present.

[ ] Buttons have clear labels.

[ ] Loading/error/empty states exist.

[ ] The entire demo can be presented in approximately five minutes.

---

# 46. FINAL PRODUCT STATEMENT

RAYGO is not a chatbot.

RAYGO is not another analytics dashboard.

RAYGO is an autonomous revenue operating layer for AI-native commerce.

Its core loop is:

DISCOVER
→ REASON
→ EXPERIMENT
→ APPROVE
→ EXECUTE
→ MEASURE
→ LEARN

The frontend must make that loop visible, understandable, trustworthy, and visually memorable.
