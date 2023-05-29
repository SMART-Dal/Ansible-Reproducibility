# TODO add pip to package installers
# checks if a task uses the shell, service,
# systemd modules and returns a message indicating which module was used
def check_task_for_shell_service_systemd(task_name,task):
    modules_to_check = ['shell', 'service', 'systemd']
    messages = []
    task_name = task_name

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
def check_task_for_package_installer(task_name, task):
    package_installers_to_check = ['apt', 'apt-get', 'yum', 'dnf', 'pacman', 'apk', 'pip']
    messages = []
    task_name = task_name

    for t in task:
        for installer in package_installers_to_check:
            if installer in t:
                messages.append(f"Task '{task_name}' uses the {installer} package installer.")

    if messages:
        return '\n'.join(messages)
    else:
        return f" Task '{task_name}' has not used a package installer."

# checks if a task uses one of the supported package installers
# and returns a message indicating which installer was used
def check_task_for_broken_dependency(task):
    package_installers_keys_to_check = ['apt-key', 'apt-get-key', 'yum-key', 'dnf-key', 'pacman-key', 'apk-key', 'ansible.builtin.rpm-key']
    checkers = [('fingerprint', "Task '{name}' uses fixed fingerprint which can get outdated."),
                ('id', "Task '{name}' uses fixed id which can get outdated or not correct across platfroms."),
                ('url', "Task '{name}' uses fixed url to download key which can get outdated or removed.")]
    messages = []
    task_name = task['name']

    for t in task:
        keys = task[t].keys()
        for installer_key in package_installers_keys_to_check:
            if installer_key in t:
                for checker, message in checkers:
                    if checker in keys:
                        messages.append(message.format(name=task_name))
    if messages:
        return '\n'.join(messages)
    else:
        return f" Task '{task_name}' has not used a package key installer."


# checks if a task installs or updates packages and returns a message indicating
# whether the task installs the latest packages, updates packages, or installs specific packages.
def check_task_for_outdated_package(task_name, task):
    package_installers_to_check = [
        {'name': 'apt', 'latest_state': 'latest', 'update_actions': ['upgrade', 'update_cache']},
        {'name': 'yum', 'latest_state': 'latest', 'update_actions': ['upgrade', 'update_cache']},
        {'name': 'dnf', 'latest_state': 'latest', 'update_actions': ['upgrade', 'update_cache']},
        {'name': 'pacman', 'latest_state': 'latest', 'update_actions': ['upgrade', 'update_cache']},
        {'name': 'apk', 'latest_state': 'latest', 'update_actions': ['upgrade', 'update_cache']},
        {'name': 'pip', 'latest_state': 'latest', 'update_actions': ['upgrade', 'update_cache']},
        {'name': 'apt-get', 'latest_state': 'latest', 'update_actions': ['upgrade', 'update_cache']}
    ]
    messages = []
    task_name = task_name

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
def check_task_for_idempotency(task_name, task):
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
    task_name = task_name

    for t in task:
        for component, message in idempotency_violations:
            if component in t:
                if component == 'command' or component == 'shell' or component == 'raw' or component == 'script' or component == 'win_command' or component == 'win_shell':
                    messages.append(message.format(name=task_name))
                elif 'state' in task[t] and task[t]['state'] == 'latest':
                    messages.append(message.format(name=task_name))
                elif 'upgrade' in task[t] or 'update_cache' in task[t] or 'check_update' in task[t]:
                    messages.append(message.format(name=task_name))

        if 'ansible.posix.firewalld' in t or 'community.general.ufw' in t:
            if 'state' not in task[t]:
                messages.append(f"Task '{task_name}' change the state of firewall without checking.")

        if 'file' in t or 'ansible.builtin.copy' in t or 'copy' in t or 'lineinfile' in t:
            if 'state' not in task[t]:
                messages.append(f"Task '{task_name}' change the state of file without checking.")

    if messages:
        return '\n'.join(messages)
    else:
        return f" Task '{task_name}' has not violated idempotency."


