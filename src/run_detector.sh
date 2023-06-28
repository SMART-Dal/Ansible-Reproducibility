#!/bin/bash

# List of file or repositories absolute paths to be passed as arguments
file_paths=(
    "/home/ghazal/Ansible-Reproducibility/test/testScripts/Repository1"
    "/home/ghazal/Ansible-Reproducibility/test/testScripts/Repository2"
    "/home/ghazal/Ansible-Reproducibility/test/testScripts/Repository3"
)

# Iterate over each file path and run the command
for file_path in "${file_paths[@]}"; do
    python detector.py "$file_path"
done
