from typing import TypedDict

from ._base import GetModel
from ._common import CommonGet, Tag


class Event(TypedDict):
    eventid: str
    source: int
    object: int
    objectid: str
    clock: int
    ns: int
    r_eventid: str
    c_eventid: str
    cause_eventid: str
    correlationid: str
    userid: str
    suppressed: int
    opdata: str
    urls: list[str]
    r_clock: int
    r_ns: int
    r_source: int
    r_object: int
    r_objectid: str
    severity: int
    name: str
    value: int
    acknowledged: int


class EventGet(GetModel, CommonGet):
    eventids: list[int] | int | None = None
    groupids: list[int] | int | None = None
    hostids: list[int] | int | None = None
    objectids: list[int] | int | None = None
    source: int | None = None
    object: int | None = None
    acknowledged: bool | None = None
    suppressed: bool | None = None
    symptom: bool | None = None
    severities: list[int] | int | None = None
    evaltype: int | None = None
    tags: list[Tag] | None = None
    objectid: list[int] | int | None = None
    eventid_from: int | None = None
    eventid_till: int | None = None
    time_from: int | None = None
    time_till: int | None = None
    problem_time_from: int | None = None
    problem_time_till: int | None = None
    value: list[int] | int | None = None
