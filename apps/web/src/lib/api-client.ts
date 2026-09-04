import * as fixtures from "@/data/fixtures/demo-scenario";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api/v1";

async function request<T>(
  path: string,
  options?: RequestInit,
  fallback?: T
): Promise<T> {
  try {
    const url = `${API_BASE_URL.replace(/\/+$/, "")}/${path.replace(/^\/+/, "")}`;
    const res = await fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
    });
    if (!res.ok) {
      const errBody = await res.json().catch(() => ({}));
      const message = errBody.detail || errBody.message || `Request failed with status ${res.status}`;
      throw new Error(typeof message === "string" ? message : JSON.stringify(message));
    }
    return (await res.json()) as T;
  } catch (err) {
    if (fallback !== undefined) {
      console.warn(`[api-client] Falling back to fixtures for ${path}:`, err);
      return fallback;
    }
    throw err;
  }
}

// ---------------------------------------------------------------------------
// Health & Merchant
// ---------------------------------------------------------------------------
export async function getHealth() {
  return request("health", { method: "GET" }, { status: "ok", database: "mongodb" });
}

export async function getMerchant() {
  return request("merchant", { method: "GET" }, fixtures.merchant);
}

export async function initializeOnboarding(payload?: { merchantId?: string; resetDemoData?: boolean }) {
  return request("merchant/onboarding/initialize", {
    method: "POST",
    body: JSON.stringify(payload || { merchantId: "merchant_novatech", resetDemoData: true }),
  });
}

// ---------------------------------------------------------------------------
// Dashboard Overview
// ---------------------------------------------------------------------------
export async function getDashboardOverview() {
  const fallback = {
    metrics: fixtures.metrics,
    revenueTrend: fixtures.revenueTrend,
    activeOpportunities: fixtures.opportunities.slice(0, 3),
    runningExperiment: fixtures.experiments[0],
  };
  return request("dashboard/overview", { method: "GET" }, fallback);
}

// ---------------------------------------------------------------------------
// Opportunities
// ---------------------------------------------------------------------------
export async function getOpportunities() {
  const fallback = {
    items: fixtures.opportunities,
    total: fixtures.opportunities.length,
    activeCount: fixtures.opportunities.length,
  };
  return request("opportunities", { method: "GET" }, fallback);
}

export async function getOpportunity(id: string) {
  const fallback = fixtures.opportunities.find((o) => o.id === id) || fixtures.opportunities[0];
  return request(`opportunities/${id}`, { method: "GET" }, fallback);
}

export async function approveOpportunity(
  id: string,
  approvedBy: string = "merchant_demo_user",
  confirmationText: string = "Approve & Create Experiment"
) {
  return request(`opportunities/${id}/approve`, {
    method: "POST",
    body: JSON.stringify({ approvedBy, confirmationText }),
  });
}

export async function rejectOpportunity(
  id: string,
  rejectedBy: string = "merchant_demo_user",
  reason: string = "Merchant declined the recommendation."
) {
  return request(`opportunities/${id}/reject`, {
    method: "POST",
    body: JSON.stringify({ rejectedBy, reason }),
  });
}

// ---------------------------------------------------------------------------
// Experiments
// ---------------------------------------------------------------------------
export async function getExperiments() {
  const fallback = {
    items: fixtures.experiments,
    total: fixtures.experiments.length,
    runningCount: fixtures.experiments.length,
  };
  return request("experiments", { method: "GET" }, fallback);
}

export async function getExperiment(id: string) {
  const fallback = fixtures.experiments.find((e) => e.id === id) || fixtures.experiments[0];
  return request(`experiments/${id}`, { method: "GET" }, fallback);
}

export async function scaleExperiment(
  id: string,
  approvedBy: string = "merchant_demo_user",
  confirmationText: string = "Scale Experiment"
) {
  return request(`experiments/${id}/scale`, {
    method: "POST",
    body: JSON.stringify({ approvedBy, confirmationText }),
  });
}

export async function rejectExperiment(
  id: string,
  rejectedBy: string = "merchant_demo_user",
  reason: string = "Merchant stopped the experiment."
) {
  return request(`experiments/${id}/reject`, {
    method: "POST",
    body: JSON.stringify({ rejectedBy, reason }),
  });
}

export async function getExperimentTimeline(id: string) {
  const fallback = {
    experimentId: id,
    timeline: [
      { timestamp: "11:32:04", stage: "opportunity_detected", agent: "Revenue Intelligence", message: "Cross-sell opportunity detected" },
      { timestamp: "11:32:05", stage: "hypothesis_generated", agent: "Growth Strategist", message: "Generated hypothesis with 10% bundle discount" },
      { timestamp: "11:32:06", stage: "policy_evaluated", agent: "Policy Guard", message: "Policy check passed: Discount (10% <= 20%), Margin (34% >= 25%)" },
      { timestamp: "11:32:07", stage: "approval_received", agent: "Approval Gateway", message: "Merchant approval confirmed" },
      { timestamp: "11:32:08", stage: "experiment_running", agent: "Experiment Agent", message: "Active traffic split (50/50 control vs variant)" },
    ],
  };
  return request(`experiments/${id}/timeline`, { method: "GET" }, fallback);
}

