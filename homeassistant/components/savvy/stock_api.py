"""Provides an API wrapper for Savvy to fetch product stocks."""

import os
import ssl

import aiohttp


class StockApi:
    """API wrapper for Savvy."""

    def __init__(self, base_url: str) -> None:
        """Initialize the StockApi with the base URL."""

        self.base_url = base_url
        self.cert_path = os.path.join(
            os.path.dirname(__file__), "savvy_certificate.crt"
        )

    def _create_ssl_context(self):
        """Create an SSL context if a certificate path is provided."""
        if self.cert_path:
            ssl_context = ssl.create_default_context(cafile=self.cert_path)
        else:
            ssl_context = None
        return ssl_context

    async def fetch_product_stocks(self) -> list:
        """Fetch product stocks from the Savvy API."""

        ssl_context = self._create_ssl_context()
        conn = aiohttp.TCPConnector(ssl=ssl_context)

        async with (
            aiohttp.ClientSession(connector=conn) as session,
            session.get(f"{self.base_url}/api/stock-mgmt/stock/overview") as response,
        ):
            return await response.json()

    async def async_update_stock(self, product_id, adjustmentType, amount):
        """Update stock for a product."""

        ssl_context = self._create_ssl_context()
        conn = aiohttp.TCPConnector(ssl=ssl_context)

        async with aiohttp.ClientSession(connector=conn) as session:
            await session.patch(
                f"{self.base_url}/api/stock-mgmt/stock/products/{product_id}/adjust",
                json={"adjustmentType": adjustmentType, "amount": amount},
            )
