import yaml
from yaml import SafeLoader


# checks if a task uses the shell, service,
# systemd modules and returns a message indicating which module was used
def check_task_for_shell_service_systemd(task):
    modules_to_check = ['shell', 'service', 'systemd']
    messages = []

    for t in task:
        for module in modules_to_check:
            if module in t:
                if module == 'shell':
                    messages.append(f"Task '{t['name']}' uses the shell module.")
                elif module == 'service':
                    messages.append(f"Task '{t['name']}' uses the service module.")
                elif module == 'systemd' and 'state' in t['systemd']:
                    if t['systemd']['state'] == 'reloaded':
                        messages.append(f"Task '{t['name']}' uses the systemd module with state 'reloaded'.")
                    else:
                        messages.append(
                            f"Task '{t['name']}' uses the systemd module with state '{t['systemd']['state']}'.")

    if messages:
        return '\n'.join(messages)
    else:
        return "No tasks were found that use the shell, service, or systemd modules with a state other than 'reloaded'."


# checks if a task uses one of the supported package installers
# and returns a message indicating which installer was used
def check_task_for_package_installer(task):
    package_installers_to_check = ['apt', 'apt-get', 'yum', 'dnf', 'pacman', 'apk']
    messages = []

    for t in task:
        for installer in package_installers_to_check:
            if installer in t:
                messages.append(f"Task '{t['name']}' uses the {installer} package installer.")

    if messages:
        return '\n'.join(messages)
    else:
        return "No tasks were found that use a package installer."


# checks if a task installs or updates packages and returns a message indicating
# whether the task installs the latest packages, updates packages, or installs specific packages.
def check_task_for_outdated_package(task):
    package_installers_to_check = [
        {'name': 'apt', 'latest_state': 'latest', 'update_actions': ['upgrade', 'update_cache']},
        {'name': 'yum', 'latest_state': 'latest', 'update_actions': []},
        {'name': 'dnf', 'latest_state': 'latest', 'update_actions': []},
        {'name': 'pacman', 'latest_state': None, 'update_actions': []},
        {'name': 'apk', 'latest_state': None, 'update_actions': []}
    ]
    messages = []

    for t in task:
        for installer in package_installers_to_check:
            if installer['name'] in t:
                if installer['latest_state'] and 'state' in t[installer['name']] and t[installer['name']]['state'] == installer['latest_state']:
                    messages.append(f"Task '{t['name']}' uses {installer['name']} to install the latest packages.")
                elif any(action in t[installer['name']] for action in installer['update_actions']):
                    messages.append(f"Task '{t['name']}' uses {installer['name']} to update packages.")
                else:
                    messages.append(f"Task '{t['name']}' uses {installer['name']} to install specific packages.")

    if messages:
        return '\n'.join(messages)
    else:
        return "No tasks were found that install packages."


# checks if a task violates idempotency by executing a command,
# installing or upgrading packages, or updating the package cache.
def check_task_for_idempotency(task):
    messages = []
    idempotency_violations = [
        ('command', "Task '{name}' violates idempotency because it executes a command."),
        ('shell', "Task '{name}' violates idempotency because it executes a command."),
        ('raw', "Task '{name}' violates idempotency because it executes a command."),
        ('script', "Task '{name}' violates idempotency because it executes a command."),
        ('win_command', "Task '{name}' violates idempotency because it executes a command."),
        ('win_shell', "Task '{name}' violates idempotency because it executes a command."),
        ('apt', "Task '{name}' violates idempotency because it installs or upgrades packages with apt."),
        ('yum', "Task '{name}' violates idempotency because it installs or upgrades packages with yum."),
        ('dnf', "Task '{name}' violates idempotency because it installs packages with dnf."),
        ('pacman', "Task '{name}' violates idempotency because it installs packages with pacman.")
    ]

    for t in task:
        for component, message in idempotency_violations:
            if component in t:
                if component == 'command' or component == 'shell' or component == 'raw' or component == 'script' or component == 'win_command' or component == 'win_shell':
                    messages.append(message.format(name=t['name']))
                elif 'state' in t[component] and t[component]['state'] == 'latest':
                    messages.append(message.format(name=t['name']))
                elif 'upgrade' in t[component] or 'update_cache' in t[component] or 'check_update' in t[component]:
                    messages.append(message.format(name=t['name']))

    if messages:
        return '\n'.join(messages)
    else:
        return "No tasks were found that violate idempotency."


# checks if a task installs a version-specific package
def check_task_for_version_specific_package(task):
    messages = []
    package_managers = [
        {'name': 'apt', 'version_key': 'version'},
        {'name': 'yum', 'version_key': 'version'},
        {'name': 'dnf', 'version_key': 'version'},
        {'name': 'pacman', 'version_key': 'version'},
        {'name': 'apk', 'version_key': 'version'},
    ]

    for t in task:
        for pm in package_managers:
            if pm['name'] in t:
                if pm['version_key'] in t[pm['name']]:
                    messages.append(f"Task '{t['name']}' uses {pm['name']} to install a specific version of a package.")

    if messages:
        return '\n'.join(messages)
    else:
        return "No tasks were found that install version-specific packages."


