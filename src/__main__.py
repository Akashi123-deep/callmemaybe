from llm_sdk.llm_sdk import Small_LLM_Model
from .create_llm_prompt import ConstructPrompt
from .parse_arguments import ParseArguments
from .llm_response import LlmResponse
from .constrained_decoding import ConstrainedDeconding
import sys

def main() -> None:
    llm = Small_LLM_Model()
    arg = ParseArguments(arguments= sys.argv[1:])
    prompt = ConstructPrompt()
    injected_prompt = prompt.injected_prompt()
    json_validation = ConstrainedDeconding()
    generate_tokens = LlmResponse(llm= llm, prompt = injected_prompt, ids = [], validation=json_validation)
    args = arg.process_arguments()
    while True:
        print(generate_tokens.get_next_token(), end="")
        if generate_tokens.stop_flag == 1:
            break
    
    
    

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nprogram has been killed.")
    except Exception as e:
        print(e)