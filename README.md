# Reproducibility smell detector
This tool detects programming practices, referred to as productivity smells, in Ansible scripts that can lead to reproducibility issues.

The tool has a parser that reads the given Ansible script and creates a code model object from the playbook.
The code model captures the Ansible tasks and their properties.
Finally, the smell detector checks for the presence of smells by analyzing the source code model.

## Contents
- **`script_extractor.py`**: This script tries to search for 'ansible' files or project that has ansible scripts on Github.
 -- Provide your GITHUB_ACCESS_TOKEN, and it will print the path of the repository.
  
- **`smell_detection.py`**: This scripts consists of the smell detection functions.
each function is trying to detect one smell according to the rules specified and provides a message.

- **`parser.py`**: 
- This scripts reads a .yml file (ansible script).
- checks for the smells for each task on the script.
- creates an output csv file with messages for each task smell.


## Run the program

### Build/Configure
- This tool requires Python 3.8+
- Install the packages from `requirements.txt`

### Run
Run the `parser.py` file with the path to your desired Ansible yaml file.
