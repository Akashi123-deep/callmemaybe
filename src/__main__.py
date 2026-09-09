from llm_sdk.llm_sdk import Small_LLM_Model
from .create_llm_prompt import ConstructPrompt
from .parse_arguments import ParseArguments
from .llm_response import LlmResponse
import sys

def main() -> None:
    llm = Small_LLM_Model()
    arg = ParseArguments(arguments= sys.argv[1:])
    prompt = ConstructPrompt()
    injected_prompt = prompt.injected_prompt()
    generate_tokens = LlmResponse(llm= llm, prompt = injected_prompt, ids = [])
    args = arg.process_arguments()
    print(injected_prompt)
    while True:
        print(generate_tokens.get_next_token(), end="")
    
    

if __name__ == "__main__":
    main()