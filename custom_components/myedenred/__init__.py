"""The my_edenred integration."""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.typing import ConfigType, HomeAssistantType

from .const import DOMAIN, PLATFORM, DOMAIN_DATA

__version__ = "1.0.0"
_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistantType, config: ConfigType) -> bool:
    """Set up the EventSensor component."""
    _LOGGER.debug("Set up the EventSensor component")
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry):
    """Set up the component from a config entry."""
    _LOGGER.debug("Entry data: %s", entry.data)
    _LOGGER.debug("Entry options: %s", entry.options)
    _LOGGER.debug("Entry unique ID: %s", entry.unique_id)

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, PLATFORM)
    )
    return True

async def async_unload_entry(hass: HomeAssistantType, entry: ConfigEntry):
    """Unload a config entry."""
    # forward unload
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, PLATFORM)

    if unload_ok:
        # remove update listener
        hass.data[DOMAIN_DATA].pop(entry.entry_id)()

        # remove entity from registry
        entity_registry = await er.async_get_registry(hass)
        entity_registry.async_clear_config_entry(entry.entry_id)

    return unload_ok