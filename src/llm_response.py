from pydantic import BaseModel, ConfigDict
from typing import List, Any

class LlmResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    prompt: str
    llm: Any  
    validation: Any  
    ids: List[int] = []
    _prompt_len: int = 0
    stop_flag: int = 0

    def _get_ids(self) -> List[int]:
        if not self.ids:
            encoded = self.llm.encode(self.prompt)
            self.ids = encoded[0].tolist()
        return self.ids

    def get_next_token(self) -> str:
        current_ids = self._get_ids()
        if not hasattr(self, "_prompt_len") or self._prompt_len == 0:
            self._prompt_len = len(current_ids)
        logits = self.llm.get_logits_from_input_ids(current_ids)
        while True:
            max_val = max(logits)
            token_id = logits.index(max_val)
            candidate_ids = current_ids[self._prompt_len:] + [token_id]
            full_text = self.llm.decode(candidate_ids)
            if self.validation.still_valid_structure(full_text) == "Dead end.":
                logits[token_id] = float('-inf')
            elif self.validation.still_valid_structure(full_text) == "Full.":
                self.stop_flag = 1
                return self.llm.decode([token_id]) + "\n"
            else:
                self.ids.append(token_id)
                token_str = self.llm.decode([token_id])
                return token_str