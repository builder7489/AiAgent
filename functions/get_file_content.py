import os
from config import MAX_CHARS
from google.genai import types

def get_file_content(working_directory, file_path):

    # Clean the working directory
    working_directory = os.path.abspath(working_directory)

    # Build full absolute path
    target_path = os.path.normpath(os.path.abspath(os.path.join(working_directory, file_path)))

    # Error messages
    error_outside_path = f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    error_not_file = f'Error: File not found or is not a regular file: "{file_path}"'

    # Validate the file path is in the working directory
    if not target_path.startswith(os.path.abspath(working_directory + os.sep)):
        return error_outside_path
    elif not os.path.isfile(target_path):
        return error_not_file
    
    
    # read file contents: only first 10000 characters, check if file was larger than limit
    else:
        try:
            
            with open(target_path, 'r') as file:
                # set read limit and check for truncation
                file_content = file.read(MAX_CHARS)
                file_limit_check = file.read(MAX_CHARS + 1)

                print(file_content)
                # append message for truncated files
                if file_limit_check:
                    file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

            return file_content
        except Exception as e:
            return f"Error: {e}"
        

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a given file truncating content over 10K characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to list content from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)