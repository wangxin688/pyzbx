from typing import TypedDict
from enum import IntEnum

from ._common import CommonGet
from ._base import GetModel

class HistoryType(IntEnum):
    NumFloat = 0
    Character = 1
    Log = 2
    NumUnsigned = 3
    Text = 4


class History(TypedDict):
    clock: int
    itemid: str
    ns: int
    value: float | int | str


class LogHistory(History):
    id: str
    logeventid: int
    severity: int
    source: str
    value: str


class HostoryGet(GetModel, CommonGet):
    history: HistoryType = HistoryType.NumUnsigned
    hostids: list[int] | int | None = None
    itemids: list[int] | int | None = None
    time_from: int | None = None
    time_till : int | None = None
    sortfield: str | list[str] | None = None


