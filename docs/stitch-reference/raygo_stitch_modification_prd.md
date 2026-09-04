# RAYGO — STITCH MODIFICATION PRD
## Final UI Completion & Consistency Pass
### Razorpay AI Builder Internship 2026 — Track 1: AI Growth & Agentic Commerce

---

# 0. CRITICAL INSTRUCTION

This is a MODIFICATION PRD for the EXISTING RAYGO Google Stitch project.

DO NOT restart the project.
DO NOT redesign the existing screens from scratch.
DO NOT change the established design system unless explicitly instructed below.

The existing Stitch screens are already visually approved as the foundation:

1. Onboarding — RAYGO
2. Executive Overview — RAYGO
3. Opportunity Center — RAYGO
4. Opportunity Detail — RAYGO

The goal now is to:

A. Preserve those screens.
B. Fix consistency issues.
C. Add the missing agentic-commerce screens.
D. Connect all screens into one coherent clickable product flow.
E. Make the product look like a serious fintech/AI platform rather than a generic dashboard.
F. Finish quickly because the project has only 4 days total.

PRIORITY:
Working coherent prototype > excessive visual decoration.

---

# 1. PRODUCT IDENTITY

Product:
RAYGO

Subtitle:
Autonomous Revenue Intelligence

Track:
AI Growth & Agentic Commerce

Core loop:

DISCOVER
→ REASON
→ EXPERIMENT
→ APPROVE
→ EXECUTE
→ MEASURE
→ LEARN

Core message:

"RAYGO doesn't just tell merchants what happened. It discovers revenue opportunities, proposes measurable actions, applies financial guardrails, gets merchant authorization, executes commerce actions, and measures the result."

---

# 2. DO NOT CHANGE THE EXISTING VISUAL LANGUAGE

Preserve:

- current light fintech interface
- white/off-white content surfaces
- dark typography
- restrained Razorpay-inspired red accent
- thin neutral borders
- compact professional cards
- existing sidebar
- existing top navigation
- current typography scale
- current icon style
- current button style
- current status badges
- current spacing system

DO NOT introduce:

- neon gradients
- purple AI gradients
- excessive glassmorphism
- giant rounded cards
- excessive shadows
- 3D illustrations
- cartoon AI imagery
- emoji as UI icons
- animated particle backgrounds
- unnecessary decorative graphics

The existing interface should remain recognizable as one product.

---

# 3. GLOBAL CONSISTENCY FIXES

Apply these changes across every existing and new screen.

## 3.1 Navigation

Use one consistent sidebar:

RAYGO
Revenue Intelligence

Overview
Opportunities
Experiments
AI Commerce
Orders
Products
Payments

Agent Activity
Policies
Audit Trail

Bottom:
Ask RAYGO

Active navigation item must have a clear selected state.

Do not change navigation order between screens.

---

## 3.2 Topbar

Use:

NovaTech Store

Search / command field

Notifications
Help
Profile

On detail screens use breadcrumbs where appropriate:

Opportunities > Opportunity Detail

Do not create a completely different topbar on individual screens.

---

## 3.3 Merchant Data

Use the SAME merchant everywhere:

NovaTech Store

Category:
Consumer Electronics

Do not switch merchant names between screens.

---

## 3.4 Currency

Use INR consistently.

Correct:
₹2,84,620

Correct:
₹18,400

Avoid:
$18,400

---

## 3.5 Icons

Use professional line icons.

No emoji.

---

## 3.6 Status Badges

Use consistent semantic badges:

Green:
Success / Running / Approved

Amber:
Review Required / Approval Required / Warning

Red:
Blocked / Failed / Critical

Neutral:
Draft / Ready / Inactive

Never communicate status only through color.

---

# 4. GLOBAL DATA CONSISTENCY

Use one coherent demo dataset throughout the application.

Merchant:
NovaTech Store

Products:

ProBook 14
₹62,999

Wireless Keyboard
₹2,499

Laptop Stand
₹1,799

AI Mouse Pro
₹1,299

USB-C Dock
₹4,999

NoiseCancel Headphones
₹6,499

27" 4K Monitor
₹29,999

Overview:

Total Revenue:
₹2,84,620

