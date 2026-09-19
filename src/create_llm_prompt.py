from .function_definition import FunctionDefinitionObj
from pydantic import TypeAdapter, ValidationError, ConfigDict, BaseModel, Field
from typing import cast, Annotated


class PromptItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    prompt: str


class ConstructPrompt(BaseModel):
    input_json_def: str = "data/input/functions_definition.json"
    input_json_file: str = "data/input/function_calling_tests.json"

    def __get_json_input(self) -> list[PromptItem]:
        try:
            with open(self.input_json_file, "r") as input_json:
                json = input_json.read()
            adapter = TypeAdapter(Annotated[list[PromptItem],
                                  Field(min_length=1)])
            result = adapter.validate_json(json)
            return cast(list[PromptItem], result)
        except FileNotFoundError:
            print("File does not exist.")
            exit()
        except PermissionError:
            print("Please grant the read premission to the input file.")
            exit()
        except ValidationError as e:
            for error in e.errors():
                print(error["msg"])
            exit()
        except Exception as e:
            print(e)
            exit()

    def __get_json_definition(self) -> list[FunctionDefinitionObj]:
        try:
            with open(self.input_json_def, "r") as input_json:
                json = input_json.read()
            adapter = TypeAdapter(Annotated[list[FunctionDefinitionObj],
                                  Field(min_length=1)])
            result = adapter.validate_json(json)
            description = (
                "Fallback function to call when the user "
                "request does not match any other available function or tool."
            )
            unknwon_fun = FunctionDefinitionObj(
                name="fn_unknown",
                description=description,
                parameters={},
                returns={"type": "None"}
            )
            result.append(unknwon_fun)
            return cast(list[FunctionDefinitionObj], result)
        except FileNotFoundError:
            print("File does not exist.")
            exit()
        except PermissionError:
            print("Please grant the read premission to the input file.")
            exit()
        except ValidationError as e:
            for error in e.errors():
                print(error["msg"])
            exit()
        except Exception as e:
            print(e)
            exit()

    def get_user_prompts(self) -> list[str]:
        user_prompts = []
        for input_json in self.__get_json_input():
            user_prompts.append(input_json.prompt)
        return user_prompts

    def get_function_definition(self) -> list[str]:
        functions_definition = []
        for fun_d in self.__get_json_definition():
            functions_definition.append(fun_d.name)
        return functions_definition

    def injected_prompt(self) -> str:
        prompt = (
            'You are a function-calling engine. '
            'Given a user request and the list of\n'
            'available functions below, choose'
            ' exactly one function and fill its\n'
            'parameters with correctly-typed, correctly-valued arguments.\n'
            '\n'
            'Available functions:\n\n'
            '\n'
            'Rules for building argument values:\n'
            '1. Numbers must be extracted exactly '
            'as written, no rounding, no\n'
            '   truncation, regardless of magnitude '
            '(large numbers, decimals,\n'
            '   negatives all preserved exactly).\n'
            '2. Match the number format to the parameter\'s declared type:\n'
            '   - type "number" (float)  -> always include a decimal point,\n'
            '     e.g. 2 -> 2.0, 40 -> 40.0, 3.5 -> 3.5\n'
            '   - type "integer"          -> '
            'plain integer, no decimal point,\n'
            '     e.g. 2.0 -> 2, 40 -> 40\n'
            '   Never mix the two: do not output 2 for a float parameter or\n'
            '   2.0 for an integer parameter.\n'
            '3. Strings must be copied exactly as given (case, punctuation,\n'
            '   quotes preserved), unless the function explicitly asks for a\n'
            '   transformed value.\n'
            '4. When a parameter is a regular '
            'expression (its name or description\n'
            '   mentions "regex" or "pattern"), '
            'do NOT copy one literal example you\n'
            '   see in the source text. '
            'Instead identify the category of thing\n'
            '   being described and write '
            'the minimal general pattern for it:\n'
            '   - numbers / digits          -> \\d+\n'
            '   - vowels                    -> [aeiouAEIOU]\n'
            '   - letters                   -> [A-Za-z]+\n'
            '   - whitespace / spaces       -> \\s+\n'
            '   - a specific whole word     -> \\bword\\b\n'
            '   - a specific literal symbol -> escape it, e.g. . -> \\.\n'
            '5. Output only the JSON object. '
            'No prose, no explanation, no markdown.\n'
            '\n'
            'Examples:\n\n'
            'Request: What is the sum of 40 and 2?\n'
            '-> {"name": "fn_add_numbers", '
            '"parameters": {"a": 40.0, "b": 2.0}}\n\n'
            'Request: Replace every digit in the text with X\n'
            '-> {"name": "fn_substitute_string_with_regex", '
            '"parameters": {"source_string": "...", '
            '"regex": "\\d+", "replacement": "X"}}\n\n'
            'Request: Swap every occurrence '
            'of the word foo for bar in the text\n'
            '-> {"name": "fn_substitute_string_with_regex", '
            '"parameters": {"source_string": "...", '
            '"regex": "\\bfoo\\b", "replacement": "bar"}}\n\n'
            'Request: Mask all the punctuation in the text with #\n'
            '-> {"name": "fn_substitute_string_with_regex", '
            '"parameters": {"source_string": "...", '
            '"regex": "[^\\w\\s]", "replacement": "#"}}\n\n'
            'Now process this request:\n'
        )
        prompt += "\nAvailiable functions:\n\n"
        for d_f in self.__get_json_definition():
            para = [
                f"{k}: {v['type']}"
                for k, v in d_f.parameters.items()
                ]
            prompt += f'{d_f.name}({", ".join(para)}): {d_f.description}\n'
        return prompt
