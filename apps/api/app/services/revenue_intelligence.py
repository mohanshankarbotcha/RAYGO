from app.repositories.registry import Repositories


class RevenueIntelligenceService:
    """MVP behavior: returns seeded opportunities, ranked by confidence,
    with `opp_keyboard_stand` guaranteed to rank highest."""

    def __init__(self, repos: Repositories):
        self.repos = repos

    async def ranked_opportunities(self, merchant_id: str, status: str | None = None, risk: str | None = None, limit: int = 50) -> list[dict]:
        query: dict = {"merchantId": merchant_id}
        if status:
            query["status"] = status
        if risk:
            query["risk"] = risk
        items = await self.repos.opportunities.find_many(query, limit=limit)
        items.sort(key=lambda o: (o["id"] != "opp_keyboard_stand", -o.get("confidence", 0)))
        return items