Growth:
+18.7%

RAYGO Influenced:
₹42,800

Active Opportunities:
7

AI Commerce Readiness:
82 / 100

Primary Opportunity:

Wireless Keyboard → Laptop Stand

Expected Monthly Impact:
₹18,400

Confidence:
87%

Current Attach Rate:
4.1%

Projected Attach Rate:
7.8%

Experiment:

Control:
6.2%

Variant:
8.9%

Revenue Uplift:
+23.4%

Confidence:
94%

AI Buyer Demo:

Order Total:
₹68,499

Payment:
Demo/Test Mode

Failure scenario:
Payment unsuccessful

Automatic retry:
Blocked

IMPORTANT:
All screens must reference these same values where relevant.

---

# 5. EXISTING SCREEN 01 — ONBOARDING

## KEEP THE CURRENT SCREEN.

Do not redesign.

Make only these modifications:

### A. Headline

Keep:

"Turn commerce data into autonomous growth."

### B. Add small product descriptor

"AI revenue intelligence for modern commerce."

### C. Initialize button

Use:

"Initialize RAYGO"

### D. Initialization sequence

When clicked, show a short sequential progress state:

1. Connecting merchant data
2. Mapping product catalog
3. Detecting revenue patterns
4. Preparing AI Commerce profile
5. Applying merchant policies

Then route to Overview.

Do not make the animation excessive.

---

# 6. EXISTING SCREEN 02 — EXECUTIVE OVERVIEW

## KEEP THE CURRENT SCREEN.

It is already the strongest screen.

Only improve the following.

## 6.1 KPI cards

Ensure these exact metrics are visible:

TOTAL REVENUE
₹2,84,620
+18.7% vs last period

RAYGO INFLUENCED
₹42,800
+14.2% AI lift

ACTIVE OPPORTUNITIES
7
Action required

AI COMMERCE READINESS
82 / 100

---

## 6.2 Opportunity section

Heading:

"RAYGO found 7 revenue opportunities"

Subheading:

"Top opportunities ranked by expected business impact."

Each opportunity must show:

- type
- opportunity
- estimated impact
- confidence
- status
- action

Primary opportunity:

"Cross-sell: Wireless Keyboard + Laptop Stand"

Impact:
₹18,400 / month

Confidence:
87%

Status:
Ready for Review

CTA:
Review Opportunity

---

## 6.3 Latest Reasoning

Keep the existing reasoning panel.

Improve wording to be concise and evidence-based.

Use:

"RAYGO analyzed 1,842 relevant purchase journeys and found a strong correlation between Wireless Keyboard purchases and Laptop Stand views."

Then:

"Current attach rate is 4.1%. Similar interventions suggest a potential increase to 7.8%."

Do not display fake hidden chain-of-thought.

---

# 7. EXISTING SCREEN 03 — OPPORTUNITY CENTER

## KEEP THE CURRENT SCREEN.

Modify:

### A. Add summary strip

Projected opportunity impact:
₹40,000

Active:
7

Ready for review:
4

Running:
2

---

### B. Opportunity table

Use:

Opportunity
Type
Projected Impact
AI Confidence
Risk
Status
Action

Example rows:

Keyboard + Stand
Cross-sell
₹18,400
87%
Low
Ready for Review
Review

ProBook Bundle
Bundle
₹12,200
91%
Low
Running
View

Recovery Campaign
Recovery
₹9,400
78%
Medium
Ready
Review

---

### C. Detail interaction

Clicking an opportunity must open the Opportunity Detail screen.

Do not create dead buttons.

---

# 8. EXISTING SCREEN 04 — OPPORTUNITY DETAIL

## KEEP THE CURRENT SCREEN.

This screen is approved as the core AI reasoning experience.

Add the following.

## 8.1 Action preview

Add a section:

PROPOSED ACTION

"Create a 10% Keyboard + Laptop Stand bundle experiment."

Show:

Discount:
10%

Expected uplift:
₹18,400 / month

Estimated margin:
>25%

Budget:
Within policy

---

## 8.2 Approval state

Button:

"Approve & Create Experiment"

When clicked:

1. Show Policy Check
2. Show Approval Confirmed
3. Show Experiment Created
4. Navigate to Experiment Detail

