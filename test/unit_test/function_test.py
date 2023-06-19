import unittest
import src.smell_detection as detector


class TaskDependencyTestCase(unittest.TestCase):
    def test_fingerprint_dependency(self):
        task = {'apt-key': {'fingerprint': 'ABC123'}}
        result = detector.check_task_for_broken_dependency(task)
        self.assertEqual(result,
                         'Task uses fixed fingerprint which can get outdated.\nTask did not checked the correctness of execution.')

    def test_id_dependency(self):
        task = {'yum-key': {'id': 'KEY123'}}
        result = detector.check_task_for_broken_dependency(task)
        self.assertEqual(result,
                         'Task uses fixed id which can get outdated or not correct across platfroms.\nTask did not checked the correctness of execution.')

    def test_url_dependency(self):
        task = {'ansible.builtin.rpm-key': {'url': 'https://example.com/key.rpm'}}
        result = detector.check_task_for_broken_dependency(task)
        self.assertEqual(result,
                         'Task uses fixed url to download key which can get outdated or removed.\nTask did not checked the correctness of execution.')

    def test_missing_dependency_check(self):
        task = {'apt-get-key': {'fingerprint': 'DEF456'}}
        result = detector.check_task_for_broken_dependency(task)
        self.assertEqual(result,
                         'Task uses fixed fingerprint which can get outdated.\nTask did not checked the correctness of execution.')

    def test_multiple_conditions(self):
        task = {
            'apt-key': {'fingerprint': 'ABC123'},
            'package_facts': {},
            'debug': {},
            'when': {}
        }
        result = detector.check_task_for_broken_dependency(task)
        expected_result = "Task uses fixed fingerprint which can get outdated.\nTask did not checked the correctness of execution.\nTask did not checked the correctness of execution.\nTask did not checked the correctness of execution.\nTask did not checked the correctness of execution."
        self.assertEqual(result, expected_result)

    def test_no_broken_dependency(self):
        task = {'ansible.builtin.dnf-key': {'url': 'https://example.com/key.rpm'},
                'package_facts': {},
                'debug': {},
                'when': {}}
        result = detector.check_task_for_broken_dependency(task)
        expected_result = 'Task uses fixed url to download key which can get outdated or removed.\nTask uses fixed url to download key which can get outdated or removed.\nTask did not checked the correctness of execution.\nTask did not checked the correctness of execution.\nTask did not checked the correctness of execution.\nTask did not checked the correctness of execution.'
        self.assertEqual(result, expected_result)


class TaskPackageTestCase(unittest.TestCase):
    def test_latest_state(self):
        task = {'apt': {'state': 'latest'}}
        result = detector.check_task_for_outdated_package(task)
        self.assertEqual(result, 'Task uses apt to install the latest packages.')

    def test_update_cache(self):
        task = {'yum': {'update_cache': 'yes'}}
        result = detector.check_task_for_outdated_package(task)
        self.assertEqual(result, 'Task uses yum to install the latest packages.')

    def test_no_update(self):
        task = {'dnf': {'state': 'installed'}}
        result = detector.check_task_for_outdated_package(task)
        self.assertEqual(result, 'The package installed could get outdated because the script does not update')

    def test_multiple_packages(self):
        task = {
            'apt': {'state': 'latest'},
            'yum': {'update_cache': 'yes'},
            'pip': {'state': 'latest'},
            'dnf': {'state': 'installed'},
            'package_facts': {},
            'debug': {},
            'when': {}
        }
        result = detector.check_task_for_outdated_package(task)
        expected_result = "Task uses apt to install the latest packages.\n" \
                          "Task uses yum to install the latest packages.\n" \
                          "Task uses pip to install the latest packages.\n" \
                          "The package installed could get outdated because the script does not update"
        self.assertEqual(result, expected_result)

    def test_no_outdated_package(self):
        task = {'apk': {'state': 'latest'},
                'package_facts': {},
                'debug': {},
                'when': {}}
        result = detector.check_task_for_outdated_package(task)
        self.assertEqual(result, 'Task uses apk to install the latest packages.')


