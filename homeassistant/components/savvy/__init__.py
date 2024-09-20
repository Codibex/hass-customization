"""The Savvy integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import CONF_STOCKS_URL, DOMAIN
from .coordinator import SavvyCoordinator
from .stock_api import StockApi

PLATFORMS: list[Platform] = [Platform.SENSOR]

type SavvyConfigEntry = ConfigEntry[StockApi]  # noqa: F821


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Savvy from a config entry."""

    api_url = str(entry.data.get(CONF_STOCKS_URL))
    api = StockApi(api_url)

    coordinator = SavvyCoordinator(hass, api)

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_config_entry_first_refresh()

    # Store the coordinator in hass.data so it can be accessed from other parts of the integration
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
