import asyncio

from app.db.indexes import ensure_indexes
from app.db.mongo import connect_to_mongo, get_db
from app.domain.constants import CATEGORIES
from app.domain.readiness import compute_readiness
from app.repositories.base import utcnow_iso
from app.repositories.registry import Repositories

MERCHANT_ID = "merchant_novatech"

MERCHANT = {
    "id": MERCHANT_ID,
    "name": "NovaTech Store",
    "category": "Consumer Electronics",
    "currency": "INR",
    "status": "active",
    "metrics": {
        "totalRevenue": 284620,
        "revenueGrowthPct": 18.7,
        "raygoInfluencedRevenue": 42800,
        "raygoLiftPct": 14.2,
        "activeOpportunities": 7,
        "aiCommerceReadiness": 82,
        "projectedOpportunityImpact": 40000,
    },
    "metadata": {"demo": True},
}

PRODUCTS = [
    # Core catalog (original items)
    {"id": "prod_probook_14", "name": "ProBook 14", "categoryId": "LAPTOP", "category": "Laptops", "price": 62999, "inventory": 42, "marginPct": 34, "brand": "NovaTech", "sku": "NT-LAP-001", "productType": "PHYSICAL", "active": True, "specs": {"cpu": "Intel Core Ultra 7", "ram": "32GB DDR5", "storage": "1TB NVMe"}, "shipping": {"weightKg": 1.35, "dimensionsCm": "31x22x1.6", "tier": "Standard Express"}},
    {"id": "prod_wireless_keyboard", "name": "Wireless Keyboard", "categoryId": "KEYBOARD", "category": "Keyboards", "price": 2499, "inventory": 86, "marginPct": 38, "brand": "NovaTech", "sku": "NT-KB-002", "productType": "PHYSICAL", "active": True, "specs": {"switch": "Red Linear", "connectivity": "Bluetooth / 2.4GHz", "backlight": "RGB"}, "shipping": {"weightKg": 0.65, "dimensionsCm": "32x12x3.5", "tier": "Standard"}},
    {"id": "prod_laptop_stand", "name": "Laptop Stand", "categoryId": "ACCESSORIES", "category": "Accessories", "price": 1799, "inventory": 12, "marginPct": 41, "brand": "NovaTech", "sku": "NT-ACC-003", "productType": "PHYSICAL", "active": True, "specs": {"material": "Anodized Aluminum", "maxSize": "17 inch", "adjustable": True}, "shipping": {"weightKg": 0.45, "dimensionsCm": "26x24x4", "tier": "Standard"}},
    {"id": "prod_ai_mouse_pro", "name": "AI Mouse Pro", "categoryId": "MOUSE", "category": "Mice", "price": 1299, "inventory": 64, "marginPct": 36, "brand": "NovaTech", "sku": "NT-MS-004", "productType": "PHYSICAL", "active": True, "specs": {"dpi": 4000, "sensor": "Optical Precision", "buttons": 6}, "shipping": {"weightKg": 0.12, "dimensionsCm": "11x6x3.8", "tier": "Standard"}},
    {"id": "prod_usb_c_dock", "name": "USB-C Dock", "categoryId": "DOCK", "category": "Docks", "price": 4999, "inventory": 20, "marginPct": 30, "brand": "NovaTech", "sku": "NT-DCK-005", "productType": "PHYSICAL", "active": True, "specs": {"powerDelivery": "100W", "ports": "Dual 4K HDMI, 3x USB 3.2, 1GbE", "hostInterface": "USB-C 3.2 Gen 2"}, "shipping": {"weightKg": 0.28, "dimensionsCm": "15x7x2", "tier": "Standard"}},
    {"id": "prod_headphones", "name": "NoiseCancel Headphones", "categoryId": "AUDIO", "category": "Audio", "price": 6499, "inventory": 17, "marginPct": 33, "brand": "NovaTech", "sku": "NT-AUD-006", "productType": "PHYSICAL", "active": True, "specs": {"anc": "Hybrid ANC 40dB", "batteryHours": 40, "driverSize": "40mm"}, "shipping": {"weightKg": 0.29, "dimensionsCm": "20x18x8", "tier": "Standard"}},
    {"id": "prod_4k_monitor", "name": "27 inch 4K Monitor", "categoryId": "MONITOR", "category": "Monitors", "price": 29999, "inventory": 9, "marginPct": 28, "brand": "NovaTech", "sku": "NT-MON-007", "productType": "PHYSICAL", "active": True, "specs": {"panel": "IPS 4K UHD", "colorGamut": "99% sRGB", "refreshRate": "60Hz", "hdr": "HDR400"}, "shipping": {"weightKg": 6.2, "dimensionsCm": "61x36x5", "tier": "Fragile Heavy"}},

    # CPUs (3 products)
    {"id": "prod_cpu_ryzen7", "name": "Ryzen 7 7800X3D", "categoryId": "CPU", "category": "Processors", "price": 38999, "inventory": 15, "marginPct": 26, "brand": "AMD", "sku": "NT-CPU-7800X", "productType": "PHYSICAL", "active": True, "specs": {"socket": "AM5", "cores": 8, "threads": 16, "tdp": "120W", "l3Cache": "96MB 3D V-Cache"}, "shipping": {"weightKg": 0.35, "dimensionsCm": "14x14x6", "tier": "Standard"}},
    {"id": "prod_cpu_i7_14700k", "name": "Intel Core i7-14700K", "categoryId": "CPU", "category": "Processors", "price": 34999, "inventory": 18, "marginPct": 28, "brand": "Intel", "sku": "NT-CPU-14700K", "productType": "PHYSICAL", "active": True, "specs": {"socket": "LGA1700", "cores": 20, "threads": 28, "tdp": "125W", "maxClock": "5.6 GHz"}, "shipping": {"weightKg": 0.38, "dimensionsCm": "14x14x6", "tier": "Standard"}},
    {"id": "prod_cpu_r5_7600x", "name": "AMD Ryzen 5 7600X", "categoryId": "CPU", "category": "Processors", "price": 19999, "inventory": 24, "marginPct": 29, "brand": "AMD", "sku": "NT-CPU-7600X", "productType": "PHYSICAL", "active": True, "specs": {"socket": "AM5", "cores": 6, "threads": 12, "tdp": "105W", "maxClock": "5.3 GHz"}, "shipping": {"weightKg": 0.32, "dimensionsCm": "14x14x6", "tier": "Standard"}},

    # GPUs (3 products)
    {"id": "prod_gpu_rtx_4070s", "name": "NVIDIA RTX 4070 Super 12GB", "categoryId": "GPU", "category": "Graphics Cards", "price": 58999, "inventory": 8, "marginPct": 25, "brand": "NVIDIA", "sku": "NT-GPU-4070S", "productType": "PHYSICAL", "active": True, "specs": {"vram": "12GB GDDR6X", "recommendedPsu": "650W", "interface": "PCIe 4.0 x16", "lengthMm": 242}, "shipping": {"weightKg": 1.25, "dimensionsCm": "26x12x4", "tier": "High Value Fragile"}},
    {"id": "prod_gpu_rx_7800xt", "name": "AMD Radeon RX 7800 XT 16GB", "categoryId": "GPU", "category": "Graphics Cards", "price": 51999, "inventory": 10, "marginPct": 27, "brand": "AMD", "sku": "NT-GPU-7800XT", "productType": "PHYSICAL", "active": True, "specs": {"vram": "16GB GDDR6", "recommendedPsu": "700W", "interface": "PCIe 4.0 x16", "lengthMm": 267}, "shipping": {"weightKg": 1.35, "dimensionsCm": "28x13x5", "tier": "High Value Fragile"}},
    {"id": "prod_gpu_rtx_4080s", "name": "NVIDIA RTX 4080 Super 16GB", "categoryId": "GPU", "category": "Graphics Cards", "price": 99999, "inventory": 5, "marginPct": 26, "brand": "NVIDIA", "sku": "NT-GPU-4080S", "productType": "PHYSICAL", "active": True, "specs": {"vram": "16GB GDDR6X", "recommendedPsu": "750W", "interface": "PCIe 4.0 x16", "lengthMm": 304}, "shipping": {"weightKg": 1.95, "dimensionsCm": "34x15x7", "tier": "High Value Fragile"}},

    # Motherboards (3 products)
    {"id": "prod_mb_b650e", "name": "ROG Strix B650E-F Gaming WiFi", "categoryId": "MOTHERBOARD", "category": "Motherboards", "price": 27999, "inventory": 14, "marginPct": 30, "brand": "ASUS", "sku": "NT-MB-B650E", "productType": "PHYSICAL", "active": True, "specs": {"socket": "AM5", "chipset": "AMD B650", "memorySlots": "4x DDR5", "pcieGen5": True, "formFactor": "ATX"}, "shipping": {"weightKg": 1.6, "dimensionsCm": "34x27x7", "tier": "Standard"}},
    {"id": "prod_mb_z790", "name": "Z790 AORUS Elite AX", "categoryId": "MOTHERBOARD", "category": "Motherboards", "price": 25999, "inventory": 12, "marginPct": 29, "brand": "Gigabyte", "sku": "NT-MB-Z790", "productType": "PHYSICAL", "active": True, "specs": {"socket": "LGA1700", "chipset": "Intel Z790", "memorySlots": "4x DDR5", "wifi6e": True, "formFactor": "ATX"}, "shipping": {"weightKg": 1.55, "dimensionsCm": "34x27x7", "tier": "Standard"}},
    {"id": "prod_mb_b650_tomahawk", "name": "MSI MAG B650 Tomahawk WiFi", "categoryId": "MOTHERBOARD", "category": "Motherboards", "price": 21999, "inventory": 16, "marginPct": 28, "brand": "MSI", "sku": "NT-MB-B650T", "productType": "PHYSICAL", "active": True, "specs": {"socket": "AM5", "chipset": "AMD B650", "memorySlots": "4x DDR5", "formFactor": "ATX"}, "shipping": {"weightKg": 1.5, "dimensionsCm": "34x27x7", "tier": "Standard"}},

    # PC Cases (3 products)
    {"id": "prod_case_airflow", "name": "RAYGO Airflow Case", "categoryId": "CASE", "category": "PC Cases", "price": 5999, "inventory": 20, "marginPct": 35, "brand": "RAYGO", "sku": "NT-CSE-001", "productType": "PHYSICAL", "active": True, "specs": {"formFactor": "Mid Tower", "motherboardSupport": "ATX, Micro-ATX, Mini-ITX", "gpuClearance": "380mm"}, "shipping": {"weightKg": 7.5, "dimensionsCm": "46x22x48", "tier": "Standard Heavy"}},
    {"id": "prod_case_titan", "name": "Titan ATX Gaming Case", "categoryId": "CASE", "category": "PC Cases", "price": 9999, "inventory": 11, "marginPct": 33, "brand": "Titan", "sku": "NT-CSE-002", "productType": "PHYSICAL", "active": True, "specs": {"formFactor": "Full Tower", "radiatorSupport": "Up to 420mm", "sidePanel": "Tempered Glass"}, "shipping": {"weightKg": 9.2, "dimensionsCm": "52x24x54", "tier": "Standard Heavy"}},
    {"id": "prod_case_fractal_north", "name": "Fractal Design North Case", "categoryId": "CASE", "category": "PC Cases", "price": 14999, "inventory": 8, "marginPct": 30, "brand": "Fractal", "sku": "NT-CSE-003", "productType": "PHYSICAL", "active": True, "specs": {"formFactor": "Mid Tower", "frontPanel": "Genuine Walnut", "gpuClearance": "355mm"}, "shipping": {"weightKg": 8.0, "dimensionsCm": "45x21x47", "tier": "Standard Heavy"}},

    # RAM (4 products)
    {"id": "prod_ram_ddr5_32gb", "name": "Corsair Vengeance 32GB (2x16GB) DDR5 6000MHz", "categoryId": "RAM", "category": "Memory", "price": 10499, "inventory": 28, "marginPct": 32, "brand": "Corsair", "sku": "NT-RAM-DDR5-32", "productType": "PHYSICAL", "active": True, "specs": {"type": "DDR5", "speed": "6000 MT/s", "latency": "CL36", "dimmCount": 2}, "shipping": {"weightKg": 0.15, "dimensionsCm": "16x9x1.5", "tier": "Standard"}},
    {"id": "prod_ram_gskill_32gb", "name": "G.Skill Trident Z5 RGB 32GB DDR5 6400MHz", "categoryId": "RAM", "category": "Memory", "price": 12999, "inventory": 16, "marginPct": 31, "brand": "G.Skill", "sku": "NT-RAM-TRIDENT-32", "productType": "PHYSICAL", "active": True, "specs": {"type": "DDR5", "speed": "6400 MT/s", "latency": "CL32", "rgb": True}, "shipping": {"weightKg": 0.18, "dimensionsCm": "16x9x1.8", "tier": "Standard"}},
    {"id": "prod_ram_kingston_16gb", "name": "Kingston Fury Beast 16GB DDR5 5600MHz", "categoryId": "RAM", "category": "Memory", "price": 5499, "inventory": 32, "marginPct": 34, "brand": "Kingston", "sku": "NT-RAM-FURY-16", "productType": "PHYSICAL", "active": True, "specs": {"type": "DDR5", "speed": "5600 MT/s", "latency": "CL40", "dimmCount": 1}, "shipping": {"weightKg": 0.09, "dimensionsCm": "16x9x1.2", "tier": "Standard"}},
    {"id": "prod_ram_crucial_64gb", "name": "Crucial Pro 64GB (2x32GB) DDR5 5600MHz", "categoryId": "RAM", "category": "Memory", "price": 19999, "inventory": 14, "marginPct": 28, "brand": "Crucial", "sku": "NT-RAM-CRUCIAL-64", "productType": "PHYSICAL", "active": True, "specs": {"type": "DDR5", "speed": "5600 MT/s", "latency": "CL46", "dimmCount": 2}, "shipping": {"weightKg": 0.16, "dimensionsCm": "16x9x1.5", "tier": "Standard"}},

    # SSD (4 products)
    {"id": "prod_ssd_990pro_2tb", "name": "Samsung 990 PRO 2TB NVMe M.2 SSD", "categoryId": "SSD", "category": "Solid State Drives", "price": 16999, "inventory": 22, "marginPct": 28, "brand": "Samsung", "sku": "NT-SSD-990P-2T", "productType": "PHYSICAL", "active": True, "specs": {"formFactor": "M.2 2280", "interface": "PCIe 4.0 NVMe", "readSpeed": "7450 MB/s", "writeSpeed": "6900 MB/s"}, "shipping": {"weightKg": 0.08, "dimensionsCm": "14x10x2", "tier": "Standard"}},
    {"id": "prod_ssd_sn850x_1tb", "name": "WD_BLACK SN850X 1TB NVMe SSD", "categoryId": "SSD", "category": "Solid State Drives", "price": 9499, "inventory": 30, "marginPct": 30, "brand": "Western Digital", "sku": "NT-SSD-SN850X-1T", "productType": "PHYSICAL", "active": True, "specs": {"formFactor": "M.2 2280", "interface": "PCIe 4.0 NVMe", "readSpeed": "7300 MB/s", "writeSpeed": "6300 MB/s"}, "shipping": {"weightKg": 0.08, "dimensionsCm": "14x10x2", "tier": "Standard"}},
    {"id": "prod_ssd_t700_2tb", "name": "Crucial T700 2TB PCIe Gen5 NVMe SSD", "categoryId": "SSD", "category": "Solid State Drives", "price": 28999, "inventory": 7, "marginPct": 26, "brand": "Crucial", "sku": "NT-SSD-T700-2T", "productType": "PHYSICAL", "active": True, "specs": {"formFactor": "M.2 2280", "interface": "PCIe 5.0 NVMe", "readSpeed": "12400 MB/s", "writeSpeed": "11800 MB/s"}, "shipping": {"weightKg": 0.12, "dimensionsCm": "14x10x3", "tier": "Standard"}},
    {"id": "prod_ssd_kc3000_2tb", "name": "Kingston KC3000 2TB NVMe M.2 SSD", "categoryId": "SSD", "category": "Solid State Drives", "price": 14999, "inventory": 18, "marginPct": 29, "brand": "Kingston", "sku": "NT-SSD-KC3000-2T", "productType": "PHYSICAL", "active": True, "specs": {"formFactor": "M.2 2280", "interface": "PCIe 4.0 NVMe", "readSpeed": "7000 MB/s", "writeSpeed": "7000 MB/s"}, "shipping": {"weightKg": 0.08, "dimensionsCm": "14x10x2", "tier": "Standard"}},

    # HDD (4 products)
    {"id": "prod_hdd_ironwolf_4tb", "name": "Seagate IronWolf 4TB NAS HDD", "categoryId": "HDD", "category": "Hard Disk Drives", "price": 9499, "inventory": 19, "marginPct": 30, "brand": "Seagate", "sku": "NT-HDD-IW-4TB", "productType": "PHYSICAL", "active": True, "specs": {"capacity": "4TB", "rpm": 5400, "cache": "256MB", "formFactor": "3.5 inch"}, "shipping": {"weightKg": 0.65, "dimensionsCm": "18x13x4", "tier": "Fragile Standard"}},
    {"id": "prod_hdd_wd_red_8tb", "name": "WD Red Plus 8TB NAS HDD", "categoryId": "HDD", "category": "Hard Disk Drives", "price": 18999, "inventory": 12, "marginPct": 28, "brand": "Western Digital", "sku": "NT-HDD-WDR-8TB", "productType": "PHYSICAL", "active": True, "specs": {"capacity": "8TB", "rpm": 5640, "cache": "256MB", "formFactor": "3.5 inch"}, "shipping": {"weightKg": 0.72, "dimensionsCm": "18x13x4", "tier": "Fragile Standard"}},
    {"id": "prod_hdd_barracuda_2tb", "name": "Seagate BarraCuda 2TB 7200RPM HDD", "categoryId": "HDD", "category": "Hard Disk Drives", "price": 4999, "inventory": 25, "marginPct": 33, "brand": "Seagate", "sku": "NT-HDD-BC-2TB", "productType": "PHYSICAL", "active": True, "specs": {"capacity": "2TB", "rpm": 7200, "cache": "256MB", "formFactor": "3.5 inch"}, "shipping": {"weightKg": 0.60, "dimensionsCm": "18x13x4", "tier": "Fragile Standard"}},
    {"id": "prod_hdd_toshiba_4tb", "name": "Toshiba N300 4TB NAS HDD", "categoryId": "HDD", "category": "Hard Disk Drives", "price": 8999, "inventory": 15, "marginPct": 31, "brand": "Toshiba", "sku": "NT-HDD-TOSH-4TB", "productType": "PHYSICAL", "active": True, "specs": {"capacity": "4TB", "rpm": 7200, "cache": "128MB", "formFactor": "3.5 inch"}, "shipping": {"weightKg": 0.65, "dimensionsCm": "18x13x4", "tier": "Fragile Standard"}},

    # RAM_SLOT Configuration entries (2 non-purchasable configuration items)
    {"id": "prod_cfg_ram_slot_a1", "name": "DDR5 Primary Channel Slot", "categoryId": "RAM_SLOT", "category": "RAM Slots", "price": 0, "inventory": 0, "marginPct": 0, "brand": "System", "sku": "CFG-SLOT-DDR5-A1", "productType": "CONFIGURATION", "active": False, "specs": {"channel": "Channel A", "supportedType": "DDR5", "maxCapacity": "64GB"}, "shipping": {"weightKg": 0, "dimensionsCm": "0x0x0", "tier": "None"}},
    {"id": "prod_cfg_ram_slot_b1", "name": "DDR5 Secondary Channel Slot", "categoryId": "RAM_SLOT", "category": "RAM Slots", "price": 0, "inventory": 0, "marginPct": 0, "brand": "System", "sku": "CFG-SLOT-DDR5-B1", "productType": "CONFIGURATION", "active": False, "specs": {"channel": "Channel B", "supportedType": "DDR5", "maxCapacity": "64GB"}, "shipping": {"weightKg": 0, "dimensionsCm": "0x0x0", "tier": "None"}},
]