Never directly jump from recommendation to execution.

---

# 9. NEW SCREEN 05 — EXPERIMENTS

Create a complete Experiments workspace.

## Header

Growth Experiments

Subtitle:

"RAYGO tests growth hypotheses before recommending scale."

Top metrics:

Active Experiments
3

Completed
12

Revenue Uplift
+₹31,800

Average Confidence
91%

---

## Experiment table

Columns:

Experiment
Type
Status
Control
Variant
Revenue Uplift
Confidence

Example:

Keyboard + Stand Bundle
Cross-sell
Running
6.2%
8.9%
+23.4%
94%

ProBook Bundle
Bundle
Completed
5.8%
7.1%
+16.8%
91%

Cart Recovery
Recovery
Running
3.4%
5.2%
+18.2%
88%

---

# 10. NEW SCREEN 06 — EXPERIMENT DETAIL

This is a HIGH PRIORITY screen.

## Header

Keyboard + Laptop Stand

Growth Experiment

Status:
Running

---

## Hypothesis

"Bundling a Laptop Stand with Wireless Keyboard purchases will increase basket conversion without reducing merchant margin below policy."

---

## Experiment Design

CONTROL

Keyboard only
6.2% conversion

VARIANT

Keyboard + Stand
8.9% conversion

---

## Results

Conversion uplift:
+43.5%

Revenue uplift:
+23.4%

AOV:
+8.7%

Confidence:
94%

---

## Recommendation

RAYGO recommends:

"SCALE VARIANT"

Reason:

"Variant performance exceeds control while remaining within the merchant's margin policy."

CTA:

"Scale Experiment"

Secondary:

"Keep Running"

---

# 11. NEW SCREEN 07 — AI COMMERCE

This is a HIGH PRIORITY SCREEN.

## Header

AI Commerce

Subtitle:

"Make your store discoverable, understandable and transactable by AI buyers."

---

## Hero

AI COMMERCE READINESS

82 / 100

Label:

"Good readiness — 3 areas need attention."

---

## Score breakdown

Product Discoverability
91

Structured Product Data
82

Pricing Clarity
94

Inventory Confidence
63

Policy Clarity
72

Checkout Readiness
76

Use progress indicators.

---

## AI Buyer Blockers

Show:

14 products have stale inventory data.

37 products lack structured shipping information.

8 products have ambiguous product attributes.

Each issue should have:

Severity
Affected products
Suggested action

CTA:

"Optimize Catalog"

---

# 12. NEW SCREEN 08 — AI-READABLE PRODUCT PREVIEW

Inside AI Commerce, provide a product preview.

Product:

ProBook 14

Price:
₹62,999

Availability:
In stock

Category:
Laptop

Best For:
AI development, coding, college

Specifications:

16GB RAM
512GB SSD
14-inch display

AI description:

"Portable performance laptop suitable for students and developers who need strong multitasking and development capability."

Show a small label:

AI-Readable Product Profile

---

# 13. NEW SCREEN 09 — AI BUYER

This is one of the MOST IMPORTANT DEMO SCREENS.

The visual style should differ slightly from the merchant dashboard while preserving the RAYGO design system.

Header:

RAYGO AI Commerce

Subtitle:

"Tell me what you're looking for."

Large input:

"I need a laptop setup for AI development and college under ₹70,000."

CTA:

"Find Products"

---

## AI response

"I found 3 options matching your budget, workload and availability."

Show product cards.

Primary:

ProBook 14
₹62,999

16GB RAM
512GB SSD

"Best balance for AI development and portability."

Actions:

Compare
Add to Basket

---

## Recommendation explanation

Small section:

WHY RAYGO SELECTED THIS

✓ Within budget
✓ Suitable memory
✓ In stock
✓ Good for development
✓ Merchant supports AI checkout

---

# 14. NEW SCREEN 10 — AI BUYER BASKET

Show:

Your Basket

Product
Quantity
Price

ProBook 14
1
₹62,999

Laptop Stand
1
₹1,799

USB-C Dock
1
₹4,999

Subtotal:
₹69,797

Recommended bundle adjustment:

