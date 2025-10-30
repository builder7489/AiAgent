import os

def get_files_info(working_directory, directory="."):

    # Clean the working directory
    working_directory = os.path.abspath(working_directory)

    # Build full absolute path
    full_path = os.path.abspath(os.path.join(working_directory, directory))

    # Error messages
    error_outside_path = f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    error_not_directory = f'Error: "{directory}" is not a directory'

    # Validate the directory path stays within the working directory
    if not full_path.startswith(os.path.abspath(working_directory + os.sep)):
        return error_outside_path
    elif not os.path.isdir(full_path):
        return error_not_directory
    
    # Build string containing the directory contents
    else:
        try:
        
            directory_list = os.listdir(full_path)

            filepath_list = list(map(lambda x: os.path.abspath(os.path.join(full_path, x)) , directory_list))

            file_content_list = list(map(lambda x: f"- {os.path.basename(x)}: file_size={os.path.getsize(x)} bytes, is_dir={os.path.isdir(x)}", filepath_list))
            
            file_content_str = "\n".join(file_content_list)

            return file_content_str
        except Exception as e:
            return f"Error: {e}"
