from motor.motor_asyncio import AsyncIOMotorDatabase

from app.db.indexes import Collections
from app.repositories.base import MongoRepository


class Repositories:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.merchants = MongoRepository(db[Collections.MERCHANTS])
        self.categories = MongoRepository(db[Collections.CATEGORIES])
        self.products = MongoRepository(db[Collections.PRODUCTS])
        self.dashboard_snapshots = MongoRepository(db[Collections.DASHBOARD_SNAPSHOTS])
        self.opportunities = MongoRepository(db[Collections.OPPORTUNITIES])
        self.experiments = MongoRepository(db[Collections.EXPERIMENTS])
        self.policies = MongoRepository(db[Collections.POLICIES])
        self.policy_evaluations = MongoRepository(db[Collections.POLICY_EVALUATIONS])
        self.approvals = MongoRepository(db[Collections.APPROVALS])
        self.agent_runs = MongoRepository(db[Collections.AGENT_RUNS])
        self.agent_activity = MongoRepository(db[Collections.AGENT_ACTIVITY])
        self.buyer_intents = MongoRepository(db[Collections.BUYER_INTENTS])
        self.baskets = MongoRepository(db[Collections.BASKETS])
        self.order_intents = MongoRepository(db[Collections.ORDER_INTENTS])
        self.orders = MongoRepository(db[Collections.ORDERS])
        self.razorpay_orders = MongoRepository(db[Collections.RAZORPAY_ORDERS])
        self.payment_attempts = MongoRepository(db[Collections.PAYMENT_ATTEMPTS])
        self.webhook_events = MongoRepository(db[Collections.WEBHOOK_EVENTS])
        self.audit_events = MongoRepository(db[Collections.AUDIT_EVENTS])
        self.idempotency_records = db[Collections.IDEMPOTENCY_RECORDS]


def get_repositories(db: AsyncIOMotorDatabase) -> Repositories:
    return Repositories(db)