// ---------------------------------------------------------------------------
// Catalog & Categories
// ---------------------------------------------------------------------------
export async function getCategories() {
  const fallback = {
    items: [
      { id: "LAPTOP", name: "Laptops" },
      { id: "CPU", name: "Processors" },
      { id: "GPU", name: "Graphics Cards" },
      { id: "MOTHERBOARD", name: "Motherboards" },
      { id: "RAM", name: "Memory" },
      { id: "RAM_SLOT", name: "RAM Slots" },
      { id: "SSD", name: "Solid State Drives" },
      { id: "HDD", name: "Hard Disk Drives" },
      { id: "CASE", name: "PC Cases" },
      { id: "MONITOR", name: "Monitors" },
      { id: "KEYBOARD", name: "Keyboards" },
      { id: "MOUSE", name: "Mice" },
      { id: "AUDIO", name: "Audio" },
      { id: "DOCK", name: "Docks & Hubs" },
      { id: "ACCESSORIES", name: "Accessories" },
    ],
    total: 15,
  };
  return request("categories", { method: "GET" }, fallback);
}

export async function getProducts(params?: {
  category?: string;
  search?: string;
  stock?: string;
  active?: boolean;
  min_readiness?: number;
  status?: string;
  sort?: string;
  sort_dir?: string;
  limit?: number;
}) {
  const query = new URLSearchParams();
  if (params?.category) query.set("category", params.category);
  if (params?.search) query.set("search", params.search);
  if (params?.stock) query.set("stock", params.stock);
  if (params?.active !== undefined) query.set("active", String(params.active));
  if (params?.min_readiness !== undefined) query.set("min_readiness", String(params.min_readiness));
  if (params?.status) query.set("status", params.status);
  if (params?.sort) query.set("sort", params.sort);
  if (params?.sort_dir) query.set("sort_dir", params.sort_dir);
  if (params?.limit) query.set("limit", String(params.limit));

  const qs = query.toString();
  const path = qs ? `products?${qs}` : "products";
  const fallback = { items: fixtures.products, total: fixtures.products.length };
  return request(path, { method: "GET" }, fallback);
}

export async function getProduct(id: string) {
  const fallback = fixtures.products.find((p) => p.id === id) || fixtures.products[0];
  return request(`products/${id}`, { method: "GET" }, fallback);
}