OPPORTUNITIES = [
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
        "eligibleJourneys": 1842,
        "evidence": [
            "Observed buyers of Wireless Keyboard often view Laptop Stand.",
            "Detected under-used cross-sell surface in checkout journeys.",
            "Hypothesized bundle remains above merchant margin floor.",
        ],
        "recommendedAction": "Create a 10% Keyboard + Laptop Stand bundle experiment.",
    },
    {
        "id": "opp_probook_bundle",
        "title": "Bundle opportunity: ProBook 14 -> USB-C Dock",
        "shortTitle": "ProBook Bundle",
        "type": "bundle",
        "expectedMonthlyImpact": 12200,
        "confidence": 91,
        "risk": "low",
        "status": "ready_for_review",
        "currentAttachRate": 6.5,
        "projectedAttachRate": 11.2,
        "targetSegment": "New Laptop Buyers",
        "eligibleJourneys": 980,
        "evidence": [
            "Observed ProBook 14 buyers return within 48 hours to search docking accessories.",
            "Detected USB-C Dock detail-view spikes after ProBook 14 purchases.",
        ],
        "recommendedAction": "Create a bundled USB-C Dock offer for ProBook 14 buyers.",
    },
    {
        "id": "opp_recovery_campaign",
        "title": "Recovery opportunity: Abandoned AI Mouse Pro carts",
        "shortTitle": "Recovery Campaign",
        "type": "retention",
        "expectedMonthlyImpact": 9400,
        "confidence": 78,
        "risk": "medium",
        "status": "ready_for_review",
        "currentAttachRate": 2.2,
        "projectedAttachRate": 4.6,
        "targetSegment": "Cart Abandoners",
        "eligibleJourneys": 611,
        "evidence": [
            "Observed AI Mouse Pro has the highest cart-abandonment rate in the catalog.",
            "Detected abandonment concentrates at the final pricing-review step.",
        ],
        "recommendedAction": "Send a targeted recovery nudge to cart abandoners.",
    },
]
# Round out activeOpportunities=7 with lighter-weight detected opportunities.
_EXTRA_OPPS = [
    ("opp_headphones_upsell", "Upsell opportunity: Headphones premium tier", "Headphones Upsell", "pricing", 6100, 74, "medium", "Frequent Buyers", 402),
    ("opp_monitor_bundle", "Bundle opportunity: 4K Monitor -> USB-C Dock", "Monitor Bundle", "bundle", 5400, 69, "medium", "Desk Setup Buyers", 310),
    ("opp_mouse_stand_pairing", "Cross-sell opportunity: AI Mouse Pro -> Laptop Stand", "Mouse + Stand", "cross_sell", 3800, 71, "low", "Remote Workers", 588),
    ("opp_seasonal_reactivation", "Retention opportunity: Seasonal buyer reactivation", "Seasonal Reactivation", "retention", 2600, 63, "high", "Lapsed Buyers", 240),
]
for opp_id, title, short, typ, impact, conf, risk, segment, journeys in _EXTRA_OPPS:
    OPPORTUNITIES.append(
        {
            "id": opp_id,
            "title": title,
            "shortTitle": short,
            "type": typ,
            "expectedMonthlyImpact": impact,
            "confidence": conf,
            "risk": risk,
            "status": "detected",
            "currentAttachRate": 0.0,
            "projectedAttachRate": 0.0,
            "targetSegment": segment,
            "eligibleJourneys": journeys,
            "evidence": [],
            "recommendedAction": "",
        }
    )

