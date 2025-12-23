import os
def get_files_content(working_dir, file_path):
    # absolute paths for working dir and target file
    abs_working_dir = os.path.abspath(working_dir)
    abs_file_path = os.path.abspath(os.path.join(working_dir, file_path))

    # Error messages
    #error_file_path

    return None