export async function createProduct(payload: Record<string, unknown>) {
  return request("products", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function patchProduct(id: string, payload: Record<string, unknown>) {
  return request(`products/${id}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export async function adjustStock(id: string, quantity: number, reason: string = "Manual adjustment") {
  return request(`products/${id}/stock-adjust`, {
    method: "POST",
    body: JSON.stringify({ quantity, reason }),
  });
}

export async function activateProduct(id: string) {
  return request(`products/${id}/activate`, { method: "POST" });
}

export async function deactivateProduct(id: string) {
  return request(`products/${id}/deactivate`, { method: "POST" });
}

// ---------------------------------------------------------------------------
// AI Commerce Readiness & Optimization
// ---------------------------------------------------------------------------
export async function getAiCommerceReadiness() {
  const fallback = {
    readinessScore: fixtures.metrics.aiCommerceReadiness,
    activeCatalogCount: fixtures.products.length,
    readyCount: fixtures.products.filter((p) => p.status === "ready").length,
    needsAttentionCount: fixtures.products.filter((p) => p.status === "needs_attention").length,
    products: fixtures.products,
  };
  return request("ai-commerce/readiness", { method: "GET" }, fallback);
}

export async function optimizeCatalog(productIds?: string[]) {
  return request("ai-commerce/optimize-catalog", {
    method: "POST",
    body: JSON.stringify({ productIds: productIds || [] }),
  });
}

// ---------------------------------------------------------------------------
// AI Buyer & Cart Flow
// ---------------------------------------------------------------------------
export async function searchAiBuyer(buyerRequest: string, budget?: number) {
  return request("ai-buyer/search", {
    method: "POST",
    body: JSON.stringify({ buyerRequest, budget, currency: "INR" }),
  });
}

export async function createAiBuyerBasket(items: Array<{ productId: string; quantity: number }>, buyerIntentId?: string) {
  return request("ai-buyer/basket", {
    method: "POST",
    body: JSON.stringify({ items, buyerIntentId }),
  });
}

export async function getAiBuyerBasket(basketId: string) {
  return request(`ai-buyer/basket/${basketId}`, { method: "GET" });
}

export async function createOrderIntent(basketId: string, buyerRequest?: string) {
  return request("ai-buyer/order-intent", {
    method: "POST",
    body: JSON.stringify({ basketId, buyerRequest }),
  });
}

export async function getOrderIntent(orderIntentId: string) {
  return request(`ai-buyer/order-intent/${orderIntentId}`, { method: "GET" }, fixtures.orderIntent);
}

// ---------------------------------------------------------------------------
// Razorpay Payments & Verification
// ---------------------------------------------------------------------------
export async function createRazorpayOrder(orderIntentId: string, approvedBy: string = "merchant_demo_user") {
  return request("payments/razorpay/order", {
    method: "POST",
    body: JSON.stringify({ orderIntentId, approvedBy }),
  });
}

export async function verifyRazorpayPayment(payload: {
  orderIntentId: string;
  razorpayOrderId: string;
  razorpayPaymentId: string;
  razorpaySignature: string;
}) {
  return request("payments/razorpay/verify", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function recordRazorpayFailure(payload: {
  orderIntentId: string;
  razorpayOrderId?: string;
  errorCode?: string;
  errorDescription?: string;
}) {
  return request("payments/razorpay/failure", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function recordRazorpayDismiss(payload: {
  orderIntentId: string;
  razorpayOrderId?: string;
  reason?: string;
}) {
  return request("payments/razorpay/dismiss", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function getPaymentAttempt(id: string) {
  return request(`payments/${id}`, { method: "GET" });
}

export async function reconcilePayment(id: string) {
  return request(`payments/${id}/reconcile`, { method: "POST" });
}

export async function getPayments() {
  const fallback = {
    items: [
      {
        id: "pay_att_001",
        orderId: "#RGO-10482",
        customer: "AI Buyer Demo",
        amount: 68499,
        status: "captured",
        method: "Razorpay Test Mode",
        timestamp: "Today, 11:32",
      },
    ],
    total: 1,
  };
  return request("payments", { method: "GET" }, fallback);
}

export async function getOrders() {
  const fallback = {
    items: [
      {
        id: "intent_ai_setup_001",
        displayOrderId: "#RGO-10482",
        customer: "AI Buyer Demo",
        amount: 68499,
        status: "Success",
        source: "AI Buyer",
        items: fixtures.orderIntent.items,
        timestamp: "Today, 11:32",
      },
    ],
    total: 1,
  };
  return request("orders", { method: "GET" }, fallback);
}

// ---------------------------------------------------------------------------
// Policies & Guardrails
// ---------------------------------------------------------------------------
export async function getPolicies() {
  const fallback = {
    items: fixtures.policies,
    total: fixtures.policies.length,
    actionMatrix: fixtures.actionMatrix,
  };
  return request("policies", { method: "GET" }, fallback);
}

export async function patchPolicy(id: string, patch: { limit?: string; status?: string }) {
  return request(`policies/${id}`, {
    method: "PATCH",
    body: JSON.stringify(patch),
  });
}

export async function evaluatePolicy(payload: {
  actionType: string;
  targetType: string;
  targetId: string;
  proposedAction?: {
    discountPct?: number;
    estimatedMarginPct?: number;
    campaignSpend?: number;
  };
}) {
  return request("policies/evaluate", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

// ---------------------------------------------------------------------------
// Agents & Audit
// ---------------------------------------------------------------------------
export async function getAgentStatus() {
  const fallback = {
    items: fixtures.agents,
    activity: fixtures.agentTimeline,
  };
  return request("agents/status", { method: "GET" }, fallback);
}

export async function getAgentActivity() {
  return request("agents/activity", { method: "GET" }, { items: fixtures.agentTimeline });
}

export async function askCopilot(payload: { merchantId?: string; question: string }) {
  return request("agents/copilot/ask", {
    method: "POST",
    body: JSON.stringify({ merchantId: payload.merchantId || "merchant_novatech", question: payload.question }),
  });
}

export async function getAgentRuns(params?: { limit?: number; agent?: string }) {
  const query = new URLSearchParams();
  if (params?.limit) query.set("limit", String(params.limit));
  if (params?.agent) query.set("agent", params.agent);
  const qs = query.toString();
  const path = qs ? `agents/runs?${qs}` : "agents/runs";
  return request(path, { method: "GET" }, { items: [], total: 0 });
}

export async function getAuditTrail(params?: { limit?: number }) {
  const limit = params?.limit || 50;
  const path = `audit?limit=${limit}`;
  const fallback = { items: fixtures.auditEvents, total: fixtures.auditEvents.length };
  return request(path, { method: "GET" }, fallback);
}

export async function getAuditEvent(id: string) {
  const fallback = fixtures.auditEvents.find((a) => a.id === id) || fixtures.auditEvents[0];
  return request(`audit/${id}`, { method: "GET" }, fallback);
}
