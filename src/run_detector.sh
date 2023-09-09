#!/bin/bash

# List of file or repositories absolute paths to be passed as arguments
file_paths=()

# Iterate over each file path and run the command
for file_path in "${file_paths[@]}"; do
    python detector.py "$file_path"
done
