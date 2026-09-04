import asyncio

from app.repositories.registry import Repositories

REVENUE_TREND = [
    {"label": "Week 1", "revenue": 62000, "raygoInfluencedRevenue": 8200},
    {"label": "Week 2", "revenue": 69000, "raygoInfluencedRevenue": 9700},
    {"label": "Week 3", "revenue": 71500, "raygoInfluencedRevenue": 11200},
    {"label": "Week 4", "revenue": 82120, "raygoInfluencedRevenue": 13700},
]


class DashboardService:
    def __init__(self, repos: Repositories):
        self.repos = repos

    async def overview(self, merchant_id: str) -> dict:
        # Independent reads run concurrently rather than sequentially.
        merchant, opportunities = await asyncio.gather(
            self.repos.merchants.get(merchant_id),
            self.repos.opportunities.find_many(
                {"merchantId": merchant_id}, limit=3, sort=[("confidence", -1)]
            ),
        )
        top = [
            {
                "id": o["id"],
                "title": o["title"],
                "shortTitle": o["shortTitle"],
                "expectedMonthlyImpact": o["expectedMonthlyImpact"],
                "confidence": o["confidence"],
                "risk": o["risk"],
                "status": o["status"],
            }
            for o in opportunities
        ]
        metrics = (merchant or {}).get("metrics", {})
        return {
            "merchant": {
                "id": merchant["id"],
                "name": merchant["name"],
                "category": merchant["category"],
                "currency": merchant["currency"],
            }
            if merchant
            else None,
            "metrics": metrics,
            "topOpportunities": top,
            "revenueTrend": REVENUE_TREND,
            "latestReasoning": {
                "agent": "Revenue Intelligence",
                "summary": f"RAYGO found {metrics.get('activeOpportunities', 0)} revenue opportunities using observed journey and catalog signals.",
                "route": f"/opportunities/{top[0]['id']}" if top else "/opportunities",
            },
        }
