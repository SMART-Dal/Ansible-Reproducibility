# Todo check the debug and assert or when just one time -- outside the for loops.
# Todo add 'register', 'ignore-errors', 'failed-when', 'skip-task:true' as bad practices -- separate funtion.


# checks if a task uses one of the supported package installers
# and returns a message indicating which installer was used
def check_task_for_package_installer(task):
    package_installers_to_check = ['apt', 'apt-get', 'yum', 'dnf', 'pacman', 'apk', 'pip']
    messages = []

    for t in task:
        for installer in package_installers_to_check:
            if installer in t:
                messages.append(f"Task uses the {installer} package installer.")

    if messages:
        return '\n'.join(messages)
    else:
        return "None"


# checks if a task uses one of the supported package installers
# and returns a message indicating which installer was used
def check_task_for_broken_dependency(task):
    package_installers_keys_to_check = ['apt-key', 'apt-get-key', 'yum-key', 'dnf-key', 'pacman-key', 'apk-key',
                                        'ansible.builtin.rpm-key']
    checkers = [('fingerprint', "Task uses fixed fingerprint which can get outdated."),
                ('id', "Task uses fixed id which can get outdated or not correct across platfroms."),
                ('url', "Task uses fixed url to download key which can get outdated or removed.")]
    messages = []

    for t in task:
        for installer_key in package_installers_keys_to_check:
            if installer_key in t:
                for checker, message in checkers:
                    if checker in task[t]:
                        messages.append(message)
        if 'package_facts' not in t or 'debug' not in t or 'when' not in t:
            messages.append('Task did not checked the correctness of execution.')
    if messages:
        return '\n'.join(messages)
    else:
        return "None"


# checks if a task installs or updates packages and returns a message indicating
# whether the task installs the latest packages, updates packages, or installs specific packages.
def check_task_for_outdated_package(task):
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
    for t in task:
        for installer in package_installers_to_check:
            if installer['name'] in t:
                if installer['latest_state'] and 'state' in task[t] and task[t]['state'] == installer['latest_state'] or 'update_cache' in task[t]:
                    messages.append(f"Task uses {installer['name']} to install the latest packages.")
                else:
                    messages.append(f"The package installed could get outdated because the script does not update")

    if messages:
        return '\n'.join(messages)
    else:
        return "None"


# checks if a task violates idempotency by executing a command,
# installing or upgrading packages, or updating the package cache.
def check_task_for_idempotency(task):
    messages = []
    idempotency_violations = [
        ('command', "Task violates idempotency because it executes a command."),
        ('shell', "Task violates idempotency because it executes a command."),
        ('service', "Task violates idempotency because it executes a command."),
        ('systemd', "Task violates idempotency because it executes a command.")
        ('raw', "Task violates idempotency because it executes a command."),
        ('script', "Task violates idempotency because it executes a command."),
        ('win_command', "Task violates idempotency because it executes a command."),
        ('win_shell', "Task violates idempotency because it executes a command."),
        ('apt', "Task violates idempotency because it installs or upgrades packages with apt."),
        ('yum', "Task violates idempotency because it installs or upgrades packages with yum."),
        ('dnf', "Task violates idempotency because it installs packages with dnf."),
        ('pacman', "Task violates idempotency because it installs packages with pacman.")
    ]

    for t in task:
        for component, message in idempotency_violations:
            if component in t:
                if component == 'command' or component == 'shell' or component == 'service' or component == 'systemd' or component == 'raw' or component == 'script' or component == 'win_command' or component == 'win_shell':
                    if 'state' not in task[t] or 'when' not in task[t]:
                        messages.append(message)
                elif 'state' not in task[t] or 'when' not in task[t] and task[t]['state'] == 'latest':
                    messages.append(message)
                elif 'upgrade' in task[t] or 'update_cache' in task[t] or 'check_update' in task[t]:
                    messages.append(message)

        if 'ansible.posix.firewalld' in t or 'community.general.ufw' in t:
            if 'state' not in task[t]:
                messages.append(f"Task change the state of firewall without checking.")

        if 'file' in t or 'ansible.builtin.copy' in t or 'copy' in t or 'lineinfile' in t:
            if 'state' not in task[t] or 'when' not in task[t]:
                messages.append(f"Task change the state of file without checking.")

    if messages:
        return '\n'.join(messages)
    else:
        return "None"


# checks if a task installs a version-specific package
def check_task_for_version_specific_package(task):
    messages = []
    package_managers = [
        {'name': 'apt', 'version_key': 'version'},
        {'name': 'yum', 'version_key': 'version'},
        {'name': 'dnf', 'version_key': 'version'},
        {'name': 'pacman', 'version_key': 'version'},
        {'name': 'apk', 'version_key': 'version'},
        {'name': 'pip', 'version_key': 'version'}
    ]

    for t in task:
        for pm in package_managers:
            if pm['name'] in t:
                if pm['version_key'] in task[t]:
                    messages.append(f"Task uses {pm['name']} to install a specific version of a package.")

    if messages:
        return '\n'.join(messages)
    else:
        return "None"


