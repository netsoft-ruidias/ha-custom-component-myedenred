import logging
import voluptuous as vol
import async_timeout

from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from api.myedenred import MY_EDENRED
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    { vol.Required("username"): str, vol.Required("password"): str }
)

@config_entries.HANDLERS.register(DOMAIN)
class MyEdenredConfigFlow(config_entries.ConfigFlow):
    """MyEdenred config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_ASSUMED

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user interface."""
        errors = {}

        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        if self.hass.data.get(DOMAIN):
            return self.async_abort(reason="single_instance_allowed")
        
        if user_input is not None:
            await self.async_set_unique_id(user_input["username"].lower())
            self._abort_if_unique_id_configured()

            # Validate user input
            valid = await self._test_credentials(
                user_input["username"],
                user_input["password"]
            )

            if valid:
                return self.async_create_entry(
                    title="MyEdenred", data={"username": user_input["username"], "password": user_input["password"]}
                ) 
            else:
                errors = {"base": "auth"}

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors,
        )

    async def _test_credentials(self, username, password):
        """Return true if credentials is valid."""        
        session = async_get_clientsession(self.hass, True)
        async with async_timeout.timeout(10):
            _LOGGER.info("Checking Credentials")
            api = MY_EDENRED(session)
            try:
                token = await api.login(username, password)
                return True
            except Exception as exception:
                _LOGGER.error(exception)
                return False