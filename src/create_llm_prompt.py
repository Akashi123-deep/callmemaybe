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
        user_prompt_format = '"prompt": "Put the correspond user prompt here as it is.",'
        function_used = '"name": "Here put the function name used to solve the user prompt.",'
        used_parameters = 'parameters: {"function_parameter": value from the user prompt}'
        json_output_format = user_prompt_format + function_used + used_parameters
        input_prompt_json = self.__get_json_input()
        input_function_definition = self.__get_json_definition()
        for prompt_data in input_prompt_json:
            prompt += f"The use prompt : {prompt_data["prompt"]}\n"
        prompt += "\nAvailable functions:\n"
        for function_data in input_function_definition:
            name = function_data.name
            description = function_data.description

            parameters = [f"{k} type {v["type"]}" for k,v in function_data.parameters.items()]
            prompt += f"\n{name} : {description} parameters {" ".join(parameters)}"
        prompt += f"\nPreduce a json format from these information following this format :\n[{json_output_format}]"
        prompt += '\nOutput schema format: [\n{"prompt": "<write the user prompt here>",\n"name": "<write function name used to solve the prompt>",\n"parameters": {"param_name": value}\n}\n]'
        prompt += '\nDo that for all prompts from start to the and of useres prompts as describe above.'
        return prompt