class TaskIdempotencyTestCase(unittest.TestCase):
    def test_command(self):
        task = {'command': {'cmd': 'echo Hello'}}
        result = detector.check_task_for_idempotency(task)
        self.assertEqual(result, 'Task violates idempotency because it executes a command.')

    def test_shell(self):
        task = {'shell': {'cmd': 'ls'}}
        result = detector.check_task_for_idempotency(task)
        self.assertEqual(result, 'Task violates idempotency because it executes a command.')

    def test_service(self):
        task = {'service': {'name': 'nginx'}}
        result = detector.check_task_for_idempotency(task)
        self.assertEqual(result, 'Task violates idempotency because it executes a command.')

    def test_systemd(self):
        task = {'systemd': {'name': 'nginx'}}
        result = detector.check_task_for_idempotency(task)
        self.assertEqual(result, 'Task violates idempotency because it executes a command.')

    def test_raw(self):
        task = {'raw': {'cmd': 'ls'}}
        result = detector.check_task_for_idempotency(task)
        self.assertEqual(result, 'Task violates idempotency because it executes a command.')

    def test_script(self):
        task = {'script': {'src': 'script.sh'}}
        result = detector.check_task_for_idempotency(task)
        self.assertEqual(result, 'Task violates idempotency because it executes a command.')

    def test_win_command(self):
        task = {'win_command': {'cmd': 'echo Hello'}}
        result = detector.check_task_for_idempotency(task)
        self.assertEqual(result, 'Task violates idempotency because it executes a command.\nTask violates idempotency because it executes a command.')

    def test_win_shell(self):
        task = {'win_shell': {'cmd': 'dir'}}
        result = detector.check_task_for_idempotency(task)
        self.assertEqual(result, 'Task violates idempotency because it executes a command.\nTask violates idempotency because it executes a command.')

    def test_apt(self):
        task = {'apt': {'name': 'package'}}
        result = detector.check_task_for_idempotency(task)
        self.assertEqual(result, 'Task violates idempotency because it installs or upgrades packages with apt.')

    def test_yum(self):
        task = {'yum': {'name': 'package'}}
        result = detector.check_task_for_idempotency(task)
        self.assertEqual(result, 'Task violates idempotency because it installs or upgrades packages with yum.')

    def test_dnf(self):
        task = {'dnf': {'name': 'package'}}
        result = detector.check_task_for_idempotency(task)
        self.assertEqual(result, 'Task violates idempotency because it installs packages with dnf.')

    def test_pacman(self):
        task = {'pacman': {'name': 'package'}}
        result = detector.check_task_for_idempotency(task)
        self.assertEqual(result, 'Task violates idempotency because it installs packages with pacman.')

    def test_pip(self):
        task = {'pip': {'name': 'package'}}
        result = detector.check_task_for_idempotency(task)
        self.assertEqual(result, 'Task violates idempotency because it installs packages with pip.')

    def test_apt_get(self):
        task = {'apt-get': {'name': 'package'}}
        result = detector.check_task_for_idempotency(task)
        self.assertEqual(result, 'Task violates idempotency because it installs or upgrades packages with apt.\nTask violates idempotency because it installs packages with apt-get.')

    def test_firewall_no_state(self):
        task = {'ansible.posix.firewalld': {'some_key': 'some_value'}}
        result = detector.check_task_for_idempotency(task)
        self.assertEqual(result, 'Task change the state of firewall without checking.')

    def test_firewall_with_state(self):
        task = {'ansible.posix.firewalld': {'state': 'enabled'}}
        result = detector.check_task_for_idempotency(task)
        self.assertEqual(result, 'None')

    def test_ufw_no_state(self):
        task = {'community.general.ufw': {'some_key': 'some_value'}}
        result = detector.check_task_for_idempotency(task)
        self.assertEqual(result, 'Task change the state of firewall without checking.')

    def test_ufw_with_state(self):
        task = {'community.general.ufw': {'state': 'enabled'}}
        result = detector.check_task_for_idempotency(task)
        self.assertEqual(result, 'None')

    def test_file_no_state(self):
        task = {'file': {'path': '/path/to/file'}}
        result = detector.check_task_for_idempotency(task)
        self.assertEqual(result, 'Task change the state of file without checking.')

    def test_file_with_state(self):
        task = {'file': {'path': '/path/to/file', 'state': 'file'}}
        result = detector.check_task_for_idempotency(task)
        self.assertEqual(result, 'None')

    def test_copy_no_state(self):
        task = {'ansible.builtin.copy': {'src': 'file.txt', 'dest': '/path/to/file'}}
        result = detector.check_task_for_idempotency(task)
        self.assertEqual(result, 'Task change the state of file without checking.')

    def test_copy_with_state(self):
        task = {'ansible.builtin.copy': {'src': 'file.txt', 'dest': '/path/to/file', 'state': 'file'}}
        result = detector.check_task_for_idempotency(task)
        self.assertEqual(result, 'None')

    def test_lineinfile_no_state(self):
        task = {'lineinfile': {'path': '/path/to/file', 'line': 'some_line'}}
        result = detector.check_task_for_idempotency(task)
        self.assertEqual(result, 'Task change the state of file without checking.')

    def test_lineinfile_with_state(self):
        task = {'lineinfile': {'path': '/path/to/file', 'line': 'some_line', 'state': 'present'}}
        result = detector.check_task_for_idempotency(task)
        self.assertEqual(result, 'None')