EXPERIMENT = {
    "id": "exp_keyboard_stand",
    "opportunityId": "opp_keyboard_stand",
    "name": "Keyboard + Laptop Stand",
    "status": "running",
    "hypothesis": (
        "Bundling a Laptop Stand with Wireless Keyboard purchases will increase basket "
        "conversion without reducing merchant margin below policy."
    ),
    "controlConversion": 6.2,
    "variantConversion": 8.9,
    "conversionUplift": 43.5,
    "revenueUplift": 23.4,
    "aovUplift": 8.7,
    "confidence": 94,
    "recommendation": "scale_variant",
    "decisionReason": "Variant performance exceeds control while remaining within the merchant's margin policy.",
    "metadata": {"discountPct": 10},
}

POLICIES = [
    {"id": "policy_discount_limit", "name": "Discount Limit", "limit": "20%", "status": "active", "ruleType": "discount_max_pct", "value": 20, "enforcement": "block"},
    {"id": "policy_margin_floor", "name": "Margin Floor", "limit": "25%", "status": "active", "ruleType": "margin_min_pct", "value": 25, "enforcement": "block"},
    {"id": "policy_daily_budget", "name": "Daily Budget", "limit": "₹10,000", "status": "review", "ruleType": "daily_budget", "value": 10000, "enforcement": "warn"},
    {"id": "policy_auto_execution", "name": "Auto Execution", "limit": "OFF", "status": "paused", "ruleType": "auto_execution", "value": False, "enforcement": "block"},
    {"id": "policy_merchant_auth", "name": "Merchant Auth", "limit": "REQUIRED", "status": "enforced", "ruleType": "merchant_auth", "value": True, "enforcement": "require_approval"},
    {"id": "policy_payment_retry", "name": "Payment Retry", "limit": "BLOCKED", "status": "strict", "ruleType": "payment_retry", "value": False, "enforcement": "block"},
]

