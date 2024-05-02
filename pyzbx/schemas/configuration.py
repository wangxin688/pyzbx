from typing import Literal

from pydantic import BaseModel


class ExportObject(BaseModel):
    host_groups: list[int] | None = None
    hosts: list[int] | None = None
    images: list[int] | None = None
    templates: list[int] | None = None
    template_groups: list[int] | None = None
    maps: list[int] | None = None
    mediaTypes: list[int] | None = None


class ConfigurationExport(BaseModel):
    format: Literal["xml", "json", "yaml", "raw"]
    prettyprint: bool = False
    options: ExportObject


class Rule1(BaseModel):
    createMissing: bool = False
    updateExisting: bool = False
    deleteMissing: bool = False


class Rule2(BaseModel):
    createMissing: bool = False
    updateExisting: bool = False


class Rule3(BaseModel):
    createMissing: bool = False
    deleteMissing: bool = False


class ImportRule(BaseModel):
    discoveryRules: Rule1 | None = None
    graphs: Rule1 | None = None
    host_groups: Rule2 | None = None
    template_groups: Rule2 | None = None
    hosts: Rule2 | None = None
    httptests: Rule1 | None = None
    images: Rule2 | None = None
    items: Rule1 | None = None
    maps: Rule2 | None = None
    mediaTypes: Rule2 | None = None
    templateLinkage: Rule3 | None = None
    templates: Rule2 | None = None
    templateDashboards: Rule1 | None = None
    triggers: Rule1 | None = None
    valueMaps: Rule1 | None = None


class ConfigurationImport(BaseModel):
    format: Literal["xml", "json", "yaml"]
    source: str
    rules: ImportRule


class ConfigurationImportCompare(ConfigurationImport):
    ...
