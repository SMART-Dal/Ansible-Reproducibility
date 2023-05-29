# Reproducibility smell detector
This code tries to find the coding smells from the ansible scripts that can lead to possible reproducibility issues.

In the code the parser first reads the given ansible script and creates an object from the playbook and its tasks and for each task it checks for the smells.

# Content
- **`script_extractor.py`**: This script tries to search for 'ansible' files or project that has ansible scripts on Github.
 -- Provide your GITHUB_ACCESS_TOKEN, and it will print the path of the repository.
  
- **`smell_detection.py`**: This scripts consists of the smell detection functions.
each function is trying to detect one smell according to the rules specified and provides a message.

- **`parser.py`**: 
- This scripts reads a .yml file (ansible script).
- checks for the smells for each task on the script.
- creates an output csv file with messages for each task smell.


# Run the program
1- on line 133 of `parser.py` file provide the path to the ansible script you want to check.
2- on line 188 of `parser.py` file provide the output file name you want.

Then just navigate to the project directory and run the `parser.py`  -- `python3 parser.py` 