"RAYGO found a permitted bundle price."

Bundle discount:
₹1,298

Total:
₹68,499

CTA:

"Review Purchase"

---

# 15. NEW SCREEN 11 — AI CHECKOUT

This must look like a real purchase authorization screen.

Header:

Review Purchase

Sections:

BUYER REQUEST

"I need a laptop setup for AI development and college under ₹70,000."

SELECTED PRODUCTS

Show products.

TOTAL:

₹68,499

---

## Why RAYGO prepared this purchase

✓ Matches requested budget
✓ Meets required specifications
✓ Products currently in stock
✓ Merchant allows AI commerce
✓ Price verified

---

## Authorization Gate

Prominent panel:

"Purchase authorization required"

"RAYGO will not execute payment until you confirm this purchase."

Button:

"Confirm & Pay"

Small label:

Razorpay Test Mode

---

# 16. NEW SCREEN 12 — PAYMENT SUCCESS

Create a polished success screen.

Header:

Payment Successful

Amount:

₹68,499

Order:

#RGO-10482

Payment:
Successful

Environment:
Razorpay Test Mode

---

## Transaction timeline

Intent received
✓

Products selected
✓

Order created
✓

Payment authorized
✓

Order confirmed
✓

---

## AI Commerce Summary

Decision time:
2.4 sec

Recommendation confidence:
92%

Checkout:
Completed

CTA:

"Return to Merchant Dashboard"

---

# 17. NEW SCREEN 13 — PAYMENT FAILURE

THIS IS A CRITICAL JUDGE DEMO.

Create a polished failure state.

Header:

Payment Unsuccessful

Amount:

₹68,499

Reason:

"Payment attempt was unsuccessful."

Do NOT use:
"Something went wrong."

---

## RAYGO SAFETY RESPONSE

Show:

✓ No duplicate payment attempted
✓ Order remains unpaid
✓ Inventory unchanged
✓ Failure recorded in audit trail
✓ Recovery option generated

---

## Critical status

AUTOMATIC RETRY:
BLOCKED

Reason:

"Duplicate-charge protection"

---

## Actions

Primary:

"Try Another Payment Method"

Secondary:

"Return to Basket"

---

# 18. NEW SCREEN 14 — AGENT ACTIVITY

HIGH PRIORITY.

Header:

Agent Activity

Subtitle:

"Observe what RAYGO's agents are doing across your commerce system."

---

## Agent status cards

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

---

## Live activity timeline

Example:

11:32:04
Revenue Intelligence
Detected cross-sell opportunity

11:32:05
Growth Strategist
Generated experiment hypothesis

11:32:06
Policy Guard
Policy check passed

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

The activity feed should visually communicate an agentic system without excessive animation.

---

# 19. NEW SCREEN 15 — POLICIES

HIGH PRIORITY.

Header:

Revenue Action Firewall

Subtitle:

"Control what RAYGO can propose and execute."

---

## Policy cards

Maximum Discount
20%

Minimum Margin
25%

Campaign Budget
₹10,000

Automatic Execution
OFF

Merchant Approval
REQUIRED

Payment Retry
BLOCKED

---

## Action Matrix

Columns:

Action
Can Propose
Can Execute
Approval

Create Bundle
Yes
Yes
Required

Discount >20%
Yes
No
Blocked

Create Campaign
Yes
Yes
Required

Payment Retry
Yes
No
Blocked

Refund
Yes
No
Required

Use clear status labels.

---

# 20. NEW SCREEN 16 — AUDIT TRAIL

HIGH PRIORITY.

Header:

Audit Trail

Subtitle:

"Every consequential AI action is recorded and explainable."

---

## Table

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
Buyer confirmed purchase
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

---

## Audit detail drawer

Clicking a row opens:

Decision Summary

Evidence

Action

Policy Checks

Approval

Execution Result

Failure / Recovery

Related Order

Do not show hidden chain-of-thought.

Show concise decision explanations and auditable metadata only.

---

# 21. NEW SCREEN 17 — PRODUCTS

Create a simple but polished catalog management screen.

Header:

Products

Table:

Product
Price
Inventory
AI Readiness
Issues
Status

Example:

