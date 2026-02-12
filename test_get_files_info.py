from functions.get_files_info import get_files_info

# TODO set working directory
t_working_dir = "calculator"

# TODO build list for target directories
t_directories = [".", "pkg", "/bin", "../"]

# TODO build display
for dir in t_directories:
    print(f"Result for {dir} directory:")
    print(get_files_info(t_working_dir, dir))
    print("\n")

