import os

import src.smell_detection as detector
import src.parser as parser
from results import write_results_csv


def main_method():
    try:
        # 1- Get the input script file path from the user
        # Make a test directory within the project directory and put the repository on that directory
        input_file = input("Enter the path to your input file script: ")

        # Check if the input file exists
        if not os.path.isfile(input_file):
            print("Error: The specified input file does not exist.")
            return

        # 3- Open playbook file and extract tasks
        with open(input_file) as f:
            # Get the parsed tasks as a dictionary
            tasks = parser.get_parsed_tasks(input_file=f)
            task_number = 0
            for task in tasks:
                task_number += 1
                output_tasks, new_output_tasks = detector.detect_smells(task, task_number, input_file)
                write_results_csv(output_tasks, new_output_tasks, input_file)
    except FileNotFoundError:
        print("Error: File not found.")
    except Exception as e:
        print("An error occurred:", str(e))


if __name__ == "__main__":
    main_method()