# checks if a task uses the hardware specific commands
def check_task_for_hardware_specific_commands(task):
    messages = []

    hardware_commands = ['lspci', 'lshw', 'lsblk', 'fdisk', 'parted', 'ip', 'ifconfig', 'route', 'fwupd', 'smbios-util',
                         'mdadm', 'megacli', 'vconfig', 'tpmtool', 'efibootmgr', 'cpufrequtils', 'sysctl', 'powertop',
                         'acpi', 'ifup', 'ifdown', 'iptables', 'mkfs', 'nvidia-settings', 'nvidia-smi', 'sg3_utils',
                         'multipath',
                         'mpstat', 'xinput', 'smbus-tools', 'lm-sensors']

    for t in task:
        for component in ['command', 'shell', 'raw']:
            if component in t and any(hc in task[t] for hc in hardware_commands):

                if any(hc in task[t] for hc in ['lspci', 'lshw']):
                    messages.append(f"Task uses a hardware-specific command that may not be portable.")

                elif any(hc in task[t] for hc in ['lsblk', 'fdisk', 'parted', 'mkfs', 'sg3_utils', 'multipath']):
                    messages.append(f"Task uses a disk management command that may not be portable.")

                elif any(hc in task[t] for hc in ['ip', 'ifconfig', 'route', 'vconfig', 'ifup', 'ifdown', 'iptables']):
                    messages.append(f"Task uses a network management command that may not be portable.")

                elif any(hc in task[t] for hc in ['fwupd', 'smbios-util']):
                    messages.append(
                        f"Task uses a BIOS firmware management command that may not be portable.")

                elif any(hc in task[t] for hc in ['mdadm', 'megacli']):
                    messages.append(
                        f"Task uses a RAID arrays management command that may not be portable.")

                elif any(hc in task[t] for hc in ['tpmtool', 'efibootmgr']):
                    messages.append(f"Task uses a security management command that may not be portable.")

                elif any(hc in task[t] for hc in ['cpufrequtils', 'sysctl']):
                    messages.append(
                        f"Task uses a performance settings management command that may not be portable.")

                elif any(hc in task[t] for hc in ['nvidia-settings', 'nvidia-smi']):
                    messages.append(
                        f"Task uses a GPU settings management command that may not be portable.")

                elif any(hc in task[t] for hc in ['xinput', 'xrandr']):
                    messages.append(
                        f"Task uses a I/O device management command that may not be portable.")

                elif any(hc in task[t] for hc in ['smbus-tools', 'lm-sensors']):
                    messages.append(
                        f"Task uses a system management bus command that may not be portable.")

    if messages:
        return '\n'.join(messages)
    else:
        return "None"


# checks if a task uses the software specific commands
# Todo add other executers -- idempotency
def check_task_for_software_specific_commands(task):
    software_commands = ['npm', 'pip', 'docker', 'kubectl']
    messages = []

    for t in task:
        if 'command' in t or 'shell' in t or 'raw' in t:
            for command in software_commands:
                if command in task[t]:
                    messages.append(f"Task uses a {command} command that may not be portable.")
                    break

    if messages:
        return '\n'.join(messages)
    else:
        return "None"


# checks if a task has any assumption on environment like the OS or distribution
def check_task_for_environment_assumptions(task):
    messages = []

    key_download_components = ['apt-repository', 'get-url', 'uri', 'apt-key', 'rpm-key']
    for t in task:
        if 'vars' in t or 'include_vars' in t or 'include_tasks' in t or 'when' in t:
            if 'ansible_distribution' in str(task[t]):
                messages.append(
                    f"Task assumes a default running environment.")
            if 'ansible_os_family' in str(task[t]):
                messages.append(
                    f"Task assumes the operating system family.")

        if 'ansible.posix.firewalld' in t or 'community.general.ufw' in t:
            if 'state' not in task[t]:
                messages.append(f"Task assumes the firewall and change the state without checking.")

        if 'resolv.conf' in t:
            if 'state' not in task[t]:
                messages.append(
                    f"Task assumes that the system is using a resolv.conf file to manage DNS settings")

        if 'resolv.conf' in t:
            if 'state' not in task[t]:
                messages.append(
                    f"Task assumes that the system is using a resolv.conf file to manage DNS settings.")

        if 'ethernets' in t:
            if 'state' not in task[t]:
                messages.append(f"Task changes ethenet interfaces settimgs without checking the state.")

        if 'ntp' in t:
            if 'state' not in task[t]:
                messages.append(
                    f"Task the system is using the ntp service to manage time settings and that the provided NTP servers.")

        if 'sshd_config' in t:
            if 'state' not in task[t]:
                messages.append(
                    f"Task assumes that the system is using a ssh without checking the state.")
        
        if 'assert' not in t or 'debug' not in t:
            messages.append('Task did not checked the final execution of the task.')

        for key_checker in key_download_components:
            if key_checker in t:
                if 'url' in task[t]:
                    messages.append(
                        f"Task assumes that the package repository is available at a specific URL structure.")
    if messages:
        return '\n'.join(messages)
    else:
        return "None"


# checks if a task has missing dependencies
def check_task_for_missing_dependencies(task):
    messages = []

    for t in task:
        if 'name' in t:
            if 'msg' in t:
                if 'dependencies are missing' in t['msg']:
                    messages.append(f"Task has missing dependencies: {t['msg']}")

            elif 'failed' in t:
                if 'Dependency not found' in t['msg']:
                    messages.append(f"Task has missing dependencies: {t['msg']}")

            elif 'failed_when' in t:
                if 'Dependency not found' in t['msg']:
                    messages.append(f"Task has missing dependencies: {t['msg']}")

            elif 'file' in t or 'ansible.builtin.copy' in t:
                if 'dest' in task[t] or 'path' in task[t] or 'src' in task[t]:
                    path_list = [('dest', task[t]['dest']), ('src', task[t]['src']), ('path', task[t]['path'])]
                    for comp, path in path_list:
                        from pathlib import Path
                        if Path(str(path)).is_absolute():
                            messages.append(f"Task is using absolut path")
                        else:
                            messages.append(f"Task is using relative path")

    if messages:
        return '\n'.join(messages)
    else:
        return "None"
