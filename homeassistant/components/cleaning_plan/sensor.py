"""Sensor platform for the Cleaning Plan integration."""

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .api_cleaning_plan import CleaningPlanAPI
from .api_last_cleaned import LastCleanedAPI
from .const import DOMAIN


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None,
) -> None:
    """Set up the Cleaning Plan sensor platform."""
    if discovery_info is None:
        return

    data = hass.data[DOMAIN]
    api_cleaning_plan: CleaningPlanAPI = data["cleaning_plan"]
    api_last_cleaned: LastCleanedAPI = data["last_cleaned"]

    async_add_entities(
        [
            CleaningPlanEntity(api_cleaning_plan),
            LastCleanedSensor(api_last_cleaned),
        ]
    )


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Cleaning Plan sensors from a config entry."""
    data = hass.data[DOMAIN]

    # Erhalte die APIs von den gespeicherten Daten
    api_cleaning_plan: CleaningPlanAPI = data["cleaning_plan"]
    api_last_cleaned: LastCleanedAPI = data["last_cleaned"]

    async_add_entities(
        [
            CleaningPlanEntity(api_cleaning_plan),
            LastCleanedSensor(api_last_cleaned),
        ]
    )


class CleaningPlanEntity(Entity):
    """Sensor for the Cleaning Plan."""

    def __init__(self, api_cleaning_plan: CleaningPlanAPI) -> None:
        """Initialize the sensor."""
        self.api_cleaning_plan = api_cleaning_plan
        self._attr_name = "Cleaning Plan"
        self._attr_unique_id = "cleaning_plan"
        self._attr_icon = "mdi:broom"
        self._attr_state = "active"
        self.cleaning_plan_data: dict[str, Any] = {}

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return self._attr_name or ""

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return self._attr_unique_id or ""

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return str(self._attr_state)

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Return the state attributes."""
        if self.cleaning_plan_data is not None:
            return {
                "date_range": self.cleaning_plan_data.get("dateRange") or "",
                "daily_plans": self.cleaning_plan_data.get("dailyPlans") or "",
            }

        return {}

    async def async_update(self) -> None:
        """Update the sensor."""
        self.cleaning_plan_data = self.api_cleaning_plan.get_cleaning_plan()


class LastCleanedSensor(Entity):
    """Sensor for Last Cleaned Data."""

    def __init__(self, api_last_cleaned: LastCleanedAPI) -> None:
        """Initialize the sensor."""
        self.api_last_cleaned = api_last_cleaned
        self._attr_name = "Last Cleaned"
        self._attr_unique_id = "last_cleaned"
        self._attr_icon = "mdi:broom"
        self._attr_state = "active"
        self.last_cleaned_data: dict[str, Any] = {}

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return self._attr_name or ""

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return self._attr_unique_id or ""

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return str(self._attr_state)

    async def async_update(self) -> None:
        """Update the sensor."""
        self.last_cleaned_data = self.api_last_cleaned.get_last_cleaned()
