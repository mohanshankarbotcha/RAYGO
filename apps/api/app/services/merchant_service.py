from app.repositories.registry import Repositories


class MerchantService:
    def __init__(self, repos: Repositories):
        self.repos = repos

    async def get(self, merchant_id: str) -> dict | None:
        return await self.repos.merchants.get(merchant_id)
