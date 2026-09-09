from pydantic import BaseModel


class FunctionDefinitionObj(BaseModel):
    name: str
    description: str
    parameters: dict[str, dict[str, str]]
    returns: dict[str, str]
