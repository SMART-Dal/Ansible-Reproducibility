import yaml
from yaml import SafeLoader


def check_task_for_shell_service_systemd(task):
    messages = []

    for t in task:
        if 'shell' in t:
            messages.append(f"Task '{t['name']}' uses the shell module.")
        elif 'service' in t:
            messages.append(f"Task '{t['name']}' uses the service module.")
        elif 'systemd' in t and 'state' in t['systemd']:
            if t['systemd']['state'] == 'reloaded':
                messages.append(f"Task '{t['name']}' uses the systemd module with state 'reloaded'.")
            else:
                messages.append(f"Task '{t['name']}' uses the systemd module with state '{t['systemd']['state']}'.")

    if messages:
        return '\n'.join(messages)
    else:
        return "No tasks were found that use the shell, service, or systemd modules with a state other than 'reloaded'."


def check_task_for_package_installer(task):
    messages = []

    for t in task:
        if 'apt' in t or 'apt-get' in t:
            messages.append(f"Task '{t['name']}' uses the apt or apt-get package installer.")
        elif 'yum' in t:
            messages.append(f"Task '{t['name']}' uses the yum package installer.")
        elif 'dnf' in t:
            messages.append(f"Task '{t['name']}' uses the dnf package installer.")
        elif 'pacman' in t:
            messages.append(f"Task '{t['name']}' uses the pacman package installer.")
        elif 'apk' in t:
            messages.append(f"Task '{t['name']}' uses the apk package installer.")

    if messages:
        return '\n'.join(messages)
    else:
        return "No tasks were found that use a package installer."


def check_task_for_outdated_package(task):
    messages = []

    for t in task:
        if 'apt' in t:
            if 'upgrade' in t['apt'] or 'update_cache' in t['apt']:
                messages.append(f"Task '{t['name']}' uses apt to update packages.")
            elif 'state' in t['apt'] and t['apt']['state'] == 'latest':
                messages.append(f"Task '{t['name']}' uses apt to install the latest packages.")
            else:
                messages.append(f"Task '{t['name']}' uses apt to install specific packages.")
        elif 'yum' in t:
            if 'state' in t['yum'] and t['yum']['state'] == 'latest':
                messages.append(f"Task '{t['name']}' uses yum to install the latest packages.")
            else:
                messages.append(f"Task '{t['name']}' uses yum to install specific packages.")
        elif 'dnf' in t:
            if 'state' in t['dnf'] and t['dnf']['state'] == 'latest':
                messages.append(f"Task '{t['name']}' uses dnf to install the latest packages.")
            else:
                messages.append(f"Task '{t['name']}' uses dnf to install specific packages.")
        elif 'pacman' in t:
            messages.append(f"Task '{t['name']}' uses pacman to install packages.")
        elif 'apk' in t:
            messages.append(f"Task '{t['name']}' uses apk to install packages.")

    if messages:
        return '\n'.join(messages)
    else:
        return "No tasks were found that install packages."


def check_task_for_idempotency(task):
    messages = []

    for t in task:
        if 'command' in t or 'shell' in t or 'raw' in t or 'script' in t or 'win_command' in t or 'win_shell' in t:
            messages.append(f"Task '{t['name']}' violates idempotency because it executes a command.")
        elif 'apt' in t:
            if 'state' in t['apt'] and t['apt']['state'] == 'latest':
                messages.append(f"Task '{t['name']}' violates idempotency because it installs the latest packages.")
            elif 'upgrade' in t['apt']:
                messages.append(f"Task '{t['name']}' violates idempotency because it upgrades packages.")
        elif 'yum' in t:
            if 'state' in t['yum'] and t['yum']['state'] == 'latest':
                messages.append(f"Task '{t['name']}' violates idempotency because it installs the latest packages.")
            elif 'update_cache' in t['yum'] or 'check_update' in t['yum']:
                messages.append(f"Task '{t['name']}' violates idempotency because it updates the package cache.")
        elif 'dnf' in t:
            if 'state' in t['dnf'] and t['dnf']['state'] == 'latest':
                messages.append(f"Task '{t['name']}' violates idempotency because it installs the latest packages.")
        elif 'pacman' in t:
            if 'state' in t['pacman'] and t['pacman']['state'] == 'latest':
                messages.append(f"Task '{t['name']}' violates idempotency because it installs the latest packages.")
    if messages:
        return '\n'.join(messages)
    else:
        return "No tasks were found that violates idempotency."


