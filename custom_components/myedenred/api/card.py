"""Card Class."""

class Card:
    """Represents a MyEdenred card."""

    def __init__(self, data):
        self._data = data
        
    @property
    def id(self):
        return self._data["id"]

    @property
    def number(self):
        return self._data["number"]

    @property
    def ownerName(self):
        return self._data["ownerName"]

    @property
    def status(self):
        return self._data["status"]