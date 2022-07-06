"""API to MYEDENRED."""
import aiohttp
import logging

from .account import Account
from .card import Card
from .consts import (
    API_LOGIN_URL,
    API_LIST_URL,
    API_ACCOUNTMOVEMENT_URL
)

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)


class MyEdenredAPI:
    """Interfaces to https://myedenred.pt/"""

    def __init__(self, websession, country: str):
        self.websession = websession
        self._country = country
        self.json = None

    async def login(self, username, password):
        """Issue LOGIN request."""
        try:
            params = { 'appVersion': '1.0', 'appType': 'PORTAL', 'channel': 'WEB' }
            _LOGGER.debug("Logging in...")
            async with self.websession.post(
                API_LOGIN_URL[self._country], 
                params = params,
                headers = { "Content-Type": "application/json" },
                json={"userId":username,"password":password}
            ) as res:
                if res.status == 200 and res.content_type == "application/json":
                    json = await res.json()
                    _LOGGER.debug("Done logging in.")
                    return json['data']['token']
                raise Exception("Could not retrieve token for user, login failed")
        except aiohttp.ClientError as err:
            _LOGGER.error(err)

    async def getCards(self, token) -> Card:
        """Issue CARDS requests."""
        try:
            _LOGGER.debug("Getting list of available cards...")
            async with self.websession.get(
                API_LIST_URL[self._country], 
                headers = { 
                    "Content-Type": "application/json",
                    "Authorization": token }
            ) as res:
                if res.status == 200 and res.content_type == "application/json":
                    json = await res.json()
                    _LOGGER.debug("Done getting list of available cards.")
                    return [ Card(card) for card in json['data'] ]
                raise Exception("Could not retrieve cards list from API")
        except aiohttp.ClientError as err:
            _LOGGER.error(err)

    async def getAccountDetails(self, cardId, token) -> Account:
        """Issue ACCOUNT MOVEMENT requests."""
        try:
            _LOGGER.debug("Getting card details and their movements...")
            async with self.websession.get(
                API_ACCOUNTMOVEMENT_URL[self._country].format(cardId), 
                headers = { 
                    "Content-Type": "application/json",
                    "Authorization": token }
            ) as res:
                if res.status == 200 and res.content_type == "application/json":
                    json = await res.json()
                    _LOGGER.debug("Done getting card details and their movements.")
                    return Account(
                        json['data']['account'],
                        json['data']['movementList'])
                raise Exception("Could not retrieve account information from API")
        except aiohttp.ClientError as err:
            _LOGGER.error(err)