from types import TracebackType

import httpx
from httpx import Client

from . import schemas as sc
from .exceptions import CredentialMissingError, EmptyResponseError, ZabbixAPIError
from .generics import ZbxBase, ZbxGenericBatch, ZbxGenericCrud, ZbxGenericGet, ZbxGenericUr, rpc
from .singleton import singleton


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
            CredentialMissingError: If username and password are not provided and token is not provided.

        """
        self.url = f"{url}/api_jsonrpc.php" if url[-1] != "/" else f"{url}api_jsonrpc.php"
        if not token:
            if username and password:
                token = self._login(username, password)
            else:
                msg = "Username and password are required if token is not provided."
                raise CredentialMissingError(msg)
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
    def action(self) -> "_Action":
        return _Action(self.client, "action")

    @property
    def alert(self) -> "_Alert":
        return _Alert(self.client, "alert")

    @property
    def apiinfo(self) -> "_ApiInfo":
        return _ApiInfo(self.client, "apiinfo")

    @property
    def auditlog(self) -> "_AuditLog":
        return _AuditLog(self.client, "auditlog")

    @property
    def authentication(self) -> "_Authentication":
        return _Authentication(self.client, "authentication")

    @property
    def autoregistration(self) -> "_AutoRegistration":
        return _AutoRegistration(self.client, "autoregistration")

    @property
    def configuration(self) -> "_Configuration":
        return _Configuration(self.client, "configuration")

    @property
    def connector(self) -> "_Connector":
        return _Connector(self.client, "connector")

    @property
    def correlation(self) -> "_Correlation":
        return _Correlation(self.client, "correlation")

    @property
    def dashboard(self) -> "_Dashboard":
        return _Dashboard(self.client, "dashboard")

    @property
    def discoverycheck(self) -> "_DiscoveryCheck":
        return _DiscoveryCheck(self.client, "discovery_check")

    @property
    def discoveryhost(self) -> "_DiscoveryHost":
        return _DiscoveryHost(self.client, "discovery_host")

    @property
    def event(self) -> "_Event":
        return _Event(self.client, "event")

    @property
    def graph(self) -> "_Graph":
        return _Graph(self.client, "graph")

    @property
    def graphitem(self) -> "_GraphItem":
        return _GraphItem(self.client, "graphitem")

    @property
    def graphprototype(self) -> "_GraphPrototype":
        return _GraphPrototype(self.client, "graphprototype")

    @property
    def hanode(self) -> "_HA":
        return _HA(self.client, "hanode")

    @property
    def history(self) -> "_History":
        return _History(self.client, "history")

    @property
    def host(self) -> "_Host":
        return _Host(self.client, "host")

    @property
    def hostgroup(self) -> "_HostGroup":
        return _HostGroup(self.client, "hostgroup")

    @property
    def hostinterface(self) -> "_HostInterface":
        return _HostInterface(self.client, "hostinterface")

    @property
    def hostprototype(self) -> "_HostPrototype":
        return _HostPrototype(self.client, "hostprototype")

    @property
    def housekeeping(self) -> "_HouseKeeping":
        return _HouseKeeping(self.client, "housekeeping")

    @property
    def iconmap(self) -> "_IconMap":
        return _IconMap(self.client, "icon_map")

    @property
    def image(self) -> "_Image":
        return _Image(self.client, "image")

    @property
    def item(self) -> "_Item":
        return _Item(self.client, "item")

    @property
    def itemprototype(self) -> "_ItemPrototype":
        return _ItemPrototype(self.client, "itemprototype")

    @property
    def lldrule(self) -> "_LldRule":
        return _LldRule(self.client, "lld_rule")

    @property
    def maintenance(self) -> "_Maintenance":
        return _Maintenance(self.client, "maintenance")

    @property
    def map(self) -> "_Map":
        return _Map(self.client, "map")

    @property
    def mediatype(self) -> "_MediaType":
        return _MediaType(self.client, "mediatype")

    @property
    def module(self) -> "_Module":
        return _Module(self.client, "module")

    @property
    def problem(self) -> "_Problem":
        return _Problem(self.client, "problem")

    @property
    def proxy(self) -> "_Proxy":
        return _Proxy(self.client, "proxy")

    @property
    def regularexpression(self) -> "_RegularExpression":
        return _RegularExpression(self.client, "regular_expression")

    @property
    def report(self) -> "_Report":
        return _Report(self.client, "report")

    @property
    def role(self) -> "_Role":
        return _Role(self.client, "role")

    @property
    def _script(self) -> "_Script":
        return _Script(self.client, "script")

    @property
    def service(self) -> "_Service":
        return _Service(self.client, "service")

    @property
    def settings(self) -> "_Settings":
        return _Settings(self.client, "settings")

    @property
    def sla(self) -> "_Sla":
        return _Sla(self.client, "sla")

    @property
    def task(self) -> "_Task":
        return _Task(self.client, "task")

    @property
    def template(self) -> "_Template":
        return _Template(self.client, "template")

    @property
    def templatedashboard(self) -> "_TemplateDashboard":
        return _TemplateDashboard(self.client, "templatedashboard")

    @property
    def templategroup(self) -> "_TemplateGroup":
        return _TemplateGroup(self.client, "templategroup")

    @property
    def token(self) -> "_Token":
        return _Token(self.client, "token")

    @property
    def trend(self) -> "_Trend":
        return _Trend(self.client, "trend")

    @property
    def trigger(self) -> "_Trigger":
        return _Trigger(self.client, "trigger")

    @property
    def triggerprototype(self) -> "_TriggerPrototype":
        return _TriggerPrototype(self.client, "triggerprototype")

    @property
    def user(self) -> "_User":
        return _User(self.client, "user")

    @property
    def userdirectory(self) -> "_UserDirectory":
        return _UserDirectory(self.client, "userdirectory")

    @property
    def usergroup(self) -> "_UserGroup":
        return _UserGroup(self.client, "usergroup")

    @property
    def usermacro(self) -> "_UserMacro":
        return _UserMacro(self.client, "usermacro")

    @property
    def vlauemap(self) -> "_ValueMap":
        return _ValueMap(self.client, "valuemap")

    @property
    def webscenario(self) -> "_WebScenario":
        return _WebScenario(self.client, "webscenario")


@singleton
class _Action(ZbxGenericCrud[sc.ActionCreate, sc.ActionGet, sc.ActionUpdate]):
    ...


@singleton
class _Alert(ZbxGenericGet[sc.AlertGet]):
    ...


@singleton
class _ApiInfo(ZbxBase):
    def version(self) -> str:
        return rpc(self.client, f"{self.object_name}.version", [])


@singleton
class _AuditLog(ZbxGenericGet[sc.AuditLogGet]):
    ...


@singleton
class _Authentication(ZbxGenericUr[sc.AuthUpdate, sc.AuthGet]):
    ...


@singleton
class _AutoRegistration(ZbxGenericUr[sc.AutoRegUpdate, sc.AutoRegGet]):
    ...


@singleton
class _Configuration(ZbxBase):
    def import_(self, data: sc.ConfigurationImport) -> int | None:
        ...

    def export(self, data: sc.ConfigurationExport) -> int | None:
        ...

    def importcompare(self, data: sc.ConfigurationImportCompare) -> int | None:
        ...


@singleton
class _Connector(ZbxGenericCrud[sc.ConnectorCreate, sc.ConnectorGet, sc.ConnectorUpdate]):
    ...


@singleton
class _Correlation(ZbxGenericCrud[sc.CorrelationCreate, sc.CorrelationGet, sc.CorrelationUpdate]):
    ...


@singleton
class _Dashboard(ZbxGenericCrud[sc.DashboardCreate, sc.DashboardGet, sc.DashboardUpdate]):
    ...


@singleton
class _DiscoveryHost(ZbxGenericGet[sc.DiscoveryHostGet]):
    ...


@singleton
class _DiscoveryService(ZbxGenericGet[sc.DiscoveryServiceGet]):
    ...


@singleton
class _DiscoveryCheck(ZbxGenericGet[sc.DiscoveryCheckGet]):
    ...


@singleton
class _DiscoveryRule(ZbxGenericCrud[sc.DiscoveryRuleCreate, sc.DiscoveryRuleGet, sc.DiscoveryRuleUpdate]):
    ...


@singleton
class _Event(ZbxGenericGet[sc.EventGet]):
    def acknowledge(self, data: sc.EventAcknowledge) -> int | None:
        ...


@singleton
class _Graph(ZbxGenericCrud[sc.GraphCreate, sc.GraphGet, sc.GraphUpdate]):
    ...


@singleton
class _GraphItem(ZbxGenericGet[sc.GraphItemGet]):
    ...


@singleton
class _GraphPrototype(ZbxGenericCrud[sc.GraphPrototypeCreate, sc.GraphPrototypeGet, sc.GraphPrototypeUpdate]):
    ...


@singleton
class _HA(ZbxGenericGet[sc.HAGet]):
    ...


@singleton
class _History(ZbxGenericGet[sc.HistoryGet]):
    def clear(self, data: sc.HistoryClear) -> int | None:
        ...


@singleton
class _HostGroup(
    ZbxGenericBatch[
        sc.HostGroupCreate, sc.HostGroupGet, sc.HostGroupUpdate, sc.HostGroupMassAdd, sc.HostGroupMassUpdate
    ]
):
    def propagate(self, data: sc.HostGroupPropagate) -> int | None:
        return rpc(self.client, f"{self.object_name}.propagate", data.model_dump(exclude_unset=True))


@singleton
class _Host(ZbxGenericBatch[sc.HostCreate, sc.HostGet, sc.HostUpdate, sc.HostMassAdd, sc.HostMassUpdate]):
    ...


@singleton
class _HostInterface(
    ZbxGenericBatch[
        sc.HostInterfaceCreate,
        sc.HostInterfaceGet,
        sc.HostInterfaceUpdate,
        sc.HostInterfaceMassAdd,
        sc.HostInterfaceMassUpdate,
    ]
):
    def mass_update(self) -> int | None:
        raise NotImplementedError

    def replacehostinterfaces(self) -> int | None:
        ...


@singleton
class _HostPrototype(ZbxGenericCrud[sc.HostPrototypeCreate, sc.HostPrototypeGet, sc.HostPrototypeUpdate]):
    ...


@singleton
class _HouseKeeping(ZbxGenericUr[sc.HouseKeepingGet, sc.HouseKeepingUpdate]):
    ...


@singleton
class _IconMap(ZbxGenericCrud[sc.IconMapGet, sc.IconMapCreate, sc.IconMapUpdate]):
    ...


@singleton
class _Image(ZbxGenericCrud[sc.ImageGet, sc.ImageCreate, sc.ImageUpdate]):
    ...


class _Item(ZbxGenericCrud[sc.ItemCreate, sc.ItemGet, sc.ItemUpdate]):
    ...


class _ItemPrototype(ZbxGenericCrud[sc.ItemPrototypeCreate, sc.ItemPrototypeGet, sc.ItemPrototypeUpdate]):
    ...


@singleton
class _LldRule(ZbxGenericCrud[sc.LldRuleCreate, sc.LldRuleGet, sc.LldRuleUpdate]):
    def copy(self) -> None:
        ...


@singleton
class _Maintenance(ZbxGenericCrud[sc.MaintenanceCreate, sc.MaintenanceGet, sc.MaintenanceUpdate]):
    ...


@singleton
class _Map(ZbxGenericCrud[sc.MapCreate, sc.MapGet, sc.MapUpdate]):
    ...


@singleton
class _MediaType(ZbxGenericCrud[sc.MediaTypeCreate, sc.MediaTypeGet, sc.MediaTypeUpdate]):
    ...


@singleton
class _Module(ZbxGenericCrud[sc.ModuleCreate, sc.ModuleGet, sc.ModuleUpdate]):
    ...


@singleton
class _Problem(ZbxGenericGet[sc.ProblemGet]):
    ...


@singleton
class _Proxy(ZbxGenericCrud[sc.ProxyCreate, sc.ProxyGet, sc.ProxyUpdate]):
    ...


@singleton
class _RegularExpression(
    ZbxGenericCrud[sc.RegularExpressionCreate, sc.RegularExpressionGet, sc.RegularExpressionUpdate]
):
    ...


@singleton
class _Report(ZbxGenericCrud[sc.ReportCreate, sc.ReportGet, sc.ReportUpdate]):
    ...


@singleton
class _Role(ZbxGenericCrud[sc.RoleCreate, sc.RoleGet, sc.RoleUpdate]):
    ...


@singleton
class _Script(ZbxGenericCrud[sc.ScriptCreate, sc.ScriptGet, sc.ScriptUpdate]):
    def execute(self) -> None:
        ...

    def getscriptbyevents(self) -> None:
        ...

    def getscriptbyhosts(self) -> None:
        ...


@singleton
class _Service(ZbxGenericCrud[sc.ServiceCreate, sc.ServiceGet, sc.ServiceUpdate]):
    ...


@singleton
class _Settings(ZbxGenericUr[sc.SettingsGet, sc.SettingsUpdate]):
    ...


@singleton
class _Sla(ZbxGenericCrud[sc.SlaCreate, sc.SlaGet, sc.SlaUpdate]):
    def getsli(self) -> None:
        None


@singleton
class _Task(ZbxGenericGet[sc.TaskGet]):
    def create(self, data: sc.TaskCreate) -> int | None:
        ...


@singleton
class _TemplateDashboard(
    ZbxGenericCrud[sc.TemplateDashboardCreate, sc.TemplateDashboardGet, sc.TemplateDashboardUpdate]
):
    ...


@singleton
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


@singleton
class _Template(
    ZbxGenericBatch[sc.TemplateCreate, sc.TemplateGet, sc.TemplateUpdate, sc.TemplateMassAdd, sc.TemplateMassUpdate]
):
    ...


@singleton
class _Token(ZbxGenericCrud[sc.TokenCreate, sc.TokenGet, sc.TokenUpdate]):
    ...


@singleton
class _Trend(ZbxGenericGet[sc.TrendGet]):
    ...


@singleton
class _Trigger(ZbxGenericCrud[sc.TriggerCreate, sc.TriggerGet, sc.TriggerUpdate]):
    ...


@singleton
class _TriggerPrototype(ZbxGenericCrud[sc.TriggerPrototypeCreate, sc.TriggerPrototypeGet, sc.TriggerPrototypeUpdate]):
    ...


@singleton
class _User(ZbxGenericCrud[sc.UserCreate, sc.UserGet, sc.UserUpdate]):
    def login(self) -> int | None:
        ...

    def logout(self) -> int | None:
        ...

    def provision(self) -> int | None:
        ...

    def unblock(self) -> int | None:
        ...


@singleton
class _UserDirectory(ZbxGenericCrud[sc.UserDirectoryCreate, sc.UserDirectoryGet, sc.UserDirectoryUpdate]):
    def test(self) -> int | None:
        ...


@singleton
class _UserGroup(ZbxGenericCrud[sc.UserGroupCreate, sc.UserGroupGet, sc.UserGroupUpdate]):
    ...


@singleton
class _UserMacro(ZbxGenericCrud[sc.UserMacroCreate, sc.UserMacroGet, sc.UserMacroUpdate]):
    def createglobal(self) -> int | None:
        ...

    def deleteglobal(self) -> int | None:
        ...

    def updateglobal(self) -> int | None:
        ...


@singleton
class _ValueMap(ZbxGenericCrud[sc.ValueMapCreate, sc.ValueMapGet, sc.ValueMapUpdate]):
    ...


@singleton
class _WebScenario(ZbxGenericCrud[sc.WebScenarioCreate, sc.WebScenarioGet, sc.WebScenarioUpdate]):
    ...
