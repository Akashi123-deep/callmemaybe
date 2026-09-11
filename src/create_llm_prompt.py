import json
from  .function_definition import FunctionDefinitionObj
from pydantic import TypeAdapter, ValidationError

class ConstructPrompt:
    @staticmethod
    def __get_json_input(input_json: str = "data/input/function_calling_tests.json") -> list[dict[str, str]]:
        try:
            with open(input_json, "r") as input_json:
                json = input_json.read()
            adapter = TypeAdapter(list[dict[str, str]])
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
        except Exception as e:
            print(e)
            exit()

    def injected_prompt(self) -> str:
        prompt = ""
        for prompt_data in self.__get_json_input():
            prompt += f"The user prompt: {prompt_data['prompt']}\n"
        prompt += "\nAvailable functions:\n"
        for function_data in self.__get_json_definition():
            name = function_data.name
            description = function_data.description
            parameters = [f"{k} type {v['type']}" for k, v in function_data.parameters.items()]
            prompt += f"\n{name} : {description} parameters {' '.join(parameters)}"
        prompt += '\n\nOutput schema format:\n[\n{\n"prompt": "<write the actual user prompt here>",\n"name": "<function name used to solve use prompt>",\n"parameters": {"param_name": value}\n}\n]'
        prompt += "For all prompt above."
        return prompt
