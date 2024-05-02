from typing import Any

from ._base import GetModel
from ._common import CommonGet


class AlertGet(GetModel, CommonGet):
    alertids: list[int] | int | None = None
    actionids: list[int] | None = None
    eventids: list[int] | None = None
    groupids: list[int] | None = None
    hostids: list[int] | None = None
    mediatypeids: list[int] | None = None
    objectids: list[int] | None = None
    eventobject: int | None = None
    eventsource: int | None = None
    time_from: int | None = None
    time_till: int | None = None
    selectHosts: Any | None = None
    selectUsers: Any | None = None
    selectMediatypes: Any | None = None
