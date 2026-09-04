import type {
  Merchant,
  Product,
  Metrics,
  Opportunity,
  Experiment,
  OrderIntent,
  Policy,
  AgentService,
  AuditEvent,
} from "./types";

export const merchant: Merchant = {
  id: "merchant_novatech",
  name: "NovaTech Store",
  category: "Consumer Electronics",
  currency: "INR",
};

export const products: Product[] = [
  { id: "prod_probook_14", name: "ProBook 14", category: "Laptops", price: 62999, inventory: 42, aiReadiness: 94, brand: "NovaTech", sku: "NT-LAP-001", status: "ready", specs: { cpu: "Intel Core Ultra 7", ram: "32GB DDR5", storage: "1TB NVMe" }, shipping: { weightKg: 1.35, dimensionsCm: "31x22x1.6", tier: "Standard Express" } },
  { id: "prod_wireless_keyboard", name: "Wireless Keyboard", category: "Keyboards", price: 2499, inventory: 86, aiReadiness: 89, brand: "NovaTech", sku: "NT-KB-002", status: "ready", specs: { switch: "Red Linear", connectivity: "Bluetooth / 2.4GHz" }, shipping: { weightKg: 0.65, dimensionsCm: "32x12x3.5", tier: "Standard" } },
  { id: "prod_laptop_stand", name: "Laptop Stand", category: "Accessories", price: 1799, inventory: 12, aiReadiness: 81, brand: "NovaTech", sku: "NT-ACC-003", status: "needs_attention", issues: ["Shipping metadata"], specs: { material: "Anodized Aluminum", maxSize: "17 inch" }, shipping: { weightKg: 0.45, dimensionsCm: "26x24x4", tier: "Standard" } },
  { id: "prod_ai_mouse_pro", name: "AI Mouse Pro", category: "Mice", price: 1299, inventory: 64, aiReadiness: 76, brand: "NovaTech", sku: "NT-MS-004", status: "needs_attention", issues: ["Ambiguous attributes"], specs: { dpi: 4000, sensor: "Optical Precision" }, shipping: { weightKg: 0.12, dimensionsCm: "11x6x3.8", tier: "Standard" } },
  { id: "prod_usb_c_dock", name: "USB-C Dock", category: "Docks", price: 4999, inventory: 20, aiReadiness: 84, brand: "NovaTech", sku: "NT-DCK-005", status: "ready", specs: { powerDelivery: "100W", ports: "Dual 4K HDMI, 3x USB 3.2, 1GbE" }, shipping: { weightKg: 0.28, dimensionsCm: "15x7x2", tier: "Standard" } },
  { id: "prod_headphones", name: "NoiseCancel Headphones", category: "Audio", price: 6499, inventory: 17, aiReadiness: 78, brand: "NovaTech", sku: "NT-AUD-006", status: "needs_attention", issues: ["Shipping metadata"], specs: { anc: "Hybrid ANC 40dB", batteryHours: 40 }, shipping: { weightKg: 0.29, dimensionsCm: "20x18x8", tier: "Standard" } },
  { id: "prod_4k_monitor", name: "27 inch 4K Monitor", category: "Monitors", price: 29999, inventory: 9, aiReadiness: 72, brand: "NovaTech", sku: "NT-MON-007", status: "needs_attention", issues: ["Shipping metadata"], specs: { panel: "IPS 4K UHD", colorGamut: "99% sRGB", refreshRate: "60Hz" }, shipping: { weightKg: 6.2, dimensionsCm: "61x36x5", tier: "Fragile Heavy" } },
  { id: "prod_cpu_ryzen7", name: "Ryzen 7 7800X3D", category: "CPUs", price: 38999, inventory: 15, aiReadiness: 95, brand: "AMD", sku: "NT-CPU-7800X", status: "ready", specs: { socket: "AM5", cores: 8, threads: 16, tdp: "120W", l3Cache: "96MB 3D V-Cache" }, shipping: { weightKg: 0.35, dimensionsCm: "14x14x6", tier: "Standard" } },
  { id: "prod_cpu_i7_14700k", name: "Intel Core i7-14700K", category: "CPUs", price: 34999, inventory: 18, aiReadiness: 92, brand: "Intel", sku: "NT-CPU-14700K", status: "ready", specs: { socket: "LGA1700", cores: 20, threads: 28, tdp: "125W", maxClock: "5.6 GHz" }, shipping: { weightKg: 0.38, dimensionsCm: "14x14x6", tier: "Standard" } },
  { id: "prod_case_airflow", name: "RAYGO Airflow Case", category: "PC Cases", price: 5999, inventory: 20, aiReadiness: 90, brand: "RAYGO", sku: "NT-CSE-001", status: "ready", specs: { formFactor: "Mid Tower", motherboardSupport: "ATX, Micro-ATX, Mini-ITX", gpuClearance: "380mm" }, shipping: { weightKg: 7.5, dimensionsCm: "46x22x48", tier: "Standard Heavy" } },
  { id: "prod_case_titan", name: "Titan ATX Gaming Case", category: "PC Cases", price: 9999, inventory: 11, aiReadiness: 88, brand: "Titan", sku: "NT-CSE-002", status: "ready", specs: { formFactor: "Full Tower", radiatorSupport: "Up to 420mm", sidePanel: "Tempered Glass" }, shipping: { weightKg: 9.2, dimensionsCm: "52x24x54", tier: "Standard Heavy" } },
  { id: "prod_gpu_rtx_4070s", name: "NVIDIA RTX 4070 Super 12GB", category: "Graphics Cards", price: 58999, inventory: 8, aiReadiness: 96, brand: "NVIDIA", sku: "NT-GPU-4070S", status: "ready", specs: { vram: "12GB GDDR6X", recommendedPsu: "650W", interface: "PCIe 4.0 x16" }, shipping: { weightKg: 1.25, dimensionsCm: "26x12x4", tier: "High Value Fragile" } },
  { id: "prod_gpu_rx_7800xt", name: "AMD Radeon RX 7800 XT 16GB", category: "Graphics Cards", price: 51999, inventory: 10, aiReadiness: 91, brand: "AMD", sku: "NT-GPU-7800XT", status: "ready", specs: { vram: "16GB GDDR6", recommendedPsu: "700W", interface: "PCIe 4.0 x16" }, shipping: { weightKg: 1.35, dimensionsCm: "28x13x5", tier: "High Value Fragile" } },
  { id: "prod_mb_b650e", name: "ROG Strix B650E-F Gaming WiFi", category: "Motherboards", price: 27999, inventory: 14, aiReadiness: 93, brand: "ASUS", sku: "NT-MB-B650E", status: "ready", specs: { socket: "AM5", chipset: "AMD B650", memorySlots: "4x DDR5", pcieGen5: true }, shipping: { weightKg: 1.6, dimensionsCm: "34x27x7", tier: "Standard" } },
  { id: "prod_mb_z790", name: "Z790 AORUS Elite AX", category: "Motherboards", price: 25999, inventory: 12, aiReadiness: 89, brand: "Gigabyte", sku: "NT-MB-Z790", status: "ready", specs: { socket: "LGA1700", chipset: "Intel Z790", memorySlots: "4x DDR5", wifi6e: true }, shipping: { weightKg: 1.55, dimensionsCm: "34x27x7", tier: "Standard" } },
  { id: "prod_ram_ddr5_32gb", name: "Corsair Vengeance 32GB (2x16GB) DDR5 6000MHz", category: "RAM", price: 10499, inventory: 28, aiReadiness: 94, brand: "Corsair", sku: "NT-RAM-DDR5-32", status: "ready", specs: { type: "DDR5", speed: "6000 MT/s", latency: "CL36", dimmCount: 2 }, shipping: { weightKg: 0.15, dimensionsCm: "16x9x1.5", tier: "Standard" } },
  { id: "prod_ram_gskill_32gb", name: "G.Skill Trident Z5 RGB 32GB DDR5 6400MHz", category: "RAM", price: 12999, inventory: 16, aiReadiness: 91, brand: "G.Skill", sku: "NT-RAM-TRIDENT-32", status: "ready", specs: { type: "DDR5", speed: "6400 MT/s", latency: "CL32", rgb: true }, shipping: { weightKg: 0.18, dimensionsCm: "16x9x1.8", tier: "Standard" } },
  { id: "prod_ssd_990pro_2tb", name: "Samsung 990 PRO 2TB NVMe M.2 SSD", category: "SSD", price: 16999, inventory: 22, aiReadiness: 97, brand: "Samsung", sku: "NT-SSD-990P-2T", status: "ready", specs: { formFactor: "M.2 2280", interface: "PCIe 4.0 NVMe", readSpeed: "7450 MB/s", writeSpeed: "6900 MB/s" }, shipping: { weightKg: 0.08, dimensionsCm: "14x10x2", tier: "Standard" } },
  { id: "prod_hdd_ironwolf_4tb", name: "Seagate IronWolf 4TB NAS HDD", category: "HDD", price: 9499, inventory: 19, aiReadiness: 88, brand: "Seagate", sku: "NT-HDD-IW-4TB", status: "ready", specs: { capacity: "4TB", rpm: 5400, cache: "256MB", formFactor: "3.5 inch" }, shipping: { weightKg: 0.65, dimensionsCm: "18x13x4", tier: "Fragile Standard" } },
];

