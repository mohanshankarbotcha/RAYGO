-- =============================================================================
-- RAYGO Supabase Seed Data Migration (002_seed_data.sql)
-- Complete seed data for NovaTech Store baseline & expanded hardware catalog
-- =============================================================================

-- 1. MERCHANT
INSERT INTO merchants (id, name, email, currency, timezone, status)
VALUES ('merchant_novatech', 'NovaTech Store', 'admin@novatech.store', 'INR', 'Asia/Kolkata', 'active')
ON CONFLICT (id) DO NOTHING;

-- 2. STORE
INSERT INTO stores (id, merchant_id, name, category, estimated_revenue_range, product_count, status)
VALUES ('store_novatech_main', 'merchant_novatech', 'NovaTech Store', 'Electronics & Hardware', '₹1M - ₹5M / month', 15, 'active')
ON CONFLICT (id) DO NOTHING;

-- 3. CATEGORIES
INSERT INTO categories (id, name, slug, description, parent_id) VALUES
('cat_laptops', 'Laptops & Workstations', 'laptops', 'High performance laptops and mobile workstations', NULL),
('cat_cpus', 'Processors (CPUs)', 'cpus', 'Desktop and workstation processors', NULL),
('cat_gpus', 'Graphics Cards (GPUs)', 'gpus', 'Dedicated graphics cards for gaming and AI workloads', NULL),
('cat_motherboards', 'Motherboards', 'motherboards', 'Desktop and workstation motherboards', NULL),
('cat_memory', 'RAM & Memory', 'memory', 'DDR4 and DDR5 memory modules', NULL),
('cat_storage', 'Storage (SSDs & HDDs)', 'storage', 'NVMe SSDs, SATA drives, and enterprise storage', NULL),
('cat_monitors', 'Monitors & Displays', 'monitors', 'High refresh rate and color-accurate displays', NULL),
('cat_keyboards', 'Keyboards', 'keyboards', 'Mechanical and wireless productivity keyboards', NULL),
('cat_mice', 'Mice & Pointers', 'mice', 'Ergonomic and AI-assisted productivity mice', NULL),
('cat_docks', 'Docks & Hubs', 'docks', 'Thunderbolt and USB-C multiport docking stations', NULL),
('cat_audio', 'Audio & Acoustics', 'audio', 'Active noise cancelling headphones and microphones', NULL),
('cat_accessories', 'Accessories & Stands', 'accessories', 'Ergonomic aluminum stands and cable management', NULL)
ON CONFLICT (id) DO NOTHING;

