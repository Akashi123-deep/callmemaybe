from pydantic import BaseModel, ConfigDict


class FunctionDefinitionObj(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    description: str
    parameters: dict[str, dict[str, str]]
    returns: dict[str, str]
