"""Provides an API wrapper for Savvy to fetch product stocks."""

import aiohttp


class StockApi:
    """API wrapper for Savvy."""

    def __init__(self, base_url: str) -> None:
        """Initialize the StockApi with the base URL."""

        self.base_url = base_url

    async def fetch_product_stocks(self) -> list:
        """Fetch product stocks from the Savvy API."""

        async with (
            aiohttp.ClientSession() as session,
            session.get(f"{self.base_url}/api/stock-mgmt/stock/overview") as response,
        ):
            return await response.json()
