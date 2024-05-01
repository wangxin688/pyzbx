from types import TracebackType

import httpx
from httpx import Client

from . import schemas as sc
from .exceptions import CrendentialMissingError, EmptyResponseError, ZabbixAPIError
from .generics import ZbxBase, ZbxGenericBatch, ZbxGenericCrud, ZbxGenericGet, ZbxGenericUr, _rpc


class ZabbixClient:
    def __init__(
        self,
        url: str,
        username: str | None = None,
        password: str | None = None,
        token: str | None = None,
        timeout: int | None = 5,
        session: Client | None = None,
    ) -> None:
        """
        Initializes a new instance of the ZabbixClient class.

        Args:
            url (str): The URL of the Zabbix server's API endpoint.
            username (str, optional): The username for authentication. Defaults to None.
            password (str, optional): The password for authentication. Defaults to None.
            token (str, optional): The authentication token. Defaults to None.
            timeout (int, optional): The timeout for API requests. Defaults to 5.
            session (httpx.Client, optional): An existing HTTP session to use. Defaults to None.
        Returns:
            None
        Raises:
            CrendentialMissingError: If username and password are not provided and token is not provided.

        """
        self.url = f"{url}/api_jsonrpc.php" if url[-1] != "/" else f"{url}api_jsonrpc.php"
        if not token:
            if username and password:
                token = self._login(username, password)
            else:
                msg = "Username and password are required if token is not provided."
                raise CrendentialMissingError(msg)
        self.headers = {"Content-Type": "application/json-rpc", "Authorization": f"Bearer {token}"}
        if session:
            session.base_url = self.url
            session.headers = self.headers
            session.timeout = timeout
            self.client = session
        else:
            self.client = Client(base_url=self.url, headers=self.headers, timeout=timeout)

    def __enter__(self) -> Client:
        return self.client

    def __exit__(
        self,
        exc_type: type[BaseException] | None = None,
        exc_value: BaseException | None = None,
        traceback: TracebackType | None = None,
    ) -> None:
        if self.client.is_closed:
            return
        self.client.close()

    def _login(self, username: str, password: str) -> str:
        """recommended way is creating a long term token. if not,
        remember to logout to prevent a large number of open sessions"""
        r = httpx.post(
            self.url,
            headers={"Content-Type": "application/json-rpc"},
            json={
                "jsonrpc": "2.0",
                "method": "user.login",
                "params": {"user": username, "password": password},
                "id": 1,
            },
        )
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

    @property
    def hostgroup(self) -> "_HostGroup":
        return _HostGroup(self.client, "hostgroup")

    @property
    def host(self) -> "_Host":
        return _Host(self.client, "host")

    @property
    def template(self) -> "_Template":
        return _Template(self.client, "template")

    @property
    def templategroup(self) -> "_TemplateGroup":
        return _TemplateGroup(self.client, "templategroup")


class _Action(ZbxGenericCrud[sc.ActionCreate, sc.ActionGet, sc.ActionUpdate]):
    ...


class _Alert(ZbxGenericGet[sc.AlertGet]):
    ...


class _ApiInfo(ZbxBase):
    def version(self) -> str | None:
        return _rpc(self.client, f"{self.object_name}.version")


class _AuditLog(ZbxGenericGet[sc.AuditLogGet]):
    ...


class _Authentication(ZbxGenericUr[sc.AuthUpdate, sc.AuthGet]):
    ...


class _Autoregistration(ZbxGenericUr[sc.AutoRegUpdate, sc.AutoRegGet]):
    ...


class _HostGroup(
    ZbxGenericBatch[
        sc.HostGroupCreate, sc.HostGroupGet, sc.HostGroupUpdate, sc.HostGroupMassAdd, sc.HostGroupMassUpdate
    ]
):
    def propagate(self, data: sc.HostGroupPropagate) -> int | None:
        return _rpc(self.client, f"{self.object_name}.propagate", data.model_dump(exclude_unset=True))


class _Host(ZbxGenericBatch[sc.HostCreate, sc.HostGet, sc.HostUpdate, sc.HostMassAdd, sc.HostMassUpdate]):
    ...


class _TemplateGroup(
    ZbxGenericBatch[
        sc.TemplateGroupCreate,
        sc.TemplateGroupGet,
        sc.TemplateGroupUpdate,
        sc.TemplateGroupMassAdd,
        sc.TemplateGroupMassUpdate,
    ]
):
    ...


class _Template(
    ZbxGenericBatch[sc.TemplateCreate, sc.TemplateGet, sc.TemplateUpdate, sc.TemplateMassAdd, sc.TemplateMassUpdate]
):
    ...
