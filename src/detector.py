import src.smell_detection as detector
import src.parser as parser
import csv


def perform_smell_detection_for_task(task):
    smell_name_description = {}

    idempotency = detector.check_task_for_idempotency(task=task)
    smell_name_description['Idempotency'] = idempotency

    version_specific = detector.check_task_for_version_specific_package(task=task)
    smell_name_description['Version Specific Installation'] = version_specific

    outdated_dependency = detector.check_task_for_outdated_package(task=task)
    smell_name_description['Outdated Dependencies'] = outdated_dependency

    missing_dependency = detector.check_task_for_missing_dependencies(task=task)
    smell_name_description['Missing Dependencies'] = missing_dependency

    hardware_specific = detector.check_task_for_hardware_specific_commands(task=task)
    smell_name_description['Hardware Specific Commands'] = hardware_specific

    assumption = detector.check_task_for_environment_assumptions(task=task) \
                 + ' ' + detector.check_task_for_software_specific_commands(task=task)
    smell_name_description['Assumption about Environment'] = assumption

    broken_dependency = detector.check_task_for_broken_dependency(task=task)
    smell_name_description['Broken Dependency Chain'] = broken_dependency

    return smell_name_description


def get_task_name(task, task_index):
    try:
        task_name = task['name']
    except KeyError:
        task_name = 'Task ' + str(task_index)
    return task_name


def get_tasks_line_numbers(input_file):
    task_line_numbers = []
    line_number = 0
    # Open the file and get the task line numbers
    with open(input_file) as file:
        for line in file:
            line_number += 1
            line = line.strip()
            if line.startswith('-'):
                task_line_numbers.append(line_number)
        file.close()
    return task_line_numbers


def main_method():
    # 1- Get the input script file path from the user
    # Make a test directory within the project directory and put the repository on that directory
    input_file = input("Enter the path to your input file script: ")

    # Create lists to generate output file
    csv_columns = ['Task name', 'Idempotency', 'Version specific installation', 'Outdated dependencies',
                   'Missing dependencies', 'Assumption about environment', 'Hardware specific commands',
                   'Broken Dependency']
    output_tasks = []

    new_csv_columns = ['Repository Name', 'File Name', 'Line Number', 'Task Name', 'Smell Name',
                       'Smell Description']
    new_output_tasks = []

    # Get file name and repository name for output
    file_name = input_file.split('/')[-1]
    repository_name = input_file.split('/')[0:-1]

    # 2- Create task lines list
    task_line_numbers = get_tasks_line_numbers(input_file)

    # 3- Open playbook file and extract tasks
    with open(input_file) as f:

        # Get the parsed tasks as a dictionary
        tasks = parser.get_parsed_tasks(input_file=f)
        task_number = 0
        for task in tasks:
            task_number += 1
            smell_name_description = perform_smell_detection_for_task(task=task)
            task_name = get_task_name(task=task, task_index=task_number)

            # Store task smells in a dictionary
            task_smells = {'Task name': task_name,
                           'Idempotency': smell_name_description['Idempotency'],
                           'Version specific installation': smell_name_description['Version Specific Installation'],
                           'Outdated dependencies': smell_name_description['Outdated Dependencies'],
                           'Missing dependencies': smell_name_description['Missing Dependencies'],
                           'Assumption about environment': smell_name_description['Assumption about Environment'],
                           'Hardware specific commands': smell_name_description['Hardware Specific Commands'],
                           'Broken Dependency': smell_name_description['Broken Dependency Chain']}
            output_tasks.append(task_smells)

            for smell_name in smell_name_description.keys():
                new_task_smells = {
                    'Repository Name': repository_name,
                    'File Name': file_name,
                    'Line Number': task_line_numbers[task_number],
                    'Task Name': task_name,
                    'Smell Name': smell_name,
                    'Smell Description': smell_name_description.get(smell_name),
                }
                new_output_tasks.append(new_task_smells)

            # Output file name
            output_file = '/home/ghazal/prengdl-reproduce/outputs/' + input_file.split('/')[-1] + '_smells_v1.csv'
            output_file2 = '/home/ghazal/prengdl-reproduce/outputs/' + input_file.split('/')[-1] + '_smells_v2.csv'

            # Write task smells to CSV file
            with open(output_file, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=new_csv_columns)
                writer.writeheader()
                writer.writerows(new_output_tasks)
            file.close()

            with open(output_file2, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=csv_columns)
                writer.writeheader()
                writer.writerows(output_tasks)
            file.close()


if __name__ == "__main__":
    main_method()