ACTION_MATRIX = [
    {"actionType": "Create Bundle", "canPropose": True, "canExecute": True, "approvalRequirement": "approval required"},
    {"actionType": "Discount >20%", "canPropose": True, "canExecute": False, "approvalRequirement": "blocked"},
    {"actionType": "Create Campaign", "canPropose": True, "canExecute": True, "approvalRequirement": "approval required"},
    {"actionType": "Payment Retry", "canPropose": True, "canExecute": False, "approvalRequirement": "blocked"},
    {"actionType": "Refund", "canPropose": True, "canExecute": False, "approvalRequirement": "approval required"},
]

AGENT_STATUS = [
    {"name": "RAYGO Coordinator", "status": "Active"},
    {"name": "Revenue Intelligence", "status": "Active"},
    {"name": "AI Commerce", "status": "Active"},
    {"name": "Growth Strategist", "status": "Active"},
    {"name": "Experiment Agent", "status": "Running"},
    {"name": "Policy Guard", "status": "Active"},
    {"name": "Payment Agent", "status": "Ready"},
    {"name": "Approval Gateway", "status": "Ready"},
]

AGENT_ACTIVITY = [
    ("agent_evt_001", "11:32:04", "Revenue Intelligence", "Detected cross-sell opportunity", "audit_opp_detected_001"),
    ("agent_evt_002", "11:32:05", "Growth Strategist", "Generated experiment hypothesis", "audit_hypothesis_001"),
    ("agent_evt_003", "11:32:06", "Policy Guard", "Policy check passed", "audit_policy_001"),
    ("agent_evt_004", "11:32:07", "Approval Gateway", "Merchant approval received", "audit_approval_001"),
    ("agent_evt_005", "11:32:08", "Experiment Agent", "Experiment created", "audit_experiment_001"),
    ("agent_evt_006", "11:32:12", "Payment Agent", "Payment attempt failed", "audit_payment_failed_001"),
    ("agent_evt_007", "11:32:12", "Policy Guard", "Automatic retry blocked", "audit_001"),
]

