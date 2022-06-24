"""Config flow for myEdenred integration."""
from __future__ import annotations

import logging
import voluptuous as vol
import async_timeout

from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api.myedenred import MY_EDENRED
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

DATA_SCHEMA = vol.Schema(
    { 
        vol.Required("username"): str, 
        vol.Required("password"): str,
        vol.Required("includeTransactions"): bool,
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """MyEdenred config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user interface."""
        _LOGGER.debug("Starting async_step_user...")
        errors = {}

        if user_input is not None:
            await self.async_set_unique_id(user_input["username"].lower())
            self._abort_if_unique_id_configured()

            if await self._test_credentials(user_input):
                _LOGGER.debug("Config is valid!")
                return self.async_create_entry(
                    title="MyEdenred " + user_input["username"], 
                    data = user_input
                ) 
            else:
                errors = {"base": "auth"}

        return self.async_show_form(
            step_id="user", 
            data_schema=DATA_SCHEMA, 
            errors=errors,
        )

    async def _test_credentials(self, user_input):
        """Return true if credentials is valid."""
        session = async_get_clientsession(self.hass, True)
        async with async_timeout.timeout(10):
            api = MY_EDENRED(session)
            try:
                await api.login(user_input["username"], user_input["password"])
                return True
            except Exception as exception:
                _LOGGER.error(exception)
                return False