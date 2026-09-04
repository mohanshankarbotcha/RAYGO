export type Merchant = {
  id: string;
  name: string;
  category: string;
  currency: "INR";
};

export type Product = {
  id: string;
  name: string;
  price: number;
  inventory: number;
  aiReadiness: number;
  category?: string;
  sku?: string;
  brand?: string;
  status?: "ready" | "needs_attention" | "inactive";
  issues?: string[];
  specs?: Record<string, string | number | boolean>;
  shipping?: {
    weightKg?: number;
    dimensionsCm?: string;
    tier?: string;
  };
};

export type Metrics = {
  totalRevenue: number;
  revenueGrowthPct: number;
  raygoInfluencedRevenue: number;
  raygoLiftPct: number;
  activeOpportunities: number;
  aiCommerceReadiness: number;
  projectedOpportunityImpact: number;
};

export type OpportunityStatus =
  | "ready_for_review"
  | "approved"
  | "running_experiment"
  | "declined";

export type Opportunity = {
  id: string;
  title: string;
  shortTitle: string;
  type: "cross_sell" | "bundle" | "pricing" | "retention";
  expectedMonthlyImpact: number;
  confidence: number;
  risk: "low" | "medium" | "high";
  status: OpportunityStatus;
  currentAttachRate: number;
  projectedAttachRate: number;
  targetSegment: string;
  eligibleJourneys: number;
  observed: string;
  detected: string;
  hypothesized: string;
  predicted: string;
};

export type Experiment = {
  id: string;
  opportunityId: string;
  name: string;
  status: "running" | "completed" | "paused";
  controlConversion: number;
  variantConversion: number;
  conversionUplift: number;
  revenueUplift: number;
  aovUplift: number;
  confidence: number;
  recommendation: "scale_variant" | "keep_running" | "revert_control";
  hypothesis?: string;
  sampleSize?: number;
  targetSegment?: string;
  decisionReason?: string;
};

export type OrderIntentItem = {
  productId: string;
  name: string;
  quantity: number;
  unitPrice: number;
};

export type OrderIntent = {
  orderIntentId: string;
  displayOrderId?: string;
  buyerRequest: string;
  items: OrderIntentItem[];
  subtotal: number;
  bundleDiscount: number;
  total: number;
  currency: "INR";
};

export type Policy = {
  id: string;
  name: string;
  description: string;
  limitLabel: string;
  status: "active" | "paused";
};

export type AgentService = {
  id: string;
  name: string;
  description: string;
  status: "active" | "running" | "ready" | "paused" | "error";
  lastAction: string;
  lastRunAt: string;
};

export type AuditEvent = {
  id: string;
  actor: "raygo_agent" | "merchant" | "system" | "razorpay";
  action: string;
  target: string;
  outcome: "success" | "blocked" | "failed";
  timestamp: string;
  detail: string;
};
