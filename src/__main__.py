# from calendar import prmonth
# from llm_sdk.llm_sdk import Small_LLM_Model
# from .create_llm_prompt import ConstructPrompt
# from .parse_arguments import ParseArguments
# from .llm_response import LlmResponse
# import sys
# from .constrained_decoding import ConstrainedDeconding
from .write_output import WriteOutputFile

def main() -> None:
    test = ["djebcjbe"]
    # llm = Small_LLM_Model()
    # arg = ParseArguments(arguments= sys.argv[1:])
    # args = arg.process_arguments()
    # prompt = ConstructPrompt()
    # user_prompts = prompt.get_user_prompts()
    # injected_prompt = prompt.injected_prompt()
    # llm_result = ""
    # full_json = []
    # fun_names = prompt.get_function_definition()
    # json_validation = ConstrainedDeconding(funs_names=fun_names)
    # for user_prompt in user_prompts:
    #     user_prompt = user_prompt.replace('"', "'")
    #     generated_p = injected_prompt + "\n{\n" + '"prompt":"' + user_prompt + '",'
    #     generate_tokens = LlmResponse(llm= llm, prompt = generated_p, ids = [], validation=json_validation)
    #     llm_result = "\n{\n" + '"prompt":"' + user_prompt + '",'
    #     print(llm_result)
    #     while True:
    #         next_token = generate_tokens.get_next_token()
    #         llm_result += next_token
    #         print(next_token, end="")
    #         if generate_tokens.stop_flag == 1:
    #             full_json.append(llm_result)
    #             break
    write_output = WriteOutputFile(output_list=test)
    write_output.write_to()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nprogram has been killed.")
    except Exception as e:
        print(e)