class TaskVersionSpecificPackageTestCase(unittest.TestCase):
    def test_apt_with_version(self):
        task = {'apt': {'name': 'package', 'version': '1.0'}}
        result = detector.check_task_for_version_specific_package(task)
        self.assertEqual(result, 'Task uses apt to install a specific version of a package.')

    def test_yum_with_version(self):
        task = {'yum': {'name': 'package', 'version': '2.0'}}
        result = detector.check_task_for_version_specific_package(task)
        self.assertEqual(result, 'Task uses yum to install a specific version of a package.')

    def test_dnf_with_version(self):
        task = {'dnf': {'name': 'package', 'version': '3.0'}}
        result = detector.check_task_for_version_specific_package(task)
        self.assertEqual(result, 'Task uses dnf to install a specific version of a package.')

    def test_pacman_with_version(self):
        task = {'pacman': {'name': 'package', 'version': '4.0'}}
        result = detector.check_task_for_version_specific_package(task)
        self.assertEqual(result, 'Task uses pacman to install a specific version of a package.')

    def test_apk_with_version(self):
        task = {'apk': {'name': 'package', 'version': '5.0'}}
        result = detector.check_task_for_version_specific_package(task)
        self.assertEqual(result, 'Task uses apk to install a specific version of a package.')

    def test_pip_with_version(self):
        task = {'pip': {'name': 'package', 'version': '6.0'}}
        result = detector.check_task_for_version_specific_package(task)
        self.assertEqual(result, 'Task uses pip to install a specific version of a package.')

    def test_no_version(self):
        task = {'apt': {'name': 'package'}}
        result = detector.check_task_for_version_specific_package(task)
        self.assertEqual(result, 'None')


