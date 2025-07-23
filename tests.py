from functions.get_files_info import get_files_info, get_file_content, write_file, schema_get_files_info
from functions.run_python import run_python_file

if __name__ == "__main__":
    # print(get_files_info("calculator", "."))
    # print(get_files_info("calculator", "pkg"))
    # print(get_files_info("calculator", "/bin"))
    # print(get_files_info("calculator", "../"))

    # print(get_file_content("calculator", "lorem.txt"))
    # print(get_file_content("calculator", "main.py"))
    # print(get_file_content("calculator", "pkg/calculator.py"))
    # print(get_file_content("calculator", "/bin/cat"))

    # print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    # print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    # print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

    print(1)
    print(run_python_file("calculator", "main.py"))
    print(2)
    print(run_python_file("calculator", "tests.py"))
    print(3)
    print(run_python_file("calculator", "../main.py"))
    print(4)
    print(run_python_file("calculator", "nonexistent.py"))
    pass