export const metrics: Metrics = {
  totalRevenue: 284620,
  revenueGrowthPct: 18.7,
  raygoInfluencedRevenue: 42800,
  raygoLiftPct: 14.2,
  activeOpportunities: 7,
  aiCommerceReadiness: 82,
  projectedOpportunityImpact: 40000,
};

export const revenueTrend = [
  { day: "Day 1", revenue: 7200 }, { day: "Day 5", revenue: 8100 },
  { day: "Day 10", revenue: 7800 }, { day: "Day 15", revenue: 9400 },
  { day: "Day 20", revenue: 10200 }, { day: "Day 25", revenue: 11800 },
  { day: "Day 30", revenue: 13100 },
];

export const opportunities: Opportunity[] = [
  {
    id: "opp_keyboard_stand",
    title: "Cross-sell opportunity: Wireless Keyboard -> Laptop Stand",
    shortTitle: "Keyboard + Stand",
    type: "cross_sell",
    expectedMonthlyImpact: 18400,
    confidence: 87,
    risk: "low",
    status: "ready_for_review",
    currentAttachRate: 4.1,
    projectedAttachRate: 7.8,
    targetSegment: "Remote Workers",
    eligibleJourneys: 1842,
    observed: "Wireless Keyboard purchases have increased by 14% over the last 30 days.",
    detected: "Laptop Stand views increased among the same buyer cohort.",
    hypothesized: "Users are building complete ergonomic desk setups.",
    predicted: "A cross-sell prompt can increase attach rate from 4.1% to 7.8%.",
  },
  {
    id: "opp_probook_bundle",
    title: "Bundle opportunity: ProBook 14 -> USB-C Dock",
    shortTitle: "ProBook Bundle",
    type: "bundle",
    expectedMonthlyImpact: 12200,
    confidence: 91,
    risk: "low",
    status: "running_experiment",
    currentAttachRate: 6.5,
    projectedAttachRate: 11.2,
    targetSegment: "New Laptop Buyers",
    eligibleJourneys: 980,
    observed: "ProBook 14 buyers frequently return within 48 hours to search docking accessories.",
    detected: "USB-C Dock detail views spike immediately after ProBook 14 purchases.",
    hypothesized: "Buyers want a complete workstation setup at time of purchase.",
    predicted: "A bundled dock offer can raise attach rate from 6.5% to 11.2%.",
  },
  {
    id: "opp_recovery_campaign",
    title: "Recovery opportunity: Abandoned AI Mouse Pro carts",
    shortTitle: "Recovery Campaign",
    type: "retention",
    expectedMonthlyImpact: 9400,
    confidence: 78,
    risk: "medium",
    status: "ready_for_review",
    currentAttachRate: 2.2,
    projectedAttachRate: 4.6,
    targetSegment: "Cart Abandoners",
    eligibleJourneys: 611,
    observed: "AI Mouse Pro has the highest cart-abandonment rate in the catalog.",
    detected: "Abandonment concentrates in the last pricing-review step.",
    hypothesized: "Buyers are price-sensitive at checkout, not product-uncertain.",
    predicted: "A targeted recovery nudge can double recovered checkout rate.",
  },
];