ProBook 14
₹62,999
42
94
None
Ready

Laptop Stand
₹1,799
12
81
Shipping metadata
Needs Attention

CTA:

"Optimize with RAYGO"

---

# 22. NEW SCREEN 18 — ORDERS

Header:

Orders

Metrics:

GMV
Successful Payments
Failed Payments
AI Buyer Orders

Table:

Order
Customer
Amount
Source
Payment
Status

Use realistic data.

---

# 23. NEW SCREEN 19 — PAYMENTS

Header:

Payments

Metrics:

Successful
Failed
Pending
Refunds

Table:

Payment ID
Order
Amount
Method
Status
Timestamp

Include Test Mode label where appropriate.

---

# 24. ASK RAYGO

Do NOT create a huge chatbot interface.

Create a compact command interface.

Placeholder:

"Ask RAYGO..."

Suggested commands:

Why did revenue change yesterday?

Show my highest-value opportunities.

Which experiment should I scale?

Why is AI Commerce readiness 82?

Show blocked actions.

When a command is selected, navigate to the relevant screen.

---

# 25. PRIMARY CLICKABLE DEMO FLOW

This exact flow MUST work in the Stitch prototype.

START:

Onboarding

↓

Initialize RAYGO

↓

Overview

↓

Review Opportunity

↓

Opportunity Detail

↓

Approve & Create Experiment

↓

Experiment Detail

↓

Scale Experiment

↓

AI Commerce

↓

AI Buyer

↓

Search "I need a laptop setup for AI development and college under ₹70,000."

↓

Product Recommendation

↓

Add to Basket

↓

Review Purchase

↓

Confirm & Pay

↓

Payment Success

AND separately:

Confirm & Pay

↓

Payment Failure

↓

Automatic Retry Blocked

↓

Audit Trail

This is the primary judging journey.

---

# 26. SECONDARY DEMO FLOW — AGENTIC REVENUE LOOP

The prototype should also visually communicate:

Merchant data

↓

Revenue Intelligence Agent

↓

Opportunity

↓

Growth Strategist

↓

Experiment

↓

Policy Guard

↓

Merchant Approval

↓

Execution

↓

Measurement

↓

Revenue Impact

↓

Learning

---

# 27. AGENT ARCHITECTURE MUST BE VISIBLE IN UI

Use these exact logical agents:

1. Revenue Intelligence Agent
2. AI Commerce Agent
3. Growth Strategist Agent
4. Experiment Agent
5. Policy Guard
6. Payment Agent
7. Approval Gateway

Do not invent 15+ agents.

The UI should make clear that specialized agents have different responsibilities.

---

# 28. AI REASONING UX

Never show:

"Chain of Thought"

Never expose private model reasoning.

Instead use:

OBSERVED

DETECTED

EVIDENCE

HYPOTHESIS

PREDICTED OUTCOME

RECOMMENDATION

POLICY

APPROVAL

RESULT

This is the correct UX for explainable AI.

---

# 29. FINTECH TRUST REQUIREMENTS

Every financial action must show:

- amount
- purpose
- policy state
- approval state
- execution state
- result

Sensitive actions must not look automatic unless explicitly allowed.

Use:

Approval Required

Policy Blocked

Test Mode

Merchant Authorized

Execution Pending

Execution Complete

---

# 30. ERROR STATES

Add polished states for:

## Data unavailable

"Revenue analysis could not be refreshed. Your previous insights remain available."

## Agent unavailable

"RAYGO's reasoning service is temporarily unavailable. Deterministic recommendations remain available."

## Policy blocked

"Action blocked by merchant policy."

## Payment failed

"Payment unsuccessful. No automatic retry was attempted."

## Experiment insufficient data

"Not enough evidence to recommend scaling this experiment."

This makes the product look production-minded.

---

# 31. LOADING STATES

Use meaningful messages.

Examples:

"Analyzing commerce signals..."

"Evaluating opportunity..."

"Running policy checks..."

"Preparing experiment..."

"Creating order..."

"Verifying payment..."

Do not use generic:

"Loading..."

for important AI operations.

---

# 32. EMPTY STATES

Examples:

No opportunities:

"RAYGO hasn't identified a high-confidence opportunity yet."

