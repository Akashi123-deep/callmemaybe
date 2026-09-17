import regex
from pydantic import BaseModel


class ConstrainedDeconding(BaseModel):
    funs_names: list[str]

    def still_valid_structure(self, text: str) -> str:
        must_include = "|".join(self.funs_names)
        pattern = (
            r'\n"name":\s*'
            r'"(?:' + must_include + r')"'
            r',\n"parameters":\s*\{\s*'
            r'(?:"[a-zA-Z][a-zA-Z0-9_]*":\s*(?:-?[0-9]+(?:\.[0-9]*)?|"[^"]*")'
            r'(?:,\s*"[a-zA-Z][a-zA-Z0-9_]*":\s*'
            r'(?:-?[0-9]+(?:\.[0-9]*)?|"[^"]*"))*)?'
            r'\s*}\n}')
        valid_json = regex.fullmatch(
            pattern=pattern, string=text, partial=True)
        if valid_json is None:
            return "Dead end."
        elif valid_json.partial:
            return "So far yes."
        else:
            return "Full."