export const experiments: Experiment[] = [
  {
    id: "exp_keyboard_stand",
    opportunityId: "opp_keyboard_stand",
    name: "Keyboard + Laptop Stand",
    status: "running",
    controlConversion: 6.2,
    variantConversion: 8.9,
    conversionUplift: 43.5,
    revenueUplift: 23.4,
    aovUplift: 8.7,
    confidence: 94,
    recommendation: "scale_variant",
  },
];

export const orderIntent: OrderIntent = {
  orderIntentId: "intent_ai_setup_001",
  buyerRequest: "I need a laptop setup for AI development and college under ₹70,000.",
  items: [
    { productId: "prod_probook_14", name: "ProBook 14", quantity: 1, unitPrice: 62999 },
    { productId: "prod_usb_c_dock", name: "USB-C Dock", quantity: 1, unitPrice: 4999 },
    { productId: "prod_laptop_stand", name: "Laptop Stand", quantity: 1, unitPrice: 1799 },
  ],
  subtotal: 69797,
  bundleDiscount: 1298,
  total: 68499,
  currency: "INR",
};

export const policies: Policy[] = [
  { id: "pol_discount", name: "Discount Limit", description: "Maximum discount RAYGO may propose without escalation.", limitLabel: "Max 20%", status: "active" },
  { id: "pol_margin", name: "Margin Floor", description: "Minimum acceptable margin for any proposed action.", limitLabel: "Min 25%", status: "active" },
  { id: "pol_budget", name: "Daily Budget", description: "Maximum campaign spend RAYGO may commit per day.", limitLabel: "₹10,000", status: "active" },
  { id: "pol_auto_exec", name: "Auto Execution", description: "Whether RAYGO may execute actions without merchant confirmation.", limitLabel: "OFF", status: "paused" },
  { id: "pol_merchant_auth", name: "Merchant Auth", description: "Merchant approval required before consequential actions.", limitLabel: "REQUIRED", status: "active" },
  { id: "pol_payment_retry", name: "Payment Retry", description: "Automatic retry of a failed payment attempt.", limitLabel: "BLOCKED", status: "active" },
];

export const actionMatrix = [
  { action: "Create Bundle", canPropose: true, canExecute: true, approval: "Required" },
  { action: "Discount >20%", canPropose: true, canExecute: false, approval: "Blocked" },
  { action: "Create Campaign", canPropose: true, canExecute: true, approval: "Required" },
  { action: "Payment Retry", canPropose: true, canExecute: false, approval: "Blocked" },
  { action: "Refund", canPropose: true, canExecute: false, approval: "Required" },
];

export const agents: AgentService[] = [
  { id: "agent_revenue_intel", name: "Revenue Intelligence", description: "Scans commerce signals for growth opportunities.", status: "active", lastAction: "Detected cross-sell opportunity", lastRunAt: "11:32:04" },
  { id: "agent_ai_commerce", name: "AI Commerce", description: "Maintains AI-readable catalog profile.", status: "active", lastAction: "Normalized product attributes", lastRunAt: "11:29:40" },
  { id: "agent_growth_strategist", name: "Growth Strategist", description: "Generates experiment hypotheses from opportunities.", status: "active", lastAction: "Generated experiment hypothesis", lastRunAt: "11:32:05" },
  { id: "agent_experiment", name: "Experiment Agent", description: "Runs and measures growth experiments.", status: "running", lastAction: "Experiment created", lastRunAt: "11:32:08" },
  { id: "agent_policy_guard", name: "Policy Guard", description: "Evaluates every consequential action against policy.", status: "active", lastAction: "Policy check passed", lastRunAt: "11:32:06" },
  { id: "agent_payment", name: "Payment Agent", description: "Creates and verifies Razorpay Test Mode payments.", status: "ready", lastAction: "Payment attempt failed", lastRunAt: "11:32:12" },
  { id: "agent_approval_gateway", name: "Approval Gateway", description: "Routes consequential actions for merchant approval.", status: "ready", lastAction: "Merchant approval received", lastRunAt: "11:32:07" },
];