class TaskHardwareSpecificCommandsTestCase(unittest.TestCase):
    def test_hardware_specific_command_lspci(self):
        task = {'command': 'lspci -nn'}
        result = detector.check_task_for_hardware_specific_commands(task)
        self.assertEqual(result, 'Task uses a hardware-specific command that may not be portable.')

    def test_hardware_specific_command_lsblk(self):
        task = {'shell': 'lsblk'}
        result = detector.check_task_for_hardware_specific_commands(task)
        self.assertEqual(result, 'Task uses a disk management command that may not be portable.')

    def test_hardware_specific_command_ip(self):
        task = {'raw': 'ip link show'}
        result = detector.check_task_for_hardware_specific_commands(task)
        self.assertEqual(result, 'Task uses a network management command that may not be portable.')

    def test_hardware_specific_command_fwupd(self):
        task = {'shell': 'fwupd'}
        result = detector.check_task_for_hardware_specific_commands(task)
        self.assertEqual(result, 'Task uses a BIOS firmware management command that may not be portable.')

    def test_hardware_specific_command_mdadm(self):
        task = {'command': 'mdadm --create'}
        result = detector.check_task_for_hardware_specific_commands(task)
        self.assertEqual(result, 'Task uses a RAID arrays management command that may not be portable.')

    def test_hardware_specific_command_tpmtool(self):
        task = {'raw': 'tpmtool getcap'}
        result = detector.check_task_for_hardware_specific_commands(task)
        self.assertEqual(result, 'Task uses a security management command that may not be portable.')

    def test_hardware_specific_command_cpufrequtils(self):
        task = {'shell': 'cpufrequtils'}
        result = detector.check_task_for_hardware_specific_commands(task)
        self.assertEqual(result, 'Task uses a performance settings management command that may not be portable.')

    def test_hardware_specific_command_nvidia_settings(self):
        task = {'command': 'nvidia-settings'}
        result = detector.check_task_for_hardware_specific_commands(task)
        self.assertEqual(result, 'Task uses a GPU settings management command that may not be portable.')

    def test_hardware_specific_command_xinput(self):
        task = {'command': 'xinput list'}
        result = detector.check_task_for_hardware_specific_commands(task)
        self.assertEqual(result, 'Task uses a I/O device management command that may not be portable.')

    def test_hardware_specific_command_smbus_tools(self):
        task = {'shell': 'smbus-tools'}
        result = detector.check_task_for_hardware_specific_commands(task)
        self.assertEqual(result, 'Task uses a system management bus command that may not be portable.')

    def test_no_hardware_specific_command(self):
        task = {'command': 'echo "Hello, World!"'}
        result = detector.check_task_for_hardware_specific_commands(task)
        self.assertEqual(result, 'None')


class TaskSoftwareSpecificCommandsTestCase(unittest.TestCase):
    def test_software_specific_command_npm(self):
        task = {'command': 'npm install'}
        result = detector.check_task_for_software_specific_commands(task)
        self.assertEqual(result, 'Task uses a npm command that may not be portable.')

    def test_software_specific_command_pip(self):
        task = {'shell': 'pip install'}
        result = detector.check_task_for_software_specific_commands(task)
        self.assertEqual(result, 'Task uses a pip command that may not be portable.')

    def test_software_specific_command_docker(self):
        task = {'raw': 'docker run'}
        result = detector.check_task_for_software_specific_commands(task)
        self.assertEqual(result, 'Task uses a docker command that may not be portable.')

    def test_software_specific_command_kubectl(self):
        task = {'command': 'kubectl apply'}
        result = detector.check_task_for_software_specific_commands(task)
        self.assertEqual(result, 'Task uses a kubectl command that may not be portable.')

    def test_no_software_specific_command(self):
        task = {'command': 'echo "Hello, World!"'}
        result = detector.check_task_for_software_specific_commands(task)
        self.assertEqual(result, 'None')


