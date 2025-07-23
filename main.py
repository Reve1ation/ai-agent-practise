import os
import sys
from typing import Callable
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.llm_schemas import available_functions
from functions.get_files_info import get_files_info, get_file_content, write_file
from functions.run_python import run_python_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

functions_mapping = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

def call_function(function_call_part: Callable, verbose: bool =False):
    function_name = function_call_part.name
    function_args = function_call_part.args

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    working_directory = './calculator'
    args = dict(function_args)
    args['working_directory'] = working_directory

    if function_name in functions_mapping:
        function = functions_mapping[function_name]
        function_result = function(**args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

def get_user_prompt() -> str:
    """Extract the user prompt from command-line arguments or exit with an error."""
    try:
        return sys.argv[1]
    except IndexError as exc:
        print(f"Error: {exc}")
        sys.exit(1)


def append_candidates_to_messages(response: types.GenerateContentResponse, messages: list[types.Content]):
    """Append all candidate contents returned by the model to the ongoing message list."""
    for candidate in response.candidates:
        messages.append(candidate.content)


def _pretty_print_tool_result(tool_result):
    """Utility to pretty-print tool output when verbose mode is enabled."""
    print("Result:")
    if isinstance(tool_result, list):
        for line in tool_result:
            print(line.rstrip())
    else:
        print(tool_result)


def process_function_calls(response: types.GenerateContentResponse, messages: list[types.Content], verbose: bool = False):
    """Run every function call requested by the model and append their responses to messages.

    Returns True if the response contained any function calls, otherwise False.
    """
    function_call_parts = response.function_calls or []
    for function_call_part in function_call_parts:
        func_result = call_function(function_call_part, verbose)
        messages.append(func_result)  # func_result already has the correct tool role/part structure

        if verbose and func_result.parts:
            tool_resp_wrapper = func_result.parts[0].function_response.response
            tool_result = tool_resp_wrapper.get("result") if isinstance(tool_resp_wrapper, dict) else tool_resp_wrapper
            _pretty_print_tool_result(tool_result)

    return bool(function_call_parts)

def main():
    user_prompt = get_user_prompt()
    verbose = len(sys.argv) > 2 and sys.argv[2] == "--verbose"

    # Initialise conversation
    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    for _ in range(20):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt,
                ),
            )

            append_candidates_to_messages(response, messages)

            has_function_call = process_function_calls(response, messages, verbose)

            # If the model produced a pure-text reply and no further actions are needed, finish up.
            if response.text and not has_function_call:
                print(f"Agent: {response.text}")
                break

        except Exception as exc:
            print(f"Error: {exc}")
            continue



if __name__ == "__main__":
    main()
