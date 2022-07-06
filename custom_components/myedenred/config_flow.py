"""Config flow for myEdenred integration."""
from __future__ import annotations

import logging
import voluptuous as vol
import async_timeout

from homeassistant import config_entries
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD

from .api.myedenred import MyEdenredAPI
from .api.consts import DEFAULT_COUNTRY, COUNTRIES
from .const import DOMAIN, CONF_COUNTRY

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """MyEdenred config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user interface."""
        _LOGGER.debug("Starting async_step_user...")
        errors = {}

        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_USERNAME].lower())
            self._abort_if_unique_id_configured()

            if await self._test_credentials(user_input):
                _LOGGER.debug("Config is valid!")
                return self.async_create_entry(
                    title="MyEdenred " + user_input[CONF_USERNAME], 
                    data = user_input
                ) 
            else:
                errors = {"base": "auth"}

        return self.async_show_form(
            step_id="user", 
            data_schema=vol.Schema({
                vol.Required(
                    CONF_COUNTRY, default=DEFAULT_COUNTRY
                ): selector.selector({ 
                    "select": { 
                        "options": COUNTRIES, 
                        "mode": "dropdown" 
                    } 
                }),
                vol.Required(CONF_USERNAME): str, 
                vol.Required(CONF_PASSWORD): str,
                vol.Required("includeTransactions"): bool
            }),
            errors=errors,
        )

    async def _test_credentials(self, user_input):
        """Return true if credentials is valid."""
        session = async_get_clientsession(self.hass, True)
        async with async_timeout.timeout(10):
            api = MyEdenredAPI(session, user_input[CONF_COUNTRY])
            try:
                await api.login(user_input[CONF_USERNAME], user_input[CONF_PASSWORD])
                return True
            except Exception as exception:
                _LOGGER.error(exception)
                return False