from typing import Any

from pydantic import BaseModel, ConfigDict

from ._base import GetModel
from ._common import CommonGet


class ActionGet(GetModel, CommonGet):
    ...


class ActionCreate(BaseModel):
    filter: Any | None = None
    operations: Any | None = None
    recovery_operations: Any | None = None
    update_operations: Any | None = None
    name: str
    eventsource: int

    model_config = ConfigDict(extra="allow")


class ActionUpdate(ActionCreate):
    actionid: int
    name: str | None = None
    eventsource: int | None = None
