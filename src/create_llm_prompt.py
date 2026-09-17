from .function_definition import FunctionDefinitionObj
from pydantic import TypeAdapter, ValidationError, ConfigDict, BaseModel
from typing import cast


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
            adapter = TypeAdapter(list[PromptItem])
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
            adapter = TypeAdapter(list[FunctionDefinitionObj])
            result = adapter.validate_json(json)
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
            "\nReturn ONLY a JSON. No explanation, "
            "no markdown fences, no text before or after it.\n"
            'Each object: {"prompt": "<exact input text>"'
            ', "name": "<function name>", '
            '"parameters": {<The function parametr name>: <passed value>}}\n'
        )
        prompt += (
            "Example:\n"
            "What is the sum of 7 and 1?\n"
            "Output:\n"
            '{"prompt": "What is the sum of 7 and 1?"'
            ', "name": "fn_add_numbers", '
            '"parameters": {"a": 7.0, "b": 1.0}'
            "}"
            "\nif the type is number you must "
            "write the parametrs in floating format"
            "and normal format if parameter type is integer"
        )
        prompt += "\nAvailiable functions:\n\n"
        for d_f in self.__get_json_definition():
            para = [
                f"{k}: {v["type"]}"
                for k, v in d_f.parameters.items()
                ]
            prompt += f"{d_f.name}({", ".join(para)}): {d_f.description}\n"
        prompt += (
            "You are an expert in Regular "
            "Expressions (Regex). Your task is to generate a "
            "precise, valid regex pattern based on "
            "the user's natural language request."
        )
        return prompt
