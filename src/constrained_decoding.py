import regex

class ConstrainedDeconding:

    @staticmethod
    def still_valid_structure(text: str) -> str:
        name          = r'[a-zA-Z][a-zA-Z0-9_]*'
        value         = r'(?:-?[0-9]+(?:\.[0-9]*)?|"[^"]*")'
        param_entry   = r'"' + name + r'":\s*' + value
        param_pattern = r'\{\s*(?:' + param_entry + r'(?:,\s*' + param_entry + r')*)?\s*\}'
        single_obj = (
            r'\{\s*'
            r'"prompt":\s*"[^"]*"\s*,\s*'
            r'"name":\s*"' + name + r'"\s*,\s*'
            r'"parameters":\s*' + param_pattern +
            r'\s*\}'
        )
        pattern = r'\[\s*' + single_obj + r'(?:\s*,\s*' + single_obj + r')*\s*\]'
        valid_json = regex.fullmatch(pattern=pattern, string=text, partial=True)
        if valid_json is None:
            return "Dead end."
        elif valid_json.partial:
            return "So far yes."
        else:
            return "Full."
        
        