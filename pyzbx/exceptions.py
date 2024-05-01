from typing import Any


class CrendentialMissingError(Exception):
    pass


class EmptyResponseError(Exception):
    pass


class ZabbixAPIError(Exception):
    def __init__(self, code: int | None = None, message: str | None = None, data: Any | None = None) -> None:
        self.code = code
        self.message = message
        self.data = data

    def __str__(self) -> str:
        return f"Error: code: {self.code}, message: {self.message}, data: {self.data}"
