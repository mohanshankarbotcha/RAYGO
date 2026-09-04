# RAYGO — AI AGENT LAYER + AUTOMATED QA PRD

## Mission
Implement the AI Agent Layer on the already-working RAYGO frontend and backend. Preserve the existing glassmorphism UI and routes, while making AI interactions fast, reliable, safe, and smooth.

### Non-negotiable
- Use Google Gemini API and Google ADK where appropriate.
- The real `GEMINI_API_KEY` is supplied manually by the developer. Claude must never request, print, commit, expose, or embed the secret.
- Keep the key server-side only.
- Gemini reasons/selects typed tools; backend validates and executes.
- Gemini must never directly modify MongoDB or receive payment credentials.
- Policy Guard and Approval Gateway remain backend-controlled.
- Do not expose private chain-of-thought.
- Do not rebuild completed frontend screens.

## 1. Agents
Implement:
1. RAYGO Coordinator — routing/orchestration.
2. Revenue Intelligence Agent — opportunities/evidence.
3. Growth Strategist Agent — hypotheses/actions.
4. Experiment Agent — create/evaluate/scale recommendations.
5. AI Commerce Agent — buyer intent/catalog retrieval/ranking.
6. Policy Guard — deterministic enforcement.
7. Approval Gateway — explicit authorization.
8. Payment Agent — payment orchestration only.
9. Audit integration — consequential-action records.

## 2. Gemini Provider
Create:
- `GeminiProvider`
- `DeterministicProvider`

Support:
- structured generation
- typed tool/function calling
- bounded timeouts
- bounded retries only for safe/idempotent operations
- health check
- deterministic fallback

Use `.env.example`:
```env
GEMINI_API_KEY=
GEMINI_MODEL=
GEMINI_TEMPERATURE=0.2
GEMINI_TIMEOUT_SECONDS=30
GEMINI_MAX_RETRIES=2
```

Never put the real key in frontend code, bundles, README, Git, screenshots, logs, tests, or `NEXT_PUBLIC_*`.

## 3. Coordinator
Route:
- revenue → Revenue Intelligence
- growth → Growth Strategist
- experiment → Experiment Agent
- product discovery → AI Commerce
- policy → Policy Guard
- payment → Payment Agent

Return typed output containing intent, selected agent, action, approval requirement, confidence, short reason, and next step.

The Coordinator cannot bypass policy or execute financial operations.

## 4. Revenue Intelligence
Use deterministic backend metrics as facts. Gemini interprets them.

Return:
- opportunity ID
- type
- title
- evidence
- estimated impact
- confidence
- risk
- recommendation
- approval requirement

Do not invent financial values.

## 5. Growth Strategist
Convert validated opportunities into hypotheses/actions such as:
- cross-sell
- upsell
- bundle
- recovery
- campaign
- recommendation

No direct financial execution.

## 6. Experiment Agent
Flow:
`Opportunity → Hypothesis → Design → Policy → Approval → Start → Measure → Evaluate → Recommend`

Recommendations:
- SCALE
- KEEP_RUNNING
- STOP

Backend calculates metrics; AI explains results.

## 7. AI Commerce Agent
Handle natural-language buyer intent, constraints, catalog retrieval/ranking, recommendation explanations, basket recommendations, catalog readiness, and missing metadata.

Product price, stock, specifications, and availability must come from backend catalog data.

## 8. Policy Guard + Approval
Demo rules:
- max discount 20%
- minimum margin 25%
- campaign budget ₹10,000
- automatic execution OFF
- payment retry BLOCKED

Flow:
`PROPOSE → VALIDATE → POLICY → APPROVAL → EXECUTE → AUDIT`

AI-generated text saying “approved” is never authorization.

## 9. Payment Agent
Use the existing secure Razorpay Test Mode service boundary.
- Gemini never receives Razorpay secrets.
- No blind retries.
- Preserve unpaid state after failure.
- Prevent duplicates with idempotency/state checks.
- Audit success/failure.

## 10. Tool Registry
Explicit typed allow-list for:
- revenue metrics/opportunities
- growth validation
- experiment create/read/evaluate/scale
- product search/read/readiness
- policy checks
- approvals
- payment order/status/verification
- activity/audit queries

Every tool declares input/output schemas, authorization, side-effect class, and audit requirement.

Classes:
`READ_ONLY`, `SAFE_WRITE`, `CONSEQUENTIAL`, `FINANCIAL`.

## 11. Structured Output
All machine-relevant Gemini responses must validate against typed/Pydantic schemas.

If invalid:
1. never execute the tool;
2. optionally perform one bounded safe repair;
3. otherwise fallback or return a safe error;
4. record the failure.

