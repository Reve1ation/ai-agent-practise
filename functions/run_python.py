import os
import subprocess
import sys
from google.genai import types
from functions.get_files_info import check_working_directory

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a Python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to run, relative to the working directory.",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path):
    try: 
        message = f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        abs_path = check_working_directory(working_directory, file_path, message)

        if not os.path.exists(abs_path):
            return f'Error: File "{file_path}" not found.'
        
        if not abs_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'
        
        result = subprocess.run([sys.executable, abs_path], timeout=30, capture_output = True)
        print(f'STDOUT: {result.stdout}')
        print(f'STDERR: {result.stderr}')
        if result.returncode != 0:
            return (f"Process exited with code {result.returncode}")
        if not result.stdout:
            return "No output produced."
            
        return f'Successfully ran "{file_path}"'
    
    except Exception as e:
        return f"Error: executing Python file: {e}"