class TaskEnvironmentAssumptionsTestCase(unittest.TestCase):
    def test_default_running_environment_assumption(self):
        task = {'vars': {'ansible_distribution': 'Ubuntu'}}
        result = detector.check_task_for_environment_assumptions(task)
        self.assertEqual(result, 'Task assumes a default running environment.\nTask did not checked the final execution of the task.')

    def test_operating_system_family_assumption(self):
        task = {'include_vars': 'vars.yml'}
        result = detector.check_task_for_environment_assumptions(task)
        self.assertEqual(result, 'Task did not checked the final execution of the task.')

    def test_firewall_state_assumption(self):
        task = {'ansible.posix.firewalld': {'option': 'enable'}}
        result = detector.check_task_for_environment_assumptions(task)
        self.assertEqual(result, 'Task assumes the firewall and change the state without checking.\nTask did not checked the final execution of the task.')

    def test_resolv_conf_state_assumption(self):
        task = {'resolv.conf': {'nameservers': ['8.8.8.8']}}
        result = detector.check_task_for_environment_assumptions(task)
        self.assertEqual(result, 'Task assumes that the system is using a resolv.conf file to manage DNS settings.\nTask did not checked the final execution of the task.')

    def test_ethernet_interfaces_state_assumption(self):
        task = {'ethernets': {'eth0': {'address': '192.168.0.100'}}}
        result = detector.check_task_for_environment_assumptions(task)
        self.assertEqual(result, 'Task changes ethernet interfaces settings without checking the state.\nTask did not checked the final execution of the task.')

    def test_ntp_state_assumption(self):
        task = {'ntp': {'servers': ['ntp1.example.com', 'ntp2.example.com']}}
        result = detector.check_task_for_environment_assumptions(task)
        self.assertEqual(result, 'Task the system is using the ntp service to manage time settings and that the provided NTP servers.\nTask did not checked the final execution of the task.')

    def test_sshd_config_state_assumption(self):
        task = {'sshd_config': {'Port': 22}}
        result = detector.check_task_for_environment_assumptions(task)
        self.assertEqual(result, 'Task assumes that the system is using a ssh without checking the state.\nTask did not checked the final execution of the task.')

    def test_final_execution_check_assumption(self):
        task = {'assert': 'result is success'}
        result = detector.check_task_for_environment_assumptions(task)
        self.assertEqual(result, 'Task did not checked the final execution of the task.')

    def test_package_repository_url_structure_assumption(self):
        task = {'apt-repository': {'repo': 'https://example.com/repo'}}
        result = detector.check_task_for_environment_assumptions(task)
        self.assertEqual(result, 'Task did not checked the final execution of the task.\nTask assumes that the package repository is available at a specific URL structure.')

    def test_no_environment_assumption(self):
        task = {'command': 'echo "Hello, World!"'}
        result = detector.check_task_for_environment_assumptions(task)
        self.assertEqual(result, 'Task did not checked the final execution of the task.')


class TaskMissingDependenciesTestCase(unittest.TestCase):
    def test_missing_dependencies_with_msg(self):
        task = {'name': 'Install dependencies', 'msg': 'Some dependencies are missing'}
        result = detector.check_task_for_missing_dependencies(task)
        self.assertEqual(result, 'Task has missing dependencies')

    def test_missing_dependencies_with_failed(self):
        task = {'name': 'Install dependencies', 'failed': True, 'msg': 'dependency not found'}
        result = detector.check_task_for_missing_dependencies(task)
        self.assertEqual(result, 'Task has missing dependencies')

    def test_missing_dependencies_with_failed_when(self):
        task = {'name': 'Install dependencies', 'failed_when': 'dependency not found'}
        result = detector.check_task_for_missing_dependencies(task)
        self.assertEqual(result, 'Task has missing dependencies')

    def test_task_with_absolute_paths(self):
        task = {'file': {'path': '/var/www/html/index.html'}}
        result = detector.check_task_for_missing_dependencies(task)
        self.assertEqual(result, 'Task is using absolut path for source path')

    def test_task_with_relative_paths(self):
        task = {'ansible.builtin.copy': {'src': 'app.py', 'dest': ' /opt/app/app.py'}}
        result = detector.check_task_for_missing_dependencies(task)
        self.assertEqual(result, 'Task is using relative path for source')

    def test_no_missing_dependencies(self):
        task = {'name': 'Install packages', 'command': 'apt install package'}
        result = detector.check_task_for_missing_dependencies(task)
        self.assertEqual(result, 'None')



if __name__ == '__main__':
    unittest.main()
