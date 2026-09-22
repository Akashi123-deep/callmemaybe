from pydantic import BaseModel, ConfigDict, model_validator, field_validator
import keyword
from typing import Self


class FunctionDefinitionObj(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    description: str
    parameters: dict[str, dict[str, str]]
    returns: dict[str, str]

    @model_validator(mode="after")
    def validate_fun_name(self: Self) -> Self:
        fun_name = self.name
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
        return self

    @model_validator(mode="after")
    def validate_parameter_name(self: Self) -> Self:
        para_names = [name for name in self.parameters.keys()]
        for para_name in para_names:
            if para_name == "":
                raise ValueError("parameter name is empty, invalid name.")
            if keyword.iskeyword(para_name):
                raise ValueError("parameter name match python "
                                 "keyword invalid name.")
            if para_name[:1].isdigit():
                raise ValueError("parameter name start "
                                 "with digit, invalid name.")
            if " " in para_name:
                raise ValueError("parameter name contain space, invalid name.")
            for char in para_name:
                if not char.isalnum() and char != "_":
                    raise ValueError("parameter name contain invalid symbol.")
        return self

    @model_validator(mode="after")
    def validate_parameters_type(self: Self) -> Self:
        types = ["number", "string", "integer", "boolean"]
        parameters = self.parameters
        for vals in parameters:
            type_dict = parameters[vals]
            if type_dict['type'] not in types:
                raise ValueError("invalid type.")
        return self

    @field_validator("parameters")
    def validate_parametrs_dict(value: dict[str, dict[str, str]]
                                ) -> dict[str, dict[str, str]]:
        ALLOWED_KEYS = {"type"}
        for param_name, param_name_dict in value.items():
            extra_keys = set(param_name_dict.keys()) - ALLOWED_KEYS
            if extra_keys:
                raise ValueError("Invalid keys are not allowed")
        return value

    @model_validator(mode="after")
    def validate_return(self: Self) -> Self:
        function_returns = self.returns
        types = ["number", "string", "integer", "boolean", "None"]
        if len(function_returns.keys()) > 1:
            raise ValueError("Invalid key in return section is not allowed.")
        function_return_val = function_returns['type']
        if function_return_val not in types:
            raise ValueError("Invalid type in return section.")
        return self
