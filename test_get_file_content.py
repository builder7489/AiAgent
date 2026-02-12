from functions.get_files_content import get_files_content

# TODO set working directory
t_working_dir = "calculator"

# TODO build list for target directories
t_directories = ["main.py", "pkg/calculator.py", "/bin/cat", "pkg/does_not_exist.py"]

# TODO build display
for dir in t_directories:
    print(get_files_content(t_working_dir, dir))
    print("\n")