BASKET = {
    "id": "basket_ai_setup_001",
    "merchantId": MERCHANT_ID,
    "buyerIntentId": "buyer_intent_ai_setup_001",
    "items": [
        {"productId": "prod_probook_14", "name": "ProBook 14", "quantity": 1, "unitPrice": 62999},
        {"productId": "prod_usb_c_dock", "name": "USB-C Dock", "quantity": 1, "unitPrice": 4999},
        {"productId": "prod_laptop_stand", "name": "Laptop Stand", "quantity": 1, "unitPrice": 1799},
    ],
    "subtotal": 69797,
    "bundleDiscount": 1298,
    "total": 68499,
    "currency": "INR",
    "metadata": {"buyerRequest": "I need a laptop setup for AI development and college under ₹70,000."},
}

ORDER_INTENT = {
    "id": "intent_ai_setup_001",
    "merchantId": MERCHANT_ID,
    "displayOrderId": "#RGO-10482",
    "buyerRequest": "I need a laptop setup for AI development and college under ₹70,000.",
    "whyPrepared": "RAYGO matched buyer intent to an AI-readable catalog and stayed under budget.",
    "customerName": "AI Buyer Demo",
    "source": "AI Buyer",
    "items": BASKET["items"],
    "subtotal": BASKET["subtotal"],
    "bundleDiscount": BASKET["bundleDiscount"],
    "taxesAndFeesLabel": "Calculated",
    "total": BASKET["total"],
    "currency": "INR",
    "status": "review",
    "paymentStatus": "not_started",
    "authorizationRequired": True,
    "authorizationCopy": "RAYGO will not execute payment until you confirm this purchase.",
    "metadata": {"decisionTimeSec": 2.4, "recommendationConfidence": 92},
}