-- 4. PRODUCTS
INSERT INTO products (id, store_id, category_id, sku, name, slug, description, brand, price, currency, status, ai_readiness_score, metadata) VALUES
('prod_probook_14', 'store_novatech_main', 'cat_laptops', 'NT-LAP-001', 'ProBook 14 Gen 6', 'probook-14-gen-6', 'Flagship AI developer laptop with Intel Core Ultra 7, 32GB RAM, 1TB NVMe SSD', 'NovaTech', 62999.00, 'INR', 'active', 94, '{"cpu":"Intel Core Ultra 7","ram":"32GB DDR5","storage":"1TB NVMe","ports":["Thunderbolt 4","USB-C","HDMI 2.1"],"weightKg":1.35}'::jsonb),
('prod_wireless_keyboard', 'store_novatech_main', 'cat_keyboards', 'NT-ACC-002', 'Wireless Mechanical Keyboard', 'wireless-mechanical-keyboard', 'Compact 75% wireless mechanical keyboard with hot-swappable switches and RGB', 'NovaTech', 2499.00, 'INR', 'active', 89, '{"connectivity":["Bluetooth 5.3","2.4GHz","USB-C"],"batteryHours":200,"switchType":"Linear Red"}'::jsonb),
('prod_laptop_stand', 'store_novatech_main', 'cat_accessories', 'NT-ACC-003', 'Ergonomic Aluminum Laptop Stand', 'ergonomic-aluminum-laptop-stand', 'Adjustable anodized aluminum stand supporting up to 17-inch laptops with cooling vents', 'NovaTech', 1799.00, 'INR', 'active', 81, '{"material":"Anodized Aluminum","maxLaptopSizeInch":17,"foldable":true}'::jsonb),
('prod_ai_mouse', 'store_novatech_main', 'cat_mice', 'NT-ACC-004', 'AI Mouse Pro', 'ai-mouse-pro', 'Ergonomic wireless mouse with dedicated AI productivity gesture keys and precision sensor', 'NovaTech', 1299.00, 'INR', 'active', 76, '{"dpi":4000,"connectivity":["Bluetooth","2.4GHz"],"gestureSupport":true}'::jsonb),
('prod_usbc_dock', 'store_novatech_main', 'cat_docks', 'NT-ACC-005', 'Thunderbolt 4 Multiport USB-C Dock', 'thunderbolt-4-usbc-dock', '10-in-1 100W Power Delivery docking station with dual 4K display output and Gigabit Ethernet', 'NovaTech', 4999.00, 'INR', 'active', 84, '{"powerDeliveryWatt":100,"displayOutputs":["2x DisplayPort","1x HDMI 2.1"],"ethernetGbps":1}'::jsonb),
('prod_headphones', 'store_novatech_main', 'cat_audio', 'NT-AUD-006', 'NoiseCancel Wireless Headphones Pro', 'noisecancel-wireless-headphones-pro', 'Hybrid active noise cancelling wireless headphones with 40-hour battery and spatial audio', 'NovaTech', 6499.00, 'INR', 'active', 78, '{"ancMode":"Hybrid ANC","batteryHours":40,"driverMm":40}'::jsonb),
('prod_monitor_4k', 'store_novatech_main', 'cat_monitors', 'NT-MON-007', '27-inch 4K UHD IPS Monitor', '27-inch-4k-uhd-monitor', 'Factory color-calibrated 4K UHD IPS display with USB-C 90W charging and HDR400', 'NovaTech', 29999.00, 'INR', 'active', 72, '{"resolution":"3840x2160","panel":"IPS","refreshHz":60,"colorGamut":"99% sRGB"}'::jsonb),
('prod_cpu_intel_i7', 'store_novatech_main', 'cat_cpus', 'NT-CPU-008', 'Intel Core i7-14700K', 'intel-core-i7-14700k', '20-core desktop processor up to 5.6 GHz, LGA1700 socket', 'Intel', 38999.00, 'INR', 'active', 92, '{"socket":"LGA1700","cores":20,"tdpWatt":125,"integratedGraphics":true}'::jsonb),
('prod_gpu_rtx_4070', 'store_novatech_main', 'cat_gpus', 'NT-GPU-009', 'NVIDIA GeForce RTX 4070 Super 12GB', 'rtx-4070-super-12gb', 'High performance AI and graphics acceleration with 12GB GDDR6X VRAM', 'NVIDIA', 58999.00, 'INR', 'active', 95, '{"vramGb":12,"recommendedPsuWatt":650,"pcieVersion":"PCIe 4.0 x16"}'::jsonb),
('prod_ram_ddr5_32gb', 'store_novatech_main', 'cat_memory', 'NT-RAM-010', 'Corsair Vengeance 32GB (2x16GB) DDR5 6000MHz', 'corsair-vengeance-32gb-ddr5-6000', 'High-speed dual-channel DDR5 desktop memory kit', 'Corsair', 10499.00, 'INR', 'active', 90, '{"memoryType":"DDR5","capacityGb":32,"speedMhz":6000,"latency":"CL36"}'::jsonb),
('prod_ssd_nvme_2tb', 'store_novatech_main', 'cat_storage', 'NT-SSD-011', 'Samsung 990 PRO 2TB NVMe M.2 SSD', 'samsung-990-pro-2tb-nvme', 'PCIe 4.0 NVMe SSD with read speeds up to 7450 MB/s', 'Samsung', 16999.00, 'INR', 'active', 93, '{"formFactor":"M.2 2280","interface":"PCIe 4.0 x4","readSpeedMb":7450}'::jsonb)
ON CONFLICT (id) DO NOTHING;

-- 5. INVENTORY
INSERT INTO inventory (id, product_id, quantity, reserved_quantity, available_quantity, reorder_threshold) VALUES
('inv_probook_14', 'prod_probook_14', 42, 0, 42, 5),
('inv_wireless_keyboard', 'prod_wireless_keyboard', 86, 0, 86, 10),
('inv_laptop_stand', 'prod_laptop_stand', 12, 0, 12, 5),
('inv_ai_mouse', 'prod_ai_mouse', 64, 0, 64, 10),
('inv_usbc_dock', 'prod_usbc_dock', 20, 0, 20, 5),
('inv_headphones', 'prod_headphones', 17, 0, 17, 5),
('inv_monitor_4k', 'prod_monitor_4k', 9, 0, 9, 3),
('inv_cpu_intel_i7', 'prod_cpu_intel_i7', 15, 0, 15, 4),
('inv_gpu_rtx_4070', 'prod_gpu_rtx_4070', 8, 0, 8, 2),
('inv_ram_ddr5_32gb', 'prod_ram_ddr5_32gb', 28, 0, 28, 6),
('inv_ssd_nvme_2tb', 'prod_ssd_nvme_2tb', 22, 0, 22, 5)
ON CONFLICT (id) DO NOTHING;

