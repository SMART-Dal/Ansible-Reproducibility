# checks if a task uses the shell, service,
# systemd modules and returns a message indicating which module was used
def check_task_for_shell_service_systemd(task):
    modules_to_check = ['shell', 'service', 'systemd']
    messages = []
    task_name = task['name']

    for t in task:
        for module in modules_to_check:
            if module in t:
                if module == 'shell':
                    messages.append(f"Task '{task_name}' uses the shell module.")
                elif module == 'service':
                    messages.append(f"Task '{task_name}' uses the service module.")
                elif module == 'systemd' and 'state' in t['systemd']:
                    if t['systemd']['state'] == 'reloaded':
                        messages.append(f"Task '{task_name}' uses the systemd module with state 'reloaded'.")
                    else:
                        messages.append(
                            f"Task '{task_name}' uses the systemd module with state '{t['systemd']['state']}'.")

    if messages:
        return '\n'.join(messages)
    else:
        return f" Task '{task_name}' has not used the shell, service, or systemd modules with a state other than 'reloaded'."


# checks if a task uses one of the supported package installers
# and returns a message indicating which installer was used
def check_task_for_package_installer(task):
    package_installers_to_check = ['apt', 'apt-get', 'yum', 'dnf', 'pacman', 'apk']
    messages = []
    task_name = task['name']

    for t in task:
        for installer in package_installers_to_check:
            if installer in t:
                messages.append(f"Task '{task_name}' uses the {installer} package installer.")

    if messages:
        return '\n'.join(messages)
    else:
        return f" Task '{task_name}' has not used a package installer."


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
    task_name = task['name']

    for t in task:
        for installer in package_installers_to_check:
            if installer['name'] in t:
                if installer['latest_state'] and 'state' in task[t].keys() and task[t]['state'] == installer['latest_state']:
                    messages.append(f"Task '{task_name}' uses {installer['name']} to install the latest packages.")
                elif 'update_cache' in task[t].keys() and any(action in task[t]['update_cache'] for action in installer['update_actions']):
                    messages.append(f"Task '{task_name}' uses {installer['name']} to update packages.")
                else:
                    messages.append(f"Task '{task_name}' uses {installer['name']} to install specific packages.")

    if messages:
        return '\n'.join(messages)
    else:
        return f" Task '{task_name}' has not install packages."


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
    task_name = task['name']

    for t in task:
        for component, message in idempotency_violations:
            if component in t:
                if component == 'command' or component == 'shell' or component == 'raw' or component == 'script' or component == 'win_command' or component == 'win_shell':
                    messages.append(message.format(name=task_name))
                elif 'state' in task[t] and task[t]['state'] == 'latest':
                    messages.append(message.format(name=task_name))
                elif 'upgrade' in task[t] or 'update_cache' in task[t] or 'check_update' in task[t]:
                    messages.append(message.format(name=task_name))

    if messages:
        return '\n'.join(messages)
    else:
        return f" Task '{task_name}' has not violated idempotency."


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
    task_name = task['name']

    for t in task:
        for pm in package_managers:
            if pm['name'] in t:
                if pm['version_key'] in task[t]:
                    messages.append(f"Task '{task_name}' uses {pm['name']} to install a specific version of a package.")

    if messages:
        return '\n'.join(messages)
    else:
        return f" Task '{task_name}' has not installed a version-specific packages."


# checks if a task uses the hardware specific commands
def check_task_for_hardware_specific_commands(task):
    messages = []

    hardware_commands = ['lspci', 'lshw', 'lsblk', 'fdisk', 'parted', 'ip', 'ifconfig', 'route']
    task_name = task['name']

    for t in task:
        for component in ['command', 'shell', 'raw']:
            if component in t and any(hc in task[t] for hc in hardware_commands):
                if any(hc in task[t] for hc in ['lspci', 'lshw']):
                    messages.append(f"Task '{task_name}' uses a hardware-specific command that may not be portable.")
                elif any(hc in task[t] for hc in ['lsblk', 'fdisk', 'parted']):
                    messages.append(f"Task '{task_name}' uses a disk management command that may not be portable.")
                elif any(hc in task[t] for hc in ['ip', 'ifconfig', 'route']):
                    messages.append(f"Task '{task_name}' uses a network management command that may not be portable.")

    if messages:
        return '\n'.join(messages)
    else:
        return f" Task '{task_name}' has not used hardware-specific commands."


# checks if a task uses the software specific commands
def check_task_for_software_specific_commands(task):
    software_commands = ['npm', 'pip', 'docker', 'kubectl']
    messages = []
    task_name = task['name']

    for t in task:
        if 'command' in t or 'shell' in t or 'raw' in t:
            for command in software_commands:
                if command in task[t]:
                    messages.append(f"Task '{task_name}' uses a {command} command that may not be portable.")
                    break

    if messages:
        return '\n'.join(messages)
    else:
        return f" Task '{task_name}' has not used software-specific commands."


# checks if a task has any assumption on environment like the OS or distribution
def check_task_for_environment_assumptions(task):
    messages = []
    task_name = task['name']

    for t in task:
        if 'vars' in t:
            for var in task[t]:
                if 'ansible_distribution' in var:
                    messages.append(
                        f"Task '{task_name}' assumes the running environment is {var['ansible_distribution']}.")
                if 'ansible_os_family' in var:
                    messages.append(
                        f"Task '{task_name}' assumes the operating system family is {var['ansible_os_family']}.")
        if 'when' in t:
            if 'ansible_distribution' in task[t]:
                messages.append(
                    f"Task '{task_name}' assumes the running environment is {task[t]['ansible_distribution']}.")
            if 'ansible_os_family' in task[t]:
                messages.append(
                    f"Task '{task_name}' assumes the operating system family is {task[t]['ansible_os_family']}.")

    if messages:
        return '\n'.join(messages)
    else:
        return f" Task '{task_name}' has not made assumptions about the running environment."


# checks if a task has missing dependencies
def check_task_for_missing_dependencies(task):
    messages = []
    task_name = task['name']

    for t in task:
        if 'name' in t:
            if 'msg' in t:
                if 'dependencies are missing' in t['msg']:
                    messages.append(f"Task '{task_name}' has missing dependencies: {t['msg']}")
            elif 'failed' in t:
                if 'Dependency not found' in t['msg']:
                    messages.append(f"Task '{task_name}' has missing dependencies: {t['msg']}")

    if messages:
        return '\n'.join(messages)
    else:
        return f" Task '{task_name}' has not missing dependencies."
