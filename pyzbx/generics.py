from typing import Generic, TypedDict, TypeVar

from httpx import Client
from pydantic import BaseModel

from .exceptions import EmptyResponseError, ZabbixAPIError

_CreateT = TypeVar("_CreateT", bound=BaseModel)
_GetT = TypeVar("_GetT", bound=BaseModel)
_MassAddT = TypeVar("_MassAddT", bound=BaseModel)
_MassRemoveT = TypeVar("_MassRemoveT", bound=BaseModel)
_MassUpdateT = TypeVar("_MassUpdateT", bound=BaseModel)
_UpdateT = TypeVar("_UpdateT", bound=BaseModel)

_ParamsT = TypeVar("_ParamsT", str, dict, list, int)


class ZbxCreateResponse(TypedDict):
    jsonrpc: str
    result: dict[str, list[str]]
    id: int


class ZbxBase:
    __slots__ = ["client", "object_name", "id_"]

    def __init__(self, client: Client, object_name: str, id_: int = 1) -> None:
        self.client = client
        self.object_name = object_name
        self.id_ = id_


class ZbxGenericBatch(ZbxBase, Generic[_CreateT, _GetT, _MassAddT, _MassRemoveT, _MassUpdateT, _UpdateT]):
    def create(self, data: _CreateT) -> int | None:
        self.id_ += 1
        return _rpc(self.client, f"{self.object_name}.create", data.model_dump(exclude_unset=True), self.id_)

    def get(self, data: _GetT) -> int | None:
        self.id_ += 1
        return _rpc(self.client, f"{self.object_name}.get", data.model_dump(exclude_unset=True), self.id_)

    def mass_add(self, data: _MassAddT) -> int | None:
        self.id_ += 1
        return _rpc(self.client, f"{self.object_name}.massadd", data.model_dump(exclude_unset=True), self.id_)

    def mass_remove(self, data: _MassRemoveT) -> int | None:
        self.id_ += 1
        return _rpc(self.client, f"{self.object_name}.massremove", data.model_dump(exclude_unset=True), self.id_)

    def mass_update(self, data: _MassUpdateT) -> int | None:
        self.id_ += 1
        return _rpc(self.client, f"{self.object_name}.massupdate", data.model_dump(exclude_unset=True), self.id_)

    def update(self, data: _UpdateT) -> int | None:
        self.id_ += 1
        return _rpc(self.client, f"{self.object_name}.update", data.model_dump(exclude_unset=True), self.id_)

    def delete(self, data: list[int] | int) -> int | None:
        data = _id_to_list(data)
        self.id_ += 1
        return _rpc(self.client, f"{self.object_name}.delete", data, self.id_)


class ZbxGenericCrud(ZbxBase, Generic[_CreateT, _GetT, _UpdateT]):
    def create(self, data: _CreateT) -> int | None:
        self.id_ += 1
        return _rpc(self.client, f"{self.object_name}.create", data.model_dump(exclude_unset=True), self.id_)

    def get(self, data: _GetT) -> int | None:
        self.id_ += 1
        return _rpc(self.client, f"{self.object_name}.get", data.model_dump(exclude_unset=True), self.id_)

    def update(self, data: _UpdateT) -> int | None:
        self.id_ += 1
        return _rpc(self.client, f"{self.object_name}.update", data.model_dump(exclude_unset=True), self.id_)

    def delete(self, data: list[int] | int) -> int | None:
        data = _id_to_list(data)
        self.id_ += 1
        return _rpc(self.client, f"{self.object_name}.delete", data, self.id_)


class ZbxGenericGet(ZbxBase, Generic[_GetT]):
    def get(self, data: _GetT) -> int | None:
        self.id_ += 1
        return _rpc(self.client, f"{self.object_name}.get", data.model_dump(exclude_unset=True), self.id_)


class ZbxGenericUr(ZbxBase, Generic[_GetT, _UpdateT]):
    def get(self, data: _GetT) -> int | None:
        self.id_ += 1
        return _rpc(self.client, f"{self.object_name}.get", data.model_dump(exclude_unset=True), self.id_)

    def update(self, data: _UpdateT) -> int | None:
        self.id_ += 1
        return _rpc(self.client, f"{self.object_name}.update", data.model_dump(exclude_unset=True), self.id_)


def _rpc(client: Client, method: str, params: _ParamsT, id_: int | None = 1) -> int | None:
    payload = {"jsonrpc": "2.0", "method": method, "params": params, "id": id_}
    r = client.post(json=payload)
    r.raise_for_status()
    if not (result := r.json()):
        msg = "Received empty response from Zabbix server"
        raise EmptyResponseError(msg)
    if "error" in result:
        raise ZabbixAPIError(
            code=result["error"].get("code"),
            message=result["error"].get("message"),
            data=result["error"].get("data"),
        )
    return result["result"]


def _id_to_list(id_: int | list[int]) -> list[int]:
    if isinstance(id_, int):
        return [id]
    return id


def get_id(response: ZbxCreateResponse, object_name: str) -> int:
    id_name_mappings = {
        "itemprototype": "itemids",
        "triggerprototype": "triggerids",
        "graphprototype": "graphids",
    }
    key = object_name + "ids" if object_name not in id_name_mappings else id_name_mappings[object_name]
    return int(response["result"][key][0])
