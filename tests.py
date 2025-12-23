# Importing from subdirectory
from functions.get_files_info import get_files_info
from functions.get_files_content import get_files_content
# Testing
working_dir = "calculator"

directory_list = [
    "main.py",
    "tests.py",
    ".",
    "pkg",
    "/bin",
    "../"
]

for directory in directory_list:
    print(f"TESTING: {directory}")

    # Test getting directory contents
    # print(get_files_info(working_dir, directory))

    # Test getting file contents
    print(get_files_content(working_dir, directory))