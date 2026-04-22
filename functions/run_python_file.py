import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    # Clean the working directory
    abs_working_dir = os.path.abspath(working_directory + os.sep)

    # Build full path for target file
    abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))

    # Build command to run for the subprocess
    command = ["python", abs_file_path]

    # Validate the target file path is inside the working directory
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    # Validate the file path exists and target a regular file
    if not os.path.isfile(abs_file_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    
    # Validate python file
    if not abs_file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file'
    
    else:
        try: 
            # Add any additional commands
            if args != None:
                command.extend(args)

            # Run the built commands
            process_run_completed = subprocess.run(command, cwd=abs_working_dir, capture_output=True, timeout=30, text=True)

            # Build output string from the command information
            process_run_info = ""

            if process_run_completed.returncode != 0:
                process_run_info += f"Process exited with code {process_run_completed.returncode}"

            if (process_run_completed.stdout == None) and (process_run_completed.stderr == None):
                process_run_info += "No output produced"

            else:
                process_run_info += f"STDOUT: \n{process_run_completed.stdout}\n"
                process_run_info += f"STDERR: \n{process_run_completed.stderr}"

                #return process_run_info
                return process_run_info
        
        except Exception as e:
            return f"Error: executing Python file: {e}"