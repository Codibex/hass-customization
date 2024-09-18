"""The Cleaning Plan integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .api_cleaning_plan import CleaningPlanAPI
from .api_last_cleaned import LastCleanedAPI
from .const import CONF_LAST_CLEANED_FILE, CONF_WEEKLY_PLAN_FILE, DOMAIN

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Cleaning Plan from a config entry."""

    json_file_path_cleaning_plan = str(entry.data.get(CONF_WEEKLY_PLAN_FILE))
    json_file_path_last_cleaned = str(entry.data.get(CONF_LAST_CLEANED_FILE))

    api_cleaning_plan = CleaningPlanAPI(json_file_path_cleaning_plan)
    api_last_cleaned = LastCleanedAPI(json_file_path_last_cleaned)
    hass.data[DOMAIN] = {
        "cleaning_plan": api_cleaning_plan,
        "last_cleaned": api_last_cleaned,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
