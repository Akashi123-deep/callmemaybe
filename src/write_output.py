from pydantic import BaseModel
import os

class WriteOutputFile(BaseModel):
    output_list: list[str]

    def write_to(self, path: str = "/data/output/function_calling_results.json") -> None:
        output_json = "[\n" + ", ".join(self.output_list) + "]"
        try:
            create = f"mkdir -p {path}"
            os.system(create)
            with open(path, "w") as output:
                output.write(output_json)
        except PermissionError:
            print("Please Grant write permission to the file.")
        except Exception as e:
            print(e)