# checks if a task uses the hardware specific commands
def check_task_for_hardware_specific_commands(task):
    messages = []

    hardware_commands = ['lspci', 'lshw', 'lsblk', 'fdisk', 'parted', 'ip', 'ifconfig', 'route']

    for t in task:
        for component in ['command', 'shell', 'raw']:
            if component in t and any(hc in t[component] for hc in hardware_commands):
                if any(hc in t[component] for hc in ['lspci', 'lshw']):
                    messages.append(f"Task '{t['name']}' uses a hardware-specific command that may not be portable.")
                elif any(hc in t[component] for hc in ['lsblk', 'fdisk', 'parted']):
                    messages.append(f"Task '{t['name']}' uses a disk management command that may not be portable.")
                elif any(hc in t[component] for hc in ['ip', 'ifconfig', 'route']):
                    messages.append(f"Task '{t['name']}' uses a network management command that may not be portable.")

    if messages:
        return '\n'.join(messages)
    else:
        return "No tasks were found that use hardware-specific commands."


# checks if a task uses the software specific commands
def check_task_for_software_specific_commands(task):
    software_commands = ['npm', 'pip', 'docker', 'kubectl']
    messages = []

    for t in task:
        if 'command' in t or 'shell' in t or 'raw' in t:
            for command in software_commands:
                if command in t['command']:
                    messages.append(f"Task '{t['name']}' uses a {command} command that may not be portable.")
                    break

    if messages:
        return '\n'.join(messages)
    else:
        return "No tasks were found that use software-specific commands."


# checks if a task has any assumption on environment like the OS or distribution
def check_task_for_environment_assumptions(task):
    messages = []

    for t in task:
        if 'vars' in t:
            for var in t['vars']:
                if 'ansible_distribution' in var:
                    messages.append(
                        f"Task '{t['name']}' assumes the running environment is {var['ansible_distribution']}.")
                if 'ansible_os_family' in var:
                    messages.append(
                        f"Task '{t['name']}' assumes the operating system family is {var['ansible_os_family']}.")
        if 'when' in t:
            if 'ansible_distribution' in t['when']:
                messages.append(
                    f"Task '{t['name']}' assumes the running environment is {t['when']['ansible_distribution']}.")
            if 'ansible_os_family' in t['when']:
                messages.append(
                    f"Task '{t['name']}' assumes the operating system family is {t['when']['ansible_os_family']}.")

    if messages:
        return '\n'.join(messages)
    else:
        return "No tasks were found that make assumptions about the running environment."


# checks if a task has missing dependencies
def check_task_for_missing_dependencies(task):
    messages = []

    for t in task:
        if 'name' in t:
            if 'msg' in t:
                if 'dependencies are missing' in t['msg']:
                    messages.append(f"Task '{t['name']}' has missing dependencies: {t['msg']}")
            elif 'failed' in t:
                if 'Dependency not found' in t['msg']:
                    messages.append(f"Task '{t['name']}' has missing dependencies: {t['msg']}")

    if messages:
        return '\n'.join(messages)
    else:
        return "No tasks were found that have missing dependencies."


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


def parse_playbook(file_path):
    tasks = []

    with open(file_path, 'r') as f:
        playbook = yaml.safe_load(f)

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

            task = AnsibleTask(name, hosts, remote_user, gather_facts, become, become_user,
                               become_method, check_mode, ignore_errors, max_fail_percentage, no_log,
                               order, serial, strategy, tags, vars, vars_files, when)

            for step in play['tasks']:
                task_name = step.get('name', '')
                module = list(step.keys())[1]
                args = step[module]

                task.add_task(task_name, module, args)

            tasks.append(task)

    return tasks


with open('install_and_configure.yml') as f:
    # data = yaml.load(f, Loader=SafeLoader)
    data = list(yaml.load_all(f, Loader=SafeLoader))
    tasks = data[0][0]['tasks']
    # tasks = parse_playbook('/home/ghazal/prengdl-reproduce/install_and_configure.yml')

for task in tasks:
    print(check_task_for_shell_service_systemd(task=task))
    print(check_task_for_package_installer(task=task))
    print(check_task_for_outdated_package(task=task))
    print(check_task_for_idempotency(task=task))
    print(check_task_for_version_specific_package(task=task))
    print(check_task_for_hardware_specific_commands(task=task))
    print(check_task_for_software_specific_commands(task=task))
    print(check_task_for_environment_assumptions(task=task))
    print(check_task_for_missing_dependencies(task=task))

    # print(task.to_dict())
