from llm_sdk.llm_sdk import Small_LLM_Model
from .create_llm_prompt import ConstructPrompt
from .parse_arguments import ParseArguments
from .llm_response import LlmResponse
import sys
from .constrained_decoding import ConstrainedDeconding
from .write_output import WriteOutputFile
from termcolor import colored
import os


def main() -> None:
    llm = Small_LLM_Model()
    arg = ParseArguments(arguments=sys.argv[1:])
    args = arg.process_arguments()
    in_def = args.get("functions_definition")
    in_f = args.get("input_file")
    if (in_f is not None) and (in_def is not None):
        prompt = ConstructPrompt(input_json_file=in_f, input_json_def=in_def)
    elif in_def is not None:
        prompt = ConstructPrompt(input_json_def=in_def)
    elif in_f is not None:
        prompt = ConstructPrompt(input_json_file=in_f)
    else:
        prompt = ConstructPrompt()
    user_prompts = prompt.get_user_prompts()
    injected_prompt = prompt.injected_prompt()
    llm_result = ""
    full_json = []
    fun_names = prompt.get_function_definition()
    json_validation = ConstrainedDeconding(funs_names=fun_names)
    i = 0
    for user_prompt in user_prompts:
        os.system("clear")
        user_prompt = user_prompt.replace('"', "'")
        print(colored(f"processed prompts: {i}/{len(user_prompts)}", "cyan"))
        print(colored("Available functions:\n", "yellow",
                      "on_light_green"))
        for fun_n in fun_names:
            print(colored(fun_n, "cyan"))
        print(colored(f"\nCurrent prompt: {user_prompt}",
                      "green", "on_light_magenta"))
        add_name = "{\n" + '"prompt":"' + user_prompt + '",'
        generated_p = injected_prompt + add_name
        generate_tokens = LlmResponse(
            llm=llm, prompt=generated_p,
            ids=[], validation=json_validation
        )
        llm_result = "{\n" + '"prompt":"' + user_prompt + '",'
        print(colored(llm_result, "blue"))
        i += 1
        while True:
            next_token = generate_tokens.get_next_token()
            llm_result += next_token
            print(colored(next_token, "blue"), end="")
            if generate_tokens.stop_flag == 1:
                full_json.append(llm_result)
                os.system("clear")
                break
    write_output = WriteOutputFile(output_list=full_json)
    output_arg = args.get("output_file")
    if output_arg is not None:
        write_output.write_to(path=output_arg)
    else:
        write_output.write_to()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nprogram has been killed.")
    except Exception as e:
        print(e)
