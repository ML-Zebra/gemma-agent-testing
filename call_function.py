from typing import Any, Callable

from config import WORKING_DIR
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_python import run_python_file, schema_run_python_file
from functions.write_file_content import schema_write_file, write_file

function_map: dict[str, Callable[..., Any]] = {
    schema.name: func
    for schema, func in [
        (schema_get_files_info, get_files_info),
        (schema_get_file_content, get_file_content),
        (schema_run_python_file, run_python_file),
        (schema_write_file, write_file),
    ]
    if schema.name is not None
}


def call_function(
    function_name: str,
    parameters: dict[str, Any],
    verbose: bool = False,
) -> Any:
    """
    Execute a function by name with given parameters.

    Args:
        function_name: Name of the function to call
        parameters: Dictionary of parameter name -> value
        verbose: Whether to print verbose output

    Returns:
        The result of the function execution
    """
    if verbose:
        print(f"Calling function: {function_name} with parameters: {parameters}")
    else:
        print(f"Calling function: {function_name}")

    if function_name not in function_map:
        raise ValueError(f"Unknown function: {function_name}")

    func = function_map[function_name]
    parameters_with_working_dir = {**parameters, "working_directory": WORKING_DIR}

    try:
        result = func(**parameters_with_working_dir)
        return result
    except TypeError as e:
        raise ValueError(f"Invalid parameters for {function_name}: {e}")
    except Exception as e:
        raise RuntimeError(f"Error executing {function_name}: {e}")
