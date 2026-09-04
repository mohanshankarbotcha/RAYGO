MERCHANT_ID = "merchant_novatech"
DEMO_APPROVED_BY = "merchant_demo_user"

POLICY_DISCOUNT_LIMIT = "policy_discount_limit"
POLICY_MARGIN_FLOOR = "policy_margin_floor"
POLICY_DAILY_BUDGET = "policy_daily_budget"
POLICY_AUTO_EXECUTION = "policy_auto_execution"
POLICY_MERCHANT_AUTH = "policy_merchant_auth"
POLICY_PAYMENT_RETRY = "policy_payment_retry"

DISCOUNT_MAX_PCT = 20
MARGIN_MIN_PCT = 25
DAILY_BUDGET_LIMIT = 10000

AGENT_REVENUE_INTELLIGENCE = "Revenue Intelligence"
AGENT_AI_COMMERCE = "AI Commerce"
AGENT_GROWTH_STRATEGIST = "Growth Strategist"
AGENT_EXPERIMENT = "Experiment Agent"
AGENT_POLICY_GUARD = "Policy Guard"
AGENT_PAYMENT = "Payment Agent"
AGENT_APPROVAL_GATEWAY = "Approval Gateway"
AGENT_SYSTEM = "System"

OUTCOME_PASSED = "passed"
OUTCOME_REQUIRES_APPROVAL = "requires_approval"
OUTCOME_BLOCKED = "blocked"

SEVERITY_INFO = "info"
SEVERITY_WARNING = "warning"
SEVERITY_CRITICAL = "critical"

AUDIT_OUTCOME_SUCCESS = "Success"
AUDIT_OUTCOME_PREVENTED = "Prevented"
AUDIT_OUTCOME_FAILED = "Failed"

CATEGORIES = [
    {"id": "LAPTOP", "name": "Laptops", "description": "High-performance laptops & notebooks"},
    {"id": "CPU", "name": "Processors", "description": "Desktop & workstation CPUs"},
    {"id": "GPU", "name": "Graphics Cards", "description": "Dedicated GPUs for gaming & AI"},
    {"id": "MOTHERBOARD", "name": "Motherboards", "description": "ATX, Micro-ATX, Mini-ITX system boards"},
    {"id": "RAM", "name": "Memory", "description": "DDR4 & DDR5 system RAM"},
    {"id": "RAM_SLOT", "name": "RAM Slots", "description": "System motherboard memory slots (Configuration)"},
    {"id": "SSD", "name": "Solid State Drives", "description": "NVMe M.2 & SATA high-speed storage"},
    {"id": "HDD", "name": "Hard Disk Drives", "description": "Bulk storage & NAS hard drives"},
    {"id": "CASE", "name": "PC Cases", "description": "Chassis & PC enclosures"},
    {"id": "MONITOR", "name": "Monitors", "description": "Displays & visual panels"},
    {"id": "KEYBOARD", "name": "Keyboards", "description": "Mechanical & wireless keyboards"},
    {"id": "MOUSE", "name": "Mice", "description": "Gaming & precision mice"},
    {"id": "AUDIO", "name": "Audio", "description": "Headphones, speakers & headsets"},
    {"id": "DOCK", "name": "Docks & Hubs", "description": "Thunderbolt & USB-C docking stations"},
    {"id": "ACCESSORIES", "name": "Accessories", "description": "Stands, cables & workspace accessories"},
]

CATEGORY_MAP = {c["id"]: c for c in CATEGORIES}
VALID_CATEGORY_IDS = set(CATEGORY_MAP.keys())

