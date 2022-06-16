"""Config flow for myEdenred integration."""
from __future__ import annotations

import logging
import voluptuous as vol
import async_timeout

from homeassistant import data_entry_flow, config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from api.myedenred import MY_EDENRED
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    { 
        vol.Required("username"): str, 
        vol.Required("password"): str 
    }
)

@config_entries.HANDLERS.register(DOMAIN)
class MyEdenredConfigFlow(data_entry_flow.FlowHandler):
    """MyEdenred config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user interface."""
        _LOGGER.info("Starting async_step_user...")
        errors = {}

        #if self._async_current_entries():
        #    return self.async_abort(reason="single_instance_allowed")
        #if self.hass.data.get(DOMAIN):
        #    return self.async_abort(reason="single_instance_allowed")
        
        _LOGGER.info("Setup domain %s", DOMAIN)

        if user_input is not None:
            _LOGGER.info("user_input is not None")
            _LOGGER.info(user_input)

            #await self.async_set_unique_id(user_input["username"].lower())
            #self._abort_if_unique_id_configured()

            # Validate user input
            valid = await self._test_credentials(user_input)

            if valid:
                _LOGGER.info("Config is valid!")
                return self.async_create_entry(
                    title="MyEdenred " + user_input["username"], 
                    data = user_input
                ) 
            else:
                errors = {"base": "auth"}

        _LOGGER.info("Show async_show_form...")

        return self.async_show_form(
            step_id="user", 
            data_schema=DATA_SCHEMA, 
            errors=errors,
        )

    async def _test_credentials(self, user_input):
        """Return true if credentials is valid."""        
        session = async_get_clientsession(self.hass, True)
        async with async_timeout.timeout(10):
            _LOGGER.info("Checking Credentials")
            api = MY_EDENRED(session)
            try:
                token = await api.login(user_input["username"], user_input["password"])
                return True
            except Exception as exception:
                _LOGGER.error(exception)
                return False