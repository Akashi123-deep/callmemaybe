from pydantic import BaseModel, ConfigDict
from llm_sdk.llm_sdk import Small_LLM_Model

class LlmResponse(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed= True)
    prompt : str
    llm: Small_LLM_Model
    ids: list[int]

    def __update_ids(self, id: int) -> None:
        self.ids.append(id)

    def __get_ids(self) -> list[int]:
        if not self.ids:
            ids = self.llm.encode(self.prompt).tolist()
            self.ids = ids[0]
        return self.ids

    def get_next_token(self) -> str:
        ids = self.__get_ids()
        logits = self.llm.get_logits_from_input_ids(ids)
        id = logits.index(max(logits))
        self.__update_ids(id)
        token = self.llm.decode(id)
        return token

