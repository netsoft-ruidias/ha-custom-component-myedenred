"""Platform for sensor integration."""
from __future__ import annotations
from typing import Any, Dict
import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.core import HomeAssistant
from homeassistant.const import DEVICE_CLASS_MONETARY, ATTR_ATTRIBUTION
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api.myedenred import MY_EDENRED
from .api.card import Card
from .const import (
    DEFAULT_ICON,
    UNIT_OF_MEASUREMENT
)

_LOGGER = logging.getLogger(__name__)

#    async def async_setup_platform(
#        hass: core.HomeAssistant,
#        config: ConfigType,
#        async_add_entities,
#        discovery_info: DiscoveryInfoType | None = None
#    ) -> None:
#        """Set up the sensor platform."""
#
#        session = async_get_clientsession(hass, True)
#        api = MY_EDENRED(session)
#        token = await api.login(config["username"], config["password"])
#        if (token):
#            cards = await api.getCards(token)
#            sensors = [MyEdenredSensor(card, api, config["username"], config["password"]) for card in cards]
#            async_add_entities(sensors, update_before_add=True)

async def async_setup_entry(
    hass: HomeAssistant, 
    config_entry: ConfigEntry, 
    async_add_entities):
    """Setup sensor platform."""
    session = async_get_clientsession(hass, True)
    api = MY_EDENRED(session)

    _LOGGER.info("async_setup_entry", "config_entry", config_entry)

    config = config_entry.data

    _LOGGER.info("async_setup_entry", "config", config)

    token = await api.login(config["username"], config["password"])
    if (token):
        cards = await api.getCards(token)
        sensors = [MyEdenredSensor(card, api, config["username"], config["password"]) for card in cards]
        async_add_entities(sensors)


class MyEdenredSensor(SensorEntity):
    """Representation of a MyEdenred Card (Sensor)."""

    def __init__(self, card: Card, api: MY_EDENRED, username: str, password: str):
        super().__init__()
        self._card = card
        self._api = { api, username, password }
        self._state = 0
        self._icon = DEFAULT_ICON
        self._unit_of_measurement = UNIT_OF_MEASUREMENT
        self.attrs: Dict[str, Any] = card

    _attr_native_unit_of_measurement = "€"
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_state_class = SensorStateClass.TOTAL

    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return self._card.number

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return self._card.id

    @property
    def state(self) -> float:
        return self._state

    @property
    def device_state_attributes(self) -> Dict[str, Any]:
        return self.attrs

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._attr_native_value = 23
        token = await self._api.api.login(self._api.username, self._api.password)
        if (token):
            account = await self._api.api.getAccountDetails(self._card.id, token)
            self.state = account.availableBalance
            

