from llm_sdk.llm_sdk import Small_LLM_Model
# from create_llm_prompt import ConstructPrompt
from .parse_arguments import ParseArguments
import sys

def main() -> None:
    llm = Small_LLM_Model()
    arg = ParseArguments(arguments= sys.argv)
    print(arg.process_arguments())
#    prompt = ConstructPrompt()
#    prompt.get_json_input()

if __name__ == "__main__":
    main()