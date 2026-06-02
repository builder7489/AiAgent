from google.genai import types
from collections.abc import Callable

from functions.get_file_content import schema_get_file_content
from functions.get_files_info import schema_get_files_info
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file


available_functions = types.Tool(
    function_declarations= [
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

#
# Enabling the agent to choose which function to call
#
def call_function(function_call: types.FunctionCall, verbose: bool = False) -> types.Content:

    # Handle empty or incorrect function call args
    function_name: str = function_call.name or ""

    # Add verbose option in args list
    verbose_setting = verbose

    if verbose_setting:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    # Build map of functions for function calling options
    function_map: dict[str, Callable[..., str]] = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file
    }

    # Handle functions that are not found in the map of available functions
    if not function_map.get(function_name):
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    # Create a shadow copy of the called function before overwriting an argument to reset the working directory
    args = dict(function_call.args) if function_call.args else {}
    
    # reset working directory to guard againt unknown changes
    args['working_directory'] = "./calculator"

    function_result = function_map[function_name](**args)
    
    # Return function call description
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )