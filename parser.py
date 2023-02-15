# import pyyaml module
import yaml
from yaml.loader import SafeLoader


# TODO - create an abject from each task
# TODO - add Error handlers --> try except KeyError, continue

# Open the file and load the file

def direct_url_checker(task):
    url_dict = task['get_url']
    url = url_dict['url']
    dst = url_dict['dest']

    msg = ''

    if url_dict:
        if url:
            msg = msg + 'Direct link is used --> execution problem'
        if not dst.startswith('./'):
            msg = msg + 'Using path specific declaration --> Assumption on environment'
    else:
        msg = 'no Url usage'

    return msg


def installer_checker(task):
    installer = task['ansible.builtin.apt_key'] or task['apt'] or task['pip']
    state = installer['state']

    file = installer['file']

    msg = ''

    if installer:
        msg = msg + 'using package managers can cause idempotency'
    if not state:
        msg = msg + 'not using state for a task is an anti-pattern'
    if file:
        msg = msg + 'The downloaded files can be outdated'
    return msg


def idempotency_checker(task):
    shell = task['shell']
    service = task['service']
    state = service['state']
    msg = ''

    if shell:
        msg = msg + 'Using shell can break idempotency'
    if service:
        msg = msg + 'changing state of a service can break idempotency'
    if not state:
        msg = msg + 'not using state for a task is an anti-pattern'

    return msg


def key_checker(task):
    apt_key = task['apt_key']
    url = apt_key['url']
    state = apt_key['state']

    msg = ''

    if apt_key:
        if url:
            msg = msg + 'Direct link is used --> execution problem'
        if not state:
            msg = msg + 'not using state for a task is an anti-pattern'
    else:
        msg = 'no apt-key usage'

    return msg


def get_repository_checker(task):
    apt_repo = task['apt_repository']
    url = apt_repo['repo']
    state = apt_repo['state']

    msg = ''

    if apt_repo:
        if url:
            msg = msg + 'Direct link is used --> execution problem'
        if not state:
            msg = msg + 'not using state for a task is an anti-pattern'
    else:
        msg = 'no apt-repo usage'

    return msg


def stat_checker(task):
    stat = task['stat']
    path = stat['path']

    msg = ''
    if stat:
        if not path.startswith('./'):
            msg = msg + 'Using path specific declaration --> Assumption on environment'
    return msg


with open('install_and_configure.yml') as f:
    # data = yaml.load(f, Loader=SafeLoader)
    data = list(yaml.load_all(f, Loader=SafeLoader))
    tasks = data[0][0]['tasks']

    for task in tasks:
        url_msg = direct_url_checker(task=task)
        apt_pkg_msg = installer_checker(task=task)
        idempotency_msg = idempotency_checker(task=task)
        key_msg = key_checker(task=task)
        repo_msg = get_repository_checker(task=task)
        stat_msg = stat_checker(task=task)