export const agentTimeline = [
  { time: "11:32:04", agent: "Revenue Intelligence", event: "Detected cross-sell opportunity" },
  { time: "11:32:05", agent: "Growth Strategist", event: "Generated experiment hypothesis" },
  { time: "11:32:06", agent: "Policy Guard", event: "Policy check passed" },
  { time: "11:32:07", agent: "Approval Gateway", event: "Merchant approval received" },
  { time: "11:32:08", agent: "Experiment Agent", event: "Experiment created" },
  { time: "11:32:12", agent: "Payment Agent", event: "Payment attempt failed" },
  { time: "11:32:12", agent: "Policy Guard", event: "Automatic retry blocked" },
];

export const auditEvents: AuditEvent[] = [
  {
    id: "audit_001",
    actor: "raygo_agent",
    action: "Create Order",
    target: "intent_ai_setup_001",
    outcome: "success",
    timestamp: "2026-08-31T11:30:02Z",
    detail: "Buyer confirmed purchase. Policy check passed. Merchant auth confirmed.",
  },
  {
    id: "audit_002",
    actor: "raygo_agent",
    action: "Retry Payment",
    target: "pay_attempt_failed_01",
    outcome: "blocked",
    timestamp: "2026-08-31T11:32:12Z",
    detail: "Payment failed. Automatic retry blocked by Payment Retry policy. Duplicate-charge protection engaged.",
  },
  {
    id: "audit_003",
    actor: "raygo_agent",
    action: "Create Experiment",
    target: "exp_keyboard_stand",
    outcome: "success",
    timestamp: "2026-08-31T11:32:08Z",
    detail: "Merchant approved recommendation. Policy check passed. Experiment created.",
  },
];

export const aiCommerceReadinessScore = {
  overall: 82,
  summary: "Good readiness — 3 areas need attention.",
  breakdown: [
    { label: "Product Discoverability", score: 91 },
    { label: "Structured Product Data", score: 82 },
    { label: "Pricing Clarity", score: 94 },
    { label: "Inventory Confidence", score: 63 },
    { label: "Policy Clarity", score: 72 },
    { label: "Checkout Readiness", score: 76 },
  ],
  blockers: [
    "14 products have stale inventory data.",
    "37 products lack structured shipping information.",
    "8 products have ambiguous product attributes.",
  ],
  sampleProfile: {
    name: "ProBook 14",
    price: 62999,
    availability: "In stock",
    category: "Laptop",
    bestFor: "AI development, coding, college",
    specs: "16GB RAM, 512GB SSD, 14-inch display",
    aiDescription:
      "Portable performance laptop suitable for students and developers who need strong multitasking and development capability.",
  },
};

export const aiBuyerRecommendation = {
  name: "ProBook 14 Gen 6",
  price: 62999,
  fitPct: 98,
  specs: "Core Ultra 5 125H, 16GB LPDDR5x, 512GB PCIe Gen4, 1.35 kg",
  reasons: [
    { label: "Budget Constraint", detail: "₹7,001 under your ₹70,000 maximum." },
    { label: "Memory Requirements", detail: "16GB RAM is baseline for local AI development." },
    { label: "College Suitability", detail: "Lightweight with strong battery life." },
    { label: "Immediate Stock", detail: "Available for dispatch today." },
    { label: "AI Checkout Support", detail: "Eligible for automated discount application." },
  ],
  otherOptions: [
    { name: "Ryzen 7 Laptop", price: 65490 },
    { name: "RTX 3050 Laptop", price: 69990 },
  ],
};

export const paymentResult = {
  orderId: "#RGO-10482",
  amount: 68499,
  status: "Captured",
  environment: "Razorpay Test Mode",
  timeline: ["Intent received", "Products selected", "Order created", "Payment authorized", "Order confirmed"],
  decisionTimeSec: 2.4,
  recommendationConfidence: 92,
};

export const initializeSteps = [
  "Connecting merchant data",
  "Mapping product catalog",
  "Detecting revenue patterns",
  "Preparing AI Commerce profile",
  "Applying merchant policies",
];
