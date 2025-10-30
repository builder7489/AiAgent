# Importing from subdirectory
from functions.get_files_info import get_files_info

# Testing
working_dir = "calculator"

directory_list = [
    ".",
    "pkg",
    "/bin",
    "../"
]

for directory in directory_list:
    print(f"TESTING: {directory}")
    print(get_files_info(working_dir, directory))