def check_task_for_version_specific_package(task):
    messages = []

    for t in task:
        if 'apt' in t:
            if 'version' in t['apt']:
                messages.append(f"Task '{t['name']}' uses apt to install a specific version of a package.")
        elif 'yum' in t:
            if 'version' in t['yum']:
                messages.append(f"Task '{t['name']}' uses yum to install a specific version of a package.")
        elif 'dnf' in t:
            if 'version' in t['dnf']:
                messages.append(f"Task '{t['name']}' uses dnf to install a specific version of a package.")
        elif 'pacman' in t:
            if 'version' in t['pacman']:
                messages.append(f"Task '{t['name']}' uses pacman to install a specific version of a package.")
        elif 'apk' in t:
            if 'version' in t['apk']:
                messages.append(f"Task '{t['name']}' uses apk to install a specific version of a package.")

    if messages:
        return '\n'.join(messages)
    else:
        return "No tasks were found that install version-specific packages."


def check_task_for_hardware_specific_commands(task):
    messages = []

    for t in task:
        if 'command' in t or 'shell' in t or 'raw' in t:
            if 'lspci' in t['command'] or 'lshw' in t['command']:
                messages.append(f"Task '{t['name']}' uses a hardware-specific command that may not be portable.")
            elif 'lsblk' in t['command'] or 'fdisk' in t['command'] or 'parted' in t['command']:
                messages.append(f"Task '{t['name']}' uses a disk management command that may not be portable.")
            elif 'ip' in t['command'] or 'ifconfig' in t['command'] or 'route' in t['command']:
                messages.append(f"Task '{t['name']}' uses a network management command that may not be portable.")

    if messages:
        return '\n'.join(messages)
    else:
        return "No tasks were found that use hardware-specific commands."


def check_task_for_software_specific_commands(task):
    messages = []

    for t in task:
        if 'command' in t or 'shell' in t or 'raw' in t:
            if 'npm' in t['command']:
                messages.append(f"Task '{t['name']}' uses an NPM command that may not be portable.")
            elif 'pip' in t['command']:
                messages.append(f"Task '{t['name']}' uses a pip command that may not be portable.")
            elif 'docker' in t['command']:
                messages.append(f"Task '{t['name']}' uses a Docker command that may not be portable.")
            elif 'kubectl' in t['command']:
                messages.append(f"Task '{t['name']}' uses a kubectl command that may not be portable.")

    if messages:
        return '\n'.join(messages)
    else:
        return "No tasks were found that use software-specific commands."


def check_task_for_environment_assumptions(task):
    messages = []

    for t in task:
        if 'vars' in t:
            for var in t['vars']:
                if 'ansible_distribution' in var:
                    messages.append(f"Task '{t['name']}' assumes the running environment is {var['ansible_distribution']}.")
                if 'ansible_os_family' in var:
                    messages.append(f"Task '{t['name']}' assumes the operating system family is {var['ansible_os_family']}.")
        if 'when' in t:
            if 'ansible_distribution' in t['when']:
                messages.append(f"Task '{t['name']}' assumes the running environment is {t['when']['ansible_distribution']}.")
            if 'ansible_os_family' in t['when']:
                messages.append(f"Task '{t['name']}' assumes the operating system family is {t['when']['ansible_os_family']}.")

    if messages:
        return '\n'.join(messages)
    else:
        return "No tasks were found that make assumptions about the running environment."


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


# tasks = parse_playbook('/home/ghazal/prengdl-reproduce/install_and_configure.yml')

with open('install_and_configure.yml') as f:
    # data = yaml.load(f, Loader=SafeLoader)
    data = list(yaml.load_all(f, Loader=SafeLoader))
    tasks = data[0][0]['tasks']


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