No experiments:

"No active experiments. RAYGO will surface opportunities when enough evidence is available."

No audit entries:

"No consequential agent actions recorded."

---

# 33. MOBILE / RESPONSIVE

Maintain responsive behavior.

Desktop:
Full sidebar.

Tablet:
Condensed navigation.

Mobile:
Collapsible navigation.

Tables:
Horizontal scrolling or responsive cards.

Do not allow:
- clipped text
- overlapping buttons
- horizontal page overflow
- unreadable charts

---

# 34. PERFORMANCE

Avoid unnecessary animation.

Use subtle transitions only for:

- navigation
- drawers
- approval dialogs
- experiment progress
- payment state
- agent activity updates

Do not animate every card.

---

# 35. JUDGE-FIRST DESIGN

Within 60 seconds of opening the prototype, a judge must understand:

1. RAYGO finds revenue opportunities.
2. RAYGO explains the evidence.
3. RAYGO creates measurable experiments.
4. RAYGO protects financial actions with policies.
5. RAYGO enables AI buyers to transact.
6. RAYGO records consequential actions.

If any of these are difficult to understand visually, improve the hierarchy.

---

# 36. PRIORITY ORDER — VERY IMPORTANT

Because development time is extremely limited, build/modify in this order.

## P0 — MUST HAVE

1. Overview
2. Opportunity Detail
3. Experiment Detail
4. AI Commerce
5. AI Buyer
6. AI Checkout
7. Payment Success
8. Payment Failure
9. Policies
10. Audit Trail

## P1 — SHOULD HAVE

11. Opportunity Center
12. Experiments
13. Agent Activity
14. Products
15. Orders
16. Payments

## P2 — OPTIONAL

17. Settings
18. Advanced analytics
19. Extra dashboards

DO NOT spend time polishing P2 features before P0 is complete.

---

# 37. DO NOT REBUILD THE PROJECT

If Stitch has already generated a screen that satisfies this specification:

KEEP IT.

Only modify it where this PRD explicitly asks for changes.

Do not regenerate an existing screen simply to make it different.

Consistency is more important than novelty.

---

# 38. FINAL QUALITY CHECK

Before finalizing the Stitch project:

[ ] Existing Overview preserved

[ ] Existing Opportunity Center preserved

[ ] Existing Opportunity Detail preserved

[ ] Same sidebar everywhere

[ ] Same topbar everywhere

[ ] Same merchant everywhere

[ ] Same INR values everywhere

[ ] Same product catalog everywhere

[ ] Experiment flow exists

[ ] AI Commerce screen exists

[ ] AI Buyer screen exists

[ ] Checkout exists

[ ] Payment success exists

[ ] Payment failure exists

[ ] Agent Activity exists

[ ] Policy Firewall exists

[ ] Audit Trail exists

[ ] Failure handling is visible

[ ] Approval is explicit

[ ] Test Mode is clearly labeled

[ ] No fake chain-of-thought is displayed

[ ] No emoji icons

[ ] No excessive gradients

[ ] No excessive animation

[ ] Buttons navigate somewhere meaningful

[ ] Primary demo flow is clickable

[ ] Responsive layout is usable

[ ] Mock data is consistent

[ ] Product feels like one real system

---

# 39. FINAL STITCH INSTRUCTION

Extend and modify the existing RAYGO project according to this PRD.

Preserve the current visual design and the existing four completed screens.

Do not restart the design.

Prioritize P0 screens and the primary clickable demo flow.

The finished prototype should tell one coherent story:

A merchant opens RAYGO.

RAYGO discovers a revenue opportunity.

RAYGO explains why.

RAYGO proposes an experiment.

The policy firewall validates the action.

The merchant approves it.

The experiment produces measurable uplift.

An AI buyer discovers the merchant's products.

The AI buyer builds a basket.

The buyer authorizes payment.

Razorpay Test Mode represents the transaction.

A payment failure is handled safely.

Every consequential action appears in the audit trail.

The product should leave the judge with one clear impression:

"RAYGO is not just an AI dashboard. It is an autonomous, measurable, controlled revenue operating layer for AI-native commerce."

END OF MODIFICATION PRD.
