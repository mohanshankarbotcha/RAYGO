-- =============================================================================
-- RAYGO Supabase Initial Schema Migration (001_initial_schema.sql)
-- Product: RAYGO — Autonomous Revenue Intelligence & Agentic Commerce
-- Tables: 18 relational tables with constraints, indexes, and RLS policies
-- =============================================================================

-- Enable UUID extension if not enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. MERCHANTS
CREATE TABLE IF NOT EXISTS merchants (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    currency VARCHAR(10) NOT NULL DEFAULT 'INR',
    timezone VARCHAR(50) NOT NULL DEFAULT 'Asia/Kolkata',
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. STORES
CREATE TABLE IF NOT EXISTS stores (
    id VARCHAR(64) PRIMARY KEY,
    merchant_id VARCHAR(64) NOT NULL REFERENCES merchants(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    estimated_revenue_range VARCHAR(100),
    product_count INTEGER NOT NULL DEFAULT 0,
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. CATEGORIES (Supports hierarchical categories)
CREATE TABLE IF NOT EXISTS categories (
    id VARCHAR(64) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    parent_id VARCHAR(64) REFERENCES categories(id) ON DELETE SET NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. PRODUCTS
CREATE TABLE IF NOT EXISTS products (
    id VARCHAR(64) PRIMARY KEY,
    store_id VARCHAR(64) NOT NULL REFERENCES stores(id) ON DELETE CASCADE,
    category_id VARCHAR(64) REFERENCES categories(id) ON DELETE SET NULL,
    sku VARCHAR(100) NOT NULL,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL,
    description TEXT,
    brand VARCHAR(100),
    price NUMERIC(12, 2) NOT NULL CHECK (price >= 0),
    currency VARCHAR(10) NOT NULL DEFAULT 'INR',
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    ai_readiness_score INTEGER NOT NULL DEFAULT 80 CHECK (ai_readiness_score BETWEEN 0 AND 100),
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (store_id, sku)
);

-- 5. INVENTORY
CREATE TABLE IF NOT EXISTS inventory (
    id VARCHAR(64) PRIMARY KEY,
    product_id VARCHAR(64) NOT NULL UNIQUE REFERENCES products(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    reserved_quantity INTEGER NOT NULL DEFAULT 0 CHECK (reserved_quantity >= 0),
    available_quantity INTEGER NOT NULL DEFAULT 0 CHECK (available_quantity >= 0),
    reorder_threshold INTEGER NOT NULL DEFAULT 5 CHECK (reorder_threshold >= 0),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT valid_inventory_calc CHECK (quantity = available_quantity + reserved_quantity)
);

-- 6. PRODUCT RELATIONSHIPS & COMPATIBILITY
CREATE TABLE IF NOT EXISTS product_relationships (
    id VARCHAR(64) PRIMARY KEY,
    source_product_id VARCHAR(64) NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    target_product_id VARCHAR(64) NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    relationship_type VARCHAR(50) NOT NULL CHECK (
        relationship_type IN ('compatible', 'recommended', 'requires', 'incompatible', 'upgrade', 'bundle', 'alternative')
    ),
    compatibility_score NUMERIC(4, 2) NOT NULL DEFAULT 1.0 CHECK (compatibility_score BETWEEN 0 AND 1),
    reason TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (source_product_id, target_product_id, relationship_type)
);

-- 7. ORDERS
CREATE TABLE IF NOT EXISTS orders (
    id VARCHAR(64) PRIMARY KEY,
    store_id VARCHAR(64) NOT NULL REFERENCES stores(id) ON DELETE CASCADE,
    order_number VARCHAR(100) NOT NULL UNIQUE,
    customer_id VARCHAR(64),
    status VARCHAR(50) NOT NULL DEFAULT 'draft' CHECK (
        status IN ('draft', 'pending_payment', 'payment_processing', 'paid', 'payment_failed', 'payment_uncertain', 'cancelled', 'fulfilled')
    ),
    currency VARCHAR(10) NOT NULL DEFAULT 'INR',
    subtotal NUMERIC(12, 2) NOT NULL DEFAULT 0 CHECK (subtotal >= 0),
    discount NUMERIC(12, 2) NOT NULL DEFAULT 0 CHECK (discount >= 0),
    tax NUMERIC(12, 2) NOT NULL DEFAULT 0 CHECK (tax >= 0),
    shipping NUMERIC(12, 2) NOT NULL DEFAULT 0 CHECK (shipping >= 0),
    total NUMERIC(12, 2) NOT NULL DEFAULT 0 CHECK (total >= 0),
    razorpay_order_id VARCHAR(100),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 8. ORDER ITEMS (Immutable snapshots)
CREATE TABLE IF NOT EXISTS order_items (
    id VARCHAR(64) PRIMARY KEY,
    order_id VARCHAR(64) NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id VARCHAR(64) NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
    sku_snapshot VARCHAR(100) NOT NULL,
    name_snapshot VARCHAR(255) NOT NULL,
    unit_price_snapshot NUMERIC(12, 2) NOT NULL CHECK (unit_price_snapshot >= 0),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    subtotal NUMERIC(12, 2) NOT NULL CHECK (subtotal >= 0),
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 9. PAYMENTS
CREATE TABLE IF NOT EXISTS payments (
    id VARCHAR(64) PRIMARY KEY,
    order_id VARCHAR(64) NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    provider VARCHAR(50) NOT NULL DEFAULT 'razorpay',
    provider_order_id VARCHAR(100),
    provider_payment_id VARCHAR(100),
    status VARCHAR(50) NOT NULL DEFAULT 'created' CHECK (
        status IN ('created', 'pending', 'authorized', 'captured', 'failed', 'cancelled', 'uncertain', 'refunded')
    ),
    amount NUMERIC(12, 2) NOT NULL CHECK (amount >= 0),
    currency VARCHAR(10) NOT NULL DEFAULT 'INR',
    signature_verified BOOLEAN NOT NULL DEFAULT FALSE,
    failure_code VARCHAR(100),
    failure_reason TEXT,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 10. PAYMENT EVENTS (Idempotent webhook ledger)
CREATE TABLE IF NOT EXISTS payment_events (
    id VARCHAR(64) PRIMARY KEY,
    payment_id VARCHAR(64) REFERENCES payments(id) ON DELETE SET NULL,
    event_type VARCHAR(100) NOT NULL,
    provider_event_id VARCHAR(100) UNIQUE,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    processed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 11. OPPORTUNITIES (Phase 4 Revenue Intelligence)
CREATE TABLE IF NOT EXISTS opportunities (
    id VARCHAR(64) PRIMARY KEY,
    store_id VARCHAR(64) NOT NULL REFERENCES stores(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL CHECK (
        type IN ('cross_sell', 'upsell', 'bundle', 'recovery', 'pricing', 'catalog', 'conversion', 'inventory')
    ),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'Active' CHECK (
        status IN ('Active', 'Approved', 'Rejected', 'Dismissed', 'Converted')
    ),
    confidence NUMERIC(4, 2) NOT NULL CHECK (confidence BETWEEN 0 AND 1),
    expected_impact JSONB NOT NULL DEFAULT '{"revenueUplift": 0, "conversionLift": 0}'::jsonb,
    evidence JSONB NOT NULL DEFAULT '[]'::jsonb,
    target_segment VARCHAR(100),
    recommendation JSONB NOT NULL DEFAULT '{}'::jsonb,
    policy_status VARCHAR(50) NOT NULL DEFAULT 'Passed',
    approval_status VARCHAR(50) NOT NULL DEFAULT 'Pending',
    created_by_agent VARCHAR(100) NOT NULL DEFAULT 'revenue_intelligence',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 12. EXPERIMENTS (Controlled testing of opportunities)
CREATE TABLE IF NOT EXISTS experiments (
    id VARCHAR(64) PRIMARY KEY,
    store_id VARCHAR(64) NOT NULL REFERENCES stores(id) ON DELETE CASCADE,
    opportunity_id VARCHAR(64) REFERENCES opportunities(id) ON DELETE SET NULL,
    name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'Running' CHECK (
        status IN ('Draft', 'Running', 'Paused', 'Scaled', 'Completed', 'Terminated')
    ),
    control_definition JSONB NOT NULL DEFAULT '{}'::jsonb,
    variant_definition JSONB NOT NULL DEFAULT '{}'::jsonb,
    start_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    end_at TIMESTAMPTZ,
    conversion_uplift NUMERIC(6, 2) DEFAULT 0,
    revenue_uplift NUMERIC(6, 2) DEFAULT 0,
    aov_uplift NUMERIC(6, 2) DEFAULT 0,
    statistical_confidence NUMERIC(4, 2) DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 13. POLICIES (Hard safety guardrails)
CREATE TABLE IF NOT EXISTS policies (
    id VARCHAR(64) PRIMARY KEY,
    store_id VARCHAR(64) NOT NULL REFERENCES stores(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(50) NOT NULL,
    policy_type VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'Active' CHECK (status IN ('Active', 'Paused', 'Disabled')),
    is_hard_locked BOOLEAN NOT NULL DEFAULT FALSE,
    rules JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 14. AGENT ACTIVITY (Live observability stream)
CREATE TABLE IF NOT EXISTS agent_activity (
    id VARCHAR(64) PRIMARY KEY,
    store_id VARCHAR(64) REFERENCES stores(id) ON DELETE SET NULL,
    agent VARCHAR(100) NOT NULL,
    action VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'Success',
    time TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    audit_event_id VARCHAR(64)
);

-- 15. AUDIT EVENTS (Immutable decision log)
CREATE TABLE IF NOT EXISTS audit_events (
    id VARCHAR(64) PRIMARY KEY,
    merchant_id VARCHAR(64) NOT NULL,
    store_id VARCHAR(64),
    agent VARCHAR(100) NOT NULL,
    action VARCHAR(255) NOT NULL,
    reason TEXT,
    outcome VARCHAR(50) NOT NULL DEFAULT 'Success',
    correlation_ids JSONB NOT NULL DEFAULT '{}'::jsonb,
    details JSONB NOT NULL DEFAULT '{}'::jsonb,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 16. BUYER SESSIONS (Phase 5 Agentic Commerce)
CREATE TABLE IF NOT EXISTS buyer_sessions (
    id VARCHAR(64) PRIMARY KEY,
    store_id VARCHAR(64) NOT NULL REFERENCES stores(id) ON DELETE CASCADE,
    session_token VARCHAR(255) NOT NULL UNIQUE,
    customer_id VARCHAR(64),
    context JSONB NOT NULL DEFAULT '{}'::jsonb,
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 17. BASKETS & BASKET ITEMS
CREATE TABLE IF NOT EXISTS baskets (
    id VARCHAR(64) PRIMARY KEY,
    buyer_session_id VARCHAR(64) NOT NULL REFERENCES buyer_sessions(id) ON DELETE CASCADE,
    store_id VARCHAR(64) NOT NULL REFERENCES stores(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    subtotal NUMERIC(12, 2) NOT NULL DEFAULT 0,
    discount NUMERIC(12, 2) NOT NULL DEFAULT 0,
    total NUMERIC(12, 2) NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS basket_items (
    id VARCHAR(64) PRIMARY KEY,
    basket_id VARCHAR(64) NOT NULL REFERENCES baskets(id) ON DELETE CASCADE,
    product_id VARCHAR(64) NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
    quantity INTEGER NOT NULL DEFAULT 1 CHECK (quantity > 0),
    unit_price NUMERIC(12, 2) NOT NULL CHECK (unit_price >= 0),
    subtotal NUMERIC(12, 2) NOT NULL CHECK (subtotal >= 0),
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 18. CHECKOUT INTENTS (Pre-payment authorization token)
CREATE TABLE IF NOT EXISTS checkout_intents (
    id VARCHAR(64) PRIMARY KEY,
    basket_id VARCHAR(64) NOT NULL REFERENCES baskets(id) ON DELETE CASCADE,
    store_id VARCHAR(64) NOT NULL REFERENCES stores(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL DEFAULT 'ready' CHECK (
        status IN ('ready', 'processing', 'completed', 'expired', 'failed')
    ),
    items JSONB NOT NULL DEFAULT '[]'::jsonb,
    subtotal NUMERIC(12, 2) NOT NULL,
    discount NUMERIC(12, 2) NOT NULL DEFAULT 0,
    total NUMERIC(12, 2) NOT NULL,
    currency VARCHAR(10) NOT NULL DEFAULT 'INR',
    customer JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL DEFAULT (NOW() + INTERVAL '1 hour')
);

-- =============================================================================
-- PERFORMANCE INDEXES
-- =============================================================================
CREATE INDEX IF NOT EXISTS idx_products_store ON products(store_id);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_products_sku ON products(sku);
CREATE INDEX IF NOT EXISTS idx_inventory_product ON inventory(product_id);
CREATE INDEX IF NOT EXISTS idx_orders_store ON orders(store_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);
CREATE INDEX IF NOT EXISTS idx_payments_order ON payments(order_id);
CREATE INDEX IF NOT EXISTS idx_opportunities_store_status ON opportunities(store_id, status);
CREATE INDEX IF NOT EXISTS idx_experiments_store ON experiments(store_id);
CREATE INDEX IF NOT EXISTS idx_policies_store ON policies(store_id);
CREATE INDEX IF NOT EXISTS idx_agent_activity_time ON agent_activity(time DESC);
CREATE INDEX IF NOT EXISTS idx_audit_events_time ON audit_events(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_baskets_session ON baskets(buyer_session_id);
CREATE INDEX IF NOT EXISTS idx_checkout_intents_basket ON checkout_intents(basket_id);
