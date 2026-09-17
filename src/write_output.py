from pydantic import BaseModel
from pathlib import Path
from json_repair import repair_json
import json


class WriteOutputFile(BaseModel):
    output_list: list[str]

    def write_to(
        self,
        path: str = "data/output/function_calling_results.json"
    ) -> None:
        output_json = "[\n" + ", ".join(self.output_list) + "]"
        formated_json = repair_json(output_json, return_objects=True)
        file_path = Path(path)
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w") as output:
                json.dump(formated_json, output, indent=4)
        except PermissionError:
            print("Please Grant write permission to the file.")
        except Exception as e:
            print(e)
