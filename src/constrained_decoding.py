import regex
from pydantic import BaseModel, ConfigDict
from .create_llm_prompt import ConstructPrompt


class ConstrainedDeconding(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    funs_names: list[str]
    prompt: ConstructPrompt

    def build_regex_pattern(self, fun_params: dict[str, str]) -> str:
        type_check = {
            "number": r"-?(?:0|[1-9]\d*)\.\d+",
            "integer": r"-?(?:0|[1-9]\d*)",
            "boolean": r"(?:true|false)",
            "string": r'"(?:[^"\\]|\\.)*"'
        }
        parameters = [
            f'"{key}"\\s*:\\s*{type_check[value]}'
            for key, value in fun_params.items()
        ]
        return r',\s*'.join(parameters)

    def still_valid_structure(self, text: str) -> str:
        must_include = "|".join(self.funs_names)
        fun_n = ""
        params = ""
        param_regex = ""
        if fun_n == "":
            for fun in self.funs_names:
                if fun in text:
                    fun_n = fun
        if fun_n:
            params = self.prompt.get_fun_para(fun_n)
            param_regex = self.build_regex_pattern(params)
        else:
            param_regex = r'.*'
        pattern = (
            r'"name"\s*:\s*'
            r'"(?:' + must_include + r')"'
            r'\s*,\s*\n'
            r'"parameters"\s*:\s*' + r'{' + param_regex + r'}'
            r'\s*\n}\n'
            )
        valid_json = regex.fullmatch(
            pattern=pattern, string=text, partial=True)
        if valid_json is None:
            return "Dead end."
        elif valid_json.partial:
            return "So far yes."
        else:
            return "Full."
