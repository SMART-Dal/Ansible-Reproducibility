import requests


# Search for Ansible scripts on GitHub using the GitHub API
# url = f"https://github.com/oracle/oci-ansible-collection/tree/master/samples"
# url2 = 'https://galaxy.ansible.com/search?deprecated=false&tags=system&keywords=&order_by=-relevance'
# url3 = 'https://galaxy.ansible.com/search?deprecated=false&tags=networking&keywords=&order_by=-relevance'
# url4 = 'https://galaxy.ansible.com/search?deprecated=false&tags=cloud&keywords=&order_by=-relevance'
# url5 = 'https://galaxy.ansible.com/search?deprecated=false&tags=database&keywords=&order_by=-relevance'
# url6 = 'https://galaxy.ansible.com/search?deprecated=false&tags=monitoring&keywords=&order_by=-relevance'
# url7 = 'https://galaxy.ansible.com/search?deprecated=false&tags=security&keywords=&order_by=-relevance'
# url8 = 'https://galaxy.ansible.com/search?deprecated=false&tags=web&keywords=&order_by=-relevance'

import os
import shutil
import subprocess


def clone_directory(url, directory_path):
    # Clone the GitHub repository
    subprocess.run(['git', 'clone', url])

    # Get the repository name
    repo_name = url.split('/')[-1].split('.')[0]

    # Move the directories to the desired project location
    source_path = os.path.join(repo_name, directory_path)
    destination_path = os.path.join('/home/ghazal/Ansible-Reproducibility/test/testScripts', directory_path)
    shutil.move(source_path, destination_path)

    # Remove the cloned repository
    shutil.rmtree(repo_name)


# Provide the GitHub repository URL and directory path
github_url = 'https://github.com/oracle/oci-ansible-collection.git'
directory_path = 'samples'

# Call the function to clone and save the directory
clone_directory(github_url, directory_path)
