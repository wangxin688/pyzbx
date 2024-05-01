from uuid import UUID

from pydantic import BaseModel, Field

from ._base import GetModel
from ._common import CommonGet, GroupId, HostId


class HostGroup(BaseModel):
    groupid: str = Field(description="ID of the host group.")
    name: str = Field(description="Name of the host group.")
    flags: int = Field(description="0: a plain host group, 4: a discovered host group.")
    uuid: UUID = Field(
        description=(
            "Universal unique identifier, "
            "used for linking imported host groups to already existing ones. Auto-generated, if not given"
        )
    )


class HostGroupCreate(BaseModel):
    name: str
    uuid: UUID | None = None


class HostGroupGet(GetModel, CommonGet):
    groupids: int | list[int] | None = Field(
        default=None, description="Return only host groups with the given host group IDs."
    )
    hostids: int | list[int] | None = Field(
        default=None, description="Return only host groups that contain the given hosts."
    )
    maintenanceids: int | list[int] | None = Field(
        default=None, description="Return only host groups that are affected by the given maintenances."
    )
    triggerids: int | list[int] | None = Field(
        default=None, description="Return only host groups that contain hosts with the given triggers."
    )


class HostGroupMassAdd(BaseModel):
    """This method allows to simultaneously add multiple related objects to all the given host groups."""

    groups: list[GroupId]
    hosts: list[HostId]


class HostGroupMassRemove(HostGroupMassAdd):
    """his method allows to remove related objects from multiple host groups."""


class HostGroupMassUpdate(HostGroupMassAdd):
    """This method allows to replace hosts and templates with the specified ones in multiple host groups."""


class HostGroupPropagate(BaseModel):
    groups: list[GroupId]
    permission: bool | None = None
    tag_filters: bool | None = None


class HostGroupUpdate(BaseModel):
    groupid: int | list[int]
    name: str | None = None
    flags: int | None = None
    uuid: UUID | None = None
