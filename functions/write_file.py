import os
from google.genai import types

def write_file(working_directory, file_path, content):
    # Clean the working directory
    working_dir = os.path.abspath(working_directory)

    # Build full absolute path
    target_path = os.path.normpath(os.path.abspath(os.path.join(working_dir, file_path)))

    target_path_parent_dir = os.path.dirname(target_path)

    # Check if the file path is within the working directory
    if not target_path.startswith(os.path.abspath(working_dir + os.sep)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    elif os.path.isdir(target_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    
    else:
        try:
            # Make all required parent directories
            os.makedirs(target_path_parent_dir, exist_ok=True)

            # Write to the file with the given contents
            with open(target_path, "w") as file:
                file.write(content)
                return f"Successfully wrote to {file_path} ({len(content)} characters written)"
        
        except Exception as e:
            return f"Error: {e}"
        

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write content to file within the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to run code from, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to file",
            ),
        },
    ),
)        