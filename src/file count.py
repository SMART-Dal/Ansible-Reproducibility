import os

def count_files_in_directory(path):
    file_count = 0

    for root, dirs, files in os.walk(path):
        for file in files:
            file_count += 1

    return file_count

# Input: Provide the path to the directory you want to count files in
repository_path = '/path/to/your/repository'

try:
    file_count = count_files_in_directory('/home/ghazal/Ansible-Reproducibility/test/testScripts/1')
    print(f"Total number of files in {repository_path}: {file_count}")
except FileNotFoundError:
    print(f"Directory not found: {repository_path}")
except PermissionError:
    print(f"Permission denied for {repository_path}")
