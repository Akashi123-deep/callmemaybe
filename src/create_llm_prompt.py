class ConstructPrompt:
    @staticmethod
    def get_json_input(input_json: str = "/data/input/function_calling_tests.json") -> dict[str, str]:
        try:
            with open(input_json, "r") as input_json:
                json = input_json.read()
        except FileNotFoundError:
            print("File does not exist.")
            exit()
        except PermissionError:
            print("Please grant the read premission to the input file.")
            exit()
        except Exception as e:
            print(e)
            exit()