## 12. Deterministic Fallback
If Gemini is unavailable due to missing/invalid key, timeout, rate limit, outage, or malformed output, use deterministic backend logic where possible and clearly identify fallback mode.

## 13. Smoothness + Performance — P0
The current application works but is slower than desired. Treat smoothness as a first-class requirement.

### Frontend
- Immediate visual acknowledgement for every action.
- Async requests; skeleton/loading states.
- Disable only the active action while running.
- Prevent duplicate clicks/submissions.
- No unnecessary full-page reloads.
- Preserve existing data while refreshing.
- Update only affected components.
- Cache stable read-heavy data where appropriate.
- Debounce buyer/catalog search.
- Cancel stale requests when superseded.
- Optimistic updates only for safe reversible UI states; never for payment/irreversible actions.

### Backend
- Async I/O for external calls.
- Explicit timeouts.
- Reuse HTTP/database clients where appropriate.
- Avoid N+1 queries.
- Index frequent opportunity/product/order/audit lookups.
- Paginate activity/audit data.
- Return only required fields.
- Avoid repeated expensive metric calculations.
- Run independent safe reads concurrently.
- Keep policy checks local and fast.
- Do not call Gemini when deterministic logic is sufficient.

### AI latency
- Keep prompts concise.
- Send only relevant context, not entire database/application state.
- Avoid unnecessary agent-to-agent loops.
- Bound output tokens.
- Use lower-latency configuration for simple routing where appropriate.
- Use deterministic tools for calculations/validation.
- Never block indefinitely.

### Engineering targets
- deterministic read/API path: ideally <500 ms locally where practical
- policy check: ideally <100 ms locally
- normal AI request: target <5 s end-to-end where practical
- immediate UI acknowledgement
- bounded retries and polling

Measure first, then optimize the highest-impact bottlenecks.

## 14. Observability
Record:
- correlation/request ID
- agent/provider/model
- start/end
- latency
- tool calls
- policy result
- approval result
- execution result
- success/failure

Never log secrets or private chain-of-thought.

Add timing around Gemini, database, tools, policy, and payment service calls.

## 15. Agent Activity + Audit
Emit real agent events for opportunity detection, hypothesis generation, policy decisions, approval, experiment creation, payment outcomes, and blocked retries.

Audit every consequential action with:
- audit ID
- timestamp
- agent
- action
- reason summary
- input reference
- policy result
- approval result
- execution result
- correlation ID
- status

## 16. README Update
Update `README.md` with:
- AI architecture
- agent responsibility matrix
- Gemini setup using `GEMINI_API_KEY` without exposing the secret
- UI button → route → backend endpoint → agent → tool → result mapping
- run commands
- fallback mode
- troubleshooting
- performance notes
- automated test commands
- final test status

Map at minimum:
Review Opportunity; Approve & Create Experiment; Scale Experiment; Optimize Catalog; Find Products; Add to Basket; Confirm & Pay; Agent Activity; Policies; Audit Trail.

Use actual repository routes/endpoints.

## 17. Automated QA — Claude owns testing
The user will NOT manually test the application.

Claude must:
1. run existing tests;
2. add missing agent/tool/policy/integration tests;
3. test every agent and major button flow;
4. test success/failure paths;
5. test Gemini timeout/rate-limit/malformed output;
6. test deterministic fallback;
7. test policy/approval gates;
8. test payment failure and idempotency;
9. test prompt injection;
10. scan for secret leakage;
11. measure slow endpoints/agent calls;
12. diagnose and fix failures;
13. rerun tests after fixes;
14. report final pass/fail, performance bottlenecks, fixes, and remaining limitations.

Do not weaken/delete tests just to obtain a green build.

## 18. Deliverables
- AI agents
- Gemini provider
- ADK integration
- typed schemas
- tool registry
- policy/approval integration
- payment-agent boundary
- fallback provider
- activity/audit integration
- `.env.example`
- README.md
- automated tests
- `MANUAL_TEST_PLAN.md` as test specification/reference
- final test report

## 19. Definition of Done
All P0 agents work; outputs validate; tools are allow-listed; policies cannot be bypassed; approvals are real backend authorization; payment actions are safe/idempotent; activity/audit records are real; fallback works; secrets are protected; key flows feel responsive; automated tests pass; no critical known regression remains.

End-to-end:
`Overview → Opportunity → AI Reasoning → Experiment → Policy → Approval → Experiment Result → AI Commerce → AI Buyer → Basket → Checkout → Razorpay Test Mode → Success/Failure → Activity → Audit`
