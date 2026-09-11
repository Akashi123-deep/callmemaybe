from pydantic import BaseModel
import re

class ParseArguments(BaseModel):
    arguments : list[str]

    def __parse_definition_path(self) -> str:
        arg = next(arg for arg in self.arguments if(arg.find("--functions_definition")) != -1)
        path = arg.split(" ")[1]
        return path[:-1]
        

    def __update_the_arguments(self) -> None:
        self.arguments = [" ".join(self.arguments[i: i + 2]) for i in range(0, len(self.arguments), 2)]

    def __parse_input_path(self) -> str:
        arg = next(arg for arg in self.arguments if(arg.find("--input")) != -1)
        path = arg.split(" ")[1]
        return path[:-1]

    def __parse_output_path(self) -> str:
        arg = next(arg for arg in self.arguments if(arg.find("--output")) != -1)
        path = arg.split(" ")[1]
        return path[:-1]

    def __is_valid_functions_definition_arg(self) -> bool:
        for argument in self.arguments:
            valid_match0 = re.match(r"\[--functions_definition\s+(.*)\]",argument)
            if valid_match0:
                break
        if valid_match0:
            return True
        return False

    def __is_valid_input_arg(self) -> bool:
        for argument in self.arguments:
            valid_match1 = re.match(r"\[--input\s+(.*)\]", argument)
            if valid_match1:
                break
        if valid_match1:
            return True
        return False

    def __is_valid_output_arg(self) -> bool:
        for argument in self.arguments:
            valid_match2 = re.match(r"\[--output\s+(.*)\]", argument)
            if valid_match2:
                break
        if valid_match2:
            return True
        return False

    def is_valid_arguments(self) -> None:
        if len(self.arguments) > 3:
            print("Too many arguments. Please provide valid arguments structure:  [--functions_definition <function_definition_file>] [--input <input_file>] [--"
            "output <output_file>]")
            exit()

    def process_arguments(self) -> dict[str, str]:
        self.__update_the_arguments()
        files = dict()
        if not self.arguments:
            return files
        self.is_valid_arguments()
        output_arg = self.__is_valid_output_arg()
        input_arg = self.__is_valid_input_arg()
        definition_arg = self.__is_valid_functions_definition_arg()
        count_valid_arg = [output_arg, input_arg, definition_arg].count(True)
        if count_valid_arg != 3:
            print("Note invalid arguments will be ignored.")
        if definition_arg:
            files["functions_definition"] = self.__parse_definition_path()
        if input_arg:
            files["input_file"] = self.__parse_input_path()
        if output_arg:
            files["output_file"] = self.__parse_output_path()
        return files