async def seed(db=None) -> None:
    db = db or get_db()
    repos = Repositories(db)

    await repos.merchants.upsert(dict(MERCHANT))
    for category in CATEGORIES:
        await repos.categories.upsert(dict(category))
    for product in PRODUCTS:
        computed = compute_readiness(product)
        full_product = {**product, **computed, "merchantId": MERCHANT_ID, "currency": "INR"}
        await repos.products.upsert(full_product)
    for opp in OPPORTUNITIES:
        await repos.opportunities.upsert({**opp, "merchantId": MERCHANT_ID})
    await repos.experiments.upsert({**EXPERIMENT, "merchantId": MERCHANT_ID})
    for policy in POLICIES:
        await repos.policies.upsert({**policy, "merchantId": MERCHANT_ID})
    await repos.baskets.upsert(dict(BASKET))
    await repos.order_intents.upsert(dict(ORDER_INTENT))

    for evt_id, time_label, agent, message, audit_event_id in AGENT_ACTIVITY:
        await repos.agent_activity.upsert(
            {
                "id": evt_id,
                "merchantId": MERCHANT_ID,
                "time": time_label,
                "timestamp": utcnow_iso(),
                "agent": agent,
                "message": message,
                "auditEventId": audit_event_id,
            }
        )

    await repos.audit_events.upsert(
        {
            "id": "audit_demo_initialized",
            "merchantId": MERCHANT_ID,
            "timestamp": utcnow_iso(),
            "agent": "System",
            "action": "Initialize Demo",
            "reason": "Seed script populated NovaTech Store demo data.",
            "policy": "Passed",
            "approval": "N/A",
            "outcome": "Success",
            "severity": "info",
            "correlationIds": {},
            "details": {"decisionSummary": "Demo data seeded deterministically."},
            "metadata": {},
        }
    )


async def main() -> None:
    connect_to_mongo()
    db = get_db()
    await ensure_indexes(db)
    await seed(db)
    print("Seed complete.")


if __name__ == "__main__":
    asyncio.run(main())