-- 6. PRODUCT RELATIONSHIPS & COMPATIBILITY
INSERT INTO product_relationships (id, source_product_id, target_product_id, relationship_type, compatibility_score, reason) VALUES
('rel_lap_stand', 'prod_probook_14', 'prod_laptop_stand', 'bundle', 0.96, 'High affinity bundle: 38% of laptop buyers add an ergonomic aluminum stand within 14 days'),
('rel_lap_dock', 'prod_probook_14', 'prod_usbc_dock', 'recommended', 0.94, 'Thunderbolt 4 100W PD dock allows full single-cable desktop workstation connectivity'),
('rel_lap_kb', 'prod_probook_14', 'prod_wireless_keyboard', 'bundle', 0.91, 'Wireless keyboard recommended for desktop docked setup'),
('rel_cpu_ram', 'prod_cpu_intel_i7', 'prod_ram_ddr5_32gb', 'compatible', 1.00, 'Intel 14th Gen memory controller fully supports DDR5 6000MHz memory modules'),
('rel_cpu_gpu', 'prod_cpu_intel_i7', 'prod_gpu_rtx_4070', 'recommended', 0.98, 'Balanced pairing for high-throughput AI development and gaming without CPU bottleneck')
ON CONFLICT (id) DO NOTHING;

-- 7. POLICIES (Hard safety guardrails)
INSERT INTO policies (id, store_id, name, description, category, policy_type, status, is_hard_locked, rules) VALUES
('pol_max_discount', 'store_novatech_main', 'Maximum Discount Rule', 'Caps promotional and dynamic AI discounts at 20%', 'financial', 'discount_cap', 'Active', true, '{"maxDiscountPercent": 20}'::jsonb),
('pol_min_margin', 'store_novatech_main', 'Minimum Profit Margin', 'Ensures gross margins do not drop below 25% across all SKUs', 'financial', 'margin_floor', 'Active', true, '{"minMarginPercent": 25}'::jsonb),
('pol_payment_retry', 'store_novatech_main', 'Payment Retry Hard Lock', 'Strictly prohibits automated re-attempts on failed transactions without merchant/user re-authorization', 'payment', 'retry_lock', 'Active', true, '{"allowAutoRetry": false}'::jsonb),
('pol_approval_gate', 'store_novatech_main', 'Explicit Merchant Approval', 'Requires human authorization for any experiment budget scaling or catalog restructuring', 'governance', 'approval_gate', 'Active', false, '{"requireApprovalForScale": true}'::jsonb)
ON CONFLICT (id) DO NOTHING;

-- 8. OPPORTUNITIES
INSERT INTO opportunities (id, store_id, type, title, description, status, confidence, expected_impact, evidence, target_segment, recommendation, policy_status, approval_status) VALUES
('opp_keyboard_stand', 'store_novatech_main', 'bundle', 'Bundle Laptop Stand with Wireless Keyboard', 'Customers purchasing mechanical keyboards frequently browse laptop stands. Proposing an automated 10% bundle incentive.', 'Active', 0.91, '{"revenueUplift": 420000, "conversionLift": 43.5, "aovLift": 8.7}'::jsonb, '[{"metric": "Cart Correlation", "value": "38%"}, {"metric": "Historical Attach Rate", "value": "12%"}]'::jsonb, 'Desktop / Laptop Hybrid Workers', '{"bundleDiscountPercent": 10, "targetProductIds": ["prod_wireless_keyboard", "prod_laptop_stand"]}'::jsonb, 'Passed', 'Pending')
ON CONFLICT (id) DO NOTHING;

-- 9. EXPERIMENTS
INSERT INTO experiments (id, store_id, opportunity_id, name, status, control_definition, variant_definition, conversion_uplift, revenue_uplift, aov_uplift, statistical_confidence) VALUES
('exp_keyboard_stand', 'store_novatech_main', 'opp_keyboard_stand', 'Keyboard + Stand Dynamic Bundle', 'Running', '{"discount": 0, "layout": "standard"}'::jsonb, '{"discount": 10, "layout": "bundle_card"}'::jsonb, 43.5, 23.4, 8.7, 0.94)
ON CONFLICT (id) DO NOTHING;
