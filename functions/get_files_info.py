import os
from google.genai import types

MAX_CHARS = 10_000

def check_working_directory(working_directory: str, object_path: str = '', mass_message: str = ''):
    object_path = object_path or ""
    path = os.path.join(working_directory, object_path)
    abs_path = os.path.abspath(path)
    abs_working_dir = os.path.abspath(working_directory)
    if not abs_path.startswith(abs_working_dir):
        return f'Error of check_working_directory: {mass_message}'
    # print(f'abs_path: {abs_path}')
    return abs_path

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory: str, directory: str = None):
    try: 
        message = f'Cannot list "{directory}" as it is outside the permitted working directory'
        abs_path = check_working_directory(working_directory, directory, message)
        
        if not os.path.exists(abs_path):
            return f'Error: "{directory}" is not a directory'
        
        objects_list = os.listdir(abs_path);

        print(objects_list)
        entries = []
        for object in objects_list:
            is_dir = os.path.isdir(os.path.join(abs_path, object))
            file_size = os.path.getsize(os.path.join(abs_path, object))

            print(f" - {object}: file_size = {file_size} bytes, is_dir = {is_dir}")
            entries.append(f" - {object}: file_size = {file_size} bytes, is_dir = {is_dir} \n")
        return entries

    except Exception as e:
        return f"Error: {e}"
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Opens a file and returns its content up to 10000 characters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to read from, relative to the working directory.",
            ),
        },
    ),
)
    
def get_file_content(working_directory: str, file_path: str):
    try: 
        message = f'Cannot read "{file_path}" as it is outside the permitted working directory'
        abs_path = check_working_directory(working_directory, file_path, message)
        
        if not os.path.isfile(abs_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(abs_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            # print(f'len of text: {len(file_content_string)}')
        return f'{file_content_string} [...File "{file_path}" truncated at 10000 characters]'

    except Exception as e:
        return f"Error: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to a file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)

def write_file(working_directory: str, file_path: str, content: str):
    try: 
        message = f'Cannot write to "{file_path}" as it is outside the permitted working directory'
        abs_path = check_working_directory(working_directory, file_path, message)
        path_dir = os.path.dirname(abs_path)
        if not os.path.exists(path_dir):
            os.makedirs(path_dir, mode=0o777)
        
        with open(abs_path, "w") as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
    
