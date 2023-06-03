import csv

import yaml
from yaml import SafeLoader

from Src import smell_detection as detector


# Ansible class Object with attributes
class AnsibleTask:
    def __init__(self, name, hosts, remote_user=None, gather_facts=None, become=None, become_user=None,
                 become_method=None, check_mode=None, ignore_errors=None, max_fail_percentage=None, no_log=None,
                 order=None, serial=None, strategy=None, tags=None, vars=None, vars_files=None, when=None, tasks=None):
        self.name = name
        self.hosts = hosts
        self.remote_user = remote_user
        self.gather_facts = gather_facts
        self.become = become
        self.become_user = become_user
        self.become_method = become_method
        self.check_mode = check_mode
        self.ignore_errors = ignore_errors
        self.max_fail_percentage = max_fail_percentage
        self.no_log = no_log
        self.order = order
        self.serial = serial
        self.strategy = strategy
        self.tags = tags
        self.vars = vars or {}
        self.vars_files = vars_files or []
        self.when = when
        self.tasks = tasks or []

    def add_task(self, name, module, args=None):
        task = {
            'name': name,
            module: {
                'args': args or {}
            }
        }
        self.tasks.append(task)

    def to_dict(self):
        result = {
            'name': self.name,
            'hosts': self.hosts,
            'vars': self.vars,
            'tasks': self.tasks
        }

        # Add optional attributes if they exist
        if self.remote_user:
            result['remote_user'] = self.remote_user
        if self.gather_facts is not None:
            result['gather_facts'] = self.gather_facts
        if self.become is not None:
            result['become'] = self.become
        if self.become_user:
            result['become_user'] = self.become_user
        if self.become_method:
            result['become_method'] = self.become_method
        if self.check_mode is not None:
            result['check_mode'] = self.check_mode
        if self.ignore_errors is not None:
            result['ignore_errors'] = self.ignore_errors
        if self.max_fail_percentage is not None:
            result['max_fail_percentage'] = self.max_fail_percentage
        if self.no_log is not None:
            result['no_log'] = self.no_log
        if self.order is not None:
            result['order'] = self.order
        if self.serial is not None:
            result['serial'] = self.serial
        if self.strategy:
            result['strategy'] = self.strategy
        if self.tags:
            result['tags'] = self.tags
        if self.vars_files:
            result['vars_files'] = self.vars_files
        if self.when:
            result['when'] = self.when

        return result


# Parse Ansible Playbook
def parse_playbook(file_path):
    tasks = []

    with open(file_path, 'r') as f:
        playbook = yaml.safe_load(f)

        # Get attribute values from the playbook
        for play in playbook:
            name = play.get('name', '')
            hosts = play.get('hosts', '')

            remote_user = play.get('remote_user', None)
            gather_facts = play.get('gather_facts', None)
            become = play.get('become', None)
            become_user = play.get('become_user', None)
            become_method = play.get('become_method', None)
            check_mode = play.get('check_mode', None)
            ignore_errors = play.get('ignore_errors', None)
            max_fail_percentage = play.get('max_fail_percentage', None)
            no_log = play.get('no_log', None)
            order = play.get('order', None)
            serial = play.get('serial', None)
            strategy = play.get('strategy', None)
            tags = play.get('tags', None)
            vars_files = play.get('vars_files', None)
            when = play.get('when', None)

            vars = play.get('vars', None)

            # Create Ansible task object based on attributes and values
            task = AnsibleTask(name, hosts, remote_user, gather_facts, become, become_user,
                               become_method, check_mode, ignore_errors, max_fail_percentage, no_log,
                               order, serial, strategy, tags, vars, vars_files, when)

            # Add each step to the task object
            for step in play['tasks']:
                task_name = step.get('name', '')
                module = list(step.keys())[1]
                args = step[module]

                task.add_task(task_name, module, args)

            tasks.append(task)

    return tasks


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


def get_parsed_tasks(data):
    try:
        tasks = data[0][0]['tasks']
    except KeyError:
        tasks = data[0]
    return tasks

    # Create lists to generate output file
    output_tasks = []
    csv_columns = ['Task name', 'Idempotency', 'Version specific installation', 'Outdated dependencies',
                   'Missing dependencies', 'Assumption about environment', 'Hardware specific commands',
                   'Broken Dependency']

    new_csv_columns = ['Repository Name', 'File Name', 'Line Number', 'Task Name', 'Smell Name', 'Smell Description']

    smell_name_description = {}
    file_name = input_file.split('/')[-1]
    repository_name = input_file.split('/')[0:-1]
    new_output_tasks = []

    # Parse playbook into tasks
    # tasks = parse_playbook('/home/ghazal/prengdl-reproduce/install_and_configure.yml')


def perform_smell_detection_for_task(task):
    smell_name_description = {}

    idempotency = detector.check_task_for_shell_service_systemd(task=task) + \
                  ' ' + detector.check_task_for_idempotency(task=task) + \
                  ' ' + detector.check_task_for_package_installer(task=task)
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


def main_method():
    # 1- Get the input script file path from the user
    # Make a test directory within the project directory and put the repository on that directory
    input_file = input("Enter the Relative path to your input file script: ")

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
        data = list(yaml.load_all(f, Loader=SafeLoader))

        # Get the parsed tasks as a dictionary
        tasks = get_parsed_tasks(data=data)
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
            output_file = input_file.split('/')[-1] + '_smells_v1.csv'
            output_file2 = input_file.split('/')[-1] + '_smells_v2.csv'

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
