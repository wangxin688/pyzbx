from typing import Any

from pydantic import BaseModel, Field


class GroupId(BaseModel):
    groupid: int


class HostId(BaseModel):
    hostid: int


class CommonGet(BaseModel):
    count_output: bool | None = Field(
        description="Return the number of records in the result instead of the actual data",
        alias="countOutput",
    )
    editable: bool | None = Field(
        default=False, description="If set to true return only objects that the user has write permissions to."
    )
    exclude_search: bool | None = Field(
        description="Return results that do not match the criteria given in the search parameter.",
        alias="excludeSearch",
    )
    filter: dict[str, Any] | list[dict[str, Any]] | None = None
    limit: int | None = Field(description="Limit the number of records returned.")
    output: list[str] | None = Field(default="extend", description="Return only the given fields in the result.")
    preserve_keys: bool | None = Field(
        default=None, description="Use IDs as keys in the resulting array.", alias="preservekeys"
    )
    search: list[dict[str, str]] | None = None
    search_by_any: bool | None = Field(default=False, alias="searchByAny")
    search_wildcards_enabled: bool | None = Field(default=False, alias="searchWildcardsEnabled")
    sortfield: str | list[str]
    sortorder: str | list[str]
    start_search: bool | None = Field(default=None, alias="startSearch")


class Tag(BaseModel):
    tag: str
    value: str
    operator: int
