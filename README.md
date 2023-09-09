# Reproducibility smell detector
This tool detects programming practices, referred to as productivity smells, in Ansible scripts that can lead to reproducibility issues.

The tool has a parser that reads the given Ansible script and creates a code model object from the playbook.
The code model captures the Ansible tasks and their properties.
Finally, the smell detector checks for the presence of smells by analyzing the source code model.
As an output you will get 2 csv files in output repository with the name of the input script. 

## Contents
**`Replication Package`**:
- **`Manual validation`**:
This directory contains the repositories used for manual validation of the tool.
  In each directory, for each script we have manual.csv(smells detected by reviewers) file and cleaned.csv(smells detected by tool) file.
- **`MLR`**:
This directory contains all the files regarding grey literature review.
- **`smell categories example`**: 
This file contains the code for the example scenarios mentioned in the category in the paper.

**`src`**:
- **`extraction`**:
  - **`extracted_repos`**: 
      This directory contains text files. 
      Each text file contains the links extracted from 9 categories of the 
      ansible galaxy top 100 of the most-downloaded repositories after applying criteria check on the github repository.
  - **`script`**:
      - **`criteria_check.py`**:
        This script applies criterias on the github links. 
        5 stars, 50 commits, last commit not older than 1 year ago.
      - **`link_extractor.py`**:
        This script extracts github links from the given url. 
        used for extracting the projects from the ansible galaxy.
      - **`script_extractor.py`**:
        This script gets a github link and extracts the .yml files of the repository.

- **`output`**:
  This directory contains all the detection results on the scripts.

- **`detector.py`**: 
    - This scripts contains the main logic of the tool.
    - It gets the path to the ansible script file and parse it.
    - using parsed tasks it detects the smells for each task.
- **`parser.py`**: 
    - This scripts parses a given ansible script and returns a dictionary containing the tasks of the script.
- **`smell_detection.py`**: 
    - This scripts consists of the smell detection functions. 
      each function is trying to detect one smell according to the rules specified and provides a message.
- **`results.py`**:
    - This script creates 2 csv files in 2 formats as output. 
    
**`test`**:
- **`testScripts`**:
  This directory contains the original ansible scripts from the ansible galaxy and ansible-oci-collection.
- **`unit_test`**:
  This directory contains the unit-tests for the smell_detection functions.

### Build/Configure
- This tool requires Python 3.8+
- Install the packages from `requirements.txt`

## Run the program

### Run
Navigate to the src directory of the project.

Run the `detector.py` file with the path to your desired Ansible yaml file 
`python detector.py '/path/to/file/directory`
or 
Add the path to the desired ansible files or repositories to the script and then 
Run `/bin/bash run_detector.sh`
