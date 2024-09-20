"""Config flow for Savvy."""

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from .const import CONF_STOCKS_URL, DOMAIN

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_STOCKS_URL): str,
    }
)


class SavvyConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Savvy."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._stocksUrl = ""

    async def async_step_user(self, user_input=None) -> ConfigFlowResult:
        """Handle the initial step."""
        if user_input is not None:
            self._stocksUrl = user_input[CONF_STOCKS_URL]
            return self.async_create_entry(
                title="Savvy", data={CONF_STOCKS_URL: self._stocksUrl}
            )

        return self.async_show_form(step_id="user", data_schema=STEP_USER_DATA_SCHEMA)
