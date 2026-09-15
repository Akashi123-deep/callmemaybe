import regex
from pydantic import BaseModel

class ConstrainedDeconding(BaseModel):
    funs_names: list[str]

    def still_valid_structure(self, text: str) -> str:
        must_include = "|".join(self.funs_names)
        # name          = r'[a-zA-Z][a-zA-Z0-9_]*'
        # value         = r'(?:-?[0-9]+(?:\.[0-9]*)?|"[^"]*")'
        # param_entry   = r'"' + name + r'":\s*' + value
        # param_pattern = r'\{\s*(?:' + param_entry + r'(?:,\s*' + param_entry + r')*)?\s*\}'
        # single_obj = (
        #     r'\{\s*'
        #     r'"prompt":\s*"[^"]*"\s*,\s*'
        #     r'"name":\s*"' + must_include + r'"\s*,\s*'
        #     r'"parameters":\s*' + param_pattern +
        #     r'\s*\}'
        # )
        pattern = (
            r'"name":\s*'
            r'"(?:' + must_include + r')"'
            r',\n"parameters":\s*\{\s*'
            r'(?:"[a-zA-Z][a-zA-Z0-9_]*":\s*(?:-?[0-9]+(?:\.[0-9]*)?|"[^"]*")'
            r'(?:,\s*"[a-zA-Z][a-zA-Z0-9_]*":\s*(?:-?[0-9]+(?:\.[0-9]*)?|"[^"]*"))*)?'
            r'\s*}\s*}'
)
        # pattern = r'\[\s*' + single_obj + r'(?:\s*,\s*' + single_obj + r')*\s*\]'
        valid_json = regex.fullmatch(pattern=pattern, string=text, partial=True)
        if valid_json is None:
            return "Dead end."
        elif valid_json.partial:
            return "So far yes."
        else:
            return "Full."
        
        