from pydantic import BaseModel, ConfigDict, model_validator
import keyword
from typing import Any


class FunctionDefinitionObj(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    description: str
    parameters: dict[str, dict[str, str]]
    returns: dict[str, str]

    @model_validator(mode="before")
    @classmethod
    def validate_fun_name(cls, values: Any) -> Any:
        fun_name = values.get('name')
        if fun_name == "":
            raise ValueError("Function name is empty, invalid name.")
        if keyword.iskeyword(fun_name):
            raise ValueError("Function name match python "
                             "keyword invalid name.")
        if fun_name[:1].isdigit():
            raise ValueError("Function name start with digit, invalid name.")
        if " " in fun_name:
            raise ValueError("Function name contain space, invalid name.")
        for char in fun_name:
            if not char.isalnum() and char != "_":
                raise ValueError("Function name contain invalid symbol.")
        return values

    @model_validator(mode="before")
    @classmethod
    def validate_parameters_type(cls, values: Any) -> Any:
        types = ["number", "string", "integer", "boolean"]
        parameters = values.get('parameters')
        for vals in parameters:
            type_dict = parameters[vals]
            if type_dict['type'] not in types:
                raise ValueError("invalid type.")
        return values
