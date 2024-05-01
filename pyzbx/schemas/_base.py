from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict


class GetModel(_BaseModel):
    model_config = ConfigDict(extra="allow")
