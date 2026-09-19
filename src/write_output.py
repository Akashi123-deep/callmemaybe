from pydantic import BaseModel
from pathlib import Path
import json
import re


class WriteOutputFile(BaseModel):
    output_list: list[str]

    @staticmethod
    def fix_backslashes(text: str) -> str:
        valid_escape = r'\\["\\/bfnrtu]'
        return re.sub(f'({valid_escape})|\\\\',
                      lambda m: m.group(1) or r'\\', text)

    def write_to(
        self,
        path: str = "data/output/function_calling_results.json"
    ) -> None:
        output_json = "[\n" + ", ".join(self.output_list) + "]"
        cleaned_json = self.fix_backslashes(output_json)
        data_json = json.loads(cleaned_json)
        file_path = Path(path)
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w") as output:
                json.dump(data_json, output, indent=4)
        except PermissionError:
            print("Please Grant write permission to the file.")
        except Exception as e:
            print(e)
