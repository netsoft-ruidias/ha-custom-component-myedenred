"""Account Class."""

from typing import List
from .transaction import Transaction

class Account:
    """Represents a MyEdenred account."""

    def __init__(self, account, movementList):
        self._data = account
        self._movementList = movementList
        
    @property
    def iban(self):
        return self._data["iban"]

    @property
    def cardNumber(self):
        return self._data["cardNumber"]

    @property
    def availableBalance(self) -> float:
        return self._data["availableBalance"]

    @property
    def cardHolderFirstName(self):
        return self._data["cardHolderFirstName"]

    @property
    def cardHolderLastName(self):
        return self._data["cardHolderLastName"]

    @property
    def cardActivated(self):
        return self._data["cardActivated"]

    @property
    def movementList(self) -> List[Transaction]:
        return [
            Transaction(x) for x in self._movementList
        ]
