from motor.motor_asyncio import AsyncIOMotorDatabase


class Collections:
    MERCHANTS = "merchants"
    CATEGORIES = "categories"
    PRODUCTS = "products"
    DASHBOARD_SNAPSHOTS = "dashboard_snapshots"
    OPPORTUNITIES = "opportunities"
    EXPERIMENTS = "experiments"
    POLICIES = "policies"
    POLICY_EVALUATIONS = "policy_evaluations"
    APPROVALS = "approvals"
    AGENT_RUNS = "agent_runs"
    AGENT_ACTIVITY = "agent_activity"
    BUYER_INTENTS = "buyer_intents"
    BASKETS = "baskets"
    ORDER_INTENTS = "order_intents"
    ORDERS = "orders"
    RAZORPAY_ORDERS = "razorpay_orders"
    PAYMENT_ATTEMPTS = "payment_attempts"
    WEBHOOK_EVENTS = "webhook_events"
    AUDIT_EVENTS = "audit_events"
    IDEMPOTENCY_RECORDS = "idempotency_records"


async def ensure_indexes(db: AsyncIOMotorDatabase) -> None:
    await db[Collections.MERCHANTS].create_index("id", unique=True)
    await db[Collections.CATEGORIES].create_index("id", unique=True)

    await db[Collections.PRODUCTS].create_index("id", unique=True)
    await db[Collections.PRODUCTS].create_index([("merchantId", 1), ("status", 1)])

    await db[Collections.OPPORTUNITIES].create_index("id", unique=True)
    await db[Collections.OPPORTUNITIES].create_index([("merchantId", 1), ("status", 1), ("confidence", 1)])

    await db[Collections.EXPERIMENTS].create_index("id", unique=True)
    await db[Collections.EXPERIMENTS].create_index([("merchantId", 1), ("opportunityId", 1)])

    await db[Collections.POLICIES].create_index("id", unique=True)

    await db[Collections.POLICY_EVALUATIONS].create_index("id", unique=True)
    await db[Collections.POLICY_EVALUATIONS].create_index([("merchantId", 1), ("actionType", 1), ("createdAt", 1)])

    await db[Collections.APPROVALS].create_index("id", unique=True)
    await db[Collections.APPROVALS].create_index([("merchantId", 1), ("targetType", 1), ("targetId", 1)])

    await db[Collections.AGENT_RUNS].create_index("id", unique=True)
    await db[Collections.AGENT_RUNS].create_index([("agentName", 1), ("status", 1), ("createdAt", 1)])

    await db[Collections.AGENT_ACTIVITY].create_index("id", unique=True)
    await db[Collections.AGENT_ACTIVITY].create_index("timestamp")

    await db[Collections.BUYER_INTENTS].create_index("id", unique=True)

    await db[Collections.ORDER_INTENTS].create_index("id", unique=True)
    await db[Collections.ORDER_INTENTS].create_index("displayOrderId", unique=True)

    await db[Collections.ORDERS].create_index("id", unique=True)
    await db[Collections.ORDERS].create_index([("merchantId", 1), ("status", 1), ("createdAt", 1)])

    await db[Collections.RAZORPAY_ORDERS].create_index("razorpayOrderId", unique=True)

    await db[Collections.PAYMENT_ATTEMPTS].create_index("id", unique=True)
    await db[Collections.PAYMENT_ATTEMPTS].create_index(
        "razorpayPaymentId", unique=True, sparse=True
    )
    await db[Collections.PAYMENT_ATTEMPTS].create_index([("orderIntentId", 1), ("status", 1)])

    await db[Collections.WEBHOOK_EVENTS].create_index("razorpayEventId", unique=True)

    await db[Collections.AUDIT_EVENTS].create_index("id", unique=True)
    await db[Collections.AUDIT_EVENTS].create_index("timestamp")
    await db[Collections.AUDIT_EVENTS].create_index([("merchantId", 1), ("severity", 1), ("timestamp", 1)])

    await db[Collections.IDEMPOTENCY_RECORDS].create_index(
        [("key", 1), ("route", 1)], unique=True
    )
    await db[Collections.IDEMPOTENCY_RECORDS].create_index("expiresAt", expireAfterSeconds=0)
