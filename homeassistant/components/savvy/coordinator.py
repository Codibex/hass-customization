"""Module contains the SavvyCoordinator class which manages fetching Savvy data from the API."""

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .stock_api import StockApi

_LOGGER = logging.getLogger(__name__)


class SavvyCoordinator(DataUpdateCoordinator):
    """Class to manage fetching Savvy data from the API."""

    def __init__(self, hass: HomeAssistant, api: StockApi) -> None:
        """Initialize."""

        super().__init__(
            hass,
            _LOGGER,
            name="Savvy",
            update_interval=timedelta(minutes=5),
            always_update=True,
        )

        self.api = api

    async def _async_setup(self) -> None:
        return await super()._async_setup()

    async def _async_update_data(self):
        """Fetch data from API endpoint."""
        try:
            data = await self.api.fetch_product_stocks()
            # Transform the data into a dictionary with product_id as the key
            return {item["productId"]: item for item in data}
        except (ConnectionError, TimeoutError, ValueError) as err:
            raise UpdateFailed(f"Error fetching data: {err}") from err
