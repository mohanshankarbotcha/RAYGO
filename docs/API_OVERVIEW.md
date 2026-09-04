# RAYGO: API Overview & Integration Reference

**Base URL**: `http://localhost:8000/api/v1`  
**Interactive Swagger UI**: `http://localhost:8000/docs`  
**OpenAPI Specification**: `http://localhost:8000/openapi.json`

---

## 1. Core API Domains

| Domain | Route Prefix | Responsibility | Key Endpoints |
|---|---|---|---|
| **Dashboard** | `/dashboard` | Executive KPIs & revenue trends | `GET /dashboard/overview` |
| **Products** | `/products` | Catalog & inventory control | `GET /products`, `POST /products/{id}/stock-adjust` |
| **Opportunities**| `/opportunities` | Revenue synergies & proposals | `GET /opportunities`, `POST /opportunities/{id}/approve` |
| **Experiments** | `/experiments` | A/B testing & variant scaling | `GET /experiments/{id}`, `POST /experiments/{id}/scale` |
| **AI Commerce** | `/ai-commerce` | Catalog AI readiness & profiles | `GET /ai-commerce/readiness`, `POST /ai-commerce/optimize`|
| **AI Buyer** | `/ai-buyer` | Natural language purchasing agent | `POST /ai-buyer/search`, `POST /ai-buyer/basket` |
| **Order Intents**| `/order-intents`| Checkout intent lifecycle | `POST /order-intents`, `GET /order-intents/{id}` |
| **Orders** | `/orders` | Confirmed paid orders ledger | `GET /orders`, `GET /orders/{id}` |
| **Payments** | `/payments` | Razorpay checkout & resilience | `POST /payments/razorpay/order`, `POST /payments/razorpay/verify`, `POST /payments/razorpay/failure`, `POST /payments/razorpay/dismiss`, `POST /payments/{id}/reconcile` |
| **Policies** | `/policies` | Policy Guard rule evaluations | `GET /policies`, `POST /policies/evaluate` |
| **Agents** | `/agents` | Agent control plane & Copilot | `GET /agents/status`, `GET /agents/runs`, `POST /agents/copilot/ask` |
| **Audit** | `/audit` | Immutable forensic audit trail | `GET /audit`, `GET /audit/{id}` |

---

## 2. Standard Response Envelope & Error Contract

### Standard Success Envelope
```json
{
  "items": [...],
  "total": 19,
  "nextCursor": null
}
```

### Standard Normalized Error Envelope
```json
{
  "error": {
    "code": "POLICY_BLOCKED",
    "message": "Discount 25.0% exceeds policy limit of 20.0%.",
    "details": {
      "policyEvaluationId": "pol_eval_7f9c2d11",
      "remediation": "Adjust proposed discount to 20% or lower."
    }
  }
}
```

---

## 3. Key State Machines

### 3.1 Order Intent State Machine
```text
[draft] ──► [review] ──► [approved] ──► [payment_order_created] ──► [paid]
                                                    │
                                                    ├──► [dismissed] (recoverable)
                                                    └──► [payment_failed] (retry blocked)
```

### 3.2 Experiment State Machine
```text
[draft] ──► [running] ──► [scaled] ──► [active_in_catalog]
                 │
                 └──► [terminated]
```