# checks if a task installs a version-specific package
def check_task_for_version_specific_package(task_name, task):
    messages = []
    package_managers = [
        {'name': 'apt', 'version_key': 'version'},
        {'name': 'yum', 'version_key': 'version'},
        {'name': 'dnf', 'version_key': 'version'},
        {'name': 'pacman', 'version_key': 'version'},
        {'name': 'apk', 'version_key': 'version'},
        {'name': 'pip', 'version_key': 'version'}
    ]
    task_name = task_name

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
def check_task_for_hardware_specific_commands(task_name, task):
    messages = []

    hardware_commands = ['lspci', 'lshw', 'lsblk', 'fdisk', 'parted', 'ip', 'ifconfig', 'route', 'fwupd', 'smbios-util',
                         'mdadm', 'megacli', 'vconfig', 'tpmtool', 'efibootmgr', 'cpufrequtils', 'sysctl', 'powertop',
                         'acpi', 'ifup', 'ifdown', 'iptables', 'mkfs', 'nvidia-settings', 'nvidia-smi', 'sg3_utils', 'multipath',
                         'mpstat', 'xinput', 'smbus-tools', 'lm-sensors']

    task_name = task_name
    for t in task:
        for component in ['command', 'shell', 'raw']:
            if component in t and any(hc in task[t] for hc in hardware_commands):

                if any(hc in task[t] for hc in ['lspci', 'lshw']):
                    messages.append(f"Task '{task_name}' uses a hardware-specific command that may not be portable.")

                elif any(hc in task[t] for hc in ['lsblk', 'fdisk', 'parted', 'mkfs', 'sg3_utils', 'multipath']):
                    messages.append(f"Task '{task_name}' uses a disk management command that may not be portable.")

                elif any(hc in task[t] for hc in ['ip', 'ifconfig', 'route', 'vconfig', 'ifup', 'ifdown', 'iptables']):
                    messages.append(f"Task '{task_name}' uses a network management command that may not be portable.")

                elif any(hc in task[t] for hc in ['fwupd', 'smbios-util']):
                    messages.append(f"Task '{task_name}' uses a BIOS firmware management command that may not be portable.")

                elif any(hc in task[t] for hc in ['mdadm', 'megacli']):
                    messages.append(f"Task '{task_name}' uses a RAID arrays management command that may not be portable.")

                elif any(hc in task[t] for hc in ['tpmtool', 'efibootmgr']):
                    messages.append(f"Task '{task_name}' uses a security management command that may not be portable.")

                elif any(hc in task[t] for hc in ['cpufrequtils', 'sysctl']):
                    messages.append(f"Task '{task_name}' uses a performance settings management command that may not be portable.")

                elif any(hc in task[t] for hc in ['nvidia-settings', 'nvidia-smi']):
                    messages.append(f"Task '{task_name}' uses a GPU settings management command that may not be portable.")

                elif any(hc in task[t] for hc in ['xinput','xrandr']):
                    messages.append(f"Task '{task_name}' uses a I/O device management command that may not be portable.")

                elif any(hc in task[t] for hc in ['smbus-tools', 'lm-sensors']):
                    messages.append(f"Task '{task_name}' uses a system management bus command that may not be portable.")

    if messages:
        return '\n'.join(messages)
    else:
        return f" Task '{task_name}' has not used hardware-specific commands."


# checks if a task uses the software specific commands
def check_task_for_software_specific_commands(task_name, task):
    software_commands = ['npm', 'pip', 'docker', 'kubectl']
    messages = []
    task_name = task_name

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
def check_task_for_environment_assumptions(task_name, task):
    messages = []
    task_name = task_name
    key_download_components = ['apt-repository', 'get-url', 'uri', 'apt-key', 'rpm-key']
    for t in task:
        if 'vars' in t or 'include_vars' in t or 'include_tasks' in t or 'when' in t:
            if 'ansible_distribution' in task[t]:
                messages.append(
                    f"Task '{task_name}' assumes a default running environment.")
            if 'ansible_os_family' in task[t]:
                messages.append(
                    f"Task '{task_name}' assumes the operating system family.")

        if 'ansible.posix.firewalld' in t or 'community.general.ufw' in t:
            if 'state' not in task[t]:
                messages.append(f"Task '{task_name}' assumes the firewall and change the state without checking.")

        if 'resolv.conf' in t:
            if 'state' not in task[t]:
                messages.append(f"Task '{task_name}' assumes that the system is using a resolv.conf file to manage DNS settings")

        if 'resolv.conf' in t:
            if 'state' not in task[t]:
                messages.append(f"Task '{task_name}' assumes that the system is using a resolv.conf file to manage DNS settings.")

        if 'ethernets' in t:
            if 'state' not in task[t]:
                messages.append(f"Task '{task_name}' changes ethenet interfaces settimgs without checking the state.")

        if 'ntp' in t:
            if 'state' not in task[t]:
                messages.append(f"Task '{task_name}' the system is using the ntp service to manage time settings and that the provided NTP servers.")

        if 'sshd_config' in t:
            if 'state' not in task[t]:
                messages.append(f"Task '{task_name}' assumes that the system is using a ssh without checking the state.")

        for key_checker in key_download_components:
            if key_checker in t:
                if 'url' in task[t]:
                    messages.append(
                        f"Task '{task_name}' assumes that the package repository is available at a specific URL structure.")
    if messages:
        return '\n'.join(messages)
    else:
        return f" Task '{task_name}' has not made assumptions about the running environment."


# checks if a task has missing dependencies
def check_task_for_missing_dependencies(task_name, task):
    messages = []
    task_name = task_name

    for t in task:
        if 'name' in t:
            if 'msg' in t:
                if 'dependencies are missing' in t['msg']:
                    messages.append(f"Task '{task_name}' has missing dependencies: {t['msg']}")

            elif 'failed' in t:
                if 'Dependency not found' in t['msg']:
                    messages.append(f"Task '{task_name}' has missing dependencies: {t['msg']}")

            elif 'failed_when' in t:
                if 'Dependency not found' in t['msg']:
                    messages.append(f"Task '{task_name}' has missing dependencies: {t['msg']}")

            elif 'file' in t or 'ansible.builtin.copy' in t:
                if 'dest' in task[t] or 'path' in task[t] or 'src' in task[t]:
                    path_list = [('dest', task[t]['dest']), ('src', task[t]['src']), ('path', task[t]['path'])]
                    for comp, path in path_list:
                        from pathlib import Path
                        if Path(str(path)).is_absolute():
                            messages.append(f"Task '{task_name}' is using absolut path")
                        else:
                            messages.append(f"Task '{task_name}' is using relative path")

    if messages:
        return '\n'.join(messages)
    else:
        return f" Task '{task_name}' has not missing dependencies."
