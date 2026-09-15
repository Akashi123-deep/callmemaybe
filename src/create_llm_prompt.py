import re
from  .function_definition import FunctionDefinitionObj
from pydantic import TypeAdapter, ValidationError, ConfigDict, BaseModel

class PromptItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    prompt: str

class ConstructPrompt:
    @staticmethod
    def __get_json_input(input_json_file: str = "data/input/function_calling_tests.json") -> list[PromptItem]:
        try:
            with open(input_json_file, "r") as input_json:
                json = input_json.read()
            adapter = TypeAdapter(list[PromptItem])
            return adapter.validate_json(json)
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

    @staticmethod
    def __get_json_definition(input_json_definition: str = "data/input/functions_definition.json") -> list[FunctionDefinitionObj]:
        try:
            with open(input_json_definition, "r") as input_json:
                json = input_json.read()
            adapter = TypeAdapter(list[FunctionDefinitionObj])
            return adapter.validate_json(json)
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
        prompt = """\nReturn ONLY a JSON. No explanation, no markdown fences, no text before or after it.
Each object: {"prompt": "<exact input text>", "name": "<function name>", "parameters": {<The function parametr name>: <passed value>}}\n"""
        prompt += """Example: 
What is the sum of 7 and 1?
Output:
{"prompt": "What is the sum of 7 and 1?", "name": "fn_add_numbers", "parameters": {"a": 7, "b": 1}}"""
        prompt += "\nAvailiable functions:\n\n"
        for data_definition in self.__get_json_definition():
            parameters = [f"{k}: {v["type"]}" for k,v in data_definition.parameters.items()]
            prompt += f"{data_definition.name}({", ".join(parameters)}): {data_definition.description}\n"
        
        return prompt
