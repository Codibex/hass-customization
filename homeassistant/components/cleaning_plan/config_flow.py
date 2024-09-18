"""Config flow for Cleaning Plan integration."""

from __future__ import annotations

import logging
import os
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .const import CONF_LAST_CLEANED_FILE, CONF_WEEKLY_PLAN_FILE, DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_WEEKLY_PLAN_FILE): str,
        vol.Required(CONF_LAST_CLEANED_FILE): str,
    }
)


class CleaningPlanConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Cleaning Plan."""

    def __init__(self, weeklyPlanFile: str, lastCleanedFile: str) -> None:
        """Initialize."""
        self.weeklyPlanFile = weeklyPlanFile
        self.lastCleanedFile = lastCleanedFile

    async def check_weeklyPlanFile_exists(self) -> bool:
        """Test if the weekly plan file exists."""
        if not os.path.isfile(self.weeklyPlanFile):
            return False

        return True

    async def check_lastCleanedFile_exists(self) -> bool:
        """Test if the last cleaned file exists."""
        if not os.path.isfile(self.lastCleanedFile):
            return False

        return True


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input."""

    hub = CleaningPlanConfigFlow(
        data[CONF_WEEKLY_PLAN_FILE], data[CONF_LAST_CLEANED_FILE]
    )

    if not await hub.check_weeklyPlanFile_exists():
        raise InvalidFile

    if not await hub.check_lastCleanedFile_exists():
        raise InvalidFile

    # Return info that you want to store in the config entry.
    return {"title": "Cleaning plan"}


class ConfigFileValidator(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Cleaning Plan."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except InvalidFile:
                errors["base"] = "invalid_file"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class InvalidFile(HomeAssistantError):
    """Error to indicate there is invalid file."""
