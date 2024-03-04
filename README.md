# A study on reproducibility smells
This study, first, identifies such programming practices
that we refer to as **reproducibility smells** by conducting a comprehensive multi-vocal review. We implement a
tool viz. **REDUSE** to identify reproducibility smells in Ansible scripts. Furthermore, we carry out an empirical
study to reveal the proliferation of reproducibility smells in open-source projects and explore correlation and
co-occurrence relationships among them.

## REDUCE - a reproducibility smells detection tool
The tool is designed to detect reproducibility smells in Ansible scripts.
You can provide your ansible script in `.yml` format and get output of the tool as a `csv` file containing task name, task number, smell name, reason of having the smell on  the task.

### Build/Configure
- This tool requires Python 3.8+
- Install the packages from `requirements.txt`

### Run the tool
Run the `detector.py` file in the `src` folder with the path to your desired Ansible yaml file.
```shell
python detector.py '/path/to/file/folder
```
Or, add the path to the desired ansible files or repositories to the script and then execute
```shell
/bin/bash run_detector.sh
```

#### Example
After cloning this repository, you can use the repositories provided in the test/testScripts as sample script to try the tool. Choose one of the repositories, you can either run all the scripts in the repository at once by providing the full path of the repository or you can run just for one script by providing the path to that specific script. Navigate to the source code folder in your terminal and use this command: `python detector.py /path/to/file/folder` or optionally you can provide path to the desired output directory as well `python detector.py /path/to/input/file/folder /path/to/output/folder`.

![image](https://github.com/SMART-Dal/Ansible-Reproducibility/assets/36522329/6ac58f18-4817-4d21-a574-32a19e3337d5)

You may find the output of the command in the `src/output/<folder name>`. This repository will contain 2 versions of .csv files for each script you ran.
- v1.csv file contain Repository Name,File Name,Line Number,Task Name,Smell Name,Smell Description. it checks every 6 smells for each task.
- v2.csv file contains the task name and smell name and it shows if it is present in the task or not. if the value of the smell column is none it means that the task does not have the smell.

![image](https://github.com/SMART-Dal/Ansible-Reproducibility/assets/36522329/23ee2a9c-0ff7-497f-8e9d-8e8497fe6a47)

## Replication Package
### Manual validation
This folder contains the repositories used for manual validation of the tool. In each folder, for each script we have `manual.csv`(smells detected by reviewers) file and `cleaned.csv`(smells detected by tool) file.

### MLR
This folder contains all the files regarding multi-vocal literature review.

### Reproducibility smell examples
This file contains the code for the example scenarios mentioned in the category in the paper.

### Ansible galaxy issues.pdf
### Qualitative analysis sheets
These files contains the issues extracted from the top 8 ansible galaxy repositories that mapped to the reproducibility smells.
### REDUSE - Tool for detecting Reproducibility Smells
**`src`**:
- **`extraction`**:
  - **`extracted_repos`**: 
      This folder contains text files. 
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
  This folder contains all the detection results on the scripts.

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
  This folder contains the original ansible scripts from the ansible galaxy and ansible-oci-collection.
- **`unit_test`**:
  This folder contains the unit-tests for the smell_detection functions.
